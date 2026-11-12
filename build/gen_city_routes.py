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
    out += G.trust_section(frm)
    others = [x for x in c["routes"] if x["key"] != r["key"]]
    links = "\n".join(f'      <a href="/packers-and-movers-{ck}-to-{x["key"]}">{e(frm)} to {e(x["to"])}</a>' for x in others)
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
    out += G.trust_section(n)
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
