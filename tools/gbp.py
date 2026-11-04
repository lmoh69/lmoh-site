"""Fiche Google (lue par Make) : dernier article du Journal et rotation des photos du site."""
import datetime, glob, json, os
RAW = 'https://raw.githubusercontent.com/lmoh69/lmoh-site/main/'
B = 'https://lmohphotography.com'
TODAY = datetime.date.today().isoformat()
os.makedirs('gbp', exist_ok=True)

posts = [json.load(open(f, encoding='utf-8')) for f in glob.glob('journal/posts/*.json')]
posts = sorted((p for p in posts if p.get('publish', '0000-00-00') <= TODAY), key=lambda p: p.get('publish', ''), reverse=True)
if posts:
    a = posts[0]['fr']
    lead = a['lead'] if len(a['lead']) <= 1200 else a['lead'][:1200].rsplit(' ', 1)[0] + '…'
    json.dump({'titre': a['h1'], 'texte': a['h1'] + '\n\n' + lead + '\n\nLa suite dans le Journal, sur le site.',
               'url': B + '/journal/' + a['slug'] + '/', 'photo': RAW + 'photos/' + a['cover'] + '.jpg', 'slug': a['slug']},
              open('gbp/article.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    json.dump({'languageCode': 'fr', 'summary': a['h1'] + '\n\n' + lead + '\n\nLa suite dans le Journal, sur le site.', 'topicType': 'STANDARD',
               'callToAction': {'actionType': 'LEARN_MORE', 'url': B + '/journal/' + a['slug'] + '/'},
               'media': [{'mediaFormat': 'PHOTO', 'sourceUrl': RAW + 'photos/' + a['cover'] + '.jpg'}]},
              open('gbp/article-post.json', 'w', encoding='utf-8'), ensure_ascii=False)

TEXTES = {
    'mariage': ('Un regard, un geste, une lumière : je photographie et je filme les mariages à Lyon, en Rhône-Alpes et partout en France, avec discrétion et sans faire « poser ». Votre date est-elle encore libre ?', '#/mariage'),
    'pro': ('Séminaires, soirées d\'entreprise, salons, films de marque : je photographie et je filme vos événements professionnels à Lyon et partout en France.', '#/pro'),
    'couple': ('Une séance couple, c\'est une heure pour vous, sans pression, dans un lieu qui vous ressemble. Séances à Lyon et dans toute la région.', '#/couple'),
    'mariage2': ('Un mariage au bord du lac, entre bateau, palace et lumière du soir. Je photographie et je filme les mariages à Lyon, en Savoie, en Haute-Savoie et partout en France.', '#/mariage'),
    'nb': ('Le noir et blanc garde l\'essentiel : les regards, les gestes, l\'émotion. Des images intemporelles pour votre mariage ou votre séance.', '#/noir-et-blanc'),
    'soiree': ('La soirée, c\'est là que tout se lâche. Photo et vidéo de mariages, de soirées privées et de soirées d\'entreprise à Lyon.', '#/mariage'),
    'portrait': ('Portraits professionnels, photos d\'équipe, séances mode : des images qui vous ressemblent, pour votre site, LinkedIn ou vos réseaux.', '#/portrait'),
    'details': ('Les détails racontent aussi votre histoire : alliances, robe, décoration, fleurs. Je les photographie avec le même soin que les grands moments.', '#/mariage'),
    'culinaire': ('Photo culinaire pour restaurants, traiteurs et chefs à Lyon : des images qui donnent envie de réserver.', '#/culinaire'),
    'grossesse': ('Grossesse et naissance : des images douces et naturelles pour garder ces premiers instants.', '#/naissance'),
}
media = json.load(open('media.json', encoding='utf-8'))
pool = {c: sorted(p[0][len('photos/'):-4] for p in media['photos'].get(c, [])) for c in TEXTES}
rot = []
for i in range(max(len(v) for v in pool.values())):
    for c, (texte, page) in TEXTES.items():
        if i < len(pool[c]):
            rot.append({'photo': RAW + 'photos/' + pool[c][i] + '.jpg', 'cat': c, 'texte': texte, 'url': B + '/' + page})
json.dump({'photos': rot}, open('gbp/photos.json', 'w', encoding='utf-8'), ensure_ascii=False)
print('fiche Google :', len(rot), 'photos en rotation')
