"""Job search + ad reading helpers (stdlib only). Run with: python -I jobs.py <command> ...

  seek  "<where>" <days> kw1 kw2 ...      SEEK listings (id | title | advertiser | salary | type)
  li    "<location>" <hours> kw1 kw2 ...  LinkedIn public listings, entry/associate level
  ad    seek|li <id> [...]                 full ad text
  gh    <board> [title filter]             Greenhouse board jobs (board = slug in boards.greenhouse.io/<slug>)
  ghq   <board> <job id>                   Greenhouse form questions (required | label | options)
  seen  <workspace> <term> [...]           grep logs (JOBS/BLOCKED/CLAIMS.md) for ids/companies already handled

SEEK/LinkedIn are unofficial public endpoints; they can change. Keep volume low and polite.
"""
import html, json, pathlib, re, sys, urllib.parse, urllib.request

UA = {"User-Agent": "Mozilla/5.0"}


def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=25).read().decode("utf-8", "replace")


def text(s):
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s))).strip()


def seek(where, days, *kws):
    seen = set()
    for kw in kws:
        u = ("https://au.seek.com/api/jobsearch/v5/search?siteKey=AU-Main&pageSize=30&where=%s&daterange=%s&keywords=%s"
             % (urllib.parse.quote(where), days, urllib.parse.quote(kw)))
        for j in json.loads(get(u)).get("data", []):
            if j["id"] in seen:
                continue
            seen.add(j["id"])
            print(j["id"], "|", j["title"], "|", j.get("advertiser", {}).get("description"), "|",
                  j.get("salaryLabel", ""), "|", ",".join(j.get("workTypes", [])))


def li(location, hours, *kws):
    seen = set()
    for kw in kws:
        for start in (0, 25):
            u = ("https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=%s&location=%s"
                 "&f_TPR=r%d&f_E=1%%2C2&start=%d" % (urllib.parse.quote(kw), urllib.parse.quote(location), int(hours) * 3600, start))
            try:
                t = get(u)
            except Exception as e:
                print("ERR", kw, e)
                continue
            for block in t.split("<li")[1:]:
                m = re.search(r"jobPosting:(\d+)", block)
                if not m or m.group(1) in seen:
                    continue
                seen.add(m.group(1))
                g = lambda tag: text((re.search(r"<%s[^>]*>(.*?)</%s>" % (tag, tag), block, re.S) or [None, ""])[1])
                print(m.group(1), "|", g("h3"), "|", g("h4"))


def ad(src, *ids):
    for i in ids:
        if src == "seek":
            t = get("https://au.seek.com/job/" + i)
            m = re.search(r'data-automation="jobAdDetails".*?>(.*?)</div></div>', t, re.S)
        else:
            t = get("https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/" + i)
            m = re.search(r"show-more-less-html__markup[^>]*>(.*?)</div>", t, re.S)
        print("=====", src, i, "offsite-apply" if "offsite" in t else "")
        print(text(m.group(1)) if m else "(ad text not found)")


def gh(board, flt=""):
    d = json.loads(get("https://boards-api.greenhouse.io/v1/boards/%s/jobs" % board))
    for j in d["jobs"]:
        line = "%s | %s | %s | %s" % (j["id"], j["title"], j["location"]["name"], j["absolute_url"])
        if flt.lower() in line.lower():
            print(line)


def ghq(board, job):
    d = json.loads(get("https://boards-api.greenhouse.io/v1/boards/%s/jobs/%s?questions=true" % (board, job)))
    for q in d["questions"]:
        opts = [v["label"] for f in q["fields"] for v in f.get("values", [])]
        print(q["required"], "|", q["label"], "|", [f["type"] for f in q["fields"]], opts or "")


def seen(ws, *terms):
    files = [p for p in pathlib.Path(ws).glob("*.md")]
    for t in terms:
        hits = [f"{p.name}: {l.strip()[:140]}" for p in files for l in p.read_text(encoding="utf-8").splitlines() if t.lower() in l.lower()]
        print("==", t, "->", "NEW" if not hits else "")
        for h in hits:
            print("  ", h)


if __name__ == "__main__":
    cmd, *a = sys.argv[1:] or ["help"]
    {"seek": seek, "li": li, "ad": ad, "gh": gh, "ghq": ghq, "seen": seen}.get(cmd, lambda *_: print(__doc__))(*a)
