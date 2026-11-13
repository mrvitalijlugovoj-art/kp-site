(function () {
  var D = document, W = window, H = D.documentElement;
  var reduce = W.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var $$ = function (s, r) { return [].slice.call((r || D).querySelectorAll(s)); };
  var hasIO = 'IntersectionObserver' in W;

  /* обложка всегда над сгибом: проявляем её сразу, не дожидаясь IntersectionObserver */
  setTimeout(function () { $$('.cover [data-a]').forEach(function (e) { e.classList.add('in'); setTimeout(function () { e.classList.add('done'); }, 2600); }); }, 80);

  /* показать всё сразу, если анимации недоступны */
  if (!hasIO || reduce) {
    $$('[data-a],.hd,.folio,.stp,.path').forEach(function (e) { e.classList.add('in', 'line-in'); });
    $$('.cnt').forEach(function (e) { e.textContent = (e.getAttribute('data-pre') || '') + fmt(+e.getAttribute('data-to')) + (e.getAttribute('data-suf') || ''); });
  }
  function fmt(n) { return String(Math.round(n)).replace(/\B(?=(\d{3})+(?!\d))/g, ' '); }

  /* появление по входу в экран */
  if (hasIO && !reduce) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        var t = e.target; io.unobserve(t);
        t.classList.add('in');
        if (t.classList.contains('path')) t.classList.add('line-in');
        if (t.hasAttribute('data-a')) {
          var d = parseFloat((t.style.getPropertyValue('--d') || '0')) || 0;
          setTimeout(function () { t.classList.add('done'); }, d * 1000 + 1300);
        }
      });
    }, { threshold: .12, rootMargin: '0px 0px -6% 0px' });
    $$('[data-a],.hd,.folio,.stp,.path').forEach(function (e) { io.observe(e); });
  }

  /* счётчики */
  function countUp(el) {
    var to = +el.getAttribute('data-to'), pre = el.getAttribute('data-pre') || '', suf = el.getAttribute('data-suf') || '';
    var t0 = null, dur = 1800;
    el.textContent = pre + '0' + suf;
    function step(t) {
      if (t0 === null) t0 = t;
      var p = Math.min(1, (t - t0) / dur), e = p === 1 ? 1 : 1 - Math.pow(2, -10 * p);
      el.textContent = pre + fmt(to * e) + suf;
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }
  if (hasIO && !reduce) {
    var cio = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { cio.unobserve(e.target); setTimeout(function () { countUp(e.target); }, 250); } });
    }, { threshold: .6 });
    $$('.cnt').forEach(function (e) { e.textContent = (e.getAttribute('data-pre') || '') + '0' + (e.getAttribute('data-suf') || ''); cio.observe(e); });
  }

  /* секция в кадре: анимации внутри играют, вне кадра стоят */
  var secs = $$('.sec,.cover');
  if (hasIO) {
    var sio = new IntersectionObserver(function (es) {
      es.forEach(function (e) { e.target.classList.toggle('inview', e.isIntersecting); });
    }, { rootMargin: '100px 0px' });
    secs.forEach(function (s) { sio.observe(s); });
  } else secs.forEach(function (s) { s.classList.add('inview'); });

  /* бегущий колонтитул: номер, название, полоса прочитанного */
  var vf = D.querySelector('.vf'), vfd = vf.querySelector('.vfd'), vft = vf.querySelector('.vft'), bar = vf.querySelector('.vfbar');
  var named = $$('[data-num]'), shown = '';
  function setPage(s) {
    var num = s.getAttribute('data-num'), name = s.getAttribute('data-title');
    if (num !== shown) {
      var down = !shown || num > shown; shown = num;
      var old = vfd.querySelector('i'), ni = D.createElement('i');
      ni.textContent = num; ni.className = 'in';
      if (!down) ni.style.transform = 'translateY(-110%)';
      vfd.appendChild(ni);
      requestAnimationFrame(function () { requestAnimationFrame(function () {
        ni.className = ''; ni.style.transform = '';
        if (old) { old.className = 'out'; if (!down) old.style.transform = 'translateY(110%)'; setTimeout(function () { old.remove(); }, 520); }
      }); });
    }
    if (vft.textContent !== name) { vft.classList.add('sw'); setTimeout(function () { vft.textContent = name; vft.classList.remove('sw'); }, 220); }
  }
  if (hasIO) {
    var nio = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) setPage(e.target); });
    }, { rootMargin: '-45% 0px -54% 0px' });
    named.forEach(function (s) { nio.observe(s); });
  }

  /* ряды карточек в кейсах: если их можно листать, они медленно плывут из стороны в сторону,
     пока человек сам не тронул ряд (тогда дрейф прекращается навсегда) */
  if (!reduce) $$('.gal').forEach(function (g) {
    var pos = 0, dir = 1, last = 0, wait = 0, active = false, stopped = false, raf = 0, SPEED = 30;
    function can() { return !stopped && g.scrollWidth - g.clientWidth > 8; }
    function tick(t) {
      raf = 0;
      if (!active || !can()) { last = 0; if (!can()) g.style.scrollSnapType = ''; return; }
      var dt = last ? Math.min(64, t - last) : 16; last = t;
      if (wait > 0) wait -= dt;
      else {
        var max = g.scrollWidth - g.clientWidth;
        pos += dir * SPEED * dt / 1000;
        if (pos >= max) { pos = max; dir = -1; wait = 1400; }
        else if (pos <= 0) { pos = 0; dir = 1; wait = 1400; }
        g.scrollLeft = pos;
      }
      raf = requestAnimationFrame(tick);
    }
    function start() { if (active || !can()) return; active = true; pos = g.scrollLeft; g.style.scrollSnapType = 'none'; last = 0; wait = 900; raf = requestAnimationFrame(tick); }
    function stop() { active = false; if (raf) { cancelAnimationFrame(raf); raf = 0; } }
    function touched() { stopped = true; stop(); g.style.scrollSnapType = ''; }
    ['pointerdown', 'touchstart', 'wheel', 'keydown'].forEach(function (e) { g.addEventListener(e, touched, { passive: true }); });
    if (hasIO) new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) start(); else stop(); }); }, { threshold: .35 }).observe(g);
    W.addEventListener('resize', function () { if (!can()) { stop(); g.style.scrollSnapType = ''; } else if (g.getBoundingClientRect().top < W.innerHeight) start(); });
  });

  var stick = D.querySelector('.stick'), cover = D.querySelector('.cover'), fin = D.getElementById('contact');
  var bigs = $$('.bignum'), ticking = false;
  function onScroll() {
    ticking = false;
    var y = W.scrollY || H.scrollTop, vh = W.innerHeight;
    var max = Math.max(1, H.scrollHeight - vh);
    bar.style.transform = 'scaleX(' + Math.min(1, y / max) + ')';
    var pastCover = y > cover.offsetHeight * .6;
    vf.classList.toggle('on', pastCover);
    var finTop = fin ? fin.getBoundingClientRect().top : 9e9;
    stick.classList.toggle('on', y > vh * .8 && finTop > vh * .3);
    if (!reduce) bigs.forEach(function (n) {
      var r = n.parentNode.getBoundingClientRect();
      if (r.bottom < -100 || r.top > vh + 100) return;
      var p = (vh - r.top) / (vh + r.height);
      n.style.transform = 'translateY(' + ((0.5 - p) * 40).toFixed(1) + '%)';
    });
  }
  W.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  W.addEventListener('resize', onScroll);
  onScroll();
})();
