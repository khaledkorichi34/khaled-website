"""Generate TechPulse AI brand assets and featured images (1200x630)."""
import json, math, random, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont

F = 'fonts/pjs/PlusJakartaSans-2.7.1/ttf/PlusJakartaSans-'
def font(w, s): return ImageFont.truetype(F + w + '.ttf', s)

CATS = {
    'ai-basics':      ('AI BASICS',        (59, 130, 246), (79, 70, 229)),
    'guides':         ('HOW-TO GUIDE',     (16, 185, 129), (20, 184, 166)),
    'safety-privacy': ('SAFETY & PRIVACY', (139, 92, 246), (217, 70, 239)),
}
BG = (15, 23, 42)
W, H = 1200, 630
SS = 2  # supersample


def lerp(a, b, t): return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def pulse_icon(d, x, y, s, color, width):
    """Pulse line ending in a node. (x,y) top-left, s size."""
    pts = [(0, .55), (.22, .55), (.34, .2), (.5, .9), (.62, .45), (.72, .55), (.8, .55)]
    P = [(x + px * s, y + py * s) for px, py in pts]
    d.line(P, fill=color, width=width, joint='curve')
    r = s * .11
    cx, cy = x + .88 * s, y + .55 * s
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)
    for p in (P[0],):
        d.ellipse([p[0] - width / 2, p[1] - width / 2, p[0] + width / 2, p[1] + width / 2], fill=color)


def wrap(text, f, maxw, d):
    words, lines, cur = text.split(), [], ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if d.textlength(t, font=f) <= maxw: cur = t
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines


def featured(title, cat, seed, out):
    label, c1, c2 = CATS[cat]
    w, h = W * SS, H * SS
    img = Image.new('RGB', (w, h), BG)

    # glow blobs (right side)
    glow = Image.new('RGB', (w, h), BG)
    g = ImageDraw.Draw(glow)
    g.ellipse([int(w * .55), int(-h * .35), int(w * 1.25), int(h * .75)], fill=c1)
    g.ellipse([int(w * .72), int(h * .35), int(w * 1.3), int(h * 1.3)], fill=c2)
    glow = glow.filter(ImageFilter.GaussianBlur(170 * SS))
    img = Image.blend(img, glow, .55)
    d = ImageDraw.Draw(img, 'RGBA')

    # dot grid on right half
    sp = 28 * SS
    for gx in range(int(w * .5), w, sp):
        for gy in range(0, h, sp):
            fade = (gx - w * .5) / (w * .5)
            d.ellipse([gx - 2 * SS, gy - 2 * SS, gx + 2 * SS, gy + 2 * SS], fill=(255, 255, 255, int(28 * fade + 6)))

    # neural network constellation (seeded per post)
    rnd = random.Random(seed)
    nodes = [(rnd.uniform(w * .66, w * .95), rnd.uniform(h * .12, h * .88)) for _ in range(11)]
    for i, a in enumerate(nodes):
        dists = sorted(((math.dist(a, b), j) for j, b in enumerate(nodes) if j != i))[:3]
        for _, j in dists:
            b = nodes[j]
            d.line([a, b], fill=(255, 255, 255, 70), width=2 * SS)
    for i, (nx, ny) in enumerate(nodes):
        r = rnd.choice([6, 8, 11]) * SS
        col = lerp(c1, c2, i / len(nodes))
        d.ellipse([nx - r * 2.2, ny - r * 2.2, nx + r * 2.2, ny + r * 2.2], fill=col + (60,))
        d.ellipse([nx - r, ny - r, nx + r, ny + r], fill=(255, 255, 255, 235))

    # brand mark top-left
    m = 56 * SS
    pulse_icon(d, m, m - 6 * SS, 46 * SS, (45, 212, 191), 5 * SS)
    bf = font('ExtraBold', 30 * SS)
    d.text((m + 56 * SS, m - 2 * SS), 'TechPulse', font=bf, fill=(255, 255, 255))
    tw = d.textlength('TechPulse ', font=bf)
    d.text((m + 56 * SS + tw, m - 2 * SS), 'AI', font=font('Regular', 30 * SS), fill=(45, 212, 191))

    if title is None:  # background only (text is added on the server)
        for xx in range(w):
            d.line([(xx, h - 8 * SS), (xx, h)], fill=lerp(c1, c2, xx / w))
        img.resize((W, H), Image.LANCZOS).save(out, 'JPEG', quality=90, optimize=True)
        return

    # title
    maxw = int(w * .62)
    size = 70
    while True:
        tf = font('ExtraBold', size * SS)
        lines = wrap(title, tf, maxw, d)
        if len(lines) <= 4 or size <= 44: break
        size -= 4
    lh = int(size * SS * 1.12)
    y = h - 64 * SS - lh * len(lines)
    for i, ln in enumerate(lines):
        d.text((m, y + i * lh), ln, font=tf, fill=(255, 255, 255))

    # category pill above title
    pf = font('Bold', 20 * SS)
    pw = d.textlength(label, font=pf) + 40 * SS
    ph = 44 * SS
    py = y - ph - 26 * SS
    pill = Image.new('RGBA', (int(pw), ph))
    pd = ImageDraw.Draw(pill)
    for xx in range(int(pw)):
        pd.line([(xx, 0), (xx, ph)], fill=lerp(c1, c2, xx / pw) + (255,))
    mask = Image.new('L', (int(pw), ph), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, pw - 1, ph - 1], radius=ph // 2, fill=255)
    img.paste(pill, (m, int(py)), mask)
    d = ImageDraw.Draw(img, 'RGBA')
    d.text((m + 20 * SS, py + ph / 2), label, font=pf, fill=(255, 255, 255), anchor='lm')

    # bottom accent bar
    for xx in range(w):
        d.line([(xx, h - 8 * SS), (xx, h)], fill=lerp(c1, c2, xx / w))

    img = img.resize((W, H), Image.LANCZOS)
    img.save(out, 'JPEG', quality=86, optimize=True, progressive=True)


def logo(out, dark_text=(30, 58, 138)):
    s = 4
    w, h = 560 * s, 120 * s
    img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    pulse_icon(d, 8 * s, 18 * s, 84 * s, (13, 148, 136), 9 * s)
    f1 = font('ExtraBold', 58 * s)
    d.text((112 * s, 60 * s), 'TechPulse', font=f1, fill=dark_text, anchor='lm')
    tw = d.textlength('TechPulse ', font=f1)
    d.text((112 * s + tw, 60 * s), 'AI', font=font('Regular', 58 * s), fill=(13, 148, 136), anchor='lm')
    bbox = img.getbbox()
    img = img.crop((0, 0, bbox[2] + 10 * s, h)).resize(((bbox[2] + 10 * s) // s, 120), Image.LANCZOS)
    img.save(out)


def icon(out):
    s = 4
    w = 512 * s
    img = Image.new('RGBA', (w, w), (0, 0, 0, 0))
    bg = Image.new('RGBA', (w, w))
    bd = ImageDraw.Draw(bg)
    for yy in range(w):
        bd.line([(0, yy), (w, yy)], fill=lerp((30, 58, 138), (13, 148, 136), yy / w) + (255,))
    mask = Image.new('L', (w, w), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, w - 1, w - 1], radius=110 * s, fill=255)
    img.paste(bg, (0, 0), mask)
    d = ImageDraw.Draw(img)
    pulse_icon(d, 66 * s, 47 * s, 380 * s, (255, 255, 255), 34 * s)
    img.resize((512, 512), Image.LANCZOS).save(out)


if __name__ == '__main__':
    posts = json.load(open(sys.argv[1]))
    for p in posts:
        featured(p['title'], p['cat'], p['slug'], f"out/{p['slug']}.jpg")
    logo('out/logo.png')
    icon('out/icon.png')
