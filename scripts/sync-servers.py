"""Adds new Stuxedo servers to this page from Cloudflare's DNS. Run daily by .github/workflows/servers-sync.yml.

Every server has an A record <name>.servers.<cc>.stuxedo.net in the stuxedo.net zone. A server that has a
record but isn't in assets/regions.js is added to its region, with its status from the <name> monitor (the
Status repo's own sync adds that monitor), then the README table and sitemap are rebuilt, and a release is
written: CHANGELOG.md entry and VERSION.md. The workflow commits, tags and deploys it.

Only additions are automatic. A server in a country that isn't a region yet fails the run (a region needs a
name, flag and parent: add it with the deploy-stuxedo-server skill), and a listed server with no record is only
warned about, since retiring one is a person's decision.

    CLOUDFLARE_DNS_TOKEN=... python scripts/sync-servers.py      (Zone > DNS > Read, on stuxedo.net)
"""
import datetime, json, os, re, subprocess, sys, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JS = ROOT / "assets/regions.js"
ZONE = "stuxedo.net"
HOST = re.compile(r"^([a-z0-9]+)\.servers\.([a-z]{2})\.stuxedo\.net$")


def cloudflare(path):
    req = urllib.request.Request("https://api.cloudflare.com/client/v4" + path,
                                 headers={"Authorization": "Bearer " + os.environ["CLOUDFLARE_DNS_TOKEN"]})
    with urllib.request.urlopen(req, timeout=30) as r:
        body = json.load(r)
    if not body.get("success"):
        sys.exit(f"Cloudflare: {body.get('errors')}")
    return body["result"]


def dns_servers():
    zone = cloudflare(f"/zones?name={ZONE}")[0]["id"]
    found = set()
    for rec in cloudflare(f"/zones/{zone}/dns_records?type=A&per_page=1000"):
        m = HOST.match(rec["name"])
        if m:
            found.add((m.group(1), m.group(2)))
    return found


def read(path):
    raw = path.read_bytes().decode("utf-8")
    return raw.replace("\r\n", "\n"), "\r\n" in raw


def write(path, text, crlf):
    path.write_bytes((text.replace("\n", "\r\n") if crlf else text).encode("utf-8"))


def add_server(t, name, cc):
    """Adds {name, monitor: name} to region cc's servers, keeping the file's layout."""
    m = re.search(r'(\{\s*"code":\s*"%s".*?"servers":\s*\[)(.*?)(\])' % re.escape(cc), t, re.S)
    inner = m.group(2)
    entry = '{ "name": "%s", "monitor": "%s" }' % (name, name)
    if inner.strip():
        indent = re.search(r"\n(\s*)\{", inner).group(1)
        inner = inner.rstrip() + ",\n" + indent + entry + "\n" + indent[:-2]
    else:
        inner = "\n        " + entry + "\n      "
    return t[:m.start(2)] + inner + t[m.end(2):]


def next_version():
    today = datetime.datetime.now(datetime.timezone.utc).strftime("%y.%m.%d")
    tags = subprocess.run(["git", "tag", "-l", f"v{today}*"], cwd=ROOT, capture_output=True, text=True).stdout.split()
    taken = {(ROOT / "VERSION.md").read_text().strip(), *(t[1:] for t in tags)}
    if today not in taken:
        return today
    return f"{today}-{max(int(v.split('-')[1]) if '-' in v else 0 for v in taken if v.startswith(today)) + 1}"


def main():
    t, crlf = read(JS)
    data = json.loads(t[t.index("{", t.index("REGION_DATA")): t.rindex("}") + 1])
    brand, regions = data["brand"], {r["code"]: r for r in data["regions"]}
    listed = {(s["name"], code) for code, r in regions.items() for s in r["servers"]}
    found = dns_servers()

    for name, cc in sorted(listed - found):
        if any(s["name"] == name and s["monitor"] for s in regions[cc]["servers"]):
            print(f"::warning::{name} ({cc}) is listed but has no DNS record. If it's retired, remove it by hand.")
    new = sorted(found - listed)
    unknown = [(n, cc) for n, cc in new if cc not in regions]
    for name, cc in unknown:
        print(f"::error::{name}.servers.{cc}.{ZONE}: '{cc}' isn't a region yet. Add it with the deploy-stuxedo-server skill.")
    new = [(n, cc) for n, cc in new if cc in regions]
    for name, cc in new:
        t = add_server(t, name, cc)
        print(f"added {name} to {regions[cc]['name']} ({cc})")

    if new:
        write(JS, t, crlf)
        for s in ("build-readme.py", "build-sitemap.py"):
            subprocess.run([sys.executable, f"scripts/{s}"], cwd=ROOT, check=True)
        version = next_version()
        lines = "\n".join(f"- **{n}**, a server in {regions[cc]['name']} (`{n}.servers.{cc}.{brand['domain']}`, status from "
                          f"the `{n}` monitor). Added automatically from Stuxedo's DNS." for n, cc in new)
        log, log_crlf = read(ROOT / "CHANGELOG.md")
        i = log.index("\n## v") + 1
        write(ROOT / "CHANGELOG.md", log[:i] + f"## v{version}\n\n### Added\n\n{lines}\n\n" + log[i:], log_crlf)
        (ROOT / "VERSION.md").write_text(version + "\n")
        print(f"release v{version}")
        out = os.environ.get("GITHUB_OUTPUT")
        if out:
            with open(out, "a") as f:
                f.write(f"version={version}\n")
    else:
        print("nothing new: every server with a DNS record is listed")
    if unknown:
        sys.exit(1)


main()
