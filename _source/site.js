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

  /* золотая монетка: катится по буквам заголовка, потом падает на буквы следующего блока.
     Положение целиком зависит от прокрутки, поэтому при прокрутке вверх она едет обратно */
  if (!reduce) (function () {
    var coin = D.createElement('div'); coin.className = 'coin'; coin.setAttribute('aria-hidden', 'true'); coin.innerHTML = '<i></i><b></b>';
    D.body.appendChild(coin);
    var A = [], r = 13, raf = 0, landed = false, landT = 0;
    function clamp(v, a, b) { return Math.max(a, Math.min(b, v)); }
    function measure() {
      var sy = W.scrollY || H.scrollTop, vh = W.innerHeight, list = [];
      r = (coin.offsetWidth || 26) / 2;
      var heads = [D.querySelector('.cover .mast')].concat($$('.sec .hd'));
      heads.forEach(function (h) {
        if (!h) return;
        var ln = h.querySelector('.ln'); if (!ln) return;
        var lr = ln.getBoundingClientRect(), it = ln.firstElementChild || ln;
        var rg = D.createRange(); rg.selectNodeContents(it);
        var rr = rg.getBoundingClientRect(); if (!rr.width) return;
        var fs = parseFloat(W.getComputedStyle(h).fontSize) || 100;
        var isMast = h.classList.contains('mast');
        /* слово на обложке сдвинуто параллаксом на 0.3 от прокрутки: вычитаем сдвиг, чтобы якорь монетки не уезжал */
        var po = isMast ? (parseFloat(h.closest('.cover').style.getPropertyValue('--p')) || 0) * .3 : 0;
        list.push({ y: sy + lr.top - po + fs * (isMast ? .22 : .255), x0: rr.left, x1: rr.right });
      });
      list.forEach(function (a, idx) {
        /* на обложке монетка ждёт на первой букве и падает, как только начнут листать; в остальных блоках катится по заголовку,
           пока он в кадре (длина пути не больше, чем заголовок успевает проехать по экрану) */
        a.ws = idx ? a.y - vh * .18 : vh * .55;
        var w = idx ? clamp((a.x1 - a.x0) * .5, 180, vh * .73 - 80) : 0;
        a.we = a.ws + w;
        a.xe = w ? a.x1 - r : a.x0 + r;
      });
      /* сейф в последнем блоке: монетка падает в прорезь на его крышке (прорезь на 10% высоты рисунка сверху, по центру корпуса) */
      var sf = D.querySelector('.safe');
      if (sf) {
        var sr = sf.getBoundingClientRect();
        if (sr.width) {
          var sx0 = sr.left + sr.width * (60 / 170), sy0 = sy + sr.top + sr.height * (15.5 / 132);
          var maxS = Math.max(0, H.scrollHeight - vh) + vh * .55;
          var sa = { safe: true, y: sy0, x0: sx0 - r, x1: sx0 + r, xe: sx0, we: 0 };
          sa.ws = Math.min(sy0 - vh * .18, maxS - 30);
          sa.we = sa.ws;
          list.push(sa);
        }
      }
      /* проверяем порядок: каждому заголовку остаётся своя дорожка до следующей точки */
      for (var i = list.length - 2; i >= 0; i--) {
        var nx = list[i + 1];
        list[i].ws = Math.min(list[i].ws, nx.ws - 120);
        list[i].we = Math.max(list[i].ws, Math.min(list[i].we, nx.ws - 90));
        if (list[i].we === list[i].ws) list[i].xe = list[i].x0 + r;
      }
      A = list; update();
    }
    function update() {
      raf = 0;
      var n = A.length; if (!n) return;
      var sy = W.scrollY || H.scrollTop, s = sy + W.innerHeight * .55;
      var i = 0; while (i < n - 1 && s >= A[i + 1].ws) i++;
      var gl = 0, g = 0, sp = 0;   /* блик: положение, сила и искорка */
      var a = A[i], x, yv, deg = 0, sx = 1, roll = (a.xe - (a.x0 + r)) / r * 57.2958;
      if (s <= a.ws) { x = a.x0 + r; yv = a.y - sy; }
      else if (s <= a.we) {
        var t = (s - a.ws) / (a.we - a.ws);
        x = a.x0 + r + (a.xe - a.x0 - r) * t; yv = a.y - sy;
        deg = (x - (a.x0 + r)) / r * 57.2958;
        gl = .3 * (.5 + .5 * Math.sin(t * Math.PI * 4)); g = (t * 2.2) % 1;
        var k = (s - a.ws) / 170;
        if (i > 0 && k < 1) yv -= Math.abs(Math.sin(k * Math.PI * 2.5)) * (1 - k) * 20;
      } else if (i < n - 1) {
        /* падение считается в координатах экрана: монетка всегда в кадре и ускоряется вниз, а страница уезжает вверх */
        var b = A[i + 1], u = clamp((s - a.we) / (b.ws - a.we), 0, 1), vh = W.innerHeight;
        var yl = a.y - (a.we - vh * .55), yd = b.y - (b.ws - vh * .55);
        var xs = b.x0 + r, e = u * u * (3 - 2 * u);
        x = a.xe + (xs - a.xe) * e; yv = yl + (yd - yl) * u * u;
        var degEnd = Math.round((roll + 540) / 360) * 360;
        deg = roll + (degEnd - roll) * u; sx = Math.cos(u * Math.PI * 4);
        /* в полёте монетка слегка блестит: по грани скользит блик, а на гребне полёта вспыхивает искорка */
        gl = .85 * Math.sin(u * Math.PI); g = (u * 2.4) % 1; sp = Math.max(0, Math.sin(u * Math.PI * 6)) * Math.sin(u * Math.PI);
        if (Math.abs(sx) < .12) sx = sx < 0 ? -.12 : .12;
      } else { x = a.xe; yv = a.y - sy; deg = a.safe ? 0 : roll; }
      /* прыжок в сейф: после приземления на крышку монетка по времени уходит в прорезь и пропадает, сейф вздрагивает */
      var sfe = a.safe ? D.querySelector('.safe') : null;
      if (a.safe && s > a.ws) {
        if (!landed) { landed = true; landT = performance.now(); }
        var dp = clamp((performance.now() - landT) / 560, 0, 1), de = dp * dp * (3 - 2 * dp);
        var drop = de * (2 * r + 8);
        yv += drop; deg = 0; sx = 1; x = a.xe;
        coin.style.clipPath = 'inset(-90px -90px ' + clamp(drop - 1, 0, 2 * r).toFixed(1) + 'px -90px)';
        if (dp < 1) raf = requestAnimationFrame(update);
        else {
          coin.style.opacity = '0';
          if (sfe) sfe.classList.add('got');
        }
      } else if (landed) {
        landed = false; coin.style.opacity = ''; coin.style.clipPath = '';
        var so = D.querySelector('.safe'); if (so) so.classList.remove('got');
      }
      coin.style.setProperty('--g', g.toFixed(3)); coin.style.setProperty('--gl', gl.toFixed(3)); coin.style.setProperty('--sp', sp.toFixed(3));
      coin.style.transform = 'translate3d(' + (x - r).toFixed(1) + 'px,' + (yv - 2 * r - 1).toFixed(1) + 'px,0) rotate(' + deg.toFixed(1) + 'deg) scaleX(' + sx.toFixed(3) + ')';
    }
    function req() { if (!raf) raf = requestAnimationFrame(update); }
    W.addEventListener('scroll', req, { passive: true });
    W.addEventListener('resize', measure);
    W.addEventListener('load', measure);
    [300, 900, 2200, 5000].forEach(function (ms) { setTimeout(measure, ms); });
    if (D.fonts && D.fonts.ready) D.fonts.ready.then(measure);
    if ('ResizeObserver' in W) new ResizeObserver(function () { clearTimeout(measure.t); measure.t = setTimeout(measure, 120); }).observe(D.body);
    measure();
  })();

  var stick = D.querySelector('.stick'), cover = D.querySelector('.cover'), fin = D.getElementById('contact');
  var bigs = $$('.bignum'), ticking = false;
  function onScroll() {
    ticking = false;
    var y = W.scrollY || H.scrollTop, vh = W.innerHeight;
    var max = Math.max(1, H.scrollHeight - vh);
    bar.style.transform = 'scaleX(' + Math.min(1, y / max) + ')';
    /* параллакс обложки: слово, фото и колонки смещаются с разной скоростью (CSS читает --p) */
    if (!reduce && y < cover.offsetHeight + 120) cover.style.setProperty('--p', Math.max(0, y).toFixed(1));
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
