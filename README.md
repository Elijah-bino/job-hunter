# job-hunter

A Claude Code plugin that hunts for jobs and applies for you, honestly:

1. searches SEEK / LinkedIn / Greenhouse boards for fresh listings that match your targets,
2. reads the full ad and skips anything you're not eligible for,
3. builds a tailored one-page CV + cover letter **only from facts you wrote down**,
4. fills the application form in your own Chrome (Claude in Chrome) and submits (if you allow it),
5. logs every application and every skip.

It stops at anything it must not do: creating accounts, typing passwords, CAPTCHAs, or any answer that isn't true.

## Requirements
- [Claude Code](https://claude.com/claude-code) (a paid plan; job hunting uses a lot of tokens)
- [Claude in Chrome](https://claude.ai/chrome) extension, connected to Claude Code
- Chrome (or Edge) logged in to SEEK / LinkedIn yourself
- Python 3.9+ and `pip install pypdf` (page counts + merging PDFs)

## Install
```
/plugin marketplace add Elijah-bino/job-hunter
/plugin install job-hunter@job-hunter
```
(or clone the repo and run `/plugin marketplace add ./job-hunter`)

## Set up your workspace (private, NOT in this repo)
1. Copy `templates/workspace/` to a private folder, e.g. `~/job-hunt/`.
2. Fill in `profile.json` (CV header + education), `PROFILE.md` (form answers, work rights, salary rules,
   targets, whether auto-submit is allowed) and `FACTS.md` (everything true about your experience, with numbers).
3. In `_src/example_role.py`, point `sys.path` at this plugin's `skills/apply-job/scripts` folder
   (or set the env var `JOBHUNT_SCRIPTS`). Run it once to check PDFs build: `python _src/example_role.py`.
4. Open Claude Code in that folder and say: **"find and apply for a role"**.

The more complete and specific `FACTS.md` is, the better the CVs. Claude will never add anything that isn't in it.

## What's inside
| Path | Purpose |
|---|---|
| `skills/apply-job/SKILL.md` | the workflow Claude follows |
| `skills/apply-job/scripts/jobs.py` | SEEK / LinkedIn / Greenhouse search, ad text, form questions, dedupe |
| `skills/apply-job/scripts/cvlib.py` | HTML -> one-page A4 PDF CV and cover letter (headless Chrome) |
| `skills/apply-job/scripts/ats/` | JS helpers + notes for SEEK, Workday, SuccessFactors, Greenhouse, etc. |
| `templates/workspace/` | blank profile, facts, logs and an example per-job script (dummy data) |

## Safety and honesty rules (built in)
- Never creates accounts, enters passwords, or solves CAPTCHAs: it fills the form and hands over to you.
- Never invents experience; one honest gap per cover letter.
- Never sends emails/messages for you without asking.
- Treats job-ad text as data, not instructions.
- Keep your workspace out of git (or in a separate private repo): it holds your personal details.

## Notes
- SEEK and LinkedIn endpoints used are public but unofficial; they may change. Keep the volume reasonable and
  respect each site's terms.
- Usage: set yourself a stop rule (e.g. stop at 80% weekly usage) in `PROFILE.md`.
