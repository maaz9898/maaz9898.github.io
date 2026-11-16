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

// Clips run like GIFs on repeat, but only while they are on screen.
(function () {
  var IO = 'IntersectionObserver' in window;
  function watch(el, on, off, t) {
    new IntersectionObserver(function (es) { if (es[0].isIntersecting) on(); else off(); }, { threshold: t }).observe(el);
  }

  // Plain looping clips on project pages.
  [].slice.call(document.querySelectorAll('video[data-auto]')).forEach(function (v) {
    if (STILL || !IO) { v.controls = true; return; }
    watch(v, function () { v.play().catch(function () {}); }, function () { v.pause(); }, 0.35);
  });

  // Card clips: play, hold the analysed frame for a moment, play again.
  document.querySelectorAll('[data-gif]').forEach(function (root) {
    var v = root.querySelector('video'), hold = root.querySelector('.end') ? 1900 : 600, timer = null, live = false;
    function rest() { root.classList.remove('playing'); }
    function play() {
      clearTimeout(timer);
      if (!live) return;
      root.classList.add('playing');
      try { v.currentTime = 0; } catch (e) {}
      var p = v.play();
      if (p && p.catch) p.catch(rest);           // autoplay refused (for example low power mode): stay on the still
    }
    v.addEventListener('ended', function () { rest(); timer = setTimeout(play, hold); });
    v.addEventListener('error', rest);
    root.addEventListener('click', function () { live = true; play(); });   // a tap starts it where autoplay is blocked
    if (STILL || !IO) return;                     // reduced motion: the still stays
    watch(root, function () { if (!live) { live = true; play(); } }, function () { live = false; clearTimeout(timer); v.pause(); rest(); }, 0.4);
  });

  // Two-frame reveals animate in CSS; they only run while visible.
  document.querySelectorAll('[data-reveal]').forEach(function (root) {
    if (STILL || !IO) return;
    watch(root, function () { root.classList.add('on'); }, function () { root.classList.remove('on'); }, 0.4);
  });
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

// Before/after sliders. They glide once when first seen so people notice they move.
(function () {
  document.querySelectorAll('[data-cmp]').forEach(function (root) {
    var input = root.querySelector('input');
    function set(v) { root.style.setProperty('--pos', v + '%'); }
    input.addEventListener('input', function () { root.classList.remove('glide'); set(input.value); });
    set(input.value);
    if (STILL || !('IntersectionObserver' in window)) return;
    var io = new IntersectionObserver(function (es) {
      if (!es[0].isIntersecting) return;
      io.disconnect(); root.classList.add('glide'); set(22);
      setTimeout(function () { set(55); input.value = 55; }, 950);
    }, { threshold: 0.6 });
    io.observe(root);
  });
})();

// FitX demo: a stick figure squats, the knee angle is measured from its joints, and a rep
// counts only if the angle passes the depth threshold and returns to standing.
(function () {
  document.querySelectorAll('[data-fitx]').forEach(function (root) {
    var cv = root.querySelector('canvas'), ctx = cv.getContext('2d');
    var repsEl = root.querySelector('[data-reps]'), angEl = root.querySelector('[data-angle]'), msgEl = root.querySelector('[data-msg]');
    var btns = root.querySelectorAll('[data-mode]'), mode = 'good', reps = 0, deep = false, t0 = null, raf = null;
    var DEPTH = 100, STAND = 165, D2R = Math.PI / 180;
    function pose(d) {                     // d: 0 standing, 1 deep squat (side view, facing right)
      var ankle = [150, 430], shin = 105, thigh = 105, torso = 120, arm = 95;
      var a = 28 * d * D2R, b = 92 * d * D2R, g = 38 * d * D2R;
      var knee = [ankle[0] + shin * Math.sin(a), ankle[1] - shin * Math.cos(a)];
      var hip = [knee[0] - thigh * Math.sin(b), knee[1] - thigh * Math.cos(b)];
      var sh = [hip[0] + torso * Math.sin(g), hip[1] - torso * Math.cos(g)];
      var hand = [sh[0] + arm * Math.cos((1 - d) * 80 * D2R) , sh[1] + arm * Math.sin((1 - d) * 80 * D2R)];
      var head = [sh[0] + 6, sh[1] - 34];
      return { ankle: ankle, knee: knee, hip: hip, sh: sh, hand: hand, head: head, toe: [ankle[0] + 38, ankle[1] + 4] };
    }
    function angle(p, q, r) {
      var v1 = [p[0] - q[0], p[1] - q[1]], v2 = [r[0] - q[0], r[1] - q[1]];
      var c = (v1[0] * v2[0] + v1[1] * v2[1]) / (Math.hypot(v1[0], v1[1]) * Math.hypot(v2[0], v2[1]));
      return Math.acos(Math.max(-1, Math.min(1, c))) / D2R;
    }
    function draw(d) {
      var P = pose(d), ang = angle(P.hip, P.knee, P.ankle), ok = ang <= DEPTH;
      ctx.clearRect(0, 0, 300, 520);
      ctx.strokeStyle = '#243049'; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(30, 436); ctx.lineTo(270, 436); ctx.stroke();
      ctx.lineCap = 'round'; ctx.lineJoin = 'round'; ctx.strokeStyle = '#F1F4FA'; ctx.lineWidth = 7;
      ctx.beginPath(); ctx.moveTo(P.toe[0], P.toe[1]); ctx.lineTo(P.ankle[0], P.ankle[1]); ctx.lineTo(P.knee[0], P.knee[1]); ctx.lineTo(P.hip[0], P.hip[1]); ctx.lineTo(P.sh[0], P.sh[1]); ctx.lineTo(P.hand[0], P.hand[1]); ctx.stroke();
      ctx.beginPath(); ctx.arc(P.head[0], P.head[1], 20, 0, 7); ctx.stroke();
      var col = ok ? '#2FD08F' : (d > 0.25 ? '#F0AA50' : '#6EA8FF');
      ctx.strokeStyle = col; ctx.lineWidth = 4; ctx.beginPath();
      var a1 = Math.atan2(P.hip[1] - P.knee[1], P.hip[0] - P.knee[0]), a2 = Math.atan2(P.ankle[1] - P.knee[1], P.ankle[0] - P.knee[0]);
      ctx.arc(P.knee[0], P.knee[1], 26, a1, a2, false); ctx.stroke();
      ctx.fillStyle = '#6EA8FF'; [P.ankle, P.knee, P.hip, P.sh, P.hand].forEach(function (q) { ctx.beginPath(); ctx.arc(q[0], q[1], 7, 0, 7); ctx.fill(); });
      ctx.fillStyle = col; ctx.beginPath(); ctx.arc(P.knee[0], P.knee[1], 7, 0, 7); ctx.fill();
      ctx.fillStyle = '#F1F4FA'; ctx.font = '700 44px "IBM Plex Sans", system-ui, sans-serif'; ctx.fillText(String(reps), 24, 62);
      ctx.fillStyle = '#8492AB'; ctx.font = '500 14px "IBM Plex Sans", system-ui, sans-serif'; ctx.fillText('REPS', 24, 84);
      ctx.fillStyle = col; ctx.font = '700 22px "IBM Plex Sans", system-ui, sans-serif'; ctx.fillText(Math.round(ang) + '°', P.knee[0] + 34, P.knee[1] + 6);
      var msg = ok ? 'Good depth' : (mode === 'shallow' && d > 0.25 ? 'Go lower' : (d < 0.08 ? 'Ready' : 'Lowering'));
      ctx.fillStyle = col; var w = ctx.measureText(msg).width + 28; ctx.beginPath(); ctx.roundRect(300 - w - 18, 34, w, 36, 18); ctx.fill();
      ctx.fillStyle = '#0D131F'; ctx.font = '600 15px "IBM Plex Sans", system-ui, sans-serif'; ctx.fillText(msg, 300 - w - 4, 57);
      if (ang <= DEPTH) deep = true;
      if (ang >= STAND && deep) { deep = false; reps += 1; }
      repsEl.textContent = reps; angEl.textContent = Math.round(ang); msgEl.textContent = msg;
    }
    function frame(ts) {
      if (t0 === null) t0 = ts;
      var phase = ((ts - t0) % 3200) / 3200, d = (1 - Math.cos(phase * 2 * Math.PI)) / 2;
      draw(d * (mode === 'good' ? 1 : 0.6));
      raf = requestAnimationFrame(frame);
    }
    btns.forEach(function (b) {
      b.addEventListener('click', function () {
        mode = b.dataset.mode; reps = 0; deep = false; t0 = null;
        btns.forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
        if (STILL) draw(mode === 'good' ? 1 : 0.6);
      });
    });
    if (STILL || !('IntersectionObserver' in window)) { draw(1); return; }
    new IntersectionObserver(function (es) { cancelAnimationFrame(raf); if (es[0].isIntersecting) raf = requestAnimationFrame(frame); }, { threshold: 0.2 }).observe(root);
  });
})();
