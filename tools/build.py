#!/usr/bin/env python3
"""Generates every page of the ACE Roofing site.

Edit page content in this file, styling in assets/css/styles.css and scripts in
assets/js/main.js, then rebuild from the repository root:

    python3 tools/build.py

The CSS and JS are minified and inlined into each page so nothing blocks the
first paint (GitHub Pages only lets browsers cache separate files for 10 min).
"""
import html
import json
import os
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SITE = "https://www.aceroofingtx.com"
CDN = "https://irp.cdn-website.com/ff2f5b1a/dms3rep/multi/opt/"
CDN_FULL = "https://irp.cdn-website.com/ff2f5b1a/dms3rep/multi/"

PHONE = "956-534-2911"
PHONE_DISPLAY = "(956) 534-2911"

FACEBOOK = "https://www.facebook.com/aceroofingtx"
INSTAGRAM = "https://www.instagram.com/aceroofing_tx/"
TIKTOK = "https://www.tiktok.com/@aceroofing_tx"


def img(name):
    return CDN + name


import re as _re
from datetime import date as _date

TODAY = _date.today().isoformat()


def sized(url, w):
    """Return the CDN url resized to width w (the CDN resizes on demand)."""
    return _re.sub(r"-\d+w\.(\w+)$", rf"-{w}w.\1", url)


def srcset(url, widths=(480, 768, 1080, 1440, 1920)):
    return ", ".join(f"{sized(url, w)} {w}w" for w in widths)


def rimg(url, alt, sizes="100vw", cls="", w=1200, h=800, lazy=True, priority=False, widths=(480, 768, 1080, 1440, 1920)):
    attrs = [f'src="{sized(url, 1080)}"', f'srcset="{srcset(url, widths)}"', f'sizes="{sizes}"',
             f'alt="{e(alt)}"', f'width="{w}"', f'height="{h}"']
    if not priority:
        attrs.append('decoding="async"')
    if cls:
        attrs.insert(0, f'class="{cls}"')
    if priority:
        attrs.append('fetchpriority="high"')
    elif lazy:
        attrs.append('loading="lazy"')
    return f"<img {' '.join(attrs)}>"


LOGO = img("PNG-High-Res-533a3d51-1920w.png")
LOGO_WHITE = img("PNG-White-High-Res-595w.png")
FAVICON = img("icon-black-house-115h.png")
SPADE_BLACK = img("icon-black-124h.png")
SPADE_GOLD = img("icon-black-house-115h.png")
SPADES_ROW = img("Testimonials-2-243w.png")
OG_IMAGE = img("social+networks+image-1920w.jpg")

BADGES = [
    ("602e376ed9ced200045a579c-1920w.png", "BBB Accredited Business", 360, 184),
    ("04d16ecf-4c00-40e1-80f9-a4bcaf84e1ab-1920w.png", "Licensed Roofing Contractors Association of Texas", 360, 360),
    ("185-1851668_gaf-certified-contractor-hd-png-download-1920w.png", "GAF Certified Weather Stopper Roofing Contractor", 360, 146),
    ("Home-Advisor-1920w.png", "HomeAdvisor Top Rated", 209, 241),
]

# Service card images
IMG_REPLACE = img("pexels-photo-37677394-1920w.jpeg")
IMG_RESTORE = img("Screenshot+2026-11-17+at+4.52.47-PM-1920w.png")
IMG_INSURANCE = img("insurance+claim-1920w.webp")
IMG_REPAIR = img("Roof+Repairs-1920w.jpg")
IMG_STORM = img("storm+damage+repair-1920w.jpg")
IMG_COMMERCIAL = img("commercial-roofing-1920w.jpg")

GALLERY = [
    ("08", "jpg", "Brick home with a steep new roof completed by ACE Roofing in Dallas-Fort Worth"),
    ("Screenshot+2023-10-25+9.19.48+AM", "png", "Aerial view of a house with orange roof tiles surrounded by green trees"),
    ("Screenshot+2023-10-25+9.18.20+AM", "png", "Aerial view of a gray-roofed suburban house with a driveway and trees"),
    ("Screenshot+2023-10-25+9.21.41+AM", "png", "Aerial view of a large dark-roofed house surrounded by green trees"),
    ("Screenshot+2023-10-25+9.22.04+AM", "png", "Aerial view of a dark gray roof over a home with a wooden patio"),
    ("pexels-photo-37677394", "jpeg", "Newly installed residential shingle roof in the Dallas-Fort Worth area"),
    ("Screenshot+2026-11-17+at+4.52.47-PM", "png", "Recent ACE Roofing residential roofing project in North Texas"),
    ("Screenshot+2026-11-17+at+4.52.38-PM", "png", "Recent ACE Roofing residential roof replacement in DFW"),
]

e = html.escape

# --------------------------------------------------------------------------
# Icons
# --------------------------------------------------------------------------
ICON_PHONE = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 0 1 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1z"/></svg>'
ICON_FB = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M14 8V6.2c0-.8.2-1.2 1.4-1.2H17V2h-2.6C11.2 2 10 3.6 10 6.2V8H8v3h2v11h4V11h2.7l.3-3z"/></svg>'
ICON_IG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 7a5 5 0 1 0 0 10 5 5 0 0 0 0-10zm0 8.2a3.2 3.2 0 1 1 0-6.4 3.2 3.2 0 0 1 0 6.4zM17.3 5.5a1.2 1.2 0 1 0 0 2.4 1.2 1.2 0 0 0 0-2.4zM21.9 7.9c-.1-1.6-.4-3-1.6-4.2-1.2-1.2-2.6-1.5-4.2-1.6C14.5 2 9.5 2 7.9 2.1c-1.6.1-3 .4-4.2 1.6C2.5 4.9 2.2 6.3 2.1 7.9 2 9.5 2 14.5 2.1 16.1c.1 1.6.4 3 1.6 4.2 1.2 1.2 2.6 1.5 4.2 1.6 1.6.1 6.6.1 8.2 0 1.6-.1 3-.4 4.2-1.6 1.2-1.2 1.5-2.6 1.6-4.2.1-1.6.1-6.6 0-8.2zm-2.1 10a3.3 3.3 0 0 1-1.9 1.9c-1.3.5-4.4.4-5.9.4s-4.6.1-5.9-.4a3.3 3.3 0 0 1-1.9-1.9c-.5-1.3-.4-4.4-.4-5.9s-.1-4.6.4-5.9a3.3 3.3 0 0 1 1.9-1.9c1.3-.5 4.4-.4 5.9-.4s4.6-.1 5.9.4a3.3 3.3 0 0 1 1.9 1.9c.5 1.3.4 4.4.4 5.9s.1 4.6-.4 5.9z"/></svg>'
ICON_TT = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M16.6 5.8A4.3 4.3 0 0 1 15.5 3h-3.1v12.4a2.6 2.6 0 0 1-2.6 2.5 2.6 2.6 0 0 1 0-5.2c.3 0 .5 0 .8.1V9.6a5.8 5.8 0 0 0-.8-.1 5.7 5.7 0 1 0 5.7 5.7V9a7.4 7.4 0 0 0 4.3 1.4V7.3s-1.9.1-3.2-1.5z"/></svg>'
ICON_PIN = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a7 7 0 0 0-7 7c0 5.3 7 13 7 13s7-7.7 7-13a7 7 0 0 0-7-7zm0 9.5a2.5 2.5 0 1 1 0-5 2.5 2.5 0 0 1 0 5z"/></svg>'
ICON_CLOCK = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20zm0 18a8 8 0 1 1 0-16 8 8 0 0 1 0 16zm.5-13H11v6l5.2 3.2.8-1.3-4.5-2.7z"/></svg>'


def social_links():
    return (
        f'<a href="{FACEBOOK}" target="_blank" rel="noopener" aria-label="ACE Roofing on Facebook">{ICON_FB}</a>'
        f'<a href="{INSTAGRAM}" target="_blank" rel="noopener" aria-label="ACE Roofing on Instagram">{ICON_IG}</a>'
        f'<a href="{TIKTOK}" target="_blank" rel="noopener" aria-label="ACE Roofing on TikTok">{ICON_TT}</a>'
    )


# --------------------------------------------------------------------------
# Page shell
# --------------------------------------------------------------------------
NAV = [
    ("Home", ""),
    ("About Us", "about-us/"),
    ("Our Services", "our-services/"),
    ("Recent Projects", "gallery/"),
    ("Contact Us", "contact/"),
]

SERVICES_MENU = [
    ("Residential Roofing", "our-services/residential-roofing/", False),
    ("Roof Replacement", "our-services/residential-roofing/roof-replacement/", True),
    ("Roof Repair", "our-services/residential-roofing/roof-repair/", True),
    ("Roof Restoration", "our-services/residential-roofing/roof-restoration/", True),
    ("Storm Damage Repair", "our-services/residential-roofing/storm-damage-repair/", True),
    ("Commercial Roofing", "our-services/commercial-roofing/", False),
]


def header(r, path):
    items = []
    for label, href in NAV:
        current = ' aria-current="page"' if href == path or (href and path.startswith(href) and href != "") else ""
        if href == "" and path == "":
            current = ' aria-current="page"'
        if label == "Our Services":
            sub = "".join(
                f'<li{" class=\"sub\"" if is_sub else ""}><a href="{r}{h}">{e(l)}</a></li>'
                for l, h, is_sub in SERVICES_MENU
            )
            items.append(
                f'<li class="has-dropdown"><a class="nav__link" href="{r}{href}"{current} aria-haspopup="true" aria-expanded="false">'
                f'{e(label)}<span class="nav__caret" aria-hidden="true">&#9662;</span></a>'
                f'<ul class="dropdown">{sub}</ul></li>'
            )
        else:
            items.append(f'<li><a class="nav__link" href="{r}{href}"{current}>{e(label)}</a></li>')

    return f"""<a class="skip-link" href="#main">Skip to content</a>
<div class="topbar">
  <div class="container">
    <span class="topbar__msg">Free Inspection Within 24 Hours &bull; 24/7 Emergency Services</span>
    <a href="tel:{PHONE}">Call {PHONE_DISPLAY}</a>
    <div class="topbar__social">{social_links()}</div>
  </div>
</div>
<header class="site-header">
  <div class="container">
    <a class="logo" href="{r}" aria-label="ACE Roofing home">
      <img src="{sized(LOGO, 200)}" srcset="{sized(LOGO, 200)} 200w, {sized(LOGO, 300)} 300w, {sized(LOGO, 400)} 400w" sizes="(max-width: 960px) 158px, 186px" alt="ACE Roofing - Dallas-Fort Worth roofing contractor" width="186" height="64">
    </a>
    <nav class="nav" aria-label="Main">
      <ul class="nav__list">
        {''.join(items)}
      </ul>
      <a class="btn header-call" href="tel:{PHONE}">{ICON_PHONE} Click To Call</a>
    </nav>
    <button class="nav-toggle" aria-label="Open menu" aria-expanded="false"><span></span></button>
  </div>
</header>"""


def badges_html():
    return "".join(
        f'<img src="{sized(img(f), 360)}" alt="{e(a)}" loading="lazy" decoding="async" width="{bw}" height="{bh}">' for f, a, bw, bh in BADGES
    )


def footer(r):
    services = "".join(f'<li><a href="{r}{h}">{e(l)}</a></li>' for l, h, _ in SERVICES_MENU)
    pages = "".join(f'<li><a href="{r}{h}">{e(l)}</a></li>' for l, h in NAV)
    return f"""<footer class="site-footer">
  <div class="footer-badges">
    <div class="container badges">{badges_html()}</div>
  </div>
  <div class="container footer-main">
    <div>
      <img class="footer-logo" src="{sized(LOGO_WHITE, 600)}" alt="ACE Roofing" loading="lazy" decoding="async" width="240" height="82">
      <p>Residential and commercial roofing contractor for homes and businesses across Dallas-Fort Worth, Texas. Don&rsquo;t gamble your roof &mdash; bet on ACE Roofing.</p>
      <div class="social">{social_links()}</div>
    </div>
    <div>
      <p class="footer-title">Company</p>
      <ul>{pages}</ul>
    </div>
    <div>
      <p class="footer-title">Services</p>
      <ul>{services}<li><a href="{r}contact/">Insurance Claims</a></li></ul>
    </div>
    <div>
      <p class="footer-title">Contact</p>
      <ul>
        <li><a href="tel:{PHONE}">{PHONE_DISPLAY}</a></li>
        <li>Serving the Dallas-Fort Worth metroplex</li>
        <li>24/7 Emergency Services</li>
      </ul>
      <p style="margin-top:18px"><a class="btn" href="{r}contact/">Contact Us Today!</a></p>
    </div>
  </div>
  <div class="footer-bottom">
    <div class="container">
      <span>&copy; <span data-year>2026</span> ACE Roofing. All Rights Reserved.</span>
      <span>Roofing in {", ".join(AREAS)} &amp; surrounding DFW communities</span>
    </div>
  </div>
</footer>
<a class="mobile-call" href="tel:{PHONE}">Call Now &mdash; Free Inspection</a>"""


AREAS = ["Dallas", "Fort Worth", "Plano", "Frisco", "McKinney", "Allen", "Murphy", "Sachse"]
BUSINESS_ID = SITE + "/#business"

BUSINESS = {
    "@type": "RoofingContractor",
    "@id": BUSINESS_ID,
    "name": "ACE Roofing",
    "alternateName": "ACE Roofing Company",
    "description": "Residential and commercial roofing contractor serving Dallas-Fort Worth, Texas: roof replacement, roof repair, roof restoration, hail and storm damage repair, and insurance claim help. Free roof inspections within 24 hours and 24/7 emergency service.",
    "url": SITE + "/",
    "logo": LOGO,
    "image": OG_IMAGE,
    "telephone": "+1-" + PHONE,
    "priceRange": "$$",
    "areaServed": [{"@type": "AdministrativeArea", "name": "Dallas-Fort Worth metroplex, Texas"}]
    + [{"@type": "City", "name": f"{c}, TX"} for c in AREAS],
    "knowsAbout": ["Roof replacement", "Roof repair", "Roof restoration", "Hail damage roof repair",
                   "Storm damage roof repair", "Roofing insurance claims", "Commercial roofing", "Roof inspection"],
    "openingHoursSpecification": [{
        "@type": "OpeningHoursSpecification",
        "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
        "opens": "00:00",
        "closes": "23:59",
    }],
    "contactPoint": [{"@type": "ContactPoint", "telephone": "+1-" + PHONE, "contactType": "customer service",
                      "areaServed": "US-TX", "availableLanguage": "English"}],
    "sameAs": [FACEBOOK, INSTAGRAM, TIKTOK],
}

PAGES = []  # (path) for sitemap


def minify_css(css):
    css = _re.sub(r"/\*.*?\*/", "", css, flags=_re.S)
    css = _re.sub(r"\s+", " ", css)
    css = _re.sub(r"\s*([{};,>])\s*", r"\1", css)
    css = _re.sub(r"([{;])\s*([a-z-]+)\s*:\s*", r"\1\2:", css)
    css = css.replace(";}", "}")
    return css.strip()


def minify_js(js):
    js = _re.sub(r"/\*.*?\*/", "", js, flags=_re.S)
    out = []
    for line in js.splitlines():
        t = line.strip()
        if not t or t.startswith("//"):
            continue
        out.append(t)
    return "\n".join(out)


with open(os.path.join(OUT, "assets", "css", "styles.css")) as _f:
    INLINE_CSS = minify_css(_f.read())
with open(os.path.join(OUT, "assets", "js", "main.js")) as _f:
    INLINE_JS = minify_js(_f.read())

# Switches the Google Fonts stylesheet on once it has loaded (replaces an
# inline onload="" handler, which a strict Content-Security-Policy blocks).
FONT_JS = ("(function(l){if(!l)return;var f=function(){l.media='all'};"
           "if(l.sheet)f();else l.addEventListener('load',f)})(document.getElementById('gfonts'));")


def _sha256(code):
    import base64
    import hashlib
    return "'sha256-" + base64.b64encode(hashlib.sha256(code.encode("utf-8")).digest()).decode() + "'"


# Strict CSP (Lighthouse "Ensure CSP is effective against XSS attacks" and
# "Mitigate DOM-based XSS with Trusted Types"). Only the two inline scripts
# above, identified by their hashes, may run. 'unsafe-inline' and https: are
# ignored by modern browsers when hashes + 'strict-dynamic' are present; they
# only keep very old browsers working. GitHub Pages can't send headers, so it
# goes in a <meta> tag.
CSP = "; ".join([
    f"script-src {_sha256(FONT_JS)} {_sha256(INLINE_JS)} 'strict-dynamic' 'unsafe-inline' https:",
    "object-src 'none'",
    "base-uri 'none'",
    "form-action 'self'",
    "require-trusted-types-for 'script'",
    "upgrade-insecure-requests",
])


def canonical_for(path):
    return SITE + "/" + path


def breadcrumbs_schema(crumbs):
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": name, "item": canonical_for(path)}
            for i, (name, path) in enumerate(crumbs)
        ],
    }


def breadcrumbs_html(r, crumbs):
    items = []
    for i, (name, path) in enumerate(crumbs):
        if i == len(crumbs) - 1:
            items.append(f'<li aria-current="page">{e(name)}</li>')
        else:
            items.append(f'<li><a href="{r}{path}">{e(name)}</a></li>')
    return f'<nav class="breadcrumbs" aria-label="Breadcrumb"><div class="container"><ol>{"".join(items)}</ol></div></nav>'


def page(path, title, description, body, crumbs=None, extra_schema=None, page_type="WebPage"):
    depth = path.count("/")
    r = "../" * depth if depth else "./"
    canonical = canonical_for(path)
    PAGES.append(path)
    main = body(r)

    graph = [BUSINESS, {
        "@type": page_type,
        "@id": canonical + "#webpage",
        "url": canonical,
        "name": title,
        "description": description,
        "isPartOf": {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": "ACE Roofing"},
        "about": {"@id": BUSINESS_ID},
        "inLanguage": "en-US",
    }]
    if crumbs:
        full = [("Home", "")] + crumbs
        graph.append(breadcrumbs_schema(full))
        # visible breadcrumbs go right after the page hero
        idx = main.find("</section>")
        if idx != -1:
            idx += len("</section>")
            main = main[:idx] + "\n" + breadcrumbs_html(r, full) + main[idx:]
    if extra_schema:
        graph.extend(extra_schema)
    schema = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)

    # Preload the hero image (largest element on screen) so it shows faster.
    preload = ""
    m = _re.search(r'<img class="hero__bg" src="([^"]+)" srcset="([^"]+)" sizes="([^"]+)"', main)
    if m:
        preload = f'<link rel="preload" as="image" href="{m.group(1)}" imagesrcset="{m.group(2)}" imagesizes="{m.group(3)}" fetchpriority="high">'

    fonts = "https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Poppins:wght@400;600&display=swap"
    doc = f"""<!DOCTYPE html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="{CSP}">
<meta name="referrer" content="strict-origin-when-cross-origin">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="{canonical}">
<meta name="geo.region" content="US-TX">
<meta name="geo.placename" content="Dallas-Fort Worth">
<meta property="og:type" content="website">
<meta property="og:locale" content="en_US">
<meta property="og:site_name" content="ACE Roofing">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{OG_IMAGE}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(description)}">
<meta name="twitter:image" content="{OG_IMAGE}">
<meta name="theme-color" content="#000000">
<link rel="icon" type="image/png" href="{FAVICON}">
<link rel="apple-touch-icon" href="{FAVICON}">
<link rel="preconnect" href="https://irp.cdn-website.com" crossorigin>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
{preload}
<style>{INLINE_CSS}</style>
<link id="gfonts" rel="stylesheet" href="{fonts}" media="print">
<script>{FONT_JS}</script>
<noscript><link rel="stylesheet" href="{fonts}"></noscript>
<script type="application/ld+json">{schema}</script>
</head>
<body>
{header(r, path)}
<main id="main">
{main}
</main>
{footer(r)}
<script>{INLINE_JS}</script>
</body>
</html>
"""
    out_dir = os.path.join(OUT, path)
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "index.html"), "w") as f:
        f.write(doc)
    return path


# --------------------------------------------------------------------------
# Shared blocks
# --------------------------------------------------------------------------
def inspection_form(heading_tag="h2"):
    hear = ["Ace Roofing Representative", "Referral", "Google", "Social Media"]
    checks = "".join(
        f'<label><input type="checkbox" name="heard_about" value="{e(h)}"> {e(h)}</label>' for h in hear
    )
    return f"""<form class="form-card" data-contact-form novalidate>
  <{heading_tag}>Request Your Free Inspection Today</{heading_tag}>
  <input type="hidden" name="_subject" value="New free inspection request — aceroofingtx.com">
  <div class="form-grid">
    <div class="field"><label for="fi-first">First Name</label><input id="fi-first" name="first_name" autocomplete="given-name" required></div>
    <div class="field"><label for="fi-last">Last Name</label><input id="fi-last" name="last_name" autocomplete="family-name" required></div>
    <div class="field"><label for="fi-email">Email</label><input id="fi-email" type="email" name="email" autocomplete="email" required></div>
    <div class="field"><label for="fi-phone">Phone #</label><input id="fi-phone" type="tel" name="phone" autocomplete="tel" required></div>
    <div class="field full"><label for="fi-city">City / Location</label><input id="fi-city" name="location" autocomplete="address-level2"></div>
    <div class="field full"><label for="fi-msg">Explain Your Project Needs</label><textarea id="fi-msg" name="message"></textarea></div>
    <fieldset class="field full"><legend>How Did You Hear About Us?</legend><div class="checks">{checks}</div></fieldset>
    <input class="hp" type="text" name="_honey" tabindex="-1" autocomplete="off" aria-hidden="true">
    <div class="full"><button class="btn btn--block" type="submit">Submit</button></div>
  </div>
  <div class="form-status" role="status" aria-live="polite"></div>
</form>"""


def cta_band(r, text="Schedule A Free Roof Inspection Today!"):
    return f"""<section class="cta-band">
  <div class="container">
    <h2>{text}</h2>
    <div class="actions">
      <a class="btn btn--dark" href="{r}contact/">Contact Us Today!</a>
      <a class="btn btn--dark" href="tel:{PHONE}">{PHONE_DISPLAY}</a>
    </div>
  </div>
</section>"""


# The hero photo sits behind a dark overlay, so a lighter file looks the same.
HERO_SIZES = "(max-width: 960px) 60vw, 70vw"
HERO_WIDTHS = (480, 768, 1080)


def page_hero(r, title, intro, bg, button=True, alt=""):
    btn = (f'<div class="hero__actions hero__actions--center"><a class="btn" href="{r}contact/">Get A Free Inspection</a>'
           f'<a class="btn btn--outline" href="tel:{PHONE}">Call {PHONE_DISPLAY}</a></div>') if button else ""
    return f"""<section class="hero page-hero">
  {rimg(bg, alt, cls="hero__bg", priority=True, sizes=HERO_SIZES, widths=HERO_WIDTHS)}
  <div class="container">
    <h1>{e(title)}</h1>
    <p>{e(intro)}</p>
    {btn}
  </div>
</section>"""


CARD_TEXT = {
    "replace": ("Roof Replacements", "Providing A Durable & Secure New Roof For Your Home"),
    "repair": ("Roof Repairs", "Extending The Lifespan Of Your Roof With Superior Materials"),
    "restore": ("Roof Restorations", "Enhancing Your Roof's Functionality, Stability, & Appeal"),
    "storm": ("Storm Damage Repair", "Ensuring A Stronger & Better Roof After Hail & Storm Damage"),
    "insurance": ("Insurance Claims", "Helping You Streamline Your Insurance Claims Process"),
    "commercial": ("Commercial Roofing", "Offering Resilient & Affordable Roofing Solutions For Businesses"),
    "maintenance": ("Roof Maintenance", "Keeping Your Commercial Roof Protected Year-Round"),
}
CARD_LINK = {
    "replace": "our-services/residential-roofing/roof-replacement/",
    "repair": "our-services/residential-roofing/roof-repair/",
    "restore": "our-services/residential-roofing/roof-restoration/",
    "storm": "our-services/residential-roofing/storm-damage-repair/",
    "insurance": "contact/",
    "commercial": "our-services/commercial-roofing/",
    "maintenance": "contact/",
}
CARD_IMG = {
    "replace": IMG_REPLACE,
    "repair": IMG_REPAIR,
    "restore": IMG_RESTORE,
    "storm": IMG_STORM,
    "insurance": IMG_INSURANCE,
    "commercial": IMG_COMMERCIAL,
    "maintenance": img("04-ee4676b9-1920w.jpg"),
}


def cards(r, keys, cls="cards", images=None):
    images = images or {}
    out = []
    for k in keys:
        t, s = CARD_TEXT[k]
        bg = images.get(k, CARD_IMG[k])
        out.append(
            f'<a class="card" href="{r}{CARD_LINK[k]}">'
            + rimg(bg, "", sizes="(max-width: 640px) 100vw, (max-width: 960px) 50vw, 400px", cls="card__bg",
                   w=800, h=760, widths=(480, 640, 800, 1080))
            + f'<div class="card__body"><h3>{e(t)}</h3><p>{e(s)}</p><span class="card__more">Learn More<span class="sr-only"> about {e(t)}</span></span></div></a>'
        )
    return f'<div class="{cls}">{"".join(out)}</div>'


def gallery_html(items, cls="gallery"):
    out = []
    for name, ext, alt in items:
        out.append(
            f'<a href="{CDN}{name}-1600w.{ext}" data-lightbox>'
            + rimg(f"{CDN}{name}-640w.{ext}", alt, sizes="(max-width: 640px) 100vw, (max-width: 960px) 50vw, 400px",
                   w=640, h=480, widths=(400, 640, 960))
            + '</a>'
        )
    return f'<div class="{cls}">{"".join(out)}</div>'


def testimonial(quote, city):
    return (
        f'<figure class="testimonial">'
        f"<blockquote>{e(quote)}</blockquote><figcaption>{e(city)}</figcaption></figure>"
    )


def paras(*ps):
    return "".join(f"<p>{e(p)}</p>" for p in ps)


def badges_section():
    return ""


# --------------------------------------------------------------------------
# HOME
# --------------------------------------------------------------------------
FAQ = [
    (
        "Did You Experience a Bad Storm Recently?",
        [
            "As an Ace Roofing customer in the Dallas-Fort Worth, Texas area, it is important to schedule a roof inspection after your home or business recently suffered from severe weather. The unpredictable nature of storms, high winds, hail, and falling debris can result in damage to your roof. By conducting a thorough roof inspection, our roofers can promptly identify any visible signs of damage, such as missing or damaged shingles, water stains or leaks, dents in your gutters, to name a few, ensuring that necessary repairs or maintenance are carried out promptly.",
            "Inspecting your roof after severe weather not only allows Ace Roofing to address any existing damage but also helps prevent further issues from arising. Even minor damage, if left unattended, can lead to leaks, water damage, and even structural problems down the line. By taking proactive measures to inspect and address any damage, Ace Roofing ensures the longevity and durability of your roof in the Dallas-Fort Worth area.",
            "Furthermore, documenting any damage discovered during the inspection can be beneficial when filing insurance claims. Ace Roofing will thoroughly photograph and document the extent of the damage, providing you with the necessary evidence to support your claim and maximize your coverage.",
            "Above all, the safety of your home and family is paramount. Damaged roofs can pose safety risks, especially with loose or unstable materials. By conducting a roof inspection, Ace Roofing can identify any potential hazards, proactively ensuring the safety and security of your property.",
            "Remember that regular roof inspections, such as those provided by Ace Roofing, are recommended at least once a year, even in the absence of severe weather events. These inspections allow for the early detection of hidden damage and ensure the longevity of your roof, ultimately saving you money and providing peace of mind.",
        ],
    ),
    (
        "Has Your Roof Started Leaking?",
        [
            "If you notice a leak in your roof, it is essential to promptly schedule an inspection with Ace Roofing. While a leak may appear as a minor issue, it can indicate underlying damage that requires immediate attention. Our roofing professionals can conduct a thorough inspection to identify the source of the leak and prevent further water damage to your home or business.",
            "Early detection can save you from costly repairs and prevent further damage. Addressing a small leak promptly is always preferable to allowing it to worsen over time.",
            "While initial inspections can be done personally, it is advisable to consult professionals like Ace Roofing for a comprehensive assessment. We carry the knowledge, expertise, and specialized equipment needed to accurately evaluate the condition of your roof and provide appropriate solutions.",
        ],
    ),
    (
        "Are You Missing Shingles on the Roof?",
        [
            "Missing shingles can compromise the integrity of your roof, leading to potential leaks and further damage. As an experienced roofing company, we at Ace Roofing understand the importance of identifying and addressing missing shingles promptly. We will thoroughly assess the extent of the missing shingles and evaluate any potential underlying issues.",
        ],
    ),
    (
        "Is the Fiberglass from the Asphalt Shingle Visible?",
        [
            "If you notice visible fiberglass on your commercial or residential roof, it is advisable to schedule an inspection with our skilled roofers at Ace Roofing as soon as possible. Visible fiberglass can indicate potential issues with your roof and should be assessed by professionals.",
            "It is important to note that fiberglass is not typically intended to be exposed on asphalt shingle roofs. The presence of visible fiberglass could suggest that the shingles have deteriorated or experienced damage, compromising their effectiveness in protecting your property. We will examine the visible fiberglass and identify any underlying issues or potential damage that may require attention.",
        ],
    ),
    (
        "How Often Should You Have Your Roof Inspected?",
        [
            "As a general guideline, it is recommended to inspect your roof at least once a year. Regular roof inspections help identify any potential issues before they escalate into major problems, saving you from costly repairs and preventing further damage.",
            "We advise homeowners and business owners to consider more frequent inspections due to the varying weather conditions in the Dallas-Fort Worth, Texas area. Extreme heat, storms, and high winds can have an impact on the condition of your roof. Therefore, scheduling inspections every six months or after significant weather events is advisable.",
        ],
    ),
]


def home_body(r):
    faq = "".join(
        f'<details{" open" if i == 0 else ""}><summary>{e(q)}</summary><div class="faq__body">{paras(*a)}</div></details>'
        for i, (q, a) in enumerate(FAQ)
    )
    return f"""<section class="hero hero--home">
  {rimg(img("Screenshot+2023-10-25+9.18.25+AM-1920w.png"), "Aerial view of a Dallas-Fort Worth home roof", cls="hero__bg", priority=True, sizes=HERO_SIZES, widths=HERO_WIDTHS)}
  <div class="container">
    <div>
      <p class="hero__tagline">Don&rsquo;t Gamble Your Roof, Bet on ACE Roofing</p>
      <h1><span class="gold">Dallas-Fort Worth Roofing Contractor</span> That Gets It Done the First Time!</h1>
      <ul class="hero__list">
        <li>Free Inspection Within 24 Hours</li>
        <li>Full Roof Replacement</li>
        <li>24/7 Emergency Services</li>
      </ul>
      <div class="hero__actions">
        <a class="btn" href="{r}contact/">Contact Us Today!</a>
        <a class="btn btn--outline" href="tel:{PHONE}">{PHONE_DISPLAY}</a>
      </div>
    </div>
    {inspection_form()}
  </div>
</section>

<section class="section section--light" id="inspection">
  <div class="container">
    <div class="section-title center">
      <img class="spade-divider" src="{SPADE_BLACK}" alt="" width="70" height="72">
      <h2>When Do You Need A Professional Roof Inspection From ACE Roofing?</h2>
    </div>
    <div class="faq">{faq}</div>
  </div>
</section>

{cta_band(r)}

<section class="section" id="services">
  <div class="container">
    <div class="section-title center">
      <img class="spade-divider" src="{SPADE_GOLD}" alt="" width="70" height="72">
      <h2>Our Roofing Services</h2>
    </div>
    {cards(r, ["replace", "restore", "insurance", "repair", "storm", "commercial"])}
  </div>
</section>

<section class="section section--light" id="projects">
  <div class="container">
    <div class="section-title center">
      <h2>Check Out Our Recent Projects</h2>
    </div>
    {gallery_html(GALLERY)}
    <p class="center" style="margin-top:36px"><a class="btn btn--dark" href="{r}gallery/">View All Projects</a></p>
  </div>
</section>

<section class="section" id="why-ace">
  <div class="container split split--top">
    <div>
      {rimg(img("Screenshot+2023-10-25+9.22.04+AM-1920w.png"), "Aerial view of a Dallas-Fort Worth home with a new roof by ACE Roofing", sizes="(max-width: 960px) 100vw, 570px", cls="rounded", w=1200, h=800, widths=(480, 768, 1140))}
      <div class="testimonials" style="grid-template-columns:1fr;margin-top:30px">
        {testimonial("Ace Roofing has been an absolute pleasure to work with. Their professionalism, attention to detail and customer service is commendable. I am very satisfied with their roof repair service for my business and would highly recommend them to others.", "McKinney")}
        {testimonial("Our experience with Ace Roofing was exceptional. The team was highly skilled, efficient, and courteous. They addressed all our questions, gave us regular updates on their progress, and made sure that we were satisfied with the outcome.", "Plano")}
      </div>
    </div>
    <div class="prose">
      <img src="{SPADE_BLACK}" alt="" width="60" height="62" style="margin-bottom:14px">
      <h2>Why Ace Roofing?</h2>
      {paras(
        "Ace Roofing Company is a reliable choice for both your residential and commercial roofing needs in the Dallas-Fort Worth, Texas area. We have an experienced and professional team who offer top-notch roofing services that cater to the specific requirements of our clients.",
        "We have established ourselves in the industry as a trusted roofing contractor that genuinely cares about the safety and satisfaction of our clients. Our extensive knowledge and expertise allow us to handle a wide range of roofing projects, from straightforward repairs to long-term roof installation projects. We understand the unique challenges that come with the local climate and are well-equipped to provide effective solutions.",
        "Our goal is to deliver exceptional roofing solutions by ensuring clear communication, prompt response times, and attention to detail. Our professional approach and commitment to quality workmanship set us apart from other roofing companies in the area. Whether it's a residential property or a commercial building, we work closely with our clients to understand their needs and exceed their expectations.",
        "To learn more about our services and our process and to schedule a free roof inspection, give us a call and one of our representatives would be more than happy to assist you.",
      )}
      <a class="btn" href="tel:{PHONE}">{ICON_PHONE.replace('<svg', '<svg width="18" height="18" style="fill:currentColor"')} Call {PHONE_DISPLAY}</a>
    </div>
  </div>
</section>

<section class="section section--light" id="service-areas">
  <div class="container narrow center">
    <span class="eyebrow">Service Areas</span>
    <h2>Roofing Contractor Serving the Dallas-Fort Worth Metroplex</h2>
    <p>ACE Roofing provides roof inspections, roof replacement, roof repair, roof restoration, hail and storm damage repair and commercial roofing for homeowners and businesses throughout North Texas, including:</p>
    <ul class="areas">{"".join(f"<li>{e(c)}, TX</li>" for c in AREAS)}</ul>
    <p>Not sure if we cover your neighborhood? Call <a href="tel:{PHONE}">{PHONE_DISPLAY}</a> &mdash; if you&rsquo;re in the DFW area, we&rsquo;ll come to you with a free roof inspection within 24 hours.</p>
  </div>
</section>

<section class="section section--dark" id="reviews">
  <div class="container">
    <div class="section-title center">
      <img class="spade-divider" src="{SPADES_ROW}" alt="" style="width:200px" width="200" height="38">
      <h2>Why People Believe In Us!</h2>
    </div>
    <div class="testimonials">
      {testimonial("Ace Roofing has been my go-to roofing company ever since they installed the roof for my home. Whenever I needed a roof inspection after a storm, they always treated me and my family with respect. I highly recommend them for all your roofing needs.", "Frisco")}
      {testimonial("I had a wonderful experience with Ace Roofing. Their team was knowledgeable, hardworking, and took great care to ensure that my roof was installed correctly. They left the job site clean and tidy. I am very impressed with their service.", "Murphy")}
      {testimonial("I needed storm damage repair for my roof and Ace Roofing was there to help me from start to finish. Their roofers were prompt, helpful, and incredibly meticulous when it came to doing repairs and installing new shingles.", "Allen")}
      {testimonial("These guys are nothing but great. I had an issue with roof leaks so I decided to call and ask for an estimate. They did not take advantage of my situation and instead they explained to me my problem and what was the best way to fix it without going over budget.", "Sachse")}
    </div>
  </div>
</section>

{cta_band(r, "Contact Us Today!")}"""


page(
    "",
    "Roofing Contractor in Dallas-Fort Worth, TX | ACE Roofing",
    "Dallas-Fort Worth roofing contractor for roof replacement, roof repair and hail & storm damage. Free roof inspection within 24 hours, 24/7 emergency service.",
    home_body,
    extra_schema=[{
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": " ".join(a)}}
            for q, a in FAQ
        ],
    }],
)


# --------------------------------------------------------------------------
# ABOUT
# --------------------------------------------------------------------------
def about_body(r):
    principles = [
        ("Efficiency", "Our experienced team employs a systematic approach to project management, ensuring that every phase, from planning to execution, is carried out within the stipulated timeline. We strive to minimize disruption to your daily activities while delivering top-notch roofing services."),
        ("Precision", "We believe in getting it right the first time. From the initial assessment and cost estimation to the final installation, every step is executed with meticulous precision. We leverage cutting-edge technology and tools for accurate measurements, detailed schematics, and precise installations, reducing the margin for error and ensuring optimal use of resources."),
        ("Quality of Work", "At Ace Roofing, quality is not just a buzzword; it is a commitment. From terracotta tiles to metal roofs, we use only superior-grade materials and state-of-the-art equipment in all our projects. Our team of skilled professionals follows industry best practices to deliver durable and robust roofing solutions that can withstand the test of time and weather."),
        ("Customer Service", "We place the highest importance on customer satisfaction. Our customer service team is always accessible to answer your questions, provide timely updates, and ensure a seamless experience from the initial consultation to project completion. We believe in building lasting relationships with our clients through open communication, transparent dealings, and unwavering dedication to their satisfaction."),
    ]
    pr = "".join(f'<div class="benefit"><h3>{e(t)}</h3><p>{e(d)}</p></div>' for t, d in principles)
    return f"""{page_hero(r, "About ACE Roofing", "ACE Roofing provides comprehensive residential and commercial roofing services to ensure your home or business looks great and remains protected for many years.", img("ace-crew-installing-shingles-1920w.jpg"), alt="ACE Roofing crew installing new shingles on a Dallas-Fort Worth home")}

<section class="section">
  <div class="container split">
    <div class="prose">
      <span class="eyebrow">Who We Are</span>
      <h2>Rooted in Dallas-Fort Worth</h2>
      {paras(
        "Ace Roofing Company is a reliable choice for both residential and commercial roofing needs in the Dallas-Fort Worth, Texas area. Our deep-seated roots in our community have fostered a strong sense of responsibility towards our neighbors. Leveraging our rich experience and intimate understanding of local architectural nuances and climatic conditions, we provide roofing solutions that are not just functional, but also aesthetically congruous with the surrounding environment.",
        "At Ace Roofing, we firmly believe that being a trusted roofing contractor extends beyond technical expertise. Our service delivery is guided by four fundamental principles:",
      )}
    </div>
    <div class="photo-grid">
      {rimg(img("ace-team-member-roof-selfie-tall-1920w.jpg"), "ACE Roofing team member on a shingle roof in Dallas-Fort Worth", sizes="(max-width: 960px) 50vw, 280px", w=600, h=800, widths=(320, 480, 640))}
      {rimg(img("ace-team-client-consultation-1920w.jpg"), "ACE Roofing team member reviewing a roofing project with a DFW homeowner", sizes="(max-width: 960px) 50vw, 280px", w=600, h=800, widths=(320, 480, 640))}
    </div>
  </div>
</section>

<section class="section section--light">
  <div class="container">
    <div class="section-title center">
      <img class="spade-divider" src="{SPADE_GOLD}" alt="" width="70" height="72">
      <h2>Our Four Principles</h2>
    </div>
    <div class="principles">{pr}</div>
  </div>
</section>

<section class="section">
  <div class="container split">
    {rimg(img("touch_v1-1920w.png"), "ACE Roofing roofer on a newly installed shingle roof in North Texas", sizes="(max-width: 960px) 100vw, 570px", cls="rounded", w=1200, h=800, widths=(480, 768, 1140))}
    <div class="prose">
      {paras(
        "At Ace Roofing, these core principles are not just theoretical concepts but the very foundation of our operations. As a result, we are able to consistently deliver a superior roofing service that not only fulfills but surpasses your expectations. Trust Ace Roofing for all your roofing needs - where exceptional craftsmanship and customer satisfaction are our highest priorities.",
      )}
      <a class="btn" href="{r}contact/">Contact Us Today!</a>
    </div>
  </div>
</section>

{cta_band(r)}"""


page(
    "about-us/",
    "About ACE Roofing | Dallas-Fort Worth Roofing Company",
    "Meet ACE Roofing, a Dallas-Fort Worth roofing company built on efficiency, precision, quality work and customer service. Residential and commercial roofing.",
    about_body,
    crumbs=[("About Us", "about-us/")],
    page_type="AboutPage",
)


# --------------------------------------------------------------------------
# SERVICES OVERVIEW / RESIDENTIAL / COMMERCIAL
# --------------------------------------------------------------------------
def services_body(r):
    return f"""{page_hero(r, "Roofing Services in Dallas-Fort Worth", "ACE Roofing provides comprehensive residential and commercial roofing services. Our expertise guarantees that your property will not only look great but will also stay protected for years to come.", img("Screenshot+2023-10-25+9.18.25+AM-1920w.png"), alt="Aerial view of a Dallas-Fort Worth neighborhood roof")}
<section class="section">
  <div class="container">
    {cards(r, ["replace", "repair", "restore", "storm", "insurance", "commercial"])}
  </div>
</section>
<section class="section section--light">
  <div class="container split split--top">
    <div class="prose">
      <span class="eyebrow">Residential Roofing</span>
      <h2>Roofing For DFW Homeowners</h2>
      <p>From a few blown-off shingles to a complete tear-off, ACE Roofing handles every kind of residential roofing project in the Dallas-Fort Worth area. We start with a free roof inspection within 24 hours, explain exactly what we find, and only recommend a full replacement when it is truly the most cost-effective option for your family.</p>
      <p><a href="{r}our-services/residential-roofing/">Explore residential roofing &rarr;</a></p>
    </div>
    <div class="prose">
      <span class="eyebrow">Commercial Roofing</span>
      <h2>Roofing For DFW Businesses</h2>
      <p>Offices, retail spaces and other commercial properties across North Texas rely on ACE Roofing for replacements, repairs, restorations, storm damage repair and ongoing maintenance. We plan every phase around your schedule to keep disruption to your business to a minimum.</p>
      <p><a href="{r}our-services/commercial-roofing/">Explore commercial roofing &rarr;</a></p>
    </div>
  </div>
</section>
{cta_band(r)}"""


page(
    "our-services/",
    "Roofing Services in Dallas-Fort Worth | ACE Roofing",
    "Roof replacement, repair, restoration, hail & storm damage repair, insurance claims and commercial roofing across Dallas-Fort Worth. Free inspections.",
    services_body,
    crumbs=[("Our Services", "our-services/")],
    page_type="CollectionPage",
)


def residential_body(r):
    return f"""{page_hero(r, "Residential Roofing in Dallas-Fort Worth", "Ace Roofing is your one-stop shop for all your residential roofing needs. Let's secure a safer and more aesthetically pleasing roof for your home.", img("Screenshot+2026-11-17+at+4.52.27-PM-1920w.png"), alt="Residential roof by ACE Roofing in Dallas-Fort Worth")}
<section class="section">
  <div class="container">
    {cards(r, ["replace", "repair", "restore", "storm"], "cards cards--2")}
  </div>
</section>
<section class="section section--light">
  <div class="container narrow prose center">
    <img class="spade-divider" src="{SPADE_BLACK}" alt="" width="70" height="72">
    <h2>Protecting North Texas Homes From Hail, Wind &amp; Heat</h2>
    <p>Dallas-Fort Worth roofs take a beating: spring hail storms, high winds and long stretches of extreme summer heat all shorten the life of shingles, flashing and underlayment. ACE Roofing&rsquo;s residential team inspects, repairs, restores and replaces roofs on homes throughout the metroplex, so small problems get fixed before they turn into leaks, water damage or structural issues.</p>
    <p>Every project starts with a free roof inspection within 24 hours. If your roof was damaged in a storm, we photograph and document everything you need to support your insurance claim. And if you have an emergency, we&rsquo;re available 24/7.</p>
    <a class="btn" href="{r}contact/">Schedule A Free Inspection</a>
  </div>
</section>
{cta_band(r)}"""


page(
    "our-services/residential-roofing/",
    "Residential Roofing in Dallas-Fort Worth | ACE Roofing",
    "Residential roofing in Dallas-Fort Worth: roof replacement, repair, restoration and hail & storm damage repair with insurance claim help. Free inspections.",
    residential_body,
    crumbs=[("Our Services", "our-services/"), ("Residential Roofing", "our-services/residential-roofing/")],
    page_type="CollectionPage",
)


def commercial_body(r):
    images = {
        "replace": img("roofing+replacement-1920w.jpg"),
        "restore": img("04-ee4676b9-1920w.jpg"),
        "maintenance": IMG_COMMERCIAL,
    }
    return f"""{page_hero(r, "Commercial Roofing in Dallas-Fort Worth", "We at Ace Roofing provide a comprehensive range of commercial roofing services designed to protect and enhance the value of your business property.", IMG_COMMERCIAL, alt="Commercial building roof in Dallas-Fort Worth")}
<section class="section">
  <div class="container">
    {cards(r, ["replace", "repair", "restore", "storm", "insurance", "maintenance"], images=images)}
  </div>
</section>
<section class="section section--light">
  <div class="container narrow prose center">
    <img class="spade-divider" src="{SPADE_BLACK}" alt="" width="70" height="72">
    <h2>A Commercial Roofing Contractor That Works Around Your Business</h2>
    <p>Your roof protects your inventory, your equipment, your employees and your customers. ACE Roofing provides commercial roof replacement, roof repair, roof restoration, storm damage repair, insurance claim assistance and preventative roof maintenance for business owners and property managers throughout the Dallas-Fort Worth area.</p>
    <p>We follow a systematic project plan so every phase, from inspection to final clean-up, is finished on schedule with as little disruption to your operations as possible. Call us for a free commercial roof inspection, or any time for 24/7 emergency service.</p>
    <a class="btn" href="{r}contact/">Request A Commercial Roof Inspection</a>
  </div>
</section>
{cta_band(r)}"""


page(
    "our-services/commercial-roofing/",
    "Commercial Roofing in Dallas-Fort Worth | ACE Roofing",
    "Commercial roofing contractor in Dallas-Fort Worth: roof replacement, repair, restoration, maintenance, storm damage and insurance claims. Free inspections.",
    commercial_body,
    crumbs=[("Our Services", "our-services/"), ("Commercial Roofing", "our-services/commercial-roofing/")],
    extra_schema=[{
        "@type": "Service",
        "name": "Commercial Roofing",
        "serviceType": "Commercial roofing",
        "provider": {"@id": BUSINESS_ID},
        "areaServed": {"@type": "AdministrativeArea", "name": "Dallas-Fort Worth metroplex, Texas"},
        "url": canonical_for("our-services/commercial-roofing/"),
    }],
)


# --------------------------------------------------------------------------
# SERVICE DETAIL PAGES
# --------------------------------------------------------------------------
SERVICE_KEYS = {
    "our-services/residential-roofing/roof-replacement/": "replace",
    "our-services/residential-roofing/roof-repair/": "repair",
    "our-services/residential-roofing/roof-restoration/": "restore",
    "our-services/residential-roofing/storm-damage-repair/": "storm",
}
SEO = {
    "replace": ("Roof Replacement in Dallas-Fort Worth, TX | ACE Roofing",
                "Roof replacement in Dallas-Fort Worth: full tear-off, new underlayment, flashing and ventilation, done right the first time. Free inspection within 24 hours.",
                "Roof Replacement in Dallas-Fort Worth"),
    "repair": ("Roof Repair in Dallas-Fort Worth, TX | ACE Roofing",
               "Roof repair in Dallas-Fort Worth for leaks, missing or damaged shingles, flashing and storm damage. Free inspection within 24 hours, 24/7 emergency service.",
               "Roof Repair in Dallas-Fort Worth"),
    "restore": ("Roof Restoration in Dallas-Fort Worth | ACE Roofing",
                "Roof restoration in Dallas-Fort Worth: repairs, cleaning and a protective coating to extend your roof's life and delay replacement. Free inspection.",
                "Roof Restoration in Dallas-Fort Worth"),
    "storm": ("Hail & Storm Damage Roof Repair in DFW | ACE Roofing",
              "Hail and storm damage roof repair in Dallas-Fort Worth, with documented reports for your insurance claim. Free inspection in 24 hours. 24/7 emergency service.",
              "Hail &amp; Storm Damage Roof Repair in Dallas-Fort Worth"),
}


def service_page(path, title, meta, h1, intro, hero_img, what_h, what, benefits_h, benefits, why_h, why, side_img):
    key = SERVICE_KEYS[path]
    service_name = h1
    title, meta, h1 = SEO[key]
    h1 = html.unescape(h1)
    others = [k for k in ["replace", "repair", "restore", "storm"] if k != key] + ["commercial"]

    def body(r):
        b = "".join(f'<div class="benefit"><h3>{e(t)}</h3><p>{e(d)}</p></div>' for t, d in benefits)
        return f"""{page_hero(r, h1, intro, hero_img, alt=f"{service_name} project by ACE Roofing in Dallas-Fort Worth")}
<section class="section">
  <div class="container split split--top">
    <div class="prose">
      <span class="eyebrow">The Process</span>
      <h2>{e(what_h)}</h2>
      {paras(*what)}
    </div>
    <div>
      {rimg(side_img, f"{service_name} by ACE Roofing in Dallas-Fort Worth, TX", sizes="(max-width: 960px) 100vw, 570px", cls="rounded", w=1200, h=800, widths=(480, 768, 1140))}
      <div style="margin-top:30px">{inspection_form("h3")}</div>
    </div>
  </div>
</section>
<section class="section section--light">
  <div class="container">
    <div class="section-title center">
      <img class="spade-divider" src="{SPADE_GOLD}" alt="" width="70" height="72">
      <h2>{e(benefits_h)}</h2>
    </div>
    <div class="benefits">{b}</div>
  </div>
</section>
<section class="section">
  <div class="container narrow prose center">
    <img class="spade-divider" src="{SPADE_BLACK}" alt="" width="70" height="72">
    <h2>{e(why_h)}</h2>
    {paras(*why)}
    <a class="btn" href="{r}contact/">Contact Us Today!</a>
  </div>
</section>
<section class="section section--light">
  <div class="container">
    <div class="section-title center">
      <h2>More Roofing Services in Dallas-Fort Worth</h2>
    </div>
    {cards(r, others[:3])}
  </div>
</section>
{cta_band(r)}"""

    page(
        path, title, meta, body,
        crumbs=[("Our Services", "our-services/"), ("Residential Roofing", "our-services/residential-roofing/"),
                (service_name, path)],
        extra_schema=[{
            "@type": "Service",
            "name": service_name,
            "serviceType": service_name,
            "description": meta,
            "provider": {"@id": BUSINESS_ID},
            "areaServed": [{"@type": "AdministrativeArea", "name": "Dallas-Fort Worth metroplex, Texas"}]
            + [{"@type": "City", "name": f"{c}, TX"} for c in AREAS],
            "url": canonical_for(path),
        }],
    )


service_page(
    "our-services/residential-roofing/roof-replacement/",
    "Residential Roof Replacement Services | Ace Roofing | Dallas, Fort Worth TX",
    "Ace Roofing: Roof replacement for residential & commercial properties. Contact us for a seamless, robust roof. Enhance aesthetics, energy efficiency, home value & insurance coverage.",
    "Roof Replacement",
    "Ace Roofing is your trusted partner for comprehensive roof replacement solutions. We bring our expertise and commitment to quality to every project, ensuring a seamless and robust roof over your head.",
    img("Screenshot+2026-11-17+at+4.52.27-PM-1920w.png"),
    "What is Residential Roof Replacement and The Process?",
    [
        "Residential roof replacement involves the complete replacement of an existing roof on a residential property. It is a meticulous process that encompasses the removal of old roof materials, thorough inspection and repair of the underlying structure if necessary, and the precise installation of new roofing materials to ensure a durable and watertight covering for the house. This essential service aims to maintain the integrity of a home's roof and safeguard it from the harsh elements.",
        "The process of residential roof replacement follows a systematic approach to achieve a successful outcome. It begins with an initial roof inspection by a professional roofing contractor to assess the condition of the existing roof and determine if a complete replacement is necessary. Once the decision is made, homeowners can select the desired roofing materials based on factors like budget, durability, and climate suitability. The old roof materials are then carefully removed, allowing the roofing contractor to inspect and repair the underlying structure as needed. Following this, the installation process commences, involving the strategic placement and securing of each roofing component. From drip edges to underlayment, flashing to ventilation, every step is executed meticulously to create a robust and watertight roof. Ultimately, the completion of the residential roof replacement is marked by a thorough clean-up and final inspection to ensure adherence to quality standards and specifications.",
    ],
    "The Benefits Of Having A Roof Replacement Service",
    [
        ("Increase Home Value", "Installing a new roof can significantly increase the value of a home. It enhances curb appeal and provides potential buyers with confidence in the overall condition of the property."),
        ("Maintain Insurance Coverage", "Insurance companies often require homes to have a well-maintained and structurally sound roof to provide coverage. By replacing an old roof, homeowners can ensure they meet insurance requirements and maintain coverage."),
        ("Improve Energy Efficiency", "A new roof with modern materials and proper insulation can improve a home's energy efficiency. It helps regulate temperature, reduce heating and cooling costs, and create a more comfortable living environment."),
        ("Enhance Aesthetics", "Replacing an old roof gives homeowners the opportunity to update the look of their home. With a new roof, they can choose from a variety of materials, colors, and styles to improve the overall appearance and give their home a fresh makeover."),
    ],
    "Why Ace Roofing for Residential Roof Replacement Service?",
    [
        "Ace Roofing is a reputable roofing company specializing in residential roof replacement. We have a team of experienced professionals who are well-versed in residential roof replacements. Our roofers have the knowledge and skills to assess the condition of roofs, recommend suitable replacement options, and execute the installation with precision and quality craftsmanship.",
        "Being based in the Dallas-Fort Worth Texas area, we at Ace Roofing understand the unique roofing needs of homeowners in the region. We are familiar with local weather conditions and regulations, ensuring that our clients' roof replacements are tailored to withstand the specific challenges faced in the area. Rest assured that we will only recommend a complete overhaul if we see that it is the most cost-effective and efficient option for you and your family. Call us today to schedule a free roof inspection and to learn more about our services.",
    ],
    IMG_REPLACE,
)

service_page(
    "our-services/residential-roofing/roof-repair/",
    "Residential Roof Repair Services | Ace Roofing | Dallas, Fort Worth TX",
    "Ace Roofing - Reliable roof repair services for your home in Dallas-Fort Worth. Leaks, shingles, flashing and storm damage. Contact us today!",
    "Roof Repair",
    "Ace Roofing is your reliable provider of superior roof repair services. We specialize in delivering professional, high-quality roofing solutions designed to meet the unique needs of your home.",
    img("Screenshot+2026-11-17+at+4.52.47-PM-1920w.png"),
    "What is Residential Roof Repair and The Process?",
    [
        "Residential roof repair is a specialized discipline that focuses on diagnosing and rectifying issues associated with the structural integrity and functionality of a home's roof. This practice requires a deep understanding of roofing systems and their components, as well as the ability to apply this knowledge to ensure the roof's optimal performance and aesthetics. Key types of roof repairs include fixing leaks, repairing or replacing damaged or missing shingles, addressing issues with flashing, and dealing with storm damage.",
        "At Ace Roofing, our process for repairing roofs is thorough and meticulous. We begin with a comprehensive roof inspection to identify the problem areas. Based on our findings, we devise a detailed plan that addresses the issues while considering your budget and timeline. Our team of experienced roofers then executes this plan with precision and efficiency. The importance of hiring professional residential roofing contractors who are currently based in your area cannot be overstated; proper roof repair requires specialized knowledge and skills to ensure your roof remains durable and effective for years to come.",
    ],
    "The Benefits Of Having A Residential Roof Repair Service",
    [
        ("Extended Lifecycle", "One of the most significant benefits of timely, professional roof repair is the extended lifecycle of your roof. Regular maintenance and prompt repairs can prevent minor issues from escalating into major problems, thereby prolonging the roof's lifespan."),
        ("Cost-Effectiveness", "Professional roof repair contractors have access to quality materials at lower costs due to their relationships with suppliers. Our expertise in the field helps ensure effective and efficient repairs, reducing the potential for additional costs."),
        ("Energy Efficiency", "Properly maintained roofs contribute to a home's energy efficiency. We can help you ensure proper insulation and ventilation, which can significantly minimize heating and cooling costs."),
        ("Warranty Protection", "Many professional roofing companies offer warranties on their work. This warranty protection means that if issues arise within the specified period, the company will handle necessary repairs or replacements at no additional cost to you."),
    ],
    "Why Ace Roofing for Residential Roof Repair Service?",
    [
        "Ace Roofing is not just a roofing company, we are your trusted partners in maintaining the integrity of your home. Our extensive experience, coupled with our commitment to customer satisfaction, makes us the ideal choice for residential roof repair services in the Dallas-Fort Worth, Texas area. We take pride in our work and treat each project with the utmost professionalism and dedication.",
        "When you choose Ace Roofing, you are not just hiring a roofing contractor; you are investing in your peace of mind. We stand by the quality of our work and are always ready to go the extra mile to ensure your complete satisfaction. Don't let roof issues compromise your family's safety and bother you any longer. Contact us today for a comprehensive and professional roof repair service and for a free roof inspection. Let our expertise work for you.",
    ],
    IMG_REPAIR,
)

service_page(
    "our-services/residential-roofing/roof-restoration/",
    "Residential Roof Restoration | Ace Roofing | Dallas, Fort Worth TX",
    "Ace Roofing: Expert residential roof restoration services. Quality workmanship and exceptional customer service. Free roof inspection and consultation.",
    "Roof Restoration",
    "At Ace Roofing, we take pride in offering top-notch residential roof restoration services that breathe new life into your home. Our team of expert roofers is dedicated to providing quality workmanship and exceptional customer service every time.",
    img("Screenshot+2026-11-17+at+4.52.38-PM-1920w.png"),
    "What is Residential Roof Restoration and The Process?",
    [
        "Residential roof restoration is a comprehensive process that involves the repair, cleaning, and re-coating of a roof. It is a proactive maintenance strategy designed to extend the lifespan of your roof, improve its appearance, and enhance its performance. Over time, roofs can deteriorate due to weather conditions, aging, and other factors. This can lead to leaks, energy inefficiency, and an unattractive appearance. Roof restoration addresses these issues, restoring your roof to its original condition or even better.",
        "At Ace Roofing, our roof restoration process begins with a thorough inspection to identify any potential problems. After this, we carry out necessary repairs, clean the roof to remove debris and algae, and then apply a protective coating. The importance of hiring skilled and experienced roofing professionals like our team cannot be overstated. We ensure that the job is done right the first time, saving you time and money in the long run. We also prioritize safety and adhere to all industry regulations, giving you peace of mind.",
    ],
    "The Benefits Of Having A Roof Restoration Service",
    [
        ("Extended Roof Life", "Our expert roof restoration services at Ace Roofing revitalize your roof, repairing damages and reinforcing weak sections, effectively prolonging its service life and delaying the need for a full replacement."),
        ("Improved Energy Efficiency", "The improved thermal efficiency from roof restoration can lower your home's interior temperature during hot seasons, leading to reduced energy consumption and substantial savings on your energy bills."),
        ("Enhanced Curb Appeal", "We will roll up our sleeves to transform your roof and give your home a refreshed, attractive look. This can drastically help in increasing your home's value and make it more attractive to potential buyers."),
        ("Preventative Maintenance", "During regular roof restoration, your roofing contractor should be able to identify and rectify minor issues before they escalate into major problems. This proactive approach can save you from unexpected repair costs."),
    ],
    "Why Ace Roofing for Residential Roof Restoration Service?",
    [
        "Choosing Ace Roofing for your residential roof restoration needs means choosing a roofing company with a track record of excellence. Currently serving homeowners in the Dallas-Fort Worth, Texas area, our team is highly skilled and experienced, ensuring that your roof restoration project is handled with the utmost care and attention to detail. We use top-quality materials and utilize the latest techniques, providing you with a roof that not only looks great but performs exceptionally as well.",
        "We understand that roof restoration is a significant investment, and we are here to guide you through the process, answering any questions you might have and providing regular updates on our progress. Give your roof the care it deserves with Ace Roofing's residential roof restoration services. Contact us today for a free roof inspection and consultation and let our team restore your roof to its optimal condition.",
    ],
    IMG_RESTORE,
)

service_page(
    "our-services/residential-roofing/storm-damage-repair/",
    "Residential Storm Damage Repair | Ace Roofing | Dallas, Fort Worth TX",
    "Ace Roofing: Expert storm damage repair & insurance claim assistance in Dallas-Fort Worth, Texas area.",
    "Storm Damage Repair",
    "At Ace Roofing, we offer robust and comprehensive residential storm damage repair services that restore the integrity of your home and ensure your peace of mind.",
    img("Roof+Replacements-1920w.jpg"),
    "What is Residential Storm Damage Repair and The Process?",
    [
        "Residential storm damage repair requires meticulous assessment and repairs of roof damages incurred by a home during severe weather conditions. This often includes hail, wind, rain, or snow damage that can compromise the aesthetic appeal and structural integrity of a home, particularly the roof. It is an essential residential roofing service that ensures the safety of your family and the longevity of your property.",
        "Our storm damage repair process at Ace Roofing begins with a thorough inspection of your property to identify all areas affected by the storm. We then prepare a detailed report outlining the necessary repairs that can be used for proper documentation and filing for insurance claims. Our skilled and experienced roofers then set to work, using top-quality materials and modern techniques to ensure a durable repair job. While there are many roofing contractors in the Dallas-Fort Worth, Texas area, it is important to choose a team like Ace Roofing that carries tremendous experience and expertise for the job. A less experienced team may miss subtle signs of damage, leading to leaks, mold growth, or even structural instability over time.",
    ],
    "The Benefits Of Having A Storm Damage Repair Service",
    [
        ("Preventing Further Damage", "Timely repair of storm damage is crucial in preventing further deterioration of your home. If left unattended, small issues can escalate into major problems, leading to more costly repairs down the line. A professional service ensures all damages are promptly addressed, saving you from potential financial burdens."),
        ("Ensuring Safety", "The safety of your family is paramount. Damages caused by storms can compromise the structural integrity of your home, posing potential hazards. A professional storm damage repair service identifies and rectifies these issues, ensuring your living environment remains safe and secure."),
        ("Maintaining Home Value", "Your home is a significant investment. Regular maintenance, especially after a storm, is essential in preserving its value. By fixing storm-induced damages promptly and professionally, you ensure the longevity of your property, thereby maintaining its market value in the long run."),
        ("Insurance Claim Assistance", "Navigating insurance claims can be complex and confusing. A professional storm repair service not only fixes the damages but also provides detailed reports outlining the extent of the damage. This documentation is invaluable when filing insurance claims, helping you get the compensation you deserve."),
    ],
    "Why Ace Roofing for Residential Storm Damage Repair?",
    [
        "In the wake of a storm, you need a reliable, professional team on your side - and that's where Ace Roofing comes in. We understand the intricacies of storm damage and how to effectively combat it. We take pride in our meticulous attention to detail, ensuring no issue goes unnoticed and unaddressed.",
        "We are not just roofers; we are your partners in maintaining a safe and secure home. We work closely with you, keeping you informed every step of the way and ensuring our work aligns with your expectations. Don't let storm damage compromise your home or your safety. Contact Ace Roofing today for a comprehensive residential storm damage repair service that you can trust. We also offer free roof inspections upon request.",
    ],
    IMG_STORM,
)


# --------------------------------------------------------------------------
# GALLERY
# --------------------------------------------------------------------------
def gallery_body(r):
    return f"""{page_hero(r, "Recent Roofing Projects in Dallas-Fort Worth", "At Ace Roofing, we take immense pride in the quality and precision of our work. Here are some of our most recent projects, each one showcasing our unwavering commitment to excellence in all types of roofing services.", img("08-1920w.jpg"), alt="Brick home with a new roof by ACE Roofing")}
<section class="section">
  <div class="container">
    {gallery_html(GALLERY, "gallery gallery--3")}
  </div>
</section>
{cta_band(r)}"""


page(
    "gallery/",
    "Roofing Projects in Dallas-Fort Worth | ACE Roofing",
    "See recent roof replacement and roof repair projects completed by ACE Roofing for homeowners across Dallas-Fort Worth. Request your free roof inspection.",
    gallery_body,
    crumbs=[("Recent Projects", "gallery/")],
    page_type="CollectionPage",
)


# --------------------------------------------------------------------------
# CONTACT
# --------------------------------------------------------------------------
def contact_body(r):
    services = ["Residential Roofing", "Roof Replacement", "Roof Repair", "Roof Restoration", "Storm Damage Repair", "Commercial Roofing", "Insurance Claims", "Free Inspection"]
    opts = "".join(f"<option>{e(s)}</option>" for s in services)
    return f"""{page_hero(r, "Contact ACE Roofing", "If you have any questions, require a roof inspection, or wish to discuss your roofing needs, we encourage you to reach out to us at Ace Roofing.", img("Screenshot+2023-10-25+9.21.41+AM-1920w.png"), button=False, alt="Aerial view of a Dallas-Fort Worth home roof")}
<section class="section">
  <div class="container contact-grid">
    <aside class="contact-info">
      <h2>Talk To ACE Roofing</h2>
      <p>Free inspection within 24 hours and 24/7 emergency service across Dallas-Fort Worth.</p>
      <ul>
        <li>{ICON_PHONE}<div><small>Call</small><a href="tel:{PHONE}">{PHONE_DISPLAY}</a></div></li>
        <li>{ICON_PIN}<div><small>Service Area</small>Dallas-Fort Worth, Texas</div></li>
        <li>{ICON_CLOCK}<div><small>Hours</small>24/7 Emergency Services</div></li>
      </ul>
      <a class="btn btn--block" href="tel:{PHONE}" style="margin-top:10px">Click To Call</a>
      <div class="social" style="margin-top:24px">{social_links()}</div>
    </aside>
    <form class="form-card" data-contact-form novalidate>
      <h2>Let&rsquo;s Discuss Your Roofing Project With Us!</h2>
      <input type="hidden" name="_subject" value="New contact form message — aceroofingtx.com">
      <div class="form-grid">
        <div class="field full"><label for="c-name">Name</label><input id="c-name" name="name" autocomplete="name" required></div>
        <div class="field"><label for="c-phone">Phone #</label><input id="c-phone" type="tel" name="phone" autocomplete="tel" required></div>
        <div class="field"><label for="c-email">Email</label><input id="c-email" type="email" name="email" autocomplete="email" required></div>
        <div class="field full"><label for="c-service">Services</label><select id="c-service" name="service"><option value="">Select a service</option>{opts}</select></div>
        <div class="field full"><label for="c-msg">Message</label><textarea id="c-msg" name="message"></textarea></div>
        <input class="hp" type="text" name="_honey" tabindex="-1" autocomplete="off" aria-hidden="true">
        <div class="full"><button class="btn btn--block" type="submit">Send Message</button></div>
      </div>
      <div class="form-status" role="status" aria-live="polite"></div>
    </form>
  </div>
</section>"""


page(
    "contact/",
    "Contact ACE Roofing | Free Roof Inspection in DFW",
    "Call (956) 534-2911 or request a free roof inspection online. ACE Roofing serves homes and businesses across Dallas-Fort Worth with 24/7 emergency service.",
    contact_body,
    crumbs=[("Contact Us", "contact/")],
    page_type="ContactPage",
)


# --------------------------------------------------------------------------
# 404 (written to root as 404.html)
# --------------------------------------------------------------------------
def nf_body(r):
    return f"""<section class="not-found">
  <div class="container">
    <img class="spade-divider" src="{SPADE_GOLD}" alt="" width="70" height="72">
    <h1>Page Not Found</h1>
    <p>Sorry, we couldn&rsquo;t find that page. Let&rsquo;s get you back on track.</p>
    <p><a class="btn" href="/">Back To Home</a> <a class="btn btn--dark" href="tel:{PHONE}">{PHONE_DISPLAY}</a></p>
  </div>
</section>"""


PAGES_FOR_SITEMAP = list(PAGES)
# 404 must use root-absolute asset paths because it is served at any URL.
page("__404/", "Page Not Found | ACE Roofing", "The page you are looking for could not be found.", nf_body)
src = os.path.join(OUT, "__404", "index.html")
with open(src) as f:
    doc = f.read().replace('href="../', 'href="/').replace('src="../', 'src="/')
doc = doc.replace('<meta name="robots" content="index, follow, max-image-preview:large">', '<meta name="robots" content="noindex">', 1)
doc = _re.sub(r'<link rel="canonical"[^>]*>\n', '', doc)
with open(os.path.join(OUT, "404.html"), "w") as f:
    f.write(doc)
os.remove(src)
os.rmdir(os.path.join(OUT, "__404"))

PRIORITY = {"": "1.0", "our-services/": "0.9", "contact/": "0.9"}
with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    for p in PAGES_FOR_SITEMAP:
        pr = PRIORITY.get(p, "0.8")
        f.write(f"  <url><loc>{canonical_for(p)}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority></url>\n")
    f.write("</urlset>\n")
with open(os.path.join(OUT, "robots.txt"), "w") as f:
    f.write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")

print("built", len(PAGES_FOR_SITEMAP), "pages + 404")
