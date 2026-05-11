---
name: academic-writing-style
description: Use when the user asks to edit, revise, review, critique, or
  give feedback on existing academic manuscript prose — introductions,
  methods, results, discussions, abstracts, or any text destined for a
  journal paper or thesis. Trigger phrases include "edit this", "review
  this section", "tighten this paragraph", "give me feedback on", or "check
  this draft". This skill produces line-anchored suggestions only — it does
  not draft or rewrite prose. If the user asks for a draft, decline and ask
  them to write a first pass to review.
---

# Academic Manuscript Writing Style Guide

This skill encodes a specific academic writing voice derived from published work in computational statistics, statistical graphics, bioinformatics, and genomics. **Use it to review existing manuscript prose and propose suggestions — never to draft new prose in this voice.** If the user asks for a draft, decline and ask them to write a first pass that you can then review against this guide.

## Contents

- [How to Deliver Suggestions](#how-to-deliver-suggestions)
- [Core Voice](#core-voice)
- [Active Voice and Hedging](#active-voice-and-hedging)
- [Word Choice and Phrasing](#word-choice-and-phrasing)
- [Section-Specific Conventions](#section-specific-conventions)
- [Formatting Conventions](#formatting-conventions)
- [Editing Checklist](#editing-checklist)
- [Examples](#examples)

## How to Deliver Suggestions

This skill produces **suggestions, not edits**. Do not modify the manuscript file directly. Return a numbered list of proposed changes that the user can accept, reject, or adapt.

For each suggestion:

- **Anchor to the location** — file path and line number, or a short verbatim quote of the surrounding sentence.
- **Quote the original text** exactly.
- **Show the proposed text** exactly.
- **Cite the rule** from this guide that motivates the change (e.g., "stacked hedges", "passive voice", "vague quantifier", "in-recent-years cliché").

Example shape:

> **manuscript.qmd:47** — passive voice
> Original: "The analysis was performed on poly(A) libraries."
> Proposed: "We performed the analysis on poly(A) libraries."

For multi-sentence rewrites or paragraph-level restructuring, use fenced code blocks instead of inline. Group related suggestions by rule when there are many of the same kind.

If a stylistic question is genuinely a judgement call (e.g., "does this sentence overclaim?", "is this paragraph in the right place?"), flag it as a question rather than proposing a rewrite. The user makes the call.

## Core Voice

The writing voice is **precise, measured, and structurally clear**. Sentences tend to be moderately long but never sprawling — they carry one idea each with subordinate clauses used to add nuance or qualification. The tone is authoritative without being grandiose. Technical terms are used precisely but the prose remains accessible to a broad computational biology audience.

### Sentence-Level Patterns

- **Favor compound sentences joined by commas and conjunctions** over short choppy sentences. The natural rhythm alternates between longer explanatory sentences and shorter declarative ones.
- **Lead with the subject and main verb early.** Avoid burying the point in subordinate clauses. Example: "We have created a genomic DSL called plyranges that reformulates notions from existing genomic algebras" — the contribution appears immediately.
- **Use colons and dashes to introduce elaboration** rather than spawning a new sentence. Example: "This is certainly true in high-throughput biological data science, where constraints on computation time and memory, in addition to the analyst's time, makes EDA difficult."
- **Vary sentence openers.** Mix subject-first sentences with occasional prepositional phrases, adverbial clauses, or participial phrases. Avoid starting more than two consecutive sentences the same way.

### Paragraph Structure

- **Topic sentence first, then evidence/elaboration, then implication.** This pattern is consistent throughout.
- **Paragraphs tend to be 4–8 sentences.** They develop a single idea fully before moving on.
- **Transitions between paragraphs are often implicit** through logical flow rather than heavy-handed connectors like "Furthermore" or "Additionally." When explicit transitions appear, they tend to be short: "To verify this," or "Similarly," or "In contrast."

## Active Voice and Hedging

### Use Active Voice by Default

The user's existing writing already uses active voice well in many places ("We have created," "We observe," "We propose"). **Flag passive constructions and propose active replacements.**

**Suggest these substitutions:**
- "It was observed that..." → "We observed..."
- "The analysis was performed on..." → "We performed the analysis on..."
- "Genes were detected as..." → "We detected genes as..."
- "The data is modelled by..." → "We model the data with..."

**Acceptable passive:** Passive voice is fine in Methods when the agent is obvious or irrelevant ("Reads were aligned to hg38 using subjunc"), and in describing existing tools/standards ("The GRanges class is defined in...").

### Eliminate Over-Hedging

The writing sometimes stacks hedges unnecessarily. Reduce hedging to a single qualifier per claim, and only when genuinely uncertain.

**Over-hedged (avoid):**
- "It is possible that this may suggest..."
- "This could potentially indicate..."
- "It seems likely that there might be..."
- "We believe that it is perhaps the case that..."

**Appropriately hedged:**
- "This suggests..."
- "This likely reflects..."
- "We expect that..."
- "One explanation is..."

**When to hedge:** Hedge when the evidence is indirect, when extrapolating beyond the data, or when presenting one of several possible interpretations. Do not hedge when reporting direct observations or established facts.

**Strong statements for strong evidence:**
- Use "We show that..." or "We demonstrate that..." when presenting direct results
- Use "We find that..." for empirical observations
- Use "This indicates..." when the evidence is clear
- Reserve "suggests" and "is consistent with" for genuinely uncertain interpretations

## Word Choice and Phrasing

### Preferred Patterns

- **"We have [past participle]"** for introducing contributions: "We have created," "We have aimed for"
- **"This [verb]s..."** for drawing implications from results
- **"The [noun] is [adjective]"** for establishing context before elaborating
- **"By [gerund], ..."** for explaining mechanism: "By recognizing that the GRanges class follows tidy data principles, we create..."
- **Use analogies to explain technical relationships:** "By analogy, plyranges is to the genomic algebra, as dplyr is to the relational algebra."

### Clichés and Filler to Flag

Flag any of these and propose the replacement:
- "In recent years" → Be specific about the timeframe or just state the trend
- "It is well known that" → Just state the fact
- "To the best of our knowledge" → "No prior work has..." or just state the novelty
- "A plethora of" → "Many" or "Several" or give a number
- "Plays a crucial/pivotal/key role" → "Contributes to" or "Drives" or "Is required for"
- "Sheds light on" → "Clarifies" or "Reveals"
- "Paves the way for" → "Enables" or "Opens possibilities for"
- "A growing body of evidence" → Cite the evidence directly
- "Robust and reliable" → Pick one, or better, explain what makes it so
- "Novel" (unless genuinely novel) → Describe what is new specifically
- "Utilize" → "Use"
- "Facilitate" → "Enable" or "Allow"
- "Leverage" → "Use" or "Exploit"
- "Paradigm" → Almost never needed

### Preferred Vocabulary

- "Coherent" over "holistic"
- "Straightforward" over "trivial"
- "Examine" or "Investigate" over "Explore" (reserve "explore" for EDA contexts where it is literal)
- "Integrate" (fine — used precisely in the genomics sense)
- "Complementary" over "synergistic"
- "Motivates" over "drives" for intellectual justification
- "Concise" or "expressive" over "elegant" (unless describing math)

## Section-Specific Conventions

### Introduction

- **Open with the broad problem**, narrowing to the specific gap over 3–5 paragraphs.
- **Literature review is woven into the narrative**, not dumped in a block. Each cited work appears at the point where it is relevant.
- **End with a clear statement of what this paper does**, structured as: "In this paper, we [verb] [contribution]. We [show/demonstrate/find] [key result]."
- **Provide a roadmap paragraph** at the end when the paper has multiple components: "The rest of the paper is organised as follows."

### Methods

- **Present methods in the order they appear in Results.**
- **Name datasets clearly** with italicized short names and full descriptions (organism, cell type, library prep, accession number).
- **Explain statistical choices** — don't just list methods. Briefly justify why a particular approach was chosen.
- **Write formulas inline** when they are simple; display them when they need to be referenced.

### Results

- **Each subsection tells a mini-story:** observation → evidence → interpretation.
- **Figure references are woven into the prose**, not parenthetical afterthoughts. Example: "Samples cluster by experimental and biological groups in intron MDS plots across all datasets (Figure 1D) indicating that intron reads are informative."
- **Quantitative claims always include numbers.** Don't say "a significant proportion" — say "approximately 7% of reads" or "roughly 2.1 million reads per library."
- **Use present tense for general truths** and results that hold: "Intron reads are informative." Use past tense for specific procedures: "We examined intron and exon read counts."

### Discussion

- **Open by restating the key finding** in a sentence or two, without the preamble.
- **Organize by theme, not by recapitulating Results in order.**
- **Discuss limitations concretely** — name the specific limitation, explain its impact, and if possible suggest how future work could address it.
- **Connect to the broader field** in the final paragraphs, but stay grounded. Don't overclaim.

### Abstract

- **Structure:** Background (1–2 sentences) → Gap/Problem (1 sentence) → What we did (1–2 sentences) → Key results (2–3 sentences) → Significance (1 sentence).
- Keep under 250 words.
- No citations in the abstract.
- Use active voice throughout.

## Formatting Conventions

- **Software names** in bold: **plyranges**, **limma**, **edgeR**
- **Data structures** in italics: *GRanges*, *SummarizedExperiment*
- **Gene names** in italics: *PSMB7*, *EIF2S3*
- **Oxford comma:** Yes, always.
- **British spelling** (organisation, visualisation, colour) — consistent with Australian academic conventions.
- **Numbers:** Spell out one through nine; use numerals for 10+. Always use numerals with units.
- **Em dashes** with no spaces for parenthetical asides — like this — used sparingly.
- **Serial semicolons** for complex lists where items contain commas.

## Editing Checklist

When editing manuscript text, check for and fix:

1. **Passive voice** — convert to active unless in Methods describing standard procedures
2. **Stacked hedges** — reduce to one qualifier maximum per claim
3. **Vague quantifiers** — replace with actual numbers
4. **Cliché phrases** — replace with specific, concrete language
5. **Paragraph coherence** — does each paragraph have a clear topic sentence and develop a single idea?
6. **Sentence variety** — are there three or more sentences in a row with the same structure?
7. **Transition logic** — does the paragraph flow naturally from the previous one without needing "Furthermore" or "Moreover"?
8. **Figure integration** — are figures referenced naturally within the argument, not bolted on?
9. **Overclaiming** — does every claim match the strength of the evidence?
10. **Redundancy** — are there sentences that repeat what was just said in slightly different words?

## Examples

### Target voice (illustrative)

The two paragraphs below show what to flag and what the target voice looks like. The "After" is what the user would write when they have the supporting facts — it is **not** a rewrite the skill should propose, because the skill cannot invent numbers (here, "roughly 7%" and "21%") that are not in the original. Use it as a mental model of the destination, not as a template to produce.

**Before (over-hedged, passive, cliché-heavy):**

"In recent years, it has been increasingly recognized that intron reads may potentially play a role in RNA-seq analysis. It is possible that these reads could be utilized to shed light on transcriptional dynamics. A growing body of evidence suggests that intron signal might be informative, though further investigation is needed to fully elucidate the extent to which this is the case."

**After (matches target style):**

"Intron reads account for a significant proportion of RNA-seq libraries — roughly 7% in poly(A) and 21% in total RNA preparations — yet standard analyses discard them. We show that these reads carry biological signal: samples cluster by experimental group in MDS plots of intron counts alone, with comparable separation to exon-based analyses. The majority of intron reads originate from pre-mRNA, but among them we identify genes with coverage profiles consistent with intron retention."

### A real suggestion against the Before paragraph

For the same paragraph, a proposable suggestion list looks like:

> **L1** — "in recent years" cliché
> Original: "In recent years, it has been increasingly recognized that…"
> Proposed: drop the opening clause; rewrite the sentence to start with the substantive claim. **Need from user:** what timeframe or evidence motivates "increasingly recognized"?

> **L1** — passive voice + stacked hedge
> Original: "it has been increasingly recognized that intron reads may potentially play a role"
> Proposed: "intron reads contribute to RNA-seq signal" (drops "may potentially", makes the verb concrete). Confirm the strength of claim is supported.

> **L2** — "utilize" → "use", "shed light on" cliché
> Original: "could be utilized to shed light on transcriptional dynamics"
> Proposed: "reveal transcriptional dynamics" (or "inform", depending on the strength of evidence).

> **L3** — "a growing body of evidence" without citation, stacked hedge "might be… needed to fully elucidate"
> Original: "A growing body of evidence suggests that intron signal might be informative, though further investigation is needed to fully elucidate the extent to which this is the case."
> Proposed: cite the specific prior work directly, then state your own claim. **Question for user:** which references support "growing body of evidence"? Without them, the sentence should be deleted rather than rephrased.
