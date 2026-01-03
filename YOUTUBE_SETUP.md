# 🎬 YouTube Auto-Upload Setup Guide

Get your videos automatically uploaded to YouTube!

## 📋 What You Need

1. Google Account
2. YouTube Channel
3. 15 minutes

## 🚀 Step-by-Step Setup

### Step 1: Create Google Cloud Project (5 min)

1. **Go to Google Cloud Console**
   ```
   https://console.cloud.google.com/
   ```

2. **Create New Project**
   - Click "Select a project" → "New Project"
   - Name it: "YouTube Video Uploader"
   - Click "Create"

### Step 2: Enable YouTube Data API (2 min)

1. **In your project, go to APIs & Services**
   - Click "Enable APIs and Services"
   
2. **Search for "YouTube Data API v3"**
   - Click on it
   - Click "Enable"

### Step 3: Create OAuth 2.0 Credentials (5 min)

1. **Go to Credentials**
   ```
   APIs & Services → Credentials
   ```

2. **Configure OAuth Consent Screen**
   - Click "Configure Consent Screen"
   - Choose "External" → Create
   - Fill in:
     * App name: "YouTube Auto-Uploader"
     * User support email: Your email
     * Developer contact: Your email
   - Click "Save and Continue"
   - Skip "Scopes" → Save and Continue
   - Add test users: Add your Google email
   - Click "Save and Continue"

3. **Create OAuth Client ID**
   - Click "Create Credentials" → "OAuth client ID"
   - Application type: "Desktop app"
   - Name: "YouTube Uploader"
   - Click "Create"

4. **Download Credentials**
   - Click the download icon (⬇️) next to your newly created credentials
   - Save file as `client_secrets.json`
   - Move it to your `youtube_studio_generator/` folder

### Step 4: Test Authentication (3 min)

```bash
cd youtube_studio_generator

# This will open a browser for authorization
python3 youtube_uploader.py
```

The first time:
1. Browser opens
2. Select your Google account
3. Click "Continue" (it's safe - you created this app)
4. Allow access
5. Done! Token saved for future uploads

## ✅ Verification

After setup, you should have:

```
youtube_studio_generator/
├── client_secrets.json      ← Google OAuth credentials
├── youtube_token.pickle     ← Auto-created after first auth
├── youtube_uploader.py      ← Uploader module
└── main_ultimate_free.py    ← Main script with upload
```

## 🎬 Usage

### Upload an Existing Video

```bash
python3 youtube_uploader.py video.mp4 public
# Options: public, unlisted, private
```

### Create and Auto-Upload

```bash
python3 main_ultimate_free.py "Your Topic"
# It will ask if you want to upload
```

### From Python

```python
from youtube_uploader import YouTubeUploader

uploader = YouTubeUploader()
uploader.authenticate()

video_id = uploader.upload_video(
    video_file=Path("my_video.mp4"),
    title="My Amazing Video",
    description="This is a great video!",
    keywords=["tutorial", "education", "2025"],
    privacy="public"  # public, unlisted, or private
)

print(f"Live at: https://www.youtube.com/watch?v={video_id}")
```

## 🔒 Privacy Settings

- **public**: Anyone can find and watch
- **unlisted**: Only people with the link can watch
- **private**: Only you can watch

## 💡 Tips

1. **First Video**: Use "unlisted" to test
2. **Titles**: Keep under 100 characters
3. **Keywords**: Add 5-10 relevant tags
4. **Descriptions**: Make them detailed for SEO
5. **Thumbnails**: Upload custom ones for better clicks

## 🎯 Advanced: Batch Upload

```python
from youtube_uploader import YouTubeUploader
from pathlib import Path

uploader = YouTubeUploader()
uploader.authenticate()

video_dir = Path("output")
for video_file in video_dir.glob("*/*.mp4"):
    metadata_file = video_file.parent / "metadata.json"
    
    if metadata_file.exists():
        with open(metadata_file) as f:
            meta = json.load(f)
        
        video_id = uploader.upload_video(
            video_file=video_file,
            title=meta['title'],
            description=meta['description'],
            keywords=meta['keywords'],
            privacy='unlisted'
        )
        
        print(f"Uploaded: https://www.youtube.com/watch?v={video_id}")
```

## 🐛 Troubleshooting

### "client_secrets.json not found"
- Download it from Google Cloud Console
- Place it in youtube_studio_generator/ folder

### "Invalid credentials"
- Delete youtube_token.pickle
- Run again to re-authenticate

### "Access blocked: YouTube Data API v3"
- Make sure you enabled the API in Google Cloud Console
- Add yourself as a test user in OAuth consent screen

### "Quota exceeded"
- Free tier: 10,000 quota units/day
- Each upload: ~1,600 units
- = ~6 uploads/day
- Resets daily at midnight Pacific Time

### "The app is unverified"
- This is normal for personal apps
- Click "Advanced" → "Go to [App Name] (unsafe)"
- It's safe - you created the app

## 📊 YouTube Quota

Free tier includes:
- **Quota**: 10,000 units/day
- **Upload cost**: ~1,600 units
- **Result**: ~6 videos/day free

To increase:
- Request quota increase (free)
- Or use multiple Google accounts

## 🎉 Success Checklist

- ✅ Created Google Cloud project
- ✅ Enabled YouTube Data API v3
- ✅ Created OAuth credentials
- ✅ Downloaded client_secrets.json
- ✅ Authenticated successfully
- ✅ First video uploaded!

## 🔗 Useful Links

- **Google Cloud Console**: https://console.cloud.google.com/
- **YouTube API Docs**: https://developers.google.com/youtube/v3
- **Quota Calculator**: https://developers.google.com/youtube/v3/determine_quota_cost

---

**Ready to auto-upload? Let's go! 🚀**

```bash
python3 main_ultimate_free.py "Your First Auto-Upload Video"
```
