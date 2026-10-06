#!/usr/bin/env python3
"""
Elementor page-template JSON for "Final Revised Landing Page.html"
(Aussie Carport Kits — before/after project carousel version).

Built with flexbox containers + core widgets, plus two Elementor Pro widgets:
  - nested-carousel  (the before/after project slider)
  - form             (the quote form)
No HTML/code widgets anywhere.
"""
import json, itertools, sys

IMG_BASE = "https://raw.githubusercontent.com/anirudhatalmale6-alt/aussie-carport-kits-elementor/main/images"

# ---------------------------------------------------------------- tokens
INK      = "#111B27"
INK2     = "#182431"
TEXT     = "#5F6670"
GREEN    = "#36D11C"
GREEN_D  = "#2AA414"
PALE     = "#F5F7F4"
LINE     = "#D9DDD8"
DARKBG   = "#101B26"
WHITE    = "#FFFFFF"
EYE      = "#319927"
BODY_F   = "Poppins"
HEAD_F   = "Sora"
WRAP     = "min(1140px, calc(100% - 40px))"
SHADOW   = (0, 16, 38, 0, "rgba(18,31,22,0.11)")

_ids = itertools.count(0x300000)
def eid():
    return format(next(_ids), '07x')

# ---------------------------------------------------------------- helpers
def dim(t, r, b, l, unit="px"):
    return {"unit": unit, "top": str(t), "right": str(r), "bottom": str(b),
            "left": str(l), "isLinked": t == r == b == l}

def rad(v): return dim(v, v, v, v)
def sl(size, unit="px"): return {"unit": unit, "size": size, "sizes": []}
def cu(expr): return {"unit": "custom", "size": expr, "sizes": []}
def gap(v, unit="px"):
    return {"unit": unit, "size": v, "column": str(v), "row": str(v), "isLinked": True}
def gapxy(c, r, unit="px"):
    return {"unit": unit, "size": c, "column": str(c), "row": str(r), "isLinked": False}

def typo(prefix="typography", size=None, weight=None, lh=None, ls=None, transform=None,
         size_t=None, size_m=None, lh_unit="em", family=BODY_F):
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
    if "width" in st:                              # desktop width never reaches mobile
        st.setdefault("width_tablet", st["width"])
        st.setdefault("width_mobile", st["width"])
    return {"id": eid(), "elType": "container", "settings": st,
            "elements": children or [], "isInner": False}

def widget(wtype, **st):
    return {"id": eid(), "elType": "widget", "settings": st,
            "elements": [], "widgetType": wtype}

def section(children, bg=None, element_id=None, gap_v=0, pad=(92, 92), **extra):
    s = {"content_width": "boxed", "boxed_width": cu(WRAP),
         "boxed_width_tablet": cu(WRAP), "boxed_width_mobile": cu(WRAP),
         "flex_direction": "column", "flex_gap": gap(gap_v),
         "padding": dim(pad[0], 0, pad[1], 0),
         "padding_mobile": dim(round(pad[0] * 0.72), 0, round(pad[1] * 0.72), 0),
         "overflow": "hidden"}
    if bg:
        s["background_background"] = "classic"; s["background_color"] = bg
    if element_id:
        s["_element_id"] = element_id
    s.update(extra)
    return con(children, **s)

def rowc(children, gap_v=24, align=None, justify=None, stack="tablet", wrap=None, **extra):
    s = {"width": sl(100, "%"), "flex_direction": "row", "flex_gap": gap(gap_v),
         "flex_wrap": wrap or "nowrap"}
    if align:   s["flex_align_items"] = align
    if justify: s["flex_justify_content"] = justify
    if stack:
        s[f"flex_direction_{stack}"] = "column"
        if stack == "tablet":
            s["flex_direction_mobile"] = "column"
    s.update(extra)
    return con(children, **s)

def colc(children, width=None, width_t=100, width_m=100, gap_v=0, **extra):
    s = {"flex_direction": "column", "flex_gap": gap(gap_v)}
    for k, v in (("width", width), ("width_tablet", width_t), ("width_mobile", width_m)):
        if v is not None:
            s[k] = v if isinstance(v, dict) else sl(v, "%")
    s.update(extra)
    return con(children, **s)

def heading(title, tag="h2", color=INK, mb=None, **ty):
    s = {"title": title, "header_size": tag}
    if color: s["title_color"] = color
    s.update(typo(**ty))
    if mb is not None: s["_margin"] = dim(0, 0, mb, 0)
    return widget("heading", **s)

def text(html, color=TEXT, mb=None, mt=None, **ty):
    s = {"editor": html.replace("<p>", '<p style="margin:0">')}
    if color: s["text_color"] = color
    ty.setdefault("lh", 1.58)
    s.update(typo(**ty))
    if mb is not None or mt is not None:
        s["_margin"] = dim(mt or 0, 0, mb or 0, 0)
    return widget("text-editor", **s)

def image(fname, radius=22, with_shadow=True, h=None, h_t=None, h_m=None):
    s = {"image": {"url": f"{IMG_BASE}/{fname}", "id": "", "source": "library"},
         "image_size": "full", "width": sl(100, "%"),
         "image_border_radius": rad(radius)}
    if with_shadow: s.update(shadow("image_box_shadow", *SHADOW))
    if h:
        s["height"] = sl(h); s["object-fit"] = "cover"
        if h_t: s["height_tablet"] = sl(h_t)
        if h_m: s["height_mobile"] = sl(h_m)
    return widget("image", **s)

def eyebrow(txt, color=EYE, size=12.2, mb=12):
    return heading(txt, tag="div", color=color, size=size, weight=800, lh=1.2,
                   ls="0.115em", transform="uppercase", mb=mb)

def h2(txt, color=INK, size="clamp(2.45rem, 5.5vw, 4.7rem)", mb=18, size_m=42.4):
    return heading(txt, tag="h2", color=color, size=size, size_m=size_m, weight=700,
                   lh=0.98, ls="-0.045em", family=HEAD_F, mb=mb)

def section_head(kick, title, body=None, dark=False, size=None):
    kids = [eyebrow(kick, color="#70E15E" if dark else EYE),
            h2(title, color=WHITE if dark else INK, mb=18 if body else 0,
               **({"size": size} if size else {}))]
    if body:
        kids.append(text(f"<p>{body}</p>", color="#B9C0C8" if dark else TEXT, size=17.3))
    return colc(kids, width=cu("min(780px, 100%)"), gap_v=0,
                _flex_align_self="flex-start", margin=dim(0, 0, 36, 0))

def btn(label, link, kind="primary", full_mobile=True, compact=False):
    s = {"text": label, "size": "sm",
         "link": {"url": link, "is_external": "", "nofollow": "", "custom_attributes": ""},
         "border_radius": rad(10),
         "text_padding": dim(15, 12, 15, 12) if compact else dim(18, 24, 18, 24),
         "align": "left"}
    if full_mobile: s["align_mobile"] = "justify"
    s.update(typo(size=13.1 if compact else 15, weight=800, lh=1.3))
    if kind == "primary":
        s.update({"background_background": "classic", "background_color": GREEN,
                  "button_text_color": "#07120B",
                  "button_background_hover_background": "classic",
                  "button_background_hover_color": GREEN_D, "hover_color": "#07120B"})
        s.update(shadow("button_box_shadow", 0, 12, 30, 0, "rgba(54,209,28,0.22)"))
    elif kind == "dark":
        s.update({"background_background": "classic", "background_color": INK,
                  "button_text_color": WHITE,
                  "button_background_hover_background": "classic",
                  "button_background_hover_color": INK2, "hover_color": WHITE})
    elif kind == "soft":
        s.update({"background_background": "classic", "background_color": "#EEF2EF",
                  "button_text_color": "#1B2833",
                  "button_background_hover_background": "classic",
                  "button_background_hover_color": "#E2E8E3", "hover_color": "#1B2833"})
    else:  # ghost, over the hero photo
        s.update({"background_background": "classic",
                  "background_color": "rgba(255,255,255,0.08)", "button_text_color": WHITE,
                  "border_border": "solid", "border_width": dim(1, 1, 1, 1),
                  "border_color": "rgba(255,255,255,0.38)",
                  "button_background_hover_background": "classic",
                  "button_background_hover_color": "rgba(255,255,255,0.18)",
                  "hover_color": WHITE,
                  "button_hover_border_color": "rgba(255,255,255,0.5)",
                  "custom_css": "selector .elementor-button{backdrop-filter:blur(8px);}"})
    return widget("button", **s)

def chip(glyph, size=29, radius=8, bg="#EBF9E7", fg="#2B9C22", fs=14):
    return con([heading(glyph, tag="div", color=fg, size=fs, weight=800, lh=1)],
               width=sl(size), min_height=sl(size), _flex_size="none",
               flex_justify_content="center", flex_align_items="center",
               flex_gap=gap(0), background_background="classic",
               background_color=bg, border_radius=rad(radius))

def ticks(items, color=WHITE, size=13.8, weight=760, icon=GREEN, inline=True, mt=None):
    w = widget("icon-list",
               view="inline" if inline else "traditional",
               icon_list=[{"text": t, "selected_icon": {"value": "fas fa-check",
                                                        "library": "fa-solid"},
                           "_id": eid()} for t in items],
               space_between=gapxy(20, 10) if inline else sl(12),
               icon_color=icon, icon_size=sl(13), text_indent=sl(7), text_color=color,
               **typo(prefix="icon_typography", size=size, size_m=size - 1.4,
                      weight=weight, lh=1.42))
    if mt: w["settings"]["_margin"] = dim(mt, 0, 0, 0)
    return w

def card(children, featured=False, bg=WHITE, padding=30, radius=20, **extra):
    s = {"background_background": "classic", "background_color": bg,
         "border_radius": rad(radius),
         "padding": dim(padding, padding, padding, padding),
         "padding_mobile": dim(24, 24, 24, 24), "flex_gap": gap(0),
         "border_border": "solid",
         "border_width": dim(2, 2, 2, 2) if featured else dim(1, 1, 1, 1),
         "border_color": "#42B92F" if featured else LINE}
    if featured:
        s.update(shadow("box_shadow", 0, 16, 36, 0, "rgba(54,209,28,0.10)"))
    s.update(extra)
    return colc(children, **s)

def tag_pill(label):
    return con([heading(label, tag="div", color="#2E8928", size=10.7, weight=800,
                        lh=1.2, ls=0.5)],
               width=cu("fit-content"), _flex_align_self="flex-start",
               background_background="classic", background_color="#E8F6E4",
               border_radius=rad(999), padding=dim(7, 11, 7, 11), flex_gap=gap(0),
               margin=dim(0, 0, 14, 0))

# ================================================================ 1. HERO
hero_logo = heading('<b style="display:block;color:#42D928">AUSSIE</b>CARPORT KITS',
                    tag="div", color=WHITE, size=18.9, weight=800, lh=0.92,
                    ls="-0.03em", mb=26)
hero_eyebrow = heading("● &nbsp; Custom DIY Carport Kits", tag="div", color="#D9FFD4",
                       size=12.2, weight=800, lh=1.2, ls="0.115em",
                       transform="uppercase", mb=12)
hero_h1 = heading('DIY Carport Kits. '
                  '<span style="color:#36D11C">Engineered To Fit Your Home.</span>',
                  tag="h1", color=WHITE, size="clamp(3.35rem, 7.9vw, 6.4rem)",
                  size_m=50.4, weight=700, lh=0.91, ls="-0.045em", family=HEAD_F, mb=24)
hero_lead = text("<p>Send us your approximate size and postcode. We configure the "
                 "engineered aluminium frame, genuine Colorbond roofing and required "
                 "components into one complete carport kit &mdash; ready for you, your "
                 "builder or your handyman to install.</p>",
                 color="rgba(255,255,255,0.91)", size=17.8, size_m=16, lh=1.58)
hero_lead_wrap = colc([hero_lead], width=cu("min(710px, 100%)"), margin=dim(0, 0, 22, 0))

hero_price = con([
    heading("Kits from", tag="div", color="rgba(255,255,255,0.73)", size=12.8,
            weight=800, lh=1.2, ls="0.045em", transform="uppercase"),
    heading("$2,720", tag="div", color=GREEN, size=33.9, size_m=29, weight=800,
            lh=1, ls="-0.05em", family=HEAD_F),
    heading("for a 2.7m × 5.0m freestanding kit*", tag="div",
            color="rgba(255,255,255,0.73)", size=12.8, weight=800, lh=1.2,
            ls="0.045em", transform="uppercase"),
], width=sl(100, "%"), flex_direction="row", flex_wrap="wrap",
   flex_align_items="baseline", flex_gap=gap(9), margin=dim(0, 0, 24, 0))

hero_actions = con([btn("GET MY EXACT KIT PRICE →", "#quote", "primary"),
                    btn("SEE REAL PROJECTS", "#projects", "ghost")],
                   width=sl(100, "%"), flex_direction="row", flex_wrap="wrap",
                   flex_align_items="center", flex_gap=gap(12),
                   flex_direction_mobile="column", flex_align_items_mobile="stretch")

hero_micro = text("<p>Approximate measurements are fine. No-obligation quote.</p>",
                  color="rgba(255,255,255,0.77)", size=13.1, weight=650, lh=1.5,
                  mt=15)

hero_inner = colc([hero_logo, hero_eyebrow, hero_h1, hero_lead_wrap, hero_price,
                   hero_actions, hero_micro,
                   ticks(["Custom sizes", "Engineered aluminium",
                          "Genuine Colorbond roofing", "Project support"],
                         size=13.8, mt=25)],
                  width=cu("min(760px, 100%)"), gap_v=0, _flex_align_self="flex-start",
                  padding=dim(54, 0, 68, 0),
                  padding_tablet=dim(150, 0, 235, 0),
                  padding_mobile=dim(128, 0, 270, 0))

hero_card = con([
    heading("Real Price Guidance", tag="div", color="#D9FFD4", size=10.6, weight=800,
            lh=1.2, ls="0.115em", transform="uppercase", mb=8),
    heading("From $2,720*", tag="div", color=GREEN, size=37.6, size_m=33.6, weight=800,
            lh=1, ls="-0.05em", family=HEAD_F, mb=8),
    heading("Start with a real kit price.", tag="h3", color=WHITE, size=22.7,
            weight=700, lh=1.05, ls="-0.045em", family=HEAD_F, mb=9),
    text("<p>Then get the exact price for your dimensions, configuration, colours and "
         "delivery area.</p>", color="rgba(255,255,255,0.77)", size=14.1, lh=1.55),
], z_index=3, position="absolute",
   _offset_orientation_h="end", _offset_x_end=cu("4vw"),
   _offset_x_end_tablet=sl(20), _offset_x_end_mobile=sl(20),
   _offset_orientation_v="end", _offset_y_end=sl(58),
   _offset_y_end_tablet=sl(38), _offset_y_end_mobile=sl(50),
   width=cu("min(360px, 30vw)"), width_tablet=cu("calc(100% - 40px)"),
   width_mobile=cu("calc(100% - 40px)"),
   flex_gap=gap(0), padding=dim(23, 23, 23, 23),
   background_background="classic", background_color="rgba(9,19,17,0.91)",
   border_border="solid", border_width=dim(1, 1, 1, 1),
   border_color="rgba(255,255,255,0.12)", border_radius=rad(18),
   custom_css="selector{backdrop-filter:blur(12px);}",
   **shadow("box_shadow", *SHADOW))

hero_fade = con([], z_index=1, position="absolute",
                _offset_orientation_h="start", _offset_x=sl(0),
                _offset_orientation_v="end", _offset_y_end=sl(0),
                width=sl(100, "%"), min_height=sl(190), flex_gap=gap(0),
                background_background="gradient",
                background_color="rgba(5,10,12,0)", background_color_stop=sl(0, "%"),
                background_color_b="rgba(5,10,12,0.62)",
                background_color_b_stop=sl(100, "%"),
                background_gradient_type="linear", background_gradient_angle=sl(180, "deg"))

hero_stage = con([hero_inner, hero_card], width=cu(WRAP),
                 flex_direction="column", flex_justify_content="flex-end",
                 flex_gap=gap(0), z_index=2, min_height=sl(790),
                 min_height_tablet=sl(900), min_height_mobile=sl(950))

hero = con([hero_fade, hero_stage], width=sl(100, "%"),
           min_height=sl(790), min_height_tablet=sl(900), min_height_mobile=sl(950),
           flex_direction="column", flex_justify_content="flex-end",
           flex_align_items="center", flex_gap=gap(0), overflow="hidden",
           background_background="classic",
           background_image={"url": f"{IMG_BASE}/lp4-hero.webp", "id": "",
                             "source": "library"},
           background_size="cover", background_repeat="no-repeat",
           background_position="initial",
           background_xpos=sl(50, "%"), background_ypos=sl(52, "%"),
           background_xpos_tablet=sl(61, "%"), background_ypos_tablet=sl(50, "%"),
           background_xpos_mobile=sl(61, "%"), background_ypos_mobile=sl(0, "%"),
           background_overlay_background="gradient",
           background_overlay_color="rgba(7,18,17,0.93)",
           background_overlay_color_stop=sl(38, "%"),
           background_overlay_color_b="rgba(7,18,17,0.20)",
           background_overlay_color_b_stop=sl(100, "%"),
           background_overlay_gradient_type="linear",
           background_overlay_gradient_angle=sl(90, "deg"),
           background_overlay_opacity=sl(1))

# ================================================================ 2. TRUST
def trust_pill(glyph, label):
    return colc([con([chip(glyph), heading(label, tag="div", color=INK, size=15.5,
                                           weight=700, lh=1.35)],
                     width=sl(100, "%"), flex_direction="row", flex_wrap="nowrap",
                     flex_align_items="center", flex_gap=gap(10))],
                width=cu("calc(25% - 9px)"), width_t=cu("calc(50% - 6px)"), width_m=100,
                min_height=sl(64), flex_justify_content="center",
                background_background="classic", background_color=WHITE,
                border_border="solid", border_width=dim(1, 1, 1, 1), border_color=LINE,
                border_radius=rad(14), padding=dim(16, 17, 16, 17))

trust = section([
    rowc([trust_pill("✓", "30+ years industry experience"),
          trust_pill("◇", "Engineered aluminium system"),
          trust_pill("▰", "Genuine Colorbond roofing"),
          trust_pill("⌂", "Professional installation available")],
         gap_v=12, stack=None, wrap="wrap", align="stretch"),
], bg=PALE, pad=(28, 28),
   border_border="solid", border_width=dim(0, 0, 1, 0), border_color="#E8ECE7")

# ================================================================ 3. PROJECTS
def ba_media(fname, badge, after=False):
    badge_box = con([heading(badge, tag="div",
                             color="#07120B" if after else WHITE,
                             size=10.9, size_m=9.8, weight=800, lh=1, ls="0.08em",
                             transform="uppercase")],
                    z_index=2, position="absolute",
                    _offset_orientation_h="start", _offset_x=sl(14), _offset_x_mobile=sl(10),
                    _offset_orientation_v="start", _offset_y=sl(14), _offset_y_mobile=sl(10),
                    width=cu("fit-content"), min_height=sl(30), min_height_mobile=sl(27),
                    flex_justify_content="center", flex_align_items="center",
                    flex_gap=gap(0), padding=dim(0, 11, 0, 11),
                    padding_mobile=dim(0, 9, 0, 9),
                    background_background="classic",
                    background_color=GREEN if after else "rgba(16,27,38,0.9)",
                    border_radius=rad(999),
                    **({} if after else {"border_border": "solid",
                                         "border_width": dim(1, 1, 1, 1),
                                         "border_color": "rgba(255,255,255,0.22)"}),
                    **shadow("box_shadow", 0, 6, 20, 0, "rgba(0,0,0,0.16)"))
    return colc([badge_box, image(fname, radius=0, with_shadow=False,
                                  h=500, h_t=430, h_m=235)],
                width=cu("calc(50% - 6px)"), width_t=cu("calc(50% - 6px)"), width_m=100,
                min_height=sl(500), min_height_tablet=sl(430), min_height_mobile=sl(235),
                overflow="hidden", border_radius=rad(15), border_radius_mobile=rad(12),
                background_background="classic", background_color="#DCE2DC",
                flex_gap=gap(0))

PROJECTS = [
    ("Completed Project 01", "lp4-project01-before.webp", "lp4-project01-after.webp"),
    ("Completed Project 02", "lp4-project02-before.webp", "lp4-project02-after.webp"),
    ("Completed Project 03", "lp4-project03-before.webp", "lp4-project03-after.webp"),
    ("Completed Project 04", "lp4-project04-before.webp", "lp4-project04-after.webp"),
]

def carousel_slide(title, before, after):
    """A locked inner container, exactly the shape Elementor Pro's nested carousel
    exports (see the sample template Stefan supplied)."""
    label = heading(title, tag="div", color=INK, size=15.4, size_m=13.1, weight=700,
                    lh=1.2, ls="-0.02em", family=HEAD_F)
    label["settings"]["_margin"] = dim(15, 0, 2, 0)
    pair = con([ba_media(before, "Before"), ba_media(after, "After", after=True)],
               width=sl(100, "%"), flex_direction="row", flex_wrap="nowrap",
               flex_gap=gap(12), flex_gap_mobile=gap(8),
               flex_direction_mobile="column", flex_align_items="stretch")
    slide = con([pair, label], width=sl(100, "%"), flex_gap=gap(0),
                padding=dim(16, 16, 16, 16), padding_mobile=dim(10, 10, 10, 10))
    slide["isInner"] = True
    slide["isLocked"] = True
    slide["settings"]["_title"] = title
    return slide

carousel = {
    "id": eid(), "elType": "widget", "widgetType": "nested-carousel",
    "settings": {
        "carousel_name": "Before and after customer projects",
        "carousel_items": [{"slide_title": p[0], "_id": eid()[:7]} for p in PROJECTS],
        "slides_to_show": "1",
    },
    "elements": [carousel_slide(*p) for p in PROJECTS],
}

ba_shell = con([carousel], width=sl(100, "%"), flex_gap=gap(0), overflow="hidden",
               background_background="classic", background_color=WHITE,
               border_border="solid", border_width=dim(1, 1, 1, 1), border_color=LINE,
               border_radius=rad(22), **shadow("box_shadow", *SHADOW))

proof_meta = con([
    heading("4 completed customer projects", tag="div", color="#6E767F", size=11.5,
            size_m=10.4, weight=800, lh=1.3, ls="0.075em", transform="uppercase"),
    heading("Swipe or use the arrows to view all 4", tag="div", color="#6E767F",
            size=11.5, size_m=10.4, weight=800, lh=1.3, ls="0.075em",
            transform="uppercase"),
], width=sl(100, "%"), flex_direction="row", flex_wrap="wrap",
   flex_justify_content="space-between", flex_align_items="center", flex_gap=gap(16),
   margin=dim(0, 0, 16, 0))

projects = section([
    section_head("Real Customer Projects",
                 "Real customer properties. Before and after the carport.",
                 "Four recently completed customer projects, shown before and after, so "
                 "you can judge the finished result for yourself."),
    proof_meta,
    ba_shell,
    ticks(["Actual customer project photos", "Real customer properties",
           "Before and after"], color="#737B82", size=12.2, weight=720,
          icon="#2AA51E", mt=15),
    text("<p>Project photos are examples of completed configurations. Your final size, "
         "layout, colours and component requirements are quoted to your project.</p>",
         color="#858B90", size=11.8, lh=1.55, mt=12),
], element_id="projects")

# ================================================================ 4. PRICING
def price_card(kick, title, price, note, items, label, kind, featured=False, tag=None):
    kids = []
    if tag: kids.append(tag_pill(tag))
    kids += [eyebrow(kick),
             heading(title, tag="h3", color=INK, size=28.8, size_m=25, weight=700,
                     lh=1.02, ls="-0.045em", family=HEAD_F, mb=8),
             con([heading(price, tag="div", color=INK, size=42.4, size_m=37, weight=800,
                          lh=1, ls="-0.055em", family=HEAD_F),
                  heading(note, tag="div", color="#777F87", size=12, weight=700, lh=1.6)],
                 width=sl(100, "%"), flex_direction="row", flex_wrap="wrap",
                 flex_align_items="baseline", flex_gap=gap(7),
                 margin=dim(13, 0, 14, 0)),
             ticks(items, color=INK, size=15.2, weight=400, icon="#2AA51E",
                   inline=False),
             con([btn(label, "#quote", kind)], width=sl(100, "%"),
                 _flex_align_self="flex-start", flex_gap=gap(0),
                 margin=dim(23, 0, 0, 0), _flex_size="grow",
                 flex_justify_content="flex-end")]
    return card(kids, featured=featured, padding=28,
                width=cu("calc(50% - 9px)"), width_t=100, width_m=100,
                min_height=sl(330))

pricing = section([
    section_head("Real Price Guidance",
                 "Start with a real price. Then quote your exact size.",
                 "You should not have to submit an enquiry just to discover whether the "
                 "product is even in your budget. These common sizes give you a genuine "
                 "starting point before we price your actual project."),
    rowc([price_card("Compact Single", "2.7m × 5.0m Freestanding", "$2,720", "from*",
                     ["Suited to compact single-car spaces",
                      "Engineered aluminium frame", "Genuine Colorbond roofing",
                      "Complete kit ready for installation"],
                     "PRICE MY PROJECT", "primary", featured=True, tag="BEST ENTRY POINT"),
          price_card("Popular Single", "3.0m × 6.1m Freestanding", "$3,530", "from*",
                     ["Extra length for larger vehicles", "Engineered aluminium frame",
                      "Genuine Colorbond roofing", "DIY or professional installation"],
                     "PRICE MY PROJECT", "dark")],
         gap_v=18, align="stretch"),
    rowc([price_card("Double Carport", "5.0m × 5.0m Freestanding", "$4,285", "from*",
                     ["Practical coverage for two vehicles",
                      "Clean architectural aluminium finish",
                      "Complete frame and roofing system",
                      "Frame and roof colour choices"],
                     "PRICE MY PROJECT", "dark"),
          price_card("Your Exact Project", "Custom Size / Attached Layout", "Custom",
                     "quote",
                     ["Quoted around your actual measurements",
                      "Attached and freestanding layouts available",
                      "Components matched to your configuration",
                      "Clear price before you decide"],
                     "GET MY EXACT PRICE", "dark")],
         gap_v=18, align="stretch", margin=dim(18, 0, 0, 0)),
    text("<p>*Prices shown are guide prices for the listed kit sizes. Final pricing "
         "varies with dimensions, configuration, roof profile, project requirements, "
         "delivery area and optional installation.</p>",
         color="#7B8188", size=12.2, lh=1.55, mt=15),
], bg=PALE, element_id="pricing")

# ================================================================ 5. STORY
def story_point(title, body):
    return con([chip("✓", size=30, fs=15),
                colc([heading(title, tag="div", color=INK, size=15.5, weight=700, lh=1.4),
                      text(f"<p>{body}</p>", size=14.1)],
                     width=None, width_t=None, width_m=None, gap_v=3, _flex_size="grow")],
               width=sl(100, "%"), flex_direction="row", flex_wrap="nowrap",
               flex_align_items="flex-start", flex_gap=gap(12))

story = section([
    rowc([
        colc([eyebrow("Configured Around Your Project"),
              h2("Not a one-size-fits-most box. A kit built around the carport you "
                 "actually need.", size="clamp(2.5rem, 5vw, 4.45rem)"),
              text("<p>Standard kits often force your home to fit the product. We work "
                   "the other way around: start with your space, review the layout and "
                   "configure the kit around the project.</p>", size=17.3),
              con([story_point("Custom sizing",
                               "Your quote is based on the dimensions and layout you "
                               "send us."),
                   story_point("Engineered aluminium framing",
                               "Clean square beams and 110 × 110 aluminium posts create "
                               "a more architectural finish."),
                   story_point("Major components matched together",
                               "Frame, roofing, guttering, flashings, brackets and "
                               "fixing components are brought together in one order."),
                   story_point("Support before you commit",
                               "Send approximate measurements, photos or plans and we "
                               "will tell you what else is needed to finalise the "
                               "configuration.")],
                  width=sl(100, "%"), flex_direction="column", flex_gap=gap(13),
                  margin=dim(24, 0, 26, 0)),
              con([btn("GET MY PROJECT PRICE", "#quote", "primary")],
                  width=sl(100, "%"), _flex_align_self="flex-start", flex_gap=gap(0)),
              ], width=cu("calc(50% - 25px)")),
        colc([image("lp4-story.webp")], width=cu("calc(50% - 25px)")),
    ], gap_v=50, align="center")])

# ================================================================ 6. INCLUDED
INCLUDED = ["Engineered aluminium beams", "110 × 110 aluminium posts",
            "Genuine Colorbond roof sheets", "Colorbond guttering",
            "Required flashings", "Beam brackets",
            "Gutter clips", "Screws, bolts &amp; rivets",
            "Silicone sealant", "Downpipe components",
            "Installation guide", "Project consultation &amp; support"]

def included_item(label):
    return colc([con([heading("✓", tag="div", color="#70E15E", size=14, weight=800, lh=1.4),
                      heading(label, tag="div", color=WHITE, size=14.1, weight=700,
                              lh=1.35)],
                     width=sl(100, "%"), flex_direction="row", flex_wrap="nowrap",
                     flex_align_items="flex-start", flex_gap=gap(9))],
                width=cu("calc(50% - 7px)"), width_t=cu("calc(50% - 7px)"), width_m=100,
                background_background="classic", background_color="#162332",
                border_border="solid", border_width=dim(1, 1, 1, 1),
                border_color="#334251", border_radius=rad(13),
                padding=dim(13, 14, 13, 14))

included_rows = [rowc([included_item(INCLUDED[i]), included_item(INCLUDED[i + 1])],
                      gap_v=14, stack=None, align="stretch",
                      margin=dim(0 if i == 0 else 10, 0, 0, 0))
                 for i in range(0, len(INCLUDED), 2)]

included = section([
    rowc([
        colc([rowc([colc([image("lp4-detail-1.webp", radius=18, h=520, h_t=420, h_m=280)],
                         width=cu("calc(50% - 6px)")),
                    colc([image("lp4-detail-2.webp", radius=18, h=520, h_t=420, h_m=280)],
                         width=cu("calc(50% - 6px)"))],
                   gap_v=12, stack="mobile", align="stretch")],
             width=cu("calc(46% - 25px)")),
        colc([eyebrow("One Complete Kit", color="#70E15E"),
              h2("Everything that should arrive together, arrives together.",
                 color=WHITE, size="clamp(2.5rem, 5vw, 4.45rem)"),
              text("<p>Your quote clearly sets out what is included for your project, so "
                   "you know what you are paying for before you order and do not have to "
                   "piece the major system together from multiple suppliers.</p>",
                   color="#B9C0C8", size=17.3),
              con(included_rows, width=sl(100, "%"), flex_direction="column",
                  flex_gap=gap(0), margin=dim(24, 0, 0, 0)),
              con([text("<p>The exact component list depends on your configuration. Your "
                        "project quote is the source of truth for what is supplied.</p>",
                        color="#C9D1D8", size=14.1, weight=650, lh=1.5)],
                  width=sl(100, "%"), background_background="classic",
                  background_color="#1A2A38", border_border="solid",
                  border_width=dim(1, 1, 1, 1), border_color="#354656",
                  border_radius=rad(14), padding=dim(16, 18, 16, 18),
                  flex_gap=gap(0), margin=dim(20, 0, 0, 0))],
             width=cu("calc(54% - 25px)")),
    ], gap_v=50, align="center")], bg=DARKBG, element_id="included")

# ================================================================ 7. STEPS
def step_card(n, title, body):
    num = con([heading(n, tag="div", color=WHITE, size=17, weight=800, lh=1)],
              width=sl(44), min_height=sl(44), _flex_size="none",
              flex_justify_content="center", flex_align_items="center", flex_gap=gap(0),
              background_background="classic", background_color=INK,
              border_radius=rad(50), margin=dim(0, 0, 32, 0),
              margin_mobile=dim(0, 0, 26, 0))
    return colc([num,
                 heading(title, tag="h3", color=INK, size=19.8, weight=700, lh=1.25,
                         ls="-0.045em", family=HEAD_F, mb=8),
                 text(f"<p>{body}</p>", size=14.6)],
                width=cu("calc(25% - 12px)"), width_t=cu("calc(50% - 8px)"), width_m=100,
                background_background="classic", background_color=WHITE,
                border_border="solid", border_width=dim(1, 1, 1, 1), border_color=LINE,
                border_radius=rad(18), padding=dim(25, 25, 25, 25))

steps = section([
    section_head("Simple From Enquiry To Delivery",
                 "You do not need perfect plans to get a useful price.",
                 "Approximate dimensions are enough to start the conversation. We review "
                 "what you send, identify any missing details and move you toward a "
                 "clear project-specific quote."),
    rowc([step_card("1", "Send your size &amp; postcode",
                    "Approximate width and length are fine for the first review. Add "
                    "photos or plans if you have them."),
          step_card("2", "We review the layout",
                    "We look at the carport type, fixing approach and project details "
                    "and tell you what else we need."),
          step_card("3", "Receive a clear quote",
                    "Your quote sets out the proposed configuration, included components "
                    "and price before you decide."),
          step_card("4", "Choose how to install",
                    "Install it yourself, use your own trade, or ask us about "
                    "professional installation for your project.")],
         gap_v=16, stack=None, wrap="wrap", align="stretch")], bg=PALE)

# ================================================================ 8. DIY
diy = section([
    section_head("Is DIY Right For You?",
                 "DIY can save on installation &mdash; but it should match your "
                 "capability.",
                 "We would rather help you choose the right path than pretend every "
                 "homeowner should install a carport themselves."),
    rowc([
        card([tag_pill("PRIMARY OPTION"), eyebrow("DIY Kit"),
              heading("A strong fit if you are comfortable with practical construction "
                      "work.", tag="h3", color=INK, size=32, size_m=27, weight=700,
                      lh=1, ls="-0.045em", family=HEAD_F, mb=12),
              text("<p>If you use normal power tools confidently, have building "
                   "experience, or have a capable builder, handyman or friend helping, a "
                   "DIY kit gives you control over the project while avoiding a full "
                   "supply-and-install price.</p>", size=16, mb=16),
              ticks(["You want control over when the project is completed",
                     "You have capable help for lifting, positioning and fixing",
                     "You want the major components supplied together",
                     "You want product support if a question comes up"],
                    color=INK, size=15.2, weight=400, icon="#2AA51E", inline=False),
              con([btn("GET MY DIY KIT PRICE", "#quote", "primary")],
                  width=sl(100, "%"), _flex_align_self="flex-start", flex_gap=gap(0),
                  margin=dim(23, 0, 0, 0))],
             featured=True, width=cu("calc(64% - 10px)"), width_t=100, width_m=100),
        card([eyebrow("Prefer It Done For You?"),
              heading("Ask for an installed price.", tag="h3", color=INK, size=32,
                      size_m=27, weight=700, lh=1, ls="-0.045em", family=HEAD_F, mb=12),
              text("<p>If DIY is not the right fit, tell us when you enquire. We can "
                   "discuss professional installation without making you restart the "
                   "quoting process somewhere else.</p>", size=16, mb=16),
              ticks(["Same project-specific configuration",
                     "Professional installation option",
                     "Quoted to the site and project requirements"],
                    color=INK, size=15.2, weight=400, icon="#2AA51E", inline=False),
              con([btn("ASK ABOUT INSTALLATION", "#quote", "dark")],
                  width=sl(100, "%"), _flex_align_self="flex-start", flex_gap=gap(0),
                  margin=dim(23, 0, 0, 0)),
              text("<p>Installation availability and pricing depend on location, site "
                   "conditions, access, project size and final installer assessment.</p>",
                   color="#7B8188", size=12.2, lh=1.5, mt=9)],
             bg="#F9FAF9", width=cu("calc(36% - 10px)"), width_t=100, width_m=100),
    ], gap_v=20, align="stretch")])

# ================================================================ 9. COMPARE
CB = "#344251"
def cmp_row(a, b, c, head=False):
    def cell(txt, width, color, weight, bg=None):
        s = {"width": sl(width, "%"), "width_tablet": sl(width, "%"),
             "width_mobile": cu("calc(190px)"),
             "padding": dim(17, 16, 17, 16), "padding_mobile": dim(13, 10, 13, 10),
             "flex_gap": gap(0), "flex_justify_content": "flex-start"}
        if not head:
            s.update({"border_border": "solid", "border_width": dim(0, 0, 1, 0),
                      "border_color": CB})
        if bg:
            s.update({"background_background": "classic", "background_color": bg})
        return con([heading(txt, tag="div", color=color, size=14.4, size_m=12.2,
                            weight=weight, lh=1.45)], **s)
    return con([cell(a, 24, WHITE, 800 if head else 700, "#1A2635" if head else None),
                cell(b, 36, WHITE if head else "#B9C0C8", 800 if head else 400,
                     "#1A2635" if head else None),
                cell(c, 40, WHITE if head else "#77E562", 800 if head else 700,
                     "#1A2635" if head else None)],
               width=sl(100, "%"), flex_direction="row", flex_wrap="nowrap",
               flex_gap=gap(0), flex_align_items="stretch")

compare = section([
    section_head("Why Engineered Aluminium",
                 "Choose the material you want to keep looking at every day.",
                 "A carport is a permanent, highly visible part of the home. Material "
                 "choice affects handling, corrosion behaviour and the finished "
                 "architectural look &mdash; not just the upfront kit price.", dark=True),
    con([con([cmp_row("What matters", "Typical roll-formed steel kit",
                      "Aussie Carport Kits aluminium", head=True),
              cmp_row("Corrosion behaviour",
                      "Depends on the protective coating remaining intact.",
                      "Aluminium is naturally corrosion resistant and does not rust in "
                      "the same way as carbon steel."),
              cmp_row("Handling on site",
                      "Steel sections can be heavier to manoeuvre depending on profile "
                      "and span.",
                      "Lower material density can make components easier to handle and "
                      "position, subject to section size."),
              cmp_row("Finished appearance",
                      "Folded profiles often create a more utilitarian kit aesthetic.",
                      "Clean square aluminium profiles create a sharper residential "
                      "architectural finish."),
              cmp_row("Buying priority",
                      "Often selected primarily around lowest upfront kit cost.",
                      "Designed for buyers balancing fit, finish and long-term "
                      "appearance.")],
             width=cu("min(100%, 1140px)"), width_mobile=cu("max(620px, 100%)"),
             flex_direction="column", flex_gap=gap(0), overflow="hidden",
             border_border="solid", border_width=dim(1, 1, 1, 1), border_color=CB,
             border_radius=rad(16))],
        width=sl(100, "%"), flex_gap=gap(0), overflow="auto",
        margin=dim(32, 0, 0, 0)),
    text("<p>General material comparison only. Exact component weight, coating "
         "performance, structural requirements and engineering depend on the specific "
         "products and project.</p>", color="#8F9AA4", size=12.2, lh=1.55, mt=12),
], bg=DARKBG)

# ================================================================ 10. RESULT
result = section([
    rowc([
        colc([eyebrow("More Than A Roof Over The Driveway"),
              h2("A carport should look like it belongs with the home.",
                 size="clamp(2.5rem, 5vw, 4.3rem)"),
              text("<p>That is why the offer is built around fit, finish and a clear "
                   "configuration &mdash; not forcing every customer into the nearest "
                   "standard box size.</p>", size=17.3),
              con([btn("GET MY EXACT PRICE", "#quote", "primary")],
                  width=sl(100, "%"), _flex_align_self="flex-start", flex_gap=gap(0),
                  margin=dim(24, 0, 0, 0))],
             width=cu("calc(41% - 24px)")),
        colc([image("lp4-result-1.webp", radius=22, h=370, h_t=420, h_m=260),
              rowc([colc([image("lp4-result-2.webp", radius=22, h=230, h_m=260)],
                         width=cu("calc(50% - 6px)")),
                    colc([image("lp4-result-3.webp", radius=22, h=230, h_m=260)],
                         width=cu("calc(50% - 6px)"))],
                   gap_v=12, stack="mobile", align="stretch", margin=dim(12, 0, 0, 0))],
             width=cu("calc(59% - 24px)")),
    ], gap_v=48, align="center")], bg=PALE)

# ================================================================ 11. QUOTE
def mini_benefit(title, body):
    return con([chip("✓", size=32, fs=15),
                colc([heading(title, tag="div", color=INK, size=15.5, weight=700, lh=1.4),
                      text(f"<p>{body}</p>", size=13.9)],
                     width=None, width_t=None, width_m=None, gap_v=2, _flex_size="grow")],
               width=sl(100, "%"), flex_direction="row", flex_wrap="nowrap",
               flex_align_items="flex-start", flex_gap=gap(12))

form_widget = widget(
    "form", form_name="Carport Quote",
    form_fields=[
        {"custom_id": "name", "field_type": "text", "field_label": "Name",
         "placeholder": "Your name", "required": "true", "width": "100", "_id": eid()[:7]},
        {"custom_id": "phone", "field_type": "tel", "field_label": "Phone",
         "placeholder": "04xx xxx xxx", "required": "true", "width": "50", "_id": eid()[:7]},
        {"custom_id": "postcode", "field_type": "text", "field_label": "Postcode",
         "placeholder": "e.g. 2148", "required": "true", "width": "50", "_id": eid()[:7]},
        {"custom_id": "width", "field_type": "text", "field_label": "Approx. width",
         "placeholder": "e.g. 3.5m", "required": "true", "width": "50", "_id": eid()[:7]},
        {"custom_id": "length", "field_type": "text", "field_label": "Approx. length",
         "placeholder": "e.g. 6.0m", "required": "true", "width": "50", "_id": eid()[:7]},
        {"custom_id": "type", "field_type": "select", "field_label": "What do you need?",
         "field_options": "DIY kit only\nDIY kit + installation price\nNot sure yet",
         "required": "", "width": "100", "_id": eid()[:7]},
        {"custom_id": "notes", "field_type": "textarea",
         "field_label": "Anything we should know? (optional)",
         "placeholder": "Attached or freestanding? Existing concrete? Preferred colours "
                        "or any useful details.",
         "rows": "4", "required": "", "width": "100", "_id": eid()[:7]},
        {"custom_id": "files", "field_type": "upload",
         "field_label": "Upload photos or plans (optional)",
         "file_sizes": "5", "multiple_files": "yes", "max_files": "5",
         "file_types": "jpg,jpeg,png,webp,pdf,heic",
         "required": "", "width": "100", "_id": eid()[:7]},
    ],
    input_size="md", show_labels="yes", mark_required="", label_position="above",
    button_text="GET MY CARPORT PRICE →", button_size="sm", button_align="stretch",
    button_width="100",
    submit_actions=["email"],
    email_to="info@aussiecarportkits.com.au",
    email_subject="New carport enquiry from your landing page",
    email_content="[all-fields]",
    email_from_name="Aussie Carport Kits Website",
    email_content_type="html",
    success_message="Thanks — we’ve got your details and will be in touch shortly.",
    error_message="Something went wrong. Please call us instead.",
    required_field_message="This field is required.",
    invalid_message="There’s a problem with one of the fields.",
    column_gap=gap(15), row_gap=gap(15), label_spacing=sl(7),
    field_border_radius=rad(10), field_border_border="solid",
    field_border_width=dim(1, 1, 1, 1), field_border_color="#CFD4D0",
    field_background_color=WHITE, field_text_color="#1B222A",
    field_text_padding=dim(14, 15, 14, 15),
    button_background_color=GREEN, button_text_color="#07120B",
    button_border_radius=rad(10), button_text_padding=dim(18, 24, 18, 24),
    **typo(prefix="label_typography", size=11.7, weight=800, transform="uppercase",
           ls="0.07em"),
    **typo(prefix="field_typography", size=15.5, weight=400),
    **typo(prefix="button_typography", size=15, weight=800),
)

form_kicker = con([chip("1", size=28, radius=50, bg="#EAF8E6", fg="#2A9C20", fs=13),
                   heading("Tell us the basics — it takes about a minute.", tag="div",
                           color="#3E484F", size=12.5, weight=800, lh=1.4)],
                  width=sl(100, "%"), flex_direction="row", flex_wrap="nowrap",
                  flex_align_items="center", flex_gap=gap(9), margin=dim(0, 0, 18, 0))

quote = section([
    rowc([
        colc([eyebrow("Get A Project-Specific Price"),
              h2("Tell us your size. We’ll work out the right kit and price.",
                 size="clamp(2.5rem, 5vw, 4.45rem)"),
              text("<p>You do not need to know every technical detail. Send the basics "
                   "and we will review the project, identify what else we need and "
                   "prepare the next step toward an accurate quote.</p>", size=17.3),
              con([mini_benefit("No-obligation quote",
                                "See the proposed kit and price before deciding whether "
                                "to proceed."),
                   mini_benefit("Approximate measurements are fine",
                                "We can tell you which details need to be confirmed "
                                "after the first review."),
                   mini_benefit("DIY first, installation optional",
                                "Buy the kit for DIY or ask us to price professional "
                                "installation if you need it.")],
                  width=sl(100, "%"), flex_direction="column", flex_gap=gap(17),
                  margin=dim(27, 0, 0, 0)),
              con([text('<p><strong style="color:#1B2833">Have photos or plans?</strong> '
                        "Upload them with your enquiry. They can help us understand the "
                        "site and reduce back-and-forth before quoting.</p>",
                        color="#4F5A61", size=13.4, lh=1.55)],
                  width=sl(100, "%"), background_background="classic",
                  background_color="#F4F9F2", border_border="solid",
                  border_width=dim(0, 0, 0, 4), border_color=GREEN,
                  border_radius=rad(10), padding=dim(15, 16, 15, 16),
                  flex_gap=gap(0), margin=dim(18, 0, 0, 0))],
             width=cu("calc(43% - 24px)")),
        colc([colc([form_kicker, form_widget,
                    text("<p>No obligation. Your details are used to respond to your "
                         "carport enquiry.</p>", color="#848A91", size=11.5, lh=1.5,
                         mt=10)],
                   width=100, gap_v=0,
                   background_background="classic", background_color=WHITE,
                   border_border="solid", border_width=dim(1, 1, 1, 1),
                   border_color=LINE, border_radius=rad(20),
                   padding=dim(28, 28, 28, 28), **shadow("box_shadow", *SHADOW))],
             width=cu("calc(57% - 24px)")),
    ], gap_v=48, align="flex-start")], element_id="quote")

# ================================================================ 12. FAQ
FAQ = [
    ("What exactly is included in a DIY carport kit?",
     "Your quote will set out the components included for your project. Depending on the "
     "configuration, this can include engineered aluminium posts and beams, Colorbond "
     "roofing, guttering, flashings, structural brackets, gutter clips, screws, rivets, "
     "bolts, silicone, downpipe components and an installation guide."),
    ("Can you customise the size?",
     "Yes. Custom sizing is one of the main advantages of the system. Send us your "
     "approximate width, length and postcode and we can review the layout and price a "
     "configuration suited to your space."),
    ("Can the carport be attached to my house?",
     "Yes. We can review attached and freestanding layouts. The right option depends on "
     "the property, fixing point and project requirements, so photos or plans are useful "
     "when you have them."),
    ("Do I need exact measurements before I enquire?",
     "No. Approximate dimensions are enough for the initial enquiry. We will tell you if "
     "photos, plans or more precise measurements are needed before the final "
     "configuration is confirmed."),
    ("Can my builder or handyman install the kit?",
     "Yes. You can purchase the kit and have your own builder, handyman or suitable trade "
     "install it. If you would prefer professional installation, select that option when "
     "you request your quote."),
    ("What if I am not confident installing it myself?",
     "Ask us about professional installation. Availability and pricing depend on your "
     "location, site conditions, access, project size and installer assessment."),
    ("What colours are available?",
     "You can choose from available frame and genuine Colorbond roofing colours so the "
     "finished carport works with the look of your home. Available colours can vary by "
     "component and roof profile."),
    ("How quickly can my kit be delivered?",
     "Lead time depends on the kit configuration, roof type, stock availability and "
     "delivery location. We will confirm the expected timeframe for your order before you "
     "proceed."),
]

def faq_item(q, a):
    tog = widget("toggle",
                 tabs=[{"tab_title": q, "tab_content": f'<p style="margin:0">{a}</p>',
                        "_id": eid()[:7]}],
                 selected_icon={"value": "fas fa-plus", "library": "fa-solid"},
                 selected_active_icon={"value": "fas fa-minus", "library": "fa-solid"},
                 title_html_tag="div", faq_schema="yes", icon_align="right",
                 border_width=sl(0), border_color="#00000000",
                 title_background="#FFFFFF00", title_color=INK, tab_active_color=INK,
                 icon_color="#30A923", icon_active_color="#30A923", icon_space=sl(20),
                 content_background_color="#FFFFFF00", content_color=TEXT,
                 title_padding=dim(22, 0, 22, 0), content_padding=dim(0, 0, 22, 0),
                 **typo(prefix="title_typography", size=17.3, weight=800, lh=1.4),
                 **typo(prefix="content_typography", size=15.5, weight=400, lh=1.58))
    return con([tog], width=sl(100, "%"), flex_gap=gap(0),
               border_border="solid", border_width=dim(0, 0, 1, 0), border_color=LINE)

faq = section([
    section_head("Common Questions", "Questions worth answering before you order.",
                 "The aim is to make the buying decision clear before you commit "
                 "&mdash; what you are getting, what you need to provide and how the "
                 "project moves forward."),
    con([faq_item(q, a) for q, a in FAQ], width=sl(100, "%"), flex_direction="column",
        flex_gap=gap(0), border_border="solid", border_width=dim(1, 0, 0, 0),
        border_color=LINE),
], bg=PALE)

# ================================================================ 13. FINAL CTA
final_cta = section([
    rowc([
        colc([eyebrow("Ready For A Real Number?", color="#70E15E"),
              h2("Send your approximate size and get the price for your carport.",
                 color=WHITE, size="clamp(2.2rem, 4.8vw, 4.1rem)", mb=0, size_m=35.2),
              text("<p>No generic &ldquo;contact us for pricing&rdquo; loop. Give us the "
                   "basics and we can move toward a project-specific quote.</p>",
                   color="#B9C0C8", size=16, mt=12)],
             width=cu("min(720px, 100%)")),
        colc([con([btn("GET MY EXACT KIT PRICE →", "#quote", "primary")],
                  width=cu("fit-content"), _flex_align_self="flex-start",
                  flex_gap=gap(0))],
             width=cu("fit-content"), width_t=100, width_m=100, _flex_size="none"),
    ], gap_v=28, align="center", justify="space-between"),
], bg="#152330", pad=(72, 72))

# ================================================================ 14. FOOTER
footer = section([
    heading("AUSSIE CARPORT KITS", tag="div", color=WHITE, size=15.5, weight=700, lh=1.3),
    text("<p>Custom DIY carport kits in engineered aluminium, with professional "
         "installation available.</p>", color="#96A0AA", size=13.1, lh=1.55, mt=8),
], bg="#0C151E", pad=(34, 92), html_tag="footer")

# ================================================================ 15. MOBILE CTA
sticky = con([
    con([btn("SEE PRICES", "#pricing", "soft", compact=True)],
        width=cu("calc(37.5% - 4px)"), flex_gap=gap(0)),
    con([btn("GET MY PRICE", "#quote", "primary", compact=True)],
        width=cu("calc(62.5% - 4px)"), flex_gap=gap(0)),
], width=cu("calc(100% - 16px)"), position="fixed",
   _offset_orientation_h="start", _offset_x=sl(8),
   _offset_orientation_v="end", _offset_y_end=sl(8),
   z_index=99, flex_direction="row", flex_wrap="nowrap", flex_align_items="center",
   flex_gap=gap(8), padding=dim(8, 8, 8, 8),
   background_background="classic", background_color=WHITE,
   border_border="solid", border_width=dim(1, 1, 1, 1), border_color="#D8DDD8",
   border_radius=rad(13), hide_desktop="hidden-desktop", hide_tablet="hidden-tablet",
   **shadow("box_shadow", 0, 12, 34, 0, "rgba(0,0,0,0.18)"))

# ================================================================ assemble
content = [hero, trust, projects, pricing, story, included, steps, diy, compare,
           result, quote, faq, final_cta, footer, sticky]
for _c in content:
    _c["settings"].setdefault("overflow", "hidden")
# the comparison table scrolls sideways on small screens, so that section must not clip
compare["settings"]["overflow"] = ""

template = {
    "version": "0.4",
    "title": "Aussie Carport Kits — DIY Carport Kits Landing Page",
    "type": "page",
    "content": content,
    "page_settings": {"template": "elementor_canvas", "hide_title": "yes"},
}

out = sys.argv[1] if len(sys.argv) > 1 else "aussie-carport-landing-v4.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(template, f, ensure_ascii=False, separators=(",", ":"))

def count(els):
    return sum(1 + count(e.get("elements", [])) for e in els)
print(f"wrote {out}: {count(content)} elements, {len(json.dumps(template))} bytes")
