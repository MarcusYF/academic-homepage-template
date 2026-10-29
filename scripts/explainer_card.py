#!/usr/bin/env python3
"""Render the social-share card (1200x630 PNG) for a visual-intro deck.

Reads the title, subtitle and author line from the deck's first slide in
static/explainers/<slug>/index.html and writes static/explainers/<slug>/card.png
with headless Chrome. The deck's <head> should point og:image at card.png.

The site label at the bottom right is the host of baseURL in config/_default/hugo.yaml
(override with SITE_LABEL=...). Needs Google Chrome (or set CHROME=/path/to/chrome).

Usage: python3 scripts/explainer_card.py <slug> [<slug> ...]
"""

import html
import os
import re
import subprocess
import sys
import tempfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def site_label():
    if os.environ.get("SITE_LABEL"):
        return os.environ["SITE_LABEL"]
    try:
        text = open(os.path.join(ROOT, "config", "_default", "hugo.yaml"), encoding="utf-8").read()
        m = re.search(r"^baseURL:\s*['\"]?https?://([^/'\"]+)", text, re.M)
        return m.group(1).removeprefix("www.") if m else ""
    except OSError:
        return ""


CHROME = os.environ.get("CHROME", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")


def text(fragment):
    fragment = re.sub(r"<br\s*/?>", " ", fragment)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", fragment)).strip()


def card(slug):
    deck = os.path.join(ROOT, "static", "explainers", slug, "index.html")
    s = open(deck, encoding="utf-8").read()
    first = s[s.index('<section class="dk-slide"'):]
    first = first[: first.index("</section>")]
    title = text(re.search(r'<h1[^>]*class="[^"]*dk-h[^"]*"[^>]*>(.*?)</h1>', first, re.S).group(1))
    subs = [text(x) for x in re.findall(r'<p class="dk-sub"[^>]*>(.*?)</p>', first, re.S)]
    sub = subs[-1] if subs else ""
    if len(subs) > 1:  # a separate subtitle line belongs to the title
        title = f"{title}: {subs[0]}"
    meta = re.search(r'<p class="dk-meta">(.*?)</p>', first, re.S)
    meta = text(meta.group(1)) if meta else ""
    fonts = "file://" + os.path.join(ROOT, "static", "explainers", "_deck", "fonts") + "/"
    icon = "file://" + os.path.join(ROOT, "assets", "media", "icon.svg")
    size = 56 if len(title) < 70 else 48
    page = f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:"CMU Serif";src:url("{fonts}cmunrm.woff")}}
html,body{{margin:0}} body{{width:1200px;height:630px;background:#fff;font-family:"CMU Serif",Georgia,serif;color:#222;position:relative;overflow:hidden}}
.k{{position:absolute;left:70px;top:54px;display:flex;align-items:center;gap:14px;font:600 20px/1 Inter,system-ui,sans-serif;letter-spacing:.14em;text-transform:uppercase;color:#8a8a8a}}
.k img{{width:34px;height:34px}}
.c{{position:absolute;left:70px;right:70px;top:150px}}
h1{{margin:0;font-weight:400;font-size:{size}px;line-height:1.12}}
.r{{width:70px;height:3px;background:#b8913a;margin:34px 0}}
.s{{font-size:28px;line-height:1.35;color:#6b6b6b;max-width:980px}}
.m{{position:absolute;left:70px;right:70px;bottom:52px;display:flex;justify-content:space-between;gap:24px;font:400 19px/1.3 Inter,system-ui,sans-serif;color:#8a8a8a}}
.m span{{max-width:840px}} .m b{{color:#6b5a9e;font-weight:600;align-self:flex-end}}
</style></head><body>
<div class="k"><img src="{icon}">Visual introduction</div>
<div class="c"><h1>{html.escape(title)}</h1><div class="r"></div><div class="s">{html.escape(sub)}</div></div>
<div class="m"><span>{html.escape(meta)}</span><b>{html.escape(site_label())}</b></div>
</body></html>"""
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
        f.write(page)
    out = os.path.join(ROOT, "static", "explainers", slug, "card.png")
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--allow-file-access-from-files",
                    "--virtual-time-budget=3000", "--window-size=1200,630", f"--screenshot={out}", "file://" + f.name],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.unlink(f.name)
    print(out)


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        sys.exit(__doc__)
    for slug in sys.argv[1:]:
        card(slug)
