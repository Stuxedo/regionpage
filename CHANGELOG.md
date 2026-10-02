# Changelog

All notable changes to regionpage are documented here.

## v1.0.1

### Changed

- down1 (United States) shows its live status, now that it is monitored on status.stux.group

## v1.0.0

### Added

- The region page template: a Stuxedo region's name and flag, its servers with live Online / Degraded / Offline badges, and a switcher linking to every region (opening the region's own website, outside the frame)
- A "Stuxedo regions" index, shown when no region is known
- Region detection from `?region=` (which wins) or the first label of the framing site's host in `document.referrer`, plus a `page-title` `postMessage` mirroring the title to the wrapper
- `assets/regions.js`, the single list of regions and servers (10 regions; servers on uk, es, us and ca) shared by the page and the README's region table (`python scripts/build-readme.py`)
- `wrapper/index.html`, the small page each region's website serves to frame the template full-screen; the same file is uploaded unchanged to every region
- Live status from the Stux.Group status page's `summary.json`, with "Not monitored" for servers that have no monitor and no badge if the fetch fails
- Light and dark themes, flags from flag-icons, and a leaf icon for the Eco region
- The shared Stux page set: `changelog`, `404`, `legal` and its six sub-pages, `sitemap` and `sitemap.xml` (regenerated with `python scripts/build-sitemap.py`), the dev-mode banner, `dev-server.sh`/`.bat` (PHP 7.4, DEV_MODE on by default, `--no-dev-mode`), `commit.sh`/`.bat`, CI and the GitHub Pages workflow
