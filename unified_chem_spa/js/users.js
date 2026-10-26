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
  "users.csv": `登入帳號/班級座號,密碼/學號,姓名,備註,Google帳號,歸屬教師
jul,1099,化學科老師,教師,julshow418@gmail.com,jul
admin,admin1099,系統管理員,教師,,jul
31727,310609,鍾冠頡,一般,,jul
show,show,化學科老師,教師,,jul`,

  "users01.csv": `登入帳號/班級座號,密碼/學號,姓名,備註,Google帳號,歸屬教師
20501,410542,于上迪,一般,,jul
20502,410469,王伊平,一般,,jul
20503,410254,朱奕杰,一般,,jul
20504,410076,江宇玄,一般,,jul
20505,410362,吳侑昕,一般,,jul
20506,410546,吳宗翰,一般,,jul
20507,410474,吳晏,一般,,jul
20508,410405,李威蒴,一般,,jul
20509,410331,林冠燁,一般,,jul
20510,410261,林宥均,一般,,jul
20511,410083,林祐群,一般,,jul
20512,410512,林毓家,一般,,jul
20513,410015,孫翊鈞,一般,,jul
20514,410268,高永旭,一般,,jul
20515,410411,張恩偉,一般,,jul
20516,410523,莊詠翰,一般,,jul
20517,410381,許家睿,一般,,jul
20518,410019,連祐慶,一般,,jul
20519,410203,陳弘鈞,一般,,jul
20520,410126,陳立為,一般,,jul
20521,410527,陳其崴,一般,,jul
20522,410386,陳奕瑄,一般,,jul
20523,410421,陳清煦,一般,,jul
20524,410422,陳菘德,一般,,jul
20525,410488,陳澤介,一般,,jul
20526,410489,彭奕暟,一般,,jul
20527,410206,彭源皓,一般,,jul
20528,410094,曾禹睿,一般,,jul
20529,410460,黃元佑,一般,,jul
20530,410533,黃呈宇,一般,,jul
20531,410100,葉?宏,一般,,jul
20532,410166,廖丞允,一般,,jul
20533,410353,劉子瑜,一般,,jul
20534,410136,劉懷鈞,一般,,jul
20535,410032,蔡岳翰,一般,,jul
20536,410171,鄭丞翔,一般,,jul
20537,410177,鍾易澄,一般,,jul
20538,410287,簡均鋐,一般,,jul
20539,410468,羅韋順,一般,,jul`,

  "users02.csv": `登入帳號/班級座號,密碼/學號,姓名,備註,Google帳號,歸屬教師
20601,410109,王世全,一般,,jul
20602,410146,王冠凱,一般,,jul
20603,410290,王睿麟,一般,,jul
20604,410078,吳錫錕,一般,,jul
20605,410476,李宥圻,一般,,jul
20606,410186,李弈澄,一般,,jul
20607,410330,李慕懷,一般,,jul
20608,410551,沈侑霆,一般,,jul
20609,410510,周竑羽,一般,,jul
20610,410115,林羿臣,一般,,jul
20611,410116,林恩樂,一般,,jul
20612,410047,林靖博,一般,,jul
20613,410332,邱楷育,一般,,jul
20614,410197,范芫銨,一般,,jul
20615,410335,徐皓霆,一般,,jul
20616,410481,徐靖芝,一般,,jul
20617,410558,徐櫂璿,一般,,jul
20618,410017,翁天寅,一般,,jul
20619,410376,張哲維,一般,,jul
20620,410157,莊竣宇,一般,,jul
20621,410563,許柏辰,一般,,jul
20622,410088,許擇,一般,,jul
20623,410525,郭延哲,一般,,jul
20624,410202,郭家齊,一般,,jul
20625,410305,陳立威,一般,,jul
20626,410025,彭義城,一般,,jul
20627,410391,?楊瀚,一般,,jul
20628,410241,黃信謙,一般,,jul
20629,410064,黃禹澔,一般,,jul
20630,410274,黃峻晨,一般,,jul
20631,410209,楊元凱,一般,,jul
20632,410276,楊善丞,一般,,jul
20633,410461,葉耘霽,一般,,jul
20634,410315,劉憶翔,一般,,jul
20635,410245,樓子齊,一般,,jul
20636,410104,蔡碩鴻,一般,,jul
20637,410071,蕭君豪,一般,,jul
20638,410143,戴弘軒,一般,,jul
20639,410501,謝沐耕,一般,,jul
20640,410466,鍾博軒,一般,,jul`,

  "users03.csv": `登入帳號/班級座號,密碼/學號,姓名,備註,Google帳號,歸屬教師
21001,410545,吳宇晨,一般,,jul
21002,410508,吳秉軒,一般,,jul
21003,410294,李奕樺,一般,,jul
21004,410260,周育辰,一般,,jul
21005,410150,易孟杰,一般,,jul
21006,410407,林子皓,一般,,jul
21007,410553,林宇笙,一般,,jul
21008,410046,林育瑋,一般,,jul
21009,410191,林定承,一般,,jul
21010,410410,韋佑倫,一般,,jul
21011,410559,張佑銓,一般,,jul
21012,410521,張?甯,一般,,jul
21013,410340,張景鈜,一般,,jul
21014,410199,梁博鈞,一般,,jul
21015,410160,許嘉佑,一般,,jul
21016,410237,陳立杰,一般,,jul
21017,410384,陳立恩,一般,,jul
21018,410309,陳柏愷,一般,,jul
21019,410239,陳梓岳,一般,,jul
21020,410487,陳憫,一般,,jul
21021,410423,曾煒恩,一般,,jul
21022,410351,湯櫂羽,一般,,jul
21023,410132,黃秉弘,一般,,jul
21024,410243,黃柏曄,一般,,jul
21025,410535,葉宇謙,一般,,jul
21026,410067,詹翊正,一般,,jul
21027,410279,趙興謙,一般,,jul
21028,410314,劉昀叡,一般,,jul
21029,410394,鄭世懋,一般,,jul
21030,410538,鄭鼎濬,一般,,jul
21031,410249,蕭詠澤,一般,,jul
21032,410395,賴柏予,一般,,jul
21033,410321,謝清宇,一般,,jul
21034,410503,韓子晨,一般,,jul
21035,410178,顏伯宇,一般,,jul
21036,410036,羅苡宸,一般,,jul
21037,21037,21037,一般,,jul`,

  "users04.csv": `登入帳號/班級座號,密碼/學號,姓名,備註,Google帳號,歸屬教師
21301,410111,朱厚誠,一般,,jul
21302,410256,吳季衡,一般,,jul
21303,410473,吳恩祖,一般,,jul
21304,410009,沈廷寯,一般,,jul
21305,410080,周書宇,一般,,jul
21306,410408,林劭安,一般,,jul
21307,410365,林冠希,一般,,jul
21308,410192,林威廷,一般,,jul
21309,410366,林宥辰,一般,,jul
21310,410370,林瑞宥,一般,,jul
21311,410441,邱畇愷,一般,,jul
21312,410515,邱翊齊,一般,,jul
21313,410230,施皓偉,一般,,jul
21314,410556,洪祺程,一般,,jul
21315,410267,徐宇澤,一般,,jul
21316,410121,張定軒,一般,,jul
21317,410302,張展銓,一般,,jul
21318,410236,梁恩赫,一般,,jul
21319,410383,郭璨榤,一般,,jul
21320,410020,陳子愷,一般,,jul
21321,410345,陳泓翰,一般,,jul
21322,410455,陳章恩,一般,,jul
21323,410205,彭奕淮,一般,,jul
21324,410390,彭鈞浩,一般,,jul
21325,410242,黃彥鈞,一般,,jul
21326,410534,黃紹崴,一般,,jul
21327,410135,黃?皓,一般,,jul
21328,410536,詹朝鈞,一般,,jul
21329,410566,廖彥竹,一般,,jul
21330,410101,趙志杰,一般,,jul
21331,410138,蔡沅均,一般,,jul
21332,410169,蔡侑任,一般,,jul
21333,410355,蔡東穎,一般,,jul
21334,410499,蕭博謙,一般,,jul
21335,410288,魏弘硯,一般,,jul
21336,410072,魏靖恆,一般,,jul
21337,410432,饒善牧,一般,,jul`
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
    const email = (cols[4] || '').trim().toLowerCase();
    const teacher = (cols[5] || '').trim() || 'jul'; // 預設歸屬 jul

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
      email: email,
      teacher: teacher,
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
