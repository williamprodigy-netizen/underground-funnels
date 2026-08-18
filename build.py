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

NAV = [("index.html", "Overview"), ("boards.html", "Swipe boards"),
       ("ads.html", "Ad creatives")]


def shell(page, title, body, extra_head=""):
    nav = "".join(
        f'<a href="{h}"{" aria-current=\"page\"" if h == page else ""}>{html.escape(t)}</a>'
        for h, t in NAV)
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)} · Underground Funnels</title>
<link rel="icon" href="favicon.png"><link rel="stylesheet" href="style.css">{extra_head}
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
         (len(A), 'Ad creatives'), (len(AF), 'Ad formats')])}
</header>

<div class="cards">
  <a class="c" href="boards.html"><h3>Swipe boards</h3>
    <p>All {len(B)} funnels taken apart page by page. One line on what is worth stealing from each,
    then the live wired board.</p><span class="n">{len(B)} boards &rarr;</span></a>
  <a class="c" href="ads.html"><h3>Ad creatives</h3>
    <p>{len(A)} ads across {len(AF)} formats, ranked and tiered, each with its hook and a link to
    the footage in Drive.</p><span class="n">{len(AF)} formats &rarr;</span></a>

</div>

<div class="grp"><div class="grp-h"><h2>How to use it</h2></div>
<div class="e"><p class="steal">Start on <b>Swipe boards</b>. Each funnel opens with the one thing
worth taking from it &mdash; read those first, they are the point. Open the board only when you want
the wired canvas of their whole funnel.</p>
<p class="mdl" style="margin-top:14px">Ad creatives are segmented by format in Drive, so if you need a
green screen reference or a podcast-style ad, go straight to that folder.</p>
<p class="mdl" style="margin-top:12px">Each funnel&rsquo;s own copy bank &mdash; their headlines, CTAs,
guarantees and proof lines &mdash; sits inside that funnel&rsquo;s swipe site, on its <b>Copy bank</b>
tab. It is raw extraction: use it to find a phrasing, not to lift a page.</p></div></div>
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


def card(x):
    n = x['st']
    bits = []
    for v, l in ((n['pg'], 'pages'), (n['vid'], 'videos'), (n['tw'], 'words'),
                 (n['em'], 'emails'), (n['ads'], 'ads')):
        if v:
            t = f"{v/1000:.1f}k".replace('.0k', 'k') if v >= 1000 else str(v)
            bits.append(f'<b>{t}</b> {l}')
    steps_html = "".join(
        f'<a class="stp" href="{html.escape(st["u"])}" target="_blank" rel="noopener">'
        f'<b>{html.escape(st["l"])}</b><span>'
        f'{html.escape(st["u"].replace("https://","").replace("http://","").replace("www.","").split("?")[0])}'
        f'</span></a>' for st in x['steps'])
    det = (f'<details><summary><span class="car">&#9654;</span>Their funnel, step by step</summary>'
           f'<div class="body">{steps_html}</div></details>') if steps_html else ""
    return f"""<article class="fc" data-cat="{x['cat'] or 'other'}" data-new="{1 if x['new'] else 0}"
 data-q="{html.escape((x['c'] + ' ' + x['o'] + ' ' + (x['steal'] or '') + ' ' + x['model']).lower())}">
<div class="fc-h"><h3>{html.escape(x['c'])}</h3>{'<span class="new">New</span>' if x['new'] else ''}</div>
<div class="fc-o">{html.escape(x['o'])}</div>
{f'<p class="fc-s">{html.escape(x["steal"])}</p>' if x['steal'] else ''}
<div class="fc-m">{html.escape(x['model']).replace('-&gt;', '&rarr;').replace('->', '&rarr;')}</div>
<div class="fc-f"><div class="go">
<a class="btn p" href="{x['board_live']}" target="_blank" rel="noopener">Board</a>
<a class="btn" href="{x['live']}" target="_blank" rel="noopener">Swipe site</a></div>
{f'<div class="nums">{"".join(bits)}</div>' if bits else ''}
{det}</div></article>"""


TYPES = [("all", "Everything"), ("vsl", "VSL &rarr; call"), ("webinar", "Webinar"),
         ("challenge", "Challenge"), ("application", "Application"),
         ("event", "Event"), ("low_ticket", "Low ticket"), ("new", "New")]
counts = {}
for k, _ in TYPES:
    if k == "all":
        counts[k] = len(B)
    elif k == "new":
        counts[k] = sum(1 for x in B if x['new'])
    else:
        counts[k] = sum(1 for x in B if (x['cat'] or 'other') == k)
tabs = "".join(
    f'<button class="tab" data-f="{k}" aria-pressed="{"true" if k=="all" else "false"}">{t}'
    f'<b>{counts[k]}</b></button>' for k, t in TYPES if counts[k])

secs = ""
for k, t in GROUPS:
    rows = sorted([x for x in B if (x['cat'] or '') == k],
                  key=lambda y: (0 if y['steal'] else 1, y['c']))
    if not rows:
        continue
    secs += (f'<section class="grp" data-sec="{k or "other"}" id="{slug(t)}">'
             f'<div class="grp-h"><h2>{html.escape(t)}</h2><span>{len(rows)}</span></div>'
             f'<div class="fgrid">' + "".join(card(x) for x in rows) + '</div></section>')

boards = f"""
<header>
  <div class="kick">Underground Funnels</div>
  <h1>Swipe Boards</h1>
  <p class="sub">Pick a funnel type, then pick a funnel. Each one opens with the single thing worth
  stealing from it.</p>
</header>
<div class="bar"><div class="bar-in">
  <input type="search" id="q" placeholder="Search 38 funnels&hellip;" aria-label="Search funnels">
</div><div class="tabs-row">{tabs}</div></div>
<div id="hits"></div>
{secs}
<div class="none" id="none" hidden>Nothing matches that.</div>
<script src="boards.js"></script>
"""
open(os.path.join(HERE, "boards.html"), "w").write(shell("boards.html", "Swipe Boards", boards))

# ---------------------------------------------------------------- ads
import json as _json

BLURB = {
 "01 GREEN SCREEN": "Presenter in front of a keyed background, usually reacting to a screenshot or headline.",
 "02 PODCAST": "Two people at mics. Borrowed credibility and a conversation you are overhearing.",
 "03 TALKING HEAD + BROLL": "Straight to camera, cut with footage that proves each claim.",
 "04 WHITEBOARD": "Drawing the mechanism while explaining it. Slow, high-trust, teaches to sell.",
 "05 ZOOM ROOM": "Screen-share or call recording. Feels like being shown something private.",
 "06 TESTIMONIAL": "The customer does the selling. Named person, specific number.",
 "07 BREAKING NEWS + 3RD PERSON": "Framed as a report about the offer rather than an ad for it.",
 "08 INTERVIEW STYLE": "Question and answer. The interviewer asks the objection out loud.",
 "09 TWIN": "Same person twice on screen, arguing both sides of the decision.",
 "10 COMEDY + SKITS": "Sketch first, offer second. Buys attention before it asks for it.",
 "11 LIFESTYLE": "The outcome shown, not described. Sells the after, never the mechanism.",
 "12 OUTDOORS + WALKING": "Walk-and-talk. Reads as unscripted and off the cuff.",
 "13 BROLL VOICE OVER": "No presenter at all. Voice over footage, cheapest format to produce.",
}

fmt_cards, fmt_secs = "", ""
for f in sorted(AF):
    rows = sorted([a for a in A if a['f'] == f], key=lambda y: y['r'])
    if not rows:
        continue
    fid, num, label = AF[f], f[:2], f[3:].title()
    stier = sum(1 for a in rows if a['t'] == 'S')
    avg = round(sum(a['d'] for a in rows) / len(rows))
    fmt_cards += (
        f'<button class="fmtc" data-f="{html.escape(f)}">'
        f'<span class="fnum">{num}</span><h3>{html.escape(label)}</h3>'
        f'<p>{html.escape(BLURB.get(f, ""))}</p>'
        f'<span class="fmeta">{len(rows)} ads &middot; {stier} S-tier &middot; ~{avg}s avg</span></button>')
    ads = "".join(
        f'<div class="ad" data-t="{html.escape(a["t"])}" '
        f'data-q="{html.escape((a["h"] + " " + a["b"]).lower())}">'
        f'<span class="tier {html.escape(a["t"])}">{html.escape(a["t"])}</span>'
        f'<p><a href="{html.escape(a["u"])}" target="_blank" rel="noopener">{html.escape(a["h"])}</a></p>'
        f'<div class="meta"><b>{html.escape(a["b"])}</b>{a["d"]}s</div></div>' for a in rows)
    fmt_secs += (
        f'<section class="fmt" data-f="{html.escape(f)}" hidden>'
        f'<div class="fmt-h"><h2><span class="fnum">{num}</span>{html.escape(label)}</h2>'
        f'<a class="dl" href="https://drive.google.com/drive/folders/{fid}" target="_blank" '
        f'rel="noopener">Footage in Drive &rarr;</a></div>'
        f'<p class="fmt-b">{html.escape(BLURB.get(f, ""))}</p>{ads}</section>')

ads_page = f"""
<header>
  <div class="kick">Underground Funnels</div>
  <h1>Ad Creatives</h1>
  <p class="sub">{len(A)} ads sorted into {len(AF)} formats. Pick a format to see its ten, or search
  every hook at once.</p>
  {figs([(len(A), 'Ads'), (len(AF), 'Formats'), (len(set(a['b'] for a in A)), 'Brands'),
         (sum(1 for a in A if a['t'] == 'S'), 'S tier')])}
</header>

<div class="bar"><div class="bar-in">
  <input type="search" id="q" placeholder="Search every hook&hellip;" aria-label="Search hooks">
  <button class="tab" data-t="all" aria-pressed="true">All tiers</button>
  <button class="tab" data-t="S" aria-pressed="false">S</button>
  <button class="tab" data-t="A" aria-pressed="false">A</button>
  <button class="tab" data-t="B" aria-pressed="false">B</button>
  <button class="tab back" id="back" hidden>&larr; All formats</button>
</div></div>

<div id="lib"><div class="grp"><div class="grp-h"><h2>The library in Drive</h2></div>
<div class="e"><p class="steal">All footage sits in <b>AD FORMAT LIBRARY</b>, in the same {len(AF)}
folders below. Tier is our read: <b>S</b> copy now, <b>A</b> worth a test, <b>B</b> reference.</p>
<div class="go"><a class="btn p" href="{LIB_URL}" target="_blank" rel="noopener">Open the library in Drive</a></div></div></div>
<div class="fmtgrid">{fmt_cards}</div></div>

<div id="hits" hidden></div>
{fmt_secs}
<div class="none" id="none" hidden>No hook matches that.</div>
<script src="ads.js"></script>
"""
open(os.path.join(HERE, "ads.html"), "w").write(shell("ads.html", "Ad Creatives", ads_page))
print("built index.html, boards.html, ads.html")
