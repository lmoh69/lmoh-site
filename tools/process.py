"""Robot LMOH : recupere photos et videos depuis Google Drive (fichiers partages par lien),
les met au format web et regenere media.json pour le site."""
import glob, json, os, re, subprocess, unicodedata
from PIL import Image, ImageOps
import gdown

def slug(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode()
    s = re.sub(r'\.[A-Za-z0-9]+$', '', s)
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')[:60] or 'media'

def duration(p):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p],
                                capture_output=True, text=True).stdout.strip() or 10)

def poster(mp4):
    d = duration(mp4)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', f'{d*0.35:.1f}', '-i', mp4, '-frames:v', '1',
                    '-q:v', '3', mp4[:-4] + '.jpg'], check=True)

folders = json.load(open('tools/folders.json'))
os.makedirs('tmp', exist_ok=True)
log = []
# Anti-doublons : fichiers Drive deja importes + empreinte visuelle des photos deja en ligne
REG, HCACHE, MAXV = 'tools/imported.json', 'tools/hashes.json', 700 * 1024 * 1024
reg = set(json.load(open(REG))) if os.path.exists(REG) else set()
hashes = json.load(open(HCACHE)) if os.path.exists(HCACHE) else {}
def dhash(im):
    g = im.convert('L').resize((9, 8), Image.LANCZOS); px = list(g.getdata())
    return sum(1 << i for i in range(64) if px[(i // 8) * 9 + i % 8] > px[(i // 8) * 9 + i % 8 + 1])
_ready = []
def known_hashes():
    if not _ready:
        for f in glob.glob('thumbs/*/*.jpg'):
            if f not in hashes:
                try: hashes[f] = dhash(Image.open(f))
                except Exception: pass
        _ready.append(1)
    return hashes.values()
for jf in sorted(glob.glob('jobs/*.json')):
    try:
        job = json.load(open(jf))
    except Exception as e:
        log.append(f'ERR job {jf} {e}'); os.remove(jf); continue
    items = job if isinstance(job, list) else job.get('photos', []) + job.get('videos', [])
    for it in items:
        try:
            mime = it.get('mimeType', '')
            cat = it.get('cat') or folders.get((it.get('parents') or [''])[0])
            if not cat:
                log.append(f"SKIP dossier inconnu {it.get('name')}"); continue
            name = it.get('slug') or slug(it.get('name', it['id']))
            if it.get('id') in reg:
                continue
            if it.get('kind') == 'video' or mime.startswith('video/'):
                if int(it.get('size') or 0) > MAXV:
                    log.append(f"SKIP video trop lourde {it.get('name')}"); continue
                os.makedirs('video', exist_ok=True)
                out = f'video/{name}.mp4'
                if os.path.exists(out): continue
                src = gdown.download(id=it['id'], output='tmp/v', quiet=True)
                start, dur = str(it.get('start', 0)), str(it.get('duration', 60))
                subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', start, '-i', src, '-t', dur,
                    '-vf', 'scale=1280:-2:flags=lanczos,format=yuv420p', '-c:v', 'libx264', '-preset', 'slow',
                    '-crf', '28', '-c:a', 'aac', '-b:a', '96k', '-movflags', '+faststart', out], check=True)
                poster(out)
                subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', out, '-vf',
                    'fps=1/3,scale=320:-2,tile=5x4', '-frames:v', '1', f'video/{name}-planche.jpg'], check=True)
                os.remove(src)
                reg.add(it['id'])
                log.append(f'ok {out}')
            else:
                out = f'photos/{cat}/{name}.jpg'
                if os.path.exists(out): continue
                src = gdown.download(id=it['id'], output='tmp/p', quiet=True)
                im = ImageOps.exif_transpose(Image.open(src)).convert('RGB')
                h = dhash(im)
                if any(bin(h ^ v).count('1') <= 5 for v in known_hashes()):
                    os.remove(src); reg.add(it['id'])
                    log.append(f"SKIP deja sur le site {it.get('name')}"); continue
                im.thumbnail((2000, 2000), Image.LANCZOS)
                os.makedirs(f'photos/{cat}', exist_ok=True)
                im.save(out, 'JPEG', quality=82, optimize=True, progressive=True)
                os.remove(src)
                hashes['thumbs/' + out[len('photos/'):]] = h
                reg.add(it['id'])
                log.append(f'ok {out}')
        except Exception as e:
            log.append(f"ERR {it.get('name', it.get('id'))} {e}")
    os.remove(jf)
json.dump(sorted(reg), open(REG, 'w'))
json.dump(hashes, open(HCACHE, 'w'))

if not os.path.exists('video/.posters-v2'):
    for f in glob.glob('video/*.mp4'):
        poster(f)
    if os.path.isdir('video'):
        open('video/.posters-v2', 'w').write('ok')

# Miniatures legeres (900 px) pour les galeries et le bandeau
for f in glob.glob('photos/*/*.jpg'):
    t = 'thumbs/' + f[len('photos/'):]
    if os.path.exists(t): continue
    os.makedirs(os.path.dirname(t), exist_ok=True)
    im = Image.open(f); im.thumbnail((900, 900), Image.LANCZOS)
    im.save(t, 'JPEG', quality=78, optimize=True, progressive=True)

# Extraits d'ouverture : 20 s, 960 px, avec le son (fondu d'entree et de sortie pour une boucle douce),
# image d'apercu = premiere image (transition sans saut)
os.makedirs('video/clip', exist_ok=True)
for f in glob.glob('video/*.mp4'):
    out = 'video/clip/' + os.path.basename(f)
    if os.path.exists(out): continue
    d = duration(f)
    if d < 8: continue
    st = d * 0.18; ln = min(20.0, d - st - 0.5)
    try:
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', f'{st:.1f}', '-i', f, '-t', f'{ln:.1f}',
            '-vf', 'scale=960:-2:flags=lanczos,format=yuv420p', '-c:v', 'libx264', '-preset', 'slow', '-crf', '30',
            '-g', '48', '-af', f'afade=t=in:d=0.8,afade=t=out:st={max(0.0, ln - 1.5):.1f}:d=1.5',
            '-c:a', 'aac', '-b:a', '96k', '-movflags', '+faststart', out], check=True)
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', out, '-frames:v', '1', '-q:v', '4', out[:-4] + '.jpg'], check=True)
    except Exception as e:
        log.append(f'ERR extrait {f} {e}')
        if os.path.exists(out): os.remove(out)

media = {'photos': {}, 'videos': []}
for f in sorted(glob.glob('photos/*/*.jpg')):
    w, h = Image.open(f).size
    media['photos'].setdefault(f.split('/')[1], []).append([f, w, h])
for f in sorted(glob.glob('video/*.mp4')):
    media['videos'].append([f, f[:-4] + '.jpg'])
media['hero'] = [[f, f[:-4] + '.jpg'] for f in sorted(glob.glob('video/clip/*.mp4'))]
json.dump(media, open('media.json', 'w'), ensure_ascii=False, separators=(',', ':'))
os.makedirs('jobs', exist_ok=True)
open('jobs/journal.txt', 'w').write('\n'.join(log) + '\n')
print('\n'.join(log))
