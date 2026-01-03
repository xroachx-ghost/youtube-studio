#!/usr/bin/env bash
# Simple launcher to choose CLI or GUI for YouTube Studio Generator
set -e

echo "==============================="
echo " YouTube Studio Generator"
echo "==============================="
echo "1) CLI"
echo "2) GUI"
read -rp "Select mode (1/2): " MODE

if [[ "$MODE" == "2" ]]; then
  echo "Launching GUI..."
  exec python video_generator_gui.py
fi

# CLI flow
echo "Choose generator:"
echo "1) Free (main_free.py)"
echo "2) Premium Free (main_premium_free.py)"
echo "3) Ultimate Free (main_ultimate_free.py)"
read -rp "Select (1/2/3): " GEN

case "$GEN" in
  2) SCRIPT="main_premium_free.py" ;;
  3) SCRIPT="main_ultimate_free.py" ;;
  *) SCRIPT="main_free.py" ;;
esac

read -rp "Topic: " TOPIC
TOPIC=${TOPIC:-"The Future of AI"}

echo "Launching CLI generator ($SCRIPT) with topic: $TOPIC"
exec python "$SCRIPT" "$TOPIC"
