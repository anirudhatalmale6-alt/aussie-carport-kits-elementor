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

