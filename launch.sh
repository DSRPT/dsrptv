#!/bin/bash
# =============================================================
# DSRPTV | dsrptv.co
# Meta Multi-Agent Coding OS
# Aider + LangGraph + Ollama + Voice + Browser UI
# =============================================================

echo ""
echo "  ██████╗ ███████╗██████╗ ██████╗ ████████╗██╗   ██╗"
echo "  ██╔══██╗██╔════╝██╔══██╗██╔══██╗╚══██╔══╝██║   ██║"
echo "  ██║  ██║███████╗██████╔╝██████╔╝   ██║   ██║   ██║"
echo "  ██║  ██║╚════██║██╔══██╗██╔═══╝    ██║   ╚██╗ ██╔╝"
echo "  ██████╔╝███████║██║  ██║██║        ██║    ╚████╔╝ "
echo "  ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝        ╚═╝     ╚═══╝  "
echo ""
echo "  dsrptv.co | META MULTI-AGENT CODING OS"
echo "  Powered by Aider + LangGraph + Ollama"
echo "============================================================="
echo ""

# ---- Persistent Config ----
CONFIG="$HOME/.dsrptv.config"
if [ -f "$CONFIG" ]; then
  source "$CONFIG"
  echo "[CONFIG] Loaded saved config: Host=$OLLAMA_HOST | Model=$LAST_MODEL"
else
  echo "[FIRST RUN] Setting up DSRPTV..."
  read -p "Use Local or Remote Ollama? [L/r] " choice
  if [[ "$choice" =~ ^[Rr]$ ]]; then
    read -p "Enter remote Ollama URL (e.g. http://192.168.1.100:11434): " OLLAMA_HOST
  else
    OLLAMA_HOST="http://localhost:11434"
  fi
  echo "OLLAMA_HOST=$OLLAMA_HOST" > "$CONFIG"
  echo "[CONFIG] Saved to $CONFIG"
fi

# ---- Auto-start local Ollama if needed ----
if [[ "$OLLAMA_HOST" == *"localhost"* ]]; then
  if ! pgrep -x ollama > /dev/null; then
    echo "[OLLAMA] Starting Ollama in background..."
    ollama serve > /dev/null 2>&1 &
    sleep 3
  fi
fi

# ---- Auto-install dependencies ----
echo ""
echo "[DEPS] Checking dependencies..."

# Python / aider-chat
if ! command -v aider > /dev/null 2>&1; then
  echo "[DEPS] Installing Aider CLI (one-time)..."
  python -m pip install -U aider-chat
fi

# aider-desk (native agent mode fork)
if ! command -v aider-desk > /dev/null 2>&1; then
  echo "[DEPS] Installing aider-desk (native Agent Mode)..."
  pip install git+https://github.com/hotovo/aider-desk.git 2>/dev/null || echo "[WARN] aider-desk unavailable, using standard aider"
fi

# LangGraph + dependencies
python -c "import langgraph" 2>/dev/null || pip install langgraph langchain-community langchain-ollama

# Node.js dependencies for menu
if [ -f "package.json" ]; then
  npm install --silent 2>/dev/null
else
  npm install --silent inquirer chalk 2>/dev/null
fi

# faster-whisper for voice
python -c "import faster_whisper" 2>/dev/null || pip install faster-whisper

echo "[DEPS] All dependencies ready."
echo ""

# ---- Fetch available models from Ollama ----
echo "[MODELS] Fetching models from $OLLAMA_HOST..."
MODELS=$(curl -s "$OLLAMA_HOST/api/tags" 2>/dev/null | grep -o '"name":"[^"]*"' | cut -d'"' -f4 | sort)

if [ -z "$MODELS" ]; then
  echo "[WARN] Could not fetch models from $OLLAMA_HOST. Using curated defaults."
  MODELS="qwen2.5-coder:32b qwen2.5-coder:14b qwen3-coder:30b devstral:24b deepseek-coder-v2 llama3.3:70b qwen2.5-coder:7b custom"
fi

# ---- Launch interactive Node.js menu ----
node .menu.js "$OLLAMA_HOST" "$MODELS" "$LAST_MODEL"
