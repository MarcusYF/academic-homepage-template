# Adding a new paper

A paper touches several parts of the site. This checklist keeps them consistent. Step 1 is scripted;
the rest are short manual edits.

## 1. Scaffold the publication

```bash
# on arXiv and accepted at a venue (the acronym should exist in data/venues.yaml)
python3 scripts/new_paper.py <folder> --arxiv 2603.01234v1 --venue ICML --year 2026
# on arXiv, not yet accepted
python3 scripts/new_paper.py <folder> --arxiv 2603.01234v1 --working-paper
# no public version yet
python3 scripts/new_paper.py <folder> --title "Title" --authors "Ann Lee; Jordan Lee" --year 2026 --working-paper
```

- `<folder>`: lowercase letters, digits and hyphens. It becomes `publications/<folder>/`.
- The script writes `content/publications/<folder>/index.md` and `cite.bib`. With `--arxiv` it reads
  the title, authors, abstract and date from the arXiv API. Your own name (from `name.display` in
  `data/authors/me.yaml`) becomes `me`, which links to your profile.
- It uses only the Python standard library.

Then check the front matter by hand:

- **Title and author order.** Coauthor links come from `data/coauthor_links.json`; add new coauthors there
  (`kind: homepage`, `scholar` or `scholar-search`).
- **`date`** sets the order in the publication list. The homepage shows the newest ones (`show` in the
  `publication-list` block).
- **`publication_short`:** `<br>*ICML*, 2026`, plus `<br>…` parts for notes such as "Oral" or a journal
  version. The first part becomes the venue pill, and later parts become notes.
- **`links`:** `pdf`, `code`, `slides`, `video`, `dataset`, `poster` or `custom` with a `label` and an
  `icon`. With an arXiv id (`hugoblox.ids.arxiv`) an "arXiv" link is added automatically.
- **`tags`:** optional.

## 2. Citation data (automatic once step 1 is done)

- **`cite.bib`** powers the **Cite** button, which copies the BibTeX. The script writes the venue name and
  year only; update it when the proceedings appear.
- **Google Scholar tags** (`citation_*` meta tags) are generated for pages that have a PDF link or an arXiv
  id (`layouts/_partials/hooks/head-end/scholar-meta.html`). Working papers without a public version get
  none, so Scholar does not create empty citation-only entries. A new venue acronym needs one line in
  `data/venues.yaml` for the full conference name.

## 3. Homepage research section

Add the paper to one of the questions in `content/_index.md` (`research-overview` → `questions` → `papers`):

```yaml
- { id: <folder>, label: 'Short label' }
```

The chip links to the paper page and shows its year.

## 4. Visual intro (optional animated explainer)

A visual intro is a short, animated, step-by-step HTML deck that explains a paper to a broad audience.
Decks are plain HTML files in `static/explainers/<folder>/index.html`; no build step is needed. They share
the engine in `static/explainers/_deck/`:

- `deck.css`: colours, layout, animations and dark mode.
- `deck.js`: step builds, keyboard, swipe and button navigation, slide dots, deep links (`#3`).
- `icons.svg`: the line icons (`person`, `creator`, `platform`, `model`, `robot`, `doc`, `search`, ...).
- `fonts/`: Computer Modern, under the SIL Open Font Licence.

1. Copy `static/explainers/sample-paper/index.html` to `static/explainers/<folder>/index.html`.
   Keep the engine paths relative (`../_deck/...`) so the deck also works when the site lives under a
   sub-path, such as a GitHub Pages project site.
2. Write 6–9 slides: title → setting → the problem → 2–4 results (one idea each) → takeaways with links.
3. Build each slide with `data-step="1"`, `data-step="2"`, ... Animation helpers: `dk-rise` (fade up),
   `dk-draw` (draw a line), `dk-grow` (grow a bar). `data-dim="N"` dims an item once step N arrives.
4. Colours keep one meaning in every deck: people blue (`t-people`), creators orange (`t-creator`), the
   system purple (`t-platform`), good outcomes green (`t-good`), harm red (`t-bad`), extra series teal
   (`t-teal`). Use `s-*` for strokes and `f-*` / `f-*-soft` for fills; dark mode then works by itself.
5. Mark illustrations and approximate values as such. Take every number from the paper.
6. Optional "Ask about this slide" button: `<body data-ask="<url>">` adds a button that opens your Q&A page
   with `#question=...` appended.
7. Render the share card: `python3 scripts/explainer_card.py <folder>` writes `card.png` (needs Google
   Chrome). Point the deck's `og:image` at its absolute URL.
8. Add the link as the **first** entry in the publication's `links`:

   ```yaml
   - type: custom
     label: Visual intro
     icon: hero/play-circle
     url: explainers/<folder>/
   ```

9. Check every slide in light and dark mode and at phone width. In the browser console, `Deck.go(i)` jumps
   to a slide and `Deck.next()` steps through it.

## 5. News

If the paper is an acceptance or a release, add an item at the top of the news list in `content/_index.md`
(`date`, `icon`, `text`).

## 6. Check

```bash
hugo server            # live preview at http://localhost:1313/
```

Look at the homepage, the publication list and the paper page. A monthly GitHub Action
(`.github/workflows/link-check.yml`) opens an issue if any link on the live site breaks.
