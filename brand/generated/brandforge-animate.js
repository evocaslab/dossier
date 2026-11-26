/* Replays brand animations shown with <img data-brandforge-anim="id">. Does nothing under reduced motion. */
(function () {
  "use strict";
  var DEFAULTS = {"animated-mark": ["hover", "focus"]};
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)");
  function init(img) {
    if (reduce && reduce.matches) { return; }
    var attr = img.getAttribute("data-brandforge-replay");
    var modes = attr !== null ? attr.split(/\s+/) : (DEFAULTS[img.getAttribute("data-brandforge-anim")] || []);
    var base = (img.getAttribute("src") || "").split("?")[0];
    var count = 0;
    function replay() { count += 1; img.setAttribute("src", base + "?r=" + count); }
    if (modes.indexOf("hover") >= 0) { img.addEventListener("pointerenter", replay); }
    if (modes.indexOf("focus") >= 0) {
      if (!img.hasAttribute("tabindex")) { img.tabIndex = 0; }
      img.addEventListener("focus", replay);
    }
  }
  function start() {
    Array.prototype.forEach.call(document.querySelectorAll("img[data-brandforge-anim]"), init);
  }
  if (document.readyState === "loading") { document.addEventListener("DOMContentLoaded", start); }
  else { start(); }
})();
