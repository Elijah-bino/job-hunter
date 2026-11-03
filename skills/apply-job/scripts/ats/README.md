# ATS fill helpers

Paste `common.js` (plus the site script) into Chrome `javascript_tool`, then call functions in the same exec.
Goal per application: read fields once -> fill once -> verify once -> submit. Screenshot only on failure.

| File | Site | What it gives you |
|---|---|---|
| `common.js` | any | `dump()` lists fields + labels (incl. shadow DOM); `setText(el,v)` native setter + events; `fillText([[/label/i,'value']])`; `answerChoice(qRe,aRe)` |
| `seek.js` | SEEK "employer questions" step | `seekAnswer([[/right to work/i,/yes/i]])`, `seekSelect`, `seekChecks`, `seekUnanswered()` |
| `workday.js` | myworkdayjobs.com | `wdSelect`, `wdPrompt`, `wdRadio`, `wdErrors()` |
| `successfactors.js` | SAP SuccessFactors | `sfCombo`, `sfRequiredEmpty()`, `sfExpandAll()` |

Example (SEEK):
```
<contents of common.js + seek.js>
await seekAnswer([[/right to work/i, /yes|citizen|visa/i], [/years.*python/i, /2|1-2/i]])
```

## Per-site notes
- **SEEK**: apply URL `https://www.seek.com.au/job/<id>/apply`. Upload inputs `input#resume-fileFile`,
  `input#coverLetter-fileFile`. SEEK keeps max 10 stored resumes; delete old ones only if the user allows.
- **LinkedIn Easy Apply**: the resume file input is created on click. Patch
  `HTMLInputElement.prototype.click` to capture the input instead of opening the native picker, then `file_upload` to it.
  Job text: `jobs.py ad li <id>` (the logged-in page often returns empty text).
- **Greenhouse** (boards.greenhouse.io / job-boards.eu.greenhouse.io): no account. Text fields take native-setter
  values; comboboxes (right-to-work, country) need real click + type + Enter. Picking the phone country can wipe
  the phone number: retype it. Read helper text under fields (salary may be monthly). Invisible reCAPTCHA usually passes.
- **Workday**: needs an account -> stop, user creates it. Then `button[aria-haspopup=listbox]` click -> `[role=option]` click.
- **SuccessFactors**: combobox = type -> click visible option; error banners shift layout. File input appears after "Upload from Device".
- **Manatal** (shadow DOM): real clicks/typing; file input: move to document.body, upload, move back, dispatch `change` with `composed:true`.
- **Ashby**: real typing; ctrl+a types a literal "a" -> use triple_click to select.
- **Breezy**: textareas `cSummary` / `cCoverLetter`, plain radios.
- **Cornerstone (csod)**: radios grouped by input name.
- **Oracle HCM**: suburb lists can be incomplete -> block for the user if the user's suburb is missing.
- **BambooHR**: one Resume slot (merge cover+CV); honeypot field `nickname_*` stays blank; reCAPTCHA checkbox -> user ticks.
- **Lever**: often hCaptcha at submit -> fill, user ticks + submits.
- Files outside the shared workspace may be rejected by `file_upload`: keep PDFs inside the workspace.
