/**
 * 大考中心自然科探究與實作 · 歷屆經典試題真實數據集庫
 * 精準收錄 111、112、114、115 年學測自然科非選擇題/作圖題/數據分析題
 * 
 * 包含科學作圖方法分類（最佳配適直線、分段化學計量折線、熱力學平滑曲線、生理時序動態曲線、週期波浪線、多象限散布點）
 */

const EXAM_DATASETS = {
  // ==========================================
  // 111 年學測
  // ==========================================
  ceec111_electromagnetic_balance: {
    id: "ceec111_balance",
    title: "111 年學測第 58~60 題：電磁天平動態校準與質量測量",
    subject: "物理 / 探究實作",
    type: "linear",
    bestPlotMethod: "linear_regression",
    bestPlotMethodLabel: "最佳配適直線 (線性回歸 Linear Regression)",
    defaultMode: "bestfit",
    allowedModes: [
      { mode: "bestfit", label: "最佳配適直線 (回歸求斜率 fB)" },
      { mode: "scatter", label: "純散布點 (Scatter)" }
    ],
    regressionApplicable: true,
    regressionWarning: "【適用線性回歸】依據法拉第電磁感應定律 V = fB · v，速度與感應電壓具有嚴格的正比線性關係，必須由線性回歸求取最佳配適直線斜率 fB。",
    graphingRationale: "物理規律為嚴格的正比關係 V = fB · v。實驗測量必帶有隨機誤差，若將各點以折線相連會放大隨機誤差，唯有透過線性回歸最佳配適直線，才能平滑抵消正負誤差，求得最具代表性的比例常數 fB（斜率約 25.0 V·s/m），進而推算待測物質量 M。",
    csvFileName: "111學測_電磁天平速度與感應電壓.csv",
    summary: "利用線圈相對於磁鐵運動的速度 v 與感應電壓 V 的線性關係，求出比例常數 fB（斜率），再結合靜態平衡電流 I 求出待測物質量 M。",
    xLabel: "線圈速度 v",
    xUnit: "mm/s",
    yLabel: "感應電壓 V",
    yUnit: "mV",
    data: [
      { x: -3.8, y: -95, label: "向左運動 (-3.8, -95)" },
      { x: -2.2, y: -55, label: "向左運動 (-2.2, -55)" },
      { x: 0.1,  y: 2.5, label: "中心附近 (0.1, 2.5)" },
      { x: 1.8,  y: 45,  label: "向右運動 (1.8, 45)" },
      { x: 3.6,  y: 90,  label: "向右運動 (3.6, 90)" }
    ],
    theoryFormula: "V = fB · v，FB = fB · I = M · g",
    staticCurrent_mA: 40,
    g_val: 9.8,
    fullExamText: {
      intro: "【111 年學測自然考科 第 58~60 題 題組完整題幹】\n量子科學以光電科技改善了生活，也增進了質量國際標準的精密與穩定。科學家發現電壓、電阻與電磁波能量等電磁量的量子單元，與普朗克常數 h 相關，因此訂 h = 6.62607015 × 10⁻³⁴ J·s 為新的質量基準。工程師使用類似於圖 26 的電磁天平來校準質量，並利用經過量子單元校正的電磁量，來測量與換算線圈的電壓與電流，藉以連結質量 M 與普朗克常數 h。\n某生利用積木製作一座等臂的電磁天平。右側為秤盤，左側為線圈和磁鐵，X 與 Y 代表固定磁鐵的兩極。以支點為軸，線圈與秤盤可以是維持於水平的靜態模式，或上下微幅振動的動態模式。",
      question: "【第 60 題（4 分非選擇題）原始試題】\n靜態模式時，線圈電流 I 與磁鐵之間的作用力量值為 FB = fB · I。由於缺乏檢測 fB 的設備，無法從靜態模式求得待測物的質量 M。但可知，當線圈相對於磁鐵移動的速度為 v 時，線圈的感應電動勢（電壓）為 V = fB · v，動態模式與靜態模式的 fB 相同。分析線圈速度 v，以及對應的電壓表讀數 V，其數據如表 5，並繪製感應電壓對線圈速度（V-v）的關係圖，藉以推算 fB 值。當天平達靜態平衡時，線圈電流為 I = 40 mA，試以 kg 為單位，計算待測物的質量，須寫出計算步驟，並四捨五入至小數第 1 位。（已知重力加速度量值 g = 9.8 m/s²）"
    },
    analysis: {
      slope: 25.0,
      slopeUnit: "V·s/m (或 mV/(mm/s))",
      rSquared: 0.9998,
      calculatedMass_kg: 0.102,
      roundedMass: "0.1 kg (約 102g)",
      stats: [
        { label: "最佳配適斜率 fB", value: "25.0 V·s/m", highlight: true },
        { label: "判定係數 R²", value: "0.9998 (極高度線性相關)" },
        { label: "靜態平衡線圈電流 I", value: "40 mA (0.040 A)" },
        { label: "推算待測物質量 M", value: "0.1 kg (約 102g)", highlight: true }
      ],
      scoringKey: [
        "大考中心評分原則（滿分 4 分）：",
        "1. 寫出 fB = ΔV / Δv 得 1 分。可由表 5 數據計算求出，亦可由最佳配適直線斜率決定 (fB = 25.0 V·s/m)。",
        "2. 將所求出的 fB 代入 FB = fB · I 得 1 分 (FB = 25.0 × 0.040 = 1.0 N)。",
        "3. 寫出 FB = M · g 重力平衡關係得 1 分。",
        "4. 計算求出正確答案 M ≈ 0.1 kg 得 1 分（未寫步驟僅寫答案不給分）。"
      ]
    },
    inquiryFocus: {
      acquisition: "利用高精度位置感測器動態記錄線圈微幅振動，藉由示波器/數據擷取器記錄瞬間電動勢。",
      recording: "留意速度與電壓的正負方向性（正負號代表運動方向與感應電動勢極性），記錄有效位數與公制單位前綴 (milli-)。",
      processing: "作圖決定最佳配適直線斜率 fB，再代入靜態平衡方程式求解未知的宏觀物理量（質量 M）。"
    }
  },

  ceec111_coastal_uplift: {
    id: "ceec111_coastal",
    title: "111 年學測第 43~45 題：海岸海階累積高程與碳-14定年（平均抬升速率計算）",
    subject: "地球科學 / 探究實作",
    type: "step",
    bestPlotMethod: "step_and_regression",
    bestPlotMethodLabel: "階梯式抬升折線 (地震特徵) ＋ 平均趨勢直線",
    defaultMode: "line",
    allowedModes: [
      { mode: "line", label: "階梯式抬升折線 (真實大地震跳升機制)" },
      { mode: "bestfit", label: "平均抬升趨勢直線 (計算長期平均速率)" },
      { mode: "scatter", label: "純散布點 (Scatter)" }
    ],
    regressionApplicable: true,
    regressionWarning: "【注意作圖情境區分】若題意要求呈現「偶發大地震引起的快速抬升」，大考中心評分標準要求必須畫出「階梯狀跳升」；全域線性直線僅能用於宏觀計算「平均抬升速率（7.5 mm/年）」。",
    graphingRationale: "題幹明確強調『此海階形成主要由偶發大地震引起，兩次地震間無明顯抬升』。大考中心第 45 題評分標準明訂：在答題卷坐標紙上，地震時為急遽垂直跳升，平時為水平橫線段（階梯狀）得 2 分滿分；若僅畫單一直線則僅給 1 分。而長期平均抬升速率則由首尾連線斜率計算 (18m / 2400yr = 7.5 mm/yr)。",
    csvFileName: "111學測_海岸海階累積高程與碳14定年.csv",
    summary: "分析海岸 0T 到 3T 四個海階的碳-14定年年代與累積高程，在答題坐標紙描點作圖呈現偶發大地震快速抬升之時空特徵，並列式計算平均抬升速率。",
    xLabel: "定年時間 t",
    xUnit: "年 (yr)",
    yLabel: "累積高程 h",
    yUnit: "公尺 (m)",
    data: [
      { x: 0,    y: 0,  label: "0T (現今海面基準 0m)", isRequiredPoint: true },
      { x: 800,  y: 6,  label: "1T (800年前抬升至 6m)", isRequiredPoint: true },
      { x: 1600, y: 10, label: "2T (1600年前抬升至 10m)", isRequiredPoint: true },
      { x: 2400, y: 18, label: "3T (2400年前抬升至 18m)", isRequiredPoint: true }
    ],
    theoryFormula: "平均抬升速率 v = Δh / Δt = (18 - 0) m / (2400 - 0) 年 = 7.5 mm/年",
    fullExamText: {
      intro: "【111 年學測自然考科 第 43~45 題 題組完整題幹】\n某海岸有不同高程的海階，如圖 18 的 0T 至 3T 所示。海階常有海蝕凹壁。小莉推論海蝕凹壁為當地堅硬的火成岩壁受潮水長期侵蝕而成。海蝕凹壁上常有大量的穿孔貝附著在凹壁上。穿孔貝僅在潮起潮落之間的高度存活，無法長期離開水面。因此，小莉推論此海階上的海蝕凹壁主要由大地震所造成的垂直抬升而成。小莉詳細丈量每個海階和海蝕凹壁的高程，並利用凹壁上穿孔貝的碳進行碳-14 定年分析。所得的結果如表 3 所示。",
      question: "【第 45 題（4 分非選擇題）原始試題】\n若此海岸海階的形成主要由偶發大地震事件所引起，假設在兩次大地震之間無明顯抬升與海水面高度變化，請依下列坐標軸與表 3 的數據，畫出此海岸 0T 到 3T 期間，最符合上述地體抬升情形之累積高程（縱軸）隨時間（橫軸）的變化圖（2 分）。注意：由大地震引起的快速抬升，和緩慢抬升是有所不同的。並列式計算此海岸 0T 到 3T 期間的平均抬升速率（單位為 mm/年，計算至小數點第一位）（2 分）。"
    },
    analysis: {
      slope: 0.0075,
      slopeUnit: "m/年 (即 7.5 mm/年)",
      rSquared: 0.9846,
      stats: [
        { label: "平均抬升速率", value: "7.5 mm/年 (0.0075 m/年)", highlight: true },
        { label: "總定年跨度", value: "2400 年 (0T ~ 3T)" },
        { label: "累積抬升總高程", value: "18 公尺" },
        { label: "作圖評分關鍵", value: "階梯狀跳升得滿分 (大地震特性)", highlight: true }
      ],
      scoringKey: [
        "大考中心評分原則（滿分 4 分）：",
        "（1）作圖題（2分）：在坐標紙上繪出階梯狀（地震突發快速抬升，其餘時間無抬升呈水平線段）之階梯折線圖得 2 分；若僅以直線連接各點則給 1 分。",
        "（2）計算題（2分）：列式 (18 - 0) m / (2400 - 0) yr = 0.0075 m/yr = 7.5 mm/yr（列式 1 分，答案計算至小數點第一位 7.5 mm/年 得 1 分）。"
      ]
    },
    inquiryFocus: {
      acquisition: "野外地質調查採集海蝕凹壁穿孔貝，利用碳-14放射性同位素定年。",
      recording: "整理海階年代（橫軸）與累積高程（縱軸）數值表。",
      processing: "區分『偶發大地震快速階梯抬升』與『長期平均線性抬升速率』在作圖與物理意義上的本質差異。"
    }
  },

  // ==========================================
  // 112 年學測
  // ==========================================
  ceec112_solubility_curves: {
    id: "ceec112_solubility",
    title: "112 年學測第 20 題：KNO3 與 KCl 溶解度曲線 (交點判讀與再結晶分離)",
    subject: "化學 / 探究實作",
    type: "multi_curve",
    bestPlotMethod: "smooth_curve",
    bestPlotMethodLabel: "雙系列平滑熱力學曲線 (交點判讀與再結晶)",
    defaultMode: "line",
    allowedModes: [
      { mode: "line", label: "雙系列平滑熱力學曲線 (標準呈現)" },
      { mode: "scatter", label: "純散布點 (Scatter)" }
    ],
    regressionApplicable: false,
    regressionWarning: "【嚴禁線性回歸】固體對水之溶解平衡隨溫度呈熱力學非線性變化（KNO3 溶解度隨溫度指數型暴增，KCl 平緩微升），絕不可用全域線性回歸直線，否則將完全抹殺曲線交點與結晶析出規律！",
    graphingRationale: "自變數溫度是連續物理量，不同溶質有各自的溶解熱（ΔH）。KNO3 溶解熱大，隨溫度急遽攀升；KCl 則平緩微升。使用雙系列平滑趨勢曲線能清晰判讀 24.5°C 處的等溶解度交點 (~36.2 g/100g 水)，並提供高溫飽和液降溫結晶純化 KNO3 的理論依據。",
    csvFileName: "112學測_硝酸鉀與氯化鉀溶解度.csv",
    summary: "比較 KNO3 與 KCl 在 0~70℃ 的溶解度變化曲線，藉由交點 (約 24.5℃, 36.2g) 與曲線斜率陡峭程度，設計降溫再結晶分離固體混合物之策略。",
    xLabel: "溫度 T",
    xUnit: "℃",
    yLabel: "溶解度 S",
    yUnit: "g/100g水",
    series: [
      {
        name: "KNO3 (硝酸鉀，斜率陡峭)",
        color: "#f43f5e",
        data: [
          { x: 0,  y: 13.3 },
          { x: 10, y: 20.9 },
          { x: 20, y: 31.6 },
          { x: 30, y: 45.8 },
          { x: 40, y: 63.9 },
          { x: 50, y: 85.5 },
          { x: 60, y: 110.0 },
          { x: 70, y: 138.0 }
        ]
      },
      {
        name: "KCl (氯化鉀，斜率平緩)",
        color: "#06b6d4",
        data: [
          { x: 0,  y: 27.6 },
          { x: 10, y: 31.0 },
          { x: 20, y: 34.0 },
          { x: 30, y: 37.0 },
          { x: 40, y: 40.0 },
          { x: 50, y: 42.6 },
          { x: 60, y: 45.5 },
          { x: 70, y: 48.3 }
        ]
      }
    ],
    theoryFormula: "ln S = -ΔH_sol / (R·T) + C（熱力學凡特何夫非線性關係）",
    fullExamText: {
      intro: "【112 年學測自然考科 第 20 題 完整題幹】\n圖 4 為 KNO3 和 KCl 對水的溶解度（克/100克水）與溫度的關係圖。表 3 為不同溫度下，KNO3 和 KCl 對水的溶解度數據。\n溫度 0℃：KNO3 13.3，KCl 27.6\n溫度 10℃：KNO3 20.9，KCl 31.0\n溫度 20℃：KNO3 31.6，KCl 34.0\n溫度 30℃：KNO3 45.8，KCl 37.0\n溫度 40℃：KNO3 63.9，KCl 40.0\n溫度 50℃：KNO3 85.5，KCl 42.6\n溫度 60℃：KNO3 110，KCl 45.5\n溫度 70℃：KNO3 138，KCl 48.3（單位為克/100克水）",
      question: "【第 20 題】某生根據圖 4 和表 3 的資料，提出下列幾項推論：\n(甲) 在 20℃ 到 30℃ 之間，有一特定溫度，此時兩化合物對水的溶解度相同\n(乙) 在 70℃ 時，將等質量的 KNO3 和 KCl 溶於等質量的水中，配成未飽和溶液，降溫至 10℃ 時，KNO3 會先結晶析出\n(丙) 在 70℃ 時，100 克水最多可溶解 KNO3 和 KCl 的總質量為 186.3 克\n下列何者正確？ (A) 僅有甲 (B) 甲和乙 (C) 甲和丙 (D) 乙和丙 (E) 甲、乙和丙"
    },
    analysis: {
      stats: [
        { label: "等溶解度交點溫度", value: "約 24.5 ℃", highlight: true },
        { label: "交點處等溶解度值", value: "約 36.2 g/100g水" },
        { label: "KNO3 70℃->10℃析出量", value: "117.1 克 (138 - 20.9)", highlight: true },
        { label: "KCl 70℃->10℃析出量", value: "17.3 克 (48.3 - 31.0)" }
      ],
      scoringKey: [
        "考點解析（答案選 B：甲和乙）：",
        "1. 甲推論正確：20℃時 KNO3(31.6) < KCl(34.0)，30℃時 KNO3(45.8) > KCl(37.0)，兩曲線在 24~25℃ 間必然相交，交點溶解度約 36.2 g/100g 水。",
        "2. 乙推論正確：KNO3 溶解度隨溫度劇增（斜率極陡），高溫飽和液降溫至 10℃ 時溶解度驟降至 20.9g，會比 KCl (31.0g) 率先達到飽和並大量結晶析出。",
        "3. 丙推論錯誤：兩種不同溶質同時溶於同一份水時，因同離子效應或彼此相互作用，不可將各自的單獨溶解度直接線性相加。"
      ]
    },
    inquiryFocus: {
      acquisition: "精密恆溫水浴槽與高精度天平，測定不同溫度下的飽和溶液溶質質量。",
      recording: "基準化記錄：固定 100g 水為溶劑基準，記錄各溫階溶質溶解克數。",
      processing: "繪製雙系列非線性平滑曲線，藉由交點內插與斜率差異制定混合物結晶分離純化策略。"
    }
  },

  ceec112_metal_oxide_stoichiometry: {
    id: "ceec112_metal_oxide",
    title: "112 年學測第 25~26 題：金屬 M 與氧氣化合反應量與限量試劑轉折",
    subject: "化學 / 探究實作",
    type: "turning_point",
    bestPlotMethod: "piecewise_linear",
    bestPlotMethodLabel: "限量試劑分段折線 (化學計量轉折點)",
    defaultMode: "line",
    allowedModes: [
      { mode: "line", label: "限量試劑分段折線 (上升段 ＋ 水平飽和段)" },
      { mode: "scatter", label: "純散布點 (Scatter)" }
    ],
    regressionApplicable: false,
    regressionWarning: "【嚴禁全域線性回歸】本題為化學計量限量試劑經典題。轉折點前氧氣不足（正斜率上升段），轉折點後金屬 M 耗盡（斜率為 0 的水平飽和段）。若硬做全域單一直線回歸，會破壞限量試劑與定比定律的核心化學意義！",
    graphingRationale: "化學反應受限量試劑控制。固定金屬 M 為 5.4g，通入氧氣在 4.8g 之前為正比上升（限量為氧氣）；通入 4.8g 處恰好完全反應生成 10.2g M2Ox；超過 4.8g 後產物恆為 10.2g。作圖必須使用兩段折線（正斜率直線與水平線）交會於轉折點 (4.8, 10.2)，藉此推導化學式 Al2O3 與原子量 M = 27。",
    csvFileName: "112學測_金屬M與氧氣化合質量關係.csv",
    summary: "在固定 5.4 g 金屬 M 容器中通入不同質量氧氣，探討生成物 M2Ox 質量變化，藉由化學計量轉折點判斷限量試劑並推導金屬 M 原子量。",
    xLabel: "通入氧氣質量",
    xUnit: "克 (g)",
    yLabel: "生成 M2Ox 質量",
    yUnit: "克 (g)",
    data: [
      { x: 1.6, y: 3.4, note: "甲容器：氧氣不足 (限量試劑)，M未反應完", phase: "limiting" },
      { x: 3.2, y: 6.8, note: "乙容器：氧氣不足 (限量試劑)，M未反應完", phase: "limiting" },
      { x: 4.8, y: 10.2, note: "丙容器：恰好完全反應 (化學計量轉折點)", phase: "stoichiometric", isRequiredPoint: true },
      { x: 6.4, y: 10.2, note: "丁容器：金屬M耗盡，氧氣過量殘留", phase: "excess", isRequiredPoint: true }
    ],
    theoryFormula: "4 M + x O2 -> 2 M2Ox (轉折點：5.4g M + 4.8g O2 -> 10.2g M2Ox)",
    fullExamText: {
      intro: "【112 年學測自然考科 第 25~26 題 題組完整題幹】\n貼有甲、乙、丙、丁標籤的四個相同真空密閉容器，其中，甲、丁之間有一個關閉的氣閥相連，並分別於四個容器內置入 5.4 克 M 金屬粉末。接著，曉諭將不同質量的氧氣分別通入上述四個容器內，在適當的條件下與 M 反應，產生相同的氧化物 M₂Oₓ。待反應完全後，分別測量每個容器內所生成 M₂Oₓ 的質量，結果如表 4：\n容器甲：通入氧氣 1.6 克，生成 3.4 克 M₂Oₓ\n容器乙：通入氧氣 3.2 克，生成 6.8 克 M₂Oₓ\n容器丙：通入氧氣 4.8 克，生成 10.2 克 M₂Oₓ\n容器丁：通入氧氣 6.4 克，生成 10.2 克 M₂Oₓ",
      question: "【第 25 題】已知 M 的原子量介於 20 與 30 amu 之間，且 x 為整數，則下列敘述哪些正確？（應選 2 項）\n(A) x＝1  (B) M 的原子量為 24 amu  (C) M₂Oₓ 的莫耳質量為 102 克/莫耳  (D) 反應完全後，丙容器內有殘餘未反應的金屬 M  (E) 反應完全後，丁容器內有殘餘未反應的氧氣\n【第 26 題】待以上四個容器反應完成後，曉諭打開連接甲、丁二容器的氣閥，使氣體可以自由流動進行第二次反應，則二次反應完成後容器的敘述何者正確？"
    },
    analysis: {
      stoichiometricOxygen_g: 4.8,
      maxProduct_g: 10.2,
      metalMass_g: 5.4,
      metalAtomicMass: 27,
      formula: "Al2O3 (氧化鋁)",
      stats: [
        { label: "化學計量轉折點", value: "通入 4.8 g 氧氣", highlight: true },
        { label: "生成物最大質量", value: "10.2 克 (水平平台線)" },
        { label: "金屬 M 推算原子量", value: "27 amu (鋁 Al)", highlight: true },
        { label: "氧化物化學式與式量", value: "Al2O3，莫耳質量 102 g/mol" }
      ],
      scoringKey: [
        "考點解析（第 25 題選 C、E；第 26 題選 B）：",
        "1. 轉折點分析：通入氧氣 1.6g->3.4g，3.2g->6.8g，4.8g->10.2g，斜率為 10.2/4.8 = 2.125；當氧氣增至 6.4g 時產物仍為 10.2g，顯示在 4.8g 處出現平折轉折點！",
        "2. 化學式推導：5.4g 金屬 M 恰與 4.8g 氧完全反應生成 10.2g 氧化物。(5.4/M) : (4.8/16) = 2 : x => M = 18x。因為 20 < M < 30 且 x 為整數，故 x = 3，M = 27 (鋁 Al)，化合物為 Al2O3（式量 102 g/mol）。",
        "3. 限量試劑二次反應：丁容器過量氧氣 1.6g 流入甲容器，與甲未反應的 3.6g M 反應，剛好再生成 3.4g 氧化物，使固體質量增加 1.6g。"
      ]
    },
    inquiryFocus: {
      acquisition: "在密閉真空間隔中定量注入氣體反應物，高精度電子天平秤量化合產物質量。",
      recording: "記錄反應物質量與生成物質量，繪製折線圖觀察質量守恆與反應極限。",
      processing: "作圖找出由「限量試劑上升段」至「過量試劑水平段」之交界轉折點，定量推算莫耳比與未知元素原子量。"
    }
  },

  // ==========================================
  // 114 年學測
  // ==========================================
  ceec114_milkfish_rgn_mrna: {
    id: "ceec114_milkfish",
    title: "114 年學測第 38 題：虱目魚耐寒抗低溫調適之 RGN mRNA 逐時生成量",
    subject: "生物 / 探究實作",
    type: "multi_curve",
    bestPlotMethod: "dynamic_curve",
    bestPlotMethodLabel: "雙池生理時序動態曲線 (大考答題卷作圖題)",
    defaultMode: "line",
    allowedModes: [
      { mode: "line", label: "生理時序平滑曲線 (雙池比較)" },
      { mode: "scatter", label: "純散布點 (Scatter)" }
    ],
    regressionApplicable: false,
    regressionWarning: "【嚴禁線性回歸】生物基因表現隨暴露時間呈現非線性應激反饋（鹹水池在 12 小時出現尖銳波峰後下降，淡水池緩慢上升至 168 小時維持高水平），絕非直線，不可進行線性回歸！",
    graphingRationale: "這是大考中心真實的非選擇『手繪作圖題』！考生必須依據題目所給 12 小時與 168 小時數據，於答題紙上精準描點並連接成平滑動態曲線，直觀比較兩池虱目魚在低溫應激期（鹹水池急性爆發）與適應期（淡水池慢性維持）的生理調適策略。",
    csvFileName: "114學測_虱目魚低溫調適mRNA生成量.csv",
    summary: "將畜養於淡水池與鹹水池之虱目魚移至 18℃ 低溫，逐時追蹤 RGN mRNA 生成量變化，於圖中描點繪圖補足曲線趨勢並比較抗寒機制。",
    xLabel: "低溫暴露時間 t",
    xUnit: "小時 (hr)",
    yLabel: "RGN mRNA 相對量",
    yUnit: "倍數 (fold)",
    series: [
      {
        name: "鹹水池 (急性應激反應，12h尖峰)",
        color: "#f59e0b",
        data: [
          { x: 0,   y: 1.0 },
          { x: 12,  y: 3.5, isTargetDraw: true, label: "★ 12h 鹹水尖峰 (3.5倍)" },
          { x: 48,  y: 2.1 },
          { x: 168, y: 1.2 }
        ]
      },
      {
        name: "淡水池 (慢性長期抗寒維持)",
        color: "#38bdf8",
        data: [
          { x: 0,   y: 1.0 },
          { x: 12,  y: 1.8 },
          { x: 48,  y: 2.6 },
          { x: 168, y: 3.3, isTargetDraw: true, label: "★ 168h 淡水維持 (3.3倍)" }
        ]
      }
    ],
    theoryFormula: "基因轉錄量 = f(暴露時間, 滲透壓環境)（非線性生物回饋）",
    fullExamText: {
      intro: "【114 年學測自然考科 第 36~38 題 題組完整題幹】\n台灣冬天的寒流常造成沿海養殖的虱目魚大量凍死。科學家研究發現虱目魚細胞中的回歸蛋白（regucalcin, RGN）在低溫耐受性扮演關鍵角色。研究人員將分別蓄養於淡水池與鹹水池的虱目魚，由 28℃ 移至 18℃ 的低溫環境中，並在低溫暴露 0、12、48 及 168 小時後，分別測定兩組魚鰓組織中 RGN mRNA 的相對量，結果如表 1：\n暴露時間 0h：淡水池 1.0，鹹水池 1.0\n暴露時間 12h：淡水池 1.8，鹹水池 3.5\n暴露時間 48h：淡水池 2.6，鹹水池 2.1\n暴露時間 168h：淡水池 3.3，鹹水池 1.2",
      question: "【第 38 題（4 分非選擇題）原始試題】\n圖 11 的坐標圖中，已繪出低溫暴露下，部分時間點兩組魚鰓中 RGN mRNA 相對量的變化。請參考表 1 的數據，在答題卷對應的圖中：\n（a）以『●』描出鹹水池組在 12 小時的數據點，並以實線補全該組的折線圖。（2 分）\n（b）以『▲』描出淡水池組在 168 小時的數據點，並以虛線補全該組的折線圖。（2 分）"
    },
    analysis: {
      stats: [
        { label: "鹹水池應激峰值", value: "12 小時達 3.5 倍", highlight: true },
        { label: "淡水池最高累積", value: "168 小時達 3.3 倍", highlight: true },
        { label: "答題卷作圖標的點", value: "12h(鹹水) 與 168h(淡水)" },
        { label: "調適機制結論", value: "鹹水急性爆發 / 淡水慢性適應" }
      ],
      scoringKey: [
        "大考中心評分原則（滿分 4 分）：",
        "（a）小題（2分）：在橫軸 12、縱軸 3.5 處正確以『●』描點得 1 分；以實線正確連接 (0,1.0) -> (12,3.5) -> (48,2.1) 得 1 分。",
        "（b）小題（2分）：在橫軸 168、縱軸 3.3 處正確以『▲』描點得 1 分；以虛線由 (48,2.6) 連接至 (168,3.3) 得 1 分。"
      ]
    },
    inquiryFocus: {
      acquisition: "定量即時聚合酶連鎖反應 (RT-qPCR) 測量極微量 mRNA 轉錄表現倍數。",
      recording: "時間序列基準化（對照組 0 小時設定為 1.0），圖例實線/虛線與不同形狀標記（圓點/三角形）之標準規範。",
      processing: "多系列生理曲線作圖，藉由波峰出現時機與衰減趨勢，分析不同滲透壓預調節對抗寒能力的深層影響。"
    }
  },

  ceec114_neuron_na_channel: {
    id: "ceec114_neuron",
    title: "114 年學測第 48~49 題：神經細胞膜鈉離子通道 I-V 特性與膜電阻測量",
    subject: "生物物理 / 探究實作",
    type: "linear",
    bestPlotMethod: "linear_regression",
    bestPlotMethodLabel: "最佳配適直線 (歐姆定律線性回歸求截距與斜率)",
    defaultMode: "bestfit",
    allowedModes: [
      { mode: "bestfit", label: "最佳配適直線 (求截距 ENa 與斜率 1/RNa)" },
      { mode: "scatter", label: "純散布點 (Scatter)" }
    ],
    regressionApplicable: true,
    regressionWarning: "【適用線性回歸】依據細胞膜通道歐姆定律 V = ENa + INa · RNa，電壓與電流呈高度線性關係，必須由趨勢線求橫軸截距 ENa 與斜率倒數 RNa。",
    graphingRationale: "題幹明確假設『Na⁺ 通道的 I-V 特性為線性，且平衡電位 ENa 為定值』。大考中心評分指引中，解法一即為標準的『趨勢線截距法』：當 INa = 0 時求出橫軸截距 ENa ≈ 46~50 mV，再由趨勢線斜率倒數求出膜電阻 RNa ≈ 140 Ω。此題具備高度物理線性關聯（R²=0.9985），完全適合且必須使用最佳配適直線！",
    csvFileName: "114學測_神經細胞膜鈉通道電壓與電流.csv",
    summary: "透過膜電位箝定技術測量神經細胞膜鈉通道在不同電位差 V 下的離子電流 INa，利用趨勢線求出平衡電壓 ENa 與膜電阻 RNa。",
    xLabel: "跨膜電位差 V",
    xUnit: "mV",
    yLabel: "鈉離子電流 INa",
    yUnit: "mA",
    data: [
      { x: -60, y: -0.75, label: "內向電流 (-60, -0.75)" },
      { x: -40, y: -0.60, label: "內向電流 (-40, -0.60)" },
      { x: -20, y: -0.46, label: "內向電流 (-20, -0.46)" },
      { x: 0,   y: -0.33, label: "零電位差 (0, -0.33)" },
      { x: 20,  y: -0.19, label: "內向電流 (20, -0.19)" },
      { x: 40,  y: -0.05, label: "趨近平衡 (40, -0.05)" },
      { x: 60,  y: 0.10,  label: "外向電流 (60, 0.10)" }
    ],
    theoryFormula: "V = ENa + INa · RNa => INa = (1 / RNa) · V - (ENa / RNa)",
    fullExamText: {
      intro: "【114 年學測自然考科 第 47~49 題 題組完整題幹】\n神經細胞受刺激時，細胞膜上的電位敏感型離子通道會開啟，使離子快速跨膜流動產生神經衝動。神經生理學家利用膜電位箝定技術探究細胞膜離子通道的特性。細胞膜內外的離子濃度不同，在平衡時會建立特定的電位差，例如鈉離子與鉀離子分別為平衡電壓 ENa 與 EK。圖 15 為 Na⁺ 通道在導通狀況下的等效直流電路，V 為細胞內外的電位差，INa 為 Na⁺ 電流。假設 Na⁺ 通道的 I-V 特性為線性，且 ENa 為定值。圖 16 為實驗測量數據與趨勢線。",
      question: "【第 49 題（4 分非選擇題）原始試題】\n若已知 V = ENa + INa · RNa，試根據圖 16 中的趨勢線，分析並計算鈉離子通道的（a）平衡電壓 ENa，（b）電阻值 RNa。（4 分）"
    },
    analysis: {
      slope: 0.00708,
      slopeUnit: "mA/mV (即 1/RNa = 1/140 Ω)",
      rSquared: 0.9985,
      eNa_val: "約 46 ~ 50 mV",
      rNa_val: "約 140 Ω (給分標準 125 ~ 175 Ω)",
      stats: [
        { label: "鈉通道平衡電位 ENa", value: "約 46 ~ 50 mV", highlight: true },
        { label: "鈉通道膜電阻 RNa", value: "約 140 Ω (給分區間 125~175Ω)", highlight: true },
        { label: "趨勢線斜率 1/RNa", value: "0.0071 mA/mV" },
        { label: "線性判定係數 R²", value: "0.9985" }
      ],
      scoringKey: [
        "大考中心評分原則（滿分 4 分）：",
        "解法一（截距法）：由 V = ENa + INa · RNa 可知，當 INa = 0 mA 時，V = ENa。由趨勢線上 INa = 0 時的 V 值約為 50 mV，即 ENa ≈ 50 mV。再代入數據點 (-40, -0.6) 得 RNa ≈ 150 Ω。",
        "解法二（聯立方程法）：取數據點 (-60, -0.75) 與 (60, 0.10) 列聯立式，解得 ENa ≈ 46 mV，RNa ≈ 140 Ω。",
        "大考中心評分寬容區間：ENa 於 45 mV ~ 55 mV 皆給分；RNa 於 125 Ω ~ 175 Ω 皆給分（單位亦必須正確寫出）。"
      ]
    },
    inquiryFocus: {
      acquisition: "膜電位箝定技術 (Patch-clamp) 記錄單一微米離子通道在不同階梯電壓下的皮安培級電流。",
      recording: "注意跨膜電位 (mV) 與離子內流外流方向（內向電流定義為負值，外向電流為正值）。",
      processing: "作圖決定趨勢線斜率與電壓截距，從純電學測量中分離出化學濃度差驅動力 (ENa) 與物理歐姆阻抗 (RNa)。"
    }
  },

  ceec114_alkane_combustion_heat: {
    id: "ceec114_alkane",
    title: "114 年學測第 55~56 題：烷類碳數與莫耳燃燒熱線性關係推算",
    subject: "化學 / 探究實作",
    type: "linear",
    bestPlotMethod: "linear_regression",
    bestPlotMethodLabel: "最佳配適直線 (同系物線性回歸與內插推算)",
    defaultMode: "bestfit",
    allowedModes: [
      { mode: "bestfit", label: "最佳配適直線 (線性回歸內插丙烷)" },
      { mode: "scatter", label: "純散布點 (Scatter)" }
    ],
    regressionApplicable: true,
    regressionWarning: "【適用線性回歸】有機同系物每增一個 -CH2- 鍵能變化大致恆定，題目亦明確要求『假設莫耳燃燒熱與烷類碳數大致呈線性關係』，適合建立線性模型推算丙烷燃燒熱。",
    graphingRationale: "題目第 56(b) 題題幹直接寫明：『假設莫耳燃燒熱與烷類碳數大致呈線性關係，試列式推算丙烷的莫耳燃燒熱』。烷類同系物每多一個 -CH2-，完全燃燒釋放的化學鍵能呈等差線性遞增（R²=0.9999），透過線性回歸直線內插 x=3，即可推算丙烷的莫耳燃燒熱約為 2200~2230 kJ/mol。",
    csvFileName: "114學測_烷類碳數與莫耳燃燒熱.csv",
    summary: "利用甲烷、乙烷、丁烷、戊烷與辛烷的莫耳燃燒熱數據，建立燃燒熱對碳數的線性回歸模型，推算丙烷的分子式、分子量與莫耳燃燒熱。",
    xLabel: "烷類碳數 n",
    xUnit: "個碳",
    yLabel: "莫耳燃燒熱 ΔH",
    yUnit: "kJ/mol",
    data: [
      { x: 1, y: 890,  label: "甲烷 (CH4, M=16)" },
      { x: 2, y: 1560, label: "乙烷 (C2H6, M=30)" },
      { x: 4, y: 2874, label: "丁烷 (C4H10, M=58)" },
      { x: 5, y: 3509, label: "戊烷 (C5H12, M=72)" },
      { x: 8, y: 5460, label: "辛烷 (C8H18, M=114)" }
    ],
    theoryFormula: "ΔH ≈ 653 · n + 245 kJ/mol (每增一 -CH2- 增加約 650~670 kJ/mol)",
    fullExamText: {
      intro: "【114 年學測自然考科 第 55~57 題 題組完整題幹】\n烷類在充足的氧氣下，可進行燃燒反應產生二氧化碳並釋出熱量。市售液化天然氣是以甲烷為成分，液化石油氣則是丙烷與丁烷的混合物。表 3 為幾種烷類的分子式、分子量及莫耳燃燒熱：\n甲烷 CH₄，分子量 16，莫耳燃燒熱 890 kJ/mol\n乙烷 C₂H₆，分子量 30，莫耳燃燒熱 1560 kJ/mol\n丁烷 C₄H₁₀，分子量 58，莫耳燃燒熱 2874 kJ/mol\n戊烷 C₅H₁₂，分子量 72，莫耳燃燒熱 3509 kJ/mol\n辛烷 C₈H₁₈，分子量 114，莫耳燃燒熱 5460 kJ/mol",
      question: "【第 56 題（4 分非選擇題）原始試題】\n（a）根據表 3，試推測丙烷的分子式為何？並計算其分子量為何？（2 分）\n（b）假設莫耳燃燒熱與烷類碳數大致呈線性關係，試列式推算丙烷的莫耳燃燒熱的數值為何？（單位：千焦耳/莫耳）（2 分）"
    },
    analysis: {
      slope: 653.2,
      slopeUnit: "kJ/(mol·碳數)",
      rSquared: 0.9999,
      propanePredicted_kJ: "2196 ~ 2230 kJ/mol",
      stats: [
        { label: "線性回歸斜率", value: "653.2 kJ/(mol·碳)", highlight: true },
        { label: "判定係數 R²", value: "0.9999 (極高線性相關)" },
        { label: "丙烷推算燃燒熱", value: "約 2217 ~ 2230 kJ/mol", highlight: true },
        { label: "丙烷分子式與分子量", value: "C3H8，分子量 44" }
      ],
      scoringKey: [
        "大考中心評分原則（滿分 4 分）：",
        "（a）小題（2分）：寫出丙烷分子式 C3H8 得 1 分；分子量 12×3 + 8 = 44 得 1 分。",
        "（b）小題（2分）：列式正確得 1 分，推算數值正確再得 1 分。",
        "  • 解法一（等差法）：(1560 + 2874) / 2 = 2217 kJ/mol。",
        "  • 解法二（差值遞加法）：1560 - 890 = 670，推算丙烷為 1560 + 670 = 2230 kJ/mol。",
        "  • 解法三（線性函數/回歸法）：y = 653x + 245，代入 x=3 得約 2200 kJ/mol（2196~2230 皆可獲滿分）。"
      ]
    },
    inquiryFocus: {
      acquisition: "彈卡計 (Bomb calorimeter) 測量標準莫耳燃燒熱，水當量校正與溫升記錄。",
      recording: "同系物化學結構遞增規則（-CH2- 亞甲基鏈段），整理分子量與焓變數值矩陣。",
      processing: "線性回歸模型建構、內插未知同系物燃燒熱、評估模型預測力與決定係數 R²。"
    }
  },

  // ==========================================
  // 115 年學測 (參考試卷 / 研究試卷)
  // ==========================================
  ceec115_zns_quantum_dots: {
    id: "ceec115_zns_qd",
    title: "115 年學測第 44~46 題：硫化鋅奈米量子點合成產率與反應物莫耳比",
    subject: "化學 / 探究實作",
    type: "curve",
    bestPlotMethod: "plateau_threshold_curve",
    bestPlotMethodLabel: "反應產率階躍與飽和平台折線 / 散布圖",
    defaultMode: "line",
    allowedModes: [
      { mode: "line", label: "反應產率階躍與飽和平台折線 (非線性規律)" },
      { mode: "scatter", label: "純散布點 (Scatter)" }
    ],
    regressionApplicable: false,
    regressionWarning: "【嚴禁線性回歸】本實驗之硫化鋅量子點產率在 Na2S 達 100 莫耳後即進入約 44%~50% 的飽和平台區間，屬於限制試劑閾值跳躍與表面包覆飽和現象。若硬作全域線性回歸，會產生一條貫穿飽和平台的假線性直線，徹底扭曲化學反應機理！",
    graphingRationale: "依據化學計量與膠體化學，當硫源 Na2S 由 50 增至 100 時產率由 18.1% 急遽跳躍至 44.7%，隨後在 100~400 範圍內產率穩定維持在 44%~50% 的飽和平台。最適作圖為『分段折線/平台曲線』或『純散布點』，以真實反映限制試劑耗盡後產率不再大幅增長的化學本質，嚴禁做全域線性回歸！",
    csvFileName: "115學測_硫化鋅量子點產率與反應物量.csv",
    summary: "在固定 ZnSO4 與半胱胺酸條件下，改變反應物 Na2S 莫耳數，測定硫化鋅量子點產率與殘留離子量，分析奈米粒子合成之化學計量與顆粒數。",
    xLabel: "反應物 Na2S 莫耳數",
    xUnit: "×10⁻⁶ mol",
    yLabel: "量子點產率",
    yUnit: "%",
    data: [
      { x: 50,  y: 18.1, label: "樣品 1 (Na2S 極不足，限制試劑)", note: "硫源不足 (18.1%)" },
      { x: 100, y: 44.7, label: "樣品 2 (產率躍升跳階)", note: "躍升跳階點 (44.7%)" },
      { x: 150, y: 44.4, label: "樣品 3 (產率進入平台)", note: "飽和平台 (44.4%)" },
      { x: 200, y: 44.0, label: "樣品 4 (等莫耳比 Zn:S=1:1，第46題標的)", isRequiredPoint: true, note: "★第46題考查標的 (44.0%)" },
      { x: 300, y: 45.5, label: "樣品 5 (Na2S 過量)", note: "過量微升 (45.5%)" },
      { x: 400, y: 50.2, label: "樣品 6 (Na2S 2倍過量)", note: "2倍過量 (50.2%)" }
    ],
    theoryFormula: "Zn²⁺ + S²⁻ -> ZnS (界面活性劑包裹抑制聚集沉澱，非線性產率)",
    fullExamText: {
      intro: "【115 年學測自然考科 第 44~46 題 題組完整題幹】\n在 2023 年，諾貝爾化學獎頒給從事奈米級量子點研究的三位學者。量子點是直徑介於 1 至 10 奈米的奈米粒子，可表現出獨特的光電性質。硫化鋅量子點合成實驗中，配製甲溶液（半胱胺酸 + ZnSO4）與乙溶液（Na2S）混合反應，以冰冷乙醇沉澱析出。表 8 顯示不同比例反應物所得產物的鋅離子、硫離子含量及量子點產率：\n樣品 1：ZnSO4 200，Na2S 50，產率 18.1%\n樣品 2：ZnSO4 200，Na2S 100，產率 44.7%\n樣品 3：ZnSO4 200，Na2S 150，產率 44.4%\n樣品 4：ZnSO4 200，Na2S 200，產率 44.0%\n樣品 5：ZnSO4 200，Na2S 300，產率 45.5%\n樣品 6：ZnSO4 200，Na2S 400，產率 50.2%（莫耳數單位為 10⁻⁶ mol）",
      question: "【第 46 題（4 分非選擇題）原始試題】\n若已知樣品 4 中，每顆硫化鋅量子點約含有 1×10⁴ 個硫化鋅（原子量：Zn=65.4, S=32.0）。\n（a）生成硫化鋅量子點的莫耳數為多少？（2 分）\n（b）每顆量子點含有多少克硫化鋅？（2 分）"
    },
    analysis: {
      stats: [
        { label: "產率陡增轉折點", value: "Na2S 達 100×10⁻⁶ mol", highlight: true },
        { label: "飽和平台產率區間", value: "約 44.0% ~ 50.2%" },
        { label: "樣品4量子點生成莫耳數", value: "8.8×10⁻¹⁰ mol (88×10⁻⁶/10⁴)", highlight: true },
        { label: "單顆量子點質量", value: "1.62×10⁻¹⁸ g", highlight: true },
        { label: "作圖模式警示", value: "非線性飽和曲線 · 嚴禁回歸直線", highlight: true }
      ],
      scoringKey: [
        "大考中心評分原則（滿分 4 分）：",
        "（a）小題（2分）：由表 8 樣品 4 可知硫化鋅 ZnS 生成量為 88.0×10⁻⁶ 莫耳。每顆量子點含 1×10⁴ 個 ZnS，故生成量子點莫耳數為 (88.0×10⁻⁶ mol) / (1×10⁴) = 8.8×10⁻¹⁰ 莫耳（列式 1 分，答案 1 分）。",
        "（b）小題（2分）：ZnS 式量為 65.4 + 32.0 = 97.4 g/mol。每顆量子點含 ZnS 克數為 (1×10⁴ / 6.02×10²³) × 97.4 ≈ 1.62×10⁻¹⁸ 克（列式 1 分，答案 1 分）。"
      ]
    },
    inquiryFocus: {
      acquisition: "離心分離與紫外線-可見光吸收光譜 (UV-Vis) 定量奈米膠體濃度與帶隙吸收邊緣。",
      recording: "微莫耳級反應物配比、沉澱產率百分比與離子消耗量核算。",
      processing: "奈米粒子聚集度與產率關聯繪圖、巨觀莫耳數與微觀單顆粒子原子數（亞佛加厥常數）雙向換算。"
    }
  },

  ceec115_tidal_water_level: {
    id: "ceec115_tide",
    title: "115 年學測第 50~52 題：港口觀測站逐時相對潮位與潮差計算",
    subject: "地球科學 / 探究實作",
    type: "time_series",
    bestPlotMethod: "time_series_wave",
    bestPlotMethodLabel: "週期性時間序列波浪曲線 (正弦波動與潮差極值)",
    defaultMode: "line",
    allowedModes: [
      { mode: "line", label: "逐時潮位平滑波動曲線 (週期性波動)" },
      { mode: "scatter", label: "純散布點 (Scatter 描點)" }
    ],
    regressionApplicable: false,
    regressionWarning: "【嚴禁線性回歸】潮汐為月球與太陽引力引起的週期性正弦/餘弦流體波動，非線性單調變化，嚴禁使用線性回歸直線！",
    graphingRationale: "潮位隨時間呈現約 12.4 小時為半週期的正弦波動曲線。大考中心第 51 題非選擇題明確要求考生在坐標方格紙中，精準標記指定時間的點，並以平滑連續曲線連接各點，以判讀 15 時的乾潮極小值 (-1.50m) 與 21 時的滿潮極大值 (+1.75m)，並計算潮差 3.25m。這是典型的連續週期波動圖形。",
    csvFileName: "115學測_潮汐觀測站逐時相對潮位.csv",
    summary: "港口碼頭潮汐觀測站記錄 24 小時相對潮位，要求在坐標方格紙中精準描點連線，分析滿潮與乾潮極值並計算潮差。",
    xLabel: "記錄時間 t",
    xUnit: "時 (hr)",
    yLabel: "相對潮位 h",
    yUnit: "公尺 (m)",
    data: [
      { x: 12, y: 0.0,   isRequiredPoint: false, label: "12時 (起點)" },
      { x: 13, y: -0.75, isRequiredPoint: true,  label: "13時 (必描點)" },
      { x: 14, y: -1.25, isRequiredPoint: false },
      { x: 15, y: -1.50, isRequiredPoint: true,  label: "15時 乾潮極小值 (-1.50m)", note: "乾潮極小值" },
      { x: 16, y: -1.25, isRequiredPoint: false },
      { x: 17, y: -1.00, isRequiredPoint: true,  label: "17時 (必描點)" },
      { x: 18, y: -0.50, isRequiredPoint: false },
      { x: 19, y: 0.25,  isRequiredPoint: true,  label: "19時 (必描點)" },
      { x: 20, y: 1.25,  isRequiredPoint: false },
      { x: 21, y: 1.75,  isRequiredPoint: true,  label: "21時 滿潮極大值 (+1.75m)", note: "滿潮極大值" },
      { x: 22, y: 1.50,  isRequiredPoint: false },
      { x: 23, y: 1.00,  isRequiredPoint: true,  label: "23時 (必描點)" },
      { x: 24, y: 0.25,  isRequiredPoint: false, altLabel: "0時" },
      { x: 25, y: -0.25, isRequiredPoint: true,  label: "次日1時 (必描點)", altLabel: "次日1時" }
    ],
    theoryFormula: "h(t) ≈ A · cos(ωt - φ)，潮差 Δh = h_max - h_min = 1.75 - (-1.50) = 3.25 m",
    fullExamText: {
      intro: "【115 年學測自然考科 第 50~52 題 題組完整題幹】\n海洋蘊含豐富的天然資源，其中潮汐發電是利用海水漲落之水位差（潮差）驅動水輪機發電的再生能源技術。某海港設有潮汐觀測站，連續 24 小時記錄碼頭相對潮位 h（公尺）隨時間 t（小時）的變化，取當日中午 12 時為 t = 12，次日中午 12 時為 t = 24 或次日 12 時。表 9 列出部分觀測時間的相對潮位數據。",
      question: "【第 51 題（4 分非選擇題）原始試題】\n（a）依據表 9 數據，在答題卷對應之方格紙中，以『●』描出 t = 13、15、17、19、21、23 及次日 1 時（共 7 個時間點）的相對潮位，並以平滑曲線依序連接各點。（2 分）\n（b）由圖形判讀該海港在該日的滿潮與乾潮相對潮位，並列式計算此週期的潮差為多少公尺？（2 分）"
    },
    analysis: {
      stats: [
        { label: "乾潮極小值 (15時)", value: "-1.50 公尺", highlight: true },
        { label: "滿潮極大值 (21時)", value: "+1.75 公尺", highlight: true },
        { label: "單日計算潮差 Δh", value: "3.25 公尺 (1.75 - (-1.50))", highlight: true },
        { label: "大考必描數據點", value: "共 7 個關鍵時點" }
      ],
      scoringKey: [
        "大考中心評分原則（滿分 4 分）：",
        "（a）小題（2分）：7 個指定時間點坐標精確點出得 1 分；以平滑連續曲線順利連接各點得 1 分。",
        "（b）小題（2分）：寫出滿潮 +1.75m 與乾潮 -1.50m 得 1 分；列式 1.75 - (-1.50) = 3.25 公尺得 1 分（未列式僅寫 3.25 給 1 分）。"
      ]
    },
    inquiryFocus: {
      acquisition: "利用超音波或壓力式潮位儀長時間連續取樣，基準值校正（減去平均水位）。",
      recording: "時間序列記錄法（24 小時制與跨日標示），負值水位的物理意義（低於平均基準面）。",
      processing: "週期性波動曲線繪製、極值判讀、潮差波幅運算與水力發電重力位能估算。"
    }
  },

  ceec115_induced_current_quadrants: {
    id: "ceec115_current",
    title: "115 年學測第 53 題：磁鐵相對於線圈運動之感應電流多象限分佈",
    subject: "物理 / 探究實作",
    type: "scatter_quadrant",
    bestPlotMethod: "quadrant_scatter",
    bestPlotMethodLabel: "跨第 1、3 象限純散布點 (冷次定律方向與非對稱性)",
    defaultMode: "scatter",
    allowedModes: [
      { mode: "scatter", label: "第 1、3 象限精準散布點 (大考中心指定描點)" },
      { mode: "line", label: "平滑趨勢導引線 (觀察加速度效應)" }
    ],
    regressionApplicable: false,
    regressionWarning: "【嚴禁線性回歸】感應電流隨位置分布呈現非對稱雙峰趨勢，在線圈內部未測量，且向上加速打破空間對稱性，嚴禁使用單一直線回歸！",
    graphingRationale: "大考中心第 53(c) 題明確指示：『在答題卷對應之方格紙的坐標系中，描繪表 10 中所有數據點（共有 8 個點）』。題目旨在考查考生對『冷次定律正負號方向性（進入為第 3 象限、穿出為第 1 象限）』與『加速穿過造成第 1 象限量值較大』的理解，最精確的圖型就是四象限跨坐標散布圖，不需要全域連線，更嚴禁回歸直線！",
    csvFileName: "115學測_磁鐵運動感應電流與位置.csv",
    summary: "利用錄影格放分析磁鐵加速穿過線圈的瞬時位置 z 與感應電流 I，探討冷次定律方向性並在第 1、3 象限精準描繪 8 個數據點。",
    xLabel: "磁鐵位置 z",
    xUnit: "cm",
    yLabel: "感應電流 I",
    yUnit: "mA",
    data: [
      // z < 0 (進入線圈前，下方加速接近，感應電流為負，第3象限)
      { x: -20, y: -0.43, quadrant: 3, label: "z=-20cm" },
      { x: -15, y: -0.95, quadrant: 3, label: "z=-15cm" },
      { x: -10, y: -2.10, quadrant: 3, label: "z=-10cm" },
      { x: -5,  y: -3.40, quadrant: 3, label: "z=-5cm (下方進入，接近)" },
      // z > 0 (穿出線圈後，上方加速遠離，感應電流為正，第1象限)
      { x: 5,   y: 4.30,  quadrant: 1, label: "z=+5cm (上方穿出，v更快)" },
      { x: 10,  y: 2.70,  quadrant: 1, label: "z=+10cm" },
      { x: 15,  y: 1.20,  quadrant: 1, label: "z=+15cm" },
      { x: 20,  y: 0.54,  quadrant: 1, label: "z=+20cm" }
    ],
    theoryFormula: "ε = -dΦB / dt，I = ε / R（冷次定律正負號與加速度非對稱性）",
    fullExamText: {
      intro: "【115 年學測自然考科 第 53 題 原始試題題幹】\n某同學用手帶動磁鐵相對於線圈運動，以模擬潮汐驅動圖 21 發電設施中磁鐵相對於線圈的運動，如圖 22 所示，並將線圈串接檢流計 G。圖 22 中線圈與導線所標示的箭號，亦即電流由下往上流經檢流計的方向，取為正；並取線圈中點為位置 z 的原點，且 z 向上為正。\n該同學今將磁鐵從線圈下方，自靜止加速上提使磁鐵速度越來越快地穿過線圈。然後從錄影分析磁鐵位置 z 與感應電流 I，表 10 僅列出磁鐵在線圈外部的測量結果。",
      question: "【第 53 題（4 分非選擇題）原始三子題】\n（a）當 z < 0 時，說明研判感應電流 I 方向為正或負的理由。（1 分）\n（b）考量感應電流量值較大的一列數據，說明研判其屬於 z < 0 或 z > 0 的理由。（1 分）\n（c）在答題卷對應之方格紙的坐標系中，描繪表 10 中所有數據點（共有 8 個點）。（2 分）"
    },
    analysis: {
      stats: [
        { label: "分佈主要象限", value: "第 1 象限 與 第 3 象限", highlight: true },
        { label: "加速度非對稱效應", value: "|I(+5)| = 4.30 > |I(-5)| = 3.40", highlight: true },
        { label: "冷次定律方向判斷", value: "接近時阻礙 (I<0)，遠離時拉回 (I>0)" },
        { label: "必描繪數據點數", value: "共 8 個精確點" }
      ],
      scoringKey: [
        "大考中心評分原則：",
        "1. 象限判斷：依據冷次定律，磁鐵進入線圈時抗衡磁場產生反向感應電流 (I < 0)，故分佈於第 3 象限；離開時為第 1 象限。",
        "2. 非對稱性成因：磁鐵由靜止持續加速運動，穿出時速率大於進入時速率，故磁通量變化率更大，z = +5cm 處的感應電流量值 (4.30 mA) 顯著大於 z = -5cm 處 (3.40 mA)！",
        "3. 描點評分：8 個點必須精準坐落於第 1 與第 3 象限，且量值大者在第 1 象限。"
      ]
    },
    inquiryFocus: {
      acquisition: "高速攝影（60fps 或 120fps）搭配檢流計，將時間、空間與電磁量進行同步化格放擷取。",
      recording: "正負符號定義（原點設定在線圈中心，向上為正；電流向上為正），多象限數據記錄規範。",
      processing: "多象限散布圖繪製、對稱性打破的物理探究（加速度效應造成量值差異）。"
    }
  }
};

if (typeof module !== 'undefined' && module.exports) {
  module.exports = EXAM_DATASETS;
}
