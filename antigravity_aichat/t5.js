
        // ─── Initialization ───────────────────────────────────────────────
        mermaid.initialize({ startOnLoad: false, theme: 'default', securityLevel: 'loose' });

        const CANVAS_SIZE = 4000;
        const viewport = document.getElementById('viewport');
        const transformContainer = document.getElementById('transform-container');
        const bgCanvas = document.getElementById('bg-canvas');
        const drawingCanvas = document.getElementById('drawing-canvas');
        const bgCtx = bgCanvas.getContext('2d');
        const drawCtx = drawingCanvas.getContext('2d');

        let scale = 1, translateX = 0, translateY = 0;
        let currentMode = 'pen';
        let isDrawing = false, isPanning = false;
        let lastPanX = 0, lastPanY = 0;
        let lastCropCenter = null; // Store crop center for placing tags

        // ─── Layout Resizer ───────────────────────────────────────────────
        const layoutResizer = document.getElementById('layout-resizer');
        const rightPanel = document.getElementById('right-panel');
        let isResizingPanel = false;

        layoutResizer.addEventListener('mousedown', (e) => {
            isResizingPanel = true;
            layoutResizer.classList.add('active');
            document.body.style.cursor = 'col-resize';
            document.body.style.userSelect = 'none';
        });

        document.addEventListener('mousemove', (e) => {
            if (!isResizingPanel) return;
            const newWidth = document.body.clientWidth - e.clientX;
            // Bound between 250px and 50% of screen
            if (newWidth >= 250 && newWidth <= document.body.clientWidth * 0.6) {
                rightPanel.style.flex = `0 0 ${newWidth}px`;
            }
        });

        document.addEventListener('mouseup', () => {
            if (isResizingPanel) {
                isResizingPanel = false;
                layoutResizer.classList.remove('active');
                document.body.style.cursor = '';
                document.body.style.userSelect = '';
                centerCanvas(); // optional: recenter canvas after resize
            }
        });

        // ─── Transform Logic ──────────────────────────────────────────────
        function centerCanvas() {
            const r = viewport.getBoundingClientRect();
            translateX = (r.width - CANVAS_SIZE) / 2;
            translateY = (r.height - CANVAS_SIZE) / 2;
            updateTransform();
        }
        window.addEventListener('load', centerCanvas);

        function updateTransform() {
            transformContainer.style.transform = `translate(${translateX}px, ${translateY}px) scale(${scale})`;
            viewport.style.backgroundPosition = `${translateX}px ${translateY}px`;
            viewport.style.backgroundSize = `${20 * scale}px ${20 * scale}px`;
        }

        function getCanvasCoords(e) {
            const r = viewport.getBoundingClientRect();
            return {
                x: (e.clientX - r.left - translateX) / scale,
                y: (e.clientY - r.top  - translateY) / scale
            };
        }

        // ─── Zoom (scroll wheel) ──────────────────────────────────────────
        viewport.addEventListener('wheel', (e) => {
            if (isCropping) return;
            e.preventDefault();
            const factor = Math.exp((e.deltaY < 0 ? 1 : -1) * 0.1);
            const r = viewport.getBoundingClientRect();
            const mx = e.clientX - r.left, my = e.clientY - r.top;
            const cx = (mx - translateX) / scale, cy = (my - translateY) / scale;
            scale = Math.min(5, Math.max(0.15, scale * factor));
            translateX = mx - cx * scale;
            translateY = my - cy * scale;
            updateTransform();
        }, { passive: false });

        // ─── Pan & Draw ───────────────────────────────────────────────────
        viewport.addEventListener('mousedown', (e) => {
            if (currentMode === 'crop') return;
            if (currentMode === 'pan' || e.button === 1 || e.button === 2) {
                isPanning = true; lastPanX = e.clientX; lastPanY = e.clientY;
                viewport.style.cursor = 'grabbing'; return;
            }
            isDrawing = true; draw(e, true);
        });
        viewport.addEventListener('mousemove', (e) => {
            if (isPanning) {
                translateX += e.clientX - lastPanX; translateY += e.clientY - lastPanY;
                lastPanX = e.clientX; lastPanY = e.clientY;
                updateTransform(); return;
            }
            if (isDrawing) draw(e, false);
        });
        viewport.addEventListener('mouseup', () => {
            isPanning = false;
            if (isDrawing) { isDrawing = false; drawCtx.beginPath(); }
            if (currentMode === 'pan') viewport.style.cursor = 'grab';
        });
        viewport.addEventListener('contextmenu', e => e.preventDefault());

        function draw(e, isStart) {
            const pos = getCanvasCoords(e);
            drawCtx.lineWidth = currentMode === 'eraser'
                ? document.getElementById('eraser-width').value
                : document.getElementById('pen-width').value;
            drawCtx.lineCap = 'round'; drawCtx.lineJoin = 'round';
            drawCtx.globalCompositeOperation = currentMode === 'eraser' ? 'destination-out' : 'source-over';
            drawCtx.strokeStyle = currentMode === 'eraser' ? 'rgba(0,0,0,1)' : document.getElementById('color-picker').value;
            if (isStart) { drawCtx.beginPath(); drawCtx.moveTo(pos.x, pos.y); }
            else { drawCtx.lineTo(pos.x, pos.y); drawCtx.stroke(); drawCtx.beginPath(); drawCtx.moveTo(pos.x, pos.y); }
        }

        // Clear Canvas and Chat
        document.getElementById('btn-clear')?.addEventListener('click', () => {
            if (confirm('確定要清空畫布與對話紀錄嗎？')) {
                drawCtx.clearRect(0, 0, CANVAS_SIZE, CANVAS_SIZE);
                document.getElementById('chat-messages').innerHTML = '';
                document.getElementById('tags-container').innerHTML = '';
            }
        });

        // ─── Toolbar ──────────────────────────────────────────────────────
        const btnPen = document.getElementById('btn-pen');
        const btnEraser = document.getElementById('btn-eraser');
        const btnPan = document.getElementById('btn-pan');

        function setTool(mode, activeBtn) {
            currentMode = mode;
            [btnPen, btnEraser, btnPan].forEach(b => { b.classList.remove('active'); b.style.transform = ''; });
            activeBtn.classList.add('active'); activeBtn.style.transform = 'scale(1.15)';
            document.getElementById('pen-popup').style.display    = mode === 'pen'    ? 'block' : 'none';
            document.getElementById('eraser-popup').style.display = mode === 'eraser' ? 'block' : 'none';
            if (mode === 'pan') { viewport.style.cursor = 'grab'; drawingCanvas.style.pointerEvents = 'none'; }
            else { viewport.style.cursor = 'crosshair'; drawingCanvas.style.pointerEvents = 'auto'; }
        }

        btnPen.addEventListener('click',    e => { setTool('pen', btnPen); e.stopPropagation(); });
        btnEraser.addEventListener('click', e => { setTool('eraser', btnEraser); e.stopPropagation(); });
        btnPan.addEventListener('click',    e => { setTool('pan', btnPan); e.stopPropagation(); });
        document.addEventListener('click', (e) => {
            if (!e.target.closest('.tool-group')) {
                document.getElementById('pen-popup').style.display = 'none';
                document.getElementById('eraser-popup').style.display = 'none';
            }
        });
        document.getElementById('btn-clear').addEventListener('click', () => {
            if (confirm('確定要清空筆跡與知識卡嗎？(講義背景不會清除)')) {
                drawCtx.clearRect(0, 0, CANVAS_SIZE, CANVAS_SIZE);
                document.getElementById('tags-container').innerHTML = '';
            }
        });

        // ─── PDF & Image Loading ──────────────────────────────────────────
        let currentPdfDoc = null, currentPageNum = 1;
        let currentFileUrl = null, currentFileType = null; // for saving state
        const pagingUI = document.getElementById('paging-ui');
        const pageIndicator = document.getElementById('page-indicator');
        const pageDrawings = {}; // Store handwriting per page

        document.getElementById('img-upload').addEventListener('change', async function(e) {
            const file = e.target.files[0]; if (!file) return;
            currentFileType = file.type;
            currentFileUrl = await readFileAsDataURL(file);
            await loadFileData(currentFileUrl, currentFileType);
            this.value = ''; // allow re-selecting same file
        });

        async function loadFileData(url, type) {
            bgCtx.clearRect(0, 0, CANVAS_SIZE, CANVAS_SIZE);
            drawCtx.clearRect(0, 0, CANVAS_SIZE, CANVAS_SIZE);
            document.getElementById('tags-container').innerHTML = '';
            for (let k in pageDrawings) delete pageDrawings[k]; // clear memory
            chatHistory = []; // Reset conversation history
            scale = 1; centerCanvas();

            if (type === 'application/pdf') {
                const base64Data = url.split(',')[1];
                const binaryData = atob(base64Data);
                const arr = new Uint8Array(binaryData.length);
                for (let i = 0; i < binaryData.length; i++) arr[i] = binaryData.charCodeAt(i);
                
                pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.16.105/pdf.worker.min.js';
                currentPdfDoc = await pdfjsLib.getDocument(arr).promise;
                currentPageNum = 1;
                pagingUI.style.display = 'flex';
                await renderPDFPage(currentPageNum);
            } else if (url) {
                currentPdfDoc = null; pagingUI.style.display = 'none';
                return new Promise(resolve => {
                    const img = new Image();
                    img.onload = () => { 
                        bgCtx.drawImage(img, (CANVAS_SIZE - img.width) / 2, (CANVAS_SIZE - img.height) / 2); 
                        resolve();
                    };
                    img.src = url;
                });
            }
        }

        function readFileAsDataURL(file) {
            return new Promise(resolve => {
                const reader = new FileReader();
                reader.onload = e => resolve(e.target.result);
                reader.readAsDataURL(file);
            });
        }

        async function renderPDFPage(num) {
            if (!currentPdfDoc) return;
            document.getElementById('btn-prev-page').disabled = num <= 1;
            document.getElementById('btn-next-page').disabled = num >= currentPdfDoc.numPages;
            pageIndicator.textContent = `第 ${num} / ${currentPdfDoc.numPages} 頁`;
            
            // Show only tags for this page
            document.querySelectorAll('.wb-tag').forEach(t => {
                t.style.display = (t.dataset.page == num) ? 'block' : 'none';
            });

            const page = await currentPdfDoc.getPage(num);
            const vp = page.getViewport({ scale: 2.5 });
            const tmp = document.createElement('canvas');
            tmp.width = vp.width; tmp.height = vp.height;
            await page.render({ canvasContext: tmp.getContext('2d'), viewport: vp }).promise;
            
            bgCtx.clearRect(0, 0, CANVAS_SIZE, CANVAS_SIZE);
            const ox = (CANVAS_SIZE - vp.width) / 2, oy = (CANVAS_SIZE - vp.height) / 2;
            bgCtx.fillStyle = '#ffffff'; bgCtx.fillRect(ox, oy, vp.width, vp.height);
            bgCtx.drawImage(tmp, ox, oy);
            
            // Restore handwriting for this page
            drawCtx.clearRect(0, 0, CANVAS_SIZE, CANVAS_SIZE);
            if (pageDrawings[num]) {
                const img = new Image();
                img.onload = () => drawCtx.drawImage(img, 0, 0);
                img.src = pageDrawings[num];
            }
        }

        document.getElementById('btn-prev-page').addEventListener('click', () => {
            if (currentPageNum <= 1) return;
            pageDrawings[currentPageNum] = drawingCanvas.toDataURL(); // Save current page handwriting
            currentPageNum--; 
            renderPDFPage(currentPageNum);
        });
        document.getElementById('btn-next-page').addEventListener('click', () => {
            if (!currentPdfDoc || currentPageNum >= currentPdfDoc.numPages) return;
            pageDrawings[currentPageNum] = drawingCanvas.toDataURL(); // Save current page handwriting
            currentPageNum++; 
            renderPDFPage(currentPageNum);
        });

        // ─── Save & Load State ────────────────────────────────────────────
        document.getElementById('btn-save').addEventListener('click', () => {
            pageDrawings[currentPageNum] = drawingCanvas.toDataURL(); // Force save current page
            
            const tags = [];
            document.querySelectorAll('.wb-tag').forEach(tag => {
                tags.push({
                    title: tag.dataset.title,
                    html: tag.dataset.html,
                    x: parseFloat(tag.style.left) || 0,
                    y: parseFloat(tag.style.top) || 0,
                    page: parseInt(tag.dataset.page) || 1
                });
            });

            const state = {
                fileUrl: currentFileUrl,
                fileType: currentFileType,
                pageDrawings: pageDrawings,
                tags: tags,
                currentPageNum: currentPageNum,
                chatHistory: chatHistory
            };

            const blob = new Blob([JSON.stringify(state)], {type: 'application/json'});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url; a.download = 'whiteboard_backup.aibyte';
            document.body.appendChild(a); a.click(); document.body.removeChild(a);
            URL.revokeObjectURL(url);
        });

        document.getElementById('state-upload').addEventListener('change', async function(e) {
            const file = e.target.files[0]; if (!file) return;
            const text = await new Promise(resolve => {
                const reader = new FileReader();
                reader.onload = e => resolve(e.target.result);
                reader.readAsText(file);
            });
            try {
                const state = JSON.parse(text);
                currentFileUrl = state.fileUrl;
                currentFileType = state.fileType;
                
                await loadFileData(currentFileUrl, currentFileType);
                
                Object.assign(pageDrawings, state.pageDrawings || {});
                currentPageNum = state.currentPageNum || 1;
                chatHistory = state.chatHistory || [];
                
                if (currentPdfDoc) {
                    await renderPDFPage(currentPageNum);
                } else if (pageDrawings[1]) {
                    const img = new Image();
                    img.onload = () => drawCtx.drawImage(img, 0, 0);
                    img.src = pageDrawings[1];
                }

                document.getElementById('tags-container').innerHTML = '';
                (state.tags || []).forEach(t => {
                    createWhiteboardTag(decodeURIComponent(t.title), decodeURIComponent(t.html), {x: t.x, y: t.y}, t.page);
                });
            } catch (err) {
                alert('載入進度失敗：' + err.message);
            }
            this.value = '';
        });

        // ─── Settings Modal ───────────────────────────────────────────────
        const settingsModal = document.getElementById('settings-modal');
        const apiKeyInput = document.getElementById('api-key-input');
        const modelSelect = document.getElementById('model-select');

        function loadSettings() {
            const key   = localStorage.getItem('gemini_api_key') || '';
            const model = localStorage.getItem('gemini_model') || 'gemini-2.0-flash';
            apiKeyInput.value = key;
            // Try to set saved model in select
            if ([...modelSelect.options].some(o => o.value === model)) {
                modelSelect.value = model;
            } else {
                // Add and select it dynamically
                const opt = new Option(model, model, true, true);
                modelSelect.appendChild(opt);
            }
            updateModelIndicator(model);
        }
        function updateModelIndicator(model) {
            const names = {
                'gemini-2.0-flash':  'Gemini 2.0 Flash',
                'gemini-1.5-flash':  'Gemini 1.5 Flash',
                'gemini-1.5-pro':    'Gemini 1.5 Pro',
                'gemini-pro':        'Gemini Pro'
            };
            document.getElementById('model-indicator').textContent = `模型：${names[model] || model}`;
        }

        document.getElementById('btn-settings').addEventListener('click', () => {
            loadSettings();
            document.getElementById('test-result').style.display = 'none';
            settingsModal.classList.add('open');
        });
        document.getElementById('btn-settings-cancel').addEventListener('click', () => settingsModal.classList.remove('open'));
        document.getElementById('btn-settings-save').addEventListener('click', () => {
            localStorage.setItem('gemini_api_key', apiKeyInput.value.trim());
            localStorage.setItem('gemini_model', modelSelect.value);
            updateModelIndicator(modelSelect.value);
            settingsModal.classList.remove('open');
            addMessage('ai', '✅ 設定已儲存！現在可以開始發問了。', null, false);
        });

        // Auto-detect available models
        document.getElementById('btn-list-models').addEventListener('click', async () => {
            const key = apiKeyInput.value.trim();
            const resultDiv = document.getElementById('test-result');
            if (!key) {
                resultDiv.style.display = 'block';
                resultDiv.style.background = '#fff3cd';
                resultDiv.textContent = '⚠️ 請先輸入 API Key 再偵測模型';
                return;
            }
            resultDiv.style.display = 'block';
            resultDiv.style.background = '#e8f4fd';
            resultDiv.textContent = '🔍 偵測可用模型中...';
            try {
                const res = await fetch(`https://generativelanguage.googleapis.com/v1beta/models?key=${key}&pageSize=50`);
                if (!res.ok) throw new Error('HTTP ' + res.status);
                const data = await res.json();
                // Filter to models that support generateContent
                const models = (data.models || []).filter(m =>
                    m.supportedGenerationMethods?.includes('generateContent') &&
                    m.name.includes('gemini')
                );
                if (models.length === 0) throw new Error('未找到可用模型');
                // Repopulate select
                modelSelect.innerHTML = '';
                models.forEach(m => {
                    const id = m.name.replace('models/', '');
                    const opt = new Option(`${id}  (輸入: ${m.inputTokenLimit||'?'}, 輸出: ${m.outputTokenLimit||'?'})`, id);
                    modelSelect.appendChild(opt);
                });
                // Pick gemini-2.0-flash or first available
                const preferred = ['gemini-2.0-flash','gemini-1.5-flash','gemini-1.5-pro'];
                const best = preferred.find(p => [...modelSelect.options].some(o => o.value === p));
                if (best) modelSelect.value = best;
                resultDiv.style.background = '#d4edda';
                resultDiv.textContent = `✅ 偵測完成！找到 ${models.length} 個可用模型，請從列表中選擇。`;
            } catch(e) {
                resultDiv.style.background = '#f8d7da';
                resultDiv.textContent = `❌ 偵測失敗: ${e.message}`;
            }
        });

        // Test connection button
        document.getElementById('btn-test-conn').addEventListener('click', async () => {
            const key   = apiKeyInput.value.trim();
            const model = modelSelect.value;
            const resultDiv = document.getElementById('test-result');
            if (!key) {
                resultDiv.style.display = 'block';
                resultDiv.style.background = '#fff3cd';
                resultDiv.textContent = '⚠️ 請先輸入 API Key';
                return;
            }
            resultDiv.style.display = 'block';
            resultDiv.style.background = '#e8f4fd';
            resultDiv.textContent = '🔌 測試中...';
            try {
                const url = getApiUrl(model, key);

                const res = await fetch(url, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ contents: [{ role: 'user', parts: [{ text: 'Hi, reply with one word OK.' }] }] })
                });
                if (res.ok) {
                    resultDiv.style.background = '#d4edda';
                    resultDiv.textContent = '✅ 連線成功！可以儲存並開始使用。';
                } else {
                    const err = await res.json().catch(() => ({}));
                    resultDiv.style.background = '#f8d7da';
                    resultDiv.textContent = `❌ 失敗：${err.error?.message || 'HTTP ' + res.status}。請嘗試換一個模型。`;
                }
            } catch(e) {
                resultDiv.style.background = '#f8d7da';
                resultDiv.textContent = `❌ 網路錯誤：${e.message}`;
            }
        });

        settingsModal.addEventListener('click', (e) => { if (e.target === settingsModal) settingsModal.classList.remove('open'); });
        loadSettings();

        // ── Right panel: Ctrl+Scroll to adjust font size ──────────────────
        let rightFontSize = 14; // px
        document.querySelector('.right-panel').addEventListener('wheel', (e) => {
            if (!e.ctrlKey) return; // only trigger on Ctrl+scroll
            e.preventDefault();
            rightFontSize = Math.min(22, Math.max(10, rightFontSize + (e.deltaY < 0 ? 1 : -1)));
            document.getElementById('chat-messages').style.fontSize = rightFontSize + 'px';
        }, { passive: false });


        // ─── Screenshot / Crop ────────────────────────────────────────────
        let pendingImageData = null;
        const cropOverlay = document.getElementById('crop-overlay');
        const cropBox = document.getElementById('crop-box');
        let isCropping = false, cropStartX = 0, cropStartY = 0;

        document.getElementById('btn-screenshot').addEventListener('click', () => {
            currentMode = 'crop';
            cropOverlay.style.display = 'block';
            cropBox.style.display = 'none';
        });

        cropOverlay.addEventListener('mousedown', (e) => {
            isCropping = true;
            const r = cropOverlay.getBoundingClientRect();
            cropStartX = e.clientX - r.left; cropStartY = e.clientY - r.top;
            Object.assign(cropBox.style, { left: cropStartX+'px', top: cropStartY+'px', width: '0', height: '0', display: 'block' });
        });
        cropOverlay.addEventListener('mousemove', (e) => {
            if (!isCropping) return;
            const r = cropOverlay.getBoundingClientRect();
            const cx = e.clientX - r.left, cy = e.clientY - r.top;
            Object.assign(cropBox.style, {
                left: Math.min(cx, cropStartX)+'px', top: Math.min(cy, cropStartY)+'px',
                width: Math.abs(cx - cropStartX)+'px', height: Math.abs(cy - cropStartY)+'px'
            });
        });
        cropOverlay.addEventListener('mouseup', () => {
            isCropping = false; cropOverlay.style.display = 'none';
            setTool('pen', btnPen);
            const w = parseInt(cropBox.style.width), h = parseInt(cropBox.style.height);
            if (w < 20 || h < 20) return;
            const x = parseInt(cropBox.style.left), y = parseInt(cropBox.style.top);
            const cx = (x - translateX) / scale, cy = (y - translateY) / scale;
            const cw = w / scale, ch = h / scale;
            lastCropCenter = { x: cx + cw / 2, y: cy + ch / 2 };

            const exp = document.createElement('canvas');
            exp.width = cw; exp.height = ch;

            const ectx = exp.getContext('2d');
            ectx.fillStyle = '#f0f0f0'; ectx.fillRect(0, 0, cw, ch);
            ectx.drawImage(bgCanvas, cx, cy, cw, ch, 0, 0, cw, ch);
            ectx.drawImage(drawingCanvas, cx, cy, cw, ch, 0, 0, cw, ch);
            pendingImageData = exp.toDataURL('image/png');
            document.getElementById('pending-img-hint').style.display = 'flex';
            // Show tiny preview in chat
            addMessage('user', '', pendingImageData, false);
            document.getElementById('chat-input').focus();
        });

        // ─── Chat Logic ───────────────────────────────────────────────────
        const chatMessages = document.getElementById('chat-messages');
        const chatInput = document.getElementById('chat-input');
        let chatHistory = []; // Store conversation context

        // Auto-resize textarea
        chatInput.addEventListener('input', () => {
            chatInput.style.height = 'auto';
            chatInput.style.height = Math.min(chatInput.scrollHeight, 100) + 'px';
        });
        chatInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage(); }
        });
        document.getElementById('btn-send').addEventListener('click', sendMessage);

        function addMessage(sender, text, imgData = null, rich = false) {
            const div = document.createElement('div');
            div.className = `message ${sender}`;
            if (rich && sender === 'ai') {
                const content = document.createElement('div');
                content.className = 'ai-content';
                content.innerHTML = renderMarkdown(text);
                div.appendChild(content);
            } else {
                if (text) div.textContent = text;
            }
            if (imgData) {
                const img = document.createElement('img');
                img.src = imgData; div.appendChild(img);
            }
            chatMessages.appendChild(div);
            chatMessages.scrollTop = chatMessages.scrollHeight;
            return div;
        }

        function renderMarkdown(text) {
            // Extract mermaid blocks before marked processes them
            const mermaidBlocks = [];
            const processed = text.replace(/```mermaid\n([\s\S]*?)```/g, (_, code) => {
                const id = `mermaid-${Date.now()}-${mermaidBlocks.length}`;
                mermaidBlocks.push({ id, code: code.trim() });
                return `<div class="mermaid" id="${id}">MERMAID_PLACEHOLDER_${mermaidBlocks.length - 1}</div>`;
            });
            let html = marked.parse(processed);
            // Restore mermaid blocks
            mermaidBlocks.forEach((block, i) => {
                html = html.replace(`<p>MERMAID_PLACEHOLDER_${i}</p>`, `<div class="mermaid" id="${block.id}">${block.code}</div>`);
                html = html.replace(`MERMAID_PLACEHOLDER_${i}`, block.code);
            });
            return html;
        }

        async function renderMermaidInElement(el) {
            const diagrams = el.querySelectorAll('.mermaid');
            for (const d of diagrams) {
                try { await mermaid.run({ nodes: [d] }); } catch(err) { d.textContent = '[圖表語法錯誤]'; }
            }
        }

        async function renderMathInElement(el) {
            if (window.MathJax && MathJax.typesetPromise) {
                try { await MathJax.typesetPromise([el]); } catch(e) {}
            }
        }

        async function sendMessage() {
            const text = chatInput.value.trim();
            if (!text && !pendingImageData) return;

            const apiKey = localStorage.getItem('gemini_api_key');
            if (!apiKey) {
                addMessage('ai', '⚠️ 請先點擊右上角「⚙️ 設定」輸入您的 Gemini API Key！', null, false);
                return;
            }

            if (text) addMessage('user', text);
            chatInput.value = ''; chatInput.style.height = 'auto';
            document.getElementById('pending-img-hint').style.display = 'none';

            const imgToSend = pendingImageData;
            pendingImageData = null;

            const loadingDiv = addMessage('ai', '✨ Gemini 思考中...', null, false);
            loadingDiv.classList.add('loading');

            try {
                const reply = await fetchGeminiResponse(text, imgToSend, apiKey);
                chatMessages.removeChild(loadingDiv);
                const msgDiv = addMessage('ai', reply, null, true);
                await renderMermaidInElement(msgDiv);
                await renderMathInElement(msgDiv);
                chatMessages.scrollTop = chatMessages.scrollHeight;

                // Extract and pin knowledge card
                const cardMatch = reply.match(/【核心重點】[：:]?\s*(.+)/);
                const title = cardMatch ? cardMatch[1].trim() : 'AI 回答筆記';
                createWhiteboardTag(title, msgDiv.innerHTML, lastCropCenter);
                lastCropCenter = null; // reset
            } catch (err) {

                chatMessages.removeChild(loadingDiv);
                addMessage('ai', `❌ 錯誤：${err.message}\n\n請確認 API Key 是否正確，以及網路是否正常。`, null, false);
            }
        }

        // ─── Gemini API Call ──────────────────────────────────────────────
        const SYSTEM_PROMPT = `你是一位親切的家教老師。請嚴格遵守以下回答原則：

【核心原則：問什麼就答什麼】
- 問原理 → 只解釋原理，不額外補充發展史、應用場景或相關定律。
- 問方法 → 只給步驟或方法，不加背景知識。
- 問計算 → 只給算法與答案，不延伸解說。
- 問定義 → 只給定義，一兩句即可。
絕對不要主動「延伸補充」或「順便提到」使用者沒問的內容。

【格式規則】
- 回答力求精簡，用 Markdown 條列重點即可。
- 若需要公式，使用 LaTeX（行內 $...$，獨立 $$...$$）。
- 若使用者明確要求「詳細」、「完整說明」或「做一頁筆記」，才展開完整格式與 Mermaid 圖表。
- 語氣活潑自然，像朋友在討論，不要像課本。
- 首次對話時可以簡單打個招呼，之後直接回答就好。`;
        // Smart URL: gemini-pro uses v1; all others use v1beta
        function getApiUrl(model, apiKey) {
            const useV1 = model === 'gemini-1.0-pro';
            const version = useV1 ? 'v1' : 'v1beta';
            return `https://generativelanguage.googleapis.com/${version}/models/${model}:generateContent?key=${apiKey}`;
        }

        async function fetchGeminiResponse(question, imgBase64, apiKey) {
            const model = localStorage.getItem('gemini_model') || 'gemini-2.0-flash';
            const url = getApiUrl(model, apiKey);


            const userParts = [];
            if (question) userParts.push({ text: question });
            if (imgBase64) {
                const base64Data = imgBase64.split(',')[1];
                userParts.push({ inlineData: { mimeType: 'image/png', data: base64Data } });
            }
            if (!question && imgBase64) userParts.push({ text: '請分析這張圖片的內容並詳細解說。' });

            const newTurn = { role: 'user', parts: userParts };
            
            // Reconstruct full conversation history
            const contents = [
                { role: 'user',  parts: [{ text: SYSTEM_PROMPT }] },
                { role: 'model', parts: [{ text: '明白！我會以活潑自然的語氣教學，並將解答整理成精美易讀的一頁式簡報格式。' }] },
                ...chatHistory,
                newTurn
            ];

            const body = {
                contents: contents,
                generationConfig: { temperature: 0.7, maxOutputTokens: 4096 }
            };

            const res = await fetch(url, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(body)
            });

            if (!res.ok) {
                const err = await res.json().catch(() => ({}));
                throw new Error(err.error?.message || `HTTP 錯誤 ${res.status}`);
            }

            const data = await res.json();
            const text = data.candidates?.[0]?.content?.parts?.[0]?.text;
            if (!text) throw new Error('API 未回傳任何內容，請重試。');
            
            // Save successful turn to history
            chatHistory.push(newTurn);
            chatHistory.push({ role: 'model', parts: [{ text: text }] });
            
            return text;
        }


        // ─── Whiteboard Tags ──────────────────────────────────────────────
        let tagCounter = 0;
        let lastCreatedTag = null; // 記錄最後產生的知識卡

        function createWhiteboardTag(title, fullHtml, pos, pageNum) {
            const container = document.getElementById('tags-container');
            const tag = document.createElement('div');
            tag.className = 'wb-tag';
            tag.dataset.page = pageNum || currentPageNum || 1; // Tie to current page
            tag.dataset.title = encodeURIComponent(title);
            tag.dataset.html = encodeURIComponent(fullHtml);
            
            const btnId = `tag-btn-${tagCounter++}`;

            tag.innerHTML = `
                <div class="tag-header" style="cursor:move;">
                    <span style="display:flex; align-items:center; gap:6px;">
                        <input type="checkbox" class="merge-checkbox" onclick="event.stopPropagation(); updateMergeButton();">
                        💡 知識卡
                    </span>
                    <span class="close-btn" onclick="const t = this.closest('.wb-tag'); if(lastCreatedTag === t) lastCreatedTag = null; t.remove(); updateMergeButton(); event.stopPropagation();">✖</span>
                </div>
                <div style="font-weight:600; margin-bottom:8px; border-bottom:1px solid #f0f0f0; padding-bottom:6px;">${title}</div>
                <button id="${btnId}" style="width:100%; padding:6px; background:#fff; border:1px solid #4a90e2; color:#4a90e2; border-radius:6px; cursor:pointer; font-size:12px;">📖 開啟詳細筆記</button>
            `;
            
            // Positioning
            if (pos && pos.x && pos.y) {
                tag.style.left = pos.x + 'px';
                tag.style.top  = pos.y + 'px';
            } else if (lastCreatedTag && document.body.contains(lastCreatedTag)) {
                // 自動排版：接續在上一張卡片下方
                const lastX = parseFloat(lastCreatedTag.style.left) || 0;
                const lastY = parseFloat(lastCreatedTag.style.top) || 0;
                tag.style.left = lastX + 'px';
                tag.style.top  = (lastY + lastCreatedTag.clientHeight + 15) + 'px';
            } else {
                const r = viewport.getBoundingClientRect();
                tag.style.left = `${(r.width / 2 - translateX) / scale}px`;
                tag.style.top  = `${(r.height / 3 - translateY) / scale}px`;
            }

            makeDraggable(tag);
            container.appendChild(tag);
            lastCreatedTag = tag;

            // Bind click event after adding to DOM, avoiding string interpolation issues
            document.getElementById(btnId).addEventListener('click', () => {
                openNoteModal(fullHtml);
            });
        }

        // ─── 合併知識卡功能 ──────────────────────────────────────────────
        function updateMergeButton() {
            const checkboxes = document.querySelectorAll('.merge-checkbox:checked');
            const mergeBtn = document.getElementById('btn-merge-tags');
            if (checkboxes.length >= 2) {
                mergeBtn.style.display = 'block';
                mergeBtn.textContent = `🔗 合併選取的 ${checkboxes.length} 張知識卡`;
            } else {
                mergeBtn.style.display = 'none';
            }
        }

        function handleMergeTags() {
            const checkboxes = document.querySelectorAll('.merge-checkbox:checked');
            if (checkboxes.length < 2) return;

            let mergedHtml = '';
            let firstTagPos = null;
            let firstTagPage = null;

            checkboxes.forEach((cb, index) => {
                const tag = cb.closest('.wb-tag');
                if (index === 0) {
                    firstTagPos = {
                        x: parseFloat(tag.style.left),
                        y: parseFloat(tag.style.top)
                    };
                    firstTagPage = tag.dataset.page;
                }
                const title = decodeURIComponent(tag.dataset.title);
                const html = decodeURIComponent(tag.dataset.html);
                
                mergedHtml += `<div style="margin-bottom:15px;"><h3 style="margin-top:0;">${title}</h3>${html}</div><hr style="margin:20px 0; border:0; border-top:1px dashed #ccc;">`;
                
                if (lastCreatedTag === tag) lastCreatedTag = null;
                tag.remove(); // 移除舊卡片
            });

            createWhiteboardTag('合併知識卡', mergedHtml, firstTagPos, firstTagPage);
            updateMergeButton();
        }

        function openNoteModal(htmlContent) {
            const modal = document.getElementById('note-modal');
            const content = document.getElementById('note-modal-content');
            content.innerHTML = htmlContent;
            modal.style.display = 'flex';
        }

        function makeDraggable(el) {
            let p1 = 0, p2 = 0, p3 = 0, p4 = 0;
            let currentX = parseFloat(el.style.left) || 0;
            let currentY = parseFloat(el.style.top) || 0;

            el.onmousedown = (e) => {
                if (e.target.classList.contains('close-btn') || e.target.tagName === 'BUTTON') return;
                e.preventDefault(); e.stopPropagation();
                
                // Refresh starting coords
                currentX = parseFloat(el.style.left) || 0;
                currentY = parseFloat(el.style.top) || 0;
                p3 = e.clientX; p4 = e.clientY;
                
                document.onmouseup = () => { document.onmouseup = null; document.onmousemove = null; };
                document.onmousemove = (ev) => {
                    p1 = (p3 - ev.clientX) / scale; p2 = (p4 - ev.clientY) / scale;
                    p3 = ev.clientX; p4 = ev.clientY;
                    
                    currentX -= p1;
                    currentY -= p2;
                    el.style.top  = currentY + 'px';
                    el.style.left = currentX + 'px';
                };
            };
        }
    