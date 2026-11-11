"""Pages de services optimisées pour Google (/photographe-mariage-lyon/, etc.), générées depuis tools/services.json.
Reprend l'en-tête, le pied de page et les scripts d'une page du Journal pour garder le même style."""
import html, json, os, re

B = 'https://lmohphotography.com'
E = lambda s: html.escape(str(s), quote=True)
pages = json.load(open('tools/services.json', encoding='utf-8'))
media = json.load(open('media.json', encoding='utf-8'))
DIMS = {p[0][len('photos/'):-4]: (p[1], p[2]) for c in media['photos'].values() for p in c}

# Gabarit : en-tête, pied de page et scripts d'une page du Journal (deux niveaux de profondeur -> un niveau)
src = open('journal/photographe-mariage-lyon/index.html', encoding='utf-8').read()
body_start = src.index('<body')
header = src[body_start:src.index('<main>')].replace('../../', '../')
header = re.sub(r'<li><a class="lang"[^<]*</a></li>', '<li><a class="lang" href="../en/" hreflang="en" lang="en" title="English">EN</a></li>', header)
footer = src[src.index('<footer'):src.index('</body>')].replace('../../', '../')

def img(i, alt, sizes='(max-width: 900px) 100vw, 900px'):
    return (f'<img src="../photos/{i}.jpg" srcset="../thumbs/{i}.jpg 900w, ../photos/{i}.jpg 2000w" sizes="{sizes}" '
            f'alt="{E(alt)}" loading="lazy" decoding="async">')

def film(v, label):
    return (f'<figure class="jfilm" data-src="../video/{v}.mp4"><img src="../video/{v}.jpg" alt="{E(label)}" loading="lazy" decoding="async">'
            f'<button type="button" class="jplay" aria-label="Voir le film"><span></span></button><figcaption>Voir le film</figcaption></figure>')

def related_card(r):
    slug = r.split('/')[-1]
    if r.startswith('journal/'):
        f = f'journal/posts/{slug}.json'
        if os.path.exists(f):
            a = json.load(open(f, encoding='utf-8'))['fr']
        else:
            arts = json.load(open('journal/articles.json', encoding='utf-8'))['articles']
            a = next((x['fr'] for x in arts if x['fr']['slug'] == slug), None)
        if not a:
            return ''
        return (f'<a href="../journal/{slug}/"><div class="img">{img(a["cover"], a.get("cover_alt", ""), "(max-width: 900px) 100vw, 300px")}</div>'
                f'<h3>{E(a["h1"])}</h3></a>')
    p = next((x for x in pages if x['slug'] == slug), None)
    if not p:
        return ''
    return (f'<a href="../{slug}/"><div class="img">{img(p["cover"], p["cover_alt"], "(max-width: 900px) 100vw, 300px")}</div>'
            f'<h3>{E(p["h1"])}</h3></a>')

CSS = ('<style>.sgal{display:grid;grid-template-columns:repeat(2,1fr);gap:10px;margin:2.4rem 0}'
       '@media (min-width:800px){.sgal{grid-template-columns:repeat(3,1fr)}}'
       '.sgal .jfig{margin:0;float:none;width:auto}.sgal img{width:100%;height:100%;aspect-ratio:4/5;object-fit:cover;cursor:zoom-in}'
       '.steps{counter-reset:s;list-style:none;padding:0;margin:1.2rem 0 0}.steps li{counter-increment:s;position:relative;padding:0 0 1.1rem 2.6rem}'
       '.steps li::before{content:counter(s);position:absolute;left:0;top:-.1rem;width:1.8rem;height:1.8rem;border:1px solid var(--ink);border-radius:50%;'
       'display:grid;place-items:center;font-size:.8rem}.sbtns{display:flex;gap:.8rem;flex-wrap:wrap;justify-content:center}'
       '.sbtns .btn.alt{background:transparent;color:var(--ink)}.slinks{display:flex;flex-wrap:wrap;gap:.4rem 1.4rem;justify-content:center;margin:2.4rem 0 0;font-size:.9rem}'
       '.slinks a{color:var(--muted)}</style>')

urls = []
for p in pages:
    url = f'{B}/{p["slug"]}/'
    urls.append(url)
    secs, side = '', 0
    for s in p['sections']:
        head = f'<h2>{E(s["h2"])}</h2>'
        paras = ''.join(f'<p>{E(x)}</p>' for x in s['p'])
        if s.get('img'):
            w, h = DIMS.get(s['img'], (3, 2))
            if h > w * 1.1:
                side ^= 1
                secs += f'<section class="jsec">{head}<figure class="jfig tall {"right" if side else "left"}">{img(s["img"], s.get("img_alt", ""))}</figure>{paras}</section>'
            else:
                secs += f'<section class="jsec">{head}{paras}<figure class="jfig wide">{img(s["img"], s.get("img_alt", ""))}</figure></section>'
        elif s.get('video'):
            secs += f'<section class="jsec">{head}{paras}{film(s["video"], s["h2"])}</section>'
        else:
            secs += f'<section class="jsec">{head}{paras}</section>'
    gal = ''
    if p.get('gallery'):
        gal = '<div class="sgal">' + ''.join(f'<figure class="jfig">{img(g, p.get("gallery_alt", ""), "(max-width: 800px) 50vw, 300px")}</figure>' for g in p['gallery']) + '</div>'
    steps = '<section class="jsec"><h2>Comment ça se passe</h2><ol class="steps">' + ''.join(f'<li>{E(x)}</li>' for x in p['steps']) + '</ol></section>'
    faq = '<section class="jsec"><h2>Questions fréquentes</h2><div class="faq">' + ''.join(
        f'<details><summary>{E(q["q"])}</summary><p>{E(q["a"])}</p></details>' for q in p['faq']) + '</div></section>'
    wa = 'https://wa.me/33651287900?text=' + html.escape('Bonjour Lmoh, j’ai une question : '.replace(' ', '%20'))
    cta = (f'<div class="jcta"><p>{E(p["cta"])}</p><div class="sbtns"><a class="btn" href="../#/contact">{E(p["button"])}</a>'
           f'<a class="btn alt" href="{wa}" target="_blank" rel="noopener">WhatsApp</a></div></div>')
    rel = ''.join(related_card(r) for r in p.get('related', []))
    rel = f'<aside class="jrel"><span class="kicker">À lire aussi</span>{rel}</aside>' if rel else ''
    others = '<nav class="slinks" aria-label="Prestations">' + ''.join(
        f'<a href="../{o["slug"]}/">{E(o["h1"])}</a>' for o in pages if o['slug'] != p['slug']) + '</nav>'
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "ProfessionalService", "@id": B + "/#business", "name": "LMOH Photography", "url": B + "/",
         "image": f'{B}/photos/{p["cover"]}.jpg', "telephone": "+33651287900", "email": "contact@lmohphotography.com",
         "areaServed": ["Lyon", "Rhône", "Isère", "Ain", "Savoie", "Haute-Savoie", "Drôme", "Auvergne-Rhône-Alpes", "France"],
         "sameAs": ["https://www.instagram.com/lmohphotography/"]},
        {"@type": "Service", "name": p["h1"], "serviceType": p["service"], "description": p["description"], "url": url,
         "provider": {"@id": B + "/#business"}, "areaServed": {"@type": "City", "name": "Lyon"}},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q["q"], "acceptedAnswer": {"@type": "Answer", "text": q["a"]}} for q in p["faq"]]},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Accueil", "item": B + "/"},
            {"@type": "ListItem", "position": 2, "name": p["h1"], "item": url}]}]}
    head = (f'<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">'
            f'<title>{E(p["title"])}</title><meta name="description" content="{E(p["description"])}">'
            f'<meta name="robots" content="index, follow, max-image-preview:large"><link rel="canonical" href="{url}">'
            f'<meta property="og:type" content="website"><meta property="og:site_name" content="LMOH Photography">'
            f'<meta property="og:title" content="{E(p["title"])}"><meta property="og:description" content="{E(p["description"])}">'
            f'<meta property="og:url" content="{url}"><meta property="og:image" content="{B}/photos/{p["cover"]}.jpg"><meta property="og:locale" content="fr_FR">'
            f'<meta name="twitter:card" content="summary_large_image">'
            f'<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            f'<link href="https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,opsz,wght@0,6..96,400;1,6..96,400&family=Jost:wght@300;400;600&display=swap" rel="stylesheet">'
            f'<link rel="stylesheet" href="../style.css"><link rel="stylesheet" href="../journal.css">{CSS}'
            f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script></head>')
    body = (f'{header}<main><article class="wrap jarticle top-space"><nav class="crumbs" aria-label="Fil d’Ariane"><a href="../">Accueil</a> / {E(p["kicker"])}</nav>'
            f'<span class="kicker">{E(p["kicker"])}</span><h1>{E(p["h1"])}</h1><p class="lead">{E(p["lead"])}</p>'
            f'<figure class="jcover">{img(p["cover"], p["cover_alt"])}</figure><div class="jbody">{secs}{gal}{steps}{faq}</div>{cta}{rel}{others}</article></main>')
    os.makedirs(p['slug'], exist_ok=True)
    open(f'{p["slug"]}/index.html', 'w', encoding='utf-8').write(head + body + footer + '</body></html>')

# Sitemap et llms.txt : ajoute les pages si elles n'y sont pas
if os.path.exists('sitemap.xml'):
    sm = open('sitemap.xml', encoding='utf-8').read()
    add = ''.join(f'<url><loc>{u}</loc><changefreq>monthly</changefreq><priority>0.9</priority></url>' for u in urls if u not in sm)
    if add:
        open('sitemap.xml', 'w', encoding='utf-8').write(sm.replace('</urlset>', add + '</urlset>'))
if os.path.exists('llms.txt'):
    ll = open('llms.txt', encoding='utf-8').read()
    add = ''.join(f'- [{p["h1"]}]({B}/{p["slug"]}/) : {p["description"]}\n' for p in pages if f'/{p["slug"]}/' not in ll)
    if add:
        open('llms.txt', 'w', encoding='utf-8').write(ll.rstrip('\n') + '\n\n## Prestations\n' + add)
print('pages de services :', len(pages))
