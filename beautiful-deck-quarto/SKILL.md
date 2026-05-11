---
name: beautiful-deck-quarto
description: Use when the user asks for a slide deck, presentation,
  talk slides, or seminar/lecture deck built from a research artefact
  (paper, manuscript, preprint PDF, memo, or notes), or asks to restyle
  an existing deck. Trigger phrases include "make a deck", "build a
  presentation", "slides for this paper", "talk slides", "seminar deck",
  "lecture deck", "restyle this deck", or "/beautiful-deck-quarto".
  Default brand pack is WEHI; overridable via `--brand=<name>`. Output
  is a Quarto-Beamer .qmd compiled to PDF.
argument-hint: "[path-to-source] [--brand=<name>] [--citations=inline|none]"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(quarto render:*), Bash(R -e:*), Bash(xelatex:*), Bash(pdftotext:*), Bash(grep:*), Bash(head:*), Bash(tail:*), Bash(ls:*), Bash(find:*)
---

# Beautiful Deck (Quarto-Beamer)

You are building a beautiful slide deck from a research artefact. The output is a single `.qmd` file with `format: beamer`, compiled to PDF via Quarto. The brand pack defaults to **WEHI**; assets live in this skill's `assets/wehi/` directory. Do not propose alternatives unprompted. If the user invokes with `--brand=<other>`, asks for a specific aesthetic ("Tufte-clean", "dark hackathon", "serious thesis-defence minimal"), or pastes a visual reference (screenshot of a deck they want to match), Step 2 forks — see below.

This skill operationalises the Rhetoric of Decks (Scott Cunningham), adapted from Scott's `/beautiful_deck` skill in [MixtapeTools](https://github.com/scunning1975/mixtape). The full essay is vendored at `references/rhetoric_of_decks.md` — cite specific principles from it when pushing back on user requests. Your job is to enforce the philosophy, not summarise it.

**Required co-skill.** Step 7 Audit 2 invokes `/tikz` on the compiled `.tex` (collision/clipping checks) and on each generated data graphic (axis-label clipping, legend overlap). The `/tikz` slash-command skill must be installed; if it is not, Audit 2 cannot complete and the deck is not finished.

**Reference files in `references/`** (read on demand, not upfront):

- `references/rhetoric_of_decks.md` — Scott Cunningham's foundational essay (Three Laws, Aristotelian triad with audience balance table, three-act narrative arc, MB/MC equivalence as the audit lens, Devil's Advocate, common-failures catalogue). **Read on demand** to cite specific principles when pushing back; don't preload.
- `references/aristotle.md` — Scott Cunningham's deeper essay on the Aristotelian appeals (ethos / pathos / logos) applied separately to **classroom** and **research seminar** decks, with phronesis/arete/eunoia breakdown of ethos, a failure catalogue keyed to each appeal, and an explicit framing of the appeals as an **AI audit frame**. **Read on demand** when reasoning about audience epistemic state, classroom-vs-seminar weighting, or framing the rhetoric audit (Step 7 Audit 1).
- `references/quarto_beamer_patterns.md` — fenced-div syntax, two-column layouts, callout blocks, code-chunk options, citation handling. **Read this before Step 4** when drafting the .qmd; it is the syntax reference for everything below the YAML.
- `references/tikz_rules.md` — measurement-first rules and canonical templates for conceptual diagrams. **Read this before writing any TikZ block** in Step 4.

## Contents

- [Step 0 — Read the inputs](#step-0--read-the-inputs)
  - [Restyling an existing deck](#restyling-an-existing-deck)
- [Step 1 — Audience triage (MANDATORY PAUSE)](#step-1--audience-triage-mandatory-pause)
- [Step 2 — Theme proposal (MANDATORY PAUSE)](#step-2--theme-proposal-mandatory-pause)
- [Step 3 — Outline (no compile yet)](#step-3--outline-no-compile-yet)
- [Step 4 — Draft the .qmd](#step-4--draft-the-qmd)
- [Step 5 — Compile (quarto render → PDF)](#step-5--compile-quarto-render--pdf)
- [Step 6 — PAUSE: show user the first compile](#step-6--pause-show-user-the-first-compile)
- [Step 7 — Three audits (always run, in this order)](#step-7--three-audits-always-run-in-this-order)
  - [Audit 1 — Rhetoric](#audit-1--rhetoric)
  - [Audit 2 — Graphics](#audit-2--graphics)
  - [Audit 3 — "So what?"](#audit-3--so-what)
- [Step 8 — Hand off](#step-8--hand-off)
- [Notes on the iterative loop](#notes-on-the-iterative-loop)
- [Failure modes to refuse](#failure-modes-to-refuse)

---

## Step 0 — Read the inputs

**Preflight check.** Before reading any source: confirm the `/tikz` slash-command skill is installed (`ls ~/.claude/skills/tikz/SKILL.md` or equivalent). Step 7 Audit 2 requires it; without it you cannot complete the deck. If absent, tell the user: "I need `/tikz` installed for the Audit 2 graphics check — install it first or I will only be able to deliver an unaudited draft." Do not silently proceed and pretend Audit 2 ran.

Then check for an existing deck to restyle (`*.qmd` with `format: beamer` in cwd or a path the user named). If found, see [Restyling an existing deck](#restyling-an-existing-deck) below — the workflow is shorter than full construction.

The user invoked you with one or more of:
- A `.qmd` or `.md` manuscript
- A PDF of a paper or preprint
- A plain text memo or notes file
- An existing deck to restyle

Find the source files. If multiple, ask which is primary. Read enough to know:
- The single takeaway (what must the audience remember?)
- The argument arc (problem → investigation → resolution)
- The figures present (and which are conceptual diagrams vs. data graphics)
- Citations present in the source

If a PDF is the only input, extract text first via `pdftotext` or similar; you cannot reason about a paper from its filename.

Do not produce slides yet. You are still listening.

### Restyling an existing deck

If the user invoked the skill on an existing `.qmd` and the goal is restyling (not rebuilding the argument), skip Steps 1, 3, 4 — those rebuild content. Run a compressed flow instead: Step 0 (read) → Step 2 (theme proposal — same fork as full construction; if user is moving from WEHI to Fork B/C, write the new preamble next to the deck and update the `include-in-header`) → Step 5 (compile) → Step 7 Audit 2 only (visual checks; Audit 1 and Audit 3 are about argument structure and don't apply to a restyle) → Step 8 (hand off). Tell the user explicitly that you skipped the rhetoric audits because the existing argument was not changed.

---

## Step 1 — Audience triage (MANDATORY PAUSE)

Two questions structure this step: **what is the audience's expertise** and **what is the rhetorical mode** (research seminar vs. classroom). Per `references/aristotle.md`, the same Aristotelian appeals (ethos / pathos / logos) operate in both modes but with different weights — seminar audiences need ethos and logos under uncertainty (credibility + visible inference); classroom audiences need pathos and logos for orientation (emotional permission to struggle + learnable sequence). Read `references/aristotle.md` if you are unsure which weighting fits a given audience.

Ask the user, with concrete options:

> **Who is this deck for?**
>
> *Research seminar mode* (peers; central challenge is credibility under uncertainty):
> 1. Stats/methods audience (technical, dense — Logos 70%, Ethos 20%, Pathos 10%)
> 2. Bioinformatics/genetics mixed (Logos 50%, Ethos 25%, Pathos 25%)
> 3. Clinical/wet-lab (low math, high mechanism — Pathos 40%, Logos 35%, Ethos 25%)
> 4. General academic seminar (Logos 45%, Pathos 35%, Ethos 20% — matches `references/rhetoric_of_decks.md`)
>
> *Classroom mode* (less expert; central challenge is orientation, not skepticism):
> 5. Teaching/lecture (Logos 50%, Pathos 35%, Ethos 15% — more recap, more setup, longer; ethos comes from clarity and pacing, not from "I have stress-tested this claim")

Options 1, 2, 3 and 5 are stat-gen / classroom extensions to Scott Cunningham's framework (which has only "Academic seminar" — option 4 above). The general principle holds across all five: pick weights, then the deck must visibly deliver them.
>
> **How long?** (default: 20–30 slides for seminar; 40–60 for a 75-min lecture)
>
> **What single sentence must the audience remember?** This is your takeaway. Everything else is evidence.

Wait for answers. Do not proceed without them. The takeaway sentence is the most important input you will receive — it determines what every slide is for. If the user gives a vague takeaway, push back with an audience-specific template:

- **Stat-gen / methods empirical paper** → "effect size + CI + replication": "*X predicts Y with HR 1.19 (95% CI 1.10–1.28), replicated in cohort Z*". Vague: "X predicts Y".
- **Methods / algorithm paper** → "property + benchmark / regime": "*Method M is unbiased under condition C and matches state-of-art on benchmark B with N× speedup*". Vague: "M works well".
- **Clinical / wet-lab** → "mechanism + actionability": "*Mechanism X drives phenotype Y; targeting X with Z reverses Y in model M*". Vague: "X is involved in Y".
- **Teaching/lecture** → "concept + transferable skill": "*Independence ≠ mutual exclusivity — and confusing them changes the denominator*". Vague: "today we cover probability".

Don't accept the vague form. Get a takeaway you could put on a slide.

The selected option drives Step 7 Audit 1 (Rhetoric) — that audit checks whether ethos/pathos/logos are actually being delivered at the chosen weights. Record the selection.

---

## Step 2 — Theme proposal (MANDATORY PAUSE)

Show the user the planned theme **once**, get approval, then lock it. Which path you take depends on what the user has signalled:

### Fork A — Existing brand pack (default, including WEHI)

This fires when the user said nothing about styling, OR invoked with `--brand=<name>` AND `./assets/<name>/` exists.

Load the brand pack from `./assets/<name>/` (default: `wehi`). State the proposed structure to the user, in plain prose, not a wall of text. The WEHI default reads as:

> Title slide: full-bleed yellow → teal axis gradient (no logo panel — the WEHI default ships without a logo asset, and a clean gradient is more honest than a blank white panel). Title in Georgia bold (Huge), subtitle in Arial (large), author + date in small Arial — all in a single TikZ node anchored at page-north-west, so vertical layout cannot self-collide. Section divider slides: teal → yellow gradient top band (~22% of paper height), `Section N` in small sans on the left of the band, section title in large Georgia bold below. Body slides: plain — black Georgia frame title with a thin teal underline, white background, gradient reserved for title and section dividers (per your preference, to avoid visual repetition over 30 slides). Brand orange `#FF6105` reserved for emphasis: at most one per slide, on the number or word that should land. Teal-tint blocks `#E1F7F5` for key results. Itemize markers explicitly set to `\textbullet` / `$\circ$` / `$\ast$` (no Beamer triangles). XeLaTeX engine with system Georgia/Arial; TeX Gyre Termes/Heros fallback if absent.

For a non-WEHI brand pack, write the equivalent prose from that pack's `palette.yml` + `preamble.tex`. Then ask: *Approve, or change anything?*

If `--brand=<name>` was passed but `./assets/<name>/` is missing, do **not** silently fall back to WEHI. Ask: "I don't have a brand pack for `<name>` — do you want to point me at one, describe the aesthetic, or use the WEHI default?" Then route to Fork A (with the supplied path), Fork B, or Fork A (WEHI).

### Fork B — Aesthetic description (no brand pack)

This fires when the user describes a look in words ("Tufte-clean", "dark hackathon", "Bauhaus poster", "serious and minimal — this is a thesis defence, not a marketing pitch").

**Do not scaffold a permanent `assets/<aesthetic>/` directory.** Generate a single one-off `preamble.tex` next to the `.qmd` and reference it via `include-in-header:` in the YAML. The construction recipe:

1. **Restate the aesthetic in one sentence** and confirm with the user before doing anything else. ("Reading you as: high contrast, sans-only, no gradients, generous whitespace — yes?")
2. **Pick a 6-slot palette** with hex codes and one-line rationale per color:
   - Page background (usually white or near-white; dark mode flips this)
   - Block-tint background (a low-saturation tint of the structure color)
   - Structure / dark accent (frame-title underline, itemize markers, footer text — must hit WCAG-AA contrast on the page background)
   - Secondary grey (footer page numbers, attributions)
   - Emphasis (max one per slide; deliberately loud against the rest)
   - Categorical seed (a 5-color plot palette derived from this; check CVD-safe if the user's audience comparisons require it — Okabe-Ito is the safe default)
3. **Pick fonts**: title face, body face, monospace if code is shown. Default to system fonts available under XeLaTeX (Georgia, Arial, Charter, Helvetica, Source Serif/Sans, Inter); fall back to TeX Gyre Termes/Heros/Cursor if the user wants portability.
4. **Pick layout primitives**: title-slide treatment (full-bleed bg? band? plain?), section-divider treatment (band? full-page? plain?), body slide (frame-title underline color and weight, footer style, what's suppressed on the title slide).
5. **Write the one-off `preamble.tex`** next to the `.qmd`. Implement these mandatory Beamer override points (every Fork B/C theme must define them, even if the implementation is "do nothing"):
   - `\setbeamercolor{normal text}` — page foreground/background
   - `\setbeamercolor{frametitle}` + `\setbeamertemplate{frametitle}` — body-slide title bar (color, font, optional underline rule)
   - `\setbeamertemplate{itemize item/subitem/subsubitem}` — override Beamer's default triangles (use `\textbullet`, `$\circ$`, `$\ast$` or your aesthetic's equivalent — never leave triangles)
   - `\setbeamercolor{block title}` + `\setbeamercolor{block body}` — callout panel for key results
   - `\setbeamertemplate{footline}` — page numbers, conditional on `\insertframenumber>1` to suppress on the title slide
   - `\setbeamertemplate{title page}` — title-slide layout. For a "no decoration" aesthetic, this is just text in a TikZ node; for a full-bleed background, also override `\setbeamertemplate{background canvas}` conditional on `\thepage=1`
   - `\AtBeginSection[]{...}` — section divider frame. For a "no section dividers" aesthetic, define this as an empty `\begin{frame}[plain]\end{frame}` so the hook fires harmlessly rather than triggering Beamer's default

   Do not invent new override points. The audit checks in Step 7 are calibrated to this set; new hooks aren't audited.
6. **Write a `palette.yml`** next to `preamble.tex`. Schema is the brand-pack schema below. This is mandatory, not optional — Audit 2 reads it to grep the deck for emphasis-color and categorical-color discipline. Without `palette.yml`, Audit 2 falls back to "trust the visuals" which is not an audit.
7. State the result to the user as prose (same form as Fork A's WEHI paragraph) and ask for approval.

### Fork C — Visual reference (screenshot)

This fires when the user pastes an image of a deck they want to match.

1. Read the image. Extract: 4–6 dominant hex colors (sample by eye if needed), font characteristics (serif vs sans, weight, all-caps?), title-slide layout (full-bleed background? band? what corner is the title in?), section-divider layout, body-slide structure (frame-title rule? footer? logo?).
2. Restate the aesthetic in one sentence — "Reading the screenshot as: dark navy bg, white serif title centered, no body decoration, ochre rule under each frame title — yes?"
3. Get user confirmation, then proceed as Fork B from step 2 onward.

---

### Brand-pack schema (for Fork A, and for users who later promote a Fork B/C theme)

A brand pack lives at `./assets/<name>/` and contains:

- **`palette.yml`** (required) — a flat dictionary of color names → HTML hex, mirroring exactly what `preamble.tex` declares. Required slots: gradient endpoints (or one structure color if the brand has no gradient), block-tint background, dark accent (WCAG-AA on white), grey-70 and grey-50 (footer/secondary), emphasis (used at most once per slide), and a 5-color categorical palette for plots. Each foreground-on-background pair (dark accent on page bg, block body on block tint, footer grey on page bg) must include the measured contrast ratio as an inline comment so Audit 2 item 5 is mechanical — e.g., `accent: "#1F7A72"  # contrast on white: 5.2:1 (AA pass)`. Free-form additional colors fine.
- **`preamble.tex`** (required) — Beamer template overrides referencing the palette by name. Must define: frame title template, body text and structure colors, itemize markers (override Beamer's default triangles), block title and body colors, footer template (page number; conditional on frame number to suppress on title slide), title-page template, `\AtBeginSection` section divider. Use `assets/wehi/preamble.tex` as the canonical structural skeleton — copy it and substitute.
- **`logo.pdf`** (optional) — only if the brand has a logo asset and it should appear on the title slide. WEHI ships without one deliberately.
- **`fonts.tex`** (optional) — `\setmainfont{...}` / `\setsansfont{...}` / `\setmonofont{...}` declarations if the brand uses non-system fonts that need explicit XeLaTeX font setup. Otherwise the Beamer default + system-font fallback handles it.

Reference from the .qmd YAML using the absolute skill path (matches the WEHI default convention — see Step 4):

```yaml
format:
  beamer:
    pdf-engine: xelatex
    include-in-header:
      - /Users/lee.st/.claude/skills/beautiful-deck-quarto/assets/<name>/preamble.tex
      - /Users/lee.st/.claude/skills/beautiful-deck-quarto/assets/<name>/fonts.tex   # optional
```

---

## Step 3 — Outline (no compile yet)

Generate the slide-by-slide outline as numbered titles only. Each title is an **assertion**, not a label. Do not write content yet.

Apply the Aristotelian balance from Step 1. Apply the three-act arc:

- **Act I — Problem**: 3–5 slides establishing tension
- **Act II — Investigation**: 10–18 slides showing what you did
- **Act III — Resolution**: 4–7 slides delivering the insight + Devil's Advocate + takeaway

The first content slide after the title states the takeaway. Do not bury the lede.

The last slide is **never** "Questions?" or "Thank you." It is the takeaway restated, or a concrete next step.

Show the user the outline. Do **not** pause here unless the outline is clearly wrong — push through to Step 4. The user said pauses are after audience triage and after first compile.

---

## Step 4 — Draft the .qmd

Build a single `.qmd` file. Structure:

```yaml
---
title: "<takeaway-as-title-or-paper-title>"
subtitle: "<descriptor>"
author: "<author>"
date: "<date>"
format:
  beamer:
    aspectratio: 169
    pdf-engine: xelatex
    include-in-header: /Users/lee.st/.claude/skills/beautiful-deck-quarto/assets/wehi/preamble.tex
    fontsize: 11pt
    keep-tex: true
    fig-pos: "H"
mainfont: "Georgia"
sansfont: "Arial"
monofont: "Menlo"
mainfontfallback: ["TeX Gyre Termes"]
sansfontfallback: ["TeX Gyre Heros"]
---
```

The preamble at `/Users/lee.st/.claude/skills/beautiful-deck-quarto/assets/wehi/preamble.tex` is the canonical copy and is loaded by absolute path so each deck picks up improvements without needing a per-deck copy. (Trade-off: re-rendering an old talk picks up later preamble changes. Acceptable for a personal toolkit; if you ever need archival reproducibility for a specific deck, copy the preamble next to that deck's `.qmd` and switch the YAML to a relative path.) Do not reinvent it; load it.

### Slide construction rules

**Frame titles are assertions.** Write `## Treatment increased survival by 34%`, not `## Results`.

**One idea per slide.** If you write "also" or "additionally", split the slide.

**No walls of sentences.** Bullets are defeat — find the structure. Acceptable text: short labeled setups ("From the FOC:"), one concluding line at most, bullets only for genuinely structured content.

**Math.** Display equations get their own slide if they carry the argument. Inline math is fine.

**Emphasis.** Use `\textcolor{wehiOrange}{...}` for the one number per slide that should land. Never two on the same slide.

### Figures: the conceptual / data split

This distinction is load-bearing. Treat differently:

**Conceptual diagrams (TikZ, written inline in the .qmd):**
- Pipelines, flow diagrams, schematic mechanisms, conceptual contrasts (correct vs. wrong, before vs. after), hierarchies, mechanism cartoons
- Write TikZ measurement-first. Read `references/tikz_rules.md` for the six rules — explicit node dimensions, coordinate map before edges, edge-label gap calculations, boundary clearances, Bézier depths, cross-slide consistency — and the three canonical templates (pipeline, two-state contrast, hierarchy). The rules are what keep a diagram from needing post-hoc repair.
- Wrap in `{=latex}` raw blocks
- Run `/tikz <slides.tex>` after first compile as a routine collision check; `/tikz` is fast (single pass, three checks) so there's no reason to skip it

**Never use inline TikZ for quantitative shapes.** Forest plots, bar charts, dose-response curves, KM curves, scatter plots, manhattan plots, sensitivity sweeps, or anything else where shape size encodes a number — these go through Quarto code chunks (next subsection), never through hand-positioned TikZ. The reason: hand-tuned coordinates always diverge from the true value under deadline pressure, and Audit 2 item 1 will catch it. If you find yourself writing TikZ coordinates that come from a regression output or a dataframe, stop and switch to a code chunk.

**Data graphics (code-first, generated to PDF, included via `\includegraphics` or Quarto code chunks):**
- Anything from a dataframe, regression, simulation, alignment, expression matrix
- Anything quantitative from the source paper, even if it "looks like" a conceptual diagram (forest plot, effect-size dot-and-whiskers, mechanism flow with rate constants annotated)
- Generate from R or Python in a code chunk with `fig-format: pdf`, `fig-asp: 0.5` (default), white background, no chartjunk
- Use the WEHI categorical palette for `scale_color_manual` / `palette` arguments — provide it as a vector in the chunk: `c("#FF6105","#ED5E82","#9F71E5","#578CFF","#4EA749")`
- For plots that must be CVD-safe (e.g., ancestry comparisons), use Okabe-Ito or Viridis instead, not the WEHI categorical
- Strip default ggplot2 grey backgrounds; use `theme_minimal()` or `theme_classic()`

If the source paper has existing figures, triage them:
- **Quantitative result figures (forest plots, KM curves, dose-response, scatter, manhattan)** → regenerate from a code chunk if the data is available. If the data isn't available (you have the paper but not the analysis), ask the user explicitly — *"Slide 8 needs the survival curve from Figure 2. I have the paper but not the data. Options: (a) point me at the data file; (b) I include the original figure as `\includegraphics` from the paper PDF; (c) I draw a simplified schematic version and note the source."* Do not silently fabricate values to draw something that "looks like" the published figure.
- **Conceptual schematics (mechanism cartoons, study design diagrams, multi-panel comparison plates)** → copy the original PDF page rather than redraw, unless redrawing genuinely takes less time than the audit will take to verify your version matches the source. Cropping a paper's Figure 1 with `pdfcrop` is usually the right move.
- **Tables** → never copy as image. Re-render with `kable` (R) / `tabulate` (Python) into the deck so font and palette match.

### Citations: the Rhetoric of Decks policy (default)

Citations on slides as they appear in papers — `(Smith et al. 2023)` parenthetical drops — fail the MB/MC test. Default behavior:

1. Strip parenthetical citations from slide body text
2. For results that genuinely need attribution on the slide, render as small grey upper-right corner: `\hfill\textcolor{wehiGrey50}{\small Smith 2024}` (uses the brand palette, not generic `gray!70`)
3. Generate a final references slide from the `.bib` file (one slide, small font, no annotations)
4. Full author lists, journal names, DOIs do not appear on slides — they live in the `.bib` and the user's speech

Override flags:
- `--citations=inline` — keep parenthetical citations as in the source (rare, only for very citation-heavy talks)
- `--citations=none` — strip entirely, no references slide

If a `.bib` file is present in the source directory, link it via `bibliography:` in YAML — full snippet to add to the YAML at the top of the .qmd:

```yaml
bibliography: refs.bib
csl: nature.csl   # optional; omit for default Quarto citation format
suppress-bibliography: false   # default; the references slide is auto-generated
```

The references slide appears automatically at the end of the deck from cited keys. Worked example for the upper-right attribution form (default mode):

```markdown
## Treatment increased survival by 34%

[Body content]

\hfill\textcolor{wehiGrey50}{\small Smith et al. 2024}
```

For `--citations=none` decks where the speaker still wants source attribution, put it in the speaker notes (enable via `format: beamer: notes: true` in YAML) rather than on the slide. Backup slides at the end of the deck (after the references slide) are also acceptable for "I'll mention this if asked" attributions.

---

## Step 5 — Compile (quarto render → PDF)

Run `quarto render <file>.qmd --to beamer`. Quarto drives the LaTeX pipeline.

**XeLaTeX engine.** The footer template uses `\inserttotalframenumber`, which needs a second xelatex pass to resolve `n/N`.

- **First, try `quarto render slides.qmd --to beamer`** — recent Quarto runs xelatex twice automatically and resolves the frame count in one invocation. Check stderr for two `running xelatex` lines; if you see them, no second pass is needed.
- **If Quarto only ran one pass** (older Quarto, custom config), follow with `xelatex -interaction=nonstopmode slides.tex` to resolve the cross-references. Requires `keep-tex: true` in the YAML (already set in the template at Step 4).
- **If system `xelatex` is unavailable** but Quarto's bundled engine works, just use `quarto render` twice. Do **not** route through `tinytex::xelatex()` from R — in the user's environment it has failed where the system or bundled xelatex succeeds.

**Reading the LaTeX log for warnings.** Quarto runs xelatex in a scratch directory and discards `slides.log` — it is not next to `slides.tex` after `quarto render`. To capture warnings: either grep Quarto's stderr (`quarto render slides.qmd --to beamer 2>&1 | grep -E 'Overfull|Underfull'`), or run a separate `xelatex -interaction=nonstopmode slides.tex` after the Quarto render and read `slides.log` from there. Don't skip this — Overfull/Underfull warnings correspond to real visual artifacts (see "Mandatory zero-warnings rule" below).

**Mandatory zero-warnings rule.** Capture the log per the instructions above, then grep for `Overfull \hbox`, `Underfull \hbox`, `Overfull \vbox`, `Underfull \vbox`. Each one indicates a layout failure: text bleeding into the margin, awkward stretching, content overflowing the slide. Fix every warning before declaring done. Do not minimise these — they correspond to real visual artifacts even when subtle.

**Common fixes:**
- Overfull `\hbox` on a frame title → shorten the assertion, or break it onto two lines with `\\`
- Overfull `\vbox` → too much content on the slide; split into two slides
- Underfull `\hbox` in a paragraph → forced line break in wrong place; let the paragraph reflow
- TikZ figures pushing out of the textwidth → add `[scale=0.85]` or wrap in `\resizebox{\textwidth}{!}{...}`

**Beamer-specific gotchas to watch for** (each has bitten a real deck — search for them by name in the log or eyeball the PDF):

- **Title overflow via `\attrib` (or any title-side macro).** Long titles + an attribution suffix push past the right margin without raising an `Overfull \hbox` because the frametitle template absorbs it. Visually inspect the title bar of every slide.
- **TikZ key collisions.** Reusing a node name across two diagrams in the same frame, or shadowing a built-in key (`text`, `node`, `path`) in a `\tikzset`, silently produces wrong arrows. Grep the `.tex` for repeated `(name)` declarations within a frame.
- **Section divider clipping.** Long `\section{...}` titles can run off the page; the section divider template wraps inside a `text width=0.85\paperwidth` box but only if anchored at `current page.west` (see preamble). If you change the anchor, re-check.
- **Unicode arrow glyphs (`→`, `⇒`, `↦`).** XeLaTeX with Georgia falls back to TeX Gyre Termes for arrows, which renders them as boxes or wrong glyphs depending on the font cache. Use `$\to$`, `$\Rightarrow$`, `$\mapsto$` in math mode instead of the unicode characters.

After fixing all warnings, recompile and re-check.

---

## Step 6 — PAUSE: show user the first compile

This is the second mandatory pause point. Tell the user:

> First compile is done. PDF is at `<path>`. Zero LaTeX warnings.
>
> Before I run the audits, take a look. What needs to change?

Wait for feedback. If they say "go", proceed to Step 7.

---

## Step 7 — Three audits (always run, in this order)

Run all three audits autonomously. Do not skip. If any audit reports issues, fix them, recompile, and re-run that audit until clean.

### Audit 1 — Rhetoric

**Open with one Aristotelian sentence**, then walk slides. Before slide-by-slide checking, name the **strongest appeal-level miss** in one sentence — judged against the weights selected in Step 1. Examples: "Ethos is weak: the identification strategy doesn't appear until slide 8 and there is no Devil's Advocate slide." / "Pathos is weak: the opening is an outline slide instead of a tension slide." / "Logos is intact; ethos and pathos balanced for the selected audience — proceed." Use `references/aristotle.md` "AI, Decks, and the New Verification Problem" if you cannot identify the miss. If there is a miss, fix it (usually by adding or moving 1–2 slides) before walking individual slides — the slide-level audit will be wrong if the appeal balance is wrong.

Then walk every slide. For each, check:

1. **Is the title an assertion?** (Not "Methods" — "We exploit clinic closures for identification")
2. **One idea?** (No "also", no "additionally", no second contrast that doesn't pair with the first)
3. **Does the slide serve the spoken word?** (Could a reader understand it without you? If yes, it's a document, not a slide. Cut.)
4. **MB/MC equivalence?** (Is this slide carrying the same load as its neighbours? A near-empty slide between two dense ones is fine if it's a deliberate breath; flag it if it's accidental thinness.)
5. **Lede position.** Slide 2 should state the takeaway. Verify.
6. **Last slide.** It should restate the takeaway or give a next step. If it says "Questions?" or "Thank you", rewrite.

Report findings as a numbered list per slide. Fix.

### Audit 2 — Graphics

**First, run `/tikz` for collision and clipping checks** — don't re-implement them inline:

- `/tikz <deck>.tex` — math mode on the compiled TeX, audits every `tikzpicture` block for Bézier label collisions, label-to-object whitespace, and edge clipping.
- `/tikz <figure>.pdf` (or `.png`) — visual mode on each data graphic the deck emits. The output directory is whatever Quarto resolves it to: by default `<deck>_files/figure-beamer/`, but if the YAML sets `fig-path:` (or a chunk uses `fig.path=`/`fig.dir=`) the path lives there instead. Read the YAML before grepping; don't hardcode the default. Catches axis-label clipping, legend overlap, and labels running off the canvas in ggplot/matplotlib output. This is the new value of the rewritten `/tikz` and the reason the audit no longer eyeballs these manually.

`/tikz` reports findings and exits — it does not loop. Apply its proposed fixes, recompile once, and move on. Do not re-run `/tikz` after every micro-fix; one pass per figure is the design.

**Then walk every figure for the checks `/tikz` does not cover:**

1. **TikZ data integrity.** Every visual element in a TikZ diagram must encode a real value. If a bar's height, a node's size, or an arrow's thickness was hand-tuned for visual balance rather than computed from the underlying number, it is a lie — cut it or replace with a code-generated data graphic. Decorative bars that don't map to values are the most common offender. Cross-check: for each quantitative shape in the diagram, name the variable it represents and confirm the encoding (height ∝ count, width ∝ effect size, etc.) is faithful.
2. **Tick alignment.** Do tick marks align with gridlines? Are axis breaks consistent?
3. **Emphasis discipline.** Resolve the emphasis color from the active brand pack: WEHI → `wehiOrange` / `#FF6105`; Fork B/C → read the `emphasis` slot from the deck-adjacent `palette.yml` written in Step 2. Then split the `.qmd` by `^## ` (slide boundaries) and grep each slide for `\textcolor{<emphasis>}{`, `[...]{.emph}`, and the literal hex. **At most one occurrence per slide.** Two on a slide cancel each other out — cut all but one. Emphasis used for a default plot series in a code chunk is also wrong; it must be reserved for slide text.
4. **Categorical-palette discipline.** Resolve the categorical palette from WEHI's 5-color saturated set or the Fork B/C `palette.yml` `categorical` list. Then grep all `{r}` / `{python}` chunks for `scale_color_manual(values = ...)`, `scale_fill_manual(...)`, or matplotlib `color=`/`palette=` — every multi-series plot must pass the brand categorical vector explicitly, not rely on ggplot/matplotlib defaults. Default-palette plots (no `scale_*_manual`) are flagged regardless of how the colors look. Greys, the emphasis color used as a series color, or ad-hoc hex picks all count as violations.
5. **Pastel violations.** Pastels (any low-saturation tint, including the brand block-tint) appear **only** as fills behind black text or as figure backgrounds. Pastels as text color, axis lines, or plot lines on white = unreadable = wrong.
6. **CVD-safety.** For plots comparing subgroups (ancestry, condition, sex, treatment arm), confirm Okabe-Ito or Viridis was used in place of the brand categorical. The WEHI categorical orange/green is risky for protanopia; Fork B/C themes have not been CVD-tested at all and should default to Okabe-Ito for any comparison the user will publish.

Fix and recompile.

### Audit 3 — "So what?"

This is the harshest audit. Walk every slide and ask: **does this slide earn its place?**

- If you removed this slide, would the argument suffer? If no, cut it.
- Is this slide here because it was easy to generate, or because the argument needs it?
- Is this slide a "just in case" inclusion (the audience might ask)? If yes, move it to backup slides at the end, after the references.
- Is there padding? A "Background" slide that summarises a textbook? An "Outline" slide that lists three sections? Both usually fail this audit.

Cut ruthlessly. The deck is finished when you cannot remove a slide without weakening the argument.

Report cuts to the user with a one-line justification each. Recompile.

---

## Step 8 — Hand off

When all three audits are clean:

```
Deck complete. <N> slides. PDF at <path>.
- Audience: <from Step 1>
- Takeaway: <from Step 1>
- Cuts made in audit 3: <list>
- Outstanding items the user flagged that are not yet addressed: <list>
```

Do not declare done until the audits are actually clean — not "mostly clean", not "I'll fix the rest later". Clean.

---

## Notes on the iterative loop

The user will respond with feedback after Step 6 and after Step 8. Common feedback patterns and the right response:

- **"This slide is too dense"** → cut content, do not shrink fonts. The MB ratio is wrong, not the layout.
- **"This slide is too sparse"** → ask whether a deliberate breath was intended; if not, merge with neighbours or cut.
- **"The [emphasis color] is too much"** → audit emphasis use; you've probably violated the one-emphasis-per-slide rule. (For WEHI default: that's `wehiOrange`. For Fork B/C: whatever was approved as the emphasis slot.)
- **"Make it punchier"** → assertions in titles are weak; rewrite titles as concrete claims with numbers.
- **"This is too long"** → re-run "so what" audit aggressively. Aim to cut 20%.

Each iteration: regenerate the affected slides, recompile to zero warnings, re-run the relevant audit, return to the user.

---

## Failure modes to refuse

If the user asks you to:
- Add a logo to every slide → refuse, explain logo-on-every-slide costs cognitive load every slide and signals identity only once
- Use stock photos as decoration → refuse, decoration without function is noise
- Add a 3D bar chart with gradient fills → refuse, chartjunk fails Beauty-is-Function
- Pad to a slide count → refuse, count is a constraint not a target
- Reproduce paper paragraphs verbatim → refuse, slides are not documents

Push back politely but firmly. Cite the specific principle (with section reference — see `references/rhetoric_of_decks.md`). The user has read the essay; they will recognise the reference.
