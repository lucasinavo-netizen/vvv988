# -*- coding: utf-8 -*-
"""
vvv988 命理站 静态生成器
产出:
  index.html            首页(互动骰号 + 解梦入口 + 文章列表 + 导TG)
  number/00.html~99.html 100个数字详情页
  dream/xxx.html         40个解梦页
  guide/xxxx.html        命理文章页(可设数量)
  sitemap.xml            全站sitemap
  robots.txt
全部导流 TG(纯文字/连结),不放甲方博弈连结。

用法:
  python3 generate_site.py
  改下方 CONFIG 的 DOMAIN / GUIDE_COUNT / TG 设定
输出到 ./site/ 资料夹,直接部署(Vercel/Netlify/Cloudflare Pages)
"""

import os
import random
import shutil
import html
from datetime import datetime

import content_lucky as C
import materials_lucky as M

# ============ 设定 ============
CONFIG = {
    "DOMAIN": "https://vvv988.com",   # 你的域名(sitemap用)
    "SITE_NAME": "ကံကောင်းဂဏန်း",
    "SITE_TAG": "Lucky Numbers Myanmar · နေ့စဉ် ကံဇာတာ",
    "TG_NAME": "mmgoaltv",
    "TG_LINK": "https://t.me/mmgoaltv",   # 用可点连结(自己的站,导TG安全)
    "GUIDE_COUNT": 300,       # 生成几篇命理文章页(SEO衝量)
    "OUT": "site",
}

# ============ 共用样式 ============
CSS = """
:root{--ink:#1a1207;--gold:#c8a04a;--gold-bright:#e6c976;--maroon:#6e1f2a;--cream:#f4ecd8;--cream-deep:#e8dcc0;--jade:#2f6b52;--shadow:rgba(26,18,7,.18)}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Padauk','Myanmar Text','Noto Sans Myanmar',-apple-system,sans-serif;background:radial-gradient(circle at 20% 10%,rgba(200,160,74,.10),transparent 40%),radial-gradient(circle at 80% 90%,rgba(110,31,42,.08),transparent 45%),var(--cream);color:var(--ink);line-height:1.7;min-height:100vh}
.wrap{max-width:820px;margin:0 auto;padding:0 18px}
header{text-align:center;padding:26px 0 8px}
.brand{font-size:25px;font-weight:800;color:var(--maroon);display:inline-flex;align-items:center;gap:10px}
.brand a{color:inherit;text-decoration:none;display:inline-flex;align-items:center;gap:10px}
.mark{width:32px;height:32px;border-radius:50%;background:conic-gradient(from 0deg,var(--gold),var(--gold-bright),var(--maroon),var(--gold));box-shadow:0 2px 8px var(--shadow)}
.tag{font-size:13px;color:#7a6a4a;margin-top:4px}
nav.crumb{font-size:13px;margin:16px 0 4px}
nav.crumb a{color:var(--maroon);text-decoration:none;font-weight:700}
.hero{margin:20px 0;background:linear-gradient(160deg,#241a0c,#3a2a12);border:1px solid var(--gold);border-radius:22px;padding:30px 24px;text-align:center;color:var(--cream);box-shadow:0 12px 40px rgba(26,18,7,.35)}
.hero h1{font-size:20px;color:var(--gold-bright);margin-bottom:4px}
.hero .sub{font-size:13px;color:#c9bda0;margin-bottom:20px}
.dice-display{font-size:80px;font-weight:800;line-height:1;color:var(--cream);min-height:92px;display:flex;align-items:center;justify-content:center;text-shadow:0 4px 18px rgba(0,0,0,.4)}
.dice-display .ph{font-size:38px;color:#6a5a3a;font-weight:600}
.roll-btn{margin-top:18px;background:linear-gradient(180deg,var(--gold-bright),var(--gold));color:#241a0c;font-weight:800;font-size:17px;border:none;border-radius:14px;padding:14px 40px;cursor:pointer;box-shadow:0 6px 18px rgba(200,160,74,.4);transition:transform .12s}
.roll-btn:hover{transform:translateY(-2px)}
.roll-btn:disabled{opacity:.6}
.result-card{margin-top:20px;background:rgba(244,236,216,.08);border:1px solid rgba(230,201,118,.35);border-radius:14px;padding:16px;display:none}
.result-card.show{display:block}
.result-card .lbl{font-size:13px;color:var(--gold-bright);margin-bottom:6px}
.result-card .meaning{font-size:15px;color:var(--cream)}
.result-card .more{display:inline-block;margin-top:12px;background:var(--maroon);color:var(--cream);text-decoration:none;font-weight:700;font-size:14px;padding:9px 20px;border-radius:10px}
.result-card .tg{margin-top:12px;font-size:13px;color:#c9bda0;border-top:1px dashed rgba(230,201,118,.3);padding-top:10px}
.result-card .tg a{color:var(--gold-bright);font-weight:700}
.row2{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:18px 0}
@media(max-width:560px){.row2{grid-template-columns:1fr}}
.card-link{background:#fff;border:1px solid var(--cream-deep);border-radius:16px;padding:18px;text-decoration:none;color:var(--ink);display:block;transition:transform .12s;box-shadow:0 3px 12px var(--shadow)}
.card-link:hover{transform:translateY(-3px)}
.card-link .ic{font-size:28px}
.card-link h3{font-size:16px;color:var(--maroon);margin:6px 0 3px}
.card-link p{font-size:12px;color:#7a6a4a}
.section-title{font-size:18px;font-weight:800;color:var(--maroon);margin:26px 0 14px;display:flex;align-items:center;gap:10px}
.section-title::before{content:"";width:22px;height:3px;background:var(--gold);border-radius:2px}
.list{display:flex;flex-direction:column;gap:9px}
.item{background:#fff;border:1px solid var(--cream-deep);border-radius:12px;padding:13px 16px;text-decoration:none;color:var(--ink);display:flex;justify-content:space-between;align-items:center;gap:12px;transition:border-color .12s}
.item:hover{border-color:var(--gold)}
.item h4{font-size:15px;font-weight:600}
.item .arr{color:var(--gold);font-weight:800}
.numgrid{display:grid;grid-template-columns:repeat(10,1fr);gap:7px}
@media(max-width:560px){.numgrid{grid-template-columns:repeat(5,1fr)}}
.numgrid a{background:#fff;border:1px solid var(--cream-deep);border-radius:10px;padding:10px 0;text-align:center;font-weight:800;color:var(--maroon);text-decoration:none;font-size:15px;transition:all .12s}
.numgrid a:hover{background:var(--gold-bright);border-color:var(--gold)}
.detail-hero{background:linear-gradient(160deg,#241a0c,#3a2a12);border:1px solid var(--gold);border-radius:22px;padding:28px 24px;text-align:center;color:var(--cream);margin:10px 0 18px;box-shadow:0 12px 40px rgba(26,18,7,.35)}
.detail-hero .big{font-size:72px;font-weight:800;color:var(--gold-bright);line-height:1}
.detail-hero .cap{font-size:13px;color:#c9bda0;margin-top:6px}
.body-card{background:#fff;border:1px solid var(--cream-deep);border-radius:16px;padding:22px;box-shadow:0 3px 12px var(--shadow)}
.body-card h2{font-size:17px;color:var(--maroon);margin:18px 0 8px}
.body-card h2:first-child{margin-top:0}
.body-card p{font-size:15px;margin-bottom:10px}
.chip{display:inline-block;background:var(--cream);border:1px solid var(--gold);color:var(--maroon);font-weight:700;border-radius:20px;padding:5px 14px;font-size:14px;margin:4px 6px 4px 0}
.tg-cta{margin-top:20px;background:var(--jade);color:#fff;border-radius:14px;padding:18px;text-align:center}
.tg-cta p{margin-bottom:8px;font-size:15px}
.tg-cta a{font-size:18px;font-weight:800;letter-spacing:1px;background:rgba(255,255,255,.18);border-radius:10px;padding:8px 16px;display:inline-block;color:#fff;text-decoration:none}
.related{margin-top:20px}
.related h2{font-size:16px;color:var(--maroon);margin-bottom:10px}
.rel-nums{display:flex;flex-wrap:wrap;gap:8px}
.rel-nums a{background:#fff;border:1px solid var(--cream-deep);border-radius:10px;padding:8px 14px;text-decoration:none;color:var(--maroon);font-weight:700}
.rel-nums a:hover{border-color:var(--gold)}
footer{text-align:center;padding:28px 0;color:#8a7a5a;font-size:13px}
footer a{color:var(--maroon);font-weight:700;text-decoration:none}
"""

def esc(s):
    return html.escape(s, quote=True)

def page_head(title, desc, canonical, depth=0):
    """depth=0 根目录, depth=1 子目录(number/dream/guide)"""
    css_path = "styles.css" if depth == 0 else "../styles.css"
    home = "index.html" if depth == 0 else "../index.html"
    return f"""<!DOCTYPE html>
<html lang="my">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canonical}">
<link rel="stylesheet" href="{css_path}">
</head>
<body>
<div class="wrap">
<header><div class="brand"><a href="{home}"><span class="mark"></span>{CONFIG['SITE_NAME']}</a></div><div class="tag">{CONFIG['SITE_TAG']}</div></header>
"""

def page_foot(depth=0):
    home = "index.html" if depth == 0 else "../index.html"
    return f"""
<footer>နေ့စဉ် ကံကောင်းဂဏន်း · <a href="{CONFIG['TG_LINK']}">Telegram {CONFIG['TG_NAME']}</a> · <a href="{home}">ပင်မ</a></footer>
</div>
</body>
</html>"""

def tg_cta_block():
    return f"""<div class="tg-cta">
<p>🍀 နေ့စဉ် ကံကောင်းဂဏန်း၊ အိပ်မက်ဗေဒင်နှင့် ရာသီခွင်ကံဇာတာ အပြည့်အစုံ</p>
<a href="{CONFIG['TG_LINK']}">📢 Telegram: {CONFIG['TG_NAME']}</a>
</div>"""


# ============ 首页 ============
def gen_index():
    # 数字宫格
    numgrid = "".join(f'<a href="number/{i:02d}.html">{i:02d}</a>' for i in range(100))
    # 解梦入口(前8个)
    dream_items = "".join(
        f'<a class="item" href="dream/{d["slug"]}.html"><h4>🌙 {esc(d["name"])} အိပ်မက်</h4><span class="arr">→</span></a>'
        for d in C.DREAMS[:8]
    )
    # 文章列表(前10)
    guide_items = "".join(
        f'<a class="item" href="guide/{i:04d}.html"><h4>{esc(_guide_title(i))}</h4><span class="arr">→</span></a>'
        for i in range(min(10, CONFIG["GUIDE_COUNT"]))
    )

    body = f"""
<div class="hero">
<h1>🎲 ဒီနေ့ သင့်ရဲ့ ကံကောင်းဂဏန်း</h1>
<div class="sub">တစ်နေ့တာအတွက် သင့်အတွက်သီးသန့် နံပါတ်ကို ဖွင့်ကြည့်ပါ</div>
<div class="dice-display" id="dice"><span class="ph">? ?</span></div>
<button class="roll-btn" id="btn" onclick="roll()">ဂဏန်းဖွင့်မည်</button>
<div class="result-card" id="res">
<div class="lbl">သင့်ရဲ့ ယနေ့ ကံကောင်းဂဏန်း</div>
<div class="meaning" id="mean"></div>
<a class="more" id="more">အပြည့်အစုံ ကြည့်ရန် →</a>
<div class="tg">📢 နေ့စဉ်အတွက် <a href="{CONFIG['TG_LINK']}">Telegram: {CONFIG['TG_NAME']}</a></div>
</div>
</div>

<div class="row2">
<a class="card-link" href="dream/{C.DREAMS[0]['slug']}.html"><div class="ic">🌙</div><h3>အိပ်မက် အနက်ဖွင့်</h3><p>အိပ်မက်ကို ဂဏန်းအဖြစ် ပြောင်းကြည့်ပါ</p></a>
<a class="card-link" href="number/07.html"><div class="ic">🔢</div><h3>00-99 ဂဏန်း အနက်</h3><p>ဂဏန်းတစ်ခုစီရဲ့ အဓိပ္ပာယ်</p></a>
</div>

<div class="section-title">🔢 ကံကောင်းဂဏန်း 00-99</div>
<div class="numgrid">{numgrid}</div>

<div class="section-title">🌙 အိပ်မက် ဗေဒင်</div>
<div class="list">{dream_items}</div>

<div class="section-title">📖 ဗေဒင် လမ်းညွှန် ဗဟုသုတ</div>
<div class="list">{guide_items}</div>

{tg_cta_block()}
"""
    # 首页专属JS(骰号,当日固定)
    js = """
<script>
const M={"88":"\\u1004\\u103c\\u1031\\u1000\\u1036\\u1010\\u102d\\u102f\\u1038\\u101c\\u102c\\u1018\\u103a\\u1000\\u1036","07":"\\u1025\\u102c\\u100f\\u103a\\u1015\\u100a\\u102c"};
function pad(n){return n<10?"0"+n:""+n}
function today(){const d=new Date();const s=d.getFullYear()*10000+(d.getMonth()+1)*100+d.getDate();let x=Math.sin(s)*10000;return Math.floor((x-Math.floor(x))*100)}
let done=false;
function roll(){const disp=document.getElementById('dice'),btn=document.getElementById('btn'),res=document.getElementById('res');
if(done){res.classList.add('show');return}
btn.disabled=true;let t=0;const fin=today();
const sp=setInterval(()=>{disp.textContent=pad(Math.floor(Math.random()*100));if(++t>18){clearInterval(sp);disp.textContent=pad(fin);show(fin);btn.textContent='\\u1002\\u1002\\u1014\\u103a\\u1038 \\u1021\\u1014\\u1000\\u103a \\u1000\\u103c\\u100a\\u103a\\u1037\\u1019\\u100a\\u103a';btn.disabled=false;done=true}},70)}
function show(n){const k=pad(n);document.getElementById('mean').textContent="\\u101e\\u1004\\u103a\\u1037 \\u101a\\u1014\\u1031\\u1037 \\u1000\\u1036\\u1000\\u1031\\u102c\\u1004\\u103a\\u1038\\u1002\\u100f\\u1014\\u103a\\u1038\\u1019\\u103e\\u102c "+k+" \\u1016\\u103c\\u1005\\u103a\\u1015\\u102b\\u1010\\u101a\\u103a\\u104b";
document.getElementById('more').href="number/"+k+".html";document.getElementById('res').classList.add('show')}
</script>
"""
    canonical = CONFIG["DOMAIN"] + "/"
    title = f"{CONFIG['SITE_NAME']} | ဒီနေ့ ကံကောင်းဂဏန်း၊ အိပ်မက်ဗေဒင်၊ ရာသီခွင်"
    desc = "နေ့စဉ် ကံကောင်းဂဏန်း၊ 2D 3D အကြံပြုချက်၊ အိပ်မက်အနက်ဖွင့်နှင့် ရာသီခွင်ကံဇာတာ။ ဒီနေ့ သင့်ရဲ့ ကံကောင်းဂဏန်းကို ဖွင့်ကြည့်ပါ။"
    return page_head(title, desc, canonical, 0) + body + js + page_foot(0)


# ============ 数字详情页 ============
def gen_number(n):
    d = C.build_number_content(n)
    k = d["key"]
    chips = "".join(f'<span class="chip">{esc(t)}</span>' for t in d["tags"])
    # 相关数字
    rel = [(n+1)%100, (n+7)%100, (n+11)%100, (n+22)%100, (n+50)%100]
    rel_html = "".join(f'<a href="{r:02d}.html">ဂဏန်း {r:02d}</a>' for r in rel)
    canonical = f"{CONFIG['DOMAIN']}/number/{k}.html"
    title = f"ကံကောင်းဂဏန်း {k} အနက်ဖွင့် | {CONFIG['SITE_NAME']}"
    desc = f"ဂဏန်း {k} ၏ ကံဇာတာ အနက်၊ ယနေ့ ကံအခြေအနေနှင့် ဆက်စပ်ဂဏန်းများ။ {d['core'][:60]}"
    body = f"""
<nav class="crumb"><a href="../index.html">ပင်မ</a> › ဂဏန်း {k}</nav>
<div class="detail-hero"><div class="big">{k}</div><div class="cap">ကံကောင်းဂဏန်း အနက်ဖွင့်</div></div>
<div class="body-card">
<h2>ဂဏန်း၏ အဓိပ္ပာယ်</h2>
<p>{esc(d['core'])}</p>
<h2>ယနေ့ ကံဇာတာ</h2>
<p>{esc(d['fortune'])}</p>
<h2>ဆက်စပ် အဓိပ္ပာယ်</h2>
<div>{chips}</div>
{tg_cta_block()}
<div class="related"><h2>ဆက်စပ် ဂဏန်းများ</h2><div class="rel-nums">{rel_html}</div></div>
</div>
"""
    return page_head(title, desc, canonical, 1) + body + page_foot(1)


# ============ 解梦页 ============
def gen_dream(d):
    nums_html = "".join(f'<a href="../number/{x}.html">ဂဏန်း {x}</a>' for x in d["numbers"])
    canonical = f"{CONFIG['DOMAIN']}/dream/{d['slug']}.html"
    title = f"{esc(d['name'])} အိပ်မက် အနက်ဖွင့်နှင့် ကံကောင်းဂဏန်း | {CONFIG['SITE_NAME']}"
    desc = f"{d['name']} အိပ်မက်၏ အနက်: {d['meaning'][:70]}"
    body = f"""
<nav class="crumb"><a href="../index.html">ပင်မ</a> › အိပ်မက်ဗေဒင် › {esc(d['name'])}</nav>
<div class="detail-hero"><div class="big" style="font-size:40px">🌙 {esc(d['name'])}</div><div class="cap">အိပ်မက် အနက်ဖွင့်</div></div>
<div class="body-card">
<h2>အိပ်မက်၏ အနက်</h2>
<p>{esc(d['meaning'])}</p>
<h2>ဆက်စပ် ကံကောင်းဂဏန်းများ</h2>
<div class="rel-nums">{nums_html}</div>
{tg_cta_block()}
<div class="related"><h2>အခြား အိပ်မက်ဗေဒင်</h2><div class="list">{_other_dreams(d)}</div></div>
</div>
"""
    return page_head(title, desc, canonical, 1) + body + page_foot(1)

def _other_dreams(cur):
    others = [x for x in C.DREAMS if x["slug"] != cur["slug"]]
    pick = random.Random(cur["slug"]).sample(others, 5)
    return "".join(f'<a class="item" href="{o["slug"]}.html"><h4>🌙 {esc(o["name"])}</h4><span class="arr">→</span></a>' for o in pick)


# ============ 命理文章页 ============
def _fill(t):
    return (t.replace("{number}", random.choice(M.NUMBERS))
             .replace("{zodiac}", random.choice(M.ZODIACS))
             .replace("{day}", random.choice(M.DAYS))
             .replace("{year}", random.choice(M.YEARS)))

def _guide_title(i):
    rnd = random.Random(i*7+1)
    return _fill_seed(rnd, rnd.choice(M.TITLE_TEMPLATES))

def _fill_seed(rnd, t):
    return (t.replace("{number}", rnd.choice(M.NUMBERS))
             .replace("{zodiac}", rnd.choice(M.ZODIACS))
             .replace("{day}", rnd.choice(M.DAYS))
             .replace("{year}", rnd.choice(M.YEARS)))

def gen_guide(i):
    rnd = random.Random(i*7+1)
    title = _fill_seed(rnd, rnd.choice(M.TITLE_TEMPLATES))
    intro = _fill_seed(rnd, rnd.choice(M.INTRO))
    paras = [rnd.choice(M.LUCKY), rnd.choice(M.ANALYSIS), rnd.choice(M.ZODIAC)]
    rnd.shuffle(paras)
    paras = [_fill_seed(rnd, p) for p in paras]
    cta = _fill_seed(rnd, rnd.choice(M.CTA))
    # 相关文章内链
    rel_ids = [(i+1)%CONFIG["GUIDE_COUNT"], (i+5)%CONFIG["GUIDE_COUNT"], (i+13)%CONFIG["GUIDE_COUNT"]]
    rel = "".join(f'<a class="item" href="{r:04d}.html"><h4>{esc(_guide_title(r))}</h4><span class="arr">→</span></a>' for r in rel_ids)
    body_paras = f"<p>{esc(intro)}</p>" + "".join(f"<p>{esc(p)}</p>" for p in paras)
    canonical = f"{CONFIG['DOMAIN']}/guide/{i:04d}.html"
    desc = intro[:80]
    body = f"""
<nav class="crumb"><a href="../index.html">ပင်မ</a> › ဗေဒင်လမ်းညွှန်</nav>
<div class="body-card">
<h1 style="font-size:20px;color:var(--maroon);margin-bottom:14px">{esc(title)}</h1>
{body_paras}
<p>{esc(cta)}</p>
{tg_cta_block()}
<div class="related"><h2>ဆက်စပ် ဆောင်းပါးများ</h2><div class="list">{rel}</div></div>
</div>
"""
    return page_head(title, desc, canonical, 1) + body + page_foot(1)


# ============ sitemap ============
def gen_sitemap():
    now = datetime.now().strftime("%Y-%m-%d")
    urls = [CONFIG["DOMAIN"] + "/"]
    urls += [f"{CONFIG['DOMAIN']}/number/{i:02d}.html" for i in range(100)]
    urls += [f"{CONFIG['DOMAIN']}/dream/{d['slug']}.html" for d in C.DREAMS]
    urls += [f"{CONFIG['DOMAIN']}/guide/{i:04d}.html" for i in range(CONFIG["GUIDE_COUNT"])]
    items = "".join(f"<url><loc>{u}</loc><lastmod>{now}</lastmod></url>\n" for u in urls)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{items}</urlset>', len(urls)


# ============ 主流程 ============
def main():
    out = CONFIG["OUT"]
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(f"{out}/number")
    os.makedirs(f"{out}/dream")
    os.makedirs(f"{out}/guide")

    # CSS
    with open(f"{out}/styles.css", "w", encoding="utf-8") as f:
        f.write(CSS)

    # 首页
    with open(f"{out}/index.html", "w", encoding="utf-8") as f:
        f.write(gen_index())

    # 数字页
    for n in range(100):
        with open(f"{out}/number/{n:02d}.html", "w", encoding="utf-8") as f:
            f.write(gen_number(n))

    # 解梦页
    for d in C.DREAMS:
        with open(f"{out}/dream/{d['slug']}.html", "w", encoding="utf-8") as f:
            f.write(gen_dream(d))

    # 文章页
    for i in range(CONFIG["GUIDE_COUNT"]):
        with open(f"{out}/guide/{i:04d}.html", "w", encoding="utf-8") as f:
            f.write(gen_guide(i))

    # sitemap + robots
    sm, total = gen_sitemap()
    with open(f"{out}/sitemap.xml", "w", encoding="utf-8") as f:
        f.write(sm)
    with open(f"{out}/robots.txt", "w", encoding="utf-8") as f:
        f.write(f"User-agent: *\nAllow: /\nSitemap: {CONFIG['DOMAIN']}/sitemap.xml\n")

    print("=" * 50)
    print(" vvv988 命理站 生成完成")
    print("=" * 50)
    print(f"  首页: 1")
    print(f"  数字页: 100")
    print(f"  解梦页: {len(C.DREAMS)}")
    print(f"  文章页: {CONFIG['GUIDE_COUNT']}")
    print(f"  sitemap 总网址: {total}")
    print(f"  输出目录: ./{out}/")
    print(f"  导流: Telegram {CONFIG['TG_NAME']}(无甲方连结)")
    print("=" * 50)
    print(" 部署: 把 site/ 内容推到 vvv988 的 Vercel/Netlify")
    print(" GSC: 提交 sitemap.xml(一次),之后每次更新自动追踪")


if __name__ == "__main__":
    main()
