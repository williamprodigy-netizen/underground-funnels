#!/usr/bin/env python3
"""Build the Underground Funnels hub: landing, boards, ads, copy."""
import json, os, html

HERE = os.path.dirname(os.path.abspath(__file__))
B = json.loads(open('/tmp/hub.js').read()[len('const B = '):].strip().rstrip(';'))
_a = open('/tmp/ads.js').read()
A = json.loads(_a.split('const AF')[0][len('const A = '):].strip().rstrip(';'))
AF = json.loads(_a.split('const AF = ')[1].strip().rstrip(';'))
C = json.loads(open('/tmp/copybank2.js').read()[len('const C = '):].strip().rstrip(';'))

LIB_URL = "https://drive.google.com/drive/folders/15UP97tzwNZcZ00ugpnIkz17XFwDtkRqn"
SOPHRON = "https://drive.google.com/drive/folders/1euhWFBWG8G7Nql_AzI3lL_AR4qDQ59QZ"

NAV = [("index.html", "Overview"), ("boards.html", "Swipe boards"),
       ("ads.html", "Ad creatives"), ("copy.html", "Copy bank")]


def shell(page, title, body, extra_head=""):
    nav = "".join(
        f'<a href="{h}"{" aria-current=\"page\"" if h == page else ""}>{html.escape(t)}</a>'
        for h, t in NAV)
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)} · Underground Funnels</title>
<link rel="stylesheet" href="style.css">{extra_head}
</head><body>
<div class="w">
<nav class="top">{nav}</nav>
{body}
<footer>
Underground Funnels &middot; competitor research, captured read-only.<br>
Every claim is the operator&rsquo;s own. Captured through 18 August 2026.
</footer>
</div></body></html>"""


def figs(items):
    return '<div class="figs">' + "".join(
        f'<div class="fig"><b>{v}</b><span>{html.escape(l)}</span></div>' for v, l in items) + '</div>'


# ---------------------------------------------------------------- landing
tw = sum(x['st']['tw'] for x in B)
steps = sum(len(x['steps']) for x in B)
land = f"""
<header>
  <div class="kick">Underground Funnels</div>
  <h1>The Swipe Board</h1>
  <p class="sub">Every competitor funnel we have taken apart, every ad format worth copying, and every
  line of their copy &mdash; in one place, live, for the team.</p>
  {figs([(len(B), 'Funnels'), (steps, 'Pages mapped'), (f'{round(tw/1000)}k', 'Words transcribed'),
         (len(A), 'Ad creatives'), (f'{len(C):,}', 'Copy lines')])}
</header>

<div class="cards">
  <a class="c" href="boards.html"><h3>Swipe boards</h3>
    <p>All {len(B)} funnels taken apart page by page. One line on what is worth stealing from each,
    then the live wired board.</p><span class="n">{len(B)} boards &rarr;</span></a>
  <a class="c" href="ads.html"><h3>Ad creatives</h3>
    <p>{len(A)} ads across {len(AF)} formats, ranked and tiered, each with its hook and a link to
    the footage in Drive.</p><span class="n">{len(AF)} formats &rarr;</span></a>
  <a class="c" href="copy.html"><h3>Copy bank</h3>
    <p>Headlines, CTAs, guarantees, prices and proof lines pulled straight off their pages.
    Searchable.</p><span class="n">{len(C):,} lines &rarr;</span></a>
</div>

<div class="grp"><div class="grp-h"><h2>How to use it</h2></div>
<div class="e"><p class="steal">Start on <b>Swipe boards</b>. Each funnel opens with the one thing
worth taking from it &mdash; read those first, they are the point. Open the board only when you want
the wired canvas of their whole funnel.</p>
<p class="mdl" style="margin-top:14px">Ad creatives are segmented by format in Drive, so if you need a
green screen reference or a podcast-style ad, go straight to that folder. The copy bank is raw
extraction &mdash; use it to find a phrasing, not to lift a whole page.</p></div></div>
"""
open(os.path.join(HERE, "index.html"), "w").write(shell("index.html", "The Swipe Board", land))

# ---------------------------------------------------------------- boards
GROUPS = [("vsl", "VSL to a call"), ("webinar", "Webinar"), ("challenge", "Challenge"),
          ("application", "Straight to application"), ("event", "Event"),
          ("low_ticket", "Low ticket"), ("", "Other")]


def board_entry(x):
    steps_html = "".join(
        f'<a class="stp" href="{html.escape(s["u"])}" target="_blank" rel="noopener">'
        f'<b>{html.escape(s["l"])}</b><span>'
        f'{html.escape(s["u"].replace("https://","").replace("http://","").replace("www.","").split("?")[0])}'
        f'</span></a>' for s in x['steps'])
    n = x['st']
    bits = []
    for v, l in ((n['pg'], 'pages'), (n['vid'], 'videos'), (n['tw'], 'words'),
                 (n['em'], 'emails'), (n['ads'], 'ads')):
        if v:
            s = f"{v/1000:.1f}k".replace('.0k', 'k') if v >= 1000 else str(v)
            bits.append(f'<b>{s}</b> {l}')
    inner = ""
    if steps_html:
        inner += f'<span class="lbl">Their live funnel</span>{steps_html}'
    if bits:
        inner += f'<div class="nums">{"".join(bits)}</div>'
    det = (f'<details><summary><span class="car">&#9654;</span>Their funnel, step by step</summary>'
           f'<div class="body">{inner}</div></details>') if inner else ""
    return f"""<article class="e" id="{__import__('re').sub(r'[^a-z0-9]+','-',x['c'].lower()).strip('-')}">
<div class="e-h"><h3><a href="{x['board_live']}" target="_blank" rel="noopener">{html.escape(x['c'])}</a></h3>
{'<span class="new">New</span>' if x['new'] else ''}</div>
{f'<div class="e-o">{html.escape(x["o"])}</div>' if x['o'] else ''}
{f'<p class="steal">{html.escape(x["steal"])}</p>' if x['steal'] else ''}
{f'<div class="mdl">{html.escape(x["model"]).replace("-&gt;","&rarr;").replace("->","&rarr;")}</div>' if x['model'] else ''}
<div class="go"><a class="btn p" href="{x['board_live']}" target="_blank" rel="noopener">Open the board</a>
<a class="btn" href="{x['live']}" target="_blank" rel="noopener">Full swipe site</a></div>
{det}</article>"""


def slug(n):
    import re as _r
    return _r.sub(r"[^a-z0-9]+", "-", n.lower()).strip("-")


toc = ""
secs = ""
for k, t in GROUPS:
    rows = sorted([x for x in B if (x['cat'] or '') == k],
                  key=lambda y: (0 if y['steal'] else 1, y['c']))
    if not rows:
        continue
    gid = slug(t)
    toc += (f'<div class="toc-g"><h3>{html.escape(t)} <em>{len(rows)}</em></h3><ol>' +
            "".join(f'<li><a href="#{slug(x["c"])}">{html.escape(x["c"])}</a>'
                    f'<span>{html.escape((x["steal"] or x["o"] or "")[:64])}</span></li>' for x in rows) +
            '</ol></div>')
    secs += (f'<section class="grp" id="{gid}"><div class="grp-h"><h2>{html.escape(t)}</h2>'
             f'<span>{len(rows)}</span></div>' + "".join(board_entry(x) for x in rows) + '</section>')

boards = f"""
<header>
  <div class="kick">Underground Funnels</div>
  <h1>Swipe Boards</h1>
  <p class="sub">The competitor funnels we have taken apart page by page &mdash; what each one does
  that is worth stealing, and the wired board behind it.</p>
  {figs([(len(B), 'Funnels'), (steps, 'Pages mapped'), (f'{round(tw/1000)}k', 'Words')])}
</header>
<section class="toc"><div class="grp-h"><h2>Contents</h2><span>{len(B)} funnels</span></div>
<div class="toc-w">{toc}</div></section>
{secs}
"""
open(os.path.join(HERE, "boards.html"), "w").write(shell("boards.html", "Swipe Boards", boards))

# ---------------------------------------------------------------- ads
fmt_secs = ""
for f in sorted(AF):
    rows = sorted([a for a in A if a['f'] == f], key=lambda y: y['r'])
    if not rows:
        continue
    fid = AF[f]
    ads = "".join(
        f'<div class="ad"><span class="tier {html.escape(a["t"])}">{html.escape(a["t"])}</span>'
        f'<p><a href="{html.escape(a["u"])}" target="_blank" rel="noopener">{html.escape(a["h"])}</a></p>'
        f'<div class="meta"><b>{html.escape(a["b"])}</b>{a["d"]}s</div></div>' for a in rows)
    fmt_secs += (f'<section class="fmt" id="f{f[:2]}"><div class="fmt-h"><h2>{html.escape(f)}</h2>'
                 f'<a class="dl" href="https://drive.google.com/drive/folders/{fid}" target="_blank" '
                 f'rel="noopener">Footage in Drive &rarr;</a></div>{ads}</section>')

jump = " ".join(f'<a class="btn" href="#f{f[:2]}">{html.escape(f[3:].title())}</a>' for f in sorted(AF))
ads_page = f"""
<header>
  <div class="kick">Underground Funnels</div>
  <h1>Ad Creatives</h1>
  <p class="sub">{len(A)} ads across {len(AF)} formats, tiered and ranked. The hook is the line that
  opens it &mdash; click any hook to see the ad, or jump to the footage in Drive.</p>
  {figs([(len(A), 'Ads'), (len(AF), 'Formats'), (len(set(a['b'] for a in A)), 'Brands'),
         (sum(1 for a in A if a['t'] == 'S'), 'S tier')])}
  <div class="warn"><b>Tier is our read, not theirs.</b> S is a format worth copying now, A is worth a
  test, B is reference. Every ad links out to Foreplay for the full creative.</div>
</header>
<div class="grp"><div class="grp-h"><h2>The library in Drive</h2></div>
<div class="e"><p class="steal">All footage lives in <b>AD FORMAT LIBRARY</b>, segmented into the
same {len(AF)} folders you see below.</p>
<div class="go"><a class="btn p" href="{LIB_URL}" target="_blank" rel="noopener">Open AD FORMAT LIBRARY</a>
<a class="btn" href="{SOPHRON}" target="_blank" rel="noopener">63 Ad Format Swipe File (Sophron)</a></div></div></div>
<div class="grp"><div class="grp-h"><h2>Jump to a format</h2></div>
<div class="e"><div class="go">{jump}</div></div></div>
{fmt_secs}
"""
open(os.path.join(HERE, "ads.html"), "w").write(shell("ads.html", "Ad Creatives", ads_page))

# ---------------------------------------------------------------- copy
copy_page = f"""
<header>
  <div class="kick">Underground Funnels</div>
  <h1>Copy Bank</h1>
  <p class="sub">Every headline, CTA, price, guarantee and proof line pulled off the captured pages of
  27 competitor funnels &mdash; searchable, with the page it came from.</p>
  <div class="warn"><b>Read this first.</b> These lines are machine-extracted from their live pages,
  unedited. Nothing is curated or approved &mdash; the guarantees bank in particular mixes real offers
  with legal disclaimers. Raw ore, not a finished swipe.</div>
</header>
<div class="bar"><div class="bar-in">
  <input type="search" id="q" placeholder="Search every line&hellip;" aria-label="Search copy">
  <select id="who" aria-label="Filter by competitor"></select>
</div><div class="bar-in" style="margin-top:9px" id="banks"></div></div>
<div id="count"></div><main id="out"></main>
<div class="none" id="none" hidden>Nothing matches that.</div>
<script>const C = {json.dumps(C, ensure_ascii=False)};</script>
<script src="copy.js"></script>
"""
open(os.path.join(HERE, "copy.html"), "w").write(shell("copy.html", "Copy Bank", copy_page))
print("built index.html, boards.html, ads.html, copy.html")
