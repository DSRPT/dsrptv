#!/bin/bash
# =============================================================
# DSRPTV | dsrptv.co
# by DSRPT.AI — https://dsrpt.ai
#
# Meta Multi-Agent Coding OS
# Aider + LangGraph + Ollama + Voice + Browser UI
# Supervisor + Coder + Tester + Persistent Checkpointing
#
# Pinokio v7 Terminal Plugin
# GitHub: https://github.com/DSRPT/dsrptv
# =============================================================

echo ""
echo "  ██████╗ ███████╗██████╗ ██████╗ ████████╗██╗   ██╗"
echo "  ██╔══██╗██╔════╝██╔══██╗██╔══██╗╚══██╔══╝██║   ██║"
echo "  ██║  ██║███████╗██████╔╝██████╔╝   ██║   ██║   ██║"
echo "  ██║  ██║╚════██║██╔══██╗██╔═══╝    ██║   ╚██╗ ██╔╝"
echo "  ██████╔╝███████║██║  ██║██║        ██║    ╚████╔╝ "
echo "  ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝        ╚═╝     ╚═══╝  "
echo ""
echo "  dsrptv.co  |  META MULTI-AGENT CODING OS"
echo "  by DSRPT.AI — https://dsrpt.ai"
echo "  GitHub: https://github.com/DSRPT/dsrptv"
echo "============================================================="
echo ""

# ---- Auto-install Node.js for beautiful menu ----
if ! command -v node > /dev/null 2>&1; then
  echo "[NODE] Installing Node.js..."
  curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && apt-get install -y nodejs || brew install node || echo "[WARN] Please install Node.js manually from https://nodejs.org"
fi

# ---- Auto-install Node.js menu dependencies ----
if [ ! -d "node_modules" ]; then
  echo "[DEPS] Installing Node.js dependencies (inquirer, chalk)..."
  npm install --silent 2>/dev/null || npm install inquirer chalk --silent
fi

# ---- Auto-install Python dependencies (one-time) ----
echo "[DEPS] Checking Python dependencies..."
pip install -q langgraph langchain-community langchain-ollama faster-whisper pyttsx3 aider-chat || true

# ---- Auto-install aider-desk fork for native Agent Mode ----
if ! command -v aider-desk > /dev/null 2>&1; then
  echo "[DEPS] Installing aider-desk (native autonomous Agent Mode)..."
  pip install -q git+https://github.com/hotovo/aider-desk.git 2>/dev/null || echo "[WARN] aider-desk unavailable, standard aider will be used"
fi

echo "[DEPS] All dependencies ready."
echo ""

# ---- Launch interactive Node.js menu ----
node ./menu.js
