# 1st VRL Packers and Movers website — rules for every session

Site: https://www.1stvrlpackersandmovers.com (static HTML, GoDaddy cPanel).
Owner: Deepak Giri. Talk to him in Hinglish.

## How publishing works
- `site/` in this repo = website files. Push to `main` → GoDaddy cron (`~/deploy/deploy.sh`, every 5–15 min) copies ONLY changed files under `site/` to `public_html/1stvrlpackersandmovers.com`.
- Deletions are NOT deployed. Never commit zips, csv, leads, backups.
- **Never create or edit `shifting-price.html`.** It lives only on the server.
- After adding pages run `python3 build/update_sitemap.py` (rebuilds `site/sitemap.xml` from canonicals).

## Generators
- `build/gen_vrl_pages.py site` → VRL brand page + VRL Tricity pages (shared head/hero/footer/styles used by all generators).
- `build/gen_city_routes.py site <city> ...` → `packers-and-movers-<city>` + `packers-and-movers-<city>-to-<dest>`; content in `build/city_data.py` (`CITY_DATA`, `ROUTE_EXTRA`).
## Publishing workflow (Deepak's rule: no page goes live without passing 2 checks)
1. **Writer:** a separate content-writer agent drafts each page's unique content (SEO-first: keyword in title/h1/first paragraph, real local areas, route facts, unique FAQs, natural Hinglish-free English) into `build/city_data.py`.
2. **Build:** run the generators.
3. **Check 1:** a separate checker agent (fresh, has not seen the writing) checks facts, geography, prices vs rate card, links, JSON-LD, titles/descriptions, mobile, duplicate text < 65% on 8-word shingles. Fix everything.
4. **Check 2:** a second fresh checker re-checks the fixed pages. Publish only if it reports no CRITICAL or SHOULD FIX items; otherwise fix and re-check.
5. Rebuild sitemap, commit, push. Confirm the live URLs return 200 after the next cron run.
6. **Competitors:** at least once a week compare against agarwalpackers.com, ompackersindia.com, porter.in and the top 3 Google results for the target keyword. Note what they do better (content, tools, trust signals, page types, internal links) in `build/COMPETITORS.md` and apply the honest, fitting ideas to our site. Never copy their text and never copy claims we cannot back (years, branches, IBA, awards).

## Facts (must be exact)
- Phone ONLY +91 82640 91243 (tel:+918264091243, wa.me/918264091243). 24-hour booking line.
- GSTIN 06AEYPV2101B1ZM, registered 27 Apr 2023. Proprietorship.
- Offices (own): #705, Sector-7, Panchkula, Haryana 134109 (head office); Jammu (Last Morh, Shop No.12, Block A, 22B, Gandhi Nagar, 180003); Shimla (Shop No-60, Ridge, Middle Bazar, The Mall, 171001). Zirakpur office is CLOSED — never show it.
- Other cities: work is done by verified partner teams. Never claim an office/branch there.
- Renamed from "VRL Packers and Movers" to "1st VRL Packers and Movers" in Oct 2026. Not affiliated with VRL Logistics Ltd.
- ISO 9001:2015 certified. No trademark (no ®). IBA approval belongs to a partner: "IBA-approved partner (code MUK-2068)" — never call the company IBA approved.
- 2000+ moves (company + partner network).
- Google rating 5.0 with 1200+ reviews across the Jammu and Shimla Google profiles (Deepak, 2026-11-11).
- Average callback time under 30 minutes (confirmed by Deepak, 2026-11-11) — keep this line on the quote form.
- No external links except WhatsApp and the Google Maps links of own offices. Do not link or redirect vrl-packers-movers.co.in.
- Exception (Deepak, 2026-11-11): the existing `share.google` links on packers-and-movers-jammu/shimla/india.html stay as they are. Do not remove them and never ask about them again. Do not add new ones.
- Keep "in-house crew" wording on old service pages.

## Approved rate card (excl. 18% GST) — do not change without Deepak
Bands by road km: up to 500 / 500–1,500 / 1,500+.
- House [local, ≤500, 500–1500, 1500+]: 1RK 3–6.5k, 8.5–15k, 13–23k, 18–32k; 1BHK 5–9k, 9.5–17k, 15–27k, 20–35k; 2BHK 8–15k, 13–24k, 20–36k, 27–47k; 3BHK 12–21k, 17–32k, 26–46k, 34–60k; 4BHK 17–29k, 23–41k, 34–58k, 44–78k.
- Car [≤500, 500–1500, 1500+]: Hatchback 5.5–9k, 9–15k, 13–22k; Sedan 6.5–10.5k, 10.5–17k, 15–25k; Compact SUV 7.5–12k, 12–19k, 17–28k; SUV/MUV 9–14k, 14–22k, 20–34k; Luxury enclosed 18–30k, 28–45k, 40–65k. No local car/bike rates.
- Bike: Scooter 2.5–4k, 3.5–5.5k, 4.5–7k; ≤150cc 3–4.5k, 4–6k, 5–7.5k; 150–350cc 4–6k, 5.5–8k, 7–10k; Premium 350+ 6–9k, 8–11.5k, 10–14.5k; Superbike crate 10–15k, 14–20k, 18–28k.
- Office [local, ≤500, 500–1500, 1500+]: Small ≤10 WS 12–25k, 25–45k, 40–70k, 55–90k; Medium 10–30 WS 25–60k, 50k–1L, 80k–1.5L, 1.1–2L; Large 30–100 WS 60k–1.5L, 1.2–2.5L, survey, survey; 100+ survey. Add-ons: workstation 800–2,000, server rack 3–8k.

## Standing page rules
- City page: one rate chart (house, all bands) + links to its route pages + unique local content + FAQs.
- Route page: unique journey/destination content, 4 rate charts (house, car by model, bike by model, office), route calculator, unique FAQs.
- Home page: one rate chart.

## SEO priority (in order)
1. "VRL Packers and Movers" (with and without city). 2. "VRL Packers and Movers <city>". 3. "Packers and movers <city>" + route pages. 4. "Packers and movers".
Queue and progress: `build/QUEUE.md`.
