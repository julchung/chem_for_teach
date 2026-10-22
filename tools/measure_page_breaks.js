const { spawn } = require('child_process');
const http = require('http');
const path = require('path');
const os = require('os');
const fs = require('fs');

const chromePath = '/Users/julchung/.cache/puppeteer/chrome/mac_arm-155.0.8059.39/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing';
const htmlPath = process.argv[2];
const fileUrl = 'file://' + path.resolve(htmlPath);
const tempDir = fs.mkdtempSync(path.join(os.tmpdir(), 'chrome-meas-'));
const port = 9555;

const proc = spawn(chromePath, [
  '--headless=new', '--disable-gpu', '--no-sandbox',
  `--user-data-dir=${tempDir}`, `--remote-debugging-port=${port}`
], { detached: true });

async function run() {
  let browserWsUrl = null;
  for (let i = 0; i < 30; i++) {
    await new Promise(r => setTimeout(r, 100));
    try {
      browserWsUrl = await new Promise((res, rej) => {
        http.get(`http://127.0.0.1:${port}/json/version`, r => {
          let d = ''; r.on('data', c => d += c); r.on('end', () => res(JSON.parse(d).webSocketDebuggerUrl));
        }).on('error', rej);
      });
      if (browserWsUrl) break;
    } catch(e) {}
  }

  const ws = new WebSocket(browserWsUrl);
  let id = 1;
  const cbs = new Map();
  ws.onmessage = e => {
    const m = JSON.parse(e.data);
    if (m.id && cbs.has(m.id)) { cbs.get(m.id)(m.result); cbs.delete(m.id); }
  };
  await new Promise(r => ws.onopen = r);
  function send(method, params = {}) {
    return new Promise(r => { const mid = id++; cbs.set(mid, r); ws.send(JSON.stringify({ id: mid, method, params })); });
  }
  const { targetId } = await send('Target.createTarget', { url: 'about:blank' });
  const { sessionId } = await send('Target.attachToTarget', { targetId, flatten: true });
  function sSend(method, params = {}) {
    return new Promise(r => { const mid = id++; cbs.set(mid, r); ws.send(JSON.stringify({ id: mid, sessionId, method, params })); });
  }
  await sSend('Page.enable');
  await sSend('Page.navigate', { url: fileUrl });
  await new Promise(r => setTimeout(r, 2000));
  
  const evalRes = await sSend('Runtime.evaluate', {
    expression: `
      (() => {
        const container = document.querySelector('.worksheet-container');
        if (!container) return 'No .worksheet-container';
        const children = Array.from(container.children);
        let pages = [[]];
        children.forEach(c => {
          if (c.classList.contains('page-break')) {
            pages.push([]);
          } else {
            pages[pages.length - 1].push(c);
          }
        });
        return pages.map((pChildren, idx) => {
          const totalH = pChildren.reduce((acc, el) => {
            const style = window.getComputedStyle(el);
            const mb = parseInt(style.marginBottom) || 0;
            const mt = parseInt(style.marginTop) || 0;
            return acc + el.offsetHeight + mb + mt;
          }, 0);
          return { page: idx + 1, heightPx: totalH, count: pChildren.length };
        });
      })()
    `,
    returnByValue: true
  });
  console.log(JSON.stringify(evalRes.result.value, null, 2));
  try { await send('Browser.close'); } catch(e){}
  try { process.kill(-proc.pid, 'SIGKILL'); } catch(e){}
  try {
    fs.rmSync(tempDir, { recursive: true, force: true });
  } catch(e) {}
}
run();
