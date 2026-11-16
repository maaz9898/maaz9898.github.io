// Theme switch, remembered per browser.
(function () {
  var btn = document.getElementById('theme');
  if (!btn) return;
  btn.addEventListener('click', function () {
    var next = document.documentElement.dataset.theme === 'light' ? 'dark' : 'light';
    document.documentElement.dataset.theme = next;
    try { localStorage.setItem('theme', next); } catch (e) {}
  });
})();

var STILL = matchMedia('(prefers-reduced-motion: reduce)').matches;

// Clips marked data-auto play only while on screen. With reduced motion they get controls instead.
(function () {
  var vids = [].slice.call(document.querySelectorAll('video[data-auto]'));
  if (STILL || !('IntersectionObserver' in window)) { vids.forEach(function (v) { v.controls = true; }); return; }
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) e.target.play().catch(function () {}); else e.target.pause(); });
  }, { threshold: 0.35 });
  vids.forEach(function (v) { io.observe(v); });
})();

// Tabbed visuals: click a pill, or let them cycle while on screen until you do.
(function () {
  document.querySelectorAll('[data-tabs]').forEach(function (root) {
    var items = [].slice.call(root.querySelectorAll('.stage > img, .stage > video'));
    var btns = root.querySelectorAll('.pills button');
    var cur = 0, timer = null, auto = true;
    function show(n) {
      cur = n;
      items.forEach(function (el, i) {
        el.classList.toggle('show', i === n);
        if (el.tagName === 'VIDEO') { if (i === n) { el.currentTime = 0; el.play().catch(function () {}); } else el.pause(); }
      });
      btns.forEach(function (b, i) { b.setAttribute('aria-pressed', i === n ? 'true' : 'false'); });
    }
    function next() {
      clearTimeout(timer);
      if (!auto) return;
      timer = setTimeout(function () { show((cur + 1) % items.length); next(); }, items[cur].tagName === 'VIDEO' ? 5200 : 2400);
    }
    btns.forEach(function (b, i) { b.addEventListener('click', function () { auto = false; clearTimeout(timer); show(i); }); });
    if (!STILL && 'IntersectionObserver' in window) {
      new IntersectionObserver(function (es) { clearTimeout(timer); if (es[0].isIntersecting) next(); }, { threshold: 0.5 }).observe(root);
    }
  });
})();
