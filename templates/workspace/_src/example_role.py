"""Example per-job script. Copy to <company>_<role>.py, rewrite from FACTS.md only, then: python <file>.py
All content below is DUMMY data for "Alex Example". Replace every line with your own verified facts."""
import os, sys

# Point this at the plugin's scripts folder (or set JOBHUNT_SCRIPTS).
sys.path.insert(0, os.environ.get("JOBHUNT_SCRIPTS", r"C:\path\to\job-hunter\skills\apply-job\scripts"))
from cvlib import cv, cover_letter, item, others

# Reusable building blocks: define once per person, reuse across jobs.
JOB1 = item("Data Analyst - Example Org", "Python, SQL, Tableau",
            ["Built a weekly KPI dashboard used by <b>4 teams</b>; reconciled to source with <b>0 discrepancies</b>.",
             "Automated a manual report with Python, cutting prep time from <b>3 hours to 10 minutes</b>."],
            "Jan 2025 - Present")
PROJ1 = item("Sales Forecasting Model", "Python, scikit-learn",
             ["Forecast monthly sales from <b>50,000 rows</b> of history; <b>12% MAPE</b> on a held-out year."],
             link="github.com/your-github/sales-forecast")

cv("CV_Alex_DataAnalyst_AcmeCo",
   "Data analyst who turns messy data into decisions. Built KPI reporting used by <b>4 teams</b> and automated reports "
   "from <b>3 hours to 10 minutes</b>. SQL, Python, Tableau.",
   [("Analytics", "KPI reporting, segmentation, statistics (hypothesis testing, regression)"),
    ("Tools", "SQL, Python (pandas), Tableau, Excel")],
   [JOB1],
   [PROJ1, others(["Example side project: one line with one number."])])

cover_letter("CoverLetter_Alex_DataAnalyst_AcmeCo", "1 January 2027",
   "Hiring Team<br>Acme Co<br>Melbourne, VIC", "Re: Data Analyst",
   ["Dear Hiring Team,",
    "Opening: strongest proof point for THIS role, with a bold number, e.g. a dashboard used by <b>4 teams</b>.",
    "Middle: map 2-3 of the ad's key requirements to facts from FACTS.md.",
    "Honest gap: name one requirement you don't fully meet and how you'd close it.",
    "Close: availability, work rights wording from PROFILE.md, thanks."])
