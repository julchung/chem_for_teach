/**
 * 高中化學學習網 - Firebase 即時雲端同步模組 (firebase_sync.js)
 * 
 * 功能：
 * 1. 學生跨裝置進度即時同步（已解鎖單元、通關紀錄、最後停留章節）
 * 2. 學生各章節講義手寫筆記（繪圖座標）雲端保存與跨裝置還原
 * 3. 教師端全班學習進度查核與監控（即時讀取所有學生學習狀態）
 * 4. 斷網離線保護：無網路或尚未同步時自動退回 localStorage 快取
 */

const FIREBASE_CONFIG = {
  apiKey: "AIzaSyBkjb_ETNesXktDwQAT1hswrjER0SIk07M",
  authDomain: "my-chem-web.firebaseapp.com",
  databaseURL: "https://my-chem-web-default-rtdb.europe-west1.firebasedatabase.app",
  projectId: "my-chem-web",
  storageBucket: "my-chem-web.firebasestorage.app",
  messagingSenderId: "269404768589",
  appId: "1:269404768589:web:0401e1f14f60bec9510f04",
  measurementId: "G-SH28KL24NW"
};

class ChemFirebaseSync {
  constructor() {
    this.isInitialized = false;
    this.db = null;
    this.initFirebase();
  }

  initFirebase() {
    try {
      if (typeof firebase !== 'undefined' && firebase.initializeApp) {
        if (!firebase.apps.length) {
          firebase.initializeApp(FIREBASE_CONFIG);
        }
        this.db = firebase.database();
        this.isInitialized = true;
        console.log("☁️ [Firebase] 雲端即時資料庫連線初始化成功！");
      } else {
        console.warn("⚠️ [Firebase] 未載入 Firebase SDK，將自動使用本機 localStorage 模式。");
      }
    } catch (e) {
      console.error("❌ [Firebase] 初始化失敗：", e);
      this.isInitialized = false;
    }
  }

  // ── 學生端：載入雲端進度 ──
  async loadStudentProgress(username) {
    if (!this.isInitialized || !username) return null;
    try {
      const snapshot = await this.db.ref(`students/${username}/progress`).once('value');
      if (snapshot.exists()) {
        const val = snapshot.val();
        console.log(`☁️ [Firebase] 已成功自雲端載入學生 [${username}] 的進度`);
        return val;
      }
    } catch (e) {
      console.warn("雲端讀取進度失敗，將使用本機快取：", e);
    }
    return null;
  }

  // ── 學生端：儲存進度至雲端 ──
  async saveStudentProgress(user, progress) {
    if (!this.isInitialized || !user || !user.username) return;
    try {
      const now = Date.now();
      const payload = {
        unlockedSections: progress.unlockedSections || ['ch1_s1'],
        completedSections: progress.completedSections || [],
        lastActiveSection: progress.lastActiveSection || 'ch1_s1',
        lastUpdated: now
      };
      // 更新學生專屬進度
      await this.db.ref(`students/${user.username}/progress`).update(payload);
      // 更新學生簡介與最新在線紀錄（供教師查核）
      await this.db.ref(`students/${user.username}/profile`).update({
        name: user.name || user.username,
        role: user.role || 'student',
        group: user.group || 'users.csv',
        lastActive: now,
        lastActiveSection: progress.lastActiveSection || 'ch1_s1',
        unlockedCount: (progress.unlockedSections || []).length
      });
      console.log(`☁️ [Firebase] 學生 [${user.username}] 進度已即時同步至雲端`);
    } catch (e) {
      console.warn("雲端儲存進度失敗：", e);
    }
  }

  // ── 學生端：載入章節講義手寫筆記 ──
  async loadSectionNotes(username, sectionId) {
    if (!this.isInitialized || !username || !sectionId) return null;
    try {
      const snapshot = await this.db.ref(`students/${username}/notes/${sectionId}`).once('value');
      if (snapshot.exists()) {
        const strokes = snapshot.val();
        console.log(`☁️ [Firebase] 載入學生 [${username}] 在章節 [${sectionId}] 的雲端手寫筆記 (${strokes.length} 筆筆畫)`);
        return strokes;
      }
    } catch (e) {
      console.warn("雲端讀取筆記失敗：", e);
    }
    return null;
  }

  // ── 學生端：儲存章節講義手寫筆記至雲端 ──
  async saveSectionNotes(username, sectionId, strokes) {
    if (!this.isInitialized || !username || !sectionId) return;
    try {
      await this.db.ref(`students/${username}/notes/${sectionId}`).set(strokes || []);
      console.log(`☁️ [Firebase] 學生 [${username}] 在 [${sectionId}] 的手寫筆記已同步至雲端`);
    } catch (e) {
      console.warn("雲端儲存筆記失敗：", e);
    }
  }

  // ── 教師端：即時監聽與抓取所有學生學習狀態 ──
  subscribeAllStudents(onDataChange) {
    if (!this.isInitialized) return () => {};
    try {
      const ref = this.db.ref('students');
      const listener = ref.on('value', snapshot => {
        const data = snapshot.val() || {};
        onDataChange(data);
      });
      return () => ref.off('value', listener);
    } catch (e) {
      console.error("訂閱全班學習進度失敗：", e);
      return () => {};
    }
  }
}

// 建立全域單例
window.chemSync = new ChemFirebaseSync();
