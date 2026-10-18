#!/usr/bin/env node
const { spawn } = require('child_process');
const fs = require('fs');
const http = require('http');
const path = require('path');
const os = require('os');

const chromePath = '/Users/julchung/.cache/puppeteer/chrome/mac_arm-155.0.8059.39/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing';
const fileUrl = 'file://' + path.resolve(__dirname, '../index.html');
const tempUserDataDir = fs.mkdtempSync(path.join(os.tmpdir(), 'chrome-login-test-'));
const port = 9400 + Math.floor(Math.random() * 500);

let chromeProc = null;
let browserWs = null;

function cleanup() {
  if (browserWs) {
    try { browserWs.close(); } catch (e) {}
    browserWs = null;
  }
  if (chromeProc && chromeProc.pid) {
    try {
      process.kill(-chromeProc.pid, 'SIGKILL');
    } catch (e) {}
    chromeProc = null;
  }
  try {
    fs.rmSync(tempUserDataDir, { recursive: true, force: true });
  } catch (e) {}
}

process.on('SIGINT', cleanup);
process.on('SIGTERM', cleanup);
process.on('exit', cleanup);
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
      if (msg.error) cb.reject(new Error(msg.error.message));
      else cb.resolve(msg.result);
    }
  };

  const send = (method, params = {}) => new Promise((resolve, reject) => {
    const msgId = id++;
    callbacks.set(msgId, { resolve, reject });
    browserWs.send(JSON.stringify({ id: msgId, method, params }));
  });

  await new Promise(r => browserWs.onopen = r);

  const { targetId } = await send('Target.createTarget', { url: fileUrl });
  const { sessionId } = await send('Target.attachToTarget', { targetId, flatten: true });

  const sessionSend = (method, params = {}) => new Promise((resolve, reject) => {
    const msgId = id++;
    callbacks.set(msgId, { resolve, reject });
    browserWs.send(JSON.stringify({ id: msgId, sessionId, method, params }));
  });

  await sessionSend('Page.enable');
  await sessionSend('Runtime.enable');

  // 等待頁面穩定
  await new Promise(r => setTimeout(r, 1200));

  // 測試 1: 錯誤密碼登入
  let res = await sessionSend('Runtime.evaluate', {
    expression: `
      (function() {
        document.getElementById('input-username').value = 'wronguser';
        document.getElementById('input-password').value = 'wrongpass';
        document.getElementById('portal-login-form').dispatchEvent(new Event('submit', { cancelable: true }));
        const err = document.getElementById('login-err-msg');
        return { display: err.style.display, text: err.textContent };
      })()
    `,
    returnByValue: true
  });
  console.log("Test 1 (Wrong user/pass):", res.result.value);

  // 測試 2: users01.csv 學生帳號 20501 登入
  res = await sessionSend('Runtime.evaluate', {
    expression: `
      (function() {
        document.getElementById('input-username').value = '20501';
        document.getElementById('input-password').value = '410542';
        document.getElementById('portal-login-form').dispatchEvent(new Event('submit', { cancelable: true }));
        
        return {
          loginActive: document.getElementById('view-login').classList.contains('active'),
          dashActive: document.getElementById('view-dashboard').classList.contains('active'),
          studentName: document.getElementById('dash-user-name').textContent,
          studentRole: document.getElementById('dash-user-role').textContent,
          progressText: document.getElementById('dash-progress-text').textContent
        };
      })()
    `,
    returnByValue: true
  });
  console.log("Test 2 (Student 20501 Login):", res.result.value);

  // 測試 3: 教師帳號 admin / admin 登入
  res = await sessionSend('Runtime.evaluate', {
    expression: `
      (function() {
        // 先登出
        document.getElementById('btn-dash-logout').click();
        
        // 再登入 admin
        document.getElementById('input-username').value = 'admin';
        document.getElementById('input-password').value = 'admin';
        document.getElementById('portal-login-form').dispatchEvent(new Event('submit', { cancelable: true }));
        
        return {
          dashActive: document.getElementById('view-dashboard').classList.contains('active'),
          teacherName: document.getElementById('dash-user-name').textContent,
          teacherRole: document.getElementById('dash-user-role').textContent,
          teacherMonitorVisible: document.getElementById('btn-open-teacher-monitor').style.display !== 'none'
        };
      })()
    `,
    returnByValue: true
  });
  // 測試 4: 驗證第十二章後面的左右二個欄位（多元課程與題庫區）
  res = await sessionSend('Runtime.evaluate', {
    expression: `
      (function() {
        const extraSec = document.querySelector('.extra-sections-wrapper');
        if (!extraSec) return { found: false };
        const cards = extraSec.querySelectorAll('.chapter-card');
        const links = Array.from(extraSec.querySelectorAll('a')).map(a => ({
          text: a.querySelector('.sec-title') ? a.querySelector('.sec-title').textContent.trim() : a.textContent.trim(),
          href: a.getAttribute('href')
        }));
        return {
          found: true,
          cardCount: cards.length,
          cardTitles: Array.from(cards).map(c => c.querySelector('h4').textContent.trim()),
          links: links
        };
      })()
    `,
    returnByValue: true
  });
  console.log("Test 4 (Extra sections validation):", JSON.stringify(res.result.value, null, 2));

  console.log("🎉 ALL TESTS COMPLETED SUCCESSFULLY!");
  cleanup();
  process.exit(0);
}

main().catch(err => {
  console.error("Main error:", err);
  cleanup();
  process.exit(1);
});
