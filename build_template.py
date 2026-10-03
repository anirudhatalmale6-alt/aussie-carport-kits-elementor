#!/usr/bin/env python3
"""
Builds an Elementor page-template JSON that recreates
aussie_carport_kits_conversion_redesign.html using Elementor flexbox
containers + core widgets (+ the Elementor Pro Form widget for the quote form).
"""
import json, itertools, sys

IMG_BASE = "https://raw.githubusercontent.com/anirudhatalmale6-alt/aussie-carport-kits-elementor/main/images"

# ---------------------------------------------------------------- tokens
INK      = "#14202C"
INK_SOFT = "#243342"
TOPBAR   = "#0F1923"
GREEN    = "#52D52D"
GREEN2   = "#3ABB1D"
GREEN_TX = "#0C2811"
SOFT     = "#F4F7F4"
LINE     = "#DDE5DF"
LEAD     = "#40515F"
SUBC     = "#657481"
WHITE    = "#FFFFFF"
FONT     = "Inter"
MAXW     = 1132          # 1180 wrap - 2*24 padding
PAD_X    = "24"

_ids = itertools.count(0x100000)
def eid():
    return format(next(_ids), '07x')

# ---------------------------------------------------------------- helpers
def dim(top, right, bottom, left, unit="px"):
    linked = top == right == bottom == left
    return {"unit": unit, "top": str(top), "right": str(right),
            "bottom": str(bottom), "left": str(left), "isLinked": linked}

def rad(v):
    return dim(v, v, v, v)

def sl(size, unit="px"):
    return {"unit": unit, "size": size, "sizes": []}

def cu(expr):
    """Elementor 'custom' slider unit — emits the raw CSS value."""
    return {"unit": "custom", "size": expr, "sizes": []}

def gap(v, unit="px"):
    return {"unit": unit, "size": v, "column": str(v), "row": str(v), "isLinked": True}

def gapxy(col, row, unit="px"):
    return {"unit": unit, "size": col, "column": str(col), "row": str(row), "isLinked": False}

def typo(prefix="typography", size=None, weight=None, lh=None, ls=None,
         transform=None, size_t=None, size_m=None, lh_unit="em", family=FONT,
         ls_m=None):
    s = {f"{prefix}_typography": "custom"}
    if family:    s[f"{prefix}_font_family"] = family
    if size:      s[f"{prefix}_font_size"] = cu(size) if isinstance(size, str) else sl(size)
    if size_t:    s[f"{prefix}_font_size_tablet"] = sl(size_t)
    if size_m:    s[f"{prefix}_font_size_mobile"] = sl(size_m)
    if weight:    s[f"{prefix}_font_weight"] = str(weight)
    if lh:        s[f"{prefix}_line_height"] = sl(lh, lh_unit)
    if ls is not None: s[f"{prefix}_letter_spacing"] = sl(ls)
    if ls_m is not None: s[f"{prefix}_letter_spacing_mobile"] = sl(ls_m)
    if transform: s[f"{prefix}_text_transform"] = transform
    return s

def shadow(group, h, v, blur, spread, color):
    """group is the Elementor group-control name, e.g. 'box_shadow',
    'button_box_shadow', 'image_box_shadow'."""
    return {f"{group}_box_shadow_type": "yes",
            f"{group}_box_shadow": {"horizontal": h, "vertical": v, "blur": blur,
                                    "spread": spread, "color": color}}

def con(children=None, **settings):
    settings.setdefault("content_width", "full")
    # Elementor's kit gives every container 10px padding by default, which the
    # reference HTML doesn't have. Zero it unless the design calls for padding.
    settings.setdefault("padding", dim(0, 0, 0, 0))
    # Elementor deliberately does NOT inherit the desktop container width down to
    # mobile, so mirror it explicitly unless a breakpoint value was given.
    if "width" in settings:
        settings.setdefault("width_tablet", settings["width"])
        settings.setdefault("width_mobile", settings["width"])
    return {"id": eid(), "elType": "container", "settings": settings,
            "elements": children or [], "isInner": False}

def section(children, bg=None, pad_top=78, pad_bottom=78, gap_v=34,
            element_id=None, **extra):
    s = {"content_width": "boxed",
         "boxed_width": sl(MAXW),
         "flex_direction": "column",
         "flex_gap": gap(gap_v),
         "padding": dim(pad_top, PAD_X, pad_bottom, PAD_X),
         "padding_mobile": dim(max(pad_top - 20, 0), "17", max(pad_bottom - 20, 0), "17")}
    if bg:
        s["background_background"] = "classic"
        s["background_color"] = bg
    if element_id:
        s["_element_id"] = element_id
    s.update(extra)
    return con(children, **s)

def row(children, gap_v=24, align=None, justify=None, wrap=None,
        stack_on="tablet", **extra):
    s = {"content_width": "full",
         "width": sl(100, "%"),
         "flex_direction": "row",
         "flex_gap": gap(gap_v)}
    if align:   s["flex_align_items"] = align
    if justify: s["flex_justify_content"] = justify
    # Elementor containers wrap by default; wrapping fires before flex-shrink, so a
    # row whose children + gap exceed 100% would break onto two lines. Rows shrink
    # instead unless wrapping is explicitly asked for.
    s["flex_wrap"] = wrap or "nowrap"
    if stack_on:
        s[f"flex_direction_{stack_on}"] = "column"
        if stack_on == "tablet":
            s["flex_direction_mobile"] = "column"
    s.update(extra)
    return con(children, **s)

def col(children, width=None, width_t=100, width_m=100, gap_v=12, **extra):
    s = {"content_width": "full", "flex_direction": "column", "flex_gap": gap(gap_v)}
    if width is not None:
        s["width"] = width if isinstance(width, dict) else sl(width, "%")
    if width_t is not None:
        s["width_tablet"] = width_t if isinstance(width_t, dict) else sl(width_t, "%")
    if width_m is not None:
        s["width_mobile"] = width_m if isinstance(width_m, dict) else sl(width_m, "%")
    s.update(extra)
    return con(children, **s)

def widget(wtype, **settings):
    return {"id": eid(), "elType": "widget", "settings": settings,
            "elements": [], "widgetType": wtype}

def heading(title, tag="h2", color=INK, align=None, link=None, **ty):
    s = {"title": title, "header_size": tag}
    if color: s["title_color"] = color
    if align: s["align"] = align
    if link:  s["link"] = {"url": link, "is_external": "", "nofollow": "",
                           "custom_attributes": ""}
    s.update(typo(**ty))
    return widget("heading", **s)

def text(html, color=None, align=None, **ty):
    # WordPress/theme CSS puts a bottom margin on <p>; the reference design doesn't.
    s = {"editor": html.replace("<p>", '<p style="margin:0">')}
    if color: s["text_color"] = color
    if align: s["align"] = align
    s.update(typo(**ty))
    return widget("text-editor", **s)

def button(label, link, variant="primary", align="left", size_px=None, full=False,
           full_mobile=False, compact=False):
    s = {"text": label, "size": "sm",
         "link": {"url": link, "is_external": "", "nofollow": "", "custom_attributes": ""},
         "border_radius": rad(8) if compact else rad(10),
         "text_padding": dim(10, 14, 10, 14) if compact else dim(14, 20, 14, 20)}
    s.update(typo(size=size_px or (14 if compact else 15), weight=700, lh=1.1))
    if full:
        s["align"] = "justify"
    elif align:
        s["align"] = align
    if full_mobile:
        s["align_mobile"] = "justify"
    if variant == "primary":
        s.update({"background_background": "classic", "background_color": GREEN,
                  "button_text_color": GREEN_TX,
                  "button_background_hover_background": "classic",
                  "button_background_hover_color": GREEN2,
                  "hover_color": GREEN_TX})
        s.update(shadow("button_box_shadow", 0, 7, 18, 0, "rgba(82,213,45,0.25)"))
    elif variant == "dark":
        s.update({"background_background": "classic", "background_color": INK,
                  "button_text_color": WHITE,
                  "button_background_hover_background": "classic",
                  "button_background_hover_color": INK_SOFT,
                  "hover_color": WHITE})
    else:  # outline
        s.update({"background_background": "classic", "background_color": WHITE,
                  "button_text_color": INK,
                  "border_border": "solid", "border_width": dim(1, 1, 1, 1),
                  "border_color": "#B9C7BD",
                  "button_background_hover_background": "classic",
                  "button_background_hover_color": SOFT,
                  "hover_color": INK,
                  "button_hover_border_color": "#B9C7BD"})
    return widget("button", **s)

def image(fname, radius=20, shadow_cfg=None, w=100):
    s = {"image": {"url": f"{IMG_BASE}/{fname}", "id": "", "alt": "", "source": "library"},
         "image_size": "full",
         "width": sl(w, "%"),
         "image_border_radius": rad(radius)}
    if shadow_cfg:
        s.update(shadow("image_box_shadow", *shadow_cfg))
    return widget("image", **s)

def pill(html):
    return con([text(html, color=INK, size=14, weight=600, lh=1.3)],
               content_width="full",
               _flex_align_self="flex-start", width=cu("fit-content"),
               background_background="classic", background_color=WHITE,
               border_border="solid", border_width=dim(1, 1, 1, 1), border_color=LINE,
               border_radius=rad(9),
               padding=dim(9, 12, 9, 12), flex_gap=gap(0))

def checklist(items):
    return widget("icon-list",
                  icon_list=[{"text": t,
                              "selected_icon": {"value": "fas fa-check", "library": "fa-solid"},
                              "_id": eid()} for t in items],
                  space_between=sl(10),
                  icon_color="#2D9E1F",
                  icon_size=sl(14),
                  text_indent=sl(9),
                  text_color=INK,
                  **typo(prefix="icon_typography", size=15, weight=500, lh=1.45))

def kicker(txt, color="#31901F"):
    return heading(txt, tag="div", color=color, size=12, weight=800,
                   transform="uppercase", ls=1)

def h2(txt, color=INK, size="clamp(34px, 4vw, 52px)"):
    return heading(txt, tag="h2", color=color, size=size,
                   weight=800, lh=1.05, ls=-2)

def sub(txt, color=SUBC):
    return text(f"<p>{txt}</p>", color=color, size=18, lh=1.5)


# ---------------------------------------------------------------- 1. topbar
topbar = con([
    text('<p><b style="color:#ffffff">Premium engineered aluminium carport kits</b> '
         '&middot; DIY or professional installation available</p>',
         color="#DCE6EE", align="center", size=13, lh=1.5)
], content_width="full", width=sl(100, "%"),
   background_background="classic", background_color=TOPBAR,
   padding=dim(8, 16, 8, 16), flex_direction="column",
   flex_align_items="center", flex_gap=gap(0))

# ---------------------------------------------------------------- 2. header
brand_heading = heading('AUSSIE <span style="color:#3ABB1D">CARPORT KITS</span>',
                        tag="div", color=INK, size=22, size_m=18, weight=800,
                        ls=-0.5, lh=1)
brand_heading["settings"]["_flex_size"] = "none"

header = con([
    brand_heading,
    con([
        heading("Call for advice", tag="div", color=INK, link="tel:+61000000000",
                size=14, weight=700, lh=1,
                ),
        button("Why aluminium?", "#compare", variant="outline", compact=True),
        button("Get My Price", "#quote", variant="primary", compact=True),
    ], content_width="full", flex_direction="row", flex_align_items="center",
       flex_gap=gap(10), flex_wrap="nowrap", _flex_size="none",
       width=cu("fit-content"), flex_justify_content="flex-end"),
], content_width="boxed", boxed_width=sl(MAXW),
   html_tag="header",
   flex_direction="row", flex_align_items="center",
   flex_justify_content="space-between", flex_gap=gap(20), flex_wrap="nowrap",
   min_height=sl(74), min_height_mobile=sl(66),
   padding=dim(0, PAD_X, 0, PAD_X), padding_mobile=dim(0, "17", 0, "17"),
   background_background="classic", background_color="rgba(255,255,255,0.96)",
   border_border="solid", border_width=dim(0, 0, 1, 0), border_color="#EDF1EE",
   z_index=30, sticky="top", sticky_on=["desktop", "tablet", "mobile"],
   sticky_offset=0)

# tablet/mobile: hide the phone link + outline button (matches the CSS media rules)
header["elements"][1]["elements"][0]["settings"].update(
    {"hide_tablet": "hidden-tablet", "hide_mobile": "hidden-mobile"})
header["elements"][1]["elements"][1]["settings"].update(
    {"hide_mobile": "hidden-mobile"})

# ---------------------------------------------------------------- 3. hero (revised)
HERO_BG   = "hero-background-1284x1109.jpg"
HERO_LOGO = "aussie-carport-kits-logo.png"

# green dot with its soft ring
eyebrow_dot = con([], content_width="full", width=sl(9), min_height=sl(9),
                  _flex_size="none", flex_gap=gap(0),
                  background_background="classic", background_color="#60C62F",
                  border_radius=rad(50),
                  **shadow("box_shadow", 0, 0, 0, 6, "rgba(96,198,47,0.16)"))

hero_eyebrow = con([
    eyebrow_dot,
    heading("Custom DIY Carport Kits", tag="div", color="#D7F2CC",
            size=13, weight=800, transform="uppercase", ls=1.7, lh=1.2),
], content_width="full", width=cu("fit-content"), flex_direction="row",
   flex_align_items="center", flex_gap=gap(9), flex_wrap="nowrap",
   margin=dim(0, 0, 20, 0))

hero_h1 = heading('Your Space.<br>Your Size.<br>'
                  '<span style="color:#60C62F">One Complete Kit.</span>',
                  tag="h1", color=WHITE, size="clamp(46px, 6.2vw, 82px)",
                  size_m=44, weight=900, lh=0.98)
hero_h1["settings"]["typography_letter_spacing"] = cu("-0.055em")
hero_h1["settings"]["typography_line_height_mobile"] = sl(1.02, "em")
hero_h1["settings"].update(
    {"text_shadow_text_shadow_type": "yes",
     "text_shadow_text_shadow": {"horizontal": 0, "vertical": 12, "blur": 34,
                                 "color": "rgba(0,0,0,0.28)"}})

hero_sub = text("<p>Send us your measurements or plans and we&rsquo;ll configure a "
                "<strong style=\"color:#ffffff\">complete engineered aluminium carport "
                "kit</strong> to suit your home &mdash; ready for fast delivery to "
                "eligible Sydney areas.</p>",
                color="#E3E9ED", size=20, size_m=17, lh=1.55)
hero_sub["settings"].update(
    {"text_shadow_text_shadow_type": "yes",
     "text_shadow_text_shadow": {"horizontal": 0, "vertical": 8, "blur": 22,
                                 "color": "rgba(0,0,0,0.24)"}})

hero_sub_wrap = con([hero_sub], content_width="full", width=cu("min(680px, 100%)"),
                    flex_gap=gap(0), margin=dim(24, 0, 0, 0))

def hero_button(label, link, primary=True):
    s = {"text": label, "size": "sm",
         "link": {"url": link, "is_external": "", "nofollow": "", "custom_attributes": ""},
         "border_radius": rad(14),
         "text_padding": dim(22, 28, 22, 28) if primary else dim(22, 22, 22, 22),
         "align": "left", "align_mobile": "justify"}
    if primary:
        s.update(typo(size=15, weight=900, lh=1.1, ls=0.5, transform="uppercase"))
        s.update({"background_background": "gradient",
                  "background_color": "#6BD839", "background_color_stop": sl(0, "%"),
                  "background_color_b": "#55BA2D", "background_color_b_stop": sl(100, "%"),
                  "background_gradient_type": "linear",
                  "background_gradient_angle": sl(180, "deg"),
                  "button_text_color": "#10200B",
                  "button_background_hover_background": "classic",
                  "button_background_hover_color": "#55BA2D",
                  "hover_color": "#10200B"})
        s.update(shadow("button_box_shadow", 0, 16, 34, 0, "rgba(96,198,47,0.28)"))
    else:
        s.update(typo(size=15, weight=800, lh=1.1))
        s.update({"background_background": "classic",
                  "background_color": "rgba(255,255,255,0.09)",
                  "button_text_color": WHITE,
                  "border_border": "solid", "border_width": dim(1, 1, 1, 1),
                  "border_color": "rgba(255,255,255,0.18)",
                  "button_background_hover_background": "classic",
                  "button_background_hover_color": "rgba(255,255,255,0.18)",
                  "hover_color": WHITE,
                  "button_hover_border_color": "rgba(255,255,255,0.28)",
                  "custom_css": "selector .elementor-button{backdrop-filter:blur(8px);}"})
    return widget("button", **s)

hero_actions = con([
    hero_button("Get My Custom Kit Price →", "#quote", primary=True),
    hero_button("See What’s Included", "#compare", primary=False),
], content_width="full", width=sl(100, "%"), flex_direction="row",
   flex_wrap="wrap", flex_align_items="center", flex_gap=gap(15),
   flex_direction_mobile="column", margin=dim(32, 0, 0, 0))

hero_proof = widget("icon-list",
                    view="inline",
                    icon_list=[{"text": t,
                                "selected_icon": {"value": "fas fa-check",
                                                  "library": "fa-solid"},
                                "_id": eid()}
                               for t in ["Free quote", "No obligation",
                                         "Custom sizes", "Engineer-certified"]],
                    space_between=gapxy(20, 12),
                    icon_color="#60C62F",
                    icon_size=sl(13),
                    text_indent=sl(7),
                    text_color="#D4DDE2",
                    **typo(prefix="icon_typography", size=13, weight=700, lh=1.4))
hero_proof["settings"]["_margin"] = dim(18, 0, 0, 0)

hero_content = con([hero_eyebrow, hero_h1, hero_sub_wrap, hero_actions, hero_proof],
                   content_width="full", width=cu("min(760px, 100%)"),
                   width_tablet=sl(100, "%"), width_mobile=sl(100, "%"),
                   min_height=sl(650), min_height_tablet=sl(700),
                   flex_direction="column", flex_justify_content="center",
                   flex_align_items="flex-start", flex_gap=gap(0),
                   padding=dim(104, 58, 58, 58),
                   padding_tablet=dim(100, 28, 200, 28),
                   padding_mobile=dim(88, 20, 220, 20),
                   z_index=2)

hero_mark = con([
    widget("image",
           image={"url": f"{IMG_BASE}/{HERO_LOGO}", "id": "", "alt": "Aussie Carport Kits",
                  "source": "library"},
           image_size="full",
           width=sl(138), width_mobile=sl(118)),
], content_width="full", width=cu("fit-content"), flex_gap=gap(0), z_index=3,
   position="absolute", _offset_orientation_h="start",
   _offset_x=sl(34), _offset_x_tablet=sl(28), _offset_x_mobile=sl(20),
   _offset_orientation_v="start",
   _offset_y=sl(28), _offset_y_mobile=sl(22))

hero_value_card = con([
    heading("Built around your property", tag="div", color="#CCEFC0",
            size=11, weight=800, transform="uppercase", ls=1.3, lh=1.3),
    heading("No generic one-size-fits-all package.", tag="div", color=WHITE,
            size=19, weight=700, lh=1.3),
    text("<p>We help match the structure, sizing and components to your actual space, "
         "so you know what you&rsquo;re ordering before it arrives.</p>",
         color="#D7DFE4", size=13, lh=1.5),
], content_width="full", z_index=3,
   width=cu("min(370px, calc(100% - 68px))"),
   width_tablet=cu("calc(100% - 56px)"), width_mobile=cu("calc(100% - 40px)"),
   position="absolute",
   _offset_orientation_h="end",
   _offset_x_end=sl(34), _offset_x_end_tablet=sl(28), _offset_x_end_mobile=sl(20),
   _offset_orientation_v="end",
   _offset_y_end=sl(34), _offset_y_end_tablet=sl(28), _offset_y_end_mobile=sl(20),
   flex_gap=gap(7), padding=dim(22, 22, 22, 22),
   background_background="classic", background_color="rgba(9,15,19,0.64)",
   border_border="solid", border_width=dim(1, 1, 1, 1),
   border_color="rgba(255,255,255,0.12)", border_radius=rad(18),
   custom_css="selector{backdrop-filter:blur(10px);}",
   **shadow("box_shadow", 0, 18, 46, 0, "rgba(0,0,0,0.24)"))

# second darkening pass (the vertical gradient in the reference), kept below the copy
hero_veil = con([], content_width="full", z_index=1,
                position="absolute", _offset_orientation_h="start", _offset_x=sl(0),
                _offset_orientation_v="start", _offset_y=sl(0),
                width=sl(100, "%"), min_height=sl(100, "%"), flex_gap=gap(0),
                background_background="gradient",
                background_color="rgba(0,0,0,0.1)", background_color_stop=sl(0, "%"),
                background_color_b="rgba(0,0,0,0.28)", background_color_b_stop=sl(100, "%"),
                background_gradient_type="linear",
                background_gradient_angle=sl(180, "deg"))

hero_card = con([hero_veil, hero_mark, hero_content, hero_value_card],
                content_width="full",
                width=cu("min(1220px, 100%)"),
                min_height=sl(650), min_height_tablet=sl(700),
                flex_direction="column", flex_gap=gap(0),
                overflow="hidden",
                border_radius=rad(28), border_radius_mobile=rad(20),
                background_background="classic",
                background_image={"url": f"{IMG_BASE}/{HERO_BG}", "id": "",
                                  "source": "library"},
                background_size="cover",
                background_repeat="no-repeat",
                background_position="initial",
                background_xpos=sl(50, "%"), background_ypos=sl(48, "%"),
                background_xpos_mobile=sl(62, "%"), background_ypos_mobile=sl(50, "%"),
                background_overlay_background="gradient",
                background_overlay_color="rgba(7,13,17,0.82)",
                background_overlay_color_stop=sl(38, "%"),
                background_overlay_color_b="rgba(7,13,17,0.22)",
                background_overlay_color_b_stop=sl(100, "%"),
                background_overlay_gradient_type="linear",
                background_overlay_gradient_angle=sl(90, "deg"),
                background_overlay_opacity=sl(1),
                **shadow("box_shadow", 0, 28, 80, 0, "rgba(17,28,34,0.20)"))

hero_notes = con([
    heading("Why this replaces the promotion section better", tag="h2",
            color="#243038", size=26, weight=800, lh=1.25, ls=-0.78),
    con([text("<p>The old block had only one reason to act: a temporary discount. This "
              "version gives the section a permanent conversion job &mdash; reduce "
              "uncertainty, explain the custom-fit offer, and move serious buyers into a "
              "quote without relying on an expiry date.</p>",
              color="#5D6870", size=16, lh=1.6)],
        content_width="full", width=cu("min(980px, 100%)"), flex_gap=gap(0)),
], content_width="full", width=cu("min(1220px, 100%)"), flex_gap=gap(10),
   margin=dim(22, 0, 0, 0), padding=dim(22, 4, 0, 4))

hero = con([hero_card, hero_notes],
           content_width="full", width=sl(100, "%"),
           flex_direction="column", flex_align_items="center", flex_gap=gap(0),
           padding=dim(48, 18, 48, 18),
           padding_mobile=dim(18, 10, 18, 10),
           background_background="classic", background_color="#EEF2EF")


# ---------------------------------------------------------------- 4. trust strip
def trust_item(glyph, label):
    return col([
        con([
            con([heading(glyph, tag="div", color="#2D8F1F", size=17, lh=1)],
                content_width="full", width=sl(34), min_height=sl(34),
                flex_justify_content="center", flex_align_items="center",
                flex_gap=gap(0), _flex_size="none",
                background_background="classic", background_color="#E9F7E6",
                border_radius=rad(10), padding=dim(0, 0, 0, 0)),
            heading(label, tag="div", color=INK, size=13, weight=700, lh=1.3),
        ], content_width="full", flex_direction="row", flex_align_items="center",
           flex_gap=gap(10), width=sl(100, "%")),
    ], width=cu("calc(25% - 13.5px)"), width_t=cu("calc(50% - 9px)"),
       width_m=100, gap_v=0)

trust = section([
    row([trust_item("✓", "30+ years industry experience"),
         trust_item("◈", "Premium engineered aluminium"),
         trust_item("▰", "Genuine Colorbond roofing"),
         trust_item("⌂", "Licensed installers available")],
        gap_v=18, stack_on=None, wrap="wrap"),
], pad_top=22, pad_bottom=22, gap_v=0,
   border_border="solid", border_width=dim(1, 0, 1, 0), border_color="#EEF2EF")

# ---------------------------------------------------------------- 5. two paths
def choice_card(option, title, body, items, btn_label, btn_variant, featured=False):
    kids = []
    if featured:
        kids.append(con([heading("MOST ONLINE BUYERS", tag="div", color="#28771A",
                                 size=11, weight=800, lh=1.2)],
                        content_width="full", position="absolute",
                        _offset_orientation_h="end", _offset_x_end=sl(18),
                        _offset_y=sl(18), width=cu("fit-content"),
                        background_background="classic", background_color="#E8F8E5",
                        border_radius=rad(999), padding=dim(6, 9, 6, 9),
                        flex_gap=gap(0), flex_align_items="center"))
    kids += [
        kicker(option),
        heading(title, tag="h3", color=INK, size=27, size_m=23, weight=800, lh=1.15, ls=-0.8),
        text(f"<p>{body}</p>", color="#667683", size=16, lh=1.55),
        checklist(items),
        con([button(btn_label, "#quote", variant=btn_variant)],
            content_width="full", width=sl(100, "%"),
            _flex_align_self="flex-start", flex_gap=gap(0),
            margin=dim(6, 0, 0, 0)),
    ]
    s = {"background_background": "classic", "background_color": WHITE,
         "border_radius": rad(18), "padding": dim(28, 28, 28, 28),
         "flex_gap": gap(10), "overflow": "hidden",
         "border_border": "solid",
         "border_width": dim(2, 2, 2, 2) if featured else dim(1, 1, 1, 1),
         "border_color": GREEN2 if featured else LINE}
    if featured:
        s.update(shadow("box_shadow", 0, 15, 40, 0, "rgba(47,145,32,0.12)"))
    return col(kids, width=50, width_t=100, **s)

choices = section([
    col([kicker("One page. Two clear paths."),
         h2("Do it yourself &mdash; or have us organise the installation."),
         sub("The current page mixes DIY kits and installation together. This redesign "
             "makes the visitor choose the path that matches their intent instead of "
             "making them decode the offer.")],
        width=100, gap_v=10),
    row([
        choice_card("Option 1", "Supply me the kit",
                    "For homeowners or trades who want a premium carport kit delivered "
                    "and ready to assemble.",
                    ["Engineered aluminium beams and posts",
                     "Genuine Colorbond roofing",
                     "Fast Sydney delivery",
                     "Help choosing the correct kit"],
                    "Price My DIY Kit", "primary", featured=True),
        choice_card("Option 2", "Supply + install it for me",
                    "Skip the DIY work and let licensed, insured professionals take care "
                    "of the installation.",
                    ["Kit supplied to suit your project",
                     "Licensed professional installation",
                     "One clear point of contact",
                     "Installation pricing from $140/m²"],
                    "Get An Installed Price", "dark"),
    ], gap_v=22, align="stretch"),
], bg=SOFT)

# ---------------------------------------------------------------- 6. steps
def step_card(n, title, body):
    return col([
        con([heading(n, tag="div", color=WHITE, size=16, weight=800, lh=1)],
            content_width="full", width=sl(38), min_height=sl(38),
            flex_justify_content="center", flex_align_items="center",
            flex_gap=gap(0), _flex_size="none",
            background_background="classic", background_color=INK,
            border_radius=rad(50), margin=dim(0, 0, 10, 0)),
        heading(title, tag="h3", color=INK, size=18, weight=800, lh=1.25),
        text(f"<p>{body}</p>", color="#6C7C87", size=14, lh=1.5),
    ], width=cu("calc(25% - 12px)"), width_t=cu("calc(50% - 8px)"),
       width_m=100, gap_v=8,
       background_background="classic", background_color=WHITE,
       border_border="solid", border_width=dim(1, 1, 1, 1), border_color=LINE,
       border_radius=rad(14), padding=dim(24, 24, 24, 24))

steps = section([
    col([kicker("Remove buying friction"),
         h2("Here&rsquo;s what happens after you enquire."),
         sub("Paid traffic converts better when the next step feels small, concrete and safe.")],
        width=100, gap_v=10),
    row([step_card("1", "Tell us the basics",
                   "Carport size, postcode and whether you want DIY or installation."),
         step_card("2", "We check the fit",
                   "We help confirm the appropriate kit and any key project details."),
         step_card("3", "You get a clear quote",
                   "Know what you&rsquo;re paying before you commit."),
         step_card("4", "Delivery or install",
                   "Your kit is organised for delivery, with installation coordinated "
                   "if selected.")],
        gap_v=16, stack_on=None, wrap="wrap", align="stretch"),
])

# ---------------------------------------------------------------- 7. product proof
def metric(title, body):
    return col([
        heading(title, tag="div", color=INK, size=30, size_m=24, weight=800, lh=1.15, ls=-1),
        text(f"<p>{body}</p>", color="#667683", size=13, lh=1.45),
    ], width=50, width_t=50, width_m=50, gap_v=4, _flex_size="custom", _flex_shrink=1,
       background_background="classic", background_color=WHITE,
       border_border="solid", border_width=dim(1, 1, 1, 1), border_color=LINE,
       border_radius=rad(14), padding=dim(20, 20, 20, 20))

proof = section([
    col([kicker("Product confidence"),
         h2("Built to look premium &mdash; not like a cheap bolt-together afterthought.")],
        width=100, gap_v=10),
    row([
        col([image("product-detail-1160x1080.jpg", radius=18)], width=52, gap_v=0),
        col([
            sub("Your original page has strong product ingredients, but they are spread "
                "across too many isolated blocks. This section consolidates the physical "
                "reasons to believe into one high-impact product story."),
            row([metric("Aluminium", "Lightweight, durable and rust resistant"),
                 metric("Colorbond", "Recognisable premium Australian roofing brand")],
                gap_v=14, stack_on=None, align="stretch"),
            row([metric("Engineered",
                        "Structural system positioned above generic roll-formed alternatives"),
                 metric("Support", "Real help before you place the order")],
                gap_v=14, stack_on=None, align="stretch"),
        ], width=46, gap_v=14),
    ], gap_v=28, align="center"),
], bg=SOFT)

# ---------------------------------------------------------------- 8. comparison
C_BORDER = "#334653"
def cmp_row(a, b, c, head=False):
    def cell(txt, width, color, weight, bg=None, align_left=True):
        s = {"content_width": "full", "width": sl(width, "%"),
             "width_tablet": sl(width, "%"), "width_mobile": sl(width, "%"),
             "padding": dim(16, 18, 16, 18), "padding_mobile": dim(12, 8, 12, 8),
             "flex_gap": gap(0), "flex_justify_content": "center"}
        if not head:
            s.update({"border_border": "solid", "border_width": dim(1, 0, 0, 0),
                      "border_color": C_BORDER})
        if bg:
            s.update({"background_background": "classic", "background_color": bg})
        return con([heading(txt, tag="div", color=color, size=15, size_m=12,
                            weight=weight, lh=1.35)], **s)
    cells = [
        cell(a, 41.2, WHITE if head else WHITE, 800 if head else 600,
             "#1C2B37" if head else None),
        cell(b, 29.4, WHITE if head else "#C9D2D9", 800 if head else 500,
             "#1C2B37" if head else None),
        cell(c, 29.4, WHITE if head else "#6FE84D", 800 if head else 700,
             "#1C2B37" if head else "rgba(82,213,45,0.06)"),
    ]
    return con(cells, content_width="full", width=sl(100, "%"),
               flex_direction="row", flex_gap=gap(0), flex_align_items="stretch",
               flex_wrap="nowrap")

compare = section([
    col([kicker("Why the system matters", color="#6FE84D"),
         h2("Premium engineered aluminium vs common roll-formed steel.", color=WHITE),
         sub("Keep the comparison factual and specific. Avoid vague claims like "
             "&ldquo;beyond measurable&rdquo; &mdash; they sound promotional without "
             "proving anything.", color="#B9C5CF")],
        width=100, gap_v=10),
    con([
        cmp_row("Feature", "Typical roll-formed steel",
                "Aussie Carport Kits aluminium", head=True),
        cmp_row("Rust resistance", "Coating dependent", "Aluminium advantage"),
        cmp_row("Weight", "Heavier sections", "Lightweight material"),
        cmp_row("Finish / presentation", "Industrial profile common",
                "Clean RHS-style appearance"),
        cmp_row("System positioning", "Commodity-style option",
                "Premium engineered system"),
    ], content_width="full", width=sl(100, "%"), flex_direction="column",
       flex_gap=gap(0), overflow="hidden",
       border_border="solid", border_width=dim(1, 1, 1, 1), border_color=C_BORDER,
       border_radius=rad(16)),
], bg=INK, element_id="compare", gap_v=30)

# ---------------------------------------------------------------- 9. outcome
outcome = section([
    row([
        col([kicker("Real-world outcome"),
             h2("Make the finished carport the hero."),
             sub("Your current page uses good project imagery, but the call-to-action "
                 "buttons are placed directly over photos and compete with the product. "
                 "In this version the imagery sells the result, while the CTA sits in "
                 "clean surrounding space."),
             con([button("Get My Carport Price", "#quote", variant="primary")],
                 content_width="full", width=sl(100, "%"),
                 _flex_align_self="flex-start", flex_gap=gap(0),
                 margin=dim(10, 0, 0, 0)),
             ], width=52, gap_v=12),
        col([image("project-outcome-1160x1080.jpg", radius=18)], width=46, gap_v=0),
    ], gap_v=28, align="center"),
], gap_v=0)

# ---------------------------------------------------------------- 10. quote form
def offer_item(title, body):
    return con([
        con([heading("✓", tag="div", color="#2D8F1F", size=17, lh=1)],
            content_width="full", width=sl(34), min_height=sl(34), _flex_size="none",
            flex_justify_content="center", flex_align_items="center", flex_gap=gap(0),
            background_background="classic", background_color="#E9F7E6",
            border_radius=rad(10)),
        col([heading(title, tag="div", color=INK, size=16, weight=800, lh=1.3),
             text(f"<p>{body}</p>", color="#687884", size=14, lh=1.45)],
            width=None, width_t=None, width_m=None, gap_v=2, _flex_size="grow"),
    ], content_width="full", width=sl(100, "%"), flex_direction="row",
       flex_align_items="flex-start", flex_gap=gap(12))

form_widget = widget(
    "form",
    form_name="Carport Quote",
    form_fields=[
        {"custom_id": "name", "field_type": "text", "field_label": "NAME",
         "placeholder": "Your name", "required": "true", "width": "50", "_id": eid()},
        {"custom_id": "phone", "field_type": "tel", "field_label": "PHONE",
         "placeholder": "04xx xxx xxx", "required": "true", "width": "50", "_id": eid()},
        {"custom_id": "postcode", "field_type": "text", "field_label": "POSTCODE",
         "placeholder": "e.g. 2148", "required": "true", "width": "50", "_id": eid()},
        {"custom_id": "i_want", "field_type": "select", "field_label": "I WANT",
         "field_options": "DIY kit only\nSupply + installation\nNot sure yet",
         "required": "", "width": "50", "_id": eid()},
        {"custom_id": "width", "field_type": "text", "field_label": "APPROX. WIDTH",
         "placeholder": "e.g. 3.5m", "required": "", "width": "50", "_id": eid()},
        {"custom_id": "length", "field_type": "text", "field_label": "APPROX. LENGTH",
         "placeholder": "e.g. 6m", "required": "", "width": "50", "_id": eid()},
        {"custom_id": "message", "field_type": "textarea", "field_label": "ANYTHING ELSE?",
         "placeholder": "Tell us about your site, preferred colour or attach details later.",
         "rows": "4", "required": "", "width": "100", "_id": eid()},
    ],
    input_size="sm",
    show_labels="yes",
    mark_required="",
    label_position="above",
    button_text="Get My Exact Carport Price →",
    button_size="sm",
    button_align="stretch",
    button_width="100",
    submit_actions=["email"],
    email_to="info@aussiecarportkits.com.au",
    email_subject="New carport quote request from your website",
    email_content="[all-fields]",
    email_from_name="Aussie Carport Kits Website",
    email_reply_to="",
    email_content_type="html",
    success_message="Thanks — we’ve got your details and will be in touch shortly.",
    error_message="Something went wrong. Please call us instead.",
    required_field_message="This field is required.",
    invalid_message="There’s a problem with one of the fields.",
    column_gap=gap(12),
    row_gap=gap(12),
    label_spacing=sl(6),
    field_border_radius=rad(9),
    field_border_border="solid",
    field_border_width=dim(1, 1, 1, 1),
    field_border_color="#CFD9D2",
    field_background_color=WHITE,
    field_text_color=INK,
    button_background_color=GREEN,
    button_text_color=GREEN_TX,
    button_border_radius=rad(10),
    button_text_padding=dim(14, 20, 14, 20),
    **typo(prefix="label_typography", size=12, weight=800, transform="uppercase"),
    **typo(prefix="field_typography", size=15, weight=400),
    **typo(prefix="button_typography", size=15, weight=700),
)

quote = section([
    row([
        col([kicker("Get a fast price"),
             h2("Tell us what you need. We&rsquo;ll help you price the right setup."),
             sub("This is the core conversion event. Keep the form short enough to "
                 "finish, but collect the three details that materially affect the quote."),
             con([offer_item("No-obligation quote",
                             "No checkout pressure before you know the correct setup."),
                  offer_item("DIY or installed",
                             "One enquiry path, then route the lead correctly."),
                  offer_item("Human project support",
                             "Use your experience as the conversion advantage over "
                             "faceless kit sellers.")],
                 content_width="full", width=sl(100, "%"), flex_direction="column",
                 flex_gap=gap(13), margin=dim(10, 0, 0, 0)),
             ], width=45, gap_v=12),
        col([
            col([form_widget,
                 text("<p>By submitting, you&rsquo;re asking Aussie Carport Kits to contact "
                      "you about your quote. Replace this prototype text with your actual "
                      "privacy wording.</p>", color="#7A878F", size=11, lh=1.45)],
                width=100, gap_v=10,
                background_background="classic", background_color=WHITE,
                border_border="solid", border_width=dim(1, 1, 1, 1), border_color=LINE,
                border_radius=rad(18), padding=dim(26, 26, 26, 26),
                **shadow("box_shadow", 0, 14, 45, 0, "rgba(20,32,44,0.09)")),
        ], width=53, gap_v=0),
    ], gap_v=44, align="flex-start"),
], bg=SOFT, element_id="quote", gap_v=0)

# ---------------------------------------------------------------- 11. FAQ
faq_items = [
    ("Can I buy the kit without installation?",
     "Yes. The DIY kit remains the core offer, with professional installation presented "
     "as an optional service rather than mixed into every message."),
    ("How quickly can you deliver?",
     "Your page currently promotes 7-day Sydney delivery. Keep this highly visible only "
     "where that timeframe can be reliably met and define when the timeframe starts."),
    ("What information do you need to quote?",
     "At minimum: approximate width and length, postcode, and whether you want DIY supply "
     "only or professional installation."),
    ("Why aluminium?",
     "Explain tangible material benefits such as lower weight and corrosion resistance, "
     "then support broader structural claims with your engineering documentation."),
]

faq_widget = widget(
    "accordion",
    tabs=[{"tab_title": t, "tab_content": f"<p>{c}</p>", "_id": eid()}
          for t, c in faq_items],
    selected_icon={"value": "fas fa-plus", "library": "fa-solid"},
    selected_active_icon={"value": "fas fa-minus", "library": "fa-solid"},
    title_html_tag="div",
    faq_schema="yes",
    border_width=sl(1),
    border_color=LINE,
    title_background="#FFFFFF00",
    title_color=INK,
    tab_active_color=INK,
    icon_color="#2D9E1F",
    icon_active_color="#2D9E1F",
    content_background_color="#FFFFFF00",
    content_color="#687884",
    title_padding=dim(18, 0, 18, 0),
    content_padding=dim(0, 0, 18, 0),
    **typo(prefix="title_typography", size=17, weight=800, lh=1.4),
    **typo(prefix="content_typography", size=15, weight=400, lh=1.6),
)

faq = section([
    col([kicker("Questions buyers ask before converting"),
         h2("Answer objections before they become reasons to leave.")],
        width=100, gap_v=10),
    con([faq_widget], content_width="full", width=sl(880, "px"),
        width_tablet=sl(100, "%"), flex_gap=gap(0), _flex_align_self="center"),
])

# ---------------------------------------------------------------- 12. footer
footer = con([
    row([
        col([text('<p><b style="color:#ffffff">AUSSIE CARPORT KITS</b><br>'
                  'Premium DIY carport kits + optional professional installation.</p>',
                  color="#BCC8D0", size=13, lh=1.6)], width=55, gap_v=0),
        col([text("<p>Prototype landing-page redesign &middot; Replace placeholder "
                  "phone/privacy details before publishing.</p>",
                  color="#BCC8D0", size=13, lh=1.6)], width=40, gap_v=0)],
        gap_v=24, justify="space-between", wrap="wrap", stack_on=None),
], content_width="boxed", boxed_width=sl(MAXW), html_tag="footer",
   flex_direction="column", flex_gap=gap(0),
   padding=dim(30, PAD_X, 95, PAD_X),
   background_background="classic", background_color="#0E1821")

# ---------------------------------------------------------------- 13. mobile CTA
sticky_cta = con([
    con([button("Call Us", "tel:+61000000000", variant="outline", full=True)],
        content_width="full", width=cu("calc(45% - 4px)"), flex_gap=gap(0)),
    con([button("Get My Price", "#quote", variant="primary", full=True)],
        content_width="full", width=cu("calc(55% - 4px)"), flex_gap=gap(0)),
], content_width="full", width=sl(100, "%"),
   position="fixed", _offset_orientation_h="start", _offset_x=sl(0),
   _offset_orientation_v="end", _offset_y_end=sl(0),
   z_index=50,
   flex_direction="row", flex_gap=gap(8), flex_align_items="center",
   flex_wrap="nowrap",
   padding=dim(9, 9, 9, 9),
   background_background="classic", background_color=WHITE,
   border_border="solid", border_width=dim(1, 0, 0, 0), border_color="#DCE5DF",
   hide_desktop="hidden-desktop", hide_tablet="hidden-tablet")

# ---------------------------------------------------------------- assemble
content = [topbar, header, hero, trust, choices, steps, proof,
           compare, outcome, quote, faq, footer, sticky_cta]

template = {
    "version": "0.4",
    "title": "Aussie Carport Kits — Conversion Landing Page",
    "type": "page",
    "content": content,
    "page_settings": {
        "template": "elementor_canvas",
        "hide_title": "yes",
    },
}

out = sys.argv[1] if len(sys.argv) > 1 else "aussie-carport-kits-landing-template.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(template, f, ensure_ascii=False, separators=(",", ":"))

def count(els):
    n = 0
    for e in els:
        n += 1 + count(e.get("elements", []))
    return n
print(f"wrote {out}: {count(content)} elements, {len(json.dumps(template))} bytes")
