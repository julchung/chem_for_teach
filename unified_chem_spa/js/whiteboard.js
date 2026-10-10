/**
 * 高中化學學習網 - 手寫電子白板模組 (whiteboard.js)
 * 核心升級：
 * 1. 向量世界座標系統 (Document Coordinates)：手寫筆跡精準黏附於講義、例題演算區
 * 2. 隨頁面滾動即時同步重繪 (Scroll-aware Redraw)：畫面捲動時筆跡自然跟著滑動，絕不固定停滯
 * 3. 支援滑鼠、iPad/觸控筆、筆刷顏色、筆刷粗細、橡皮擦、復原 (Undo) 與一鍵全清
 */

class WhiteboardController {
  constructor() {
    this.canvas = null;
    this.ctx = null;
    this.isDrawingMode = false;
    this.isDrawing = false;
    this.drawMode = 'pen'; // 'pen' | 'eraser'
    this.penColor = '#38bdf8'; // 預設天藍色
    this.penSize = 3;
    
    // 筆劃紀錄陣列：[{ mode, color, size, points: [{x, y}] }]
    this.strokes = [];
    this.currentStroke = null;
    this.lastDocX = 0;
    this.lastDocY = 0;
    this.redrawScheduled = false;
    this.externalScrollX = null;
    this.externalScrollY = null;
  }

  init() {
    this.canvas = document.getElementById('whiteboard-canvas') || document.getElementById('drawing-layer');
    if (!this.canvas) return;
    this.ctx = this.canvas.getContext('2d');

    this.resizeCanvas();
    window.addEventListener('resize', () => this.resizeCanvas());

    // 監聽視窗捲動事件，筆跡跟隨畫面自然捲動
    window.addEventListener('scroll', () => this.requestRedraw(), { passive: true });

    // 觸控與滑鼠事件綁定
    this.canvas.addEventListener('mousedown', (e) => this.startDrawing(e));
    this.canvas.addEventListener('mousemove', (e) => this.draw(e));
    this.canvas.addEventListener('mouseup', () => this.stopDrawing());
    this.canvas.addEventListener('mouseleave', () => this.stopDrawing());

    this.canvas.addEventListener('touchstart', (e) => {
      if (!this.isDrawingMode) return;
      e.preventDefault();
      this.startDrawing(e);
    }, { passive: false });

    this.canvas.addEventListener('touchmove', (e) => {
      if (!this.isDrawingMode) return;
      e.preventDefault();
      this.draw(e);
    }, { passive: false });

    this.canvas.addEventListener('touchend', () => this.stopDrawing());

    // 綁定工具列控制項
    this.bindToolbar();
  }

  resizeCanvas() {
    if (!this.canvas) return;
    this.canvas.width = window.innerWidth;
    this.canvas.height = window.innerHeight;
    this.redraw();
  }

  // 取得相對於整個網頁文件頂端的「世界座標 (Document Coordinates)」
  getDocCoords(e) {
    const clientX = e.touches ? e.touches[0].clientX : e.clientX;
    const clientY = e.touches ? e.touches[0].clientY : e.clientY;
    const scrollX = this.externalScrollX !== null ? this.externalScrollX : (window.pageXOffset || document.documentElement.scrollLeft || 0);
    const scrollY = this.externalScrollY !== null ? this.externalScrollY : (window.pageYOffset || document.documentElement.scrollTop || 0);
    return [clientX + scrollX, clientY + scrollY];
  }

  startDrawing(e) {
    if (!this.isDrawingMode) return;
    this.isDrawing = true;
    const [docX, docY] = this.getDocCoords(e);
    this.lastDocX = docX;
    this.lastDocY = docY;

    this.currentStroke = {
      mode: this.drawMode,
      color: this.penColor,
      size: this.penSize,
      points: [{ x: docX, y: docY }]
    };
    this.strokes.push(this.currentStroke);

    // 繪製初始接觸點（相對於 viewport）
    const scrollX = this.externalScrollX !== null ? this.externalScrollX : (window.pageXOffset || document.documentElement.scrollLeft || 0);
    const scrollY = this.externalScrollY !== null ? this.externalScrollY : (window.pageYOffset || document.documentElement.scrollTop || 0);
    const viewX = docX - scrollX;
    const viewY = docY - scrollY;

    this.ctx.beginPath();
    this.ctx.moveTo(viewX, viewY);
    this.ctx.lineTo(viewX + 0.1, viewY + 0.1);

    if (this.drawMode === 'eraser') {
      this.ctx.globalCompositeOperation = 'destination-out';
      this.ctx.lineWidth = this.penSize * 10;
    } else {
      this.ctx.globalCompositeOperation = 'source-over';
      this.ctx.strokeStyle = this.penColor;
      this.ctx.lineWidth = this.penSize;
    }
    this.ctx.lineCap = 'round';
    this.ctx.lineJoin = 'round';
    this.ctx.stroke();
  }

  draw(e) {
    if (!this.isDrawing || !this.isDrawingMode || !this.currentStroke) return;
    const [docX, docY] = this.getDocCoords(e);
    this.currentStroke.points.push({ x: docX, y: docY });

    const scrollX = this.externalScrollX !== null ? this.externalScrollX : (window.pageXOffset || document.documentElement.scrollLeft || 0);
    const scrollY = this.externalScrollY !== null ? this.externalScrollY : (window.pageYOffset || document.documentElement.scrollTop || 0);

    const fromX = this.lastDocX - scrollX;
    const fromY = this.lastDocY - scrollY;
    const toX = docX - scrollX;
    const toY = docY - scrollY;

    this.ctx.beginPath();
    this.ctx.moveTo(fromX, fromY);
    this.ctx.lineTo(toX, toY);

    if (this.drawMode === 'eraser') {
      this.ctx.globalCompositeOperation = 'destination-out';
      this.ctx.lineWidth = this.penSize * 10;
    } else {
      this.ctx.globalCompositeOperation = 'source-over';
      this.ctx.strokeStyle = this.penColor;
      this.ctx.lineWidth = this.penSize;
    }

    this.ctx.lineCap = 'round';
    this.ctx.lineJoin = 'round';
    this.ctx.stroke();

    this.lastDocX = docX;
    this.lastDocY = docY;
  }

  stopDrawing() {
    if (this.isDrawing) {
      this.isDrawing = false;
      this.currentStroke = null;
      // 停止時觸發一次精確重繪，平滑路徑
      this.requestRedraw();
    }
  }

  // 透過 requestAnimationFrame 調度重繪，保證 60fps / 120fps 高刷捲動極致流暢
  requestRedraw() {
    if (this.redrawScheduled) return;
    this.redrawScheduled = true;
    window.requestAnimationFrame(() => {
      this.redrawScheduled = false;
      this.redraw();
    });
  }

  // 外部同步捲動位置 (用於 iframe 等容器捲動同步)
  syncScroll(x, y) {
    this.externalScrollX = x;
    this.externalScrollY = y;
    this.requestRedraw();
  }

  // 核心：將世界座標轉換為當前視窗的可見筆跡進行重繪
  redraw() {
    if (!this.ctx || !this.canvas) return;
    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

    if (this.strokes.length === 0) return;

    const scrollX = this.externalScrollX !== null ? this.externalScrollX : (window.pageXOffset || document.documentElement.scrollLeft || 0);
    const scrollY = this.externalScrollY !== null ? this.externalScrollY : (window.pageYOffset || document.documentElement.scrollTop || 0);
    const viewW = this.canvas.width;
    const viewH = this.canvas.height;

    this.ctx.save();
    // 將世界座標平移至當前視窗偏移量
    this.ctx.translate(-scrollX, -scrollY);

    for (const stroke of this.strokes) {
      if (!stroke.points || stroke.points.length === 0) continue;

      if (stroke.mode === 'eraser') {
        this.ctx.globalCompositeOperation = 'destination-out';
        this.ctx.lineWidth = stroke.size * 10;
      } else {
        this.ctx.globalCompositeOperation = 'source-over';
        this.ctx.strokeStyle = stroke.color;
        this.ctx.lineWidth = stroke.size;
      }

      this.ctx.lineCap = 'round';
      this.ctx.lineJoin = 'round';

      this.ctx.beginPath();
      const pts = stroke.points;
      this.ctx.moveTo(pts[0].x, pts[0].y);

      if (pts.length === 1) {
        this.ctx.lineTo(pts[0].x + 0.1, pts[0].y + 0.1);
      } else {
        for (let i = 1; i < pts.length; i++) {
          this.ctx.lineTo(pts[i].x, pts[i].y);
        }
      }
      this.ctx.stroke();
    }

    this.ctx.restore();
  }

  // 復原上一步筆跡
  undo() {
    if (this.strokes.length > 0) {
      this.strokes.pop();
      this.requestRedraw();
    }
  }

  // 全清筆跡
  clear() {
    this.strokes = [];
    if (this.ctx && this.canvas) {
      this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    }
  }

  bindToolbar() {
    const btnDraw = document.getElementById('btn-draw-toggle');
    const colorPicker = document.getElementById('color-picker-group');
    const sizePicker = document.getElementById('size-picker-group');
    const eraserGroup = document.getElementById('eraser-group');
    const btnEraser = document.getElementById('btn-eraser-tool');
    const btnUndo = document.getElementById('btn-undo-tool');
    const btnClear = document.getElementById('btn-clear-canvas');
    const penSizeInput = document.getElementById('pen-size-slider');

    if (btnDraw) {
      btnDraw.addEventListener('click', () => {
        this.isDrawingMode = !this.isDrawingMode;
        this.canvas.classList.toggle('active', this.isDrawingMode);
        btnDraw.classList.toggle('active-tool', this.isDrawingMode);

        const show = this.isDrawingMode ? 'flex' : 'none';
        if (colorPicker) colorPicker.style.display = show;
        if (sizePicker) sizePicker.style.display = show;
        if (eraserGroup) eraserGroup.style.display = show;

        if (this.isDrawingMode) {
          this.drawMode = 'pen';
          if (btnEraser) btnEraser.classList.remove('active-tool');
        }
      });
    }

    if (btnEraser) {
      btnEraser.addEventListener('click', () => {
        this.drawMode = (this.drawMode === 'eraser' ? 'pen' : 'eraser');
        btnEraser.classList.toggle('active-tool', this.drawMode === 'eraser');
      });
    }

    if (btnUndo) {
      btnUndo.addEventListener('click', () => {
        this.undo();
      });
    }

    if (btnClear) {
      btnClear.addEventListener('click', () => {
        if (confirm('確定要清除畫布上的所有手寫筆記嗎？')) {
          this.clear();
        }
      });
    }

    if (penSizeInput) {
      penSizeInput.addEventListener('input', (e) => {
        this.penSize = parseInt(e.target.value) || 3;
      });
    }

    // 色盤選擇
    document.querySelectorAll('.color-dot').forEach(dot => {
      dot.addEventListener('click', () => {
        document.querySelectorAll('.color-dot').forEach(d => d.classList.remove('selected'));
        dot.classList.add('selected');
        this.penColor = dot.dataset.color;
        this.drawMode = 'pen';
        if (btnEraser) btnEraser.classList.remove('active-tool');
      });
    });

    // 工具列拖曳支援
    this.initToolbarDraggable();
  }

  initToolbarDraggable() {
    const toolbar = document.getElementById('floating-toolbar');
    const handle = document.getElementById('drag-handle-bar');
    if (!toolbar || !handle) return;

    let isDragging = false;
    let offsetY = 0;

    const startDrag = (clientY) => {
      isDragging = true;
      offsetY = clientY - toolbar.offsetTop;
    };

    const doDrag = (clientY) => {
      if (!isDragging) return;
      let newY = clientY - offsetY;
      const maxY = window.innerHeight - toolbar.offsetHeight - 10;
      if (newY < 10) newY = 10;
      if (newY > maxY) newY = maxY;
      toolbar.style.top = `${newY}px`;
      toolbar.style.transform = 'none';
    };

    const stopDrag = () => { isDragging = false; };

    handle.addEventListener('mousedown', (e) => startDrag(e.clientY));
    window.addEventListener('mousemove', (e) => doDrag(e.clientY));
    window.addEventListener('mouseup', stopDrag);

    handle.addEventListener('touchstart', (e) => startDrag(e.touches[0].clientY));
    window.addEventListener('touchmove', (e) => doDrag(e.touches[0].clientY));
    window.addEventListener('touchend', stopDrag);
  }
}

// 建立全域實例
window.whiteboard = new WhiteboardController();
