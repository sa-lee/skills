# Audit Report Template

The main session writes the audit report to:

- `session_logs/YYYY-MM-DD_analysis-review_<topic>.md` (if root-level
  `session_logs/` exists)
- `docs/session_logs/YYYY-MM-DD_analysis-review_<topic>.md` (if that
  convention is used instead)

`<topic>` is sanitised from the spec source: lowercase, alphanumerics
and hyphens only. If unclear, use `audit`.

## Contents

- [Schema](#schema)
- [Overall Assessment](#overall-assessment)
- [Phase 1 — Static Audit](#phase-1--static-audit)
- [Phase 2 — Simulation-Recovery](#phase-2--simulation-recovery)
- [Open items](#open-items)
- [Hand-off](#hand-off)

## Schema

```markdown
# Analysis Audit: [topic]

**Date:** YYYY-MM-DD
**Project:** [absolute path or repo name]
**Spec source:** [PLAN.md path | session log path | "free-text: <quoted question>"]
**Repo flavour:** [paper-analysis | R-package | pipeline-only]
**Paper draft:** [path, or "none"]

---

## Overall Assessment

[3-4 sentences: what was audited, principal strength, single most critical issue.]

**Status:** [Clean for paper write-up | Revise before write-up | Substantial revision needed]

---

## Phase 1 — Static Audit

### Agent A — Sample, Phenotype, Variable Construction

[Paste Agent A's full output verbatim here.]

---

### Agent B — Model Specification & Inference

[Paste Agent B's full output verbatim here.]

---

### Agent C — Output Provenance & Reproducibility

[Paste Agent C's full output verbatim here.]

---

### Consolidated Priority

Triage rule: data-side wrongness (Agent A CRITICAL) outranks model-side
wrongness (Agent B CRITICAL) outranks reproducibility (Agent C). Within a
severity tier, prefer the finding that affects the most downstream outputs.

**CRITICAL:**
1. ...

**MAJOR:**
2. ...

**MINOR:**
3. ...

---

## Phase 2 — Simulation-Recovery

**Transformation under test:** `function_X` in `R/foo.R:LINE`

**Why this one:** [one sentence — why it's load-bearing for the manuscript]

**Truth specification:** [stated explicitly — input property, expected output property, tolerance]

**Tolerance:** [e.g., relative 1% across N=100 replicates; or 95% CI covers truth in ≥90% of replicates]

**Simulator location:** [`scripts/sim_recover_X.R` or `tests/testthat/test-X.R`]

**Result:** [PASSED | FAILED-CODE | FAILED-SIMULATOR | ACCEPTABLE-MISMATCH | ABORTED]

**Recovery figure:** ![](figures/sim_recover_X.pdf)

[Diagnosis paragraph if mismatch.]

---

## Open items

- [Phase 1 findings not addressed this session]
- [Other transformations that should be simulation-recovered next]
- [Threats to inference flagged but not investigated]

---

## Hand-off

[Paste recommended next skill from references/handoff-table.md.]
```
