#!/usr/bin/env python3
"""
Elementor page-template JSON for "Patio_Experts_Single_and_Double_Carport_Packages.html".

LEAN build. The earlier pages wrapped almost every widget in its own container
(213 containers for 219 widgets on the before/after page). Rules here:

  * a container only exists to lay out MORE THAN ONE child
  * multi-column layouts use a Grid container, not a row of column containers
  * width / spacing / background / border / position go on the widget's own
    Advanced settings, never on a wrapper around it
  * badges, pills and eyebrows are single styled widgets
  * depth: section -> layout -> card -> widgets, never deeper

Pro widgets used: form (x2), nested-carousel (x1). No HTML/code widgets.
"""
import json, itertools, sys

IMG_BASE = "https://raw.githubusercontent.com/anirudhatalmale6-alt/aussie-carport-kits-elementor/main/images"

# ---------------------------------------------------------------- tokens
NAVY   = "#081A33"
BLUE   = "#12A7E2"
BLUE2  = "#0788C0"
INK    = "#111827"
MUTED  = "#667085"
LINE   = "#E6EBF0"
OFF    = "#F5F8FB"
GREEN  = "#0E9F6E"
WHITE  = "#FFFFFF"
BODY_F = "Inter"
HEAD_F = "Sora"
WRAP   = "min(1160px, calc(100% - 36px))"
WRAP_M = "calc(100% - 24px)"
PHONE  = "1300 431 458"
TEL    = "tel:1300431458"

_ids = itertools.count(0x500000)
def eid():
    return format(next(_ids), '07x')

# ---------------------------------------------------------------- primitives
def dim(t, r, b, l, unit="px"):
    return {"unit": unit, "top": str(t), "right": str(r), "bottom": str(b),
            "left": str(l), "isLinked": t == r == b == l}
def rad(v): return dim(v, v, v, v)
def sl(size, unit="px"): return {"unit": unit, "size": size, "sizes": []}
def cu(expr): return {"unit": "custom", "size": expr, "sizes": []}
def gap(v, unit="px"):
    return {"unit": unit, "size": v, "column": str(v), "row": str(v), "isLinked": True}
def gapxy(col, row, unit="px"):
    return {"unit": unit, "size": col, "column": str(col), "row": str(row), "isLinked": False}

def typo(prefix="typography", size=None, weight=None, lh=None, ls=None, transform=None,
         size_t=None, size_m=None, family=BODY_F, lh_unit="em"):
    s = {f"{prefix}_typography": "custom"}
    if family:    s[f"{prefix}_font_family"] = family
    if size:      s[f"{prefix}_font_size"] = cu(size) if isinstance(size, str) else sl(size)
    if size_t:    s[f"{prefix}_font_size_tablet"] = sl(size_t)
    if size_m:    s[f"{prefix}_font_size_mobile"] = sl(size_m)
    if weight:    s[f"{prefix}_font_weight"] = str(weight)
    if lh:        s[f"{prefix}_line_height"] = sl(lh, lh_unit)
    if ls is not None:
        s[f"{prefix}_letter_spacing"] = cu(ls) if isinstance(ls, str) else sl(ls)
    if transform: s[f"{prefix}_text_transform"] = transform
    return s

def shadow(group, h, v, blur, spread, color):
    return {f"{group}_box_shadow_type": "yes",
            f"{group}_box_shadow": {"horizontal": h, "vertical": v, "blur": blur,
                                    "spread": spread, "color": color}}

def con(children=None, **st):
    st.setdefault("content_width", "full")
    st.setdefault("padding", dim(0, 0, 0, 0))     # Elementor's kit default is 10px
    st.setdefault("flex_gap", gap(0))
    if "width" in st:                              # desktop width never reaches mobile
        st.setdefault("width_tablet", st["width"])
        st.setdefault("width_mobile", st["width"])
    return {"id": eid(), "elType": "container", "settings": st,
            "elements": children or [], "isInner": False}

def grid(children, cols, cols_t=None, cols_m="1fr", rows="auto", rows_m=None,
         g=(0, 0), g_m=None, **st):
    """Grid container. Elementor defaults rows to repeat(2,1fr) and desktop columns
    to repeat(3,1fr), so both are always written explicitly at every breakpoint."""
    s = {"container_type": "grid",
         "grid_columns_grid": cu(cols),
         "grid_columns_grid_tablet": cu(cols_t or cols),
         "grid_columns_grid_mobile": cu(cols_m),
         "grid_rows_grid": cu(rows),
         "grid_rows_grid_tablet": cu(rows),
         "grid_rows_grid_mobile": cu(rows_m or rows),
         "grid_gaps": gapxy(g[0], g[1])}
    if g_m:
        s["grid_gaps_mobile"] = gapxy(g_m[0], g_m[1])
    s.update(st)
    return con(children, **s)

def section(children, bg=None, pad=(92, 92), pad_m=(68, 68), wrap=WRAP, wrap_m=WRAP_M,
            row=False, element_id=None, **extra):
    s = {"content_width": "boxed",
         "boxed_width": cu(wrap), "boxed_width_tablet": cu(wrap),
         "boxed_width_mobile": cu(wrap_m),
         "flex_direction": "row" if row else "column",
         "padding": dim(pad[0], 0, pad[1], 0),
         "padding_mobile": dim(pad_m[0], 0, pad_m[1], 0)}
    if row:
        s.update({"flex_direction_tablet": "column", "flex_direction_mobile": "column",
                  "flex_wrap": "nowrap"})
    if bg:
        s["background_background"] = "classic"; s["background_color"] = bg
    if element_id:
        s["_element_id"] = element_id
    s.update(extra)
    return con(children, **s)

def widget(wtype, **st):
    return {"id": eid(), "elType": "widget", "settings": st,
            "elements": [], "widgetType": wtype}

def adv(w, *, mt=None, mb=None, mr=None, ml=None, width=None, width_t=None, width_m=None,
        auto=False, align_self=None, grow=False, pad=None, pad_m=None, bg=None,
        border=None, border_m=None, border_color=None, radius=None, box_shadow=None,
        z=None, hide_m=False, hide_t=False, **extra):
    """Style a widget through its own Advanced tab instead of wrapping it."""
    s = w["settings"]
    if any(v is not None for v in (mt, mb, mr, ml)):
        s["_margin"] = dim(mt or 0, mr or 0, mb or 0, ml or 0)
    if auto:
        s["_element_width"] = "auto"
    if width is not None:
        s["_element_width"] = "initial"
        s["_element_custom_width"] = cu(width) if isinstance(width, str) else sl(width)
        for bp, v in (("tablet", width_t), ("mobile", width_m)):
            if v is not None:
                s[f"_element_width_{bp}"] = "initial"
                s[f"_element_custom_width_{bp}"] = cu(v) if isinstance(v, str) else sl(v)
    if align_self: s["_flex_align_self"] = align_self
    if grow:       s["_flex_size"] = "grow"
    if pad:        s["_padding"] = dim(*pad)
    if pad_m:      s["_padding_mobile"] = dim(*pad_m)
    if bg:
        s["_background_background"] = "classic"; s["_background_color"] = bg
    if border:
        s["_border_border"] = "solid"; s["_border_width"] = dim(*border)
        s["_border_color"] = border_color or LINE
    if border_m:
        s["_border_width_mobile"] = dim(*border_m)
    if radius is not None: s["_border_radius"] = rad(radius)
    if box_shadow:         s.update(shadow("_box_shadow", *box_shadow))
    if z is not None:      s["_z_index"] = z
    if hide_m: s["hide_mobile"] = "hidden-mobile"
    if hide_t: s["hide_tablet"] = "hidden-tablet"
    s.update(extra)
    return w

def heading(title, tag="div", color=INK, align=None, link=None, **ty):
    s = {"title": title, "header_size": tag, "title_color": color}
    if align: s["align"] = align
    if link:  s["link"] = {"url": link, "is_external": "", "nofollow": "",
                           "custom_attributes": ""}
    s.update(typo(**ty))
    return widget("heading", **s)

def text(html, color=MUTED, align=None, **ty):
    s = {"editor": html.replace("<p>", '<p style="margin:0">'), "text_color": color}
    if align: s["align"] = align
    ty.setdefault("lh", 1.55)
    s.update(typo(**ty))
    return widget("text-editor", **s)

def ticks(items, color=INK, icon_color=GREEN, size=15, weight=400, space=12,
          inline=False, icon="fas fa-check", icon_size=13):
    return widget("icon-list",
                  view="inline" if inline else "traditional",
                  icon_list=[{"text": t, "selected_icon": {"value": icon, "library": "fa-solid"},
                              "_id": eid()} for t in items],
                  space_between=gapxy(22, 9) if inline else sl(space),
                  icon_color=icon_color, icon_size=sl(icon_size), text_indent=sl(9),
                  text_color=color,
                  **typo(prefix="icon_typography", size=size, weight=weight, lh=1.48))

def button(label, link, kind="primary", full=False, full_m=True, compact=False):
    s = {"text": label, "size": "sm",
         "link": {"url": link, "is_external": "", "nofollow": "", "custom_attributes": ""},
         "border_radius": rad(9 if not compact else 8),
         "text_padding": dim(15, 12, 15, 12) if compact else dim(18, 22, 18, 22),
         "align": "justify" if full else "left"}
    if full_m: s["align_mobile"] = "justify"
    s.update(typo(size=16 if not compact else 15, weight=800, lh=1.25))
    palette = {
        "primary": (BLUE, WHITE, BLUE2, None),
        "dark":    (NAVY, WHITE, "#0D294C", None),
        "outline": (WHITE, NAVY, "#F2F6F9", "#DFE6ED"),
        "soft":    ("#EDF2F6", NAVY, "#E2E9EF", None),
    }[kind]
    bg, fg, hover, border = palette
    s.update({"background_background": "classic", "background_color": bg,
              "button_text_color": fg, "hover_color": fg,
              "button_background_hover_background": "classic",
              "button_background_hover_color": hover})
    if border:
        s.update({"border_border": "solid", "border_width": dim(1, 1, 1, 1),
                  "border_color": border, "button_hover_border_color": border})
    if kind in ("primary", "dark"):
        s.update(shadow("button_box_shadow", 0, 10, 24, 0, "rgba(0,0,0,0.14)"))
    return widget("button", **s)

def image(fname, h=None, h_t=None, h_m=None, radius=0, pos=None):
    s = {"image": {"url": f"{IMG_BASE}/{fname}", "id": "", "source": "library"},
         "image_size": "full", "width": sl(100, "%"), "image_border_radius": rad(radius)}
    if h:
        s["height"] = sl(h); s["object-fit"] = "cover"
        if h_t: s["height_tablet"] = sl(h_t)
        if h_m: s["height_mobile"] = sl(h_m)
    if pos: s["object-position"] = pos
    return widget("image", **s)

# ---------------------------------------------------------------- shared pieces
def eyebrow(t, color=BLUE, mb=12, align=None):
    return adv(heading(t, color=color, align=align, size=12, weight=900, lh=1.3,
                       ls="0.14em", transform="uppercase"), mb=mb)

def h1(t, color=WHITE):
    return heading(t, tag="h1", color=color, size="clamp(42px, 5.2vw, 70px)", size_m=43,
                   weight=800, lh=1.06, ls="-0.035em", family=HEAD_F)

def h2(t, color=INK, align=None):
    return heading(t, tag="h2", color=color, align=align, size="clamp(34px, 4vw, 54px)",
                   size_m=36, weight=800, lh=1.06, ls="-0.035em", family=HEAD_F)

def h3(t, color=INK, size=22, size_m=None):
    return heading(t, tag="h3", color=color, size=size, size_m=size_m, weight=800,
                   lh=1.15, ls="-0.035em", family=HEAD_F)

def section_head(kick, title, body=None, kick_color=BLUE, title_color=INK,
                 body_color=MUTED, maxw="min(790px, 100%)", mb=42):
    """Eyebrow + h2 + intro, each capped at the head width on the widget itself."""
    ws = [eyebrow(kick, color=kick_color),
          adv(h2(title, color=title_color), width=maxw, mb=0 if body else mb)]
    if body:
        ws.append(adv(text(f"<p>{body}</p>", color=body_color, size=18, size_m=16),
                      width=maxw, mt=17, mb=mb))
    return ws

def check_grid(items, color, icon_color, mt=24, mb=24):
    """2-up tick grid (1-up on phones). One single-item list per cell keeps the
    reading order 1 2 / 3 4 on desktop and 1 2 3 4 on a phone."""
    return grid([ticks([t], color=color, icon_color=icon_color, size=15, weight=700,
                       icon="fas fa-check-circle", icon_size=19) for t in items],
                cols="1fr 1fr", cols_m="1fr", g=(18, 10),
                margin=dim(mt, 0, mb, 0))

def form(name, fields, button_text, columns_gap=10, subject="New Patio Experts carport enquiry"):
    return widget(
        "form", form_name=name, form_fields=fields,
        input_size="md", show_labels="", mark_required="", label_position="above",
        button_text=button_text, button_size="sm", button_align="stretch",
        button_width="100",
        submit_actions=["email"],
        email_to="info@patioexperts.com.au",
        email_subject=subject,
        email_content="[all-fields]",
        email_from_name="Patio Experts Website",
        email_content_type="html",
        success_message="Thanks — we’ll be in touch shortly.",
        error_message="Something went wrong. Please call us on " + PHONE + ".",
        required_field_message="This field is required.",
        invalid_message="There’s a problem with one of the fields.",
        column_gap=gap(columns_gap), row_gap=gap(columns_gap),
        field_border_radius=rad(8), field_border_border="solid",
        field_border_width=dim(1, 1, 1, 1), field_border_color="#D8E0E7",
        field_background_color=WHITE, field_text_color="#1D2939",
        button_background_color=BLUE, button_text_color=WHITE,
        button_background_hover_color=BLUE2,
        button_border_radius=rad(9), button_text_padding=dim(18, 22, 18, 22),
        **typo(prefix="field_typography", size=16, weight=400),
        **typo(prefix="button_typography", size=16, weight=800))

def field(cid, ftype, placeholder, width="100", required=True, options=None):
    f = {"custom_id": cid, "field_type": ftype, "field_label": placeholder,
         "placeholder": placeholder, "required": "true" if required else "",
         "width": width, "width_mobile": "100", "_id": eid()}
    if options: f["field_options"] = options
    return f

# ================================================================ 0. TOPBAR
topbar = section([
    text('<p><b style="color:#7DD9FF">Sydney Carport Builders</b> · Engineered aluminium '
         'supply + install</p>', color="#D9E6F3", size=13, lh=1.5),
    adv(text("<p>30+ Years Industry Experience · Project-Specific Quotations</p>",
             color="#D9E6F3", size=13, lh=1.5), hide_m=True),
], bg="#061427", pad=(9, 9), pad_m=(9, 9), row=True,
   flex_direction_tablet="row", flex_direction_mobile="row",
   flex_justify_content="space-between", flex_align_items="center", flex_gap=gap(16))

# ================================================================ 1. HERO
header = section([
    adv(heading('Patio <span style="color:#12A7E2">Experts</span>', color=WHITE,
                link="#top", size=28, size_m=24, weight=900, lh=1.1, ls="-0.055em",
                family=HEAD_F), grow=True),
    heading(PHONE, color=WHITE, link=TEL, size=16, size_m=14, weight=900, lh=1.2),
    adv(button("Request a Quote", "#quote", "primary", full_m=False), hide_m=True),
], pad=(17, 17), pad_m=(17, 17), row=True,
   flex_direction_tablet="row", flex_direction_mobile="row",
   flex_align_items="center", flex_gap=gap(15),
   border_border="solid", border_width=dim(0, 0, 1, 0),
   border_color="rgba(255,255,255,0.16)")

hero_copy = con([
    eyebrow("Carport Builders Sydney · Supply + Install", color="#81DFFF"),
    adv(h1("Aluminium Carports Supplied &amp; Installed Across Sydney."),
        width="min(760px, 100%)"),
    adv(text("<p>Choose from our single and double freestanding carport packages, "
             "professionally supplied and installed across Sydney. Both packages include "
             "engineered aluminium construction, genuine COLORBOND roofing and "
             "installation into concrete footings.</p>",
             color="#E9F2FA", size=19, size_m=17, lh=1.58),
        width="min(690px, 100%)", mt=20),
    adv(text('<p><span style="font-size:15px;font-weight:800;color:#ffffff">Single carport '
             'package <b style="color:#8BE2FF;font-size:18px">from $6,690*</b></span><br>'
             '<span style="font-size:12px;font-weight:600;color:#D9E6F3">Double carport '
             'package also available — see both below</span></p>',
             color=WHITE, size=15, lh=1.4),
        auto=True, align_self="flex-start", mt=22, pad=(10, 13, 10, 13),
        bg="rgba(255,255,255,0.10)", border=(1, 1, 1, 1),
        border_color="rgba(255,255,255,0.18)", radius=8,
        custom_css="selector{backdrop-filter:blur(8px);}"),
    check_grid(["Engineered aluminium posts &amp; beams", "Attached and freestanding designs",
                "Supply and installation arranged", "Project-specific written quotation"],
               color=WHITE, icon_color="#8AF0CA"),
    con([button("Request My Carport Quote →", "#quote", "primary"),
         button(f"Call {PHONE}", TEL, "outline")],
        flex_direction="row", flex_wrap="wrap", flex_gap=gap(12),
        flex_direction_mobile="column", flex_align_items_mobile="stretch"),
    adv(text("<p>*$6,690 applies to the 2.8m W × 5.8m L × 2.7m H single flat-roof package "
             "at eligible sites. See both packages and the included specifications below. "
             "Double-carport pricing is confirmed by quotation.</p>",
             color="#C7D5E4", size=12.5, lh=1.5),
        width="min(680px, 100%)", mt=14),
], flex_direction="column",
   # explicit width: a growing flex item sizes to its content first and shoves the
   # 410px quote card off the right edge
   width=cu("calc(100% - 464px)"), width_tablet=sl(100, "%"), width_mobile=sl(100, "%"))

quote_card = con([
    eyebrow("Request a Sydney Carport Quote", mb=8),
    h3("Carport Supply &amp; Installation Quote", size=28, size_m=25),
    adv(text("<p>Share your suburb and the carport you’re considering. We’ll contact you to "
             "discuss the project and prepare a supply-and-installation quotation.</p>",
             size=14), mt=8),
    adv(heading('<span style="display:inline-block;width:22px;height:22px;line-height:22px;'
                'text-align:center;border-radius:50%;background:#E6F7FD;color:#087DAB;'
                'margin-right:8px">1</span>Four details to get your enquiry started',
                color="#475467", size=12, weight=800, lh=1.6), mt=16, mb=13),
    form("Hero quote", [
        field("name", "text", "Full name", "50"),
        field("mobile", "tel", "Mobile number", "50"),
        field("suburb", "text", "Suburb / postcode", "50"),
        field("carport", "select", "Your carport requirements", "100", required=False,
              options="Your carport requirements|\n"
                      "Single package — 2.8m × 5.8m × 2.7m\n"
                      "Double package — 5.5m × 5m × 2.8m\n"
                      "Other single carport\nOther double carport\n"
                      "Attached carport — size to confirm\nOther / not sure yet"),
    ], "Request My Written Quote →",
       subject="New carport quote request (top form) - Patio Experts"),
    adv(text("<p>Free, no-obligation enquiry. We’ll use your details to discuss your "
             "proposed carport.</p>", color="#778292", align="center", size=11.5),
        mt=10),
], flex_direction="column", _element_id="quote", _flex_size="none",
   width=sl(410), width_tablet=cu("min(650px, 100%)"), width_mobile=sl(100, "%"),
   padding=dim(28, 28, 28, 28), padding_mobile=dim(22, 22, 22, 22),
   background_background="classic", background_color=WHITE, border_radius=rad(16),
   **shadow("box_shadow", 0, 30, 70, 0, "rgba(0,0,0,0.28)"))

hero_row = section([hero_copy, quote_card], row=True, pad=(64, 74), pad_m=(58, 52),
                   flex_align_items="center", flex_gap=gap(54),
                   flex_gap_tablet=gap(34), flex_align_items_tablet="stretch")

hero = con([header, hero_row], flex_direction="column", _element_id="top",
           min_height=sl(770), min_height_mobile=sl(0),
           background_background="classic",
           background_image={"url": f"{IMG_BASE}/pe-hero.webp", "id": "", "source": "library"},
           background_size="cover", background_repeat="no-repeat",
           background_position="initial",
           background_xpos=sl(50, "%"), background_ypos=sl(48, "%"),
           background_xpos_mobile=sl(62, "%"), background_ypos_mobile=sl(50, "%"),
           background_overlay_background="gradient",
           background_overlay_color="rgba(5,20,42,0.95)",
           background_overlay_color_stop=sl(46, "%"),
           background_overlay_color_b="rgba(6,24,50,0.30)",
           background_overlay_color_b_stop=sl(100, "%"),
           background_overlay_gradient_type="linear",
           background_overlay_gradient_angle=sl(90, "deg"),
           background_overlay_opacity=sl(1))

# ================================================================ 2. PROOF BAR
def proof(title, desc, border, border_m):
    return adv(widget("icon-box",
                      selected_icon={"value": "", "library": ""},
                      title_text=title, description_text=desc, title_size="div",
                      text_align="center", title_bottom_space=sl(3),
                      title_color=NAVY, description_color=MUTED,
                      **typo(prefix="title_typography", size=16, weight=800, lh=1.3),
                      **typo(prefix="description_typography", size=12.5, lh=1.45)),
               pad=(22, 15, 22, 15), pad_m=(16, 8, 16, 8),
               border=border, border_m=border_m)

proofbar = section([
    proof("30+ Years", "Industry experience", (0, 1, 0, 0), (0, 1, 0, 0)),
    proof("Engineered Aluminium", "Posts and beams specified for your project",
                (0, 1, 0, 0), (0, 0, 0, 0)),
          proof("Sydney Supply + Install", "Coordinated supply and installation",
                (0, 1, 0, 0), (0, 1, 0, 0)),
          proof("Site-Specific Quotes", "Project scope and price explained",
                (0, 0, 0, 0), (0, 0, 0, 0)),
], bg=WHITE, pad=(0, 0), pad_m=(0, 0),
   border_border="solid", border_width=dim(0, 0, 1, 0), border_color=LINE,
   # the section itself is the 4-up grid (boxed grid containers lay out .e-con-inner)
   container_type="grid",
   grid_columns_grid=cu("repeat(4, 1fr)"), grid_columns_grid_tablet=cu("repeat(4, 1fr)"),
   grid_columns_grid_mobile=cu("1fr 1fr"),
   grid_rows_grid=cu("auto"), grid_rows_grid_tablet=cu("auto"),
   grid_rows_grid_mobile=cu("auto"), grid_gaps=gapxy(0, 0))

# ================================================================ 3. PACKAGES
INCLUSIONS = ["Freestanding installation into concrete footings",
              "Fully supplied and installed", "Engineered aluminium beams",
              "110 × 110 mm engineered aluminium posts",
              "Genuine COLORBOND® metal roofing, flashings and gutters",
              "Built within 7 days from check measure*", "Fully licensed NSW builders"]

def package(kicker, title, dims, roof, price, caption, cta, fine, featured=False,
            pending=False):
    price_w = heading(price, color=NAVY,
                      size=30 if pending else 54, size_m=28 if pending else 47,
                      weight=900, lh=1.35 if pending else 1,
                      ls="-0.045em" if pending else "-0.055em", family=HEAD_F)
    kids = [
        heading(kicker, color=MUTED, size=12, weight=900, lh=1.3, ls="0.12em",
                transform="uppercase"),
        adv(h3(title, color=NAVY, size=27, size_m=24), mt=13, mb=10),
        heading(dims, color=INK, size=17, size_m=16, weight=900, lh=1.4),
        adv(text(f"<p>{roof}</p>", size=13), mt=6),
        adv(price_w, mt=22, mb=7),
        text(f"<p>{caption}</p>", size=14),
        adv(heading("Included in this package", color=NAVY, size=15, weight=900, lh=1.4),
            mt=25, pad=(20, 0, 0, 0), border=(1, 0, 0, 0)),
        adv(ticks(INCLUSIONS, color=INK, icon_color=GREEN, size=14, space=13),
            mt=14, mb=20, grow=True),
        button(cta, "#quote", "primary", full=True),
        adv(text(f"<p>{fine}</p>", color="#7A8595", size=11.5, lh=1.5), mt=15),
    ]
    st = dict(flex_direction="column", background_background="classic",
              background_color=WHITE, border_radius=rad(16),
              padding=dim(30, 30, 30, 30), padding_mobile=dim(24, 24, 24, 24),
              border_border="solid", border_width=dim(1, 1, 1, 1), border_color=LINE,
              **shadow("box_shadow", 0, 14, 38, 0, "rgba(8,26,51,0.08)"))
    if featured:
        # The design's featured card has a 4px BLUE top edge on 1px GREY sides. An
        # Elementor border is one colour, so the blue edge is an inset shadow added on
        # top of the card's normal drop shadow (Pro custom CSS; without it the card
        # simply shows the grey border like its neighbour).
        st["custom_css"] = ("selector{box-shadow:inset 0 4px 0 #12A7E2,"
                            "0 14px 38px rgba(8,26,51,.08);}")
    return con(kids, **st)

packages = section([
    adv(eyebrow("Carport Supply &amp; Installation Packages", align="center"),
        align_mobile="left"),
    adv(h2("Single &amp; Double Carport Packages.", align="center"),
        width="min(960px, 100%)", align_self="center", align_mobile="left"),
    adv(text("<p>Two defined freestanding carport options, with the structure, roofing, "
             "concrete footings and professional installation included. Review the "
             "dimensions and inclusions below, then request a quote for your property.</p>",
             align="center", size=18, size_m=16),
        width="min(825px, 100%)", align_self="center", mt=18, mb=36,
        align_mobile="left", _margin_mobile=dim(18, 0, 26, 0)),
    grid([package("Single Carport Package", "Single Flat-Roof Carport",
                  "2.8m wide × 5.8m long × 2.7m high", "Freestanding · Flat roof",
                  "$6,690", "Single-carport package · Supply + installation",
                  "Request Single Package Quote →",
                  "<strong>From $6,690</strong> for the single-carport configuration above at "
                  "eligible sites. Ground conditions, site access and any required approvals "
                  "or additional work are assessed before confirming the final price.",
                  featured=True),
          package("Double Carport Package", "Double Carport",
                  "5.5m wide × 5m long × 2.8m high",
                  "Freestanding · Roof configuration confirmed in quote",
                  "Price on request", "Double-carport package · Supply + installation",
                  "Request Double Package Quote →",
                  "<strong>Double-package price:</strong> To be confirmed in your quotation. "
                  "Ground conditions, site access and any required approvals or additional "
                  "work are assessed before confirming the final price.", pending=True)],
         cols="minmax(0, 1fr) minmax(0, 1fr)", cols_m="minmax(0, 1fr)",
         g=(24, 24), g_m=(20, 20)),
    adv(text("<p><strong>Installation timeframe:</strong> *7 days from check measure applies "
             "to eligible, site-ready projects, subject to required approvals, suitable "
             "ground and access conditions, and confirmed installation scheduling. Final "
             "scope and any additional site work are specified in the written quotation.</p>",
             align="center", size=12.5, lh=1.6),
        width="min(1000px, 100%)", align_self="center", mt=22, align_mobile="left"),
], bg=OFF, element_id="carport-packages")

# ================================================================ 4. GALLERY
def gal(fname, h, h_m, span_rows=False):
    w = image(fname, h=h, h_m=h_m, radius=14)
    if span_rows:
        w["settings"].update({"_grid_row": "2", "_grid_row_mobile": "1",
                              "object-position": "center center"})
    return w

gallery = section(
    section_head("Carport Styles &amp; Configurations",
                 "View Our Aluminium Carport Designs &amp; Installations.",
                 "See examples of attached and freestanding aluminium carport layouts, "
                 "frame finishes and roof configurations.") + [
    grid([gal("pe-gallery-1.webp", 514, 260, span_rows=True),
          gal("pe-gallery-2.webp", 250, 210),
          gal("pe-gallery-3.webp", 250, 210)],
         cols="1.2fr 0.8fr", cols_m="1fr", rows="250px 250px",
         rows_m="260px 210px 210px", g=(14, 14)),
    adv(text("<p>Images show examples of carport designs. Your quotation will confirm the "
             "proposed layout, materials and finishes for your property.</p>", size=12),
        mt=13),
], pad=(92, 76), pad_m=(68, 56))

# ================================================================ 5. BEFORE / AFTER
PROJECTS = [
    ("Dark Aluminium Driveway Carport", "lp4-project01-before.webp", "lp4-project01-after.webp"),
    ("Light Aluminium Outdoor Roof", "lp4-project02-before.webp", "lp4-project02-after.webp"),
    ("White Driveway Carport", "lp4-project03-before.webp", "lp4-project03-after.webp"),
    ("Dark Double-Driveway Carport", "lp4-project04-before.webp", "lp4-project04-after.webp"),
]

def ba_media(fname, label, after=False):
    badge = heading(label, color=WHITE, size=11, size_m=10, weight=900, lh=1.6,
                    ls="0.09em", transform="uppercase")
    adv(badge, auto=True, pad=(3, 12, 3, 12), pad_m=(2, 10, 2, 10), radius=50, z=2,
        bg=BLUE if after else "rgba(8,26,51,0.91)",
        border=None if after else (1, 1, 1, 1), border_color="rgba(255,255,255,0.23)",
        box_shadow=(0, 5, 17, 0, "rgba(0,0,0,0.14)"),
        _position="absolute", _offset_orientation_h="start", _offset_x=sl(14),
        _offset_x_mobile=sl(10), _offset_orientation_v="start", _offset_y=sl(14),
        _offset_y_mobile=sl(10))
    return con([image(fname, h=450, h_t=370, h_m=225), badge],
               overflow="hidden", border_radius=rad(12), border_radius_mobile=rad(10),
               background_background="classic", background_color="#E7EDF2",
               min_height=sl(450), min_height_tablet=sl(370), min_height_mobile=sl(225))

# His controls bar: project name + "n / 4" on the left, dots and two square arrows on
# the right, under a hairline. The name/counter row lives in each slide (so it changes
# with the slide, no script); the carousel's own arrows and dots are placed over the
# right end of that row through the widget's Navigation / Pagination settings.
ARROW, ARROW_M = 42, 39            # button size
CTL_PAD, CTL_PAD_M = 17, 12        # bar side padding (his .pe-ba-controls)
CTL_H, CTL_H_M = 73, 63            # 15 + 42 + 16  /  12 + 39 + 12

def ba_slide(n, title, before, after):
    """Locked inner container (the shape nested-carousel exports): the 2-up pair, then
    the bar with the project name and counter."""
    pair = grid([ba_media(before, "Before"), ba_media(after, "After", after=True)],
                cols="minmax(0, 1fr) minmax(0, 1fr)", cols_m="minmax(0, 1fr)",
                g=(12, 12), g_m=(8, 8),
                padding=dim(15, 15, 15, 15), padding_mobile=dim(9, 9, 9, 9))
    bar = con([adv(heading(title, color=NAVY, size=15, size_m=13, weight=900, lh=1.3,
                           ls="-0.025em", family=HEAD_F), auto=True),
               adv(heading(f"{n} / {len(PROJECTS)}", color="#778598", size=12, size_m=11,
                           weight=800, lh=1.3), _flex_size="none")],
              flex_direction="row", flex_wrap="nowrap", flex_align_items="center",
              flex_gap=gap(11), flex_gap_mobile=gap(7),
              min_height=sl(CTL_H), min_height_mobile=sl(CTL_H_M),
              # right padding keeps the text clear of the dots + arrows
              padding=dim(8, 2 * ARROW + 8 + CTL_PAD + 18 + 73 + 18, 8, CTL_PAD),
              padding_mobile=dim(6, 2 * ARROW_M + 8 + CTL_PAD_M + 10, 6, CTL_PAD_M),
              border_border="solid", border_width=dim(1, 0, 0, 0), border_color=LINE)
    s = con([pair, bar], flex_direction="column")
    s["isInner"] = True
    s["isLocked"] = True
    s["settings"]["_title"] = title
    return s

def ba_nav():
    """Arrows: 42px squares, 9px radius, bottom-right of the shell, 8px apart.
    Dots: 9px, left of the arrows, hidden on mobile (as in his file)."""
    pos = lambda v: sl(v)
    prev_x = -(CTL_PAD + ARROW + 8)              # prev sits one button + gap left of next
    prev_x_m = -(CTL_PAD_M + ARROW_M + 8)
    # vertical: 'end' puts the button's bottom at 100% + offset - 15px (Pro's caption
    # spacing), so offset = 15 - bottom padding
    s = {
        "arrows": "yes", "arrows_position": "inside",
        "navigation_previous_icon": {"value": "fas fa-arrow-left", "library": "fa-solid"},
        "navigation_next_icon": {"value": "fas fa-arrow-right", "library": "fa-solid"},
        "navigation_previous_icon_horizontal_orientation": "end",
        "navigation_previous_icon_horizontal_position": pos(prev_x),
        "navigation_previous_icon_horizontal_position_mobile": pos(prev_x_m),
        "navigation_previous_icon_vertical_orientation": "end",
        "navigation_previous_icon_vertical_position": pos(15 - 16),
        "navigation_previous_icon_vertical_position_mobile": pos(15 - CTL_PAD_M),
        "navigation_next_icon_horizontal_orientation": "end",
        "navigation_next_icon_horizontal_position": pos(CTL_PAD),
        "navigation_next_icon_horizontal_position_mobile": pos(CTL_PAD_M),
        "navigation_next_icon_vertical_orientation": "end",
        "navigation_next_icon_vertical_position": pos(15 - 16),
        "navigation_next_icon_vertical_position_mobile": pos(15 - CTL_PAD_M),
        "arrows_size": sl(16), "arrows_size_mobile": sl(15),
        "arrows_padding": dim(12, 12, 12, 12),
        "arrows_padding_mobile": dim(11, 11, 11, 11),
        "arrows_border_radius": rad(9),
        "arrow_normal_color": NAVY, "arrow_hover_color": NAVY,
        "arrows_normal_background_background": "classic",
        "arrows_normal_background_color": WHITE,
        "arrows_normal_border_type_border": "solid",
        "arrows_normal_border_type_width": dim(1, 1, 1, 1),
        "arrows_normal_border_type_color": "#D6E1E9",
        "arrows_hover_background_background": "classic",
        "arrows_hover_background_color": "#EDF9FE",
        "arrows_hover_border_type_border": "solid",
        "arrows_hover_border_type_width": dim(1, 1, 1, 1),
        "arrows_hover_border_type_color": BLUE,
        "pagination": "bullets", "dots_position": "inside",
        "dots_size": sl(9), "dots_gap": sl(3.5),
        "dots_normal_color": "#C6D1DC", "dots_hover_color": "#9FB0C0",
        "dots_custom_position": "yes",
        "dots_horizontal_position": "end",
        "dots_horizontal_offset": pos(-(CTL_PAD + 2 * ARROW + 8 + 18)),
        "dots_vertical_position": "end",
        "dots_vertical_offset": pos(-(16 + (ARROW - 9) // 2)),
    }
    return s

carousel = adv({
    "id": eid(), "elType": "widget", "widgetType": "nested-carousel",
    "settings": {"carousel_name": "Before and after customer projects",
                 "carousel_items": [{"slide_title": p[0], "_id": eid()} for p in PROJECTS],
                 "slides_to_show": "1", "slides_to_show_tablet": "1",
                 "slides_to_show_mobile": "1", "slides_to_scroll": "1",
                 "autoplay": "", "infinite": "yes", "speed": 400,
                 "image_spacing_custom": sl(0), "image_spacing_custom_tablet": sl(0),
                 "image_spacing_custom_mobile": sl(0),
                 **ba_nav(),
                 # active dot = 25px blue pill; dots hidden on phones (his file does both)
                 "custom_css": (
                     "selector .swiper-pagination-bullet{opacity:1;border-radius:999px;"
                     "transition:width .2s,background .2s;}"
                     "selector .swiper-pagination-bullet-active{width:25px;"
                     "background:#12A7E2;}"
                     "@media (max-width:767px){selector .swiper-pagination{display:none;}}")},
    "elements": [ba_slide(i + 1, *p) for i, p in enumerate(PROJECTS)],
}, bg=WHITE, border=(1, 1, 1, 1), border_color="#DCE5ED", radius=17,
   box_shadow=(0, 20, 55, 0, "rgba(8,26,51,0.09)"))

before_after = section(
    section_head("Real Customer Projects",
                 "Completed Customer Projects — Before &amp; After.",
                 "Compare the original spaces with the completed roof structures at four "
                 "customer properties. View each project using the arrows or swipe on mobile.",
                 maxw="min(850px, 100%)", mb=28) + [
    con([heading("4 customer project comparisons", color="#66768A", size=11.5, size_m=10.5,
                 weight=900, lh=1.3, ls="0.095em", transform="uppercase"),
         heading("Swipe or use the arrows to view all 4", color="#66768A", size=11.5,
                 size_m=10.5, weight=900, lh=1.3, ls="0.095em", transform="uppercase")],
        flex_direction="row", flex_wrap="wrap", flex_justify_content="space-between",
        flex_align_items="center", flex_gap=gapxy(15, 6), margin=dim(0, 0, 15, 0)),
    carousel,
    adv(ticks(["Customer project photographs", "Real customer properties",
               "Before and after"], color="#5C6B7C", icon_color=BLUE2, size=12,
              weight=700, inline=True, icon_size=11), mt=18),
    adv(text("<p>The photos show individual customer projects. Your carport dimensions, "
             "colours, specifications and installation scope will be confirmed in your own "
             "quotation.</p>", color="#7B8796", size=12, lh=1.6), mt=12),
], bg=OFF, pad=(86, 90), element_id="pe-customer-projects")

# ================================================================ 6. WHY
def benefit(num, title, body):
    return con([adv(heading(num, color="#7CDDFF", size=11, weight=900, lh=1.3, ls="0.12em"),
                    mb=13),
                h3(title, color=WHITE, size=21),
                adv(text(f"<p>{body}</p>", color="#CCD8E5", size=14), mt=10)],
               flex_direction="column", padding=dim(25, 25, 25, 25),
               background_background="classic", background_color="rgba(255,255,255,0.065)",
               border_border="solid", border_width=dim(1, 1, 1, 1),
               border_color="rgba(255,255,255,0.11)", border_radius=rad(13))

why = section(
    section_head("Why Patio Experts", "What You Can Expect From Patio Experts.",
                 "We supply engineered aluminium carports, assess the requirements of your "
                 "property and arrange professional installation. The proposed design, scope "
                 "of work and price are confirmed before you accept your quote.",
                 kick_color="#7CDDFF", title_color=WHITE, body_color="#C9D6E4") + [
    grid([benefit("01 · SUPPLY + INSTALL", "Carport Supply &amp; Installation",
                  "Your carport structure and installation requirements are considered "
                  "together, with coordination from quotation through to scheduling."),
          benefit("02 · EXPERIENCE", "30+ Years Industry Experience",
                  "Experience informing the discussion of carport layouts, structural "
                  "requirements and practical installation considerations."),
          benefit("03 · ENGINEERED FRAME", "Aluminium Posts &amp; Beams",
                  "An engineered aluminium frame, with the configuration and finishes "
                  "specified for the proposed carport."),
          benefit("04 · CLEAR QUOTATIONS", "Defined Installation Scope",
                  "Your quotation identifies the proposed carport and installation "
                  "requirements so you can review the scope before proceeding.")],
         cols="repeat(4, 1fr)", cols_t="1fr 1fr", cols_m="1fr", g=(14, 14)),
], bg="#0A1C35")

# ================================================================ 7. PROCESS
def step(num, title, body):
    chip = heading(num, color="#0785B9", align="center", size=16, weight=900, lh=44,
                   lh_unit="px")
    adv(chip, width=44, bg="#E9F8FE", radius=10, _grid_row="2")
    return grid([chip, h3(title, size=22, size_m=20),
                 text(f"<p>{body}</p>", size=14)],
                cols="48px 1fr", cols_m="48px 1fr", rows="auto auto", g=(15, 5),
                grid_align_items="start", padding=dim(19, 19, 19, 19),
                background_background="classic", background_color=WHITE,
                border_border="solid", border_width=dim(1, 1, 1, 1), border_color=LINE,
                border_radius=rad(12))

process = section([
    con([eyebrow("How the Project Works"),
         h2("Our Carport Supply &amp; Installation Process."),
         adv(text("<p>Send through your carport details, review your project quotation and "
                  "confirm the work before installation is arranged.</p>", size=18,
                  size_m=16), mt=17),
         adv(button("Request My Carport Quote →", "#quote", "dark"), mt=25)],
        flex_direction="column", width=cu("calc(41% - 31px)"), width_tablet=sl(100, "%"),
        width_mobile=sl(100, "%")),
    con([step("01", "Tell Us About Your Carport",
              "Tell us your suburb, the approximate area to be covered and whether you prefer "
              "an attached or freestanding design."),
         step("02", "Review Your Project Quote",
              "We review the site and design requirements, then prepare a quotation covering "
              "the proposed carport, installation scope and price."),
         step("03", "Confirm &amp; Arrange Installation",
              "Once you approve the quote and any required site checks or approvals are "
              "addressed, we coordinate the supply and installation schedule.")],
        flex_direction="column", flex_gap=gap(12), width=cu("calc(59% - 31px)"),
        width_tablet=sl(100, "%"), width_mobile=sl(100, "%")),
], row=True, flex_align_items="flex-start", flex_gap=gap(62), flex_gap_tablet=gap(35))

# ================================================================ 8. QUALIFY
def qual(title, items, dark=False):
    return con([adv(h3(title, color=WHITE if dark else INK), mb=13),
                ticks(items, color="#D5E0EA" if dark else "#475467",
                      icon_color="#87E9C5" if dark else GREEN, size=16, space=11)],
               flex_direction="column", padding=dim(28, 28, 28, 28),
               background_background="classic", background_color=NAVY if dark else WHITE,
               border_border="solid", border_width=dim(1, 1, 1, 1),
               border_color=NAVY if dark else LINE, border_radius=rad(14))

qualify = section(
    section_head("Your Project Requirements",
                 "What We Check Before Preparing Your Carport Quote.",
                 "Your quotation is based on the carport configuration and the conditions at "
                 "your property. We confirm the relevant details before you proceed.") + [
    grid([qual("Your Carport", ["Attached or freestanding layout",
                                "Approximate carport dimensions",
                                "Aluminium frame, roofing and finish options",
                                "Supply and installation inclusions and price"]),
          qual("Installation Requirements", ["Site access and existing surface conditions",
                                             "Engineering or approvals that may be required",
                                             "Footing or fixing requirements, where relevant",
                                             "Installation timing once the scope is reviewed"],
               dark=True)],
         cols="1fr 1fr", cols_m="1fr", g=(24, 24)),
], bg=OFF)

# ================================================================ 9. FAQ
FAQ = [
    ("How soon can my carport be built?",
     "Both advertised packages include construction within 7 days from check measure for "
     "eligible, site-ready projects. The timeframe depends on completion of any required "
     "approvals, satisfactory site and ground conditions, site access and confirmed "
     "installation scheduling. We confirm your actual timing during the quotation process."),
    ("Do you supply and install attached and freestanding carports?",
     "Yes. We offer attached and freestanding aluminium carport configurations. We consider "
     "your available space, proposed connection points and intended use when discussing the "
     "design."),
    ("Will my carport require council approval?",
     "That depends on the property, carport dimensions, location and applicable planning "
     "controls. Approval requirements must be checked for your proposed work; we can discuss "
     "the likely next steps during the quotation process."),
    ("What does the $6,690 single-carport package include?",
     "The $6,690 starting price is for a 2.8m wide × 5.8m long × 2.7m high freestanding "
     "flat-roof carport. The advertised package includes installation into concrete footings, "
     "engineered aluminium beams, 110 × 110 mm engineered aluminium posts, genuine COLORBOND "
     "metal roofing, flashings and gutters, and supply and installation by licensed NSW "
     "builders. The final price is subject to your site conditions and any required "
     "additional work."),
    ("Do you offer a double-carport package?",
     "Yes. Our freestanding double-carport package measures 5.5m wide × 5m long × 2.8m high. "
     "It includes the same advertised material and installation inclusions as the "
     "single-carport package. We will provide the double-carport price in a project-specific "
     "quotation."),
    ("What materials are included in the carport packages?",
     "Both advertised packages include engineered aluminium beams, 110 × 110 mm engineered "
     "aluminium posts, genuine COLORBOND metal roofing, flashings and gutters, and "
     "installation into concrete footings. The specific roof configuration, colour selections "
     "and final project details are confirmed in the written quotation."),
]

def faq_row(q, a, last=False):
    """One toggle per question, carrying its own top rule (and the closing rule on the
    last one) on the widget itself — no row containers."""
    return adv(widget("toggle",
                      tabs=[{"tab_title": q, "tab_content": f'<p style="margin:0">{a}</p>',
                             "_id": eid()}],
                      selected_icon={"value": "fas fa-plus", "library": "fa-solid"},
                      selected_active_icon={"value": "fas fa-minus", "library": "fa-solid"},
                      title_html_tag="div", faq_schema="yes", icon_align="right",
                      border_width=sl(0), border_color="#00000000",
                      title_background="#FFFFFF00", title_color=INK, tab_active_color=INK,
                      icon_color=BLUE, icon_active_color=BLUE, icon_space=sl(20),
                      content_background_color="#FFFFFF00", content_color=MUTED,
                      title_padding=dim(21, 0, 21, 0), content_padding=dim(0, 42, 22, 0),
                      **typo(prefix="title_typography", size=16, weight=900, lh=1.4),
                      **typo(prefix="content_typography", size=16, weight=400, lh=1.55)),
               border=(1, 0, 1 if last else 0, 0))

faq = section(
    section_head("Carport Installation FAQs",
                 "Questions About Pricing, Design &amp; Installation") +
    [faq_row(q, a, last=(i == len(FAQ) - 1)) for i, (q, a) in enumerate(FAQ)],
    wrap="min(890px, calc(100% - 36px))")

# ================================================================ 10. FINAL CTA
final_card = con([
    h3("Request a Carport Quote"),
    adv(text("<p>Leave your details and our team will contact you to discuss your carport "
             "specifications and site requirements.</p>", size=14), mt=8, mb=15),
    form("Final quote", [field("name", "text", "Name"),
                         field("phone", "tel", "Phone"),
                         field("suburb", "text", "Suburb / postcode")],
         "Request My Carport Quote →", columns_gap=9,
         subject="New carport quote request (bottom form) - Patio Experts"),
    adv(heading(f"Or call {PHONE}", color=NAVY, align="center", link=TEL, size=16,
                weight=900, lh=1.4), mt=13),
], flex_direction="column", padding=dim(28, 28, 28, 28), background_background="classic",
   background_color=WHITE, border_radius=rad(15),
   width=cu("calc(46% - 26px)"), width_tablet=sl(100, "%"), width_mobile=sl(100, "%"))

final = section([
    con([eyebrow("Request a Written Quotation", color="#7CDDFF"),
         h2("Request Your Sydney Carport Quote.", color=WHITE),
         adv(text("<p>Choose our single or double carport package, or request a quote for a "
                  "different size. We’ll confirm the applicable specifications, site "
                  "requirements and price in writing.</p>", color="#D1DDE8", size=18,
                  size_m=16), mt=16),
         check_grid(["Free, no-obligation enquiry", "Supply and installation pricing",
                     "Engineered aluminium construction", "Project-specific installation scope"],
                    color=WHITE, icon_color="#B9F0D9", mb=0)],
        flex_direction="column", width=cu("calc(54% - 26px)"), width_tablet=sl(100, "%"),
        width_mobile=sl(100, "%")),
    final_card,
], row=True, flex_align_items="center", flex_gap=gap(52), flex_gap_tablet=gap(34),
   background_background="gradient", background_color="#0A1C35",
   background_color_b="#102D51", background_gradient_type="linear",
   background_gradient_angle=sl(135, "deg"))

# ================================================================ 11. FOOTER
footer = section([
    text('<p><strong style="color:#ffffff">Patio Experts</strong> · Sydney Carport Builders</p>',
         color="#AAB8C6", size=13, size_m=13),
    text(f"<p>{PHONE}</p>", color="#AAB8C6", size=13),
], bg="#061427", pad=(24, 24), pad_m=(24, 96), row=True, html_tag="footer",
   flex_direction_tablet="row", flex_justify_content="space-between",
   flex_align_items="center", flex_align_items_mobile="center", flex_gap=gap(20),
   flex_gap_mobile=gap(5))

# ================================================================ 12. MOBILE CTA
mobile_cta = con([
    adv(button("Call Now", TEL, "soft", full=True, compact=True),
        width="calc(44.4% - 4px)"),
    adv(button("Request Quote", "#quote", "primary", full=True, compact=True),
        width="calc(55.6% - 4px)"),
], position="fixed", _offset_orientation_h="start", _offset_x=sl(0),
   _offset_orientation_v="end", _offset_y_end=sl(0), width=sl(100, "%"), z_index=80,
   flex_direction="row", flex_wrap="nowrap", flex_gap=gap(8), flex_align_items="center",
   padding=dim(9, 10, 9, 10), background_background="classic", background_color=WHITE,
   border_border="solid", border_width=dim(1, 0, 0, 0), border_color=LINE,
   hide_desktop="hidden-desktop", hide_tablet="hidden-tablet",
   **shadow("box_shadow", 0, -8, 25, 0, "rgba(0,0,0,0.12)"))

# ================================================================ assemble
content = [topbar, hero, proofbar, packages, gallery, before_after, why, process,
           qualify, faq, final, footer, mobile_cta]
for c in content:
    c["settings"].setdefault("overflow", "hidden")

template = {"version": "0.4", "title": "Patio Experts — Single & Double Carport Packages",
            "type": "page", "content": content,
            "page_settings": {"template": "elementor_canvas", "hide_title": "yes"}}

def stats(els):
    c = w = single = depth = 0
    def walk(es, d, cd):
        nonlocal c, w, single, depth
        for e in es:
            if e["elType"] == "container":
                c += 1; cd2 = cd + 1
                if len(e.get("elements", [])) == 1: single += 1
            else:
                w += 1; cd2 = cd
            depth = max(depth, cd2)
            walk(e.get("elements", []), d + 1, cd2)
    walk(els, 0, 0)
    return c, w, single, depth

out = sys.argv[1] if len(sys.argv) > 1 else "patio-experts-landing.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(template, f, ensure_ascii=False, separators=(",", ":"))
c, w, single, depth = stats(content)
print(f"wrote {out}: {c} containers, {w} widgets, {single} single-child containers, "
      f"max {depth} containers stacked")
