#!/usr/bin/env python3
"""Builds the static site: index.html plus one page per project in projects/."""
import os, html

ROOT = os.path.dirname(os.path.abspath(__file__))
AI = None

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

def compare(human, machine, alt, pre='', ar='16 / 10'):
    """Before/after slider: the plain view on the left of the handle, the machine view on the right."""
    return (f'<div class="cmp" data-cmp style="--ar:{ar}">'
            f'<img src="{pre}assets/{machine}" alt="" loading="lazy">'
            f'<img class="over" src="{pre}assets/{human}" alt="{html.escape(alt)}" loading="lazy">'
            f'<span class="handle" aria-hidden="true"></span>'
            f'<input type="range" min="0" max="100" value="55" aria-label="Drag to compare the camera view with the machine view">'
            f'</div>')

def figure(inner, caption=None):
    c = f'<figcaption>{caption}</figcaption>' if caption else ''
    return f'<figure class="fig">{inner}{c}</figure>'

def label(x, y, text, w):
    return f'<g class="lab"><rect x="{x}" y="{y - 30}" width="{w}" height="42" rx="8"/><text x="{x + 14}" y="{y}">{text}</text></g>'

def film_annot(pre):
    return f"""<div class="annot" data-annot data-step="0">
  <div class="stage" style="--ar:1312 / 864">
    <img src="{pre}assets/cadreal.webp" alt="The alignment rig: a hollow white cylinder held in clamps on a gantry, a smaller cylinder on a stage to its left, and a round camera opening in the base plate below" loading="lazy">
    <video src="{pre}assets/insert.mp4" muted loop playsinline preload="none" aria-label="The smaller cylinder sliding into the hollow one"></video>
    <svg class="ov" viewBox="0 0 1312 864" aria-hidden="true">
      <g class="s1">
        <ellipse class="cam" cx="797" cy="707" rx="108" ry="30"/>
        <path class="sight draw" pathLength="1" d="M797 707 L465 175"/>
        {label(850, 790, 'Upward-facing camera', 300)}
      </g>
      <g class="s2">
        <ellipse class="end draw" pathLength="1" cx="465" cy="175" rx="20" ry="92"/>
        {label(505, 62, 'Open end detected as an ellipse', 440)}
      </g>
      <g class="s3">
        <path class="dx draw" pathLength="1" d="M465 175 L800 172"/>
        <path class="dy draw" pathLength="1" d="M800 172 L797 707"/>
        {label(570, 150, 'dX 178 mm', 176)}
        {label(822, 440, 'dY 281.9 mm', 204)}
        {label(430, 470, 'Centre distance 333.4 mm', 362)}
      </g>
    </svg>
  </div>
  <div class="pills"><button type="button" aria-pressed="true">Rig</button><button type="button" aria-pressed="false">Camera</button><button type="button" aria-pressed="false">Detect the end</button><button type="button" aria-pressed="false">Measure offset</button><button type="button" aria-pressed="false">Insertion</button></div>
</div>"""

def stats(items):
    return '<div class="stats">' + ''.join(f'<div><b>{a}</b><span>{b}</span></div>' for a, b in items) + '</div>'

def tags(items):
    return '<ul class="tags">' + ''.join(f'<li>{t}</li>' for t in items) + '</ul>'

# ---------- projects ----------
def projects(pre):
    P = pre
    return [
        dict(
            slug='joint-engagement', title='Automated Assessment of Joint Engagement in Children', kicker='Hamad Bin Khalifa University, Sep 2025 – Present',
            line='Video models that measure social engagement between two children from a single camera.',
            tags=['Video understanding', 'Pose', 'Gaze', 'PyTorch'],
            card=compare('je_frame.webp', 'je_features.webp', 'Two children at a toy box. Drag to reveal the detected skeletons and gaze', P),
            facts=[('Role', 'Lead researcher'), ('Where', 'A-Sense, HBKU, Doha'), ('Paper', 'STIN, EUVIP 2026'), ('Stack', 'PyTorch, pose and gaze models')],
            body=lambda: f'''
<h2>Problem</h2>
<p>Joint engagement between children is a key behavioural measure in autism research. It is currently rated manually from video, one window at a time, which is slow and difficult to scale.</p>
<div class="pair">
  <figure class="clip">{vid('engaged', 'Two children building the same track together', True, P, True)}<figcaption><span class="dot"></span>Jointly engaged: one shared activity</figcaption></figure>
  <figure class="clip">{vid('not-engaged', 'Two children playing separately at the same box', True, P, True)}<figcaption><span class="dot off"></span>Not jointly engaged: parallel play</figcaption></figure>
</div>
<p class="note">Generated examples. No frame shows a real participant.</p>

<h2>Input Signals</h2>
{tabs([(img('je_frame.webp', 'Two children at a toy box, seen from a fixed camera', True, P), 'Video'), (img('je_features.webp', 'The same frame with boxes, body skeletons and gaze arrows', False, P), 'Pose and gaze'), (img('je_depth.webp', 'A depth map of the same frame with the distance between the children marked', False, P), 'Depth and distance')], '699 / 581')}
<p class="note">Generated frame. A journal paper on the 3D pipeline is in preparation.</p>

<h2>Model: STIN</h2>
<p>STIN represents each child with a stream of pose, gaze and appearance features. Cross-attention between the two streams is guided by the distance and orientation between the pair.</p>
{figure(media(img('stin_arch.webp', 'Architecture of STIN: two per-person streams, cross-attention between them, pooling and a classifier', True, P), '1018 / 1449', None, True), 'STIN architecture, from the paper.')}

<h2>Results</h2>
{stats([('94% AP', 'public UCO-LAEO benchmark'), ('71% AP', 'child pairs never seen in training'), ('EUVIP 2026', 'first-author paper')])}
'''),
        dict(
            slug='bolt-fastening', title='Vision-Guided Robotic Bolt Fastening', kicker='4DiVISION, Seoul, Feb 2025 – Jul 2025',
            line='6-DoF pose estimation that guides an industrial robot arm to within 1 mm.',
            tags=['6-DoF pose', 'ROS2', 'Point clouds', 'C++'],
            card=compare('bolt.webp', 'bolt_pose.webp', 'A robot arm over a ring of bolts. Drag to reveal the estimated pose of each bolt', P),
            facts=[('Role', 'ML researcher'), ('Where', '4DiVISION, Seoul'), ('Accuracy', 'Within 1 mm'), ('Stack', 'ROS2, PyTorch, Open3D, C++')],
            body=lambda: f"""
<h2>Overview</h2>
<p>An industrial robot arm must place a fastening tool on every bolt of a part whose exact position is not known in advance. The vision pipeline detects each bolt, estimates its 6-DoF pose and sends the targets to the arm.</p>
{tabs([(img('bolt.webp', 'A robot arm holding a fastening tool over a ring of bolts', True, P), 'Scene'), (img('bolt_detect.webp', 'A green box around each bolt', False, P), 'Detect'), (img('bolt_seg.webp', 'A colour mask on each bolt', False, P), 'Segment'), (img('bolt_cloud.webp', 'The scene as a depth-coloured point cloud', False, P), 'Point cloud'), (img('bolt_pose.webp', 'Red, green and blue pose axes on each bolt', False, P), '6-DoF pose'), (vid('bolt', 'The robot arm moving the tool to the next bolt', False, P), 'Fasten')], '16 / 10', AI)}
{stats([('&le; 1 mm', 'pose accuracy'), ('Unseen cells', 'accuracy held in factory cells outside the training data'), ('ROS2', 'targets streamed to the arm')])}

<h2>Lab Setup</h2>
{figure(media(img('lab.webp', 'A collaborative robot arm with a camera and tool on an aluminium test bench in the lab', True, P), '4 / 3'), 'The lab setup used to develop and test the pipeline.')}
"""),
        dict(
            slug='film-roll', title='Vision-Based Alignment for Film Roll Handling', kicker='KOREATECH, Mar 2023 – Feb 2025',
            line='Camera-based pose estimation that aligns two cylinders for automated insertion.',
            tags=['Pose estimation', 'Ellipse fitting', '3D shape matching'],
            card=tabs([(img('cadreal.webp', 'The alignment rig with a hollow white cylinder in clamps and a smaller cylinder beside it', True, P), 'Rig'), (vid('insert', 'The smaller cylinder sliding into the hollow one', False, P, False, 'cadreal.webp'), 'Insertion')], '1312 / 864', AI),
            facts=[('Role', 'Graduate researcher'), ('Where', 'KOREATECH'), ('Problem', 'One cylinder into another'), ('Measured', 'dX, dY and centre distance')],
            body=lambda: f"""
<h2>Overview</h2>
<p>In film production lines that cut and align large rolls, one cylinder must be inserted into another. A camera mounted in the base looks up at the open end of the cylinder, locates it and measures its offset so the insertion can be corrected.</p>
{film_annot(P)}

<h2>CAD Model</h2>
{figure(media(img('agv-cad.webp', 'CAD view of the rig with the measured dX, dY and centre distance', True, P), '900 / 599', None, True), 'The CAD model with the measured offsets.')}
"""),
        dict(
            slug='precisiongan', title='PrecisionGAN: Skeletonization of Historical Printed Characters', kicker="KOREATECH, master's thesis, Mar 2023 – Feb 2025",
            line='A GAN that extracts clean, structure-preserving skeletons from historical print.',
            tags=['GAN', 'Image-to-image', 'Springer IJDAR'],
            card=compare('sk_before.webp', 'sk_after.webp', 'Three printed characters. Drag to reveal their skeletons', P),
            facts=[('Role', 'First author'), ('Where', 'KOREATECH'), ('Published', 'IJDAR, Springer, 2024'), ('Stack', 'PyTorch')],
            links=[('Paper', 'https://link.springer.com/article/10.1007/s10032-024-00505-7'), ('Code', 'https://github.com/maaz9898/PrecisionGAN')],
            body=lambda: f'''
<h2>Motivation</h2>
<p>Identifying whether two printed characters came from the same piece of type requires comparing their shapes. Ink spread distorts that comparison, and skeletonization removes it.</p>
{figure(media(img('pg_fig1.webp', 'Overlap scores between characters before and after skeletonization', True, P), '1180 / 634', None, True), 'Comparing characters before and after skeletonization. From the paper.')}

<h2>Limitation of Classical Thinning</h2>
<p>Classical thinning algorithms break strokes and introduce spurious branches. PrecisionGAN learns the mapping from printed character to skeleton and preserves the stroke structure.</p>
{figure(media(img('precisiongan.webp', 'A character, a broken classical skeleton, and a clean PrecisionGAN skeleton', True, P), '689 / 560', None, True), 'Original, classical thinning, PrecisionGAN. From the paper.')}

<h2>Architecture</h2>
{figure(media(img('pg_arch.webp', 'Generator architecture with attention in the skip connections', True, P), '903 / 748', None, True), 'Generator with multi-head attention in the skip connections. From the paper.')}
'''),
        dict(
            slug='metal-type', title='Movable Metal Type Analysis for Joseon-Era Books', kicker='KOREATECH with the National Museum of Korea, Mar 2023 – Feb 2025',
            line='Shape similarity analysis that identifies prints made from the same metal type.',
            tags=['Shape similarity', 'Document analysis', 'Cultural heritage'],
            card=compare('mt_before.webp', 'mt_after.webp', 'Twelve prints of one character. Drag to reveal them grouped by metal type', P),
            facts=[('Role', 'Researcher, first and second author'), ('Where', 'KOREATECH'), ('Funded by', 'National Museum of Korea'), ('Papers', '3')],
            links=[('Similarity paper', 'http://journal.auric.kr/ieiespc/XmlViewer/f450827'), ('Chases paper', 'https://diglib.eg.org/items/930f4c5d-f291-4cf6-868a-b03688164b69')],
            body=lambda: f'''
<h2>Overview</h2>
<p>Joseon-era books were printed with individual metal types, each with small distinguishing features. Prints from the same type share a shape, so grouping characters by shape similarity reveals the type set and how a book was printed.</p>
{figure(media(vid('metaltype', 'Twelve prints of one character sorting into three groups', True, P, True, 'metaltype-anim.webp'), '16 / 10'))}

<h2>Pipeline</h2>
{figure(media(img('metaltype.webp', 'From scanned page to segmented characters, similarity grouping and reconstructed type', True, P), '1200 / 298', None, True), 'From scanned page to grouped characters. From the paper.')}
'''),
        dict(
            slug='smart-cart', title='Real-Time Action Recognition for Smart Shopping Carts', kicker='Bleed AI, for Veeve, Jan 2022 – Mar 2023',
            line='Edge models that detect items being added to or removed from a cart.',
            tags=['Action recognition', 'Edge TPU', 'Real time'],
            card=compare('veeve.webp', 'veeve_det.webp', 'A hand placing a box into a cart. Drag to reveal what the model detects', P),
            facts=[('Role', 'Project lead and engineer'), ('Client', 'Veeve'), ('Runs on', 'Google Coral Edge TPU'), ('Team', '5 engineers')],
            body=lambda: f'''
<h2>Overview</h2>
<p>A camera mounted on the cart observes the basket. The model recognises items being added or removed in real time on a low-power edge accelerator.</p>
{tabs([(img('veeve_det.webp', 'A hand placing a box into a cart with keypoints and a box drawn on it', True, P), 'Model view'), (vid('veeve', 'A hand placing a box into a shopping cart', False, P), 'Clip')], '16 / 10', AI)}
{stats([('Real time', 'on Coral Edge TPU'), ('10+', 'client projects led at Bleed AI'), ('5', 'engineers on the team')])}
'''),
        dict(
            slug='vidan', title='Vidan.ai Video Analytics Platform', kicker='Liquid Technologies, Karachi, Aug 2021 – Feb 2022',
            line='Real-time video analytics, dashboards and alerts running on edge devices.',
            tags=['Video analytics', 'Dashboards', 'Edge devices'],
            card=compare('vidan.webp', 'vidan_det.webp', 'A freight train passing a platform. Drag to reveal the detected wagons', P),
            facts=[('Role', 'Core developer'), ('Where', 'Liquid Technologies'), ('Built', 'Architecture, ALPR, train monitoring, dashboards'), ('Runs on', 'Single-board computers')],
            links=[('vidan.ai', 'https://vidan.ai/')],
            body=lambda: f"""
<h2>Platform Overview</h2>
<p>Each camera runs its own model on an edge device. Events are collected in a central dashboard, and alerts are sent to the responsible team.</p>
<div class="dash" data-dash>
  <div class="dash-top"><b>Operations overview</b><span class="live"><i></i>Live</span></div>
  <div class="dash-grid">
    <div class="cams">
      <figure class="cam">{vid('vidan', 'A freight train passing a platform', True, P, True)}<figcaption>Rail yard<span>Train monitoring</span></figcaption></figure>
      <figure class="cam">{img('gate.webp', 'A van at a gate with its number plate boxed', True, P)}<figcaption>Main gate<span>Plate recognition</span></figcaption></figure>
      <figure class="cam">{img('ppe.webp', 'Workers on a factory floor boxed green or red by safety gear', True, P)}<figcaption>Floor 2<span>Safety gear</span></figcaption></figure>
      <figure class="cam">{img('zone.webp', 'A forklift entering a red restricted zone in a warehouse', True, P)}<figcaption>Warehouse B<span>Restricted zone</span></figcaption></figure>
    </div>
    <aside class="dash-side">
      <div class="kpis"><div><b data-count="412">412</b><span>wagons counted</span></div><div><b data-count="128">128</b><span>vehicles read</span></div><div><b>3</b><span>open alerts</span></div></div>
      <svg class="bars" viewBox="0 0 240 70" role="img" aria-label="Events per hour, rising through the day"><g>{''.join(f'<rect x="{6 + k * 19.5:.1f}" y="{66 - h}" width="13" height="{h}" rx="3"/>' for k, h in enumerate([14, 20, 17, 30, 38, 34, 46, 52, 41, 58, 49, 62]))}</g></svg>
      <ul class="alerts" data-alerts>
        <li class="warn"><b>No hard hat</b><span>Floor 2</span></li>
        <li class="bad"><b>Forklift in restricted zone</b><span>Warehouse B</span></li>
        <li><b>Unknown vehicle at gate</b><span>Main gate</span></li>
        <li><b>Train arrived, 34 wagons</b><span>Rail yard</span></li>
        <li class="warn"><b>Wagon door open</b><span>Rail yard</span></li>
      </ul>
    </aside>
  </div>
</div>
<p class="note">Illustrative mock-up of the dashboard, with generated camera views and sample numbers.</p>

<h2>My Contributions</h2>
{stats([('Architecture', 'the platform design, edge to dashboard'), ('Two modules', 'plate recognition and train monitoring'), ('Dashboards', 'live views, counts and alerts')])}

<h2>Detection Modules</h2>
{tabs([(img('vidan_det.webp', 'A freight train with a box around each wagon', True, P), 'Trains'), (img('gate.webp', 'A van at a gate with its number plate boxed', False, P), 'Plates'), (img('ppe.webp', 'Workers on a factory floor boxed green or red by safety gear', False, P), 'Safety gear'), (img('zone.webp', 'A forklift entering a red restricted zone in a warehouse', False, P), 'Restricted zones'), (vid('vidan', 'A freight train passing a platform', False, P), 'Clip')], '16 / 10', AI)}
"""),
        dict(
            slug='fitx', title='FitX: Real-Time Exercise Form Analysis', kicker='Mobile app',
            line='A mobile app that counts repetitions and flags form errors using pose estimation.',
            tags=['Pose estimation', 'MediaPipe', 'Mobile'],
            card=compare('fitx_photo.webp', 'fitx_pose.webp', 'A man at the bottom of a squat. Drag to reveal the detected body keypoints and knee angle', P),
            facts=[('Role', 'Prototype, architecture, project lead'), ('Stack', 'Python, MediaPipe'), ('Features', 'Rep counter, form error detection'), ('Platform', 'Mobile')],
            body=lambda: f"""
<h2>Overview</h2>
<p>The app tracks body joints through the phone camera, counts each repetition and notifies the user when their form deviates.</p>
{compare('fitx_photo.webp', 'fitx_pose.webp', 'A man at the bottom of a squat. Drag to reveal the detected body keypoints and knee angle', P)}

<h2>How It Works</h2>
<p>Joint angles are computed from the detected keypoints on every frame. A repetition counts only when the knee angle passes the depth threshold and returns to standing. Try both modes.</p>
<div class="fx" data-fitx>
  <div class="phone"><canvas width="300" height="520" role="img" aria-label="A stick figure doing squats with a live knee angle, a rep counter and form feedback"></canvas></div>
  <div class="fx-side">
    <div class="pills"><button type="button" aria-pressed="true" data-mode="good">Full squats</button><button type="button" aria-pressed="false" data-mode="shallow">Shallow squats</button></div>
    <dl class="fx-read">
      <div><dt>Repetitions</dt><dd data-reps>0</dd></div>
      <div><dt>Knee angle</dt><dd><span data-angle>180</span>&deg;</dd></div>
      <div><dt>Feedback</dt><dd data-msg>Ready</dd></div>
    </dl>
    <p class="note">Interactive illustration of the counting logic. A shallow squat never reaches the depth threshold, so it is flagged and not counted.</p>
  </div>
</div>

<h2>In Use</h2>
<div class="two-up">
  {figure(media(vid('fitx_squat', 'A man standing up from a squat and lowering back down', True, P, True, 'fitx_photo.webp'), '16 / 10'), 'A full repetition, from the bottom of the squat to standing and back.')}
  {figure(media(vid('fitx', 'A person doing squats with a pose skeleton drawn over them', True, P, True), '16 / 10'), 'Output from the working prototype.')}
</div>
{figure(media(img('fitx_phone.webp', 'The FitX app on a phone showing a squat with the skeleton and joint angle', True, P), '429 / 884'), 'The app on a phone.')}
"""),
    ]

PUBS = [
    ('STIN: A Socio-Temporal Interaction Network for Dyadic Interaction Analysis', None, 'EUVIP 2026', True),
    ('Evaluating Similarity between Characters Printed Using Ancient Movable Metal Types', 'http://journal.auric.kr/ieiespc/XmlViewer/f450827', 'IEIE Transactions on Smart Processing and Computing, 2026', True),
    ('Smoothed Boundary Distance Loss Function for Enhancing Character Extraction from High-Resolution Scans of Historical Documents', 'https://paper.cricit.kr/user/search/site/ieie2018/cart_rdoc.asp?URL=files/filename%3Fnum%3D457024%26db%3DRD_R&dn=457024&db=RD_R&usernum=0&seid=', 'IEIE Transactions on Smart Processing and Computing, 2025', False),
    ('PrecisionGAN: Enhanced Image-to-Image Translation for Preserving Structural Integrity in Skeletonized Images', 'https://link.springer.com/article/10.1007/s10032-024-00505-7', 'IJDAR (Springer), 2024', True),
    ('Estimating the Number of Chases Used for Printing Books with Movable Metal Types', 'https://diglib.eg.org/items/930f4c5d-f291-4cf6-868a-b03688164b69', 'Eurographics GCH, 2023', False),
]

EXPERIENCE = [
    dict(when='Sep 2025 – Present', title='Graduate Research Assistant', org='Hamad Bin Khalifa University (A-Sense)', loc='Doha, Qatar',
         bullets=['Built STIN, a temporal network that combines body pose, gaze and interpersonal distance to classify social engagement between two people in video. It reaches 94% AP on the UCO-LAEO benchmark and 71% AP on unseen child pairs. Published at EUVIP 2026.',
                  'Built the video pipeline behind it, from person detection and tracking to pose and gaze target estimation on free-play recordings.',
                  'Building a synthetic data framework for child interaction video, because privacy and IRB rules keep recordings of children out of public datasets.'],
         links=[('Joint engagement project', 'joint-engagement')]),
    dict(when='Feb 2025 – Jul 2025', title='Machine Learning Researcher', org='4DiVISION', loc='Seoul, South Korea',
         bullets=['Built the vision pipeline for an automated robotic bolt fastening cell, covering bolt detection, instance segmentation, RGB and point cloud registration, 6-DoF pose estimation and ROS2 nodes that stream target poses to the manipulator.',
                  'Held pose accuracy within 1 mm in factory cells the model had not seen during training.',
                  'Developed automated switch-position verification on Tesseravue, the company inspection product, designed to cut manual QA time by about 70%.'],
         links=[('Bolt fastening project', 'bolt-fastening')]),
    dict(when='Mar 2023 – Feb 2025', title='Graduate Research Assistant', org='KOREATECH, Computer Vision and Video Processing Lab', loc='Cheonan, South Korea',
         bullets=['Developed PrecisionGAN, an image-to-image translation GAN that skeletonizes historical Korean and Chinese printed characters while preserving stroke structure. Published as first author in Springer IJDAR.',
                  'Developed camera-based pose estimation that aligns two cylinders for automated insertion on a film roll handling rig.',
                  'Worked on a National Museum of Korea funded project that uses image similarity measures to analyze Joseon-era movable metal type and printing methods.'],
         links=[('PrecisionGAN', 'precisiongan'), ('Film roll alignment', 'film-roll'), ('Metal type analysis', 'metal-type')]),
    dict(when='Jan 2022 – Mar 2023', title='AI Project Manager', org='Bleed AI', loc='Remote, United States',
         bullets=['Led a team of five engineers across more than 10 client computer vision projects, owning scope, budgets, staffing and delivery, and built and trained models hands-on.',
                  'For Veeve (smart shopping carts), implemented real-time action recognition on cart camera streams to detect items being added or removed, deployed on Google Coral Edge TPUs.',
                  'Contributed to camera-based sports and fitness analytics and a hand-tracking therapy app for patients with a rare form of hand arthritis.'],
         links=[('Smart cart project', 'smart-cart'), ('FitX', 'fitx')]),
    dict(when='Aug 2021 – Feb 2022', title='Machine Learning Engineer', org='Liquid Technologies', loc='Karachi, Pakistan',
         bullets=['Core developer of Vidan.ai, a real-time video analytics platform for industrial and security monitoring.',
                  'Designed the platform architecture and built the automatic license plate recognition and train monitoring modules, along with dashboards for live views, counts and alerts.',
                  'Optimized and deployed production vision models on single-board computers.'],
         links=[('Vidan.ai project', 'vidan')]),
    dict(when='Jan 2020 – Aug 2021', title='Embedded Systems Engineer', org='Sudoware', loc='Karachi, Pakistan',
         bullets=['Led development of a wireless sensor network for hydroponic farms using Raspberry Pi and NodeMCU nodes over MQTT, BLE and HTTP, with remote camera streaming.',
                  'Built IoT applications for industrial clients on ESP32, Arduino, Raspberry Pi, OpenWRT and Jetson Nano.'],
         links=[]),
]

EDUCATION = [
    ('Mar 2023 – Feb 2025', 'Master of Science (M.S.) in Future Convergence Engineering, Computer Vision', 'Korea University of Technology and Education (KOREATECH), Cheonan, South Korea', 'GPA 4.25 / 4.5. Thesis: PrecisionGAN, enhanced image-to-image translation for preserving structural integrity in skeletonized images.'),
    ('Sep 2017 – Jun 2021', 'Bachelor of Engineering (B.E.) in Electrical Engineering', 'DHA Suffa University, Karachi, Pakistan', 'GPA 3.5 / 4.0.'),
]

SKILLS = [
    ('Programming', 'Python, C++, C, MATLAB, Bash'),
    ('Deep learning', 'PyTorch, TensorFlow, Keras, CNN and transformer architectures, vision-language models (VLMs), multimodal learning, generative models (GANs, generative AI)'),
    ('Computer vision', 'OpenCV, YOLO, Detectron2, MMPose, OpenPose, object detection, instance segmentation, human pose estimation, 6-DoF object pose estimation, depth estimation, gaze estimation, multi-object tracking, video action recognition'),
    ('3D and robotics', 'ROS2 (ROS), Open3D, PCL, camera calibration, sensor fusion, LiDAR, RGB-D and point cloud registration, 3D reconstruction, robot manipulator integration'),
    ('Deployment and MLOps', 'TensorRT, ONNX, CUDA, NVIDIA Jetson, Google Coral Edge TPU, Raspberry Pi, ESP32, Docker, FastAPI, AWS, GCP, Git, Linux'),
    ('Languages', 'English (fluent, IELTS 8.0), Urdu and Hindi (native), Korean (basic)'),
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

def page(title, desc, pre, body, og='home', path=''):
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
<link rel="canonical" href="https://maaz9898.github.io/{path}">
<meta property="og:type" content="website">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="https://maaz9898.github.io/{path}">
<meta property="og:image" content="https://maaz9898.github.io/assets/og/{og}.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"Person","name":"Maaz Ahmed","jobTitle":"Machine Learning Engineer and Researcher","email":"mailto:maaz9898@gmail.com","url":"https://maaz9898.github.io/","address":{{"@type":"PostalAddress","addressLocality":"Doha","addressCountry":"QA"}},"alumniOf":["Korea University of Technology and Education","DHA Suffa University"],"knowsAbout":["Computer vision","Deep learning","6-DoF pose estimation","3D perception","Robotics","ROS2","PyTorch","Video understanding"],"sameAs":["https://github.com/maaz9898","https://www.linkedin.com/in/maazahmed98","https://scholar.google.com/citations?user=TZpghL4AAAAJ"]}}</script>
</head>
<body>
<a class="skip" href="#content">Skip to content</a>
<header class="top">
  <div class="wrap bar">
    <a class="brand" href="{pre}index.html">Maaz Ahmed</a>
    <nav aria-label="Main">
      <a href="{pre}index.html#work">Projects</a>
      <a href="{pre}index.html#experience">Experience</a>
      <a href="{pre}index.html#skills">Skills</a>
      <a href="{pre}index.html#publications">Publications</a>
      <a href="{pre}index.html#contact">Contact</a>
    </nav>
    <button class="icon" id="theme" type="button" aria-label="Switch between dark and light mode" title="Switch theme">{icon('moon', 'moon')}{icon('sun', 'sun')}</button>
  </div>
</header>
<main id="content" class="wrap">
{body}
</main>
<footer class="wrap foot">
  <span>Maaz Ahmed, Doha, Qatar. Some project visuals are illustrative.</span>
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
      <li class="card{" wide" if i < 2 else ""}">
        {p["card"]}
        <a class="body" href="projects/{p["slug"]}.html">
          <h3>{p["title"]}</h3>
          <p>{p["line"]}</p>
          {tags(p["tags"][:3])}
          <span class="more">View project</span>
        </a>
      </li>'''
    pubs = ''
    for t, url, venue, first in PUBS:
        tt = f'<a class="t" href="{url}">{t}</a>' if url else f'<span class="t">{t}</span>'
        pubs += f'<li>{tt}<span class="v">{venue}. {"<span class=\"me\">First author</span>" if first else "Second author"}</span></li>'
    exp = ''
    for e in EXPERIENCE:
        bl = ''.join(f'<li>{b}</li>' for b in e['bullets'])
        ln = ''.join(f'<a href="projects/{slug}.html">{t}</a>' for t, slug in e['links'])
        exp += f'''
      <article class="job">
        <p class="when">{e['when']}</p>
        <div>
          <h3>{e['title']}</h3>
          <p class="at">{e['org']}, {e['loc']}</p>
          <ul>{bl}</ul>
          {f'<p class="links small">{ln}</p>' if ln else ''}
        </div>
      </article>'''
    edu = ''.join(f'<article class="job"><p class="when">{w}</p><div><h3>{d}</h3><p class="at">{o}</p><p class="plain">{n}</p></div></article>' for w, d, o, n in EDUCATION)
    skills = ''.join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in SKILLS)
    body = f'''
  <section class="intro">
    <img class="portrait" src="assets/maaz.webp" alt="Portrait of Maaz Ahmed" width="148" height="148">
    <div>
      <h1>Maaz Ahmed</h1>
      <p class="role">Machine Learning Engineer and Researcher. I build computer vision systems for robotics, 3D perception and human behaviour analysis.</p>
      <p class="links"><a class="btn" href="mailto:maaz9898@gmail.com">Email me</a><a href="https://github.com/maaz9898">GitHub</a><a href="https://scholar.google.com/citations?user=TZpghL4AAAAJ">Google Scholar</a><a href="https://www.linkedin.com/in/maazahmed98">LinkedIn</a></p>
    </div>
  </section>

  <div class="herowrap">
    {compare('hero_photo.webp', 'hero_cloud.webp', 'A robot arm with a camera over a steel part. Drag to reveal the depth map of the same scene', '', '1600 / 672')}
    <p class="hint">Drag the line to switch between the camera view and the depth map.</p>
  </div>

  <section id="work">
    <h2>Projects</h2>
    <ul class="cards">{cards}
    </ul>
  </section>

  <section id="experience">
    <h2>Experience</h2>
    {exp}
  </section>

  <section id="education">
    <h2>Education</h2>
    {edu}
  </section>

  <section id="skills">
    <h2>Technical Skills</h2>
    <dl class="skills">{skills}</dl>
  </section>

  <section id="publications">
    <h2>Publications</h2>
    <ul class="pubs">{pubs}</ul>
  </section>

  <section id="contact">
    <h2>Contact</h2>
    <p class="links"><a href="mailto:maaz9898@gmail.com">maaz9898@gmail.com</a><a href="https://www.linkedin.com/in/maazahmed98">LinkedIn</a><a href="https://github.com/maaz9898">GitHub</a><a href="https://scholar.google.com/citations?user=TZpghL4AAAAJ">Google Scholar</a></p>
  </section>
'''
    open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf8').write(
        page('Maaz Ahmed | Computer Vision and Robotics', 'Maaz Ahmed is a machine learning engineer and researcher in computer vision, 3D perception and robotics. Projects, publications and contact.', '', body))

def build_projects():
    ps = projects('../')
    os.makedirs(os.path.join(ROOT, 'projects'), exist_ok=True)
    for i, p in enumerate(ps):
        prev, nxt = ps[i - 1], ps[(i + 1) % len(ps)]
        facts = ''.join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in p['facts'])
        links = ''.join(f'<a class="btn ghost" href="{u}">{t}</a>' for t, u in p.get('links', []))
        body = f'''
  <article class="project">
    <a class="back" href="../index.html#work">All projects</a>
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
            page(p['title'] + ' | Maaz Ahmed', p['line'], '../', body, p['slug'], 'projects/' + p['slug'] + '.html'))

if __name__ == '__main__':
    build_home(); build_projects(); print('built', 1 + len(projects('')), 'pages')
