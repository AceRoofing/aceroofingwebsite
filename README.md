# ACE Roofing — aceroofingtx.com

Static rebuild of [aceroofingtx.com](https://www.aceroofingtx.com/). It is plain HTML, CSS and JavaScript, with no build step and no dependencies. It can be hosted on GitHub Pages, Netlify, Cloudflare Pages or any web host.

## Pages

| URL | File |
| --- | --- |
| `/` | `index.html` |
| `/about-us/` | `about-us/index.html` |
| `/our-services/` | `our-services/index.html` |
| `/our-services/residential-roofing/` | `our-services/residential-roofing/index.html` |
| `/our-services/residential-roofing/roof-replacement/` | `…/roof-replacement/index.html` |
| `/our-services/residential-roofing/roof-repair/` | `…/roof-repair/index.html` |
| `/our-services/residential-roofing/roof-restoration/` | `…/roof-restoration/index.html` |
| `/our-services/residential-roofing/storm-damage-repair/` | `…/storm-damage-repair/index.html` |
| `/our-services/commercial-roofing/` | `our-services/commercial-roofing/index.html` |
| `/gallery/` | `gallery/index.html` |
| `/contact/` | `contact/index.html` |

The URLs match the current site, so existing Google rankings and links carry over.

Shared files:

- `assets/css/styles.css`: all styling. Brand colors and fonts are at the top (`--gold`, `--black`, etc.).
- `assets/js/main.js`: mobile menu, gallery lightbox and contact forms.
- `sitemap.xml`, `robots.txt`, `404.html`

## Before going live

1. **Forms.** Both forms email nperez@aceroofingtx.com through [FormSubmit](https://formsubmit.co). The address is set in `FORM_ENDPOINT` at the top of `assets/js/main.js`. The first submission sends a one-time confirmation email to that inbox; click the link in it to turn the forms on.
2. **Images.** Images are still loaded from the current website host (`irp.cdn-website.com`). They will disappear if that account is cancelled. Run `scripts/localize-images.sh` from the repo root to download them into `assets/images/` and update every page to use the local copies.
3. **Hosting / domain.** For GitHub Pages: go to Settings → Pages, deploy from `main`, root folder, then set the custom domain to `www.aceroofingtx.com`.

## Making changes

Edit the HTML file for the page you want to change. The header and footer are repeated on every page, so update those in all pages at once.
