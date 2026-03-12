/**
 * apollo_particle_bridge.js
 * 
 * Smooth particle scroll interpolation for Apollo's step-based
 * navigation. Replaces scroll_timeline.js since Apollo uses
 * discrete steps instead of vertical scroll.
 * 
 * Depends on: particle_hero.js (must load first — provides window.__oParticleHero)
 * 
 * Usage from Reflex:
 *   rx.call_script("window.animateParticleScroll(0.5, 800);")
 */
(function () {
  'use strict';

  window._apolloParticleProgress = 0;
  window._apolloAnimId = null;

  /**
   * Get the particle hero API, with polling retry until it boots.
   * @returns {object|null} The API or null if not available after retries
   */
  function getParticleApi() {
    return window.__oParticleHero || null;
  }

  /**
   * Smoothly interpolate the particle scrollProgress from the
   * current value to targetProgress over `duration` ms.
   *
   * Uses easeInOutQuad — same feel as onano_website's smoothStep.
   *
   * @param {number} targetProgress  0–1 target for setScrollProgress
   * @param {number} duration        animation duration in ms
   */
  window.animateParticleScroll = function (targetProgress, duration) {
    var api = getParticleApi();
    if (!api) {
      // Particle engine not yet booted — poll with exponential backoff
      var retries = 0;
      var maxRetries = 10;
      var baseDelay = 50;
      
      function poll() {
        api = getParticleApi();
        if (api) {
          window.animateParticleScroll(targetProgress, duration);
          return;
        }
        retries++;
        if (retries < maxRetries) {
          // Exponential backoff: 50, 100, 200, 400, 800...
          setTimeout(poll, baseDelay * Math.pow(2, retries - 1));
        }
        // Silent fail after max retries — particles just won't animate
      }
      
      setTimeout(poll, baseDelay);
      return;
    }

    if (window._apolloAnimId) cancelAnimationFrame(window._apolloAnimId);

    var startProgress = window._apolloParticleProgress;
    var startT = performance.now();

    function tick(now) {
      var elapsed = now - startT;
      var t = Math.min(elapsed / duration, 1);
      // easeInOutQuad
      var ease = t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;
      var val = startProgress + (targetProgress - startProgress) * ease;
      api.setScrollProgress(val);
      window._apolloParticleProgress = val;
      if (t < 1) {
        window._apolloAnimId = requestAnimationFrame(tick);
      } else {
        api.setScrollProgress(targetProgress);
        window._apolloParticleProgress = targetProgress;
        window._apolloAnimId = null;
      }
    }

    window._apolloAnimId = requestAnimationFrame(tick);
  };
})();
