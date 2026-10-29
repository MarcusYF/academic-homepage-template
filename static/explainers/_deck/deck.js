/* Paper explainer decks.
   Markup: <main class="dk-deck"> with <section class="dk-slide" data-label="...">.
   Inside a slide, [data-step="n"] appears at build step n; [data-dim="n"] fades once step n is shown.
   Animations: .dk-draw (stroke draws in; dashed strokes fade in), .dk-grow (bar grows), [data-count-to] (number counts up).
   They run when the slide is current and their nearest [data-step] (if any) is shown.
   Extension hooks for per-deck interactions: Deck.on("enter", (index, slide) => {}), Deck.on("step", (index, step, slide) => {}). */
(function () {
  "use strict";
  const deck = document.querySelector(".dk-deck");
  if (!deck) return;
  const slides = Array.from(deck.querySelectorAll(".dk-slide"));
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const listeners = { enter: [], step: [] };
  const counter = document.querySelector("[data-dk-count]");
  const dotsBox = document.querySelector(".dk-dots");
  const prevBtn = document.querySelector("[data-dk-prev]");
  const nextBtn = document.querySelector("[data-dk-next]");

  // Optional "Ask about this slide": set <body data-ask="<url>"> to add a button that opens a Q&A page (for example an
  // AI assistant you host) with a question about the current slide appended as #question=...; a slide can set its own
  // question with data-ask="...". Without data-ask nothing is added.
  const askRoom = document.body.dataset.ask;
  let askLink = null;
  if (askRoom) {
    askLink = document.createElement("a");
    askLink.className = "dk-askbtn";
    askLink.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 5.5A2.5 2.5 0 0 1 6.5 3h11A2.5 2.5 0 0 1 20 5.5v8A2.5 2.5 0 0 1 17.5 16H10l-5 4v-4.3A2.5 2.5 0 0 1 4 13.5z"/><path d="M8.5 8.5h7M8.5 11.5h4.5"/></svg><span>Ask about this slide</span>';
    const nav = document.querySelector(".dk-nav");
    if (nav) nav.append(askLink);
  }
  function askQuestion(slide, i) {
    if (slide.dataset.ask) return slide.dataset.ask;
    const h = slide.querySelector(".dk-h");
    const title = h ? h.textContent.replace(/\s+/g, " ").trim() : "";
    if (i === 0 || !title) return "What problem does this paper address, and what are its main contributions?";
    return "I am reading the visual introduction. Can you explain this point in more detail, using the paper: \u201c" + title + "\u201d";
  }

  const steps = slides.map((s) => {
    const values = new Set();
    s.querySelectorAll("[data-step]").forEach((el) => values.add(Number(el.dataset.step)));
    return Array.from(values).sort((a, b) => a - b);
  });

  slides.forEach((s, i) => {
    if (s.dataset.label) {
      const l = document.createElement("div");
      l.className = "dk-label"; l.textContent = s.dataset.label; s.prepend(l);
    }
    const n = document.createElement("div");
    n.className = "dk-num"; n.textContent = String(i + 1); s.append(n);
    s.setAttribute("aria-roledescription", "slide");
    s.setAttribute("aria-label", (i + 1) + " of " + slides.length);
    if (dotsBox) dotsBox.append(document.createElement("span"));
  });

  // Prepare stroke drawing. Dashed strokes cannot use the dash-offset trick (it would make them
  // solid), so they fade in instead.
  deck.querySelectorAll(".dk-draw").forEach((p) => {
    const dashes = getComputedStyle(p).strokeDasharray;
    if (p.classList.contains("dash") || (dashes && dashes !== "none")) {
      p.dataset.fade = "1";
      p.style.opacity = reduce ? 1 : 0;
      return;
    }
    try {
      const len = Math.ceil(p.getTotalLength());
      p.style.strokeDasharray = len + " " + len;
      p.style.strokeDashoffset = reduce ? 0 : len;
      p.dataset.len = len;
    } catch (e) { /* not a geometry element */ }
  });

  function visibleIn(el, slide) {
    const host = el.closest("[data-step]");
    return slide.classList.contains("is-current") && (!host || host.classList.contains("is-on"));
  }

  function animateCount(el) {
    const to = Number(el.dataset.countTo);
    const dec = Number(el.dataset.decimals || 0);
    const pre = el.dataset.prefix || "", suf = el.dataset.suffix || "";
    const fmt = (v) => pre + v.toLocaleString("en-US", { minimumFractionDigits: dec, maximumFractionDigits: dec }) + suf;
    if (reduce) { el.textContent = fmt(to); return; }
    const t0 = performance.now(), dur = 1100;
    const tick = (t) => {
      const k = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - k, 3);
      el.textContent = fmt(to * e);
      if (k < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  }

  function refresh(slide) {
    slide.querySelectorAll(".dk-draw").forEach((p) => {
      if (p.dataset.fade) p.style.opacity = visibleIn(p, slide) || reduce ? 1 : 0;
      else if (p.dataset.len) p.style.strokeDashoffset = visibleIn(p, slide) || reduce ? 0 : p.dataset.len;
    });
    slide.querySelectorAll(".dk-grow").forEach((g) => g.classList.toggle("is-grown", visibleIn(g, slide)));
    slide.querySelectorAll("[data-count-to]").forEach((c) => {
      const vis = visibleIn(c, slide);
      if (vis && !c.dataset.done) { c.dataset.done = "1"; animateCount(c); }
      if (!vis) { c.dataset.done = ""; }
    });
  }

  let cur = 0, stepIdx = 0;

  function render(fireEnter) {
    slides.forEach((s, i) => {
      s.classList.toggle("is-current", i === cur);
      s.classList.toggle("is-before", i < cur);
      s.setAttribute("aria-hidden", i === cur ? "false" : "true");
      if (i !== cur) refresh(s);
    });
    const s = slides[cur];
    const shown = stepIdx > 0 ? steps[cur][stepIdx - 1] : -Infinity;
    s.querySelectorAll("[data-step]").forEach((el) => el.classList.toggle("is-on", Number(el.dataset.step) <= shown));
    s.querySelectorAll("[data-dim]").forEach((el) => el.classList.toggle("is-dimmed", Number(el.dataset.dim) <= shown));
    refresh(s);
    if (counter) counter.textContent = (cur + 1) + " / " + slides.length;
    if (dotsBox) Array.from(dotsBox.children).forEach((d, i) => d.classList.toggle("is-on", i === cur));
    if (prevBtn) prevBtn.disabled = cur === 0 && stepIdx === 0;
    if (nextBtn) nextBtn.disabled = cur === slides.length - 1 && stepIdx === steps[cur].length;
    if (askLink) askLink.href = askRoom + "#question=" + encodeURIComponent(askQuestion(s, cur));
    if (fireEnter) listeners.enter.forEach((f) => f(cur, s));
    listeners.step.forEach((f) => f(cur, shown, s));
    const h = "#" + (cur + 1);
    if (location.hash !== h) history.replaceState(null, "", h);
  }

  function go(i, atEnd) {
    cur = Math.max(0, Math.min(slides.length - 1, i));
    stepIdx = atEnd ? steps[cur].length : 0;
    slides[cur].scrollTop = 0;
    render(true);
  }
  function next() {
    if (stepIdx < steps[cur].length) { stepIdx++; render(false); }
    else if (cur < slides.length - 1) go(cur + 1, false);
  }
  function prev() {
    if (stepIdx > 0) { stepIdx--; render(false); }
    else if (cur > 0) go(cur - 1, true);
  }

  document.addEventListener("keydown", (e) => {
    if (e.target.closest("input, textarea, select")) return;
    if (["ArrowRight", "PageDown", " ", "Enter"].includes(e.key)) { e.preventDefault(); next(); }
    else if (["ArrowLeft", "PageUp", "Backspace"].includes(e.key)) { e.preventDefault(); prev(); }
    else if (e.key === "Home") { e.preventDefault(); go(0, false); }
    else if (e.key === "End") { e.preventDefault(); go(slides.length - 1, true); }
  });
  deck.addEventListener("click", (e) => {
    if (e.target.closest("a, button, input, label, select, textarea, [data-interactive]")) return;
    if (window.getSelection && String(window.getSelection())) return;
    const r = deck.getBoundingClientRect();
    if (e.clientX - r.left < r.width * 0.28) prev(); else next();
  });
  let tx = 0, ty = 0;
  deck.addEventListener("touchstart", (e) => { tx = e.touches[0].clientX; ty = e.touches[0].clientY; }, { passive: true });
  deck.addEventListener("touchend", (e) => {
    if (e.target.closest("input, [data-interactive], .dk-fig.is-scroll")) return;
    const dx = e.changedTouches[0].clientX - tx, dy = e.changedTouches[0].clientY - ty;
    if (Math.abs(dx) > 50 && Math.abs(dy) < 60) { dx < 0 ? next() : prev(); }
  }, { passive: true });
  if (prevBtn) prevBtn.addEventListener("click", prev);
  if (nextBtn) nextBtn.addEventListener("click", next);

  window.Deck = {
    on(evt, fn) { if (listeners[evt]) listeners[evt].push(fn); },
    next, prev, go: (i) => go(i, false),
    get index() { return cur; }
  };

  // Narrow screens: keep wide diagrams legible (min width, horizontal scroll) and suggest landscape once.
  function fitFigures() {
    const narrow = window.innerWidth < 640;
    deck.querySelectorAll(".dk-fig").forEach((fig) => {
      const svg = fig.querySelector(":scope > svg[viewBox]");
      if (!svg) return;
      const vbw = Number((svg.getAttribute("viewBox") || "").split(/[ ,]+/)[2]) || 0;
      svg.style.minWidth = narrow && vbw > 520 ? Math.round(vbw * 0.7) + "px" : "";
      fig.classList.toggle("is-scroll", narrow && svg.scrollWidth > fig.clientWidth + 4);
    });
  }
  fitFigures();
  window.addEventListener("resize", fitFigures);
  try {
    if (window.innerWidth < 640 && window.innerHeight > window.innerWidth && !sessionStorage.getItem("dk-rotate")) {
      const tip = document.createElement("div");
      tip.className = "dk-rotate";
      tip.innerHTML = '<span>Tip: turn your phone sideways for larger diagrams.</span><button type="button" aria-label="Dismiss">×</button>';
      tip.querySelector("button").addEventListener("click", () => { tip.remove(); try { sessionStorage.setItem("dk-rotate", "1"); } catch (e) {} });
      document.body.append(tip);
    }
  } catch (e) { /* storage unavailable */ }

  const start = parseInt((location.hash || "").slice(1), 10);
  window.addEventListener("load", () => go(Number.isFinite(start) ? start - 1 : 0, false));
})();
