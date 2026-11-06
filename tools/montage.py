"""Montage automatique d'un film court (aftermovie) a partir de rushes du Drive.
Jobs : jobs-montage/*.json = {"out": "pro-xxx", "w": 1280, "h": 720, "fade": 0.6, "clips": [{"id", "ss", "t"}]}"""
import glob, json, os, subprocess
import gdown

def has_audio(p):
    r = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'a', '-show_entries', 'stream=index', '-of', 'csv=p=0', p],
                       capture_output=True, text=True)
    return bool(r.stdout.strip())

os.makedirs('video', exist_ok=True)
for jf in sorted(glob.glob('jobs-montage/*.json')):
    job = json.load(open(jf))
    if job.get('poster_only'):
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', str(job.get('at', 2)), '-i', f"video/{job['out']}.mp4",
                        '-frames:v', '1', '-q:v', '3', f"video/{job['out']}.jpg"], check=True)
        os.remove(jf)
        continue
    W, H, F = job.get('w', 1280), job.get('h', 720), float(job.get('fade', 0.6))
    files = {}
    for c in job['clips']:
        if c['id'] not in files:
            p = f"/tmp/rush{len(files)}.mp4"
            gdown.download(id=c['id'], output=p, quiet=True)
            files[c['id']] = p
    cmd = ['ffmpeg', '-y', '-loglevel', 'error']
    for c in job['clips']:
        cmd += ['-ss', str(c['ss']), '-t', str(c['t']), '-i', files[c['id']]]
    n = len(job['clips']); parts = []
    for i, c in enumerate(job['clips']):
        parts.append(f"[{i}:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps=25,format=yuv420p,setsar=1,settb=AVTB[v{i}]")
        if has_audio(files[c['id']]):
            parts.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,apad,atrim=0:{c['t']},asetpts=PTS-STARTPTS[a{i}]")
        else:
            parts.append(f"anullsrc=r=48000:cl=stereo,atrim=0:{c['t']},asetpts=PTS-STARTPTS[a{i}]")
    vl, al, off = 'v0', 'a0', 0.0
    for i in range(1, n):
        off += float(job['clips'][i - 1]['t']) - F
        parts.append(f"[{vl}][v{i}]xfade=transition=fade:duration={F}:offset={off:.3f}[x{i}]")
        parts.append(f"[{al}][a{i}]acrossfade=d={F}[y{i}]")
        vl, al = f'x{i}', f'y{i}'
    total = sum(float(c['t']) for c in job['clips']) - F * (n - 1)
    parts.append(f"[{vl}]fade=t=in:st=0:d=0.8,fade=t=out:st={total - 1.2:.2f}:d=1.2[vout]")
    m = job.get('music')
    if m:
        mp = '/tmp/music-src'
        gdown.download(id=m['id'], output=mp, quiet=True)
        files['__music__'] = mp
        cmd += ['-ss', str(m.get('ss', 0)), '-t', f'{total + 1:.2f}', '-i', mp]
        parts.append(f"[{al}]volume={job.get('volume', 0.25)}[amb]")
        parts.append(f"[{n}:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{total:.2f},asetpts=PTS-STARTPTS,volume={m.get('volume', 1.0)}[mus]")
        parts.append(f"[amb][mus]amix=inputs=2:duration=first:normalize=0,afade=t=in:st=0:d=0.6,afade=t=out:st={total - 1.8:.2f}:d=1.8,alimiter=limit=0.95[aout]")
    else:
        parts.append(f"[{al}]volume={job.get('volume', 0.8)},afade=t=in:st=0:d=0.8,afade=t=out:st={total - 1.2:.2f}:d=1.2[aout]")
    out = f"video/{job['out']}.mp4"
    cmd += ['-filter_complex', ';'.join(parts), '-map', '[vout]', '-map', '[aout]', '-c:v', 'libx264', '-preset', 'slow',
            '-crf', '23', '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', out]
    subprocess.run(cmd, check=True)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', str(job.get('poster', 2.5)), '-i', out, '-frames:v', '1',
                    '-q:v', '3', f"video/{job['out']}.jpg"], check=True)
    for p in files.values():
        os.remove(p)
    os.remove(jf)
