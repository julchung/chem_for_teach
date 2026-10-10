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

admin,admin,系統管理員,教師

31727,310609,鍾冠頡,一般`,

  'users01.csv': `登入帳號/班級座號,密碼/學號,姓名,備註

20501,410542,于上迪,一般

20502,410469,王伊平,一般

20503,410254,朱奕杰,一般

20504,410076,江宇玄,一般

20505,410362,吳侑昕,一般

20506,410546,吳宗翰,一般

20507,410474,吳晏,一般

20508,410405,李威蒴,一般

20509,410331,林冠燁,一般

20510,410261,林宥均,一般

20511,410083,林祐群,一般

20512,410512,林毓家,一般

20513,410015,孫翊鈞,一般

20514,410268,高永旭,一般

20515,410411,張恩偉,一般

20516,410523,莊詠翰,一般

20517,410381,許家睿,一般

20518,410019,連祐慶,一般

20519,410203,陳弘鈞,一般

20520,410126,陳立為,一般

20521,410527,陳其崴,一般

20522,410386,陳奕瑄,一般

20523,410421,陳清煦,一般

20524,410422,陳菘德,一般

20525,410488,陳澤介,一般

20526,410489,彭奕暟,一般

20527,410206,彭源皓,一般

20528,410094,曾禹睿,一般

20529,410460,黃元佑,一般

20530,410533,黃呈宇,一般

20531,410100,葉?宏,一般

20532,410166,廖丞允,一般

20533,410353,劉子瑜,一般

20534,410136,劉懷鈞,一般

20535,410032,蔡岳翰,一般

20536,410171,鄭丞翔,一般

20537,410177,鍾易澄,一般

20538,410287,簡均鋐,一般

20539,410468,羅韋順,一般`,

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
