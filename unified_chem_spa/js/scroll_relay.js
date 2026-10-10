/**
 * scroll_relay.js - 捲動位置中繼器 v2
 *
 * 此腳本嵌入於各章節 iframe 頁面內，負責監聽頁面捲動並透過 postMessage
 * 將捲動座標即時回報給父視窗（portal.js）。
 *
 * 這是唯一能繞過 Chrome file:// 跨目錄安全限制的可靠方案——
 * 父視窗無法直接讀取 iframe.contentWindow.scrollY，
 * 但 iframe 自身可讀取後透過 postMessage 回傳。
 *
 * v2 改進：
 * - 增加 wheel / touchmove / keydown 事件的 RAF + timeout 雙重延遲報告
 * - 加入自訂 scroller 元素的 scroll 監聽（如 #main-scroller）
 * - 針對 __chem_get_scroll 請求立即回報
 * - 針對 __chem_scroll_by 指令執行捲動並立即回報
 */
(function () {
  // 避免重複安裝
  if (window.__chemScrollRelayInstalled) return;
  window.__chemScrollRelayInstalled = true;

  // 若不在 iframe 中（直接開啟頁面）則無需運作
  if (!window.parent || window.parent === window) return;

  function getScrollPos() {
    var sy = window.scrollY || window.pageYOffset ||
      (document.documentElement && document.documentElement.scrollTop) ||
      (document.body && document.body.scrollTop) || 0;
    var sx = window.scrollX || window.pageXOffset ||
      (document.documentElement && document.documentElement.scrollLeft) || 0;

    // 也嘗試從常見的自訂 scroller 讀取
    var scroller = document.getElementById('slides-container') ||
                   document.getElementById('main-scroller') ||
                   document.getElementById('slide-scroller') ||
                   document.querySelector('[data-scroller]');
    if (scroller && scroller.scrollTop > sy) {
      sy = scroller.scrollTop;
      sx = scroller.scrollLeft || 0;
    }
    return { sy: sy, sx: sx };
  }

  function reportScroll() {
    try {
      var pos = getScrollPos();
      window.parent.postMessage({ type: '__chem_scroll', sy: pos.sy, sx: pos.sx }, '*');
    } catch (e) {}
  }

  // 節流版 reportScroll（RAF 確保每幀只報一次）
  var rafPending = false;
  function scheduleReport() {
    if (!rafPending) {
      rafPending = true;
      requestAnimationFrame(function () {
        rafPending = false;
        reportScroll();
      });
    }
  }

  // 監聽所有可能觸發捲動的目標
  window.addEventListener('scroll', scheduleReport, { capture: true, passive: true });
  document.addEventListener('scroll', scheduleReport, { capture: true, passive: true });

  // wheel 後 RAF + 延遲雙重確認（因為 scroll event 可能在 wheel 之後才觸發）
  window.addEventListener('wheel', function () {
    scheduleReport();
    setTimeout(reportScroll, 50);
    setTimeout(reportScroll, 150);
  }, { capture: true, passive: true });

  // 觸控
  window.addEventListener('touchmove', function () {
    scheduleReport();
    setTimeout(reportScroll, 80);
  }, { capture: true, passive: true });

  // 鍵盤捲動（方向鍵、PageUp/Down）
  window.addEventListener('keydown', function (e) {
    if (['ArrowUp', 'ArrowDown', 'PageUp', 'PageDown', 'Space', 'Home', 'End'].indexOf(e.code) !== -1) {
      scheduleReport();
      setTimeout(reportScroll, 60);
      setTimeout(reportScroll, 200);
    }
  }, { passive: true });

  // 也監聽 #main-scroller / #slides-container
  function attachScrollerListener() {
    var scroller = document.getElementById('slides-container') ||
                   document.getElementById('main-scroller') ||
                   document.getElementById('slide-scroller');
    if (scroller && !scroller.__chemScrollListened) {
      scroller.__chemScrollListened = true;
      scroller.addEventListener('scroll', scheduleReport, { passive: true });
    }
  }
  // DOMContentLoaded 後嘗試掛載
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () {
      attachScrollerListener();
      reportScroll();
    });
  } else {
    attachScrollerListener();
  }

  // 父視窗請求操作處理
  window.addEventListener('message', function (e) {
    if (!e.data) return;
    // 父視窗要求立即回報捲動位置
    if (e.data.type === '__chem_get_scroll') {
      reportScroll();
    }
    // 父視窗要求執行捲動（由 portal canvas wheel 轉發）
    if (e.data.type === '__chem_scroll_by') {
      var dy = e.data.deltaY || 0;
      var dx = e.data.deltaX || 0;
      // 優先捲動 body/document
      window.scrollBy({ top: dy, left: dx, behavior: 'instant' });
      // 也嘗試直接操作常見元素（避免瀏覽器相容問題）
      if (document.documentElement) document.documentElement.scrollTop += dy;
      if (document.body) document.body.scrollTop += dy;
      var scroller = document.getElementById('slides-container') ||
                     document.getElementById('main-scroller');
      if (scroller) scroller.scrollTop += dy;
      // 立即回報新的位置
      scheduleReport();
      setTimeout(reportScroll, 50);
    }
  });

  // 頁面載入完成後立即回報初始位置
  window.addEventListener('load', reportScroll);
  reportScroll();
})();
