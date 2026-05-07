---
name: interview-me
description: Interactive interview to formalize a research idea into a structured specification — biology/prior, cohort, comparator, threats to inference, sensitivity analyses. Tuned to statistical genetics and genetic epidemiology, but works for any quantitative analysis.
disable-model-invocation: true
argument-hint: "[brief topic or 'start fresh']"
allowed-tools: ["Read", "Write"]
---

# Research Interview

Conduct a structured interview to help formalize a research idea into a concrete specification.

**Input:** `$ARGUMENTS` — a brief topic description or "start fresh" for an open-ended exploration.

---

## How This Works

This is a **conversational** skill. Instead of producing a report immediately, you conduct an interview by asking questions one at a time, probing deeper based on answers, and building toward a structured research specification.

**Do NOT use AskUserQuestion.** Ask questions directly in your text responses, one or two at a time. Wait for the user to respond before continuing.

---

## Interview Structure

### Phase 1: The Big Picture (1-2 questions)
- "What phenomenon or puzzle are you trying to understand?"
- "Why does this matter? Who should care about the answer?"

### Phase 2: Prior Knowledge (1-2 questions)
- "What's known so far — biology, mechanism, prior findings? Where does this sit in the literature?"
- "What's your prior on what we'll find, and how strong is it? What would surprise you?"

### Phase 3: Data and Cohort (2-3 questions)
- "What cohort or biobank — UKB, GEL, AoU, FinnGen, in-house, meta-analysis?"
- "Ancestry composition, sample size, and case count? Discovery cohort and replication cohort?"
- "Phenotype source — ICD/HES, primary care, self-report, biomarker, imaging? Genotyping/sequencing platform if relevant?"

### Phase 4: Inference and Confounding (2-3 questions)
- "What's the comparator group, and how is it defined? What's the case definition?"
- "What's the causal or biological model — direct effect, mediation, pleiotropy, instrument?"
- "Threats to inference — population stratification, ascertainment, batch effects, survivorship, winner's curse, reverse causation? Which one worries you most?"

### Phase 5: Expected Results (1-2 questions)
- "What would you expect to find? What effect size is plausible given prior literature?"
- "What would the results imply biologically or clinically? What would change in how the field thinks?"

### Phase 6: Contribution (1 question)
- "How does this differ from what's already been done? What's the gap you're filling?"

---

## After the Interview

Once you have enough information (typically 5-8 exchanges), produce a **Research Specification Document**:

```markdown
# Research Specification: [Title]

**Date:** [YYYY-MM-DD]
**Researcher:** [from conversation context]

## Research Question

[Clear, specific question in one sentence]

## Motivation

[2-3 paragraphs: why this matters, prior biology/literature, biological or clinical relevance]

## Hypothesis

[Testable prediction with expected direction]

## Empirical Strategy

- **Design:** [e.g., case-control GWAS, cohort survival, two-sample MR, family-based association, PheWAS]
- **Exposure / variant / phenotype:** [What varies across units]
- **Outcome:** [What is measured]
- **Comparator:** [Case definition and control definition; or exposed vs unexposed]
- **Threats to inference:** [Population stratification, ascertainment, batch, survivorship, winner's curse, reverse causation — and how each is addressed]
- **Sensitivity analyses:** [Ancestry-stratified, leave-one-out, MR pleiotropy checks, etc.]

## Data

- **Cohort(s):** [Discovery + replication; biobank or study name]
- **Ancestry composition:** [European / multi-ancestry / specific group; relevance for portability]
- **Phenotype source:** [ICD/HES, primary care, biomarker, imaging, self-report]
- **Genotyping / sequencing:** [Array + imputation panel, WES, WGS, depth]
- **Sample size:** [N total, N cases, N controls; effective sample size if relevant]

## Expected Results

[What the researcher expects to find and why]

## Contribution

[How this advances the literature — 2-3 sentences]

## Open Questions

[Issues raised during the interview that need further thought]
```

**Save to:** `session_logs/[YYYY-MM-DD]_research-spec_[sanitized_topic].md`

---

## Interview Style

- **Be curious, not prescriptive.** Your job is to draw out the researcher's thinking, not impose your own ideas.
- **Probe weak spots gently.** If the identification strategy sounds fragile, ask "What would a skeptic say about...?" rather than "This won't work because..."
- **Build on answers.** Each question should follow from the previous response.
- **Know when to stop.** If the researcher has a clear vision after 4-5 exchanges, move to the specification. Don't over-interview.
