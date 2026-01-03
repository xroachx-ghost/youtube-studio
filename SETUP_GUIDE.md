# 🚀 Premium FREE Setup Guide

Get the **BEST FREE quality** for your YouTube videos! All tools below are 100% free.

## ⚡ Quick Setup (15 minutes)

### 1️⃣ Install Ollama (Best Free AI - 5 min)

**Why?** Professional scripts that rival GPT-4

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Download Llama 2 (best free model)
ollama pull llama2

# Test it
ollama run llama2 "Write a hook about AI"
```

**Cost:** $0 | **Quality:** ⭐⭐⭐⭐⭐

---

### 2️⃣ ElevenLabs Voice (Best Free TTS - 2 min)

**Why?** Studio-quality voiceovers (way better than Google TTS)

**Free Tier:** 10,000 characters/month (about 10-15 videos)

1. Visit: https://elevenlabs.io
2. Sign up (free, no credit card)
3. Go to Profile → API Key
4. Copy your API key

```bash
export ELEVENLABS_API_KEY='your-key-here'
```

**Cost:** $0 | **Quality:** ⭐⭐⭐⭐⭐

---

### 3️⃣ Pexels Videos (Best Free Stock - 1 min)

**Why?** Million+ HD videos, completely free

1. Visit: https://www.pexels.com/api/
2. Click "Get Started"
3. Sign up (30 seconds)
4. Copy your API key

```bash
export PEXELS_API_KEY='your-key-here'
```

**Limits:** 200 requests/hour (more than enough!)

**Cost:** $0 | **Quality:** ⭐⭐⭐⭐⭐

---

### 4️⃣ Pixabay Videos (Backup Source - 1 min)

**Why?** Extra video sources, more variety

1. Visit: https://pixabay.com/api/docs/
2. Sign up
3. Get API key

```bash
export PIXABAY_API_KEY='your-key-here'
```

**Cost:** $0 | **Quality:** ⭐⭐⭐⭐

---

## 🎬 Usage

### Basic (works immediately with defaults)
```bash
python main_premium_free.py "The Future of AI"
```

### With ALL premium tools
```bash
# Set all API keys first
export ELEVENLABS_API_KEY='your-key'
export PEXELS_API_KEY='your-key'
export PIXABAY_API_KEY='your-key'

# Make sure Ollama is running
ollama serve

# Create video
python main_premium_free.py "10 Mind-Blowing AI Facts"
```

---

## 💾 Persist API Keys

Add to `~/.bashrc` so you don't need to set them every time:

```bash
echo 'export ELEVENLABS_API_KEY="your-key"' >> ~/.bashrc
echo 'export PEXELS_API_KEY="your-key"' >> ~/.bashrc
echo 'export PIXABAY_API_KEY="your-key"' >> ~/.bashrc
source ~/.bashrc
```

---

## 🎯 Quality Comparison

| Setup Level | Script | Voice | Video | Time | Quality |
|-------------|--------|-------|-------|------|---------|
| **Basic** | Template | gTTS | Generated | 0 min | ⭐⭐⭐ |
| **Good** | Template | gTTS | Pexels | 1 min | ⭐⭐⭐⭐ |
| **Premium** | Ollama | ElevenLabs | Pexels+Pixabay | 15 min | ⭐⭐⭐⭐⭐ |

**ALL ARE FREE!** Premium just takes 15 min to setup once.

---

## 🎤 ElevenLabs Voice Options

The premium script uses the best free voices:

- **Rachel** (default) - Professional female
- **Adam** - Deep male narrator
- **Antoni** - Warm male voice
- **Elli** - Young female
- **Josh** - Young male

To change voice, edit `main_premium_free.py` line 88:
```python
url = "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM"  # Rachel
# Other voice IDs:
# Adam: pNInz6obpgDQGcFmaJgB
# Antoni: ErXwobaYiN019PkySvjV
# Elli: MF3mGyEYCl7XYWbV9V6O
# Josh: TxGEqnHWrfWFTfGW9XjX
```

---

## 📊 Free Tier Limits

| Service | Monthly Limit | Videos/Month |
|---------|---------------|--------------|
| **ElevenLabs** | 10k characters | ~12 videos |
| **Pexels** | 200 req/hour | Unlimited |
| **Pixabay** | 5k req/hour | Unlimited |
| **Ollama** | Unlimited | Unlimited |

**Pro Tip:** If you hit ElevenLabs limit, it automatically falls back to gTTS!

---

## 🎨 Advanced: Background Music

Want free background music too?

### Option 1: YouTube Audio Library
1. Visit: https://www.youtube.com/audiolibrary
2. Download royalty-free music
3. Place in `assets/music/`

### Option 2: Incompetech (Kevin MacLeod)
1. Visit: https://incompetech.com/music/
2. Download free tracks
3. Credit: "Music by Kevin MacLeod"

### Add music to video:
```python
# In the script, add:
music_file = Path("assets/music/your_track.mp3")
gen.add_background_music(final_video, music_file, volume=0.2)
```

---

## 🔧 Troubleshooting

### "Ollama not found"
```bash
# Make sure it's running
ollama serve

# In another terminal:
ollama list  # Should show llama2
```

### "ElevenLabs quota exceeded"
Script automatically falls back to gTTS. Quota resets monthly.

### "No videos found"
Make sure API keys are set:
```bash
echo $PEXELS_API_KEY  # Should show your key
echo $PIXABAY_API_KEY
```

### "Voice sounds robotic"
You're using gTTS fallback. Set up ElevenLabs for premium quality.

---

## ⏱️ Processing Times

With all premium tools:
- Script generation: 10-20 seconds (Ollama)
- Voiceover: 5-10 seconds (ElevenLabs)
- Video download: 15-30 seconds per clip
- Assembly: 30-60 seconds

**Total: 3-5 minutes per 60-second video**

---

## 🎯 Best Practices

1. **Topic Specificity**: "10 Python Tips for Data Science" > "Python"
2. **Video Length**: 60-90 seconds optimal for engagement
3. **Multiple Runs**: Generate 2-3 versions, pick best
4. **Keywords**: Let Ollama suggest them automatically
5. **Thumbnails**: Use first frame or create custom (future feature!)

---

## 💡 Pro Tips

### Get Even More Free Videos
- **Videvo**: https://www.videvo.net/ (no API, manual download)
- **Coverr**: https://coverr.co/ (no API, manual download)
- **Mixkit**: https://mixkit.co/ (no API, manual download)

### Enhance Scripts
```bash
# Use larger Ollama models for better scripts
ollama pull llama2:13b  # Bigger = better (requires more RAM)
```

### Batch Processing
```bash
# Create multiple videos
for topic in "AI" "Python" "Tech"; do
    python main_premium_free.py "$topic"
done
```

---

## 📈 Roadmap

Coming soon (all free):
- [ ] Automatic thumbnail generation
- [ ] Background music integration
- [ ] Batch processing mode
- [ ] Web interface
- [ ] Direct YouTube upload
- [ ] More video sources

---

## ❓ FAQ

**Q: Is this really 100% free?**
A: Yes! All tools have generous free tiers.

**Q: Can I monetize videos?**
A: Yes! Pexels/Pixabay are royalty-free. Music needs attribution.

**Q: How many videos can I make?**
A: Unlimited! Only ElevenLabs has a soft limit (10k chars/month).

**Q: Quality vs paid tools?**
A: Very close! ElevenLabs free = 90% of OpenAI TTS quality.

**Q: Do I need GPU for Ollama?**
A: No, but it helps. CPU works fine for scripts.

---

**Ready to create PREMIUM quality videos for FREE? Let's go! 🚀**

```bash
python main_premium_free.py "Your Amazing Topic"
```
