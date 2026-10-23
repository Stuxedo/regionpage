#!/usr/bin/env bash
# Checks the link-preview and icon setup: every page's Discord component embed is valid JSON under
# Discord's 3,000-byte limit (no stray "$1", none on the 404 page), the favicon files exist at the
# right sizes, site.webmanifest is complete, and every <head> carries the icon tag set.
# Run with: bash tests/site.sh
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PY="$(command -v python3 || command -v python)"
[ -n "$PY" ] || { echo "FAIL - python3 is needed to run these checks"; exit 1; }

"$PY" -I - "$ROOT" <<'PYEOF'
import json, re, struct, sys
from pathlib import Path

root = Path(sys.argv[1])
passed = failed = 0


def check(name, ok):
    global passed, failed
    if ok:
        passed += 1; print("ok   - " + name)
    else:
        failed += 1; print("FAIL - " + name)


def png_info(p):
    d = p.read_bytes()
    if d[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    w, h, depth, ctype = struct.unpack(">IIBB", d[16:26])
    return w, h, ctype


SKIP = ("node_modules", ".dev", ".git", "_site")
pages = sorted(p for p in root.rglob("*.html") if not any(s in p.relative_to(root).parts for s in SKIP))
rel = lambda p: p.relative_to(root).as_posix()

# Discord embeds
EMB = re.compile(r'<script id="discord:component-embed" type="application/json">(.*?)</script>', re.S)
for p in pages:
    t = p.read_text(encoding="utf-8")
    m = EMB.search(t)
    if rel(p) == "404.html":
        check("404.html has no Discord embed", "discord:component-embed" not in t)
        continue
    if not m:
        check(rel(p) + " has a Discord embed (or a left-out comment)", "<!-- discord:component-embed left out" in t)
        continue
    raw = m.group(1)
    try:
        data = json.loads(raw)
        ok = data["component"]["type"] == 17
    except Exception:
        ok = False
    check(rel(p) + ": embed is valid JSON", ok)
    check(rel(p) + ": embed is under 3,000 bytes", len(raw.encode("utf-8")) <= 3000)
    check(rel(p) + ": embed has no literal $1 and no unescaped </", "$1" not in raw and "</" not in raw)
    check(rel(p) + ": embed has only one copy", len(EMB.findall(t)) == 1)

# Favicon files
ico = root / "favicon.ico"
d = ico.read_bytes() if ico.exists() else b""
count = struct.unpack("<H", d[4:6])[0] if len(d) > 6 else 0
sizes = sorted((d[6 + 16 * i] or 256) for i in range(count)) if count else []
check("favicon.ico holds 16, 32 and 48 px images", sizes == [16, 32, 48])
check("favicon.ico images are PNG-in-ICO", count > 0 and all(
    d[struct.unpack("<I", d[6 + 16 * i + 12:6 + 16 * i + 16])[0]:][:8] == b"\x89PNG\r\n\x1a\n" for i in range(count)))
a = png_info(root / "apple-touch-icon.png") if (root / "apple-touch-icon.png").exists() else None
check("apple-touch-icon.png is 180x180 and opaque (no alpha)", a is not None and a[:2] == (180, 180) and a[2] in (0, 2))
for name, size in (("icon-192.png", 192), ("icon-512.png", 512), ("icon-maskable-512.png", 512)):
    i = png_info(root / name) if (root / name).exists() else None
    check(name + " is %dx%d" % (size, size), i is not None and i[:2] == (size, size))
i = png_info(root / "icon-maskable-512.png") if (root / "icon-maskable-512.png").exists() else None
check("icon-maskable-512.png is opaque (no alpha)", i is not None and i[2] in (0, 2))

# Manifest
try:
    man = json.loads((root / "site.webmanifest").read_text(encoding="utf-8"))
except Exception:
    man = {}
check("site.webmanifest has name, short_name, start_url / and display browser",
      bool(man.get("name")) and bool(man.get("short_name")) and man.get("start_url") == "/" and man.get("display") == "browser")
check("site.webmanifest has theme and background colours",
      all(re.fullmatch(r"#[0-9a-fA-F]{6}", str(man.get(k, ""))) for k in ("theme_color", "background_color")))
icons = {(x.get("sizes"), x.get("purpose", "any")): x.get("src", "") for x in man.get("icons", [])}
check("site.webmanifest lists 192, 512 and a maskable 512 icon, and the files exist",
      all(icons.get(k) and (root / icons[k].lstrip("/")).exists()
          for k in (("192x192", "any"), ("512x512", "any"), ("512x512", "maskable"))))

# Every <head> carries the tag set
TAGS = [
    r'<link rel="icon" href="[^"]*favicon\.ico" sizes="48x48">',
    r'<link rel="icon" type="image/png" sizes="512x512" href="[^"]*icon-512\.png">',
    r'<link rel="apple-touch-icon" href="[^"]*apple-touch-icon\.png">',
    r'<link rel="manifest" href="[^"]*site\.webmanifest">',
]
for p in pages:
    t = p.read_text(encoding="utf-8")
    heads = re.findall(r"<head>(.*?)</head>", t, re.S)
    check(rel(p) + ": has a <head> carrying the icon tag set",
          len(heads) >= 1 and all(re.search(x, h) for h in heads for x in TAGS))

print("%d passed, %d failed" % (passed, failed))
sys.exit(1 if failed else 0)
PYEOF
