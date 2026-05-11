# skills

Personal [Claude Code](https://docs.claude.com/en/docs/claude-code) skills for
statistical genetics / genetic epidemiology research workflows. R-first,
Quarto for documents and decks.

Each subdirectory is a self-contained skill with a `SKILL.md` whose
frontmatter declares when Claude should invoke it. Drop the directory into
`~/.claude/skills/` (or symlink it) and Claude will pick it up.

## Skills

| Skill | What it does |
|---|---|
| [`academic-writing-style`](academic-writing-style/) | Reviews existing manuscript prose against a specific academic voice. Produces line-anchored suggestions only — never drafts. |
| [`analysis-review`](analysis-review/) | Code-level pre-paper audit of a bioinformatics or statistical genetics pipeline. Parallel referee agents check samples, models, and provenance; then co-writes a simulation-recovery test. Sibling to `paper-review`. |
| [`beautiful-deck-quarto`](beautiful-deck-quarto/) | Builds a Quarto-Beamer slide deck from a paper, preprint, or memo. WEHI brand by default. |
| [`deep-read`](deep-read/) | Deep, faithful summary of a local academic PDF — preserves effect sizes, sample sizes, accessions, software versions, and direct quotes. For papers where the specifics make it replicable. |
| [`interview-me`](interview-me/) | Interactive Socratic interview that turns a research idea into a structured spec (biology, cohort, comparator, threats to inference, sensitivity analyses). |
| [`paper-review`](paper-review/) | Peer-review-style critique of a bioinformatics / statistical genetics manuscript or preprint. Six parallel referee agents cover copyediting, internal consistency, claims, reproducibility, figures, and contribution. Sibling to `analysis-review`. |
| [`r-package-tdd`](r-package-tdd/) | TDD cycle for R package code with testthat, roxygen2, air, and lintr gates. |
| [`tikz`](tikz/) | Fast visual-collision check for figures — TikZ in `.tex` or rendered `.png`/`.jpg`/`.pdf`. Catches the class of error that compiles cleanly but looks wrong. |

## Layout

```
<skill-name>/
  SKILL.md              # entry point, with frontmatter description
  references/           # supporting prose Claude reads on demand
  scripts/              # helper scripts the skill invokes
  assets/               # templates, brand packs, etc.
```

The `SKILL.md` frontmatter `description` is what Claude uses to decide
whether to invoke the skill, so it is written in trigger-phrase form
("Use when the user asks to …").

## Install

```sh
git clone https://github.com/sa-lee/skills.git ~/.claude/skills
```

Or clone elsewhere and symlink individual skills into `~/.claude/skills/`.
