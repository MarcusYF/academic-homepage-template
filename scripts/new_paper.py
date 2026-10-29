#!/usr/bin/env python3
"""Scaffold a new publication so every part of the site stays consistent.

Creates content/publications/<folder>/index.md and cite.bib from arXiv metadata (or a title and
authors you give), and prints the remaining manual steps (see docs/ADDING_A_PAPER.md).
Standard library only.

Examples:
  # a paper on arXiv, accepted at a venue
  python3 scripts/new_paper.py my-paper --arxiv 2603.01234v1 --venue ICML --year 2026
  # a working paper on arXiv
  python3 scripts/new_paper.py my-paper --arxiv 2603.01234v1 --working-paper
  # no public version yet
  python3 scripts/new_paper.py my-paper --title "A Title" --authors "Ann Lee; Jordan Lee" --year 2026 --working-paper
"""

import argparse
import datetime
import os
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
UA = "Mozilla/5.0 (new_paper scaffold; academic-homepage-template)"


def owner_name():
    """Your display name from data/authors/me.yaml; written as "me" in front matter so the site links your profile."""
    path = os.path.join(ROOT, "data", "authors", "me.yaml")
    in_name = False
    for line in open(path, encoding="utf-8"):
        if line.startswith("name:"):
            in_name = True
        elif in_name and re.match(r"\s+display:\s*(.+?)\s*$", line):
            return re.match(r"\s+display:\s*(.+?)\s*$", line).group(1).strip("'\"")
        elif in_name and not line.startswith(" "):
            in_name = False
    sys.exit("could not read name.display from data/authors/me.yaml")


OWNER = owner_name()


def arxiv_meta(arxiv_id):
    url = "https://export.arxiv.org/api/query?id_list=" + arxiv_id
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=60) as r:
        root = ET.fromstring(r.read())
    ns = {"a": "http://www.w3.org/2005/Atom"}
    e = root.find("a:entry", ns)
    if e is None or e.find("a:title", ns) is None:
        sys.exit(f"arXiv id {arxiv_id} not found")
    clean = lambda s: " ".join((s or "").split())
    return {
        "title": clean(e.find("a:title", ns).text),
        "authors": [clean(a.find("a:name", ns).text) for a in e.findall("a:author", ns)],
        "abstract": clean(e.find("a:summary", ns).text),
        "date": e.find("a:published", ns).text[:10],
    }


def venues():
    out = {}
    path = os.path.join(ROOT, "data", "venues.yaml")
    for line in open(path, encoding="utf-8"):
        m = re.match(r"^([A-Za-z]+):\s*(.+?)\s*$", line)
        if m:
            out[m.group(1)] = m.group(2)
    return out


def yq(s):
    """Single-quoted YAML scalar."""
    return "'" + s.replace("'", "''") + "'"


def bib_name(n):
    parts = n.split()
    return f"{parts[-1]}, {' '.join(parts[:-1])}" if len(parts) > 1 else n


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("folder", help="folder name under content/publications (lowercase, hyphens)")
    ap.add_argument("--arxiv", help="arXiv id with version, e.g. 2603.01234v1")
    ap.add_argument("--title")
    ap.add_argument("--authors", help='"First Last; First Last" (use when there is no arXiv version)')
    ap.add_argument("--venue", help="acronym from data/venues.yaml, e.g. ICML")
    ap.add_argument("--year", type=int)
    ap.add_argument("--date", help="YYYY-MM-DD used for ordering (default: arXiv date or today)")
    ap.add_argument("--working-paper", action="store_true")
    ap.add_argument("--note", action="append", default=[], help='extra line under the venue, e.g. "Oral"')
    a = ap.parse_args()

    folder = a.folder
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", folder):
        sys.exit("folder: use lowercase letters, digits and hyphens (it becomes the URL)")
    pub_dir = os.path.join(ROOT, "content", "publications", folder)
    if os.path.exists(pub_dir):
        sys.exit(f"{pub_dir} already exists")

    meta = arxiv_meta(a.arxiv) if a.arxiv else {"title": a.title, "authors": [], "abstract": "", "date": None}
    if a.title:
        meta["title"] = a.title
    if a.authors:
        meta["authors"] = [x.strip() for x in a.authors.split(";") if x.strip()]
    if not meta["title"] or not meta["authors"]:
        sys.exit("need --arxiv, or --title and --authors")
    date = a.date or meta["date"] or datetime.date.today().isoformat()
    year = a.year or int(date[:4])
    if not a.working_paper and not a.venue:
        sys.exit("give --venue (and --year) or --working-paper")
    vmap = venues()
    if a.venue and a.venue not in vmap:
        sys.exit(f"venue {a.venue!r} is not in data/venues.yaml; add its full name there first")

    arxiv_base = re.sub(r"v\d+$", "", a.arxiv) if a.arxiv else None
    venue_line = "Working paper." if a.working_paper else f"*{a.venue}*, {year}"
    short = "<br>" + venue_line + "".join(f"<br>{n}" for n in a.note)
    authors_fm = "\n".join(f"  - {'me' if n == OWNER else n}" for n in meta["authors"])
    abstract = meta["abstract"] or "TODO: abstract."
    links = []
    if arxiv_base:
        links.append(f"  - type: pdf\n    url: https://arxiv.org/pdf/{arxiv_base}")
    fm = f"""---
title: {yq(meta['title'])}
authors:
{authors_fm}
date: '{date}T00:00:00Z'
publishDate: '{date}T00:00:00Z'
publication_types: ['{'preprint' if a.working_paper else 'paper-conference'}']
publication: {yq(venue_line)}
publication_short: {yq(short)}
abstract: |
  {abstract}
summary: >-
  {abstract}
tags: []
featured: false
"""
    if arxiv_base:
        fm += f"hugoblox:\n  ids:\n    arxiv: {arxiv_base}\n"
    fm += "links:\n" + ("\n".join(links) if links else "  []") + "\n---\n"
    os.makedirs(pub_dir)
    open(os.path.join(pub_dir, "index.md"), "w", encoding="utf-8").write(fm)

    # cite.bib: no page numbers or edition ordinals; venue name + year only.
    first = meta["authors"][0].split()[-1].lower()
    word = next((w for w in re.findall(r"[a-z]+", meta["title"].lower()) if w not in {"a", "an", "the", "on", "of", "how", "is"}), "paper")
    key = f"{first}{year}{word}"
    fields = [("title", "{" + meta["title"] + "}"), ("author", "{" + " and ".join(bib_name(n) for n in meta["authors"]) + "}")]
    if a.working_paper:
        kind = "misc" if arxiv_base else "unpublished"
    else:
        kind = "inproceedings"
        fields.append(("booktitle", "{" + vmap[a.venue] + f" ({a.venue})" + "}"))
    fields.append(("year", "{" + str(year) + "}"))
    if arxiv_base:
        fields += [("eprint", "{" + arxiv_base + "}"), ("archivePrefix", "{arXiv}")]
    if a.working_paper:
        fields.append(("note", "{Working paper}"))
    w = max(len(k) for k, _ in fields)
    bib = f"@{kind}{{{key},\n" + ",\n".join(f"  {k.ljust(w)} = {v}" for k, v in fields) + "\n}\n"
    open(os.path.join(pub_dir, "cite.bib"), "w", encoding="utf-8").write(bib)
    created = [f"content/publications/{folder}/index.md", f"content/publications/{folder}/cite.bib"]

    print("Created:\n  " + "\n  ".join(created))
    print(f"""
Next (details in docs/ADDING_A_PAPER.md):
  1. Check the front matter: title, author order ("me" = {OWNER}), date, venue line, tags, extra links (code, slides, video).
  2. Homepage research section: add {{ id: {folder}, label: '<short label>' }} to one question in content/_index.md.
  3. Visual intro: build static/explainers/{folder}/index.html from the reference deck, then add the
     "Visual intro" link (first in links) and a card.png (see the docs).
  4. News: add an item to the news list in content/_index.md if it is an acceptance or release.
  5. Check: hugo server (or hugo --environment production) and look at the homepage and the paper page.""")


if __name__ == "__main__":
    main()
