"""Render the README banners from their SVG sources.

Requires Pillow, Playwright, and Chrome (or a Playwright Chromium installation):
    python -m pip install pillow playwright
    python scripts/render-profile-assets.py

The animation plays once, takes less than five seconds, and ends on the static
banner. The README selects the original SVG when reduced motion is preferred.
"""

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
BANNERS = (
    ("profile-header", 1200, "M849 95H1028Q1060 95 1060 127V201Q1060 233 1028 233H849"),
    ("profile-header-mobile", 640, "M381 271H591"),
)


def render_banner(browser, name, width, path):
    page = browser.new_page(viewport={"width": width, "height": 320})
    try:
        page.goto((ASSETS / f"{name}.svg").as_uri())
        page.evaluate("document.fonts.ready")
        svg = page.locator("svg")
        outside = page.evaluate("""() => {
            const root = document.querySelector('svg');
            return Array.from(root.querySelectorAll('text')).filter(text => {
                const b = text.getBBox();
                return b.x < 0 || b.y < 0 || b.x + b.width > root.width.baseVal.value
                    || b.y + b.height > root.height.baseVal.value;
            }).map(text => text.textContent);
        }""")
        if outside:
            raise ValueError(f"Text outside {name}: {outside}")

        rgba = Image.open(io.BytesIO(svg.screenshot(omit_background=True))).convert("RGBA")
        transparent = rgba.getchannel("A").point(lambda alpha: 255 if alpha < 128 else 0)
        base = Image.new("RGB", rgba.size, "#14283f")
        base.paste(rgba, mask=rgba.getchannel("A"))
        palette = base.quantize(colors=240)
        palette.paste(255, mask=transparent)
        frames = [palette]
        page.evaluate("""path => {
            const ns = 'http://www.w3.org/2000/svg';
            const root = document.querySelector('svg');
            const guide = document.createElementNS(ns, 'path');
            guide.setAttribute('d', path);
            guide.setAttribute('fill', 'none');
            root.appendChild(guide);
            const marker = document.createElementNS(ns, 'g');
            marker.id = 'packet';
            marker.innerHTML = '<circle r="12" fill="#f2c879" opacity="0.15"/>'
                + '<circle r="4.5" fill="#f2c879"/>';
            root.appendChild(marker);
            window.placePacket = progress => {
                const point = guide.getPointAtLength(progress * guide.getTotalLength());
                marker.setAttribute('transform', `translate(${point.x} ${point.y})`);
                marker.setAttribute('opacity', Math.min(1, progress * 12, (1-progress)*12));
            };
        }""", path)
        for frame in range(1, 37):
            page.evaluate("progress => window.placePacket(progress)", frame / 37)
            rgba = Image.open(io.BytesIO(svg.screenshot(omit_background=True))).convert("RGBA")
            bitmap = Image.new("RGB", rgba.size, "#14283f")
            bitmap.paste(rgba, mask=rgba.getchannel("A"))
            indexed = bitmap.quantize(palette=palette, dither=Image.Dither.NONE)
            indexed.paste(255, mask=transparent)
            frames.append(indexed)
        frames.append(palette.copy())
        target = ASSETS / f"{name}.gif"
        frames[0].save(
            target,
            save_all=True,
            append_images=frames[1:],
            duration=[150] + [100] * 36 + [1000],
            optimize=True,
            disposal=1,
            transparency=255,
        )
        print(f"{target.name}: {target.stat().st_size:,} bytes")
    finally:
        page.close()


def main():
    executable = str(CHROME) if CHROME.is_file() else shutil.which("google-chrome")
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            executable_path=executable, headless=True
        )
        try:
            for banner in BANNERS:
                render_banner(browser, *banner)
        finally:
            browser.close()


if __name__ == "__main__":
    main()
