module.exports = {
  title: "DSRPTV | dsrptv.co",
  description: "META MULTI-AGENT OS with LangGraph — Supervisor + Coder + Tester + Persistent Checkpointing + Visual Traces",
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
