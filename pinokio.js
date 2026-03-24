module.exports = {
  title: "DSRPTV | dsrptv.co",
  description: "META MULTI-AGENT CODING OS — Aider + LangGraph + Ollama + Voice + Browser UI. Fully local, fully private, fully yours.",
  icon: "icon.png",
  homepage: "https://dsrptv.co",
  menu: async (kernel, info) => {
    return [
      {
        text: "Launch DSRPTV",
        href: "launch.json",
      }
    ]
  }
}
