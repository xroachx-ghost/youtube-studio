#!/bin/bash
# Automated setup script for ALL premium free tools

echo "╔════════════════════════════════════════════════════════╗"
echo "║  PREMIUM FREE SETUP - Automated Installation          ║"
echo "║  Sets up: Ollama + ElevenLabs + Pexels + Pixabay     ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Check root for some installations
if [ "$EUID" -eq 0 ]; then 
    echo -e "${RED}❌ Don't run as root. Run as normal user.${NC}"
    exit 1
fi

echo -e "${YELLOW}📦 Step 1/5: Installing system dependencies...${NC}"
sudo apt update -qq
sudo apt install -y ffmpeg python3-pip curl > /dev/null 2>&1
echo -e "${GREEN}✅ System dependencies installed${NC}\n"

echo -e "${YELLOW}📦 Step 2/5: Installing Python packages...${NC}"
pip3 install -q gtts requests
echo -e "${GREEN}✅ Python packages installed${NC}\n"

echo -e "${YELLOW}🤖 Step 3/5: Installing Ollama (Local AI)...${NC}"
if command -v ollama &> /dev/null; then
    echo -e "${GREEN}✅ Ollama already installed${NC}\n"
else
    echo "   This may take 2-3 minutes..."
    curl -fsSL https://ollama.com/install.sh | sh
    echo -e "${GREEN}✅ Ollama installed${NC}\n"
fi

echo -e "${YELLOW}📥 Step 4/5: Downloading Llama 2 model...${NC}"
echo "   This may take 5-10 minutes (4GB download)..."
ollama pull llama2 > /dev/null 2>&1 &
OLLAMA_PID=$!

# Start Ollama server in background
ollama serve > /dev/null 2>&1 &
sleep 2

# Wait for download
wait $OLLAMA_PID
echo -e "${GREEN}✅ Llama 2 model downloaded${NC}\n"

echo -e "${YELLOW}🔑 Step 5/5: Setting up API keys...${NC}"
echo ""
echo "Now you need to get FREE API keys (takes 5 minutes total):"
echo ""

# ElevenLabs
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}1. ElevenLabs (Best Free Voice)${NC}"
echo "   → Visit: https://elevenlabs.io"
echo "   → Sign up (free, no credit card)"
echo "   → Go to Profile → API Key"
echo "   → Copy your key"
echo ""
read -p "   Paste your ElevenLabs API key (or press Enter to skip): " elevenlabs_key
if [ ! -z "$elevenlabs_key" ]; then
    echo "export ELEVENLABS_API_KEY='$elevenlabs_key'" >> ~/.bashrc
    export ELEVENLABS_API_KEY="$elevenlabs_key"
    echo -e "   ${GREEN}✅ ElevenLabs configured${NC}"
else
    echo -e "   ${YELLOW}⚠️  Skipped - will use gTTS voice${NC}"
fi
echo ""

# Pexels
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}2. Pexels (Free HD Videos)${NC}"
echo "   → Visit: https://www.pexels.com/api/"
echo "   → Click 'Get Started'"
echo "   → Sign up (30 seconds)"
echo "   → Copy your API key"
echo ""
read -p "   Paste your Pexels API key (or press Enter to skip): " pexels_key
if [ ! -z "$pexels_key" ]; then
    echo "export PEXELS_API_KEY='$pexels_key'" >> ~/.bashrc
    export PEXELS_API_KEY="$pexels_key"
    echo -e "   ${GREEN}✅ Pexels configured${NC}"
else
    echo -e "   ${YELLOW}⚠️  Skipped - will use generated backgrounds${NC}"
fi
echo ""

# Pixabay
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}3. Pixabay (Extra Video Source)${NC}"
echo "   → Visit: https://pixabay.com/api/docs/"
echo "   → Sign up"
echo "   → Get your API key"
echo ""
read -p "   Paste your Pixabay API key (or press Enter to skip): " pixabay_key
if [ ! -z "$pixabay_key" ]; then
    echo "export PIXABAY_API_KEY='$pixabay_key'" >> ~/.bashrc
    export PIXABAY_API_KEY="$pixabay_key"
    echo -e "   ${GREEN}✅ Pixabay configured${NC}"
else
    echo -e "   ${YELLOW}⚠️  Skipped - optional${NC}"
fi
echo ""

echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${GREEN}✅ Setup complete!${NC}"
echo ""
echo "📊 Your configuration:"
echo ""

# Show status
if [ ! -z "$elevenlabs_key" ]; then
    echo -e "  ✅ ElevenLabs: ${GREEN}Configured${NC} (Premium voice)"
else
    echo -e "  ⚠️  ElevenLabs: ${YELLOW}Not set${NC} (will use gTTS)"
fi

if [ ! -z "$pexels_key" ]; then
    echo -e "  ✅ Pexels: ${GREEN}Configured${NC} (HD videos)"
else
    echo -e "  ⚠️  Pexels: ${YELLOW}Not set${NC} (will use backgrounds)"
fi

if [ ! -z "$pixabay_key" ]; then
    echo -e "  ✅ Pixabay: ${GREEN}Configured${NC} (Extra videos)"
else
    echo -e "  ℹ️  Pixabay: ${YELLOW}Not set${NC} (optional)"
fi

echo -e "  ✅ Ollama: ${GREEN}Running${NC} (AI scripts)"
echo ""
echo "🎬 Ready to create videos!"
echo ""
echo "Usage:"
echo "  python3 main_premium_free.py 'Your Video Topic'"
echo ""
echo "Example:"
echo "  python3 main_premium_free.py 'The Future of AI'"
echo ""
echo "💡 Tip: Reload your terminal or run 'source ~/.bashrc' to use new keys"
echo ""
