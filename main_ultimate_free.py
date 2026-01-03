#!/usr/bin/env python3
"""
ULTIMATE FREE YouTube Video Generator + Auto-Upload
Best quality voice + HD videos + AI scripts + YouTube auto-upload
"""

import os, sys, json, time, random, subprocess, urllib.parse
from pathlib import Path
from datetime import datetime
import requests
from typing import List, Dict, Optional
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

# Import YouTube uploader
try:
    from youtube_uploader import YouTubeUploader
    YOUTUBE_AVAILABLE = True
except:
    YOUTUBE_AVAILABLE = False

class UltimateFreeGenerator:
    def __init__(self):
        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)
        
        # API keys
        self.pexels_key = os.getenv('PEXELS_API_KEY', '')
        self.pixabay_key = os.getenv('PIXABAY_API_KEY', '')
        self.elevenlabs_key = os.getenv('ELEVENLABS_API_KEY', '')
        self.script_provider = "template"
        self.video_sources: List[str] = []
        
        # YouTube uploader
        self.youtube_uploader = YouTubeUploader() if YOUTUBE_AVAILABLE else None
        
    def generate_script(self, topic: str, duration: int = 60) -> Dict:
        """Generate script with Gemini Pro (if available) or Ollama"""
        print(f"🎬 Generating AI script (Gemini/Ollama)...")

        prompt = f"""Create an ENGAGING YouTube video script about: {topic}

Requirements:
- Duration: {duration} seconds
- Hook: Start with a question or bold statement to grab attention
- Structure: Break into 3-5 clear sections
- Call-to-action: End with subscribe request
- SEO: Provide viral-worthy title and 10 keywords
- Visuals: Suggest specific footage for each section

Make it conversational, energetic, and YouTube algorithm-friendly!"""

        for provider in get_script_providers():
            if provider == "openai":
                text, err = generate_with_openai(prompt)
                if text:
                    print("✅ AI script generated (OpenAI)")
                    self.script_provider = "openai"
                    return self._parse_script(text, topic, duration)
                if has_openai_key() and err:
                    print(f"⚠️  OpenAI request failed: {err[:180]}")

            elif provider == "gemini":
                text, err = generate_with_gemini(prompt)
                if text:
                    print("✅ AI script generated (Gemini Pro)")
                    self.script_provider = "gemini"
                    return self._parse_script(text, topic, duration)
                if has_gemini_key() and err:
                    print(f"⚠️  Gemini Pro request failed: {err[:180]}")

            elif provider == "ollama":
                try:
                    r = requests.post(
                        'http://localhost:11434/api/generate',
                        json={"model": "llama2", "prompt": prompt, "stream": False},
                        timeout=60
                    )
                    
                    if r.status_code == 200:
                        text = r.json()['response']
                        print("✅ AI script generated (Ollama)")
                        self.script_provider = "ollama"
                        return self._parse_script(text, topic, duration)
                except Exception as e:
                    print(f"⚠️  Ollama error: {e}")

            elif provider == "template":
                return self._create_viral_template(topic, duration)

        return self._create_viral_template(topic, duration)
    
    def _create_viral_template(self, topic: str, duration: int) -> Dict:
        """Create engaging template script"""
        self.script_provider = "template"
        sections = [
            {
                "time": "0-8s",
                "narration": f"Wait, you won't believe what I discovered about {topic}! This will completely change how you think about it.",
                "visuals": f"shocking {topic} reveal"
            },
            {
                "time": "8-23s",
                "narration": f"Most people have no idea about this, but {topic} is way more important than you think. Here's why.",
                "visuals": f"professional {topic} breakdown"
            },
            {
                "time": "23-38s",
                "narration": f"The secret behind {topic} that experts don't want you to know. This changes everything.",
                "visuals": f"expert {topic} demonstration"
            },
            {
                "time": "38-53s",
                "narration": f"And here's the best part about {topic} - it's easier than you think to get started today.",
                "visuals": f"simple {topic} tutorial"
            },
            {
                "time": "53-60s",
                "narration": "If this blew your mind, smash that subscribe button and drop a comment below! See you in the next one!",
                "visuals": "call to action animation"
            }
        ]
        
        return {
            "title": f"{topic}: The Truth Nobody Tells You (2025)",
            "hook": sections[0]["narration"],
            "sections": sections,
            "cta": "Subscribe for more mind-blowing content!",
            "keywords": [topic, f"{topic} explained", f"{topic} 2025", "tutorial", 
                        f"best {topic}", f"{topic} guide", "how to", f"{topic} tips",
                        "beginner", "complete guide"],
            "description": f"""In this video, I reveal everything you need to know about {topic}!

🔥 What you'll learn:
• The truth about {topic}
• Why {topic} matters in 2025
• How to get started with {topic}
• Expert tips and tricks

📌 Timestamps:
0:00 - Shocking revelation
0:08 - Why this matters
0:23 - The secret
0:38 - How to start
0:53 - Subscribe!

💬 Drop a comment if you found this helpful!
👍 Like this video to support the channel
🔔 Subscribe for weekly content on {topic} and more!

#${topic.replace(' ', '')} #Tutorial #2025"""
        }
    
    def _parse_script(self, text: str, topic: str, duration: int) -> Dict:
        """Parse AI output"""
        lines = [l.strip() for l in text.split('\n') if l.strip()]
        
        title = next((l.split(':', 1)[1].strip() for l in lines if 'title' in l.lower()), 
                     f"{topic} - The Complete Guide")
        
        section_count = 5
        sec_duration = duration // section_count
        sections = []
        
        content_lines = [l for l in lines if len(l) > 20 and not l.lower().startswith(('title', 'keyword'))]
        
        for i in range(section_count):
            start = i * sec_duration
            end = (i + 1) * sec_duration
            text_idx = min(i, len(content_lines) - 1)
            narration = content_lines[text_idx] if content_lines else f"Point {i+1} about {topic}"
            
            sections.append({
                "time": f"{start}-{end}s",
                "narration": narration[:400],
                "visuals": f"{topic} scene {i+1}"
            })
        
        keywords = [topic, f"{topic} 2025", "tutorial", "guide", "how to"]
        
        description = f"""Complete guide to {topic}!

What you'll learn in this video about {topic}.

Like and subscribe for more!

#${topic.replace(' ', '')}"""
        
        return {
            "title": title[:100],
            "hook": sections[0]["narration"],
            "sections": sections,
            "cta": "Thanks for watching! Subscribe!",
            "keywords": keywords,
            "description": description
        }
    
    def generate_ultra_realistic_voice(self, text: str, output: Path, voice: str = "Rachel") -> Path:
        """Generate ultra-realistic voice with ElevenLabs (BEST quality)"""
        print(f"🎙️  Generating ULTRA-REALISTIC voice with ElevenLabs...")
        
        if not self.elevenlabs_key:
            print("⚠️  No ElevenLabs key - using gTTS fallback")
            return self.generate_voiceover_gtts(text, output)
        
        # Best ElevenLabs voices (most realistic)
        voices = {
            "Rachel": "21m00Tcm4TlvDq8ikWAM",  # Professional female (default)
            "Adam": "pNInz6obpgDQGcFmaJgB",    # Deep male narrator
            "Antoni": "ErXwobaYiN019PkySvjV",  # Warm male
            "Bella": "EXAVITQu4vr4xnSDxMaL",   # Youthful female
            "Josh": "TxGEqnHWrfWFTfGW9XjX",    # Energetic male
            "Domi": "AZnzlk1XvdvUeBnXmlld",    # Strong female
            "Elli": "MF3mGyEYCl7XYWbV9V6O",    # Young female
            "Arnold": "VR6AewLTigWG4xSOukaG",  # Mature male
            "Sam": "yoZ06aMxZJJ28mfd3POQ"      # Young male
        }
        
        voice_id = voices.get(voice, voices["Rachel"])
        
        try:
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
            
            headers = {
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": self.elevenlabs_key
            }
            
            # Premium settings for maximum realism
            data = {
                "text": text[:5000],
                "model_id": "eleven_multilingual_v2",  # Best model
                "voice_settings": {
                    "stability": 0.5,           # Natural variation
                    "similarity_boost": 0.8,    # Voice accuracy
                    "style": 0.5,               # Expressive
                    "use_speaker_boost": True   # Enhanced clarity
                }
            }
            
            response = requests.post(url, json=data, headers=headers, timeout=60)
            
            if response.status_code == 200:
                with open(output, 'wb') as f:
                    f.write(response.content)
                print(f"✅ ULTRA-REALISTIC voice created! ({voice})")
                print(f"   Quality: ⭐⭐⭐⭐⭐ (Human-like)")
                return output
            else:
                print(f"⚠️  ElevenLabs error {response.status_code}")
        except Exception as e:
            print(f"⚠️  ElevenLabs failed: {e}")
        
        return self.generate_voiceover_gtts(text, output)
    
    def generate_voiceover_gtts(self, text: str, output: Path) -> Path:
        """Fallback gTTS voice"""
        print(f"🎙️  Generating voice with gTTS...")
        from gtts import gTTS
        tts = gTTS(text=text[:5000], lang='en', slow=False)
        tts.save(str(output))
        print(f"✅ Voice created (gTTS)")
        return output

    def _image_to_video(self, image_bytes: bytes, output: Path, duration: int = 10) -> Path:
        """Convert a generated image into a short MP4 clip."""
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
    
    def download_hd_video(self, query: str, output: Path, duration: int = 10) -> Path:
        """Download HD video from multiple sources"""
        print(f"🎥 Searching HD videos: {query[:30]}...")

        for provider in get_image_providers():
            if provider == "openai":
                if has_openai_key():
                    img_bytes, img_error = generate_image_with_openai(query, width=1280, height=720)
                    if img_bytes:
                        try:
                            self._image_to_video(img_bytes, output, duration=duration)
                            print("  ✅ OpenAI image → video clip")
                            self.video_sources.append("openai-image")
                            return output
                        except Exception as e:
                            print(f"  ⚠️  OpenAI image-to-video failed: {e}")
                    else:
                        print(f"  ⚠️  OpenAI image failed: {img_error}")

            elif provider == "gemini":
                if has_gemini_key():
                    img_bytes, img_error = generate_image_with_gemini(query, width=1280, height=720)
                    if img_bytes:
                        try:
                            self._image_to_video(img_bytes, output, duration=duration)
                            print("  ✅ Gemini image → video clip")
                            self.video_sources.append("gemini-image")
                            return output
                        except Exception as e:
                            print(f"  ⚠️  Gemini image-to-video failed: {e}")
                    else:
                        print(f"  ⚠️  Gemini image failed: {img_error}")

            elif provider == "veo":
                vid_bytes, uri, err = generate_video_with_veo(query, poll_interval=10, max_polls=18, timeout=90)
                if vid_bytes:
                    with open(output, 'wb') as f:
                        f.write(vid_bytes)
                    self.video_sources.append("veo-3.1")
                    print("  ✅ Veo video clip")
                    return output
                if err:
                    print(f"  ⚠️  Veo video failed: {err}")

            elif provider == "pexels":
                if self.pexels_key:
                    video = self._download_pexels(query, output)
                    if video:
                        self.video_sources.append("pexels")
                        return video

            elif provider == "pixabay":
                if self.pixabay_key:
                    video = self._download_pixabay(query, output)
                    if video:
                        self.video_sources.append("pixabay")
                        return video

            elif provider == "ffmpeg":
                return self._create_cinematic_background(output, duration, query)

        return self._create_cinematic_background(output, duration, query)
    
    def _download_pexels(self, query: str, output: Path) -> Optional[Path]:
        """Download from Pexels"""
        print("  → Pexels...")
        try:
            r = requests.get(
                f"https://api.pexels.com/videos/search?query={urllib.parse.quote(query)}&per_page=5&orientation=landscape",
                headers={'Authorization': self.pexels_key}, timeout=15)
            
            if r.status_code == 200 and r.json().get('videos'):
                for video in r.json()['videos']:
                    vfiles = video['video_files']
                    hd = next((v for v in vfiles if v.get('width') == 1920), None) or \
                         next((v for v in vfiles if v.get('width', 0) >= 1280), vfiles[0])
                    
                    try:
                        vdata = requests.get(hd['link'], timeout=30).content
                        with open(output, 'wb') as f:
                            f.write(vdata)
                        print(f"  ✅ HD video (Pexels)")
                        self.video_sources.append("pexels")
                        return output
                    except:
                        continue
        except:
            pass
        return None
    
    def _download_pixabay(self, query: str, output: Path) -> Optional[Path]:
        """Download from Pixabay"""
        print("  → Pixabay...")
        try:
            r = requests.get(
                f"https://pixabay.com/api/videos/?key={self.pixabay_key}&q={urllib.parse.quote(query)}&per_page=5",
                timeout=15)
            
            if r.status_code == 200 and r.json().get('hits'):
                for video in r.json()['hits']:
                    vdata = video.get('videos', {})
                    url = vdata.get('large', {}).get('url') or vdata.get('medium', {}).get('url')
                    if url:
                        try:
                            data = requests.get(url, timeout=30).content
                            with open(output, 'wb') as f:
                                f.write(data)
                            print(f"  ✅ HD video (Pixabay)")
                            self.video_sources.append("pixabay")
                            return output
                        except:
                            continue
        except:
            pass
        return None
    
    def _create_cinematic_background(self, output: Path, duration: int, text: str) -> Path:
        """Create cinematic gradient background"""
        gradients = [
            ('0x1a1a2e', '0x16213e'),
            ('0x2d132c', '0x801336'),
            ('0x141e30', '0x243b55'),
            ('0x134e5e', '0x71b280'),
        ]
        gradient = random.choice(gradients)
        
        subprocess.run([
            'ffmpeg', '-y', '-f', 'lavfi',
            '-i', f'color=c={gradient[0]}:s=1920x1080:d={duration}',
            '-vf', f"drawtext=text='{text[:30]}':fontsize=70:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2:alpha=0.9,fade=in:0:30",
            '-c:v', 'libx264', '-preset', 'medium', '-crf', '18',
            str(output)
        ], capture_output=True, check=True)
        
        print(f"  ✅ Cinematic background")
        self.video_sources.append("ffmpeg-gradient")
        return output
    
    def create_subtitles(self, sections: List[Dict], output: Path) -> Path:
        """Create professional subtitles"""
        with open(output, 'w', encoding='utf-8') as f:
            for idx, sec in enumerate(sections, 1):
                times = sec['time'].replace('s', '').split('-')
                start, end = int(times[0]), int(times[1])
                
                text = sec['narration']
                words = text.split()
                lines = []
                current = []
                
                for word in words:
                    current.append(word)
                    if len(' '.join(current)) > 42:
                        lines.append(' '.join(current))
                        current = []
                if current:
                    lines.append(' '.join(current))
                
                subtitle = '\n'.join(lines[:2])
                f.write(f"{idx}\n00:00:{start:02d},000 --> 00:00:{end:02d},000\n{subtitle}\n\n")
        
        return output
    
    def assemble_premium_video(self, videos: List[Path], audio: Path, subs: Path, output: Path) -> Path:
        """Assemble with premium settings"""
        print("🎬 Assembling premium video...")
        
        concat_file = output.parent / "concat.txt"
        with open(concat_file, 'w') as f:
            for v in videos:
                f.write(f"file '{v.absolute()}'\n")
        
        temp = output.parent / "temp.mp4"
        subprocess.run([
            'ffmpeg', '-y', '-f', 'concat', '-safe', '0',
            '-i', str(concat_file), '-c:v', 'libx264',
            '-preset', 'medium', '-crf', '18', str(temp)
        ], capture_output=True, check=True)
        
        subtitle_style = "FontName=Arial Bold,FontSize=28,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=4,Outline=2,Shadow=2,MarginV=35"
        
        subprocess.run([
            'ffmpeg', '-y', '-i', str(temp), '-i', str(audio),
            '-c:v', 'libx264', '-preset', 'medium', '-crf', '18',
            '-c:a', 'aac', '-b:a', '192k', '-shortest',
            '-vf', f"scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=black,subtitles={subs}:force_style='{subtitle_style}'",
            '-pix_fmt', 'yuv420p', str(output)
        ], check=True, capture_output=True)
        
        temp.unlink(missing_ok=True)
        concat_file.unlink(missing_ok=True)
        print(f"✅ Premium video created")
        return output
    
    def create_and_upload_video(self, topic: str, duration: int = 60, 
                                voice: str = "Rachel", upload: bool = True,
                                privacy: str = "public") -> Dict:
        """Create video and optionally upload to YouTube"""
        print(f"\n{'='*70}")
        print(f"🎥 ULTIMATE FREE VIDEO GENERATOR + YOUTUBE UPLOAD")
        print(f"{'='*70}")
        print(f"Topic: {topic}")
        print(f"Duration: {duration}s")
        print(f"Voice: {voice} (Ultra-realistic)")
        print(f"Upload: {'Yes' if upload else 'No'}")
        print(f"💰 Cost: $0.00\n")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        proj_dir = self.output_dir / f"video_{timestamp}"
        proj_dir.mkdir()
        self.video_sources = []
        
        # 1. Generate AI script
        script = self.generate_script(topic, duration)
        with open(proj_dir / "script.json", 'w', encoding='utf-8') as f:
            json.dump(script, f, indent=2, ensure_ascii=False)
        
        # 2. Generate ULTRA-REALISTIC voiceover
        narration = ' '.join([script['hook']] + [s['narration'] for s in script['sections']] + [script['cta']])
        audio = self.generate_ultra_realistic_voice(narration, proj_dir / "voiceover.mp3", voice)
        
        # 3. Download HD videos
        videos = []
        for idx, sec in enumerate(script['sections']):
            vfile = proj_dir / f"clip_{idx:03d}.mp4"
            self.download_hd_video(sec['visuals'], vfile, duration=12)
            videos.append(vfile)
            time.sleep(1.5)
        
        if not videos:
            vfile = proj_dir / "clip_000.mp4"
            self._create_cinematic_background(vfile, duration, topic)
            videos.append(vfile)
        
        # 4. Create subtitles
        subs = self.create_subtitles(script['sections'], proj_dir / "subtitles.srt")
        
        # 5. Assemble video
        safe_title = "".join(c for c in script['title'][:45] if c.isalnum() or c in ' -_').replace(' ', '_')
        final = proj_dir / f"{safe_title}.mp4"
        self.assemble_premium_video(videos, audio, subs, final)
        
        # 6. Save metadata
        metadata = {
            "title": script['title'],
            "description": script.get('description', f"Video about {topic}"),
            "keywords": script['keywords'],
            "created": timestamp,
            "duration": duration,
            "cost": "$0.00",
            "voice": voice,
            "quality": "ULTRA-PREMIUM",
            "script_provider": self.script_provider,
            "video_sources": self.video_sources
        }
        
        with open(proj_dir / "metadata.json", 'w') as f:
            json.dump(metadata, f, indent=2)
        
        result = {
            "video_file": final,
            "title": script['title'],
            "keywords": script['keywords']
        }
        
        # 7. Upload to YouTube
        if upload and YOUTUBE_AVAILABLE and self.youtube_uploader:
            print(f"\n{'='*70}")
            print(f"📤 UPLOADING TO YOUTUBE")
            print(f"{'='*70}\n")
            
            try:
                self.youtube_uploader.authenticate()
                video_id = self.youtube_uploader.upload_video(
                    video_file=final,
                    title=script['title'],
                    description=script.get('description', ''),
                    keywords=script['keywords'],
                    privacy=privacy
                )
                
                result["youtube_url"] = f"https://www.youtube.com/watch?v={video_id}"
                result["video_id"] = video_id
                
            except Exception as e:
                print(f"⚠️  Upload failed: {e}")
                print(f"   You can upload manually from: {final}")
        
        print(f"\n{'='*70}")
        print(f"✅ COMPLETE!")
        print(f"{'='*70}")
        print(f"📁 Video: {final}")
        print(f"📝 Title: {script['title']}")
        if "youtube_url" in result:
            print(f"🌐 YouTube: {result['youtube_url']}")
        print(f"💰 Cost: $0.00")
        print(f"⭐ Quality: ULTRA-PREMIUM")
        print(f"{'='*70}\n")
        print(f"Script source: {self.script_provider}")
        print(f"Video sources: {', '.join(self.video_sources) or 'Unknown'}")
        
        return result


if __name__ == "__main__":
    print("""
╔════════════════════════════════════════════════════════╗
║  ULTIMATE FREE VIDEO GENERATOR + YOUTUBE UPLOAD       ║
║  Ultra-Realistic Voice + HD Videos + Auto-Upload      ║
╚════════════════════════════════════════════════════════╝
""")
    
    # Check requirements
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
    except:
        print("❌ Install ffmpeg: sudo apt install ffmpeg")
        sys.exit(1)
    
    # Check tools
    print("🔍 Checking tools...\n")

    if os.getenv('GEMINI_API_KEY'):
        print("✅ Gemini Pro (AI scripts + image clips)")
    else:
        print("ℹ️  Gemini Pro available - set GEMINI_API_KEY to use Google AI scripts/images")

    if os.getenv('OPENAI_API_KEY') or os.getenv('OPENAI_ACCESS_TOKEN'):
        print("✅ OpenAI (AI scripts + image clips)")
    else:
        print("ℹ️  OpenAI available - set OPENAI_API_KEY or OPENAI_ACCESS_TOKEN")
    
    if os.getenv('ELEVENLABS_API_KEY'):
        print("✅ ElevenLabs (Ultra-realistic voice)")
    else:
        print("⚠️  Get ElevenLabs key: https://elevenlabs.io")
    
    if os.getenv('PEXELS_API_KEY'):
        print("✅ Pexels (HD videos)")
    else:
        print("ℹ️  Get Pexels key: https://www.pexels.com/api/")
    
    if YOUTUBE_AVAILABLE:
        print("✅ YouTube API ready")
    else:
        print("ℹ️  Install: pip install google-auth google-auth-oauthlib google-api-python-client")
    
    print()
    
    # Get input
    topic = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else input("🎬 Video Topic: ").strip() or "The Future of AI"
    
    # Options
    upload = input("\n📤 Upload to YouTube? (y/n): ").lower().startswith('y')
    
    if upload:
        privacy = input("🔒 Privacy (public/unlisted/private): ").lower()
        if privacy not in ['public', 'unlisted', 'private']:
            privacy = 'public'
    else:
        privacy = 'public'
    
    voice = input("🎤 Voice (Rachel/Adam/Antoni/Bella/Josh/Domi/Elli/Arnold/Sam): ").strip() or "Rachel"
    
    print()
    
    # Create and upload
    try:
        gen = UltimateFreeGenerator()
        result = gen.create_and_upload_video(
            topic=topic,
            duration=60,
            voice=voice,
            upload=upload,
            privacy=privacy
        )
        
        if "youtube_url" in result:
            print(f"🎉 Live on YouTube: {result['youtube_url']}")
        else:
            print(f"🎉 Video ready: {result['video_file']}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
