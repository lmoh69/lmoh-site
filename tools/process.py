"""Robot LMOH : recupere photos et videos depuis Google Drive (fichiers partages par lien),
les met au format web et regenere media.json pour le site."""
import glob, json, os, re, subprocess, unicodedata
from PIL import Image, ImageOps
import gdown

def slug(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode()
    s = re.sub(r'\.[A-Za-z0-9]+$', '', s)
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')[:60] or 'media'

def poster(mp4):
    d = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', mp4],
                             capture_output=True, text=True).stdout.strip() or 10)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', f'{d*0.35:.1f}', '-i', mp4, '-frames:v', '1',
                    '-q:v', '3', mp4[:-4] + '.jpg'], check=True)

folders = json.load(open('tools/folders.json'))
os.makedirs('tmp', exist_ok=True)
log = []
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
            if it.get('kind') == 'video' or mime.startswith('video/'):
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
                log.append(f'ok {out}')
            else:
                out = f'photos/{cat}/{name}.jpg'
                if os.path.exists(out): continue
                src = gdown.download(id=it['id'], output='tmp/p', quiet=True)
                im = ImageOps.exif_transpose(Image.open(src)).convert('RGB')
                im.thumbnail((2000, 2000), Image.LANCZOS)
                os.makedirs(f'photos/{cat}', exist_ok=True)
                im.save(out, 'JPEG', quality=82, optimize=True, progressive=True)
                os.remove(src)
                log.append(f'ok {out}')
        except Exception as e:
            log.append(f"ERR {it.get('name', it.get('id'))} {e}")
    os.remove(jf)

if not os.path.exists('video/.posters-v2'):
    for f in glob.glob('video/*.mp4'):
        poster(f)
    if os.path.isdir('video'):
        open('video/.posters-v2', 'w').write('ok')

media = {'photos': {}, 'videos': []}
for f in sorted(glob.glob('photos/*/*.jpg')):
    w, h = Image.open(f).size
    media['photos'].setdefault(f.split('/')[1], []).append([f, w, h])
for f in sorted(glob.glob('video/*.mp4')):
    media['videos'].append([f, f[:-4] + '.jpg'])
json.dump(media, open('media.json', 'w'), ensure_ascii=False, separators=(',', ':'))
os.makedirs('jobs', exist_ok=True)
open('jobs/journal.txt', 'w').write('\n'.join(log) + '\n')
print('\n'.join(log))
