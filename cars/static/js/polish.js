(function () {
    document.documentElement.classList.add('js');
    var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches || location.hash === '#static';

    // Reveal on scroll
    var items = document.querySelectorAll('.reveal');
    if (reduce || !('IntersectionObserver' in window)) {
        items.forEach(function (el) { el.classList.add('in'); });
    } else {
        var io = new IntersectionObserver(function (entries) {
            entries.forEach(function (e) {
                if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
            });
        }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
        items.forEach(function (el, i) {
            // stagger siblings inside grids
            el.style.transitionDelay = ((i % 4) * 80) + 'ms';
            io.observe(el);
        });
    }

    // Count-up numbers (e.g. 500+, 10K+, 24/7 are left untouched when not plain numbers)
    document.querySelectorAll('[data-count]').forEach(function (el) {
        var end = parseFloat(el.getAttribute('data-count')), suffix = el.getAttribute('data-suffix') || '';
        if (reduce || isNaN(end)) { el.textContent = end + suffix; return; }
        var started = false;
        new IntersectionObserver(function (entries, obs) {
            if (!entries[0].isIntersecting || started) return;
            started = true; obs.disconnect();
            var t0 = performance.now(), dur = 1400;
            (function tick(t) {
                var p = Math.min((t - t0) / dur, 1), eased = 1 - Math.pow(1 - p, 3);
                el.textContent = Math.round(end * eased) + suffix;
                if (p < 1) requestAnimationFrame(tick);
            })(t0);
        }, { threshold: 0.6 }).observe(el);
    });

    // Header gets a glow once the page is scrolled
    var header = document.querySelector('header');
    function onScroll() { if (header) header.classList.toggle('scrolled', window.scrollY > 24); }
    window.addEventListener('scroll', onScroll, { passive: true }); onScroll();
})();
