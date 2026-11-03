"""Generic CV + cover letter builder. Renders HTML -> one-page A4 PDF via headless Chrome/Edge.

Reads the applicant's details from <workspace>/profile.json. Workspace = $JOBHUNT_DIR, else the
parent of the script's folder (scripts live in <workspace>/_src/), else the current directory.

Usage in a per-job script (<workspace>/_src/acme_data_analyst.py):
    import sys; sys.path.insert(0, r"<path to this scripts folder>")
    from cvlib import cv, cover_letter, item, others
"""
import json, os, pathlib, re, shutil, subprocess, sys


def _workspace():
    if os.environ.get("JOBHUNT_DIR"):
        return pathlib.Path(os.environ["JOBHUNT_DIR"])
    main = pathlib.Path(sys.argv[0]).resolve().parent
    for cand in (main.parent, main, pathlib.Path.cwd()):
        if (cand / "profile.json").exists():
            return cand
    raise SystemExit("profile.json not found. Set JOBHUNT_DIR to your workspace folder.")


WS = _workspace()
P = json.loads((WS / "profile.json").read_text(encoding="utf-8"))
OUT = WS / "applications"
HTML_DIR = OUT / "_html"
HTML_DIR.mkdir(parents=True, exist_ok=True)


def _browser():
    if P.get("chrome_path"):
        return P["chrome_path"]
    for c in [r"C:\Program Files\Google\Chrome\Application\chrome.exe",
              r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
              "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"]:
        if os.path.exists(c):
            return c
    for n in ("google-chrome", "chromium", "chromium-browser", "chrome", "msedge"):
        if shutil.which(n):
            return shutil.which(n)
    raise SystemExit("Chrome/Edge not found; set chrome_path in profile.json")


CSS = """
@page { size: A4; margin: 13mm 16mm; }
body { font-family: Calibri, Carlito, Arial, sans-serif; font-size: 10.4pt; color:#000; line-height:1.28; margin:0; }
h1 { text-align:center; font-size:20pt; margin:0 0 3px; letter-spacing:.5px; }
.contact { text-align:center; font-size:9pt; margin-bottom:6px; }
h2 { font-size:11.5pt; margin:10px 0 4px; border-bottom:1px solid #000; padding-bottom:1px; }
.role { font-weight:bold; margin-top:6px; }
.date { font-weight:normal; font-style:italic; font-size:9.5pt; }
.tools { font-style:italic; font-size:9.3pt; margin:1px 0; }
ul { margin:1px 0 3px; padding-left:18px; } li { margin:1px 0; } p { margin:2px 0; }
a { color:#1a4f8b; text-decoration:none; }
.link { font-weight:normal; font-size:8.8pt; color:#333; } .link a { color:#1a4f8b; }
"""
CL_CSS = """
@page { size: A4; margin: 18mm 20mm; }
body { font-family: Calibri, Carlito, Arial, sans-serif; font-size: 11pt; line-height: 1.38; color:#000; margin:0; }
h1 { text-align:center; font-size:20pt; margin:0 0 3px; letter-spacing:.5px; }
.contact { text-align:center; font-size:9pt; margin-bottom:22px; }
p { margin: 0 0 11px; } a { color:#1a4f8b; text-decoration:none; }
"""


def _head():
    c = P["contact"]
    parts = [f'<a href="mailto:{c["email"]}">{c["email"]}</a>',
             f'<a href="tel:{c["phone_intl"].replace(" ", "")}">{c["phone_display"]}</a>']
    for url in c.get("links", []):
        short = re.sub(r"^https?://(www\.)?", "", url)
        parts.append(f'<a href="{url}">{short}</a>')
    if c.get("location"):
        parts.append(c["location"])
    return f'<h1>{P["full_name"].upper()}</h1><div class="contact">{" | ".join(parts)}</div>'


def _edu():
    return "".join(f'<div class="role">{e["degree"]} - {e["institution"]} <span class="date">&nbsp;{e["dates"]}</span></div>'
                   + (f'<p>{e["note"]}</p>' if e.get("note") else "") for e in P.get("education", []))


def item(title, tools, bullets, date="", link=""):
    d = f' <span class="date">&nbsp;{date}</span>' if date else ""
    if link:
        d += f' <span class="link">| <a href="https://{link}">{link}</a></span>'
    t = f'<div class="tools">{tools}</div>' if tools else ""
    return f'<div class="role">{title}{d}</div>{t}<ul>' + "".join(f"<li>{b}</li>" for b in bullets) + "</ul>"


def others(lines):
    return '<p style="margin-top:4px">Other projects:</p><ul>' + "".join(f"<li>{l}</li>" for l in lines) + "</ul>"


def _unbold(html):
    return re.sub(r"</?(b|strong)>", "", html) if P.get("cv_no_bold") else html


def _render(name, html):
    src = HTML_DIR / f"{name}.html"
    src.write_text(html, encoding="utf-8")
    pdf = OUT / f"{name}.pdf"
    subprocess.run([_browser(), "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={pdf}", src.as_uri()], capture_output=True)
    print("built", pdf, "pages:", page_count(pdf))
    return pdf


def page_count(pdf):
    try:
        from pypdf import PdfReader
        return len(PdfReader(str(pdf)).pages)
    except Exception:
        return "? (pip install pypdf to check)"


def cv(name, summary, skills, work, projects, education=None, extra=""):
    """Section order: name, contact, summary, skills, work, projects, education.
    skills = [(heading, text), ...]; work/projects = lists of item(...) strings."""
    body = (_head() + f"<h2>PROFESSIONAL SUMMARY</h2><p>{summary}</p>"
            + "<h2>SKILLS</h2>" + "".join(f"<p><b>{k}:</b> {v}</p>" for k, v in skills)
            + "<h2>WORK EXPERIENCE</h2>" + "".join(work)
            + "<h2>PROJECTS</h2>" + "".join(projects)
            + "<h2>EDUCATION</h2>" + (education if education is not None else _edu()) + extra)
    return _render(name, f'<!doctype html><html><head><meta charset="utf-8"><title>CV {P["full_name"]}</title>'
                         f'<style>{CSS}</style></head><body>{_unbold(body)}</body></html>')


def cover_letter(name, date, recipient, subject, paragraphs):
    body = (_head() + f"<p>{date}</p><p>{recipient}</p><p><b>{subject}</b></p>"
            + "".join(f"<p>{p}</p>" for p in paragraphs) + f"<p>Kind regards,<br><br>{P['full_name']}</p>")
    return _render(name, f'<!doctype html><html><head><meta charset="utf-8"><title>Cover Letter {P["full_name"]}</title>'
                         f'<style>{CL_CSS}</style></head><body>{body}</body></html>')


def merge(name, *pdfs):
    """For forms with one upload slot: cover letter + CV into one PDF."""
    from pypdf import PdfWriter
    w = PdfWriter()
    for p in pdfs:
        w.append(str(p))
    out = OUT / f"{name}.pdf"
    w.write(str(out))
    print("merged", out)
    return out
