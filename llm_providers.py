"""Helper utilities for external LLM providers."""

from typing import Optional, Tuple
import os
import base64
import time

import requests

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
GEMINI_IMAGE_URL = "https://generativelanguage.googleapis.com/v1beta/images:generate"
OPENAI_CHAT_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_IMAGE_URL = "https://api.openai.com/v1/images/generations"
OPENAI_DEFAULT_MODEL = os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini")
OPENAI_IMAGE_MODEL = os.getenv("OPENAI_IMAGE_MODEL", "dall-e-3")
VEO_BASE_URL = "https://generativelanguage.googleapis.com/v1beta"


def has_gemini_key() -> bool:
    """Return True when a Gemini API key or OAuth access token is available."""
    return bool(os.getenv("GEMINI_API_KEY") or os.getenv("GEMINI_ACCESS_TOKEN"))


def has_openai_key() -> bool:
    """Return True when an OpenAI API key or access token is available."""
    return bool(os.getenv("OPENAI_API_KEY") or os.getenv("OPENAI_ACCESS_TOKEN"))


def _get_gemini_auth():
    """Return headers/params for Gemini auth."""
    token = os.getenv("GEMINI_ACCESS_TOKEN")
    api_key = os.getenv("GEMINI_API_KEY")

    headers = {"Content-Type": "application/json"}
    params = {}

    if token:
        headers["Authorization"] = f"Bearer {token}"
    elif api_key:
        params["key"] = api_key
    else:
        return None, None, "GEMINI_API_KEY or GEMINI_ACCESS_TOKEN not set"

    return headers, params, None


def _get_openai_auth():
    """Return headers for OpenAI auth."""
    token = os.getenv("OPENAI_ACCESS_TOKEN") or os.getenv("OPENAI_API_KEY")
    if not token:
        return None, "OPENAI_API_KEY or OPENAI_ACCESS_TOKEN not set"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    return headers, None


def _parse_priority(env_value: str, defaults):
    parts = [p.strip().lower() for p in env_value.split(",") if p.strip()]
    seen = []
    for p in parts + defaults:
        if p not in seen:
            seen.append(p)
    return seen


def get_script_providers():
    """Return prioritized script providers based on env."""
    default = ["openai", "gemini", "ollama", "template"]
    env_val = os.getenv("PROVIDER_PRIORITY_SCRIPT")
    return _parse_priority(env_val, default) if env_val else default


def get_image_providers():
    """Return prioritized image/video providers based on env."""
    default = ["veo", "openai", "gemini", "pexels", "pixabay", "ffmpeg"]
    env_val = os.getenv("PROVIDER_PRIORITY_IMAGE")
    return _parse_priority(env_val, default) if env_val else default


def generate_video_with_veo(prompt: str, poll_interval: int = 10, max_polls: int = 12, timeout: int = 60):
    """
    Generate a video using Veo 3.1 via Gemini API.

    Returns (video_bytes, download_url, error).
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None, None, "GEMINI_API_KEY not set"

    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": api_key,
    }

    # Start long-running operation
    try:
        resp = requests.post(
            f"{VEO_BASE_URL}/models/veo-3.1-generate-preview:predictLongRunning",
            json={"instances": [{"prompt": prompt}]},
            headers=headers,
            timeout=timeout,
        )
    except Exception as exc:
        return None, None, str(exc)

    if resp.status_code != 200:
        return None, None, f"Veo start failed: {resp.status_code} {resp.text[:200]}"

    operation_name = resp.json().get("name")
    if not operation_name:
        return None, None, "Veo start response missing operation name"

    # Poll
    for _ in range(max_polls):
        try:
            status_resp = requests.get(f"{VEO_BASE_URL}/{operation_name}", headers=headers, timeout=timeout)
        except Exception as exc:
            return None, None, f"Veo poll error: {exc}"

        if status_resp.status_code != 200:
            return None, None, f"Veo poll failed: {status_resp.status_code} {status_resp.text[:200]}"

        data = status_resp.json()
        if data.get("done"):
            try:
                uri = data["response"]["generateVideoResponse"]["generatedSamples"][0]["video"]["uri"]
            except Exception:
                return None, None, "Veo response missing video URI"

            # Download video
            try:
                vid_resp = requests.get(uri, headers=headers, timeout=timeout, allow_redirects=True)
                if vid_resp.status_code != 200:
                    return None, uri, f"Veo download failed: {vid_resp.status_code}"
                return vid_resp.content, uri, None
            except Exception as exc:
                return None, uri, f"Veo download error: {exc}"

        time.sleep(poll_interval)

    return None, None, "Veo operation timed out"


def generate_with_gemini(prompt: str, timeout: int = 60) -> Tuple[Optional[str], Optional[str]]:
    """
    Call Gemini Pro with the given prompt.

    Returns a tuple of (text, error). When successful, text contains the model
    response and error is None. On failure, text is None and error provides a
    short description.
    """
    headers, params, err = _get_gemini_auth()
    if err:
        return None, err

    try:
        resp = requests.post(
            GEMINI_URL,
            json={"contents": [{"parts": [{"text": prompt}]}]},
            headers=headers,
            params=params,
            timeout=timeout,
        )
    except Exception as exc:  # pragma: no cover - network issues
        return None, str(exc)

    if resp.status_code != 200:
        snippet = resp.text[:200] if resp.text else f"HTTP {resp.status_code}"
        return None, f"Status {resp.status_code}: {snippet}"

    try:
        data = resp.json()
    except ValueError:
        snippet = resp.text[:200]
        return None, f"Non-JSON response: {snippet}"

    candidates = data.get("candidates") or []
    if not candidates:
        return None, "No candidates returned from Gemini"

    parts = candidates[0].get("content", {}).get("parts", [])
    text = "".join(part.get("text", "") for part in parts).strip()
    if not text:
        return None, "Empty response from Gemini"

    return text, None


def generate_with_openai(prompt: str, timeout: int = 60) -> Tuple[Optional[str], Optional[str]]:
    """
    Call OpenAI chat completions with the given prompt.

    Returns (text, error).
    """
    headers, err = _get_openai_auth()
    if err:
        return None, err

    body = {
        "model": OPENAI_DEFAULT_MODEL,
        "messages": [{"role": "user", "content": prompt}],
    }

    try:
        resp = requests.post(
            OPENAI_CHAT_URL,
            json=body,
            headers=headers,
            timeout=timeout,
        )
    except Exception as exc:  # pragma: no cover
        return None, str(exc)

    if resp.status_code != 200:
        snippet = resp.text[:200] if resp.text else f"HTTP {resp.status_code}"
        return None, f"Status {resp.status_code}: {snippet}"

    try:
        data = resp.json()
    except ValueError:
        snippet = resp.text[:200]
        return None, f"Non-JSON response: {snippet}"

    choices = data.get("choices") or []
    if not choices:
        return None, "No choices returned from OpenAI"

    message = choices[0].get("message", {})
    text = (message.get("content") or "").strip()
    if not text:
        return None, "Empty response from OpenAI"

    return text, None


def generate_image_with_gemini(prompt: str, width: int = 1280, height: int = 720, timeout: int = 60) -> Tuple[Optional[bytes], Optional[str]]:
    """
    Generate an image using Gemini/Imagen.

    Returns (image_bytes, error). Image is raw binary (PNG/JPEG). On failure,
    image_bytes is None and error contains a short reason.
    """
    headers, params, err = _get_gemini_auth()
    if err:
        return None, err

    payload = {
        "model": "imagegeneration",
        "prompt": {"text": prompt},
        "parameters": {
            "sampleCount": 1,
            "imageWidth": width,
            "imageHeight": height,
        },
    }

    try:
        resp = requests.post(
            GEMINI_IMAGE_URL,
            json=payload,
            headers=headers,
            params=params,
            timeout=timeout,
        )
    except Exception as exc:  # pragma: no cover - network issues
        return None, str(exc)

    if resp.status_code != 200:
        snippet = resp.text[:200] if resp.text else f"HTTP {resp.status_code}"
        return None, f"Status {resp.status_code}: {snippet}"

    try:
        data = resp.json()
    except ValueError:
        snippet = resp.text[:200]
        return None, f"Non-JSON response: {snippet}"

    images = data.get("images") or []
    if not images:
        return None, "No images returned from Gemini"

    first = images[0]
    encoded = first.get("image") or first.get("data")
    if not encoded:
        return None, "Image payload missing in Gemini response"

    try:
        return base64.b64decode(encoded), None
    except Exception:
        return None, "Failed to decode Gemini image data"


def generate_image_with_openai(prompt: str, width: int = 1280, height: int = 720, timeout: int = 60) -> Tuple[Optional[bytes], Optional[str]]:
    """
    Generate an image using OpenAI DALL-E.

    Returns (image_bytes, error).
    """
    headers, err = _get_openai_auth()
    if err:
        return None, err

    # Pick the closest supported size for DALL-E 3
    size = "1792x1024" if width >= height else "1024x1792"

    body = {
        "prompt": prompt,
        "model": OPENAI_IMAGE_MODEL,
        "n": 1,
        "size": size,
        "response_format": "b64_json",
    }

    try:
        resp = requests.post(
            OPENAI_IMAGE_URL,
            json=body,
            headers=headers,
            timeout=timeout,
        )
    except Exception as exc:  # pragma: no cover
        return None, str(exc)

    if resp.status_code != 200:
        snippet = resp.text[:200] if resp.text else f"HTTP {resp.status_code}"
        return None, f"Status {resp.status_code}: {snippet}"

    try:
        data = resp.json()
    except ValueError:
        snippet = resp.text[:200]
        return None, f"Non-JSON response: {snippet}"

    results = data.get("data") or []
    if not results:
        return None, "No images returned from OpenAI"

    encoded = results[0].get("b64_json")
    if not encoded:
        return None, "Image payload missing in OpenAI response"

    try:
        return base64.b64decode(encoded), None
    except Exception:
        return None, "Failed to decode OpenAI image data"
