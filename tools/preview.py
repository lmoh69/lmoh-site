"""Planches d'apercu de videos du Drive (pour choisir les meilleurs plans). Jobs : jobs-preview/*.json = [{"id","slug"}]."""
import glob, json, os, subprocess
import gdown
os.makedirs('maquette/preview', exist_ok=True)
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
for jf in sorted(glob.glob('jobs-preview/*.json')):
    for it in json.load(open(jf)):
        src = '/tmp/preview-src'
        try:
            gdown.download(id=it['id'], output=src, quiet=True)
            d = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', src],
                                     capture_output=True, text=True).stdout.strip() or 1)
            n = int(it.get('n', 12)); fps = n / max(d, 1)
            txt = f",drawtext=fontfile={FONT}:text=%{{pts\\:hms}}:x=8:y=8:fontsize=22:fontcolor=white:box=1:boxcolor=black@0.5" if False else ''
            subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', src, '-vf',
                            f'fps={fps:.5f},scale=360:-2{txt},tile=4x3',
                            '-frames:v', '1', f"maquette/preview/{it['slug']}.jpg"], check=True)
            open('maquette/preview/infos.txt', 'a').write(f"{it['slug']} duree={d:.1f}s\n")
        except Exception as e:
            open('maquette/preview/erreurs.txt', 'a').write(f"{it.get('slug')} {e}\n")
        finally:
            if os.path.exists(src):
                os.remove(src)
    os.remove(jf)
