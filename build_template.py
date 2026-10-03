#!/usr/bin/env python3
"""
Elementor page-template JSON for
aussie_carport_kits_paid_traffic_copy_revision.html
(Poppins/Sora copy revision — full-bleed hero, 1120px wrap).
"""
import json, itertools, sys

IMG_BASE = "https://raw.githubusercontent.com/anirudhatalmale6-alt/aussie-carport-kits-elementor/main/images"

HERO_BG   = "hero-background-carport.jpg"
IMG_STORY = "product-story-carport.jpg"
IMG_RESULT = "result-carport.jpg"

# ---------------------------------------------------------------- tokens
INK      = "#111B27"
TEXT     = "#5F6670"
GREEN    = "#36D11C"
GREEN_D  = "#2AA414"
PALE     = "#F5F7F4"
LINE     = "#D9DDD8"
DARKBG   = "#101B26"
WHITE    = "#FFFFFF"
EYEBROW  = "#329B2A"
BODY_F   = "Poppins"
HEAD_F   = "Sora"
WRAP     = "min(1120px, calc(100% - 40px))"
SHADOW   = (0, 14, 35, 0, "rgba(18,31,22,0.10)")

_ids = itertools.count(0x200000)
def eid():
    return format(next(_ids), '07x')

# ---------------------------------------------------------------- helpers
def dim(top, right, bottom, left, unit="px"):
    return {"unit": unit, "top": str(top), "right": str(right), "bottom": str(bottom),
            "left": str(left), "isLinked": top == right == bottom == left}

def rad(v):
    return dim(v, v, v, v)

def sl(size, unit="px"):
    return {"unit": unit, "size": size, "sizes": []}

def cu(expr):
    """Elementor's 'custom' slider unit — emits the raw CSS value."""
    return {"unit": "custom", "size": expr, "sizes": []}

def gap(v, unit="px"):
    return {"unit": unit, "size": v, "column": str(v), "row": str(v), "isLinked": True}

def gapxy(col, row, unit="px"):
    return {"unit": unit, "size": col, "column": str(col), "row": str(row), "isLinked": False}

def typo(prefix="typography", size=None, weight=None, lh=None, ls=None, transform=None,
         size_t=None, size_m=None, lh_unit="em", family=BODY_F, ls_unit="px"):
    s = {f"{prefix}_typography": "custom"}
    if family:    s[f"{prefix}_font_family"] = family
    if size:      s[f"{prefix}_font_size"] = cu(size) if isinstance(size, str) else sl(size)
    if size_t:    s[f"{prefix}_font_size_tablet"] = sl(size_t)
    if size_m:    s[f"{prefix}_font_size_mobile"] = sl(size_m)
    if weight:    s[f"{prefix}_font_weight"] = str(weight)
    if lh:        s[f"{prefix}_line_height"] = sl(lh, lh_unit)
    if ls is not None:
        s[f"{prefix}_letter_spacing"] = cu(ls) if isinstance(ls, str) else sl(ls, ls_unit)
    if transform: s[f"{prefix}_text_transform"] = transform
    return s

def shadow(group, h, v, blur, spread, color):
    return {f"{group}_box_shadow_type": "yes",
            f"{group}_box_shadow": {"horizontal": h, "vertical": v, "blur": blur,
                                    "spread": spread, "color": color}}

def con(children=None, **settings):
    settings.setdefault("content_width", "full")
    settings.setdefault("padding", dim(0, 0, 0, 0))   # kill Elementor's default 10px
    if "width" in settings:
        settings.setdefault("width_tablet", settings["width"])
        settings.setdefault("width_mobile", settings["width"])
    return {"id": eid(), "elType": "container", "settings": settings,
            "elements": children or [], "isInner": False}

def widget(wtype, **settings):
    return {"id": eid(), "elType": "widget", "settings": settings,
            "elements": [], "widgetType": wtype}

def section(children, bg=None, element_id=None, gap_v=0, **extra):
    # boxed_width is responsive and Elementor does NOT inherit the desktop value down
    # to mobile, so the wrap has to be declared at every breakpoint.
    s = {"content_width": "boxed", "boxed_width": cu(WRAP),
         "boxed_width_tablet": cu(WRAP), "boxed_width_mobile": cu(WRAP),
         "flex_direction": "column", "flex_gap": gap(gap_v),
         "padding": dim(92, 0, 92, 0), "padding_mobile": dim(66, 0, 66, 0),
         "overflow": "hidden"}
    if bg:
        s["background_background"] = "classic"
        s["background_color"] = bg
    if element_id:
        s["_element_id"] = element_id
    s.update(extra)
    return con(children, **s)

def rowc(children, gap_v=24, align=None, justify=None, stack="tablet", **extra):
    s = {"width": sl(100, "%"), "flex_direction": "row", "flex_gap": gap(gap_v),
         "flex_wrap": extra.pop("flex_wrap", "nowrap")}
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
    for key, val in (("width", width), ("width_tablet", width_t), ("width_mobile", width_m)):
        if val is not None:
            s[key] = val if isinstance(val, dict) else sl(val, "%")
    s.update(extra)
    return con(children, **s)

def heading(title, tag="h2", color=INK, link=None, **ty):
    s = {"title": title, "header_size": tag}
    if color: s["title_color"] = color
    if link:  s["link"] = {"url": link, "is_external": "", "nofollow": "",
                           "custom_attributes": ""}
    s.update(typo(**ty))
    return widget("heading", **s)

def text(html, color=TEXT, **ty):
    s = {"editor": html.replace("<p>", '<p style="margin:0">')}
    if color: s["text_color"] = color
    ty.setdefault("lh", 1.55)
    s.update(typo(**ty))
    return widget("text-editor", **s)

def image(fname, radius=22, with_shadow=True, max_h=None):
    s = {"image": {"url": f"{IMG_BASE}/{fname}", "id": "", "source": "library"},
         "image_size": "full", "width": sl(100, "%"),
         "image_border_radius": rad(radius)}
    if with_shadow:
        s.update(shadow("image_box_shadow", *SHADOW))
    if max_h:
        s["height"] = sl(max_h)
        s["object-fit"] = "cover"
    return widget("image", **s)

# --- shared pieces -------------------------------------------------------
def eyebrow(txt, color=EYEBROW, size=12.5):
    return heading(txt, tag="div", color=color, size=size, weight=800, lh=1.2,
                   ls="0.11em", transform="uppercase")

def h2(txt, color=INK, size="clamp(2.4rem, 5.5vw, 4.6rem)"):
    return heading(txt, tag="h2", color=color, size=size, weight=700, lh=0.98,
                   ls="-0.045em", family=HEAD_F)

def section_head(kick, title, body=None, dark=False, title_size=None):
    kids = [eyebrow(kick, color="#70E15E" if dark else EYEBROW),
            h2(title, color=WHITE if dark else INK,
               **({"size": title_size} if title_size else {}))]
    kids[0]["settings"]["_margin"] = dim(0, 0, 12, 0)
    kids[1]["settings"]["_margin"] = dim(0, 0, 18 if body else 0, 0)
    if body:
        kids.append(text(f"<p>{body}</p>", color="#B9C0C8" if dark else TEXT, size=17.3))
    return colc(kids, width=cu("min(760px, 100%)"), width_t=100, width_m=100,
                gap_v=0, _flex_align_self="flex-start", margin=dim(0, 0, 34, 0))

def btn(label, link, kind="primary", full_mobile=True):
    s = {"text": label, "size": "sm",
         "link": {"url": link, "is_external": "", "nofollow": "", "custom_attributes": ""},
         "border_radius": rad(10),
         "text_padding": dim(18, 24, 18, 24),
         "align": "left"}
    if full_mobile:
        s["align_mobile"] = "justify"
    s.update(typo(size=16, weight=800, lh=1.25))
    if kind == "primary":
        s.update({"background_background": "classic", "background_color": GREEN,
                  "button_text_color": "#07120B",
                  "button_background_hover_background": "classic",
                  "button_background_hover_color": GREEN_D,
                  "hover_color": "#07120B"})
        s.update(shadow("button_box_shadow", 0, 12, 30, 0, "rgba(54,209,28,0.23)"))
    elif kind == "dark":
        s.update({"background_background": "classic", "background_color": INK,
                  "button_text_color": WHITE,
                  "button_background_hover_background": "classic",
                  "button_background_hover_color": "#1A2431",
                  "hover_color": WHITE})
    else:  # ghost (on the hero photo)
        s.update({"background_background": "classic",
                  "background_color": "rgba(255,255,255,0.08)",
                  "button_text_color": WHITE,
                  "border_border": "solid", "border_width": dim(1, 1, 1, 1),
                  "border_color": "rgba(255,255,255,0.38)",
                  "button_background_hover_background": "classic",
                  "button_background_hover_color": "rgba(255,255,255,0.18)",
                  "hover_color": WHITE,
                  "button_hover_border_color": "rgba(255,255,255,0.5)",
                  "custom_css": "selector .elementor-button{backdrop-filter:blur(8px);}"})
    return widget("button", **s)

def chip(glyph, size=28, radius=8, bg="#EBF9E7", fg="#2B9C22", fs=14):
    return con([heading(glyph, tag="div", color=fg, size=fs, weight=800, lh=1)],
               width=sl(size), min_height=sl(size), _flex_size="none",
               flex_justify_content="center", flex_align_items="center",
               flex_gap=gap(0), background_background="classic",
               background_color=bg, border_radius=rad(radius))

# ---------------------------------------------------------------- 1. hero
hero_logo = heading('<b style="display:block;color:#42D928">AUSSIE</b>CARPORT KITS',
                    tag="div", color=WHITE, size=18.9, weight=800, lh=0.92, ls="-0.03em")
hero_logo["settings"]["_margin"] = dim(0, 0, 26, 0)

hero_eyebrow = heading("● &nbsp; Custom DIY Carport Kits", tag="div", color="#D9FFD4",
                       size=12.5, weight=800, lh=1.2, ls="0.11em", transform="uppercase")
hero_eyebrow["settings"]["_margin"] = dim(0, 0, 12, 0)

hero_h1 = heading('DIY Carport Kits <span style="color:#36D11C">Built For Your Space.</span>',
                  tag="h1", color=WHITE, size="clamp(3.2rem, 8vw, 6.3rem)",
                  size_m=49.6, weight=700, lh=0.92, ls="-0.045em", family=HEAD_F)
hero_h1["settings"]["_margin"] = dim(0, 0, 24, 0)

hero_p = text("<p>Send your measurements or plans. We&rsquo;ll configure a complete "
              "engineered aluminium carport kit to suit your home, ready for fast "
              "Sydney delivery.</p>",
              color="rgba(255,255,255,0.9)", size=17.6, size_m=16, lh=1.55)

hero_actions = con([btn("GET MY KIT PRICE →", "#quote", "primary"),
                    btn("See What’s Included", "#included", "ghost")],
                   width=sl(100, "%"), flex_direction="row", flex_wrap="wrap",
                   flex_gap=gap(12), flex_align_items="center",
                   flex_direction_mobile="column", flex_align_items_mobile="stretch",
                   margin=dim(28, 0, 0, 0))

hero_proof = widget("icon-list", view="inline",
                    icon_list=[{"text": t, "selected_icon": {"value": "fas fa-check",
                                                             "library": "fa-solid"},
                                "_id": eid()}
                               for t in ["Free quote", "No obligation",
                                         "Custom sizes", "Engineered system"]],
                    space_between=gapxy(20, 10), space_between_mobile=gapxy(18, 10),
                    icon_color=GREEN, icon_size=sl(13), text_indent=sl(7),
                    text_color=WHITE,
                    **typo(prefix="icon_typography", size=14.1, size_m=12.5,
                           weight=700, lh=1.4))
hero_proof["settings"]["_margin"] = dim(28, 0, 0, 0)

# Left-aligned inside the 1120 wrap. The reference centres this block, which pushes the
# copy under the floating card and collides the logo with the eyebrow — see README.
hero_inner = colc([hero_logo, hero_eyebrow, hero_h1,
                   colc([hero_p], width=cu("min(680px, 100%)"), width_t=100, width_m=100),
                   hero_actions, hero_proof],
                  width=cu("min(720px, 100%)"), width_t=100, width_m=100, gap_v=0,
                  _flex_align_self="flex-start",
                  padding=dim(52, 0, 64, 0),
                  padding_tablet=dim(150, 0, 230, 0),
                  padding_mobile=dim(130, 0, 255, 0))

hero_card = con([
    heading("Built Around Your Property", tag="div", color="#D9FFD4", size=10.9,
            weight=800, lh=1.2, ls="0.11em", transform="uppercase"),
    heading("Built around your space, not a box.", tag="h3", color=WHITE, size=24.8,
            weight=700, lh=1.05, ls="-0.045em", family=HEAD_F),
    text("<p>We match the size, structure and components to your project, so you know "
         "exactly what you&rsquo;re getting before it arrives.</p>",
         color="rgba(255,255,255,0.78)", size=14.7, lh=1.55),
], z_index=3, position="absolute",
   _offset_orientation_h="end", _offset_x_end=cu("4vw"),
   _offset_x_end_tablet=sl(20), _offset_x_end_mobile=sl(20),
   _offset_orientation_v="end", _offset_y_end=sl(54),
   _offset_y_end_tablet=sl(38), _offset_y_end_mobile=sl(50),
   width=cu("min(370px, 32vw)"), width_tablet=cu("calc(100% - 40px)"),
   width_mobile=cu("calc(100% - 40px)"),
   flex_gap=gapxy(0, 9), padding=dim(24, 24, 24, 24),
   background_background="classic", background_color="rgba(9,19,17,0.90)",
   border_border="solid", border_width=dim(1, 1, 1, 1),
   border_color="rgba(255,255,255,0.12)", border_radius=rad(18),
   custom_css="selector{backdrop-filter:blur(12px);}",
   **shadow("box_shadow", *SHADOW))

# the 180px darkening at the foot of the photo (.hero:after)
hero_fade = con([], z_index=1, position="absolute",
                _offset_orientation_h="start", _offset_x=sl(0),
                _offset_orientation_v="end", _offset_y_end=sl(0),
                width=sl(100, "%"), min_height=sl(180), flex_gap=gap(0),
                background_background="gradient",
                background_color="rgba(5,10,12,0)", background_color_stop=sl(0, "%"),
                background_color_b="rgba(5,10,12,0.65)", background_color_b_stop=sl(100, "%"),
                background_gradient_type="linear", background_gradient_angle=sl(180, "deg"))

hero_stage = con([hero_inner, hero_card], width=cu(WRAP),
                 flex_direction="column", flex_justify_content="flex-end",
                 flex_gap=gap(0), z_index=2, min_height=sl(760),
                 min_height_tablet=sl(880), min_height_mobile=sl(930))

hero = con([hero_fade, hero_stage],
           width=sl(100, "%"), min_height=sl(760),
           min_height_tablet=sl(880), min_height_mobile=sl(930),
           flex_direction="column", flex_justify_content="flex-end",
           flex_align_items="center", flex_gap=gap(0), overflow="hidden",
           background_background="classic",
           background_image={"url": f"{IMG_BASE}/{HERO_BG}", "id": "", "source": "library"},
           background_size="cover", background_repeat="no-repeat",
           background_position="center center",
           background_position_mobile="center top",
           background_overlay_background="gradient",
           background_overlay_color="rgba(7,18,17,0.90)",
           background_overlay_color_stop=sl(20, "%"),
           background_overlay_color_b="rgba(7,18,17,0.48)",
           background_overlay_color_b_stop=sl(100, "%"),
           background_overlay_gradient_type="linear",
           background_overlay_gradient_angle=sl(90, "deg"),
           background_overlay_opacity=sl(1))

# ---------------------------------------------------------------- 2. trust
def trust_pill(glyph, label):
    return colc([con([chip(glyph), heading(label, tag="div", color=INK, size=16,
                                           weight=700, lh=1.35)],
                     width=sl(100, "%"), flex_direction="row", flex_wrap="nowrap",
                     flex_align_items="center", flex_gap=gap(10))],
                width=cu("calc(25% - 9px)"), width_t=cu("calc(50% - 6px)"), width_m=100,
                background_background="classic", background_color=WHITE,
                border_border="solid", border_width=dim(1, 1, 1, 1), border_color=LINE,
                border_radius=rad(14), padding=dim(17, 18, 17, 18))

trust = section([
    rowc([trust_pill("✓", "30+ years industry experience"),
          trust_pill("◇", "Premium engineered aluminium"),
          trust_pill("▰", "Genuine Colorbond roofing"),
          trust_pill("⌂", "Licensed installers available")],
         gap_v=12, stack=None, flex_wrap="wrap", align="stretch",
         margin=dim(24, 0, 0, 0)),
], bg=PALE, element_id="included")

# ---------------------------------------------------------------- 3. two options
def option_card(opt, title, body, items, label, kind, featured=False, fine=None):
    kids = []
    if featured:
        tag = heading("MOST ONLINE BUYERS", tag="div", color="#2E8928", size=10.9,
                      weight=800, lh=1.2, ls=0.3)
        kids.append(con([tag], z_index=2, position="absolute",
                        _offset_orientation_h="end", _offset_x_end=sl(22),
                        _offset_y=sl(22), width=cu("fit-content"),
                        position_mobile="", background_background="classic",
                        background_color="#E8F6E4", border_radius=rad(999),
                        padding=dim(7, 11, 7, 11), flex_gap=gap(0)))
    eb = eyebrow(opt)
    eb["settings"]["_margin"] = dim(0, 0, 12, 0)
    hd = heading(title, tag="h3", color=INK, size=32, weight=700, lh=1,
                 ls="-0.045em", family=HEAD_F)
    hd["settings"]["_margin"] = dim(0, 0, 12, 0)
    body_w = text(f"<p>{body}</p>", size=16)
    body_w["settings"]["_margin"] = dim(0, 0, 16, 0)
    checks = widget("icon-list",
                    icon_list=[{"text": t, "selected_icon": {"value": "fas fa-check",
                                                             "library": "fa-solid"},
                                "_id": eid()} for t in items],
                    space_between=sl(12), icon_color="#2AA51E", icon_size=sl(14),
                    text_indent=sl(10), text_color=INK,
                    **typo(prefix="icon_typography", size=16, weight=400, lh=1.4))
    checks["settings"]["_margin"] = dim(0, 0, 22, 0)
    kids += [eb, hd, body_w, checks,
             con([btn(label, "#quote", kind)], width=sl(100, "%"),
                 _flex_align_self="flex-start", flex_gap=gap(0))]
    if fine:
        kids.append(text(f"<p>{fine}</p>", color="#7B8188", size=12.2, lh=1.5,
                         **{}))
        kids[-1]["settings"]["_margin"] = dim(8, 0, 0, 0)
    s = {"background_background": "classic", "background_color": WHITE,
         "border_radius": rad(20), "padding": dim(30, 30, 30, 30),
         "padding_mobile": dim(24, 24, 24, 24), "flex_gap": gap(0),
         "border_border": "solid",
         "border_width": dim(2, 2, 2, 2) if featured else dim(1, 1, 1, 1),
         "border_color": "#42B92F" if featured else LINE}
    if featured:
        s.update(shadow("box_shadow", 0, 16, 36, 0, "rgba(54,209,28,0.10)"))
    return colc(kids, width=cu("calc(50% - 11px)"), width_t=100, width_m=100, **s)

choices = section([
    section_head("One Project. Two Clear Options.",
                 "DIY the build &mdash; or have us organise installation.",
                 "Choose the option that suits you. We can supply the complete kit, or "
                 "arrange professional installation for you."),
    rowc([option_card("Option 1", "Supply me the kit",
                      "For homeowners or trades who want a premium carport kit delivered "
                      "and ready to assemble.",
                      ["Engineered aluminium beams and posts",
                       "Genuine Colorbond roofing",
                       "Fast Sydney delivery",
                       "Help choosing the right kit"],
                      "Price My DIY Kit", "primary", featured=True),
          option_card("Option 2", "Supply + install it for me",
                      "Prefer it done for you? We can also arrange professional "
                      "installation.",
                      ["Kit supplied to suit your project",
                       "Licensed professional installation",
                       "One clear point of contact",
                       "Installation pricing from $140/m²*"],
                      "Get An Installed Price", "dark",
                      fine="*Subject to site, size and project requirements.")],
         gap_v=22, align="stretch")])

# ---------------------------------------------------------------- 4. steps
def step_card(n, title, body):
    num = con([heading(n, tag="div", color=WHITE, size=17, weight=800, lh=1)],
              width=sl(44), min_height=sl(44), _flex_size="none",
              flex_justify_content="center", flex_align_items="center",
              flex_gap=gap(0), background_background="classic", background_color=INK,
              border_radius=rad(50), margin=dim(0, 0, 35, 0),
              margin_mobile=dim(0, 0, 26, 0))
    hd = heading(title, tag="h3", color=INK, size=20, weight=700, lh=1.25,
                 ls="-0.045em", family=HEAD_F)
    hd["settings"]["_margin"] = dim(0, 0, 8, 0)
    return colc([num, hd, text(f"<p>{body}</p>", size=15)],
                width=cu("calc(25% - 12px)"), width_t=cu("calc(50% - 8px)"), width_m=100,
                background_background="classic", background_color=WHITE,
                border_border="solid", border_width=dim(1, 1, 1, 1), border_color=LINE,
                border_radius=rad(18), padding=dim(25, 25, 25, 25))

steps = section([
    section_head("Simple From Enquiry To Delivery",
                 "From enquiry to a clear price &mdash; fast.",
                 "No checkout. No guesswork. We confirm the right setup before you commit."),
    rowc([step_card("1", "Tell us the basics",
                    "Send your size, postcode and whether you want DIY or installation."),
          step_card("2", "We check the fit",
                    "We review your details and flag anything we need to confirm."),
          step_card("3", "You get a clear quote",
                    "Know what&rsquo;s included and what you&rsquo;re paying before you commit."),
          step_card("4", "Delivery or install",
                    "We organise delivery &mdash; and installation if you choose it.")],
         gap_v=16, stack=None, flex_wrap="wrap", align="stretch")], bg=PALE)

# ---------------------------------------------------------------- 5. product story
def feature(title, body):
    hd = heading(title, tag="h3", color=INK, size=20, weight=700, lh=1.2,
                 ls="-0.045em", family=HEAD_F)
    hd["settings"]["_margin"] = dim(0, 0, 5, 0)
    return colc([hd, text(f"<p>{body}</p>", size=13.9)],
                width=cu("calc(50% - 7px)"), width_t=cu("calc(50% - 7px)"),
                width_m=cu("calc(50% - 7px)"),
                background_background="classic", background_color=WHITE,
                border_border="solid", border_width=dim(1, 1, 1, 1), border_color=LINE,
                border_radius=rad(16), padding=dim(20, 20, 20, 20))

story_eb = eyebrow("Product Confidence"); story_eb["settings"]["_margin"] = dim(0, 0, 12, 0)
story_h2 = h2("Built to look premium &mdash; not like a bolt-on afterthought.",
              size="clamp(2.5rem, 5vw, 4.5rem)")
story_h2["settings"]["_margin"] = dim(0, 0, 18, 0)

product_story = section([
    rowc([
        colc([story_eb, story_h2,
              text("<p>Premium aluminium, genuine Colorbond roofing and an engineered "
                   "system sized around your project.</p>", size=17.3),
              rowc([feature("Aluminium", "Lightweight, durable and corrosion resistant."),
                    feature("Colorbond", "Genuine premium steel roofing.")],
                   gap_v=14, stack=None, align="stretch", margin=dim(24, 0, 0, 0)),
              rowc([feature("Engineered", "Structural system sized to suit your project."),
                    feature("Support", "Real help before you place the order.")],
                   gap_v=14, stack=None, align="stretch", margin=dim(14, 0, 0, 0)),
              ], width=cu("calc(52.5% - 24px)")),
        colc([image(IMG_STORY)], width=cu("calc(47.5% - 24px)")),
    ], gap_v=48, align="center")])

# ---------------------------------------------------------------- 6. comparison
CB = "#344251"
def cmp_row(a, b, c, head=False):
    def cell(txt, width, color, weight, bg=None):
        s = {"width": sl(width, "%"), "width_tablet": sl(width, "%"),
             "width_mobile": sl(width, "%"),
             "padding": dim(17, 16, 17, 16), "padding_mobile": dim(12, 8, 12, 8),
             "flex_gap": gap(0), "flex_justify_content": "flex-start"}
        if not head:
            s.update({"border_border": "solid", "border_width": dim(0, 0, 1, 0),
                      "border_color": CB})
        if bg:
            s.update({"background_background": "classic", "background_color": bg})
        return con([heading(txt, tag="div", color=color, size=14.4, size_m=11.5,
                            weight=weight, lh=1.4)], **s)
    return con([cell(a, 22, WHITE, 800 if head else 700, "#1A2635" if head else None),
                cell(b, 33, WHITE if head else "#B9C0C8", 800 if head else 400,
                     "#1A2635" if head else None),
                cell(c, 45, WHITE if head else "#77E562", 800 if head else 700,
                     "#1A2635" if head else None)],
               width=sl(100, "%"), flex_direction="row", flex_wrap="nowrap",
               flex_gap=gap(0), flex_align_items="stretch")

compare = section([
    section_head("Why Aluminium",
                 "Premium aluminium vs common roll-formed steel.",
                 "A lighter, corrosion-resistant structural system with clean lines and a "
                 "premium residential finish.", dark=True),
    con([cmp_row("Feature", "Typical roll-formed steel",
                 "Aussie Carport Kits aluminium", head=True),
         cmp_row("Rust resistance", "Relies on protective coating",
                 "Aluminium is corrosion resistant"),
         cmp_row("Weight", "Heavier sections", "Lightweight material"),
         cmp_row("Finish", "Folded / formed profile", "Clean RHS-style appearance"),
         cmp_row("System", "Formed steel sections",
                 "Engineered aluminium beams + posts")],
        width=sl(100, "%"), flex_direction="column", flex_gap=gap(0), overflow="hidden",
        border_border="solid", border_width=dim(1, 1, 1, 1), border_color=CB,
        border_radius=rad(16), margin=dim(32, 0, 0, 0)),
    text("<p>General material comparison only. Exact structural requirements depend on "
         "the specific project and engineering.</p>", color="#8F9AA4", size=12.2,
         lh=1.55),
], bg=DARKBG)
compare["elements"][-1]["settings"]["_margin"] = dim(12, 0, 0, 0)

# ---------------------------------------------------------------- 7. result
result_eb = eyebrow("Real-World Result"); result_eb["settings"]["_margin"] = dim(0, 0, 12, 0)
result_h2 = h2("Built to look right on your home.", size="clamp(2.5rem, 5vw, 4.3rem)")
result_h2["settings"]["_margin"] = dim(0, 0, 18, 0)

result = section([
    rowc([
        colc([result_eb, result_h2,
              text("<p>Clean lines, premium materials and a layout sized to your "
                   "property &mdash; without the guesswork of an off-the-shelf kit.</p>",
                   size=17.3),
              con([btn("Get My Carport Price", "#quote", "primary")],
                  width=sl(100, "%"), _flex_align_self="flex-start", flex_gap=gap(0),
                  margin=dim(24, 0, 0, 0))],
             width=cu("calc(42.5% - 24px)")),
        colc([image(IMG_RESULT)], width=cu("calc(57.5% - 24px)")),
    ], gap_v=48, align="center")], bg=PALE)

# ---------------------------------------------------------------- 8. quote form
def mini_benefit(title, body):
    return con([chip("✓", size=32, fs=15),
                colc([heading(title, tag="div", color=INK, size=16, weight=700, lh=1.4),
                      text(f"<p>{body}</p>", size=14.1)],
                     width=None, width_t=None, width_m=None, gap_v=2, _flex_size="grow")],
               width=sl(100, "%"), flex_direction="row", flex_wrap="nowrap",
               flex_align_items="flex-start", flex_gap=gap(12))

form_widget = widget(
    "form", form_name="Carport Quote",
    form_fields=[
        {"custom_id": "name", "field_type": "text", "field_label": "Name",
         "placeholder": "Your name", "required": "true", "width": "100", "_id": eid()},
        {"custom_id": "phone", "field_type": "tel", "field_label": "Phone",
         "placeholder": "04xx xxx xxx", "required": "true", "width": "50", "_id": eid()},
        {"custom_id": "postcode", "field_type": "text", "field_label": "Postcode",
         "placeholder": "e.g. 2148", "required": "true", "width": "50", "_id": eid()},
        {"custom_id": "i_want", "field_type": "select", "field_label": "I want",
         "field_options": "DIY kit only\nSupply + installation\nNot sure yet",
         "required": "", "width": "100", "_id": eid()},
        {"custom_id": "width", "field_type": "text", "field_label": "Approx. width",
         "placeholder": "e.g. 3.5m", "required": "", "width": "50", "_id": eid()},
        {"custom_id": "length", "field_type": "text", "field_label": "Approx. length",
         "placeholder": "e.g. 6m", "required": "", "width": "50", "_id": eid()},
        {"custom_id": "message", "field_type": "textarea", "field_label": "Anything else?",
         "placeholder": "Tell us about your site, preferred colour or any details that "
                        "may help.",
         "rows": "5", "required": "", "width": "100", "_id": eid()},
    ],
    input_size="md", show_labels="yes", mark_required="", label_position="above",
    button_text="Get My Carport Price →", button_size="sm", button_align="stretch",
    button_width="100",
    submit_actions=["email"],
    email_to="info@aussiecarportkits.com.au",
    email_subject="New carport quote request from your website",
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
    **typo(prefix="label_typography", size=12, weight=800, transform="uppercase",
           ls="0.07em"),
    **typo(prefix="field_typography", size=16, weight=400),
    **typo(prefix="button_typography", size=16, weight=800),
)

quote_eb = eyebrow("Get A Fast Price"); quote_eb["settings"]["_margin"] = dim(0, 0, 12, 0)
quote_h2 = h2("Tell us your size. We&rsquo;ll price the right kit.",
              size="clamp(2.5rem, 5vw, 4.3rem)")
quote_h2["settings"]["_margin"] = dim(0, 0, 18, 0)

quote = section([
    rowc([
        colc([quote_eb, quote_h2,
              text("<p>Send the basics below. We&rsquo;ll review your project and come "
                   "back with a clear, no-obligation price.</p>", size=17.3),
              con([mini_benefit("No-obligation quote", "Know the price before you commit."),
                   mini_benefit("DIY or installed", "Choose the option that suits you."),
                   mini_benefit("Real project support",
                                "Get help from people who understand carport projects.")],
                  width=sl(100, "%"), flex_direction="column", flex_gap=gap(18),
                  margin=dim(28, 0, 0, 0))],
             width=cu("calc(45% - 24px)")),
        colc([colc([form_widget,
                    text("<p>By submitting, you agree to be contacted by Aussie Carport "
                         "Kits about your quote.</p>", color="#848A91", size=11.5,
                         lh=1.5)],
                   width=100, gap_v=10,
                   background_background="classic", background_color=WHITE,
                   border_border="solid", border_width=dim(1, 1, 1, 1),
                   border_color=LINE, border_radius=rad(20),
                   padding=dim(28, 28, 28, 28), **shadow("box_shadow", *SHADOW))],
             width=cu("calc(55% - 24px)")),
    ], gap_v=48, align="flex-start")], element_id="quote")

# ---------------------------------------------------------------- 9. FAQ
FAQ_ITEMS = [
    ("Can I buy the kit without installation?",
     "Yes. The DIY kit is the core offer. We can supply the complete kit for you or "
     "your installer to assemble."),
    ("How quickly can you deliver?",
     "Delivery timing depends on the kit, roof type and location. We confirm the "
     "expected lead time in your quote before you order."),
    ("What information do you need to quote?",
     "Approximate width, length and postcode are enough to start. Photos or plans help "
     "us confirm the right setup faster."),
    ("Why aluminium?",
     "Aluminium is lightweight, corrosion resistant and gives the structure clean "
     "lines. Your final beam and post sizes are determined by the project "
     "requirements."),
]

def faq_item(question, answer):
    """One <details>-style row. Separate Toggle widgets (rather than one Accordion)
    so each row can carry only a bottom rule, like the reference, and so the rows
    open independently the way <details> does."""
    tog = widget("toggle",
                 tabs=[{"tab_title": question,
                        "tab_content": f'<p style="margin:0">{answer}</p>',
                        "_id": eid()}],
                 selected_icon={"value": "fas fa-plus", "library": "fa-solid"},
                 selected_active_icon={"value": "fas fa-minus", "library": "fa-solid"},
                 title_html_tag="div", faq_schema="yes", icon_align="right",
                 border_width=sl(0), border_color="#00000000",
                 title_background="#FFFFFF00", title_color=INK, tab_active_color=INK,
                 icon_color="#30A923", icon_active_color="#30A923", icon_space=sl(20),
                 content_background_color="#FFFFFF00", content_color=TEXT,
                 title_padding=dim(22, 0, 22, 0), content_padding=dim(0, 0, 22, 0),
                 **typo(prefix="title_typography", size=17.6, weight=800, lh=1.4),
                 **typo(prefix="content_typography", size=16, weight=400, lh=1.55))
    return con([tog], width=sl(100, "%"), flex_gap=gap(0),
               border_border="solid", border_width=dim(0, 0, 1, 0), border_color=LINE)

faq = section([
    section_head("Common Questions", "Get the answers you need before you enquire."),
    con([faq_item(q, a) for q, a in FAQ_ITEMS],
        width=sl(100, "%"), flex_direction="column", flex_gap=gap(0),
        border_border="solid", border_width=dim(1, 0, 0, 0), border_color=LINE),
], bg=PALE)


# ---------------------------------------------------------------- 10. footer
footer = section([
    heading("AUSSIE CARPORT KITS", tag="div", color=WHITE, size=16, weight=700, lh=1.3),
    text("<p>Premium DIY carport kits + optional professional installation.</p>",
         color="#96A0AA", size=13.3, lh=1.55),
], bg=DARKBG, padding=dim(34, 0, 90, 0), padding_mobile=dim(34, 0, 110, 0),
   gap_v=8, html_tag="footer")

# ---------------------------------------------------------------- 11. mobile CTA
sticky = con([
    con([btn("Call Us", "#quote", "ghost", full_mobile=True)],
        width=cu("calc(45% - 4px)"), flex_gap=gap(0)),
    con([btn("Get My Price", "#quote", "primary", full_mobile=True)],
        width=cu("calc(55% - 4px)"), flex_gap=gap(0)),
], width=cu("calc(100% - 16px)"), position="fixed",
   _offset_orientation_h="start", _offset_x=sl(8),
   _offset_orientation_v="end", _offset_y_end=sl(8),
   z_index=99, flex_direction="row", flex_wrap="nowrap", flex_align_items="center",
   flex_gap=gap(8), padding=dim(8, 8, 8, 8),
   background_background="classic", background_color=WHITE,
   border_border="solid", border_width=dim(1, 1, 1, 1), border_color=LINE,
   border_radius=rad(18),
   hide_desktop="hidden-desktop", hide_tablet="hidden-tablet",
   **shadow("box_shadow", 0, 14, 36, 0, "rgba(0,0,0,0.22)"))

# the sticky bar's "Call Us" needs a light treatment, not the hero's glass one
sticky["elements"][0]["elements"][0]["settings"].update({
    "background_color": WHITE, "button_text_color": INK,
    "border_color": "#CFD4D0", "button_background_hover_color": PALE,
    "hover_color": INK, "custom_css": ""})

# ---------------------------------------------------------------- assemble
content = [hero, trust, choices, steps, product_story, compare, result, quote,
           faq, footer, sticky]
for _c in content:
    _c["settings"].setdefault("overflow", "hidden")

template = {
    "version": "0.4",
    "title": "Aussie Carport Kits — Paid Traffic Landing Page",
    "type": "page",
    "content": content,
    "page_settings": {"template": "elementor_canvas", "hide_title": "yes"},
}

out = sys.argv[1] if len(sys.argv) > 1 else "aussie-carport-kits-landing-template.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(template, f, ensure_ascii=False, separators=(",", ":"))

def count(els):
    return sum(1 + count(e.get("elements", [])) for e in els)
print(f"wrote {out}: {count(content)} elements, {len(json.dumps(template))} bytes")
