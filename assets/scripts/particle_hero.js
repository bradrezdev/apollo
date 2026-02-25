/**
 * ONANO Particle Hero v2 — Scroll-Driven Nanoparticle Simulation
 *
 * Simula la transición científica de una aglomeración compacta de
 * nanopartículas hacia sub-clústeres dispersos, finalizando con
 * encapsulación protectora.
 *
 * Control:
 *   – setScrollProgress(0→1)  — timeline maestro controlado externamente
 *   – Fase 1 (0→0.33): vibración intensa (estado aglomerado activo)
 *   – Fase 2 (0.33→0.66): dispersión hacia sub-clústeres nanométricos
 *   – Fase 3 (0.66→1.0): encapsulación — círculos "stroke-draw" progresivos
 *
 * Auto-inicializable con MutationObserver (Reflex SPA).
 *
 * @version 2.0.0
 */

function initParticleHero(canvasId, opts) {
  'use strict';

  /* ═══════════════════════════════════════════════════════
     CONFIGURACIÓN
     ═══════════════════════════════════════════════════════ */
  var D = {
    particleCount:   120,
    clusterMin:      3,
    clusterMax:      5,
    /* Colores */
    cyan:       [12, 188, 229],   // #0CBCE5
    cyanLight:  [61, 201, 234],   // #3DC9EA
    cyanPale:   [206, 242, 250],  // #CEF2FA
    darkBlue:   [6,  42,  99],    // #062A63
    bg:         '#070D1A',
    /* Aglomeración */
    agglomRadius:  0.10,
    agglomGlow:    0.18,
    /* Vibración */
    vibAmp:        2.8,
    vibSpeedMin:   0.6,
    vibSpeedMax:   2.0,
    /* Dispersión — semi-ejes de la elipse como fracción del canvas (W y H).
     * 📐 AJUSTE MANUAL: sube containX/containY para más expansión.
     *    containX 0.42 = moderado | 0.54 = amplio | 0.68 = máximo
     *    containY 0.20 = moderado | 0.32 = amplio | 0.45 = máximo      */
    containX:      0.54,
    containY:      0.32,
    /* Render */
    glowMul:       3.5,
    connAlphaAgg:  0.055,
    connAlphaDisp: 0.22,
    /* Pulso visual */
    pulseSpeed:    0.0012,
    pulseAmp:      0.25,
  };

  if (opts) { for (var k in opts) { if (opts.hasOwnProperty(k)) D[k] = opts[k]; } }

  /* ═══════════════════════════════════════════════════════
     CANVAS
     ═══════════════════════════════════════════════════════ */
  var canvas = document.getElementById(canvasId);
  if (!canvas) return null;
  var ctx = canvas.getContext('2d');
  var W = 0, H = 0, dpr = 1;
  var animId;

  /* ═══════════════════════════════════════════════════════
     ESTADO
     ═══════════════════════════════════════════════════════ */
  var particles        = [];
  var clusterMeta      = [];
  var clusterMembers   = null;   // Array<Array<index>> — precalculado
  var dispersedTargets = null;   // Array<{tx,ty}> — determinístico (sin aleatoriedad)

  /* Scroll-driven state */
  var scrollProgress = 0.0;
  var encapProgress  = 0.0;

  /* ═══════════════════════════════════════════════════════
     UTILIDADES
     ═══════════════════════════════════════════════════════ */
  function rgba(c, a) { return 'rgba(' + c[0] + ',' + c[1] + ',' + c[2] + ',' + a + ')'; }
  function lerp(a, b, t) { return a + (b - a) * t; }
  function smoothStep(t) { return t * t * (3 - 2 * t); }
  function clamp(v, lo, hi) { return v < lo ? lo : v > hi ? hi : v; }
  function rand(lo, hi) { return lo + Math.random() * (hi - lo); }
  function gaussRand() {
    var u = 1 - Math.random(), v = Math.random();
    return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v);
  }

  /* ═══════════════════════════════════════════════════════
     PARTÍCULA
     ═══════════════════════════════════════════════════════ */
  function Particle(x, y, cid) {
    this.x  = x;  this.y  = y;
    this.hx = x;  this.hy = y;  // posición home (agglomerated)
    this.r   = rand(1.4, 4.6);
    this.op  = rand(0.45, 0.95);
    this.cid = cid;
    this.vPhase = Math.random() * Math.PI * 2;
    this.vSpd   = rand(D.vibSpeedMin, D.vibSpeedMax);
    this.vDirX  = (Math.random() - 0.5) * 2;
    this.vDirY  = (Math.random() - 0.5) * 2;
  }

  /* ═══════════════════════════════════════════════════════
     CREAR ESCENA
     ═══════════════════════════════════════════════════════ */
  function createScene() {
    var cx = W / 2, cy = H / 2;
    var baseR = Math.min(W, H) * D.agglomRadius;

    particles   = [];
    clusterMeta = [];
    var assignments = [];
    var cid = 0;
    while (assignments.length < D.particleCount) {
      var sz = D.clusterMin + Math.floor(Math.random() * (D.clusterMax - D.clusterMin + 1));
      for (var s = 0; s < sz && assignments.length < D.particleCount; s++) {
        assignments.push(cid);
      }
      cid++;
    }
    for (var i = assignments.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var tmp = assignments[i]; assignments[i] = assignments[j]; assignments[j] = tmp;
    }

    for (var i = 0; i < D.particleCount; i++) {
      var ang  = Math.random() * Math.PI * 2;
      var dist = Math.min(Math.abs(gaussRand()) * baseR * 0.45, baseR * 1.2);
      particles.push(new Particle(
        cx + Math.cos(ang) * dist,
        cy + Math.sin(ang) * dist,
        assignments[i]
      ));
    }

    for (var c = 0; c < cid; c++) {
      clusterMeta.push({ c: c });
    }

    buildClusterMemberLists();
    computeDispersedTargets();
    dispersedTargets = null;  // Se recalcula en el primer uso post-resize
  }

  /* ═══════════════════════════════════════════════════════
     PRECÁLCULOS
     ═══════════════════════════════════════════════════════ */
  /**
   * Índices de partículas por clúster — O(1) lookup.
   */
  function buildClusterMemberLists() {
    clusterMembers = [];
    for (var c = 0; c < clusterMeta.length; c++) clusterMembers.push([]);
    for (var i = 0; i < particles.length; i++) clusterMembers[particles[i].cid].push(i);
  }

  /**
   * Posiciones objetivo de dispersión, determinísticas (sin Math.random).
   * Garantiza que scroll-up/down sea el espejo exacto del mismo movimiento.
   */
  function computeDispersedTargets() {
    if (!particles.length) return;
    var cx = W / 2, cy = H / 2;
    var ellA = W * D.containX;
    var ellB = H * D.containY;
    var N = clusterMeta.length;

    /* Targets por clúster — ángulos y radios determinísticos */
    var cTargets = [];
    for (var c = 0; c < N; c++) {
      var ang = (c / N) * Math.PI * 2 + (c % 3 === 0 ? 0.42 : c % 3 === 1 ? -0.31 : 0.18);
      /* 📐 AJUSTE MANUAL: rf define qué tan lejos del centro cae cada clúster.
       *  base 0.28→0.38 = compacto | 0.38→0.48 = amplio              */
      var rf  = 0.38 + (c % 5) * 0.13;
      cTargets.push({
        tx: cx + Math.cos(ang) * ellA * rf,
        ty: cy + Math.sin(ang) * ellB * rf,
      });
    }

    /* Por partícula: offset dentro del clúster usando vDirX/Y (fijo) */
    dispersedTargets = [];
    for (var i = 0; i < particles.length; i++) {
      var p  = particles[i];
      var ct = cTargets[p.cid];
      var offset = 9 + (i % D.clusterMax) * 3.5;
      dispersedTargets.push({
        tx: ct.tx + p.vDirX * offset,
        ty: ct.ty + p.vDirY * offset,
      });
    }
  }

  /* ═══════════════════════════════════════════════════════
     UPDATE — SCROLL-DRIVEN
     ═══════════════════════════════════════════════════════ */
  function update(t) {
    var sp = scrollProgress;

    /* Fases del scroll (0→1) */
    var p1 = smoothStep(clamp(sp / 0.33, 0, 1));           // vibración
    var p2 = smoothStep(clamp((sp - 0.33) / 0.33, 0, 1));  // dispersión
    encapProgress = smoothStep(clamp((sp - 0.66) / 0.34, 0, 1)); // encapsulación

    var vibMul = 1 + p1 * 2.6;  // vibración hasta 3.6× en pico

    if (!dispersedTargets) computeDispersedTargets();

    for (var i = 0; i < particles.length; i++) {
      var p  = particles[i];
      var dt = dispersedTargets[i];

      /* Posición base: lerp home → target (reversible en scroll-up) */
      var bx = lerp(p.hx, dt.tx, p2);
      var by = lerp(p.hy, dt.ty, p2);

      /* Vibración orgánica sobre la posición base */
      var vib = Math.sin(t * 0.001 * p.vSpd + p.vPhase);
      p.x = bx + vib * p.vDirX * D.vibAmp * vibMul;
      p.y = by + vib * p.vDirY * D.vibAmp * vibMul;
    }
  }

  /* ═══════════════════════════════════════════════════════
     RENDER
     ═══════════════════════════════════════════════════════ */
  function draw(t) {
    ctx.fillStyle = D.bg;
    ctx.fillRect(0, 0, W, H);

    /* Viñeta radial */
    var vigR = Math.max(W, H) * 0.7;
    var vig  = ctx.createRadialGradient(W / 2, H / 2, 0, W / 2, H / 2, vigR);
    vig.addColorStop(0,   rgba(D.cyan, 0.018));
    vig.addColorStop(0.5, rgba(D.darkBlue, 0.008));
    vig.addColorStop(1,   'rgba(0,0,0,0)');
    ctx.fillStyle = vig;
    ctx.fillRect(0, 0, W, H);

    var sp = scrollProgress;
    var p2 = clamp((sp - 0.33) / 0.33, 0, 1);

    if (p2 < 0.05) {
      /* Fase 1 + inicial: visual de aglomeración */
      drawAgglomerated(t);
    } else {
      /* Fase 2+: visual de clústeres dispersos */
      drawDispersed();
    }

    /* Fase 3: anillos de encapsulación */
    if (encapProgress > 0) drawEncapsulation();
  }

  /* ── Render: aglomeración ─────────────────────────────── */
  function drawAgglomerated(t) {
    var cx = W / 2, cy = H / 2;

    /* Glow central pulsante */
    var sp     = scrollProgress;
    var p1     = smoothStep(clamp(sp / 0.33, 0, 1));
    var pulse  = 1 + Math.sin(t * D.pulseSpeed) * D.pulseAmp * (0.35 + p1 * 0.4);
    var glR    = Math.min(W, H) * D.agglomGlow * pulse;
    var glow   = ctx.createRadialGradient(cx, cy, 0, cx, cy, glR);
    glow.addColorStop(0,   rgba(D.cyan, 0.065 + p1 * 0.05));
    glow.addColorStop(0.4, rgba(D.cyan, 0.025));
    glow.addColorStop(1,   rgba(D.cyan, 0));
    ctx.beginPath();
    ctx.arc(cx, cy, glR, 0, Math.PI * 2);
    ctx.fillStyle = glow;
    ctx.fill();

    /* Conexiones moleculares */
    var baseR  = Math.min(W, H) * D.agglomRadius;
    var thresh = baseR * baseR * 0.14;
    ctx.beginPath();
    for (var i = 0; i < particles.length; i++) {
      for (var j = i + 1; j < particles.length; j++) {
        var dx = particles[i].x - particles[j].x;
        var dy = particles[i].y - particles[j].y;
        if (dx * dx + dy * dy < thresh) {
          ctx.moveTo(particles[i].x, particles[i].y);
          ctx.lineTo(particles[j].x, particles[j].y);
        }
      }
    }
    ctx.strokeStyle = rgba(D.cyan, D.connAlphaAgg);
    ctx.lineWidth   = 0.4;
    ctx.stroke();

    drawParticles();
  }

  /* ── Render: clústeres dispersos ──────────────────────── */
  function drawDispersed() {
    if (!clusterMembers) return;

    for (var c = 0; c < clusterMembers.length; c++) {
      var mIdx = clusterMembers[c];
      if (mIdx.length < 2) continue;

      var avgX = 0, avgY = 0;
      for (var m = 0; m < mIdx.length; m++) {
        avgX += particles[mIdx[m]].x;
        avgY += particles[mIdx[m]].y;
      }
      avgX /= mIdx.length;
      avgY /= mIdx.length;

      /* Glow compartido */
      var cgR  = 28 + mIdx.length * 3;
      var cgl  = ctx.createRadialGradient(avgX, avgY, 0, avgX, avgY, cgR);
      cgl.addColorStop(0, rgba(D.cyan, 0.032));
      cgl.addColorStop(1, rgba(D.cyan, 0));
      ctx.beginPath();
      ctx.arc(avgX, avgY, cgR, 0, Math.PI * 2);
      ctx.fillStyle = cgl;
      ctx.fill();

      /* Conexiones intra-clúster */
      ctx.beginPath();
      for (var a = 0; a < mIdx.length; a++) {
        for (var b = a + 1; b < mIdx.length; b++) {
          var pa = particles[mIdx[a]], pb = particles[mIdx[b]];
          var dx = pa.x - pb.x, dy = pa.y - pb.y;
          if (Math.sqrt(dx * dx + dy * dy) < 90) {
            ctx.moveTo(pa.x, pa.y);
            ctx.lineTo(pb.x, pb.y);
          }
        }
      }
      ctx.strokeStyle = rgba(D.cyan, D.connAlphaDisp * 0.7);
      ctx.lineWidth   = 0.6;
      ctx.stroke();
    }

    drawParticles();
  }

  /* ── Render: partículas individuales ──────────────────── */
  function drawParticles() {
    for (var i = 0; i < particles.length; i++) {
      var p = particles[i];

      var gr   = p.r * D.glowMul;
      var grad = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, gr);
      grad.addColorStop(0, rgba(D.cyan, p.op * 0.22));
      grad.addColorStop(1, rgba(D.cyan, 0));
      ctx.beginPath();
      ctx.arc(p.x, p.y, gr, 0, Math.PI * 2);
      ctx.fillStyle = grad;
      ctx.fill();

      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fillStyle = rgba(D.cyanLight, p.op);
      ctx.fill();
    }
  }

  /* ── Render: encapsulación (Fase 3) ───────────────────── */
  function drawEncapsulation() {
    if (!clusterMembers || encapProgress <= 0) return;
    var ep = encapProgress;

    for (var c = 0; c < clusterMembers.length; c++) {
      var mIdx = clusterMembers[c];
      if (mIdx.length < 2) continue;

      /* Centro de masa del clúster */
      var cx = 0, cy = 0;
      for (var m = 0; m < mIdx.length; m++) {
        cx += particles[mIdx[m]].x;
        cy += particles[mIdx[m]].y;
      }
      cx /= mIdx.length;
      cy /= mIdx.length;

      /* Radio envolvente */
      var maxD = 0;
      for (var m = 0; m < mIdx.length; m++) {
        var dx = particles[mIdx[m]].x - cx;
        var dy = particles[mIdx[m]].y - cy;
        var d  = Math.sqrt(dx * dx + dy * dy);
        if (d > maxD) maxD = d;
      }
      var r = maxD + particles[mIdx[0]].r * 3 + 7;

      /* Stroke-draw progresivo: comienza desde -π/2, barre ep*2π */
      ctx.beginPath();
      ctx.arc(cx, cy, r, -Math.PI / 2, -Math.PI / 2 + Math.PI * 2 * ep);
      ctx.strokeStyle = rgba(D.cyan, (0.40 + ep * 0.35) * ep);
      ctx.lineWidth   = 0.8 + ep * 0.6;
      ctx.stroke();

      /* Segundo anillo tenue (profundidad) */
      ctx.beginPath();
      ctx.arc(cx, cy, r + 4, -Math.PI / 2, -Math.PI / 2 + Math.PI * 2 * ep);
      ctx.strokeStyle = rgba(D.cyan, 0.10 * ep);
      ctx.lineWidth   = 0.5;
      ctx.stroke();

      /* Relleno glow en el interior al cerrar (ep > 0.5) */
      if (ep > 0.5) {
        var fe   = (ep - 0.5) * 2;
        var fgl  = ctx.createRadialGradient(cx, cy, r * 0.25, cx, cy, r);
        fgl.addColorStop(0, rgba(D.cyan, 0.025 * fe));
        fgl.addColorStop(1, rgba(D.cyan, 0));
        ctx.beginPath();
        ctx.arc(cx, cy, r, 0, Math.PI * 2);
        ctx.fillStyle = fgl;
        ctx.fill();
      }
    }
  }

  /* ═══════════════════════════════════════════════════════
     RESIZE
     ═══════════════════════════════════════════════════════ */
  function resize() {
    var par = canvas.parentElement;
    W   = par ? par.clientWidth  : window.innerWidth;
    H   = par ? par.clientHeight : window.innerHeight;
    dpr = window.devicePixelRatio || 1;
    canvas.width  = W * dpr;
    canvas.height = H * dpr;
    canvas.style.width  = W + 'px';
    canvas.style.height = H + 'px';
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }

  /* ═══════════════════════════════════════════════════════
     LOOP DE ANIMACIÓN
     ═══════════════════════════════════════════════════════ */
  function animate(t) {
    animId = requestAnimationFrame(animate);
    update(t);
    draw(t);
  }

  /* ═══════════════════════════════════════════════════════
     EVENTOS
     ═══════════════════════════════════════════════════════ */
  var resizeTimer;
  function onResize() {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(function () {
      var oW = W || 1, oH = H || 1;
      resize();
      var sx = W / oW, sy = H / oH;
      for (var i = 0; i < particles.length; i++) {
        particles[i].hx *= sx;
        particles[i].hy *= sy;
      }
      dispersedTargets = null;  // Recalcular post-resize
    }, 100);
  }

  window.addEventListener('resize', onResize);

  /* ═══════════════════════════════════════════════════════
     API PÚBLICA
     ═══════════════════════════════════════════════════════ */
  var api = {
    /**
     * Setter principal del timeline de scroll.
     * @param {number} p  — progreso normalizado 0–1
     */
    setScrollProgress: function (p) {
      scrollProgress = clamp(p, 0, 1);
    },
    destroy: function () {
      cancelAnimationFrame(animId);
      window.removeEventListener('resize', onResize);
    },
  };

  if (!window.__oParticleHero) {
    window.__oParticleHero = api;
  }

  /* ═══════════════════════════════════════════════════════
     ARRANQUE
     ═══════════════════════════════════════════════════════ */
  resize();
  createScene();
  animate(0);

  return api;
}

/* ═══════════════════════════════════════════════════════
   AUTO-INICIALIZACIÓN  (Reflex SPA)
   ═══════════════════════════════════════════════════════ */
(function () {
  var ID    = 'particle-hero-canvas';
  var _inst = null;

  function boot() {
    var c = document.getElementById(ID);
    if (!c || c.dataset.heroInit === '1') return;
    c.dataset.heroInit = '1';
    if (_inst && _inst.destroy) _inst.destroy();
    _inst = initParticleHero(ID);
    window.__oParticleHero = _inst;
  }

  var obs = new MutationObserver(boot);
  obs.observe(document.documentElement, { childList: true, subtree: true });
  boot();
})();
