#!/usr/bin/env python3
"""Generate the "VRL Packers and Movers" brand page and Tricity city pages
for 1stvrlpackersandmovers.com, reusing the Shimla page's styles and quote form."""
import json, re, sys, html
from pathlib import Path

SITE = Path(sys.argv[1])
BASE = "https://www.1stvrlpackersandmovers.com"
PHONE = "+918264091243"
PHONE_TXT = "+91 82640 91243"
WA = "https://wa.me/918264091243?text=Hi%2C%20I%20need%20a%20moving%20quote"
GSTIN = "06AEYPV2101B1ZM"
ADDR = "#705, Sector-7, Panchkula, Haryana 134109"
IBA = "MUK-2068"

shimla = (SITE / "packers-and-movers-shimla.html").read_text(encoding="utf-8")
STYLE = re.search(r"<style>.*?</style>", shimla, re.S).group(0)
STYLE = STYLE.replace("</style>", """.photo-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:20px}
.photo-grid img{width:100%;height:260px;object-fit:cover;border-radius:12px;display:block}
.photo-grid figure{margin:0}.photo-grid figcaption{font-size:13px;color:#5b6676;margin-top:6px;line-height:1.5}
.note{background:#fff7e6;border:1px solid #f3d9a4;border-radius:10px;padding:16px 18px;color:#5a4a26;font-size:14.5px;line-height:1.65}
.area-list{columns:3;gap:24px;padding-left:18px;margin:12px 0;color:#3c4757;line-height:1.9}
.city-links{display:flex;flex-wrap:wrap;gap:10px;margin-top:14px}
.city-links a{background:#fff;border:1px solid #dde3ec;border-radius:999px;padding:9px 16px;color:#0e2a47;font-weight:600;text-decoration:none;font-size:14px}
.city-links a:hover{border-color:#e8542f;color:#e8542f}
@media(max-width:960px){.photo-grid{grid-template-columns:1fr 1fr}.area-list{columns:2}}
@media(max-width:620px){.photo-grid{grid-template-columns:1fr}.area-list{columns:1}}
@media(max-width:960px){.hero-copy{order:1}.hero-form{order:2}}
</style>""")
STYLE = re.sub(r"\.trust-strip\{.*?@media\(max-width:860px\)\{\.trust-strip\{display:block\}\}\n", "", STYLE, flags=re.S)
FORM = re.search(r'<div class="quote-switch">.*?</script></div>', shimla, re.S).group(0)

RATES = """<div class="table-wrap"><table class="rate-table">
      <thead><tr><th>Home size</th><th>Local shift</th><th>Up to 500 km</th><th>500 to 1,500 km</th><th>1,500 km plus</th></tr></thead>
      <tbody>
        <tr><td>1 RK / Studio</td><td>Rs 3,000 - 6,500</td><td>Rs 8,500 - 15,000</td><td>Rs 13,000 - 23,000</td><td>Rs 18,000 - 32,000</td></tr>
        <tr><td>1 BHK</td><td>Rs 5,000 - 9,000</td><td>Rs 9,500 - 17,000</td><td>Rs 15,000 - 27,000</td><td>Rs 20,000 - 35,000</td></tr>
        <tr><td>2 BHK</td><td>Rs 8,000 - 15,000</td><td>Rs 13,000 - 24,000</td><td>Rs 20,000 - 36,000</td><td>Rs 27,000 - 47,000</td></tr>
        <tr><td>3 BHK</td><td>Rs 12,000 - 21,000</td><td>Rs 17,000 - 32,000</td><td>Rs 26,000 - 46,000</td><td>Rs 34,000 - 60,000</td></tr>
        <tr><td>4 BHK / Villa</td><td>Rs 17,000 - 29,000</td><td>Rs 23,000 - 41,000</td><td>Rs 34,000 - 58,000</td><td>Rs 44,000 - 78,000</td></tr>
      </tbody>
    </table></div>
    <p><strong>All figures exclude 18 per cent GST.</strong> The written estimate after the survey is the number paid at delivery. <a href="/moving-cost-calculator.html">Check your price band in the calculator</a>.</p>"""

def head(title, desc, slug, schema_list):
    url = f"{BASE}/{slug}"
    ld = "\n".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in schema_list)
    e = html.escape
    return f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="stylesheet" href="/assets/css/style.css">
{STYLE}
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#0e2a47">
<meta property="og:type" content="website">
<meta property="og:site_name" content="1st VRL Packers and Movers">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}/assets/img/vrl-team-uniform.webp">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
{ld}
</head>
<body>

<header class="site-header">
  <div class="container site-header__inner">
    <a class="brand" href="/">
      <img src="/assets/img/vrl-logo.webp" alt="1st VRL Packers and Movers logo" width="340" height="142">
      <span><span class="brand__name">1st VRL Packers and Movers</span></span>
    </a>
    <nav class="nav" aria-label="Main navigation">
      <a href="/">Home</a>
      <a href="/services/">Services</a>
      <a href="/about">About</a>
      <a href="/contact">Contact</a>
      <a class="nav__phone" href="tel:{PHONE}">{PHONE_TXT}</a>
      <a class="btn btn--primary" href="#quote" style="padding: 10px 20px;">Get Quote</a>
    </nav>
    <button class="nav-toggle" aria-label="Open menu" aria-expanded="false">&#9776;</button>
  </div>
</header>
"""

def hero(h1_html, para, page_id):
    form = FORM.replace('value="packers-and-movers-shimla"', f'value="{page_id}"').replace('action="quote-send.php"', 'action="/quote-send.php"')
    form = form.replace('<input type="hidden" name="page"', '<div class="hp-field" hidden><input name="website" type="text" tabindex="-1" autocomplete="off" aria-hidden="true"></div><input type="hidden" name="page"')
    return f"""
<section class="section">
  <div class="container hero-grid">
    <div class="hero-copy">
      <h1>{h1_html}</h1>
      <p>{para}</p>
      <div class="hero-cta">
        <a class="btn btn--primary" href="tel:{PHONE}">Call {PHONE_TXT}</a>
        <a class="btn btn--wa" href="{WA}" target="_blank" rel="noopener noreferrer">WhatsApp Us</a>
      </div>
    </div>
    <div class="hero-form" id="quote">
      <h2 style="margin:0 0 4px;font-size:20px;color:#0e2a47">Get your free moving quote</h2>
      <p class="sub">24-hour booking line. Average callback time under 30 minutes.</p>
      {form}
      <p class="fine">We call back with a written quote. No spam, no repeated follow-ups. By submitting you agree to be contacted about your move.</p>
    </div>
  </div>
</section>

<section class="section section--tint">
  <div class="container">
    <div class="conv-strip">
      <div class="conv-item"><span class="conv-num">2023</span><span class="conv-label">GST registered since April 2023, Panchkula</span></div>
      <div class="conv-item"><span class="conv-num">2000+</span><span class="conv-label">Moves done by our team and partner network</span></div>
      <div class="conv-item"><span class="conv-num">ISO</span><span class="conv-label">ISO 9001:2015 certified</span></div>
      <div class="conv-item"><span class="conv-num">24 hr</span><span class="conv-label">Booking line, all seven days</span></div>
    </div>
  </div>
</section>
"""

PHOTOS = """<div class="photo-grid">
      <figure><img src="/assets/img/vrl-team-uniform.webp" alt="1st VRL Packers and Movers crew in yellow uniform" width="794" height="836" loading="lazy"><figcaption>Our crew in the 1st VRL uniform.</figcaption></figure>
      <figure><img src="/assets/img/vrl-old-uniform-crew.webp" alt="VRL Packers and Movers crew in the earlier VRL uniform at a home shifting in the Tricity" width="1200" height="860" loading="lazy"><figcaption>The same team in the earlier VRL Packers and Movers uniform.</figcaption></figure>
      <figure><img src="/assets/img/vrl-crew-stretch-wrap.webp" alt="1st VRL packer stretch wrapping furniture" width="532" height="1008" loading="lazy"><figcaption>Stretch wrap over every furniture piece.</figcaption></figure>
      <figure><img src="/assets/img/vrl-crew-carton-lift.webp" alt="Packed carton sealed with 1st VRL branded tape" width="892" height="774" loading="lazy"><figcaption>Cartons sealed with our own branded tape.</figcaption></figure>
      <figure><img src="/assets/img/vrl-crew-wardrobe-taping.webp" alt="1st VRL crew taping a wrapped wardrobe panel" width="1200" height="581" loading="lazy"><figcaption>Wardrobe panels wrapped and taped before loading.</figcaption></figure>
    </div>"""

def trust_section():
    return f"""
<section class="section">
  <div class="container">
    <h2>Why people book with 1st VRL Packers and Movers</h2>
    <div class="trust-row">
      <div><strong>Written estimate</strong><span>Itemised before any advance is paid. The figure on paper is the figure at delivery.</span></div>
      <div><strong>One coordinator</strong><span>One person on your number from the survey to the last carton.</span></div>
      <div><strong>GST invoice</strong><span>GSTIN {GSTIN}. Verify it on the GST portal before you book.</span></div>
      <div><strong>Bank and PSU moves</strong><span>Moves for bank and PSU transfers through our IBA-approved partner, code {IBA}.</span></div>
    </div>
    <p style="margin-top:22px">Moves inside the Tricity are run by our Panchkula crew. For intercity moves, our coordinator stays with you throughout and our verified partner team in the destination city handles the unloading and setup, so you deal with one company and one bill.</p>
  </div>
</section>
"""

def faq_block(faqs):
    items = "\n".join(f'    <details class="faq-item"><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>' for q, a in faqs)
    return f"""
<section class="section section--tint">
  <div class="container">
    <h2>Common questions</h2>
{items}
  </div>
</section>
"""

def faq_schema(faqs):
    return {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]}

def business_schema(slug, area=None):
    s = {"@context":"https://schema.org","@type":"MovingCompany","@id":f"{BASE}/#business",
         "name":"1st VRL Packers and Movers",
         "alternateName":["VRL Packers and Movers","VRL Packers Movers","1st VRL Packers & Movers"],
         "url":f"{BASE}/","logo":f"{BASE}/assets/img/vrl-logo.webp","image":f"{BASE}/assets/img/vrl-team-uniform.webp",
         "telephone":PHONE,"email":"support@1stvrlpackersandmovers.com","taxID":GSTIN,"foundingDate":"2023-04-27",
         "priceRange":"Rs","currenciesAccepted":"INR",
         "address":{"@type":"PostalAddress","streetAddress":"#705, Sector-7","addressLocality":"Panchkula","addressRegion":"Haryana","postalCode":"134109","addressCountry":"IN"},
         "areaServed": [{"@type":"City","name":area}] if area else [{"@type":"Country","name":"India"}]}
    return s

def breadcrumb(name, slug):
    return {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Home","item":f"{BASE}/"},
        {"@type":"ListItem","position":2,"name":name,"item":f"{BASE}/{slug}"}]}

def city_links(exclude=None):
    links = [('/vrl-packers-and-movers','VRL Packers and Movers')] + [(f'/vrl-packers-and-movers-{k}', f'VRL Packers and Movers {v["name"]}') for k,v in CITIES.items()] + [('/packers-and-movers-shimla.html','Packers and Movers Shimla'),('/packers-and-movers-jammu.html','Packers and Movers Jammu')]
    return "\n".join(f'      <a href="{h}">{t}</a>' for h,t in links if h != exclude)

DISCLAIMER = "1st VRL Packers and Movers, Panchkula (formerly VRL Packers and Movers) is an independent proprietorship. It is not connected with VRL Logistics Ltd. or with other companies that use VRL in their name."

def footer():
    return f"""
<section class="section">
  <div class="container" style="text-align:center">
    <h2>Ready to get a price?</h2>
    <p>Call for a free survey and a written quote. No obligation, no spam.</p>
    <div class="hero-cta" style="justify-content:center">
      <a class="btn btn--primary" href="tel:{PHONE}">Call {PHONE_TXT}</a>
      <a class="btn btn--wa" href="{WA}" target="_blank" rel="noopener noreferrer">WhatsApp Us</a>
    </div>
  </div>
</section>

<footer class="site-footer">
  <div class="container">
    <div class="site-footer__grid">
      <div class="footer__brand">
        <img src="/assets/img/vrl-logo.webp" alt="1st VRL Packers and Movers logo" width="340" height="142">
        <p>Home and office shifting, car and bike transport and warehousing across India.</p>
      </div>
      <div>
        <h4>Services</h4>
        <a href="/services/home-shifting">Home Shifting</a>
        <a href="/services/office-relocation">Office Relocation</a>
        <a href="/services/local-shifting">Local Shifting</a>
        <a href="/services/intercity-relocation">Intercity Relocation</a>
        <a href="/services/car-transportation">Car Transport</a>
        <a href="/services/bike-transportation">Bike Transport</a>
        <a href="/services/warehouse-storage">Warehousing and Storage</a>
      </div>
      <div>
        <h4>Company</h4>
        <a href="/about">About us</a>
        <a href="/contact">Contact</a>
        <a href="/vrl-packers-and-movers">VRL Packers and Movers</a>
        <a href="/packers-and-movers-delhi">Packers and Movers Delhi</a>
        <a href="/privacy-policy">Privacy Policy</a>
        <a href="/terms">Terms and Conditions</a>
      </div>
      <div>
        <h4>Reach us</h4>
        <p><strong>Phone:</strong> <a href="tel:{PHONE}">{PHONE_TXT}</a></p>
        <p><strong>Email:</strong> support@1stvrlpackersandmovers.com</p>
        <p><strong>Office:</strong> {ADDR}</p>
        <p><strong>Jammu:</strong> Last Morh, Shop No.12, Block A, 22B, Gandhi Nagar, Jammu, J&amp;K 180003</p>
        <p><strong>Shimla:</strong> Shop No-60, Ridge, Middle Bazar, The Mall, Shimla, Himachal Pradesh 171001</p>
      </div>
    </div>
    <p style="font-size:12.5px;opacity:.8;margin:18px 0 0;line-height:1.6">{DISCLAIMER}</p>
    <div class="site-footer__bottom">
      <span>&copy; <span id="year">2026</span> 1st VRL Packers and Movers. All rights reserved.</span>
      <span>GSTIN: {GSTIN}</span>
      <span>ISO 9001:2015 certified</span>
    </div>
  </div>
</footer>
<script src="/assets/js/main.js"></script>

<div class="mobile-cta">
  <a class="btn btn--primary" href="tel:{PHONE}">Call Now</a>
  <a class="btn btn--wa" href="https://wa.me/918264091243">WhatsApp</a>
</div>
</body>
</html>
"""

# ---------- Brand page ----------
def brand_page():
    slug = "vrl-packers-and-movers"
    faqs = [
     ("Is 1st VRL Packers and Movers the same as VRL Packers and Movers?", "Yes. VRL Packers and Movers in Panchkula changed its name to 1st VRL Packers and Movers in October 2026. The owner, the team, the office at Sector 7 Panchkula and the GST number 06AEYPV2101B1ZM are the same."),
     ("Are you part of VRL Logistics?", "No. 1st VRL Packers and Movers is an independent proprietorship based in Panchkula. It has no connection with VRL Logistics Ltd. or with other companies that use VRL in their name in Pune, Hyderabad, Mumbai or elsewhere."),
     ("How do I know I am talking to the original 1st VRL team?", "Our only booking number is +91 82640 91243 and our email ends in @1stvrlpackersandmovers.com. Every estimate and invoice carries GSTIN 06AEYPV2101B1ZM, which you can check on the GST portal. If someone quotes in our name from another number, call us before paying anything."),
     ("Do you shift outside the Tricity?", "Yes. We run local moves in Panchkula, Zirakpur, Chandigarh and Mohali with our own crew, and intercity moves across India with our verified partner teams in the destination city. One coordinator and one bill cover the whole move."),
     ("Can bank and PSU employees get a bill for their transfer claim?", "Yes. For bank and PSU transfers we arrange the move through our IBA-approved partner (code MUK-2068), so the bill and the documents match what the transfer claim needs."),
     ("How much does a move cost?", "A local 1 BHK move usually costs Rs 5,000 to 9,000 and a local 2 BHK Rs 8,000 to 15,000. Intercity moves depend on distance and volume. All figures exclude 18 per cent GST, and the written estimate after the survey is the final number."),
    ]
    schemas = [business_schema(slug), faq_schema(faqs), breadcrumb("VRL Packers and Movers", slug)]
    title = "VRL Packers and Movers | Now 1st VRL Packers and Movers, Panchkula"
    desc = "VRL Packers and Movers, Panchkula is now 1st VRL Packers and Movers. Home, office, car and bike shifting across India. Call +91 82640 91243."
    body = head(title, desc, slug, schemas)
    body += hero('VRL Packers and Movers <span class="accent">is now 1st VRL</span>',
                 "VRL Packers and Movers, Panchkula changed its name to 1st VRL Packers and Movers in October 2026. The team, the Sector 7 Panchkula office, the phone number and the GST number are unchanged. We shift homes, offices, cars and bikes across the Tricity and across India.",
                 slug)
    body += f"""
<section class="section" id="name-change">
  <div class="container">
    <h2>Why the name changed, and what stayed the same</h2>
    <div class="split">
      <div>
        <p>Many unrelated companies across India use the letters VRL in their name. Customers searching for us were landing on other firms, and some were being quoted in our name by people we have never worked with. Adding "1st" gives our company a name that belongs only to us.</p>
        <p>Nothing else changed, and since then the company has also become ISO 9001:2015 certified. If you moved with VRL Packers and Movers in Panchkula, Zirakpur, Chandigarh or Mohali before, you are dealing with the same people today.</p>
      </div>
      <div>
        <ul class="inc">
          <li><strong>Same owner and team.</strong> The crew in the photos below.</li>
          <li><strong>Same office:</strong> {ADDR}</li>
          <li><strong>Same GSTIN:</strong> {GSTIN}, registered since April 2023</li>
          <li><strong>Same booking line:</strong> <a href="tel:{PHONE}">{PHONE_TXT}</a></li>
          <li><strong>Same 24-hour booking line,</strong> all seven days</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="section section--tint">
  <div class="container">
    <h2>Our team, then and now</h2>
    <p>Real photos from our jobs. The older uniform says VRL Packers and Movers, the new one says 1st VRL. The cartons are sealed with our own printed tape.</p>
    {PHOTOS}
  </div>
</section>

<section class="section">
  <div class="container">
    <h2>How to make sure you are talking to the original 1st VRL</h2>
    <div class="note">
      <p style="margin:0 0 8px"><strong>Check these four things before you pay an advance:</strong></p>
      <p style="margin:0">1. The number is {PHONE_TXT}. 2. The estimate and invoice show GSTIN {GSTIN} and the name 1st VRL Packers and Movers. 3. Email comes only from @1stvrlpackersandmovers.com. 4. The advance is 10 to 20 per cent, never most of the bill. If anything does not match, call us on {PHONE_TXT} first.</p>
    </div>
    <p style="margin-top:18px;font-size:14px;color:#5b6676">{DISCLAIMER}</p>
  </div>
</section>
"""
    body += trust_section()
    body += f"""
<section class="section section--tint">
  <div class="container">
    <h2>What a move costs</h2>
    <p>These are the price bands for a full-service job: packing, labour, transport in a sized vehicle and up to one flight of stairs, or any floor with a working lift.</p>
    {RATES}
  </div>
</section>

<section class="section">
  <div class="container">
    <h2>VRL Packers and Movers near you</h2>
    <p>Local pages for the cities we serve most:</p>
    <div class="city-links">
{city_links(exclude='/'+slug)}
    </div>
  </div>
</section>
"""
    body += faq_block(faqs)
    body += footer()
    return slug, body

CITIES = {
 "panchkula": dict(name="Panchkula", state="Haryana",
   intro="Our office is in Sector 7, Panchkula, so moves inside Panchkula are handled by the team that sits a few minutes from your door. Survey, packing, loading and delivery are run by the same coordinator from start to finish.",
   local="Panchkula is laid out in sectors with a mix of kothis, MDC houses, builder floors and society flats. Kothi moves usually mean wide gates and easy truck access but more furniture per room, so we send a bigger crew. Society flats in the upper sectors and on the Amravati Enclave side need the lift booked and a move-in slot from the society office, which we fix during the survey.",
   areas=["All Panchkula sectors","MDC Sector 4, 5 and 6","Industrial Area Phase 1 and 2","Pinjore","Kalka","Raipur Rani","Barwala","Morni Road","Amravati Enclave","Surajpur","Majri Chowk"],
   routes=["Panchkula to Delhi","Panchkula to Gurugram","Panchkula to Noida","Panchkula to Jaipur","Panchkula to Bengaluru","Panchkula to Pune"],
   example="A 3 BHK kothi in Sector 9 moving to a flat in Sector 20 is a local move of roughly Rs 12,000 to 21,000 plus GST, depending on the furniture count and how many floors the goods go up at the new place.",
   photos=["vrl-team-uniform","vrl-old-uniform-crew","vrl-crew-wardrobe-taping"],
   faqs=[("Is your office really in Panchkula?","Yes. Our office is at #705, Sector-7, Panchkula, Haryana 134109, and the same address is on our GST registration. You are welcome to visit before you book."),
         ("Do you shift kothis and MDC houses with a lot of furniture?","Yes. For kothis we send a larger crew, dismantle beds and wardrobes on the spot and wrap every panel before loading. The survey tells us how many people and which vehicle the job needs."),
         ("Do you cover Pinjore, Kalka and Barwala?","Yes. Pinjore, Kalka, Barwala, Raipur Rani and the Morni Road side are covered by the same Panchkula team, with the same written estimate.")]),
 "zirakpur": dict(name="Zirakpur", state="Punjab",
   intro="Zirakpur is one of the busiest shifting markets in the Tricity, with new societies on VIP Road, Patiala Road and the Peer Muchalla side handing over flats every year. Our Panchkula team is close by and completes most 1 and 2 BHK Zirakpur moves in a single day.",
   local="Most Zirakpur moves are high-rise society flats. That means a lift booking, a fixed move-in window and, in some societies, a refundable shifting deposit. Traffic on the Zirakpur flyover and the Chandigarh-Ambala highway decides the loading time, so we plan for the truck to reach the gate before the peak hours.",
   areas=["VIP Road","Patiala Road","Ambala Highway","Dhakoli","Baltana","Peer Muchalla","Bhabat","Lohgarh","Gazipur","Singhpura","Kishanpura","Nabha Sahib","Highland Marg"],
   routes=["Zirakpur to Delhi","Zirakpur to Gurugram","Zirakpur to Jaipur","Zirakpur to Bengaluru","Zirakpur to Hyderabad","Zirakpur to Mumbai"],
   example="A 2 BHK flat on VIP Road moving to a society in Mohali is a local move of roughly Rs 8,000 to 15,000 plus GST. A society shifting deposit, if your society asks for one, is refundable and paid to the society, not to us.",
   photos=["vrl-crew-stretch-wrap","vrl-crew-carton-lift","vrl-old-uniform-crew"],
   faqs=[("My society asks for a shifting deposit. What is it?","Many Zirakpur societies take a refundable deposit before a move to cover any damage to lifts or common areas. It is paid to the society, not to us, and is returned after the move. We help you book the lift slot and the gate pass."),
         ("What time is best to load in Zirakpur?","Early morning or after the evening rush. Traffic on the flyover and the Ambala highway can hold a truck for an hour at peak times, so we schedule the truck to reach your gate before it builds up."),
         ("Can my move be finished in one day in Zirakpur?","Most 1 and 2 BHK flats are packed, moved and set up in one day when the booking is confirmed a day earlier and the lift slot is fixed. A 3 BHK or a move with a short lift window may need two days.")]),
 "chandigarh": dict(name="Chandigarh", state="Chandigarh",
   intro="Chandigarh moves are handled from our Panchkula office, a short drive away. Government houses, sector kothis and flats in Manimajra and the southern sectors each need a different plan, and the survey decides the crew size and the vehicle before the day.",
   local="Many Chandigarh moves are employee transfers: government, bank and PSU staff moving in or out of the city. These moves often need a proper GST bill and an itemised estimate for the transfer claim. For bank and PSU employees we can arrange the move through our IBA-approved partner so the bill matches what the claim needs.",
   areas=["Sector 1 to Sector 56","Manimajra","Modern Housing Complex","IT Park","Industrial Area Phase 1 and 2","Mauli Jagran","Daria","Dhanas","Kaimbwala","Hallomajra","Behlana","Maloya"],
   routes=["Chandigarh to Delhi","Chandigarh to Gurugram","Chandigarh to Lucknow","Chandigarh to Jaipur","Chandigarh to Bengaluru","Chandigarh to Kolkata"],
   example="A transferred employee moving a 2 BHK from a government house in Chandigarh to Delhi is an intercity move of roughly Rs 13,000 to 24,000 plus GST, with an itemised GST bill for the transfer claim.",
   photos=["vrl-team-uniform","vrl-crew-carton-lift","vrl-crew-wardrobe-taping"],
   faqs=[("I am a bank or PSU employee on transfer. Can I get an IBA bill?","Yes. For bank and PSU transfers we arrange the move through our IBA-approved partner (code MUK-2068), so the bill and documents match what your transfer claim needs. Tell us at the time of booking."),
         ("Do you shift government houses that must be vacated by a date?","Yes. Tell us the date by which the house must be handed over and we plan the packing a day or two earlier, so the house is empty and clean in time."),
         ("Do you handle office shifting in the IT Park and Industrial Area?","Yes. Office moves are planned after working hours or over a weekend, with systems, files and furniture labelled desk by desk so work can restart the next day.")]),
 "mohali": dict(name="Mohali", state="Punjab",
   intro="Mohali has grown fast along Airport Road, Aerocity and the IT City side, and a large share of its moves are IT and corporate employees shifting in or out on short notice. Our Panchkula team covers Mohali, Kharar and New Chandigarh with a free survey and a written quote.",
   local="Mohali mixes old phase houses, new high-rise societies on Airport Road and the Kharar belt, and offices in the IT City and Industrial Area. Office moves are planned after working hours so desks and systems are ready for the next morning. For societies we confirm the lift slot and the gate pass with the management a day before.",
   areas=["Phase 1 to Phase 11","Sector 62 to Sector 91","Airport Road","Aerocity","IT City","Industrial Area","Kharar","Sunny Enclave","New Chandigarh","Landran","Banur","Sohana"],
   routes=["Mohali to Delhi","Mohali to Gurugram","Mohali to Noida","Mohali to Bengaluru","Mohali to Pune","Mohali to Hyderabad"],
   example="A 2 BHK flat on Airport Road moving to Bengaluru is a long-distance move of roughly Rs 27,000 to 47,000 plus GST, with the car or bike quoted separately if it travels too.",
   photos=["vrl-crew-stretch-wrap","vrl-team-uniform","vrl-old-uniform-crew"],
   faqs=[("I have joined a new job and need to move within a week. Is that possible?","Usually yes. A video survey can be done the same day, and most local Mohali moves can be scheduled within two to four days of booking. Intercity moves need a little more time to fix the vehicle."),
         ("Can you move my car or bike along with the household goods?","Yes. Cars go on a separate carrier and bikes are cradle-packed. Each is quoted as its own line on the estimate so you can see exactly what it costs."),
         ("Do you cover Kharar and New Chandigarh?","Yes. Kharar, Sunny Enclave, New Chandigarh, Landran and Banur are covered by the same team with the same written estimate.")]),
}

PHOTO_META = {
 "vrl-team-uniform": ("794","836","1st VRL Packers and Movers crew in yellow uniform","Our crew in the 1st VRL uniform."),
 "vrl-old-uniform-crew": ("1200","860","VRL Packers and Movers crew in the earlier VRL uniform at a home shifting","The same team in the earlier VRL Packers and Movers uniform."),
 "vrl-crew-stretch-wrap": ("532","1008","1st VRL packer stretch wrapping furniture","Stretch wrap over every furniture piece."),
 "vrl-crew-carton-lift": ("892","774","Packed carton sealed with 1st VRL branded tape","Cartons sealed with our own branded tape."),
 "vrl-crew-wardrobe-taping": ("1200","581","1st VRL crew taping a wrapped wardrobe panel","Wardrobe panels wrapped and taped before loading."),
}
def photo_grid(keys, city):
    figs = "".join(f'<figure><img src="/assets/img/{k}.webp" alt="{PHOTO_META[k][2]}, {city}" width="{PHOTO_META[k][0]}" height="{PHOTO_META[k][1]}" loading="lazy"><figcaption>{PHOTO_META[k][3]}</figcaption></figure>' for k in keys)
    return f'<div class="photo-grid">{figs}</div>'

def city_page(key, c):
    slug = f"vrl-packers-and-movers-{key}"
    n = c["name"]
    faqs = [(f"Is VRL Packers and Movers {n} the same as 1st VRL Packers and Movers?", f"Yes. VRL Packers and Movers changed its name to 1st VRL Packers and Movers in October 2026. {n} moves are run by the same team from our Sector 7, Panchkula office, under the same GSTIN {GSTIN}.")] + c["faqs"]
    schemas = [business_schema(slug, area=n), faq_schema(faqs), breadcrumb(f"VRL Packers and Movers {n}", slug)]
    title = f"VRL Packers and Movers {n} | Now 1st VRL Packers and Movers"
    desc = f"VRL Packers and Movers {n} is now 1st VRL. Home and office shifting with free survey, written quote and GST bill. Call {PHONE_TXT}."
    areas = "".join(f"<li>{html.escape(a)}</li>" for a in c["areas"])
    routes = " &middot; ".join(html.escape(r) for r in c["routes"])
    body = head(title, desc, slug, schemas)
    body += hero(f'VRL Packers and Movers <span class="accent">in {n}</span>',
                 f"{c['intro']} We were known as VRL Packers and Movers and now work as 1st VRL Packers and Movers, with the same team and the same GST number.",
                 slug)
    body += f"""
<section class="section">
  <div class="container">
    <h2>Shifting in {n}: what we plan for</h2>
    <p>{c['local']}</p>
    <h3 style="margin-top:22px">Areas we cover in and around {n}</h3>
    <ul class="area-list">{areas}</ul>
    <p><strong>Popular intercity routes:</strong> {routes}, and every other major city in India. For moves outside the Tricity, our coordinator stays with you and our verified partner team in the destination city handles unloading and setup, under one bill.</p>
    <p><strong>Office:</strong> {ADDR}. <strong>Phone:</strong> <a href="tel:{PHONE}">{PHONE_TXT}</a>, 24-hour booking line, all seven days.</p>
  </div>
</section>

<section class="section section--tint">
  <div class="container">
    <h2>What a move costs in {n}</h2>
    <p><strong>Example:</strong> {c['example']}</p>
    <p>General price bands for a full-service job: packing, labour, transport in a sized vehicle and up to one flight of stairs, or any floor with a working lift.</p>
    {RATES}
  </div>
</section>

<section class="section">
  <div class="container">
    <h2>Our team at work</h2>
    <p>Real photos from our jobs, in the old VRL uniform and the new 1st VRL uniform. Estimates and invoices carry GSTIN {GSTIN}; bank and PSU transfers are handled through our IBA-approved partner (code {IBA}).</p>
    {photo_grid(c['photos'], n)}
  </div>
</section>

<section class="section section--tint">
  <div class="container">
    <h2>Other VRL Packers and Movers pages</h2>
    <div class="city-links">
{city_links(exclude='/'+slug)}
    </div>
  </div>
</section>
"""
    body += faq_block(faqs).replace('section--tint','section', 1)
    body += footer()
    return slug, body

if __name__ == "__main__":
    out = []
    out.append(brand_page())
    for k, c in CITIES.items():
        out.append(city_page(k, c))
    for slug, content in out:
        (SITE / f"{slug}.html").write_text(content, encoding="utf-8")
        print("wrote", slug, len(content))
