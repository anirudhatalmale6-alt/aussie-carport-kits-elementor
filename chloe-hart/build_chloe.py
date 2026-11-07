#!/usr/bin/env python3
"""
Chloe Hart homepage -> Elementor templates that work on FREE Elementor.

Outputs (next to this file):
  chloe-hart-homepage.json   page template (Elementor Full Width)
  chloe-hart-header.json     section template for the Ultimate Addons (HFE) header
  chloe-hart-footer.json     section template for the HFE footer

Only free widgets: heading, text-editor, image, button, html, icon-list,
social-icons, plus HFE's navigation-menu in the header. Everything that needs
more than Elementor's controls (stacking cards, pinned backgrounds, marquee,
cover fan) is a class name here + a rule in chloe-hart-additional.css.
"""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import elhelp as H
from elhelp import dim, rad, sl, cu, gap, gapxy, typo, shadow, con, grid, widget, adv

OUT = os.path.dirname(os.path.abspath(__file__))
IMG = H.IMG_BASE

# ---------------------------------------------------------------- tokens
INK, PLUM, WINE = "#140D13", "#24131F", "#5A2140"
ROSE, ROSE2, BLUSH, CREAM = "#E8A3B3", "#D9708D", "#F7DFE3", "#FFF4EE"
MUTED, GOLD, MINT = "#C9B3BD", "#E7C36B", "#9FD3BD"
SERIF, SANS, DISP = "DM Serif Display", "DM Sans", "Bebas Neue"
WRAP, WRAP_M = "min(1180px, calc(100% - 40px))", "calc(100% - 32px)"
IG_URL = "https://www.instagram.com/chloehart.author/"
BOOKS = [
    dict(n=1, word="one", slug="book-1", title="Out of My League", pair="Asher + Brittany",
         tropes=["Brother’s best friend", "Player × coach", "Forbidden"], tag="Rugby boys ruin lives",
         blurb="A rugby league bad boy meets the one woman he shouldn’t want: his best friend’s "
               "sister, who just became the team’s new coach.",
         buy="https://www.amazon.com.au/dp/B0F5BYW5YY", color="#FF8FB5", btn="rose"),
    dict(n=2, word="two", slug="book-2", title="Name of the Game", pair="Cameron + Sarah",
         tropes=["Fake dating", "Enemies to lovers", "Second chances"], tag="Fake it until it hurts",
         blurb="Cameron and Sarah can barely stand each other. A fake relationship brings old "
               "wounds, dangerous chemistry and unfinished business back to the surface.",
         buy="https://www.amazon.com.au/dp/B0GHQC2CFQ", color="#C6A2FF", btn="rose"),
    dict(n=3, word="three · New", slug="book-3", title="Match of the Season",
         pair="Lara + Mitchell + Casey", tropes=["Rugby romance", "Single dad", "Why choose"],
         tag="Twice the trouble",
         blurb="A fresh start turns complicated when Lara finds herself falling for two very "
               "different rugby players who want the same thing: her.",
         buy="https://www.amazon.com.au/dp/B0HGWNQT1B", color=GOLD, btn="gold"),
]

def lnk(url, ext=False):
    return {"url": url, "is_external": "on" if ext else "", "nofollow": "",
            "custom_attributes": ""}

def cls(el, *names):
    key = "css_classes" if el["elType"] == "container" else "_css_classes"
    el["settings"][key] = " ".join(n for n in (el["settings"].get(key, ""),) + names if n).strip()
    return el

def anim(el, kind="fadeInUp"):
    el["settings"]["animation" if el["elType"] == "container" else "_animation"] = kind
    return el

# ---------------------------------------------------------------- widgets
def hd(title, tag="div", color=CREAM, family=SERIF, size=None, size_m=None, weight=400,
       lh=1.0, ls=None, transform=None, italic=False, link=None, ext=False, align=None):
    s = {"title": title, "header_size": tag, "title_color": color}
    s.update(typo(size=size, size_m=size_m, weight=weight, lh=lh, ls=ls, transform=transform,
                  family=family))
    if italic: s["typography_font_style"] = "italic"
    if link: s["link"] = lnk(link, ext)
    if align: s["align"] = align
    return widget("heading", **s)

def eyebrow(t, color=ROSE, mb=0, align=None):
    return adv(hd(t, color=color, family=SANS, size=12, weight=700, lh=1.3, ls="0.2em",
                  transform="uppercase", align=align), mb=mb)

def tx(html, color=MUTED, size=17, size_m=16, lh=1.65, align=None):
    s = {"editor": html, "text_color": color}
    s.update(typo(size=size, size_m=size_m, lh=lh, family=SANS, weight=400))
    if align: s["align"] = align
    return widget("text-editor", **s)

def btn(label, url, kind="rose", ext=False, small=False, full_m=False, ident=None):
    s = {"text": label, "link": lnk(url, ext), "size": "md",
         "border_radius": rad(999),
         "text_padding": dim(13, 20, 13, 20) if small else dim(18, 28, 18, 28)}
    s.update(typo(size=12.5 if small else 14, weight=700, lh=1, ls="0.08em",
                  transform="uppercase", family=SANS))
    pal = {"rose": (ROSE2, "#FFFFFF", "#C85A79", None),
           "gold": (GOLD, "#22180A", "#F2D27F", None),
           "line": ("rgba(0,0,0,0)", CREAM, CREAM, "rgba(255,244,238,0.45)"),
           "white": ("rgba(255,255,255,0.92)", INK, "#FFFFFF", None)}[kind]
    bg, fg, hov, border = pal
    s.update({"background_background": "classic", "background_color": bg,
              "button_text_color": fg, "hover_color": INK if kind == "line" else fg,
              "button_background_hover_background": "classic",
              "button_background_hover_color": hov})
    if border:
        s.update({"border_border": "solid", "border_width": dim(1.5, 1.5, 1.5, 1.5),
                  "border_color": border, "button_hover_border_color": CREAM})
    if full_m: s["align_mobile"] = "justify"
    if ident: s["button_css_id"] = ident
    return widget("button", **s)

def img(fname, link=None, ext=False, alt="", width=None):
    s = {"image": {"url": f"{IMG}/{fname}", "id": "", "source": "library", "alt": alt},
         "image_size": "full"}
    if link:
        s["link_to"] = "custom"; s["link"] = lnk(link, ext)
    if width: s["width"] = width
    return widget("image", **s)

def html(code):
    return widget("html", html=code)

def chips(items):
    return tx('<p style="margin:0">' + "".join(f'<span class="ch-chip">{t}</span>' for t in items)
              + "</p>", color=BLUSH, size=12, lh=1)

def sec(children, ident=None, classes=(), pad=(110, 110), pad_m=(70, 70), row=False,
        bg=None, align="center", gap_px=40, gap_t=None, **extra):
    s = {"content_width": "boxed", "boxed_width": cu(WRAP), "boxed_width_tablet": cu(WRAP),
         "boxed_width_mobile": cu(WRAP_M),
         "flex_direction": "row" if row else "column",
         "flex_direction_tablet": "column", "flex_direction_mobile": "column",
         "flex_align_items": align if row else "stretch",
         "flex_gap": gap(gap_px), "flex_gap_tablet": gap(gap_t or gap_px), "flex_wrap": "nowrap",
         "padding": dim(pad[0], 0, pad[1], 0), "padding_mobile": dim(pad_m[0], 0, pad_m[1], 0)}
    if bg: s.update({"background_background": "classic", "background_color": bg})
    if ident: s["_element_id"] = ident
    s.update(extra)
    c = con(children, **s)
    return cls(c, *classes)

def col(children, width=None, gap_px=0, classes=(), **st):
    s = {"flex_direction": "column", "flex_gap": gap(gap_px)}
    if width:
        s["width"] = cu(width) if isinstance(width, str) else sl(width, "%")
        s["width_tablet"] = sl(100, "%"); s["width_mobile"] = sl(100, "%")
    s.update(st)
    return cls(con(children, **s), *classes)

def rowc(children, gap_px=12, wrap=True, classes=(), **st):
    s = {"flex_direction": "row", "flex_wrap": "wrap" if wrap else "nowrap",
         "flex_gap": gap(gap_px), "flex_align_items": "center"}
    s.update(st)
    return cls(con(children, **s), *classes)

# ================================================================ PAGE
H1 = 'Good girls love <em>bad</em> stories<span class="ch-dot">.</span>'
hero = sec([
    col([eyebrow("Chloe Hart · Rucked &amp; Ruined series", mb=22),
         adv(hd(H1, tag="h1", size="clamp(52px, 7.6vw, 112px)", size_m=50, lh=0.92,
                ls="-0.035em"), mb=24),
         adv(tx("<p>Rugby league bad boys. Forbidden chemistry. Fierce women who refuse to "
                "play by the rules. Welcome to your next fictional obsession.</p>", size=19,
                size_m=17), width="min(560px, 100%)"),
         adv(rowc([btn("Start with Book One →", "#book-1", full_m=True),
                   btn("New release ↓", "#new", "line", full_m=True)], gap_px=12,
                  classes=("ch-ctas",)), mt=34)],
        width="52%"),
    col([cls(img("chloe-book1.webp", "#book-1", alt="Out of My League by Chloe Hart"),
             "ch-cover", "ch-c1"),
         cls(img("chloe-book3.webp", "#new", alt="Match of the Season by Chloe Hart"),
             "ch-cover", "ch-c2"),
         cls(img("chloe-book2.webp", "#book-2", alt="Name of the Game by Chloe Hart"),
             "ch-cover", "ch-c3"),
         cls(hd("New · Book 3", family=SANS, size=11, weight=700, lh=1, ls="0.18em",
                transform="uppercase", color="#22180A"), "ch-newtag"),
         cls(hd("Love hard.<br>Play dirty.", italic=True, size=25, size_m=22, lh=1.08,
                color=WINE, align="center"), "ch-sticker", "ch-sticker-hero")],
        width="48%", classes=("ch-fan",)),
], ident="top", classes=("ch-hero",), row=True, pad=(70, 110), pad_m=(44, 60), gap_px=40)

def marquee(items, cls_name):
    one = "".join(f"<span>{t}</span>" for t in items)
    return html(f'<div class="{cls_name}" aria-hidden="true"><div class="ch-track">{one}{one}'
                f'</div></div>')

band = marquee(["Brother’s best friend ✦", "Fake dating ✦", "Enemies to lovers ✦", "Single dad ✦",
                "Why choose ✦", "Player × coach ✦", "Second chances ✦"], "ch-band")

b3 = BOOKS[2]
release = sec([
    cls(img("chloe-book3.webp", b3["buy"], ext=True, alt="Match of the Season by Chloe Hart"),
        "ch-cover-lg"),
    col([eyebrow("New release · Rucked &amp; Ruined Book 3", color=MINT, mb=18),
         adv(hd("Match of the Season", tag="h2", family=DISP, size="clamp(60px, 8vw, 118px)",
                size_m=58, lh=0.86, ls="0.01em", color=GOLD), mb=10),
         adv(hd(b3["pair"], italic=True, size=26, size_m=22, lh=1.2, color=BLUSH), mb=22),
         chips(b3["tropes"]),
         adv(tx(f"<p>{b3['blurb']}</p>", color="#E7DDE2", size=19, size_m=17), mt=22, mb=30),
         btn("Buy on Amazon", b3["buy"], "gold", ext=True, full_m=True)], width="58%"),
], ident="new", classes=("ch-pinned", "ch-bg-turf"), row=True, pad=(130, 130), pad_m=(80, 80),
   gap_px=80, gap_t=40)

def card(b, i):
    body = col([
        hd(f"Book {b['word']}", family=SANS, size=12, weight=700, lh=1, ls="0.2em",
           transform="uppercase", color="rgba(255,244,238,0.75)"),
        adv(hd(b["title"], tag="h3", family=DISP, size="clamp(46px, 5vw, 70px)", size_m=38,
               lh=0.88, ls="0.01em", color=b["color"]), mt=12, mb=6),
        adv(hd(b["pair"], italic=True, size=21, size_m=18, lh=1.2, color=BLUSH), mb=16),
        chips(b["tropes"]),
        adv(tx(f"<p>{b['blurb']}</p>", color="#EADDE3", size=16.5, size_m=15.5), mt=16, mb=20),
        btn("Buy on Amazon", b["buy"], b["btn"], ext=True, small=True),
    ], classes=("ch-card-body",), _flex_size="grow")
    c = con([cls(hd(b["tag"], italic=True, size=15, size_m=13, lh=1, color=WINE), "ch-tag"),
             cls(img(f"chloe-book{b['n']}.webp", b["buy"], ext=True,
                     alt=f"{b['title']} book cover"), "ch-card-cover"),
             body],
            flex_direction="row", flex_gap=gap(36), flex_align_items="flex-start",
            flex_wrap="nowrap", padding=dim(40, 40, 40, 40), padding_mobile=dim(22, 18, 22, 18),
            border_radius=rad(26), _element_id=b["slug"])
    return cls(c, "ch-card", f"ch-k{b['n']}", f"ch-i{i}")

series = sec([
    col([eyebrow("The Rucked &amp; Ruined series", mb=18),
         adv(hd("Love is a <em>contact sport.</em>", tag="h2", size="clamp(42px, 5.2vw, 76px)",
                size_m=40, lh=0.98, ls="-0.03em"), mb=22),
         tx("<p>Three interconnected standalones set in the high-stakes world of Australian "
            "rugby league, where the games are brutal and the chemistry is even more "
            "dangerous.</p>", size=18, size_m=17),
         adv(tx('<p class="ch-order"><a href="#book-1"><span>1</span>Out of My League</a>'
                '<a href="#book-2"><span>2</span>Name of the Game</a>'
                '<a href="#book-3"><span>3</span>Match of the Season</a></p>',
                color=BLUSH, size=16, lh=1.4), mt=30)],
        width="38%", classes=("ch-sticky",)),
    col([card(b, i) for i, b in enumerate(BOOKS)], width="62%", gap_px=28,
        classes=("ch-stack",)),
], ident="books", row=True, align="flex-start", pad=(130, 70), pad_m=(80, 50), gap_px=60, gap_t=30)

warnings = sec([tx("<p>Content and trigger warnings are included at the front of each book.</p>",
                   size=14, align="center")], pad=(0, 40), pad_m=(0, 30))

about = sec([
    con([
        col([cls(img("chloe-author-photo-placeholder.webp", alt="Chloe Hart"), "ch-arch"),
             cls(hd("A little<br>unhinged ♡", italic=True, size=17, lh=1.05, color=WINE,
                    align="center"), "ch-sticker", "ch-sticker-about")],
            width="42%", classes=("ch-photo",)),
        col([eyebrow("The author behind the chaos", mb=16),
             adv(hd("Hey, I’m <em>Chloe.</em>", tag="h2", size="clamp(42px, 5.2vw, 76px)",
                    size_m=40, lh=0.98, ls="-0.03em"), mb=22),
             tx("<p>I write the kind of love stories that take over your thoughts, wreck your "
                "bedtime and make you question your taste in fictional men.</p>"
                "<p>My Rucked &amp; Ruined series takes you into the high-stakes world of "
                "Australian rugby league, where the games are brutal and the chemistry is even "
                "more dangerous.</p>"
                "<p>Come for the boys who play dirty. Stay for the women who give them a run "
                "for their money.</p>"),
             adv(hd("Love, Chloe x", italic=True, size=34, size_m=30, lh=1, color=ROSE),
                 mt=24, mb=26),
             btn("Find me on Instagram ↗", IG_URL, "line", ext=True)],
            width="58%"),
    ], flex_direction="row", flex_direction_tablet="column", flex_direction_mobile="column",
       flex_gap=gap(70), flex_gap_tablet=gap(36), flex_align_items="center",
       padding=dim(60, 60, 60, 60), padding_mobile=dim(26, 22, 30, 22),
       background_background="classic", background_color="rgba(20,13,19,0.92)",
       border_border="solid", border_width=dim(1, 1, 1, 1),
       border_color="rgba(255,228,236,0.16)", border_radius=rad(30)),
], ident="about", classes=("ch-pinned", "ch-bg-check"), pad=(150, 150), pad_m=(80, 80))

def tile(i, title, sub, go, url, ext=False, k=1):
    c = con([col([hd(title, tag="h3", size="clamp(34px, 3.4vw, 46px)", size_m=32, lh=1,
                     color="inherit"),
                  adv(hd(sub, family=SANS, size=12.5, weight=700, lh=1.6, ls="0.14em",
                         transform="uppercase", color="inherit"), mt=14)]),
             cls(hd(go, family=SANS, size=12.5, weight=700, lh=1, ls="0.14em",
                    transform="uppercase", color=INK), "ch-go")],
            html_tag="a", link=lnk(url, ext), flex_direction="column",
            flex_justify_content="space-between", flex_gap=gap(20),
            min_height=sl(260), min_height_mobile=sl(230),
            padding=dim(34, 34, 30, 34), padding_mobile=dim(28, 24, 24, 24),
            border_radius=rad(24))
    return cls(c, "ch-tile", f"ch-t{k}", f"ch-i{i}")

nextsec = sec([
    col([eyebrow("For the morally grey kind of reader", mb=16),
         adv(hd("Where to <em>next?</em>", tag="h2", size="clamp(42px, 5.2vw, 76px)", size_m=40,
                lh=0.98, ls="-0.03em"), mb=18),
         tx("<p>A dangerous book boyfriend? An athlete with a filthy mouth? Pick your "
            "poison.</p>", size=18, size_m=17)], width="50%", classes=("ch-sticky",)),
    col([tile(0, "Start the series", "Asher, Brittany and one very bad idea", "Book one →",
              "#book-1", k=1),
         tile(1, "Get the extras", "Cover reveals, bonus content and first dibs on new releases",
              "Join the list →", "#list", k=2),
         tile(2, "Come say hi", "Teasers, book boyfriends and the chaos behind the pages",
              "@chloehart.author ↗", IG_URL, ext=True, k=3)],
        width="50%", gap_px=24, classes=("ch-tiles",)),
], row=True, align="flex-start", pad=(130, 130), pad_m=(80, 80), gap_px=90, gap_t=30)

FORM = """<!-- NEWSLETTER: replace everything inside this box with the MailerLite embed code -->
<form class="ch-news-form" onsubmit="return false">
  <input type="text" name="first_name" placeholder="First name" aria-label="First name">
  <input type="email" name="email" placeholder="Email address" aria-label="Email address" required>
  <button type="submit">Count me in</button>
</form>"""

news = sec([
    con([eyebrow("Your invitation to the dark side", color=ROSE2, mb=16, align="center"),
         adv(hd("Get on <em>the list.</em>", tag="h2", size="clamp(42px, 5.2vw, 76px)",
                size_m=40, lh=0.98, ls="-0.03em", color="#2A0F20", align="center"), mb=16),
         tx("<p>First dibs on new releases, cover reveals, exclusive extras and all the chaos "
            "behind the pages. No boring emails. Promise.</p>", color="#6D4A5B", size=17,
            align="center"),
         adv(cls(html(FORM), "ch-news-embed"), mt=30)],
        flex_direction="column", flex_align_items="stretch",
        width=cu("min(820px, 100%)"), width_tablet=cu("min(820px, 100%)"),
        width_mobile=sl(100, "%"), margin=dim(0, "auto", 0, "auto"),
        padding=dim(64, 64, 64, 64), padding_mobile=dim(32, 22, 32, 22),
        background_background="classic", background_color=CREAM, border_radius=rad(30),
        **shadow("box_shadow", 0, 40, 90, 0, "rgba(60,10,30,0.35)")),
], ident="list", classes=("ch-pinned", "ch-bg-hearts"), pad=(140, 140), pad_m=(80, 80))

IG_TILES = [("chloe-book1.webp", "50% 20%"), ("chloe-book2.webp", "50% 85%"),
            ("chloe-book3.webp", "50% 15%"), ("chloe-book1.webp", "50% 90%"),
            ("chloe-book2.webp", "50% 15%"), ("chloe-book3.webp", "50% 85%")]
insta = sec([
    rowc([col([eyebrow("Follow along", mb=12),
               hd("@chloehart.author", tag="h2", size="clamp(32px, 3.4vw, 46px)", size_m=32,
                  lh=1.02, ls="-0.02em")], width="auto"),
          btn("Follow on Instagram ↗", IG_URL, "line", ext=True, small=True)],
         gap_px=20, flex_justify_content="space-between", flex_align_items="flex-end"),
    cls(grid([cls(img(f, IG_URL, ext=True), "ch-ig", f"ch-ig-{n}") for n, (f, _) in
                            enumerate(IG_TILES)],
                           cols="repeat(6, minmax(0, 1fr))", cols_t="repeat(3, minmax(0, 1fr))",
                           cols_m="repeat(2, minmax(0, 1fr))", g=(10, 10)), "ch-ig-grid"),
], ident="instagram", pad=(110, 80), pad_m=(70, 60), gap_px=28)

STACK_JS = """<script>
/* Stacked book cards: the card underneath shrinks and dims as the next one slides over it. */
(function(){
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var cards = [].slice.call(document.querySelectorAll('.ch-card')), busy = false;
  function run(){
    cards.forEach(function(c, i){
      var n = cards[i + 1];
      if (!n) { c.style.transform = ''; c.style.filter = ''; return; }
      var gap = n.getBoundingClientRect().top - c.getBoundingClientRect().top;
      var p = Math.min(1, Math.max(0, 1 - gap / c.offsetHeight));
      c.style.transform = 'scale(' + (1 - p * 0.06) + ')';
      c.style.filter = 'brightness(' + (1 - p * 0.35) + ')';
    });
    busy = false;
  }
  window.addEventListener('scroll', function(){ if (!busy) { busy = true; requestAnimationFrame(run); } }, {passive: true});
  run();
})();
</script>"""
js = cls(html(STACK_JS), "ch-js")

for el in (hero["elements"][0], release["elements"][1], about["elements"][0],
           news["elements"][0]):
    anim(el)

page_content = [hero, band, release, series, warnings, about, nextsec, news, insta, js]

# ================================================================ HEADER
strip = marquee([f'<a href="/#new">New release ✦ Match of the Season is out now</a>',
                 "✦ Rucked &amp; Ruined · Book 3", '<a href="/#book-1">✦ Start the series with '
                 'Out of My League</a>', "✦ Love hard. Play dirty. ✦"], "ch-strip")
logo = col([hd('chloe <span class="ch-logo-hart">hart.</span>', size=34, size_m=29, lh=1,
               ls="-0.04em", link="/"),
            adv(hd("Dark &amp; sports romance", family=SANS, size=9.5, weight=700, lh=1,
                   ls="0.24em", transform="uppercase", color=MUTED), mt=6)],
           classes=("ch-logo",), _flex_size="none")
logo["settings"].update(width=cu("auto"), width_tablet=cu("auto"), width_mobile=cu("auto"))
nav = widget("navigation-menu",
             layout="horizontal", navmenu_align="right", dropdown="mobile",
             resp_align="left", full_width_dropdown="yes",
             color_menu_item=BLUSH, color_menu_item_hover=ROSE, color_menu_item_active=ROSE,
             padding_horizontal_menu_item=sl(15), padding_vertical_menu_item=sl(10),
             color_dropdown_item=BLUSH, background_color_dropdown_item=INK,
             color_dropdown_item_hover=ROSE, background_color_dropdown_item_hover=PLUM,
             padding_horizontal_dropdown_item=sl(20), padding_vertical_dropdown_item=sl(16),
             toggle_color=CREAM, toggle_size=sl(22),
             **typo(prefix="menu_typography", size=13, weight=700, lh=1, ls="0.14em",
                    transform="uppercase", family=SANS),
             **typo(prefix="dropdown_typography", size=14, weight=700, lh=1, ls="0.14em",
                    transform="uppercase", family=SANS))
nav = cls(adv(nav, grow=True), "ch-nav")
social = cls(widget("social-icons",
                    social_icon_list=[{"_id": "ig01", "social_icon": {"value": "fab fa-instagram",
                                       "library": "fa-brands"}, "link": lnk(IG_URL, True)}],
                    icon_color="custom", icon_primary_color="rgba(0,0,0,0)",
                    icon_secondary_color=BLUSH, icon_size=sl(17), icon_padding=sl(11),
                    border_border="solid", border_width=dim(1, 1, 1, 1),
                    border_color="rgba(255,228,236,0.16)", border_radius=rad(50),
                    hide_mobile="hidden-mobile"), "ch-social")
join = adv(btn("Join the list", "/#list", small=True), hide_m=True)
header_row = con([logo, nav, social, join], content_width="boxed",
                 boxed_width=cu(WRAP), boxed_width_tablet=cu(WRAP), boxed_width_mobile=cu(WRAP_M),
                 flex_direction="row", flex_direction_tablet="row", flex_direction_mobile="row",
                 flex_align_items="center", flex_wrap="nowrap", flex_gap=gap(18),
                 min_height=sl(76), min_height_mobile=sl(66))
header = cls(con([strip, header_row], flex_direction="column",
                 background_background="classic", background_color="rgba(20,13,19,0.92)",
                 border_border="solid", border_width=dim(0, 0, 1, 0),
                 border_color="rgba(255,228,236,0.16)"), "ch-header")
header_content = [header]

# ================================================================ FOOTER
def links(items):
    return widget("icon-list", icon_list=[
        {"_id": f"l{i:02d}", "text": t, "selected_icon": {"value": "", "library": ""},
         "link": lnk(u, u.startswith("http"))} for i, (t, u) in enumerate(items)],
        space_between=sl(10), text_color=MUTED, text_color_hover=CREAM,
        **typo(prefix="icon_typography", size=15, lh=1.5, family=SANS, weight=400))

footer = cls(sec([
    cls(grid([col([hd('chloe <span class="ch-logo-hart">hart.</span>', size=34, lh=1,
                      ls="-0.04em", link="/"),
                   adv(hd("Dark &amp; sports romance author", family=SANS, size=9.5, weight=700,
                          lh=1, ls="0.24em", transform="uppercase", color=MUTED), mt=6),
                   adv(tx("<p>Rugby bad boys. Dangerous chemistry. Stories that don’t play "
                          "nice.</p>", size=15), mt=16, width="min(320px, 100%)")],
                  classes=("ch-foot-brand",)),
              col([adv(eyebrow("Explore"), mb=18),
                   links([("The books", "/#books"), ("New release", "/#new"),
                          ("Meet Chloe", "/#about")])]),
              col([adv(eyebrow("Stay close"), mb=18),
                   links([("Newsletter", "/#list"), ("Instagram ↗", IG_URL)])])],
             cols="1.3fr 1fr 1fr", cols_t="1.3fr 1fr 1fr", cols_m="1fr 1fr", g=(40, 30)),
        "ch-foot-grid"),
    rowc([tx("<p>© 2026 Chloe Hart. Made for readers who like it dark.</p>", color="#9B8590",
             size=13),
          tx('<p><a href="#top">Back to top ↑</a></p>', color="#9B8590", size=13)],
         gap_px=20, flex_justify_content="space-between", classes=("ch-legal",),
         padding=dim(24, 0, 0, 0), border_border="solid", border_width=dim(1, 0, 0, 0),
         border_color="rgba(255,228,236,0.16)"),
], pad=(60, 34), pad_m=(50, 30), gap_px=50, bg="#0F0A0E"), "ch-footer")
footer_content = [footer]

# ================================================================ write
def count(els, kind):
    n = 0
    for e in els:
        n += e["elType"] == kind
        n += count(e.get("elements", []), kind)
    return n

def dump(name, title, content, typ, page_settings=None):
    t = {"version": "0.4", "title": title, "type": typ, "content": content}
    if page_settings is not None: t["page_settings"] = page_settings
    p = os.path.join(OUT, name)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(t, f, ensure_ascii=False, indent=1)
    print(f"wrote {name}: {count(content, 'container')} containers, "
          f"{count(content, 'widget')} widgets")

dump("chloe-hart-homepage.json", "Chloe Hart — Homepage", page_content, "page",
     {"template": "elementor_header_footer", "hide_title": "yes",
      "background_background": "classic", "background_color": INK})
dump("chloe-hart-header.json", "Chloe Hart — Header", header_content, "section")
dump("chloe-hart-footer.json", "Chloe Hart — Footer", footer_content, "section")
