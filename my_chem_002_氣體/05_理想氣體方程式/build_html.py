import re
import os

target_dir = r'c:\Users\julsh\OneDrive - 國立新化高級工業職業學校\玩具檔案\my_化學網\my_chem_002_氣體\05_理想氣體方程式'
template_file = r'c:\Users\julsh\OneDrive - 國立新化高級工業職業學校\玩具檔案\my_化學網\my_chem_002_氣體\04_亞佛加厥定律\index.html'

with open(template_file, 'r', encoding='utf-8') as f:
    template = f.read()

# The new HTML content
new_slides = r'''                <!-- Slide 1: Equation -->
                <div class="slide">
                    <h1>理想氣體方程式</h1>
                    <div class="flex-row">
                        <div class="flex-col">
                            <h2 class="text-yellow">公式推導</h2>
                            <p>結合波以耳、查理與亞佛加厥定律：</p>
                            <div class="formula-box" style="font-size: 2.5rem; padding: 2rem;">
                                $PV = nRT$
                            </div>
                            <p>其中 <strong class="text-red">R</strong> 為氣體常數。</p>
                        </div>
                        <div class="flex-col">
                            <h2 class="text-yellow">氣體常數 $R$ 的數值</h2>
                            <ul class="rule-card" style="list-style: none; margin-left: 0;">
                                <li>✅ $0.082 \text{ atm}\cdot\text{L} / \text{mol}\cdot\text{K}$</li>
                                <li>✅ $8.314 \text{ J} / \text{mol}\cdot\text{K} \text{ (SI 單位)}$</li>
                                <li>✅ $62.4 \text{ mmHg}\cdot\text{L} / \text{mol}\cdot\text{K}$</li>
                            </ul>
                            <div class="rule-card" style="margin-top: 1.5rem; border-color: var(--accent-cyan);">
                                <p><strong class="text-cyan">注意單位匹配：</strong></p>
                                <p>若 $R=0.082$，則 $P$ 必為 atm，$V$ 必為 L，$T$ 必為 K。</p>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Slide 2: Molecular Weight & Density -->
                <div class="slide">
                    <h1>分子量與密度的求法</h1>
                    <div class="flex-row">
                        <div class="flex-col">
                            <h2 class="text-yellow">分子量 (M) 求法</h2>
                            <p>將 $n = W/M$ 代入 $PV = nRT$：</p>
                            <div class="formula-box">
                                $M = \frac{W \cdot R \cdot T}{P \cdot V}$
                            </div>
                        </div>
                        <div class="flex-col">
                            <h2 class="text-yellow">密度 (d) 求法</h2>
                            <p>由 $PM = \frac{W}{V}RT = dRT$ 得：</p>
                            <div class="formula-box" style="border-left-color: var(--accent-cyan);">
                                $d = \frac{PM}{RT} \quad \text{或} \quad M = \frac{dRT}{P}$
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Slide 3: Ideal vs Real -->
                <div class="slide">
                    <h1>理想氣體與真實氣體</h1>
                    <div class="flex-row">
                        <div class="flex-col">
                            <h2 class="text-yellow">理想氣體假說</h2>
                            <ul class="rule-card" style="margin-left: 1.5rem;">
                                <li>分子本身 <strong class="text-red">無體積</strong>。</li>
                                <li>分子間 <strong class="text-red">無作用力</strong>。</li>
                                <li>碰撞為 <strong class="text-cyan">完全彈性碰撞</strong>。</li>
                                <li>符合 $PV = nRT$。</li>
                            </ul>
                        </div>
                        <div class="flex-col">
                            <h2 class="text-green">真實氣體趨近理想的條件</h2>
                            <div class="rule-card" style="background: rgba(52, 211, 153, 0.1); border-color: var(--accent-green);">
                                <h3 style="text-align: center; margin-bottom: 1rem;" class="text-green">高溫、低壓</h3>
                                <p>此時分子動能大、距離遠，作用力與體積影響最小。</p>
                            </div>
                            <p style="font-size: 1rem; margin-top: 1rem; opacity: 0.8;">* 極低溫或極高壓時，真實氣體會液化或固化，不再符合方程式。</p>
                        </div>
                    </div>
                </div>

                <!-- Slide 4: Examples -->
                <div class="slide">
                    <h1>範例題</h1>

                    <!-- Ex 1 -->
                    <div class="ex-split-row">
                        <div class="ex-left">
                            <h2 class="text-yellow">範例 1</h2>
                            <p>某氣體在 STP 下的密度為 $1.43 \text{ g/L}$，請問其分子量約為多少？</p>
                            <button class="btn-show-ans" data-ans="ex-ans-1">顯示解答</button>
                        </div>
                        <div class="ex-right">
                            <div id="ex-ans-1" class="ex-answer-box">
                                <div class="ans-label">解答：32 g/mol</div>
                                <div class="ans-body">
                                    $M = dRT/P$<br>
                                    STP 下 $d = 1.43 \text{ g/L}$<br>
                                    $M = 1.43 \times 22.4 \approx 32$<br>
                                    (此氣體為氧氣 $O_2$)
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Ex 2 -->
                    <div class="ex-split-row">
                        <div class="ex-left">
                            <h2 class="text-yellow">範例 2</h2>
                            <p>真實氣體在何種環境條件下，其性質最接近理想氣體？</p>
                            <button class="btn-show-ans" data-ans="ex-ans-2">顯示解答</button>
                        </div>
                        <div class="ex-right">
                            <div id="ex-ans-2" class="ex-answer-box">
                                <div class="ans-label">解答：低壓高溫</div>
                                <div class="ans-body">
                                    低壓：分子距離遠，引力忽略。<br>
                                    高溫：分子運動快，引力忽略。
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Ex 3 -->
                    <div class="ex-split-row">
                        <div class="ex-left">
                            <h2 class="text-yellow">範例 3</h2>
                            <p>當 $1$ 大氣壓、$27^\circ\text{C}$ 下，將 $80$ 克某液體放入一個 $10.0$ 升的容器後密封。當加熱至 $127^\circ\text{C}$ 時，該密封容器內的壓力為 $9.53$ 大氣壓，假設在 $27^\circ\text{C}$ 時該液體之蒸氣可忽略，在 $127^\circ\text{C}$ 時該液體完全汽化；則該液體分子量為何？</p>
                            <ul class="ex-options">
                                <li>(A) 28</li>
                                <li>(B) 32</li>
                                <li>(C) 46</li>
                                <li>(D) 64</li>
                            </ul>
                            <div style="display: flex; justify-content: flex-start; gap: 2rem; margin-top: 1.5rem;">
                                <svg width="160" height="224" viewBox="0 0 100 140">
                                    <rect x="10" y="10" width="80" height="100" rx="15" fill="transparent" stroke="var(--accent-blue)" stroke-width="3"/>
                                    <path d="M 12 100 Q 20 90, 30 95 T 50 95 T 70 95 T 88 100 L 88 105 A 15 15 0 0 1 73 110 L 27 110 A 15 15 0 0 1 12 105 Z" fill="var(--accent-red)"/>
                                    <text x="50" y="102" fill="white" font-size="10" text-anchor="middle">液體</text>
                                    <text x="50" y="130" fill="var(--text-main)" font-size="14" text-anchor="middle">27°C</text>
                                </svg>
                                <svg width="160" height="224" viewBox="0 0 100 140">
                                    <rect x="10" y="10" width="80" height="100" rx="15" fill="transparent" stroke="var(--accent-blue)" stroke-width="3"/>
                                    <circle cx="20" cy="30" r="1.5" fill="var(--accent-red)"/><circle cx="40" cy="20" r="1.5" fill="var(--accent-red)"/><circle cx="70" cy="40" r="1.5" fill="var(--accent-red)"/><circle cx="80" cy="25" r="1.5" fill="var(--accent-red)"/><circle cx="30" cy="60" r="1.5" fill="var(--accent-red)"/><circle cx="60" cy="70" r="1.5" fill="var(--accent-red)"/><circle cx="40" cy="90" r="1.5" fill="var(--accent-red)"/><circle cx="25" cy="80" r="1.5" fill="var(--accent-red)"/><circle cx="75" cy="85" r="1.5" fill="var(--accent-red)"/><circle cx="50" cy="50" r="1.5" fill="var(--accent-red)"/><circle cx="80" cy="60" r="1.5" fill="var(--accent-red)"/>
                                    <text x="50" y="130" fill="var(--text-main)" font-size="14" text-anchor="middle">127°C 完全汽化</text>
                                </svg>
                            </div>
                            <button class="btn-show-ans" data-ans="ex-ans-3">顯示解答</button>
                        </div>
                        <div class="ex-right">
                            <div id="ex-ans-3" class="ex-answer-box">
                                <div class="ans-label">解答：(B)</div>
                                <div class="ans-body">
                                    1. 容器內原來有 1 大氣壓的空氣。<br>
                                    2. 加熱至 $127^\circ\text{C}$ (400 K) 時，空氣的壓力 $P_{\text{air}} = 1 \times \frac{400}{300} = 1.33 \text{ atm}$<br>
                                    3. 該液體完全汽化後的總壓為 $9.53 \text{ atm}$，故氣體蒸氣壓 $P_{\text{gas}} = 9.53 - 1.33 = 8.20 \text{ atm}$<br>
                                    4. 由 $PV = \frac{W}{M}RT$：<br>
                                    $8.20 \times 10.0 = \frac{80}{M} \times 0.082 \times 400$<br>
                                    $82 = \frac{80}{M} \times 32.8 \Rightarrow M = \frac{80 \times 32.8}{82} = \boxed{32 \text{ g/mol}}$
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Ex 4 -->
                    <div class="ex-split-row">
                        <div class="ex-left">
                            <h2 class="text-yellow">範例 4</h2>
                            <p>甲、乙兩容器以活門連接，甲容積 $50\text{ mL}$ 充入 $\text{He}_{(g)}$ 壓力為 $108\text{ mmHg}$，溫度 $27^\circ\text{C}$，乙為真空容器維持 $327^\circ\text{C}$，打開活門使 $\text{He}_{(g)}$ 擴散至乙而二容器溫度各保持不變，達壓力平衡時關閉活門，測得甲中壓力 $36\text{ mmHg}$，則乙容器的容積為：</p>
                            <ul class="ex-options">
                                <li>(A) $200\text{ mL}$</li>
                                <li>(B) $150\text{ mL}$</li>
                                <li>(C) $100\text{ mL}$</li>
                                <li>(D) $80\text{ mL}$</li>
                            </ul>
                            <div style="display: flex; justify-content: flex-start; gap: 2rem; margin-top: 1.5rem;">
                                <div style="text-align: center;">
                                    <div style="color: var(--accent-purple); font-weight: bold; margin-bottom: 5px; font-size: 1.5rem;">前</div>
                                    <svg width="200" height="140" viewBox="0 0 250 170">
                                        <circle cx="50" cy="75" r="40" fill="transparent" stroke="var(--accent-blue)" stroke-width="2"/>
                                        <text x="50" y="50" fill="var(--text-main)" font-size="16" text-anchor="middle">50 mL</text>
                                        <text x="50" y="75" fill="var(--text-main)" font-size="16" text-anchor="middle">27°C</text>
                                        <text x="50" y="100" fill="var(--text-main)" font-size="16" text-anchor="middle">108 mmHg</text>
                                        <text x="50" y="135" fill="var(--accent-purple)" font-size="20" text-anchor="middle">甲</text>
                                        
                                        <rect x="90" y="70" width="30" height="10" fill="transparent" stroke="var(--accent-blue)" stroke-width="2"/>
                                        <line x1="105" y1="65" x2="105" y2="85" stroke="var(--accent-blue)" stroke-width="3"/>
                                        
                                        <circle cx="180" cy="75" r="60" fill="transparent" stroke="var(--accent-blue)" stroke-width="2"/>
                                        <text x="180" y="50" fill="var(--text-main)" font-size="16" text-anchor="middle">V₂ mL</text>
                                        <text x="180" y="75" fill="var(--text-main)" font-size="16" text-anchor="middle">327°C</text>
                                        <text x="180" y="100" fill="var(--text-main)" font-size="16" text-anchor="middle">真空</text>
                                        <text x="180" y="155" fill="var(--accent-purple)" font-size="20" text-anchor="middle">乙</text>
                                    </svg>
                                </div>
                                <div style="text-align: center;">
                                    <div style="color: var(--accent-purple); font-weight: bold; margin-bottom: 5px; font-size: 1.5rem;">後</div>
                                    <svg width="200" height="140" viewBox="0 0 250 170">
                                        <circle cx="50" cy="75" r="40" fill="transparent" stroke="var(--accent-blue)" stroke-width="2"/>
                                        <circle cx="30" cy="70" r="1.5" fill="var(--accent-green)"/><circle cx="45" cy="55" r="1.5" fill="var(--accent-green)"/><circle cx="60" cy="80" r="1.5" fill="var(--accent-green)"/><circle cx="50" cy="95" r="1.5" fill="var(--accent-green)"/><circle cx="70" cy="65" r="1.5" fill="var(--accent-green)"/>
                                        <text x="50" y="135" fill="var(--accent-purple)" font-size="18" text-anchor="middle">甲 (36 mmHg)</text>
                                        
                                        <rect x="90" y="70" width="30" height="10" fill="transparent" stroke="var(--accent-blue)" stroke-width="2"/>
                                        
                                        <circle cx="180" cy="75" r="60" fill="transparent" stroke="var(--accent-blue)" stroke-width="2"/>
                                        <circle cx="150" cy="60" r="1.5" fill="var(--accent-green)"/><circle cx="170" cy="50" r="1.5" fill="var(--accent-green)"/><circle cx="200" cy="70" r="1.5" fill="var(--accent-green)"/><circle cx="180" cy="100" r="1.5" fill="var(--accent-green)"/><circle cx="160" cy="90" r="1.5" fill="var(--accent-green)"/><circle cx="210" cy="90" r="1.5" fill="var(--accent-green)"/>
                                        <text x="180" y="155" fill="var(--accent-purple)" font-size="18" text-anchor="middle">乙 (36 mmHg)</text>
                                    </svg>
                                </div>
                            </div>
                            <button class="btn-show-ans" data-ans="ex-ans-4">顯示解答</button>
                        </div>
                        <div class="ex-right">
                            <div id="ex-ans-4" class="ex-answer-box">
                                <div class="ans-label">解答：(A)</div>
                                <div class="ans-body">
                                    利用莫耳數守恆：$n_{\text{初}} = n_{\text{末}} \Rightarrow \frac{P_{\text{甲初}}V_{\text{甲}}}{T_{\text{甲}}} + 0 = \frac{P_{\text{末}}V_{\text{甲}}}{T_{\text{甲}}} + \frac{P_{\text{末}}V_{\text{乙}}}{T_{\text{乙}}}$<br>
                                    代入數值：$\frac{108 \times 50}{300} = \frac{36 \times 50}{300} + \frac{36 \times V_{\text{乙}}}{600}$<br>
                                    $18 = 6 + \frac{36 V_{\text{乙}}}{600}$<br>
                                    $12 = \frac{36 V_{\text{乙}}}{600} \Rightarrow V_{\text{乙}} = \frac{12 \times 600}{36} = \boxed{200 \text{ mL}}$
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Ex 5 -->
                    <div class="ex-split-row">
                        <div class="ex-left">
                            <h2 class="text-yellow">範例 5</h2>
                            <p>兩個等體積燒瓶用細管相連接（體積省略）初在 $27^\circ\text{C}$ 下置入 $0.70\text{ mol } \text{H}_2$ 壓力為 $0.5\text{ atm}$。今 $V_1$ 改置入 $127^\circ\text{C}$ 沸油中，而 $V_2$ 仍然 $27^\circ\text{C}$ 而最後達至平衡，求最後壓力為若干？</p>
                            <ul class="ex-options">
                                <li>(A) $0.3\text{ atm}$</li>
                                <li>(B) $0.4\text{ atm}$</li>
                                <li>(C) $0.5\text{ atm}$</li>
                                <li>(D) $0.57\text{ atm}$</li>
                            </ul>
                            <div style="display: flex; justify-content: flex-start; margin-top: 1.5rem;">
                                <svg width="240" height="120" viewBox="0 0 300 150">
                                    <rect x="20" y="40" width="100" height="80" fill="rgba(255,255,255,0.1)" stroke="var(--text-main)" stroke-width="2"/>
                                    <text x="70" y="140" fill="var(--text-main)" font-size="14" text-anchor="middle">127°C 沸油</text>
                                    
                                    <circle cx="70" cy="80" r="30" fill="transparent" stroke="var(--accent-blue)" stroke-width="2"/>
                                    <text x="70" y="85" fill="var(--text-main)" font-size="16" text-anchor="middle">V₁</text>
                                    
                                    <path d="M 70 50 L 70 20 L 220 20 L 220 50" fill="transparent" stroke="var(--accent-blue)" stroke-width="6"/>
                                    <path d="M 70 50 L 70 20 L 220 20 L 220 50" fill="transparent" stroke="var(--bg-dark)" stroke-width="2"/>
                                    
                                    <circle cx="220" cy="80" r="30" fill="transparent" stroke="var(--accent-blue)" stroke-width="2"/>
                                    <text x="220" y="85" fill="var(--text-main)" font-size="16" text-anchor="middle">V₂</text>
                                    <text x="220" y="140" fill="var(--text-main)" font-size="14" text-anchor="middle">27°C</text>
                                </svg>
                            </div>
                            <button class="btn-show-ans" data-ans="ex-ans-5">顯示解答</button>
                        </div>
                        <div class="ex-right">
                            <div id="ex-ans-5" class="ex-answer-box">
                                <div class="ans-label">解答：(D)</div>
                                <div class="ans-body">
                                    1. 原本總莫耳數：$n = \frac{0.5 \times (2V)}{R \times 300} = 0.70$<br>
                                    2. 後來：兩邊莫耳數相加等於總莫耳數 $n = n_1 + n_2$<br>
                                    $\frac{0.5 \times 2V}{R \times 300} = \frac{P' \times V}{R \times 400} + \frac{P' \times V}{R \times 300}$<br>
                                    約去 $\frac{V}{R}$：$\frac{1}{300} = P'(\frac{1}{400} + \frac{1}{300}) = P'(\frac{3+4}{1200}) = P' \times \frac{7}{1200}$<br>
                                    $P' = \frac{1}{300} \times \frac{1200}{7} = \frac{4}{7} \approx \boxed{0.57 \text{ atm}}$
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Ex 6 -->
                    <div class="ex-split-row">
                        <div class="ex-left">
                            <h2 class="text-yellow">範例 6</h2>
                            <p>$\text{N}_2\text{O}_4$ 分解之反應為 $\text{N}_2\text{O}_{4(g)} \rightleftharpoons 2\text{NO}_{2(g)}$ 在 $25^\circ\text{C}$ 及 $1\text{ atm}$ 下，平衡系中混合氣體之密度為 $3.13\text{ g/L}$，則 $\text{N}_2\text{O}_4$ 之分解百分率約為：</p>
                            <ul class="ex-options">
                                <li>(A) 20%</li>
                                <li>(B) 30%</li>
                                <li>(C) 40%</li>
                                <li>(D) 50%</li>
                            </ul>
                            <button class="btn-show-ans" data-ans="ex-ans-6">顯示解答</button>
                        </div>
                        <div class="ex-right" style="justify-content: flex-start;">
                            <div style="width: 100%; text-align: center; margin-bottom: 2rem; color: var(--accent-yellow); font-size: 1.8rem; font-weight: bold; background: rgba(0,0,0,0.3); padding: 1rem; border-radius: 10px; border: 1px solid var(--accent-blue);">
                                $\text{N}_2\text{O}_{4(g)} \rightleftharpoons 2\text{NO}_{2(g)}$
                            </div>
                            <div id="ex-ans-6" class="ex-answer-box">
                                <div class="ans-label">解答：(A)</div>
                                <div class="ans-body">
                                    1. 混合氣體的平均分子量 $\bar{M} = \frac{dRT}{P} = \frac{3.13 \times 0.082 \times 298}{1} = 76.5$<br>
                                    2. $\text{N}_2\text{O}_4$ 的分子量為 $92$。<br>
                                    3. 設分解率為 $\alpha$，則：<br>
                                    $\text{N}_2\text{O}_4 \rightleftharpoons 2\text{NO}_2$<br>
                                    $1-\alpha \quad\quad 2\alpha$<br>
                                    總莫耳數 $= 1 + \alpha$<br>
                                    4. 質量守恆，平均分子量 $\bar{M} = \frac{\text{總質量}}{\text{總莫耳數}} = \frac{92}{1+\alpha}$<br>
                                    $76.5 = \frac{92}{1+\alpha} \Rightarrow 1+\alpha = \frac{92}{76.5} \approx 1.20$<br>
                                    $\alpha = 0.20 = \boxed{20\%}$
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Game -->
                <div class="slide" id="slide-game">
                    <h1>單元挑戰：理想氣體連連看</h1>
                    <p style="text-align: center; color: var(--accent-green); margin-bottom: 1rem;">請連接正確的描述與數值。</p>
                    <div id="game-container" style="position: relative; flex: 1; display: flex; justify-content: space-between; padding: 20px 40px; background: rgba(0,0,0,0.2); border-radius: 20px; min-height: 400px; touch-action: none;">
                        <svg id="game-svg" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 5;"></svg>
                        <div id="left-column" style="display: flex; flex-direction: column; justify-content: space-around; gap: 8px; z-index: 10; width: 40%;"></div>
                        <div id="right-column" style="display: flex; flex-direction: column; justify-content: space-around; gap: 8px; z-index: 10; width: 40%;"></div>
                        <div id="game-feedback" style="display: none; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); background: rgba(16, 185, 129, 0.95); padding: 2rem 4rem; border-radius: 20px; font-size: 2.5rem; color: white; font-weight: bold; box-shadow: 0 0 50px rgba(16, 185, 129, 0.5); z-index: 100; text-align: center;">🎉 太棒了！</div>
                    </div>
                    <div style="text-align: center; margin-top: 15px;">
                        <button class="btn-tool primary" style="width: auto; padding: 8px 30px;" onclick="resetGame()">再玩一次</button>
                    </div>
                </div>'''

new_game_data = r'''
            const gameDataPool = [
                { left: '理想氣體方程式', right: '$PV = nRT$', match: 0 },
                { left: '氣體常數 $R$ (atm)', right: '0.082', match: 1 },
                { left: '氣體常數 $R$ (SI)', right: '8.314', match: 2 },
                { left: '理想氣體條件', right: '分子無體積、無引力', match: 3 },
                { left: '最接近理想狀態', right: '高溫、低壓', match: 4 },
                { left: '分子量求法公式', right: '$M = dRT/P$', match: 5 },
                { left: '真實氣體體積', right: '大於容器體積（分子有體積）', match: 6 },
                { left: '真實氣體壓力', right: '小於理想氣體壓力（有引力）', match: 7 },
                { left: '同溫同壓同體積', right: '莫耳數相同（亞佛加厥）', match: 8 }
            ];
'''

out = template
out = re.sub(r'<title>.*?</title>', '<title>理想氣體方程式 - 互動教學</title>', out)
out = re.sub(r'<h1>亞佛加厥定律</h1>', '<h1>理想氣體方程式</h1>', out)
out = re.sub(r'<p style="color: rgba\(255,255,255,0\.7\);.*?氣體體積與莫耳數的關係</p>', 
             '<p style="color: rgba(255,255,255,0.7); font-size: clamp(1.2rem, 3vw, 1.5rem); margin-bottom: 3rem; text-align: center;">$PV = nRT$ 的應用與探討</p>', out)

out = re.sub(r'<div id="slides-container">.*?</div>\s*<canvas id="drawing-layer">', 
             lambda m: f'<div id="slides-container">\n{new_slides}\n            </div>\n            <canvas id="drawing-layer">', 
             out, flags=re.DOTALL)

out = re.sub(r'const gameDataPool = \[.*?\];', lambda m: new_game_data.strip(), out, flags=re.DOTALL)

with open(os.path.join(target_dir, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(out)

print("Done")
