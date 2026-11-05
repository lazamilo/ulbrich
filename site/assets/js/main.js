(() => {
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const isTouch = window.matchMedia('(hover: none)').matches;
  const root = document.documentElement;
  if (reduced) root.classList.add('reduced');
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];
  const hasGsap = typeof gsap !== 'undefined';
  if (hasGsap) gsap.registerPlugin(ScrollTrigger);

  /* smooth scroll */
  let lenis = null;
  if (!reduced && typeof Lenis !== 'undefined') {
    lenis = new Lenis({ duration: 1.15, smoothWheel: true });
    if (hasGsap) {
      lenis.on('scroll', ScrollTrigger.update);
      gsap.ticker.add(t => lenis.raf(t * 1000));
      gsap.ticker.lagSmoothing(0);
    } else {
      const raf = t => { lenis.raf(t); requestAnimationFrame(raf); };
      requestAnimationFrame(raf);
    }
  }

  /* header: solid after scroll, hide on scroll down */
  const hdr = $('.hdr');
  let lastY = 0;
  const onScroll = () => {
    const y = window.scrollY;
    hdr.classList.toggle('is-solid', y > 40);
    const megaOpen = $('.mega.is-open');
    hdr.classList.toggle('is-hidden', y > 300 && y > lastY && !megaOpen && !root.classList.contains('menu-open'));
    lastY = y;
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* mega menu */
  const mega = $('.mega'), scrim = $('.mega-scrim'), trigger = $('[data-mega]');
  if (mega && trigger) {
    let closeT;
    const open = () => { clearTimeout(closeT); mega.classList.add('is-open'); scrim.classList.add('is-open'); hdr.classList.add('is-solid'); };
    const close = () => { closeT = setTimeout(() => { mega.classList.remove('is-open'); scrim.classList.remove('is-open'); onScroll(); }, 120); };
    trigger.addEventListener('mouseenter', open);
    trigger.addEventListener('click', e => { e.preventDefault(); mega.classList.contains('is-open') ? close() : open(); });
    trigger.addEventListener('mouseleave', close);
    mega.addEventListener('mouseenter', open);
    mega.addEventListener('mouseleave', close);
    scrim.addEventListener('click', close);
    const cats = $$('.mega-cats a'), subs = $$('.mega-subs'), pic = $('.mega-pic img');
    cats.forEach((a, i) => a.addEventListener('mouseenter', () => {
      cats.forEach(c => c.classList.toggle('is-on', c === a));
      subs.forEach((s, j) => s.classList.toggle('is-on', j === i));
      if (pic) { pic.style.opacity = 0; setTimeout(() => { pic.src = a.dataset.pic; pic.style.opacity = 1; }, 150); }
    }));
  }

  /* mobile menu */
  const burger = $('.burger');
  if (burger) burger.addEventListener('click', () => {
    root.classList.toggle('menu-open');
    if (lenis) root.classList.contains('menu-open') ? lenis.stop() : lenis.start();
  });

  /* inquiry drawer */
  const drawer = $('.drawer'), dscrim = $('.drawer-scrim');
  const openDrawer = topic => {
    if (!drawer) return;
    drawer.classList.remove('sent');
    $('.topic', drawer).textContent = topic || 'Splošno povpraševanje';
    const tf = $('input[name=tema]', drawer); if (tf) tf.value = topic || '';
    drawer.classList.add('is-open'); dscrim.classList.add('is-open');
    if (lenis) lenis.stop();
  };
  const closeDrawer = () => { drawer.classList.remove('is-open'); dscrim.classList.remove('is-open'); if (lenis) lenis.start(); };
  $$('[data-inquiry]').forEach(b => b.addEventListener('click', e => { e.preventDefault(); openDrawer(b.dataset.inquiry); }));
  if (drawer) {
    $('.x', drawer).addEventListener('click', closeDrawer);
    dscrim.addEventListener('click', closeDrawer);
    document.addEventListener('keydown', e => { if (e.key === 'Escape') closeDrawer(); });
    $('form', drawer).addEventListener('submit', e => { e.preventDefault(); drawer.classList.add('sent'); });
  }
  const pageForm = $('.page-form');
  if (pageForm) pageForm.addEventListener('submit', e => { e.preventDefault(); pageForm.closest('.formbox').classList.add('sent'); });

  /* tech index: floating product image */
  const float = $('.tech-float');
  if (float && !isTouch) {
    const imgs = $$('img', float);
    let x = 0, y = 0, cx = 0, cy = 0;
    $$('.tech-row').forEach((row, i) => {
      row.addEventListener('mouseenter', () => { float.classList.add('on'); imgs.forEach((im, j) => im.classList.toggle('on', i === j)); });
      row.addEventListener('mouseleave', () => float.classList.remove('on'));
    });
    window.addEventListener('mousemove', e => { x = e.clientX; y = e.clientY; });
    window.addEventListener('scroll', () => {
      const el = document.elementFromPoint(x, y);
      if (!el || !el.closest('.tech-row')) float.classList.remove('on');
    }, { passive: true });
    const tick = () => { cx += (x - cx) * .14; cy += (y - cy) * .14; float.style.left = cx + 'px'; float.style.top = cy + 'px'; requestAnimationFrame(tick); };
    tick();
  }

  if (!hasGsap || reduced) { $$('.rv').forEach(el => { el.style.opacity = 1; el.style.transform = 'none'; }); const l = $('.loader'); if (l) l.remove(); return; }

  /* loader: logo wipe */
  const loader = $('.loader');
  const intro = gsap.timeline();
  if (loader) {
    intro.from('.loader .lg img', { yPercent: 105, duration: .8, ease: 'power3.out' })
      .to('.loader .lg img', { yPercent: -105, duration: .6, ease: 'power3.in', delay: .25 })
      .to(loader, { yPercent: -100, duration: .8, ease: 'power3.inOut' }, '-=.15')
      .set(loader, { display: 'none' });
  }

  /* hero headline */
  if ($('.hero h1')) {
    intro.from('.hero h1 .line > span', { yPercent: 110, duration: 1.1, stagger: .09, ease: 'power4.out' }, loader ? '-=.45' : 0)
      .from('.hero-side > *', { y: 24, opacity: 0, duration: .8, stagger: .08, ease: 'power3.out' }, '-=.8')
      .from('.hero-band', { scaleY: 0, duration: 1.1, ease: 'power4.inOut' }, '-=1');
  }
  if ($('.phero h1')) {
    intro.from('.phero h1 .line > span', { yPercent: 110, duration: 1.05, stagger: .08, ease: 'power4.out' }, loader ? '-=.45' : 0)
      .from('.phero-pic', { clipPath: 'inset(100% 0 0 0)', duration: 1.2, ease: 'power4.inOut' }, '-=.9');
  }

  /* hero reel: endless drift, speeds up with scroll velocity */
  const reel = $('.reel');
  if (reel) {
    reel.innerHTML += reel.innerHTML;
    let pos = 0, boost = 0;
    const half = () => reel.scrollWidth / 2;
    if (lenis) lenis.on('scroll', ({ velocity }) => { boost = Math.min(Math.abs(velocity) * .6, 14); });
    gsap.ticker.add(() => {
      pos -= .55 + boost; boost *= .92;
      if (-pos >= half()) pos += half();
      reel.style.transform = `translate3d(${pos}px,-50%,0)`;
    });
    gsap.to('.hero-band', { scrollTrigger: { trigger: '.hero-band', start: 'top 70%', end: 'bottom top', scrub: true }, yPercent: 8, ease: 'none' });
  }

  /* statement: words light up on scroll */
  const st = $('.statement .h-xl');
  if (st) {
    st.innerHTML = st.textContent.trim().split(/\s+/).map(w => `<span class="w">${w}</span>`).join(' ');
    gsap.to('.statement .w', { opacity: 1, stagger: .1, ease: 'none', scrollTrigger: { trigger: st, start: 'top 80%', end: 'bottom 45%', scrub: true } });
  }

  /* horizontal plasma track */
  const hs = $('.hscroll');
  if (hs && window.innerWidth > 820) {
    const track = $('.track', hs);
    const dist = () => track.scrollWidth - window.innerWidth + 40;
    gsap.to(track, { x: () => -dist(), ease: 'none', scrollTrigger: { trigger: hs, start: 'top top', end: () => '+=' + dist(), pin: '.hscroll-pin', scrub: .6, invalidateOnRefresh: true } });
    $$('.pcard .pic:not(.fit) img', hs).forEach(img => gsap.fromTo(img, { xPercent: -6 }, { xPercent: 6, ease: 'none', scrollTrigger: { trigger: hs, start: 'top top', end: () => '+=' + dist(), scrub: true } }));
  }

  /* parallax inside frames */
  $$('[data-par]').forEach(el => gsap.fromTo(el, { yPercent: -8 }, { yPercent: 8, ease: 'none', scrollTrigger: { trigger: el.parentElement, start: 'top bottom', end: 'bottom top', scrub: true } }));

  /* numbers count up */
  $$('[data-count]').forEach(el => {
    const end = +el.dataset.count, obj = { v: el.dataset.from ? +el.dataset.from : 0 };
    gsap.to(obj, { v: end, duration: 1.8, ease: 'power3.out', scrollTrigger: { trigger: el, start: 'top 85%', once: true }, onUpdate: () => { el.firstChild.nodeValue = Math.round(obj.v); } });
  });

  /* generic reveals */
  $$('.rv').forEach(el => gsap.to(el, { opacity: 1, y: 0, duration: 1, ease: 'power3.out', scrollTrigger: { trigger: el, start: 'top 88%', once: true } }));
  $$('[data-stagger]').forEach(g => gsap.from(g.children, { opacity: 0, y: 40, duration: .9, stagger: .06, ease: 'power3.out', scrollTrigger: { trigger: g, start: 'top 85%', once: true } }));
  $$('.split-lines').forEach(h => {
    gsap.from(h, { clipPath: 'inset(0 0 100% 0)', y: 50, duration: 1.1, ease: 'power4.out', scrollTrigger: { trigger: h, start: 'top 88%', once: true } });
  });

  window.addEventListener('load', () => ScrollTrigger.refresh());
})();
