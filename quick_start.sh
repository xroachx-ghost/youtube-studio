#!/bin/bash
# Quick start script for YouTube Video Generator

echo "╔══════════════════════════════════════════════════════════╗"
echo "║     YOUTUBE VIDEO GENERATOR - QUICK START               ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Please install Python 3.8+"
    exit 1
fi

# Check if ffmpeg is installed
if ! command -v ffmpeg &> /dev/null; then
    echo "❌ FFmpeg not found. Installing..."
    sudo apt update && sudo apt install -y ffmpeg
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Check for API key
if [ -z "$OPENAI_API_KEY" ]; then
    echo ""
    echo "⚠️  OPENAI_API_KEY not set!"
    echo ""
    echo "Please set your OpenAI API key:"
    echo "  export OPENAI_API_KEY='sk-your-key-here'"
    echo ""
    echo "Or create a .env file with your key."
    echo ""
    exit 1
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Usage examples:"
echo "  python main.py 'Your video topic here'"
echo "  python main.py 'Top 10 AI Tools for 2025'"
echo ""
echo "🎬 Ready to create amazing videos!"
echo ""
