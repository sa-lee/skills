# deep-read

A Claude skill for rigorous, detail-preserving reading and summarization of academic
PDFs — especially in bioinformatics, statistical genetics, and related fields.

Combines a batched, image-based reading mechanism with the FOCUS output format from
[Lin (2025), *Nature Biotechnology*](https://doi.org/10.1038/s41587-025-02947-8).

## What it does

Long academic PDFs blow up Claude's context when read all at once, and even when they
fit, attention degrades and details get hallucinated or skipped. `deep-read` solves this
with a two-part approach:

**Reading mechanism.** Splits PDFs into 4-page chunks (using `pypdf`), reads 3 at a time
via the Read tool with pause-and-confirm between batches, accumulating structured working
notes. Image-based by default so figures, plots, and complex tables aren't lost. A
text-only fast path (`pypdfium2`) is available for prose-heavy papers.

**Output format.** Produces a FOCUS-style summary: YAML frontmatter, a 3–6 sentence
overview, then a numbered, section-by-section extraction with embedded direct quotes and
specific details (effect sizes, sample sizes, accessions, software versions). Always
includes dedicated **Statistical Methods** and **Reproducibility** sections.

## What's different from the originals

This skill merges two earlier skills (`focus` and `split-pdf`) and refactors for
bio/genetics use:

- `pypdf` instead of deprecated `PyPDF2`
- `pypdfium2` text-only fast path for prose-heavy papers (Apache/BSD licensed)
- Skip-split path for short PDFs (<15 pages)
- Bio/genetics extraction scaffolding (cohorts, ancestry, biobanks, accessions, software
  versions, effect sizes) replacing the original economics-flavored 8-dimension extract
- FOCUS becomes the output format; structured extraction is internal scaffolding only
- Always reads supplementary PDFs found in the same folder
- Local PDF inputs only (no web search or DOI lookup)
- Subagent isolation preserved for use within lit-review workflows

## Installation

Add the `deep-read` folder to your Claude skills directory, or zip it as a `.skill` file
and install via [customize/skills](https://claude.ai/customize/skills).

```sh
cd path/to/this/folder
zip -r deep-read.skill SKILL.md references/
```

## Dependencies

Installed automatically on first use:

- `pypdf` — PDF splitting (replaces deprecated PyPDF2)
- `pypdfium2` — text extraction for the fast path

## Usage

Trigger with any of:

- `/deep-read` (with a local PDF path)
- "Deep read this paper: /path/to/paper.pdf"
- "FOCUS summary of /path/to/paper.pdf"
- "Summarize this paper exhaustively"

Add `--text-only` (or say "text only") for prose-heavy papers without important figures.

The skill takes **local PDF paths only**. It does not search the web or download from
DOIs — provide the file yourself.

## Output

Two files are produced and retained:

- `<basename>_focus.md` — the final FOCUS summary, alongside the source PDF
- `<folder>_build/split_<basename>/notes.md` — working notes used during reading

The `_focus.md` file has YAML frontmatter (title, authors, year, journal, DOI), an
overview, then numbered FOCUS-format sections mirroring the paper structure plus
dedicated Statistical Methods and Reproducibility sections.

## What this skill is not

- Not a triage tool. For deciding whether to read a paper, just read the first split
  (pages 1–4) without invoking this.
- Not a web search or DOI resolver. Bring your own PDF.
- Not a high-level abstract rewriter. The output is exhaustive by design.

## Attribution

The FOCUS output format is from:

> Lin, Z. FOCUS: an AI-assisted reading workflow for information overload.
> *Nat. Biotechnol.* **43**, 2070–2075 (2025). https://doi.org/10.1038/s41587-025-02947-8

The batched reading mechanism, build directory convention, and subagent isolation
protocol are adapted from the `split-pdf` skill (Stephen Turner, with improvements by
Ben Bentzin, 2026).

## License

MIT
