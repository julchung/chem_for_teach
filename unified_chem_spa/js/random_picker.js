/**
 * 高中化學學習網 - 隨機抽號小工具模組 (random_picker.js)
 * 課堂互動抽籤，支援自訂總人數、動態跳號動效、不重複抽取與重設
 */

class RandomPicker {
  constructor() {
    this.total = 40;
    this.drawnSet = new Set();
    this.animTimer = null;
    this.isDrawing = false;
  }

  init() {
    this.modal = document.getElementById('random-draw-modal');
    this.btnOpen = document.getElementById('btn-open-draw');
    this.btnClose = document.getElementById('btn-close-draw');
    this.btnDraw = document.getElementById('btn-do-draw');
    this.btnReset = document.getElementById('btn-reset-draw');
    this.totalInput = document.getElementById('draw-total-input');
    this.ballsContainer = document.getElementById('draw-balls-container');
    this.winnerBanner = document.getElementById('draw-winner-banner');

    if (this.btnOpen) {
      this.btnOpen.addEventListener('click', () => this.open());
    }
    if (this.btnClose) {
      this.btnClose.addEventListener('click', () => this.close());
    }
    if (this.btnDraw) {
      this.btnDraw.addEventListener('click', () => this.draw());
    }
    if (this.btnReset) {
      this.btnReset.addEventListener('click', () => this.reset());
    }
    if (this.totalInput) {
      this.totalInput.addEventListener('change', () => {
        this.total = Math.max(1, Math.min(100, parseInt(this.totalInput.value) || 40));
        this.totalInput.value = this.total;
        this.reset();
      });
    }

    if (this.modal) {
      this.modal.addEventListener('click', (e) => {
        if (e.target === this.modal) this.close();
      });
    }

    this.renderBalls();
  }

  open() {
    if (!this.modal) return;
    this.modal.style.display = 'flex';
  }

  close() {
    if (!this.modal) return;
    this.modal.style.display = 'none';
  }

  renderBalls() {
    if (!this.ballsContainer) return;
    this.ballsContainer.innerHTML = '';

    for (let i = 1; i <= this.total; i++) {
      const ball = document.createElement('div');
      ball.className = 'draw-ball' + (this.drawnSet.has(i) ? ' drawn' : '');
      ball.id = `draw-ball-${i}`;
      ball.textContent = i;
      this.ballsContainer.appendChild(ball);
    }
  }

  draw() {
    if (this.isDrawing) return;

    // 找出未抽出的號碼
    const available = [];
    for (let i = 1; i <= this.total; i++) {
      if (!this.drawnSet.has(i)) available.push(i);
    }

    if (available.length === 0) {
      alert('所有號碼皆已抽完！為您重新洗牌。');
      this.reset();
      return;
    }

    this.isDrawing = true;
    this.btnDraw.disabled = true;
    if (this.winnerBanner) {
      this.winnerBanner.textContent = '抽號中... 🎲';
      this.winnerBanner.classList.add('rolling');
    }

    const winner = available[Math.floor(Math.random() * available.length)];
    let ticks = 0;
    const maxTicks = 24;

    const undrawnBalls = Array.from(document.querySelectorAll('.draw-ball:not(.drawn)'));

    if (this.animTimer) clearInterval(this.animTimer);

    this.animTimer = setInterval(() => {
      undrawnBalls.forEach(b => b.classList.remove('flicker'));
      const randBall = undrawnBalls[Math.floor(Math.random() * undrawnBalls.length)];
      if (randBall) randBall.classList.add('flicker');

      ticks++;
      if (ticks >= maxTicks) {
        clearInterval(this.animTimer);
        this.animTimer = null;
        undrawnBalls.forEach(b => b.classList.remove('flicker'));

        // 揭曉得主
        const winBall = document.getElementById(`draw-ball-${winner}`);
        if (winBall) {
          winBall.classList.add('winner');
        }

        if (this.winnerBanner) {
          this.winnerBanner.innerHTML = `🎉 恭喜 <span style="color:#facc15;font-size:2rem;font-weight:bold;">${winner}</span> 號同學！`;
          this.winnerBanner.classList.remove('rolling');
        }

        this.drawnSet.add(winner);

        setTimeout(() => {
          if (winBall) {
            winBall.classList.remove('winner');
            winBall.classList.add('drawn');
          }
          this.isDrawing = false;
          this.btnDraw.disabled = false;
        }, 1200);
      }
    }, 60);
  }

  reset() {
    this.drawnSet.clear();
    this.renderBalls();
    if (this.winnerBanner) {
      this.winnerBanner.textContent = '點擊「開始抽號」進行隨機選號';
      this.winnerBanner.classList.remove('rolling');
    }
  }
}

window.randomPicker = new RandomPicker();
