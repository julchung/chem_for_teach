#!/usr/bin/env node
/**
 * safe_html_to_pdf.js
 * Bulletproof HTML to PDF generator using headless Chrome.
 * Guarantees NO zombie / orphaned Chrome Helper processes.
 */
const { spawn } = require('child_process');
const fs = require('fs');
const http = require('http');
const path = require('path');
const os = require('os');

const chromePath = '/Users/julchung/.cache/puppeteer/chrome/mac_arm-155.0.8059.39/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing';

const htmlPath = process.argv[2];
const pdfPath = process.argv[3];

if (!htmlPath || !pdfPath) {
  console.error("Usage: node safe_html_to_pdf.js <input.html> <output.pdf>");
  process.exit(1);
}

const fileUrl = 'file://' + (path.isAbsolute(htmlPath) ? htmlPath : path.resolve(process.cwd(), htmlPath));
const absPdfPath = path.isAbsolute(pdfPath) ? pdfPath : path.resolve(process.cwd(), pdfPath);

const tempUserDataDir = fs.mkdtempSync(path.join(os.tmpdir(), 'chrome-pdf-'));
const port = 9300 + Math.floor(Math.random() * 500);

let chromeProc = null;
let browserWs = null;

function cleanup() {
  if (browserWs) {
    try { browserWs.close(); } catch (e) {}
    browserWs = null;
  }
  if (chromeProc && chromeProc.pid) {
    try {
      // Kill entire process group on macOS
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

async function main() {
  chromeProc = spawn(chromePath, [
    '--headless=new',
    '--disable-gpu',
    '--no-sandbox',
    '--disable-dev-shm-usage',
    `--user-data-dir=${tempUserDataDir}`,
    `--remote-debugging-port=${port}`
  ], {
    detached: true,
    stdio: 'ignore'
  });

  // Wait for remote debugging endpoint
  let browserWsUrl = null;
  for (let i = 0; i < 40; i++) {
    await new Promise(r => setTimeout(r, 150));
    try {
      browserWsUrl = await new Promise((resolve, reject) => {
        const req = http.get(`http://127.0.0.1:${port}/json/version`, res => {
          let data = '';
          res.on('data', chunk => data += chunk);
          res.on('end', () => {
            try {
              resolve(JSON.parse(data).webSocketDebuggerUrl);
            } catch (e) { reject(e); }
          });
        });
        req.on('error', reject);
        req.setTimeout(500, () => { req.destroy(); reject(new Error('timeout')); });
      });
      if (browserWsUrl) break;
    } catch (e) {}
  }

  if (!browserWsUrl) {
    throw new Error(`Failed to connect to Chrome on port ${port}`);
  }

  browserWs = new WebSocket(browserWsUrl);
  let id = 1;
  const callbacks = new Map();

  browserWs.onmessage = (event) => {
    const msg = JSON.parse(event.data);
    if (msg.id && callbacks.has(msg.id)) {
      const cb = callbacks.get(msg.id);
      callbacks.delete(msg.id);
      if (msg.error) cb.reject(msg.error);
      else cb.resolve(msg.result);
    }
  };

  await new Promise((resolve, reject) => {
    browserWs.onopen = resolve;
    browserWs.onerror = reject;
  });

  function sendBrowser(method, params = {}) {
    return new Promise((resolve, reject) => {
      const msgId = id++;
      callbacks.set(msgId, { resolve, reject });
      browserWs.send(JSON.stringify({ id: msgId, method, params }));
    });
  }

  const { targetId } = await sendBrowser("Target.createTarget", { url: "about:blank" });
  const { sessionId } = await sendBrowser("Target.attachToTarget", { targetId, flatten: true });

  function sendSession(method, params = {}) {
    return new Promise((resolve, reject) => {
      const msgId = id++;
      callbacks.set(msgId, { resolve, reject });
      browserWs.send(JSON.stringify({ id: msgId, sessionId, method, params }));
    });
  }

  await sendSession("Page.enable");
  await sendSession("Runtime.enable");
  await sendSession("Page.navigate", { url: fileUrl });

  // Wait for MathJax typesetting and web fonts
  for (let i = 0; i < 50; i++) {
    await new Promise(r => setTimeout(r, 200));
    try {
      const evalRes = await sendSession("Runtime.evaluate", {
        expression: "document.body.classList.contains('mathjax-typeset-done')",
        returnByValue: true
      });
      if (evalRes && evalRes.result && evalRes.result.value) {
        break;
      }
    } catch (e) {}
  }
  // Extra buffer for layout and fonts stabilization
  await new Promise(r => setTimeout(r, 1200));

  let pdfBuffer = null;
  try {
    const pdfResult = await sendSession("Page.printToPDF", {
      preferCSSPageSize: true,
      printBackground: true,
      displayHeaderFooter: false
    });
    pdfBuffer = Buffer.from(pdfResult.data, 'base64');
  } catch (err) {
    console.warn(`[WARN] Single-shot printToPDF failed (${err.message}). Falling back to multi-page chunked print...`);
    const pageCountRes = await sendSession("Runtime.evaluate", {
      expression: "document.querySelectorAll('.a4-sheet, .concept-page, .teach-page, [id^=\"sheet-\"], [id^=\"page-\"]').length || 1",
      returnByValue: true
    });
    const pageCount = (pageCountRes && pageCountRes.result && pageCountRes.result.value) || 1;
    const tempDir = fs.mkdtempSync(path.join(os.tmpdir(), 'pdf-parts-'));
    const partFiles = [];

    for (let p = 1; p <= pageCount; p++) {
      const partRes = await sendSession("Page.printToPDF", {
        pageRanges: String(p),
        preferCSSPageSize: true,
        printBackground: true,
        displayHeaderFooter: false
      });
      const partFile = path.join(tempDir, `part_${p}.pdf`);
      fs.writeFileSync(partFile, Buffer.from(partRes.data, 'base64'));
      partFiles.push(partFile);
    }

    // Merge using python3 pypdf (PdfWriter)
    const mergeScript = `
import sys
from pypdf import PdfWriter
writer = PdfWriter()
for f in sys.argv[2:]:
    writer.append(f)
writer.write(sys.argv[1])
writer.close()
`;
    const { execFileSync } = require('child_process');
    execFileSync('python3', ['-c', mergeScript, absPdfPath, ...partFiles]);
    fs.rmSync(tempDir, { recursive: true, force: true });
    console.log(`[SUCCESS] PDF successfully generated via chunked merge: ${absPdfPath}`);
    try { await sendBrowser("Browser.close"); } catch (e) {}
    return;
  }

  fs.writeFileSync(absPdfPath, pdfBuffer);
  console.log(`[SUCCESS] PDF successfully generated: ${absPdfPath}`);

  // Gracefully request browser exit via CDP
  try {
    await sendBrowser("Browser.close");
  } catch (e) {}
}

main()
  .catch(err => {
    console.error("[ERROR] Failed to convert PDF:", err.message);
    process.exitCode = 1;
  })
  .finally(() => {
    cleanup();
  });
