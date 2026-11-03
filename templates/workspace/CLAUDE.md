# Job hunt workspace

- Use the `job-hunter:apply-job` skill for any "find and apply" request.
- Read PROFILE.md, FACTS.md and PENDING.md at session start. Never re-ask anything in PROFILE.md.
- FACTS.md is the only source of truth for CV, cover letter and form answers. Never fabricate.
- Keep JOBS.md, BLOCKED.md, CLAIMS.md and PENDING.md updated.
- Respond briefly.

## Token / model efficiency
- Main chat: you pick the model (`/model sonnet` recommended). Claude can't switch it or run `/clear` itself.
- Subagent models (Claude sets `model` on each spawn):
  - Haiku: search listings, dedupe, log updates.
  - Sonnet: apply (form fill, screening answers), CV/cover tailoring.
  - Opus: only when stuck or when you ask.
- One job at a time: main session orchestrates; each job runs in ONE fresh Sonnet agent (fresh context = like `/clear`), which applies, updates JOBS/BLOCKED/CLAIMS/PENDING, and returns a 3-line report. No parallel agents unless asked.
- The MD logs are the memory between jobs: write everything the next job needs before finishing.
- Screenshots only on failure. You can `/clear` the main chat anytime; work resumes from PENDING.md.
