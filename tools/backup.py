"""Sauvegarde complete du site en archives ZIP autonomes de 40 Mo maximum."""
import os, zipfile, datetime
LIMIT = 40 * 1024 * 1024
OUT = '/tmp/sauvegarde'
os.makedirs(OUT, exist_ok=True)
files = []
for root, dirs, names in os.walk('.'):
    dirs[:] = [d for d in dirs if d not in ('.git', 'tmp')]
    for n in names:
        p = os.path.join(root, n)[2:]
        files.append((p, os.path.getsize(p)))
code = [f for f in files if not f[0].startswith(('photos/', 'thumbs/', 'video/'))]
media = sorted([f for f in files if f not in code])
month = datetime.date.today().strftime('%Y-%m')
groups, cur, size = [code], [], 0
for f in media:
    if cur and size + f[1] > LIMIT:
        groups.append(cur); cur, size = [], 0
    cur.append(f); size += f[1]
if cur: groups.append(cur)
for i, g in enumerate(groups, 1):
    name = f'{OUT}/site-lmoh-{month}-{i:02d}' + ('-pages-et-reglages' if i == 1 else '') + '.zip'
    with zipfile.ZipFile(name, 'w', zipfile.ZIP_STORED if i > 1 else zipfile.ZIP_DEFLATED) as z:
        for p, _ in g:
            z.write(p)
    print(name, round(os.path.getsize(name) / 1048576, 1), 'Mo', len(g), 'fichiers')
