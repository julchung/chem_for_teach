/* =========================================================
   data.js  ─  氧化還原平衡化學資料庫
   ========================================================= */

/* ── 物種資料庫 ──────────────────────────────────────────
   每個物種的屬性：
   · htmlParts  : 渲染化學式所需的零件陣列
     type: "key"  → 氧化數有變化的關鍵原子（標示 ID 用於 SVG 連線）
           "txt"  → 普通文字
           "sub"  → 下標
           "sup"  → 上標
   · oxNum      : 關鍵原子的氧化數
   · keyCount   : 每個化學式中關鍵原子的個數（Cr₂O₇²⁻ 是 2）
   · charge     : 離子整體電荷
   · state      : 狀態符號
   · H, O       : 每個化學式中 H 和 O 的個數（步驟四用）
   ─────────────────────────────────────────────────────── */
const SPECIES = {

  /* ── 氧化劑本體 ── */
  "MnO4": {
    name: "高錳酸根離子",
    htmlParts: [
      { type:"key", text:"Mn" },
      { type:"txt", text:"O" }, { type:"sub", text:"4" },
      { type:"sup", text:"−" }
    ],
    oxNum: 7, keyCount: 1, charge: -1, state:"(aq)", H:0, O:4
  },
  "Cr2O7": {
    name: "重鉻酸根離子",
    htmlParts: [
      { type:"key", text:"Cr" }, { type:"sub", text:"2" },
      { type:"txt", text:"O" }, { type:"sub", text:"7" },
      { type:"sup", text:"2−" }
    ],
    oxNum: 6, keyCount: 2, charge: -2, state:"(aq)", H:0, O:7
  },
  "Cl2": {
    name: "氯氣",
    htmlParts: [
      { type:"key", text:"Cl" }, { type:"sub", text:"2" }
    ],
    oxNum: 0, keyCount: 2, charge: 0, state:"(aq)", H:0, O:0
  },
  "Fe3ox": {   /* Fe³⁺ 作為氧化劑 */
    name: "鐵(III)離子",
    htmlParts: [
      { type:"key", text:"Fe" }, { type:"sup", text:"3+" }
    ],
    oxNum: 3, keyCount: 1, charge: 3, state:"(aq)", H:0, O:0
  },
  "H2O2": {
    name: "雙氧水",
    htmlParts: [
      { type:"txt", text:"H" }, { type:"sub", text:"2" },
      { type:"key", text:"O" }, { type:"sub", text:"2" }
    ],
    oxNum: -1, keyCount: 2, charge: 0, state:"(aq)", H:2, O:2
  },
  "NO3-": {
    name: "硝酸根離子",
    htmlParts: [
      { type:"key", text:"N" },
      { type:"txt", text:"O" }, { type:"sub", text:"3" },
      { type:"sup", text:"−" }
    ],
    oxNum: 5, keyCount: 1, charge: -1, state:"(aq)", H:0, O:3
  },
  "Hplus": {
    name: "氫離子",
    htmlParts: [
      { type:"key", text:"H" }, { type:"sup", text:"+" }
    ],
    oxNum: 1, keyCount: 1, charge: 1, state:"(aq)", H:1, O:0
  },
  "H2O_ox": {
    name: "水",
    htmlParts: [
      { type:"key", text:"H" }, { type:"sub", text:"2" },
      { type:"txt", text:"O" }
    ],
    oxNum: 1, keyCount: 2, charge: 0, state:"(l)", H:2, O:1
  },

  /* ── 氧化劑的共軛產物（還原後） ── */
  "Mn2": {
    name: "錳(II)離子",
    htmlParts: [
      { type:"key", text:"Mn" }, { type:"sup", text:"2+" }
    ],
    oxNum: 2, keyCount: 1, charge: 2, state:"(aq)", H:0, O:0
  },
  "MnO2": {
    name: "二氧化錳",
    htmlParts: [
      { type:"key", text:"Mn" },
      { type:"txt", text:"O" }, { type:"sub", text:"2" }
    ],
    oxNum: 4, keyCount: 1, charge: 0, state:"(s)", H:0, O:2
  },
  "MnO4_2-": {
    name: "錳酸根離子",
    htmlParts: [
      { type:"key", text:"Mn" },
      { type:"txt", text:"O" }, { type:"sub", text:"4" },
      { type:"sup", text:"2−" }
    ],
    oxNum: 6, keyCount: 1, charge: -2, state:"(aq)", H:0, O:4
  },
  "Mn2O3": {
    name: "三氧化二錳",
    htmlParts: [
      { type:"key", text:"Mn" }, { type:"sub", text:"2" },
      { type:"txt", text:"O" }, { type:"sub", text:"3" }
    ],
    oxNum: 3, keyCount: 2, charge: 0, state:"(s)", H:0, O:3
  },
  "Cr3": {
    name: "鉻(III)離子",
    htmlParts: [
      { type:"key", text:"Cr" }, { type:"sup", text:"3+" }
    ],
    oxNum: 3, keyCount: 1, charge: 3, state:"(aq)", H:0, O:0
  },
  "Cl-": {
    name: "氯離子",
    htmlParts: [
      { type:"key", text:"Cl" }, { type:"sup", text:"−" }
    ],
    oxNum: -1, keyCount: 1, charge: -1, state:"(aq)", H:0, O:0
  },
  "Fe2prod": {   /* Fe³⁺ 被還原成 Fe²⁺ */
    name: "亞鐵離子",
    htmlParts: [
      { type:"key", text:"Fe" }, { type:"sup", text:"2+" }
    ],
    oxNum: 2, keyCount: 1, charge: 2, state:"(aq)", H:0, O:0
  },
  "H2O_prod": {
    name: "水",
    htmlParts: [
      { type:"txt", text:"H" }, { type:"sub", text:"2" },
      { type:"key", text:"O" }
    ],
    oxNum: -2, keyCount: 1, charge: 0, state:"(l)", H:2, O:1
  },
  "NO2": {
    name: "二氧化氮",
    htmlParts: [
      { type:"key", text:"N" },
      { type:"txt", text:"O" }, { type:"sub", text:"2" }
    ],
    oxNum: 4, keyCount: 1, charge: 0, state:"(g)", H:0, O:2
  },
  "NO": {
    name: "一氧化氮",
    htmlParts: [
      { type:"key", text:"N" }, { type:"txt", text:"O" }
    ],
    oxNum: 2, keyCount: 1, charge: 0, state:"(g)", H:0, O:1
  },
  "H2": {
    name: "氫氣",
    htmlParts: [
      { type:"key", text:"H" }, { type:"sub", text:"2" }
    ],
    oxNum: 0, keyCount: 2, charge: 0, state:"(g)", H:2, O:0
  },

  /* ── 還原劑本體 ── */
  "Fe2": {
    name: "亞鐵離子",
    htmlParts: [
      { type:"key", text:"Fe" }, { type:"sup", text:"2+" }
    ],
    oxNum: 2, keyCount: 1, charge: 2, state:"(aq)", H:0, O:0
  },
  "I-": {
    name: "碘離子",
    htmlParts: [
      { type:"key", text:"I" }, { type:"sup", text:"−" }
    ],
    oxNum: -1, keyCount: 1, charge: -1, state:"(aq)", H:0, O:0
  },
  "Sn2": {
    name: "錫(II)離子",
    htmlParts: [
      { type:"key", text:"Sn" }, { type:"sup", text:"2+" }
    ],
    oxNum: 2, keyCount: 1, charge: 2, state:"(aq)", H:0, O:0
  },
  "Br-": {
    name: "溴離子",
    htmlParts: [
      { type:"key", text:"Br" }, { type:"sup", text:"−" }
    ],
    oxNum: -1, keyCount: 1, charge: -1, state:"(aq)", H:0, O:0
  },
  "C2O4": {
    name: "草酸根離子",
    htmlParts: [
      { type:"key", text:"C" }, { type:"sub", text:"2" },
      { type:"txt", text:"O" }, { type:"sub", text:"4" },
      { type:"sup", text:"2−" }
    ],
    oxNum: 3, keyCount: 2, charge: -2, state:"(aq)", H:0, O:4
  },
  "S2O3": {
    name: "硫代硫酸根離子",
    htmlParts: [
      { type:"key", text:"S" }, { type:"sub", text:"2" },
      { type:"txt", text:"O" }, { type:"sub", text:"3" },
      { type:"sup", text:"2−" }
    ],
    oxNum: 2, keyCount: 2, charge: -2, state:"(aq)", H:0, O:3
  },
  "Cu": {
    name: "金屬銅",
    htmlParts: [ { type:"key", text:"Cu" } ],
    oxNum: 0, keyCount: 1, charge: 0, state:"(s)", H:0, O:0
  },
  "HSO3-": {
    name: "亞硫酸氫根離子",
    htmlParts: [
      { type:"txt", text:"H" },
      { type:"key", text:"S" },
      { type:"txt", text:"O" }, { type:"sub", text:"3" },
      { type:"sup", text:"−" }
    ],
    oxNum: 4, keyCount: 1, charge: -1, state:"(aq)", H:1, O:3
  },
  "Al": {
    name: "金屬鋁",
    htmlParts: [ { type:"key", text:"Al" } ],
    oxNum: 0, keyCount: 1, charge: 0, state:"(s)", H:0, O:0
  },

  /* ── 還原劑的共軛產物（氧化後） ── */
  "Fe3": {
    name: "鐵(III)離子",
    htmlParts: [
      { type:"key", text:"Fe" }, { type:"sup", text:"3+" }
    ],
    oxNum: 3, keyCount: 1, charge: 3, state:"(aq)", H:0, O:0
  },
  "I2": {
    name: "碘分子",
    htmlParts: [
      { type:"key", text:"I" }, { type:"sub", text:"2" }
    ],
    oxNum: 0, keyCount: 2, charge: 0, state:"(aq)", H:0, O:0
  },
  "Sn4": {
    name: "錫(IV)離子",
    htmlParts: [
      { type:"key", text:"Sn" }, { type:"sup", text:"4+" }
    ],
    oxNum: 4, keyCount: 1, charge: 4, state:"(aq)", H:0, O:0
  },
  "Br2": {
    name: "溴分子",
    htmlParts: [
      { type:"key", text:"Br" }, { type:"sub", text:"2" }
    ],
    oxNum: 0, keyCount: 2, charge: 0, state:"(aq)", H:0, O:0
  },
  "CO2": {
    name: "二氧化碳",
    htmlParts: [
      { type:"key", text:"C" },
      { type:"txt", text:"O" }, { type:"sub", text:"2" }
    ],
    oxNum: 4, keyCount: 1, charge: 0, state:"(g)", H:0, O:2
  },
  "IO3-": {
    name: "碘酸根離子",
    htmlParts: [
      { type:"key", text:"I" },
      { type:"txt", text:"O" }, { type:"sub", text:"3" },
      { type:"sup", text:"−" }
    ],
    oxNum: 5, keyCount: 1, charge: -1, state:"(aq)", H:0, O:3
  },
  "S4O6": {
    name: "連四硫酸根離子",
    htmlParts: [
      { type:"key", text:"S" }, { type:"sub", text:"4" },
      { type:"txt", text:"O" }, { type:"sub", text:"6" },
      { type:"sup", text:"2−" }
    ],
    oxNum: 2.5, keyCount: 4, charge: -2, state:"(aq)", H:0, O:6
  },
  "SO4": {
    name: "硫酸根離子",
    htmlParts: [
      { type:"key", text:"S" },
      { type:"txt", text:"O" }, { type:"sub", text:"4" },
      { type:"sup", text:"2−" }
    ],
    oxNum: 6, keyCount: 1, charge: -2, state:"(aq)", H:0, O:4
  },
  "O2": {
    name: "氧氣",
    htmlParts: [
      { type:"key", text:"O" }, { type:"sub", text:"2" }
    ],
    oxNum: 0, keyCount: 2, charge: 0, state:"(g)", H:0, O:2
  },
  "Cu2+": {
    name: "銅(II)離子",
    htmlParts: [
      { type:"key", text:"Cu" }, { type:"sup", text:"2+" }
    ],
    oxNum: 2, keyCount: 1, charge: 2, state:"(aq)", H:0, O:0
  },
  "Al3": {
    name: "鋁離子",
    htmlParts: [
      { type:"key", text:"Al" }, { type:"sup", text:"3+" }
    ],
    oxNum: 3, keyCount: 1, charge: 3, state:"(aq)", H:0, O:0
  },
  "AlOH4": {
    name: "四羥基合鋁酸根",
    htmlParts: [
      { type:"key", text:"Al" },
      { type:"txt", text:"(" }, { type:"txt", text:"OH" }, { type:"txt", text:")" }, { type:"sub", text:"4" },
      { type:"sup", text:"−" }
    ],
    oxNum: 3, keyCount: 1, charge: -1, state:"(aq)", H:4, O:4
  }
};

/* ── 左側面板：反應物清單 (分為氧化劑與還原劑區塊) ─────────────────────────────── */
const OXIDIZERS_LIST = [
  { id: "MnO4",  formulaHTML: "MnO<sub>4</sub><sup>−</sup>", name: "高錳酸根離子", compound: "KMnO₄" },
  { id: "Cr2O7", formulaHTML: "Cr<sub>2</sub>O<sub>7</sub><sup>2−</sup>", name: "重鉻酸根離子", compound: "K₂Cr₂O₇" },
  { id: "Cl2",   formulaHTML: "Cl<sub>2</sub>", name: "氯氣", compound: "Cl₂" },
  { id: "Br2",   formulaHTML: "Br<sub>2</sub>", name: "溴水", compound: "Br₂" },
  { id: "Fe3ox", formulaHTML: "Fe<sup>3+</sup>", name: "鐵(III)離子", compound: "FeCl₃" },
  { id: "IO3-",  formulaHTML: "IO<sub>3</sub><sup>−</sup>", name: "碘酸根", compound: "KIO₃" },
  { id: "H2O2",  formulaHTML: "H<sub>2</sub>O<sub>2</sub>", name: "雙氧水", compound: "H₂O₂" },
  { id: "NO3-",  formulaHTML: "NO<sub>3</sub><sup>−</sup>", name: "硝酸根離子", compound: "HNO₃" },
  { id: "Hplus", formulaHTML: "H<sup>+</sup>", name: "氫離子", compound: "H⁺" },
  { id: "H2O_ox", formulaHTML: "H<sub>2</sub>O", name: "水", compound: "H₂O" }
];

const REDUCERS_LIST = [
  { id:"Fe2",  formulaHTML:"Fe<sup>2+</sup>",                     name:"亞鐵離子",   compound:"FeSO₄" },
  { id:"I-",   formulaHTML:"I<sup>−</sup>",                       name:"碘化物離子", compound:"KI" },
  { id:"Sn2",  formulaHTML:"Sn<sup>2+</sup>",                     name:"錫(II)離子", compound:"SnCl₂" },
  { id:"Br-",  formulaHTML:"Br<sup>−</sup>",                      name:"溴化物離子", compound:"KBr" },
  { id:"C2O4", formulaHTML:"C<sub>2</sub>O<sub>4</sub><sup>2−</sup>", name:"草酸根離子", compound:"Na₂C₂O₄" },
  { id:"S2O3", formulaHTML:"S<sub>2</sub>O<sub>3</sub><sup>2−</sup>", name:"硫代硫酸根", compound: "Na₂S₂O₃" },
  { id:"I2",   formulaHTML:"I<sub>2</sub>",                       name:"碘分子", compound: "I₂" },
  { id:"H2O2", formulaHTML:"H<sub>2</sub>O<sub>2</sub>",          name:"雙氧水", compound: "H₂O₂" },
  { id:"Cu",   formulaHTML:"Cu",                                  name:"金屬銅", compound: "Cu" },
  { id:"HSO3-",formulaHTML:"HSO<sub>3</sub><sup>−</sup>",         name:"亞硫酸氫根", compound: "NaHSO₃" },
  { id:"Al",   formulaHTML:"Al",                                  name:"金屬鋁", compound: "Al" }
];

/* ╔═══════════════════════════════════════════════════════╗
   ║  HALF_REACTIONS ─ 預定義的半反應模組 (包含 E0 與產物)   ║
   ╚═══════════════════════════════════════════════════════╝ */
const HALF_REACTIONS = [
  { oxForm: "MnO4", redForm: "Mn2",     conds: ["acid"], E0: 1.51 }, // MnO4- -> Mn2+
  { oxForm: "MnO4", redForm: "MnO2",    conds: ["neutral", "weak_base", "acid", "base"], E0: 1.69 }, // MnO4- -> MnO2
  { oxForm: "MnO4", redForm: "MnO4_2-", conds: ["base"], E0: 0.56 }, // MnO4- -> MnO4^2-
  { oxForm: "MnO4", redForm: "Mn2O3",   conds: ["acid", "base"], E0: 1.0 }, // MnO4- -> Mn2O3
  { oxForm: "Cr2O7",redForm: "Cr3",     conds: ["acid"], E0: 1.33 },
  { oxForm: "Cl2",  redForm: "Cl-",     conds: ["acid", "base", "neutral"], E0: 1.36 },
  { oxForm: "Br2",  redForm: "Br-",     conds: ["acid", "base", "neutral"], E0: 1.07 },
  { oxForm: "Fe3ox",redForm: "Fe2prod", conds: ["acid"], E0: 0.77 },   // Fe3+ -> Fe2+
  { oxForm: "Fe3",  redForm: "Fe2",     conds: ["acid"], E0: 0.77 },   // Fe3+ -> Fe2+ (aliases)
  { oxForm: "I2",   redForm: "I-",      conds: ["acid", "base", "neutral"], E0: 0.54 },
  { oxForm: "IO3-", redForm: "I2",      conds: ["acid"], E0: 1.20 },
  { oxForm: "S4O6", redForm: "S2O3",    conds: ["acid", "base", "neutral"], E0: 0.08, maxOxE0: 0.70 }, // 只與較弱氧化劑產生 S4O6 (例如 I2)
  { oxForm: "SO4",  redForm: "S2O3",    conds: ["acid", "base", "neutral"], E0: 0.40, minOxE0: 0.71 }, // 遇到強氧化劑則直接氧化至 SO4
  { oxForm: "Sn4",  redForm: "Sn2",     conds: ["acid"], E0: 0.15 },
  { oxForm: "CO2",  redForm: "C2O4",    conds: ["acid", "base"], E0: -0.49 },
  { oxForm: "H2O2", redForm: "H2O_prod", conds: ["acid", "base", "neutral"], E0: 1.78 },
  { oxForm: "O2",   redForm: "H2O2",     conds: ["acid", "base", "neutral"], E0: 0.68 },
  { oxForm: "NO3-", redForm: "NO2",     conds: ["acid"], E0: 0.80 },
  { oxForm: "NO3-", redForm: "NO",      conds: ["acid"], E0: 0.96 },
  { oxForm: "Cu2+", redForm: "Cu",      conds: ["acid", "base", "neutral"], E0: 0.34 },
  { oxForm: "SO4",  redForm: "HSO3-",   conds: ["acid", "base", "neutral"], E0: 0.17 },
  { oxForm: "Hplus", redForm: "H2",     conds: ["acid"], E0: 0 },
  { oxForm: "H2O_ox", redForm: "H2",    conds: ["base"], E0: -0.83 },
  { oxForm: "Al3",  redForm: "Al",      conds: ["acid"], E0: -1.66 },
  { oxForm: "AlOH4", redForm: "Al",     conds: ["base"], E0: -2.33 }
];

/* 輔助函式：取得物種參與的半反應 */
function getHalfReactionsFor(id) {
  // Alias grouping
  const aliasOf = { 'Fe3ox':'Fe3', 'Fe2prod':'Fe2' };
  const getBase = x => aliasOf[x] || x;
  const baseId = getBase(id);

  return HALF_REACTIONS.filter(hr => getBase(hr.oxForm) === baseId || getBase(hr.redForm) === baseId);
}

function gcd(a, b) { return b === 0 ? a : gcd(b, a % b); }
function lcm(a, b) { return (a * b) / gcd(a, b); }
