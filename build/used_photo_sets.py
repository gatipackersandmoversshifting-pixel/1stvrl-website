#!/usr/bin/env python3
"""List the photo sets already used by generated pages (VRL city pages + packers-and-movers city/route pages).
New pages must use a 4-photo set (as an unordered set) that is not in this list. Usage: python3 build/used_photo_sets.py [--check k1,k2,k3,k4]"""
import sys, re
from pathlib import Path
SITE = Path(__file__).parent.parent / "site"
sets = {}
for f in sorted(SITE.glob("*.html")):
    t = f.read_text(encoding="utf-8", errors="ignore")
    ks = tuple(sorted(set(re.findall(r'src="/assets/img/((?:sp|crew)/[a-z0-9-]+)\.webp', t)) - {"crew/crew-team-banner", "crew/crew-team-banner-mobile"}))
    if ks: sets.setdefault(ks, []).append(f.stem)
if len(sys.argv) > 2 and sys.argv[1] == "--check":
    want = tuple(sorted(sys.argv[2].split(",")))
    print("USED by " + ", ".join(sets[want]) if want in sets else "free")
else:
    for ks, pages in sorted(sets.items(), key=lambda x: -len(x[1])):
        print(len(pages), " | ".join(ks), "<-", ", ".join(pages[:4]))
