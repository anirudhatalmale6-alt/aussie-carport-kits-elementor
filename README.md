# Aussie Carport Kits — Elementor landing page template

Elementor page template that recreates `aussie_carport_kits_paid_traffic_copy_revision.html`
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
   find *Aussie Carport Kits — Paid Traffic Landing Page* → **Insert**.
5. When Elementor asks **"Import Document Settings?"**, choose **Yes**. That applies the
   Elementor Canvas page layout. If you click **No**, the page keeps your theme's own
   template, which wraps the design in your theme's container — that can push content
   sideways. You can switch it later on the page: **Settings** (gear, bottom-left) →
   **Page Layout → Elementor Canvas**.
6. Publish.

The design carries no announcement bar and no nav header — the full-bleed hero is the
first thing on the page, so your theme's own site header sits directly above it. It does
include its own footer strip and a mobile-only sticky CTA bar; delete those two
containers if your theme already provides them.

---

## Requirements

- Elementor **Pro** active (needed for the quote form).
- Elementor 3.16 or newer (flexbox containers). Built and tested against Elementor 4.3.3.
- Google Fonts **Poppins** (body) and **Sora** (headings) — Elementor loads both
  automatically.

---

## Images

All three photos are your own, taken straight out of the HTML you supplied. None of them
are placeholders.

| Where | File | Supplied size |
|---|---|---|
| Hero background (full-bleed) | `images/hero-background-carport.jpg` | 472 × 568 px |
| "Built to look premium" section | `images/product-story-carport.jpg` | 472 × 352 px |
| "Built to look right on your home" | `images/result-carport.jpg` | 472 × 568 px |

⚠️ **These are small.** 472px wide is fine for a thumbnail but the hero stretches across
the whole screen, so it will look soft on a desktop monitor. If you have the originals off
the camera or phone, swap all three for versions **1920px wide or larger** — the hero one
matters most. The layout won't move when you replace them.

The hero background and the "Built to look right on your home" photo are the same image in
your HTML; that's reproduced as supplied.

During import Elementor downloads all three into your Media Library automatically. If your
server blocks remote fetches they'll show as broken — in that case upload the files from
the `images/` folder here and re-select them on each Image widget.

---

## Quote form

The form is the Elementor Pro **Form** widget. Submissions are set to email:

```
info@aussiecarportkits.com.au
```

Fields: Name (full width), Phone, Postcode, I want (DIY kit only / Supply + installation /
Not sure yet), Approx. width, Approx. length, Anything else — matching the field widths in
your HTML.

After importing, open the Form widget → **Actions After Submit → Email** and confirm the
"To" address came across. Send yourself one test submission before going live — if your
host blocks WordPress mail, add an SMTP plugin (WP Mail SMTP or similar).

---

## Two fixes applied to the supplied HTML

Both of these are rendering faults in the reference file itself. They were corrected
rather than reproduced:

1. **Logo overlapped the eyebrow.** `.logo` is absolutely positioned at `top:32px` while
   `.hero-inner` only has `52px` of top padding, so on desktop the wordmark printed on top
   of "● CUSTOM DIY CARPORT KITS". The logo now sits in normal flow above the eyebrow with
   proper spacing.
2. **The hero paragraph ran underneath the floating card.** `.hero-inner` is
   `width:min(1120px,…)` capped by `max-width:720px` with `margin:auto`, which centres the
   text block; combined with the card at `right:4vw` the copy disappeared behind it. The
   text block is now left-aligned inside the 1120px wrap, so it clears the card and lines
   up with every section below it.

---

## Things to change before publishing

- **Phone number** — the "Call Us" button in the mobile sticky bar points at `#quote`;
  point it at your real `tel:` number.
- **Photo resolution** — see the Images note above.

---

## Structure

1. Hero — full-bleed photo, dark left-to-right gradient, text wordmark, green-dot eyebrow,
   "DIY Carport Kits Built For Your Space.", sub copy, two CTAs, tick row, and the glass
   card bottom-right
2. Trust strip — 4 pills (anchor `#included`)
3. "DIY the build — or have us organise installation." — 2 option cards
4. "From enquiry to a clear price — fast." — 4 numbered steps
5. "Built to look premium…" — copy + 4 feature boxes + photo
6. Dark comparison table — aluminium vs roll-formed steel
7. "Built to look right on your home." — copy + photo
8. Quote section (anchor `#quote`) — benefits + form card
9. FAQ
10. Footer
11. Mobile-only sticky CTA bar (hidden on desktop and tablet)

The FAQ is built as four separate **Toggle** widgets, each in its own container carrying a
single bottom rule, rather than one Accordion widget. That reproduces the plain horizontal
rules of the reference, lets each row open independently like the `<details>` elements in
your HTML, and keeps every row locked to the page width when expanded — verified with all
four rows open at 1920 / 1280 / 1024 / 820 / 600 / 390 / 360 px.

Every top-level container is set to **Overflow: Hidden** so an absolutely-positioned
element can't push past its section and give the page a horizontal scrollbar.

The content wrap is `min(1120px, calc(100% - 40px))`, declared at desktop, tablet *and*
mobile — Elementor does not inherit a container's width down to the mobile breakpoint, so
leaving it off makes content run to the screen edge on phones.

Breakpoints follow Elementor defaults — tablet ≤ 1024px, mobile ≤ 767px — mapped from the
900px / 560px media queries in the reference HTML.
