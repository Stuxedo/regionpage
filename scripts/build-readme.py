#!/usr/bin/env python3
"""Regenerate the region table in README.md from assets/regions.js.

Run from anywhere: python scripts/build-readme.py
assets/regions.js is the one place regions and servers are listed; this copies it into the
README between the <!-- regions:start --> and <!-- regions:end --> markers.

Copyright (c) Stux.Group. All Rights Reserved.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load():
    text = (ROOT / "assets" / "regions.js").read_text(encoding="utf-8")
    start = text.index("window.REGION_DATA = ") + len("window.REGION_DATA = ")
    end = text.rindex("};") + 1
    return json.loads(text[start:end])


def table(data) -> str:
    brand = data["brand"]
    regions = data["regions"]
    by_code = {r["code"]: r for r in regions}
    server_domain = brand.get("serverDomain") or brand["domain"]

    def children(code):
        return [r for r in regions if r.get("parent") == code]

    def count(r):
        return len(r["servers"]) + sum(count(c) for c in children(r["code"]))

    rows = ["| Region | Code | Part of | Website | Servers |", "|---|---|---|---|---|"]
    for r in regions:
        site = f"https://{r['code']}.{brand['domain']}"
        parent = by_code[r["parent"]]["name"] if r.get("parent") else "—"
        own = [f"`{s['name']}.servers.{r['code']}.{server_domain}`" + ("" if s["monitor"] else " (not monitored)")
               for s in r["servers"]]
        kids = children(r["code"])
        if kids:
            n = count(r)
            names = ", ".join(c["name"] for c in kids)
            own.append(f"{n} across {names}" if n else f"None yet (covers {names})")
        name = f"**{r['name']}**" if not r.get("parent") else r["name"]
        rows.append(f"| {name} | `{r['code']}` | {parent} | [{site}]({site}) | {'<br>'.join(own) or 'None yet'} |")
    return chr(10).join(rows)


def main() -> None:
    data = load()
    readme = ROOT / "README.md"
    text = readme.read_text(encoding="utf-8")
    pattern = re.compile(r"(<!-- regions:start -->\n).*?(<!-- regions:end -->)", re.DOTALL)
    if not pattern.search(text):
        raise SystemExit("README.md has no <!-- regions:start --> / <!-- regions:end --> markers")
    text = pattern.sub(lambda m: m.group(1) + table(data) + "\n" + m.group(2), text)
    readme.write_text(text, encoding="utf-8", newline="\n")
    print(f"Updated README.md ({len(data['regions'])} regions)")


if __name__ == "__main__":
    main()
