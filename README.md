# DSRPTV | dsrptv.co

**Meta Multi-Agent Coding OS**  
*by [DSRPT.AI](https://dsrpt.ai)*

> **Claude Code CLI, but more feature-rich.**  
> Aider + LangGraph + Ollama + Voice + Browser UI  
> Fully branded Pinokio v7 Terminal Plugin

---

## ⚡ What is DSRPTV?

DSRPTV is a **production-grade meta multi-agent coding system** designed to function like Claude Code CLI but with significantly more features:

- 🧠 **LangGraph Multi-Agent Core**: Supervisor → Coder (Aider) → Tester → Loop with persistent SQLite checkpointing
- 🏛️ **Architect Mode**: Two-model planning + execution (plan with primary, edit with editor model)
- 🎙️ **Voice Input**: Local Whisper integration for voice-to-code
- 🌐 **Web UI**: Aider browser interface (always enabled by default)
- 📊 **Auto-Test + Lint**: Pytest/npm test + ruff/eslint loops
- 💾 **Persistent Memory**: Chat history + checkpoint recovery
- 🤖 **Ollama Model Picker**: Interactive menu to select primary + editor models from your local/remote Ollama instance
- 🚀 **Windows Compatible**: Direct Windows bash path support via Pinokio kernel

---

## 📦 Installation

### Option 1: Pinokio (Recommended)

1. Open [Pinokio](https://pinokio.computer/)
2. Go to **Plugins** → **Install**
3. Enter: `https://github.com/DSRPT/dsrptv`
4. Select your target project directory
5. DSRPTV will auto-install dependencies and launch

### Option 2: Manual

```bash
git clone https://github.com/DSRPT/dsrptv.git
cd dsrptv
pip install aider-chat langgraph langchain-community langchain-ollama

# Interactive menu launcher
node menu.js

# OR direct LangGraph meta-agent
python graph.py

# OR direct aider launch
bash launch.sh
```

---

## 🔧 Usage

### Pinokio Plugin Mode

After installation, DSRPTV appears in your Pinokio Plugins list:

1. **Click DSRPTV** → Select target project
2. **Choose environment variables** (prompted on first run):
   - `OLLAMA_API_BASE`: Local (`http://localhost:11434`) or remote Ollama server
   - `DSRPTV_MODEL`: Primary model (e.g., `ollama/qwen2.5-coder:32b`)
   - `DSRPTV_EDITOR_MODEL`: Editor model (e.g., `ollama/qwen2.5-coder:14b`)
   - `DSRPTV_MODE`: `architect` | `agent` | `code` | `ask` | `voice` | `browser`
3. **DSRPTV launches** directly in your project with Aider Architect mode

### Interactive Menu (`menu.js`)

Run `node menu.js` for a full interactive setup:

- **Ollama Host**: Configure local or remote server
- **Model Selection**: Live-fetch models from Ollama or use recommended list
- **Primary + Editor Models**: Pick separate models or use same for both
- **Agent Mode**:
  1. **Meta Multi-Agent** — LangGraph: Supervisor + Coder + Tester (durable checkpointing)
  2. **Native Agent** — aider `--yes --map` autonomous mode
  3. **Architect** — Two-model plan + execute (default)
  4. **Voice-to-Code** — Whisper input enabled
  5. **Browser Web UI** — Aider in browser
  6. **Code Mode** — Fast single-model editing
  7. **Ask Mode** — Questions only
- **Extras**: Voice, persistent memory, auto-test, auto-lint, web URL ingestion

### LangGraph Meta-Agent (`graph.py`)

Run `python graph.py` for the **Supervisor → Coder → Tester** loop:

```
================================================================
  DSRPTV | dsrptv.co — META MULTI-AGENT CODING OS
  by DSRPT.AI — https://dsrpt.ai
  GitHub: https://github.com/DSRPT/dsrptv
================================================================
  LangGraph Meta-Agent Core
  Ollama: http://localhost:11434
  Primary: qwen2.5-coder:32b
  Editor: qwen2.5-coder:14b
  CWD: /your/project
================================================================

[DSRPTV] LangGraph Meta-Agent Ready.
[DSRPTV] Persistent memory: ~/.dsrptv_memory.db
[DSRPTV] Type your coding task below (or 'exit'):

You: add a login route to app.py with JWT authentication

[SUPERVISOR] Analyzing task (iteration 0/5)...
[SUPERVISOR] Routing to CODER

[CODER] Running Aider to implement code changes...
[CODER] Aider succeeded.

[SUPERVISOR] Routing to TESTER

[TESTER] Running tests and lint...
[TESTER] pytest passed.
[TESTER] ruff passed.

[SUPERVISOR] Code applied and tests passed. Task complete.

[DSRPTV] Task complete. State persisted to ~/.dsrptv_memory.db
```

### Direct Aider Launch (`launch.sh`)

Run `bash launch.sh` for immediate Aider Architect mode with DSRPTV branding:

```bash
================================================================
  DSRPTV | dsrptv.co — META MULTI-AGENT CODING OS
  by DSRPT.AI — https://dsrpt.ai
  GitHub: https://github.com/DSRPT/dsrptv
================================================================
  Model: ollama/qwen2.5-coder:32b
  Editor: ollama/qwen2.5-coder:14b
  Mode: architect
  Ollama: http://localhost:11434
================================================================

aider --model ollama/qwen2.5-coder:32b --editor-model ollama/qwen2.5-coder:14b --architect --auto-accept-architect --yes --stream --map --message-history .dsrptv-memory.json
```

---

## 🎯 Features Comparison

| Feature | Claude Code CLI | DSRPTV |
|---------|----------------|--------|
| **Terminal Interface** | ✔️ | ✔️ |
| **Architect Mode** | ✔️ (single model) | ✔️ (dual model: primary + editor) |
| **Autonomous Agent** | ✔️ | ✔️ |
| **LangGraph Multi-Agent** | ❌ | ✔️ (Supervisor + Coder + Tester) |
| **Persistent Checkpointing** | ❌ | ✔️ (SQLite) |
| **Ollama Support** | ❌ | ✔️ (local + remote) |
| **Model Picker** | ❌ | ✔️ (interactive) |
| **Voice Input** | ❌ | ✔️ (local Whisper) |
| **Auto-Test + Lint Loops** | ❌ | ✔️ (pytest/npm, ruff/eslint) |
| **Web URL Ingestion** | ✔️ | ✔️ |
| **Pinokio Plugin** | ❌ | ✔️ (fully integrated) |
| **Windows Support** | Limited | ✔️ (native bash path) |
| **Open Source** | ❌ | ✔️ |

---

## 📁 Repository Structure

```
DSRPT/dsrptv/
├── README.md          # This file
├── pinokio.js         # Pinokio v7 Terminal Plugin config
├── launch.sh          # Direct Aider launcher with DSRPTV branding
├── menu.js            # Interactive Node.js launcher (Ollama picker, mode selection, extras)
├── graph.py           # LangGraph meta-agent core (Supervisor + Coder + Tester)
└── icon.png           # DSRPTV icon (optional)
```

---

## 🧩 Architecture

### 1. Pinokio v7 Plugin (`pinokio.js`)

- **Env Prompts**: First-run config for Ollama host, models, mode
- **Windows Bash**: Direct kernel path to `miniconda/Library/bin/bash.exe`
- **Auto-Install**: `pip install aider-chat langgraph ...` on first run
- **Direct Launch**: Executes aider in target project (`{{args.cwd}}`)

### 2. Interactive Menu (`menu.js`)

- **Ollama API**: Fetches live model list from `/api/tags`
- **Model Selection**: Numbered menu with defaults
- **7 Agent Modes**: Meta multi-agent, native agent, architect, voice, browser, code, ask
- **Extras**: Voice, memory, auto-test, auto-lint, web URLs
- **Command Builder**: Constructs full `aider` command with all flags

### 3. LangGraph Meta-Agent (`graph.py`)

**StateGraph Workflow**:

```
      START
        ↓
   [SUPERVISOR]
        │
    ┌───┼───┐
    │       │
 [CODER] [TESTER]
    │       │
    └───┬───┘
        │
   [SUPERVISOR]
        ↓
    FINISH/LOOP
```

- **Supervisor Node**: Routes to coder/tester based on `code_applied` and `tests_passed` state
- **Coder Node**: Runs `aider --model ollama/{EDITOR_MODEL} --yes --auto-commits --message "{task}"`
- **Tester Node**: Runs `pytest` + `ruff`, updates state
- **Checkpointing**: SqliteSaver persists state to `~/.dsrptv_memory.db`
- **Max Iterations**: 5 (configurable)

### 4. Direct Launcher (`launch.sh`)

- **ASCII Banner**: DSRPTV branding
- **Auto-Install**: Checks for aider, installs if missing
- **Direct Exec**: `aider --architect --auto-accept-architect ...`

---

## 👥 Credits

**Built by [DSRPT.AI](https://dsrpt.ai)**  
**Website**: [dsrptv.co](https://dsrptv.co)  
**GitHub**: [DSRPT/dsrptv](https://github.com/DSRPT/dsrptv)

### Powered By

- [Aider](https://github.com/paul-gauthier/aider) — AI pair programming in terminal
- [LangGraph](https://github.com/langchain-ai/langgraph) — Multi-agent orchestration
- [Ollama](https://ollama.com/) — Local LLM inference
- [Pinokio](https://pinokio.computer/) — One-click AI app launcher

---

## 📜 License

MIT License - see [LICENSE](LICENSE) for details.

---

## 🔗 Links

- **Website**: [dsrptv.co](https://dsrptv.co)
- **DSRPT.AI**: [dsrpt.ai](https://dsrpt.ai)
- **GitHub**: [DSRPT/dsrptv](https://github.com/DSRPT/dsrptv)
- **Issues**: [Report a bug](https://github.com/DSRPT/dsrptv/issues)
