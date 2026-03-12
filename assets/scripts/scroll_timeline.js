/**
 * ONANO Scroll Timeline v1.0
 *
 * Controlador maestro de scroll para la experiencia narrativa del HERO.
 * Lee el progreso de scroll sobre #scroll-hero-root y:
 *
 *  1. Pasa el progreso normalizado (0–1) a la API de partículas.
 *  2. Controla el fade-in/out de los slides de texto (.scroll-slide-N).
 *  3. Gestiona el fade del canvas al salir de la sección.
 *  4. Implementa el smooth-scroll para el CTA button.
 *
 * Sin dependencias externas. Compatible con Safari iOS.
 *
 * @version 1.0.0
 */

(function () {
  'use strict';

  /* ─────────────────────────────────────────────────────
     CONSTANTES
     ───────────────────────────────────────────────────── */
  var ROOT_ID   = 'scroll-hero-root';
  var SLIDES_ID = 'scroll-slides';
  var CTA_ID    = 'scroll-cta';

  /**
   * Ventanas de visibilidad por slide (fracción del progreso 0–1).
   * Orden: [slide-hero, slide-science-1, slide-science-2, slide-science-3]
   */
  var SLIDE_WINDOWS = [
    { fadeIn: -0.1, peak: 0.0, fadeOut: 0.08, gone: 0.20 },  // slide-0: hero
    { fadeIn: 0.12, peak: 0.22, fadeOut: 0.44, gone: 0.56 }, // slide-1: aglomerado
    { fadeIn: 0.48, peak: 0.58, fadeOut: 0.74, gone: 0.84 }, // slide-2: dispersión
    { fadeIn: 0.78, peak: 0.88, fadeOut: 1.10, gone: 1.20 }, // slide-3: encapsulación
  ];

  /**
   * SNAP_TARGETS — fracciones de progreso (0–1) donde el scroll hace "tope".
   * 📐 AJUSTE MANUAL: modifica los valores para mover el punto de cada tope.
   *    Deben coincidir con el `peak` del slide destino en SLIDE_WINDOWS.
   */
  var SNAP_TARGETS = [0.0, 0.22, 0.58, 0.88]; // peaks: hero, slide-1, slide-2, slide-3

  /**
   * Duración de la animación de snap (ms).
   * 📐 AJUSTE MANUAL: 500 = rápido  |  700 = normal  |  1000 = lento
   */
  var SNAP_DURATION_MS = 700;

  /* ─────────────────────────────────────────────────────
     UTILIDADES
     ───────────────────────────────────────────────────── */
  function lerp(a, b, t)   { return a + (b - a) * t; }
  function clamp(v, lo, hi) { return v < lo ? lo : v > hi ? hi : v; }
  function easeInOut(t)    { return t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t; }
  function easeOut(t)      { return 1 - (1 - t) * (1 - t); }

  function opacity01(p, win) {
    if (p < win.fadeIn)  return 0;
    if (p < win.peak)    return easeOut((p - win.fadeIn) / (win.peak - win.fadeIn));
    if (p <= win.fadeOut) return 1;
    if (p < win.gone)    return 1 - easeInOut((p - win.fadeOut) / (win.gone - win.fadeOut));
    return 0;
  }

  /* ─────────────────────────────────────────────────────
     ESTADO INTERNO
     ───────────────────────────────────────────────────── */
  var root, slides, canvasWrap, ctaEl;
  var rawProgress      = 0;
  var smoothProgress   = 0;
  var rafId;
  var initialized      = false;
  /* Snap */
  var snapDebounceId   = null;
  var lastScrollY      = 0;
  var scrollDirection  = 1;   // 1 = abajo, -1 = arriba
  /* Flag para evitar snap en cascada durante scroll programático */
  var isSnapping       = false;
  /* Inmunidad post-snap: evita disparo de snapToNearest por inercia/momentum */
  var snapImmunityUntil = 0;

  /* ─────────────────────────────────────────────────────
     CÁLCULO DE PROGRESO
     ───────────────────────────────────────────────────── */
  function computeRawProgress() {
    if (!root) return 0;
    var rect  = root.getBoundingClientRect();
    var total = root.offsetHeight - window.innerHeight;
    if (total <= 0) return 0;
    return clamp(-rect.top / total, 0, 1);
  }

  /* ─────────────────────────────────────────────────────
     APLICAR SLIDES
     ───────────────────────────────────────────────────── */
  function applySlides(p) {
    if (!slides) return;
    for (var i = 0; i < SLIDE_WINDOWS.length; i++) {
      var el = slides.querySelector('.scroll-slide-' + i);
      if (!el) continue;
      var op = opacity01(p, SLIDE_WINDOWS[i]);
      el.style.opacity = op;
      /* Bug-4: gestionar pointer-events en elementos interactivos dentro del slide.
         El slide wrapper tiene pointer-events:none en CSS; sus hijos con
         pointer-events:auto (botones, .cta-glow-wrap) quedan activos aunque
         el slide sea invisible. Los desactivamos cuando el slide es opaco < 5%. */
      var interactives = el.querySelectorAll('.cta-glow-wrap, .btn-nav, button');
      for (var j = 0; j < interactives.length; j++) {
        interactives[j].style.pointerEvents = (op < 0.05) ? 'none' : 'auto';
      }
      /* translateY: entra desde +40px, sale hacia -40px */
      var ty = 0;
      var w  = SLIDE_WINDOWS[i];
      if (p < w.peak && p > w.fadeIn) {
        ty = (1 - easeOut((p - w.fadeIn) / (w.peak - w.fadeIn))) * 40;
      } else if (p > w.fadeOut && p < w.gone) {
        ty = -easeInOut((p - w.fadeOut) / (w.gone - w.fadeOut)) * 40;
      }
      el.style.transform = 'translateY(' + ty + 'px)';
    }
  }

  /* ─────────────────────────────────────────────────────
     APLICAR CANVAS FADE
     Fade-out cuando el scroll root empieza a salir del viewport.
     ───────────────────────────────────────────────────── */
  function applyCanvasFade(p) {
    if (!canvasWrap) return;
    if (!root) { canvasWrap.style.opacity = 1; return; }

    /* Fade in al entrar (por si el canvas empieza oculto) */
    var rectTop = root.getBoundingClientRect().top;
    if (rectTop > window.innerHeight * 0.2) {
      canvasWrap.style.opacity = 0;
      return;
    }

    /* Fade out al salir (bottom del root pasa de la pantalla) */
    var rectBottom = root.getBoundingClientRect().bottom;
    if (rectBottom < window.innerHeight * 0.5) {
      var fade = clamp(rectBottom / (window.innerHeight * 0.5), 0, 1);
      canvasWrap.style.opacity = easeInOut(fade);
      return;
    }

    canvasWrap.style.opacity = 1;
  }

  /* ─────────────────────────────────────────────────────
     RAF LOOP
     ───────────────────────────────────────────────────── */
  function tick() {
    rafId = requestAnimationFrame(tick);

    rawProgress    = computeRawProgress();
    smoothProgress = lerp(smoothProgress, rawProgress, 0.09);

    /* Umbral mínimo para evitar micro-updates */
    var delta = Math.abs(smoothProgress - rawProgress);
    var p     = delta < 0.0004 ? rawProgress : smoothProgress;

    /* Partículas */
    if (window.__oParticleHero) {
      window.__oParticleHero.setScrollProgress(p);
    }

    /* Texto + canvas */
    applySlides(p);
    applyCanvasFade(p);
  }

  /* ─────────────────────────────────────────────────────
     SMOOTH SCROLL  (CTA "Conocer más")
     Interpolación manual con easing — no depende de CSS scroll-behavior.
     ───────────────────────────────────────────────────── */
  function smoothScrollTo(targetY, durationMs) {
    var startY = window.scrollY;
    var delta  = targetY - startY;
    /* Si el destino ya está cerca, no hacer nada */
    if (Math.abs(delta) < 4) { isSnapping = false; return; }

    /* Bloquea onPageScroll durante la animación para evitar snap en cascada */
    isSnapping = true;
    clearTimeout(snapDebounceId);

    var startTime = null;
    function step(time) {
      if (!startTime) startTime = time;
      var elapsed = time - startTime;
      var t    = clamp(elapsed / durationMs, 0, 1);
      var ease = t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t; // easeInOut cubic
      window.scrollTo(0, startY + delta * ease);
      if (t < 1) {
        requestAnimationFrame(step);
      } else {
        /* Animación terminada — liberar el bloqueo y establecer inmunidad breve
           para absorber el momentum residual del trackpad/touch. */
        isSnapping = false;
        snapImmunityUntil = Date.now() + 600;
      }
    }
    requestAnimationFrame(step);
  }

  /* ─────────────────────────────────────────────────────
     SCROLL SNAP
     — Detecta fin de scroll y anima al peak del slide más cercano
       según la dirección del movimiento.
     ───────────────────────────────────────────────────── */
  function snapToNearest() {
    if (!root) return;
    var p          = computeRawProgress();
    var scrollable = root.offsetHeight - window.innerHeight;
    var target     = null;

    if (scrollDirection >= 0) {
      /* Hacia abajo: primer snap target >= progreso actual (margen -0.03) */
      for (var i = 0; i < SNAP_TARGETS.length; i++) {
        if (SNAP_TARGETS[i] >= p - 0.03) { target = SNAP_TARGETS[i]; break; }
      }
    } else {
      /* Hacia arriba: último snap target <= progreso actual (margen +0.03) */
      for (var i = SNAP_TARGETS.length - 1; i >= 0; i--) {
        if (SNAP_TARGETS[i] <= p + 0.03) { target = SNAP_TARGETS[i]; break; }
      }
    }

    if (target === null) return;
    var targetY = root.offsetTop + target * scrollable;
    smoothScrollTo(targetY, SNAP_DURATION_MS);
  }

  function onPageScroll() {
    /* Ignorar eventos generados por smoothScrollTo (previene snap en cascada) */
    if (isSnapping || Date.now() < snapImmunityUntil) return;

    var y = window.scrollY;
    scrollDirection = (y >= lastScrollY) ? 1 : -1;
    lastScrollY = y;

    /* Solo actuar si el hero root está visible en el viewport */
    if (!root) return;
    var rTop = root.getBoundingClientRect().top;
    var rBot = root.getBoundingClientRect().bottom;
    if (rBot < 0 || rTop > window.innerHeight) return;

    clearTimeout(snapDebounceId);
    snapDebounceId = setTimeout(snapToNearest, 220);
  }

  /* ─────────────────────────────────────────────────────
     BOTÓN “SIGUIENTE”
     ───────────────────────────────────────────────────── */
  function bindNavButtons() {
    /*
     * Mapa: ID del botón → fracción de progreso destino.
     * IMPORTANTE: Usar valores explícitos (NO índices de SNAP_TARGETS) para
     * que sean inmunes a cambios en el array.
     *   slide-next-1 → slide-2 peak (0.58)
     *   slide-next-2 → slide-3 peak (0.88)
     *   slide-prev-2 → slide-1 peak (0.22)
     *   slide-prev-3 → slide-2 peak (0.58)
     */
    var map = {
      'slide-next-1': SLIDE_WINDOWS[2].peak,
      'slide-next-2': SLIDE_WINDOWS[3].peak,
      'slide-prev-2': SLIDE_WINDOWS[1].peak,
      'slide-prev-3': SLIDE_WINDOWS[2].peak,
    };
    Object.keys(map).forEach(function (id) {
      var el = document.getElementById(id);
      if (!el || el.dataset.navBound) return;
      el.dataset.navBound = '1';
      var tgt = map[id];
      el.addEventListener('click', function () {
        if (!root) return;
        var scrollable = root.offsetHeight - window.innerHeight;
        smoothScrollTo(root.offsetTop + tgt * scrollable, SNAP_DURATION_MS);
      });
    });
  }

  function bindCTA() {
    if (!ctaEl || ctaEl.dataset.ctaBound) return;
    ctaEl.dataset.ctaBound = '1';
    ctaEl.addEventListener('click', function (e) {
      e.preventDefault();
      if (!root) return;
      /* Bug-3: Target exacto al peak de slide-1 (0.22) para que el snap
         posterior lo encuentre como destino y NO salte al siguiente (0.58).
         La immunity window en smoothScrollTo evita que el momentum post-animación
         dispare un nuevo snap hacia slide-2. */
      var targetScroll = root.offsetTop + (root.offsetHeight - window.innerHeight) * 0.22;
      /* ⏱ VELOCIDAD DEL CTA — ajusta este valor para cambiar la duración:
         900 ms = rápido | 1200 ms = normal | 1600 ms = lento             */
      smoothScrollTo(targetScroll, 150);
    });
  }

  /* ─────────────────────────────────────────────────────
     BOOT — espera que el DOM esté listo
     ───────────────────────────────────────────────────── */
  function boot() {
    root       = document.getElementById(ROOT_ID);
    slides     = document.getElementById(SLIDES_ID);
    ctaEl      = document.getElementById(CTA_ID);
    canvasWrap = document.getElementById('particle-hero-canvas')
                 ? document.getElementById('particle-hero-canvas').parentElement
                 : null;

    if (!root || !slides) return;
    if (initialized) return;
    initialized = true;

    bindCTA();
    bindNavButtons();
    window.addEventListener('scroll', onPageScroll, { passive: true });
    cancelAnimationFrame(rafId);
    rafId = requestAnimationFrame(tick);
  }

  var obs = new MutationObserver(boot);
  obs.observe(document.documentElement, { childList: true, subtree: true });
  boot();

  /* Rebind en caso de navegación SPA */
  window.addEventListener('popstate', function () {
    initialized = false;
    boot();
  });

})();
