"""Build the dark profile panels, looping GIFs, and linked button images.

Requires Pillow, Playwright, and Chrome (or Playwright Chromium):
    python -m pip install pillow playwright
    python scripts/render-profile-assets.py

All professional content stays visible throughout the animation. The README
selects a static SVG for reduced motion, and links to PROFILE.md for plain text.
"""

from html import escape
import io
import os
from pathlib import Path
import shutil

from PIL import Image
from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
CHROME = Path(os.environ.get("PROGRAMFILES", "C:/Program Files")) / (
    "Google/Chrome/Application/chrome.exe"
)
BG, CARD, LINE = "#111821", "#19232e", "#2c3c4b"
WHITE, MUTED, ACCENT = "#f2f5f8", "#b1bdc9", "#88cec9"
FONT = "Bahnschrift, 'Trebuchet MS', Arial, sans-serif"
MONO = "Consolas, 'Liberation Mono', monospace"
PROJECTS = (
    ("Catalejo Travel", "Travel catalog, seasonal rates & CMS"),
    ("Quinta Pata", "Enrollment, Excel imports & QR IDs"),
    ("Inspira Ingeniería", "Corporate site & secure admin panel"),
    ("Madryn Buceo", "Website, reservations & management"),
)
STACK = (
    ("Web", "React, Next.js, TypeScript"),
    ("Backend & data", "Laravel, PHP, PostgreSQL, MySQL"),
    ("Mobile", "React Native, Expo, Flutter"),
    ("Delivery", "Linux / VPS, Docker, CI/CD, Git, AWS"),
)


def text(x, y, value, size=22, color=WHITE, weight=400, extra=""):
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" '
            f'font-weight="{weight}" {extra}>{escape(value)}</text>')


def rect(x, y, width, height, fill=CARD, radius=10):
    return (f'<rect x="{x}" y="{y}" width="{width}" height="{height}" '
            f'rx="{radius}" fill="{fill}"/>')


def rule(x, y, width):
    return f'<path d="M{x} {y}h{width}" fill="none" stroke="{LINE}"/>'


def orbit(cx, cy, radius):
    return (f'<circle cx="{cx}" cy="{cy}" r="{radius}" fill="none" '
            f'stroke="{LINE}" stroke-width="2"/>'
            f'<g id="orbit" data-cx="{cx}" data-cy="{cy}">'
            f'<path d="M{cx} {cy-radius} A{radius} {radius} 0 0 1 '
            f'{cx+radius} {cy}" fill="none" stroke="{ACCENT}" '
            f'stroke-width="3" stroke-linecap="round"/>'
            f'<circle cx="{cx}" cy="{cy-radius}" r="5" fill="{ACCENT}"/></g>')


def panel(mobile=False):
    width, height = (640, 1560) if mobile else (1000, 1080)
    margin = 30 if mobile else 42
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" '
             f'height="{height}" viewBox="0 0 {width} {height}" role="img" '
             f'aria-labelledby="title desc" font-family="{FONT}">',
             '<title id="title">Máximo Ozonas — Development Lead and Full Stack Developer</title>',
             '<desc id="desc">Business software, technical leadership, Gili and Food Partners '
             'Patagonia experience, four Xenova projects, web and mobile tools, UTN '
             'education, Spanish native and English B1. Full text is available in PROFILE.md.</desc>',
             rect(0, 0, width, height, BG, 14),
             rect(0, 0, width, 262 if not mobile else 252, "#17212b", 14),
             text(margin, 36, "maxiozonas / software + systems", 17, MUTED,
                  extra=f'font-family="{MONO}"'),
             text(margin-2, 110 if mobile else 119, "Máximo Ozonas", 57 if mobile else 66, weight=600),
             text(margin, 151 if mobile else 161, "Development Lead / Full Stack Developer", 25 if mobile else 24),
             text(margin, 199 if mobile else 213, "> building business software", 24, ACCENT,
                  extra=f'id="typed" font-family="{MONO}"'),
             f'<rect id="cursor" x="{margin+405}" y="{181 if mobile else 195}" '
             f'width="11" height="24" fill="{ACCENT}"/>',
             text(margin, 233 if mobile else 246, "Bahía Blanca, Argentina", 19, MUTED),
             orbit(560 if mobile else 845, 208 if mobile else 142, 29 if mobile else 66),
             rule(margin, 252 if mobile else 262, width-margin*2),
             text(margin, 294 if mobile else 315, "Experience", 28, weight=600)]
    if not mobile:
        parts += [text(692, 315, "Requirements → production", 18, MUTED),
                  text(795, 155, "M/O", 42, ACCENT, 600),
                  text(761, 235, "build. ship. maintain.", 15, MUTED,
                       extra=f'font-family="{MONO}"')]
        for y in (336, 482):
            parts += [rect(42, y, 916, 132),
                      f'<rect x="42" y="{y+26}" width="3" height="80" rx="1.5" fill="{ACCENT}"/>']
        parts += [text(66, 374, "Gili / Giliycia SRL", 25, weight=600),
                  text(759, 374, "Oct 2025–present", 17, MUTED),
                  text(66, 410, "Development Lead · Architecture, roadmap & delivery.", 22),
                  text(66, 444, "Picking, logistics, B2B & automation. Flexxus + Magento.", 21, MUTED),
                  text(66, 520, "Food Partners Patagonia", 25, weight=600),
                  text(758, 520, "Sep 2025–present", 17, MUTED),
                  text(66, 554, "Full Stack Developer · Xenova / Laravel + React + TypeScript", 21),
                  text(66, 587, "ERP: production, quality, stock, traceability, exports, HR & employee PWA.", 21, MUTED),
                  text(42, 666, "Selected projects", 28, weight=600),
                  text(551, 666, "Toolkit", 28, weight=600),
                  text(42, 694, "Freelance through Xenova / 2025–present", 17, MUTED),
                  f'<path d="M514 650V952" stroke="{LINE}"/>']
        for index, ((name, description), (area, tools)) in enumerate(zip(PROJECTS, STACK)):
            y = 737 + index*65
            parts += [text(42, y, name, 23, weight=500),
                      text(42, y+28, description, 20, MUTED),
                      text(551, y, area, 22, ACCENT, 500),
                      text(551, y+28, tools, 20, MUTED)]
        parts += [rule(42, 974, 916),
                  text(42, 1010, "UTN · University Technical Degree in Programming / 2021–2024", 21),
                  text(42, 1043, "Spanish: native / English: B1", 19, MUTED),
                  text(610, 1043, "Claude Code / Codex / OpenCode", 18, MUTED)]
    else:
        parts += [rect(24, 315, 592, 177),
                  text(44, 354, "Gili / Giliycia SRL", 29, weight=600),
                  text(44, 385, "Oct 2025–present", 21, MUTED),
                  text(44, 420, "Development Lead", 27, ACCENT),
                  text(44, 454, "Picking, logistics, B2B & automation.", 27, MUTED),
                  text(44, 483, "Flexxus + Magento integrations.", 27, MUTED),
                  rect(24, 507, 592, 207),
                  text(44, 549, "Food Partners Patagonia", 29, weight=600),
                  text(44, 580, "Sep 2025–present", 21, MUTED),
                  text(44, 615, "Full Stack Developer / Xenova", 27, ACCENT),
                  text(44, 650, "ERP: production, quality & traceability.", 27, MUTED),
                  text(44, 680, "Stock, exports, HR & employee PWA.", 27, MUTED),
                  text(30, 760, "Selected projects", 29, weight=600),
                  text(30, 790, "Freelance through Xenova / 2025–present", 21, MUTED)]
        for index, (name, description) in enumerate(PROJECTS):
            y = 834 + index*66
            parts += [text(30, y, name, 28, weight=500),
                      text(30, y+31, description, 27, MUTED)]
        parts += [rule(30, 1090, 580), text(30, 1134, "Toolkit", 29, weight=600)]
        for index, (area, tools) in enumerate(STACK):
            y = 1178 + index*63
            parts += [text(30, y, area, 26, ACCENT, 500),
                      text(30, y+29, tools, 25, MUTED)]
        parts += [rule(30, 1430, 580),
                  text(30, 1470, "University Technical Degree in Programming", 25),
                  text(30, 1503, "UTN / 2021–2024", 24, MUTED),
                  text(30, 1538, "Spanish: native / English: B1", 24, MUTED)]
    parts += [f'<path id="flow" d="M{margin} {height-3}H{width-margin}" stroke="{ACCENT}" '
              'stroke-width="3" fill="none" stroke-dasharray="100 1800"/>', '</svg>']
    return "\n".join(parts), width, height


def save_buttons():
    for name, label in (("portfolio", "Portfolio"), ("linkedin", "LinkedIn"),
                        ("email", "Email me"), ("cv", "CV / PDF")):
        body = [f'<svg xmlns="http://www.w3.org/2000/svg" width="180" height="48" '
                f'viewBox="0 0 180 48" font-family="{FONT}" role="img">',
                f'<title>{label}</title>', rect(0, 0, 180, 48, CARD, 8),
                text(90, 31, label, 22, ACCENT, 500, 'text-anchor="middle"'), '</svg>']
        (ASSETS / f'link-{name}.svg').write_text("\n".join(body), encoding="utf-8")


def render_panel(browser, name, mobile):
    source, width, height = panel(mobile)
    path = ASSETS / f'{name}.svg'
    path.write_text(source, encoding="utf-8")
    page = browser.new_page(viewport={"width": width, "height": height})
    try:
        page.goto(path.as_uri())
        page.evaluate("document.fonts.ready")
        outside = page.evaluate("""() => {
            const root = document.querySelector('svg');
            return [...root.querySelectorAll('text')].filter(text => {
                const b = text.getBBox();
                return b.x < 0 || b.y < 0 || b.x + b.width > root.width.baseVal.value
                    || b.y + b.height > root.height.baseVal.value;
            }).map(text => text.textContent);
        }""")
        if outside:
            raise ValueError(f"Text outside {name}: {outside}")
        page.evaluate("""() => {
            const typed = document.getElementById('typed');
            const cursor = document.getElementById('cursor');
            const orbit = document.getElementById('orbit');
            const flow = document.getElementById('flow');
            const phrases = ['building business software', 'leading technical delivery', 'shipping web & mobile apps'];
            window.animateProfile = frame => {
                const segment = Math.floor(frame / 24);
                const local = frame % 24;
                const phrase = phrases[segment];
                let count = phrase.length;
                if(local < 10) count = Math.round(phrase.length * (local + 1) / 10);
                if(local > 19) count = Math.round(phrase.length * (24 - local) / 5);
                typed.textContent = '> ' + phrase.slice(0, count);
                const bounds = typed.getBBox();
                cursor.setAttribute('x', bounds.x + bounds.width + 8);
                cursor.setAttribute('opacity', local % 6 < 4 ? 1 : 0);
                orbit.setAttribute('transform', `rotate(${frame*5} ${orbit.dataset.cx} ${orbit.dataset.cy})`);
                flow.setAttribute('stroke-dashoffset', -frame*16);
            };
        }""")
        svg = page.locator('svg')
        frames = []
        palette = None
        for frame in range(72):
            page.evaluate('frame => window.animateProfile(frame)', frame)
            rgba = Image.open(io.BytesIO(svg.screenshot(omit_background=True))).convert('RGBA')
            bitmap = Image.new('RGB', rgba.size, BG)
            bitmap.paste(rgba, mask=rgba.getchannel('A'))
            if palette is None:
                palette = bitmap.quantize(colors=240)
            indexed = bitmap.quantize(palette=palette, dither=Image.Dither.NONE)
            indexed.paste(255, mask=rgba.getchannel('A').point(lambda alpha: 255 if alpha < 128 else 0))
            frames.append(indexed)
        target = ASSETS / f'{name}.gif'
        frames[0].save(target, save_all=True, append_images=frames[1:], duration=120,
                       loop=0, optimize=True, disposal=1, transparency=255)
        print(f'{target.name}: {target.stat().st_size:,} bytes; 72 frames; continuous loop', flush=True)
    finally:
        page.close()


def main():
    save_buttons()
    executable = str(CHROME) if CHROME.is_file() else shutil.which('google-chrome')
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(executable_path=executable, headless=True)
        try:
            render_panel(browser, 'profile-dark', False)
            render_panel(browser, 'profile-dark-mobile', True)
        finally:
            browser.close()


if __name__ == '__main__':
    main()
