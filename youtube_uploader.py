#!/usr/bin/env python3
"""
YouTube Auto-Uploader
Automatically upload videos to YouTube using Google API
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

# YouTube API scopes
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

class YouTubeUploader:
    def __init__(self):
        self.credentials = None
        self.youtube = None
        self.token_file = Path('youtube_token.pickle')
        self.client_secrets_file = Path('client_secrets.json')
        
    def authenticate(self):
        """Authenticate with YouTube API"""
        print("🔐 Authenticating with YouTube...")
        
        # Check for existing credentials
        if self.token_file.exists():
            with open(self.token_file, 'rb') as token:
                self.credentials = pickle.load(token)
        
        # Refresh or get new credentials
        if not self.credentials or not self.credentials.valid:
            if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                print("   Refreshing token...")
                self.credentials.refresh(Request())
            else:
                if not self.client_secrets_file.exists():
                    print("\n❌ client_secrets.json not found!")
                    print("\nTo get it:")
                    print("1. Go to: https://console.cloud.google.com/")
                    print("2. Create a project")
                    print("3. Enable YouTube Data API v3")
                    print("4. Create OAuth 2.0 credentials")
                    print("5. Download as client_secrets.json")
                    print("6. Place in this directory\n")
                    sys.exit(1)
                
                print("   Opening browser for authorization...")
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(self.client_secrets_file), SCOPES)
                self.credentials = flow.run_local_server(port=8080)
            
            # Save credentials
            with open(self.token_file, 'wb') as token:
                pickle.dump(self.credentials, token)
        
        self.youtube = build('youtube', 'v3', credentials=self.credentials)
        print("✅ Authentication successful!\n")
    
    def upload_video(self, video_file: Path, title: str, description: str, 
                    keywords: list, category: str = "22", 
                    privacy: str = "public") -> str:
        """
        Upload video to YouTube
        
        Args:
            video_file: Path to video file
            title: Video title (max 100 chars)
            description: Video description (max 5000 chars)
            keywords: List of keywords/tags (max 500 chars total)
            category: YouTube category ID (22 = People & Blogs)
            privacy: public, private, or unlisted
        
        Returns:
            Video ID of uploaded video
        """
        
        if not self.youtube:
            self.authenticate()
        
        print(f"📤 Uploading to YouTube...")
        print(f"   Title: {title[:50]}...")
        print(f"   Privacy: {privacy}")
        
        # Prepare video metadata
        body = {
            'snippet': {
                'title': title[:100],  # YouTube limit
                'description': description[:5000],  # YouTube limit
                'tags': keywords[:30],  # Max 30 tags
                'categoryId': category
            },
            'status': {
                'privacyStatus': privacy,
                'selfDeclaredMadeForKids': False
            }
        }
        
        # Prepare upload
        media = MediaFileUpload(
            str(video_file),
            chunksize=1024*1024,  # 1MB chunks
            resumable=True
        )
        
        try:
            # Execute upload
            request = self.youtube.videos().insert(
                part='snippet,status',
                body=body,
                media_body=media
            )
            
            response = None
            last_progress = 0
            
            while response is None:
                status, response = request.next_chunk()
                if status:
                    progress = int(status.progress() * 100)
                    if progress != last_progress:
                        print(f"   Upload progress: {progress}%")
                        last_progress = progress
            
            video_id = response['id']
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            
            print(f"\n✅ Upload successful!")
            print(f"   Video ID: {video_id}")
            print(f"   URL: {video_url}\n")
            
            return video_id
            
        except HttpError as e:
            print(f"\n❌ Upload failed: {e}")
            raise
    
    def set_thumbnail(self, video_id: str, thumbnail_file: Path):
        """Set custom thumbnail for video"""
        print(f"🖼️  Uploading thumbnail...")
        
        try:
            request = self.youtube.thumbnails().set(
                videoId=video_id,
                media_body=MediaFileUpload(str(thumbnail_file))
            )
            response = request.execute()
            print("✅ Thumbnail uploaded!\n")
            return response
        except HttpError as e:
            print(f"⚠️  Thumbnail upload failed: {e}\n")
    
    def update_video_details(self, video_id: str, title: str = None, 
                           description: str = None, keywords: list = None):
        """Update video details after upload"""
        if not any([title, description, keywords]):
            return
        
        print(f"📝 Updating video details...")
        
        # Get current video details
        response = self.youtube.videos().list(
            part='snippet',
            id=video_id
        ).execute()
        
        if not response['items']:
            print("❌ Video not found")
            return
        
        snippet = response['items'][0]['snippet']
        
        # Update fields
        if title:
            snippet['title'] = title
        if description:
            snippet['description'] = description
        if keywords:
            snippet['tags'] = keywords
        
        # Update video
        self.youtube.videos().update(
            part='snippet',
            body={
                'id': video_id,
                'snippet': snippet
            }
        ).execute()
        
        print("✅ Video details updated!\n")


def upload_to_youtube(video_file: Path, metadata_file: Path = None, 
                     privacy: str = "public") -> str:
    """
    Simple function to upload video with metadata
    
    Args:
        video_file: Path to MP4 file
        metadata_file: Optional JSON file with title, description, keywords
        privacy: public, private, or unlisted
    
    Returns:
        Video URL
    """
    
    # Load metadata
    if metadata_file and metadata_file.exists():
        with open(metadata_file, 'r') as f:
            metadata = json.load(f)
    else:
        # Generate from video filename
        title = video_file.stem.replace('_', ' ')[:100]
        metadata = {
            'title': title,
            'description': f"Video about {title}",
            'keywords': [title]
        }
    
    # Create uploader
    uploader = YouTubeUploader()
    uploader.authenticate()
    
    # Upload
    video_id = uploader.upload_video(
        video_file=video_file,
        title=metadata.get('title', 'Untitled Video'),
        description=metadata.get('description', ''),
        keywords=metadata.get('keywords', []),
        privacy=privacy
    )
    
    return f"https://www.youtube.com/watch?v={video_id}"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python youtube_uploader.py <video_file> [privacy]")
        print("Privacy options: public, private, unlisted (default: public)")
        sys.exit(1)
    
    video_path = Path(sys.argv[1])
    privacy = sys.argv[2] if len(sys.argv) > 2 else "public"
    
    if not video_path.exists():
        print(f"❌ Video file not found: {video_path}")
        sys.exit(1)
    
    # Look for metadata in same directory
    metadata_path = video_path.parent / "metadata.json"
    
    url = upload_to_youtube(video_path, metadata_path, privacy)
    print(f"🎉 Video live at: {url}")
