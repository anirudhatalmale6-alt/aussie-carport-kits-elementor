# Aussie Carport Kits — Elementor landing page template

Elementor page template that recreates `aussie_carport_kits_conversion_redesign.html`
section for section, built with Elementor flexbox containers and core widgets
(plus the Elementor **Pro** Form widget for the quote form).

**File to import:** `aussie-carport-kits-landing-template.json`
(also provided as `aussie-carport-kits-template.zip` if your browser won't download the
raw .json — unzip it first, Elementor needs the .json itself, not the zip)

---

## How to install

1. WordPress admin → **Templates → Saved Templates → Import Templates**.
2. Upload `aussie-carport-kits-landing-template.json` and click **Import Now**.
3. Create your new page → **Edit with Elementor**.
4. In the editor, open the **folder icon** (Add Template) → **My Templates** tab →
   find *Aussie Carport Kits — Conversion Landing Page* → **Insert**.
5. When Elementor asks **"Import Document Settings?"**, choose **Yes**. That applies the
   Elementor Canvas page layout. If you click **No**, the page keeps your theme's own
   template, which wraps the design in your theme's container — that can push content
   sideways and will show your theme's header and footer around it. You can switch it
   later on the page: **Settings** (gear, bottom-left) → **Page Layout → Elementor Canvas**.
6. Publish.

The design no longer carries its own announcement bar or nav header — the hero photo card
is the first thing on the page. It still has its own footer and a mobile-only sticky CTA
bar at the very bottom; delete those two containers if your theme already provides them.

---

## Requirements

- Elementor **Pro** active (needed for the quote form).
- Elementor 3.16 or newer (flexbox containers). Built and tested against Elementor 4.3.3.
- The page uses the **Inter** Google Font — Elementor loads it automatically.

---

## Images

The two lower-section images are grey placeholders with the size printed on them —
replace each with your own photo at the same dimensions and the layout won't move.

| Where | File | Size |
|---|---|---|
| Hero background (full-bleed) | `images/hero-background-1284x1109.jpg` | your own photo — **1920 × 1100 px or larger**, since it now spans the full screen width |
| Hero logo mark (top-left of the card) | `images/aussie-carport-kits-logo.png` | your logo, transparent PNG, shown 138 px wide |
| "Built to look premium" section | `images/product-detail-1160x1080.jpg` | **1160 × 1080 px** |
| "Make the finished carport the hero" | `images/project-outcome-1160x1080.jpg` | **1160 × 1080 px** |

The hero background photo and the logo are your own assets, taken straight out of the
revised hero HTML you supplied — they are not placeholders. The logo PNG you supplied
had a large transparent margin around it; that margin is trimmed here so the mark reads
properly at the 34 px height the design specifies.

During import Elementor downloads all four images into your Media Library
automatically. If your server blocks remote fetches they'll show as broken — in that
case upload the files from the `images/` folder here and re-select them on each
Image widget.

---

## Quote form

The form is the Elementor Pro **Form** widget. Submissions are set to email:

```
info@aussiecarportkits.com.au
```

Fields: Name, Phone, Postcode, I Want (DIY kit only / Supply + installation / Not sure
yet), Approx. Width, Approx. Length, Anything Else.

After importing, open the Form widget → **Actions After Submit → Email** and confirm the
"To" address came across. Send yourself one test submission before going live — if your
host blocks WordPress mail, add an SMTP plugin (WP Mail SMTP or similar).

---

## Things to change before publishing

- **Phone number** — `tel:+61000000000` is a placeholder, on the "Call Us" button in the
  mobile sticky bar.
- **Body copy** — the HTML reference contains notes written to you rather than final
  page copy (for example "Your original page has strong product ingredients…"). Those
  have been reproduced exactly as supplied; swap them for your real copy.
- **Prices** — $2,290, $140/m² and 7-day Sydney delivery came from the reference file.
- **Privacy line** under the form.

---

## Structure

1. Hero — true full-bleed photo (edge to edge, no rounded card, no outer frame) with the
   dark gradient overlay, logo mark, green-dot eyebrow, "Your Space. Your Size. One
   Complete Kit.", sub copy, two CTAs, proof row, and the glass value card bottom-right.
   The photo spans the full viewport; the content inside it stays boxed at 1220px and
   centred so the composition keeps the reference proportions on wide screens.
2. Trust strip — 4 items
3. "Do it yourself — or have us organise the installation" — 2 choice cards
4. "Here's what happens after you enquire" — 4 numbered steps
5. "Built to look premium" — image + 4 metric boxes
6. Dark comparison table — aluminium vs roll-formed steel (anchor `#compare`)
7. "Make the finished carport the hero" — copy + image
8. Quote section (anchor `#quote`) — benefits + form card
9. FAQ accordion
10. Footer
11. Mobile-only sticky CTA bar (hidden on desktop and tablet)

Every top-level container is set to **Overflow: Hidden**, so an absolutely-positioned
element (the hero logo mark, the value card, the "MOST ONLINE BUYERS" tag) can't push
past its section and give the page a horizontal scrollbar on a live theme.

Breakpoints follow Elementor defaults — tablet ≤ 1024px, mobile ≤ 767px — mapped from
the 900px / 620px media queries in the reference HTML.
