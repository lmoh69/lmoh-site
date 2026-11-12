"""Rédaction automatique des articles du Journal avec GitHub Models (gratuit, sans clé : jeton GitHub Actions).
Lit journal/request.json (préparé par ai_request.py), écrit la version française puis l'adaptation anglaise,
vérifie la qualité, puis dépose l'article dans journal/incoming/ (publié ensuite par process_ai.py).
Usage : python tools/ai_write.py [--test]   (--test : écrit dans maquette/test-ia.json sans publier)"""
import datetime, json, os, re, sys, time, urllib.request, urllib.error

TEST = '--test' in sys.argv
TOKEN = os.environ.get('GITHUB_TOKEN', '')
URL = 'https://models.github.ai/inference/chat/completions'
MODELS = ['openai/gpt-4.1', 'openai/gpt-4o', 'openai/gpt-4.1-mini']
INTERDITS = ['dans un monde où', 'n’hésitez pas', "n'hésitez pas", 'plongez', 'découvrez', 'en conclusion', 'en somme',
             'il est important de noter', 'véritable', 'incontournable', 'sublimer', 'immortaliser', 'magique', 'inoubliable',
             'http', 'www.', '!']


def call(system, user, max_tokens=4000):
    last = ''
    for model in MODELS:
        body = json.dumps({'model': model, 'temperature': 0.8, 'max_tokens': max_tokens,
                           'response_format': {'type': 'json_object'},
                           'messages': [{'role': 'system', 'content': system}, {'role': 'user', 'content': user}]}).encode()
        for essai in range(2):
            req = urllib.request.Request(URL, data=body, headers={'Authorization': f'Bearer {TOKEN}', 'Content-Type': 'application/json',
                                                                  'Accept': 'application/json'})
            try:
                with urllib.request.urlopen(req, timeout=300) as r:
                    data = json.load(r)
                txt = data['choices'][0]['message']['content'].strip()
                txt = re.sub(r'^```(?:json)?\s*|\s*```$', '', txt)
                return json.loads(txt), model
            except urllib.error.HTTPError as e:
                last = f'{model} HTTP {e.code} {e.read()[:300]!r}'
                if e.code == 429:
                    time.sleep(65)
                    continue
                break
            except Exception as e:
                last = f'{model} {e}'
                time.sleep(5)
    raise RuntimeError('aucun modèle disponible : ' + last)


def mots(t):
    return len(re.findall(r'\w+', t))


def texte(a):
    return ' '.join([a.get('lead', '')] + [p for s in a.get('sections', []) for p in s.get('p', [])])


def controle(a, kw, lang, mini):
    pb = []
    for k in ['slug', 'title', 'description', 'h1', 'lead', 'cover', 'sections', 'faq', 'cta']:
        if not a.get(k):
            pb.append(f'champ manquant : {k}')
    if pb:
        return pb
    n = mots(texte(a))
    if n < mini:
        pb.append(f'texte trop court ({n} mots, minimum {mini}) : développe davantage chaque section')
    if len(a['sections']) < 6:
        pb.append('il faut au moins 6 sections')
    if len(a['faq']) < 4:
        pb.append('il faut 4 questions de FAQ')
    if not a['title'].rstrip().endswith('| LMOH'):
        pb.append('le title doit se terminer par « | LMOH »')
    if not 120 <= len(a['description']) <= 160:
        pb.append(f'la meta description doit faire 140 à 155 caractères (actuellement {len(a["description"])})')
    base = (a['h1'] + ' ' + a['lead'] + ' ' + a['title']).lower()
    manque = [w for w in re.findall(r"[a-zà-ÿ’']+", kw.lower()) if len(w) > 3 and w not in base]
    if manque:
        pb.append(f'mot-clé principal « {kw} » absent du title, du h1 ou du lead (mots manquants : {", ".join(manque)})')
    tout = json.dumps(a, ensure_ascii=False).lower()
    if lang == 'fr':
        bad = [w for w in INTERDITS if w in tout]
        if bad:
            pb.append('formules interdites présentes : ' + ', '.join(bad))
    elif 'http' in tout:
        pb.append('aucun lien externe autorisé')
    return pb


req = json.load(open('journal/request.json', encoding='utf-8'))
if 'contents' not in req:
    print('Aucun sujet en attente.')
    sys.exit(0)
system = req['systemInstruction']['parts'][0]['text']
user = req['contents'][0]['parts'][0]['text']
kw_fr = (re.search(r'Mot-clé principal \(FR\) : (.+)', user) or [None, ''])[1].strip()
kw_en = (re.search(r'Mot-clé principal \(EN\) : (.+)', user) or [None, ''])[1].strip()
fmt = system.split('FORMAT DE SORTIE')[0]
art_spec = ('FORMAT DE SORTIE : uniquement un objet JSON valide ARTICLE = {"slug": "...", "title": "...", "description": "...", '
            '"kicker": "...", "h1": "...", "lead": "...", "cover": "id-photo", "cover_alt": "...", "sections": [{"h2": "...", '
            '"p": ["paragraphe", "paragraphe", "paragraphe"], "img": "id-photo (facultatif)", "img_alt": "...", '
            '"video": "id-video (facultatif, à la place de img)"}], "faq": [{"q": "...", "a": "..."}], "cta": "..."}')

# 1. Version française
sys_fr = fmt + art_spec + ('\nÉcris la version FRANÇAISE uniquement : 1100 à 1400 mots, 7 à 9 sections de 2 à 3 paragraphes '
                           'développés, 4 à 5 questions de FAQ. Le title fait 55 à 65 caractères et se termine par « | LMOH ».')
fr, modele = call(sys_fr, user)
for tour in range(2):
    pb = controle(fr, kw_fr, 'fr', 950)
    if not pb:
        break
    fr, modele = call(sys_fr, user + '\n\nTA VERSION PRÉCÉDENTE A ÉTÉ REFUSÉE. Corrige ces points :\n- ' + '\n- '.join(pb)
                      + '\n\nVersion précédente :\n' + json.dumps(fr, ensure_ascii=False))
pb_fr = controle(fr, kw_fr, 'fr', 950)

# 2. Adaptation anglaise
sys_en = fmt + art_spec + ('\nWrite the ENGLISH adaptation only (not a literal translation), for international couples and companies '
                           f'planning a wedding or event in France. Main English keyword: « {kw_en} ». 850 to 1100 words, '
                           '6 to 9 sections, 4 FAQ questions. Keep exactly the same image and video ids as the French article. '
                           'The English slug is in English. The title is 55 to 65 characters and ends with « | LMOH ».')
en, _ = call(sys_en, 'Article français à adapter (JSON) :\n' + json.dumps(fr, ensure_ascii=False))
pb_en = controle(en, kw_en, 'en', 700)
if pb_en:
    en, _ = call(sys_en, 'Article français à adapter (JSON) :\n' + json.dumps(fr, ensure_ascii=False)
                 + '\n\nYOUR PREVIOUS VERSION WAS REJECTED. Fix:\n- ' + '\n- '.join(pb_en))
    pb_en = controle(en, kw_en, 'en', 700)

art = {'fr': fr, 'en': en}
rapport = {'modele': modele, 'mots_fr': mots(texte(fr)), 'mots_en': mots(texte(en)), 'problemes_fr': pb_fr, 'problemes_en': pb_en}
print(json.dumps(rapport, ensure_ascii=False))
if TEST:
    os.makedirs('maquette', exist_ok=True)
    json.dump({'rapport': rapport, 'article': art}, open('maquette/test-ia.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    sys.exit(0)
if pb_fr or pb_en:
    raise SystemExit('Article refusé par le contrôle qualité : ' + '; '.join(pb_fr + pb_en))
os.makedirs('journal/incoming', exist_ok=True)
nom = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
json.dump(art, open(f'journal/incoming/{nom}.json', 'w', encoding='utf-8'), ensure_ascii=False)
print('article prêt :', fr['h1'])
