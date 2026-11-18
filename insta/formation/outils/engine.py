import subprocess, os, sys, json
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
B = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
SE = '/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf'
SA = '/usr/share/fonts/truetype/dejavu/DejaVuSans-ExtraLight.ttf'
GOLD = (212, 175, 110, 255); WHITE = (255, 255, 255, 255); IV = (240, 232, 218, 255)
DIM = (160, 145, 115, 255); BG = (17, 17, 17, 255)
V = '/home/claude/vids'; P = '/home/claude/repo/insta/bulles'
TTS = '/home/claude/tts/fr_FR-tom-medium.onnx'
ENC = ['-r', '30', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p', '-an']
LOOKS = {
    'dark': ',eq=brightness=-0.2:saturation=0.6,gblur=sigma=5',
    'bw': ',eq=saturation=0:brightness=-0.1:contrast=1.1',
    'warm': ',eq=saturation=1.15:contrast=1.05:brightness=-0.06',
    'dim': ',eq=brightness=-0.25:contrast=1.1',
}


def run(a):
    subprocess.run(['ffmpeg', '-v', 'error', '-y'] + a, check=True)


def font(p, s):
    return ImageFont.truetype(p, s)


def text_overlay(path, lines, y0, gap=22):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    y = y0
    for ln in lines:
        t, sz = ln['t'], ln.get('size', 90)
        f = font(B, sz)
        while d.textlength(t, font=f) > W - 110 and sz > 40:
            sz -= 4; f = font(B, sz)
        words = t.split(' ')
        widths = [d.textlength(w + ' ', font=f) for w in words]
        x = (W - sum(widths) + d.textlength(' ', font=f)) / 2
        for w, wd in zip(words, widths):
            col = GOLD if w.strip('.,?!:').upper() in ln.get('hl', []) else WHITE
            d.text((x, y), w, font=f, fill=col, stroke_width=6, stroke_fill=(0, 0, 0, 255))
            x += wd
        y += sz + gap
    im.save(path)


def card_price(path):
    im = Image.new('RGBA', (W, H), BG); d = ImageDraw.Draw(im)
    d.text((W // 2, 560), 'FORMATION', font=font(SA, 64), fill=GOLD, anchor='mm')
    d.text((W // 2, 700), 'Photo · Vidéo · IA', font=font(SE, 110), fill=IV, anchor='mm')
    d.line((W // 2 - 90, 800, W // 2 + 90, 800), fill=GOLD, width=3)
    d.text((W // 2, 930), 'à partir de', font=font(SE, 70), fill=(200, 190, 170, 255), anchor='mm')
    d.text((W // 2, 1090), '300 €', font=font(B, 200), fill=GOLD, anchor='mm')
    d.text((W // 2, H - 170), 'LMOH PHOTOGRAPHY', font=font(SA, 36), fill=(140, 120, 90, 255), anchor='mm')
    im.save(path)


def card_cta(path):
    im = Image.new('RGBA', (W, H), BG); d = ImageDraw.Draw(im)
    d.text((W // 2, 700), 'Écris', font=font(SE, 110), fill=IV, anchor='mm')
    d.rounded_rectangle((150, 800, 930, 980), radius=90, outline=GOLD, width=6)
    d.text((W // 2, 890), 'FORMATION', font=font(B, 100), fill=GOLD, anchor='mm')
    d.text((W // 2, 1080), 'en message', font=font(SE, 90), fill=IV, anchor='mm')
    d.text((W // 2, 1240), 'je te réponds personnellement', font=font(SA, 36), fill=DIM, anchor='mm')
    d.text((W // 2, H - 170), 'LMOH PHOTOGRAPHY', font=font(SA, 36), fill=(140, 120, 90, 255), anchor='mm')
    im.save(path)


def card_big(path, top, big, sub=None):
    im = Image.new('RGBA', (W, H), BG); d = ImageDraw.Draw(im)
    if top: d.text((W // 2, 640), top, font=font(SA, 58), fill=GOLD, anchor='mm')
    y = 800
    for ln in big:
        sz = 120; f = font(SE, sz)
        while d.textlength(ln, font=f) > W - 140: sz -= 6; f = font(SE, sz)
        d.text((W // 2, y), ln, font=f, fill=IV, anchor='mm'); y += sz + 20
    d.line((W // 2 - 90, y + 10, W // 2 + 90, y + 10), fill=GOLD, width=3)
    if sub: d.text((W // 2, y + 100), sub, font=font(SA, 44), fill=GOLD, anchor='mm')
    d.text((W // 2, H - 170), 'LMOH PHOTOGRAPHY', font=font(SA, 36), fill=(140, 120, 90, 255), anchor='mm')
    im.save(path)


def card_step(path, title, nodes, active, step, desc):
    """Schéma d'automatisation : blocs reliés, le bloc actif en or."""
    im = Image.new('RGBA', (W, H), BG); d = ImageDraw.Draw(im)
    d.text((W // 2, 280), title, font=font(SA, 44), fill=DIM, anchor='mm')
    d.text((W // 2, 430), f'ÉTAPE {step}', font=font(B, 120), fill=GOLD, anchor='mm')
    n = len(nodes); r = 72; x0 = 250; y0 = 640; sp = 180
    for i in range(n - 1):
        col = GOLD if i < active else (70, 62, 48, 255)
        ya, yb = y0 + i * sp + r, y0 + (i + 1) * sp - r
        d.line((x0, ya, x0, yb), fill=col, width=8)
        d.polygon([(x0, yb + 2), (x0 - 16, yb - 24), (x0 + 16, yb - 24)], fill=col)
    for i, lab in enumerate(nodes):
        on = i <= active; y = y0 + i * sp
        d.ellipse((x0 - r, y - r, x0 + r, y + r), fill=(35, 32, 26, 255) if on else (24, 24, 24, 255),
                  outline=GOLD if on else (70, 62, 48, 255), width=7 if i == active else 3)
        d.text((x0, y), str(i + 1), font=font(B, 64), fill=GOLD if on else (90, 82, 66, 255), anchor='mm')
        d.text((x0 + r + 50, y), lab, font=font(B, 62 if i == active else 52),
               fill=GOLD if i == active else (IV if on else (110, 100, 85, 255)), anchor='lm')
    y = y0 + n * sp + 60
    for ln in desc:
        sz = 66; f = font(SE, sz)
        while d.textlength(ln, font=f) > W - 140: sz -= 4; f = font(SE, sz)
        d.text((W // 2, y), ln, font=f, fill=IV, anchor='mm'); y += sz + 18
    d.text((W // 2, H - 230), 'sans écrire une ligne de code', font=font(SA, 40), fill=DIM, anchor='mm')
    d.text((W // 2, H - 170), 'LMOH PHOTOGRAPHY', font=font(SA, 36), fill=(140, 120, 90, 255), anchor='mm')
    im.save(path)


def tts(text, out):
    p = subprocess.run(['python3', '-m', 'piper', '-m', TTS, '--length-scale', '0.92', '-f', out],
                       input=text.encode(), capture_output=True)
    if p.returncode: raise SystemExit(p.stderr.decode())
    return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', out])) + 0.25


FIT = "scale=1134:2016:force_original_aspect_ratio=increase,crop=1134:2016,crop=1080:1920:x='{dx}*t/{d}':y='{dy}*t/{d}'"


def scene(D, i, sc, d):
    out = f'{D}/sc{i}.mp4'; tmp = out + '.tmp.mp4'; ov = f'{D}/o{i}.png'
    bg = sc['bg']
    if bg[0] in ('vid', 'img'):
        text_overlay(ov, sc['text'], sc.get('y', 1250))
        src, ss, look = bg[1], bg[2] if bg[0] == 'vid' else 0, LOOKS.get(bg[-1], '')
        dx, dy = (27, 48) if i % 2 else (0, 0)
        if i % 2 == 0: FITx = FIT.replace("x='{dx}*t/{d}'", "x='27-27*t/{d}'").replace("y='{dy}*t/{d}'", "y='48-48*t/{d}'")
        else: FITx = FIT
        vf = f"[0:v]{FITx.format(dx=dx, dy=dy, d=d)},fps=30{look}[b];[b][1:v]overlay=0:0,format=yuv420p,trim=duration={d},fade=in:st=0:d=0.12"
        inp = ['-ss', str(ss), '-i', src] if bg[0] == 'vid' else ['-loop', '1', '-framerate', '30', '-i', src]
        run(inp + ['-loop', '1', '-framerate', '30', '-i', ov, '-filter_complex', vf, '-t', str(d)] + ENC + [tmp])
    else:
        kind = bg[0]
        if kind == 'price': card_price(ov)
        elif kind == 'cta': card_cta(ov)
        elif kind == 'big': card_big(ov, *bg[1:])
        elif kind == 'step': card_step(ov, *bg[1:])
        vf = (f"[0:v]scale=1080:1920,format=yuv420p,zoompan=z='1+0.0012*on':x='iw/2-(iw/zoom/2)':"
              f"y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30,trim=duration={d},fade=in:st=0:d=0.12")
        run(['-loop', '1', '-framerate', '30', '-i', ov, '-filter_complex', vf, '-t', str(d)] + ENC + [tmp])
    os.rename(tmp, out)


def build(name, scenes):
    D = f'/home/claude/out/{name}'; os.makedirs(D, exist_ok=True)
    durs = []
    for i, sc in enumerate(scenes, 1):
        d = tts(sc['say'], f'{D}/a{i}.wav'); durs.append(d)
        scene(D, i, sc, d)
    with open(f'{D}/list.txt', 'w') as f:
        for i in range(1, len(scenes) + 1): f.write(f"file 'sc{i}.mp4'\n")
    run(['-f', 'concat', '-safe', '0', '-i', f'{D}/list.txt', '-c', 'copy', f'{D}/video.mp4'])
    n = len(scenes)
    ins = []; filt = ''
    for i in range(1, n + 1):
        ins += ['-i', f'{D}/a{i}.wav']; filt += f'[{i-1}:a]aresample=44100,apad=pad_dur=0.25[a{i}];'
    filt += ''.join(f'[a{i}]' for i in range(1, n + 1)) + f'concat=n={n}:v=0:a=1,highpass=f=80,equalizer=f=180:t=q:w=1:g=3,acompressor=threshold=-18dB:ratio=3:attack=5:release=80,loudnorm=I=-15:TP=-1.5[v]'
    run(ins + ['-filter_complex', filt, '-map', '[v]', '-ac', '2', f'{D}/voice.wav'])
    T = sum(durs)
    pad = ("aevalsrc='0.10*sin(2*PI*55*t)*(0.6+0.4*sin(2*PI*0.5*t))+0.06*sin(2*PI*110*t)"
           "+0.035*sin(2*PI*164.8*t)+0.025*sin(2*PI*220*t)*(0.5+0.5*sin(2*PI*2*t))'" + f":s=44100:d={T}")
    run(['-f', 'lavfi', '-i', pad, '-af', f'lowpass=f=1200,afade=in:d=1,afade=out:st={T-1.5}:d=1.5', '-ac', '2', f'{D}/pad.wav'])
    run(['-i', f'{D}/voice.wav', '-i', f'{D}/pad.wav', '-filter_complex',
         '[1:a]volume=0.35[p];[0:a][p]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[a]', '-map', '[a]', f'{D}/mix.wav'])
    run(['-i', f'{D}/video.mp4', '-i', f'{D}/mix.wav', '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-preset', 'slow',
         '-crf', '27', '-maxrate', '1000k', '-bufsize', '2000k', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '128k',
         '-movflags', '+faststart', '-shortest', f'/home/claude/out/{name}.tmp.mp4'])
    os.rename(f'/home/claude/out/{name}.tmp.mp4', f'/home/claude/out/{name}.mp4')
    # planche de contrôle
    t = 0; thumbs = []
    for i, d in enumerate(durs, 1):
        fr = f'{D}/th{i}.jpg'
        run(['-ss', str(t + min(1.0, d / 2)), '-i', f'/home/claude/out/{name}.mp4', '-frames:v', '1', '-vf', 'scale=216:384', fr])
        thumbs.append(fr); t += d
    ims = [Image.open(x) for x in thumbs]
    s = Image.new('RGB', (216 * len(ims), 384))
    for k, x in enumerate(ims): s.paste(x, (k * 216, 0))
    s.save(f'/home/claude/out/{name}_check.jpg')
    print(name, round(T, 1), 's', os.path.getsize(f'/home/claude/out/{name}.mp4') // 1000, 'KB')


def split_voice(wav, lines):
    """Coupe la voix aux pauses qui correspondent aux fins de lignes (alignement sur la longueur du texte)."""
    import re
    T = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', wav]))
    log = subprocess.run(['ffmpeg', '-i', wav, '-af', 'silencedetect=noise=-35dB:d=0.18', '-f', 'null', '-'], capture_output=True, text=True).stderr
    st = [float(x) for x in re.findall(r'silence_start: ([0-9.]+)', log)]
    en = [float(x) for x in re.findall(r'silence_end: ([0-9.]+)', log)]
    sil = [((a + b) / 2, b - a) for a, b in zip(st, en) if a > 0.3 and b < T - 0.2]
    n = len(lines)
    lens = [len(l) for l in lines]; tot = sum(lens)
    exp = []; c = 0
    for l in lens[:-1]:
        c += l; exp.append(T * c / tot)
    # DP : choisir n-1 pauses croissantes, proches des positions attendues, en préférant les longues
    import math
    m = len(sil); INF = 1e18
    best = [[INF] * m for _ in range(n - 1)]; prev = [[-1] * m for _ in range(n - 1)]
    for j in range(m):
        best[0][j] = ((sil[j][0] - exp[0]) / T) ** 2 * 40 - sil[j][1]
    for k in range(1, n - 1):
        for j in range(m):
            cost = ((sil[j][0] - exp[k]) / T) ** 2 * 40 - sil[j][1]
            for i in range(j):
                if best[k - 1][i] + cost < best[k][j]:
                    best[k][j] = best[k - 1][i] + cost; prev[k][j] = i
    j = min(range(m), key=lambda x: best[n - 2][x])
    cuts = []
    for k in range(n - 2, -1, -1):
        cuts.append(sil[j][0]); j = prev[k][j]
    cuts = cuts[::-1]
    bounds = [0] + cuts + [T + 0.4]
    return [bounds[i + 1] - bounds[i] for i in range(n)], T


def build_voice(name, scenes, wav):
    D = f'/home/claude/out/{name}'; os.makedirs(D, exist_ok=True)
    durs, T = split_voice(wav, [s['say'] for s in scenes])
    for i, (sc, d) in enumerate(zip(scenes, durs), 1):
        scene(D, i, sc, d)
    with open(f'{D}/list.txt', 'w') as f:
        for i in range(1, len(scenes) + 1): f.write(f"file 'sc{i}.mp4'\n")
    run(['-f', 'concat', '-safe', '0', '-i', f'{D}/list.txt', '-c', 'copy', f'{D}/video.mp4'])
    TT = sum(durs)
    run(['-i', wav, '-af', f'aresample=44100,highpass=f=70,acompressor=threshold=-20dB:ratio=2.5:attack=5:release=100,loudnorm=I=-15:TP=-1.5,apad=whole_dur={TT}', '-ac', '2', f'{D}/voice.wav'])
    pad = ("aevalsrc='0.10*sin(2*PI*55*t)*(0.6+0.4*sin(2*PI*0.5*t))+0.06*sin(2*PI*110*t)"
           "+0.035*sin(2*PI*164.8*t)+0.025*sin(2*PI*220*t)*(0.5+0.5*sin(2*PI*2*t))'" + f":s=44100:d={TT}")
    run(['-f', 'lavfi', '-i', pad, '-af', f'lowpass=f=1200,afade=in:d=1,afade=out:st={TT-1.5}:d=1.5', '-ac', '2', f'{D}/pad.wav'])
    run(['-i', f'{D}/voice.wav', '-i', f'{D}/pad.wav', '-filter_complex',
         '[1:a]volume=0.3[p];[0:a][p]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[a]', '-map', '[a]', f'{D}/mix.wav'])
    run(['-i', f'{D}/video.mp4', '-i', f'{D}/mix.wav', '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-preset', 'slow',
         '-crf', '27', '-maxrate', '1000k', '-bufsize', '2000k', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '128k',
         '-movflags', '+faststart', '-shortest', f'/home/claude/out/{name}.tmp.mp4'])
    os.rename(f'/home/claude/out/{name}.tmp.mp4', f'/home/claude/out/{name}.mp4')
    print(name, round(TT, 1), 's', [round(x, 2) for x in durs], os.path.getsize(f'/home/claude/out/{name}.mp4') // 1000, 'KB')


_WM = None
def split_voice_whisper(wav, lines):
    global _WM
    import numpy as np, difflib, unicodedata, re
    from faster_whisper import WhisperModel
    if _WM is None: _WM = WhisperModel("small", device="cpu", compute_type="int8")
    raw = subprocess.check_output(['ffmpeg', '-v', 'error', '-i', wav, '-f', 's16le', '-ac', '1', '-ar', '16000', '-'])
    audio = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
    T = len(audio) / 16000
    segs, _ = _WM.transcribe(audio, language='fr', word_timestamps=True)
    words = [w for s in segs for w in s.words]
    norm = lambda t: re.sub(r'[^a-z0-9]', '', unicodedata.normalize('NFKD', t.lower()).encode('ascii', 'ignore').decode())
    NUM = {'trois': '300', 'cents': '', 'un': '1', 'deux': '2', 'quatre': '4'}
    hw = [norm(w.word) for w in words]
    sw = []; owner = []
    for li, l in enumerate(lines):
        for w in re.split(r"[\s'’,.?!:]+", l):
            if norm(w): sw.append(norm(w)); owner.append(li)
    sm = difflib.SequenceMatcher(None, sw, hw, autojunk=False)
    m = {}
    for a, b, size in sm.get_matching_blocks():
        for k in range(size): m[a + k] = b + k
    ends = []
    for li in range(len(lines) - 1):
        idx = [m[i] for i in range(len(sw)) if owner[i] == li and i in m]
        ends.append(max(idx) if idx else None)
    cuts = []
    last = 0.0
    for li, e in enumerate(ends):
        if e is None or e + 1 >= len(words):
            cuts.append(None); continue
        c = (words[e].end + words[e + 1].start) / 2
        cuts.append(max(c, last + 0.8)); last = cuts[-1]
    # combler d'éventuels trous par interpolation
    for i, c in enumerate(cuts):
        if c is None:
            a = cuts[i - 1] if i else 0; b = next((x for x in cuts[i + 1:] if x), T)
            cuts[i] = (a + b) / 2
    gaps = [((words[i].end + words[i + 1].start) / 2) for i in range(len(words) - 1) if words[i + 1].start - words[i].end >= 0.35]
    snapped = []; last = 0.0
    for c in cuts:
        cand = [g for g in gaps if g > last + 0.6]
        g = min(cand, key=lambda x: abs(x - c)) if cand else c
        if abs(g - c) > 1.6: g = c
        snapped.append(g); last = g
    bounds = [0] + snapped + [T + 0.4]
    return [float(bounds[i + 1] - bounds[i]) for i in range(len(lines))], T

split_voice = split_voice_whisper
