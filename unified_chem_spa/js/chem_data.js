/**
 * 高中化學全螢幕學習系統 - 全課程教材資料庫 (chem_data.js)
 * 涵蓋完整 12 大章節、40+ 單元模組，連動 38 個原創深度互動模擬實驗！
 */

const CHEM_CURRICULUM = [
  {
    "id": "ch1",
    "num": 1,
    "title": "化學反應與能量",
    "icon": "🔥",
    "desc": "化學反應類型、方程式平衡、化學計量、限量試劑與反應熱赫士定律",
    "sections": [
      {
        "id": "ch1_s1",
        "num": "1-1",
        "title": "化學反應類型與質量守恆",
        "origPath": "../my_chem_001_化學反應/01_化學類型及概述/index.html",
        "origTitle": "化學反應類型與質量守恆 - 互動教學系統"
      },
      {
        "id": "ch1_s2",
        "num": "1-2",
        "title": "氧化數與原子氧化態判斷",
        "origPath": "../my_chem_009_氧化還原/01_氧化數/index.html",
        "origTitle": "Oxidation Master Pro | 進階氧化數解析平台",
        "blocks": [
          {
            "type": "slide",
            "title": "氧化數判定法則與本質",
            "subtitle": "氧化數增加為氧化，氧化數減少為還原",
            "content": "<ul>\n  <li>元素態物質（如 $\\text{O}_2, \\text{Fe}$）氧化數為 $0$。</li>\n  <li>化合物中：氟必為 $-1$；$1A$ 鹼金屬必為 $+1$；$2A$ 鹼土金屬必為 $+2$。</li>\n  <li>氫通常為 $+1$（但在活潑金屬氫化物如 $\\text{NaH}, \\text{CaH}_2$ 中為 $-1$）。</li>\n  <li>氧通常為 $-2$（但在過氧化物 $\\text{H}_2\\text{O}_2, \\text{Na}_2\\text{O}_2$ 中為 $-1$；超氧化物中為 $-\\frac{1}{2}$；$\\text{OF}_2$ 中為 $+2$）。</li>\n  <li>中性分子中所有原子氧化數代數和為 $0$；多原子離子代數和等於所帶電荷。</li>\n</ul>"
          },
          {
            "type": "checkpoint",
            "title": "單元 1-2 學習檢核",
            "desc": "完成檢核解鎖 1-3 氧化還原方程式平衡。",
            "questionText": "在過錳酸根離子 (MnO4-) 中，錳 (Mn) 原子的氧化數為多少？",
            "options": [
              "+7",
              "+2",
              "+4",
              "+6"
            ],
            "correctIndex": 0,
            "expl": "O 為 -2 * 4 = -8，離子總電荷為 -1，故 Mn + (-8) = -1 => Mn = +7。"
          }
        ]
      },
      {
        "id": "ch1_s3",
        "num": "1-3",
        "title": "氧化還原方程式平衡",
        "origPath": "../my_chem_009_氧化還原/03_氧化還原方程式平衡/index.html",
        "origTitle": "氧化還原方程式平衡 | 互動教學",
        "blocks": [
          {
            "type": "slide",
            "title": "氧化數法與半反應法核心法則",
            "subtitle": "升降守恆 · 電荷平衡 · 原子不滅",
            "content": "<ol>\n  <li><strong>氧化數法</strong>：標示升降氧化數，取最小公倍數平衡主係數；依酸鹼性補 $\\text{H}^+/\\text{OH}^-$ 平衡電荷，最後加水補平原子。</li>\n  <li><strong>半反應法</strong>：拆為氧化與還原半反應；先平中心原子，加電子平得失，依液性補酸鹼平電荷，最後加水並乘倍數消電子相加。</li>\n</ol>"
          },
          {
            "type": "checkpoint",
            "title": "單元 1-3 學習檢核",
            "desc": "完成檢核解鎖 1-4 化學計量與限量試劑。",
            "questionText": "在酸性水溶液中，MnO4- 還原為 Mn2+ 時，需轉移多少莫耳電子？",
            "options": [
              "5 mol 電子",
              "3 mol 電子",
              "2 mol 電子",
              "7 mol 電子"
            ],
            "correctIndex": 0,
            "expl": "Mn 氧化數由 +7 降至 +2，差值為 5，故需獲得 5 莫耳電子 (MnO4- + 8H+ + 5e- -> Mn2+ + 4H2O)。"
          }
        ]
      },
      {
        "id": "ch1_s4",
        "num": "1-4",
        "title": "化學計量與限量試劑",
        "origPath": "../my_chem_001_化學反應/03_限量試劑/index.html",
        "origTitle": "化學計量與限量試劑互動教學系統",
        "blocks": [
          {
            "type": "slide",
            "title": "限量試劑判定與莫耳數換算",
            "subtitle": "初中末三段式計算法",
            "content": "<p>當反應物並非恰好依係數比混合時，其中完全耗盡者稱為<strong>限量試劑 (Limiting Reagent)</strong>，決定生成物的最大產量。</p>\n<div class=\"formula-box\">$$\\text{判定法：比較各反應物之 } \\frac{\\text{初莫耳數}}{\\text{平衡係數}} \\text{，比值最小者即為限量試劑！}$$</div>\n<div class=\"flex-row\">\n  <div class=\"flex-col\">\n    <h3 class=\"text-yellow\">計量三步驟</h3>\n    <ol>\n      <li>質量轉莫耳數：$n = \\frac{W}{M}$。</li>\n      <li>依係數比以限量試劑計算消耗量與生成量。</li>\n      <li>初量 $-$ 消耗量 = 末剩餘量。</li>\n    </ol>\n  </div>\n  <div class=\"flex-col\">\n    <h3 class=\"text-cyan\">產率計算</h3>\n    <div class=\"formula-box\">$$\\text{產率 (\\%)} = \\frac{\\text{實際產量}}{\\text{理論最大產量}} \\times 100\\%$$</div>\n  </div>\n</div>"
          },
          {
            "type": "example",
            "title": "經典範例 1-4：合成氨限量試劑演練",
            "problemHtml": "<p class=\"problem-lead\">在密閉容器中混合 3 莫耳 $\\text{N}_2$ 與 6 莫耳 $\\text{H}_2$ 合成氨氣：</p>\n<div class=\"formula-box\">$$\\text{N}_2(g) + 3\\text{H}_2(g) \\rightarrow 2\\text{NH}_3(g)$$</div>\n<ol>\n  <li>試判斷誰為限量試劑？</li>\n  <li>反應完全後，可生成多少莫耳的 $\\text{NH}_3$？剩餘哪種反應物多少莫耳？</li>\n</ol>",
            "solutionHtml": "<h4 class=\"sol-title\">詳細解析步驟</h4>\n<div class=\"sol-step\">\n  <p><strong>Step 1：比較比值判斷限量試劑</strong></p>\n  <p>$\\text{N}_2$：$\\frac{3}{1} = 3$；$\\text{H}_2$：$\\frac{6}{3} = 2$。因 $2 < 3$，故 <strong>$\\text{H}_2$ 為限量試劑</strong>！</p>\n  <p><strong>Step 2：三段式計量</strong></p>\n  <p>消耗 $\\text{H}_2 = 6\\text{ mol}$；消耗 $\\text{N}_2 = 6 \\times \\frac{1}{3} = 2\\text{ mol}$；生成 $\\text{NH}_3 = 6 \\times \\frac{2}{3} = 4\\text{ mol}$。</p>\n  <p>剩餘 $\\text{N}_2 = 3 - 2 = 1\\text{ mol}$。</p>\n</div>\n<div class=\"sol-ans\"><p class=\"text-green font-bold\">答：(1) $\\text{H}_2$ 為限量試劑；(2) 生成 4 mol $\\text{NH}_3$，剩餘 1 mol $\\text{N}_2$。</p></div>"
          },
          {
            "type": "checkpoint",
            "title": "單元 1-4 學習檢核",
            "desc": "完成檢核解鎖 1-5 反應熱加成性與赫士定律。",
            "questionText": "將 4 莫耳 H2 與 3 莫耳 O2 反應生成水 (2H2 + O2 -> 2H2O)，何者為限量試劑？可生成幾莫耳水？",
            "options": [
              "H2 為限量試劑，生成 4 莫耳水",
              "O2 為限量試劑，生成 6 莫耳水",
              "H2 為限量試劑，生成 2 莫耳水",
              "恰好完全反應，生成 5 莫耳水"
            ],
            "correctIndex": 0,
            "expl": "H2 比值為 4/2 = 2，O2 比值為 3/1 = 3。比值小者 H2 為限量試劑，消耗 4 莫耳 H2 生成 4 莫耳 H2O。"
          }
        ]
      },
      {
        "id": "ch1_s5",
        "num": "1-5",
        "title": "反應熱加成性與赫士定律",
        "origPath": "../my_chem_001_化學反應/04_反應熱加成性/index.html",
        "origTitle": "赫士定律與反應熱互動教學",
        "blocks": [
          {
            "type": "slide",
            "title": "赫士定律 (Hess's Law) 核心原理",
            "subtitle": "狀態函數與反應熱代數和",
            "content": "<p>化學反應的反應熱 ($\\Delta H$) 僅取決於最初與最終狀態，而與其<strong>經歷途徑無關</strong>。反應熱具有<strong>狀態函數加成性</strong>。</p>\n<div class=\"formula-box\">$$\\Delta H_{\\text{total}} = \\Delta H_1 + \\Delta H_2 + \\dots$$</div>\n<ul>\n  <li>方程式同乘 $n$ 倍：$\\Delta H' = n \\times \\Delta H$。</li>\n  <li>方程式逆寫：$\\Delta H' = -\\Delta H$（正放逆必等量吸）。</li>\n  <li>反應相加：$\\Delta H' = \\Delta H_A + \\Delta H_B$。</li>\n</ul>"
          },
          {
            "type": "example",
            "title": "經典範例 1-5：利用赫士定律求解 CO 生成熱",
            "problemHtml": "<p class=\"problem-lead\">已知：</p>\n<p>(1) $\\text{C}(s) + \\text{O}_2(g) \\rightarrow \\text{CO}_2(g) \\quad \\Delta H_1 = -393.5\\text{ kJ}$</p>\n<p>(2) $\\text{CO}(g) + \\frac{1}{2}\\text{O}_2(g) \\rightarrow \\text{CO}_2(g) \\quad \\Delta H_2 = -283.0\\text{ kJ}$</p>\n<p>求反應 $\\text{C}(s) + \\frac{1}{2}\\text{O}_2(g) \\rightarrow \\text{CO}(g)$ 之反應熱 $\\Delta H$ 為何？</p>",
            "solutionHtml": "<h4 class=\"sol-title\">詳細解析步驟</h4>\n<div class=\"sol-step\">\n  <p>目標式：$\\text{C}(s) + \\frac{1}{2}\\text{O}_2(g) \\rightarrow \\text{CO}(g)$。</p>\n  <p>將式 (1) 減去式 (2)：</p>\n  <p>$$\\Delta H = (-393.5) - (-283.0) = -110.5\\text{ kJ}$$</p>\n</div>\n<div class=\"sol-ans\"><p class=\"text-green font-bold\">答：$\\Delta H = -110.5\\text{ kJ/mol}$。</p></div>"
          },
          {
            "type": "checkpoint",
            "title": "單元 1-5 學習檢核",
            "desc": "恭喜完成第 1 章全數單元！完成此檢核進入第 2 章氣體。",
            "questionText": "若 A -> B 之 ΔH = -50 kJ，B -> C 之 ΔH = +30 kJ，則 A -> C 之反應熱為？",
            "options": [
              "-20 kJ",
              "+20 kJ",
              "-80 kJ",
              "+80 kJ"
            ],
            "correctIndex": 0,
            "expl": "依赫士定律，A -> C 為兩式相加，ΔH = (-50) + (+30) = -20 kJ。"
          }
        ]
      }
    ]
  },
  {
    "id": "ch2",
    "num": 2,
    "title": "氣體",
    "icon": "💨",
    "desc": "波以耳、查理、亞佛加厥定律、理想氣體方程式 PV=nRT、道耳吞分壓、擴散與逸散",
    "sections": [
      {
        "id": "ch2_s1",
        "num": "2-1",
        "title": "氣體通性與水銀壓力計",
        "origPath": "../my_chem_002_氣體/01_氣體通性與水銀壓力計/index.html",
        "origTitle": "氣體的通性與水銀壓力計 - 互動教學",
        "blocks": [
          {
            "type": "slide",
            "title": "氣體壓力與托里切利實驗",
            "subtitle": "大氣壓力與開閉口水銀壓力計判讀",
            "content": "<p>氣體壓力單位換算標準：</p>\n<div class=\"formula-box\">$$1\\text{ atm} = 76\\text{ cm-Hg} = 760\\text{ mmHg (torr)} = 1013\\text{ hPa} = 1.013 \\times 10^5\\text{ Pa}$$</div>\n<ul>\n  <li>閉口式水銀計：$P_{\\text{gas}} = h$ (cm-Hg)。</li>\n  <li>開口式水銀計（氣壓大於外界）：$P_{\\text{gas}} = P_{\\text{atm}} + h$。</li>\n  <li>開口式水銀計（氣壓小於外界）：$P_{\\text{gas}} = P_{\\text{atm}} - h$。</li>\n</ul>"
          },
          {
            "type": "checkpoint",
            "title": "單元 2-1 學習檢核",
            "desc": "完成檢核解鎖下一節。",
            "questionText": "一大氣壓 (1 atm) 等於多少 mmHg (托耳)？",
            "options": [
              "760 mmHg",
              "76 mmHg",
              "1013 mmHg",
              "100 mmHg"
            ],
            "correctIndex": 0,
            "expl": "1 atm = 76 cm-Hg = 760 mmHg = 760 torr。"
          }
        ]
      },
      {
        "id": "ch2_s2",
        "num": "2-2",
        "title": "波以耳定律 (Boyle's Law)",
        "origPath": "../my_chem_002_氣體/02_波以耳定律/index.html",
        "origTitle": "波以耳定律 - 互動式教學網頁",
        "blocks": [
          {
            "type": "slide",
            "title": "波以耳定律：壓力與體積反比",
            "subtitle": "定溫、定量氣體 ($T, n$ 為常數)",
            "content": "<div class=\"formula-box\">$$P_1 V_1 = P_2 V_2 = \\text{常數}$$</div>\n<p>在定溫下，氣體壓力與體積乘積為定值。壓縮體積會使分子碰撞器壁頻率成比例上升，因而壓力倍增。</p>"
          },
          {
            "type": "checkpoint",
            "title": "單元 2-2 學習檢核",
            "desc": "完成檢核解鎖下一節。",
            "questionText": "定溫下定量氣體體積減半，其壓力變為原本的幾倍？",
            "options": [
              "2 倍",
              "0.5 倍",
              "4 倍",
              "不變"
            ],
            "correctIndex": 0,
            "expl": "P 與 V 成反比，體積變為 1/2，壓力變為 2 倍。"
          }
        ]
      },
      {
        "id": "ch2_s3",
        "num": "2-3",
        "title": "查理與給呂薩克定律",
        "origPath": "../my_chem_002_氣體/03_查理給呂薩克定律/index.html",
        "origTitle": "查理給呂薩克定律 - 互動教學",
        "blocks": [
          {
            "type": "slide",
            "title": "查理定律：體積與絕對溫度正比",
            "subtitle": "定壓、定量氣體 ($P, n$ 為常數)",
            "content": "<div class=\"formula-box\">$$\\frac{V_1}{T_1} = \\frac{V_2}{T_2} \\quad (T = t + 273.15\\text{ K})$$</div>\n<p>定壓定量下，氣體體積與絕對溫度 (K) 成正比。絕對零度 (0 K = -273.15°C) 為氣體外推體積為零之理論極限。</p>"
          },
          {
            "type": "checkpoint",
            "title": "單元 2-3 學習檢核",
            "desc": "完成檢核解鎖下一節。",
            "questionText": "定壓下，將 27°C (300 K) 的氣體加熱至 127°C (400 K)，體積擴大為原本的幾倍？",
            "options": [
              "4/3 倍",
              "2 倍",
              "127/27 倍",
              "3/4 倍"
            ],
            "correctIndex": 0,
            "expl": "V2/V1 = T2/T1 = 400/300 = 4/3 倍。"
          }
        ]
      },
      {
        "id": "ch2_s4",
        "num": "2-4",
        "title": "亞佛加厥定律與氣體莫耳體積",
        "origPath": "../my_chem_002_氣體/04_亞佛加厥定律/index.html",
        "origTitle": "亞佛加厥定律 - 互動教學",
        "blocks": [
          {
            "type": "slide",
            "title": "同溫同壓同體積，同分子數",
            "subtitle": "STP 與 NTP 莫耳體積標準",
            "content": "<p>同溫同壓下，任何氣體之體積比等於其莫耳數比 ($V \\propto n$)。</p>\n<div class=\"formula-box\">$$\\text{STP (0}^\\circ\\text{C, 1 atm): } V_m = 22.4\\text{ L/mol}$$</div>\n<div class=\"formula-box\">$$\\text{NTP (25}^\\circ\\text{C, 1 atm): } V_m = 24.5\\text{ L/mol}$$</div>"
          },
          {
            "type": "checkpoint",
            "title": "單元 2-4 學習檢核",
            "desc": "完成檢核解鎖下一節。",
            "questionText": "在 STP 下，2 莫耳氧氣佔據的體積為多少公升？",
            "options": [
              "44.8 L",
              "22.4 L",
              "49.0 L",
              "11.2 L"
            ],
            "correctIndex": 0,
            "expl": "2 * 22.4 L = 44.8 L。"
          }
        ]
      },
      {
        "id": "ch2_s5",
        "num": "2-5",
        "title": "理想氣體方程式 (PV = nRT)",
        "origPath": "../my_chem_002_氣體/05_理想氣體方程式/index.html",
        "origTitle": "理想氣體方程式 - 互動教學",
        "blocks": [
          {
            "type": "slide",
            "title": "理想氣體狀態方程式與氣體常數 R",
            "subtitle": "狀態換算與氣體密度公式 PM = dRT",
            "content": "<div class=\"formula-box\">$$PV = nRT = \\frac{W}{M}RT \\iff PM = dRT$$</div>\n<p>氣體常數 $R = 0.082 \\, \\text{atm}\\cdot\\text{L}/(\\text{mol}\\cdot\\text{K})$。在<strong>高溫、低壓</strong>環境下，真實氣體最接近理想氣體。</p>"
          },
          {
            "type": "checkpoint",
            "title": "單元 2-5 學習檢核",
            "desc": "完成檢核解鎖下一節。",
            "questionText": "氣體方程式 PM = dRT 中，d 代表氣體的何種物理量？",
            "options": [
              "密度 (Density)",
              "直徑 (Diameter)",
              "擴散係數 (Diffusion)",
              "分壓 (Dalton)"
            ],
            "correctIndex": 0,
            "expl": "d 代表氣體密度 (單位 g/L)。"
          }
        ]
      },
      {
        "id": "ch2_s6",
        "num": "2-6",
        "title": "道耳吞分壓定律",
        "origPath": "../my_chem_002_氣體/06_道耳吞分壓定律/index.html",
        "origTitle": "道耳吞分壓定律 - 互動教學",
        "blocks": [
          {
            "type": "slide",
            "title": "混合氣體分壓與莫耳分率",
            "subtitle": "排水集氣法飽和水蒸氣壓修正",
            "content": "<div class=\"formula-box\">$$P_{\\text{total}} = P_A + P_B + \\dots \\quad P_A = X_A \\cdot P_{\\text{total}}$$</div>\n<p>排水集氣法收集氣體時，瓶內總壓等於外界氣壓：$P_{\\text{total}} = P_{\\text{gas}} + P_{\\text{water}}$，乾燥氣體分壓需扣除飽和水蒸氣壓。</p>"
          },
          {
            "type": "checkpoint",
            "title": "單元 2-6 學習檢核",
            "desc": "完成檢核解鎖下一節。",
            "questionText": "在 760 mmHg 下排水集氣收集氣體，若 25°C 飽和水蒸氣壓為 24 mmHg，則乾燥氣體分壓為？",
            "options": [
              "736 mmHg",
              "784 mmHg",
              "760 mmHg",
              "24 mmHg"
            ],
            "correctIndex": 0,
            "expl": "P(乾燥) = 760 - 24 = 736 mmHg。"
          }
        ]
      },
      {
        "id": "ch2_s7",
        "num": "2-7",
        "title": "擴散與逸散定律 (Graham's Law)",
        "origPath": "../my_chem_002_氣體/07_擴散與逸散/index.html",
        "origTitle": "擴散與逸散 - 互動教學",
        "blocks": [
          {
            "type": "slide",
            "title": "格銳目擴散定律",
            "subtitle": "擴散速率與分子量平方根反比",
            "content": "<div class=\"formula-box\">$$\\frac{r_1}{r_2} = \\sqrt{\\frac{M_2}{M_1}} = \\sqrt{\\frac{d_2}{d_1}}$$</div>\n<p>氣體平均運動速率與分子量平方根成反比。較輕的氣體（分子量小）運動速度快、擴散速率亦快。</p>"
          },
          {
            "type": "checkpoint",
            "title": "單元 2-7 學習檢核",
            "desc": "完成檢核解鎖下一節。",
            "questionText": "同溫下 CH4 (M=16) 與 SO2 (M=64) 之擴散速率比為何？",
            "options": [
              "2 : 1",
              "1 : 2",
              "4 : 1",
              "1 : 4"
            ],
            "correctIndex": 0,
            "expl": "r(CH4)/r(SO2) = sqrt(64/16) = sqrt(4) = 2 : 1。"
          }
        ]
      },
      {
        "id": "ch2_s8",
        "num": "（補充）",
        "title": "凡得瓦方程式與真實氣體",
        "origPath": "../my_chem_002_氣體/09_補充_凡得瓦方程式/index.html",
        "origTitle": "凡得瓦方程式：理想氣體的修正",
        "blocks": [
          {
            "type": "slide",
            "title": "凡得瓦方程式對真實氣體的修正",
            "subtitle": "分子自身體積 (b) 與分子間引力 (a)",
            "content": "<div class=\"formula-box\">$$\\left(P + \\frac{n^2 a}{V^2}\\right)(V - nb) = nRT$$</div>\n<p>高壓下分子自身體積不可忽視，有效自由體積修正為 $V - nb$；低溫下分子間吸引力顯現，壓力修正為 $P + \\frac{n^2 a}{V^2}$。</p>"
          },
          {
            "type": "checkpoint",
            "title": "補充單元學習檢核",
            "desc": "完成此檢核鞏固真實氣體修正觀念。",
            "questionText": "凡得瓦方程式中，參數 a 用以修正何種效應？",
            "options": [
              "分子間吸引力",
              "分子自身體積",
              "重力",
              "容器熱膨脹"
            ],
            "correctIndex": 0,
            "expl": "參數 a 修正分子間吸引力，參數 b 修正自身體積。"
          }
        ]
      },
      {
        "id": "ch2_s9",
        "num": "（補充）",
        "title": "理想氣體方程式圖示",
        "origPath": "../my_chem_002_氣體/08_補充_PV=nRT圖示/index.html",
        "origTitle": "PV=nRT 理想氣體互動演示",
        "blocks": [
          {
            "type": "slide",
            "title": "理想氣體三維關係圖 (PV=nRT)",
            "subtitle": "1 莫耳理想氣體之 P-V-T 關係表面與剖面",
            "content": "<div class=\"formula-box\">$$PV = nRT$$</div>\n<p>透過三維曲面及等溫線 (P-V)、等壓線 (V-T)、等容線 (P-T) 2D 投影圖，動態探索理想氣體狀態變化。</p>"
          },
          {
            "type": "checkpoint",
            "title": "補充單元學習檢核",
            "desc": "完成此檢核鞏固理想氣體圖形觀念。",
            "questionText": "在定溫下，理想氣體的 P-V 圖形呈現何種曲線？",
            "options": [
              "等溫雙曲線（反比關係）",
              "過原點直線（正比關係）",
              "拋物線",
              "水平直線"
            ],
            "correctIndex": 0,
            "expl": "波以耳定律：定溫下，P 與 V 成反比，P-V 圖為等溫雙曲線。"
          }
        ]
      }
    ]
  },
  {
    "id": "ch3",
    "num": 3,
    "title": "溶液",
    "icon": "🧪",
    "desc": "三相圖、溶解度與濃度表示法、拉午耳定律、依數性質、沉澱表規則與沉澱小遊戲(補充)",
    "sections": [
      {
        "id": "ch3_s1",
        "num": "3-1",
        "title": "物質的狀態與三相圖",
        "origPath": "../my_chem_003_溶液/01_物質的狀態與三相圖/index.html",
        "origTitle": "物質的狀態與三相圖 - 互動教學",
        "blocks": [
          {
            "type": "slide",
            "title": "三相圖判讀與超臨界流體",
            "subtitle": "固液氣共存的三相點與臨界點",
            "content": "<p>三相圖描繪不同溫度與壓力下物質最穩定的聚集狀態：</p>\n<ul>\n  <li><strong>三相點 (Triple Point)</strong>：固、液、氣三相共存之特定點。</li>\n  <li><strong>臨界點 (Critical Point)</strong>：高於此溫壓時氣液界面消失，成為<strong>超臨界流體 (Supercritical Fluid)</strong>。</li>\n  <li><strong>水的三相圖特徵</strong>：固-液平衡線斜率為<strong>負</strong>（加壓熔點下降，因冰的密度小於水）。</li>\n</ul>"
          },
          {
            "type": "checkpoint",
            "title": "單元 3-1 學習檢核",
            "desc": "完成檢核解鎖下一節。",
            "questionText": "水的三相圖中，固液平衡線（熔化線）斜率為負，其原因為何？",
            "options": [
              "冰的密度小於水，加壓熔點下降",
              "冰的密度大於水，加壓熔點上升",
              "水分子量較小",
              "水分子具共價鍵"
            ],
            "correctIndex": 0,
            "expl": "冰具氫鍵網狀結構密度較小，依勒沙特略原理加壓趨向體積小的液態水，故熔點隨壓力增加而降低。"
          }
        ]
      },
      {
        "id": "ch3_s2",
        "num": "3-2",
        "title": "溶解度與濃度表示法",
        "origPath": "../my_chem_003_溶液/02_溶解度與濃度表示法/index.html",
        "origTitle": "溶解度與濃度表示法 - 互動教學",
        "blocks": [
          {
            "type": "slide",
            "title": "五大濃度換算公式",
            "subtitle": "重量百分率、體積莫耳濃度、重量莫耳濃度、百萬分點",
            "content": "<div class=\"formula-box\">$$C_M = \\frac{n_{\\text{質}}}{V_{\\text{液}}(L)} \\quad (\\text{受溫度影響})$$</div>\n<div class=\"formula-box\">$$C_m = \\frac{n_{\\text{質}}}{W_{\\text{劑}}(kg)} \\quad (\\text{不受溫度影響})$$</div>\n<ul>\n  <li>重量百分濃度 $P\\% = \\frac{W_{\\text{質}}}{W_{\\text{液}}} \\times 100\\%$</li>\n  <li>百萬分點 $\\text{ppm} = \\frac{W_{\\text{質}}}{W_{\\text{液}}} \\times 10^6 \\approx \\frac{\\text{mg}}{\\text{L}}$ (稀薄水溶液)</li>\n</ul>"
          },
          {
            "type": "checkpoint",
            "title": "單元 3-2 學習檢核",
            "desc": "完成檢核解鎖下一節。",
            "questionText": "下列何種濃度表示法「不會」受到溫度熱脹冷縮的影響？",
            "options": [
              "重量莫耳濃度 (Cm)",
              "體積莫耳濃度 (CM)",
              "體積百分濃度 (% v/v)",
              "當量濃度 (N)"
            ],
            "correctIndex": 0,
            "expl": "重量莫耳濃度 Cm = 溶質莫耳數 / 溶劑公斤數，純粹以質量計算，不受溫度影響。"
          }
        ]
      },
      {
        "id": "ch3_s3",
        "num": "3-3",
        "title": "溶液蒸氣壓與拉午耳定律",
        "origPath": "../my_chem_003_溶液/03_拉午耳定律/index.html",
        "origTitle": "溶液的蒸氣壓與拉午耳定律 - 互動教學",
        "blocks": [
          {
            "type": "slide",
            "title": "拉午耳定律 (Raoult's Law)",
            "subtitle": "非揮發性與揮發性溶質之蒸氣壓下降",
            "content": "<div class=\"formula-box\">$$P_A = X_A \\cdot P_A^\\circ$$</div>\n<p>非揮發性難解離溶質的溶液蒸氣壓：$P_{\\text{液}} = X_{\\text{劑}} \\cdot P_{\\text{劑}}^\\circ$。</p>\n<p>蒸氣壓下降量：$\\Delta P = X_{\\text{質}} \\cdot P_{\\text{劑}}^\\circ$。蒸氣壓下降量與溶質莫耳分率成正比。</p>"
          },
          {
            "type": "checkpoint",
            "title": "單元 3-3 學習檢核",
            "desc": "完成檢核解鎖下一節。",
            "questionText": "在純水中溶入非揮發性蔗糖，該溶液的飽和蒸氣壓會？",
            "options": [
              "低於純水蒸氣壓",
              "高於純水蒸氣壓",
              "保持不變",
              "無法預測"
            ],
            "correctIndex": 0,
            "expl": "溶質粒子佔據表面降低溶劑分子揮發機率，使溶液蒸氣壓下降 (拉午耳定律)。"
          }
        ]
      },
      {
        "id": "ch3_s4",
        "num": "3-4",
        "title": "溶液的依數性質",
        "origPath": "../my_chem_003_溶液/04_依數性質/index.html",
        "origTitle": "溶液的依數性質 - 互動教學",
        "blocks": [
          {
            "type": "slide",
            "title": "四大依數性質公式總結",
            "subtitle": "僅取決於溶質粒子數，而與種類無關",
            "content": "<ul>\n  <li><strong>蒸氣壓下降</strong>：$\\Delta P = X_B P_A^\\circ$</li>\n  <li><strong>沸點上升</strong>：$\\Delta T_b = K_b \\cdot C_m \\cdot i$</li>\n  <li><strong>凝固點下降</strong>：$\\Delta T_f = K_f \\cdot C_m \\cdot i$</li>\n  <li><strong>滲透壓</strong>：$\\Pi = C_M R T \\cdot i$ (凡特何夫方程式)</li>\n</ul>\n<p>其中 $i$ 為凡特何夫因子（電解質如 $\\text{NaCl}$ 解離為 2 離子，$i \\approx 2$）。</p>"
          },
          {
            "type": "checkpoint",
            "title": "單元 3-4 學習檢核",
            "desc": "完成檢核解鎖下一節。",
            "questionText": "同重量莫耳濃度 (0.1 m) 之水溶液，何者凝固點最低（凝固點下降最多）？",
            "options": [
              "CaCl2 氯化鈣",
              "NaCl 氯化鈉",
              "蔗糖水溶液",
              "酒精水溶液"
            ],
            "correctIndex": 0,
            "expl": "CaCl2 解離出 1 個 Ca2+ 與 2 個 Cl-，i = 3，粒子數最多，凝固點下降最多（凝固點最低）。"
          }
        ]
      },
      {
        "id": "ch3_s5",
        "num": "3-5",
        "title": "沉澱表與沉澱規則",
        "origPath": "../my_chem_003_溶液/05_補充_沉澱表規則/index.html",
        "origTitle": "沉澱表與沉澱規則 - 互動教學",
        "blocks": [
          {
            "type": "slide",
            "title": "高中化學核心沉澱口訣心法",
            "subtitle": "必溶離子與難溶沉澱鹽類",
            "content": "<div class=\"flex-row\">\n  <div class=\"flex-col\">\n    <h3 class=\"text-green\">全溶陽離子與陰離子</h3>\n    <ul>\n      <li>陽離子：$1A\\text{ 族 (Li}^+, \\text{Na}^+, \\text{K}^+...)$、$\\text{NH}_4^+$ 皆可溶。</li>\n      <li>陰離子：$\\text{NO}_3^-$ (硝酸根)、$\\text{CH}_3\\text{COO}^-$ (醋酸根) 全可溶。</li>\n    </ul>\n  </div>\n  <div class=\"flex-col\">\n    <h3 class=\"text-yellow\">常見沉澱判斷</h3>\n    <ul>\n      <li>鹵化物：$\\text{Ag}^+, \\text{Pb}^{2+}, \\text{Hg}_2^{2+}, \\text{Cu}^+, \\text{Tl}^+$ 沉澱。</li>\n      <li>硫酸鹽：$\\text{Ba}^{2+}, \\text{Sr}^{2+}, \\text{Pb}^{2+}, \\text{Ca}^{2+}$ 沉澱。</li>\n      <li>硫化物：僅 $1A, 2A, \\text{NH}_4^+$ 可溶，其餘過渡金屬大多黑/色沉澱。</li>\n    </ul>\n  </div>\n</div>"
          },
          {
            "type": "checkpoint",
            "title": "單元 3-5 學習檢核",
            "desc": "恭喜完成第 3 章！完成此檢核進入第 4 章原子結構，並解鎖化學沉澱射擊小遊戲補充單元。",
            "questionText": "在含有 Ag+、Ba2+、Na+ 之混合液中加入 NaCl，哪種離子會產生沉澱？",
            "options": [
              "Ag+ 產生白色 AgCl 沉澱",
              "Ba2+ 產生 BaCl2 沉澱",
              "Na+ 產生 NaCl 沉澱",
              "皆不沉澱"
            ],
            "correctIndex": 0,
            "expl": "Ag+ 與 Cl- 結合產生不溶於水的白色 AgCl 沉澱；BaCl2 與 NaCl 皆可溶。"
          }
        ]
      },
      {
        "id": "ch3_s6",
        "num": "(補充)",
        "title": "化學沉澱射擊小遊戲",
        "origPath": "../my_chem_012_生活中的化學及補充/07_沉澱表遊戲/index.html",
        "origTitle": "Chemical Bubble Shooter - 沉澱泡泡射擊",
        "blocks": [
          {
            "type": "slide",
            "title": "趣味沉澱配對遊戲",
            "subtitle": "用射擊遊戲複習陰陽離子沉澱配對規則",
            "content": "<p>點擊上方「🚀 立即啟動模擬探究」即可在彈出視窗體驗化學泡泡射擊遊戲！利用發射帶電荷的離子泡泡命中相應的對抗離子，完成沉澱配對消除消波！</p>"
          },
          {
            "type": "checkpoint",
            "title": "補充單元學習檢核",
            "desc": "完成此檢核鞏固沉澱表規則與離子配對觀念。",
            "questionText": "在水中與氯離子 (Cl-) 碰撞時會生成白色沉澱的陽離子為何？",
            "options": [
              "Ag+ 銀離子",
              "Na+ 鈉離子",
              "K+ 鉀離子",
              "NH4+ 銨根離子"
            ],
            "correctIndex": 0,
            "expl": "Ag+ 與 Cl- 結合產生 AgCl 白色沉澱。"
          }
        ]
      }
    ]
  },
  {
    "id": "ch4",
    "num": 4,
    "title": "原子結構與週期性",
    "icon": "⚛️",
    "desc": "原子模型發展、氫原子波耳模型、原子軌域量子數、電子組態、原子半徑、游離能、電子親和力與電負度",
    "sections": [
      {
        "id": "ch4_s1",
        "num": "4-1",
        "title": "原子結構發展近代史",
        "origPath": "../my_chem_004_原子結構/01_原子結構發展近代史/index.html",
        "origTitle": "原子結構發展近代史 - 互動教學",
        "blocks": [
          {
            "type": "slide",
            "title": "四大里程碑實驗",
            "subtitle": "陰極射線、油滴實驗、金箔散射與中子發現",
            "content": "<ul>\n  <li><strong>湯姆森 (1897)</strong>：陰極射線實驗，發現<strong>電子</strong>並測出荷質比 ($e/m$)，提出西瓜/梅子布丁模型。</li>\n  <li><strong>密立坎 (1909)</strong>：油滴實驗，精確測得電子基本電荷量 $e = 1.6 \\times 10^{-19}\\text{ C}$。</li>\n  <li><strong>拉塞福 (1911)</strong>：$\\alpha$ 粒子撞擊金箔散射實驗，發現帶正電且極小的<strong>原子核</strong>，建立行星軌道模型。</li>\n  <li><strong>查兌克 (1932)</strong>：$\\alpha$ 粒子轟擊鈹核，發現不帶電的<strong>中子</strong>。</li>\n</ul>"
          },
          {
            "type": "checkpoint",
            "title": "單元 4-1 學習檢核",
            "desc": "完成檢核解鎖下一節。",
            "questionText": "拉塞福金箔散射實驗中，極少數 α 粒子發生大角度偏折，證明了？",
            "options": [
              "原子內部存在體積極小且質量極大的帶正電原子核",
              "電子均勻鑲嵌在正電荷球體中",
              "原子核內有中子",
              "電子具有波粒二象性"
            ],
            "correctIndex": 0,
            "expl": "極少數 α 粒子大角度彈回，證實原子的質量與正電荷高度集中在體積極小的原子核中。"
          }
        ]
      },
      {
        "id": "ch4_s2",
        "num": "4-2",
        "title": "氫原子光譜與波耳模型",
        "origPath": "../my_chem_004_原子結構/02_氫原子光譜與波耳模型/index.html",
        "origTitle": "氫原子光譜與波耳模型 - 互動教學",
        "blocks": [
          {
            "type": "slide",
            "title": "波耳氫原子能階與光譜系列",
            "subtitle": "定態軌道與躍遷放光 $\\Delta E = h\\nu$",
            "content": "<div class=\"formula-box\">$$E_n = -\\frac{1312}{n^2} \\, \\text{kJ/mol} = -\\frac{13.6}{n^2} \\, \\text{eV} \\quad (n=1,2,3\\dots)$$</div>\n<ul>\n  <li><strong>來曼系 (Lyman)</strong>：躍遷落至 $n=1$，為<strong>紫外線</strong>區。</li>\n  <li><strong>巴耳末系 (Balmer)</strong>：躍遷落至 $n=2$，為<strong>可見光</strong>區（含紅、綠、藍、紫 4 條譜線）。</li>\n  <li><strong>帕申系 (Paschen)</strong>：躍遷落至 $n=3$，為<strong>紅外線</strong>區。</li>\n</ul>"
          },
          {
            "type": "checkpoint",
            "title": "單元 4-2 學習檢核",
            "desc": "完成檢核解鎖下一節。",
            "questionText": "氫原子光譜中，電子由高能階躍遷至 n = 2 能階所放射的光譜線屬於哪一光譜系列？",
            "options": [
              "巴耳末系 (Balmer series，可見光)",
              "來曼系 (Lyman series，紫外線)",
              "帕申系 (Paschen series，紅外線)",
              "布拉格系 (Bragg series)"
            ],
            "correctIndex": 0,
            "expl": "躍遷落至 n=2 為巴耳末系，波長落於可見光範圍。"
          }
        ]
      },
      {
        "id": "ch4_s3",
        "num": "4-3",
        "title": "原子軌域與四大量子數",
        "origPath": "../my_chem_004_原子結構/03_原子軌域/index.html",
        "origTitle": "原子軌域與量子數 - 互動教學",
        "blocks": [
          {
            "type": "slide",
            "title": "四大量子數 $(n, l, m_l, m_s)$ 意義",
            "subtitle": "電子雲機率分佈與軌域空間走向",
            "content": "<ul>\n  <li><strong>主量子數 $n$</strong>：主能殼層 ($n=1,2,3...$)，決定軌域大小與主要能量。</li>\n  <li><strong>角動量量子數 $l$</strong>：副能階形狀 ($l = 0 \\sim n-1$)：$l=0$ 為 $s$ 軌域 (球形)；$l=1$ 為 $p$ 軌域 (啞鈴形)；$l=2$ 為 $d$ 軌域；$l=3$ 為 $f$ 軌域。</li>\n  <li><strong>磁量子數 $m_l$</strong>：空間延伸方向 ($m_l = -l \\sim +l$)，軌域個數為 $2l+1$ 個。</li>\n  <li><strong>自旋量子數 $m_s$</strong>：電子自旋方向 ($+\\frac{1}{2}, -\\frac{1}{2}$)。</li>\n</ul>"
          },
          {
            "type": "checkpoint",
            "title": "單元 4-3 學習檢核",
            "desc": "完成檢核解鎖下一節。",
            "questionText": "當主量子數 n = 3 時，副量子數 l 的可能取值有哪些？",
            "options": [
              "0, 1, 2 (分別對應 3s, 3p, 3d)",
              "1, 2, 3",
              "0, 1",
              "只有 3"
            ],
            "correctIndex": 0,
            "expl": "l 取值範圍為 0 到 n-1，故 n=3 時 l = 0, 1, 2。"
          }
        ]
      },
      {
        "id": "ch4_s4",
        "num": "4-4",
        "title": "電子組態填寫三大原理",
        "origPath": "../my_chem_004_原子結構/04_電子組態/index.html",
        "origTitle": "電子組態的填寫規則 - 互動教學",
        "blocks": [
          {
            "type": "slide",
            "title": "基態電子排布三大法則",
            "subtitle": "構造原理、包立不相容、洪德定則",
            "content": "<ul>\n  <li><strong>構造原理 (Aufbau Principle)</strong>：電子優先填入能量最低的軌域 ($n+l$ 規則)。如 $4s$ 能階低於 $3d$。</li>\n  <li><strong>包立不相容原理 (Pauli Principle)</strong>：同原子中絕無四個量子數皆相同之兩電子；同一軌域最多容納 2 電子且自旋必相反。</li>\n  <li><strong>洪德定則 (Hund's Rule)</strong>：等能軌域排入電子時，電子優先以相同自旋方向單獨佔據不同軌域，以達自旋多重度最大。</li>\n</ul>\n<p class=\"text-yellow\"><strong>特殊反常穩定組態</strong>：Cr: $[\\text{Ar}]4s^1 3d^5$ (半滿)；Cu: $[\\text{Ar}]4s^1 3d^{10}$ (全滿)。</p>"
          },
          {
            "type": "checkpoint",
            "title": "單元 4-4 學習檢核",
            "desc": "完成檢核解鎖下一節。",
            "questionText": "鉻原子 (24Cr) 基態的正確電子組態為何？",
            "options": [
              "[Ar] 4s1 3d5 (半滿穩定)",
              "[Ar] 4s2 3d4",
              "[Ar] 4s0 3d6",
              "[Ar] 3d6"
            ],
            "correctIndex": 0,
            "expl": "d 軌域半滿具額外對稱交換能穩定性，故電子組態為 [Ar] 4s1 3d5。"
          }
        ]
      },
      {
        "id": "ch4_s5",
        "num": "4-5",
        "title": "元素週期性：原子半徑",
        "origPath": "../my_chem_004_原子結構/05_元素週期性_原子半徑/index.html",
        "origTitle": "元素週期性 - 原子半徑 | 互動教學",
        "blocks": [
          {
            "type": "slide",
            "title": "原子半徑之週期趨勢",
            "subtitle": "主量子數能殼與有效核電荷之競賽",
            "content": "<ul>\n  <li><strong>同週期 (左 $\\rightarrow$ 右)</strong>：電子層數相同，有效核電荷 ($Z_{\\text{eff}}$) 增加，引力增大，<strong>半徑逐漸變小</strong>。</li>\n  <li><strong>同族 (上 $\\rightarrow$ 下)</strong>：電子層數增加，遮蔽效應顯著，<strong>半徑逐漸變大</strong>。</li>\n  <li><strong>離子半徑規則</strong>：陽離子 < 中性原子 < 陰離子 ($r_{\\text{Fe}^{3+}} < r_{\\text{Fe}^{2+}} < r_{\\text{Fe}}$)。</li>\n</ul>"
          },
          {
            "type": "checkpoint",
            "title": "單元 4-5 學習檢核",
            "desc": "完成檢核解鎖下一節。",
            "questionText": "同週期元素從左到右，原子半徑的變化趨勢為何？",
            "options": [
              "逐漸變小 (有效核電荷增加)",
              "逐漸變大",
              "先變大後變小",
              "完全不變"
            ],
            "correctIndex": 0,
            "expl": "同週期電子層數相同，核電荷增加引力變強，原子半徑由左向右逐漸變小。"
          }
        ]
      },
      {
        "id": "ch4_s6",
        "num": "4-6",
        "title": "元素週期性：第一游離能 (IE1)",
        "origPath": "../my_chem_004_原子結構/06_元素週期性_游離能/index.html",
        "origTitle": "元素週期性 - 元素游離能 | 互動教學網頁",
        "blocks": [
          {
            "type": "slide",
            "title": "游離能定則與反常現象",
            "subtitle": "2A > 3A (Be > B) 與 5A > 6A (N > O)",
            "content": "<p>氣態基態原子移去最外層 1 個電子所需之最小能量稱為<strong>第一游離能 ($IE_1$)</strong>：</p>\n<div class=\"formula-box\">$$\\text{總趨勢：同週期左至右整體上升，同族上至下整體下降}$$</div>\n<p class=\"text-yellow\"><strong>二大反常現象解析</strong>：</p>\n<ul>\n  <li>$2A > 3A$：$\\text{Be}(2s^2) > \\text{B}(2s^2 2p^1)$，因 $s$ 全滿貫穿能力強，$p$ 電子易脫離。</li>\n  <li>$5A > 6A$：$\\text{N}(2p^3) > \\text{O}(2p^4)$，因 $p$ 半滿對稱無電子成對排斥，$\\text{O}$ 具成對電子互斥易被游離。</li>\n</ul>"
          },
          {
            "type": "checkpoint",
            "title": "單元 4-6 學習檢核",
            "desc": "完成檢核解鎖下一節。",
            "questionText": "第二週期元素中，氮 (7N) 的第一游離能大於氧 (8O) 的主因為何？",
            "options": [
              "氮原子之 2p 軌域呈半滿狀態，對稱且無電子成對排斥",
              "氮原子核電荷比氧大",
              "氧原子半徑比氮大",
              "氮具有雙鍵"
            ],
            "correctIndex": 0,
            "expl": "N(2p3) 軌域半滿較穩定，O(2p4) 有一組軌域雙電子成對排斥，故 O 較容易游離。"
          }
        ]
      },
      {
        "id": "ch4_s7",
        "num": "4-7",
        "title": "電子親和力",
        "origPath": "../my_chem_004_原子結構/07_元素週期性_電子親和力/index.html",
        "origTitle": "元素週期性 - 電子親和力 | 互動教學",
        "blocks": [
          {
            "type": "slide",
            "title": "電子親和力 (Electron Affinity) 規律與特例",
            "subtitle": "氣態中性原子結合電子之能量變化",
            "content": "<p><strong>電子親和力 ($E_{\\text{ea}}$)</strong> 代表氣態基態原子結合一個電子形成一價氣態陰離子所釋放的能量：</p>\n<div class=\"formula-box\">$$\\text{X}(g) + e^- \\rightarrow \\text{X}^-(g) \\quad (\\text{放熱越多，} E_{\\text{ea}} \\text{ 數值越大})$$</div>\n<p class=\"text-yellow\"><strong>週期表重要規律與特例解析</strong>：</p>\n<ul>\n  <li><strong>整體趨勢</strong>：同週期由左至右整體增大（鹵素 7A 族最大）；同族由上至下整體減小。</li>\n  <li><strong>全表最高反常</strong>：全週期表最高為<strong>氯 ($\\text{Cl}$, $349\\text{ kJ/mol}$)</strong>，而非氟 ($\\text{F}$)。原因為氟原子半徑極小，電子雲密度過高排斥力強。</li>\n  <li><strong>鈍氣與 2A 族趨近零</strong>：因軌域全滿或半滿具對稱穩定性，不易容納額外電子。</li>\n</ul>"
          },
          {
            "type": "checkpoint",
            "title": "單元 4-7 學習檢核",
            "desc": "完成檢核解鎖下一節。",
            "questionText": "整個元素週期表中，電子親和力 (Electron Affinity) 數值最大的元素為何？",
            "options": [
              "氯 (Cl)",
              "氟 (F)",
              "氧 (O)",
              "氦 (He)"
            ],
            "correctIndex": 0,
            "expl": "全表電子親和力最高者為氯 (Cl, 349 kJ/mol)，氟因原子半徑極小、2p 電子雲密度過大導致排斥力強，數值小於氯。"
          }
        ]
      },
      {
        "id": "ch4_s8",
        "num": "4-8",
        "title": "電負度",
        "origPath": "../my_chem_004_原子結構/08_元素週期性_電負度/index.html",
        "origTitle": "元素週期性 - 電負度 | 互動教學",
        "blocks": [
          {
            "type": "slide",
            "title": "電負度 (Electronegativity) 與極性",
            "subtitle": "包林電負度標度 (F = 4.0 最高)",
            "content": "<p><strong>電負度</strong>代表分子中原子吸引共用共價電子對之相對能力：</p>\n<div class=\"formula-box\">$$\\text{週期表電負度：氟 (F = 4.0) > 氧 (O = 3.5) > 氯 (Cl = 3.0) \\approx 氮 (N = 3.0) > 溴 (Br = 2.8)}$$</div>\n<ul>\n  <li>電負度差 $\\Delta EN > 1.7$：通常形成<strong>離子鍵</strong>。</li>\n  <li>電負度差 $\\Delta EN < 1.7$：形成<strong>極性共價鍵</strong>；差值為 0 為<strong>非極性共價鍵</strong>。</li>\n</ul>"
          },
          {
            "type": "checkpoint",
            "title": "單元 4-8 學習檢核",
            "desc": "恭喜完成第 4 章！完成此檢核進入第 5 章化學鍵。",
            "questionText": "整個週期表中，電負度最高的元素為何？",
            "options": [
              "氟 (F)",
              "氧 (O)",
              "氯 (Cl)",
              "氦 (He)"
            ],
            "correctIndex": 0,
            "expl": "氟 (F) 的包林電負度為 4.0，為全週期表中吸引共用電子能力最強之元素。"
          }
        ]
      }
    ]
  },
  {
    "id": "ch5",
    "num": 5,
    "title": "物質的結構與化學鍵",
    "icon": "🔗",
    "desc": "離子鍵與金屬鍵、共價鍵與八隅體、混成軌域與分子形狀、極性分子間作用力、氫鍵，及晶體堆積與能帶理論(補充)",
    "sections": [
      {
        "id": "ch5_s1",
        "num": "5-1",
        "title": "金屬鍵、離子鍵與晶體結構",
        "origPath": "../my_chem_005_化學鍵/01_金屬鍵離子鍵與晶體結構/index.html",
        "origTitle": "金屬鍵、離子鍵與晶體結構 | 互動教學",
        "blocks": [
          {
            "type": "slide",
            "title": "離子鍵與金屬鍵之比較",
            "subtitle": "晶格能與自由電子海模型",
            "content": "<div class=\"flex-row\">\n  <div class=\"flex-col\">\n    <h3 class=\"text-cyan\">離子鍵 (Ionic Bond)</h3>\n    <p>金屬與非金屬轉移電子形成陰陽離子之靜電引力。晶格能 $E \\propto \\frac{q_1 q_2}{r}$。固態不導電，熔融態或水溶液可導電；性脆易碎。</p>\n  </div>\n  <div class=\"flex-col\">\n    <h3 class=\"text-yellow\">金屬鍵 (Metallic Bond)</h3>\n    <p>金屬陽離子浸潤在離域的<strong>自由電子海</strong>中。具優良延展性、導電導熱性與金屬光澤；固態及熔融液態皆能導電。</p>\n  </div>\n</div>"
          },
          {
            "type": "checkpoint",
            "title": "單元 5-1 學習檢核",
            "desc": "完成檢核解鎖下一節。",
            "questionText": "金屬之所以具有優良的延展性與導電性，主因在於其具有？",
            "options": [
              "自由電子海 (Electron Sea)",
              "共價網狀結構",
              "配位共價鍵",
              "強大凡得瓦力"
            ],
            "correctIndex": 0,
            "expl": "金屬價電子可自由移動形成電子海，受外力時原子層滑動仍受電子吸引而不易斷裂，故具延展性與導電性。"
          }
        ]
      },
      {
        "id": "ch5_s2",
        "num": "5-2",
        "title": "共價鍵及鍵結軌域",
        "origPath": "../my_chem_005_化學鍵/02_共價鍵及鍵結軌域/index.html",
        "origTitle": "共價鍵及鍵結軌域 | 互動教學",
        "blocks": [
          {
            "type": "slide",
            "title": "路易斯結構與 $\\sigma$ 鍵、$\\pi$ 鍵",
            "subtitle": "頭碰頭軸向重疊 vs 肩並肩側向重疊",
            "content": "<ul>\n  <li><strong>$\\sigma$ 鍵 (Sigma)</strong>：兩軌域沿鍵軸「頭碰頭」正面重疊，電子雲集中在兩核連線上，<strong>強度大、可自由旋轉</strong>。單鍵必為 $\\sigma$ 鍵。</li>\n  <li><strong>$\\pi$ 鍵 (Pi)</strong>：未混成的 $p$ 軌域在鍵軸兩側「肩並肩」側面重疊，重疊度較小，<strong>強度弱、不可自由旋轉</strong>。</li>\n  <li>雙鍵 = $1\\sigma + 1\\pi$；參鍵 = $1\\sigma + 2\\pi$。</li>\n</ul>"
          },
          {
            "type": "checkpoint",
            "title": "單元 5-2 學習檢核",
            "desc": "完成檢核解鎖下一節。",
            "questionText": "乙炔分子 (C2H2, H-C≡C-H) 中，總共包含幾個 σ 鍵與幾個 π 鍵？",
            "options": [
              "3 個 σ 鍵，2 個 π 鍵",
              "2 個 σ 鍵，3 個 π 鍵",
              "5 個 σ 鍵，0 個 π 鍵",
              "1 個 σ 鍵，4 個 π 鍵"
            ],
            "correctIndex": 0,
            "expl": "兩個 C-H 單鍵為 2 個 σ 鍵，C≡C 參鍵含 1 個 σ 鍵與 2 個 π 鍵，總計 3σ + 2π。"
          }
        ]
      },
      {
        "id": "ch5_s3",
        "num": "5-3",
        "title": "混成軌域及分子形狀 (VSEPR)",
        "origPath": "../my_chem_005_化學鍵/03_混成軌域及分子形狀/index.html",
        "origTitle": "混成軌域與分子形狀 | 互動教學",
        "blocks": [
          {
            "type": "slide",
            "title": "價殼層電子對互斥理論 (VSEPR)",
            "subtitle": "混成軌域與分子立體幾何構型",
            "content": "<div class=\"formula-box\">$$\\text{立體數 (SN)} = \\sigma \\text{ 鍵數} + \\text{中心原子孤對電子對數 (LP)}$$</div>\n<ul>\n  <li><strong>SN = 2 ($sp$)</strong>：直線形 ($180^\\circ$)，如 $\\text{BeCl}_2, \\text{CO}_2$。</li>\n  <li><strong>SN = 3 ($sp^2$)</strong>：平面三角形 ($120^\\circ$) 如 $\\text{BF}_3$；若有 1 對 LP 則為<strong>彎曲形</strong>如 $\\text{SO}_2$。</li>\n  <li><strong>SN = 4 ($sp^3$)</strong>：正四面體 ($109.5^\\circ$) 如 $\\text{CH}_4$；1 對 LP 為<strong>三角錐形 ($107^\\circ$)</strong> 如 $\\text{NH}_3$；2 對 LP 為<strong>彎曲形 ($104.5^\\circ$)</strong> 如 $\\text{H}_2\\text{O}$。</li>\n</ul>"
          },
          {
            "type": "checkpoint",
            "title": "單元 5-3 學習檢核",
            "desc": "完成檢核解鎖下一節。",
            "questionText": "水分子 (H2O) 之中心氧原子混成軌域及分子空間形狀為何？",
            "options": [
              "sp3 混成，彎曲形 (角形)",
              "sp2 混成，平面三角形",
              "sp 混成，直線形",
              "sp3 混成，正四面體形"
            ],
            "correctIndex": 0,
            "expl": "水分子氧原子有 2 個單鍵與 2 對孤對電子，SN = 4 屬 sp3 混成，排除孤對電子後分子立體形狀為彎曲形 (約 104.5°)。"
          }
        ]
      },
      {
        "id": "ch5_s4",
        "num": "5-4",
        "title": "極性與分子間作用力",
        "origPath": "../my_chem_005_化學鍵/04_極性與分子間作用力/index.html",
        "origTitle": "極性與分子間作用力 | 互動教學",
        "blocks": [
          {
            "type": "slide",
            "title": "偶極矩與凡得瓦作用力",
            "subtitle": "偶極-偶極力、偶極-誘發偶極力、分散力",
            "content": "<ul>\n  <li><strong>分子極性</strong>：由鍵極性之向量和決定（淨偶極矩 $\\mu \\neq 0$ 為極性分子；對稱抵消 $\\mu = 0$ 為非極性分子）。</li>\n  <li><strong>倫敦分散力 (Dispersion Force)</strong>：存在於<strong>所有分子</strong>之間。分子量愈大、電子數愈多、接觸表面積愈大，極化度愈高，分散力愈強！</li>\n  <li><strong>偶極-偶極力 (Dipole-Dipole)</strong>：存在於極性分子之間。</li>\n</ul>"
          },
          {
            "type": "checkpoint",
            "title": "單元 5-4 學習檢核",
            "desc": "完成檢核解鎖下一節。",
            "questionText": "四氯化碳 (CCl4) 含有 4 個極性 C-Cl 共價鍵，為何整體分子為非極性？",
            "options": [
              "分子呈高度對稱的正四面體形，偶極矩向量和為零互相抵消",
              "氯原子電負度太低",
              "碳原子為金屬",
              "含有雙鍵"
            ],
            "correctIndex": 0,
            "expl": "正四面體對稱結構使 4 個鍵偶極向量合力恰為零，故為非極性分子。"
          }
        ]
      },
      {
        "id": "ch5_s5",
        "num": "5-5",
        "title": "氫鍵專題 (Hydrogen Bond)",
        "origPath": "../my_chem_005_化學鍵/05_氫鍵/index.html",
        "origTitle": "氫鍵 | 互動教學",
        "blocks": [
          {
            "type": "slide",
            "title": "氫鍵形成條件與反常高沸點",
            "subtitle": "H 與 F, O, N 強電負度原子鍵結",
            "content": "<div class=\"formula-box\">$$\\text{條件：} X - \\text{H} \\cdots :Y \\quad (X, Y = \\text{F, O, N})$$</div>\n<ul>\n  <li>氫原子半徑極小且去屏蔽，與相鄰分子未共用電子對產生強大局部靜電吸引力。</li>\n  <li>強度高於一般凡得瓦力，但遠小於共價鍵（約共價鍵的 5%~10%）。</li>\n  <li>造成 $\\text{HF}, \\text{H}_2\\text{O}, \\text{NH}_3$ 沸點反常高於同族氫化物。</li>\n</ul>"
          },
          {
            "type": "checkpoint",
            "title": "單元 5-5 學習檢核",
            "desc": "恭喜完成第 5 章！完成此檢核進入第 6 章反應速率。",
            "questionText": "下列化合物分子之間，何者「不能」形成分子間氫鍵？",
            "options": [
              "CH4 甲烷",
              "H2O 水",
              "NH3 氨",
              "HF 氟化氫"
            ],
            "correctIndex": 0,
            "expl": "氫鍵必須是 H 與強電負度之 F, O, N 直接相連。CH4 中 C-H 鍵無法形成氫鍵。"
          }
        ]
      },
      {
        "id": "ch5_s6",
        "num": "(補充)",
        "title": "固態晶體堆積與配位數",
        "origPath": "../my_chem_012_生活中的化學及補充/08_晶體堆積與配位數/index.html",
        "origTitle": "晶體堆積與配位數 | 互動教學",
        "blocks": [
          {
            "type": "slide",
            "title": "四大金屬晶胞結構比較",
            "subtitle": "簡單立方、體心立方、面心立方與六方最密堆積",
            "content": "<div class=\"flex-row\">\n  <div class=\"flex-col\">\n    <h3 class=\"text-yellow\">體心立方 (BCC)</h3>\n    <p>晶胞內原子數 = <strong>2</strong> 個 ($8 \\times \\frac{1}{8} + 1$)。</p>\n    <p>配位數 = <strong>8</strong>；空間填充率 = <strong>68%</strong>。</p>\n    <p>代表金屬：Na, K, Fe(α)。</p>\n  </div>\n  <div class=\"flex-col\">\n    <h3 class=\"text-green\">面心立方 (FCC / 最密堆積)</h3>\n    <p>晶胞內原子數 = <strong>4</strong> 個 ($8 \\times \\frac{1}{8} + 6 \\times \\frac{1}{2}$)。</p>\n    <p>配位數 = <strong>12</strong>；空間最高填充率 = <strong>74%</strong>。</p>\n    <p>代表金屬：Cu, Ag, Au, Al。</p>\n  </div>\n</div>"
          },
          {
            "type": "checkpoint",
            "title": "補充單元學習檢核",
            "desc": "完成此檢核鞏固晶體堆積與配位數觀念。",
            "questionText": "在面心立方最密堆積 (FCC) 金屬晶格中，每一個原子的配位數為何？",
            "options": [
              "12 (空間填充率 74%)",
              "8",
              "6",
              "4"
            ],
            "correctIndex": 0,
            "expl": "面心立方堆積為最密堆積結構，配位數達理論最高值 12。"
          }
        ]
      },
      {
        "id": "ch5_s7",
        "num": "(補充)",
        "title": "能帶理論：價帶與傳導帶",
        "origPath": "../my_chem_012_生活中的化學及補充/09_價帶理論/index.html",
        "origTitle": "能帶理論：價帶與傳導帶 - 互動教學",
        "blocks": [
          {
            "type": "slide",
            "title": "導體、半導體與絕緣體之能隙 (Band Gap)",
            "subtitle": "價帶 (VB)、傳導帶 (CB) 與禁制能帶 (Eg)",
            "content": "<ul>\n  <li><strong>導體 (Conductor)</strong>：價帶與傳導帶重疊，能隙 $E_g = 0$，電子可自由跨越導電。</li>\n  <li><strong>半導體 (Semiconductor)</strong>：能隙適中 ($E_g \\approx 1.1\\text{ eV}$ 如矽 Si)，照光或升溫時價帶電子可躍遷至傳導帶導電；升溫電阻<strong>下降</strong>。</li>\n  <li><strong>絕緣體 (Insulator)</strong>：能隙過大 ($E_g > 5\\text{ eV}$)，電子極難越過禁帶。</li>\n</ul>"
          },
          {
            "type": "checkpoint",
            "title": "補充單元學習檢核",
            "desc": "完成此檢核鞏固能帶理論觀念。",
            "questionText": "半導體材料（如單晶矽 Si）隨溫度升高時，其導電度會產生何種變化？",
            "options": [
              "導電度提高 (熱激發使躍遷至傳導帶的載子數增加)",
              "導電度下降",
              "導電度不變",
              "變為絕緣體"
            ],
            "correctIndex": 0,
            "expl": "半導體升溫提供熱能，使更多價帶電子跨越能隙躍遷至傳導帶，載子濃度增加，導電度提高。"
          }
        ]
      }
    ]
  },
  {
    "id": "ch6",
    "num": 6,
    "title": "化學反應速率",
    "icon": "⏱️",
    "desc": "反應速率定義、速率定律式、碰撞學說、活化能、溫度阿瑞尼斯方程式、催化劑與秒錶反應",
    "sections": [
      {
        "id": "ch6_s1",
        "num": "6-1",
        "title": "化學反應速率與定律式",
        "origPath": "../my_chem_006_反應速率/01_反應速率定律式/index.html",
        "origTitle": "化學反應速率 | 互動教學",
        "blocks": [
          {
            "type": "slide",
            "title": "反應速率定義與定律式",
            "subtitle": "瞬時速率與平均速率、反應級數判定",
            "content": "<div class=\"formula-box\">$$R = -\\frac{1}{a}\\frac{\\Delta[A]}{\\Delta t} = +\\frac{1}{c}\\frac{\\Delta[C]}{\\Delta t} = k [A]^m [B]^n$$</div>\n<ul>\n  <li><strong>反應級數 ($m, n$)</strong>：必須由<strong>實驗測定</strong>，不可直接視為平衡係數！</li>\n  <li>總級數 = $m + n$。</li>\n  <li><strong>速率常數 $k$</strong>：受反應物本性、溫度、催化劑影響，但與反應物濃度無關。</li>\n</ul>"
          },
          {
            "type": "checkpoint",
            "title": "單元 6-1 學習檢核",
            "desc": "完成檢核解鎖下一節。",
            "questionText": "化學反應速率定律式 R = k [A]^m [B]^n 中的反應級數 m 與 n 應如何求得？",
            "options": [
              "由實驗測定數據求得",
              "直接等於化學方程式的平衡係數",
              "等於反應物的莫耳質量比",
              "等於生成物的分子量"
            ],
            "correctIndex": 0,
            "expl": "反應級數為動力學參數，由反應機理決定，必須透過實驗測定數據推求。"
          }
        ]
      },
      {
        "id": "ch6_s2",
        "num": "6-2",
        "title": "碰撞學說與活化能",
        "origPath": "../my_chem_006_反應速率/02_碰撞學說/index.html",
        "origTitle": "碰撞學說 | 互動教學",
        "blocks": [
          {
            "type": "slide",
            "title": "有效碰撞的二大必備條件",
            "subtitle": "足夠的動能 (E >= Ea) 與適當的碰撞方位",
            "content": "<p>並非所有分子碰撞皆能引發反應，只有<strong>有效碰撞 (Effective Collision)</strong> 才能克服能障形成活化複合體：</p>\n<ol>\n  <li><strong>足夠能量</strong>：碰撞分子的動能必須大於或等於<strong>活化能 ($E_a$)</strong>。</li>\n  <li><strong>正確方位 (空間幾何配向)</strong>：碰撞時活性部位必須相互接觸。</li>\n</ol>\n<div class=\"formula-box\">$$\\Delta H = E_{a(\\text{正})} - E_{a(\\text{逆})}$$</div>"
          },
          {
            "type": "checkpoint",
            "title": "單元 6-2 學習檢核",
            "desc": "完成檢核解鎖下一節。",
            "questionText": "若某正反應為放熱反應 (ΔH < 0)，則正反應活化能 Ea(正) 與逆反應活化能 Ea(逆) 之大小關係為何？",
            "options": [
              "Ea(正) < Ea(逆)",
              "Ea(正) > Ea(逆)",
              "Ea(正) = Ea(逆)",
              "無法比較"
            ],
            "correctIndex": 0,
            "expl": "ΔH = Ea(正) - Ea(逆) < 0，故放熱反應之正反應活化能小於逆反應活化能。"
          }
        ]
      },
      {
        "id": "ch6_s3",
        "num": "6-3",
        "title": "影響反應速率的因素",
        "origPath": "../my_chem_006_反應速率/03_影響反應速率的因素/index.html",
        "origTitle": "影響反應速率的因素 | 互動教學",
        "blocks": [
          {
            "type": "slide",
            "title": "五大影響反應速率之變因",
            "subtitle": "反應物本性、濃度、接觸面積、溫度、催化劑",
            "content": "<ul>\n  <li><strong>本性 (Nature)</strong>：離子水溶液沉澱/酸鹼反應速率極快；共價鍵斷裂與生成反應相對較慢。</li>\n  <li><strong>濃度與壓力</strong>：濃度增加，單位體積內粒子數增多，<strong>碰撞頻率增加</strong>。</li>\n  <li><strong>接觸面積</strong>：異相反應（如固液、固氣）粉末化可大幅提升接觸頻率。</li>\n</ul>"
          },
          {
            "type": "checkpoint",
            "title": "單元 6-3 學習檢核",
            "desc": "完成檢核解鎖下一節。",
            "questionText": "等質量的碳酸鈣與等濃度的鹽酸反應，何者產生 CO2 的初反應速率最快？",
            "options": [
              "碳酸鈣細粉末 (接觸面積大)",
              "碳酸鈣大塊狀",
              "碳酸鈣顆粒",
              "反應速率皆相同"
            ],
            "correctIndex": 0,
            "expl": "固體粉末化使接觸表面積大幅提升，單位時間內碰撞機會增加，反應速率最快。"
          }
        ]
      },
      {
        "id": "ch6_s4",
        "num": "6-4",
        "title": "溫度與阿瑞尼斯方程式",
        "origPath": "../my_chem_006_反應速率/04_影響速率因素-溫度/index.html",
        "origTitle": "影響反應速率的因素 - 溫度 | 互動教學",
        "blocks": [
          {
            "type": "slide",
            "title": "溫度對反應速率的倍增效應",
            "subtitle": "馬克士威-波茲曼能量分佈曲線與阿瑞尼斯方程式",
            "content": "<div class=\"formula-box\">$$k = A \\cdot e^{-\\frac{E_a}{RT}} \\implies \\ln k = -\\frac{E_a}{R} \\frac{1}{T} + \\ln A$$</div>\n<p>溫度升高時，分子能量分佈曲線向高能端平移且變寬，<strong>具有超過活化能 ($E \\ge E_a$) 的高動能分子數比例呈指數級劇增</strong>，故反應速率顯著加快（一般室溫附近每升溫 10°C，速率約增為 2~3 倍）。</p>"
          },
          {
            "type": "checkpoint",
            "title": "單元 6-4 學習檢核",
            "desc": "完成檢核解鎖下一節。",
            "questionText": "升溫使反應速率大幅提高的最主要微觀原因為何？",
            "options": [
              "超過活化能的高能量有效分子數比例大幅增加",
              "分子平均碰撞頻率倍增",
              "降低了反應的活化能",
              "改變了反應途徑"
            ],
            "correctIndex": 0,
            "expl": "升溫使超過活化能之分子數百分比呈指數性增加，此效應遠大於碰撞頻率之微幅增加。"
          }
        ]
      },
      {
        "id": "ch6_s5",
        "num": "6-5",
        "title": "催化劑與反應途徑改變",
        "origPath": "../my_chem_006_反應速率/05_影響速率因素-催化劑/index.html",
        "origTitle": "催化劑與反應速率 | 互動教學",
        "blocks": [
          {
            "type": "slide",
            "title": "催化劑加速反應的機制",
            "subtitle": "降低活化能，但不改變反應熱 ΔH 與平衡常數 K",
            "content": "<ul>\n  <li>催化劑藉由參與反應，<strong>提供一條具有較低活化能的新反應途徑</strong>。</li>\n  <li>正反應活化能與逆反應活化能<strong>降低等量的數值</strong>，故正、逆反應速率等倍率提升。</li>\n  <li><strong>不變的物理量</strong>：反應熱 ($\\Delta H$)、平衡狀態、平衡常數 ($K$)、產物產率皆保持不變！</li>\n</ul>"
          },
          {
            "type": "checkpoint",
            "title": "單元 6-5 學習檢核",
            "desc": "完成檢核解鎖下一節。",
            "questionText": "加入催化劑對化學反應產生的影響，下列敘述何者正確？",
            "options": [
              "降低活化能，但反應熱 ΔH 不變",
              "降低活化能，使反應熱 ΔH 增加",
              "改變平衡常數 K",
              "使吸熱反應變成放熱反應"
            ],
            "correctIndex": 0,
            "expl": "催化劑僅提供低活化能途徑加速達到平衡，始態與終態能量不變，故反應熱 ΔH 與平衡常數 K 均不變。"
          }
        ]
      },
      {
        "id": "ch6_s6",
        "num": "6-6",
        "title": "秒錶反應互動模擬實驗",
        "origPath": "../my_chem_006_反應速率/06_秒錶反應/index.html",
        "origTitle": "秒錶反應 - 互動式模擬實驗",
        "blocks": [
          {
            "type": "slide",
            "title": "碘鐘反應 (Iodine Clock Reaction)",
            "subtitle": "碘酸鉀與亞硫酸氫鈉之競爭反應",
            "content": "<p>經典秒錶反應由兩步競爭反應組成：</p>\n<ol>\n  <li>慢反應：$\\text{IO}_3^- + 3\\text{HSO}_3^- \\rightarrow \\text{I}^- + 3\\text{SO}_4^{2-} + 3\\text{H}^+$</li>\n  <li>快反應：$\\text{IO}_3^- + 5\\text{I}^- + 6\\text{H}^+ \\rightarrow 3\\text{I}_2 + 3\\text{H}_2\\text{O}$</li>\n  <li>消耗反應：$\\text{I}_2 + \\text{HSO}_3^- + \\text{H}_2\\text{O} \\rightarrow 2\\text{I}^- + \\text{SO}_4^{2-} + 3\\text{H}^+$</li>\n</ol>\n<p>當 $\\text{HSO}_3^-$ 耗盡時，生成的 $\\text{I}_2$ 立即與澱粉結合呈現深藍色！</p>"
          },
          {
            "type": "checkpoint",
            "title": "單元 6-6 學習檢核",
            "desc": "恭喜完成第 6 章！完成此檢核進入第 7 章化學平衡。",
            "questionText": "秒錶反應中，溶液突然轉變為深藍色的關鍵瞬間為何？",
            "options": [
              "亞硫酸氫根離子 (HSO3-) 恰好耗盡，游離的 I2 與澱粉結合變色",
              "碘酸根離子 (IO3-) 完全耗盡",
              "澱粉分解",
              "生成硫酸根"
            ],
            "correctIndex": 0,
            "expl": "當還原劑 HSO3- 耗盡時，產生的 I2 無法再被還原為 I-，游離出的 I2 立即與澱粉錯合變為藍黑色。"
          }
        ]
      }
    ]
  },
  {
    "id": "ch7",
    "num": 7,
    "title": "化學平衡",
    "icon": "⚖️",
    "desc": "平衡常數 Kc 與 Kp、多重平衡規則、勒沙特略原理、溶解平衡與溶度積 Ksp、比色法實驗",
    "sections": [
      {
        "id": "ch7_s1",
        "num": "7-1",
        "title": "平衡常數表示法 (Kc, Kp)",
        "origPath": "../my_chem_007_平衡常數/01_平衡常數的表示法/index.html",
        "origTitle": "平衡常數的表示法 | 互動教學",
        "blocks": [
          {
            "type": "slide",
            "title": "平衡常數質量作用定律",
            "subtitle": "固體與純液體不列入平衡常數式",
            "content": "<div class=\"formula-box\">$$aA + bB \\rightleftharpoons cC + dD \\implies K_c = \\frac{[C]^c [D]^d}{[A]^a [B]^b}$$</div>\n<div class=\"formula-box\">$$K_p = K_c (RT)^{\\Delta n} \\quad (\\Delta n = (c+d) - (a+b))$$</div>\n<ul>\n  <li>純固體 (s) 與純液體 (l) 的濃度為定值，<strong>不寫入平衡常數式</strong>。</li>\n  <li>平衡常數 $K$ <strong>僅隨溫度改變</strong>，與濃度、壓力、催化劑無關。</li>\n</ul>"
          },
          {
            "type": "checkpoint",
            "title": "單元 7-1 學習檢核",
            "desc": "完成檢核解鎖下一節。",
            "questionText": "對於反應 CaCO3(s) <=> CaO(s) + CO2(g)，其平衡分壓常數 Kp 表示式為？",
            "options": [
              "Kp = P(CO2)",
              "Kp = P(CaO)*P(CO2)/P(CaCO3)",
              "Kp = 1/P(CO2)",
              "Kp = P(CO2)^2"
            ],
            "correctIndex": 0,
            "expl": "純固體 CaCO3 與 CaO 不列入平衡常數式，故 Kp = P(CO2)。"
          }
        ]
      },
      {
        "id": "ch7_s2",
        "num": "7-2",
        "title": "影響平衡因素與勒沙特略原理",
        "origPath": "../my_chem_007_平衡常數/02_影響平衡常數的因素/index.html",
        "origTitle": "勒沙特略原理 | 互動教學",
        "blocks": [
          {
            "type": "slide",
            "title": "勒沙特略原理 (Le Chatelier's Principle)",
            "subtitle": "抗拒外加變化的動態平衡調節",
            "content": "<p>處於平衡之系統受到外在變數干擾時，系統平衡朝向<strong>減弱該干擾方向移動</strong>：</p>\n<ul>\n  <li><strong>濃度改變</strong>：加入反應物，平衡向右；移除產物，平衡向右。</li>\n  <li><strong>壓力與體積</strong>：加壓（壓縮體積），平衡朝向<strong>氣體總莫耳數變少</strong>的方向移動。</li>\n  <li><strong>溫度改變</strong>：升溫使平衡朝<strong>吸熱方向</strong>（$\\Delta H > 0$）移動，吸熱反應之 $K$ 值隨升溫而變大。</li>\n</ul>"
          },
          {
            "type": "checkpoint",
            "title": "單元 7-2 學習檢核",
            "desc": "完成檢核解鎖下一節。",
            "questionText": "對於放熱反應 N2(g) + 3H2(g) <=> 2NH3(g) (ΔH < 0)，欲使 NH3 產量提高，應採取？",
            "options": [
              "降溫且加壓",
              "升溫且加壓",
              "升溫且減壓",
              "降溫且減壓"
            ],
            "correctIndex": 0,
            "expl": "放熱反應降溫朝放熱(右)移動；氣體係數 4 -> 2，加壓朝莫耳數少(右)移動。故降溫加壓可使平衡向右。"
          }
        ]
      },
      {
        "id": "ch7_s3",
        "num": "7-3",
        "title": "溶解平衡與溶度積 (Ksp)",
        "origPath": "../my_chem_007_平衡常數/03_溶解平衡/index.html",
        "origTitle": "溶解度積 (Ksp) | 互動教學",
        "blocks": [
          {
            "type": "slide",
            "title": "溶度積常數 (Ksp) 與沉澱判斷",
            "subtitle": "離子積 Q 與 Ksp 關係、同離子效應",
            "content": "<div class=\"formula-box\">$$A_x B_y(s) \\rightleftharpoons x A^{y+} + y B^{x-} \\implies K_{sp} = [A^{y+}]^x [B^{x-}]^y$$</div>\n<ul>\n  <li><strong>$Q < K_{sp}$</strong>：未飽和溶液，無沉澱生成。</li>\n  <li><strong>$Q = K_{sp}$</strong>：剛好達飽和平衡。</li>\n  <li><strong>$Q > K_{sp}$</strong>：過飽和，必析出沉澱直至 $Q = K_{sp}$。</li>\n  <li><strong>同離子效應</strong>：溶液中已存在共同離子時，會抑制難溶鹽溶解，使溶解度下降。</li>\n</ul>"
          },
          {
            "type": "checkpoint",
            "title": "單元 7-3 學習檢核",
            "desc": "完成檢核解鎖下一節。",
            "questionText": "若 BaSO4 在純水中的溶解度為 S，則其溶度積 Ksp 為？",
            "options": [
              "S^2",
              "4S^3",
              "S",
              "2S^2"
            ],
            "correctIndex": 0,
            "expl": "BaSO4(s) <=> Ba2+ + SO4(2-)，平衡時 [Ba2+] = S, [SO4(2-)] = S，故 Ksp = S * S = S^2。"
          }
        ]
      },
      {
        "id": "ch7_s4",
        "num": "7-4",
        "title": "比色法測平衡常數實驗",
        "origPath": "../my_chem_007_平衡常數/04_比色法測平衡常數/index.html",
        "origTitle": "比色法測平衡常數 - 互動實驗",
        "blocks": [
          {
            "type": "slide",
            "title": "硫氰化鐵錯合物比色原理",
            "subtitle": "比爾定律與標準樣品顏色深度比值",
            "content": "<div class=\"formula-box\">$$\\text{Fe}^{3+}(aq) + \\text{SCN}^-(aq) \\rightleftharpoons [\\text{Fe(SCN)}]^{2+}(aq) \\quad (\\text{血紅色})$$</div>\n<p>依比爾定律 (Beer's Law)：吸光度 $A = \\epsilon b c$。當俯視兩支比色管顏色深淺相同時，其液柱深度 ($h_1, h_2$) 與濃度成反比：</p>\n<div class=\"formula-box\">$$C_1 h_1 = C_2 h_2 \\implies C_1 = C_2 \\frac{h_2}{h_1}$$</div>"
          },
          {
            "type": "checkpoint",
            "title": "單元 7-4 學習檢核",
            "desc": "恭喜完成第 7 章！完成此檢核進入第 8 章酸鹼鹽。",
            "questionText": "在比色法測平衡常數實驗中，Fe3+ 與 SCN- 生成之血紅色錯離子化學式為？",
            "options": [
              "[Fe(SCN)]2+",
              "[Fe(SCN)6]3-",
              "FeS",
              "Fe(OH)3"
            ],
            "correctIndex": 0,
            "expl": "鐵離子與硫氰酸根生成血紅色的一配位硫氰酸鐵錯離子 [Fe(SCN)]2+。"
          }
        ]
      }
    ]
  },
  {
    "id": "ch8",
    "num": 8,
    "title": "酸鹼鹽",
    "icon": "🧫",
    "desc": "酸鹼通性與命名、布忍斯特-羅瑞共軛酸鹼學說、Kw與pH計算、弱酸解離平衡、酸鹼中和與滴定曲線",
    "sections": [
      {
        "id": "ch8_s1",
        "num": "8-1",
        "title": "酸鹼通性與命名",
        "origPath": "../my_chem_008_酸鹼鹽/01_酸鹼的通性與命名/index.html",
        "origTitle": "酸、鹼、鹽的命名 | 互動教學",
        "blocks": [
          {
            "type": "slide",
            "title": "常見強酸強鹼與命名法則",
            "subtitle": "六大強酸與二大強鹼家族",
            "content": "<div class=\"flex-row\">\n  <div class=\"flex-col\">\n    <h3 class=\"text-red\">六大無機強酸</h3>\n    <ul>\n      <li>高氯酸 ($\\text{HClO}_4$)</li>\n      <li>氫碘酸 ($\\text{HI}$)、氫溴酸 ($\\text{HBr}$)、鹽酸 ($\\text{HCl}$)</li>\n      <li>硫酸 ($\\text{H}_2\\text{SO}_4$)、硝酸 ($\\text{HNO}_3$)</li>\n    </ul>\n  </div>\n  <div class=\"flex-col\">\n    <h3 class=\"text-blue\">強鹼家族</h3>\n    <ul>\n      <li>$1A$ 族鹼金屬氫氧化物：$\\text{LiOH, NaOH, KOH...}$</li>\n      <li>$2A$ 族較重金屬氫氧化物：$\\text{Ca(OH)}_2, \\text{Sr(OH)}_2, \\text{Ba(OH)}_2$</li>\n    </ul>\n  </div>\n</div>"
          },
          {
            "type": "checkpoint",
            "title": "單元 8-1 學習檢核",
            "desc": "完成檢核解鎖下一節。",
            "questionText": "下列何者屬於弱酸（在水中僅部分解離）？",
            "options": [
              "HF 氫氟酸",
              "HCl 鹽酸",
              "HNO3 硝酸",
              "H2SO4 硫酸"
            ],
            "correctIndex": 0,
            "expl": "HF 氫氟酸因鍵能大且水合半徑小，在水中為弱酸；HCl、HNO3、H2SO4 皆為強酸。"
          }
        ]
      },
      {
        "id": "ch8_s2",
        "num": "8-2",
        "title": "酸鹼學說 (布忍斯特-羅瑞與路易斯)",
        "origPath": "../my_chem_008_酸鹼鹽/02_酸鹼理論/index.html",
        "origTitle": "酸鹼學說 - 互動教學",
        "blocks": [
          {
            "type": "slide",
            "title": "質子轉移與電子對酸鹼定義",
            "subtitle": "共軛酸鹼對 (Conjugate Acid-Base Pair)",
            "content": "<ul>\n  <li><strong>阿瑞尼斯說</strong>：水中解離出 $\\text{H}^+$ 者為酸，解離出 $\\text{OH}^-$ 者為鹼。</li>\n  <li><strong>布忍斯特-羅瑞說</strong>：<strong>質子 ($\\text{H}^+$) 給予者為酸，質子接受者為鹼</strong>。相差一個質子者互為「共軛酸鹼對」。</li>\n  <li><strong>路易斯說</strong>：<strong>提供孤對電子對者為鹼，接受孤對電子對者為酸</strong>。</li>\n</ul>"
          },
          {
            "type": "checkpoint",
            "title": "單元 8-2 學習檢核",
            "desc": "完成檢核解鎖下一節。",
            "questionText": "在水溶液中，H2O 提供質子給 NH3 形成 NH4+ 與 OH-，在此反應中 H2O 扮演何種角色？",
            "options": [
              "布忍斯特酸 (質子給予者)",
              "布忍斯特鹼 (質子接受者)",
              "路易斯鹼",
              "催化劑"
            ],
            "correctIndex": 0,
            "expl": "H2O 釋放出 H+ 轉移給 NH3，依布忍斯特-羅瑞定義，質子給予者為酸。"
          }
        ]
      },
      {
        "id": "ch8_s3",
        "num": "8-3",
        "title": "水的解離、pH 與弱酸解離平衡",
        "origPath": "../my_chem_008_酸鹼鹽/03_酸鹼的解離與水解/index.html",
        "origTitle": "酸鹼的解離與水解 | 互動教學",
        "blocks": [
          {
            "type": "slide",
            "title": "水的離子積常數 Kw 與弱酸 Ka 計算",
            "subtitle": "25°C 下 Kw = 10^-14，pH + pOH = 14",
            "content": "<div class=\"formula-box\">$$K_w = [\\text{H}^+][\\text{OH}^-] = 1.0 \\times 10^{-14} \\quad (25^\\circ\\text{C})$$</div>\n<div class=\"formula-box\">$$\\text{單質子弱酸 HA 解離：} [\\text{H}^+] \\approx \\sqrt{C_0 \\cdot K_a} \\quad (\\text{若 } \\alpha < 5\\%)$$</div>\n<p>鹽類水解規律：強酸弱鹼鹽水解呈弱酸性（如 $\\text{NH}_4\\text{Cl}$）；弱酸強鹼鹽水解呈弱鹼性（如 $\\text{CH}_3\\text{COONa}$）。</p>"
          },
          {
            "type": "checkpoint",
            "title": "單元 8-3 學習檢核",
            "desc": "完成檢核解鎖下一節。",
            "questionText": "在 25°C 下，0.1 M 醋酸溶液 (Ka = 1.8 x 10^-5) 的 [H+] 約為？",
            "options": [
              "1.34 x 10^-3 M",
              "0.1 M",
              "1.8 x 10^-6 M",
              "1.0 x 10^-7 M"
            ],
            "correctIndex": 0,
            "expl": "[H+] ≈ sqrt(C0 * Ka) = sqrt(0.1 * 1.8*10^-5) = sqrt(1.8*10^-6) ≈ 1.34*10^-3 M。"
          }
        ]
      },
      {
        "id": "ch8_s4",
        "num": "8-4",
        "title": "酸鹼中和與滴定曲線",
        "origPath": "../my_chem_008_酸鹼鹽/04_酸鹼中和/index.html",
        "origTitle": "8-4 酸鹼中和與滴定曲線 · 互動教學",
        "blocks": [
          {
            "type": "slide",
            "title": "當量點、終點與滴定曲線特徵",
            "subtitle": "強酸滴定弱酸之半當量點 pH = pKa 緩衝區",
            "content": "<ul>\n  <li><strong>當量點 (Equivalence Point)</strong>：酸提供之 $\\text{H}^+$ 莫耳數等於鹼提供之 $\\text{OH}^-$ 莫耳數 ($N_A V_A = N_B V_B$)。</li>\n  <li><strong>強酸強鹼滴定</strong>：當量點 $\\text{pH} = 7$。</li>\n  <li><strong>強鹼滴定弱酸</strong>：當量點因弱酸根水解呈弱鹼性 ($\\text{pH} > 7$)，適合以<strong>酚酞</strong>為指示劑；在半當量點時 $[\\text{HA}] = [\\text{A}^-]$，故 $\\text{pH} = pK_a$。</li>\n</ul>"
          },
          {
            "type": "checkpoint",
            "title": "單元 8-4 學習檢核",
            "desc": "完成檢核解鎖下一節：8-5 緩衝溶液與同離子效應。",
            "questionText": "以 0.1 M NaOH 滴定 0.1 M 醋酸 (CH3COOH)，當量點時溶液的 pH 值範圍為何？",
            "options": [
              "pH > 7 (弱鹼性，因醋酸根水解)",
              "pH = 7",
              "pH < 7",
              "pH = 1"
            ],
            "correctIndex": 0,
            "expl": "當量點生成醋酸鈉，弱酸根 CH3COO- 在水中發生水解生成 OH-，使溶液呈弱鹼性 (pH > 7)。"
          }
        ]
      },
      {
        "id": "ch8_s5",
        "num": "8-5",
        "title": "緩衝溶液與同離子效應",
        "origPath": "../my_chem_008_酸鹼鹽/06_緩衝溶液/index.html",
        "origTitle": "8-5 緩衝溶液與同離子效應 | 互動教學（建置中）",
        "blocks": [
          {
            "type": "slide",
            "title": "緩衝溶液原理與組成條件",
            "subtitle": "同離子效應、Henderson-Hasselbalch 方程式與血液緩衝系統",
            "content": "<p><strong>緩衝溶液 (Buffer Solution)</strong> 能在外加少量強酸或強鹼時，抵抗 $\\text{pH}$ 的大幅劇變：</p>\n<ul>\n  <li><strong>酸性緩衝液</strong>：弱酸及其共軛鹼鹽（如 $\\text{CH}_3\\text{COOH} + \\text{CH}_3\\text{COONa}$），$\\text{pH} = pK_a + \\log\\frac{[\\text{A}^-]}{[\\text{HA}]}$。</li>\n  <li><strong>鹼性緩衝液</strong>：弱鹼及其共軛酸鹽（如 $\\text{NH}_3 + \\text{NH}_4\\text{Cl}$），$\\text{pOH} = pK_b + \\log\\frac{[\\text{BH}^+]}{[\\text{B}]}$。</li>\n  <li><strong>緩衝容量最大點</strong>：弱酸與其鹽濃度相等時 ($[\\text{HA}] = [\\text{A}^-]$)，$\\text{pH} = pK_a$。</li>\n</ul>"
          },
          {
            "type": "checkpoint",
            "title": "單元 8-5 學習檢核",
            "desc": "恭喜完成第 8 章！完成此檢核進入第 9 章氧化還原。",
            "questionText": "下列哪一組水溶液組合具有顯著的酸鹼緩衝能力？",
            "options": [
              "CH3COOH 與 CH3COONa",
              "HCl 與 NaCl",
              "NaOH 與 NaCl",
              "HNO3 與 KNO3"
            ],
            "correctIndex": 0,
            "expl": "緩衝溶液必須由「弱酸與其共軛鹼鹽」或「弱鹼與其共軛酸鹽」組成；強酸強鹼與其鹽類無緩衝效果。"
          }
        ]
      }
    ]
  },
  {
    "id": "ch9",
    "num": 9,
    "title": "氧化還原反應與電化學",
    "icon": "⚡",
    "desc": "氧化數規則、氧化劑與還原劑、方程式平衡、氧化還原滴定、標準電位、化學電池與電解電鍍",
    "sections": [
      {
        "id": "ch9_s1",
        "num": "9-1",
        "title": "氧化數規則與原子氧化態判斷",
        "origPath": "../my_chem_009_氧化還原/01_氧化數/index.html",
        "origTitle": "Oxidation Master Pro | 進階氧化數解析平台",
        "blocks": [
          {
            "type": "slide",
            "title": "氧化數核心判定法則",
            "subtitle": "氧化數增加為氧化，氧化數減少為還原",
            "content": "<ul>\n  <li>元素態物質（如 $\\text{O}_2, \\text{Fe}$）氧化數為 $0$。</li>\n  <li>化合物中：氟必為 $-1$；$1A$ 金屬必為 $+1$；$2A$ 金屬必為 $+2$。</li>\n  <li>氫通常為 $+1$（但在活潑金屬氫化物如 $\\text{NaH}$ 中為 $-1$）。</li>\n  <li>氧通常為 $-2$（但在過氧化物 $\\text{H}_2\\text{O}_2$ 中為 $-1$；超氧化物中為 $-\\frac{1}{2}$；$\\text{OF}_2$ 中為 $+2$）。</li>\n  <li>中性分子中所有原子氧化數總和為 $0$。</li>\n</ul>"
          },
          {
            "type": "checkpoint",
            "title": "單元 9-1 學習檢核",
            "desc": "完成檢核解鎖下一節。",
            "questionText": "在過錳酸鉀 (KMnO4) 化合物中，錳 (Mn) 原子的氧化數為多少？",
            "options": [
              "+7",
              "+2",
              "+4",
              "+6"
            ],
            "correctIndex": 0,
            "expl": "K 為 +1，O 為 -2 * 4 = -8，分子總和為 0，故 (+1) + Mn + (-8) = 0 => Mn = +7。"
          }
        ]
      },
      {
        "id": "ch9_s2",
        "num": "9-2",
        "title": "氧化還原方程式平衡 (半反應法)",
        "origPath": "../my_chem_009_氧化還原/03_氧化還原方程式平衡/index.html",
        "origTitle": "氧化還原方程式平衡 | 互動教學",
        "blocks": [
          {
            "type": "slide",
            "title": "半反應平衡五步心法 (酸性介質)",
            "subtitle": "質量守恆與電子得失電荷守恆",
            "content": "<ol>\n  <li><strong>拆分</strong>：將總反應拆為氧化半反應與還原半反應。</li>\n  <li><strong>平衡非 H、O 原子</strong>。</li>\n  <li><strong>加水補氧</strong>：欠缺氧原子端以 $\\text{H}_2\\text{O}$ 補平。</li>\n  <li><strong>加酸補氫</strong>：欠缺氫原子端以 $\\text{H}^+$ 補平。</li>\n  <li><strong>加電子補電荷</strong>：使半反應兩端電荷守恆。</li>\n  <li><strong>得失電子相消相加</strong>：最小公倍數消除電子即得全反應式。</li>\n</ol>"
          },
          {
            "type": "checkpoint",
            "title": "單元 9-2 學習檢核",
            "desc": "完成檢核解鎖下一節。",
            "questionText": "酸性溶液中，MnO4- 被還原為 Mn2+ 時，每莫耳 MnO4- 需吸收多少莫耳電子？",
            "options": [
              "5 mol 電子",
              "3 mol 電子",
              "2 mol 電子",
              "7 mol 電子"
            ],
            "correctIndex": 0,
            "expl": "Mn 氧化數由 +7 降至 +2，差值為 5，故需獲得 5 莫耳電子 (MnO4- + 8H+ + 5e- -> Mn2+ + 4H2O)。"
          }
        ]
      },
      {
        "id": "ch9_s3",
        "num": "9-3",
        "title": "氧化劑與還原劑強弱比較",
        "origPath": "../my_chem_009_氧化還原/02_氧化劑與還原劑/index.html",
        "origTitle": "氧化劑與還原劑 - 互動教學",
        "blocks": [
          {
            "type": "slide",
            "title": "得失電子與自身氧化還原",
            "subtitle": "自身被還原者為氧化劑，自身被氧化者為還原劑",
            "content": "<div class=\"flex-row\">\n  <div class=\"flex-col\">\n    <h3 class=\"text-red\">氧化劑 (Oxidizing Agent)</h3>\n    <p>自身得到電子、氧化數降低，促使他人氧化。如酸性過錳酸鉀 ($\\text{MnO}_4^-$)、重鉻酸鉀 ($\\text{Cr}_2\\text{O}_7^{2-}$)、濃硝酸。</p>\n  </div>\n  <div class=\"flex-col\">\n    <h3 class=\"text-green\">還原劑 (Reducing Agent)</h3>\n    <p>自身失去電子、氧化數升高，促使他人還原。如金屬活性大的金屬單質 ($\\text{Zn, Mg}$)、草酸 ($\\text{H}_2\\text{C}_2\\text{O}_4$)、$\\text{SO}_2$。</p>\n  </div>\n</div>"
          },
          {
            "type": "checkpoint",
            "title": "單元 9-3 學習檢核",
            "desc": "完成檢核解鎖下一節。",
            "questionText": "反應 Zn + Cu2+ -> Zn2+ + Cu 中，何者扮演還原劑？",
            "options": [
              "Zn (失去電子，自身被氧化)",
              "Cu2+",
              "Zn2+",
              "Cu"
            ],
            "correctIndex": 0,
            "expl": "Zn 氧化數由 0 升至 +2（失去電子，自身被氧化），使 Cu2+ 還原，故 Zn 為還原劑。"
          }
        ]
      },
      {
        "id": "ch9_s4",
        "num": "9-4",
        "title": "氧化還原滴定 (過錳酸鉀滴定)",
        "origPath": "../my_chem_009_氧化還原/04_氧化還原滴定/index.html",
        "origTitle": "氧化還原滴定 | 互動教學",
        "blocks": [
          {
            "type": "slide",
            "title": "自體指示劑過錳酸鉀滴定草酸",
            "subtitle": "氧化還原當量關係式：得電子數 = 失電子數",
            "content": "<div class=\"formula-box\">$$2\\text{MnO}_4^- + 5\\text{H}_2\\text{C}_2\\text{O}_4 + 6\\text{H}^+ \\rightarrow 2\\text{Mn}^{2+} + 10\\text{CO}_2 + 8\\text{H}_2\\text{O}$$</div>\n<ul>\n  <li>$\\text{KMnO}_4$ 自帶鮮豔紫紅色，滴定終點時一滴過量的 $\\text{MnO}_4^-$ 即可使溶液呈現微粉紅色，<strong>不需外加指示劑</strong>。</li>\n  <li>通常加入稀硫酸酸化，不可使用鹽酸（$\\text{Cl}^-$ 會被氧化）或硝酸（具氧化性）。</li>\n</ul>"
          },
          {
            "type": "checkpoint",
            "title": "單元 9-4 學習檢核",
            "desc": "完成檢核解鎖下一節。",
            "questionText": "在過錳酸鉀滴定實驗中，為何通常使用稀硫酸 (H2SO4) 來酸化溶液，而不用鹽酸 (HCl)？",
            "options": [
              "鹽酸中的氯離子 (Cl-) 會被強氧化劑 KMnO4 氧化為氯氣干擾滴定",
              "硫酸較便宜",
              "鹽酸會與草酸反應",
              "硫酸是弱酸"
            ],
            "correctIndex": 0,
            "expl": "MnO4- 氧化力極強會將 Cl- 氧化成 Cl2，消耗額外滴定液導致測定誤差；硫酸根則不會被氧化。"
          }
        ]
      },
      {
        "id": "ch9_s5",
        "num": "9-5",
        "title": "標準還原電位與半電池 (E°)",
        "origPath": "../my_chem_009_氧化還原/05_標準還原電位/index.html",
        "origTitle": "標準電位測量 - 互動式學習",
        "blocks": [
          {
            "type": "slide",
            "title": "標準氫電極 (SHE) 與電池電動勢",
            "subtitle": "25°C 下規定 2H+ + 2e- <=> H2 之 E° = 0.00 V",
            "content": "<div class=\"formula-box\">$$E^\\circ_{\\text{cell}} = E^\\circ_{\\text{陰極(還原)}} - E^\\circ_{\\text{陽極(氧化)}}$$</div>\n<ul>\n  <li><strong>標準還原電位 ($E^\\circ$) 愈正</strong>：還原能力愈強，氧化劑強度愈強（如 $\\text{F}_2, E^\\circ = +2.87\\text{ V}$）。</li>\n  <li><strong>標準還原電位 ($E^\\circ$) 愈負</strong>：還原態愈易失去電子，還原劑強度愈強（如 $\\text{Li}, E^\\circ = -3.05\\text{ V}$）。</li>\n  <li>$E^\\circ_{\\text{cell}} > 0$ 代表自發反應。</li>\n</ul>"
          },
          {
            "type": "checkpoint",
            "title": "單元 9-5 學習檢核",
            "desc": "完成檢核解鎖下一節。",
            "questionText": "已知 Zn2+/Zn 之 E° = -0.76 V，Cu2+/Cu 之 E° = +0.34 V，則 Zn-Cu 丹尼耳電池標準電動勢為？",
            "options": [
              "+1.10 V",
              "+0.42 V",
              "-1.10 V",
              "+0.58 V"
            ],
            "correctIndex": 0,
            "expl": "E°cell = E°(陰極Cu) - E°(陽極Zn) = (+0.34) - (-0.76) = +1.10 V。"
          }
        ]
      },
      {
        "id": "ch9_s6",
        "num": "9-6",
        "title": "常見化學電池",
        "origPath": "../my_chem_009_氧化還原/06_化學電池/index.html",
        "origTitle": "常用電池 | 互動教學",
        "blocks": [
          {
            "type": "slide",
            "title": "一次電池與二次充電電池",
            "subtitle": "乾電池、鉛蓄電池與氫氧燃料電池",
            "content": "<ul>\n  <li><strong>鋅碳乾電池</strong>：負極為鋅殼，正極為碳棒加 $\\text{MnO}_2$；一次電池不可充電。</li>\n  <li><strong>鉛蓄電池 (Lead-Acid)</strong>：負極為鉛 ($\\text{Pb}$)，正極為二氧化鉛 ($\\text{PbO}_2$)，電解液為硫酸。放電時兩極皆生成白色 $\\text{PbSO}_4$，硫酸濃度與密度下降；可反覆充電。</li>\n  <li><strong>氫氧燃料電池</strong>：負極通 $\\text{H}_2$，正極通 $\\text{O}_2$，產物為純水，能量轉換效率高且零碳排。</li>\n</ul>"
          },
          {
            "type": "checkpoint",
            "title": "單元 9-6 學習檢核",
            "desc": "完成檢核解鎖下一節。",
            "questionText": "鉛蓄電池在放電過程中，負極與正極所生成的共同化學物質為何？",
            "options": [
              "硫酸鉛 (PbSO4)",
              "金屬鉛 (Pb)",
              "二氧化鉛 (PbO2)",
              "硫酸 (H2SO4)"
            ],
            "correctIndex": 0,
            "expl": "放電時負極 Pb 氧化成 PbSO4，正極 PbO2 還原成 PbSO4，兩極重量皆增加。"
          }
        ]
      },
      {
        "id": "ch9_s7",
        "num": "9-7",
        "title": "電解與電鍍、法拉第電解定律",
        "origPath": "../my_chem_009_氧化還原/07_電解與電鍍/index.html",
        "origTitle": "法拉第電解定律與電解電鍍 | 互動教學",
        "blocks": [
          {
            "type": "slide",
            "title": "法拉第電解定律",
            "subtitle": "通電量 Q = I * t 與析出物質莫耳數關係",
            "content": "<div class=\"formula-box\">$$Q = I \\cdot t = n_e \\cdot F \\quad (1\\text{ F} = 96500\\text{ 庫侖/莫耳電子})$$</div>\n<div class=\"formula-box\">$$W = \\frac{I \\cdot t}{96500} \\cdot \\frac{M}{n}$$</div>\n<p><strong>電鍍原理</strong>：被鍍物接在<strong>陰極</strong>（吸引陽離子析出鍍層）；鍍層金屬接在<strong>陽極</strong>（不斷氧化溶解補充離子）；含有鍍層金屬離子的鹽類作為電解液。</p>"
          },
          {
            "type": "checkpoint",
            "title": "單元 9-7 學習檢核",
            "desc": "恭喜完成第 9 章！完成此檢核進入第 10 章無機化合物。",
            "questionText": "欲在鐵湯匙表面鍍上一層銀 (Ag)，鐵湯匙應連接在電源的哪一極？",
            "options": [
              "陰極 (負極，發生還原析出銀)",
              "陽極 (正極)",
              "兩者皆可",
              "不接電"
            ],
            "correctIndex": 0,
            "expl": "電鍍時被鍍金屬件必須置於陰極，使金屬陽離子 Ag+ 獲得電子析出均勻沉積在表面。"
          }
        ]
      }
    ]
  },
  {
    "id": "ch10",
    "num": 10,
    "title": "無機化合物",
    "icon": "🧱",
    "desc": "週期表與元素規律、主族非金屬化合物、過渡金屬錯合物與常見重要無機試劑",
    "sections": [
      {
        "id": "ch10_s1",
        "num": "10-1",
        "title": "互動式元素週期表探索與性質通論",
        "origPath": "../my_chem_010_無機化合物/000_週期表/index.html",
        "origTitle": "互動式週期表與測驗系統",
        "blocks": [
          {
            "type": "slide",
            "title": "週期表族與區塊劃分",
            "subtitle": "s 區、p 區、d 區與 f 區元素分佈",
            "content": "<ul>\n  <li><strong>鹼金屬 (1A)</strong>：質軟、密度小、強還原性，與水劇烈反應產生 $\\text{H}_2$ 與強鹼。</li>\n  <li><strong>鹵素 (7A)</strong>：單質雙原子分子，由上至下顏色加深 (F2 淡黃、Cl2 黃綠、Br2 紅棕液體、I2 紫黑固體)，氧化力依次減弱。</li>\n  <li><strong>鈍氣 (8A)</strong>：八隅體全滿穩定，單原子氣體。</li>\n</ul>"
          },
          {
            "type": "checkpoint",
            "title": "單元 10-1 學習檢核",
            "desc": "完成檢核解鎖下一節。",
            "questionText": "常溫常壓下，唯一呈現紅棕色液態的非金屬元素單質為何？",
            "options": [
              "溴 (Br2)",
              "汞 (Hg)",
              "碘 (I2)",
              "氯 (Cl2)"
            ],
            "correctIndex": 0,
            "expl": "常溫下只有兩種液態元素單質：金屬為汞 (Hg)，非金屬為紅棕色的溴 (Br2)。"
          }
        ]
      },
      {
        "id": "ch10_s2",
        "num": "10-2",
        "title": "常見無機非金屬與金屬元素化合物",
        "origPath": "",
        "origTitle": "",
        "blocks": [
          {
            "type": "slide",
            "title": "重要過渡元素與錯合物概論",
            "subtitle": "中心金屬離子、配位基與配位鍵",
            "content": "<ul>\n  <li><strong>錯合物 (Complex)</strong>：過渡金屬具有未填滿之 $d$ 軌域，接受配位基（具孤對電子的分子或離子如 $\\text{H}_2\\text{O}, \\text{NH}_3, \\text{CN}^-, \\text{Cl}^-$）提供電子對形成<strong>配位共價鍵</strong>。</li>\n  <li><strong>顏色特徵</strong>：$d$ 軌域受配位場分裂 ($d-d$ 躍遷)，吸收特定波長可見光，常呈現鮮豔顏色（如 $[\\text{Cu(H}_2\\text{O)}_4]^{2+}$ 呈天藍色，$[\\text{Cu(NH}_3)_4]^{2+}$ 呈深深藍色）。</li>\n</ul>"
          },
          {
            "type": "checkpoint",
            "title": "單元 10-2 學習檢核",
            "desc": "恭喜完成第 10 章！完成此檢核進入第 11 章有機化合物。",
            "questionText": "在水合銅離子 [Cu(H2O)4]2+ 錯合物中，水分子 (H2O) 扮演何種角色？",
            "options": [
              "配位基 (提供孤對電子對)",
              "中心陽離子",
              "還原劑",
              "酸催化劑"
            ],
            "correctIndex": 0,
            "expl": "水分子提供孤對電子對與中心 Cu2+ 形成配位鍵，故稱為配位基 (Ligand)。"
          }
        ]
      }
    ]
  },
  {
    "id": "ch11",
    "num": 11,
    "title": "有機化合物",
    "icon": "🌿",
    "desc": "碳鏈結構、同分異構物、烴類、醇酚醚、醛酮、羧酸酯與高分子聚合物",
    "sections": [
      {
        "id": "ch11_s1",
        "num": "11-1",
        "title": "有機化合物結構與同分異構物",
        "origPath": "",
        "origTitle": "",
        "blocks": [
          {
            "type": "slide",
            "title": "同分異構物三大類別",
            "subtitle": "分子式相同，結構或空間排列不同",
            "content": "<ul>\n  <li><strong>結構異構物</strong>：\n    <ul>\n      <li>骨架異構物：如正丁烷與異丁烷。</li>\n      <li>位置異構物：如 1-丙醇與 2-丙醇。</li>\n      <li>官能基異構物：如乙醇 ($\\text{C}_2\\text{H}_5\\text{OH}$) 與二甲醚 ($\\text{CH}_3\\text{OCH}_3$)。</li>\n    </ul>\n  </li>\n  <li><strong>幾何異構物 (順反異構)</strong>：雙鍵不能自由旋轉，如順-2-丁烯與反-2-丁烯。</li>\n  <li><strong>光學異構物 (鏡像異構)</strong>：具<strong>對掌碳原子</strong>（連接 4 個相異基團）。</li>\n</ul>"
          },
          {
            "type": "checkpoint",
            "title": "單元 11-1 學習檢核",
            "desc": "完成檢核解鎖下一節。",
            "questionText": "分子式為 C2H6O 的有機化合物，具有兩種互為官能基異構物的結構，分別為何？",
            "options": [
              "乙醇 (醇類) 與二甲醚 (醚類)",
              "乙酸與乙酸乙酯",
              "乙烷與乙烯",
              "乙醛與丙酮"
            ],
            "correctIndex": 0,
            "expl": "C2H6O 可寫成醇類的乙醇 (C2H5OH) 或醚類的二甲醚 (CH3OCH3)，二者互為官能基異構物。"
          }
        ]
      },
      {
        "id": "ch11_s2",
        "num": "11-2",
        "title": "常見有機官能基與反應概述",
        "origPath": "",
        "origTitle": "",
        "blocks": [
          {
            "type": "slide",
            "title": "主要官能基家族特徵",
            "subtitle": "醇酚醚、醛酮、酸酯的氧化與酯化反應",
            "content": "<ul>\n  <li><strong>醇 ($-OH$)</strong>：一級醇氧化得醛再氧化得羧酸；二級醇氧化得酮；三級醇不易被氧化。</li>\n  <li><strong>醛 ($-CHO$) 與 酮 ($>C=O$)</strong>：醛具還原性，可發生斐林試劑 (生成紅磚色 Cu2O) 或多侖試劑 (銀鏡反應)；酮不反應。</li>\n  <li><strong>酯化反應</strong>：羧酸 $+$ 醇 $\\xrightarrow{\\text{濃 } \\text{H}_2\\text{SO}_4}$ 酯 $+$ 水（具芳香氣味）。</li>\n</ul>"
          },
          {
            "type": "checkpoint",
            "title": "單元 11-2 學習檢核",
            "desc": "恭喜完成第 11 章！完成此檢核進入第 12 章生活中的化學。",
            "questionText": "下列何種有機化合物能與多侖試劑反應產生光亮的「銀鏡反應」？",
            "options": [
              "甲醛 (含有醛基 -CHO)",
              "丙酮 (酮類)",
              "乙醇 (醇類)",
              "乙酸乙酯 (酯類)"
            ],
            "correctIndex": 0,
            "expl": "醛類具還原性，能將多侖試劑中的銀氨錯離子 [Ag(NH3)2]+ 還原為金屬銀鍍在管壁形成銀鏡。"
          }
        ]
      }
    ]
  },
  {
    "id": "ch12",
    "num": 12,
    "title": "生活中的化學及補充",
    "icon": "🌍",
    "desc": "光觸媒 TiO2、導電高分子、界面活性劑與新興綠色生活材料",
    "sections": [
      {
        "id": "ch12_s1",
        "num": "12-1",
        "title": "新興綠色生活化學材料",
        "origPath": "",
        "origTitle": "",
        "blocks": [
          {
            "type": "slide",
            "title": "生活中的尖端化學材料",
            "subtitle": "光觸媒 TiO2、導電塑膠與界面活性劑",
            "content": "<ul>\n  <li><strong>光觸媒 (TiO2)</strong>：吸收紫外光激發產生電子與電洞，產生超氧陰離子與氫氧自由基，強效降解環境污染物與抗菌。</li>\n  <li><strong>導電高分子</strong>：如聚乙炔具共軛雙鍵，經碘或鈉摻雜 (Doping) 後具備類金屬導電性。</li>\n  <li><strong>界面活性劑</strong>：分子具親水端與疏水端，在水中形成微胞 (Micelle) 包覆油污乳化去污。</li>\n</ul>"
          },
          {
            "type": "checkpoint",
            "title": "單元 12-1 學習檢核",
            "desc": "🎉 恭喜！您已全數完成高中化學學習網全部 12 章課程！",
            "questionText": "肥皂去污的微觀機制中，其長碳氫鏈主要扮演何種角色？",
            "options": [
              "親油端 (疏水端)，深入油污內部",
              "親水端，溶於水中",
              "催化劑",
              "漂白劑"
            ],
            "correctIndex": 0,
            "expl": "肥皂分子的非極性碳氫長鏈為疏水親油端，能深入油污使其乳化懸浮於水中。"
          }
        ]
      }
    ]
  }
];
