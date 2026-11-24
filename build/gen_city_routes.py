#!/usr/bin/env python3
"""City pages + route pages for 1stvrlpackersandmovers.com.
Usage: python3 gen_city_routes.py <site_dir> <city_key> [<city_key> ...]
Reuses head/hero/footer/style from gen_vrl_pages.py so the design matches."""
import sys, json, html
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import gen_vrl_pages as G
from city_data import CITY_DATA, ROUTE_EXTRA

SITE = Path(sys.argv[1])
BASE = G.BASE
e = html.escape

# ---------- approved rate cards (excl. GST) ----------
BANDS = ["Up to 500 km", "500 to 1,500 km", "1,500 km plus"]
HOUSE = [  # [local, <=500, 500-1500, 1500+]
 ("1 RK / Studio", [(3000,6500),(8500,15000),(13000,23000),(18000,32000)]),
 ("1 BHK", [(5000,9000),(9500,17000),(15000,27000),(20000,35000)]),
 ("2 BHK", [(8000,15000),(13000,24000),(20000,36000),(27000,47000)]),
 ("3 BHK", [(12000,21000),(17000,32000),(26000,46000),(34000,60000)]),
 ("4 BHK / Villa", [(17000,29000),(23000,41000),(34000,58000),(44000,78000)]),
]
CAR = [
 ("Hatchback", "Alto, WagonR, Swift, i10, i20, Tiago", [(5500,9000),(9000,15000),(13000,22000)]),
 ("Sedan", "Dzire, Amaze, City, Verna, Slavia", [(6500,10500),(10500,17000),(15000,25000)]),
 ("Compact SUV", "Brezza, Nexon, Venue, Creta, Seltos", [(7500,12000),(12000,19000),(17000,28000)]),
 ("SUV / MUV", "Ertiga, Innova, XUV700, Scorpio, Fortuner", [(9000,14000),(14000,22000),(20000,34000)]),
 ("Luxury (enclosed carrier)", "BMW, Audi, Mercedes", [(18000,30000),(28000,45000),(40000,65000)]),
]
BIKE = [
 ("Scooter", "Activa, Jupiter, Access", [(2500,4000),(3500,5500),(4500,7000)]),
 ("Bike up to 150cc", "Splendor, Shine, Pulsar 150", [(3000,4500),(4000,6000),(5000,7500)]),
 ("150cc to 350cc", "Classic 350, Bullet, Apache, Duke 200", [(4000,6000),(5500,8000),(7000,10000)]),
 ("Premium 350cc plus", "RE 650, Duke 390, Dominar, Himalayan", [(6000,9000),(8000,11500),(10000,14500)]),
 ("Superbike (wooden crate)", "Ninja, Harley, BMW", [(10000,15000),(14000,20000),(18000,28000)]),
]
OFFICE = [  # [local, <=500, 500-1500, 1500+]; None = on survey
 ("Small office", "up to 10 workstations", [(12000,25000),(25000,45000),(40000,70000),(55000,90000)]),
 ("Medium office", "10 to 30 workstations", [(25000,60000),(50000,100000),(80000,150000),(110000,200000)]),
 ("Large office", "30 to 100 workstations", [(60000,150000),(120000,250000),None,None]),
 ("Corporate HQ", "100+ seats", [None,None,None,None]),
]

def inr(n):
    s = str(n)
    if len(s) <= 3: return s
    last3, rest = s[-3:], s[:-3]
    parts = []
    while len(rest) > 2:
        parts.insert(0, rest[-2:]); rest = rest[:-2]
    if rest: parts.insert(0, rest)
    return ",".join(parts) + "," + last3
def rng(r): return "On survey" if r is None else f"Rs {inr(r[0])} - {inr(r[1])}"
def band_of(km): return 0 if km <= 500 else (1 if km <= 1500 else 2)

def tbl(head, rows):
    th = "".join(f"<th>{h}</th>" for h in head)
    tr = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<div class="table-wrap"><table class="rate-table"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'

GST_NOTE = '<p><strong>All figures exclude 18 per cent GST.</strong> The written estimate after the survey is the final number paid at delivery.</p>'

def calculator(slug, b, km, frm, to):
    data = {
      "house": [[n, r[b+1]] for n, r in HOUSE],
      "car":   [[n + " - " + m, r[b]] for n, m, r in CAR],
      "bike":  [[n + " - " + m, r[b]] for n, m, r in BIKE],
      "office":[[n + ", " + m, r[b+1]] for n, m, r in OFFICE],
    }
    return f"""<div class="calc" id="calc">
  <div class="calc__row">
    <label>What are you moving?<select id="calc-type"><option value="house">Household (BHK)</option><option value="car">Car</option><option value="bike">Bike / scooter</option><option value="office">Office</option></select></label>
    <label>Size or model<select id="calc-item"></select></label>
  </div>
  <p class="calc__out" id="calc-out" aria-live="polite">Select a type to see the price band.</p>
  <p class="calc__fine">{e(frm)} to {e(to)}, about {inr(km)} km. Price band excludes 18 per cent GST. Call <a href="tel:{G.PHONE}">{G.PHONE_TXT}</a> for a written quote.</p>
</div>
<script>(function(){{var D={json.dumps(data)};var t=document.getElementById('calc-type'),i=document.getElementById('calc-item'),o=document.getElementById('calc-out');
function f(n){{return n.toLocaleString('en-IN');}}
function fill(){{var rows=D[t.value];i.innerHTML='';rows.forEach(function(r,k){{var op=document.createElement('option');op.value=k;op.textContent=r[0];i.appendChild(op);}});show();}}
function show(){{var r=D[t.value][i.value||0][1];o.innerHTML=r?'Estimated price: <strong>Rs '+f(r[0])+' to Rs '+f(r[1])+'</strong> + GST':'<strong>Priced after a free survey.</strong> Call us for a written quote.';}}
t.addEventListener('change',fill);i.addEventListener('change',show);fill();}})();</script>"""

EXTRA_CSS = """<style>
.calc{background:#fff;border:2px solid #0e2a47;border-radius:14px;padding:20px;margin:18px 0}
.calc__row{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.calc label{display:block;font-size:13px;font-weight:700;color:#0e2a47}
.calc select{display:block;width:100%;margin-top:6px;padding:12px;border:1px solid #cfd8e3;border-radius:8px;font-size:15px;min-height:46px;background:#fff}
.calc__out{font-size:20px;color:#0e2a47;margin:16px 0 6px}
.calc__out strong{color:#e8542f}
.calc__fine{font-size:13px;color:#5b6676;margin:0}
.route-facts{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin:18px 0}
.route-facts div{background:#fff;border:1px solid #e4e8ef;border-radius:10px;padding:14px;text-align:center}
.route-facts strong{display:block;font-size:20px;color:#0e2a47}
.route-facts span{font-size:13px;color:#5b6676}
.rate-tabs h3{margin:26px 0 6px}
@media(max-width:700px){.calc__row,.route-facts{grid-template-columns:1fr 1fr}}
@media(max-width:480px){.calc__row{grid-template-columns:1fr}.route-facts strong{font-size:16px}}
</style>
</head>"""

def head(title, desc, slug, schemas):
    h = G.head(title, desc, slug, schemas)
    return h.replace("</head>", EXTRA_CSS, 1)

def service_schema(name, slug, areas):
    return {"@context":"https://schema.org","@type":"Service","name":name,"serviceType":"Packers and movers",
            "url":f"{BASE}/{slug}","provider":{"@id":f"{BASE}/#business"},
            "areaServed":[{"@type":"City","name":a} for a in areas]}

def crumbs(items):
    return {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":i+1,"name":n,"item":f"{BASE}/{s}" if s else f"{BASE}/"} for i,(n,s) in enumerate(items)]}

def faq_section(faqs):
    return G.faq_block(faqs)

# ---------- 2026-11-22: richer content for new city/route pages (Deepak 2026-11-16 + 2026-11-21) ----------
import hashlib
def _pick(key):
    h = int(hashlib.md5(key.encode()).hexdigest(), 16)
    return lambda opts, salt: opts[(h >> (salt * 4)) % len(opts)]

def more_sections(more, start_tint=False):
    out = ""
    for i, (h, ps) in enumerate(more or []):
        tint = ' section--tint' if (i % 2 == 1) != start_tint else ''
        paras = ''.join(f'<p>{p}</p>' for p in (ps if isinstance(ps, (list, tuple)) else [ps]))
        out += f"""
<section class="section{tint}">
  <div class="container">
    <h2>{e(h)}</h2>
    {paras}
  </div>
</section>
"""
    return out

def photo_block(keys, city, title, lead, partner=True):
    if not keys: return ""
    return f"""
<section class="section">
  <div class="container">
    <h2>{e(title)}</h2>
    <p>{lead}</p>
    {G.photo_grid(keys, None, partner, city)}
  </div>
</section>
"""

def city_keyword_section(ck, c):
    n = c["name"]; v = _pick(ck)
    ar = [a for a in c["areas"] if " and " not in a][:6]
    a1 = ", ".join(e(a) for a in ar[:-1]) + f" and {e(ar[-1])}"
    h2 = v([f"Packers and movers {n}: house, car and bike shifting", f"Home, car and bike shifting with packers and movers in {n}", f"Packers and movers in {n} for homes, cars and bikes"], 1)
    p1 = v([
        f"People find us by searching packers and movers {n}, home shifting in {n} or by our old name, VRL Packers and Movers {n}. Every booking reaches the same 24-hour line, and homes in {a1} get the same written estimate and GST bill.",
        f"Whether you type packers and movers {n}, {n} shifting charges or VRL Packers and Movers {n}, the call comes to one 24-hour line. Families in {a1} get one written estimate, one coordinator and one GST bill.",
        f"Home shifting in {n} is booked the same way from {a1} and every other part of the city: one call, a survey, a written quote. Some customers still search for us as VRL Packers and Movers {n}, our name before October 2026."], 2)
    p2 = v([
        f"Car shifting from {n} is quoted on the same estimate as the house. Up to 500 km, a hatchback on a car carrier is roughly Rs 5,500 to 9,000 plus GST and a sedan roughly Rs 6,500 to 10,500 plus GST; from 500 to 1,500 km a hatchback is roughly Rs 9,000 to 15,000 plus GST. Bike shifting up to 500 km is roughly Rs 2,500 to 4,000 plus GST for a scooter and Rs 3,000 to 4,500 plus GST for a bike up to 150cc.",
        f"A car or bike leaving {n} gets its own line on the quote. For 500 to 1,500 km, a compact SUV is roughly Rs 12,000 to 19,000 plus GST and an SUV or MUV roughly Rs 14,000 to 22,000 plus GST. A scooter over the same distance is roughly Rs 3,500 to 5,500 plus GST and a 150 to 350cc bike roughly Rs 5,500 to 8,000 plus GST.",
        f"Vehicles from {n} move on the same booking. Over 1,500 km, a hatchback is roughly Rs 13,000 to 22,000 plus GST and a sedan roughly Rs 15,000 to 25,000 plus GST; a bike up to 150cc is roughly Rs 5,000 to 7,500 plus GST and a premium bike above 350cc roughly Rs 10,000 to 14,500 plus GST. There is no separate local car or bike rate."], 3)
    p3 = v([
        f"Looking for the best packers and movers in {n}? Judge any company, including us, on four plain checks: a written estimate with a GSTIN, an item list signed at loading and at delivery, one named coordinator, and a phone number you can call back.",
        f"To pick the best packers and movers {n} has for your move, ask three things before paying anything: the quote in writing with a GST number on it, the name of the person on the phone during transit, and the inventory sheet before the truck leaves.",
        f"Every company claims to be the best packers and movers in {n}, so ask for proof instead: a GST invoice, a signed inventory list, photos of your car or bike at pickup and a written figure before any advance. We give all of these in writing."], 4)
    ph = c.get("photos", [])[:2]
    return f"""
<section class="section">
  <div class="container">
    <h2>{e(h2)}</h2>
    <p>{p1}</p>
    {G.photo_grid(ph, None, c.get("team") != "own", n)}
    <p>{p2}</p>
    <p>{p3}</p>
  </div>
</section>
"""

def route_keyword_section(ck, c, r, b):
    frm, to = c["name"], r["to"]; v = _pick(ck + r["key"])
    hb, sd, sv = (CAR[0][2][b], CAR[1][2][b], CAR[3][2][b]); sc, bk = BIKE[0][2][b], BIKE[1][2][b]
    h2 = v([f"Packers and movers {frm} to {to}: house, car and bike", f"{frm} to {to} shifting: house, car and bike on one booking", f"Car and bike shifting from {frm} to {to}, with the house"], 1)
    p1 = v([
        f"Searches for packers and movers {frm} to {to}, {frm} to {to} shifting charges or VRL Packers and Movers {frm} all reach the same 24-hour line. You get one written estimate and one GST bill for the whole {frm} to {to} move.",
        f"Whether you look for {frm} to {to} packers and movers, home shifting from {frm} to {to} or our old name, VRL Packers and Movers {frm}, the booking comes to one coordinator who stays on your number until the last carton is unpacked in {to}.",
        f"Most customers on this route search for {frm} to {to} shifting charges first. The charts above answer that, and the survey turns the band into one written figure. Some still know us as VRL Packers and Movers {frm}, our name before October 2026."], 2)
    p2 = v([
        f"Car shifting from {frm} to {to} on a carrier is roughly {rng(hb)} for a hatchback, {rng(sd)} for a sedan and {rng(sv)} for an SUV or MUV, plus GST. Bike shifting is roughly {rng(sc)} for a scooter and {rng(bk)} for a bike up to 150cc, plus GST.",
        f"For the car, budget roughly {rng(sd)} plus GST for a sedan or {rng(hb)} plus GST for a hatchback on this route; an SUV or MUV is roughly {rng(sv)} plus GST. A scooter goes for roughly {rng(sc)} and a motorcycle up to 150cc for roughly {rng(bk)}, both plus GST.",
        f"A bike packed in foam and cardboard costs roughly {rng(bk)} plus GST up to 150cc and {rng(sc)} plus GST for a scooter. A car on a carrier costs roughly {rng(hb)} plus GST for a hatchback, {rng(sd)} plus GST for a sedan and {rng(sv)} plus GST for an SUV or MUV."], 3)
    p3 = v([
        f"Looking for the best packers and movers from {frm} to {to}? Judge any company, including us, on plain checks: a written estimate with a GSTIN, a signed item list at both ends, a named coordinator and a driver number shared at loading.",
        f"Before you choose the best packers and movers for {frm} to {to}, ask for the quote in writing with a GST number, the inventory sheet before the truck leaves and photos of the car or bike at pickup. A genuine mover agrees to all of it.",
        f"Every company claims to be the best packers and movers from {frm} to {to}, so ask for proof instead of promises: a GST invoice, a signed inventory list, transit insurance offered in writing and no advance before the estimate is on paper."], 4)
    ph = r.get("photos", [])[:2]
    return f"""
<section class="section">
  <div class="container">
    <h2>{e(h2)}</h2>
    <p>{p1}</p>
    {G.photo_grid(ph, None, c.get("team") != "own", frm)}
    <p>{p2}</p>
    <p>{p3}</p>
  </div>
</section>
"""

# ---------- route page ----------
def route_page(ck, c, r):
    frm, to, km = c["name"], r["to"], r["km"]
    x = ROUTE_EXTRA[(ck, r["key"])]
    slug = f"packers-and-movers-{ck}-to-{r['key']}"
    b = band_of(km)
    faqs = [(f"How much do packers and movers charge from {frm} to {to}?",
             f"For about {inr(km)} km, a 1 BHK costs {rng(HOUSE[1][1][b+1])}, a 2 BHK {rng(HOUSE[2][1][b+1])} and a 3 BHK {rng(HOUSE[3][1][b+1])}, plus 18 per cent GST. The written estimate after the survey is the final price.")] + r["faqs"]
    title = f"{frm} to {to} Packers and Movers | Rate Chart | 1st VRL"
    desc = f"{frm} to {to} packers and movers: house, car, bike and office shifting rate chart for {inr(km)} km. Free survey, written quote. Call {G.PHONE_TXT}."
    schemas = [service_schema(f"Packers and movers from {frm} to {to}", slug, [frm, to]), G.faq_schema(faqs + x["faqs"]),
               crumbs([("Home",""),(f"Packers and Movers {frm}", f"packers-and-movers-{ck}"),(f"{frm} to {to}", slug)])]
    out = head(title, desc, slug, schemas)
    out += G.hero(f'{e(frm)} to {e(to)} <span class="accent">Packers and Movers</span>',
                  f"Our {e(frm)} to {e(to)} packers and movers service handles house, car, bike and office moves. {r['intro']}", slug)
    house_rows = [[n, rng(rr[b+1])] for n, rr in HOUSE]
    car_rows = [[n, m, rng(rr[b])] for n, m, rr in CAR]
    bike_rows = [[n, m, rng(rr[b])] for n, m, rr in BIKE]
    off_rows = [[n, m, rng(rr[b+1])] for n, m, rr in OFFICE]
    out += f"""
<section class="section">
  <div class="container">
    <h2>{e(frm)} to {e(to)} at a glance</h2>
    <div class="route-facts">
      <div><strong>{inr(km)} km</strong><span>Road distance, approx.</span></div>
      <div><strong>{e(r['days'])}</strong><span>Household transit time</span></div>
      <div><strong>{e(r['road'])}</strong><span>Main route</span></div>
      <div><strong>{BANDS[b]}</strong><span>Price band used below</span></div>
    </div>
    <p>{r['about']}</p>
    <p>{x['journey']}</p>
  </div>
</section>

<section class="section section--tint">
  <div class="container">
    <h2>Check your {e(frm)} to {e(to)} price</h2>
    {calculator(slug, b, km, frm, to)}
  </div>
</section>

<section class="section rate-tabs" id="rates">
  <div class="container">
    <h2>{e(frm)} to {e(to)} shifting rate chart</h2>
    <p>{x['lead']}</p>
    <h3>1. House shifting charges</h3>
    {tbl(["Home size", f"{e(frm)} to {e(to)}"], house_rows)}
    <h3>2. Car transport charges</h3>
    {tbl(["Car type", "Models", "Price"], car_rows)}
    <h3>3. Bike transport charges</h3>
    {tbl(["Bike type", "Models", "Price"], bike_rows)}
    <h3>4. Office and corporate shifting charges</h3>
    {tbl(["Office size", "Workstations", "Price"], off_rows)}
    <p>Workstation dismantling and reinstallation Rs 800 - 2,000 per desk. Server rack Rs 3,000 - 8,000. Staff household moves for companies use the house chart, billed to the company.</p>
    {GST_NOTE}
  </div>
</section>

<section class="section section--tint">
  <div class="container">
    <h2>Moving into {e(to)}: what to plan for</h2>
    <p>{r['dest']}</p>
    <p>{x['areas']}</p>
    <p><strong>Our tip for this route:</strong> {r['tip']}</p>
  </div>
</section>
"""
    if r.get("photos"):
        out += more_sections(r.get("more"))
        out += route_keyword_section(ck, c, r, b)
    out += G.trust_section(None if c.get("team") == "own" else frm)
    out += G.PROCESS
    if r.get("photos"):
        if c.get("team") == "own":
            out += photo_block(r["photos"][2:], frm, "Our packing standard on this route", f"Real photos of the 1st VRL crew at work. In {e(frm)} our own Panchkula crew packs and loads; the team that unloads in {e(to)} works from the same item list and handling standard.", False)
        else:
            out += photo_block(r["photos"][2:], frm, "Our packing standard on this route", f"Real photos of the 1st VRL crew at work. Partner teams on the {e(frm)} to {e(to)} route follow the same packing standard, item list and branded tape.")
    others = [x for x in c["routes"] if x["key"] != r["key"]]
    links = "\n".join(f'      <a href="/packers-and-movers-{ck}-to-{x["key"]}">{e(frm)} to {e(x["to"])}</a>' for x in others)
    rev = CITY_DATA.get(r["key"])
    if rev and any(y["key"] == ck for y in rev["routes"]):
        links += f'\n      <a href="/packers-and-movers-{r["key"]}-to-{ck}">{e(rev["name"])} to {e(frm)} (return route)</a>'
    if r["key"] in CITY_DATA:
        links += f'\n      <a href="/packers-and-movers-{r["key"]}">Packers and Movers {e(CITY_DATA[r["key"]]["name"])}</a>' 
    out += f"""
<section class="section section--tint">
  <div class="container">
    <h2>More routes from {e(frm)}</h2>
    <div class="city-links">
      <a href="/packers-and-movers-{ck}">Packers and Movers {e(frm)}</a>
{links}
    </div>
  </div>
</section>
"""
    out += G.faq_block(faqs + x['faqs']).replace('section section--tint', 'section', 1)
    out += G.footer()
    return slug, out

# ---------- city page ----------
def city_page(ck, c):
    n = c["name"]; slug = f"packers-and-movers-{ck}"
    faqs = c["faqs"]
    title = f"Packers and Movers in {n} | Rates and Free Quote | 1st VRL"
    desc = f"Packers and movers in {n} for home, office, car and bike shifting. Local and intercity rate chart, free survey, written quote. Call {G.PHONE_TXT}."
    schemas = [service_schema(f"Packers and movers in {n}", slug, [n]), G.faq_schema(faqs), crumbs([("Home",""),(f"Packers and Movers {n}", slug)])]
    out = head(title, desc, slug, schemas)
    out += G.hero(f'Packers and Movers <span class="accent">in {e(n)}</span>', c["intro"], slug)
    areas = "".join(f"<li>{e(a)}</li>" for a in c["areas"])
    house = [[nm, rng(rr[0]), rng(rr[1]), rng(rr[2]), rng(rr[3])] for nm, rr in HOUSE]
    route_cards = "\n".join(
        f'      <div class="svc-card"><h3><a href="/packers-and-movers-{ck}-to-{r["key"]}">{e(n)} to {e(r["to"])}</a></h3><p>About {inr(r["km"])} km, {e(r["days"])}. 2 BHK {rng(HOUSE[2][1][band_of(r["km"])+1])} + GST.</p></div>'
        for r in c["routes"])
    out += f"""
<section class="section">
  <div class="container">
    <h2>Shifting in {e(n)}: what we plan for</h2>
    <p>{c['local']}</p>
    <p>{c['how']}</p>
    <h3 style="margin-top:22px">Areas we cover in {e(n)}</h3>
    <ul class="area-list">{areas}</ul>
  </div>
</section>

<section class="section section--tint" id="rates">
  <div class="container">
    <h2>{e(n)} packers and movers rate chart</h2>
    <p>House shifting price bands from {e(n)}: packing, labour, transport in a sized vehicle and up to one flight of stairs, or any floor with a working lift. Car, bike and office rates are on each route page below.</p>
    {tbl(["Home size","Local "+e(n),"Up to 500 km","500 to 1,500 km","1,500 km plus"], house)}
    {GST_NOTE}
  </div>
</section>

<section class="section">
  <div class="container">
    <h2>Popular routes from {e(n)}</h2>
    <p>Each route page has its own house, car, bike and office rate chart and a price calculator.</p>
    <div class="svc-grid">
{route_cards}
    </div>
  </div>
</section>
"""
    if c.get("photos"):
        out += more_sections(c.get("more"), True)
        out += city_keyword_section(ck, c)
    out += G.trust_section(None if c.get("team") == "own" else n)
    out += G.PROCESS
    if c.get("photos"):
        if c.get("team") == "own":
            out += photo_block(c["photos"][2:], n, f"Our crew at work: home shifting in {n}", f"Real photos of the 1st VRL crew at work. Moves in {e(n)} and the Tricity are packed and loaded by our own crew from the Panchkula office.", False)
        else:
            out += photo_block(c["photos"][2:], n, f"Our packing standard for home shifting in {n}", f"Real photos of the 1st VRL crew at work. Partner teams in {e(n)} follow the same packing standard, item list and branded tape.")
    out += G.faq_block(faqs)
    out += G.footer()
    return slug, out

if __name__ == "__main__":
    written = []
    for ck in sys.argv[2:]:
        c = CITY_DATA[ck]
        for slug, body in [city_page(ck, c)] + [route_page(ck, c, r) for r in c["routes"]]:
            (SITE / f"{slug}.html").write_text(body, encoding="utf-8"); written.append(slug)
    print("\n".join(written))
