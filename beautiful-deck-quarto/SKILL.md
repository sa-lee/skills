---
name: beautiful-deck-quarto
description: Build a beautiful Quarto-Beamer deck (PDF) from a research artefact — paper, manuscript, memo, or notes. Applies the Rhetoric of Decks: titles as assertions, one idea per slide, MB/MC equivalence, Narrative → Application → Picture → Codeblock → Technical pedagogical movement. Default brand pack is WEHI (gradient title slide + section dividers, Georgia/Arial via XeLaTeX, brand orange reserved for emphasis); overridable per-project. TikZ for conceptual diagrams written measurement-first; data graphics generated code-first from R/Python and included as PDF. Compiles via `quarto render` to PDF; runs three audits (rhetoric, graphics, "so what") before declaring done. Pauses for user input after audience triage + theme proposal, and after first compile.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebFetch
---

# Beautiful Deck (Quarto-Beamer)

You are building a beautiful slide deck from a research artefact. The output is a single `.qmd` file with `format: beamer`, compiled to PDF via Quarto. The brand pack defaults to WEHI; assets live in this skill's `assets/wehi/` directory. The user has explicitly asked for the WEHI default; do not propose alternatives unless the user invokes with `--brand=<other>`.

This skill embodies the Rhetoric of Decks philosophy. The user has read the essay. Your job is to enforce it, not summarise it back to them.

---

## Step 0 — Read the inputs

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

---

## Step 1 — Audience triage (MANDATORY PAUSE)

Ask the user, with concrete options:

> **Who is this deck for?**
> 1. Stats/methods audience (technical, dense — Logos 70%)
> 2. Bioinformatics/genetics mixed (Logos 50%, Pathos 30%, Ethos 20%)
> 3. Clinical/wet-lab (low math, high mechanism — Pathos 50%, Logos 30%)
> 4. General academic seminar (Logos 45%, Pathos 35%, Ethos 20%)
> 5. Teaching/lecture (more recap, more setup, longer)
>
> **How long?** (default: 20–30 slides for seminar)
>
> **What single sentence must the audience remember?** This is your takeaway. Everything else is evidence.

Wait for answers. Do not proceed without them. The takeaway sentence is the most important input you will receive — it determines what every slide is for. If the user gives a vague takeaway ("my method is good"), push back: "What about it? What number, mechanism, or comparison should land?"

---

## Step 2 — Theme proposal (MANDATORY PAUSE)

Show the user the planned theme **once**, get approval, then lock it.

Default brand pack: **WEHI**. The palette and assets are in `./assets/wehi/`:

- `palette.yml` — color definitions
- `logo.pdf` — logo for title slide (if absent, fall back to text-only title)
- `gradient.tex` — TikZ snippet defining the title-slide / section-divider gradient

**Proposed structure** (state this to the user, in plain prose, not a wall of text):

> Title slide: yellow → mint → teal gradient background, white right panel for logo, Georgia bold for the heading, Arial for subheading. Section divider slides: same gradient as a top band, section number on the left in serif. Body slides: plain — black frame title in Georgia, white background, gradient reserved for section dividers (per your preference, to avoid visual repetition over 30 slides). Brand orange `#FF6105` reserved for emphasis: at most one per slide, on the number or word that should land. Teal-tint blocks `#E1F7F5` for key results. XeLaTeX engine with system Georgia/Arial; PostScript fallback if absent.

Then ask:
> Approve, or change anything?

If the user invoked with `--brand=<other>`, look for `./assets/<other>/palette.yml` etc. and use that instead. If the brand pack is missing, ask the user to point you at brand assets or fall back to a generic minimal theme.

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
    include-in-header: assets/wehi/preamble.tex
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

The preamble at `assets/wehi/preamble.tex` defines colors, the gradient TikZ, and the Beamer template overrides for title slide + section dividers. Do not reinvent it; load it.

### Slide construction rules

**Frame titles are assertions.** Write `## Treatment increased survival by 34%`, not `## Results`.

**One idea per slide.** If you write "also" or "additionally", split the slide.

**No walls of sentences.** Bullets are defeat — find the structure. Acceptable text: short labeled setups ("From the FOC:"), one concluding line at most, bullets only for genuinely structured content.

**Math.** Display equations get their own slide if they carry the argument. Inline math is fine.

**Emphasis.** Use `\textcolor{wehiOrange}{...}` for the one number per slide that should land. Never two on the same slide.

### Figures: the conceptual / data split

This distinction is load-bearing. Treat differently:

**Conceptual diagrams (TikZ, written inline in the .qmd):**
- Pipelines, flow diagrams, schematic mechanisms, conceptual contrasts
- Write TikZ measurement-first: declare node dimensions explicitly, build a coordinate map before drawing edges, use canonical templates from `./assets/tikz_templates/` if present
- Wrap in `{=latex}` raw blocks
- Test: a TikZ diagram should render correctly the first time, not need a `/tikz` repair pass

**Data graphics (code-first, generated to PDF, included via `\includegraphics` or Quarto code chunks):**
- Anything from a dataframe, regression, simulation, alignment, expression matrix
- Generate from R or Python in a code chunk with `fig-format: pdf`, `fig-asp: 0.5` (default), white background, no chartjunk
- Use the WEHI categorical palette for `scale_color_manual` / `palette` arguments — provide it as a vector in the chunk: `c("#FF6105","#ED5E82","#9F71E5","#578CFF","#4EA749")`
- For plots that must be CVD-safe (e.g., ancestry comparisons), use Okabe-Ito or Viridis instead, not the WEHI categorical
- Strip default ggplot2 grey backgrounds; use `theme_minimal()` or `theme_classic()`

If the source paper has existing figures, prefer regenerating from code where possible (consistency); keep the original only if it's a complex schematic that would take longer to redraw than it would to copy.

### Citations: the Rhetoric of Decks policy (default)

Citations on slides as they appear in papers — `(Smith et al. 2023)` parenthetical drops — fail the MB/MC test. Default behavior:

1. Strip parenthetical citations from slide body text
2. For results that genuinely need attribution on the slide, render as small grey upper-right corner: `\hfill\textcolor{gray!70}{\small Smith 2024}`
3. Generate a final references slide from the `.bib` file (one slide, small font, no annotations)
4. Full author lists, journal names, DOIs do not appear on slides — they live in the `.bib` and the user's speech

Override flags:
- `--citations=inline` — keep parenthetical citations as in the source (rare, only for very citation-heavy talks)
- `--citations=none` — strip entirely, no references slide

If a `.bib` file is present in the source directory, link it via `bibliography:` in YAML.

---

## Step 5 — Compile (quarto render → PDF)

Run `quarto render <file>.qmd --to beamer`. Quarto handles the LaTeX pipeline.

**Mandatory zero-warnings rule.** Read the LaTeX log (`<file>.log`) for `Overfull \hbox`, `Underfull \hbox`, `Overfull \vbox`, `Underfull \vbox`. Each one indicates a layout failure: text bleeding into the margin, awkward stretching, content overflowing the slide. Fix every warning before declaring done. Do not minimise these — they correspond to real visual artifacts even when subtle.

**Common fixes:**
- Overfull `\hbox` on a frame title → shorten the assertion, or break it onto two lines with `\\`
- Overfull `\vbox` → too much content on the slide; split into two slides
- Underfull `\hbox` in a paragraph → forced line break in wrong place; let the paragraph reflow
- TikZ figures pushing out of the textwidth → add `[scale=0.85]` or wrap in `\resizebox{\textwidth}{!}{...}`

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

Walk every slide. For each, check:

1. **Is the title an assertion?** (Not "Methods" — "We exploit clinic closures for identification")
2. **One idea?** (No "also", no "additionally", no second contrast that doesn't pair with the first)
3. **Does the slide serve the spoken word?** (Could a reader understand it without you? If yes, it's a document, not a slide. Cut.)
4. **MB/MC equivalence?** (Is this slide carrying the same load as its neighbours? A near-empty slide between two dense ones is fine if it's a deliberate breath; flag it if it's accidental thinness.)
5. **Lede position.** Slide 2 should state the takeaway. Verify.
6. **Last slide.** It should restate the takeaway or give a next step. If it says "Questions?" or "Thank you", rewrite.

Report findings as a numbered list per slide. Fix.

### Audit 2 — Graphics

Walk every figure (TikZ and data graphic). For each:

1. **TikZ collisions.** Open the PDF (or read it back if you can). Are labels overlapping nodes? Are arrows passing through other shapes? Are coordinate calculations off?
2. **Plot label clipping.** Are axis labels cut off at the figure boundary? Are legends obscuring data points?
3. **Tick alignment.** Do tick marks align with gridlines? Are axis breaks consistent?
4. **Color use.** Did you use orange for emphasis (correct) or for a default series in a 5-color plot (wrong)? Categorical plots use the saturated set; emphasis is reserved.
5. **Pastel violations.** Pastels appear only as fills behind black text or in figure backgrounds. Pastels as text or as plot lines on white = unreadable = wrong.
6. **CVD-safety.** For comparisons of subgroups (ancestry, condition, sex), confirm Okabe-Ito or Viridis was used. The WEHI categorical orange/green is risky for protanopia.

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
- **"The orange is too much"** → audit emphasis use; you've probably violated the one-orange-per-slide rule.
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

Push back politely but firmly. Cite the specific principle. The user has read the essay; they will recognise the reference.
