/**
 * Fetches the 3D SDF structure and IUPAC name from PubChem for a given SMILES string.
 */

const PUBCHEM_BASE = 'https://pubchem.ncbi.nlm.nih.gov/rest/pug';

export interface MoleculeInfo {
  iupacName: string;
  chineseName: string;
  sdf: string;
  cid: number;
}

// ── IUPAC → Chinese name mapping ──────────────────────────────────────────
const IUPAC_ZH_MAP: Record<string, string> = {
  // Alkanes
  methane: '甲烷', ethane: '乙烷', propane: '丙烷', butane: '丁烷',
  pentane: '戊烷', hexane: '己烷', heptane: '庚烷', octane: '辛烷',
  nonane: '壬烷', decane: '癸烷', undecane: '十一烷', dodecane: '十二烷',
  isobutane: '異丁烷', isopentane: '異戊烷', neopentane: '新戊烷',
  '2-methylpropane': '2-甲基丙烷', '2-methylbutane': '2-甲基丁烷',
  cyclohexane: '環己烷', cyclopentane: '環戊烷', cyclobutane: '環丁烷', cyclopropane: '環丙烷',

  // Alkenes
  ethene: '乙烯', propene: '丙烯', 'but-1-ene': '1-丁烯', 'but-2-ene': '2-丁烯',
  '2-methylpropene': '2-甲基丙烯', 'pent-1-ene': '1-戊烯', 'hex-1-ene': '1-己烯',
  ethylene: '乙烯', propylene: '丙烯',

  // Alkynes
  ethyne: '乙炔', propyne: '丙炔', 'but-1-yne': '1-丁炔', 'but-2-yne': '2-丁炔',
  acetylene: '乙炔',

  // Aromatic
  benzene: '苯', toluene: '甲苯', ethylbenzene: '乙苯', styrene: '苯乙烯', xylene: '二甲苯',
  naphthalene: '萘', aniline: '苯胺', phenol: '苯酚',

  // Alcohols
  methanol: '甲醇', ethanol: '乙醇',
  'propan-1-ol': '1-丙醇', 'propan-2-ol': '2-丙醇',
  'butan-1-ol': '1-丁醇', 'butan-2-ol': '2-丁醇',
  'pentan-1-ol': '1-戊醇', 'hexan-1-ol': '1-己醇',
  '2-methylpropan-1-ol': '異丁醇', '2-methylpropan-2-ol': '叔丁醇',
  'ethylene glycol': '乙二醇', glycerol: '甘油', glycerin: '甘油',

  // Ethers
  methoxymethane: '二甲醚', ethoxyethane: '乙醚', 'diethyl ether': '乙醚',
  'dimethyl ether': '二甲醚', methoxyethane: '甲乙醚',

  // Aldehydes
  methanal: '甲醛', ethanal: '乙醛', propanal: '丙醛', butanal: '丁醛', pentanal: '戊醛',
  formaldehyde: '甲醛', acetaldehyde: '乙醛',

  // Ketones
  'propan-2-one': '丙酮', acetone: '丙酮', 'butan-2-one': '丁酮',
  'methyl ethyl ketone': '甲乙酮', 'pentan-2-one': '戊-2-酮', 'pentan-3-one': '戊-3-酮',
  cyclohexanone: '環己酮',

  // Carboxylic acids
  'methanoic acid': '甲酸', 'formic acid': '甲酸',
  'ethanoic acid': '乙酸', 'acetic acid': '乙酸',
  'propanoic acid': '丙酸', 'butanoic acid': '丁酸',
  'pentanoic acid': '戊酸', 'hexanoic acid': '己酸',
  'benzoic acid': '苯甲酸', 'oxalic acid': '草酸',
  'citric acid': '檸檬酸', 'lactic acid': '乳酸',
  'pyruvic acid': '丙酮酸', 'malonic acid': '丙二酸',
  'succinic acid': '琥珀酸', 'glutaric acid': '戊二酸', 'adipic acid': '己二酸',
  'acrylic acid': '丙烯酸', 'methacrylic acid': '甲基丙烯酸',

  // Esters
  'methyl methanoate': '甲酸甲酯', 'methyl acetate': '乙酸甲酯',
  'ethyl acetate': '乙酸乙酯', 'ethyl formate': '甲酸乙酯',
  'methyl propanoate': '丙酸甲酯', 'ethyl propanoate': '丙酸乙酯',

  // Amines
  methanamine: '甲胺', methylamine: '甲胺', ethanamine: '乙胺', ethylamine: '乙胺',
  'propan-1-amine': '1-丙胺', dimethylamine: '二甲胺', trimethylamine: '三甲胺',
  diethylamine: '二乙胺', triethylamine: '三乙胺',

  // Amides
  methanamide: '甲醯胺', ethanamide: '乙醯胺', acetamide: '乙醯胺',
  propanamide: '丙醯胺', urea: '尿素', carbamide: '脲',

  // Halides
  fluoromethane: '氟甲烷', chloromethane: '氯甲烷', bromomethane: '溴甲烷', iodomethane: '碘甲烷',
  fluoroethane: '氟乙烷', chloroethane: '氯乙烷', bromoethane: '溴乙烷', iodoethane: '碘乙烷',
  fluoroethene: '氟乙烯', chloroethene: '氯乙烯', bromoethene: '溴乙烯', iodoethene: '碘乙烯',
  dichloromethane: '二氯甲烷', chloroform: '三氯甲烷', 'carbon tetrachloride': '四氯化碳',
  trichloromethane: '三氯甲烷', tetrachloromethane: '四氯甲烷',
  '1-chloropropane': '1-氯丙烷', '2-chloropropane': '2-氯丙烷', '1-bromopropane': '1-溴丙烷',

  // Nitriles / nitrogen
  nitromethane: '硝基甲烷', acetonitrile: '乙腈', propionitrile: '丙腈', acrylonitrile: '丙烯腈',

  // Biochemicals
  glucose: '葡萄糖', fructose: '果糖', sucrose: '蔗糖',
  glycine: '甘胺酸', alanine: '丙胺酸', serine: '絲胺酸', threonine: '蘇胺酸',

  // Simple / common
  water: '水', 'hydrogen chloride': '氯化氫',
  'carbon dioxide': '二氧化碳', 'carbon monoxide': '一氧化碳',
};

// ── Systematic IUPAC → Chinese rule-based translator ──────────────────────

const CHAIN_ZH: Record<string, string> = {
  meth: '甲', eth: '乙', prop: '丙', but: '丁',
  pent: '戊', hex: '己', hept: '庚', oct: '辛',
  non: '壬', dec: '癸', undec: '十一', dodec: '十二',
};

const SUFFIX_ZH: Record<string, string> = {
  ane: '烷', ene: '烯', yne: '炔',
  ol:  '醇', al:  '醛', one: '酮',
  'oic acid': '酸', 'amine': '胺', 'amide': '醯胺',
  'nitrile': '腈',
};

const PREFIX_ZH: Record<string, string> = {
  methyl:   '甲基',  ethyl:    '乙基',  propyl:   '丙基',
  butyl:    '丁基',  pentyl:   '戊基',  hexyl:    '己基',
  heptyl:   '庚基',  octyl:    '辛基',  nonyl:    '壬基',
  decyl:    '癸基',  isopropyl:'異丙基', isobutyl: '異丁基',
  'tert-butyl': '叔丁基',
  fluoro:   '氟',    chloro:   '氯',    bromo:    '溴',    iodo: '碘',
  hydroxy:  '羥',    amino:    '胺',    nitro:    '硝基',  oxo: '酮基',
  cyclo:    '環',    di: '二', tri: '三', tetra: '四',
  'sec-':   '仲',    'tert-':  '叔',
};

const HALIDE_PARENT: Record<string, string> = {
  fluorometh: '氟甲', chlorometh: '氯甲', bromometh: '溴甲', iodometh: '碘甲',
  fluoroeth:  '氟乙', chloroeth:  '氯乙', bromoeth:  '溴乙', iodoeth:  '碘乙',
  fluoroprop: '氟丙', chloroprop: '氯丙', bromoprop: '溴丙', iodoprop: '碘丙',
};

function translateChain(stem: string): string {
  return CHAIN_ZH[stem] ?? stem;
}

/**
 * Attempt a systematic rule-based translation of an IUPAC name.
 * Returns null if the name doesn't match any known pattern.
 */
function systematicTranslate(name: string): string | null {
  const n = name.toLowerCase().trim();

  // ── Handle halide-named parents (e.g. bromoethene → 溴乙烯) ──────────
  for (const [halPfx, zhPfx] of Object.entries(HALIDE_PARENT)) {
    if (n.startsWith(halPfx)) {
      const rest = n.slice(halPfx.length); // e.g. "ene", "ane", "ol"
      const sfx = SUFFIX_ZH[rest];
      if (sfx) return `${zhPfx}${sfx}`;
    }
  }

  // ── Handle cyclo- prefix ───────────────────────────────────────────────
  const cycloMatch = n.match(/^cyclo([a-z]+)(ane|ene|yne|ol|one|al)$/);
  if (cycloMatch) {
    const chain = translateChain(cycloMatch[1]);
    const sfx   = SUFFIX_ZH[cycloMatch[2]] ?? cycloMatch[2];
    return `環${chain}${sfx}`;
  }

  // ── Handle names like "2-methylbut-1-ene", "3-ethylhex-2-yne" ─────────
  // Pattern: [locant-]substituent(s)-parent-[locant-]suffix
  // e.g. "2-methylbut-1-ene" → 2-甲基-1-丁烯（舊式）
  //      "2,3-dimethylbutane" → 2,3-二甲基丁烷
  //      "but-2-ene"          → 2-丁烯（舊式）
  //      "pent-1-ene"         → 1-戊烯（舊式）

  // 1. Attempt to detect parent chain in middle of name
  const chainKeys = Object.keys(CHAIN_ZH).sort((a, b) => b.length - a.length);
  for (const stem of chainKeys) {
    // match: (prefix-part)(stem)(optional position like -2-)(suffix)
    // e.g.  "2-methyl" + "but" + "-1-" + "ene"
    const regex = new RegExp(
      `^(.*?)(${stem})((?:-\\d+(?:,\\d+)*-)?)(ane|ene|yne|ol|one|al|oic acid|amine|amide|nitrile)$`
    );
    const m = n.match(regex);
    if (!m) continue;

    const prefixPart = m[1];   // e.g. "2-methyl" or "2,3-dimethyl" or ""
    const chainStem  = m[2];   // e.g. "but"
    const posInfix   = m[3];   // e.g. "-1-" or ""
    const suffix     = m[4];   // e.g. "ene"

    // Translate prefix substituents
    let zhPrefix = prefixPart;
    for (const [en, zh] of Object.entries(PREFIX_ZH)) {
      zhPrefix = zhPrefix.replace(new RegExp(en, 'g'), zh);
    }
    // Clean up remaining dashes and normalize
    zhPrefix = zhPrefix.replace(/-+$/, '');

    const zhChain  = CHAIN_ZH[chainStem] ?? chainStem;
    // 舊式：位次在主鏈名前，e.g. 2-丁烯、2-甲基-1-丁烯
    // posInfix 原為 "-1-"，轉換成前置 "1-" 並接在 zhPrefix 後面
    const posPrefix = posInfix ? posInfix.replace(/^-/, '').replace(/-$/, '-') : '';
    const zhSuffix  = SUFFIX_ZH[suffix] ?? suffix;

    // 組合：取代基前綴（含原本的位次如 2-甲基）+ 後段位次 + 主鏈 + 字尾
    // e.g. "2-甲基" + "1-" + "丁" + "烯" = "2-甲基-1-丁烯"
    const combined = zhPrefix
      ? `${zhPrefix}-${posPrefix}${zhChain}${zhSuffix}`
      : `${posPrefix}${zhChain}${zhSuffix}`;
    return combined.replace(/^-/, '');
  }

  // ── Simple "parent + suffix" (no substituents, with optional locant) ───
  //  e.g. "but-1-yne" → 1-丁炔, "pent-2-ene" → 2-戊烯（舊式）
  const simpleMatch = n.match(/^([a-z]+?)(-\d+-|\d+-)?(ane|ene|yne|ol|one|al|oic acid|amine|amide|nitrile)$/);
  if (simpleMatch) {
    const chainZh = CHAIN_ZH[simpleMatch[1]];
    if (chainZh) {
      // 舊式：把 "-2-" 轉成前置 "2-"，放在主鏈前
      const rawPos = simpleMatch[2] ?? '';
      const pos    = rawPos.replace(/^-/, '').replace(/-$/, '-'); // "-2-" → "2-"
      const sfxZh  = SUFFIX_ZH[simpleMatch[3]] ?? simpleMatch[3];
      return `${pos}${chainZh}${sfxZh}`;
    }
  }

  return null;
}

export function translateToZh(iupacName: string): string {
  const key = iupacName.toLowerCase().trim();
  // 1. Exact lookup in static map
  if (IUPAC_ZH_MAP[key]) return IUPAC_ZH_MAP[key];
  // 2. Systematic rule-based translator
  const sys = systematicTranslate(key);
  if (sys) return sys;
  // 3. Fall back to original English name
  return iupacName;

}

export async function fetchMoleculeInfo(smiles: string): Promise<MoleculeInfo | null> {
  try {
    const encodedSmiles = encodeURIComponent(smiles);

    // Get CID from SMILES
    const cidResp = await fetch(
      `${PUBCHEM_BASE}/compound/smiles/${encodedSmiles}/cids/JSON`
    );
    if (!cidResp.ok) return null;
    const cidData = await cidResp.json();
    const cid: number = cidData.IdentifierList?.CID?.[0];
    if (!cid) return null;

    // Get IUPAC name and 3D SDF in parallel
    const [propResp, sdfResp] = await Promise.all([
      fetch(`${PUBCHEM_BASE}/compound/cid/${cid}/property/IUPACName/JSON`),
      fetch(`${PUBCHEM_BASE}/compound/cid/${cid}/SDF?record_type=3d`),
    ]);

    const propData = await propResp.json();
    const iupacName: string =
      propData.PropertyTable?.Properties?.[0]?.IUPACName ?? '';
    const sdf = await sdfResp.text();

    return {
      iupacName,
      chineseName: translateToZh(iupacName),
      sdf,
      cid,
    };
  } catch (e) {
    console.error('fetchMoleculeInfo error', e);
    return null;
  }
}
