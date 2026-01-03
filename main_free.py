#!/usr/bin/env python3
"""
FREE YouTube Video Generator - 100% Free, No API Keys!
Uses: Pexels videos + Google TTS + Ollama (optional)
"""

import os, sys, json, time, random, subprocess, urllib.parse
from pathlib import Path
from datetime import datetime
import requests
from typing import List, Dict, Optional
from gtts import gTTS
from llm_providers import (
    generate_with_gemini,
    has_gemini_key,
    generate_image_with_gemini,
    generate_with_openai,
    has_openai_key,
    generate_image_with_openai,
    get_script_providers,
    get_image_providers,
    generate_video_with_veo,
)

class FreeYouTubeGenerator:
    def __init__(self):
        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)
        self.pexels_key = os.getenv('PEXELS_API_KEY', '')
        self.script_provider = "template"
        self.video_sources: List[str] = []
        
    def generate_script(self, topic: str, duration: int = 60) -> Dict:
        """Generate script with Ollama or template"""
        print(f"🎬 Generating script for: {topic}")

        prompt = (
            f"Write a {duration}-second YouTube script about \"{topic}\" with a hook, "
            "3 concise sections, and a closing call to action. Put each part on its "
            "own line and include simple visual suggestions."
        )

        for provider in get_script_providers():
            if provider == "openai":
                text, err = generate_with_openai(prompt)
                if text:
                    print("✅ Script from OpenAI")
                    self.script_provider = "openai"
                    return self._parse_script(text, topic, duration)
                if has_openai_key() and err:
                    print(f"⚠️  OpenAI request failed: {err[:180]}")

            elif provider == "gemini":
                text, err = generate_with_gemini(prompt)
                if text:
                    print("✅ Script from Gemini Pro")
                    self.script_provider = "gemini"
                    return self._parse_script(text, topic, duration)
                if has_gemini_key() and err:
                    print(f"⚠️  Gemini Pro request failed: {err[:180]}")

            elif provider == "ollama":
                try:
                    r = requests.post('http://localhost:11434/api/generate',
                        json={"model": "llama2", "prompt": prompt, "stream": False},
                        timeout=30)
                    if r.status_code == 200:
                        text = r.json()['response']
                        print("✅ Script from Ollama")
                        self.script_provider = "ollama"
                        return self._parse_script(text, topic, duration)
                except Exception as e:
                    print(f"⚠️  Ollama error: {e}")

            elif provider == "template":
                script = f"""Hook: {topic} - Let me show you why this matters!

Point 1: {topic} is important because it affects us daily.
Point 2: Understanding {topic} can help you make better decisions.
Point 3: The future of {topic} looks promising.

CTA: Like and subscribe for more content like this!"""
                self.script_provider = "template"
                return self._parse_script(script, topic, duration)

        # Absolute fallback
        script = f"Hook: {topic}\nPoint 1: {topic}\nPoint 2: {topic}\nPoint 3: {topic}\nCTA: Subscribe!"
        self.script_provider = "template"
        return self._parse_script(script, topic, duration)
    
    def _parse_script(self, text: str, topic: str, duration: int) -> Dict:
        lines = [l.strip() for l in text.split('\n') if l.strip()]
        sec_dur = duration // 3
        
        sections = []
        for i in range(3):
            sections.append({
                "time": f"{i*sec_dur}-{(i+1)*sec_dur}s",
                "narration": lines[i] if i < len(lines) else topic,
                "visuals": topic
            })
        
        return {
            "title": f"{topic} - Explained",
            "hook": lines[0] if lines else topic,
            "sections": sections,
            "cta": "Thanks for watching!",
            "keywords": [topic]
        }
    
    def generate_voiceover(self, text: str, output: Path) -> Path:
        """FREE voiceover with Google TTS"""
        print(f"🎙️ Generating FREE voiceover...")
        tts = gTTS(text=text[:5000], lang='en', slow=False)
        tts.save(str(output))
        print(f"✅ Voiceover: {output}")
        return output

    def _image_to_video(self, image_bytes: bytes, output: Path, duration: int = 10) -> Path:
        """Convert a single image to an MP4 clip."""
        image_path = output.with_suffix(".jpg")
        with open(image_path, 'wb') as f:
            f.write(image_bytes)

        subprocess.run([
            'ffmpeg', '-y', '-loop', '1',
            '-i', str(image_path),
            '-t', str(duration),
            '-vf', 'scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2',
            '-pix_fmt', 'yuv420p',
            str(output)
        ], capture_output=True, check=True)

        return output
    
    def download_video(self, query: str, output: Path) -> Path:
        """Download FREE video from Pexels or create colored bg"""
        print(f"🎥 Getting video: {query[:30]}...")

        for provider in get_image_providers():
            if provider == "openai":
                if has_openai_key():
                    img_bytes, img_error = generate_image_with_openai(query, width=1280, height=720)
                    if img_bytes:
                        try:
                            self._image_to_video(img_bytes, output, duration=10)
                            print(f"✅ OpenAI image → video: {output}")
                            self.video_sources.append("openai-image")
                            return output
                        except Exception as e:
                            print(f"⚠️  OpenAI image-to-video failed: {e}")
                    else:
                        print(f"⚠️  OpenAI image failed: {img_error}")

            elif provider == "gemini":
                if has_gemini_key():
                    img_bytes, img_error = generate_image_with_gemini(query, width=1280, height=720)
                    if img_bytes:
                        try:
                            self._image_to_video(img_bytes, output, duration=10)
                            print(f"✅ Gemini image → video: {output}")
                            self.video_sources.append("gemini-image")
                            return output
                        except Exception as e:
                            print(f"⚠️  Gemini image-to-video failed: {e}")
                    else:
                        print(f"⚠️  Gemini image failed: {img_error}")

            elif provider == "veo":
                vid_bytes, uri, err = generate_video_with_veo(query, poll_interval=10, max_polls=18, timeout=60)
                if vid_bytes:
                    with open(output, 'wb') as f:
                        f.write(vid_bytes)
                    self.video_sources.append("veo-3.1")
                    print(f"✅ Veo video downloaded from {uri}")
                    return output
                if err:
                    print(f"⚠️  Veo video failed: {err}")

            elif provider == "pexels":
                if self.pexels_key:
                    try:
                        r = requests.get(
                            f"https://api.pexels.com/videos/search?query={urllib.parse.quote(query)}&per_page=1",
                            headers={'Authorization': self.pexels_key},
                            timeout=10
                        )
                        if r.status_code == 200 and r.json().get('videos'):
                            vfiles = r.json()['videos'][0]['video_files']
                            vid_url = next((v['link'] for v in vfiles if v.get('width', 0) >= 1280), vfiles[0]['link'])
                            
                            vdata = requests.get(vid_url, timeout=30).content
                            with open(output, 'wb') as f:
                                f.write(vdata)
                            print(f"✅ Downloaded: {output}")
                            self.video_sources.append("pexels")
                            return output
                    except Exception as e:
                        print(f"⚠️  Pexels failed: {e}")

            elif provider == "ffmpeg":
                color = random.choice(['blue', 'green', 'purple', 'red', 'orange'])
                subprocess.run([
                    'ffmpeg', '-y', '-f', 'lavfi',
                    '-i', f'color=c={color}:s=1920x1080:d=10',
                    '-vf', f"drawtext=text='{query[:25]}':fontsize=60:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2",
                    '-t', '10', '-pix_fmt', 'yuv420p', str(output)
                ], capture_output=True, check=True)
                print(f"✅ Created background: {output}")
                self.video_sources.append("ffmpeg-color")
                return output

        # If nothing matched, fallback to color
        color = random.choice(['blue', 'green', 'purple', 'red', 'orange'])
        subprocess.run([
            'ffmpeg', '-y', '-f', 'lavfi',
            '-i', f'color=c={color}:s=1920x1080:d=10',
            '-vf', f"drawtext=text='{query[:25]}':fontsize=60:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2",
            '-t', '10', '-pix_fmt', 'yuv420p', str(output)
        ], capture_output=True, check=True)
        print(f"✅ Created background: {output}")
        self.video_sources.append("ffmpeg-color")
        return output
    
    def create_subtitles(self, sections: List[Dict], output: Path) -> Path:
        """Create SRT subtitles"""
        print("📝 Creating subtitles...")
        with open(output, 'w') as f:
            for idx, sec in enumerate(sections, 1):
                times = sec['time'].replace('s', '').split('-')
                start, end = int(times[0]), int(times[1])
                f.write(f"{idx}\n00:00:{start:02d},000 --> 00:00:{end:02d},000\n{sec['narration']}\n\n")
        print(f"✅ Subtitles: {output}")
        return output
    
    def assemble_video(self, videos: List[Path], audio: Path, subs: Optional[Path], output: Path) -> Path:
        """Assemble final video with ffmpeg"""
        print("🎬 Assembling video...")
        
        # Concat videos
        concat_file = output.parent / "concat.txt"
        with open(concat_file, 'w') as f:
            for v in videos:
                f.write(f"file '{v.absolute()}'\n")
        
        temp_vid = output.parent / "temp.mp4"
        subprocess.run([
            'ffmpeg', '-y', '-f', 'concat', '-safe', '0',
            '-i', str(concat_file), '-c', 'copy', str(temp_vid)
        ], capture_output=True, check=True)
        
        # Add audio and optionally subtitles
        cmd = [
            'ffmpeg', '-y',
            '-i', str(temp_vid), '-i', str(audio),
            '-c:v', 'libx264', '-preset', 'fast', '-crf', '23',
            '-c:a', 'aac', '-b:a', '128k', '-shortest',
            '-vf', 'scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2'
        ]
        
        if subs and subs.exists():
            cmd[-1] += f",subtitles={subs}:force_style='FontSize=24,PrimaryColour=&H00FFFFFF'"
        
        cmd.append(str(output))
        subprocess.run(cmd, check=True, capture_output=True)
        
        temp_vid.unlink(missing_ok=True)
        concat_file.unlink(missing_ok=True)
        print(f"✅ Video created: {output}")
        return output
    
    def create_video(self, topic: str, duration: int = 60) -> Path:
        """Main method - create complete FREE video"""
        print(f"\n{'='*60}\n🎥 FREE YOUTUBE VIDEO GENERATOR\n{'='*60}")
        print(f"Topic: {topic}\nDuration: {duration}s\n💰 Cost: $0.00\n")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        proj_dir = self.output_dir / f"video_{timestamp}"
        proj_dir.mkdir()
        self.video_sources = []
        
        # 1. Script
        script = self.generate_script(topic, duration)
        with open(proj_dir / "script.json", 'w') as f:
            json.dump(script, f, indent=2)
        
        # 2. Voiceover
        narration = ' '.join([script['hook']] + [s['narration'] for s in script['sections']] + [script['cta']])
        audio = self.generate_voiceover(narration, proj_dir / "voice.mp3")
        
        # 3. Video clips
        videos = []
        for idx, sec in enumerate(script['sections']):
            vfile = proj_dir / f"clip_{idx:03d}.mp4"
            self.download_video(sec['visuals'], vfile)
            videos.append(vfile)
            time.sleep(1)
        
        # 4. Subtitles
        subs = self.create_subtitles(script['sections'], proj_dir / "subs.srt")
        
        # 5. Assemble
        safe_title = "".join(c for c in script['title'][:40] if c.isalnum() or c in ' -_').replace(' ', '_')
        final = proj_dir / f"{safe_title}.mp4"
        self.assemble_video(videos, audio, subs, final)
        
        # Metadata
        with open(proj_dir / "meta.json", 'w') as f:
            json.dump({
                "title": script['title'],
                "cost": "$0.00",
                "created": timestamp,
                "script_provider": self.script_provider,
                "video_sources": self.video_sources,
                "voice": "gTTS"
            }, f, indent=2)
        
        print(f"\n{'='*60}\n✅ DONE! Cost: $0.00 (FREE)\n📁 {final}\n{'='*60}\n")
        print(f"Script source: {self.script_provider}")
        print(f"Video sources: {', '.join(self.video_sources) or 'Unknown'}")
        return final

if __name__ == "__main__":
    print("""
╔════════════════════════════════════════════════╗
║   FREE YOUTUBE VIDEO GENERATOR                ║
║   100% Free - No API Keys Required!           ║
╚════════════════════════════════════════════════╝
""")
    
    # Check ffmpeg
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
    except:
        print("❌ Install ffmpeg: sudo apt install ffmpeg")
        sys.exit(1)

    # Gemini Pro (optional)
    if os.getenv('GEMINI_API_KEY'):
        print("✅ Gemini Pro key detected\n")
    else:
        print("ℹ️  Set GEMINI_API_KEY to use Gemini Pro for scripts\n")
    
    # Check Ollama (optional)
    try:
        if requests.get('http://localhost:11434/api/tags', timeout=2).status_code == 200:
            print("✅ Ollama detected\n")
    except:
        print("ℹ️  Ollama not found (optional) - using templates\n")
    
    # Get topic
    topic = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else input("Topic: ").strip() or "The Future of AI"
    
    # Info about Pexels
    if not os.getenv('PEXELS_API_KEY'):
        print("💡 TIP: Get FREE Pexels API at https://www.pexels.com/api/\n   Then: export PEXELS_API_KEY='your-key'\n")
    
    # Create video
    try:
        gen = FreeYouTubeGenerator()
        video = gen.create_video(topic, duration=60)
        print(f"🎉 Your FREE video: {video}")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
