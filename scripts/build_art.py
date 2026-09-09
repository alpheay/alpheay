#!/usr/bin/env python3
"""Rebuild the profile's self-contained SVG artwork using only Python's stdlib."""

from html import escape
from math import cos, pi, sin
from pathlib import Path
import random

ROOT = Path(__file__).resolve().parents[1]
WHITE = "#f4f3ef"
GRAY = "#aaa9a6"
FONT = "Arial, Helvetica, sans-serif"
MONO = "'SFMono-Regular', Consolas, 'Liberation Mono', monospace"


def text(x, y, value, size=24, color=WHITE, weight=400, extra=""):
    return (f'<text x="{x}" y="{y}" fill="{color}" font-family="{FONT}" '
            f'font-size="{size}" font-weight="{weight}" {extra}>{escape(value)}</text>')


def label(x, y, value, size=14, color=GRAY):
    return (f'<text x="{x}" y="{y}" fill="{color}" font-family="{MONO}" '
            f'font-size="{size}" letter-spacing="2">{escape(value)}</text>')


def line(x1, y1, x2, y2, color="#303030", width=1, extra=""):
    return (f'<path d="M{x1} {y1}L{x2} {y2}" stroke="{color}" '
            f'stroke-width="{width}" {extra}/>')


def circle(x, y, r, fill=WHITE, extra=""):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" {extra}/>'


def path(points, stroke=WHITE, width=1, opacity=1, close=False):
    d = "M" + "L".join(f"{x:.2f} {y:.2f}" for x, y in points)
    return (f'<path d="{d}{"Z" if close else ""}" fill="none" stroke="{stroke}" '
            f'stroke-width="{width}" opacity="{opacity:.3f}"/>')


def arrow(x, y, size=20):
    return (f'<path d="M{x} {y+size}l{size} -{size}m-{size} 0h{size}v{size}" '
            f'fill="none" stroke="{WHITE}" stroke-width="2"/>')


def svg(filename, width, height, title, description, content):
    destination = ROOT / "assets" / filename
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="none" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title>
<desc id="desc">{escape(description)}</desc>
<defs>
  <radialGradient id="halo"><stop stop-color="#2b2b2b"/><stop offset="1" stop-color="#080808" stop-opacity="0"/></radialGradient>
  <linearGradient id="metal" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#797979"/><stop offset=".22" stop-color="#ecebe7"/><stop offset=".5" stop-color="#555"/><stop offset="1" stop-color="#161616"/></linearGradient>
  <linearGradient id="panel" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#202020"/><stop offset="1" stop-color="#0b0b0b"/></linearGradient>
  <clipPath id="canvas"><rect width="{width}" height="{height}" rx="16"/></clipPath>
</defs>
<g clip-path="url(#canvas)">
<rect width="{width}" height="{height}" fill="#080808"/>
{content}
</g>
<rect x=".5" y=".5" width="{width-1}" height="{height-1}" rx="15.5" stroke="#282828"/>
</svg>
''')


def torus(cx, cy, scale=1):
    """A tilted, depth-sorted torus drawn as fine metallic contour lines."""
    rings = []
    for i in range(88):
        u = 2 * pi * i / 88
        points = []
        depths = []
        for j in range(97):
            v = 2 * pi * j / 96
            radius = 130 + 53 * cos(v)
            x, y, z = radius * cos(u), radius * sin(u), 53 * sin(v)
            y, z = y * cos(.93) - z * sin(.93), y * sin(.93) + z * cos(.93)
            x, y = x * cos(-.55) - y * sin(-.55), x * sin(-.55) + y * cos(-.55)
            points.append((cx + x * scale, cy + y * scale))
            depths.append(z)
        depth = sum(depths) / len(depths)
        rings.append((depth, path(points, WHITE, .85 * scale, .18 + .64 * (depth + 145) / 290)))
    return circle(cx, cy, 270 * scale, "url(#halo)") + "".join(p for _, p in sorted(rings))


def stars(w, h, seed=8):
    rng = random.Random(seed)
    return "".join(circle(round(rng.uniform(24, w-24), 1), round(rng.uniform(24, h-24), 1),
                          rng.choice([.6, .8, 1]), "#777", 'opacity=".4"') for _ in range(55))


def header(mobile=False):
    w, h = (640, 800) if mobile else (1200, 540)
    content = stars(w, h)
    content += label(40 if mobile else 56, 48, "NN / ALPHEAY", 17 if mobile else 14)
    content += label(w-195, 48, "RESEARCH + CODE", 13)
    content += line(40 if mobile else 56, 72, w-40 if mobile else w-56, 72)
    if mobile:
        content += torus(425, 444, 1.08)
        content += text(38, 197, "Nik Nandi", 91, weight=600, extra='letter-spacing="-6"')
        content += text(42, 244, "Machine learning researcher", 26, GRAY)
        content += text(42, 660, "Hey, welcome", 54, weight=400, extra='letter-spacing="-2"')
        content += text(42, 718, "to my GitHub.", 54, weight=400, extra='letter-spacing="-2"')
        content += label(43, 767, "AI / PYTHON / WEB APPS", 15)
        content += label(42, 383, "HELLO", 14) + line(43, 400, 135, 400)
        content += label(42, 432, ":)", 18)
    else:
        content += torus(936, 274, 1.17)
        content += circle(936, 274, 242, "none", 'stroke="#272727" stroke-dasharray="2 9"')
        content += text(51, 232, "Nik Nandi", 112, weight=600, extra='letter-spacing="-7"')
        content += text(56, 284, "Machine learning researcher", 26, GRAY)
        content += text(56, 367, "Hey, welcome to my GitHub.", 40, extra='letter-spacing="-1.4"')
        content += label(57, 406, "AI / PYTHON / WEB APPS", 14)
        content += line(56, 465, 1144, 465)
        content += circle(62, 501, 4, WHITE)
        content += label(78, 506, "OPEN TO WORK", 13)
        content += label(949, 506, "@ALPHEAY", 13)
    svg("mobile/header.svg" if mobile else "header.svg", w, h, "Nik Nandi — welcome to my GitHub.",
        "Machine learning researcher. AI, Python, and web apps. Open to work.", content)


def mission(mobile=False):
    w, h = (640, 362) if mobile else (1200, 224)
    c = label(40 if mobile else 48, 47, "ABOUT ME", 16 if mobile else 14)
    if mobile:
        c += text(40, 111, "I work on AI", 43, extra='letter-spacing="-1.5"')
        c += text(40, 164, "and software.", 43, extra='letter-spacing="-1.5"')
        c += line(40, 197, 600, 197)
        c += text(40, 243, "Mostly ML models, AI agents,", 25, GRAY)
        c += text(40, 280, "and web apps. I also like trying", 25, GRAY)
        c += text(40, 317, "out WebGL and Rust.", 25, GRAY)
    else:
        c += text(48, 110, "I work on AI", 40, extra='letter-spacing="-1.3"')
        c += text(48, 160, "and software.", 40, extra='letter-spacing="-1.3"')
        c += line(571, 48, 571, 176)
        c += text(626, 96, "Mostly ML models, AI agents,", 25, GRAY)
        c += text(626, 132, "and web apps. I also like trying", 25, GRAY)
        c += text(626, 168, "out WebGL and Rust.", 25, GRAY)
    svg("mobile/hero_animation.svg" if mobile else "hero_animation.svg", w, h,
        "I work on AI and software.", "Mostly ML models, AI agents, and web apps. I also like trying out WebGL and Rust.", c)


def document_art():
    c = circle(0, 0, 240, "url(#halo)")
    for i in range(4):
        x, y = -108+i*27, -126+i*16
        c += f'<g transform="translate({x} {y}) skewY(-12)">'
        c += '<rect width="166" height="207" rx="5" fill="url(#panel)" stroke="#747474"/>'
        c += line(22, 28, 97, 28, "#ddd", 3)
        c += line(22, 45, 67, 45, "#555", 2)
        for j in range(4):
            c += line(22, 68+j*12, 142 if j % 2 == 0 else 119, 68+j*12, "#555", 2)
        for j, height in enumerate([17, 29, 22, 45, 60, 53]):
            c += f'<rect x="{22+j*20}" y="{180-height}" width="11" height="{height}" fill="url(#metal)"/>'
        c += '</g>'
    return c


def routing_art():
    c = circle(0, 0, 230, "url(#halo)")
    for y in [-95, 0, 95]:
        c += f'<path d="M-140 0H-75Q-50 0 -50 {y/2}V{y}H50" stroke="#888" stroke-width="1.4"/>'
        c += f'<rect x="40" y="{y-25}" width="119" height="50" rx="7" fill="url(#panel)" stroke="#6c6c6c"/>'
        c += label(58, y+6, { -95: "GET", 0: "POST", 95: "PATCH"}[y], 15, WHITE)
        c += circle(145, y, 3, WHITE)
    c += '<rect x="-178" y="-35" width="70" height="70" rx="12" fill="url(#panel)" stroke="#aaa"/>'
    c += text(-162, 9, "{ }", 26)
    return c


def intelligence_art():
    c = circle(0, 0, 235, "url(#halo)")
    for i in range(48):
        angle = i*pi/48
        points = []
        for j in range(101):
            t = 2*pi*j/100
            x, y = 163*cos(t), 38*sin(t)
            points.append((x*cos(angle)-y*sin(angle), (x*sin(angle)+y*cos(angle))*.81))
        c += path(points, WHITE, .7, .22 + .5*abs(sin(angle)))
    c += circle(0, 0, 9, WHITE) + circle(0, 0, 17, "none", 'stroke="#fff" stroke-opacity=".3"')
    return c


def health_art():
    c = circle(0, 0, 225, "url(#halo)")
    for i in range(19):
        points = []
        for j in range(111):
            x = -220+4*j
            envelope = max(0, 1-(x/225)**2)
            y = (i-9)*8 + sin(x/39+i*.13)*28*envelope
            points.append((x, y))
        c += path(points, WHITE, .8, .16+.23*sin(i*pi/18))
    c += '<rect x="-32" y="-138" width="64" height="276" rx="30" fill="#111" stroke="#777"/>'
    c += '<rect x="-57" y="-71" width="114" height="142" rx="35" fill="url(#metal)"/>'
    c += '<rect x="-51" y="-65" width="102" height="130" rx="29" fill="#0b0b0b" stroke="#555"/>'
    c += path([(-34, 2), (-21, 2), (-13, -10), (-3, 21), (8, -24), (18, 2), (34, 2)], WHITE, 2)
    c += circle(0, 40, 3, "#bbb")
    return c


def terminal_art():
    c = circle(0, 0, 230, "url(#halo)")
    for i in range(3, -1, -1):
        c += f'<rect x="{-167+i*12}" y="{-100-i*12}" width="310" height="208" rx="10" fill="url(#panel)" stroke="{["#999", "#505050", "#383838", "#282828"][i]}"/>'
    c += line(-167, -58, 143, -58, "#444")
    for x in [-146, -132, -118]:
        c += circle(x, -79, 3, "#888")
    c += label(-144, -17, "> glycerin", 16, WHITE)
    c += line(-142, 12, 73, 12, "#737373", 3)
    c += line(-142, 31, 43, 31, "#4e4e4e", 3)
    c += line(-142, 50, 95, 50, "#4e4e4e", 3)
    c += text(-144, 87, ">", 19, WHITE)
    c += '<rect x="-120" y="72" width="10" height="17" fill="#ddd"/>'
    return c


def archive_art():
    c = circle(0, 0, 230, "url(#halo)")
    for i in range(5):
        y = 75-i*39
        c += f'<path d="M-163 {y}L0 {y-69}L163 {y}L0 {y+69}Z" fill="url(#panel)" stroke="{["#333", "#444", "#666", "#999", "#ddd"][i]}"/>'
        for j in [-.5, 0, .5]:
            c += line(-81+j*81, y-34-j*34, 81+j*81, y+34-j*34, "#3d3d3d")
            c += line(-81+j*81, y+34+j*34, 81+j*81, y-34+j*34, "#3d3d3d")
    return c


PROJECTS = [
    ("ipo_mine", "IPO-Mine", "RESEARCH / IPO DOCUMENTS", ["A dataset and tools for analyzing", "text and images in IPO documents."], "PYTHON / PYTORCH / DOCKER", document_art),
    ("jec", "JEC", "OPEN SOURCE / DEVELOPER TOOLS", ["A FastAPI framework that lets you", "organize your routes using classes."], "PYTHON / FASTAPI / DOCKER", routing_art),
    ("hyperbleed", "HyperBleed", "APP / AI ASSISTANT", ["An AI assistant that can plan tasks", "and use tools to help get them done."], "REACT / TYPESCRIPT / PYTHON", intelligence_art),
    ("vene", "Vene", "APP / CAREGIVING", ["Uses wearables to detect distress", "and offer support in the moment."], "SWIFT / PYTHON / TENSORFLOW", health_art),
    ("glycerin", "Glycerin", "OPEN SOURCE / CLI", ["Chat with AI from your terminal.", "Bring your own API keys."], "TYPESCRIPT / NODE.JS / SHELL", terminal_art),
    ("portfolio", "Other projects", "MORE / PROJECTS", ["More of my research, experiments,", "and other things I've worked on."], "RESEARCH / WEBGL / SYSTEMS", archive_art),
]


def project(index, data, mobile=False):
    slug, title, category, copy, stack, art = data
    w, h = (640, 606) if mobile else (1200, 348)
    if mobile:
        c = f'<g transform="translate(320 163) scale(.94)">{art()}</g>'
        c += line(36, 316, 604, 316)
        c += label(36, 357, f"{index:02d} / {category.split(' / ')[0]}", 16)
        c += text(34, 423, title, 56, weight=500, extra='letter-spacing="-2"')
        c += arrow(574, 382, 25)
        for j, value in enumerate(copy):
            c += text(36, 471+j*35, value, 26, GRAY)
        c += label(36, 565, stack, 15)
    else:
        c = label(44, 43, f"{index:02d} / {category}", 13)
        c += text(41, 124, title, 60, weight=500, extra='letter-spacing="-2.5"')
        for j, value in enumerate(copy):
            c += text(44, 180+j*34, value, 25, GRAY)
        c += label(44, 297, stack, 13)
        c += line(633, 36, 633, 312, "#242424")
        c += f'<g transform="translate(918 174)">{art()}</g>'
        c += arrow(1139, 38, 18)
    svg(f"featured/{'mobile/' if mobile else ''}{slug}.svg", w, h, title,
        category + ". " + " ".join(copy) + " " + stack + ".", c)


def stack(mobile=False):
    groups = [
        ("01 / MACHINE LEARNING", ["Python · PyTorch · TensorFlow", "AI agents · ML research"]),
        ("02 / FRONTEND", ["TypeScript · React · Next.js", "WebGL · Three.js · Swift"]),
        ("03 / BACKEND", ["Node.js · FastAPI · PostgreSQL", "Rust · Go · Redis"]),
        ("04 / INFRASTRUCTURE", ["Docker · Kubernetes · GitHub", "AWS · GCP · Vercel"]),
    ]
    w, h = (640, 694) if mobile else (1200, 348)
    c = ""
    for i, (name, values) in enumerate(groups):
        x = 40 if mobile else 44+(i % 2)*600
        y = 48+i*169 if mobile else 45+(i // 2)*174
        c += label(x, y, name, 17 if mobile else 14)
        c += text(x, y+48, values[0], 26 if mobile else 24)
        c += text(x, y+83, values[1], 24 if mobile else 22, GRAY)
        if mobile and i < 3:
            c += line(40, y+123, 600, y+123)
    if not mobile:
        c += line(600, 35, 600, 313) + line(44, 174, 1156, 174)
    svg("mobile/stack.svg" if mobile else "stack.svg", w, h, "Tech stack",
        ". ".join(name.split(" / ")[1] + ": " + ", ".join(values) for name, values in groups), c)


def connect(mobile=False):
    w, h = (640, 380) if mobile else (1200, 300)
    c = stars(w, h, 12)
    c += label(40 if mobile else 48, 49, "CONTACT", 16 if mobile else 14)
    c += text(38 if mobile else 44, 124 if mobile else 130, "Want to work", 66 if mobile else 62, extra='letter-spacing="-2.5"')
    c += text(38 if mobile else 44, 195 if mobile else 201, "on something?", 43 if mobile else 62, extra='letter-spacing="-2"')
    c += text(40 if mobile else 48, 258, "Have a project or a role in mind? Email me.", 24, GRAY)
    if mobile:
        c += line(40, 294, 600, 294) + text(40, 343, "Email me", 25) + arrow(568, 321, 24)
    else:
        c += circle(1058, 150, 66, "url(#panel)", 'stroke="#5c5c5c"') + arrow(1035, 127, 46)
    svg("mobile/connect_animation.svg" if mobile else "connect_animation.svg", w, h,
        "Want to work on something?", "Have a project or a role in mind? Email Nik Nandi.", c)


def footer(mobile=False):
    w, h = (640, 104) if mobile else (1200, 104)
    c = label(36 if mobile else 44, 59, "NN / ALPHEAY", 18 if mobile else 14, WHITE)
    c += text(w-254 if mobile else w-235, 60, "Thanks for visiting.", 24 if mobile else 21, GRAY)
    svg("mobile/footer.svg" if mobile else "footer.svg", w, h, "Nik Nandi / alpheay", "Thanks for visiting.", c)


def main():
    for mobile in (False, True):
        header(mobile)
        mission(mobile)
        for index, data in enumerate(PROJECTS, 1):
            project(index, data, mobile)
        stack(mobile)
        connect(mobile)
        footer(mobile)
    print("Rebuilt 22 profile illustrations.")


if __name__ == "__main__":
    main()
