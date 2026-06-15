
(function () {
    let starting = false;
    function startTeaching(ev) {
        if (ev) { ev.preventDefault(); ev.stopPropagation(); }
        if (starting) return;
        starting = true;
        document.getElementById('start-overlay').style.display = 'none';
        document.getElementById('app').classList.add('started');
        const el = document.documentElement;
        try { const p = el.requestFullscreen && el.requestFullscreen(); if (p && p.catch) p.catch(function () {}); } catch (e) {}
        try { if (el.webkitRequestFullscreen) el.webkitRequestFullscreen(); } catch (e) {}
        requestAnimationFrame(function () {
            requestAnimationFrame(function () {
                if (typeof window.updateSlides === 'function') window.updateSlides();
                if (typeof window.updateAllMB === 'function') window.updateAllMB();
            });
        });
    }
    const btn = document.getElementById('btn-start');
    if (btn) { btn.addEventListener('click', startTeaching); btn.addEventListener('touchend', startTeaching, { passive: false }); }
})();
