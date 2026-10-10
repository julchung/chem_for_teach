# 高中化學學習網 · Google Firebase 雲端同步升級建置指引

> **文件狀態**：規劃與預備階段  
> **適用目標**：完成整體教材頁面架構並上傳 GitHub Pages 順暢運作後，進一步為系統無痛升級「跨裝置進度同步」與「個人手寫筆記雲端化」。

---

## 📌 一、為什麼需要導入 Firebase 雲端同步？

### 1. 現狀（本機 localStorage 模式）
* **運作方式**：教材部署於 GitHub Pages，學生的闖關進度（解鎖單元）與手寫筆記儲存於「學生當前使用之電腦瀏覽器」（`localStorage`）。
* **優點**：架構極簡、免伺服器、免租金、零維護成本。
* **限制**：學生換設備（例如在學校電腦教室上課，回家改用平板或手機複習），舊電腦的筆記與通關進度無法自動帶到新設備。

### 2. 升級後（GitHub Pages + Firebase 雙核心模式）
* **教材端（GitHub Pages）**：繼續負責靜態網頁（HTML/CSS/JS/模擬實驗）之極速派發。
* **數據端（Google Firebase）**：免費提供學生帳號的「已解鎖單元進度」與「各章節手寫筆記座標」的即時雲端讀寫。
* **達成效果**：
  1. 學生在任何電腦、手機或平板只要輸入同一學號，**進度與筆記立刻 100% 同步**。
  2. 老師可在 Firebase 後台直接看見全班學習進度（如：全班有哪些人已通關到第 3 章）。
  3. 支援離線快取（網路暫斷時依然能寫筆記，連線後自動同步補傳）。

---

## 💰 二、費用與免費額度評估（Spark 免費方案）

Google Firebase 提供永久免費的 **Spark Plan**，專門支援教育與個人專案，不需綁定信用卡即可使用：

| 資源項目 | Firebase 免費額度 | 高中化學教學預估使用量 | 費用評估 |
| :--- | :--- | :--- | :--- |
| **資料庫儲存容量** | **1 GB** | 1000 位學生的筆記與進度約佔 20~50 MB | 綽綽有餘（使用率 < 5%） |
| **每日讀取次數** | **50,000 次 / 天** | 全校學生每日登入載入約 1,000~3,000 次 | 完全在免費額度內 |
| **每日寫入次數** | **20,000 次 / 天** | 學生完成章節或儲存筆記約 1,000~2,000 次 | 完全在免費額度內 |
| **網路流量** | **10 GB / 月** | 文字與座標 JSON 封包極小（< 1 GB / 月） | **完全免費 $0** |

---

## 🗄️ 三、雲端資料庫結構規劃

在 Firebase Realtime Database 或 Firestore 中的 JSON 結構設計：

```json
{
  "students": {
    "10101": {
      "profile": {
        "name": "王小明",
        "lastActive": "2026-09-17 18:30:00"
      },
      "progress": {
        "unlockedSections": ["ch1_s1", "ch1_s2", "ch1_s3", "ch2_s1"],
        "completedSections": ["ch1_s1", "ch1_s2"],
        "lastActiveSection": "ch2_s1"
      },
      "notes": {
        "ch1_s1": [
          { "mode": "pen", "color": "#38bdf8", "size": 4, "points": [{"x": 350, "y": 420}, {"x": 580, "y": 420}] }
        ],
        "ch1_s2": [ /* 1-2 筆記 */ ]
      }
    },
    "10102": {
      /* 學生 10102 的專屬進度與筆記 */
    }
  }
}
```

---

## 🛠️ 四、後續升級時的 5 步驟建置流程

當您教材頁面皆完成、GitHub Pages 上線穩定後，只需花 5 分鐘執行以下步驟：

### 步驟 1：建立 Firebase 免費專案
1. 開啟瀏覽器，登入 [Google Firebase Console](https://console.firebase.google.com/)。
2. 點擊「**新增專案**」，專案名稱可輸入 `my-chem-web`。
3. Google Analytics（分析）可選擇「略過」或「開啟」，點擊「建立專案」。

### 步驟 2：啟用 Realtime Database（即時資料庫）
1. 在左側選單中點選「**建置 (Build)**」➔「**Realtime Database**」。
2. 點選「**建立資料庫**」，伺服器位置選擇最近的（如亞洲地區或預設）。
3. 安全性規則選擇「**以測試模式啟動 (Test mode)**」方便初始連線。

### 步驟 3：獲取前端連線金鑰 (Config)
1. 點擊專案首頁的「**Web 圖示 (`</>`)**」註冊網頁應用程式。
2. 應用程式暱稱填寫 `ChemWeb`，點擊註冊。
3. Firebase 會給出一小段設定金鑰（類似下方格式，複製備用）：
   ```javascript
   const firebaseConfig = {
     apiKey: "AIzaSyD-xxxxxxxxxxxxxxxxxxxx",
     authDomain: "my-chem-web.firebaseapp.com",
     databaseURL: "https://my-chem-web-default-rtdb.firebaseio.com",
     projectId: "my-chem-web",
     storageBucket: "my-chem-web.appspot.com",
     messagingSenderId: "1234567890",
     appId: "1:1234567890:web:abcdef123456"
   };
   ```

### 步驟 4：在專案中建立設定檔
在 `unified_chem_spa/js/` 下新增一個檔案 `firebase-config.js`，貼上步驟 3 的 Config 並初始化 Firebase SDK：
```html
<!-- 在 index.html 底部引入 Firebase SDK -->
<script src="https://www.gstatic.com/firebasejs/9.23.0/firebase-app-compat.js"></script>
<script src="https://www.gstatic.com/firebasejs/9.23.0/firebase-database-compat.js"></script>
<script src="unified_chem_spa/js/firebase-config.js"></script>
```

### 步驟 5：替換 portal.js 中的讀寫介面
我們只需在 `portal.js` 的 4 個核心函式加入雲端同步（自動雙向保留：本機 `localStorage` 當快取，雲端當真理來源）：
1. `loadUserProgress()`：優先自雲端抓取該學號之 `progress`。
2. `saveProgress()`：更新解鎖時，同步推播至雲端。
3. `loadSectionNotes(sectionId)`：載入該單元手寫筆記。
4. `saveCurrentSectionNotes()`：畫完收合工具時，將筆跡 JSON 同步至雲端。

---

## 🧭 五、當前階段建議工作流程

1. **第一步（當前主軸）**：
   - 繼續將 12 大章節中各小節資料夾的 HTML 教材內容逐步完善充實。
   - 確保本機上透過 `index.html` 瀏覽、解鎖闖關、手寫板畫圖、小工具運作正常。
2. **第二步**：
   - 將整包專案上傳至 GitHub，開啟 GitHub Pages 網址測試線上讀取速度。
3. **第三步**：
   - 一切運作無誤後，隨時向 AI 提出：「*現在我要開始串接 Firebase 雲端同步了*」，屆時我們將按本文件迅速為您接通雲端庫！
