# Coleção Editorial Premium Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild the ten soap-offer bonuses as substantial premium workbooks with original art direction and publish real inside-page demonstrations on the sales page.

**Architecture:** Content is stored as structured Python data, rendered through a shared editorial engine with ten theme configurations. Original image assets are generated once into a curated visual library and reused in covers, section openers, examples, and website previews. Automated tests enforce page counts, content depth, output integrity, and site references; visual QA renders every page to PNG.

**Tech Stack:** Python, ReportLab, Pillow, pypdf, Poppler, static HTML/CSS/JavaScript, image generation.

**Spec:** `docs/superpowers/specs/2026-10-04-colecao-premium-bonus-sabonetes-design.md`

## Global Constraints

- Produce ten separate A4 PDFs within the page-count ranges defined by the spec.
- Use original generated imagery plus existing product photography.
- Keep prose blocks below 90 words and favor visual recipes, cards, worksheets, examples, and diagrams.
- Do not promise sales, income, regulatory approval, or guaranteed results.
- Render and inspect every page before publishing.
- Preserve mobile site usability and keep purchase CTAs pointing to `#comprar` until checkout URLs exist.

---

### Task 1: Create the editorial system and original image library

**Files:**
- Create: `bonus_editorial/themes.py`
- Create: `bonus_editorial/components.py`
- Create: `assets/bonus-premium/` image library
- Test: `tests/test_editorial_system.py`

**Interfaces:** Produces `THEMES`, reusable page components, and at least twenty original JPG/PNG visuals grouped by volume.

- [ ] Write a failing test asserting ten unique themes and at least two original visuals per volume.
- [ ] Run `python -m unittest tests/test_editorial_system.py` and verify the missing-module failure.
- [ ] Generate editorial still-life, packaging, flat-lay, label, planner, pricing, photography, and collection imagery; implement cover, opener, card, worksheet, table, checklist, quote, and footer components.
- [ ] Re-run the test and verify it passes.
- [ ] Commit with `git commit -m "feat: add soap bonus editorial system"`.

### Task 2: Author volumes 1-5

**Files:**
- Create: `bonus_editorial/content/volume_01_fornecedores.py`
- Create: `bonus_editorial/content/volume_02_precificacao.py`
- Create: `bonus_editorial/content/volume_03_economia.py`
- Create: `bonus_editorial/content/volume_04_rotulos.py`
- Create: `bonus_editorial/content/volume_05_primeira_venda.py`
- Test: `tests/test_bonus_content.py`

**Interfaces:** Each module exports `BOOK` with title, theme, sections, examples, tools, and page-target metadata.

- [ ] Write failing tests requiring five `BOOK` objects, spec-aligned sections, at least two concrete examples, and one usable worksheet per volume.
- [ ] Run `python -m unittest tests/test_bonus_content.py` and verify import failures.
- [ ] Author the five complete workbooks with the content and visual formats specified in the design.
- [ ] Re-run the content tests and verify they pass.
- [ ] Commit with `git commit -m "feat: author premium soap bonus volumes one to five"`.

### Task 3: Author volumes 6-10

**Files:**
- Create: `bonus_editorial/content/volume_06_colecoes.py`
- Create: `bonus_editorial/content/volume_07_nomes.py`
- Create: `bonus_editorial/content/volume_08_vitrine.py`
- Create: `bonus_editorial/content/volume_09_tags.py`
- Create: `bonus_editorial/content/volume_10_calendario.py`
- Modify: `tests/test_bonus_content.py`

**Interfaces:** Adds five `BOOK` objects, exactly 30 collection cards, 100 names, 30 adaptable sales texts, printable tag models, and twelve monthly campaign maps.

- [ ] Extend the failing tests with exact counts for collections, names, sales texts, tag models, and monthly maps.
- [ ] Run `python -m unittest tests/test_bonus_content.py` and verify count/import failures.
- [ ] Author volumes 6-10 with examples, visual references, worksheets, and action pages.
- [ ] Re-run the tests and verify they pass.
- [ ] Commit with `git commit -m "feat: author premium soap bonus volumes six to ten"`.

### Task 4: Render and validate the ten PDFs

**Files:**
- Create: `tools/build_premium_bonus_collection.py`
- Replace: `deliverables/bonus/*.pdf`
- Modify: `tests/test_bonus_guides.py`

**Interfaces:** Consumes all `BOOK` objects and themes; produces ten final PDFs plus preview images in `assets/bonus-premium/previews/`.

- [ ] Write failing tests enforcing ten outputs, spec page-count ranges, extractable titles, minimum file size, and no blank pages.
- [ ] Run `python -m unittest tests/test_bonus_guides.py` and verify current one-page PDFs fail.
- [ ] Implement the renderer, generate the ten PDFs, and export representative inside-page previews.
- [ ] Re-run tests and verify all structural checks pass.
- [ ] Commit with `git commit -m "feat: render premium soap bonus collection"`.

### Task 5: Perform complete visual QA

**Files:**
- Create: `tmp/pdfs/` rendered QA pages
- Modify as needed: editorial components, content modules, and generated PDFs

**Interfaces:** Produces visually approved PDFs with no clipping, overlap, distortion, accidental blank pages, or broken glyphs.

- [ ] Render every page at 150 DPI with Poppler and create contact sheets per volume.
- [ ] Inspect all contact sheets and log defects by volume/page.
- [ ] Fix every logged defect and regenerate affected PDFs.
- [ ] Re-render affected pages and confirm zero remaining defects.
- [ ] Run the full PDF and content test suite and commit with `git commit -m "fix: polish premium bonus collection layout"`.

### Task 6: Publish real demonstrations on the sales page

**Files:**
- Modify: `index.html`
- Modify: `css/styles.css`
- Modify: `tests/test_offer_page.py`

**Interfaces:** Consumes ten cover mockups and internal-page previews; produces a responsive ten-product showcase and rotating inside-page gallery.

- [ ] Write failing tests requiring ten product mockups, ten benefit statements, real inside-page previews, responsive gallery hooks, and CTA links to `#comprar`.
- [ ] Run `python -m unittest tests/test_offer_page.py` and verify the new requirements fail.
- [ ] Implement the showcase, preview gallery, concise benefit copy, and desktop/tablet/mobile layouts.
- [ ] Run page tests, `node --check js/main.js`, and `git diff --check`; verify all pass.
- [ ] Commit with `git commit -m "feat: showcase premium soap bonus collection"`, push `HEAD:main`, and verify deployment status.
