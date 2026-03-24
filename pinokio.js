/**
 * DSRPTV | dsrptv.co
 * by DSRPT.AI — https://dsrpt.ai
 *
 * Meta Multi-Agent Coding OS
 * Aider + LangGraph + Ollama + Voice + Browser UI
 * Supervisor + Coder + Tester + Persistent Checkpointing
 *
 * Pinokio v7 Terminal Plugin
 * GitHub: https://github.com/DSRPT/dsrptv
 */

module.exports = {
  title: "DSRPTV | dsrptv.co",
  description: "by DSRPT.AI — Aider-powered meta multi-agent coding OS. Ollama model picker, Architect + Agent + Voice modes, LangGraph orchestration, persistent memory.",
  icon: "icon.png",
  homepage: "https://dsrptv.co",

  // Env vars prompted on first run (saved per-machine)
  env: [{
    key: "OLLAMA_API_BASE",
    description: "Ollama host URL (local or remote)",
    default: "http://localhost:11434"
  }, {
    key: "DSRPTV_MODEL",
    description: "Primary Aider model (e.g. ollama/qwen2.5-coder:32b, ollama/devstral:24b)",
    default: "ollama/qwen2.5-coder:14b"
  }, {
    key: "DSRPTV_EDITOR_MODEL",
    description: "Editor model for Aider Architect mode (can be same or smaller/faster)",
    default: "ollama/qwen2.5-coder:14b"
  }, {
    key: "DSRPTV_MODE",
    description: "Agent mode: architect | agent | code | ask | voice | browser",
    default: "architect"
  }],

  run: [
    // ── Step 1: Install aider-chat (one-time, skips if already installed) ──
    {
      when: "{{platform === 'win32'}}",
      id: "install",
      method: "shell.run",
      params: {
        shell: "{{kernel.path('bin/miniconda/Library/bin/bash.exe')}}",
        conda: { skip: true },
        message: "pip install -q aider-chat langgraph langchain-community langchain-ollama 2>/dev/null || true",
        path: "{{env.path}}"
      }
    },
    {
      when: "{{platform !== 'win32'}}",
      id: "install",
      method: "shell.run",
      params: {
        message: "pip install -q aider-chat langgraph langchain-community langchain-ollama 2>/dev/null || true",
        path: "{{env.path}}"
      }
    },

    // ── Step 2: Launch DSRPTV in the target project directory ──
    {
      when: "{{platform === 'win32'}}",
      id: "run",
      method: "shell.run",
      params: {
        shell: "{{kernel.path('bin/miniconda/Library/bin/bash.exe')}}",
        conda: { skip: true },
        env: {
          OLLAMA_API_BASE: "{{env.OLLAMA_API_BASE}}",
          DSRPTV_MODEL: "{{env.DSRPTV_MODEL}}",
          DSRPTV_EDITOR_MODEL: "{{env.DSRPTV_EDITOR_MODEL}}",
          DSRPTV_MODE: "{{env.DSRPTV_MODE}}"
        },
        message: [
          "echo ''",
          "echo '================================================================'",
          "echo ' DSRPTV | dsrptv.co  —  META MULTI-AGENT CODING OS'",
          "echo ' by DSRPT.AI — https://dsrpt.ai'",
          "echo ' GitHub: https://github.com/DSRPT/dsrptv'",
          "echo '================================================================'",
          "echo ' Model  : '\"$DSRPTV_MODEL\"",
          "echo ' Editor : '\"$DSRPTV_EDITOR_MODEL\"",
          "echo ' Mode   : '\"$DSRPTV_MODE\"",
          "echo ' Ollama : '\"$OLLAMA_API_BASE\"",
          "echo '================================================================'",
          "echo ''",
          "aider --model \"$DSRPTV_MODEL\" --editor-model \"$DSRPTV_EDITOR_MODEL\" --architect --auto-accept-architect --yes --stream --map --message-history .dsrptv-memory.json {{args.prompt ? '--message ' + JSON.stringify(args.prompt) : ''}}"
        ].join("\n"),
        path: "{{args.cwd}}",
        input: true,
        buffer: 16384
      }
    },
    {
      when: "{{platform !== 'win32'}}",
      id: "run",
      method: "shell.run",
      params: {
        env: {
          OLLAMA_API_BASE: "{{env.OLLAMA_API_BASE}}",
          DSRPTV_MODEL: "{{env.DSRPTV_MODEL}}",
          DSRPTV_EDITOR_MODEL: "{{env.DSRPTV_EDITOR_MODEL}}",
          DSRPTV_MODE: "{{env.DSRPTV_MODE}}"
        },
        message: [
          "echo ''",
          "echo '================================================================'",
          "echo ' DSRPTV | dsrptv.co  —  META MULTI-AGENT CODING OS'",
          "echo ' by DSRPT.AI — https://dsrpt.ai'",
          "echo ' GitHub: https://github.com/DSRPT/dsrptv'",
          "echo '================================================================'",
          "echo \" Model  : $DSRPTV_MODEL\"",
          "echo \" Editor : $DSRPTV_EDITOR_MODEL\"",
          "echo \" Mode   : $DSRPTV_MODE\"",
          "echo \" Ollama : $OLLAMA_API_BASE\"",
          "echo '================================================================'",
          "echo ''",
          "aider --model \"$DSRPTV_MODEL\" --editor-model \"$DSRPTV_EDITOR_MODEL\" --architect --auto-accept-architect --yes --stream --map --message-history .dsrptv-memory.json {{args.prompt ? '\"--message\" \"' + args.prompt + '\"' : ''}}"
        ].join("\n"),
        path: "{{args.cwd}}",
        input: true,
        buffer: 16384
      }
    }
  ]
}
