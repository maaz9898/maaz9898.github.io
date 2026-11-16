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

// Annotated stepper: each pill adds a layer of drawing over the same picture; the last one plays a clip.
(function () {
  document.querySelectorAll('[data-annot]').forEach(function (root) {
    var btns = root.querySelectorAll('.pills button'), v = root.querySelector('video'), cur = 0, timer = null, auto = true, last = btns.length - 1;
    function show(n) {
      cur = n; root.dataset.step = String(n);
      btns.forEach(function (b, i) { b.setAttribute('aria-pressed', i === n ? 'true' : 'false'); });
      if (v) { if (n === last) { v.currentTime = 0; v.play().catch(function () {}); } else v.pause(); }
    }
    function next() { clearTimeout(timer); if (!auto) return; timer = setTimeout(function () { show((cur + 1) % btns.length); next(); }, cur === last ? 5200 : 2800); }
    btns.forEach(function (b, i) { b.addEventListener('click', function () { auto = false; clearTimeout(timer); show(i); }); });
    if (!STILL && 'IntersectionObserver' in window) new IntersectionObserver(function (es) { clearTimeout(timer); if (es[0].isIntersecting) next(); }, { threshold: 0.5 }).observe(root);
  });
})();

// Dashboard mock-up: the alert feed rotates and the counters tick while it is on screen.
(function () {
  document.querySelectorAll('[data-dash]').forEach(function (root) {
    if (STILL || !('IntersectionObserver' in window)) return;
    var list = root.querySelector('[data-alerts]'), counts = root.querySelectorAll('[data-count]'), timer = null;
    function tick() {
      var last = list.lastElementChild;
      last.classList.remove('new'); list.insertBefore(last, list.firstElementChild); void last.offsetWidth; last.classList.add('new');
      counts.forEach(function (c) { c.textContent = String(+c.textContent + Math.ceil(Math.random() * 3)); });
    }
    new IntersectionObserver(function (es) { clearInterval(timer); if (es[0].isIntersecting) timer = setInterval(tick, 2600); }, { threshold: 0.4 }).observe(root);
  });
})();
