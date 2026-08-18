(function () {
  var q = document.getElementById('q'),
      none = document.getElementById('none'),
      hits = document.getElementById('hits'),
      tabs = [].slice.call(document.querySelectorAll('.tab')),
      cards = [].slice.call(document.querySelectorAll('.fc')),
      secs = [].slice.call(document.querySelectorAll('.grp[data-sec]')),
      filter = 'all';

  function render() {
    var t = q.value.trim().toLowerCase(), shown = 0;
    cards.forEach(function (c) {
      var okCat = filter === 'all' ||
                  (filter === 'new' ? c.dataset.new === '1' : c.dataset.cat === filter);
      var okQ = !t || c.dataset.q.indexOf(t) > -1;
      var show = okCat && okQ;
      c.hidden = !show;
      if (show) shown++;
    });
    secs.forEach(function (s) {
      var any = [].slice.call(s.querySelectorAll('.fc')).some(function (c) { return !c.hidden; });
      s.hidden = !any;
    });
    none.hidden = shown > 0;
    hits.textContent = shown === cards.length
      ? cards.length + ' funnels'
      : shown + ' of ' + cards.length + ' funnels';
  }

  tabs.forEach(function (b) {
    b.addEventListener('click', function () {
      tabs.forEach(function (o) { o.setAttribute('aria-pressed', 'false'); });
      b.setAttribute('aria-pressed', 'true');
      filter = b.dataset.f;
      render();
      window.scrollTo({ top: document.querySelector('.bar').offsetTop - 8, behavior: 'smooth' });
    });
  });
  q.addEventListener('input', render);
  render();
})();
