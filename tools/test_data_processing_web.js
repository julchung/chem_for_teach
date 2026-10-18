#!/usr/bin/env node
const { spawn } = require('child_process');
const fs = require('fs');
const http = require('http');
const path = require('path');
const os = require('os');

const chromePath = '/Users/julchung/.cache/puppeteer/chrome/mac_arm-155.0.8059.39/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing';
const pagesToTest = [
  'index.html',
  'lab01_millikan_oil_drop.html',
  'lab02_spectrophotometry_beer_law.html',
  'lab03_ionization_energy_log.html',
  'lab04_precipitation_stoichiometry.html',
  'lab05_protein_electrophoresis.html'
];

const tempUserDataDir = fs.mkdtempSync(path.join(os.tmpdir(), 'chrome-test-web-'));
const port = 9400 + Math.floor(Math.random() * 500);

let chromeProc = null;
let ws = null;

function cleanup() {
  if (ws) {
    try { ws.close(); } catch (e) {}
    ws = null;
  }
  if (chromeProc && chromeProc.pid) {
    try {
      process.kill(-chromeProc.pid, 'SIGKILL');
    } catch (e) {
      try { chromeProc.kill('SIGKILL'); } catch (err) {}
    }
    chromeProc = null;
  }
  try {
    fs.rmSync(tempUserDataDir, { recursive: true, force: true });
  } catch (e) {}
}

process.on('exit', cleanup);
process.on('SIGINT', () => { cleanup(); process.exit(1); });
process.on('SIGTERM', () => { cleanup(); process.exit(1); });
process.on('uncaughtException', (err) => {
  console.error("Uncaught exception:", err);
  cleanup();
  process.exit(1);
});

async function run() {
  chromeProc = spawn(chromePath, [
    '--headless=new',
    '--disable-gpu',
    '--no-sandbox',
    '--disable-dev-shm-usage',
    `--remote-debugging-port=${port}`,
    `--user-data-dir=${tempUserDataDir}`,
    'about:blank'
  ], { detached: true });

  await new Promise((res, rej) => {
    let retries = 0;
    const check = () => {
      http.get(`http://127.0.0.1:${port}/json/version`, (r) => {
        let body = '';
        r.on('data', d => body += d);
        r.on('end', () => {
          try {
            res(JSON.parse(body).webSocketDebuggerUrl);
          } catch(e) { setTimeout(check, 100); }
        });
      }).on('error', () => {
        if (++retries > 30) return rej(new Error("Chrome launch timeout"));
        setTimeout(check, 100);
      });
    };
    check();
  });

  const targets = await new Promise((res, rej) => {
    http.get(`http://127.0.0.1:${port}/json`, (r) => {
      let b = '';
      r.on('data', d => b += d);
      r.on('end', () => res(JSON.parse(b)));
    }).on('error', rej);
  });

  const pageTarget = targets.find(t => t.type === 'page');
  ws = new WebSocket(pageTarget.webSocketDebuggerUrl);

  await new Promise((res, rej) => {
    ws.onopen = res;
    ws.onerror = rej;
  });

  let idCounter = 1;
  const callbacks = new Map();
  let currentErrors = [];

  ws.onmessage = (event) => {
    const msg = JSON.parse(event.data);
    if (msg.method === 'Runtime.consoleAPICalled' && msg.params.type === 'error') {
      currentErrors.push(msg.params.args.map(a => a.value || a.description).join(' '));
    }
    if (msg.id && callbacks.has(msg.id)) {
      const cb = callbacks.get(msg.id);
      callbacks.delete(msg.id);
      cb(msg.result);
    }
  };

  const send = (method, params = {}) => new Promise((res) => {
    const id = idCounter++;
    callbacks.set(id, res);
    ws.send(JSON.stringify({ id, method, params }));
  });

  await send('Runtime.enable');
  await send('Page.enable');

  let allPassed = true;

  for (const pageFile of pagesToTest) {
    const fullPath = path.resolve(__dirname, '../antigravity_數據處理', pageFile);
    const fileUrl = 'file://' + fullPath;
    currentErrors = [];

    await send('Page.navigate', { url: fileUrl });
    await new Promise(r => setTimeout(r, 600));

    const evalRes = await send('Runtime.evaluate', {
      expression: `(() => ({
        title: document.title,
        canvasCount: document.querySelectorAll('canvas').length,
        buttonsCount: document.querySelectorAll('button').length,
        bodyLen: document.body.innerText.length
      }))()`,
      returnByValue: true
    });

    const val = evalRes.result ? evalRes.result.value : null;
    if (currentErrors.length > 0) {
      console.error(`❌ [${pageFile}] Error:`, currentErrors);
      allPassed = false;
    } else {
      console.log(`✅ [${pageFile}] OK! Title: "${val.title}", Canvases: ${val.canvasCount}, Buttons: ${val.buttonsCount}, TextLen: ${val.bodyLen}`);
    }
  }

  cleanup();
  process.exit(allPassed ? 0 : 1);
}

run();
