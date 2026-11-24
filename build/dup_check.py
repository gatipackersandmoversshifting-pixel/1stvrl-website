#!/usr/bin/env python3
"""Duplicate text check: share of a page's 8-word shingles (visible text) found in one other page.
Usage: python3 build/dup_check.py site <slug> [<slug> ...]   -> prints the max share per page vs every other page (limit 0.65)."""
import sys, re, html
from pathlib import Path
SITE = Path(sys.argv[1])
def text(p):
    t = p.read_text(encoding="utf-8", errors="ignore")
    t = re.sub(r"(?is)<(script|style|head)[^>]*>.*?</\1>", " ", t)
    t = re.sub(r"(?s)<[^>]+>", " ", t)
    return re.findall(r"[a-z0-9]+", html.unescape(t).lower())
def sh(w): return {" ".join(w[i:i+8]) for i in range(len(w) - 7)}
pages = {p.stem: p for p in SITE.glob("*.html") if p.stem.startswith(("packers-and-movers", "vrl-packers"))}
S = {k: sh(text(p)) for k, p in pages.items()}
worst = 0
for slug in sys.argv[2:]:
    a = S[slug]; best = max(((len(a & b) / len(a), k) for k, b in S.items() if k != slug), default=(0, ""))
    words = len(text(pages[slug])); worst = max(worst, best[0])
    print(f"{slug}: words={words} max_dup={best[0]:.3f} vs {best[1]}")
print("WORST", round(worst, 3), "OK" if worst < 0.65 else "FAIL")
