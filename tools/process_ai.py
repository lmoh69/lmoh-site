"""Integre les articles generes par l'IA (journal/incoming/*.json) : verification, photos, liens, publication."""
import datetime, glob, json, os, re, unicodedata
os.makedirs('journal/posts', exist_ok=True)
DONE = 'journal/topics-done.json'
done = json.load(open(DONE, encoding='utf-8')) if os.path.exists(DONE) else []
meta = json.load(open('journal/request-meta.json', encoding='utf-8')) if os.path.exists('journal/request-meta.json') else {}
today = datetime.date.today().isoformat()
log = []

def slugify(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')[:70] or 'article'

def all_articles():
    out = json.load(open('journal/articles.json', encoding='utf-8'))['articles']
    for f in sorted(glob.glob('journal/posts/*.json')):
        out.append(json.load(open(f, encoding='utf-8')))
    return out

REQ = ['title', 'description', 'kicker', 'h1', 'lead', 'cover', 'cover_alt', 'sections', 'faq', 'cta']
for f in sorted(glob.glob('journal/incoming/*.json')):
    try:
        raw = open(f, encoding='utf-8').read().strip()
        raw = re.sub(r'^```(?:json)?\s*|\s*```$', '', raw)
        art = json.loads(raw)
        existing = all_articles()
        slugs = {a[l]['slug'] for a in existing for l in ('fr', 'en')}
        for lang in ('fr', 'en'):
            x = art[lang]
            for k in REQ:
                if not x.get(k): raise ValueError(f'champ manquant {lang}.{k}')
            s = slugify(x.get('slug') or x['h1']); base, n = s, 2
            while s in slugs: s = f'{base}-{n}'; n += 1
            x['slug'] = s; slugs.add(s)
            if not os.path.exists(f'photos/{x["cover"]}.jpg'): x['cover'] = 'couple/p1020416'
            for sec in x['sections']:
                if sec.get('img') and not os.path.exists(f'photos/{sec["img"]}.jpg'): sec.pop('img', None)
                if sec.get('video') and not os.path.exists(f'video/{sec["video"]}.mp4'): sec.pop('video', None)
                sec['p'] = [p for p in sec.get('p', []) if p.strip()]
        prev = existing[-1] if len(existing) > 0 else None
        if prev:
            art['fr']['related'], art['en']['related'] = prev['fr']['slug'], prev['en']['slug']
        else:
            art['fr']['related'], art['en']['related'] = art['fr']['slug'], art['en']['slug']
        art['publish'] = today
        art['topic'] = meta.get('sujet', '')
        json.dump(art, open(f'journal/posts/{art["fr"]["slug"]}.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        if art['topic'] and art['topic'] not in done: done.append(art['topic'])
        log.append(f'publie : {art["fr"]["slug"]}')
    except Exception as e:
        log.append(f'ERREUR {f} : {e}')
    os.remove(f)
json.dump(done, open(DONE, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
if log:
    open('journal/journal-log.txt', 'a', encoding='utf-8').write(f'{today}\n' + '\n'.join(log) + '\n')
print('\n'.join(log) or 'Aucun nouvel article')
