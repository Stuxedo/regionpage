# Changelog

All notable changes to regionpage are documented here.

## v2.0.3

### Fixed

- The imprint said this page is published as Stuxedo, "which is operated by Stuxedo, which is operated by" Stux Group Ltd, repeating itself; it now reads "published as Stuxedo, which is operated by" Stux Group Ltd

## v2.0.2

### Changed

- README footer now matches the Stuxedo `.github` footer: "Built & Maintained by Stuxedo" with the Stuxedo icon, and "Stuxedo is a part of the Stux.Group brand of businesses" (replacing v2.0.1's "Stuxedo is operated by Stux Group Ltd…" line)
- Every page's footer, the imprint and the privacy policy now say Stuxedo is operated by Stux Group Ltd, matching the other Stux.Group brands' pages, instead of "operated by Stux.Cloud, which is operated by Stux Group Ltd"

## v2.0.1

### Changed

- README footer now matches the other Stux.Group brands' page repos: "Built & Maintained by Stuxedo" with the Stuxedo icon from `global.media.stuxedo.com` (instead of the GitHub avatar), and "Stuxedo is operated by Stux Group Ltd…" (it previously read "operated by Stux.Cloud, which is operated by Stux Group Ltd…")

## v2.0.0

### Changed

- Rebranded to Stuxedo's new tuxedo-cat logo colours: the logo's neon `#4bf708` is the accent on the dark theme (with dark button text) and its deep green `#032f14` is the accent on the light theme (with white button text). Every old green accent, floating-particle shade and site-banner accent follows that pairing; button hovers are a step lighter (`#78ff42` / `#0b4a24`); each theme's divider bar is now solid in that theme's accent instead of a two-tone gradient; the backgrounds and text are retinted to match (`#031e0d`, `#e6fff0`)
- The logo, icon and favicon pick up the new Stuxedo assets automatically from `global.media.stuxedo.com`
- README links the archived original design: [regionpage-v1](https://github.com/Stuxedo/regionpage-v1)

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
