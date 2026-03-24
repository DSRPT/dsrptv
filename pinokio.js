/**
 * DSRPTV | dsrptv.co
 * by DSRPT.AI — https://dsrpt.ai
 *
 * Meta Multi-Agent Coding OS
 * Aider + LangGraph + Ollama + Voice + Browser UI
 * Supervisor + Coder + Tester + Persistent Checkpointing + Visual Traces
 *
 * Pinokio v7 Terminal Plugin
 * GitHub: https://github.com/DSRPT/dsrptv
 */

module.exports = {
  title: "DSRPTV | dsrptv.co",
  description: "by DSRPT.AI — Meta Multi-Agent Coding OS: LangGraph + Aider + Ollama. Supervisor + Coder + Tester + Persistent Checkpointing + Visual Traces.",
  icon: "icon.png",
  homepage: "https://dsrptv.co",
  run: [{
    method: "shell.run",
    params: {
      message: "bash ./launch.sh",
      path: "{{args.cwd}}",
      input: true,
      buffer: 16384
    }
  }]
}
