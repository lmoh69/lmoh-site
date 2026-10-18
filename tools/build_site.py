"""Genere les pages statiques indexables : Journal FR/EN, accueil anglais, sitemap, robots, llms.txt.
Contenu : journal/articles.json. Lance par le robot GitHub a chaque modification."""
import json, os, html
D = json.load(open('journal/articles.json', encoding='utf-8'))
B, BR = D['base'], D['brand']
E = lambda s: html.escape(s, quote=True)
MONO = '<svg width="0" height="0" style="position:absolute" aria-hidden="true"><symbol id="mono" viewBox="0 0 30 34"><path fill="none" stroke="currentColor" stroke-width="1.6" d="M0.8 0V34M4.4 0V34M0 33.2H21.5M4.4 0.8H19A9.35 9.35 0 0 1 19 19.5H4.4"/></symbol></svg>'
LOGO = '<svg viewBox="0 0 30 34" aria-hidden="true"><use href="#mono"/></svg><span class="word"><b>LMOH</b>PHOTOGRAPHY</span>'
FAV = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='-4 -2 38 38'%3E%3Cpath fill='none' stroke='black' stroke-width='2.4' d='M0.8 0V34M4.4 0V34M0 33.2H21.5M4.4 0.8H19A9.35 9.35 0 0 1 19 19.5H4.4'/%3E%3C/svg%3E"
ORG = {"@type": "ProfessionalService", "@id": B + "/#business", "name": BR, "url": B + "/",
       "image": B + "/photos/couple/p1020416.jpg", "telephone": D['phone'], "email": D['email'],
       "description": "Photographe et vidéaste professionnel : mariage, couple, événements privés et d’entreprise, shooting produit et culinaire.",
       "address": {"@type": "PostalAddress", "addressRegion": "Auvergne-Rhône-Alpes", "addressCountry": "FR"},
       "areaServed": ["Lyon", "Rhône", "Isère", "Ain", "Savoie", "Haute-Savoie", "Drôme", "Ardèche", "Auvergne-Rhône-Alpes", "France", "Europe"],
       "sameAs": [D['instagram']], "knowsLanguage": ["fr", "en"]}

def img(R, p, alt, cls='', eager=False):
    return (f'<img src="{R}photos/{p}.jpg" srcset="{R}thumbs/{p}.jpg 900w, {R}photos/{p}.jpg 2000w" '
            f'sizes="(max-width: 900px) 100vw, 900px" alt="{E(alt)}"' + ('' if eager else ' loading="lazy"') +
            f' decoding="async"{" class=" + chr(34) + cls + chr(34) if cls else ""}>')

def nav(lang, R, alt_url):
    if lang == 'fr':
        items = [('Portfolio', R + '#/mariage'), ('Films', R + '#/films'), ('Journal', R + 'journal/'),
                 ('Blog', R + '#/blog'), ('Contact', R + '#/contact')]
        sw = ('EN', alt_url, 'en', 'English version')
    else:
        items = [('Portfolio', R + '#/mariage'), ('Films', R + '#/films'), ('Journal', R + 'en/journal/'),
                 ('Contact', R + 'en/#contact')]
        sw = ('FR', alt_url, 'fr', 'Version française')
    li = ''.join(f'<li><a href="{u}">{t}</a></li>' for t, u in items)
    li += f'<li><a class="lang" href="{sw[1]}" hreflang="{sw[2]}" lang="{sw[2]}" title="{sw[3]}">{sw[0]}</a></li>'
    home = R if lang == 'fr' else R + 'en/'
    return (f'<header id="hdr"><div class="wrap bar"><a class="logo" href="{home}" aria-label="{BR}">{LOGO}</a>'
            f'<button class="burger" id="burger" aria-expanded="false" aria-controls="nav">Menu</button>'
            f'<nav class="main" id="nav" aria-label="Navigation"><ul>{li}</ul></nav></div></header>')

def footer(lang, R):
    if lang == 'fr':
        links = [('Portfolio', R + '#/mariage'), ('Journal', R + 'journal/'), ('Blog', R + '#/blog'), ('Contact', R + '#/contact'), ('English', R + 'en/')]
        tag = 'Photographe & vidéaste professionnel · Lyon, Rhône-Alpes, France et international'
    else:
        links = [('Portfolio', R + '#/mariage'), ('Journal', R + 'en/journal/'), ('Contact', R + 'en/#contact'), ('Français', R)]
        tag = 'Professional photographer & videographer · Lyon, south-east France and worldwide'
    a = ''.join(f'<a href="{u}">{t}</a>' for t, u in links) + f'<a href="{D["instagram"]}" rel="noopener" target="_blank">Instagram</a>'
    return (f'<footer><a class="logo" href="{R if lang == "fr" else R + "en/"}">{LOGO}</a><nav>{a}</nav>'
            f'<p class="ftag">{tag}</p><span>© {BR}</span></footer>')

SCRIPT = ("<script>(function(){var b=document.getElementById('burger'),n=document.getElementById('nav');"
          "b.addEventListener('click',function(){var o=n.classList.toggle('open');b.setAttribute('aria-expanded',o)});"
          "var h=document.getElementById('hdr');window.addEventListener('scroll',function(){h.classList.toggle('compact',scrollY>40)},{passive:true});"
          "})();</script>")

def page(lang, R, title, desc, path, alt_path, body, ld, ogimg, ogtype='website'):
    fr_url, en_url = (B + path, B + alt_path) if lang == 'fr' else (B + alt_path, B + path)
    head = (f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">'
            f'<title>{E(title)}</title><meta name="description" content="{E(desc)}">'
            '<meta name="robots" content="index, follow, max-image-preview:large">'
            f'<link rel="canonical" href="{B + path}">'
            f'<link rel="alternate" hreflang="fr" href="{fr_url}"><link rel="alternate" hreflang="en" href="{en_url}">'
            f'<link rel="alternate" hreflang="x-default" href="{fr_url}">'
            f'<meta property="og:type" content="{ogtype}"><meta property="og:site_name" content="{BR}">'
            f'<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}">'
            f'<meta property="og:url" content="{B + path}"><meta property="og:image" content="{ogimg}">'
            f'<meta property="og:locale" content="{"fr_FR" if lang == "fr" else "en_GB"}">'
            '<meta name="twitter:card" content="summary_large_image">'
            f'<link rel="icon" href="{FAV}">'
            '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            '<link href="https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,opsz,wght@0,6..96,400;1,6..96,400&family=Jost:wght@300;400;600&display=swap" rel="stylesheet">'
            f'<link rel="stylesheet" href="{R}style.css"><link rel="stylesheet" href="{R}journal.css">'
            f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script></head>')
    return head + f'<body class="static">{MONO}{nav(lang, R, R + alt_path.lstrip("/"))}<main>{body}</main>{footer(lang, R)}{SCRIPT}</body></html>'

def write(p, s):
    os.makedirs(os.path.dirname(p) or '.', exist_ok=True)
    open(p, 'w', encoding='utf-8').write(s)

L = {'fr': {'faq': 'Questions fréquentes', 'related': 'À lire aussi', 'contact': 'Parlons de votre projet', 'home': 'Accueil',
            'journal': 'Journal', 'read': 'Lire l’article', 'jt': 'Journal : conseils de photographe et vidéaste à Lyon | LMOH',
            'jd': 'Conseils et retours d’expérience d’un photographe et vidéaste professionnel à Lyon : mariage, événements, entreprise, shooting produit.',
            'jh': 'Journal', 'jl': 'Conseils, coulisses et retours d’expérience pour préparer votre mariage, votre événement ou votre shooting.'},
     'en': {'faq': 'Frequently asked questions', 'related': 'Read next', 'contact': 'Let’s talk about your project', 'home': 'Home',
            'journal': 'Journal', 'read': 'Read the article', 'jt': 'Journal: advice from a wedding and event photographer in Lyon, France | LMOH',
            'jd': 'Advice from a professional photographer and videographer in Lyon, France: weddings in France, events, corporate and product photography.',
            'jh': 'Journal', 'jl': 'Advice and behind-the-scenes stories to help you plan your wedding, event or shoot in France.'}}
bySlug = {}
for a in D['articles']:
    for lang in ('fr', 'en'):
        bySlug[a[lang]['slug']] = (a, lang)

urls = []
def jpath(lang, slug=None):
    base = '/journal/' if lang == 'fr' else '/en/journal/'
    return base + (slug + '/' if slug else '')

for a in D['articles']:
    for lang in ('fr', 'en'):
        x, other = a[lang], a['en' if lang == 'fr' else 'fr']
        t = L[lang]
        path, alt = jpath(lang, x['slug']), jpath('en' if lang == 'fr' else 'fr', other['slug'])
        R = '../../' if lang == 'fr' else '../../../'
        contact = R + ('#/contact' if lang == 'fr' else 'en/#contact')
        secs = ''
        for s in x['sections']:
            secs += f'<h2>{E(s["h2"])}</h2>' + ''.join(f'<p>{E(p)}</p>' for p in s['p'])
            if s.get('img'):
                secs += f'<figure class="jfig">{img(R, s["img"], s.get("img_alt", ""))}</figure>'
        faq = ''.join(f'<details><summary>{E(q["q"])}</summary><p>{E(q["a"])}</p></details>' for q in x['faq'])
        ra, rl = bySlug[x['related']]
        rx = ra[rl]
        body = (f'<article class="wrap jarticle top-space">'
                f'<nav class="crumbs" aria-label="Fil d’Ariane"><a href="{R if lang == "fr" else R + "en/"}">{t["home"]}</a> / <a href="{R + jpath(lang).lstrip("/")}">{t["journal"]}</a></nav>'
                f'<span class="kicker">{E(x["kicker"])}</span><h1>{E(x["h1"])}</h1><p class="lead">{E(x["lead"])}</p>'
                f'<figure class="jcover">{img(R, x["cover"], x["cover_alt"], eager=True)}</figure>'
                f'<div class="jbody">{secs}<h2>{t["faq"]}</h2><div class="faq">{faq}</div></div>'
                f'<div class="jcta"><p>{E(x["cta"])}</p><a class="btn" href="{contact}">{t["contact"]}</a></div>'
                f'<aside class="jrel"><span class="kicker">{t["related"]}</span>'
                f'<a href="{R + jpath(lang, rx["slug"]).lstrip("/")}"><div class="img">{img(R, rx["cover"], rx["cover_alt"])}</div><h3>{E(rx["h1"])}</h3></a></aside>'
                '</article>')
        ld = {"@context": "https://schema.org", "@graph": [
            {"@type": "BlogPosting", "headline": x['h1'], "description": x['description'], "inLanguage": lang,
             "image": f'{B}/photos/{x["cover"]}.jpg', "mainEntityOfPage": B + path,
             "datePublished": D['updated'], "dateModified": D['updated'],
             "author": {"@type": "Person", "name": "Lmoh", "url": B + "/"}, "publisher": {"@id": B + "/#business"}},
            {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q['q'], "acceptedAnswer": {"@type": "Answer", "text": q['a']}} for q in x['faq']]},
            {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": t['home'], "item": B + ('/' if lang == 'fr' else '/en/')},
                {"@type": "ListItem", "position": 2, "name": t['journal'], "item": B + jpath(lang)},
                {"@type": "ListItem", "position": 3, "name": x['h1'], "item": B + path}]},
            ORG]}
        write(path.lstrip('/') + 'index.html', page(lang, R, x['title'], x['description'], path, alt, body, ld, f'{B}/photos/{x["cover"]}.jpg', 'article'))
        urls.append((path, alt))

# Index du Journal
for lang in ('fr', 'en'):
    t, R = L[lang], ('../' if lang == 'fr' else '../../')
    cards = ''.join(
        f'<a class="jcard" href="{a[lang]["slug"]}/"><div class="img">{img(R, a[lang]["cover"], a[lang]["cover_alt"])}</div>'
        f'<span class="kicker">{E(a[lang]["kicker"])}</span><h2>{E(a[lang]["h1"])}</h2><p>{E(a[lang]["description"])}</p>'
        f'<span class="more">{t["read"]}</span></a>' for a in D['articles'])
    body = f'<section class="wrap top-space jindex"><div class="title"><h1>{t["jh"]}</h1><p>{t["jl"]}</p></div><div class="jgrid">{cards}</div></section>'
    path, alt = jpath(lang), jpath('en' if lang == 'fr' else 'fr')
    ld = {"@context": "https://schema.org", "@graph": [{"@type": "Blog", "name": f'{BR} – {t["jh"]}', "url": B + path, "inLanguage": lang, "publisher": {"@id": B + "/#business"}}, ORG]}
    write(path.lstrip('/') + 'index.html', page(lang, R, t['jt'], t['jd'], path, alt, body, ld, f'{B}/photos/couple/p1020416.jpg'))
    urls.append((path, alt))

# Accueil anglais
H, R = D['en_home'], '../'
cards = ''.join(f'<a class="ecard" href="{u}"><div class="img">{img(R, p, t)}</div><h3>{E(t)}</h3><p>{E(d)}</p></a>' for t, d, u, p in H['services'])
arts = ''.join(f'<a class="jcard" href="journal/{a["en"]["slug"]}/"><div class="img">{img(R, a["en"]["cover"], a["en"]["cover_alt"])}</div>'
               f'<span class="kicker">{E(a["en"]["kicker"])}</span><h2>{E(a["en"]["h1"])}</h2><span class="more">Read the article</span></a>' for a in D['articles'])
body = (f'<section class="ehero">{img(R, H["cover"], "Couple under a bandstand at sunset, wedding photography in France", eager=True)}'
        f'<div class="ehero-in"><svg viewBox="0 0 30 34" aria-hidden="true"><use href="#mono"/></svg><h1>{E(H["h1"])}</h1></div></section>'
        f'<section class="wrap eintro"><p class="big">{E(H["lead"])}</p><a class="btn line" href="#contact">Check my availability</a></section>'
        f'<section class="wrap"><div class="title"><span class="kicker">What I do</span><h2>Photography &amp; films</h2></div><div class="egrid">{cards}</div></section>'
        f'<section class="wrap ejournal"><div class="title"><span class="kicker">Journal</span><h2>Planning a wedding or an event in France</h2></div><div class="jgrid">{arts}</div></section>'
        f'<section class="wrap econtact" id="contact"><div class="title"><span class="kicker">Contact</span><h2>Tell me about your plans</h2>'
        f'<p>Share your date, venue and what you have in mind. I will get back to you quickly.</p></div>'
        f'<p class="ecoords"><a class="btn" href="mailto:{D["email"]}?subject=Wedding%20%2F%20event%20enquiry">{D["email"]}</a></p>'
        f'<p class="ecoords"><a href="tel:{D["phone"].replace(" ", "")}">{D["phone"]}</a> · <a href="{D["instagram"]}" target="_blank" rel="noopener">@lmohphotography</a></p></section>')
ld = {"@context": "https://schema.org", "@graph": [ORG, {"@type": "WebSite", "name": BR, "url": B + "/", "inLanguage": ["fr", "en"]}]}
write('en/index.html', page('en', R, H['title'], H['description'], '/en/', '/', body, ld, f'{B}/photos/{H["cover"]}.jpg'))
urls.append(('/en/', '/'))

# Sitemap, robots, llms.txt
sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
pairs = [('/', '/en/')] + [(p, a) for p, a in urls if not p.startswith('/en/')]
for fr, en in pairs:
    for loc in (fr, en):
        sm.append(f'<url><loc>{B + loc}</loc><lastmod>{D["updated"]}</lastmod>'
                  f'<xhtml:link rel="alternate" hreflang="fr" href="{B + fr}"/><xhtml:link rel="alternate" hreflang="en" href="{B + en}"/>'
                  f'<xhtml:link rel="alternate" hreflang="x-default" href="{B + fr}"/></url>')
sm.append('</urlset>')
write('sitemap.xml', '\n'.join(sm) + '\n')
write('robots.txt', 'User-agent: *\nAllow: /\nDisallow: /tools/\nDisallow: /jobs/\n\nUser-agent: GPTBot\nAllow: /\n\nUser-agent: ClaudeBot\nAllow: /\n\nUser-agent: PerplexityBot\nAllow: /\n\nUser-agent: Google-Extended\nAllow: /\n\n'
      f'Sitemap: {B}/sitemap.xml\n')
lt = [f'# {BR}', '', '> Photographe et vidéaste professionnel basé près de Lyon (France) : mariages, films de mariage, séances couple, portraits, événements privés et d’entreprise, shooting produit et culinaire. Intervient à Lyon, en Auvergne-Rhône-Alpes, partout en France et à l’étranger. Français et anglais.', '',
      f'- Contact : {D["email"]} · {D["phone"]} · Instagram {D["instagram"]}', '', '## Pages principales', '',
      f'- [Accueil et portfolio]({B}/)', f'- [English home]({B}/en/)', f'- [Journal (FR)]({B}/journal/)', f'- [Journal (EN)]({B}/en/journal/)', '', '## Articles', '']
for a in D['articles']:
    for lang in ('fr', 'en'):
        lt.append(f'- [{a[lang]["h1"]}]({B}{jpath(lang, a[lang]["slug"])}) : {a[lang]["description"]}')
write('llms.txt', '\n'.join(lt) + '\n')
print('pages generees :', len(urls))
