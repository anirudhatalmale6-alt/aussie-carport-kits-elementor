# Aussie Carport Kits — Elementor landing page template

Elementor page template that recreates `aussie_carport_kits_conversion_redesign.html`
section for section, built with Elementor flexbox containers and core widgets
(plus the Elementor **Pro** Form widget for the quote form).

**File to import:** `aussie-carport-kits-landing-template.json`

---

## How to install

1. WordPress admin → **Templates → Saved Templates → Import Templates**.
2. Upload `aussie-carport-kits-landing-template.json` and click **Import Now**.
3. Create your new page → **Edit with Elementor**.
4. In the editor, open the **folder icon** (Add Template) → **My Templates** tab →
   find *Aussie Carport Kits — Conversion Landing Page* → **Insert**.
5. When Elementor asks **"Import Document Settings?"**, choose **Yes**. That applies the
   Elementor Canvas page layout, so your theme's header and footer don't appear twice
   (the design has its own top bar, sticky header and footer built in).
6. Publish.

If you'd rather keep your theme's header/footer, answer **No** at step 5 and delete the
first two containers (the dark top bar and the white nav bar) plus the last two
(the footer and the mobile sticky bar).

---

## Requirements

- Elementor **Pro** active (needed for the quote form and the sticky header).
- Elementor 3.16 or newer (flexbox containers). Built and tested against Elementor 4.3.3.
- The page uses the **Inter** Google Font — Elementor loads it automatically.

---

## Images

Placeholders are included so you can see the sizes. Replace each one with your own
photo at the same dimensions and the layout won't move.

| Where | File | Size |
|---|---|---|
| Hero (right of the headline) | `images/hero-carport-1200x900.jpg` | **1200 × 900 px** (4:3) |
| "Built to look premium" section | `images/product-detail-1160x1080.jpg` | **1160 × 1080 px** |
| "Make the finished carport the hero" | `images/project-outcome-1160x1080.jpg` | **1160 × 1080 px** |

During import Elementor downloads these three placeholders into your Media Library
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

- **Phone number** — `tel:+61000000000` is a placeholder. It's on "Call for advice"
  (header), "Speak To A Carport Expert" (hero) and "Call Us" (mobile sticky bar).
- **Body copy** — the HTML reference contains notes written to you rather than final
  page copy (for example "Your original page has strong product ingredients…"). Those
  have been reproduced exactly as supplied; swap them for your real copy.
- **Prices** — $2,290, $140/m² and 7-day Sydney delivery came from the reference file.
- **Privacy line** under the form.

---

## Structure

1. Dark announcement top bar
2. Sticky header — brand, "Call for advice", "Why aluminium?", "Get My Price"
3. Hero — eyebrow pill, headline, lead, 3 price pills, 2 CTAs, image + floating price card
4. Trust strip — 4 items
5. "Do it yourself — or have us organise the installation" — 2 choice cards
6. "Here's what happens after you enquire" — 4 numbered steps
7. "Built to look premium" — image + 4 metric boxes
8. Dark comparison table — aluminium vs roll-formed steel (anchor `#compare`)
9. "Make the finished carport the hero" — copy + image
10. Quote section (anchor `#quote`) — benefits + form card
11. FAQ accordion
12. Footer
13. Mobile-only sticky CTA bar (hidden on desktop and tablet)

Breakpoints follow Elementor defaults — tablet ≤ 1024px, mobile ≤ 767px — mapped from
the 900px / 620px media queries in the reference HTML.
