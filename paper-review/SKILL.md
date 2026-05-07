---
name: paper-review
description: Run a 6-agent pre-submission referee report for a bioinformatics, statistical genetics, or genetic epidemiology manuscript. Use this skill whenever the user asks to review a paper, get feedback on a manuscript, run a pre-submission check, simulate peer review, or wants a structured critique of their academic writing. Triggers on phrases like "review my paper", "pre-submission check", "referee report", "manuscript review", "check my paper before submission", or references to reviewing .qmd/.tex files targeting genetics or bioinformatics journals. Also use when the user mentions journal names like Nature Genetics, AJHG, Genome Biology, or similar.
---

# Pre-Submission Paper Review for Bioinformatics & Statistical Genetics

Run a rigorous 6-agent parallel review of an academic manuscript, simulating peer review at top genetics and bioinformatics journals.

## Phase 1: Parse Arguments, Discover the Paper, and Render

### 1.1 Parse `$ARGUMENTS`

Recognized journal names (case-insensitive):

- **Nature family**: `NatGenet`, `NatMethods`, `NatComms`, `NatMed`
- **Genetics**: `AJHG`, `HGGAdvances`
- **Genomics/Bioinformatics**: `GenomeBiology`, `GenomeRes`, `Bioinformatics`
- **Clinical/Neurology**: `MovementDisorders`, `Brain`

Parsing rules:
- If the first token of `$ARGUMENTS` matches a journal name, treat it as `TARGET_JOURNAL`; remaining text is the file path.
- If no match, treat the entire argument as a file path and set `TARGET_JOURNAL` to `top-field`.
- If `$ARGUMENTS` is empty, auto-detect both (no file path, `top-field`).

### 1.2 Discover the Manuscript

Search for the manuscript in this order:

1. If a path was provided, use it (file or directory).
2. Look for `_quarto.yml` in the current directory → Quarto project (read the yml to find chapter/section `.qmd` files).
3. Look for a single `.qmd` file in the current directory.
4. Fall back to `.tex` files: find the main file containing `\documentclass` or `\begin{document}`, then trace `\input{}`, `\include{}`, `\subfile{}`.

For Quarto projects, also check for:
- `_extensions/` directory (custom filters, formats)
- `references.bib` or similar bibliography files
- `_freeze/` directory (cached computations)

Build a complete file manifest:
- All `.qmd` or `.tex` source files and their roles
- Figure files: search `**/figures/**`, `**/Figures/**`, `**/fig/**`, `**/plots/**`, `**/output/**` for `.png`, `.pdf`, `.svg`, `.jpg`, `.jpeg`, `.eps`, `.tiff`
- Table files: search for `**/tables/**`, `**/Tables/**`, standalone table `.tex` or `.qmd` files
- Supplementary materials: search for `**/supplement*/**`, `**/supp*/**`, `**/extended_data/**`, `**/SI/**`, files matching `*supplement*`, `*supp_*`, `*extended*`, `*SI_*`
- Data files referenced in code chunks: `.csv`, `.tsv`, `.rds`, `.parquet` (note paths but don't read large data files)

Extract from the source:
- Paper title, authors, abstract
- YAML front matter (output format, bibliography, csl, crossref settings)

### 1.3 Auto-Detect Paper Type

Classify the paper into one or more categories based on content signals. Pass the classification to all agents.

| Category | Signals |
|---|---|
| **GWAS/Association** | Manhattan plot, QQ plot, `regenie`, PLINK, BOLT-LMM, SAIGE, summary statistics, genome-wide significance, lead SNPs, locus zoom, fine-mapping |
| **Survival/Penetrance** | Cox, Kaplan-Meier, hazard ratio, survival analysis, penetrance, age at onset, time-to-event, left truncation, prevalent cases |
| **Multi-omics** | proteomics, metabolomics, transcriptomics, differential expression, DESeq2, limma, Olink, pQTL, integration, Mendelian randomization |
| **Methods/Pipeline** | Nextflow, Snakemake, benchmarking, tool comparison, sensitivity/specificity, concordance, software, algorithm, container, Docker, Singularity |

A paper may be multiple types (e.g., GWAS + survival). Store as `PAPER_TYPES` list.

### 1.4 Attempt Rendering

Try to render the manuscript:

```bash
# For Quarto
quarto render <main-file-or-project-dir> --to html --execute-daemon 0

# If that fails, try with cache
quarto render <main-file-or-project-dir> --to html --cache

# If using _freeze, try without execution
quarto render <main-file-or-project-dir> --to html --no-execute
```

Record the outcome:
- **Success**: note the rendered HTML path; agents can reference it
- **Failure with cached output**: use `_freeze` or existing rendered files; flag in reproducibility report
- **Complete failure**: proceed with source-only review; flag prominently in reproducibility report as a critical finding

The rendering outcome is itself data for Agent 4 (Reproducibility).

## Phase 2: Launch 6 Review Agents in Parallel

Launch all 6 agents in a single message using the Agent tool with `subagent_type: "general-purpose"`. Pass each agent the complete file manifest, paper type classification, and target journal.

For agent-specific instructions, read the corresponding reference file before constructing the agent prompt:

| Agent | Reference File | Focus |
|---|---|---|
| Agent 1 — Copy Editing & Style | `references/agent1-copyediting.md` | Prose quality, NHST language abuse, journal style |
| Agent 2 — Internal Consistency | `references/agent2-consistency.md` | Cross-references, notation, numbers, main↔supplementary |
| Agent 3 — Claims & Identification | `references/agent3-claims.md` | Overclaiming, causal language, genetic epi threats, Gelman tenets |
| Agent 4 — Reproducibility & Methods | `references/agent4-reproducibility.md` | Pipeline docs, software versions, data access, rendering |
| Agent 5 — Figures, Tables & Code | `references/agent5-figures.md` | Genomics figure conventions, code chunk review, documentation |
| Agent 6 — Contribution & Referee | `references/agent6-contribution.md` | Novelty, replication, biological plausibility, journal fit |

Read each reference file and use its contents as the agent prompt, substituting `TARGET_JOURNAL`, `PAPER_TYPES`, file lists, and rendering outcome where indicated.

## Phase 3: Consolidate and Save

After all 6 agents return, consolidate into a single report saved to:

`PRE_SUBMISSION_REVIEW_[YYYY-MM-DD].md`

Report structure:

```markdown
# Pre-Submission Referee Report

**Paper**: [Title]
**Authors**: [Authors]
**Date**: [Today's date]
**Target Journal**: [TARGET_JOURNAL — if top-field, write "Leading Field Journal"]
**Paper Type**: [PAPER_TYPES, comma-separated]
**Rendering**: [Success / Partial (cached) / Failed — with brief explanation]

---

## Overall Assessment

[3–4 sentences: what the paper does, principal strength, single most critical issue.]

**Preliminary Recommendation**: [Send to referees as-is | Revise before submitting | Substantial revision required]

---

## 1. Copy Editing & Style
[Agent 1 output]

---

## 2. Internal Consistency & Cross-References
[Agent 2 output]

---

## 3. Claims & Identification Integrity
[Agent 3 output]

---

## 4. Reproducibility & Methods Transparency
[Agent 4 output]

---

## 5. Figures, Tables & Code Review
[Agent 5 output]

---

## 6. Contribution & Referee Assessment
[Agent 6 output]

---

## Priority Action Items

Triage hierarchy: identification and causal claims (Agent 3, Agent 6 Part 2) > missing required analyses (Agent 6 Part 3) > reproducibility failures (Agent 4) > internal inconsistencies (Agent 2) > figures/tables documentation (Agent 5) > style and grammar (Agent 1).

**CRITICAL** (must fix — could cause desk rejection):
1. ...

**MAJOR** (likely raised by referees):
2. ...

**MINOR** (polish):
3. ...
```

After saving, report:
1. Path to the saved report
2. Preliminary recommendation from Agent 6
3. Top 5 priority action items
4. Issue counts per category
