const { spawn } = require('child_process');
const readline = require('readline');

// DSRPTV — Meta Multi-Agent Coding OS
// by DSRPT.AI — https://dsrpt.ai
// GitHub: https://github.com/DSRPT/dsrptv
// Pinokio v7 Terminal Plugin

const BRAND = 'DSRPTV | dsrptv.co';
const BRAND_FULL = 'DSRPTV — META MULTI-AGENT CODING OS';
const OLLAMA_DEFAULT = 'http://localhost:11434';

const chalk = {
  cyan: (s) => `\x1b[36m${s}\x1b[0m`,
  green: (s) => `\x1b[32m${s}\x1b[0m`,
  yellow: (s) => `\x1b[33m${s}\x1b[0m`,
  red: (s) => `\x1b[31m${s}\x1b[0m`,
  bold: (s) => `\x1b[1m${s}\x1b[0m`,
  gray: (s) => `\x1b[90m${s}\x1b[0m`,
};

const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
const ask = (q) => new Promise((res) => rl.question(q, res));

function banner() {
  console.log(chalk.cyan('\n================================================================'));
  console.log(chalk.bold(chalk.cyan(`  ${BRAND_FULL}`)));
  console.log(chalk.gray('  Aider + LangGraph + Ollama + Voice + Browser UI'));
  console.log(chalk.gray('  Supervisor + Coder + Tester + Persistent Checkpointing'));
  console.log(chalk.cyan('================================================================'));
  console.log(chalk.gray(`  dsrptv.co | META MULTI-AGENT CODING OS`));
  console.log(chalk.gray(`  by DSRPT.AI — https://dsrpt.ai`));
  console.log(chalk.gray(`  GitHub: https://github.com/DSRPT/dsrptv`));
  console.log(chalk.cyan('================================================================\n'));
}

async function fetchModels(host) {
  return new Promise((resolve) => {
    const url = new URL('/api/tags', host);
    const http = require(url.protocol === 'https:' ? 'https' : 'http');
    let data = '';
    const req = http.get(url.href, (res) => {
      res.on('data', (chunk) => (data += chunk));
      res.on('end', () => {
        try {
          const parsed = JSON.parse(data);
          const models = (parsed.models || []).map((m) => m.name).sort();
          resolve(models.length ? models : []);
        } catch {
          resolve([]);
        }
      });
    });
    req.on('error', () => resolve([]));
    req.setTimeout(5000, () => { req.destroy(); resolve([]); });
  });
}

async function selectFromList(prompt, items, defaultIdx = 0) {
  items.forEach((item, i) => {
    const marker = i === defaultIdx ? chalk.green(' > ') : '   ';
    console.log(`${marker}${chalk.yellow(`${i + 1}.`)} ${item}`);
  });
  const ans = await ask(`\n${prompt} [1-${items.length}] (default ${defaultIdx + 1}): `);
  const idx = parseInt(ans) - 1;
  return (idx >= 0 && idx < items.length) ? items[idx] : items[defaultIdx];
}

async function main() {
  banner();

  // === OLLAMA HOST SETUP ===
  const savedHost = process.env.DSRPTV_HOST || OLLAMA_DEFAULT;
  console.log(chalk.gray(`Current Ollama host: ${savedHost}`));
  const changeHost = await ask('Use different Ollama host? [y/N]: ');
  let ollamaHost = savedHost;
  if (changeHost.toLowerCase() === 'y') {
    const input = await ask('Enter Ollama URL (e.g. http://192.168.1.100:11434): ');
    ollamaHost = input.trim() || savedHost;
  }

  // === FETCH MODELS ===
  console.log(chalk.gray(`\nFetching models from ${ollamaHost}...`));
  let models = await fetchModels(ollamaHost);
  const fallback = [
    'qwen2.5-coder:32b',
    'qwen3-coder:30b',
    'devstral:24b',
    'deepseek-coder-v2',
    'qwen2.5-coder:14b',
    'qwen2.5-coder:7b'
  ];
  if (!models.length) {
    console.log(chalk.yellow('  Could not fetch models — using recommended coding list'));
    models = fallback;
  }
  models.push('custom...');

  // === PRIMARY MODEL ===
  console.log(chalk.cyan('\n[ Primary Model — Architect/Agent brain ]'));
  let primary = await selectFromList('Select primary model', models, 0);
  if (primary === 'custom...') {
    primary = await ask('Enter model name: ');
  }

  // === EDITOR MODEL ===
  console.log(chalk.cyan('\n[ Editor Model — precision code edits ]'));
  const sameEditor = await ask('Same as primary? [Y/n]: ');
  let editor = primary;
  if (sameEditor.toLowerCase() === 'n') {
    editor = await selectFromList('Select editor model', models, 4);
    if (editor === 'custom...') editor = await ask('Enter model name: ');
  }

  // === AGENT MODE ===
  console.log(chalk.cyan('\n[ Agent Mode ]'));
  const modes = [
    '1. Meta Multi-Agent — LangGraph: Supervisor + Coder + Tester (durable)',
    '2. Native Agent — aider autonomous mode with --yes --map',
    '3. Architect — Two-model plan + execute (default)',
    '4. Voice-to-Code — Whisper input enabled',
    '5. Browser Web UI — Aider in browser',
    '6. Code Mode — Fast single-model editing',
    '7. Ask Mode — Questions only',
  ];
  const modeChoice = await selectFromList('Select agent mode', modes, 2);
  const modeIdx = parseInt(modeChoice[0]);

  // === EXTRAS ===
  console.log(chalk.cyan('\n[ Extras ]'));
  const enableVoice = await ask('Enable Voice Input (local Whisper)? [y/N]: ');
  const enableMemory = await ask('Enable Persistent Memory Bank? [Y/n]: ');
  const enableAutoTest = await ask('Enable Auto-Test loops? [y/N]: ');
  const enableLint = await ask('Enable Auto-Lint? [y/N]: ');
  const webUrls = await ask('Add web URLs/docs (comma-separated, or blank): ');

  rl.close();

  // === BUILD COMMAND ===
  const env = { ...process.env, OLLAMA_API_BASE: ollamaHost, DSRPTV_HOST: ollamaHost };
  
  console.log(chalk.cyan('\n================================================================'));
  console.log(chalk.bold(chalk.green(`  Launching DSRPTV with ${primary} @ ${ollamaHost}`)));
  console.log(chalk.gray(`  Editor: ${editor} | Mode: ${modeChoice.slice(3).trim()}`));
  console.log(chalk.cyan('================================================================\n'));

  // === LANGGRAPH META-AGENT MODE ===
  if (modeIdx === 1) {
    const proc = spawn('python', ['graph.py'], { stdio: 'inherit', env });
    proc.on('exit', code => process.exit(code || 0));
    return;
  }

  // === BUILD AIDER COMMAND ===
  let cmd = `aider --model ollama/${primary} --editor-model ollama/${editor}`;
  
  // Mode flags
  if (modeIdx === 2) {
    cmd += ' --yes --map'; // Native agent
  } else if (modeIdx === 3) {
    cmd += ' --architect --auto-accept-architect'; // Architect (default)
  } else if (modeIdx === 4) {
    cmd += ' --architect --voice'; // Voice
  } else if (modeIdx === 5) {
    cmd += ' --architect'; // Browser UI
  } else if (modeIdx === 6) {
    cmd += ''; // Code mode (fast)
  } else if (modeIdx === 7) {
    cmd += ' --ask'; // Ask mode
  } else {
    cmd += ' --architect --auto-accept-architect'; // Default fallback
  }

  // Additional flags
  if (enableVoice.toLowerCase() === 'y') cmd += ' --voice';
  if (enableMemory.toLowerCase() !== 'n') cmd += ' --message-history .dsrptv-memory.json';
  if (enableAutoTest.toLowerCase() === 'y') cmd += " --test-cmd 'pytest || npm test'";
  if (enableLint.toLowerCase() === 'y') cmd += " --lint-cmd 'ruff || eslint'";
  
  cmd += ' --yes --stream --map';

  // Add web URLs
  if (webUrls.trim()) {
    webUrls.split(',').map(u => u.trim()).filter(Boolean).forEach(u => {
      cmd += ` --read ${u}`;
    });
  }

  // System message
  cmd += ` --message "You are DSRPTV — built by DSRPT.AI (https://dsrpt.ai). An elite meta multi-agent coding partner. Be precise, proactive, and use best practices."`;

  const proc = spawn(cmd, { shell: true, stdio: 'inherit', env });
  proc.on('exit', code => process.exit(code || 0));
}

main().catch(err => {
  console.error(chalk.red('[ERROR]'), err.message);
  process.exit(1);
});
