"""Ensure every page with a quote-send.php form has <script src="/ad-track.js"></script>
exactly once, right before </body>. Rule in CLAUDE.md (Deepak, 2026-11-19). Never remove the tag.
Usage: python3 build/add_ad_track.py site        -> fix static pages in place
       python3 build/add_ad_track.py site --check -> only report, exit 1 on any problem"""
import sys, re
from pathlib import Path
TAG = '<script src="/ad-track.js"></script>'
site = Path(sys.argv[1]); check = "--check" in sys.argv
bad = []; fixed = 0; forms = 0
for p in sorted(site.rglob("*.html")):
    if p.name == "shifting-price.html":
        continue  # server-only file, never touched from the repo
    s = p.read_text(encoding="utf-8")
    if "quote-send.php" not in s:  # absolute or relative form action
        continue
    forms += 1
    ok = s.count(TAG) == 1 and s.count("</body>") == 1 and re.search(re.escape(TAG) + r"\s*</body>", s)
    if ok:
        continue
    if check:
        bad.append(f"{p}: tag={s.count(TAG)} body={s.count('</body>')}"); continue
    if s.count("</body>") != 1:
        bad.append(f"{p}: </body> count {s.count('</body>')}"); continue
    s = s.replace(TAG + "\n", "").replace(TAG, "")
    s = s.replace("</body>", TAG + "\n</body>")
    p.write_text(s, encoding="utf-8"); fixed += 1
print(f"form pages: {forms}, fixed: {fixed}, problems: {len(bad)}")
for b in bad: print("  ", b)
sys.exit(1 if bad else 0)
