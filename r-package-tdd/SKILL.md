---
name: r-package-tdd
description: Use when implementing or modifying functions in an R package (files under R/, tests/testthat/, src/), before writing implementation code. Covers TDD cycle with testthat, roxygen2 documentation, namespace management, formatting with air, and linting with lintr.
allowed-tools: Bash(air*), Bash(Rscript*), Bash(R*), Read, Write, Edit
---

# R Package TDD

Test-driven development cycle for R package code, with integrated documentation, formatting, and linting gates.

**REQUIRED BACKGROUND:** superpowers:test-driven-development defines the RED-GREEN-REFACTOR cycle. This skill adapts it for R packages.

## Trigger & Scope

**Triggers when:** writing or modifying R functions in a package (`R/`, `tests/testthat/`, `src/`).

**Does NOT trigger for:** vignettes, README, DESCRIPTION-only edits, CI config, `data-raw/` scripts, `.qmd` files.

## Classify the Work

| Type | TDD approach |
|------|-------------|
| New exported function | Full cycle: test + roxygen2 + implementation |
| Modify existing function | Failing test showing new/fixed behaviour first |
| New S4/S7 class | Test constructor, validity, key methods |
| Bug fix | Reproduce bug as failing test, then fix |

## TDD Cycle

### RED -- Write failing test

- File: `tests/testthat/test-<module>.R` matching `R/<module>.R`
- Use `test_that("descriptive string", { ... })` with Arrange-Act-Assert
- Run: `Rscript --vanilla -e "devtools::test_active_file('R/<module>.R')"`
- Confirm: fails for the right reason (wrong result or missing function, not syntax error)

### GREEN -- Minimal passing implementation

Implementation in `R/<module>.R` is not "green" until ALL of these are satisfied:

**Code requirements:**
- Exported/main functions first, internal helpers below
- Validate inputs at function boundaries (`rlang::arg_match()`, `cli::cli_abort()`)
- Use `pkg::fun()` or `@importFrom` for dependencies, never `library()`/`require()`
- Run `air format .` after generating or editing R code

**Documentation requirements (roxygen2):**
- Every user-facing function MUST be exported (`@export`) and have full roxygen2 documentation
- Internal functions should NOT have roxygen documentation
- `@param` for every parameter
- `@returns` describing the return value
- `@examples` for exported functions (`\dontrun{}` if needed)
- `@importFrom` tags for any new namespace imports
- Run `Rscript --vanilla -e "devtools::document()"` after changing any roxygen2 comment

**For S4/S7 classes additionally:**
- `@slot` or typed properties documented
- `@exportClass` / `@exportMethod` as needed
- `setValidity()` or S7 validator defined

**Then:** Run test file, confirm pass.

### REFACTOR -- Clean up, keep tests green

- DRY: extract helpers, parameterise near-identical logic
- Run test file after each change to confirm still green

## Compiled Code Notes

When adding C-optimised operations:

1. **Write a pure-R reference implementation first** — this is the TDD baseline
2. **Write all tests against the R implementation** — cover edge cases (empty input, NA, large input, single element, ties)
3. **Implement the C version** — it must pass all existing tests without modification
4. **Benchmark C against R** — the R implementation serves as the performance baseline

The R reference can remain in the codebase as a correctness oracle (e.g. `find_nearest_r()` in `engine-nearest-r.R`) or be removed once the C version is stable.

## Per-Iteration Verification

After each RED-GREEN-REFACTOR cycle, run on **modified files only**:

```bash
air format .
Rscript --vanilla -e "lintr::lint('R/<module>.R')"
Rscript --vanilla -e "devtools::test_active_file('R/<module>.R')"
```

## Final Gate (before commit)

- [ ] `air format .` on all modified R files
- [ ] `Rscript --vanilla -e "lintr::lint('R/<module>.R')"` on all modified R files -- issues addressed
- [ ] `Rscript --vanilla -e "devtools::test()"` -- full test suite passes
- [ ] `Rscript --vanilla -e "devtools::document()"` -- NAMESPACE and man pages current
- [ ] `Rscript --vanilla -e "devtools::check()"` -- 0 errors, 0 warnings (notes reviewed)
- [ ] No `browser()`, `debug()`, commented-out code, or credentials

## Quick Reference

| Action | Command |
|--------|---------|
| Run code interactively | `Rscript --vanilla -e "devtools::load_all(); code"` |
| Run all tests | `Rscript --vanilla -e "devtools::test()"` |
| Run tests by prefix | `Rscript --vanilla -e "devtools::test(filter = '^{name}')"` |
| Run tests for a file | `Rscript --vanilla -e "devtools::test_active_file('R/{name}.R')"` |
| Run single test by desc | `Rscript --vanilla -e "devtools::test_active_file('R/{name}.R', desc = 'blah')"` |
| Regenerate docs | `Rscript --vanilla -e "devtools::document()"` |
| Full R CMD check | `Rscript --vanilla -e "devtools::check()"` |
| Format code | `air format .` |
| Lint file | `Rscript --vanilla -e "lintr::lint('R/foo.R')"` |
| Test coverage | `Rscript --vanilla -e "covr::package_coverage()"` |
