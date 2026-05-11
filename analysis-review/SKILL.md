---
name: analysis-review
description: Use when the user asks to audit, referee, or check a
  bioinformatics or statistical genetics analysis pipeline before writing
  it up — phrases like "audit my analysis", "referee my pipeline", "check
  my code before I write this up", or before invoking paper-review on a
  finished manuscript. Sibling to paper-review (which audits the manuscript
  prose, not the code).
argument-hint: "[path-to-spec | free-text question | empty for auto-discover]"
allowed-tools: Read, Glob, Grep, Bash(ls:*), Bash(git status:*), Bash(git log:*), Bash(Rscript -e "renv::status()"), Bash(Rscript scripts/*:*), Bash(Rscript tests/*:*), Write, Agent
---

# Analysis Review

Code-level pre-paper audit. Sibling to `paper-review`. Two phases:
parallel static audit (Phase 1) followed by interactive simulation-recovery
(Phase 2).

## Contents

- [Phase 0: Discovery](#phase-0-discovery)
- [Phase 1: Parallel static audit](#phase-1-parallel-static-audit)
- [Phase 2: Interactive simulation-recovery](#phase-2-interactive-simulation-recovery)
- [Phase 3: Hand-off](#phase-3-hand-off)
- [Constraints](#constraints)

## Phase 0: Discovery

### 0.1 Parse `$ARGUMENTS`

Resolve the spec source:

- `$ARGUMENTS` empty → auto-discover, in order:
  1. `PLAN.md` at repo root
  2. Most recent `session_logs/*.md`, then `docs/session_logs/*.md`
  3. If neither exists, ask the user to state the research question
- `$ARGUMENTS` is a path that resolves to an existing file → read as spec
- Otherwise → treat as free-text research question; quote verbatim into
  the audit report's `Spec source:` frontmatter

Set `SPEC_SOURCE` (the actual content) and `SPEC_LABEL` (short label
for the report frontmatter).

### 0.2 Detect repo flavour

Set `REPO_FLAVOUR`:

- `R-package` if `DESCRIPTION` and `NAMESPACE` exist at the repo root.
- `paper-analysis` else if `PLAN.md` exists at the repo root, OR `_targets.R`
  exists, OR a `paper.qmd` / `_quarto.yml` exists.
- `pipeline-only` otherwise.

### 0.3 Build manifests

- `CODE_MANIFEST`: glob for `R/**/*.R`, `scripts/**/*.{R,py,sh}`,
  `_targets.R`, `_targets_packages.R`, `src/**/*.{cpp,c}`. List paths
  relative to repo root.
- `OUTPUT_MANIFEST`: glob for files under `figures/`, `Figures/`, `tables/`,
  `Tables/`, `output/`, `results/`, plus `_targets/objects/` listing if
  present.
- `PAPER_DRAFT_PATH`: search for `paper.qmd`, `paper.tex`, `_quarto.yml`,
  or any `.tex` file containing `\documentclass`. If multiple, pick the
  most recently modified. If none, set to `"none"`.

### 0.4 Determine session log path

Look for an existing convention:

- If `session_logs/` exists at repo root, use it.
- Else if `docs/session_logs/` exists, use it.
- Else create `session_logs/` at repo root and use it.

Compose the report path:
`<session_log_dir>/YYYY-MM-DD_analysis-review_<topic>.md`

`<topic>` is the spec label, sanitised: lowercase, alphanumerics and
hyphens only, max 40 chars. Default to `audit` if no clear topic.

### 0.5 Confirm with user

Before launching agents, briefly state in 3-5 lines what you found:

- Spec source + one-line interpretation
- Repo flavour + main directories
- Whether a paper draft was found
- Where the audit report will be written

Wait for user confirmation. If they push back on the spec interpretation,
clarify before proceeding.

## Phase 1: Parallel static audit

### 1.1 Read agent reference files

Read all three:

- `references/agentA-sample-phenotype.md`
- `references/agentB-model-inference.md`
- `references/agentC-provenance-reproducibility.md`

### 1.2 Construct agent prompts

For each agent, the prompt is the **full text of the reference file**, with
input variables substituted. Substitution targets in each reference file:

- `PROJECT_PATH`
- `SPEC_SOURCE`
- `REPO_FLAVOUR`
- `CODE_MANIFEST`
- `OUTPUT_MANIFEST` (Agent C only)
- `PAPER_DRAFT_PATH`

Render these as a `## Context` block prepended to the reference content
when constructing the agent prompt — do not edit the reference file.

### 1.3 Dispatch all three agents in ONE message

Use the `Agent` tool with `subagent_type: "general-purpose"` for each.
**Send all three Agent tool calls in a single assistant message** so they
execute in parallel. Per-agent settings:

- Agent A and B: read-only — do not grant Bash beyond `Bash(ls:*)`.
- Agent C: also gets `Bash(Rscript -e "renv::status()":*)`,
  `Bash(git status:*)`, `Bash(git log:*)`.

Each agent's `description` field for telemetry: `"analysis-review Agent
[A|B|C]"`. Include `PROJECT_PATH`, `REPO_FLAVOUR`, and the spec label in
the prompt header so the agent has orientation context.

### 1.4 Consolidate findings

After all three return:

1. Read `references/report-template.md`.
2. Construct the audit report by substituting Phase 1 sections with each
   agent's output verbatim (under `### Agent A Findings`, etc.).
3. Build the **Consolidated Priority** section. Triage rule:
   - All Agent A CRITICALs first.
   - Then Agent B CRITICALs.
   - Then Agent C CRITICALs.
   - Then MAJORs from each, in the same order.
   - Then MINORs.
   - Within a tier, prefer findings affecting more downstream outputs
     (cross-reference via grep).
4. Write the **Overall Assessment** (3-4 sentences) and set **Status**.
5. Write the report to the path determined in Phase 0.4. Do **not** include
   a Phase 2 section yet.

### 1.5 Pause and present

Show the user:

- The path the draft was written to.
- A 5-line summary: counts of CRITICAL / MAJOR / MINOR per agent.
- The list of **load-bearing transformation candidates** extracted from
  Agents A and B (these are flagged in their output under that heading).

Ask the user to either:

a) Pick one candidate for Phase 2.
b) Name their own transformation.
c) Skip Phase 2 (jump to hand-off).

## Phase 2: Interactive simulation-recovery

If the user picked (c) skip, jump to Phase 3 (Hand-off) below.

Otherwise, walk through the following with the user. **One transformation
per Phase 2 invocation.**

### 2.1 Lock the transformation

State explicitly: "We are testing whether `function_X(input)` correctly
produces `output_Y` when truth is known." Get user's confirmation in one
exchange before writing any code.

### 2.2 Co-write truth specification

Ask the user, one question at a time:

1. What property of the input gives a known answer? (e.g., "every individual
   has true HR = 2.0").
2. What does correct recovery look like? (e.g., "Cox fit recovers
   log(HR) = 0.693 ± 0.05 in 95% of replicates").
3. What tolerance counts as PASSED?

Defaults if the user says "use defaults":

- Continuous parameter recovery: 1% relative error, N=100 replicates.
- CI coverage: nominal level (95% CI covers truth in ≥90% of replicates).
- Exact transformations (deduplication, encoding): equality.

Record the truth specification and tolerance — they go in the audit report.

### 2.3 Write the simulator

Save location depends on `REPO_FLAVOUR`:

- `R-package` → `tests/testthat/test-<transformation>.R`
- `paper-analysis` or `pipeline-only` → `scripts/sim_recover_<transformation>.R`

Structure of the simulator:

```r
# Header: what's being tested, truth spec, tolerance
# 1. Generate input data with known property baked in
# 2. Apply the actual pipeline function — DO NOT reimplement
# 3. Repeat over N replicates
# 4. Summarise recovery (mean estimate, CI coverage, MSE)
# 5. Render figure: pred-vs-truth scatter, recovery distribution, or QQ
```

If the function depends on upstream functions, mock the **inputs only**.
Never mock the function under test — the user's CLAUDE.md anti-pattern
"tests that exercise the mock instead of the code" applies.

### 2.4 Run and check

Execute the simulator. Capture:

- Numerical recovery summary.
- The figure (file path).

Compare to tolerance. Show the user the figure ("visualisation as
verification" — do not summarise; render and look).

### 2.5 Diagnose if mismatch

Three branches:

- **Code is wrong.** Bug in the pipeline function. Record fix proposal,
  do not fix in this session — file as a follow-up.
- **Simulator is wrong.** Truth spec from 2.2 was incorrect. Revise and
  re-run from 2.3.
- **Acceptable mismatch.** Expected bias under a known assumption.
  Document why explicitly.

### 2.6 Append to audit report

Append the **Phase 2** section to the report at the path from Phase 0.4.
Use the schema in `references/report-template.md`. Embed the figure with a
relative path.

## Phase 3: Hand-off

Read `references/handoff-table.md`. Select the row that matches the
Phase 1 + Phase 2 outcomes. Append the **Hand-off** section to the audit
report and state the recommendation in chat.

Do not auto-invoke the next skill — the user invokes it explicitly.

## Constraints

- Single combined audit report — Phase 1 and Phase 2 (if run) live in one
  file at `<session_log_dir>/YYYY-MM-DD_analysis-review_<topic>.md`.
- Phase 1 agents are read-only static analysis (Agent C has the small
  status-command exception).
- Phase 2 is one transformation only. To test more, re-invoke.
- Never edit production code in this skill. Findings and fix proposals
  only — fixing happens in a follow-up session, often via `r-package-tdd`
  or `superpowers:systematic-debugging`.
