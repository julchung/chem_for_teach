const { spawn } = require('child_process');
const fs = require('fs');
const http = require('http');
const path = require('path');
const os = require('os');

const chromePath = '/Users/julchung/.cache/puppeteer/chrome/mac_arm-155.0.8059.39/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing';
const htmlPath = path.resolve('my_chem_003_溶液/03_拉午耳定律/03_拉午耳定律_課堂講義學習單.html');
const outDir = path.resolve('tools/page_screenshots');

if (!fs.existsSync(outDir)) {
  fs.mkdirSync(outDir, { recursive: true });
}

const fileUrl = 'file://' + htmlPath;
const tempUserDataDir = fs.mkdtempSync(path.join(os.tmpdir(), 'chrome-ss-'));
const port = 9400 + Math.floor(Math.random() * 500);

let chromeProc = null;
let browserWs = null;

function cleanup() {
  if (browserWs) {
    try { browserWs.close(); } catch (e) {}
    browserWs = null;
  }
  if (chromeProc && chromeProc.pid) {
    try { process.kill(-chromeProc.pid, 'SIGKILL'); } catch (e) {
      try { chromeProc.kill('SIGKILL'); } catch (err) {}
    }
    chromeProc = null;
  }
  try { fs.rmSync(tempUserDataDir, { recursive: true, force: true }); } catch (e) {}
}

process.on('exit', cleanup);
process.on('SIGINT', () => { cleanup(); process.exit(1); });
process.on('uncaughtException', (err) => { console.error(err); cleanup(); process.exit(1); });

async function run() {
  chromeProc = spawn(chromePath, [
    '--headless=new',
    '--disable-gpu',
    '--no-sandbox',
    '--disable-dev-shm-usage',
    `--remote-debugging-port=${port}`,
    `--user-data-dir=${tempUserDataDir}`,
    'about:blank'
  ], { detached: true, stdio: 'ignore' });

  let browserWsUrl = null;
  for (let i = 0; i < 40; i++) {
    await new Promise(r => setTimeout(r, 200));
    try {
      const data = await new Promise((resolve, reject) => {
        http.get(`http://127.0.0.1:${port}/json/version`, res => {
          let raw = '';
          res.on('data', chunk => raw += chunk);
          res.on('end', () => resolve(raw));
        }).on('error', reject);
      });
      browserWsUrl = JSON.parse(data).webSocketDebuggerUrl;
      if (browserWsUrl) break;
    } catch (e) {}
  }

  if (!browserWsUrl) throw new Error("Could not connect to Chrome");

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
  await sendSession("Emulation.setDeviceMetricsOverride", {
    width: 794,
    height: 1123,
    deviceScaleFactor: 1.5,
    mobile: false
  });

  await sendSession("Page.navigate", { url: fileUrl });
  await new Promise(r => setTimeout(r, 2000));

  // 取得頁面中各段高度與區塊
  const pageCountRes = await sendSession("Runtime.evaluate", {
    expression: `(() => {
      // 依 page-break 分割出頁面或計算總高度
      return {
        scrollHeight: document.documentElement.scrollHeight,
        clientHeight: window.innerHeight
      };
    })()`,
    returnByValue: true
  });

  console.log("Page info:", pageCountRes.result.value);

  // 截圖整頁與第一頁、第二頁
  // 第一頁頂端
  const ss1 = await sendSession("Page.captureScreenshot", {
    format: "png",
    clip: { x: 0, y: 0, width: 794, height: 1123, scale: 1 }
  });
  fs.writeFileSync(path.join(outDir, 'page_1.png'), Buffer.from(ss1.data, 'base64'));

  // 第二頁
  const ss2 = await sendSession("Page.captureScreenshot", {
    format: "png",
    clip: { x: 0, y: 1123, width: 794, height: 1123, scale: 1 }
  });
  fs.writeFileSync(path.join(outDir, 'page_2.png'), Buffer.from(ss2.data, 'base64'));

  console.log("Screenshots saved to tools/page_screenshots/");
  cleanup();
}

run().catch(err => {
  console.error(err);
  cleanup();
  process.exit(1);
});
