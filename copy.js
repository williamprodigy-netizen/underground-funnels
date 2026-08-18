(function () {
  var ORDER = ["Headlines", "CTAs", "Guarantees", "Prices", "Proof", "Urgency"];
  var out = document.getElementById('out'), q = document.getElementById('q'),
      none = document.getElementById('none'), cnt = document.getElementById('count'),
      who = document.getElementById('who'), bank = 'all';

  var names = {};
  C.forEach(function (x) { names[x.w] = (names[x.w] || 0) + 1; });
  who.innerHTML = '<option value="all">All ' + Object.keys(names).length + ' funnels</option>' +
    Object.keys(names).sort().map(function (n) {
      return '<option value="' + n.replace(/"/g, '&quot;') + '">' + n + ' (' + names[n] + ')</option>';
    }).join('');

  var bc = {};
  C.forEach(function (x) { bc[x.b] = (bc[x.b] || 0) + 1; });
  document.getElementById('banks').innerHTML =
    '<button class="chip" data-b="all" aria-pressed="true">All<b>' + C.length + '</b></button>' +
    ORDER.filter(function (b) { return bc[b]; }).map(function (b) {
      return '<button class="chip" data-b="' + b + '" aria-pressed="false">' + b + '<b>' + bc[b] + '</b></button>';
    }).join('');

  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
    });
  }
  function hi(s, t) {
    if (!t) return esc(s);
    var i = s.toLowerCase().indexOf(t);
    if (i < 0) return esc(s);
    return esc(s.slice(0, i)) + '<mark>' + esc(s.slice(i, i + t.length)) + '</mark>' + esc(s.slice(i + t.length));
  }

  function render() {
    var t = q.value.trim().toLowerCase(), w = who.value;
    var rows = C.filter(function (x) {
      if (bank !== 'all' && x.b !== bank) return false;
      if (w !== 'all' && x.w !== w) return false;
      if (t && x.l.toLowerCase().indexOf(t) < 0 && x.w.toLowerCase().indexOf(t) < 0) return false;
      return true;
    });
    var by = {};
    rows.forEach(function (x) { (by[x.b] = by[x.b] || []).push(x); });
    out.innerHTML = ORDER.filter(function (b) { return by[b]; }).map(function (b) {
      return '<section class="grp"><div class="grp-h"><h2>' + b + '</h2><span>' + by[b].length + '</span></div>' +
        by[b].map(function (x) {
          return '<div class="ln"><p>' + hi(x.l, t) + '</p>' +
            '<div class="who"><b>' + esc(x.w) + '</b>' + esc(x.s) + '</div></div>';
        }).join('') + '</section>';
    }).join('');
    none.hidden = rows.length > 0;
    cnt.textContent = rows.length.toLocaleString() + ' lines';
  }

  q.addEventListener('input', render);
  who.addEventListener('change', render);
  document.getElementById('banks').addEventListener('click', function (e) {
    var b = e.target.closest('.chip');
    if (!b) return;
    [].slice.call(this.querySelectorAll('.chip')).forEach(function (o) { o.setAttribute('aria-pressed', 'false'); });
    b.setAttribute('aria-pressed', 'true');
    bank = b.dataset.b;
    render();
  });
  render();
})();
