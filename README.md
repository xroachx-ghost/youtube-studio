# FREE YouTube Video Generator 🎬

Create professional YouTube videos **100% FREE** - no paid APIs, no subscriptions!

## 💰 Cost: $0.00

Unlike paid tools that cost $0.50-3.00 per video, this is completely free.

## ✨ Features

- **FREE Script Generation**: Templates or Ollama (local AI)
- **FREE Voiceovers**: Google Text-to-Speech (100+ languages)
- **FREE Video Clips**: Pexels stock footage or generated backgrounds
- **FREE Assembly**: FFmpeg video processing
- **Automatic Subtitles**: SRT generation included
- **1080p HD Output**: Professional quality

## 🚀 Quick Start

```bash
cd youtube_studio_generator

# Install (only 2 free packages!)
pip install -r requirements.txt

# Create your first video!
python main_free.py "The Future of AI"
```

That's it! No API keys required.

## 🎯 Optional Upgrades (Still Free!)

### Better Scripts: Gemini Pro (have a Google AI key?)
```bash
# 1. Get an API key: https://ai.google.dev/
# 2. Export your key (works with all generator scripts)
export GEMINI_API_KEY='your-google-ai-key'
```

With the key set, Gemini is used first for scripts and to generate images that are auto-turned into video clips (fallbacks stay in place).

### Better Scripts/Images: OpenAI (if you have an OpenAI account)
```bash
# 1. Grab an API key: https://platform.openai.com/account/api-keys
#    (or use an access token if you have one)
export OPENAI_API_KEY='your-openai-key'
```

If set, OpenAI is used first for scripts and DALL·E image clips, then Gemini/Ollama/template as fallbacks.

### Better Videos: Pexels API (30 seconds to setup)
```bash
# 1. Visit https://www.pexels.com/api/
# 2. Sign up (free)
# 3. Get API key
export PEXELS_API_KEY='your-key-here'
```

### Better Scripts: Ollama (10 minutes to setup)
```bash
# Install Ollama: https://ollama.ai
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama2
```

## 📖 Usage

### Command Line
```bash
python main_free.py "Top 10 Life Hacks"
python main_free.py "How Bitcoin Works"
python main_free.py "Best Python Tips for 2025"
```

### Python API
```python
from main_free import FreeYouTubeGenerator

gen = FreeYouTubeGenerator()
video = gen.create_video("Your Topic Here", duration=60)
print(f"Video created: {video}")
```

## 🌍 Languages Supported

100+ languages via gTTS:
- English, Spanish, French, German, Italian, Portuguese
- Hindi, Japanese, Korean, Chinese, Arabic, Russian
- And 90+ more!

To change language, edit the generator code:
```python
tts = gTTS(text=text, lang='es', slow=False)  # Spanish
tts = gTTS(text=text, lang='fr', slow=False)  # French
```

## 📂 Output Structure

```
output/video_20241230_180000/
├── script.json       # Generated script
├── voice.mp3         # Voiceover
├── clip_000.mp4      # Video clips
├── clip_001.mp4
├── clip_002.mp4
├── subs.srt          # Subtitles
├── meta.json         # Metadata
└── Your_Topic.mp4    # FINAL VIDEO ✅
```

## 💡 Tips for Best Results

1. **Be Specific**: "10 Python Tips for Beginners" > "Python"
2. **Get Pexels API**: Takes 30 seconds, huge quality boost
3. **Install Ollama**: Better scripts = better videos
4. **Optimal Length**: 60-120 seconds for YouTube

## 🔧 Requirements

- Python 3.8+
- FFmpeg (`sudo apt install ffmpeg`)
- Internet (for video downloads & TTS)

## ❓ Troubleshooting

**"ffmpeg not found"**
```bash
sudo apt install ffmpeg
```

**Want Better Quality?**
- Get Pexels API (free): https://www.pexels.com/api/
- Install Ollama (free): https://ollama.ai

**Videos have colored backgrounds?**
- This means Pexels API isn't set up
- Get free key at https://www.pexels.com/api/

## 🆚 Comparison

| Feature | This Tool | Paid Tools |
|---------|-----------|------------|
| Script | FREE | $0.03-0.10 |
| Voiceover | FREE | $0.30-1.50 |
| Videos | FREE | $0.20-2.00 |
| **Total** | **$0.00** | **$0.53-3.60** |

## 📈 What You Can Create

- Educational content
- Product reviews
- Tutorials & how-tos
- News summaries
- Motivational content
- Business explainers
- Social media content

## 🎓 Examples

```bash
# Tech
python main_free.py "5 ChatGPT Prompts That Will Blow Your Mind"

# Education  
python main_free.py "Photosynthesis Explained in 60 Seconds"

# Business
python main_free.py "How to Start a Side Hustle in 2025"

# Lifestyle
python main_free.py "Morning Routine of Successful People"
```

## 🤝 Contributing

This is open source! Feel free to:
- Add new features
- Fix bugs
- Improve documentation
- Share your creations

## 📜 License

MIT License - Use freely!

## 🎉 Credits

Built with:
- **gTTS** - Google Text-to-Speech
- **Pexels** - Free stock videos
- **FFmpeg** - Video processing
- **Ollama** - Optional local AI

---

**Ready to create unlimited FREE videos? Let's go! 🚀**

```bash
python main_free.py "Your Amazing Topic Here"
```
