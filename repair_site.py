import os
import re
from pathlib import Path

root = Path(r"c:\My Web Sites\my website agency")
site_root = root / "themazine.com" / "mr" / "andeo"


def make_svg(path: Path, label: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9._-]+", "-", path.stem)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="800" viewBox="0 0 1200 800">
  <rect width="1200" height="800" fill="#eef4ff"/>
  <rect x="40" y="40" width="1120" height="720" rx="24" fill="#ffffff" stroke="#6dbfb8" stroke-width="6"/>
  <circle cx="900" cy="220" r="120" fill="#6dbfb8" opacity="0.18"/>
  <text x="600" y="420" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" font-size="44" fill="#1f2937">{label}</text>
  <text x="600" y="480" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" font-size="24" fill="#6b7280">{safe}</text>
</svg>'''


def make_html_stub(path: Path, title: str) -> str:
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{title}</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 0; padding: 3rem; background: #f8fafc; color: #111827; }}
    .card {{ max-width: 720px; margin: 0 auto; background: white; padding: 2rem; border-radius: 16px; box-shadow: 0 10px 30px rgba(0,0,0,0.08); }}
    a {{ color: #0f766e; }}
  </style>
</head>
<body>
  <div class="card">
    <h1>{title}</h1>
    <p>This placeholder page was created to keep the local mirror functional offline.</p>
    <p><a href="index.html">Return to home</a></p>
  </div>
</body>
</html>
'''


def relpath(target: Path, base: Path) -> str:
    return os.path.relpath(target, base).replace("\\", "/")


def ensure_svg(target: Path, label: str) -> Path:
    if target.suffix.lower() != ".svg":
        target = target.with_suffix(".svg")
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.exists() or target.stat().st_size == 0:
        target.write_text(make_svg(target, label), encoding="utf-8")
    return target


def ensure_html(target: Path, title: str) -> Path:
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.exists() or target.stat().st_size == 0:
        target.write_text(make_html_stub(target, title), encoding="utf-8")
    return target


def resolve_target(ref: str, current_file: Path) -> Path:
    clean = ref.split("#", 1)[0].split("?", 1)[0]
    if not clean:
        return current_file
    if clean.startswith("/"):
        return (site_root / clean.lstrip("/")).resolve()
    return (current_file.parent / clean).resolve()


def rewrite_html_file(path: Path) -> int:
    text = path.read_text(encoding="utf-8", errors="ignore")
    original = text

    def handle_attr(match):
        attr = match.group(1).lower()
        quote = match.group(2)
        value = match.group(3)
        if value.startswith(("http://", "https://", "mailto:", "tel:", "javascript:", "#", "data:")):
            return match.group(0)

        target = resolve_target(value, path)
        if attr == "href" and value.endswith((".html", ".htm")):
            if not target.exists() or target.stat().st_size == 0:
                ensure_html(target, target.stem.replace("-", " ").title())
            return f'{attr}={quote}{value}{quote}'

        if attr in {"src", "poster"} and value.endswith((".html", ".htm")):
            if target.exists() and target.stat().st_size > 0:
                return f'{attr}={quote}{value}{quote}'
            svg_target = ensure_svg(target, target.stem.replace("-", " ").title())
            new_value = relpath(svg_target, path.parent)
            return f'{attr}={quote}{new_value}{quote}'

        if attr in {"src", "poster", "href"}:
            if not target.exists() or target.stat().st_size == 0:
                if value.endswith((".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".bmp", ".tif", ".tiff")):
                    svg_target = ensure_svg(target, target.stem.replace("-", " ").title())
                    return f'{attr}={quote}{relpath(svg_target, path.parent)}{quote}'
                if value.endswith((".css", ".js")):
                    return f'{attr}={quote}{value}{quote}'
                svg_target = ensure_svg(target, target.stem.replace("-", " ").title())
                return f'{attr}={quote}{relpath(svg_target, path.parent)}{quote}'

        return f'{attr}={quote}{value}{quote}'

    text = re.sub(r'(src|href|poster)=(["\'])([^"\']*)(\2)', lambda m: handle_attr(m), text, flags=re.I)

    def handle_css_url(match):
        value = match.group(1)
        if value.startswith(("http://", "https://", "mailto:", "tel:", "javascript:", "#", "data:")):
            return match.group(0)
        target = resolve_target(value, path)
        if value.endswith((".html", ".htm")):
            if not target.exists() or target.stat().st_size == 0:
                svg_target = ensure_svg(target, target.stem.replace("-", " ").title())
                return f"url('{relpath(svg_target, path.parent)}')"
        if not target.exists() or target.stat().st_size == 0:
            svg_target = ensure_svg(target, target.stem.replace("-", " ").title())
            return f"url('{relpath(svg_target, path.parent)}')"
        return match.group(0)

    text = re.sub(r"url\(['\"]([^'\"]+)['\"]\)", lambda m: handle_css_url(m), text, flags=re.I)

    # Fix the specific broken root assets and favicon references.
    text = text.replace('href="images/fabicon.png"', 'href="images/fabicon.svg"')
    text = text.replace('content="images/assets/ogg.html"', 'content="images/assets/ogg.svg"')
    text = text.replace('src="images/icon/search.html"', 'src="images/icon/search.svg"')
    text = text.replace('src="images/icon/grid.html"', 'src="images/icon/grid.svg"')
    text = text.replace('src="images/shape/shape-01.html"', 'src="images/shape/shape-01.svg"')
    text = text.replace('src="images/shape/shape-02.html"', 'src="images/shape/shape-02.svg"')
    text = text.replace('url(\'images/bg/bg-01.html\')', "url('images/bg/bg-01.svg')")
    text = text.replace('url(\'images/bg/bg-03.html\')', "url('images/bg/bg-03.svg')")
    text = text.replace('url(\'images/banner/banner-03.html\')', "url('images/banner/banner-03.svg')")

    if text != original:
        path.write_text(text, encoding="utf-8")
    return 1 if text != original else 0


# Fix the root landing page.
root_index = root / "index.html"
root_index.write_text('''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta http-equiv="refresh" content="0; url=themazine.com/mr/andeo/index.html" />
  <title>Andeo site</title>
  <style>
    body { font-family: Arial, sans-serif; background: #f3f4f6; color: #111827; margin: 0; display: grid; place-items: center; min-height: 100vh; }
    .box { background: white; padding: 2rem 2.5rem; border-radius: 16px; box-shadow: 0 14px 40px rgba(0,0,0,.08); }
    a { color: #0f766e; }
  </style>
</head>
<body>
  <div class="box">
    <h1>Andeo website is ready locally</h1>
    <p>The main homepage is available at <a href="themazine.com/mr/andeo/index.html">themazine.com/mr/andeo/index.html</a>.</p>
    <p>If you are not redirected automatically, click the link above.</p>
  </div>
</body>
</html>
''', encoding="utf-8")

# Create the core missing assets.
ensure_svg(site_root / "images" / "fabicon.png", "Favicon")
ensure_svg(site_root / "images" / "assets" / "ogg.html", "Open Graph Image")
ensure_svg(site_root / "images" / "icon" / "search.html", "Search Icon")
ensure_svg(site_root / "images" / "icon" / "grid.html", "Grid Icon")
ensure_svg(site_root / "images" / "shape" / "shape-01.html", "Shape 01")
ensure_svg(site_root / "images" / "shape" / "shape-02.html", "Shape 02")
ensure_svg(site_root / "images" / "bg" / "bg-01.html", "Background 01")
ensure_svg(site_root / "images" / "bg" / "bg-03.html", "Background 03")
ensure_svg(site_root / "images" / "banner" / "banner-03.html", "Banner 03")

# Rewrite the mirrored HTML files.
html_files = list(site_root.rglob("*.html"))
changed = 0
for html_file in html_files:
    changed += rewrite_html_file(html_file)

# Create a few placeholder pages for any missing internal links.
for rel in ["faq.html", "service.html", "service-details.html", "blog.html", "blog-details.html"]:
    ensure_html(site_root / rel, rel.replace(".html", "").replace("-", " ").title())

print(f"Processed {len(html_files)} HTML files; updated {changed} files.")
