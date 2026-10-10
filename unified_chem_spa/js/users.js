/**
 * 高中化學學習網 - 多群組使用者與帳號名冊管理模組 (users.js)
 * 
 * 支援多個編號名冊 (users.csv, users01.csv, users02.csv ... usersXX.csv)，
 * 分類管理不同群組/班級學生，四欄定義如下：
 *   第一欄：登入帳號 / 班級座號 (username)
 *   第二欄：密碼 / 學號 (password)
 *   第三欄：姓名 (name)
 *   第四欄：備註 (unlockAll / role) -> 若包含「教師/teacher/全開/true/1」則具備全解鎖權限
 */

// 預設各群組 CSV 內容
const DEFAULT_ROSTER_GROUPS = {
  'users.csv': `登入帳號/班級座號,密碼/學號,姓名,備註
jul,1099,化學科老師,教師
admin,admin,系統管理員,教師`,

  'users01.csv': `登入帳號/班級座號,密碼/學號,姓名,備註
10101,10101,王大同,一般
10102,10102,李小華,一般
10103,10103,張志豪,一般
10104,10104,陳美玲,一般
10105,10105,林育群,一般`,

  'users02.csv': `登入帳號/班級座號,密碼/學號,姓名,備註
10201,10201,黃欣怡,一般
10202,10202,吳宗翰,一般
10203,10203,蔡佳穎,一般
10204,10204,趙敏儀,一般
10205,10205,周博文,一般`
};

// CSV 單行解析工具（支援逗號、Tab分隔與雙引號字串）
function parseCSVLine(line) {
  const parts = [];
  let cur = '';
  let inQuotes = false;
  const isTab = !line.includes(',') && line.includes('\t');
  const delim = isTab ? '\t' : ',';

  for (let i = 0; i < line.length; i++) {
    const ch = line[i];
    if (ch === '"') {
      if (inQuotes && line[i + 1] === '"') {
        cur += '"';
        i++;
      } else {
        inQuotes = !inQuotes;
      }
    } else if (ch === delim && !inQuotes) {
      parts.push(cur.trim());
      cur = '';
    } else {
      cur += ch;
    }
  }
  parts.push(cur.trim());
  return parts;
}

// 將單個 CSV / TSV 文字轉換為使用者陣列
function parseUsersCSV(csvText, groupName = 'users.csv') {
  if (!csvText || typeof csvText !== 'string') return [];
  // 移除 UTF-8 BOM (避免第一欄文字受到影響)
  if (csvText.charCodeAt(0) === 0xFEFF) {
    csvText = csvText.slice(1);
  }
  const lines = csvText.split(/\r?\n/).map(l => l.trim()).filter(l => l.length > 0);
  const users = [];

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const cols = parseCSVLine(line);
    if (cols.length < 2) continue;

    const u = (cols[0] || '').trim();
    const p = (cols[1] || '').trim();
    const name = (cols[2] || '').trim();
    const note = (cols[3] || '').trim();

    // 過濾標題列
    if (i === 0 && (u.includes('帳號') || u.toLowerCase().includes('username') || u.includes('座號'))) {
      continue;
    }

    if (!u) continue;

    const noteLower = note.toLowerCase();
    const isTeacher = noteLower.includes('教師') || 
                      noteLower.includes('teacher') || 
                      noteLower.includes('全開') || 
                      noteLower.includes('全解鎖') || 
                      noteLower === 'true' || 
                      noteLower === '1';

    users.push({
      username: u,
      password: p,
      name: name || u,
      role: isTeacher ? 'teacher' : 'student',
      unlockAll: isTeacher,
      group: groupName
    });
  }
  return users;
}

// 載入多群組資料
let ROSTER_GROUPS = Object.assign({}, DEFAULT_ROSTER_GROUPS);

try {
  if (typeof localStorage !== 'undefined') {
    const cached = localStorage.getItem('chem_roster_groups');
    if (cached) {
      const parsed = JSON.parse(cached);
      if (parsed && typeof parsed === 'object') {
        ROSTER_GROUPS = Object.assign({}, DEFAULT_ROSTER_GROUPS, parsed);
      }
    }
  }
} catch(e) {}

// 合併所有群組為單一 USER_DATABASE
function rebuildUserDatabase() {
  const merged = [];
  const seenUsernames = new Set();

  for (const [groupName, csvText] of Object.entries(ROSTER_GROUPS)) {
    const list = parseUsersCSV(csvText, groupName);
    list.forEach(item => {
      const key = item.username.toLowerCase();
      if (!seenUsernames.has(key)) {
        seenUsernames.add(key);
        merged.push(item);
      }
    });
  }

  USER_DATABASE = merged;
  if (typeof window !== 'undefined') {
    window.USER_DATABASE = merged;
    window.ROSTER_GROUPS = ROSTER_GROUPS;
  }
  return merged;
}

let USER_DATABASE = [];
rebuildUserDatabase();

// 若在 HTTP/HTTPS 環境，平行嘗試探測與載入 users.csv, users01.csv ~ users10.csv
if (typeof window !== 'undefined' && window.location && window.location.protocol.startsWith('http')) {
  const probeFiles = ['users.csv'];
  for (let i = 1; i <= 10; i++) {
    const pad = i < 10 ? '0' + i : '' + i;
    probeFiles.push(`users${pad}.csv`);
  }

  Promise.all(probeFiles.map(fn => {
    return fetch(`${fn}?v=${Date.now()}`)
      .then(res => {
        if (res.ok) return res.text().then(txt => ({ fn, txt }));
        return null;
      })
      .catch(() => null);
  })).then(results => {
    let updated = false;
    results.forEach(r => {
      if (r && r.txt && r.txt.trim().length > 0) {
        ROSTER_GROUPS[r.fn] = r.txt;
        updated = true;
      }
    });
    if (updated) {
      rebuildUserDatabase();
      console.log(`[users.js] 已同步遠端名冊群組，目前有效使用者共 ${USER_DATABASE.length} 位。`);
    }
  });
}

// 匯出至全域環境
if (typeof window !== 'undefined') {
  window.USER_DATABASE = USER_DATABASE;
  window.ROSTER_GROUPS = ROSTER_GROUPS;
  window.DEFAULT_ROSTER_GROUPS = DEFAULT_ROSTER_GROUPS;
  window.parseUsersCSV = parseUsersCSV;
  window.rebuildUserDatabase = rebuildUserDatabase;

  // 匯入單一群組名冊 (例如 groupName = 'users01.csv')
  window.importRosterGroup = function(groupName, csvText) {
    if (!groupName) groupName = 'users.csv';
    ROSTER_GROUPS[groupName] = csvText;
    try {
      localStorage.setItem('chem_roster_groups', JSON.stringify(ROSTER_GROUPS));
    } catch(e) {}
    rebuildUserDatabase();
    return USER_DATABASE;
  };

  // 刪除自訂群組
  window.removeRosterGroup = function(groupName) {
    delete ROSTER_GROUPS[groupName];
    try {
      localStorage.setItem('chem_roster_groups', JSON.stringify(ROSTER_GROUPS));
    } catch(e) {}
    rebuildUserDatabase();
    return USER_DATABASE;
  };

  // 還原為系統預設名冊群組
  window.resetRosterGroups = function() {
    ROSTER_GROUPS = Object.assign({}, DEFAULT_ROSTER_GROUPS);
    try {
      localStorage.removeItem('chem_roster_groups');
    } catch(e) {}
    rebuildUserDatabase();
    return USER_DATABASE;
  };
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = { 
    USER_DATABASE, 
    ROSTER_GROUPS, 
    DEFAULT_ROSTER_GROUPS, 
    parseUsersCSV, 
    rebuildUserDatabase 
  };
}
