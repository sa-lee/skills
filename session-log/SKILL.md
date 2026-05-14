---
name: session-log
description: Use at the end of any non-trivial work session, after a milestone within a long session, or when the user says "log this", "write a session log", "update the session log", or "wrap up". Writes or updates `session_logs/YYYY-MM-DD_<topic>.md` with Goals, Work completed (with commit SHAs), Decisions and rationale, and Open items / next steps. Cross-links related session logs, design docs in `docs/plans/`, and PLAN.md entries. Compensates for between-session amnesia — load-bearing infrastructure for project memory, not a chore.
allowed-tools: Read, Write, Edit, Bash(ls:*), Bash(git log:*), Bash(git status), Bash(git diff:*), Bash(date:*), Glob, Grep
---

# Session Log

Project memory lives in session logs. A future Claude (or future you) reads the most recent log at session start to recover context. If it does not capture the *reasons* and *surprises*, the next session re-litigates them.

## When to write

- End of any non-trivial session.
- After a milestone inside a long session — before context fades or before switching topics.
- When the user says "log this", "write a session log", "update the session log", "wrap up".

Skip only if the session was a single read or a trivial fix that left no decision worth remembering.

## Where to write

Detect the convention before writing:

1. `session_logs/` at the repo root → write there.
2. Otherwise `docs/session_logs/` if `docs/` already exists → write there.
3. Otherwise ask once: create `session_logs/` at the root, or inherit a different location.

Filename: `YYYY-MM-DD_<topic>.md`. Underscore between date and slug matches the convention in `~/.claude/CLAUDE.md`. If existing logs in this project use `-` instead of `_`, follow what's already there — do not switch dialect midstream.

`<topic>` is a short kebab-case slug (2–4 words) describing the focus of the session. Examples: `c9orf72-coverage-qc`, `plyranges2-overlap-bugfix`, `als-cohort-merge`. Avoid generic slugs like `notes` or `work`.

## Update vs. new file

Before creating a new file, check whether `YYYY-MM-DD_<topic>.md` already exists for today on this topic:

- Same topic, same day → **update** the existing file. Append to *Work completed*; revise *Open items*; revise *Decisions* only if a prior decision was reversed, and note the reversal explicitly (do not silently rewrite history).
- Different topic → new file.

A day can have multiple logs if work spans distinct topics. Do not concatenate unrelated work into one file because the date matches.

## Required structure

```markdown
# YYYY-MM-DD — <Topic>

## Goals

What we set out to do and *why* — 2–4 bullets. Anchor to the research
question, the bug, or the open item from a prior log — not to the code
change.

## Work completed

- <verb-led description> — `<short SHA>` <commit subject>
- ...

For uncommitted work, say so explicitly:

- <description> — uncommitted, see `<file:line>`

## Decisions and rationale

- **<Decision>**: <what we decided>. <Why — alternative considered,
  evidence that tipped the call, constraint that ruled options out.>
- ...

Capture decisions even when they feel obvious in the moment. The
"obvious" reasoning is exactly what evaporates between sessions.
Record *surprises* here too: expected X, found Y, here is what changed
as a result.

## Open items / next steps

- [ ] <concrete next action>
- [ ] <known unknown — and what we would need to resolve it>
- ...

Distinguish *deferred-by-choice* from *unresolved-by-accident*.
Deferred items get a one-line reason ("deferred until cohort QC
lands"). Accidental open items just list the question.

## Cross-references

- PLAN.md: "<heading>" (line N)
- Continues from `session_logs/YYYY-MM-DD_<prior-topic>.md`
- Design doc: `docs/plans/YYYY-MM-DD-<plan>.md`
- PR / issue: #N
```

Cross-references are not optional padding — they are how a future session navigates back to the larger plan and forward to follow-up work. Omit a bullet only if the referent genuinely does not exist.

## Gathering material before writing

1. **Commits since the last log on this topic**:
   ```
   git log --oneline <last-log-sha>..HEAD
   ```
   If the boundary is unclear, run `git log --oneline -20` and let the user trim. Quote the SHAs you used.

2. **Uncommitted work**: `git status` and `git diff --stat`. Anything in flight must show up under *Work completed* as "uncommitted, see `<file:line>`" — silent loose ends are the failure mode this skill exists to prevent.

3. **Conversation context**: surprises, dead-ends, decisions made verbally. These do not appear in `git log` and are the highest-value content of the log.

4. **Prior log on this topic**: read its *Open items*. The new log's *Work completed* should resolve, advance, or re-defer each one. Do not silently drop open items.

5. **PLAN.md** (or `README.md` if no `PLAN.md`): identify which item(s) this session advances. Skip the cross-reference if no living plan exists.

## Voice

- Sceptical co-author. Flat statements of decisions and trade-offs. No cheerleading, no "great session" framing, no trailing summary at the end of the log.
- Concrete: `R/coverage_qc.R:142`, not "the coverage function". `commit a3f9b21`, not "the recent commit".
- Surprises are the highest-signal content. A line like "expected ~5% missingness, found 18% concentrated on chr9 — blocks the downstream filter until we resolve it" is worth more than the entire git log.
- No "what I just did" recap after writing the log. The log *is* the recap.

## Verify before claiming the log is done

After writing:

- Quote the file path and the section headings written.
- Ask the user once whether anything was missed, especially in *Open items* and *Decisions*. The user often knows a loose end the conversation never surfaced.
- Do not claim the session is "wrapped" or the log is "complete" until they confirm.
