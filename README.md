# job-hunter

![Claude Code](https://img.shields.io/badge/Claude_Code-plugin-D97757?logo=anthropic&logoColor=white)
![Claude in Chrome](https://img.shields.io/badge/Claude_in_Chrome-browser_agent-4285F4?logo=googlechrome&logoColor=white)
![Skill](https://img.shields.io/badge/skill-apply--job-6E56CF)
![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python&logoColor=white)

**Skills:** `apply-job`: find a job, check fit, write a tailored CV and cover letter, fill and submit the application, and log it.

## What it does
job-hunter turns Claude Code into your job-application assistant. It searches SEEK, LinkedIn and company job
boards for fresh roles that match you, reads each ad in full and skips the ones you're not eligible for, then
writes a one-page CV and cover letter built **only from facts you've given it**. It then fills in the application
form in your own Chrome browser, submits it (if you allow that) and keeps a log of every application and every skip.

It never creates accounts, types passwords, solves CAPTCHAs or gives an untrue answer. When it reaches one of
those, it stops and hands over to you.

## Requirements (optional reading)
- [Claude Code](https://claude.com/claude-code) on a paid plan (job hunting uses a lot of tokens)
- [Claude in Chrome](https://claude.ai/chrome) extension, connected to Claude Code
- Chrome (or Edge)
- Python 3.9+ and `pip install pypdf`

## Install
In Claude Code:
```
/plugin marketplace add Elijah-bino/job-hunter
/plugin install job-hunter@job-hunter
```
Then copy `templates/workspace/` to a private folder on your computer (for example `~/job-hunt/`) and open
Claude Code in that folder. This is your workspace. Keep it out of any public repo: it will hold your personal details.

## Steps

### 1. Tell Claude about yourself
Chat with Claude and give it all your information: contact details, work rights, education, every job,
project and skill, with real numbers wherever you have them, plus your salary expectations, notice period and
the roles and locations you want. Ask Claude to save it into `FACTS.md`, `PROFILE.md` and `profile.json`.
`FACTS.md` is the only source Claude uses for your CVs and form answers, so the more complete it is, the better
your applications will be.

### 2. Log in to your accounts in the browser
In the Chrome browser that Claude Code is connected to, log in to SEEK, LinkedIn, Gmail and any other job sites
you use. Claude works inside your logged-in sessions and will never type your passwords.

### 3. Find a role and apply
Say **"find and apply for a role"** (or paste a job link). Watch what Claude does live in the browser.
If something goes wrong (a wrong answer, a bad CV line, a stuck form), tell Claude to correct it, and ask it
to update the `.md` files as you go so it doesn't repeat the mistake.

## Note: it learns as you go
This is a progressive learning setup. Every correction you make gets written into your `.md` files, so after
roughly 10 applications and plenty of back-and-forth, it knows your answers, your style and the quirks of each
job site well enough to run on autopilot on its own.

## What's inside
| Path | Purpose |
|---|---|
| `skills/apply-job/SKILL.md` | the workflow Claude follows |
| `skills/apply-job/scripts/jobs.py` | SEEK / LinkedIn / Greenhouse search, ad text, form questions, dedupe |
| `skills/apply-job/scripts/cvlib.py` | builds one-page A4 PDF CVs and cover letters (headless Chrome) |
| `skills/apply-job/scripts/ats/` | form-filling helpers and notes for SEEK, Workday, SuccessFactors, Greenhouse and more |
| `templates/workspace/` | blank profile, facts and logs, plus an example per-job script (dummy data) |

## Safety and honesty rules (built in)
- Never creates accounts, enters passwords or solves CAPTCHAs: it fills the form and hands over to you.
- Never invents experience; each cover letter is honest about one gap.
- Never sends emails or messages for you without your go-ahead.
- Treats job-ad text as data, not instructions.
- SEEK and LinkedIn endpoints used are public but unofficial and may change. Keep volume reasonable and respect each site's terms.
