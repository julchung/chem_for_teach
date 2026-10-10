import json

print("Building question bank for Chapter 4-8 元素週期性：電負度...")

questions = [
    {
        "id": "q1",
        "tag": "第三週期原子半徑最大元素性質",
        "question": "元素 $X$ 為第三週期原子半徑最大的元素，下列敘述何者<strong>正確</strong>？",
        "options": [
            "(A) 元素 $X$ 易與同週期中原子半徑最大的元素形成離子化合物",
            "(B) 元素 $X$ 是第三週期中電負度最大的元素",
            "(C) 元素 $X$ 是第三週期中游離能最小的元素",
            "(D) 元素 $X$ 易形成陰離子 $X^-$",
            "(E) 元素 $X$ 是第三週期中價電子最多的元素"
        ],
        "ans": 2,
        "explanation": "<strong>解析：</strong><br>• 同週期由左至右，隨有效核電荷增大，原子半徑逐漸減小；因此第三週期中原子半徑最大者為最左側第 1A 族的<strong>鈉元素（$\\text{Na}$）</strong>。<br>• <strong>(C) 正確：</strong>鈉為活潑鹼金屬，外層僅 1 個價電子且原子半徑大，第一游離能為第三週期最小（$\\text{IE}_1 = 496\\text{ kJ/mol}$）。<br>• (A) 錯誤：同週期半徑最大者為鈉自身，鈉與鈉結合成金屬晶體，非離子化合物；易與半徑小、電負度大的非金屬（如氯）形成離子化合物 $\\text{NaCl}$。<br>• (B) 錯誤：鈉的電負度僅 0.9，為第三週期中電負度最小者。<br>• (D) 錯誤：鈉傾向失去 1 個電子形成穩定八隅體陽離子 $\\text{Na}^+$。<br>• (E) 錯誤：鈉僅有 1 個價電子，為第三週期中最少。<br>故選 <strong>(C)</strong>。"
    },
    {
        "id": "q2",
        "tag": "原子序 1～20 元素週期性質圖表辨識",
        "question": "附圖是以原子序（1～20）為橫軸，以質子數、中子數、質量數、電負度、第一游離能中某種性質為縱軸所作之關係圖。其中圖(三)在原子序 2、10、18 處無對應數值而以虛線相連。試問下列各圖縱軸對應之性質何者<strong>正確</strong>？",
        "options": [
            "(A) 圖(一)為質子數",
            "(B) 圖(二)為電負度",
            "(C) 圖(三)為中子數",
            "(D) 圖(四)為第一游離能",
            "(E) 圖(一)為質量數"
        ],
        "ans": 3,
        "explanation": "<strong>解析：</strong><br>• <strong>圖(一) 為中子數：</strong>質量數減質子數（$A - Z$），數值隨原子序大致上升但因同位素而呈現微幅波折。<br>• <strong>圖(二) 為質子數：</strong>原子序即為質子數 $Z$，圖形為通過原點、斜率為 1 的完美直線。<br>• <strong>圖(三) 為電負度：</strong>縱軸最高點分別為氟 F(4.0)、氯 Cl(3.0)，且原子序 2 (He)、10 (Ne)、18 (Ar) 惰性氣體無對應數值以虛線相連，完全符合鮑林電負度特徵。<br>• <strong>圖(四) 為第一游離能：</strong>同週期呈現鋸齒狀波動上升，在鈍氣（He、Ne、Ar）處達峰值（約 400~600 kcal/mol），在鹼金屬（Li、Na、K）處暴跌至谷底。<br>故選 <strong>(D)</strong>。"
    },
    {
        "id": "q3",
        "tag": "原子結構與週期性綜合多選",
        "question": "下列有關原子結構與週期性規律的敘述，何者為<strong>錯誤</strong>？",
        "options": [
            "(A) 碳原子在基態時的電子組態，具有 2 個不成對電子",
            "(B) 鈉原子的第一游離能比鎂原子的第一游離能小",
            "(C) 硫原子的原子半徑比磷原子的原子半徑小",
            "(D) 氯原子的電負度是全週期表所有原子中最大的"
        ],
        "ans": 3,
        "explanation": "<strong>解析：</strong><br>• <strong>(D) 錯誤：</strong>全週期表中電負度最大的元素為<strong>氟原子（F = 4.0）</strong>。氯原子的電負度為 3.0，小於氟與氧（O = 3.5）。<br>• <strong>(A) 正確：</strong>碳原子（$Z=6$）基態電子組態為 $1s^2 2s^2 2p_x^1 2p_y^1$，依洪德定則，2p 軌域具有 2 個自旋平行之不成對電子。<br>• <strong>(B) 正確：</strong>$\\text{Na}(496\\text{ kJ/mol}) < \\text{Mg}(738\\text{ kJ/mol})$，鈉的核電荷較小且半徑大，第一游離能較小。<br>• <strong>(C) 正確：</strong>同週期由左至右有效核電荷增大，原子半徑遞減，硫（S）位於磷（P）之右側，故原子半徑 $\\text{S} < \\text{P}$。<br>故選 <strong>(D)</strong>。"
    },
    {
        "id": "q4",
        "tag": "第三列元素連續游離能與性質推論",
        "question": "甲、乙、丙為週期表中第三列（第三週期）的三種元素，其游離能與失去電子數目之關係圖中：丙在失去第 3 個電子時游離能暴增；甲在失去第 4 個電子時游離能暴增；乙在失去第 5 個電子時游離能暴增。則下列敘述何者<strong>錯誤</strong>？",
        "options": [
            "(A) 乙元素（Si）常被用來作為半導體之原料晶圓",
            "(B) 甲（Al）的氧化物溶於水呈強鹼性",
            "(C) 三者的原子半徑大小關係為：丙 > 甲 > 乙（Mg > Al > Si）",
            "(D) 三者的電負度大小順序為：乙 > 甲 > 丙（Si > Al > Mg）"
        ],
        "ans": 1,
        "explanation": "<strong>解析：</strong><br>• <strong>元素身分推導：</strong><br>&nbsp;&nbsp;• 丙於 $\\text{IE}_3$ 暴增 $\\rightarrow$ 具 2 個價電子 $\\rightarrow$ 第三週期 2A 族<strong>鎂（Mg）</strong>。<br>&nbsp;&nbsp;• 甲於 $\\text{IE}_4$ 暴增 $\\rightarrow$ 具 3 個價電子 $\\rightarrow$ 第三週期 3A 族<strong>鋁（Al）</strong>。<br>&nbsp;&nbsp;• 乙於 $\\text{IE}_5$ 暴增 $\\rightarrow$ 具 4 個價電子 $\\rightarrow$ 第三週期 4A 族<strong>矽（Si）</strong>。<br>• <strong>(B) 錯誤：</strong>甲為鋁，其氧化物 $\\text{Al}_2\\text{O}_3$ 為難溶於水的<strong>兩性氧化物</strong>，既可溶於強酸亦可溶於強鹼，溶於水不呈強鹼性（呈強鹼性者為 1A 族如 $\\text{Na}_2\\text{O}$）。<br>• <strong>(A) 正確：</strong>矽為現代積體電路與半導體晶片之核心原料。<br>• <strong>(C) 正確：</strong>同週期由左至右原子半徑變小，故 $\\text{Mg} > \\text{Al} > \\text{Si}$（丙 > 甲 > 乙）。<br>• <strong>(D) 正確：</strong>同週期由左至右電負度遞增，故 $\\text{Si (1.8)} > \\text{Al (1.5)} > \\text{Mg (1.2)}$（乙 > 甲 > 丙）。<br>故選 <strong>(B)</strong>。"
    },
    {
        "id": "q5",
        "tag": "週期性圖表關係正誤判斷",
        "question": "下列關於元素週期性與縱座標圖形關係之敘述，何者為<strong>完全正確</strong>？",
        "options": [
            "(A) 碳原子連續游離能應在移去第 3 個電子時急遽暴增跳躍",
            "(B) 鹵素元素（F、Cl、Br、I、At）之電負度隨原子序增加而逐漸遞減",
            "(C) 第三週期原子之原子半徑隨原子序增加而呈現直線向上遞增",
            "(D) 原子序 1～20 元素之價電子數隨原子序增加呈現斜率為 1 之單調直線"
        ],
        "ans": 1,
        "explanation": "<strong>解析：</strong><br>• <strong>(B) 正確：</strong>鹵素元素（第 17 族）由上而下隨原子序增加，電子層數增加且半徑擴大，原子核對鍵結共用電子的吸引力減弱，故電負度由 F(4.0) 經 Cl(3.0)、Br(2.8)、I(2.5) 依序遞減至 At(2.2)。<br>• <strong>(A) 錯誤：</strong>碳原子（$Z=6$，組態 $1s^2 2s^2 2p^2$）外層有 4 個價電子，連續游離能應在移去第 5 個電子（$\\text{IE}_5$，破壞 1s 鈍氣核心）時劇烈暴增。<br>• <strong>(C) 錯誤：</strong>同週期由左至右有效核電荷增大，原子半徑隨原子序增加而向下遞減。<br>• <strong>(D) 錯誤：</strong>主族元素價電子數呈週期性循環（1~8），不會隨原子序無上限線性增加。<br>故選 <strong>(B)</strong>。"
    },
    {
        "id": "q6",
        "tag": "原子結構與元素週期推斷綜合",
        "question": "現有四種原子：$W$ 為鹵素中電負度最大者；$X$ 是第四週期元素且最穩定離子 $X^{2+}$ 具全滿 d 軌域；$Y$ 之 $Y^{2-}$ 與第三週期鈍氣電子組態相同；$Z$ 為第 2 族非放射性元素中原子序最大者。則下列敘述何者<strong>錯誤</strong>？",
        "options": [
            "(A) $0.1\\text{ M}$ 的 $X^{2+}$ 與 $0.1\\text{ M}$ 的 $Y^{2-}$ 水溶液混合會產生沉澱",
            "(B) $0.1\\text{ M}$ 的 $Z^{2+}$ 水溶液可與硫酸鈉水溶液反應產生白色沉澱",
            "(C) $X^{2+}$ 離子的基態電子組態中仍具有 $4s$ 軌域電子",
            "(D) 這四種原子中，以 $Z$ 原子的原子半徑最大"
        ],
        "ans": 2,
        "explanation": "<strong>解析：</strong><br>• <strong>微粒身分推導：</strong><br>&nbsp;&nbsp;• (i) 鹵素中電負度最大者：$W = \\text{F}$（氟，$Z=9$）。<br>&nbsp;&nbsp;• (ii) 第四週期最穩定 $X^{2+}$ 具 $3d^{10}$ 全滿：$X = \\text{Zn}$（鋅，$Z=30$）。<br>&nbsp;&nbsp;• (iii) $Y^{2-}$ 與第三週期鈍氣 Ar 組態相同：$Y = \\text{S}$（硫，$Z=16$）。<br>&nbsp;&nbsp;• (iv) 第 2 族鹼土金屬非放射性最大者（Be, Mg, Ca, Sr, Ba, Ra，鐳 Ra 具放射性）：$Z = \\text{Ba}$（鋇，$Z=56$）。<br>• <strong>(C) 錯誤：</strong>鋅原子基態為 $[\\text{Ar}]3d^{10}4s^2$，形成 $\\text{Zn}^{2+}$ 時失去最外層的 $4s^2$ 電子，電子組態為 $[\\text{Ar}]3d^{10}$，已無 $4s$ 軌域電子。<br>• <strong>(A) 正確：</strong>$\\text{Zn}^{2+} + \\text{S}^{2-} \\rightarrow \\text{ZnS}\\downarrow$（白色沉澱）。<br>• <strong>(B) 正確：</strong>$\\text{Ba}^{2+} + \\text{SO}_4^{2-} \\rightarrow \\text{BaSO}_4\\downarrow$（難溶性白色硫酸鋇沉澱）。<br>• <strong>(D) 正確：</strong>鋇位於第六週期且為鹼土金屬，半徑遠大於 F、S、Zn。<br>故選 <strong>(C)</strong>。"
    },
    {
        "id": "q7",
        "tag": "原子序 1～19 週期性物理量與單位判讀",
        "question": "附圖為原子序 1～19 之元素的某種性質關係圖，其峰值出現在鹼金屬 Li、Na、K，且各週期內隨原子序增加而逐漸下降。則該關係圖中 y 軸的物理量與適用單位分別為何？",
        "options": [
            "(A) 原子半徑；單位為 $\\text{pm}$（皮米）",
            "(B) 第一游離能；單位為 $\\text{kJ/mol}$",
            "(C) 鮑林電負度；無單位",
            "(D) 中子數；無單位"
        ],
        "ans": 0,
        "explanation": "<strong>解析：</strong><br>• <strong>(A) 正確：</strong>該關係圖中，每週期起點的第 1 族鹼金屬（Li 約 152、Na 約 186、K 約 227）處呈現極大峰值；進入同週期後隨原子序增加，因有效核電荷增大，數值逐漸遞減至鹵素與鈍氣；進入下一週期又劇烈暴增。此週期性規律完全符合「<strong>原子半徑（Atomic Radius）</strong>」，其常用長度單位為皮米（$\\text{pm} = 10^{-12}\\text{ m}$）或埃（$\\text{\\AA} = 100\\text{ pm}$）。<br>• 游離能與電負度皆是在鈍氣或鹵素處達峰值、鹼金屬處為谷底，與本圖形走勢恰好相反。<br>故選 <strong>(A)</strong>。"
    },
    {
        "id": "q8",
        "tag": "價電子與不成對電子差值 (m-n) 推導",
        "question": "元素甲～戊為第二、三週期原子序相連的五個元素，價電子數 $m$ 與基態不成對電子數 $n$ 之差值 $(m-n)$ 分別為：甲=8、乙=6、丙=4、丁=2、戊=0。已知只有一種原子基態不具不成對電子，則下列有關五元素的敘述何者<strong>錯誤</strong>？",
        "options": [
            "(A) 第一游離能最大的原子為甲（Ne）",
            "(B) 電負度最大的原子為乙（F）",
            "(C) 原子半徑最大的原子為戊（Na）",
            "(D) 具有同素異形體的元素為丁（N）"
        ],
        "ans": 3,
        "explanation": "<strong>解析：</strong><br>• <strong>差值邏輯分析：</strong><br>&nbsp;&nbsp;• 8A 族鈍氣（$s^2 p^6$）：$m=8, n=0 \\rightarrow m-n = 8$，故甲必為鈍氣！<br>&nbsp;&nbsp;• 7A 族鹵素（$s^2 p^5$）：$m=7, n=1 \\rightarrow m-n = 6$，故乙必為鹵素！<br>&nbsp;&nbsp;• 6A 族氧族（$s^2 p^4$）：$m=6, n=2 \\rightarrow m-n = 4$，故丙必為 6A 族！<br>&nbsp;&nbsp;• 1A 族鹼金屬（$s^1$）：$m=1, n=1 \\rightarrow m-n = 0$，故戊必為 1A 族！<br>&nbsp;&nbsp;• 丁之 $m-n = 2$：可為 5A 族（$m=5, n=3$）。<br>• <strong>元素定位：</strong>五元素原子序相連且跨第二、三週期，且「只有一種原子不具不成對電子（$n=0$ 僅有 Ne，不能包含 Mg）」，因此這五個連續元素必為：<br>&nbsp;&nbsp;丁：$_7\\text{N}$、$丙：_8\\text{O}$、$乙：_9\\text{F}$、$甲：_{10}\\text{Ne}$、$戊：_{11}\\text{Na}$。<br>• <strong>(D) 錯誤：</strong>氧元素（丙）具有同素異形體（$\\text{O}_2$ 氧氣與 $\\text{O}_3$ 臭氧）；丁（氮）在自然界中無同素異形體。<br>• (A) Ne 鈍氣游離能最高；(B) 氟 F 電負度全表最高（4.0）；(C) 鈉 Na 位於第三週期，半徑最大。<br>故選 <strong>(D)</strong>。"
    },
    {
        "id": "q9",
        "tag": "第二週期游離能折線走勢特徵",
        "question": "關於第二週期 C、N、O、F 四種元素的第一游離能隨原子序（$Z=6\\sim 9$）增加之變化圖形，其折線走勢特徵為何？",
        "options": [
            "(A) 單調直線向下遞減",
            "(B) 先升至最高點後平緩向下遞減",
            "(C) 先上升後轉折下降，隨後再次大幅攀升（鋸齒狀轉折）",
            "(D) 呈現水平直線保持不變"
        ],
        "ans": 2,
        "explanation": "<strong>解析：</strong><br>• 第二週期元素第一游離能數據為：$\\text{C}(1086) < \\text{O}(1314) < \\text{N}(1402) < \\text{F}(1681\\text{ kJ/mol})$。<br>• 隨原子序增加（$Z = 6 \\rightarrow 7 \\rightarrow 8 \\rightarrow 9$）：<br>&nbsp;&nbsp;1. C 到 N：有效核電荷增加，且 N($2p^3$) 具半滿穩定組態，游離能上升（1086 $\\rightarrow$ 1402）；<br>&nbsp;&nbsp;2. N 到 O：O($2p^4$) 因軌域內出現第一對成對電子，電子間排斥力較強，游離能發生<strong>反常下降</strong>（1402 $\\rightarrow$ 1314）；<br>&nbsp;&nbsp;3. O 到 F：有效核電荷顯著增加且半徑極小，游離能再度大幅衝高（1314 $\\rightarrow$ 1681）。<br>• 因此圖形特徵呈現「上升 $\\rightarrow$ 轉折下降 $\\rightarrow$ 大幅衝高」之經典鋸齒狀折線。故選 <strong>(C)</strong>。"
    },
    {
        "id": "q10",
        "tag": "鮑林電負度定義與基準",
        "question": "下列關於鮑林電負度（Electronegativity）定義與基準之敘述，何者<strong>完全正確</strong>？",
        "options": [
            "(A) 電負度是指中性氣態原子獲得一個電子形成陰離子所放出的能量",
            "(B) 鮑林電負度是以氟原子為基準，定其電負度為 4.0",
            "(C) 電負度具有明確之物理能量單位，通常以 $\\text{kJ/mol}$ 表示",
            "(D) 電負度越大代表該原子越容易失去電子成為陽離子"
        ],
        "ans": 1,
        "explanation": "<strong>解析：</strong><br>• <strong>(B) 正確：</strong>鮑林標度以吸引共用電子能力最強之<strong>氟（F）</strong>原子為全表基準，定其電負度為 <strong>4.0</strong>，其他原子皆為相對比較值。<br>• (A) 錯誤：此為「電子親和力（Electron Affinity）」之定義；電負度是指「分子內部成份原子吸引成鍵共用電子對之相對能力」。<br>• (C) 錯誤：鮑林電負度為相對無因次標度數值，無能量單位。<br>• (D) 錯誤：電負度大代表吸引電子能力強，越容易得到電子呈現非金屬性。<br>故選 <strong>(B)</strong>。"
    },
    {
        "id": "q11",
        "tag": "電負度差值與化學鍵性質",
        "question": "根據鮑林電負度準則，當鍵結兩原子之電負度差值 $\\Delta\\text{EN}$ 大於約 1.9 時，兩原子間主要形成何種化學鍵？",
        "options": [
            "(A) 非極性共價鍵",
            "(B) 極性共價鍵",
            "(C) 離子鍵",
            "(D) 配位共價鍵"
        ],
        "ans": 2,
        "explanation": "<strong>解析：</strong><br>• <strong>(C) 正確：</strong>當兩原子電負度差值 $\\Delta\\text{EN} \\ge 1.9$ 時，共用電子對幾乎完全轉移至電負度大的非金屬原子上，形成陰陽離子間強烈庫侖靜電引力，通常界定為「<strong>離子鍵</strong>」。<br>• 當 $\\Delta\\text{EN} = 0$ 時為非極性共價鍵；當 $0 < \\Delta\\text{EN} < 1.9$ 時為極性共價鍵。<br>故選 <strong>(C)</strong>。"
    },
    {
        "id": "q12",
        "tag": "路易斯結構中心原子選取原則",
        "question": "繪製共價分子之路易斯結構式（Lewis Structure）時，通常應依據下列何種原則選定中心原子？",
        "options": [
            "(A) 通常以電負度較大的原子為中心原子",
            "(B) 通常以電負度較小的原子為中心原子（H 與 F 除外）",
            "(C) 氫原子（H）永遠為首選之中心原子",
            "(D) 氟原子（F）因電負度最大，恆作為中心原子"
        ],
        "ans": 1,
        "explanation": "<strong>解析：</strong><br>• <strong>(B) 正確：</strong>電負度較小的原子吸引外層電子相對較鬆，能提供更多價軌域與多個周圍原子共用電子對，故通常以<strong>電負度較小的原子為中心原子</strong>。<br>• <strong>重要例外：</strong>氫（H）僅有 1s 軌域只能形成 1 個單鍵，氟（F）電負度極大且幾乎只形成單鍵，兩者<strong>幾乎永遠只能作為分子外圍端點原子</strong>。<br>故選 <strong>(B)</strong>。"
    },
    {
        "id": "q13",
        "tag": "金屬非金屬性與電負度分野",
        "question": "下列有關元素電負度與金屬、非金屬性強弱關係之敘述，何者為<strong>錯誤</strong>？",
        "options": [
            "(A) 一般典型金屬元素的鮑林電負度通常小於 2.0",
            "(B) 典型非金屬元素的鮑林電負度通常大於 2.0",
            "(C) 電負度越小的金屬元素，其還原力與金屬活性越強",
            "(D) 銫（Cs）的電負度高達 4.0，為最強的金屬元素"
        ],
        "ans": 3,
        "explanation": "<strong>解析：</strong><br>• <strong>(D) 錯誤：</strong>銫（Cs）與鍅（Fr）位於週期表左下角，其電負度僅約 <strong>0.7</strong>，為全表電負度最小、最容易失去電子的最強金屬元素；4.0 是非金屬氟（F）的電負度。<br>• (A)(B)(C) 敘述皆完全正確。<br>故選 <strong>(D)</strong>。"
    },
    {
        "id": "q14",
        "tag": "第二週期主族元素電負度遞增規律",
        "question": "下列第二週期主族元素中，鮑林電負度數值之大小排列順序，何者<strong>完全正確</strong>？",
        "options": [
            "(A) $\\text{Li} > \\text{Be} > \\text{B} > \\text{C}$",
            "(B) $\\text{F} > \\text{O} > \\text{N} > \\text{C}$",
            "(C) $\\text{C} > \\text{N} > \\text{O} > \\text{F}$",
            "(D) $\\text{N} > \\text{O} > \\text{F} > \\text{C}$"
        ],
        "ans": 1,
        "explanation": "<strong>解析：</strong><br>• <strong>(B) 正確：</strong>第二週期由左至右隨有效核電荷增大，電負度依序遞增：$\\text{Li (1.0)} < \\text{Be (1.5)} < \\text{B (2.0)} < \\text{C (2.5)} < \\text{N (3.0)} < \\text{O (3.5)} < \\text{F (4.0)}$。由大至小排列即為：$\\text{F (4.0)} > \\text{O (3.5)} > \\text{N (3.0)} > \\text{C (2.5)}$。<br>故選 <strong>(B)</strong>。"
    }
]

# Write question_bank.json
with open('question_bank.json', 'w', encoding='utf-8') as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

print(f"question_bank.json generated with {len(questions)} high-quality questions!")

# Generate Markdown file
md_content = "# 4-8 元素週期性：電負度 · 通關測驗題庫電子檔\n\n"
md_content += f"> 本題庫收錄 4-8 單元核心檢核、原創圖表題及螢幕擷取試題解析，共收錄 {len(questions)} 題完整試題與深度觀念解析。\n\n---\n\n"

for i, q in enumerate(questions, 1):
    md_content += f"### 第 {i} 題【{q['tag']}】\n\n"
    md_content += f"**題目：**\n{q['question']}\n\n"
    md_content += "**選項：**\n"
    for opt in q['options']:
        md_content += f"- {opt}\n"
    correct_opt_char = chr(ord('A') + q['ans'])
    md_content += f"\n**【正確答案】**：({correct_opt_char})\n\n"
    clean_exp = q['explanation'].replace('<br>', '\n').replace('&nbsp;', ' ').replace('<strong>', '**').replace('</strong>', '**')
    md_content += f"**【詳解與觀念剖析】**：\n{clean_exp}\n\n---\n\n"

with open('電負度_通關測驗題庫.md', 'w', encoding='utf-8') as f:
    f.write(md_content)

print("電負度_通關測驗題庫.md generated successfully!")
