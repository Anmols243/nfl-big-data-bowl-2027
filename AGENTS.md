# AGENTS.md — NFL Big Data Bowl 2027 (Codex laws)

Project: Kaggle NFL Big Data Bowl 2027, "Combine to NFL Performance" — link 10 Hz Combine tracking to regular-season performance. Solo, University Track.
Submission: writeup ≤2,000 words, ≤9 figures/tables, attached PUBLIC Kaggle notebook, all code reproducible in that notebook. Deadline 6 Jan 2027 23:59 UTC. Submissions not using player tracking data are NOT scored.

## Data laws
- Competition data is CC BY-NC 4.0. NEVER commit data files, the Kaggle archive, or kaggle.json / any token. Data lives in `data/`, gitignored.
- Frozen ground truth (quote only these until a new verified freeze replaces them): 510 players / 510 unique nfl_id; combine_results 510 rows; combine_tracking 463,189 rows; player_play 314,197 rows; games 1,002 rows; game_tracking rows 2023: 3,665,443 / 2024: 7,827,944 / 2025: 11,160,903. Sampling verified 100 ms (10 Hz) in both tracking sources. Provided `s`/`a` columns exist; `s` spot-checked vs x/y-derived (mean abs diff 0.121 yd/s, n=36 frames — indicative only).
- Method v2: clock onset at 1.5 yd/s (three sustained frames), extrapolation flagged, median absolute error 0.0593 s, crossing coverage 789/793.
- Kaggle's web Data tab mislabels file sizes. Trust local file counts, reconciled totals, and this file — not the UI.
- Every percentage states its denominator and coverage window. Per-season game coverage uses ELIGIBLE players only (draft_year ≤ season) as denominator, never 510 for 2023/2024.
- An empty join means "no rows in supplied data" — never report it as 0 performance. 13/510 players have zero player_play rows; state that explicitly wherever coverage is discussed.
- Use lazy scans (Polars) / chunked reads for player_play.csv and all tracking files. Never load a tracking file whole into memory without a stated reason.

## Working laws
- One task per prompt. Do exactly the task asked; no speculative features, no extra analysis, no unrelated fixes.
- EDA tasks are REPORT ONLY: descriptive tables and counts, no modelling, no conclusions, no slice recommendation. The human chooses the slice.
- If a live check contradicts the task spec or these laws, STOP and report the contradiction instead of silently adjusting.
- Never weaken a check or change a frozen number to make output agree. Re-freeze openly: new number, source, date, reason.
- Skills — MANDATORY, not optional: before starting ANY task, scan the installed skills for a relevant one. If a skill matches the task type, invoke it by name ($skill-name) at the start of the task, follow its workflow, and name it in the task report. If two skills could match, use the more specific one as primary; never stack unrelated skills. If no installed skill matches, say so in the report and proceed. Known routing for this project:
  - Mapping / orientation / resuming work → $gsd-map-codebase, $gsd-progress (or the GSD resume skill if a session was interrupted)
  - Planning a multi-step phase before executing it → the GSD plan skill for that phase; spec/scope questions → $grill-me or $to-spec if installed
  - Writing feature, extraction, or feature-engineering code → $tdd first, then $implement
  - A bug, failure, or wrong number → $diagnosing-bugs (mandatory when a bug survives one fix attempt — do not keep patching ad hoc)
  - Library/API usage you are not 100% sure of (Polars, Kaggle API, plotting) → check current docs via the context7 skill if installed, before writing the code
  - Finishing any task → $verification-before-completion before claiming done, every time
  - Phase gates, pre-commit, pre-submission → $code-review on top of verification
  - Code that works but is convoluted → $code-simplifier, only after checks are green
  - Modelling / ML training code if a phase introduces it → the relevant Hugging Face / ML skill from the installed packs, named in the report
  - This routing is a floor, not a ceiling: any other installed skill that clearly matches a task (data validation, visualisation, documentation) must be used the same way — relevance is decided by the task, not by whether it is listed here.
- End every task with: what was run, exact output tables/counts, files changed, and anything unverified. No summary claims without the numbers behind them.
- Commit only when the human says so, and only after the task's checks pass. Never commit on a failed or partial run.

## Layout
- `data/` — competition CSVs (gitignored), `notebooks/` — EDA/analysis notebooks, `nfl-bdb2027-eda-session1.ipynb` is the Session 1 notebook.
- Final deliverable notebook must run end-to-end on Kaggle with the competition dataset attached — keep paths Kaggle-compatible (`/kaggle/input/...` fallback to local `data/`).
