# Progressive Publics Calgary 2025

This repository contains the website for the Progressive Publics conference series.

The site is built with [Hugo](https://gohugo.io/) and the [Blowfish](https://blowfish.page/)
theme, and it allows for easy switching English and French content, light and dark mode,
and is mobile friendly.

## Prerequisites

- [**Hugo**](https://github.com/gohugoio/hugo) `v0.154.5` or newer (use the
extended build if possible so SCSS assets compile correctly).
- **Go** (optional) if you install Hugo via `go install`.

## Quick start

```bash
git clone git@github.com:progressivepublics/progressivepublics.git
cd progressivepublics
hugo server 
```

Visit <http://localhost:1313> to see the local site. Hit `Ctrl+C` to stop the server.

Run `hugo --minify` to produce a production build in `public/`.

## Repository tour

| Path | Purpose |
| --- | --- |
| `content/` | Markdown content. Every English page needs a matching French page (and vice versa) otherwise the language switching doesn't work. |
| `config/_default/` | Hugo configuration split into multiple TOML files. Hugo only reads files that live in a layer directory (`_default`, `production`, `en`, `fr`, etc.), so keep new settings inside those folders. |
| `i18n/` | Translation files for UI strings that are not in Markdown. |
| `assets/` | Custom CSS, SVG backgrounds, and the seasonal colour palettes. Hugo processes these via `assets/css/custom.css`. |
| `static/fonts/` | Bundled fonts. `IBM_Selectric_Light_Italic.ttf` includes extra accented glyphs (é, É, à, À, # tweaks)  |

## Theme, colour, and typography

- Blowfish provides the base layout
- Overrides live in `assets/css/custom.css` and the seasonal scheme files are in `assets/css/schemes/`.

## Navigation, menus, and translations

- Update `config/_default/menus.en.toml` and `config/_default/menus.fr.toml`
together so navigation stays in sync between languages.
- UI copy (button labels, etc.) lives in `i18n/en.yaml` and `i18n/fr.yaml`.
- Markdown content must exist in both languages (e.g., `content/about/_index.md`
and `content/about/_index.fr.md`). Hugo automatically links the language variants.

## Creating a site for a new conference

1. **Clone this repo**

As the baseline for the next event.

Rename the folder and update the Git remote.

2. **Adjust the conference details**

Most things (dates, speakers, schedule) are in `content/`,

Colour scheme and them are in `config/_default/params.toml`.

3. **Run `hugo server`**

