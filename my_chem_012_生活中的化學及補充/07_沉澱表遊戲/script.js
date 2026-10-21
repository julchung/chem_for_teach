// Mobile detection
const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) || 
               (navigator.maxTouchPoints > 0);

if (isMobile) {
    document.body.classList.add('is-mobile');
}

const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

// Constants for internal game resolution
const INTERNAL_WIDTH = 600;
const INTERNAL_HEIGHT = 900;
const HEADER_HEIGHT = 50;
const BUBBLE_RADIUS = 30;
const BUBBLE_DIAMETER = BUBBLE_RADIUS * 2;
const GRID_COLS = Math.floor(INTERNAL_WIDTH / BUBBLE_DIAMETER);
const GRID_ROWS = 15;

// Scaling variables
let scale = 1;

// Game State
let gameState = 'START'; // START, PLAYING, GAME_OVER, WIN
let grid = {};
let fallingBubbles = [];
let projectile = null;
let score = 0;
let level = 1;
let startTime = 0;
let gameWon = false;
let gameOver = false;

// Shooter
let shooterAngle = Math.PI / 2;
let currentIon = null;
let nextIon = null;
let next2Ion = null;
let nextIsCation = true;
let recoil = 0; // Visual recoil effect

// Combo & Stats
let currentCombo = 0;
let maxCombo = 0;
let totalDrops = 0;
let precipitateCounts = {}; // Key: precipId -> count
let scorePopups = []; // Floating score texts

// Level 3 Timer
let lastSpawnTime = 0;

// Ions Data
const IONS = {
    'K': { charge: 1, color: [148, 0, 211], formula: 'K', charge_disp: '＋' },
    'Na': { charge: 1, color: [255, 215, 0], formula: 'Na', charge_disp: '＋' },
    'Mg': { charge: 2, color: [50, 205, 50], formula: 'Mg', charge_disp: '２＋' },
    'Ba': { charge: 2, color: [0, 255, 127], formula: 'Ba', charge_disp: '２＋' },
    'Ag': { charge: 1, color: [192, 192, 192], formula: 'Ag', charge_disp: '＋' },
    'Cu': { charge: 2, color: [0, 100, 255], formula: 'Cu', charge_disp: '２＋' },
    'Pb': { charge: 2, color: [130, 130, 140], formula: 'Pb', charge_disp: '２＋' },
    'Zn': { charge: 2, color: [100, 149, 237], formula: 'Zn', charge_disp: '２＋' },
    'Cu1': { charge: 1, color: [255, 140, 0], formula: 'Cu', charge_disp: '＋' },
    'NO3': { charge: -1, color: [255, 182, 193], formula: 'NO3', charge_disp: '－' },
    'SO4': { charge: -2, color: [255, 255, 0], formula: 'SO4', charge_disp: '２－' },
    'Cl': { charge: -1, color: [144, 238, 144], formula: 'Cl', charge_disp: '－' },
    'CO3': { charge: -2, color: [160, 160, 160], formula: 'CO3', charge_disp: '２－' },
    'I': { charge: -1, color: [75, 0, 130], formula: 'I', charge_disp: '－' },
    'S': { charge: -2, color: [255, 255, 102], formula: 'S', charge_disp: '２－' },
    'OH': { charge: -1, color: [0, 255, 255], formula: 'OH', charge_disp: '－' },
    'Br': { charge: -1, color: [180, 50, 50], formula: 'Br', charge_disp: '－' },
};

// Precipitate Specifications & Scoring Matrix
const PRECIPITATES_DATA = {
    // 3-cluster High Difficulty (Tier Gold)
    'PbI2': { name: '碘化鉛 (金雨)', formula: 'PbI₂', colorDesc: '金黃結晶', colorHex: '#eab308', stars: 3, baseScore: 600, tier: 'gold', ions: ['Pb', 'I'] },
    'Ag2S': { name: '硫化銀', formula: 'Ag₂S', colorDesc: '黑色沉澱', colorHex: '#18181b', stars: 3, baseScore: 520, tier: 'gold', ions: ['Ag', 'S'] },
    'Cu2SO4': { name: '硫酸亞銅', formula: 'Cu₂SO₄', colorDesc: '白色沉澱', colorHex: '#f8fafc', stars: 3, baseScore: 500, tier: 'gold', ions: ['Cu1', 'SO4'] },
    'Ag2CO3': { name: '碳酸銀', formula: 'Ag₂CO₃', colorDesc: '黃色沉澱', colorHex: '#fde047', stars: 3, baseScore: 500, tier: 'gold', ions: ['Ag', 'CO3'] },
    'Cu(OH)2': { name: '氫氧化銅', formula: 'Cu(OH)₂', colorDesc: '藍色沉澱', colorHex: '#38bdf8', stars: 3, baseScore: 480, tier: 'gold', ions: ['Cu', 'OH'] },
    'PbCl2': { name: '氯化鉛', formula: 'PbCl₂', colorDesc: '白色結晶', colorHex: '#f1f5f9', stars: 3, baseScore: 450, tier: 'gold', ions: ['Pb', 'Cl'] },
    'PbBr2': { name: '溴化鉛', formula: 'PbBr₂', colorDesc: '白色結晶', colorHex: '#f1f5f9', stars: 3, baseScore: 450, tier: 'gold', ions: ['Pb', 'Br'] },
    'Mg(OH)2': { name: '氫氧化鎂', formula: 'Mg(OH)₂', colorDesc: '白色沉澱', colorHex: '#f8fafc', stars: 3, baseScore: 450, tier: 'gold', ions: ['Mg', 'OH'] },
    'Pb(OH)2': { name: '氫氧化鉛', formula: 'Pb(OH)₂', colorDesc: '白色沉澱', colorHex: '#f8fafc', stars: 3, baseScore: 450, tier: 'gold', ions: ['Pb', 'OH'] },

    // Rare/Sulfide/Carbonate (Tier Purple)
    'CuCO3': { name: '碳酸銅', formula: 'CuCO₃', colorDesc: '藍綠沉澱', colorHex: '#2dd4bf', stars: 2, baseScore: 260, tier: 'purple', ions: ['Cu', 'CO3'] },
    'PbS': { name: '硫化鉛', formula: 'PbS', colorDesc: '黑色沉澱', colorHex: '#18181b', stars: 2, baseScore: 250, tier: 'purple', ions: ['Pb', 'S'] },
    'CuS': { name: '硫化銅', formula: 'CuS', colorDesc: '黑色沉澱', colorHex: '#09090b', stars: 2, baseScore: 250, tier: 'purple', ions: ['Cu', 'S'] },
    'AgOH': { name: '氧化銀', formula: 'Ag₂O', colorDesc: '棕黑沉澱', colorHex: '#78350f', stars: 2, baseScore: 220, tier: 'purple', ions: ['Ag', 'OH'] },
    'CuI': { name: '碘化亞銅', formula: 'CuI', colorDesc: '棕白沉澱', colorHex: '#d6d3d1', stars: 2, baseScore: 220, tier: 'purple', ions: ['Cu1', 'I'] },

    // Basic Halides & Sulfates (Tier Cyan)
    'AgI': { name: '碘化銀', formula: 'AgI', colorDesc: '黃色沉澱', colorHex: '#facc15', stars: 1, baseScore: 200, tier: 'cyan', ions: ['Ag', 'I'] },
    'AgBr': { name: '溴化銀', formula: 'AgBr', colorDesc: '淡黃沉澱', colorHex: '#fef08a', stars: 1, baseScore: 180, tier: 'cyan', ions: ['Ag', 'Br'] },
    'AgCl': { name: '氯化銀', formula: 'AgCl', colorDesc: '白色沉澱', colorHex: '#f8fafc', stars: 1, baseScore: 180, tier: 'cyan', ions: ['Ag', 'Cl'] },
    'CuCl': { name: '氯化亞銅', formula: 'CuCl', colorDesc: '白色沉澱', colorHex: '#f1f5f9', stars: 1, baseScore: 180, tier: 'cyan', ions: ['Cu1', 'Cl'] },
    'CuBr': { name: '溴化亞銅', formula: 'CuBr', colorDesc: '白色沉澱', colorHex: '#f1f5f9', stars: 1, baseScore: 200, tier: 'cyan', ions: ['Cu1', 'Br'] },
    'PbSO4': { name: '硫酸鉛', formula: 'PbSO₄', colorDesc: '白色沉澱', colorHex: '#f1f5f9', stars: 1, baseScore: 180, tier: 'cyan', ions: ['Pb', 'SO4'] },
    'BaSO4': { name: '硫酸鋇', formula: 'BaSO₄', colorDesc: '白色沉澱', colorHex: '#ffffff', stars: 1, baseScore: 180, tier: 'cyan', ions: ['Ba', 'SO4'] },
    'BaCO3': { name: '碳酸鋇', formula: 'BaCO₃', colorDesc: '白色沉澱', colorHex: '#f8fafc', stars: 1, baseScore: 180, tier: 'cyan', ions: ['Ba', 'CO3'] },
    'MgCO3': { name: '碳酸鎂', formula: 'MgCO₃', colorDesc: '白色沉澱', colorHex: '#f8fafc', stars: 1, baseScore: 180, tier: 'cyan', ions: ['Mg', 'CO3'] },
    'PbCO3': { name: '碳酸鉛', formula: 'PbCO₃', colorDesc: '白色沉澱', colorHex: '#f1f5f9', stars: 1, baseScore: 180, tier: 'cyan', ions: ['Pb', 'CO3'] },
};

const LEVEL1_CATIONS = ['Na', 'Ag', 'Cu1', 'Cu', 'Pb'];
const LEVEL1_ANIONS = ['Cl', 'Br', 'I', 'NO3', 'SO4'];
const LEVEL2_CATIONS = ['Na', 'Mg', 'Ba', 'Ag', 'Cu', 'Pb'];
const LEVEL2_ANIONS = ['Cl', 'NO3', 'S', 'CO3', 'SO4', 'OH'];

// Floating Score Popups Class
class ScorePopup {
    constructor(x, y, text, color = '#ffd700', subText = '') {
        this.x = x;
        this.y = y;
        this.text = text;
        this.subText = subText;
        this.color = color;
        this.alpha = 1.0;
        this.vy = -1.8;
        this.life = 60;
    }

    update() {
        this.y += this.vy;
        this.vy *= 0.96;
        this.life--;
        if (this.life < 20) {
            this.alpha = this.life / 20;
        }
    }

    draw() {
        ctx.save();
        ctx.globalAlpha = Math.max(0, this.alpha);
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        
        // Glow shadow
        ctx.shadowColor = this.color;
        ctx.shadowBlur = 10;
        
        ctx.font = 'bold 22px "Noto Sans TC", sans-serif';
        ctx.fillStyle = this.color;
        ctx.fillText(this.text, this.x, this.y);

        if (this.subText) {
            ctx.font = 'bold 13px "Noto Sans TC", sans-serif';
            ctx.fillStyle = '#ffffff';
            ctx.fillText(this.subText, this.x, this.y + 18);
        }
        ctx.restore();
    }
}

// Bubble Class
class Bubble {
    constructor(ion, r, c) {
        this.ion = ion;
        this.r = r;
        this.c = c;
        this.x = 0;
        this.y = 0;
        this.state = 'normal';
        this.popTimer = 0;
        this.scale = 1.0;
        this.updatePos();
    }

    updatePos() {
        const offset = (this.r % 2 === 1) ? BUBBLE_RADIUS : 0;
        this.x = this.c * BUBBLE_DIAMETER + BUBBLE_RADIUS + offset;
        this.y = this.r * (BUBBLE_DIAMETER * 0.85) + BUBBLE_RADIUS + HEADER_HEIGHT;
    }

    draw() {
        if (this.state === 'popping') {
            this.scale = 1.0 + (30 - this.popTimer) / 30 * 0.5;
        }
        drawBubble(this.x, this.y, BUBBLE_RADIUS * this.scale, this.ion);
    }
}

class Projectile {
    constructor(ion, x, y, angle) {
        this.ion = ion;
        this.x = x;
        this.y = y;
        this.angle = angle;
        this.speed = 30;
        this.dx = Math.cos(angle) * this.speed;
        this.dy = -Math.sin(angle) * this.speed;
        this.scale = 0.75;
    }

    move() {
        this.x += this.dx;
        this.y += this.dy;

        const r = BUBBLE_RADIUS * this.scale;

        // Wall Bounce
        if (this.x < r) {
            this.x = r;
            this.dx *= -1;
        } else if (this.x > INTERNAL_WIDTH - r) {
            this.x = INTERNAL_WIDTH - r;
            this.dx *= -1;
        }
    }

    draw() {
        drawBubble(this.x, this.y, BUBBLE_RADIUS * this.scale, this.ion);
    }
}

class FallingBubble {
    constructor(ion, x, y) {
        this.ion = ion;
        this.x = x;
        this.y = y;
        this.dy = -2;
        this.gravity = 0.5;
    }

    update() {
        this.dy += this.gravity;
        this.y += this.dy;
        this.x += (Math.random() - 0.5) * 2;
    }

    draw() {
        drawBubble(this.x, this.y, BUBBLE_RADIUS, this.ion);
    }
}

// Canvas Sizing & Center Calculation
function resizeCanvas() {
    const stage = document.getElementById('center-stage');
    const availableWidth = stage ? stage.clientWidth : window.innerWidth;
    const availableHeight = stage ? stage.clientHeight : window.innerHeight;

    const gameRatio = INTERNAL_WIDTH / INTERNAL_HEIGHT;
    const containerRatio = availableWidth / availableHeight;

    if (containerRatio > gameRatio) {
        canvas.height = availableHeight;
        canvas.width = availableHeight * gameRatio;
    } else {
        canvas.width = availableWidth;
        canvas.height = availableWidth / gameRatio;
    }

    scale = canvas.width / INTERNAL_WIDTH;
}

// Coordinate Mapping
function getGameCoords(e) {
    const rect = canvas.getBoundingClientRect();
    const touch = e.touches ? e.touches[0] : e;
    const x = (touch.clientX - rect.left) / scale;
    const y = (touch.clientY - rect.top) / scale;
    return { x, y };
}

// Draw Bubble with 3D Gloss
function drawBubble(cx, cy, radius, ionName) {
    const data = IONS[ionName];
    if (!data) return;
    const color = data.color;

    ctx.save();

    // Outer subtle glow
    ctx.shadowColor = `rgba(${color[0]}, ${color[1]}, ${color[2]}, 0.5)`;
    ctx.shadowBlur = radius * 0.4;

    const gradient = ctx.createRadialGradient(cx - radius / 3, cy - radius / 3, radius / 10, cx, cy, radius);

    const lr = Math.min(255, color[0] * 1.5);
    const lg = Math.min(255, color[1] * 1.5);
    const lb = Math.min(255, color[2] * 1.5);

    const dr = Math.floor(color[0] * 0.35);
    const dg = Math.floor(color[1] * 0.35);
    const db = Math.floor(color[2] * 0.35);

    gradient.addColorStop(0, `rgb(${lr},${lg},${lb})`);
    gradient.addColorStop(0.7, `rgb(${color[0]},${color[1]},${color[2]})`);
    gradient.addColorStop(1, `rgb(${dr},${dg},${db})`);

    ctx.fillStyle = gradient;
    ctx.beginPath();
    ctx.arc(cx, cy, radius, 0, Math.PI * 2);
    ctx.fill();

    // Specular highlight
    ctx.shadowBlur = 0;
    const highlight = ctx.createRadialGradient(cx - radius * 0.35, cy - radius * 0.35, 1, cx - radius * 0.35, cy - radius * 0.35, radius * 0.45);
    highlight.addColorStop(0, 'rgba(255, 255, 255, 0.7)');
    highlight.addColorStop(1, 'rgba(255, 255, 255, 0)');
    ctx.fillStyle = highlight;
    ctx.beginPath();
    ctx.arc(cx - radius * 0.35, cy - radius * 0.35, radius * 0.45, 0, Math.PI * 2);
    ctx.fill();

    // Edge ring
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.2)';
    ctx.lineWidth = 1.5;
    ctx.stroke();

    ctx.restore();

    drawIonText(cx, cy, data.formula, data.charge_disp, radius);
}

function drawIonText(cx, cy, formula, charge, radius) {
    ctx.fillStyle = 'white';
    ctx.strokeStyle = '#111';
    ctx.lineWidth = 3;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';

    const symbolSize = radius * 0.58;
    const subSize = radius * 0.38;
    const chargeSize = radius * 0.33;

    ctx.font = `bold ${symbolSize}px "Noto Sans TC", sans-serif`;

    let parts = [];
    let totalW = 0;

    for (let char of formula) {
        let isNum = /\d/.test(char);
        let f = isNum ? `bold ${subSize}px "Noto Sans TC", sans-serif` : `bold ${symbolSize}px "Noto Sans TC", sans-serif`;
        ctx.font = f;
        let w = ctx.measureText(char).width;
        parts.push({ char, isNum, w, font: f });
        totalW += w;
    }

    ctx.font = `bold ${chargeSize}px "Noto Sans TC", sans-serif`;
    let chargeW = ctx.measureText(charge).width;
    totalW += chargeW;

    let curX = cx - totalW / 2;
    let baseY = cy;

    parts.forEach(p => {
        ctx.font = p.font;
        let y = p.isNum ? baseY + radius * 0.22 : baseY;
        ctx.strokeText(p.char, curX + p.w / 2, y);
        ctx.fillText(p.char, curX + p.w / 2, y);
        curX += p.w;
    });

    ctx.font = `bold ${chargeSize}px "Noto Sans TC", sans-serif`;
    let chargeY = baseY - radius * 0.22;
    ctx.strokeText(charge, curX + chargeW / 2, chargeY);
    ctx.fillText(charge, curX + chargeW / 2, chargeY);
}

// Reset Game
function resetGame(lvl) {
    level = lvl || level;
    grid = {};
    fallingBubbles = [];
    projectile = null;
    score = 0;
    currentCombo = 0;
    maxCombo = 0;
    totalDrops = 0;
    precipitateCounts = {};
    scorePopups = [];
    gameWon = false;
    gameOver = false;
    startTime = Date.now();
    nextIsCation = true;
    shooterAngle = Math.PI / 2;
    lastSpawnTime = Date.now();
    recoil = 0;

    document.getElementById('level').innerText = level;
    document.getElementById('score').innerText = 0;
    document.getElementById('right-panel-score').innerText = 0;
    document.getElementById('combo-badge').classList.add('hidden');
    document.getElementById('reaction-feed').innerHTML = '<div class="feed-empty">發射離子觸發沉澱反應...</div>';

    renderPrecipitateCards();
    updateRankDisplay();

    if (level === 1) populateGrid(8, 8);
    else populateGrid(15, 15);

    currentIon = getRandomCation();
    nextIon = getRandomAnion();
    next2Ion = getRandomCation();
    nextIsCation = false;
}

function getRandomCation() {
    let list = (level === 1) ? LEVEL1_CATIONS : LEVEL2_CATIONS;
    return list[Math.floor(Math.random() * list.length)];
}

function getRandomAnion() {
    let list = (level === 1) ? LEVEL1_ANIONS : LEVEL2_ANIONS;
    return list[Math.floor(Math.random() * list.length)];
}

function populateGrid(nCat, nAni) {
    let list = [];
    for (let i = 0; i < nCat; i++) list.push(getRandomCation());
    for (let i = 0; i < nAni; i++) list.push(getRandomAnion());
    list.sort(() => Math.random() - 0.5);

    let count = 0;
    for (let ion of list) {
        while (true) {
            let r = Math.floor(count / GRID_COLS);
            let c = count % GRID_COLS;
            count++;
            if (r % 2 === 1 && c >= GRID_COLS - 1) continue;
            grid[`${r},${c}`] = new Bubble(ion, r, c);
            break;
        }
    }
}

function getNeighbors(r, c) {
    let offsets = (r % 2 === 1)
        ? [[-1, 0], [-1, 1], [0, -1], [0, 1], [1, 0], [1, 1]]
        : [[-1, -1], [-1, 0], [0, -1], [0, 1], [1, -1], [1, 0]];
    return offsets.map(([dr, dc]) => [r + dr, c + dc]);
}

function snapToGrid(proj) {
    let estR = Math.floor((proj.y - HEADER_HEIGHT) / (BUBBLE_DIAMETER * 0.85));
    let bestDist = Infinity;
    let bestPos = [0, 0];

    for (let r = Math.max(0, estR - 2); r <= estR + 3; r++) {
        for (let c = 0; c < GRID_COLS; c++) {
            if (grid[`${r},${c}`]) continue;
            if (r % 2 === 1 && c >= GRID_COLS - 1) continue;

            let offset = (r % 2 === 1) ? BUBBLE_RADIUS : 0;
            let bx = c * BUBBLE_DIAMETER + BUBBLE_RADIUS + offset;
            let by = r * (BUBBLE_DIAMETER * 0.85) + BUBBLE_RADIUS + HEADER_HEIGHT;

            let dist = Math.hypot(proj.x - bx, proj.y - by);
            if (dist < bestDist) {
                bestDist = dist;
                bestPos = [r, c];
            }
        }
    }
    return bestPos;
}

function landProjectile() {
    let [r, c] = snapToGrid(projectile);
    let bubble = new Bubble(projectile.ion, r, c);
    grid[`${r},${c}`] = bubble;
    projectile = null;

    let matched = processReaction(bubble);
    removeFloating();
    reloadShooter();

    if (!matched) {
        // Reset combo if no precipitation happened
        currentCombo = 0;
        document.getElementById('combo-badge').classList.add('hidden');
    }

    if (r >= GRID_ROWS - 1) gameOver = true;
    else if (grid[`${r},${c}`]) {
        if (grid[`${r},${c}`].y + BUBBLE_RADIUS > INTERNAL_HEIGHT - 100) {
            gameOver = true;
        }
    }
}

// Identify Precipitate Key from Ion Pairs or Clusters
function identifyPrecipitate(ionsList) {
    let sorted = [...ionsList].sort();

    // 3-ion cluster matching
    if (sorted.length === 3) {
        let counts = {};
        sorted.forEach(i => counts[i] = (counts[i] || 0) + 1);
        if (counts['Pb'] === 1 && counts['I'] === 2) return 'PbI2';
        if (counts['Ag'] === 2 && counts['S'] === 1) return 'Ag2S';
        if (counts['Cu1'] === 2 && counts['SO4'] === 1) return 'Cu2SO4';
        if (counts['Ag'] === 2 && counts['CO3'] === 1) return 'Ag2CO3';
        if (counts['Cu'] === 1 && counts['OH'] === 2) return 'Cu(OH)2';
        if (counts['Pb'] === 1 && counts['Cl'] === 2) return 'PbCl2';
        if (counts['Pb'] === 1 && counts['Br'] === 2) return 'PbBr2';
        if (counts['Mg'] === 1 && counts['OH'] === 2) return 'Mg(OH)2';
        if (counts['Pb'] === 1 && counts['OH'] === 2) return 'Pb(OH)2';
    }

    // 2-ion pair matching
    if (sorted.length === 2) {
        let pair = sorted.join(',');
        if (pair === 'Ag,Cl') return 'AgCl';
        if (pair === 'Ag,Br') return 'AgBr';
        if (pair === 'Ag,I') return 'AgI';
        if (pair === 'Cl,Cu1') return 'CuCl';
        if (pair === 'Br,Cu1') return 'CuBr';
        if (pair === 'Cu1,I') return 'CuI';
        if (pair === 'Pb,SO4') return 'PbSO4';
        if (pair === 'Ba,SO4') return 'BaSO4';
        if (pair === 'Pb,S') return 'PbS';
        if (pair === 'Cu,S') return 'CuS';
        if (pair === 'CO3,Mg') return 'MgCO3';
        if (pair === 'Ba,CO3') return 'BaCO3';
        if (pair === 'CO3,Cu') return 'CuCO3';
        if (pair === 'CO3,Pb') return 'PbCO3';
        if (pair === 'Ag,OH') return 'AgOH';
    }

    return null;
}

function processReaction(startBubble) {
    let startIon = startBubble.ion;
    let neighbors = getNeighbors(startBubble.r, startBubble.c);
    let toRemove = new Set();
    let detectedPrecipKey = null;

    const isHalogen = (i) => ['Cl', 'Br', 'I'].includes(i);
    const isAgCu1 = (i) => ['Ag', 'Cu1'].includes(i);

    // 1. Check 3-cluster patterns first (Higher priority & score!)
    let patterns = [];
    if (level === 1) {
        if (startIon === 'Cu1' || startIon === 'SO4') patterns.push({ Cu1: 2, SO4: 1 });
        if (startIon === 'Pb' || isHalogen(startIon)) {
            patterns.push({ Pb: 1, Cl: 2 });
            patterns.push({ Pb: 1, Br: 2 });
            patterns.push({ Pb: 1, I: 2 });
        }
    } else {
        if (['Cl', 'Pb'].includes(startIon)) patterns.push({ Cl: 2, Pb: 1 });
        if (['Br', 'Pb'].includes(startIon)) patterns.push({ Br: 2, Pb: 1 });
        if (['I', 'Pb'].includes(startIon)) patterns.push({ I: 2, Pb: 1 });
        if (['S', 'Ag'].includes(startIon)) patterns.push({ S: 1, Ag: 2 });
        if (['CO3', 'Ag'].includes(startIon)) patterns.push({ CO3: 1, Ag: 2 });
        if (['Mg', 'OH'].includes(startIon)) patterns.push({ Mg: 1, OH: 2 });
        if (['Cu', 'OH'].includes(startIon)) patterns.push({ Cu: 1, OH: 2 });
        if (['Pb', 'OH'].includes(startIon)) patterns.push({ Pb: 1, OH: 2 });
    }

    for (let pat of patterns) {
        let cluster = findCluster(startBubble, pat);
        if (cluster) {
            cluster.forEach(p => toRemove.add(p));
            let clusterIons = cluster.map(k => grid[k] ? grid[k].ion : null).filter(Boolean);
            detectedPrecipKey = identifyPrecipitate(clusterIons);
            break;
        }
    }

    // 2. If no 3-cluster, check 2-bubble pairs
    if (toRemove.size === 0) {
        for (let [nr, nc] of neighbors) {
            if (!grid[`${nr},${nc}`]) continue;
            let nIon = grid[`${nr},${nc}`].ion;
            let pair = [startIon, nIon].sort().join(',');

            let match = false;
            if (level === 1) {
                if (isAgCu1(startIon) && isHalogen(nIon)) match = true;
                if (isAgCu1(nIon) && isHalogen(startIon)) match = true;
                if (pair === 'Pb,SO4') match = true;
            } else {
                const P2 = [
                    'Ag,Cl', 'Ag,Br', 'Ag,I', 'Pb,S', 'Cu,S', 'Mg,CO3', 'Ba,CO3',
                    'Cu,CO3', 'Pb,CO3', 'Ba,SO4', 'Pb,SO4', 'Ag,OH'
                ].map(s => s.split(',').sort().join(','));
                if (P2.includes(pair)) match = true;
            }

            if (match) {
                toRemove.add(`${startBubble.r},${startBubble.c}`);
                toRemove.add(`${nr},${nc}`);
                detectedPrecipKey = identifyPrecipitate([startIon, nIon]);
                break;
            }
        }
    }

    if (toRemove.size > 0 && detectedPrecipKey) {
        handlePrecipitateElimination(detectedPrecipKey, startBubble.x, startBubble.y);
        toRemove.forEach(key => {
            if (grid[key]) {
                grid[key].state = 'popping';
                grid[key].popTimer = 30;
            }
        });
        return true;
    }
    return false;
}

// Handle Precipitation Elimination & Scoring
function handlePrecipitateElimination(precipKey, popX, popY) {
    const meta = PRECIPITATES_DATA[precipKey] || {
        name: precipKey,
        formula: precipKey,
        colorDesc: '沉澱',
        colorHex: '#ffffff',
        stars: 1,
        baseScore: 180,
        tier: 'cyan'
    };

    // Update Combo
    currentCombo++;
    maxCombo = Math.max(maxCombo, currentCombo);
    const comboMultiplier = 1 + (currentCombo - 1) * 0.25;
    const gainedPoints = Math.round(meta.baseScore * comboMultiplier);

    // Update Score
    score += gainedPoints;
    document.getElementById('score').innerText = score;
    document.getElementById('right-panel-score').innerText = score;
    document.getElementById('max-combo-val').innerText = maxCombo;

    // Show Combo Badge
    const comboBadge = document.getElementById('combo-badge');
    if (currentCombo > 1) {
        comboBadge.classList.remove('hidden');
        document.getElementById('combo-count').innerText = currentCombo;
    } else {
        comboBadge.classList.add('hidden');
    }

    // Update Precipitate Counts
    precipitateCounts[precipKey] = (precipitateCounts[precipKey] || 0) + 1;
    updatePrecipitateUI(precipKey);

    // Add Score Popup Animation
    let comboText = currentCombo > 1 ? `Combo x${currentCombo}` : meta.colorDesc;
    scorePopups.push(new ScorePopup(popX, popY - 20, `+${gainedPoints}`, '#00f2fe', `${meta.formula} ${comboText}`));

    // Log to Recent Feed
    addReactionFeedItem(meta, gainedPoints, currentCombo);
    updateRankDisplay();
}

function updatePrecipitateUI(justPoppedKey) {
    renderPrecipitateCards(justPoppedKey);

    const totalKinds = Object.keys(precipitateCounts).length;
    const totalCount = Object.values(precipitateCounts).reduce((a, b) => a + b, 0);

    document.getElementById('total-precip-kinds').innerText = totalKinds;
    document.getElementById('total-precip-count').innerText = totalCount;
    document.getElementById('mobile-precip-count').innerText = totalKinds;
}

function renderPrecipitateCards(highlightKey = null) {
    const container = document.getElementById('precipitate-card-list');
    if (!container) return;

    let html = '';
    const keys = Object.keys(PRECIPITATES_DATA);

    // Sort: unlocked first by count desc, then by stars desc
    keys.sort((a, b) => {
        const countA = precipitateCounts[a] || 0;
        const countB = precipitateCounts[b] || 0;
        if (countA !== countB) return countB - countA;
        return PRECIPITATES_DATA[b].stars - PRECIPITATES_DATA[a].stars;
    });

    for (let key of keys) {
        const data = PRECIPITATES_DATA[key];
        const count = precipitateCounts[key] || 0;
        const isUnlocked = count > 0;
        const isJustPopped = (key === highlightKey);

        const starsStr = '★'.repeat(data.stars);

        html += `
        <div class="precip-card ${isUnlocked ? 'unlocked' : ''} ${isJustPopped ? 'just-popped' : ''}" data-key="${key}">
            <div class="card-left">
                <span class="color-dot" style="background-color: ${data.colorHex};"></span>
                <div class="card-info">
                    <span class="formula-text">${data.formula}&#8595;</span>
                    <span class="name-text">${data.name}</span>
                    <span class="color-desc-tag">${data.colorDesc}</span>
                </div>
            </div>
            <div class="card-right">
                <span class="count-badge">&times; ${count}</span>
                <span class="card-stars">${starsStr}</span>
            </div>
        </div>`;
    }

    container.innerHTML = html;
}

function addReactionFeedItem(meta, pts, combo) {
    const feed = document.getElementById('reaction-feed');
    if (!feed) return;

    const empty = feed.querySelector('.feed-empty');
    if (empty) empty.remove();

    const item = document.createElement('div');
    item.className = `feed-item tier-${meta.tier}`;
    
    let comboBadge = combo > 1 ? `<span style="color:#f59e0b;font-weight:bold;margin-left:4px;">x${combo}</span>` : '';
    item.innerHTML = `
        <div class="feed-name">
            <span class="dot dot-${meta.tier === 'gold' ? 'gold' : meta.tier === 'purple' ? 'teal' : 'white'}"></span>
            ${meta.formula} ${meta.name} ${comboBadge}
        </div>
        <div class="feed-pts">+${pts}</div>
    `;

    feed.prepend(item);

    // Keep at most 6 recent items
    while (feed.children.length > 6) {
        feed.removeChild(feed.lastChild);
    }
}

function updateRankDisplay() {
    const rankEl = document.getElementById('player-rank');
    if (!rankEl) return;
    let rank = 'C';
    if (score >= 10000) rank = 'S+';
    else if (score >= 6000) rank = 'S';
    else if (score >= 3500) rank = 'A';
    else if (score >= 1800) rank = 'B';
    rankEl.innerText = rank;
}

function findCluster(startBubble, reqs) {
    let totalNeeded = Object.values(reqs).reduce((a, b) => a + b, 0);
    if (totalNeeded !== 3) return null;

    let startKey = `${startBubble.r},${startBubble.c}`;
    let neighbors = getNeighbors(startBubble.r, startBubble.c).filter(([r, c]) => grid[`${r},${c}`]);

    for (let i = 0; i < neighbors.length; i++) {
        for (let j = i + 1; j < neighbors.length; j++) {
            let n1 = neighbors[i];
            let n2 = neighbors[j];
            let set = [startKey, `${n1[0]},${n1[1]}`, `${n2[0]},${n2[1]}`];
            if (checkSet(set, reqs)) return set;
        }
    }

    for (let n1 of neighbors) {
        let n1Key = `${n1[0]},${n1[1]}`;
        let nn = getNeighbors(n1[0], n1[1]).filter(([r, c]) => grid[`${r},${c}`] && `${r},${c}` !== startKey);
        for (let n2 of nn) {
            let n2Key = `${n2[0]},${n2[1]}`;
            let set = [startKey, n1Key, n2Key];
            if (checkSet(set, reqs)) return set;
        }
    }
    return null;
}

function checkSet(keys, reqs) {
    let counts = {};
    for (let k of keys) {
        if (!grid[k]) return false;
        let ion = grid[k].ion;
        counts[ion] = (counts[ion] || 0) + 1;
    }
    for (let ion in reqs) {
        if (counts[ion] !== reqs[ion]) return false;
    }
    return true;
}

function removeFloating() {
    let visited = new Set();
    let q = [];
    for (let c = 0; c < GRID_COLS; c++) {
        if (grid[`0,${c}`]) {
            q.push([0, c]);
            visited.add(`0,${c}`);
        }
    }
    let head = 0;
    while (head < q.length) {
        let [r, c] = q[head++];
        for (let [nr, nc] of getNeighbors(r, c)) {
            let k = `${nr},${nc}`;
            if (grid[k] && !visited.has(k)) {
                visited.add(k);
                q.push([nr, nc]);
            }
        }
    }
    let droppedCount = 0;
    Object.keys(grid).forEach(key => {
        if (!visited.has(key)) {
            let b = grid[key];
            if (b.state !== 'popping') {
                fallingBubbles.push(new FallingBubble(b.ion, b.x, b.y));
                score += 80; // 80 pts per dropped bubble
                droppedCount++;
            }
            delete grid[key];
        }
    });

    if (droppedCount > 0) {
        totalDrops += droppedCount;
        document.getElementById('drop-count-val').innerText = `${totalDrops} 顆`;
        document.getElementById('score').innerText = score;
        document.getElementById('right-panel-score').innerText = score;
    }
}

function reloadShooter() {
    currentIon = nextIon;
    nextIon = next2Ion;
    next2Ion = nextIsCation ? getRandomCation() : getRandomAnion();
    nextIsCation = !nextIsCation;
}

function checkWin() {
    const allowed = (level === 1) ? ['Na', 'Cu', 'NO3'] : ['Na', 'NO3'];
    let remaining = Object.values(grid).filter(b => b.state !== 'popping');
    if (remaining.every(b => allowed.includes(b.ion))) {
        gameWon = true;
    }
}

function addRow() {
    let newGrid = {};
    for (let key in grid) {
        let b = grid[key];
        let nr = b.r + 1;
        if (nr % 2 === 1 && b.c >= GRID_COLS - 1) continue;
        if (nr >= GRID_ROWS - 1) gameOver = true;
        b.r = nr;
        b.updatePos();
        newGrid[`${nr},${b.c}`] = b;
    }
    grid = newGrid;
    let available = Array.from({ length: GRID_COLS }, (_, i) => i);
    available.sort(() => Math.random() - 0.5);
    for (let i = 0; i < 8; i++) {
        let c = available[i];
        let ion = (Math.random() < 0.5) ? getRandomCation() : getRandomAnion();
        grid[`0,${c}`] = new Bubble(ion, 0, c);
    }
}

// Main Update Loop
function update() {
    if (gameState !== 'PLAYING') return;

    if (gameWon) {
        gameState = 'WIN';
        document.getElementById('win-screen').classList.remove('hidden');
        document.getElementById('win-time').innerText = `通關時間: ${document.getElementById('time').innerText}`;
        document.getElementById('win-score').innerText = score;
        return;
    }
    if (gameOver) {
        gameState = 'GAME_OVER';
        document.getElementById('game-over-screen').classList.remove('hidden');
        document.getElementById('gameover-score').innerText = score;
        return;
    }

    if (!gameWon && !gameOver) {
        let elapsed = Math.floor((Date.now() - startTime) / 1000);
        let m = Math.floor(elapsed / 60).toString().padStart(2, '0');
        let s = (elapsed % 60).toString().padStart(2, '0');
        document.getElementById('time').innerText = `${m}:${s}`;
    }

    if (level === 3 && Date.now() - lastSpawnTime > 30000) {
        addRow();
        lastSpawnTime = Date.now();
    }

    // Decay recoil smoothly
    if (recoil > 0) {
        recoil *= 0.85;
        if (recoil < 0.2) recoil = 0;
    }

    if (projectile) {
        projectile.move();
        if (projectile.y < BUBBLE_RADIUS + HEADER_HEIGHT) {
            landProjectile();
        } else {
            let pr = BUBBLE_RADIUS * projectile.scale;
            for (let key in grid) {
                let b = grid[key];
                let dist = Math.hypot(projectile.x - b.x, projectile.y - b.y);
                if (dist < pr + BUBBLE_RADIUS - 5) {
                    landProjectile();
                    break;
                }
            }
        }
    }

    let popped = false;
    let toDelete = [];
    for (let key in grid) {
        let b = grid[key];
        if (b.state === 'popping') {
            b.popTimer--;
            if (b.popTimer <= 0) {
                toDelete.push(key);
                popped = true;
            }
        }
    }
    toDelete.forEach(k => {
        delete grid[k];
    });
    if (popped) removeFloating();
    checkWin();

    for (let i = fallingBubbles.length - 1; i >= 0; i--) {
        fallingBubbles[i].update();
        if (fallingBubbles[i].y > INTERNAL_HEIGHT + 50) {
            fallingBubbles.splice(i, 1);
        }
    }

    // Update Popups
    for (let i = scorePopups.length - 1; i >= 0; i--) {
        scorePopups[i].update();
        if (scorePopups[i].life <= 0) {
            scorePopups.splice(i, 1);
        }
    }
}

// Render Functions
function render() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    ctx.save();
    ctx.scale(scale, scale);

    // Separator line
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.15)';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(0, HEADER_HEIGHT);
    ctx.lineTo(INTERNAL_WIDTH, HEADER_HEIGHT);
    ctx.stroke();

    if (gameState === 'START') {
        ctx.restore();
        return;
    }

    // Danger Line
    const dangerY = (GRID_ROWS - 1) * (BUBBLE_DIAMETER * 0.85) + BUBBLE_RADIUS + HEADER_HEIGHT + BUBBLE_RADIUS;
    ctx.strokeStyle = 'rgba(239, 68, 68, 0.4)';
    ctx.lineWidth = 2;
    ctx.setLineDash([8, 8]);
    ctx.beginPath();
    ctx.moveTo(0, dangerY);
    ctx.lineTo(INTERNAL_WIDTH, dangerY);
    ctx.stroke();
    ctx.setLineDash([]);
    
    ctx.fillStyle = 'rgba(239, 68, 68, 0.25)';
    ctx.font = 'bold 16px "Noto Sans TC"';
    ctx.textAlign = 'center';
    ctx.fillText("⚠️ DANGER LINE ⚠️", INTERNAL_WIDTH / 2, dangerY - 8);

    // Draw Bubbles
    for (let key in grid) grid[key].draw();
    fallingBubbles.forEach(b => b.draw());

    // Cannon Position
    const sx = INTERNAL_WIDTH / 2;
    const sy = INTERNAL_HEIGHT - 65;

    // Laser Aiming Guide
    if (!projectile && gameState === 'PLAYING') {
        drawAimingLine(sx, sy, shooterAngle);
    }

    // Draw Modern Sci-Fi Cannon
    drawModernCannon(sx, sy, shooterAngle);

    // Draw Next Chamber Info
    drawNextChamber(sx, sy);

    // Draw Floating Score Popups
    scorePopups.forEach(p => p.draw());

    ctx.restore();
}

// Modern Sci-Fi High-Tech Chemical Cannon
function drawModernCannon(sx, sy, angle) {
    const time = Date.now() * 0.003;
    const pulse = (Math.sin(time) + 1) * 0.5;

    ctx.save();

    // 1. Base Mounting Platform (Stationary)
    // Outer Heavy Alloy Base
    const baseGrad = ctx.createRadialGradient(sx, sy, 10, sx, sy, 56);
    baseGrad.addColorStop(0, '#1e293b');
    baseGrad.addColorStop(0.7, '#0f172a');
    baseGrad.addColorStop(1, '#020617');
    ctx.fillStyle = baseGrad;
    ctx.beginPath();
    ctx.arc(sx, sy, 54, 0, Math.PI * 2);
    ctx.fill();

    // Outer Neon Ring (Pulsing Glow)
    ctx.strokeStyle = `rgba(0, 242, 254, ${0.4 + pulse * 0.4})`;
    ctx.lineWidth = 2.5;
    ctx.shadowColor = '#00f2fe';
    ctx.shadowBlur = 12 * pulse + 4;
    ctx.beginPath();
    ctx.arc(sx, sy, 52, 0, Math.PI * 2);
    ctx.stroke();
    ctx.shadowBlur = 0;

    // Precision Compass / Calibrator Ticks
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.2)';
    ctx.lineWidth = 1.5;
    for (let i = 0; i < 16; i++) {
        let tickAngle = (i / 16) * Math.PI * 2;
        let r1 = 44;
        let r2 = (i % 4 === 0) ? 50 : 47;
        ctx.beginPath();
        ctx.moveTo(sx + Math.cos(tickAngle) * r1, sy + Math.sin(tickAngle) * r1);
        ctx.lineTo(sx + Math.cos(tickAngle) * r2, sy + Math.sin(tickAngle) * r2);
        ctx.stroke();
    }

    // Inner Metallic Bearing Ring
    ctx.strokeStyle = '#475569';
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.arc(sx, sy, 36, 0, Math.PI * 2);
    ctx.stroke();

    // Central Plasma Reactor Core Glow
    const reactorGrad = ctx.createRadialGradient(sx, sy, 0, sx, sy, 22);
    reactorGrad.addColorStop(0, '#ffffff');
    reactorGrad.addColorStop(0.4, '#00f2fe');
    reactorGrad.addColorStop(0.8, '#0284c7');
    reactorGrad.addColorStop(1, 'rgba(2, 132, 199, 0)');
    ctx.fillStyle = reactorGrad;
    ctx.beginPath();
    ctx.arc(sx, sy, 22, 0, Math.PI * 2);
    ctx.fill();

    // 2. Rotating Turret Barrel with Recoil
    ctx.save();
    ctx.translate(sx, sy);
    ctx.rotate(-angle);

    // Apply Recoil shift backwards
    const recoilOffset = -recoil;
    ctx.translate(recoilOffset, 0);

    // Barrel Shadows
    ctx.shadowColor = 'rgba(0, 0, 0, 0.6)';
    ctx.shadowBlur = 8;
    ctx.shadowOffsetX = 3;
    ctx.shadowOffsetY = 3;

    // Heavy Armor Mantlet / Breech Block
    const breechGrad = ctx.createLinearGradient(-15, -26, -15, 26);
    breechGrad.addColorStop(0, '#334155');
    breechGrad.addColorStop(0.5, '#64748b');
    breechGrad.addColorStop(1, '#1e293b');
    ctx.fillStyle = breechGrad;
    roundRect(ctx, -15, -26, 30, 52, 6);
    ctx.fill();

    // Dual Ion Accelerator Barrel Rails
    const barrelGrad = ctx.createLinearGradient(0, -18, 0, 18);
    barrelGrad.addColorStop(0, '#1e293b');
    barrelGrad.addColorStop(0.2, '#475569');
    barrelGrad.addColorStop(0.5, '#94a3b8');
    barrelGrad.addColorStop(0.8, '#334155');
    barrelGrad.addColorStop(1, '#0f172a');

    ctx.fillStyle = barrelGrad;
    ctx.strokeStyle = '#0f172a';
    ctx.lineWidth = 1.5;

    // Main Extended Tube
    roundRect(ctx, 10, -18, 75, 36, 5);
    ctx.fill();
    ctx.stroke();

    // Energy Light Strips along Rails (Glowing Cyan/Blue)
    ctx.shadowBlur = 0;
    ctx.fillStyle = '#00f2fe';
    ctx.fillRect(15, -12, 60, 3);
    ctx.fillRect(15, 9, 60, 3);

    // Cooling Vents / Heat Sink Grilles
    ctx.fillStyle = '#090d16';
    for (let vx = 22; vx <= 65; vx += 9) {
        ctx.fillRect(vx, -7, 4, 14);
    }

    // Muzzle Converging Collar (Gun Tip)
    const muzzleGrad = ctx.createLinearGradient(82, -22, 82, 22);
    muzzleGrad.addColorStop(0, '#0284c7');
    muzzleGrad.addColorStop(0.5, '#38bdf8');
    muzzleGrad.addColorStop(1, '#0369a1');
    ctx.fillStyle = muzzleGrad;
    roundRect(ctx, 80, -21, 14, 42, 4);
    ctx.fill();

    // Muzzle Energy Glow Emitter Ring
    ctx.strokeStyle = '#00f2fe';
    ctx.lineWidth = 2.5;
    ctx.shadowColor = '#00f2fe';
    ctx.shadowBlur = 10;
    ctx.strokeRect(91, -19, 3, 38);
    ctx.shadowBlur = 0;

    ctx.restore(); // Restore Recoil and Rotation

    // 3. Current Ion Bubble Loaded inside the Turret
    if (!projectile) {
        let loadDist = 42 - recoil * 0.5;
        let bx = sx + Math.cos(angle) * loadDist;
        let by = sy - Math.sin(angle) * loadDist;
        drawBubble(bx, by, BUBBLE_RADIUS, currentIon);

        // Chamber Magnetic Focus Ring around the bubble
        ctx.strokeStyle = `rgba(0, 242, 254, ${0.5 + pulse * 0.3})`;
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.arc(bx, by, BUBBLE_RADIUS + 4, 0, Math.PI * 2);
        ctx.stroke();
    } else {
        projectile.draw();
    }

    ctx.restore();
}

// Utility: Rounded Rectangle
function roundRect(ctx, x, y, width, height, radius) {
    ctx.beginPath();
    ctx.moveTo(x + radius, y);
    ctx.lineTo(x + width - radius, y);
    ctx.quadraticCurveTo(x + width, y, x + width, y + radius);
    ctx.lineTo(x + width, y + height - radius);
    ctx.quadraticCurveTo(x + width, y + height, x + width - radius, y + height);
    ctx.lineTo(x + radius, y + height);
    ctx.quadraticCurveTo(x, y + height, x, y + height - radius);
    ctx.lineTo(x, y + radius);
    ctx.quadraticCurveTo(x, y, x + radius, y);
    ctx.closePath();
}

// Modern Next Ion Chamber HUD
function drawNextChamber(sx, sy) {
    const nextX = sx + 130;
    const nextY = sy - 15;

    ctx.save();

    // Hologram Plate Background
    ctx.fillStyle = 'rgba(15, 23, 42, 0.75)';
    ctx.strokeStyle = 'rgba(0, 210, 255, 0.3)';
    ctx.lineWidth = 1.5;
    roundRect(ctx, nextX - 45, nextY - 55, 125, 95, 12);
    ctx.fill();
    ctx.stroke();

    // Title Tag
    ctx.fillStyle = '#00f2fe';
    ctx.font = 'bold 11px "Noto Sans TC"';
    ctx.textAlign = 'center';
    ctx.fillText("CHAMBER", nextX - 5, nextY - 40);

    // NEXT Bubble
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.2)';
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.arc(nextX - 5, nextY + 5, 28, 0, Math.PI * 2);
    ctx.stroke();
    drawBubble(nextX - 5, nextY + 5, BUBBLE_RADIUS * 0.7, nextIon);

    // LATER Bubble
    ctx.fillStyle = 'rgba(255, 255, 255, 0.4)';
    ctx.font = '10px "Noto Sans TC"';
    ctx.fillText("NEXT", nextX + 50, nextY - 18);
    drawBubble(nextX + 50, nextY + 8, BUBBLE_RADIUS * 0.45, next2Ion);

    ctx.restore();
}

// Laser Sighting Line with Glow
function drawAimingLine(cx, cy, angle) {
    let x = cx;
    let y = cy;
    let dx = Math.cos(angle);
    let dy = -Math.sin(angle);
    let step = 10;
    let maxSteps = 150;

    ctx.save();
    ctx.beginPath();
    ctx.moveTo(x, y);
    ctx.strokeStyle = 'rgba(0, 242, 254, 0.65)';
    ctx.shadowColor = '#00f2fe';
    ctx.shadowBlur = 6;
    ctx.lineWidth = 2.5;
    ctx.setLineDash([6, 6]);

    let endX = x;
    let endY = y;

    for (let i = 0; i < maxSteps; i++) {
        x += dx * step;
        y += dy * step;
        if (x <= BUBBLE_RADIUS || x >= INTERNAL_WIDTH - BUBBLE_RADIUS) {
            dx = -dx;
            x = Math.max(BUBBLE_RADIUS, Math.min(x, INTERNAL_WIDTH - BUBBLE_RADIUS));
            ctx.lineTo(x, y);
        }
        if (y <= HEADER_HEIGHT + BUBBLE_RADIUS) {
            ctx.lineTo(x, y);
            endX = x;
            endY = y;
            break;
        }
        let collided = false;
        for (let key in grid) {
            let b = grid[key];
            let dist = Math.hypot(x - b.x, y - b.y);
            if (dist < BUBBLE_DIAMETER - 5) {
                collided = true;
                break;
            }
        }
        if (collided) {
            ctx.lineTo(x, y);
            endX = x;
            endY = y;
            break;
        }
        ctx.lineTo(x, y);
        endX = x;
        endY = y;
    }
    ctx.stroke();
    ctx.setLineDash([]);

    // Impact Laser Dot Indicator
    ctx.fillStyle = '#ffffff';
    ctx.beginPath();
    ctx.arc(endX, endY, 4, 0, Math.PI * 2);
    ctx.fill();

    ctx.strokeStyle = '#00f2fe';
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.arc(endX, endY, 8, 0, Math.PI * 2);
    ctx.stroke();

    ctx.restore();
}

// Input Handling
let lastTouchX = null;
let isDragging = false;
let startX = 0;
let startY = 0;

function fireProjectile() {
    if (!projectile && gameState === 'PLAYING') {
        const sx = INTERNAL_WIDTH / 2;
        const sy = INTERNAL_HEIGHT - 65;
        projectile = new Projectile(currentIon, sx, sy, shooterAngle);
        recoil = 12; // Trigger cannon recoil animation
    }
}

function handleInteractionStart(e) {
    if (gameState !== 'PLAYING') return;
    const touch = e.touches ? e.touches[0] : e;
    startX = touch.clientX;
    startY = touch.clientY;
    lastTouchX = startX;
    isDragging = false;
}

function handleInteractionMove(e) {
    if (gameState !== 'PLAYING') return;
    
    const touch = e.touches ? e.touches[0] : e;
    const currentX = touch.clientX;
    const currentY = touch.clientY;
    
    const dist = Math.hypot(currentX - startX, currentY - startY);
    if (dist > 5) {
        isDragging = true;
    }

    if (isDragging && lastTouchX !== null) {
        const deltaX = currentX - lastTouchX;
        const sensitivity = 0.005; 
        shooterAngle -= deltaX * sensitivity;
        shooterAngle = Math.max(0.12, Math.min(Math.PI - 0.12, shooterAngle));
    }
    
    lastTouchX = currentX;
}

function handleInteractionEnd(e) {
    if (gameState !== 'PLAYING') return;
    
    if (!isDragging) {
        fireProjectile();
    }
    
    lastTouchX = null;
    isDragging = false;
}

// Drawer Toggle Handlers (for mobile/tablet)
function setupDrawerHandlers() {
    const toggleLeft = document.getElementById('toggle-left-btn');
    const toggleRight = document.getElementById('toggle-right-btn');
    const leftSidebar = document.getElementById('left-sidebar');
    const rightSidebar = document.getElementById('right-sidebar');

    if (toggleLeft && leftSidebar) {
        toggleLeft.addEventListener('click', (e) => {
            e.stopPropagation();
            leftSidebar.classList.toggle('drawer-open');
            if (rightSidebar) rightSidebar.classList.remove('drawer-open');
        });
    }

    if (toggleRight && rightSidebar) {
        toggleRight.addEventListener('click', (e) => {
            e.stopPropagation();
            rightSidebar.classList.toggle('drawer-open');
            if (leftSidebar) leftSidebar.classList.remove('drawer-open');
        });
    }

    document.querySelectorAll('.close-drawer-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const targetId = btn.getAttribute('data-target');
            const targetEl = document.getElementById(targetId);
            if (targetEl) targetEl.classList.remove('drawer-open');
        });
    });

    // Close drawers when clicking canvas
    canvas.addEventListener('click', () => {
        if (leftSidebar) leftSidebar.classList.remove('drawer-open');
        if (rightSidebar) rightSidebar.classList.remove('drawer-open');
    });
}

// Window Event Listeners
window.addEventListener('resize', resizeCanvas);

// Touch Events
canvas.addEventListener('touchstart', (e) => {
    e.preventDefault();
    handleInteractionStart(e);
}, { passive: false });

canvas.addEventListener('touchmove', (e) => {
    e.preventDefault();
    handleInteractionMove(e);
}, { passive: false });

canvas.addEventListener('touchend', (e) => {
    e.preventDefault();
    handleInteractionEnd();
}, { passive: false });

// Mouse Events
canvas.addEventListener('mousedown', handleInteractionStart);
window.addEventListener('mousemove', handleInteractionMove);
window.addEventListener('mouseup', handleInteractionEnd);

// Keyboard Events
window.addEventListener('keydown', e => {
    if (gameState === 'PLAYING') {
        if (e.code === 'ArrowLeft') shooterAngle = Math.min(Math.PI - 0.12, shooterAngle + 0.08);
        if (e.code === 'ArrowRight') shooterAngle = Math.max(0.12, shooterAngle - 0.08);
        if (e.code === 'Space' && !projectile) {
            fireProjectile();
        }
    }
});

// UI Buttons
document.getElementById('start-btn').addEventListener('click', () => {
    document.getElementById('start-screen').classList.add('hidden');
    gameState = 'PLAYING';
    resetGame(1);
});

document.getElementById('restart-btn').addEventListener('click', () => {
    document.getElementById('game-over-screen').classList.add('hidden');
    gameState = 'PLAYING';
    resetGame();
});

document.getElementById('next-level-btn').addEventListener('click', () => {
    document.getElementById('win-screen').classList.add('hidden');
    gameState = 'PLAYING';
    level = Math.min(3, level + 1);
    resetGame();
});

document.getElementById('reset-btn').addEventListener('click', () => {
    resetGame();
});

// Initialization
setupDrawerHandlers();
resizeCanvas();
renderPrecipitateCards();

function gameLoop() {
    update();
    render();
    requestAnimationFrame(gameLoop);
}
gameLoop();
