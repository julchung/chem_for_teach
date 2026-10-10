import json

questions = [
    {
        "id": "q1",
        "tag": "週期表相對位置與原子序推導",
        "question": "右圖表示週期表中 A 族元素的一部分，其中 b 原子與 c 原子電子總數之和，恰為 a 原子電子總數的 4 倍，則下列所述何者正確？<br><div style='text-align:center; margin:10px 0;'><table style='display:inline-table; border-collapse:collapse; text-align:center; font-weight:bold;'><tr><td style='border:1px solid #64748b; padding:6px 14px; background:rgba(56,189,248,0.2);'>a</td></tr><tr><td style='border:none; padding:0;'><table style='border-collapse:collapse; text-align:center;'><tr><td style='border:1px solid #64748b; padding:6px 14px; background:rgba(56,189,248,0.15);'>b</td><td style='border:1px solid transparent; padding:6px 14px;'>&nbsp;</td><td style='border:1px solid #64748b; padding:6px 14px; background:rgba(56,189,248,0.15);'>c</td></tr></table></td></tr></table></div>",
        "options": [
            "(A) a、b、c 三原子中，有 1 個金屬元素，2 個非金屬元素",
            "(B) b、c 兩原子可形成離子化合物",
            "(C) a、b、c 三原子之原子核的正電荷總數為 40",
            "(D) a、b、c 三原子中，有 2 個金屬元素，1 個非金屬元素"
        ],
        "ans": 2,
        "explanation": "<strong>解析：</strong><br>• <strong>位置關係與原子序代數推導：</strong><br>&nbsp;&nbsp;設 a 位於第二週期主族，原子序為 $Z_a$。其正下方第三週期同族元素之原子序為 $Z_a + 8$。<br>&nbsp;&nbsp;依圖示位置，b 位於正下方左側一格，故原子序 $Z_b = Z_a + 7$；c 位於正下方右側一格，故原子序 $Z_c = Z_a + 9$。<br>• <strong>列式求解：</strong><br>&nbsp;&nbsp;依題意：$Z_b + Z_c = 4 Z_a \\implies (Z_a + 7) + (Z_a + 9) = 4 Z_a \\implies 2Z_a + 16 = 4Z_a \\implies Z_a = 8$（氧 O）。<br>&nbsp;&nbsp;因此，a 為氧（O，原子序 8）；正下方為硫（S，16）；左側 b 為磷（P，原子序 15）；右側 c 為氯（Cl，原子序 17）。<br>• <strong>選項檢核：</strong><br>&nbsp;&nbsp;(A)(D) a(O)、b(P)、c(Cl) 三者皆屬於<strong>非金屬元素</strong>（金屬 0 個，非金屬 3 個），敘述錯誤。<br>&nbsp;&nbsp;(B) P 與 Cl 皆為非金屬元素，兩者以共價鍵結合形成分子化合物（如 $\\text{PCl}_3$ 或 $\\text{PCl}_5$），非離子化合物，敘述錯誤。<br>&nbsp;&nbsp;(C) a、b、c 之核正電荷總數（即質子數總和）$= 8 + 15 + 17 = 40$，完全正確！<br>故選 <strong>(C)</strong>。"
    },
    {
        "id": "q2",
        "tag": "氣態離子半徑大小比較",
        "question": "有關氣態離子之離子半徑大小比較，下列各項關係式中，何者為<strong>錯誤</strong>？",
        "options": [
            "(A) $\\text{Cs}^+ > \\text{Na}^+$",
            "(B) $\\text{Mg}^{2+} > \\text{Na}^+$",
            "(C) $\\text{F}^- > \\text{Na}^+$",
            "(D) $\\text{Cr}^{2+} > \\text{Cr}^{3+}$"
        ],
        "ans": 1,
        "explanation": "<strong>解析：</strong><br>• <strong>(A) $\\text{Cs}^+ > \\text{Na}^+$：正確。</strong>Cs⁺ 具有 5 個電子層（氙組態），Na⁺ 僅具有 2 個電子層（氖組態）。同族離子由上至下電子層數增加，離子半徑顯著增大。<br>• <strong>(B) $\\text{Mg}^{2+} > \\text{Na}^+$：錯誤。</strong>$\\text{Mg}^{2+}$（$Z=12$）與 $\\text{Na}^+$（$Z=11$）皆具有 10 個電子的等電子組態。核電荷愈大者對電子的吸引力愈強，電子雲向內緊縮，故半徑應為 $\\text{Na}^+ > \\text{Mg}^{2+}$。<br>• <strong>(C) $\\text{F}^- > \\text{Na}^+$：正確。</strong>$\\text{F}^-$（$Z=9$）與 $\\text{Na}^+$（$Z=11$）均為 10 電子等電子物種。陰離子核電荷較小（質子數少），核引力較弱，半徑大於同組態之陽離子，故 $\\text{F}^- > \\text{Na}^+$ 正確。<br>• <strong>(D) $\\text{Cr}^{2+} > \\text{Cr}^{3+}$：正確。</strong>同一金屬元素形成不同氧化態陽離子時，價數愈高表示失去愈多電子，有效核電荷引力相對增強，半徑愈小，故低價陽離子半徑大於高價陽離子。<br>故選 <strong>(B)</strong>。"
    },
    {
        "id": "q3",
        "tag": "金屬原子與離子半徑極值比較",
        "question": "下列哪一個金屬原子或離子的半徑<strong>最大</strong>？",
        "options": [
            "(A) $\\text{Be}$",
            "(B) $\\text{Mg}^{2+}$",
            "(C) $\\text{Mn}$",
            "(D) $\\text{Ca}$"
        ],
        "ans": 3,
        "explanation": "<strong>解析：</strong><br>• <strong>主量子數（電子層數）是決定粒子半徑的首要主導因素：</strong><br>&nbsp;&nbsp;1. $\\text{Ca}$（鈣，第 4 週期 IIA 族中性原子，$Z=20$）：具有 <strong>4 個電子層</strong>，電子組態為 $[\\text{Ar}] 4s^2$，原子半徑約 197 pm。<br>&nbsp;&nbsp;2. $\\text{Mn}$（錳，第 4 週期 VIIB 族過渡元素，$Z=25$）：亦具有 4 個電子層，但因核內質子數多（有效核電荷較大），原子半徑約 127 pm，明顯小於同週期左側的 Ca。<br>&nbsp;&nbsp;3. $\\text{Be}$（鈹，第 2 週期 IIA 族，$Z=4$）：僅具有 <strong>2 個電子層</strong>，原子半徑約 112 pm。<br>&nbsp;&nbsp;4. $\\text{Mg}^{2+}$（鎂離子，$Z=12$）：失去 2 個價電子後僅剩 <strong>2 個電子層</strong>（氖組態），半徑縮小至約 72 pm。<br>• 綜合大小排列為：$\\text{Ca} > \\text{Mn} > \\text{Be} > \\text{Mg}^{2+}$，半徑最大者為 $\\text{Ca}$。<br>故選 <strong>(D)</strong>。"
    },
    {
        "id": "q4",
        "tag": "同週期原子半徑週期性趨勢",
        "question": "週期表中同列（同週期）元素之原子半徑，大致隨原子序之增加而呈現何種規律趨勢？",
        "options": [
            "(A) 遞減",
            "(B) 先減後增",
            "(C) 先增後減",
            "(D) 遞增"
        ],
        "ans": 0,
        "explanation": "<strong>解析：</strong><br>• 同列（同週期）元素的最外層電子具有相同的主量子數 $n$（即主電子層數相同），內層電子提供的屏蔽效應增加有限。<br>• 由左至右隨原子序 $Z$ 逐一增加，原子核內的質子數增加，造成<strong>有效核電荷（$Z^*$）持續增大</strong>。<br>• 原子核對最外層電子的靜電庫侖引力顯著增強，將整個電子雲向內緊密拉攏，使得原子半徑隨原子序增加而<strong>大致遞減</strong>。<br>故選 <strong>(A)</strong>。"
    },
    {
        "id": "q5",
        "tag": "同週期半徑遞減之物理機制",
        "question": "同一週期的元素，原子序愈大其原子半徑反而愈小，其主要核心物理原因為何？",
        "options": [
            "(A) 外層電子數漸增使電子間排斥力劇烈壓縮軌域",
            "(B) 價電子數增加導致內層遮蔽效應大幅增強",
            "(C) 原子核內質子數漸增使有效核電荷增大、引力增強",
            "(D) 中子數與原子量漸增使原子核重力場顯著增加"
        ],
        "ans": 2,
        "explanation": "<strong>解析：</strong><br>• 同週期元素的最外層電子均填入同一個主量子數殼層（$n$ 相同），電子層數維持不變。<br>• 隨原子序增加，原子核內的<strong>質子數（核電荷 $Z$）逐一增加</strong>；雖然外層電子也增加，但同層電子彼此之間的屏蔽常數 $\\sigma$ 增長緩慢，導致<strong>有效核電荷 $Z^* = Z - \\sigma$ 明顯增大</strong>。<br>• 增大的有效核電荷對外層電子施加更強烈的庫侖引力，將軌域電子雲緊縮向核中心靠攏，因此原子序愈大，半徑愈小。<br>故選 <strong>(C)</strong>。"
    },
    {
        "id": "q6",
        "tag": "離子半徑跨族與價數綜合判斷",
        "question": "下列有關氣態離子之半徑大小比較，何者敘述<strong>完全正確</strong>？",
        "options": [
            "(A) $\\text{Mg}^{2+} > \\text{Na}^+$",
            "(B) $\\text{K}^+ > \\text{Rb}^+$",
            "(C) $\\text{F}^- > \\text{Na}^+$",
            "(D) $\\text{Cl}^- > \\text{Br}^-$"
        ],
        "ans": 2,
        "explanation": "<strong>解析：</strong><br>• <strong>(A) 錯誤：</strong>$\\text{Mg}^{2+}$（$Z=12$）與 $\\text{Na}^+$（$Z=11$）均為 10 電子等電子微粒。Mg 核電荷較大、引力較強，半徑較小，應為 $\\text{Na}^+ > \\text{Mg}^{2+}$。<br>• <strong>(B) 錯誤：</strong>$\\text{K}^+$（第 3 週期離子，3層電子）與 $\\text{Rb}^+$（第 4 週期離子，4層電子）為同族鹼金屬離子，由上至下電子層數增加，半徑應為 $\\text{Rb}^+ > \\text{K}^+$。<br>• <strong>(C) 正確：</strong>$\\text{F}^-$（$Z=9$）與 $\\text{Na}^+$（$Z=11$）同為 10 電子等電子物種。核電荷 $Z(\\text{F}) < Z(\\text{Na})$，F 核引力較小，電子雲較為擴散，故半徑 $\\text{F}^- > \\text{Na}^+$。<br>• <strong>(D) 錯誤：</strong>同族鹵素陰離子由上至下電子層數增加，半徑應為 $\\text{Br}^- > \\text{Cl}^-$。<br>故選 <strong>(C)</strong>。"
    },
    {
        "id": "q7",
        "tag": "跨週期原子與離子半徑綜合判斷",
        "question": "下列關於粒子半徑大小的比較，何者<strong>正確</strong>？",
        "options": [
            "(A) $\\text{Fe}^{3+} > \\text{Fe}^{2+}$",
            "(B) $\\text{K}^+ > \\text{Cl}^-$",
            "(C) $\\text{Ca} > \\text{Mg}$",
            "(D) $\\text{O} > \\text{N}$"
        ],
        "ans": 2,
        "explanation": "<strong>解析：</strong><br>• <strong>(A) 錯誤：</strong>同元素陽離子氧化態愈高、失去電子愈多，有效核電荷引力愈強，半徑愈小，應為 $\\text{Fe}^{2+} > \\text{Fe}^{3+}$。<br>• <strong>(B) 錯誤：</strong>$\\text{K}^+$（$Z=19$）與 $\\text{Cl}^-$（$Z=17$）同為 18 電子等電子微粒。K 核電荷較大引力強，半徑較小，應為 $\\text{Cl}^- > \\text{K}^+$。<br>• <strong>(C) 正確：</strong>Ca（第 4 週期，4層電子）與 Mg（第 3 週期，3層電子）同屬鹼土金屬（IIA 族）。同族由上而下電子層數增加，故半徑 $\\text{Ca} > \\text{Mg}$。<br>• <strong>(D) 錯誤：</strong>N（$Z=7$）與 O（$Z=8$）為第 2 週期同列元素。同週期由左至右隨核電荷增大半徑遞減，應為 $\\text{N} > \\text{O}$。<br>故選 <strong>(C)</strong>。"
    },
    {
        "id": "q8",
        "tag": "等電子序列半徑大小排序",
        "question": "下列具有氖（Ne）基態電子組態之等電子微粒：${}_{8}\\text{O}^{2-}$、${}_{9}\\text{F}^-$、${}_{11}\\text{Na}^+$、${}_{12}\\text{Mg}^{2+}$、${}_{13}\\text{Al}^{3+}$，其離子半徑由<strong>大到小</strong>的正確順序為何？",
        "options": [
            "(A) $\\text{Al}^{3+} > \\text{Mg}^{2+} > \\text{Na}^+ > \\text{F}^- > \\text{O}^{2-}$",
            "(B) $\\text{O}^{2-} > \\text{F}^- > \\text{Na}^+ > \\text{Mg}^{2+} > \\text{Al}^{3+}$",
            "(C) $\\text{Na}^+ > \\text{Mg}^{2+} > \\text{Al}^{3+} > \\text{O}^{2-} > \\text{F}^-$",
            "(D) $\\text{F}^- > \\text{O}^{2-} > \\text{Na}^+ > \\text{Mg}^{2+} > \\text{Al}^{3+}$"
        ],
        "ans": 1,
        "explanation": "<strong>解析：</strong><br>• 題中所有微粒均含有 10 個電子（組態皆為 $1s^2 2s^2 2p^6$），屬於<strong>等電子序列 (Isoelectronic Series)</strong>。<br>• 在電子數與電子屏蔽均相同的情形下，離子半徑完全由原子核內的質子數（核電荷 $Z$）決定：<br>&nbsp;&nbsp;- 核電荷愈小，原子核對外層電子的束縛力愈弱，電子間互斥使半徑膨脹增大；<br>&nbsp;&nbsp;- 核電荷愈大，原子核對外層電子的束縛力愈強，電子雲緊縮向核靠攏，半徑縮小。<br>• 比較核電荷 $Z$：$\\text{O}(8) < \\text{F}(9) < \\text{Na}(11) < \\text{Mg}(12) < \\text{Al}(13)$。<br>• 故半徑大小順序為：$\\text{O}^{2-} > \\text{F}^- > \\text{Na}^+ > \\text{Mg}^{2+} > \\text{Al}^{3+}$。<br>故選 <strong>(B)</strong>。"
    },
    {
        "id": "q9",
        "tag": "原子與相應離子半徑關係",
        "question": "下列有關中性原子與其相應離子之半徑大小關係，何者敘述<strong>完全正確</strong>？",
        "options": [
            "(A) 鈉原子半徑小於鈉離子半徑（$\\text{Na} < \\text{Na}^+$）",
            "(B) 氯原子半徑大於氯離子半徑（$\\text{Cl} > \\text{Cl}^-$）",
            "(C) 鐵原子與其二價、三價離子半徑大小關係為：$\\text{Fe} > \\text{Fe}^{2+} > \\text{Fe}^{3+}$",
            "(D) 氧離子半徑小於中性氧原子半徑（$\\text{O}^{2-} < \\text{O}$）"
        ],
        "ans": 2,
        "explanation": "<strong>解析：</strong><br>• <strong>陽離子半徑 < 中性原子半徑：</strong>原子失去價電子形成陽離子時，最外層主電子層往往消失（例如 Na 有 3 層，Na⁺ 僅剩 2 層），且剩餘電子受到相對較強之核電荷束縛，故半徑顯著縮小（$\\text{Na} > \\text{Na}^+$，(A) 錯誤）。<br>• <strong>陰離子半徑 > 中性原子半徑：</strong>原子獲得電子形成陰離子時，核電荷不變但電子數增加，電子間相互排斥力加劇，使電子雲向外擴散，故陰離子半徑大於原原子（$\\text{Cl}^- > \\text{Cl}$，$\\text{O}^{2-} > \\text{O}$，(B)(D) 錯誤）。<br>• <strong>同元素多價陽離子：</strong>失去愈多電子，正價數愈高，有效核引力相對於剩餘電子愈強，半徑愈小，故 $\\text{Fe} > \\text{Fe}^{2+} > \\text{Fe}^{3+}$ 完全正確。<br>故選 <strong>(C)</strong>。"
    },
    {
        "id": "q10",
        "tag": "跨週期元素原子半徑排序",
        "question": "試比較第二週期至第四週期的四種主族元素：${}_{9}\\text{F}$、${}_{17}\\text{Cl}$、${}_{11}\\text{Na}$、${}_{19}\\text{K}$ 之原子半徑，其大小順序何者正確？",
        "options": [
            "(A) $\\text{K} > \\text{Na} > \\text{Cl} > \\text{F}$",
            "(B) $\\text{Na} > \\text{K} > \\text{F} > \\text{Cl}$",
            "(C) $\\text{Cl} > \\text{F} > \\text{K} > \\text{Na}$",
            "(D) $\\text{K} > \\text{Cl} > \\text{Na} > \\text{F}$"
        ],
        "ans": 0,
        "explanation": "<strong>解析：</strong><br>• <strong>第一原則（電子層數 $n$）：</strong>電子層數愈多者，半徑通常具有壓倒性優勢。<br>&nbsp;&nbsp;- K（第四週期 IA 族，4 層電子，約 227 pm）<br>&nbsp;&nbsp;- Na（第三週期 IA 族，3 層電子，約 186 pm）<br>&nbsp;&nbsp;- Cl（第三週期 VIIA 族，3 層電子，約 99 pm）<br>&nbsp;&nbsp;- F（第二週期 VIIA 族，2 層電子，約 72 pm）<br>• <strong>第二原則（同週期由左至右遞減）：</strong>Na 與 Cl 同在第三週期，IA 族的 Na 位於最左側，有效核電荷小，半徑（186 pm）遠大於右側 VIIA 族的 Cl（99 pm）。<br>• <strong>綜合順序：</strong>$\\text{K} > \\text{Na} > \\text{Cl} > \\text{F}$。<br>故選 <strong>(A)</strong>。"
    }
]

with open('question_bank.json', 'w', encoding='utf-8') as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

print(f"Successfully generated question_bank.json with {len(questions)} questions!")
