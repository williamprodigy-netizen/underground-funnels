(function () {
  var q = document.getElementById('q'),
      lib = document.getElementById('lib'),
      hits = document.getElementById('hits'),
      none = document.getElementById('none'),
      back = document.getElementById('back'),
      secs = [].slice.call(document.querySelectorAll('section.fmt')),
      cards = [].slice.call(document.querySelectorAll('.fmtc')),
      tiers = [].slice.call(document.querySelectorAll('.tab[data-t]')),
      fmt = null, tier = 'all';

  function ads() { return [].slice.call(document.querySelectorAll('.ad')); }

  function render() {
    var t = q.value.trim().toLowerCase();
    var searching = t.length > 0;
    var shown = 0;

    ads().forEach(function (a) {
      var sec = a.closest('section.fmt');
      var inScope = searching || (fmt && sec && sec.dataset.f === fmt);
      var okT = tier === 'all' || a.dataset.t === tier;
      var okQ = !searching || a.dataset.q.indexOf(t) > -1;
      var show = inScope && okT && okQ;
      a.hidden = !show;
      if (show) shown++;
    });

    secs.forEach(function (s) {
      var inScope = searching || (fmt && s.dataset.f === fmt);
      var any = [].slice.call(s.querySelectorAll('.ad')).some(function (a) { return !a.hidden; });
      s.hidden = !(inScope && any);
    });

    var browsing = !searching && !fmt;
    lib.hidden = !browsing;
    back.hidden = browsing;
    hits.hidden = browsing;
    if (!browsing) {
      hits.textContent = shown + (shown === 1 ? ' ad' : ' ads');
    }
    none.hidden = browsing || shown > 0;
  }

  cards.forEach(function (c) {
    c.addEventListener('click', function () {
      fmt = c.dataset.f;
      q.value = '';
      render();
      window.scrollTo({ top: document.querySelector('.bar').offsetTop - 8, behavior: 'smooth' });
    });
  });

  back.addEventListener('click', function () {
    fmt = null;
    q.value = '';
    tier = 'all';
    tiers.forEach(function (o) { o.setAttribute('aria-pressed', o.dataset.t === 'all' ? 'true' : 'false'); });
    render();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });

  tiers.forEach(function (b) {
    b.addEventListener('click', function () {
      tiers.forEach(function (o) { o.setAttribute('aria-pressed', 'false'); });
      b.setAttribute('aria-pressed', 'true');
      tier = b.dataset.t;
      if (tier !== 'all' && !fmt && !q.value) { fmt = null; }
      render();
    });
  });

  q.addEventListener('input', render);
  render();
})();
