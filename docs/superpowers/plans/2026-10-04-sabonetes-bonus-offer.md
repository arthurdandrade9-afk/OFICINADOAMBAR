# Sabonetes Bonus Offer Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create six premium bonus guides and update the Super Almanaque de Sabonete page with a ten-bonus value stack, clearer CTAs, and a label-generator-focused final mechanism step.

**Architecture:** New bonus sources and rendered PDFs live under the static-site repository, enabling individual delivery later without adding page-load dependencies. The page receives a self-contained visual bonus showcase using local assets; its CTAs scroll to `#comprar` until checkout URLs are supplied.

**Tech Stack:** Static HTML/CSS/JavaScript, Python, Pillow, unittest.

**Spec:** `docs/superpowers/specs/2026-10-04-oferta-sabonetes-bonus-design.md`

## Global Constraints

- Do not promise revenue, guaranteed sales, regulatory approval, or a configured checkout.
- Present ten real bonuses with clear buyer outcomes and honest deliverables.
- Use local assets and HTTPS-only external resources.
- Keep CTAs directed to `#comprar` until the user supplies checkout URLs.
- Preserve desktop and mobile legibility.

---

### Task 1: Create six standalone bonus guides

**Files:**
- Create: `tools/build_soap_bonus_guides.py`
- Create: `deliverables/bonus/01-kit-primeira-venda-7-dias.pdf`
- Create: `deliverables/bonus/02-mapa-30-colecoes.pdf`
- Create: `deliverables/bonus/03-banco-100-nomes.pdf`
- Create: `deliverables/bonus/04-kit-vitrine-que-vende.pdf`
- Create: `deliverables/bonus/05-cartoes-e-tags.pdf`
- Create: `deliverables/bonus/06-calendario-de-datas.pdf`
- Test: `tests/test_bonus_guides.py`

**Interfaces:**
- Produces: `BONUS_OUTPUTS`, a list of the six generated PDF paths.
- Consumes: existing local images in `assets/`.

- [ ] **Step 1: Write the failing test**

```python
def test_six_bonus_pdfs_exist_and_are_nonempty():
    for filename in EXPECTED_BONUSES:
        artifact = BONUS_DIR / filename
        assert artifact.exists()
        assert artifact.stat().st_size > 10_000
```

- [ ] **Step 2: Run the test and verify it fails**

Run `python -m unittest tests/test_bonus_guides.py`; expect missing output files.

- [ ] **Step 3: Implement the builder**

Render one concise, image-led PDF per guide. Every guide contains a promise, a usable checklist or examples, and a closing action. The Kit Primeira Venda avoids financial guarantees; the calendar uses recurring occasions rather than expiring dates.

- [ ] **Step 4: Run the test and verify it passes**

Run `python -m unittest tests/test_bonus_guides.py`; expect six nonempty PDFs.

- [ ] **Step 5: Commit**

Run `git add tools tests deliverables/bonus` followed by `git commit -m "feat: add premium soap offer bonus guides"`.

### Task 2: Build the visual ten-bonus showcase and CTA journey

**Files:**
- Modify: `index.html`
- Modify: `css/styles.css`
- Test: `../site-tests/test_sales_page.py`

**Interfaces:**
- Consumes: the ten bonus names, `assets/rotulos/exemplo-rotulo-sabonete.png`, and `#comprar`.
- Produces: ten buyer-outcome cards, CTA links, and the updated mechanism card.

- [ ] **Step 1: Write the failing tests**

```python
def test_ten_bonus_showcase_explains_buyer_outcomes(self):
    self.assertGreaterEqual(html.count('class="bonus-card"'), 10)
    for label in ("10 bônus", "Kit Primeira Venda", "Mapa das 30 Coleções", "Banco de 100 Nomes", "Kit Vitrine", "Cartões de Cuidado", "Calendário"):
        self.assertIn(label, html)

def test_final_mechanism_step_uses_our_generator_and_standard_label(self):
    self.assertIn("nosso Gerador de Rótulos", html)
    self.assertIn("assets/rotulos/exemplo-rotulo-sabonete.png", html)
```

- [ ] **Step 2: Run tests and verify they fail**

Run `python ../site-tests/test_sales_page.py`; expect missing ten-bonus and mechanism requirements.

- [ ] **Step 3: Implement the page changes**

Add a visual grid where each card contains a short problem-to-result sentence, an icon or local asset, and a clear value label. Add high-intent CTAs after the hero, mechanism, bonus showcase, and value stack. Update step four to use the standard label image and say the buyer generates it with our Gerador de Rótulos before presenting the product for sale.

- [ ] **Step 4: Run tests and verify they pass**

Run `python ../site-tests/test_sales_page.py`; expect all static checks green.

- [ ] **Step 5: Commit**

Run `git add index.html css/styles.css ../site-tests/test_sales_page.py` followed by `git commit -m "feat: strengthen soap offer bonus journey"`.

### Task 3: Verify and publish the complete offer

**Files:**
- Verify: `index.html`, `css/styles.css`, `js/main.js`, and `deliverables/bonus/`

**Interfaces:**
- Consumes: Tasks 1 and 2.
- Produces: a verified commit pushed to `main`.

- [ ] **Step 1: Run full static verification**

Run `python ../site-tests/test_sales_page.py`, `node --check js/main.js`, and `git diff --check`; expect zero failures and zero syntax or whitespace errors.

- [ ] **Step 2: Render PDFs for verification**

Run `python tools/build_soap_bonus_guides.py --verify`; expect a page count for every PDF.

- [ ] **Step 3: Inspect responsive rules**

Run `rg -n "@media|bonus-grid|btn--large|mechanism-step" css/styles.css`; expect narrow-screen grid and touch-safe CTA rules.

- [ ] **Step 4: Commit any verification fix**

Run `git add index.html css/styles.css js/main.js tools deliverables/bonus` followed by `git commit -m "fix: verify soap bonus offer presentation"` when a fix was needed.

- [ ] **Step 5: Publish**

Run `git push origin HEAD:main`; expect GitHub acceptance and the Vercel production deployment to start.
