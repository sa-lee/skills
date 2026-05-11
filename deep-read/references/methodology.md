# Why deep-read works the way it does

Reference material for humans. SKILL.md contains the actual instructions.

## Contents

- [Two distinct problems with one-shot PDF reading](#two-distinct-problems-with-one-shot-pdf-reading)
- [Why image-based reading is the default](#why-image-based-reading-is-the-default)
- [Why 4-page chunks, 3 at a time](#why-4-page-chunks-3-at-a-time)
- [Why pause-and-confirm](#why-pause-and-confirm)
- [Why pypdf (and why pypdfium2 for the text-only path)](#why-pypdf-and-why-pypdfium2-for-the-text-only-path)
- [Why exhaustive FOCUS extraction](#why-exhaustive-focus-extraction)
- [Limitations](#limitations)

## Two distinct problems with one-shot PDF reading

Claude can read PDFs and has a large context window, so in principle a 40-page paper
should fit. In practice, two failure modes appear:

**1. Hard failure: "prompt too long".** PDFs are containers for fonts, vector graphics,
embedded images, multi-column layouts, and math. The Read tool renders pages as images
for the vision model. A long PDF combined with the rest of the conversation context can
exceed the input limit. When it does, the session is unrecoverable — context is lost.

**2. Soft failure: shallow comprehension.** Even when the PDF doesn't trigger a hard
failure, attention degrades over long single-document inputs. The model attends carefully
to the start and end and skims the middle. The result: catches the abstract and intro,
gets fuzzy on methods, hallucinates or misses results-section detail. Splitting addresses
both: every chunk gets the model's full attention, and incremental note-writing externalises
understanding before it can decay.

## Why image-based reading is the default

For bioinformatics and statistical genetics papers, the visual content carries real
information:

- **Manhattan plots, QQ plots** — peak structure and inflation are not in the text
- **Forest plots** — effect-size patterns across cohorts/strata
- **Locus zoom plots** — fine-mapping evidence, LD structure
- **Heatmaps** — expression patterns, co-localization
- **Single-cell UMAPs** — population structure
- **Pathway / network diagrams** — mechanism

Text-only extraction loses all of this. Even tables — common for top loci or replication
results — frequently extract poorly with rule-based parsers. The benchmark literature is
clear that *all* rule-based PDF parsers underperform on scientific documents specifically,
because they extract math symbolically and break on multi-column layouts.

The text-only fast path exists for prose-only papers — perspectives, theory, commentary —
where there is genuinely nothing visual worth seeing. It's a deliberate opt-in, not a
default.

## Why 4-page chunks, 3 at a time

**Four pages per chunk:** small enough that attention stays uniform across the chunk;
large enough that logical sections (a methodology subsection, a results table with
discussion) usually stay together. A 40-page paper splits into 10 chunks.

**Three chunks per Read batch (~12 pages):** this is the largest chunk count that
empirically stays well below the per-call context budget for image-rendered PDFs while
giving the model enough material to integrate (e.g., a results figure with its caption
plus the discussion paragraph that interprets it). One chunk at a time would be too
fragmented; six would risk hitting limits.

## Why pause-and-confirm

The pause between batches is functional, not procedural:

- **Catches errors before they compound.** If the model misreads the methods, you fix it
  before the results section gets interpreted on the wrong premise.
- **Lets the user redirect.** "Skip the discussion, focus on the supplement methods."
- **Keeps context bounded.** A standalone invocation that reads 30 pages of images is
  already heavy; explicit user gates prevent the parent context from drifting toward the
  hard failure threshold.

For subagent invocations the pause is dropped — there's no interactive user, and the
subagent's context is isolated from the parent.

## Why pypdf (and why pypdfium2 for the text-only path)

**Splitting:** pypdf and PyPDF2 are essentially identical in performance for splitting
because splitting is just copying page objects between containers — no glyph parsing.
The reason to switch is that PyPDF2 is deprecated (renamed to pypdf in 2022 and no longer
maintained). API is essentially unchanged.

**Text extraction (fast path only):** pypdfium2 is the fastest open-source extractor in
the py-pdf benchmarks (Apache/BSD-licensed, wraps Google's PDFium). PyMuPDF is comparably
fast but AGPL — fine for personal use, awkward for distribution. pdfplumber is much
slower and pdfminer.six is slower still. For our use case (whole-paper extraction to
markdown for LLM consumption) pypdfium2's speed and license are the right tradeoffs;
extraction quality differences vs PyMuPDF are minor for plain text.

## Why exhaustive FOCUS extraction

The default LLM summary is a lossy compression — it strips the specifics that make a
paper actionable: the exact MAF cutoff, the software version, the GEO accession, the
effect size of the lead variant. For statistical genetics work specifically, those
specifics are the entire point; without them the summary tells you a paper exists but
not whether you can build on it or replicate it.

FOCUS-style extraction is verbose by design. The numbered, section-by-section structure
makes it scannable; the embedded direct quotes preserve the language where it matters
(definitions, claims with legal/clinical weight, careful hedges). The dedicated
Statistical Methods and Reproducibility sections force the model to consolidate
information that papers often scatter across Methods, Supplementary, and Data Availability
statements.

## Limitations

- **Slow.** A 40-page paper requires 4 batches with user confirmation between each.
  Budget 15–20 minutes wall clock.
- **Expensive in tokens.** Image-rendered pages dominate the cost. Use the text-only
  path when you can.
- **Notes can become repetitive** if a paper revisits themes (common in long Discussion
  sections). The final FOCUS pass deduplicates, but some manual editing may help.
- **Math and complex tables degrade in the text-only path.** Use image-based reading for
  any paper where these matter.
- **Assumes the paper is worth reading carefully.** For triage — deciding whether a paper
  is relevant — read just the first split (pages 1-4, abstract + intro) without invoking
  this skill.
