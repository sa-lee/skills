---
name: deep-read
description: >
  Use when the user asks to deeply read or summarize a local academic PDF — phrases like
  "/deep-read", "deep read this paper", "FOCUS summary", or "summarize this paper
  carefully/thoroughly/exhaustively". Triggers on requests where every key insight must
  be captured with concrete specifics (effect sizes, sample sizes, accessions, software
  versions) and direct quotes preserved. Especially relevant for bioinformatics,
  statistical genetics, and related fields where the specifics are what make a paper
  replicable. Also use when a paper is long enough (>15 pages) that one-shot reading
  risks shallow comprehension or context overflow. Inputs are LOCAL PDF paths only —
  this skill does not search for or download papers from the web.
---

# deep-read

Two-part skill for reading academic PDFs deeply and producing a FOCUS-format summary.

**Part 1 — Reading mechanism:** image-based batched reading via the Read tool, with optional
text-only fast path for prose-heavy papers without important figures.

**Part 2 — Output format:** FOCUS-style exhaustive extraction (numbered, section-by-section,
with embedded direct quotes), preceded by an overview and YAML frontmatter, with dedicated
Statistical Methods and Reproducibility sections.

## When to use

- The user invokes `/deep-read` or asks for a "deep read" / "FOCUS summary" of a paper
- The user provides a local PDF and wants a thorough, detail-preserving summary
- The user wants every key point captured (not a high-level gloss) with specific details and direct quotes
- A paper is long enough (>15 pages) that one-shot reading risks shallow comprehension or context overflow

**Do not use** for:
- Web search or DOI lookup — this skill takes local PDFs only
- Triage of many papers (use a one-shot read of the first split for that)
- Non-academic documents where exhaustive extraction is overkill

## Critical rule

**Never read a full long PDF in one Read call.** Image rendering of long PDFs either crashes
the session with a "prompt too long" error (destroying all context) or produces shallow,
hallucinated output. Read 4-page splits, 3 at a time, with pauses. The only exceptions are:

- PDFs <15 pages (read directly, no splitting)
- The text-only fast path (extract to markdown first, then read the markdown)

## Step 1 — Inputs and pre-flight checks

The user provides a **local PDF path**. If they didn't, ask. Do not search the web.

Resolve paths from the supplied PDF (shell variables used throughout the rest of this skill):

```bash
PDF="$(realpath user_supplied_path)"
FOLDER="$(dirname "$PDF")"
BASE="$(basename "$PDF" .pdf)"

BUILD="$FOLDER/$(basename "$FOLDER")_build"
SPLIT="$BUILD/split_$BASE"

FOCUS="$FOLDER/${BASE}_focus.md"   # final output, alongside the PDF
NOTES="$SPLIT/notes.md"            # working notes, in build dir
```

**Check for existing FOCUS output.** If `<basename>_focus.md` exists, ask:

> "A FOCUS summary already exists at `<basename>_focus.md`. Reuse it, or re-read the PDF from scratch?"

- Reuse → read the existing markdown and answer based on it. Stop.
- Re-read → continue.

**Check for supplementary PDFs.** Scan the source folder for other PDFs whose names suggest
they are supplementary material for this paper (`*_supp*.pdf`, `*_si.pdf`, `*supplementary*.pdf`,
or any PDF in the same folder sharing a substring with the main basename). If found, list them
and tell the user they will be read after the main paper. Don't ask permission — the user has
already opted into reading supplementary material when they invoked this skill.

**Check for existing splits.** If `split_dir` exists with `.pdf` files, ask:

> "Splits already exist for `<basename>` (N chunks). Reuse, or re-split?"

- Reuse → skip Step 2.
- Re-split → delete `split_dir` and continue.

## Step 2 — Decide path: short / text-only / standard

All three branches use bundled scripts under `scripts/`. They are PEP 723 single-file
uv scripts — uv installs the dependency on first run, no manual `pip install` needed.

**Short PDF path.** Get the page count:

```bash
N_PAGES=$(uv run scripts/page_count.py "$PDF")
```

If `N_PAGES < 15`, skip splitting. Read the whole PDF in one Read call. Proceed to Step 4.

**Text-only fast path.** Use this if and only if the user explicitly says "text only", passes
`--text-only`, or the paper is known to be a prose-only piece (commentary, perspective, theory
paper with no important figures). Extract the entire PDF to per-page markdown:

```bash
TEXT="$BUILD/${BASE}_text.md"
uv run scripts/extract_text.py "$PDF" "$TEXT"
```

Then Read `$TEXT` and proceed to Step 4. No batching, no pause-and-confirm — text is cheap
in the context window. **Default is NOT text-only.** Image-based reading catches figures,
Manhattan plots, forest plots, gels, structural diagrams, and complex tables that text
extraction loses. Only switch to text-only when you are sure the visual content doesn't matter.

**Standard path.** For PDFs ≥15 pages without `--text-only`, split into 4-page chunks:

```bash
uv run scripts/split_pdf.py "$PDF" "$SPLIT"   # writes ${BASE}_pp<start>-<end>.pdf into $SPLIT
```

Override the chunk size with `--pages-per-chunk N` if needed (default 4).

## Step 3 — Read in batches of 3 splits with pause-and-confirm

Read **exactly 3 split files** per Read call sequence. After each batch:

1. Read the 3 split PDFs using the Read tool
2. Update `notes.md` (see Step 4 for what to capture)
3. Pause and tell the user:

   > "Finished splits [X–Y] of [N]. Continue with the next 3?"

4. Wait for explicit confirmation before reading the next batch

Do not read ahead. The pause exists to let the user redirect, catch hallucination early, and
keep context manageable. **Pause-and-confirm is the default.** It can be skipped only if the
user explicitly says "no need to pause" or "read straight through" up front.

Process supplementary PDFs after the main paper using the same protocol.

## Step 4 — Working notes (internal scaffolding)

While reading, accumulate a working `notes.md` in the build dir. **This is internal
scaffolding, not the final output.** Capture, with concrete specifics rather than vague gloss:

1. **Bibliographic details** — title, authors, year, journal, DOI
2. **Research question & motivation** — what the paper asks, why it matters in the field
3. **Study design** — cohort(s), sample size(s), ancestry composition, tissue or cell type, study type (case/control, cohort, cross-sectional, MR, GWAS, fine-mapping, etc.)
4. **Data sources** — biobank names (UK Biobank, AoU, GEL, FinnGen, BBJ, etc.), accessions (GEO, SRA, EGA, dbGaP, ArrayExpress, ENA), reference panels, summary statistic sources, exact URLs where given
5. **Methods** — statistical models (mixed models, regression, Bayesian, ML), software with versions (PLINK 2.0, REGENIE, SAIGE, GCTA, LDSC, GATK x.y, DESeq2, STAR, Salmon, Seurat, etc.), pipelines (Nextflow, Snakemake, WDL), key parameters (MAF cutoffs, INFO thresholds, kinship, PCs, covariates, multiple-testing correction)
6. **Key findings with effect sizes** — ORs, betas, SEs, CIs, p-values, h², rg, PIPs, FDR, AUC, Δ — *capture the actual numbers*
7. **Validation / replication** — independent cohorts, holdout sets, cross-ancestry validation
8. **Code & data availability** — GitHub repos (with branch/commit if given), Zenodo DOIs, software releases, data deposition accessions, supplementary file references
9. **Limitations & caveats** — author-acknowledged limitations + your own flags (small n, single-ancestry, no replication, weak instruments, multiple-testing concerns, etc.)

Update incrementally after each batch. Do not rewrite from scratch each time.

## Step 5 — Produce final FOCUS output

After all batches (main paper + supplementary) are read, write the final output to
`<basename>_focus.md` alongside the source PDF.

### Frontmatter

```yaml
---
title: "..."
authors: ["...", "..."]
year: YYYY
journal: "..."
doi: "..."
preprint: "..."   # optional, e.g. bioRxiv DOI
---
```

Omit fields not found in the paper. Do not invent.

### Body structure

```markdown
## Overview

[3–6 sentence paragraph: main contribution, key findings, significance. No bullets.]

## Introduction

1. **Key point heading in sentence case**
Body paragraph with specific details and embedded direct quotes in *italics* within
double quotation marks, like *"the precise wording from the paper"*. Bold key terms
and concept names within the body.

2. **Another key point**
...

## Methods

[Numbered items, same format.]

## Statistical methods

[Always a separate, dedicated section even if the paper folds these into Methods.
Capture: model specifications, software + version, key parameters, multiple-testing
correction, sensitivity analyses.]

## Results

[Numbered items, same format. Capture effect sizes verbatim.]

## Discussion

[Numbered items, same format.]

## Reproducibility

[Always a dedicated section. Capture:
- Code repositories (URLs, commits/branches/tags if given)
- Data accessions (GEO, SRA, EGA, dbGaP, etc.)
- Software with versions
- Reference data (genome builds, annotations, reference panels)
- Container/environment info if given (Docker, Singularity, conda)
- Author contact for restricted data]
```

If the source paper has different section names (e.g., "Online Methods", "Extended Data"),
mirror them. If the paper is structured differently (e.g., a Letter with a single body),
organize thematically. Always include the **Statistical methods** and **Reproducibility**
sections, regardless of the source structure — synthesize them from wherever the relevant
content appears.

If supplementary material was read, integrate its content into the relevant sections (don't
make a separate "Supplement" section unless the supp contains genuinely standalone content
like a separate dataset or method).

### FOCUS formatting rules (from Lin 2025, *Nat. Biotechnol.*)

1. **Exhaustiveness over brevity.** If a section has 12 distinct points, list all 12.
2. **Specificity is mandatory.** Every point must include concrete details: numbers, effect
   sizes, sample sizes, method names, comparisons, dates, accessions. Vague paraphrases are failures.
3. **Quotes support, not duplicate.** Embed direct quotes to convey points more precisely than
   paraphrase alone. Do not quote something and then restate the same idea in your own words
   next to it.
4. **No meta-discourse.** Never write "In this section, the authors argue..." or "Below is a
   summary..." or "End of summary." Attribution to "the authors" or "the paper" is assumed.
5. **No citation markers in output.** Strip superscript numbers, bracketed refs like [12],
   inline cites like (Smith et al., 2023), URLs to citations, and DOIs of cited works (keep
   the DOI of the paper being summarized, in frontmatter).

**Correct style:**

> 1. **Cross-ancestry meta-analysis identifies 47 novel loci**
> Combining UKB (n=487,409), BBJ (n=178,726) and FinnGen R10 (n=412,181) yielded 47 genome-wide
> significant loci not previously reported, with effect sizes consistent across ancestries
> (heterogeneity *I²* < 30% for 41/47). The strongest novel signal at *PCSK9* showed
> *"comparable effect estimates across all three cohorts (β = -0.21, 0.95% CI -0.24 to -0.18)"*.

**Incorrect style:**

> 1. The authors performed a cross-ancestry meta-analysis. They report that the analysis found
> 47 novel loci. They note that *"comparable effect estimates across all three cohorts..."*

The incorrect version restates the quote's content before quoting it and inserts unnecessary
attribution.

**Output only the final FOCUS markdown.** Do not show the working notes. Do not include
preamble like "Here is the summary" or closing meta-commentary. The frontmatter starts the file.

After writing, tell the user:

> "FOCUS summary saved to `<basename>_focus.md`. Working notes retained in `<build_dir>/notes.md`."

## Subagent isolation protocol

When this skill is invoked **by another skill or workflow** (e.g., a lit-review workflow
processing many papers), the reading must run inside a subagent. PDF page images accumulate
permanently in conversation context — reading several long PDFs in one parent session leads
to unrecoverable "prompt too long" failures.

**Pattern:** the parent does the lightweight Step 1 + Step 2 (path resolution + splitting)
in its own context, then launches an Agent for Steps 3–5:

```
Read PDF split files and produce a FOCUS-format summary.

Split directory: <split_dir>
Files (read in this order, 3 at a time): <file_list>
Supplementary files (read after main): <supp_list>
Working notes path: <notes_path>
Final output path: <focus_out>
Domain: bioinformatics / statistical genetics

Process:
1. Read 3 split PDFs at a time using the Read tool
2. After each batch, update working notes with internal scaffolding
   (bibliographic details, research question, study design, data sources,
    methods, findings with effect sizes, validation, code/data availability,
    limitations)
3. Process supplementary PDFs after main paper
4. Produce final FOCUS-format markdown with YAML frontmatter, overview,
   section-by-section numbered extraction, dedicated Statistical Methods
   and Reproducibility sections, embedded direct quotes
5. Write to final output path

Skip pause-and-confirm (subagent context, no interactive user).
Report when done: pages read, sections in output, one-line summary.
```

After the agent returns, the parent reads the final markdown (cheap — plain text, no images)
and continues its workflow.

**Standalone invocations** (user runs `/deep-read` directly) use the interactive protocol
with reads in the main conversation and pause-and-confirm.

## Quick reference

| Step | Action |
|------|--------|
| **Resolve** | Get local PDF path; resolve build/split/output paths |
| **Check** | Existing `_focus.md` → offer reuse. Existing splits → offer reuse. Detect supp PDFs. |
| **Path** | `scripts/page_count.py` → <15 pages = read whole; text-only = `scripts/extract_text.py` then read md; else split |
| **Split** | `scripts/split_pdf.py` → 4-page chunks under `<folder>_build/split_<basename>/` |
| **Read** | 3 splits at a time, update `notes.md`, pause-and-confirm |
| **Supp** | Read supplementary PDFs same way |
| **Write** | FOCUS markdown to `<basename>_focus.md` (frontmatter + overview + sections + Stats + Reproducibility) |
| **Persist** | Keep both `<basename>_focus.md` and `<build_dir>/notes.md` |

## Acknowledgments

The FOCUS output format is from:

> Lin, Z. FOCUS: an AI-assisted reading workflow for information overload.
> *Nat. Biotechnol.* **43**, 2070–2075 (2025). https://doi.org/10.1038/s41587-025-02947-8

The batched reading mechanism, build directory convention, persistent extraction, split
reuse, and subagent isolation protocol were inspired by the `split-pdf` skill (Stephen
Turner / Ben Bentzin, 2026). This skill merges the two and adapts the extraction
scaffolding for bioinformatics and statistical genetics.

For background on why batched reading works, see [references/methodology.md](references/methodology.md).
