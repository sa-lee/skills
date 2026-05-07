# Hand-off Decision Table

After writing the audit report, the main session selects one row from this
table and includes its recommendation as the report's final section.

| Situation | Recommend |
|---|---|
| CRITICAL findings unaddressed | Pause; fix the analysis, then re-run `/analysis-review`. Do not invoke any other skill. |
| MAJOR findings, fix is code-shaped, repo is R package | `r-package-tdd` to fix with proper test coverage. |
| MAJOR findings, fix is code-shaped, repo is paper-analysis or pipeline-only | Main session — fix directly, with simulation-recovery as the verification step. |
| Phase 2 result is FAILED-CODE | `superpowers:systematic-debugging` to root-cause the mismatch before fixing. |
| Phase 1 clean + Phase 2 PASSED + paper draft exists | `paper-review` for the prose-level pre-submission referee. |
| Phase 1 clean + Phase 2 PASSED + no paper draft | Begin manuscript drafting; invoke `academic-writing-style` when ready. |
| More load-bearing transformations should be tested | Re-invoke `/analysis-review` with a different focus argument. |
| Open questions in design | `superpowers:brainstorming`. |

## Reasoning

- The hand-off is conservative: if there are CRITICAL findings, no other
  skill is recommended. The fix must come first.
- `r-package-tdd` is only recommended for R packages because its testthat
  workflow assumes that structure.
- For paper-analysis or pipeline-only repos, the fix is in-session because
  there's no formal test suite to extend; the simulation-recovery from
  Phase 2 is the verification proxy.
- `paper-review` is the natural sibling-after step once the analysis is
  clean and a manuscript exists.
