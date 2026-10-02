# Contributing to regionpage

Thank you for your interest in contributing! This repository is a small, static region-landing-page template, so contributions are usually small too.

## Getting Started

1. **Fork the repository** and clone your fork locally.
2. **Run it locally** with `./dev-server.sh` (or `dev-server.bat` on Windows) and open the printed URL, for example `http://127.0.0.1:8000/?region=uk`.
3. **Make your changes** to `index.html` or, to add a region or server, `assets/regions.js` — no build step required.
4. **Submit a pull request** with a clear description of what you've changed and why.

## Reporting Bugs

- Check existing issues to avoid duplicates before opening a new one.
- Provide a clear title and description, steps to reproduce, and the expected vs. actual behaviour.
- Include your browser and OS where relevant — this is a purely client-side page, so most bugs are rendering issues.

## Suggesting Features

- Open an issue with the label `enhancement` and describe your idea clearly.
- Keep in mind this project is meant to stay lightweight and dependency-free.

## Style Guidelines

- Keep `index.html` a single static HTML file where possible — no build tooling, no frameworks. `changelog.html`, `404.html` and `assets/fonts/` are the deliberate exceptions: fonts need real files to self-host, and `changelog.html` fetches and renders `CHANGELOG.md` at runtime rather than duplicating it inline.
- Regions and servers live only in `assets/regions.js` (strict JSON inside, so `scripts/build-readme.py` can read it). After editing it, run `python scripts/build-readme.py` to refresh the README's region table.
- Match the existing CSS variable naming and light/dark theme structure.
- General contact uses `hello@stuxedo.com`; legal-page contact uses `legal@stuxedo.com`.
- Test both the light and dark themes, a region with servers (`?region=uk`), a region without (`?region=au`), the index (no `?region`), and the embedded (iframe) code path through `wrapper/index.html`, before submitting.
- `wrapper/index.html` is uploaded unchanged to every region's website; don't add per-region settings to it.
- The sitemap (`sitemap.xml`, `sitemap/index.html`, `robots.txt`) is generated: after adding or removing a page, edit the `PAGES` list in `scripts/build-sitemap.py` and run `python scripts/build-sitemap.py`, then commit the result

## Questions

If you have any questions, feel free to reach out at [hello@stuxedo.com](mailto:hello@stuxedo.com) or open a discussion in this repository.

---

*Stuxedo is part of the [Stux.Group](https://github.com/StuxGroup) Brand of Companies.*
