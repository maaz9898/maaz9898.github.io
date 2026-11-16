#!/usr/bin/env python3
"""Builds the static site: index.html plus one page per project in projects/."""
import os, html

ROOT = os.path.dirname(os.path.abspath(__file__))
AI = 'AI-generated illustration'

# ---------- small helpers ----------
def img(src, alt, show=False, pre=''):
    return f'<img{" class=\"show\"" if show else ""} src="{pre}assets/{src}" alt="{html.escape(alt)}" loading="lazy">'

def vid(name, alt, show=False, pre='', auto=False, poster=None):
    return (f'<video{" class=\"show\"" if show else ""} src="{pre}assets/{name}.mp4" poster="{pre}assets/{poster or name + ".webp"}" '
            f'muted loop playsinline preload="none"{" data-auto" if auto else ""} aria-label="{html.escape(alt)}"></video>')

def tabs(items, ar='16 / 10', badge=None):
    stage = ''.join(m for m, _ in items)
    pills = ''.join(f'<button type="button" aria-pressed="{"true" if i == 0 else "false"}">{lab}</button>' for i, (_, lab) in enumerate(items))
    b = f'<span class="badge">{badge}</span>' if badge else ''
    return f'<div class="tabs" data-tabs><div class="stage" style="--ar:{ar}">{stage}{b}</div><div class="pills">{pills}</div></div>'

def media(inner, ar='16 / 10', badge=None, paper=False):
    b = f'<span class="badge">{badge}</span>' if badge else ''
    return f'<div class="media{" paper" if paper else ""}" style="--ar:{ar}">{inner}{b}</div>'

def figure(inner, caption=None):
    c = f'<figcaption>{caption}</figcaption>' if caption else ''
    return f'<figure class="fig">{inner}{c}</figure>'

def stats(items):
    return '<div class="stats">' + ''.join(f'<div><b>{a}</b><span>{b}</span></div>' for a, b in items) + '</div>'

def tags(items):
    return '<ul class="tags">' + ''.join(f'<li>{t}</li>' for t in items) + '</ul>'

# ---------- projects ----------
def projects(pre):
    P = pre
    return [
        dict(
            slug='joint-engagement', title='Are two children playing together?', kicker='Hamad Bin Khalifa University, 2025 to now',
            line='Measuring joint engagement from ordinary video.',
            tags=['Video understanding', 'Pose', 'Gaze', 'PyTorch'],
            card=media(vid('engaged', 'Two children building the same track together', True, P, True), '16 / 10'),
            facts=[('Role', 'Lead researcher'), ('Where', 'A-Sense, HBKU, Doha'), ('Paper', 'STIN, EUVIP 2026'), ('Stack', 'PyTorch, pose and gaze models')],
            body=lambda: f'''
<h2>The question</h2>
<p>Clinicians rate how engaged two children are with each other by watching video, window by window. It is slow, and it is one of the measures autism research leans on most.</p>
<div class="pair">
  <figure class="clip">{vid('engaged', 'Two children building the same track together', True, P, True)}<figcaption><span class="dot"></span>Engaged. One shared activity</figcaption></figure>
  <figure class="clip">{vid('not-engaged', 'Two children playing separately at the same box', True, P, True)}<figcaption><span class="dot off"></span>Not engaged. Each plays alone</figcaption></figure>
</div>
<p class="note">Generated examples. No frame shows a real participant.</p>

<h2>What the model looks at</h2>
{tabs([(img('je_frame.webp', 'Two children at a toy box, seen from a fixed camera', True, P), 'Video'), (img('je_features.webp', 'The same frame with boxes, body skeletons and gaze arrows', False, P), 'Pose and gaze'), (img('je_depth.webp', 'A depth map of the same frame with the distance between the children marked', False, P), 'Depth and distance')], '699 / 581')}
<p class="note">Generated frame. A journal paper on the 3D part is in preparation.</p>

<h2>STIN</h2>
<p>Each child gets a stream of pose, gaze and appearance features. The two streams attend to each other, and the distance and facing between the pair steer that attention.</p>
{figure(media(img('stin_arch.webp', 'Architecture of STIN: two per-person streams, cross-attention between them, pooling and a classifier', True, P), '1018 / 1449', None, True), 'STIN architecture, from the paper.')}

<h2>Result</h2>
{stats([('94% AP', 'public UCO-LAEO benchmark'), ('71% AP', 'child pairs never seen in training'), ('EUVIP 2026', 'first-author paper')])}
'''),
        dict(
            slug='robot-pose', title='Robots that find things within a millimetre', kicker='4DiVISION and KOREATECH, 2023 to 2025',
            line='6-DoF pose estimation for industrial robot arms.',
            tags=['6-DoF pose', 'ROS2', 'Point clouds', 'C++'],
            card=tabs([(img('bolt_pose.webp', 'A robot arm over a ring of bolts with pose axes drawn on each bolt', True, P), 'Pose'), (vid('bolt', 'The robot arm moving the tool to the next bolt', False, P), 'Clip')], '16 / 10', AI),
            facts=[('Role', 'ML researcher'), ('Where', '4DiVISION, Seoul and KOREATECH'), ('Accuracy', 'Within 1 mm'), ('Stack', 'ROS2, PyTorch, Open3D, C++')],
            body=lambda: f'''
<h2>Bolt fastening at 4DiVISION</h2>
<p>A robot arm has to put a tool on every bolt of a part it has never seen in that exact position. The camera does the finding.</p>
{tabs([(img('bolt.webp', 'A robot arm holding a fastening tool over a ring of bolts', True, P), 'Scene'), (img('bolt_detect.webp', 'A green box around each bolt', False, P), 'Detect'), (img('bolt_seg.webp', 'A colour mask on each bolt', False, P), 'Segment'), (img('bolt_cloud.webp', 'The scene as a depth-coloured point cloud', False, P), 'Point cloud'), (img('bolt_pose.webp', 'Red, green and blue pose axes on each bolt', False, P), '6-DoF pose'), (vid('bolt', 'The robot arm moving the tool to the next bolt', False, P), 'Fasten')], '16 / 10', AI)}
{stats([('&le; 1 mm', 'pose accuracy'), ('Unseen cells', 'held in factories outside the training data'), ('ROS2', 'targets streamed to the arm')])}

<h2>A robot arm on wheels at KOREATECH</h2>
<p>An arm rides on an AGV that never parks in quite the same place twice. A camera estimates the pose of the target cylinder so the arm can line itself up each time.</p>
<div class="two-up">
  {figure(media(img('agv.webp', 'A robot arm on a mobile base in the lab', True, P), '4 / 3'), 'The lab setup.')}
  {figure(media(img('agv-cad.webp', 'CAD view of the cylinder with its measured axis and offsets', True, P), '4 / 3', None, True), 'What gets estimated: the cylinder axis and its offset.')}
</div>
'''),
        dict(
            slug='precisiongan', title='PrecisionGAN', kicker="KOREATECH, master's thesis, 2023 to 2025",
            line='Thick historical print in, clean one-pixel skeleton out.',
            tags=['GAN', 'Image-to-image', 'Springer IJDAR'],
            card=media(vid('skeleton', 'Three printed characters thinning down to skeletons', True, P, True), '16 / 10', 'Illustration'),
            facts=[('Role', 'First author'), ('Where', 'KOREATECH'), ('Published', 'IJDAR, Springer, 2024'), ('Stack', 'PyTorch')],
            links=[('Paper', 'https://link.springer.com/article/10.1007/s10032-024-00505-7'), ('Code', 'https://github.com/maaz9898/PrecisionGAN')],
            body=lambda: f'''
<h2>Why skeletons</h2>
<p>To tell whether two printed characters came from the same piece of type, you compare their shapes. Ink spread gets in the way. Skeletons remove it.</p>
{figure(media(img('pg_fig1.webp', 'Overlap scores between characters before and after skeletonization', True, P), '1180 / 634', None, True), 'Comparing characters before and after skeletonization. From the paper.')}

<h2>The problem with the classical way</h2>
<p>Thinning algorithms break strokes and grow spurs. PrecisionGAN learns the mapping instead and keeps the strokes whole.</p>
{figure(media(img('precisiongan.webp', 'A character, a broken classical skeleton, and a clean PrecisionGAN skeleton', True, P), '689 / 560', None, True), 'Original, classical thinning, PrecisionGAN. From the paper.')}

<h2>The model</h2>
{figure(media(img('pg_arch.webp', 'Generator architecture with attention in the skip connections', True, P), '903 / 748', None, True), 'Generator with multi-head attention in the skip connections. From the paper.')}
'''),
        dict(
            slug='metal-type', title='Tracing Joseon metal type', kicker='KOREATECH with the National Museum of Korea, 2023 to 2025',
            line='Which prints came from the same piece of metal?',
            tags=['Shape similarity', 'Document analysis', 'Cultural heritage'],
            card=media(vid('metaltype', 'Twelve prints of one character sorting into three groups', True, P, True, 'metaltype-anim.webp'), '16 / 10', 'Illustration'),
            facts=[('Role', 'Researcher, first and second author'), ('Where', 'KOREATECH'), ('Funded by', 'National Museum of Korea'), ('Papers', '3')],
            links=[('Similarity paper', 'http://journal.auric.kr/ieiespc/XmlViewer/f450827'), ('Chases paper', 'https://diglib.eg.org/items/930f4c5d-f291-4cf6-868a-b03688164b69')],
            body=lambda: f'''
<h2>The idea</h2>
<p>Joseon printers set pages from individual metal types. Every type has tiny quirks, so prints from the same type share a shape. Group the shapes and you recover the type set, and how the book was printed.</p>
{figure(media(vid('metaltype', 'Twelve prints of one character sorting into three groups', True, P, True, 'metaltype-anim.webp'), '16 / 10', 'Illustration'))}

<h2>The pipeline</h2>
{figure(media(img('metaltype.webp', 'From scanned page to segmented characters, similarity grouping and reconstructed type', True, P), '1200 / 298', None, True), 'From scanned page to grouped characters. From the paper.')}
'''),
        dict(
            slug='smart-cart', title='Smart shopping carts', kicker='Bleed AI, for Veeve, 2022 to 2023',
            line='A cart that knows what went in and what came out.',
            tags=['Action recognition', 'Edge TPU', 'Real time'],
            card=tabs([(img('veeve_det.webp', 'A hand placing a box into a cart with keypoints and a box drawn on it', True, P), 'Model view'), (vid('veeve', 'A hand placing a box into a shopping cart', False, P), 'Clip')], '16 / 10', AI),
            facts=[('Role', 'Project lead and engineer'), ('Client', 'Veeve'), ('Runs on', 'Google Coral Edge TPU'), ('Team', '5 engineers')],
            body=lambda: f'''
<h2>What it does</h2>
<p>A camera on the cart watches the basket. The model recognises an item being added or taken out, in real time, on a chip that costs a few dollars.</p>
{tabs([(img('veeve_det.webp', 'A hand placing a box into a cart with keypoints and a box drawn on it', True, P), 'Model view'), (vid('veeve', 'A hand placing a box into a shopping cart', False, P), 'Clip')], '16 / 10', AI)}
{stats([('Real time', 'on Coral Edge TPU'), ('10+', 'client projects led at Bleed AI'), ('5', 'engineers on the team')])}
'''),
        dict(
            slug='vidan', title='Vidan.ai', kicker='Liquid Technologies, Karachi, 2021 to 2022',
            line='Video analytics on small computers.',
            tags=['Train monitoring', 'Plate recognition', 'Edge devices'],
            card=tabs([(img('vidan_det.webp', 'A freight train with a box around each wagon', True, P), 'Model view'), (vid('vidan', 'A freight train passing a platform', False, P), 'Clip')], '16 / 10', AI),
            facts=[('Role', 'Core developer'), ('Where', 'Liquid Technologies'), ('Built', 'Architecture, ALPR, train monitoring'), ('Runs on', 'Single-board computers')],
            links=[('vidan.ai', 'https://vidan.ai/')],
            body=lambda: f'''
<h2>What it does</h2>
<p>Cameras that count, read and flag things on their own. I designed the platform architecture and built the licence plate recognition and train monitoring modules.</p>
{tabs([(img('vidan_det.webp', 'A freight train with a box around each wagon', True, P), 'Model view'), (vid('vidan', 'A freight train passing a platform', False, P), 'Clip')], '16 / 10', AI)}
'''),
        dict(
            slug='fitx', title='FitX exercise coach', kicker='Mobile app',
            line='Counts reps and catches bad form from a phone camera.',
            tags=['Pose estimation', 'MediaPipe', 'Mobile'],
            card=media(vid('fitx', 'A person doing squats with a pose skeleton drawn over them', True, P, True), '16 / 10'),
            facts=[('Role', 'Prototype, architecture, project lead'), ('Stack', 'Python, MediaPipe'), ('Features', 'Rep counter, mistake detection')],
            body=lambda: f'''
<h2>What it does</h2>
<p>Point the phone at yourself and exercise. The app tracks your joints, counts each rep and tells you when your form slips.</p>
<div class="two-up">
  {figure(media(vid('fitx', 'A person doing squats with a pose skeleton drawn over them', True, P, True), '16 / 10'))}
  {figure(media(img('fitx_phone.webp', 'The app on a phone showing a squat with joint angles', True, P), '429 / 884'))}
</div>
'''),
    ]

PUBS = [
    ('STIN: A Socio-Temporal Interaction Network for Dyadic Interaction Analysis', None, 'EUVIP 2026', True),
    ('PrecisionGAN: Enhanced Image-to-Image Translation for Preserving Structural Integrity in Skeletonized Images', 'https://link.springer.com/article/10.1007/s10032-024-00505-7', 'IJDAR (Springer), 2024', True),
    ('Evaluating Similarity between Characters Printed Using Ancient Movable Metal Types', 'http://journal.auric.kr/ieiespc/XmlViewer/f450827', 'IEIE Transactions on Smart Processing and Computing, 2025', True),
    ('Smoothed Boundary Distance Loss Function for Enhancing Character Extraction from High-Resolution Scans of Historical Documents', 'https://paper.cricit.kr/user/search/site/ieie2018/cart_rdoc.asp?URL=files/filename%3Fnum%3D457024%26db%3DRD_R&dn=457024&db=RD_R&usernum=0&seid=', 'IEIE Transactions on Smart Processing and Computing, 2025', False),
    ('Estimating the Number of Chases Used for Printing Books with Movable Metal Types', 'https://diglib.eg.org/items/930f4c5d-f291-4cf6-868a-b03688164b69', 'Eurographics GCH, 2023', False),
]

EXPERIENCE = [
    ('2025 to now', 'Graduate Research Assistant', 'Hamad Bin Khalifa University, Doha'),
    ('2025', 'Machine Learning Researcher', '4DiVISION, Seoul'),
    ('2023 to 2025', 'M.S. and Research Assistant', 'KOREATECH, South Korea'),
    ('2022 to 2023', 'AI Project Manager', 'Bleed AI, remote'),
    ('2021 to 2022', 'Machine Learning Engineer', 'Liquid Technologies, Karachi'),
    ('2020 to 2021', 'Embedded Systems Engineer', 'Sudoware, Karachi'),
]

ICONS = {
    'github': '<path d="M12 .5a11.5 11.5 0 0 0-3.64 22.41c.58.1.79-.25.79-.56v-2c-3.2.7-3.88-1.37-3.88-1.37-.52-1.33-1.28-1.69-1.28-1.69-1.05-.71.08-.7.08-.7 1.16.08 1.77 1.19 1.77 1.19 1.03 1.77 2.7 1.26 3.36.96.1-.75.4-1.26.73-1.55-2.55-.29-5.24-1.28-5.24-5.69 0-1.26.45-2.29 1.19-3.09-.12-.3-.52-1.47.11-3.06 0 0 .97-.31 3.17 1.18a11 11 0 0 1 5.78 0c2.2-1.49 3.17-1.18 3.17-1.18.63 1.59.23 2.76.11 3.06.74.8 1.19 1.83 1.19 3.09 0 4.42-2.7 5.4-5.26 5.68.41.36.78 1.06.78 2.14v3.17c0 .31.21.67.8.56A11.5 11.5 0 0 0 12 .5Z"/>',
    'linkedin': '<path d="M20.45 20.45h-3.55v-5.57c0-1.33-.03-3.04-1.85-3.04-1.86 0-2.14 1.45-2.14 2.94v5.67H9.35V9h3.41v1.56h.05c.47-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46v6.28ZM5.34 7.43a2.06 2.06 0 1 1 0-4.12 2.06 2.06 0 0 1 0 4.12ZM7.12 20.45H3.56V9h3.56v11.45ZM22.22 0H1.77C.79 0 0 .77 0 1.73v20.54C0 23.23.79 24 1.77 24h20.45c.98 0 1.78-.77 1.78-1.73V1.73C24 .77 23.2 0 22.22 0Z"/>',
    'scholar': '<path d="M12 2 0 9.5l4.84 3.02A7.5 7.5 0 1 0 19.5 15v-2.69L22 10.75V17h2V9.5L12 2Zm0 18.5A5.5 5.5 0 0 1 6.5 15v-1.44L12 17l5.5-3.44V15a5.5 5.5 0 0 1-5.5 5.5Z"/>',
    'moon': '<path d="M20.4 14.5A8.5 8.5 0 0 1 9.5 3.6a.75.75 0 0 0-.98-.94A10 10 0 1 0 21.34 15.5a.75.75 0 0 0-.94-1Z"/>',
    'sun': '<path d="M12 7a5 5 0 1 0 0 10 5 5 0 0 0 0-10Zm0-6a1 1 0 0 1 1 1v2a1 1 0 1 1-2 0V2a1 1 0 0 1 1-1Zm0 18a1 1 0 0 1 1 1v2a1 1 0 1 1-2 0v-2a1 1 0 0 1 1-1ZM1 12a1 1 0 0 1 1-1h2a1 1 0 1 1 0 2H2a1 1 0 0 1-1-1Zm18 0a1 1 0 0 1 1-1h2a1 1 0 1 1 0 2h-2a1 1 0 0 1-1-1ZM4.22 4.22a1 1 0 0 1 1.42 0l1.41 1.42a1 1 0 0 1-1.41 1.41L4.22 5.64a1 1 0 0 1 0-1.42Zm12.73 12.73a1 1 0 0 1 1.41 0l1.42 1.41a1 1 0 0 1-1.42 1.42l-1.41-1.42a1 1 0 0 1 0-1.41ZM4.22 19.78a1 1 0 0 1 0-1.42l1.42-1.41a1 1 0 0 1 1.41 1.41l-1.41 1.42a1 1 0 0 1-1.42 0ZM16.95 7.05a1 1 0 0 1 0-1.41l1.41-1.42a1 1 0 1 1 1.42 1.42l-1.42 1.41a1 1 0 0 1-1.41 0Z"/>',
}
def icon(n, cls=''):
    return f'<svg{f" class=\"{cls}\"" if cls else ""} viewBox="0 0 24 24" aria-hidden="true">{ICONS[n]}</svg>'

def page(title, desc, pre, body):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="color-scheme" content="dark light">
<script>
  (function () {{
    var t = null;
    try {{ t = localStorage.getItem('theme'); }} catch (e) {{}}
    if (t !== 'light' && t !== 'dark') t = matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark';
    document.documentElement.dataset.theme = t;
  }})();
</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{pre}assets/site.css">
</head>
<body>
<a class="skip" href="#content">Skip to content</a>
<header class="top">
  <div class="wrap bar">
    <a class="brand" href="{pre}index.html">Maaz Ahmed</a>
    <nav aria-label="Main">
      <a href="{pre}index.html#work">Work</a>
      <a href="{pre}index.html#publications">Publications</a>
      <a href="{pre}index.html#experience">Experience</a>
      <a href="{pre}index.html#contact">Contact</a>
    </nav>
    <button class="icon" id="theme" type="button" aria-label="Switch between dark and light mode" title="Switch theme">{icon('moon', 'moon')}{icon('sun', 'sun')}</button>
  </div>
</header>
<main id="content" class="wrap">
{body}
</main>
<footer class="wrap foot">
  <span>Maaz Ahmed, Doha, Qatar</span>
  <span class="social">
    <a class="icon" href="https://github.com/maaz9898" aria-label="GitHub" title="GitHub">{icon('github')}</a>
    <a class="icon" href="https://www.linkedin.com/in/maazahmed98" aria-label="LinkedIn" title="LinkedIn">{icon('linkedin')}</a>
    <a class="icon" href="https://scholar.google.com/citations?user=TZpghL4AAAAJ" aria-label="Google Scholar" title="Google Scholar">{icon('scholar')}</a>
  </span>
</footer>
<script src="{pre}assets/site.js"></script>
</body>
</html>
'''

def build_home():
    ps = projects('')
    cards = ''
    for i, p in enumerate(ps):
        cards += f'''
      <li class="card{" wide" if i < 2 or i >= 5 else ""}">
        {p["card"]}
        <a class="body" href="projects/{p["slug"]}.html">
          <h3>{p["title"]}</h3>
          <p>{p["line"]}</p>
          {tags(p["tags"][:3])}
          <span class="more">Open project</span>
        </a>
      </li>'''
    pubs = ''
    for t, url, venue, first in PUBS:
        tt = f'<a class="t" href="{url}">{t}</a>' if url else f'<span class="t">{t}</span>'
        pubs += f'<li>{tt}<span class="v">{venue}. {"<span class=\"me\">First author</span>" if first else "Second author"}</span></li>'
    exp = ''.join(f'<li><span class="when">{w}</span><span><b>{t}</b> <span class="at">{o}</span></span></li>' for w, t, o in EXPERIENCE)
    body = f'''
  <section class="intro">
    <img class="portrait" src="assets/maaz.webp" alt="Portrait of Maaz Ahmed" width="148" height="148">
    <div>
      <h1>Maaz Ahmed</h1>
      <p class="role">I teach machines to see. Computer vision for robots and for video of people.</p>
      <p class="links"><a class="btn" href="mailto:maaz9898@gmail.com">Email me</a><a href="https://github.com/maaz9898">GitHub</a><a href="https://scholar.google.com/citations?user=TZpghL4AAAAJ">Google Scholar</a><a href="https://www.linkedin.com/in/maazahmed98">LinkedIn</a></p>
    </div>
  </section>

  <div class="hero">
    <video src="assets/hero.mp4" poster="assets/hero.webp" muted loop playsinline preload="none" data-auto aria-label="A lab bench turning from a photo into a glowing 3D point cloud"></video>
    <span class="badge">{AI}</span>
  </div>

  <section id="work">
    <h2>Work</h2>
    <ul class="cards">{cards}
    </ul>
  </section>

  <section id="publications">
    <h2>Publications</h2>
    <ul class="pubs">{pubs}</ul>
  </section>

  <section id="experience">
    <h2>Experience</h2>
    <ul class="slim">{exp}</ul>
  </section>

  <section id="contact">
    <h2>Contact</h2>
    <p class="links"><a href="mailto:maaz9898@gmail.com">maaz9898@gmail.com</a><a href="https://www.linkedin.com/in/maazahmed98">LinkedIn</a><a href="https://github.com/maaz9898">GitHub</a><a href="https://scholar.google.com/citations?user=TZpghL4AAAAJ">Google Scholar</a></p>
  </section>
'''
    open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf8').write(
        page('Maaz Ahmed | Computer Vision and Robotics', 'Maaz Ahmed builds computer vision for robots and for video of people. Projects, publications and contact.', '', body))

def build_projects():
    ps = projects('../')
    os.makedirs(os.path.join(ROOT, 'projects'), exist_ok=True)
    for i, p in enumerate(ps):
        prev, nxt = ps[i - 1], ps[(i + 1) % len(ps)]
        facts = ''.join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in p['facts'])
        links = ''.join(f'<a class="btn ghost" href="{u}">{t}</a>' for t, u in p.get('links', []))
        body = f'''
  <article class="project">
    <a class="back" href="../index.html#work">All work</a>
    <header class="phead">
      <p class="kicker">{p["kicker"]}</p>
      <h1>{p["title"]}</h1>
      <p class="role">{p["line"]}</p>
      {tags(p["tags"])}
      {f'<p class="links">{links}</p>' if links else ''}
    </header>
    <dl class="facts">{facts}</dl>
    <div class="prose">{p["body"]()}</div>
    <nav class="pn" aria-label="More projects">
      <a href="{prev["slug"]}.html"><span>Previous</span><b>{prev["title"]}</b></a>
      <a href="{nxt["slug"]}.html"><span>Next</span><b>{nxt["title"]}</b></a>
    </nav>
  </article>
'''
        open(os.path.join(ROOT, 'projects', p['slug'] + '.html'), 'w', encoding='utf8').write(
            page(p['title'] + ' | Maaz Ahmed', p['line'], '../', body))

if __name__ == '__main__':
    build_home(); build_projects(); print('built', 1 + len(projects('')), 'pages')
