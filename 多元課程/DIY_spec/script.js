/**
 * DIY 手機分光儀 - 核心互動邏輯與光學引擎
 * 國立新化高級工業職業學校 - 多元選修化學課程
 */

function startApp() {
    // ----------------------------------------------------
    // 1. 計算過程彈窗邏輯 (用於分頁詳細計算)
    // ----------------------------------------------------
    const modals = document.querySelectorAll('.modal');
    const overlay = document.getElementById('modal-overlay');
    const btns = document.querySelectorAll('.calc-btn');
    const closeBtns = document.querySelectorAll('.close-btn');

    if (btns.length > 0 && overlay) {
        btns.forEach(btn => {
            btn.addEventListener('click', () => {
                const modalId = btn.getAttribute('data-modal');
                const modal = document.getElementById(modalId);
                if (modal) {
                    modal.classList.add('active');
                    overlay.classList.add('active');
                }
            });
        });

        const closeModal = () => {
            modals.forEach(m => m.classList.remove('active'));
            overlay.classList.remove('active');
        };

        closeBtns.forEach(btn => btn.addEventListener('click', closeModal));
        overlay.addEventListener('click', closeModal);
    }

    // ----------------------------------------------------
    // 2. 光譜儀俯視剖面互動模擬器 (全景原理與構造教學)
    // ----------------------------------------------------
    const simSvg = document.getElementById('spectrometer-svg');
    if (simSvg) {
        initSpectrometerSimulator();
    }

    // ----------------------------------------------------
    // 3. 反射式與折射式分頁的靜態幾何圖繪製
    // ----------------------------------------------------
    initSubpageSvgs();
    initTabNavigation();
}

function initSpectrometerSimulator() {
    const simSvg = document.getElementById('spectrometer-svg');
    if (!simSvg) return;

    // 核心光學狀態 (預設以 CD 光柵 31° 為教學基準)
    const state = {
        lightOn: true,
        lightAngleDeg: 0,        // 光源入射角偏移度數 (-15 ~ +15)
        gratingType: 'cd',       // 預設為 CD 光柵
        gratingAngle: 31.0,      // CD 光柵標準夾角 31.0°
        cameraOffset: 0,         // 攝像頭水平位移 (-40 ~ +40)
        lens1Installed: true,    // 水平準直鏡
        lens2Installed: true,    // 垂直聚焦鏡
        activeComp: null         // 當前展開的浮動視窗元件 (null 代表關閉)
    };

    const gratingConfigs = {
        'cd': { name: 'CD 光柵', d: 1600, defaultAngle: 31.0, linesText: '625 lines/mm' },
        '1000': { name: '1000 柵光柵片', d: 1000, defaultAngle: 22.0, linesText: '1000 lines/mm' },
        'dvd': { name: 'DVD 光柵', d: 740, defaultAngle: 14.5, linesText: '1350 lines/mm' }
    };

    // 元件細部解說資料庫 (點擊以浮動視窗呈現)
    const componentDetails = {
        'slit': {
            icon: '✂️',
            title: '入光狹縫 (Entrance Slit)',
            desc: '狹縫是整個分光儀唯一的「線光源」。白光通過極微小的縫隙，能有效壓制光線的散射角度，避免外界各角度光斑在光柵表面重疊模糊。它是保證光譜線具有高解析度（Resolution）的最關鍵構造。',
            diy: '<strong>手搓製作秘訣：</strong>取兩片單面美工刀片刃面相對，中間夾一張普通 A4 紙（厚度約 0.1 mm）作為測厚規固定，即可獲得平行均勻的微米狹縫。',
            tip: '💡 狹縫過寬（>0.4mm）色散譜線粗糙重疊；狹縫過窄（<0.03mm）進光量太弱，手機雜訊明顯。'
        },
        'lens1': {
            icon: '🔍',
            title: '入光準直鏡 (Collimator Lens)',
            desc: '狹縫恰好位於此凸透鏡的焦點 $f$ 上。狹縫射出的發散光線通過準直鏡後，被校正為筆直的「平行光束」，確保打在光柵上每一個凹槽的光線入射角 $\\alpha$ 嚴格一致。',
            diy: '<strong>手搓平替方案：</strong>手搓入門版常省略此鏡片，改用「拉長狹縫到光柵的紙筒距離（15~20cm）」抑制發散；進階版加裝老舊放大鏡片，清晰度翻倍！',
            tip: '💡 您可點擊按鈕或拖曳取出/裝入此鏡，觀察「平行光」與「發散光」在光譜解析度上的差異。'
        },
        'grating': {
            icon: '💿',
            title: '繞射光柵 (Diffraction Grating)',
            desc: '基準採用 CD 光碟（軌道間距 $d = 1600\\text{ nm}$）。表面數千條平行凹槽產生光波同相位干涉，依照光柵方程式 $d(\\sin\\alpha - \\sin\\beta) = m\\lambda$ 將各波長光線按不同角度展開成七彩光譜。',
            diy: '<strong>擺放幾何角度：</strong>CD 光柵在此 90° 垂直幾何暗箱中，光柵與狹縫最佳夾角為 <strong>31°</strong>。此時綠光（550nm）垂直射入相機，光斑亮度最高！',
            tip: '💡 旋轉光柵角度可使不同波段的光譜精確掃入鏡頭視野中。'
        },
        'baffle': {
            icon: '⬛',
            title: '箱內消光隔板 (Optical Baffles)',
            desc: '光線射在光柵表面時，除了產生一級繞射彩虹，還會產生高亮度的「零級鏡面反射白光（$m=0$）」。消光隔板立於內角轉折處，能徹底阻擋零級白光與箱壁漫射光直接竄入相機。',
            diy: '<strong>手搓製作秘訣：</strong>用紙箱剪一塊約 4×6 cm 的厚紙板，雙面塗消光黑漆，黏在 90° 直角轉折內側，杜絕鬼影光斑。',
            tip: '💡 良好的內部消光隔板是手搓分光儀能清晰看見日光燈汞原子發射譜線的關鍵秘訣！'
        },
        'lens2': {
            icon: '🔎',
            title: '聚焦成像透鏡 (Focusing Lens)',
            desc: '將光柵反射出的不同角度平行色光，依據出射角度匯聚聚焦在相機 CMOS 感光元件平面上，形成線狀光譜條。',
            diy: '<strong>手搓平替方案：</strong>在手搓分光儀中，智慧型手機鏡頭自帶的鏡頭群即可兼作聚焦鏡（需鎖定對焦在無限遠）；若在暗箱內加裝專用凸透鏡，可大幅縮短暗箱體積。',
            tip: '💡 可透過按鈕裝卸，進行進階聚焦成像實驗。'
        },
        'camera': {
            icon: '📱',
            title: '手機攝像頭 (CMOS Camera Sensor)',
            desc: '接收色散彩虹。CMOS 感光晶片上的微透鏡與 Bayer RGB 濾色陣列將光子轉化為電荷，記錄光譜影像。配合光譜分析 App 即可直接繪出各波長強度分布曲線。',
            diy: '<strong>拍攝設定技巧：</strong>務必關閉自動曝光與自動對焦（手動對焦鎖定至無限遠），並將 ISO 壓低（ISO 50~100）以避免強光譜線泛白飽和。',
            tip: '💡 您可以微調相機鏡頭收光位置，使紅橙黃綠青藍紫光帶完整被感光元件接收。'
        },
        'light': {
            icon: '💡',
            title: '外置複合白光源 (White Light Source)',
            desc: '向暗箱發散射出錐形白光。可使用自然日光（連續光譜）、鎢絲燈泡、白光 LED 或日光燈管（含汞發射譜線）。光源垂直高度會影響入射光線對狹縫的入射角度。',
            diy: '<strong>操作說明：</strong>點擊燈泡開關燈；上下拖曳可改變入射角，觀察狹縫對斜射光斑的空間濾波特性。',
            tip: '💡 當入射角偏離過大時，狹縫有效投影面積縮小，若光線未命中光柵，暗箱內將無任何彩虹產生。'
        }
    };

    // DOM 元素引用
    const floatModal = document.getElementById('comp-float-modal');
    const modalTitle = document.getElementById('comp-modal-title');
    const modalDesc = document.getElementById('comp-modal-desc');
    const modalDiy = document.getElementById('comp-modal-diy');
    const modalTip = document.getElementById('comp-modal-tip');
    const btnCloseModal = document.getElementById('btn-close-comp-modal');

    const btnToggleLight = document.getElementById('btn-toggle-light');
    const lightIcon = document.getElementById('light-icon');
    const lightText = document.getElementById('light-text');

    const btnToggleLens1 = document.getElementById('btn-toggle-lens1');
    const lens1Text = document.getElementById('lens1-text');

    const btnToggleLens2 = document.getElementById('btn-toggle-lens2');
    const lens2Text = document.getElementById('lens2-text');

    const btnAutoAlign = document.getElementById('btn-auto-align');

    const rangeLightY = document.getElementById('range-light-y');
    const valLightAngle = document.getElementById('val-light-angle');

    const rangeGratingAngle = document.getElementById('range-grating-angle');
    const valGratingAngle = document.getElementById('val-grating-angle');

    const rangeCameraX = document.getElementById('range-camera-x');
    const valCameraPos = document.getElementById('val-camera-pos');

    const valGratingName = document.getElementById('val-grating-name');
    const btnGCd = document.getElementById('btn-g-cd');
    const btnG1000 = document.getElementById('btn-g-1000');
    const btnGDvd = document.getElementById('btn-g-dvd');

    const cameraStatusPill = document.getElementById('camera-status-pill');
    const cameraHintText = document.getElementById('camera-hint-text');
    const liveCanvas = document.getElementById('live-spectrum-canvas');
    const liveCtx = liveCanvas ? liveCanvas.getContext('2d') : null;

    // ----------------------------------------------------
    // 浮動視窗切換邏輯 (點擊顯示，再點一次隱藏)
    // ----------------------------------------------------
    function toggleComponentModal(compKey) {
        if (!floatModal) return;

        if (state.activeComp === compKey && floatModal.classList.contains('active')) {
            // 再次點擊相同元件：隱藏視窗
            floatModal.classList.remove('active');
            state.activeComp = null;
        } else {
            // 點擊新元件：顯示浮動視窗
            const data = componentDetails[compKey];
            if (!data) return;

            modalTitle.innerHTML = `<span>${data.icon}</span> ${data.title}`;
            modalDesc.innerHTML = data.desc;
            modalDiy.innerHTML = data.diy;
            modalTip.innerHTML = data.tip;

            floatModal.classList.add('active');
            state.activeComp = compKey;

            // MathJax 重新解析公式
            if (window.MathJax && window.MathJax.typesetPromise) {
                window.MathJax.typesetPromise([floatModal]).catch(() => { });
            }
        }
    }

    if (btnCloseModal) {
        btnCloseModal.addEventListener('click', () => {
            if (floatModal) floatModal.classList.remove('active');
            state.activeComp = null;
        });
    }

    // ----------------------------------------------------
    // 控件事件監聽
    // ----------------------------------------------------
    if (btnToggleLight) {
        btnToggleLight.addEventListener('click', () => {
            state.lightOn = !state.lightOn;
            updateControlsUI();
            renderSimulator();
        });
    }

    if (btnToggleLens1) {
        btnToggleLens1.addEventListener('click', () => {
            state.lens1Installed = !state.lens1Installed;
            updateControlsUI();
            renderSimulator();
        });
    }

    if (btnToggleLens2) {
        btnToggleLens2.addEventListener('click', () => {
            state.lens2Installed = !state.lens2Installed;
            updateControlsUI();
            renderSimulator();
        });
    }

    if (btnAutoAlign) {
        btnAutoAlign.addEventListener('click', () => {
            const cfg = gratingConfigs[state.gratingType];
            state.gratingAngle = cfg.defaultAngle;
            state.cameraOffset = 0;
            state.lightAngleDeg = 0;
            if (rangeGratingAngle) rangeGratingAngle.value = state.gratingAngle;
            if (rangeCameraX) rangeCameraX.value = 0;
            if (rangeLightY) rangeLightY.value = 0;
            updateControlsUI();
            renderSimulator();
        });
    }

    if (rangeLightY) {
        rangeLightY.addEventListener('input', (e) => {
            state.lightAngleDeg = parseFloat(e.target.value);
            updateControlsUI();
            renderSimulator();
        });
    }

    if (rangeGratingAngle) {
        rangeGratingAngle.addEventListener('input', (e) => {
            state.gratingAngle = parseFloat(e.target.value);
            updateControlsUI();
            renderSimulator();
        });
    }

    if (rangeCameraX) {
        rangeCameraX.addEventListener('input', (e) => {
            state.cameraOffset = parseFloat(e.target.value);
            updateControlsUI();
            renderSimulator();
        });
    }

    const switchGrating = (type) => {
        state.gratingType = type;
        const cfg = gratingConfigs[type];
        state.gratingAngle = cfg.defaultAngle;
        if (rangeGratingAngle) rangeGratingAngle.value = cfg.defaultAngle;
        updateControlsUI();
        renderSimulator();
    };

    if (btnGCd) btnGCd.addEventListener('click', () => switchGrating('cd'));
    if (btnG1000) btnG1000.addEventListener('click', () => switchGrating('1000'));
    if (btnGDvd) btnGDvd.addEventListener('click', () => switchGrating('dvd'));

    function updateControlsUI() {
        if (btnToggleLight) {
            btnToggleLight.classList.toggle('active', state.lightOn);
            if (lightIcon) lightIcon.textContent = state.lightOn ? '💡' : '⚪';
            if (lightText) lightText.textContent = state.lightOn ? '光源：開啟 (ON)' : '光源：關閉 (OFF)';
        }

        if (btnToggleLens1) {
            btnToggleLens1.classList.toggle('active', state.lens1Installed);
            if (lens1Text) lens1Text.textContent = state.lens1Installed ? '準直鏡 1：已裝入' : '準直鏡 1：已取出';
        }

        if (btnToggleLens2) {
            btnToggleLens2.classList.toggle('active', state.lens2Installed);
            if (lens2Text) lens2Text.textContent = state.lens2Installed ? '聚焦鏡 2：已裝入' : '聚焦鏡 2：已取出';
        }

        if (valLightAngle) valLightAngle.textContent = `${state.lightAngleDeg > 0 ? '+' : ''}${state.lightAngleDeg.toFixed(1)}°`;
        if (valGratingAngle) valGratingAngle.textContent = `${state.gratingAngle.toFixed(1)}°`;
        if (valCameraPos) valCameraPos.textContent = `${state.cameraOffset > 0 ? '+' : ''}${state.cameraOffset} mm`;

        if (btnGCd) btnGCd.classList.toggle('active', state.gratingType === 'cd');
        if (btnG1000) btnG1000.classList.toggle('active', state.gratingType === '1000');
        if (btnGDvd) btnGDvd.classList.toggle('active', state.gratingType === 'dvd');

        const cfg = gratingConfigs[state.gratingType];
        if (valGratingName) valGratingName.textContent = `${cfg.name} (${cfg.d} nm)`;
    }

    // ----------------------------------------------------
    // SVG 渲染核心引擎 (嚴格物理光學)
    // ----------------------------------------------------
    function renderSimulator() {
        const slitX = 170;
        const slitY = 150;
        const lens1X = 330;
        const lens1Y = 150;
        const gratingX = 530;
        const gratingY = 150;
        const lens2X = 530;
        const lens2Y = 320;
        const cameraBaseX = 530;
        const cameraX = cameraBaseX + state.cameraOffset;
        const cameraY = 445;

        // 光源座標 (垂直位移，角度與幾何高度精準對應)
        const lightSourceX = 60;
        // 每度偏角對應約 3.8px 垂直高度
        const lightOffsetY = -state.lightAngleDeg * 3.8;
        const lightSourceY = slitY + lightOffsetY;
        const lampHeadX = lightSourceX + 32; // 92
        const lampHeadY = lightSourceY;

        // 穿過狹縫的光線方向 (直線幾何傳播角度)
        const rayAngle = Math.atan2(slitY - lampHeadY, slitX - lampHeadX);
        const rayVx = Math.cos(rayAngle);
        const rayVy = Math.sin(rayAngle);

        // 光源發散錐 (以射向狹縫的軸線為中心，兩側發散各 20 度)
        const dXToWall = 150 - lampHeadX;
        const lampConeTopY = lampHeadY + dXToWall * Math.tan(rayAngle - 20 * Math.PI / 180);
        const lampConeBottomY = lampHeadY + dXToWall * Math.tan(rayAngle + 20 * Math.PI / 180);

        // 光柵參數
        const cfg = gratingConfigs[state.gratingType];
        const phiRad = state.gratingAngle * Math.PI / 180;
        const gratingHalfLen = 45;
        const gx1 = gratingX - gratingHalfLen * Math.cos(phiRad);
        const gy1 = gratingY - gratingHalfLen * Math.sin(phiRad);
        const gx2 = gratingX + gratingHalfLen * Math.cos(phiRad);
        const gy2 = gratingY + gratingHalfLen * Math.sin(phiRad);

        // 光柵外法向量 (指向迎光面：左方與下方)
        const normX = -Math.sin(phiRad);
        const normY = Math.cos(phiRad);

        // ----------------------------------------------------
        // 嚴格光線追蹤判定 (Ray Tracing & Hit Detection)
        // ----------------------------------------------------
        let hitGrating = false;
        let lens1Blocked = false;
        let hitX = gratingX;
        let hitY = gratingY;
        let inVx = 1;
        let inVy = 0;
        let missEndX = 880;
        let missEndY = 150;
        let lens1HitY = slitY + (lens1X - slitX) * (rayVy / (rayVx || 1e-5));

        if (state.lens1Installed) {
            // [有準直鏡 1 (進階版)]
            // 準直鏡通光孔徑垂直半徑 28mm (y: 122 ~ 178)
            const lens1Radius = 28;
            if (Math.abs(lens1HitY - lens1Y) > lens1Radius) {
                // 光線偏角過大，被準直鏡框擋住
                lens1Blocked = true;
                hitGrating = false;
            } else {
                // 光線穿過準直鏡：狹縫恰在焦點 f 上，出射光線被校正為水平平行光 (inVx = 1, inVy = 0)
                inVx = 1;
                inVy = 0;
                // 水平平行光前進至光柵斜面，計算交點
                // 光柵線段方程式：(x - gratingX)*sin(phi) - (y - gratingY)*cos(phi) = 0
                // 在 y = lens1HitY 處：
                const s = (lens1HitY - gratingY) / Math.sin(phiRad);
                if (Math.abs(s) <= gratingHalfLen) {
                    hitGrating = true;
                    hitX = gratingX + s * Math.cos(phiRad);
                    hitY = lens1HitY;
                } else {
                    // 平行光高度過高或過低，錯過光柵表面，直射箱壁
                    hitGrating = false;
                    missEndX = 880;
                    missEndY = lens1HitY;
                }
            }
        } else {
            // [無準直鏡 (手搓基礎版)]：光線自狹縫沿 rayAngle 直線前進
            // 與光柵線段求交點 (克拉瑪法則精確求交)
            // Ray: (slitX + t*rayVx, slitY + t*rayVy)
            // Grating: (gratingX + s*cos(phiRad), gratingY + s*sin(phiRad))
            const denom = rayVx * Math.sin(phiRad) - rayVy * Math.cos(phiRad);
            if (Math.abs(denom) > 1e-5) {
                const dx0 = gratingX - slitX;
                const dy0 = gratingY - slitY;
                const t = (dx0 * Math.sin(phiRad) - dy0 * Math.cos(phiRad)) / denom;
                const s = (rayVy * dx0 - rayVx * dy0) / denom;

                if (t > 0 && Math.abs(s) <= gratingHalfLen) {
                    hitGrating = true;
                    hitX = gratingX + s * Math.cos(phiRad);
                    hitY = gratingY + s * Math.sin(phiRad);
                    inVx = rayVx;
                    inVy = rayVy;
                }
            }

            if (!hitGrating) {
                // 未命中光柵：沿斜向直線直達箱壁
                if (rayVx > 0) {
                    const tWall = (880 - slitX) / rayVx;
                    const yAtRight = slitY + tWall * rayVy;
                    if (yAtRight >= 65 && yAtRight <= 445) {
                        missEndX = 880;
                        missEndY = yAtRight;
                    } else if (yAtRight < 65) {
                        missEndY = 65;
                        missEndX = slitX + (65 - slitY) / (rayVy || 1e-5) * rayVx;
                    } else {
                        missEndY = 445;
                        missEndX = slitX + (445 - slitY) / (rayVy || 1e-5) * rayVx;
                    }
                }
            }
        }

        // ----------------------------------------------------
        // 光柵物理反射與繞射幾何計算 (僅當 hitGrating 為真時生效)
        // ----------------------------------------------------
        let zeroEndX = hitX;
        let zeroEndY = hitY;
        let coneX1 = hitX, coneY1 = hitY, coneX2 = hitX, coneY2 = hitY;
        let reflAngle = 0;
        let alphaRad = 0;
        let alphaDeg = 0;

        if (hitGrating) {
            // 1. 鏡面反射定律 (Law of Reflection): v_refl = v_in - 2*(v_in · n)*n
            const dotVN = inVx * normX + inVy * normY;
            const reflVx = inVx - 2 * dotVN * normX;
            const reflVy = inVy - 2 * dotVN * normY;
            reflAngle = Math.atan2(reflVy, reflVx);

            const reflLen = 210;
            zeroEndX = hitX + reflLen * Math.cos(reflAngle);
            zeroEndY = hitY + reflLen * Math.sin(reflAngle);

            const spreadRad = 7.0 * Math.PI / 180;
            coneX1 = hitX + reflLen * Math.cos(reflAngle - spreadRad);
            coneY1 = hitY + reflLen * Math.sin(reflAngle - spreadRad);
            coneX2 = hitX + reflLen * Math.cos(reflAngle + spreadRad);
            coneY2 = hitY + reflLen * Math.sin(reflAngle + spreadRad);

            // 2. 光柵入射角 alpha (相對於光柵法線之夾角)
            const cosAlpha = Math.max(-1, Math.min(1, -dotVN));
            alphaRad = Math.acos(cosAlpha);
            alphaDeg = alphaRad * 180 / Math.PI;
        }

        const wavelengths = [
            { w: 390, c: '#7c3aed', name: '紫光 390nm' },
            { w: 436, c: '#2563eb', name: '汞紫藍線 436nm' },
            { w: 480, c: '#06b6d4', name: '青光 480nm' },
            { w: 546, c: '#22c55e', name: '汞綠線 546nm' },
            { w: 580, c: '#eab308', name: '黃光 580nm' },
            { w: 620, c: '#f97316', name: '橙光 620nm' },
            { w: 680, c: '#ef4444', name: '深紅光 680nm' }
        ];

        // 3. 第一級繞射光束方程式: d*(sin(alpha) - sin(beta)) = m*lambda
        const diffractionRays = wavelengths.map(item => {
            if (!hitGrating) {
                return { w: item.w, c: item.c, name: item.name, valid: false, shootAngleRad: 0, hitX: hitX };
            }

            const sinBeta = Math.sin(alphaRad) - (1 * item.w / cfg.d);
            let valid = true;
            let betaRad = 0;
            if (Math.abs(sinBeta) <= 1) {
                betaRad = Math.asin(sinBeta);
            } else {
                valid = false;
            }

            // 繞射光相對鏡面反射光的角位移 delta = alpha - beta
            const shootAngleRad = reflAngle + (alphaRad - betaRad);

            let cHitX = hitX;
            if (state.lens2Installed) {
                // 有聚焦透鏡 2：匯聚成像於焦平面
                const dyLens = lens2Y - hitY;
                const lensHitX = hitX + dyLens / Math.tan(shootAngleRad);
                const dyCam = cameraY - lens2Y;
                // 聚焦鏡折射修正
                cHitX = lensHitX + dyCam * Math.cos(shootAngleRad) * 0.85;
            } else {
                // 無聚焦透鏡：直射相機感光面
                const dy = cameraY - hitY;
                if (Math.sin(shootAngleRad) > 0.1) {
                    cHitX = hitX + dy / Math.tan(shootAngleRad);
                }
            }

            return {
                w: item.w,
                c: item.c,
                name: item.name,
                valid: valid,
                shootAngleRad: shootAngleRad,
                hitX: cHitX
            };
        });

        // ----------------------------------------------------
        // 收光狀態嚴格判定
        // ----------------------------------------------------
        const centerGreenRay = diffractionRays.find(r => r.w === 546) || diffractionRays[3];
        const greenHitX = centerGreenRay ? centerGreenRay.hitX : hitX;
        const cameraApertureHalf = 28;
        const alignDiff = greenHitX - cameraX;

        let isCaptured = false;
        let statusText = '';
        let statusBadge = '';

        if (!state.lightOn) {
            statusText = '⚪ 光源已關閉，暗箱內無光線';
            statusBadge = '<span class="camera-status-dot lost"></span>光源關閉';
        } else if (lens1Blocked) {
            statusText = '⚠️ 光源入射角度偏離過大，光束被準直鏡框阻擋，未到達光柵';
            statusBadge = '<span class="camera-status-dot lost"></span>鏡框阻擋';
        } else if (!hitGrating) {
            statusText = '⚠️ 光線未命中光柵表面，暗箱內無任何繞射彩虹產生（遵守物理定律）';
            statusBadge = '<span class="camera-status-dot lost"></span>未命中光柵';
        } else if (Math.abs(alignDiff) <= cameraApertureHalf) {
            isCaptured = true;
            statusText = '🎯 完美收光！CD 光柵第一級彩虹已精準射入手機鏡頭中心！';
            statusBadge = '<span class="camera-status-dot"></span>完美收光中';
        } else if (alignDiff < -cameraApertureHalf) {
            statusText = '⚠️ 光譜偏左 (紫光側偏差)，請調整光柵角度或相機鏡頭位置';
            statusBadge = '<span class="camera-status-dot lost"></span>光譜偏左';
        } else {
            statusText = '⚠️ 光譜偏右 (紅光側偏差)，請調整光柵角度或相機鏡頭位置';
            statusBadge = '<span class="camera-status-dot lost"></span>光譜偏右';
        }

        if (cameraStatusPill) cameraStatusPill.innerHTML = statusBadge;
        if (cameraHintText) cameraHintText.textContent = statusText;

        // ==========================================
        // 組裝 SVG 繪圖內容
        // ==========================================
        // 狹縫微散光束幾何參數
        const spreadHalfAngle = 3.6 * Math.PI / 180;
        const dXToLens1 = lens1X - slitX; // 160
        const coneTopY = slitY + dXToLens1 * Math.tan(rayAngle - spreadHalfAngle);
        const coneBotY = slitY + dXToLens1 * Math.tan(rayAngle + spreadHalfAngle);
        const xTopHit = gratingX + (coneTopY - gratingY) / Math.tan(phiRad);
        const xBotHit = gratingX + (coneBotY - gratingY) / Math.tan(phiRad);

        // 無準直鏡時狹縫微散光錐
        const spreadLen = 130;
        const spEndX = slitX + spreadLen * (rayVx || 1);
        const spTopY = slitY + spreadLen * Math.tan(rayAngle - spreadHalfAngle);
        const spBotY = slitY + spreadLen * Math.tan(rayAngle + spreadHalfAngle);

        let svgHtml = `
            <defs>
                <filter id="sim-glow" filterUnits="userSpaceOnUse" x="0" y="0" width="920" height="520">
                    <feGaussianBlur stdDeviation="3" result="blur"/>
                    <feMerge>
                        <feMergeNode in="blur"/>
                        <feMergeNode in="SourceGraphic"/>
                    </feMerge>
                </filter>
                <linearGradient id="lampDivergentGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop offset="0%" stop-color="#ffffff" stop-opacity="0.9"/>
                    <stop offset="35%" stop-color="#ffffff" stop-opacity="0.6"/>
                    <stop offset="100%" stop-color="#ffffff" stop-opacity="0.2"/>
                </linearGradient>
                <linearGradient id="slitSpreadGrad" x1="${slitX}" y1="${slitY}" x2="${lens1X}" y2="${slitY}" gradientUnits="userSpaceOnUse">
                    <stop offset="0%" stop-color="#ffffff" stop-opacity="0.42"/>
                    <stop offset="60%" stop-color="#ffffff" stop-opacity="0.22"/>
                    <stop offset="100%" stop-color="#ffffff" stop-opacity="0.08"/>
                </linearGradient>
                <linearGradient id="collimatedBeamGrad" x1="${lens1X}" y1="${slitY}" x2="${gratingX}" y2="${slitY}" gradientUnits="userSpaceOnUse">
                    <stop offset="0%" stop-color="#ffffff" stop-opacity="0.25"/>
                    <stop offset="50%" stop-color="#ffffff" stop-opacity="0.18"/>
                    <stop offset="100%" stop-color="#ffffff" stop-opacity="0.10"/>
                </linearGradient>
                <linearGradient id="diffuseConeGrad" x1="${hitX}" y1="${hitY}" x2="${zeroEndX}" y2="${zeroEndY}" gradientUnits="userSpaceOnUse">
                    <stop offset="0%" stop-color="#cbd5e1" stop-opacity="0.45"/>
                    <stop offset="50%" stop-color="#94a3b8" stop-opacity="0.22"/>
                    <stop offset="100%" stop-color="#64748b" stop-opacity="0.05"/>
                </linearGradient>
                <linearGradient id="boxWallGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                    <stop offset="0%" stop-color="#1e293b"/>
                    <stop offset="100%" stop-color="#0f172a"/>
                </linearGradient>
            </defs>

            <!-- 畫布背景與網格 -->
            <rect x="0" y="0" width="920" height="520" fill="#080c14" />
            <pattern id="gridPattern" width="20" height="20" patternUnits="userSpaceOnUse">
                <line x1="0" y1="0" x2="20" y2="0" stroke="rgba(255,255,255,0.03)" stroke-width="1" />
                <line x1="0" y1="0" x2="0" y2="20" stroke="rgba(255,255,255,0.03)" stroke-width="1" />
            </pattern>
            <rect x="0" y="0" width="920" height="520" fill="url(#gridPattern)" />

            <!-- 方形暗箱 (黑色紙箱剖面俯視 - 佔滿右側全圖區) -->
            <rect x="150" y="45" width="750" height="430" rx="16" fill="url(#boxWallGrad)" stroke="#334155" stroke-width="6" />
            <rect x="165" y="58" width="720" height="404" rx="8" fill="#020617" stroke="#1f2937" stroke-width="2" />
            <text x="750" y="85" fill="#334155" font-size="13" font-weight="bold">消光黑絨暗箱內部</text>

            <!-- 箱壁開口槽 -->
            <rect x="146" y="125" width="20" height="50" fill="#020617" />
            <rect x="${cameraX - 45}" y="455" width="90" height="25" fill="#020617" />
        `;

        // 光路繪製
        if (state.lightOn) {
            // A. 光源發散錐形白光
            svgHtml += `
                <polygon points="${lampHeadX},${lampHeadY - 10} ${lampHeadX},${lampHeadY + 10} 150,${lampConeBottomY} 150,${lampConeTopY}" fill="url(#lampDivergentGrad)" filter="url(#sim-glow)" />
                <line x1="148" y1="${lampConeTopY}" x2="148" y2="${lampConeBottomY}" stroke="#ffffff" stroke-width="3" opacity="0.4" />
            `;

            // B. 狹縫後光線傳播路徑 (呈現微散淺白光與準直平行光)
            if (state.lens1Installed) {
                // [有準直鏡 1 (進階版)]
                if (lens1Blocked) {
                    // 入射光角太大，被準直鏡框擋住
                    svgHtml += `
                        <polygon points="${slitX},${slitY - 1} ${lens1X},${coneTopY} ${lens1X},${coneBotY} ${slitX},${slitY + 1}" fill="url(#slitSpreadGrad)" filter="url(#sim-glow)" />
                        <line x1="${slitX}" y1="${slitY}" x2="${lens1X}" y2="${lens1HitY}" stroke="#ffffff" stroke-width="2.6" filter="url(#sim-glow)" opacity="0.9" />
                        <circle cx="${lens1X}" cy="${lens1HitY}" r="5" fill="#ef4444" />
                        <text x="${lens1X - 95}" y="${lens1HitY - 10}" fill="#f87171" font-size="12" font-weight="bold">光束被鏡框阻擋</text>
                    `;
                } else if (hitGrating) {
                    // 1. 狹縫至準直鏡：微散開的淺白色光束
                    svgHtml += `
                        <polygon points="${slitX},${slitY - 1} ${lens1X},${coneTopY} ${lens1X},${coneBotY} ${slitX},${slitY + 1}" fill="url(#slitSpreadGrad)" filter="url(#sim-glow)" />
                        <line x1="${slitX}" y1="${slitY}" x2="${lens1X}" y2="${lens1HitY}" stroke="#ffffff" stroke-width="2.6" filter="url(#sim-glow)" opacity="1.0" />
                        <text x="${(slitX + lens1X) / 2 - 32}" y="${Math.min(coneTopY, coneBotY) - 6}" fill="#94a3b8" font-size="11" font-weight="600">微散淺白光</text>
                    `;

                    // 2. 準直鏡至光柵：校正為水平平行淺白光束 (與中心亮白入射線平行)
                    svgHtml += `
                        <polygon points="${lens1X},${coneTopY} ${xTopHit},${coneTopY} ${xBotHit},${coneBotY} ${lens1X},${coneBotY}" fill="url(#collimatedBeamGrad)" filter="url(#sim-glow)" />
                        <line x1="${lens1X}" y1="${coneTopY}" x2="${xTopHit}" y2="${coneTopY}" stroke="rgba(255,255,255,0.25)" stroke-width="1.2" stroke-dasharray="3 3" />
                        <line x1="${lens1X}" y1="${coneBotY}" x2="${xBotHit}" y2="${coneBotY}" stroke="rgba(255,255,255,0.25)" stroke-width="1.2" stroke-dasharray="3 3" />
                        <line x1="${lens1X}" y1="${lens1HitY}" x2="${hitX}" y2="${hitY}" stroke="#ffffff" stroke-width="2.8" filter="url(#sim-glow)" opacity="1.0" />
                        <circle cx="${hitX}" cy="${hitY}" r="5" fill="#f43f5e" filter="url(#sim-glow)" />
                        <text x="${(lens1X + hitX) / 2 - 45}" y="${Math.min(coneTopY, coneBotY) - 8}" fill="#cbd5e1" font-size="12" font-weight="bold">校正平行光束</text>
                    `;
                } else {
                    // 平行光高度過高或過低，錯過光柵表面，直射箱壁
                    svgHtml += `
                        <polygon points="${slitX},${slitY - 1} ${lens1X},${coneTopY} ${lens1X},${coneBotY} ${slitX},${slitY + 1}" fill="url(#slitSpreadGrad)" filter="url(#sim-glow)" />
                        <polygon points="${lens1X},${coneTopY} ${missEndX},${coneTopY} ${missEndX},${coneBotY} ${lens1X},${coneBotY}" fill="url(#collimatedBeamGrad)" filter="url(#sim-glow)" />
                        <line x1="${slitX}" y1="${slitY}" x2="${lens1X}" y2="${lens1HitY}" stroke="#ffffff" stroke-width="2.6" filter="url(#sim-glow)" opacity="1.0" />
                        <line x1="${lens1X}" y1="${lens1HitY}" x2="${missEndX}" y2="${missEndY}" stroke="#ffffff" stroke-width="2.2" filter="url(#sim-glow)" opacity="0.85" />
                        <circle cx="${missEndX}" cy="${missEndY}" r="5" fill="#ffffff" opacity="0.75" />
                        <text x="${missEndX - 170}" y="${missEndY - 10}" fill="#94a3b8" font-size="12" font-weight="bold">平行光偏離錯過光柵（直射箱壁）</text>
                    `;
                }
            } else {
                // [無準直鏡 (手搓基礎版)]
                // 1. 狹縫出來後一段仍呈現「稍微散開的淺白色光線」
                svgHtml += `
                    <polygon points="${slitX},${slitY - 1} ${spEndX},${spTopY} ${spEndX},${spBotY} ${slitX},${slitY + 1}" fill="url(#slitSpreadGrad)" filter="url(#sim-glow)" />
                    <text x="${slitX + 25}" y="${slitY - 15}" fill="#94a3b8" font-size="11" font-weight="600">微散淺白光</text>
                `;

                // 2. 後面則僅以白色入射光直達光柵 (或箱壁)
                if (hitGrating) {
                    svgHtml += `
                        <line x1="${slitX}" y1="${slitY}" x2="${hitX}" y2="${hitY}" stroke="#ffffff" stroke-width="2.8" filter="url(#sim-glow)" opacity="1.0" />
                        <circle cx="${hitX}" cy="${hitY}" r="5" fill="#f43f5e" filter="url(#sim-glow)" />
                    `;
                } else {
                    svgHtml += `
                        <line x1="${slitX}" y1="${slitY}" x2="${missEndX}" y2="${missEndY}" stroke="#ffffff" stroke-width="2.2" filter="url(#sim-glow)" opacity="0.85" />
                        <circle cx="${missEndX}" cy="${missEndY}" r="5" fill="#ffffff" opacity="0.75" />
                        <text x="${Math.min(missEndX - 145, 720)}" y="${missEndY - 10}" fill="#94a3b8" font-size="12" font-weight="bold">未命中光柵（直射箱壁）</text>
                    `;
                }
            }

            // C. 命中光柵後的反射與繞射 (若未命中光柵則完全不繪製)
            if (hitGrating) {
                // 1. 主反射白線 + 淡灰色微散射錐體 (方向嚴格依據反射定律 reflAngle 動態更新)
                svgHtml += `
                    <polygon points="${hitX},${hitY} ${coneX1},${coneY1} ${coneX2},${coneY2}" fill="url(#diffuseConeGrad)" stroke="rgba(203, 213, 225, 0.25)" stroke-width="1.2" stroke-dasharray="3 3" />
                    <line x1="${hitX}" y1="${hitY}" x2="${zeroEndX}" y2="${zeroEndY}" stroke="#ffffff" stroke-width="2.8" filter="url(#sim-glow)" opacity="0.95" />
                    <text x="${zeroEndX - 40}" y="${zeroEndY - 8}" fill="#cbd5e1" font-size="12" font-weight="bold">主反射白線 (m=0)</text>
                `;

                // 2. 第一級彩虹光束展開 (各波長角度嚴格依據光柵方程式動態偏折)
                diffractionRays.forEach(ray => {
                    if (!ray.valid) return;
                    const width = state.lens1Installed && state.lens2Installed ? 4.2 : 3.2;
                    const rayOpacity = state.lens1Installed ? 0.96 : 0.85;

                    if (state.lens2Installed) {
                        const dyLens = lens2Y - hitY;
                        const lensHitX = hitX + dyLens / Math.tan(ray.shootAngleRad);
                        svgHtml += `
                            <line x1="${hitX}" y1="${hitY}" x2="${lensHitX}" y2="${lens2Y}" stroke="${ray.c}" stroke-width="${width}" opacity="${rayOpacity}" filter="url(#sim-glow)" />
                            <line x1="${lensHitX}" y1="${lens2Y}" x2="${ray.hitX}" y2="${cameraY - 12}" stroke="${ray.c}" stroke-width="${width + 0.6}" opacity="1.0" filter="url(#sim-glow)" />
                        `;
                    } else {
                        svgHtml += `
                            <line x1="${hitX}" y1="${hitY}" x2="${ray.hitX}" y2="${cameraY - 12}" stroke="${ray.c}" stroke-width="${width}" opacity="${rayOpacity}" filter="url(#sim-glow)" />
                        `;
                    }
                });
            }
        }

        // ==========================================
        // 元件實體繪製與互動熱區 (放大元件與清晰大字體)
        // ==========================================
        svgHtml += `
            <line x1="160" y1="150" x2="870" y2="150" stroke="rgba(255,255,255,0.08)" stroke-dasharray="3 3" />
            <line x1="530" y1="60" x2="530" y2="470" stroke="rgba(255,255,255,0.08)" stroke-dasharray="3 3" />

            <!-- A. 光源 -->
            <g class="interactive-part" id="part-light" transform="translate(${lightSourceX}, ${lightSourceY})">
                <rect x="-40" y="-22" width="62" height="44" rx="8" fill="${state.lightOn ? '#3b82f6' : '#334155'}" stroke="#93c5fd" stroke-width="2.5" />
                <path d="M 22 -16 L 36 -24 L 36 24 L 22 16 Z" fill="${state.lightOn ? '#fbbf24' : '#64748b'}" />
                <circle cx="-10" cy="0" r="12" fill="${state.lightOn ? '#fef08a' : '#1e293b'}" filter="${state.lightOn ? 'url(#sim-glow)' : 'none'}" />
                <text x="-28" y="-28" fill="#60a5fa" font-size="14" font-weight="bold">複合光源</text>
                <text x="-19" y="5" font-size="15">${state.lightOn ? '💡' : '⚪'}</text>
                <path d="M -34 -6 L -34 -14 L -29 -14 L -36 -22 L -43 -14 L -38 -14 L -38 -6 Z" fill="#94a3b8" />
                <path d="M -34 6 L -34 14 L -29 14 L -36 22 L -43 14 L -38 14 L -38 6 Z" fill="#94a3b8" />
            </g>

            <!-- B. 狹縫 -->
            <g class="interactive-part" id="part-slit" transform="translate(${slitX}, ${slitY})">
                <path d="M -10 -42 L 10 -42 L 10 -4 L -3 -4 Z" fill="#94a3b8" stroke="#cbd5e1" stroke-width="2" />
                <path d="M -10 42 L 10 42 L 10 4 L -3 4 Z" fill="#94a3b8" stroke="#cbd5e1" stroke-width="2" />
                <line x1="0" y1="-4" x2="0" y2="4" stroke="#38bdf8" stroke-width="3" />
                <circle cx="0" cy="0" r="18" fill="none" stroke="${state.activeComp === 'slit' ? '#60a5fa' : 'transparent'}" stroke-width="2.5" stroke-dasharray="3" />
                <text x="-16" y="-48" fill="#f8fafc" font-size="15" font-weight="bold">狹縫</text>
                <text x="-32" y="58" fill="#94a3b8" font-size="11" font-weight="600">0.1 mm</text>
            </g>

            <!-- C. 準直鏡 1 -->
            <g id="slot-lens1" transform="translate(${lens1X}, ${lens1Y})">
                <rect x="-18" y="-44" width="36" height="88" rx="6" fill="none" stroke="#334155" stroke-dasharray="3 3" />
                ${state.lens1Installed ? `
                    <g class="interactive-part" id="part-lens1">
                        <ellipse cx="0" cy="0" rx="12" ry="36" fill="rgba(56, 189, 248, 0.28)" stroke="#38bdf8" stroke-width="3" />
                        <rect x="-8" y="-48" width="16" height="8" fill="#475569" />
                        <rect x="-8" y="40" width="16" height="8" fill="#475569" />
                        <circle cx="0" cy="0" r="22" fill="none" stroke="${state.activeComp === 'lens1' ? '#38bdf8' : 'transparent'}" stroke-width="2.5" stroke-dasharray="3" />
                        <text x="-26" y="-54" fill="#38bdf8" font-size="15" font-weight="bold">準直鏡 1</text>
                        <text x="-26" y="60" fill="#94a3b8" font-size="11" font-weight="600">f = 16cm</text>
                    </g>
                ` : `
                    <text x="-40" y="-52" fill="#475569" font-size="13" font-weight="bold">[準直鏡1槽 (空)]</text>
                `}
            </g>

            <!-- D. 光柵 (預設 CD 31°) -->
            <g class="interactive-part" id="part-grating">
                <line x1="${gx1}" y1="${gy1}" x2="${gx2}" y2="${gy2}" stroke="#1e293b" stroke-width="12" stroke-linecap="round" />
                <line x1="${gx1}" y1="${gy1}" x2="${gx2}" y2="${gy2}" stroke="#60a5fa" stroke-width="6.5" stroke-linecap="round" />
                <!-- 旋轉中心機械轉軸 -->
                <circle cx="${gratingX}" cy="${gratingY}" r="4.5" fill="#334155" stroke="#94a3b8" stroke-width="2" />
                <line x1="${gratingX}" y1="${gratingY}" x2="${gratingX - 42 * Math.sin(phiRad)}" y2="${gratingY - 42 * Math.cos(phiRad)}" stroke="#f472b6" stroke-width="1.5" stroke-dasharray="3 2" />
                <text x="${gratingX + 18}" y="${gratingY - 24}" fill="#60a5fa" font-size="16" font-weight="bold">${cfg.name}</text>
                <text x="${gratingX + 18}" y="${gratingY - 6}" fill="#94a3b8" font-size="13" font-weight="600">φ = ${state.gratingAngle.toFixed(1)}° (${cfg.linesText})</text>
                <circle cx="${gratingX}" cy="${gratingY}" r="30" fill="none" stroke="${state.activeComp === 'grating' ? '#f43f5e' : 'transparent'}" stroke-width="2.5" stroke-dasharray="4" />
            </g>

            <!-- E. 消光隔板 -->
            <g class="interactive-part" id="part-baffle">
                <rect x="430" y="210" width="12" height="115" rx="3" fill="#0f172a" stroke="#64748b" stroke-width="2.5" />
                <path d="M 423 325 L 449 325 L 436 312 Z" fill="#64748b" />
                <circle cx="436" cy="265" r="22" fill="none" stroke="${state.activeComp === 'baffle' ? '#fbbf24' : 'transparent'}" stroke-width="2.5" stroke-dasharray="3" />
                <text x="350" y="255" fill="#e2e8f0" font-size="14" font-weight="bold">消光隔板</text>
                <text x="340" y="274" fill="#94a3b8" font-size="11" font-weight="600">擋住零級反射光</text>
            </g>

            <!-- F. 聚焦鏡 2 -->
            <g id="slot-lens2" transform="translate(${lens2X}, ${lens2Y})">
                <rect x="-46" y="-16" width="92" height="32" rx="6" fill="none" stroke="#334155" stroke-dasharray="3 3" />
                ${state.lens2Installed ? `
                    <g class="interactive-part" id="part-lens2">
                        <ellipse cx="0" cy="0" rx="40" ry="11" fill="rgba(192, 132, 252, 0.28)" stroke="#c084fc" stroke-width="3" />
                        <rect x="-50" y="-7" width="8" height="14" fill="#475569" />
                        <rect x="42" y="-7" width="8" height="14" fill="#475569" />
                        <circle cx="0" cy="0" r="26" fill="none" stroke="${state.activeComp === 'lens2' ? '#c084fc' : 'transparent'}" stroke-width="2.5" stroke-dasharray="3" />
                        <text x="54" y="4" fill="#c084fc" font-size="15" font-weight="bold">聚焦鏡 2</text>
                        <text x="54" y="20" fill="#94a3b8" font-size="11" font-weight="600">成像聚焦</text>
                    </g>
                ` : `
                    <text x="54" y="4" fill="#475569" font-size="13" font-weight="bold">[聚焦鏡2槽 (空)]</text>
                `}
            </g>

            <!-- G. 相機鏡頭 -->
            <g class="interactive-part" id="part-camera" transform="translate(${cameraX}, ${cameraY})">
                <rect x="-55" y="0" width="110" height="52" rx="10" fill="#1e293b" stroke="${isCaptured ? '#22c55e' : '#64748b'}" stroke-width="${isCaptured ? 3.5 : 2.5}" />
                <circle cx="0" cy="22" r="20" fill="#0f172a" stroke="#38bdf8" stroke-width="2.5" />
                <rect x="-12" y="14" width="24" height="16" rx="3" fill="#0284c7" opacity="0.85" />
                <circle cx="0" cy="22" r="26" fill="none" stroke="${isCaptured ? '#22c55e' : '#f59e0b'}" stroke-width="2" stroke-dasharray="${isCaptured ? 'none' : '4 3'}" filter="${isCaptured ? 'url(#sim-glow)' : 'none'}" />
                <text x="-32" y="-12" fill="${isCaptured ? '#22c55e' : '#38bdf8'}" font-size="14" font-weight="bold">${isCaptured ? '🎯 收光中' : '相機鏡頭'}</text>
                <text x="-38" y="46" fill="#94a3b8" font-size="11" font-weight="600">CMOS 感測器</text>
                <path d="M -48 24 L -56 24 L -56 20 L -63 24 L -56 28 L -56 24 Z" fill="#94a3b8" />
                <path d="M 48 24 L 56 24 L 56 20 L 63 24 L 56 28 L 56 24 Z" fill="#94a3b8" />
            </g>
        `;

        simSvg.innerHTML = svgHtml;

        // 綁定 SVG 元件互動事件
        bindSvgEvents();

        // 繪製相機感光光譜畫面
        drawLiveSpectrum(isCaptured, hitGrating, alignDiff);
    }

    // ----------------------------------------------------
    // SVG 內部互動事件 (點擊彈窗、拖曳調整)
    // ----------------------------------------------------
    function bindSvgEvents() {
        const addComponentClick = (id, compKey) => {
            const el = document.getElementById(id);
            if (el) {
                el.addEventListener('click', (e) => {
                    e.stopPropagation();
                    toggleComponentModal(compKey);
                    renderSimulator();
                });
            }
        };

        addComponentClick('part-slit', 'slit');
        addComponentClick('part-baffle', 'baffle');
        addComponentClick('part-lens1', 'lens1');
        addComponentClick('part-lens2', 'lens2');

        // 1. 光源拖曳與開關
        const partLight = document.getElementById('part-light');
        if (partLight) {
            let startY = 0;
            let startAngle = 0;
            let hasMoved = false;

            const onPointerMove = (e) => {
                const dy = e.clientY - startY;
                if (Math.abs(dy) > 3) hasMoved = true;
                let newAngle = startAngle - dy * 0.25;
                newAngle = Math.max(-15, Math.min(15, newAngle));
                state.lightAngleDeg = Math.round(newAngle * 2) / 2;
                if (rangeLightY) rangeLightY.value = state.lightAngleDeg;
                updateControlsUI();
                renderSimulator();
            };

            const onPointerUp = () => {
                window.removeEventListener('pointermove', onPointerMove);
                window.removeEventListener('pointerup', onPointerUp);
                if (!hasMoved) {
                    toggleComponentModal('light');
                    renderSimulator();
                }
            };

            partLight.addEventListener('pointerdown', (e) => {
                e.stopPropagation();
                startY = e.clientY;
                startAngle = state.lightAngleDeg;
                hasMoved = false;
                window.addEventListener('pointermove', onPointerMove);
                window.addEventListener('pointerup', onPointerUp);
            });
        }

        // 2. 光柵拖曳旋轉
        const partGrating = document.getElementById('part-grating');
        if (partGrating) {
            let startY = 0;
            let startAngle = 0;
            let hasMoved = false;

            const onGratingMove = (e) => {
                const dy = e.clientY - startY;
                if (Math.abs(dy) > 3) hasMoved = true;
                let newAngle = startAngle - dy * 0.2;
                newAngle = Math.max(10, Math.min(45, newAngle));
                state.gratingAngle = Math.round(newAngle * 2) / 2;
                if (rangeGratingAngle) rangeGratingAngle.value = state.gratingAngle;
                updateControlsUI();
                renderSimulator();
            };

            const onGratingUp = () => {
                window.removeEventListener('pointermove', onGratingMove);
                window.removeEventListener('pointerup', onGratingUp);
                if (!hasMoved) {
                    toggleComponentModal('grating');
                    renderSimulator();
                }
            };

            partGrating.addEventListener('pointerdown', (e) => {
                e.stopPropagation();
                startY = e.clientY;
                startAngle = state.gratingAngle;
                hasMoved = false;
                window.addEventListener('pointermove', onGratingMove);
                window.addEventListener('pointerup', onGratingUp);
            });
        }

        // 3. 相機拖曳收光
        const partCamera = document.getElementById('part-camera');
        if (partCamera) {
            let startX = 0;
            let startOffset = 0;
            let hasMoved = false;

            const onCameraMove = (e) => {
                const dx = e.clientX - startX;
                if (Math.abs(dx) > 2) hasMoved = true;
                let newOffset = startOffset + dx * 0.4;
                newOffset = Math.max(-40, Math.min(40, newOffset));
                state.cameraOffset = Math.round(newOffset);
                if (rangeCameraX) rangeCameraX.value = state.cameraOffset;
                updateControlsUI();
                renderSimulator();
            };

            const onCameraUp = () => {
                window.removeEventListener('pointermove', onCameraMove);
                window.removeEventListener('pointerup', onCameraUp);
                if (!hasMoved) {
                    toggleComponentModal('camera');
                    renderSimulator();
                }
            };

            partCamera.addEventListener('pointerdown', (e) => {
                e.stopPropagation();
                startX = e.clientX;
                startOffset = state.cameraOffset;
                hasMoved = false;
                window.addEventListener('pointermove', onCameraMove);
                window.addEventListener('pointerup', onCameraUp);
            });
        }
    }

    // ----------------------------------------------------
    // 相機即時感光畫面繪製 (Canvas)
    // ----------------------------------------------------
    function drawLiveSpectrum(isCaptured, hitGrating, alignDiff) {
        if (!liveCtx) return;
        const w = liveCanvas.width;
        const h = liveCanvas.height;

        liveCtx.fillStyle = '#030712';
        liveCtx.fillRect(0, 0, w, h);

        if (!state.lightOn) {
            liveCtx.fillStyle = '#475569';
            liveCtx.font = '13px sans-serif';
            liveCtx.textAlign = 'center';
            liveCtx.fillText('光源已關閉 · CMOS 感光無訊號', w / 2, h / 2 + 5);
            return;
        }

        if (!hitGrating) {
            liveCtx.fillStyle = '#f43f5e';
            liveCtx.font = '12px sans-serif';
            liveCtx.textAlign = 'center';
            liveCtx.fillText('⚠️ 入射光線偏離，未打中光柵表面（無彩虹產生）', w / 2, h / 2 + 5);
            return;
        }

        const offsetPx = -alignDiff * 2.8;

        if (Math.abs(alignDiff) > 42) {
            liveCtx.fillStyle = '#f59e0b';
            liveCtx.font = '12px sans-serif';
            liveCtx.textAlign = 'center';
            liveCtx.fillText(`⚠️ 光譜已完全偏出相機視野 (${alignDiff < 0 ? '偏左' : '偏右'})，請調整光柵角度或相機位置`, w / 2, h / 2 + 5);
            return;
        }

        // 裁切在 CMOS 感光窗口範圍內
        liveCtx.save();
        liveCtx.beginPath();
        liveCtx.rect(12, 6, w - 24, h - 12);
        liveCtx.clip();

        // 繪製連續漸層彩虹 (隨收光偏移即時橫移)
        const gradX1 = 20 + offsetPx;
        const gradX2 = w - 20 + offsetPx;
        const grad = liveCtx.createLinearGradient(gradX1, 0, gradX2, 0);
        grad.addColorStop(0.0, '#3b0764');
        grad.addColorStop(0.12, '#6d28d9');
        grad.addColorStop(0.25, '#1d4ed8');
        grad.addColorStop(0.40, '#06b6d4');
        grad.addColorStop(0.55, '#22c55e');
        grad.addColorStop(0.70, '#eab308');
        grad.addColorStop(0.85, '#ea580c');
        grad.addColorStop(1.0, '#b91c1c');

        liveCtx.fillStyle = grad;
        liveCtx.fillRect(15 + offsetPx, 8, w - 30, h - 16);

        // 日光燈水銀發射特徵譜線 (銳利度隨透鏡配置改變)
        const isSharp = state.lens1Installed && state.lens2Installed;
        const lineAlpha = isSharp ? 0.95 : 0.6;
        const lineWidth = isSharp ? 2.5 : 5;

        // 436nm 藍紫線
        liveCtx.strokeStyle = `rgba(167, 139, 250, ${lineAlpha})`;
        liveCtx.lineWidth = lineWidth;
        liveCtx.beginPath();
        liveCtx.moveTo(w * 0.20 + offsetPx, 5);
        liveCtx.lineTo(w * 0.20 + offsetPx, h - 5);
        liveCtx.stroke();

        // 546nm 綠線
        liveCtx.strokeStyle = `rgba(134, 239, 172, ${lineAlpha})`;
        liveCtx.lineWidth = lineWidth;
        liveCtx.beginPath();
        liveCtx.moveTo(w * 0.54 + offsetPx, 5);
        liveCtx.lineTo(w * 0.54 + offsetPx, h - 5);
        liveCtx.stroke();

        // 579nm 雙黃線
        liveCtx.strokeStyle = `rgba(254, 240, 138, ${lineAlpha})`;
        liveCtx.lineWidth = lineWidth;
        liveCtx.beginPath();
        liveCtx.moveTo(w * 0.68 + offsetPx, 5);
        liveCtx.lineTo(w * 0.68 + offsetPx, h - 5);
        liveCtx.stroke();

        liveCtx.restore();

        // 噪點
        liveCtx.fillStyle = 'rgba(255, 255, 255, 0.04)';
        for (let i = 0; i < 70; i++) {
            liveCtx.fillRect(Math.random() * w, Math.random() * h, 2, 2);
        }

        // 若偏離中心但仍在視野內，提示未對齊
        if (!isCaptured) {
            liveCtx.fillStyle = 'rgba(245, 158, 11, 0.85)';
            liveCtx.font = '10px sans-serif';
            liveCtx.textAlign = 'right';
            liveCtx.fillText('⚠️ 光譜未居中', w - 16, h - 8);
        }

        // 噪點
        liveCtx.fillStyle = 'rgba(255, 255, 255, 0.04)';
        for (let i = 0; i < 70; i++) {
            liveCtx.fillRect(Math.random() * w, Math.random() * h, 2, 2);
        }
    }

    // 初始化模擬器 (預設 CD 31°)
    updateControlsUI();
    renderSimulator();
}

// ----------------------------------------------------
// 分頁一、分頁二 SVG 圖繪製
// ----------------------------------------------------

// ----------------------------------------------------
// 全螢幕大分頁 (Full-Screen Tab Pages) 導航與圖形繪製引擎
// ----------------------------------------------------

function initTabNavigation() {
    const tabs = document.querySelectorAll('.tab-page');
    if (!tabs.length) return;

    function activateTab(tabId) {
        if (!tabId || tabId === '' || tabId === '#') tabId = 'home';
        tabId = tabId.replace(/^#/, '').trim();

        // 支援別名對應
        if (tabId === 'reflection' || tabId === 'ref' || tabId === 'reflection.html') {
            tabId = 'ref-cd';
        }
        if (tabId === 'transmission' || tabId === 'trans' || tabId === 'transmission.html') {
            tabId = 'trans-cd';
        }

        const validTabs = ['home', 'ref-dvd', 'ref-1000', 'ref-cd', 'trans-dvd', 'trans-1000', 'trans-cd'];
        if (!validTabs.includes(tabId)) {
            tabId = 'home';
        }

        // 1. 切換各大分頁的顯示狀態
        let targetPage = null;
        tabs.forEach(page => {
            if (page.id === `page-${tabId}`) {
                page.classList.add('active');
                page.style.display = 'block';
                targetPage = page;
            } else {
                page.classList.remove('active');
                page.style.display = 'none';
            }
        });

        if (!targetPage) {
            const home = document.getElementById('page-home');
            if (home) {
                home.classList.add('active');
                home.style.display = 'block';
            }
        }

        // 2. 更新導航列各按鈕 active 樣式
        document.querySelectorAll('.nav-link, .dropdown-item, .grating-pill').forEach(el => {
            const target = el.getAttribute('data-tab') || (el.getAttribute('href') || '').replace('#', '');
            if (target === tabId) {
                el.classList.add('active');
            } else {
                el.classList.remove('active');
            }
        });

        // 3. 更新下拉選單父項目的 active 高亮
        const refDropdown = document.getElementById('nav-dropdown-ref');
        const transDropdown = document.getElementById('nav-dropdown-trans');
        if (refDropdown) {
            const isRef = tabId.startsWith('ref-');
            refDropdown.classList.toggle('active', isRef);
            const parentLink = refDropdown.querySelector('.nav-parent-link');
            if (parentLink) parentLink.classList.toggle('active', isRef);
        }
        if (transDropdown) {
            const isTrans = tabId.startsWith('trans-');
            transDropdown.classList.toggle('active', isTrans);
            const parentLink = transDropdown.querySelector('.nav-parent-link');
            if (parentLink) parentLink.classList.toggle('active', isTrans);
        }

        // 4. 關閉任何開啟中的下拉選單
        document.querySelectorAll('.nav-dropdown').forEach(d => d.classList.remove('open'));

        // 5. 平滑滾動至頁頂
        window.scrollTo({ top: 0, behavior: 'smooth' });

        // 6. 重新排版 MathJax
        if (window.MathJax && MathJax.typesetPromise) {
            MathJax.typesetPromise();
        }

        // 7. 繪製圖形
        if (typeof renderCmosCanvases === 'function') {
            renderCmosCanvases();
        }
        if (typeof initSubpageSvgs === 'function') {
            initSubpageSvgs();
        }
    }

    // 支援 hashchange 事件
    window.addEventListener('hashchange', () => {
        activateTab(window.location.hash);
    });

    // 強大且相容的點擊攔截監聽（適用 iframe、本地檔案與行動裝置）
    document.addEventListener('click', e => {
        const link = e.target.closest('a[href^="#"], [data-tab]');
        if (link) {
            const target = link.getAttribute('data-tab') || (link.getAttribute('href') || '').replace('#', '');
            if (target) {
                e.preventDefault();
                activateTab(target);
                if (window.location.hash !== '#' + target) {
                    try {
                        history.pushState(null, '', '#' + target);
                    } catch (err) {
                        window.location.hash = '#' + target;
                    }
                }
            }
        }
    });

    // 啟動初始分頁
    const initialHash = window.location.hash || 'home';
    activateTab(initialHash);
}

function drawCmosSpectrum(canvasId, gratingType) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const w = canvas.width;
    const h = canvas.height;

    ctx.fillStyle = '#030712';
    ctx.fillRect(0, 0, w, h);

    // 依光柵色散能力設定光斑分佈
    let startX, endX, intensity;
    if (gratingType === 'dvd') {
        startX = w * 0.04;
        endX = w * 0.96;
        intensity = 0.85;
    } else if (gratingType === '1000') {
        startX = w * 0.15;
        endX = w * 0.85;
        intensity = 0.92;
    } else {
        startX = w * 0.26;
        endX = w * 0.74;
        intensity = 1.0;
    }

    // 繪製連續漸層光譜彩虹
    const grad = ctx.createLinearGradient(startX, 0, endX, 0);
    grad.addColorStop(0.0, 'rgba(148, 0, 211, ' + (0.5 * intensity) + ')');
    grad.addColorStop(0.18, 'rgba(0, 0, 255, ' + (0.65 * intensity) + ')');
    grad.addColorStop(0.40, 'rgba(0, 255, 255, ' + (0.75 * intensity) + ')');
    grad.addColorStop(0.55, 'rgba(0, 255, 0, ' + (0.85 * intensity) + ')');
    grad.addColorStop(0.70, 'rgba(255, 255, 0, ' + (0.9 * intensity) + ')');
    grad.addColorStop(0.85, 'rgba(255, 128, 0, ' + (0.8 * intensity) + ')');
    grad.addColorStop(1.0, 'rgba(255, 0, 0, ' + (0.65 * intensity) + ')');

    ctx.fillStyle = grad;
    ctx.fillRect(startX, 6, endX - startX, h - 12);

    // 繪製水銀日光燈特徵發射線 (Mercury Emission Lines)
    const lines = [
        { ratio: 0.18, color: '#38bdf8', width: 2.2, alpha: 0.95 }, // 436nm
        { ratio: 0.55, color: '#4ade80', width: 2.6, alpha: 1.0 },  // 546nm
        { ratio: 0.69, color: '#facc15', width: 1.8, alpha: 0.95 }, // 577nm
        { ratio: 0.72, color: '#facc15', width: 1.8, alpha: 0.95 }  // 579nm
    ];

    lines.forEach(l => {
        const lx = startX + (endX - startX) * l.ratio;
        ctx.strokeStyle = l.color;
        ctx.lineWidth = l.width;
        ctx.globalAlpha = l.alpha * intensity;
        ctx.beginPath();
        ctx.moveTo(lx, 4);
        ctx.lineTo(lx, h - 4);
        ctx.stroke();
    });
    ctx.globalAlpha = 1.0;

    // 外框修飾
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.15)';
    ctx.lineWidth = 1;
    ctx.strokeRect(0, 0, w, h);
}

function renderCmosCanvases() {
    drawCmosSpectrum('cmos-canvas-ref-dvd', 'dvd');
    drawCmosSpectrum('cmos-canvas-ref-1000', '1000');
    drawCmosSpectrum('cmos-canvas-ref-cd', 'cd');
    drawCmosSpectrum('cmos-canvas-trans-dvd', 'dvd');
    drawCmosSpectrum('cmos-canvas-trans-1000', '1000');
    drawCmosSpectrum('cmos-canvas-trans-cd', 'cd');
}

function initSubpageSvgs() {
                function drawLargeReflectionSVG(containerId, anglePhi, displayAngleText, gratingAngleText, l1Text, l2Text, gratingLabel) {
        const el = document.getElementById(containerId);
        if (!el) return;

        // 全面加大畫布與空間留白，確保「字與圖中的線條徹底分開，零重疊」
        // Canvas: 820 x 560
        const cx = 450;
        const cy = 210;
        const slitX = 130;
        const phoneY = 440;
        const baffleX = 280;

        const rad = anglePhi * Math.PI / 180;
        const gratingLen = 65;
        const gx1 = cx - gratingLen * Math.cos(rad);
        const gy1 = cy - gratingLen * Math.sin(rad);
        const gx2 = cx + gratingLen * Math.cos(rad);
        const gy2 = cy + gratingLen * Math.sin(rad);

        const diffLength = 230;
        const colors = [
            { c: '#9400D3', a: 96 },
            { c: '#0000FF', a: 93 },
            { c: '#00FF00', a: 90 },
            { c: '#FFFF00', a: 87 },
            { c: '#FF0000', a: 84 }
        ];

        let rainbowLines = colors.map((col, idx) => {
            const radAngle = col.a * Math.PI / 180;
            const endX = cx + diffLength * Math.cos(radAngle);
            const endY = cy + diffLength * Math.sin(radAngle);
            return `<line x1="${cx}" y1="${cy}" x2="${endX}" y2="${endY}" stroke="${col.c}" stroke-width="4.5" class="animated-beam" filter="url(#glow)" opacity="0.95" style="animation-delay: ${idx * 0.1}s;" />`;
        }).join('');

        const svg = `
            <svg viewBox="0 0 820 560" xmlns="http://www.w3.org/2000/svg" style="font-family: 'Outfit', 'Noto Sans TC', -apple-system, sans-serif;">
                <defs>
                    <filter id="glow" filterUnits="userSpaceOnUse" x="-50" y="-50" width="920" height="660">
                        <feGaussianBlur stdDeviation="3.5" result="coloredBlur"/>
                        <feMerge>
                            <feMergeNode in="coloredBlur"/>
                            <feMergeNode in="SourceGraphic"/>
                        </feMerge>
                    </filter>
                    <marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                        <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#94a3b8"/>
                    </marker>
                    <marker id="arrow-blue" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                        <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#38bdf8"/>
                    </marker>
                </defs>

                <!-- 1. 暗箱外盒邊界 (上方留 30px 空白放紙箱標籤，不互相重疊) -->
                <rect x="40" y="55" width="740" height="475" rx="16" fill="rgba(15, 23, 42, 0.55)" stroke="rgba(255, 255, 255, 0.12)" stroke-dasharray="6,4" stroke-width="2"/>
                <g transform="translate(60, 24)">
                    <rect x="0" y="0" width="310" height="28" rx="6" fill="#0f172a" stroke="rgba(255,255,255,0.2)" stroke-width="1.2"/>
                    <text x="14" y="19" fill="#cbd5e1" font-size="13" font-weight="700">📦 90° 直角消光紙箱 (內壁全消光黑化)</text>
                </g>

                <!-- 2. 光軸輔助中心虛線 (淡化處理，絕不遮掩文字) -->
                <line x1="50" y1="${cy}" x2="760" y2="${cy}" stroke="rgba(255,255,255,0.06)" stroke-dasharray="4" />
                <line x1="${cx}" y1="55" x2="${cx}" y2="520" stroke="rgba(255,255,255,0.06)" stroke-dasharray="4" />

                <!-- 3. 入射光束 (狹縫左側) -->
                <line x1="15" y1="${cy - 8}" x2="${slitX - 6}" y2="${cy - 8}" stroke="#ffffff" stroke-width="2.5" class="animated-beam" opacity="0.6" filter="url(#glow)" />
                <line x1="10" y1="${cy}" x2="${slitX - 6}" y2="${cy}" stroke="#ffffff" stroke-width="5" class="animated-beam" opacity="1.0" filter="url(#glow)" />
                <line x1="15" y1="${cy + 8}" x2="${slitX - 6}" y2="${cy + 8}" stroke="#ffffff" stroke-width="2.5" class="animated-beam" opacity="0.6" filter="url(#glow)" />

                <!-- 狹縫片 (金屬遮光刀片) -->
                <rect x="${slitX - 6}" y="${cy - 65}" width="12" height="57" fill="#94a3b8" rx="2" />
                <rect x="${slitX - 6}" y="${cy + 8}" width="12" height="57" fill="#94a3b8" rx="2" />
                
                <!-- 狹縫標籤 (獨立置於左上方 x=50, y=105，完全脫離任何線條) -->
                <g transform="translate(50, 105)">
                    <rect x="0" y="0" width="125" height="30" rx="7" fill="#0f172a" stroke="rgba(255,255,255,0.25)" stroke-width="1.5"/>
                    <text x="12" y="20" fill="#f8fafc" font-size="13" font-weight="800">✂️ 狹縫 (0.1mm)</text>
                </g>

                <!-- 4. 狹縫至光柵平行光束 -->
                <line x1="${slitX + 6}" y1="${cy}" x2="${cx}" y2="${cy}" stroke="#ffffff" stroke-width="4.5" class="animated-beam-fast" opacity="1.0" filter="url(#glow)" />

                <!-- 5. 尺寸標註 L1 (將標註線段分兩段，中間空出 180px 專門放文字，線絕不穿過文字！) -->
                <line x1="${slitX}" y1="95" x2="${slitX}" y2="65" stroke="#64748b" stroke-width="1.2" stroke-dasharray="3,3" />
                <line x1="${cx}" y1="95" x2="${cx}" y2="65" stroke="#64748b" stroke-width="1.2" stroke-dasharray="3,3" />
                <!-- 左段箭頭線 -->
                <line x1="${slitX}" y1="75" x2="200" y2="75" stroke="#94a3b8" stroke-width="1.8" stroke-dasharray="4" marker-start="url(#arrow)" />
                <!-- L1 文字框 (在斷線處中央) -->
                <g transform="translate(205, 58)">
                    <rect x="0" y="0" width="170" height="34" rx="8" fill="#0f172a" stroke="#94a3b8" stroke-width="1.5"/>
                    <text x="85" y="22" text-anchor="middle" fill="#f1f5f9" font-size="14" font-weight="800">狹縫距 L₁: ${l1Text}</text>
                </g>
                <!-- 右段箭頭線 -->
                <line x1="380" y1="75" x2="${cx}" y2="75" stroke="#94a3b8" stroke-width="1.8" stroke-dasharray="4" marker-end="url(#arrow)" />

                <!-- 6. 消光隔板 (Baffle) - 垂直擋板位於 x=280 -->
                <line x1="${baffleX}" y1="${cy + 20}" x2="${baffleX}" y2="370" stroke="#f59e0b" stroke-width="5" stroke-dasharray="6,4" stroke-linecap="round"/>
                <!-- 消光擋板文字標籤 (置於擋板左側 x=75，距離擋板有 35px 淨空，絕不壓線！) -->
                <g transform="translate(75, 290)">
                    <rect x="0" y="0" width="170" height="52" rx="8" fill="#0f172a" stroke="#f59e0b" stroke-width="1.8"/>
                    <text x="14" y="23" fill="#fbbf24" font-size="14" font-weight="800">🛡️ 消光擋板 (Baffle)</text>
                    <text x="14" y="42" fill="#cbd5e1" font-size="12">阻隔未繞射直射雜光</text>
                </g>

                <!-- 7. 第一級繞射彩虹光束 -->
                ${rainbowLines}

                <!-- 8. 光柵鏡面本體 -->
                <line x1="${gx1}" y1="${gy1}" x2="${gx2}" y2="${gy2}" stroke="#60a5fa" stroke-width="8" stroke-linecap="round" filter="url(#glow)"/>
                <line x1="${gx1 - 2}" y1="${gy1 - 2}" x2="${gx2 - 2}" y2="${gy2 - 2}" stroke="#1e293b" stroke-width="4"/>

                <!-- 光柵名稱標籤 (獨立置於光柵右上方 x=550, y=135) -->
                <g transform="translate(550, 135)">
                    <rect x="0" y="0" width="165" height="34" rx="8" fill="#0f172a" stroke="#60a5fa" stroke-width="1.8"/>
                    <text x="14" y="23" fill="#93c5fd" font-size="14" font-weight="800">💿 ${gratingLabel}</text>
                </g>

                <!-- 9. 角度標籤 1：光柵面與入射線夾角 (在光柵左上空域 x=300, y=130，無任何線條重疊) -->
                <path d="M ${cx - 55} ${cy} A 55 55 0 0 1 ${cx - 55 * Math.cos(rad)} ${cy - 55 * Math.sin(rad)}" fill="none" stroke="#f472b6" stroke-width="3" />
                <g transform="translate(300, 130)">
                    <rect x="0" y="0" width="135" height="32" rx="7" fill="#0f172a" stroke="#f472b6" stroke-width="1.8"/>
                    <text x="67" y="21" text-anchor="middle" fill="#f472b6" font-size="14" font-weight="900">光柵傾角: ${displayAngleText}</text>
                </g>

                <!-- 10. 角度標籤 2：光柵面與鏡頭軸夾角 (在彩虹光束右側 x=495, y=240，文字與光束留 30px 空隙) -->
                <path d="M ${cx} ${cy + 55} A 55 55 0 0 0 ${cx + 55 * Math.cos(rad)} ${cy + 55 * Math.sin(rad)}" fill="none" stroke="#c084fc" stroke-width="3" />
                <g transform="translate(495, 240)">
                    <rect x="0" y="0" width="145" height="32" rx="7" fill="#0f172a" stroke="#c084fc" stroke-width="1.8"/>
                    <text x="72" y="21" text-anchor="middle" fill="#c084fc" font-size="14" font-weight="900">軸線夾角: ${gratingAngleText}</text>
                </g>

                <!-- 11. 手機相機 (置於下方 y=440) -->
                <rect x="${cx - 50}" y="${phoneY}" width="100" height="46" rx="10" fill="#1e293b" stroke="#94a3b8" stroke-width="2.5"/>
                <circle cx="${cx}" cy="${phoneY}" r="11" fill="#0f172a" stroke="#38bdf8" stroke-width="3.5"/>
                <!-- 相機標籤 (獨立置於正下方 y=500，居中對齊，不壓鏡頭) -->
                <g transform="translate(${cx - 90}, 500)">
                    <rect x="0" y="0" width="180" height="30" rx="7" fill="#0f172a" stroke="#38bdf8" stroke-width="1.5"/>
                    <text x="90" y="20" text-anchor="middle" fill="#f8fafc" font-size="13" font-weight="800">📱 手機鏡頭 CMOS 感光</text>
                </g>

                <!-- 12. 尺寸標註 L2 (在最右側 x=690，垂直線條分兩段，中間中空放文字，線完全不穿透文字！) -->
                <line x1="530" y1="${cy}" x2="715" y2="${cy}" stroke="#64748b" stroke-width="1.2" stroke-dasharray="3,3" />
                <line x1="505" y1="${phoneY}" x2="715" y2="${phoneY}" stroke="#64748b" stroke-width="1.2" stroke-dasharray="3,3" />
                <!-- 上段垂直箭頭線 -->
                <line x1="690" y1="${cy}" x2="690" y2="300" stroke="#38bdf8" stroke-width="2" stroke-dasharray="4" marker-start="url(#arrow-blue)" />
                <!-- L2 文字框 (垂直中空處) -->
                <g transform="translate(615, 308)">
                    <rect x="0" y="0" width="150" height="34" rx="8" fill="#0f172a" stroke="#38bdf8" stroke-width="1.8"/>
                    <text x="75" y="23" text-anchor="middle" fill="#38bdf8" font-size="14" font-weight="800">鏡頭距 L₂: ${l2Text}</text>
                </g>
                <!-- 下段垂直箭頭線 -->
                <line x1="690" y1="350" x2="690" y2="${phoneY}" stroke="#38bdf8" stroke-width="2" stroke-dasharray="4" marker-end="url(#arrow-blue)" />
            </svg>
        `;
        el.innerHTML = svg;
    }

                function drawLargeTransmissionSVG(containerId, tiltAngle, l1Text, l2Text, gratingLabel) {
        const el = document.getElementById(containerId);
        if (!el) return;

        // 全面加大畫布與空間留白，確保「字與圖中的線條徹底分開，零重疊」
        // Canvas: 820 x 560
        const cx = 400;
        const cy = 210;
        const slitX = 130;
        const rayLen = 220;

        const colors = [
            { c: '#9400D3', a: tiltAngle - 6 },
            { c: '#0000FF', a: tiltAngle - 3 },
            { c: '#00FF00', a: tiltAngle },
            { c: '#FFFF00', a: tiltAngle + 3 },
            { c: '#FF0000', a: tiltAngle + 6 }
        ];

        let rainbowLines = colors.map((col, idx) => {
            const radAngle = col.a * Math.PI / 180;
            const endX = cx + rayLen * Math.cos(radAngle);
            const endY = cy + rayLen * Math.sin(radAngle);
            return `<line x1="${cx}" y1="${cy}" x2="${endX}" y2="${endY}" stroke="${col.c}" stroke-width="4.5" class="animated-beam" filter="url(#glow)" opacity="0.95" style="animation-delay: ${idx * 0.1}s;" />`;
        }).join('');

        const greenRad = tiltAngle * Math.PI / 180;
        const px = cx + rayLen * Math.cos(greenRad);
        const py = cy + rayLen * Math.sin(greenRad);

        // L2 尺寸線向量運算：沿繞射中軸方向向量 u，向左下側平移足夠距離 (offset=100px)，確保徹底遠離最底層紅光束
        const ux = Math.cos(greenRad);
        const uy = Math.sin(greenRad);
        const nx = -Math.sin(greenRad);
        const ny = Math.cos(greenRad);
        const offset = 100;

        const d1x = cx + offset * nx;
        const d1y = cy + offset * ny;
        const d2x = px + offset * nx;
        const d2y = py + offset * ny;

        const midX = (d1x + d2x) / 2;
        const midY = (d1y + d2y) / 2;

        // 線條分兩段，中間為標註文字留出 110px 空隙，線條絕不穿過文字！
        const s1EndX = midX - 55 * ux;
        const s1EndY = midY - 55 * uy;
        const s2StartX = midX + 55 * ux;
        const s2StartY = midY + 55 * uy;

        // 偏折夾角弧線幾何定位
        const arcR = 60;
        const arcMidRad = greenRad / 2;
        const arcMidX = cx + arcR * Math.cos(arcMidRad);
        const arcMidY = cy + arcR * Math.sin(arcMidRad);

        // 相機文字標籤置於手機背後
        const camLblX = px + 40 * ux;
        const camLblY = py + 40 * uy;

        const svg = `
            <svg viewBox="0 0 820 560" xmlns="http://www.w3.org/2000/svg" style="font-family: 'Outfit', 'Noto Sans TC', -apple-system, sans-serif;">
                <defs>
                    <filter id="glow" filterUnits="userSpaceOnUse" x="-50" y="-50" width="920" height="660">
                        <feGaussianBlur stdDeviation="3.5" result="coloredBlur"/>
                        <feMerge>
                            <feMergeNode in="coloredBlur"/>
                            <feMergeNode in="SourceGraphic"/>
                        </feMerge>
                    </filter>
                    <marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                        <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#94a3b8"/>
                    </marker>
                    <marker id="arrow-blue" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                        <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#38bdf8"/>
                    </marker>
                </defs>

                <!-- 1. 穿透斜角暗箱外殼 (底部空間充裕包覆相機與L2標註) -->
                <polygon points="40,55 350,55 770,185 750,520 180,480 40,360" fill="rgba(15, 23, 42, 0.55)" stroke="rgba(255, 255, 255, 0.12)" stroke-dasharray="6,4" stroke-width="2"/>
                <g transform="translate(60, 24)">
                    <rect x="0" y="0" width="320" height="28" rx="6" fill="#0f172a" stroke="rgba(255,255,255,0.2)" stroke-width="1.2"/>
                    <text x="14" y="19" fill="#cbd5e1" font-size="13" font-weight="700">📦 穿透式斜角紙箱 (手機依繞射角傾斜安裝)</text>
                </g>

                <!-- 水平中心虛線 -->
                <line x1="45" y1="${cy}" x2="760" y2="${cy}" stroke="rgba(255,255,255,0.06)" stroke-dasharray="4" />

                <!-- 2. 0 級直射白光與消光吸光槽 (獨立右端) -->
                <line x1="${cx}" y1="${cy}" x2="745" y2="${cy}" stroke="rgba(255,255,255,0.35)" stroke-width="2.5" stroke-dasharray="5,4"/>
                <rect x="745" y="${cy - 20}" width="20" height="40" fill="#030712" stroke="#94a3b8" rx="3"/>
                <g transform="translate(640, 160)">
                    <rect x="0" y="0" width="155" height="28" rx="6" fill="#0f172a" stroke="rgba(255,255,255,0.18)"/>
                    <text x="10" y="19" fill="#94a3b8" font-size="12" font-weight="700">0級直行白光 (黑槽吸收)</text>
                </g>

                <!-- 3. 入射光束與狹縫 -->
                <line x1="15" y1="${cy - 8}" x2="${slitX - 6}" y2="${cy - 8}" stroke="#ffffff" stroke-width="2.5" class="animated-beam" opacity="0.6" filter="url(#glow)" />
                <line x1="10" y1="${cy}" x2="${slitX - 6}" y2="${cy}" stroke="#ffffff" stroke-width="5" class="animated-beam" opacity="1.0" filter="url(#glow)" />
                <line x1="15" y1="${cy + 8}" x2="${slitX - 6}" y2="${cy + 8}" stroke="#ffffff" stroke-width="2.5" class="animated-beam" opacity="0.6" filter="url(#glow)" />

                <rect x="${slitX - 6}" y="${cy - 65}" width="12" height="57" fill="#94a3b8" rx="2" />
                <rect x="${slitX - 6}" y="${cy + 8}" width="12" height="57" fill="#94a3b8" rx="2" />
                <g transform="translate(50, 105)">
                    <rect x="0" y="0" width="115" height="30" rx="7" fill="#0f172a" stroke="rgba(255, 255, 255, 0.25)" stroke-width="1.5"/>
                    <text x="12" y="20" fill="#f8fafc" font-size="13" font-weight="800">✂️ 狹縫 (0.1mm)</text>
                </g>

                <!-- 4. 狹縫至光柵光束 -->
                <line x1="${slitX + 6}" y1="${cy}" x2="${cx}" y2="${cy}" stroke="#ffffff" stroke-width="4.5" class="animated-beam-fast" opacity="1.0" filter="url(#glow)" />

                <!-- 5. 標註 L1 (線段分兩段，中空處放置文字，絕不被線條穿過！) -->
                <line x1="${slitX}" y1="95" x2="${slitX}" y2="65" stroke="#64748b" stroke-width="1.2" stroke-dasharray="3,3" />
                <line x1="${cx}" y1="95" x2="${cx}" y2="65" stroke="#64748b" stroke-width="1.2" stroke-dasharray="3,3" />
                <line x1="${slitX}" y1="75" x2="190" y2="75" stroke="#94a3b8" stroke-width="1.8" stroke-dasharray="4" marker-start="url(#arrow)" />
                <g transform="translate(195, 58)">
                    <rect x="0" y="0" width="150" height="34" rx="8" fill="#0f172a" stroke="#94a3b8" stroke-width="1.5"/>
                    <text x="75" y="22" text-anchor="middle" fill="#f1f5f9" font-size="14" font-weight="800">準直距 L₁: ${l1Text}</text>
                </g>
                <line x1="350" y1="75" x2="${cx}" y2="75" stroke="#94a3b8" stroke-width="1.8" stroke-dasharray="4" marker-end="url(#arrow)" />

                <!-- 6. 第一級彩虹色散光束 -->
                ${rainbowLines}

                <!-- 7. 穿透光柵本體 (垂直於繞射中軸) -->
                <g transform="translate(${cx}, ${cy}) rotate(${tiltAngle})">
                    <line x1="0" y1="-56" x2="0" y2="56" stroke="#60a5fa" stroke-width="8" stroke-linecap="round" filter="url(#glow)"/>
                </g>
                <g transform="translate(290, 130)">
                    <rect x="0" y="0" width="155" height="34" rx="8" fill="#0f172a" stroke="#60a5fa" stroke-width="1.8"/>
                    <text x="12" y="23" fill="#93c5fd" font-size="14" font-weight="800">🔮 ${gratingLabel}</text>
                </g>

                <!-- 8. 偏折夾角弧線與文字標籤 (文字置於 y=130 空白安全區，以指引線連接弧線，絕對不壓在彩虹光束上！) -->
                <path d="M ${cx + 60} ${cy} A 60 60 0 0 1 ${cx + 60 * Math.cos(greenRad)} ${cy + 60 * Math.sin(greenRad)}" fill="none" stroke="#f472b6" stroke-width="3" />
                <path d="M ${arcMidX} ${arcMidY} L ${arcMidX + 18} 146 L 475 146" fill="none" stroke="#f472b6" stroke-width="1.5" stroke-dasharray="3,2" />
                <g transform="translate(475, 130)">
                    <rect x="0" y="0" width="145" height="32" rx="7" fill="#0f172a" stroke="#f472b6" stroke-width="1.8"/>
                    <text x="72" y="21" text-anchor="middle" fill="#f472b6" font-size="14" font-weight="900">偏折夾角: ${tiltAngle}°</text>
                </g>

                <!-- 9. 手機相機 (隨傾斜角旋轉安裝) -->
                <g transform="translate(${px}, ${py}) rotate(${tiltAngle})">
                    <rect x="0" y="-38" width="44" height="76" rx="10" fill="#1e293b" stroke="#94a3b8" stroke-width="2.5"/>
                    <circle cx="0" cy="0" r="11" fill="#0f172a" stroke="#38bdf8" stroke-width="3.5"/>
                </g>
                <!-- 相機標籤獨立置於手機後方，完全不壓彩虹 -->
                <g transform="translate(${camLblX - 20}, ${camLblY - 15})">
                    <rect x="0" y="0" width="130" height="30" rx="7" fill="#0f172a" stroke="#38bdf8" stroke-width="1.6"/>
                    <text x="12" y="20" fill="#f8fafc" font-size="13" font-weight="800">📱 手機鏡頭</text>
                </g>

                <!-- 10. 標註 L2 (與光路平行的尺寸線，中空處放置文字，線條完全不穿透文字，且距彩虹有80px以上充裕淨空！) -->
                <!-- 延伸引導輔助虛線 -->
                <line x1="${cx}" y1="${cy}" x2="${d1x}" y2="${d1y}" stroke="#64748b" stroke-width="1.2" stroke-dasharray="3,3" />
                <line x1="${px}" y1="${py}" x2="${d2x}" y2="${d2y}" stroke="#64748b" stroke-width="1.2" stroke-dasharray="3,3" />
                <!-- 第一段箭頭線 -->
                <line x1="${d1x}" y1="${d1y}" x2="${s1EndX}" y2="${s1EndY}" stroke="#38bdf8" stroke-width="2" stroke-dasharray="4" marker-start="url(#arrow-blue)" />
                <!-- L2 文字框 (中空處) -->
                <g transform="translate(${midX - 75}, ${midY - 17})">
                    <rect x="0" y="0" width="150" height="34" rx="8" fill="#0f172a" stroke="#38bdf8" stroke-width="1.8"/>
                    <text x="75" y="23" text-anchor="middle" fill="#38bdf8" font-size="14" font-weight="800">鏡頭距 L₂: ${l2Text}</text>
                </g>
                <!-- 第二段箭頭線 -->
                <line x1="${s2StartX}" y1="${s2StartY}" x2="${d2x}" y2="${d2y}" stroke="#38bdf8" stroke-width="2" stroke-dasharray="4" marker-end="url(#arrow-blue)" />
            </svg>
        `;
        el.innerHTML = svg;
    }

    // 繪製六大光柵全螢幕大分頁的 SVG 光路圖
    drawLargeReflectionSVG('large-svg-ref-dvd', 14.5, '14.5°', '75.5°', '15~20 cm', '3~5 cm', 'DVD 反射光柵');
    drawLargeReflectionSVG('large-svg-ref-1000', 22.1, '22°', '68°', '15~18 cm', '4~6 cm', '1000 柵 光柵片');
    drawLargeReflectionSVG('large-svg-ref-cd', 31.0, '31°', '59°', '12~15 cm', '5~7 cm', 'CD 反射光柵');

    drawLargeTransmissionSVG('large-svg-trans-dvd', 48.0, '15~20 cm', '2~4 cm', 'DVD 穿透光柵');
    drawLargeTransmissionSVG('large-svg-trans-1000', 33.4, '15~18 cm', '3~5 cm', '1000 柵 穿透片');
    drawLargeTransmissionSVG('large-svg-trans-cd', 20.1, '12~15 cm', '4~6 cm', 'CD 穿透光柵');

    // 繪製各分頁 CMOS 感光視野
    renderCmosCanvases();
}

// 增強 startApp
const originalStartApp = window.startApp;
function enhancedStartApp() {
    startApp();
    initTabNavigation();
    initSubpageSvgs();
}

// 保證 DOM 載入立即啟動
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', enhancedStartApp);
} else {
    enhancedStartApp();
}
