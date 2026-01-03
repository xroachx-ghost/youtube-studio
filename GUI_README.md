# 🖥️ GUI Application - Complete Guide

Beautiful, easy-to-use desktop application with guided setup!

## ✨ Features

### 🎯 Guided Setup Wizard
- Step-by-step configuration
- API key management
- Voice selection with previews
- YouTube upload setup
- Saves all preferences

### 🎬 Video Creation Interface
- Simple, intuitive design
- Real-time progress tracking
- Live log output
- One-click creation

### 📊 History Management
- View all created videos
- Quick access to files
- Metadata display
- Re-open projects

### ⚙️ Settings Panel
- Manage API keys securely
- Change default preferences
- Re-run setup wizard
- Export/import settings

### 🎤 Voice Previews
- Test all 9 voices
- Hear before choosing
- Voice recommendations
- Switch anytime

## 🚀 Installation

```bash
cd youtube_studio_generator

# Install GUI dependencies
pip install PyQt5

# Or install all requirements
pip install -r requirements.txt
```

## 🎬 Launch

```bash
python3 video_generator_gui.py
```

Or make it executable:
```bash
chmod +x video_generator_gui.py
./video_generator_gui.py
```

## 📖 First Time Setup

1. **Welcome Screen**
   - Overview of features
   - Time estimate

2. **API Keys** (5 min)
   - ElevenLabs - Click to open signup
   - Pexels - Click to open signup  
   - Pixabay (optional)
   - Paste keys directly

3. **Voice Selection**
   - Choose default voice
   - See recommendations
   - Test voices (coming soon!)

4. **AI Scripts** (Optional)
   - Enable Ollama
   - Download link provided
   - Setup instructions

5. **YouTube Upload** (Optional)
   - Enable auto-upload
   - Upload client_secrets.json
   - Authenticate later

6. **Preferences**
   - Default video length
   - Content style
   - Subtitle preferences
   - Privacy settings

7. **Complete!**
   - Settings saved
   - Ready to create

## 🎨 Interface Overview

### Main Window - Create Tab

```
┌─────────────────────────────────────────────────────┐
│  🎬 Create Video  📁 History  ⚙️ Settings  ❓ Help  │
├─────────────────────────────────────────────────────┤
│                                                     │
│  🎯 Video Topic                                     │
│  ┌─────────────────────────────────────────────┐   │
│  │ 10 Python Tips for Beginners in 2025       │   │
│  └─────────────────────────────────────────────┘   │
│  💡 Tip: Be specific!                              │
│                                                     │
│  📹 Video Settings     │    📤 Upload Settings     │
│  ─────────────────────────────────────────────────  │
│  Duration: 60 sec      │    ☑ Upload to YouTube   │
│  Voice: Rachel ▼       │    Privacy: unlisted ▼   │
│  Style: Professional ▼  │                          │
│  ☑ Add subtitles       │                          │
│                                                     │
│  ┌─────────────────────────────────────────────┐   │
│  │          🎬 CREATE VIDEO                   │   │
│  └─────────────────────────────────────────────┘   │
│                                                     │
│  📝 Progress Log                                    │
│  ┌─────────────────────────────────────────────┐   │
│  │ [18:45:23] Starting video creation...      │   │
│  │ [18:45:24] Generating AI script...         │   │
│  │ [18:45:35] Script generated successfully   │   │
│  └─────────────────────────────────────────────┘   │
│                                                     │
│  Status: Ready                                      │
└─────────────────────────────────────────────────────┘
```

### History Tab

```
┌─────────────────────────────────────────────────────┐
│  Title              Created      Duration  Actions  │
├─────────────────────────────────────────────────────┤
│  Python Tips        12/30 18:45  60s      📁 Open   │
│  AI Tools 2025      12/30 14:20  90s      📁 Open   │
│  Quick Tutorial     12/29 10:15  45s      📁 Open   │
└─────────────────────────────────────────────────────┘
```

### Settings Tab

```
┌─────────────────────────────────────────────────────┐
│  🔑 API Keys                                        │
│  ─────────────────────────────────────────────────  │
│  ElevenLabs: ****************  👁  [Get Key →]     │
│  Pexels:     ****************  👁  [Get Key →]     │
│                                                     │
│  💾 Save API Keys                                   │
│                                                     │
│  ⚙️ Default Settings                                │
│  ─────────────────────────────────────────────────  │
│  Default Voice:   Rachel ▼                         │
│  Default Length:  60 seconds                       │
│  Default Style:   Professional ▼                    │
│  ☑ Add subtitles by default                        │
│                                                     │
│  🔄 Run Setup Wizard Again                         │
└─────────────────────────────────────────────────────┘
```

## 🎯 Usage

### Create a Video

1. **Enter Topic**
   - Type in the text box
   - Be specific and detailed

2. **Configure** (Optional)
   - Adjust duration
   - Choose voice
   - Select style
   - Toggle subtitles

3. **Upload Settings** (Optional)
   - Check "Upload to YouTube"
   - Choose privacy level

4. **Click CREATE VIDEO**
   - Watch progress in real-time
   - See logs as it processes
   - Wait for completion (3-5 min)

5. **Done!**
   - Video saved to output folder
   - Uploaded to YouTube (if enabled)
   - View in History tab

### Managing Settings

1. Go to **Settings** tab
2. Update API keys anytime
3. Change default preferences
4. Re-run setup wizard if needed
5. Click **Save**

### Viewing History

1. Go to **History** tab
2. See all created videos
3. Click **📁 Open** to view files
4. Metadata displayed in table

## 🔥 Advanced Features

### Keyboard Shortcuts

- `Ctrl+N` - New video (focus topic field)
- `Ctrl+Enter` - Create video
- `Ctrl+H` - View history
- `Ctrl+,` - Open settings
- `Ctrl+Q` - Quit

### Batch Creation (Coming Soon!)

- Queue multiple videos
- Process in sequence
- Auto-upload all
- Batch settings

### Templates (Coming Soon!)

- Save favorite configurations
- Quick video types
- Preset durations
- Voice profiles

### Analytics (Coming Soon!)

- View video performance
- Track uploads
- Usage statistics
- Cost tracking

## 🎨 Customization

### Themes

Currently: Fusion style (clean, modern)

Coming soon:
- Dark mode
- Light mode
- Custom colors
- Font sizes

### Window Layout

- Resizable windows
- Remember size/position
- Fullscreen mode
- Multi-monitor support

## 🐛 Troubleshooting

### "PyQt5 not found"
```bash
pip install PyQt5
```

### "Generator not available"
- Ensure main scripts are in same folder
- Check file permissions
- Re-run setup wizard

### "Can't save settings"
- Check folder permissions
- Run from correct directory

### Window doesn't open
- Check Python version (need 3.6+)
- Update PyQt5: `pip install --upgrade PyQt5`
- Try: `python3 video_generator_gui.py`

### API keys not working
- Re-enter in Settings tab
- Click Save
- Restart application

## 💡 Pro Tips

1. **First Run**
   - Complete setup wizard fully
   - Test with one video first
   - Check all features work

2. **Daily Use**
   - Keep window open
   - Use keyboard shortcuts
   - Check history regularly

3. **Batch Work**
   - Create multiple topics
   - Queue them up
   - Process overnight

4. **Organization**
   - Name videos clearly
   - Use consistent styles
   - Tag/categorize (coming soon)

## 🔄 Updates

To update:
```bash
cd youtube_studio_generator
git pull  # if using git
# Or re-download files
```

Settings are preserved between updates!

## 📊 System Requirements

- **OS**: Windows, macOS, Linux
- **Python**: 3.6+
- **RAM**: 2GB minimum, 4GB recommended
- **Disk**: 1GB free space
- **Internet**: Required for API calls

## 🎓 Video Tutorial

Coming soon: Video walkthrough of GUI!

## 🤝 Contributing

Want to improve the GUI?
- Report bugs
- Suggest features
- Submit pull requests
- Share feedback

## 📜 Changelog

### v1.0.0 (Current)
- ✅ Initial release
- ✅ Guided setup wizard
- ✅ Video creation interface
- ✅ History management
- ✅ Settings panel
- ✅ Help documentation

### Coming Soon
- 🔜 Voice preview/testing
- 🔜 Batch video creation
- 🔜 Video templates
- 🔜 Dark mode
- 🔜 Analytics dashboard
- 🔜 Thumbnail generator
- 🔜 Script editor
- 🔜 Export presets

---

## 🎉 Ready to Create!

```bash
python3 video_generator_gui.py
```

**Beautiful interface + Powerful features = Amazing videos! 🚀**
