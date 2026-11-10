#!/usr/bin/env python3
"""Rebuild site/sitemap.xml from every indexable page's canonical URL.
Keeps lastmod from the existing sitemap unless the page content changed (tracked by hash in build/.sitemap_hashes.json)."""
import re, json, hashlib, datetime, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
HASHES = ROOT / "build" / ".sitemap_hashes.json"
SKIP = {"404.html", "thank-you.html"}
today = datetime.date.today().isoformat()
old = json.loads(HASHES.read_text()) if HASHES.exists() else {}
new, entries = {}, []
for f in sorted(SITE.rglob("*.html")):
    rel = str(f.relative_to(SITE))
    if f.name in SKIP: continue
    s = f.read_text(encoding="utf-8", errors="ignore")
    if re.search(r'<meta[^>]+name="robots"[^>]+noindex', s, re.I): continue
    m = re.search(r'<link rel="canonical" href="([^"]+)"', s)
    if not m: continue
    url = m.group(1)
    # skip pages whose canonical points elsewhere (duplicates that 301)
    stem = rel[:-5]
    if not (url.rstrip("/").endswith(stem) or url.endswith(rel) or (rel == "index.html" and url.endswith(".com/")) or (rel == "services/index.html" and url.endswith("/services/"))):
        continue
    h = hashlib.sha1(s.encode()).hexdigest()
    prev = old.get(url, {})
    lastmod = prev.get("lastmod", today) if prev.get("hash") == h else today
    new[url] = {"hash": h, "lastmod": lastmod}
    pr = "1.0" if url.endswith(".com/") else ("0.9" if "vrl-packers-and-movers" in url or re.search(r"packers-and-movers-[a-z-]+$", url) and "-to-" not in url else "0.8")
    entries.append((url, lastmod, pr))
seen = set(); out = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for url, lm, pr in entries:
    if url in seen: continue
    seen.add(url)
    out.append(f"  <url>\n    <loc>{url}</loc>\n    <lastmod>{lm}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>{pr}</priority>\n  </url>")
out.append("</urlset>")
(SITE / "sitemap.xml").write_text("\n".join(out) + "\n", encoding="utf-8")
HASHES.write_text(json.dumps(new, indent=0))
print(f"sitemap: {len(seen)} urls")
