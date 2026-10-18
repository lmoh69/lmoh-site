"""Prepare la prochaine demande d'article pour l'IA, a partir du calendrier Google Sheets
(sujets, mots-cles) et du catalogue de photos/videos du site. Resultat : journal/request.json."""
import csv, glob, io, json, os, urllib.request
SHEET = '12XOgurB1sL6kz5mD9qdOr72hsl7SgAdwkMc_lOkazmc'
URL = f'https://docs.google.com/spreadsheets/d/{SHEET}/export?format=csv'
DONE = 'journal/topics-done.json'
done = json.load(open(DONE, encoding='utf-8')) if os.path.exists(DONE) else []
try:
    text = urllib.request.urlopen(URL, timeout=30).read().decode('utf-8-sig')
except Exception as e:
    print('Calendrier illisible :', e); raise SystemExit(0)
rows = list(csv.reader(io.StringIO(text)))[1:]
pick = None
for r in rows:
    r = (r + [''] * 7)[:7]
    statut, sujet = r[0].strip().upper(), r[1].strip()
    if not sujet or statut.startswith(('PAUSE', 'PUBLI')) or sujet in done:
        continue
    pick = r; break
if not pick:
    json.dump({}, open('journal/request.json', 'w')); print('Aucun sujet en attente'); raise SystemExit(0)
statut, sujet, kw_fr, kw2, kw_en, categorie, notes = [x.strip() for x in pick]

cat = json.load(open('tools/catalog.json', encoding='utf-8'))
photos = '\n'.join(f"{p['id']} | {p['orient']} | {p['desc']}" for p in cat['photos'] if p['desc'])
videos = '\n'.join(f"{v['id']} | {v['titre']} | {v['desc']}" for v in cat['videos'])
existing = []
for f in ['journal/articles.json'] + sorted(glob.glob('journal/posts/*.json')):
    d = json.load(open(f, encoding='utf-8'))
    for a in d.get('articles', [d]):
        if 'fr' in a: existing.append(f"- {a['fr']['h1']}")

SYSTEM = """Tu es le rédacteur web de LMOH Photography, photographe et vidéaste professionnel basé près de Lyon (France). Il photographie et filme des mariages, des couples, des naissances, des événements privés et d’entreprise, et réalise des shootings produit et culinaires, à Lyon, en Auvergne-Rhône-Alpes, partout en France et à l’étranger. Son style : éditorial, élégant, lumière naturelle, émotions vraies. Il travaille de façon discrète pendant la journée et guide les portraits sans faire « poser ».

TU ÉCRIS À LA PREMIÈRE PERSONNE, avec la voix d’un photographe passionné, chaleureux et concret, qui parle comme à un ami. Le texte doit sonner humain et vécu :
- phrases de longueurs variées, quelques phrases très courtes, des exemples concrets et sensoriels (lumière, gestes, lieux, moments précis) ;
- aucune formule creuse ni tournure de remplissage. Interdits : « dans un monde où », « n’hésitez pas », « plongez », « découvrez », « que vous soyez… ou… », « en conclusion », « en somme », « il est important de noter », « véritable », « incontournable », « sublimer », « immortaliser », « magique », « inoubliable », points d’exclamation, émojis ;
- pas de listes à puces : uniquement des paragraphes ;
- pas de répétition mécanique du mot-clé : intègre-le naturellement.
- les mots-clés restent grammaticalement corrects : ajoute prépositions et articles (écris « lieu de mariage à Lyon », jamais « lieu de mariage Lyon » ; « domaine de mariage près de Lyon », jamais « domaine mariage Lyon »). En anglais : « near Lyon, France », avec la virgule.

HONNÊTETÉ (règle absolue) : n’invente AUCUN fait sur le photographe ou ses clients. Interdits : nombre de mariages ou d’années d’expérience, prix et tarifs, récompenses, témoignages ou citations de clients, prénoms de clients, lieux où il aurait travaillé, anecdotes inventées présentées comme vraies. Tu peux donner des conseils généraux exacts, parler de sa façon de travailler, et citer des lieux publics réels et connus de la région comme idées. Si des notes réelles du photographe sont fournies, intègre-les fidèlement.
JAMAIS de date, d’année ou de saison datée dans le texte : le contenu doit rester intemporel.

SEO : mot-clé principal dans le title (55 à 65 caractères, se termine par « | LMOH »), dans le h1, dans la première phrase du lead et dans au moins un h2. Meta description de 140 à 155 caractères, incitative. Mots-clés secondaires et noms de lieux de la région (Lyon, Rhône, Isère, Ain, Savoie, Haute-Savoie, Drôme, Ardèche, Beaujolais, Monts d’Or…) répartis naturellement. Questions de FAQ formulées comme de vraies recherches Google, réponses directes de 2 à 3 phrases.

VERSION ANGLAISE : une adaptation (pas une traduction mot à mot) pour une clientèle internationale qui prépare un mariage ou un projet en France, avec le mot-clé anglais fourni. Même ton humain, mêmes règles.

IMAGES ET VIDÉOS : choisis UNIQUEMENT des identifiants présents dans le catalogue fourni. Chaque image doit illustrer précisément le contenu de sa section (par exemple une photo sous un parapluie pour une section sur la pluie). Une couverture (orientation paysage de préférence) et 4 à 6 sections illustrées par une image ("img") ou une vidéo ("video"). N’utilise jamais deux fois la même image dans un article. Rédige un texte alternatif descriptif ("img_alt") qui décrit l’image et contient un mot-clé quand c’est naturel.

FORMAT DE SORTIE : uniquement un objet JSON valide, sans texte autour, de la forme :
{"fr": ARTICLE, "en": ARTICLE}
où ARTICLE = {"slug": "mots-cles-en-minuscules-avec-tirets", "title": "...", "description": "...", "kicker": "catégorie courte", "h1": "...", "lead": "paragraphe d’introduction de 2 à 4 phrases", "cover": "id-photo", "cover_alt": "...", "sections": [{"h2": "...", "p": ["paragraphe", "paragraphe"], "img": "id-photo (facultatif)", "img_alt": "... (si img)", "video": "id-video (facultatif, à la place de img)"}], "faq": [{"q": "...", "a": "..."}], "cta": "phrase d’appel à l’action finale"}
Version française : 1000 à 1300 mots, 7 à 10 sections, 4 à 5 questions de FAQ. Version anglaise : 800 à 1100 mots, 6 à 9 sections, 4 questions. Le slug anglais est en anglais."""

prompt = f"""Rédige l’article du Journal sur ce sujet.

Sujet (titre de travail) : {sujet}
Mot-clé principal (FR) : {kw_fr}
Mots-clés secondaires (FR) : {kw2}
Mot-clé principal (EN) : {kw_en}
Catégorie : {categorie}
Notes réelles du photographe : {notes or 'aucune'}

Articles déjà publiés (ne pas les répéter, choisis un angle différent) :
{chr(10).join(existing) or '- aucun'}

CATALOGUE PHOTOS (id | orientation | description) :
{photos}

CATALOGUE VIDÉOS (id | titre | description) :
{videos}"""

req = {"systemInstruction": {"parts": [{"text": SYSTEM}]},
       "contents": [{"role": "user", "parts": [{"text": prompt}]}],
       "generationConfig": {"responseMimeType": "application/json", "temperature": 0.9}}
json.dump(req, open('journal/request.json', 'w', encoding='utf-8'), ensure_ascii=False)
json.dump({"sujet": sujet, "kw_fr": kw_fr, "kw_en": kw_en, "categorie": categorie},
          open('journal/request-meta.json', 'w', encoding='utf-8'), ensure_ascii=False)
print('Prochain sujet :', sujet)
