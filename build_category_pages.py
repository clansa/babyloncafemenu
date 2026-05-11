# -*- coding: utf-8 -*-
"""Generates one HTML file per menu category. Run: python build_category_pages.py"""
from __future__ import annotations

import pathlib

ROOT = pathlib.Path(__file__).resolve().parent

SCRIPT = """
  <script>
    (function () {
      var toggle = document.querySelector(".menu-toggle");
      var drawer = document.querySelector(".nav-drawer");
      var links = drawer.querySelectorAll("a");
      function setOpen(open) {
        toggle.setAttribute("aria-expanded", open);
        toggle.setAttribute("aria-label", open ? "Menüyü kapat" : "Menüyü aç");
        drawer.setAttribute("aria-hidden", !open);
        drawer.classList.toggle("is-open", open);
        document.body.style.overflow = open ? "hidden" : "";
      }
      toggle.addEventListener("click", function () {
        setOpen(toggle.getAttribute("aria-expanded") !== "true");
      });
      links.forEach(function (a) {
        a.addEventListener("click", function () { setOpen(false); });
      });
      window.addEventListener("resize", function () {
        if (window.matchMedia("(min-width: 1024px)").matches) setOpen(false);
      });
    })();
  </script>
"""

SVG_LOGO = """<svg class="brand-logo" viewBox="0 0 64 64" aria-hidden="true">
        <circle cx="32" cy="32" r="30" fill="#1a1408" stroke="#d4af37" stroke-width="2.5" />
        <circle cx="32" cy="32" r="24" fill="none" stroke="#d4af37" stroke-width="0.8" opacity="0.5" />
        <path fill="#d4af37" d="M32 18c-4 0-7 2.5-8.5 6 .8-1 2-1.5 3.2-1.5 2.4 0 4.3 2.2 4.3 5 0 .8-.1 1.5-.4 2.2 1.5-1.2 3.4-2 5.4-2 1.8 0 3.5.6 4.8 1.6-.3-.7-.4-1.4-.4-2.1 0-2.8 1.9-5 4.3-5 1.2 0 2.4.5 3.2 1.5-1.5-3.5-4.5-6-8.5-6zm-6 14c-1.2 0-2.2.4-3 1.1-.8.7-1.3 1.7-1.5 2.8l-.5 3.2c-.3 2-.5 4.2-.5 6.5h22c0-2.3-.2-4.5-.5-6.5l-.5-3.2c-.2-1.1-.7-2.1-1.5-2.8-.8-.7-1.8-1.1-3-1.1-1.5 0-2.8.7-3.6 1.8-.8-1.1-2.1-1.8-3.6-1.8s-2.8.7-3.6 1.8c-.8-1.1-2.1-1.8-3.6-1.8zm3.5 16c0 1.4 1.1 2.5 2.5 2.5s2.5-1.1 2.5-2.5h5c0 1.4 1.1 2.5 2.5 2.5s2.5-1.1 2.5-2.5h2.5v-2h-20v2H29.5z" />
        <text x="32" y="54" text-anchor="middle" fill="#d4af37" font-family="Montserrat, sans-serif" font-size="5.5" font-weight="700" letter-spacing="2">CAFE</text>
      </svg>"""


def esc(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def product_card(folder: str, idx: int, name: str, price: str) -> str:
    img = f"assets/{folder}/item-{idx:02d}.jpg"
    return f"""    <article class="product-card">
      <div class="product-card__photo" style="background-image:url('{img}');"></div>
      <div class="product-card__body">
        <h3 class="product-card__title">{esc(name)}</h3>
        <p class="product-card__price">{esc(price)}</p>
      </div>
    </article>"""


def build_page(
    filename: str,
    title: str,
    banner: str,
    folder: str,
    intro: str,
    sections: list[tuple[str | None, list[tuple[str, str]]]],
    note_after: str | None = None,
) -> str:
    """sections: (subsection_title or None, [(name, price), ...])"""
    lines: list[str] = []
    idx = 1
    for sub, items in sections:
        if sub:
            lines.append(f'    <h2 class="category-sub">{esc(sub)}</h2>')
        if items:
            lines.append('    <div class="product-grid">')
            for name, price in items:
                lines.append(product_card(folder, idx, name, price))
                idx += 1
            lines.append("    </div>")
    body_products = "\n".join(lines)
    note_block = ""
    if note_after:
        note_block = f'    <p class="category-page__intro" style="margin-top:1.5rem">{esc(note_after)}</p>'

    return f"""<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover" />
  <title>{esc(title)} — Babylon Cafe</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&family=Playfair+Display:wght@500;600&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="assets/menu-doc.css" />
  <style>
    :root {{
      --category-banner: url("{esc(banner)}");
    }}
  </style>
</head>
<body>
  <header class="site-header">
    <img class="brand-logo" src="assets/logo.webp" alt="Babylon Cafe logo" />
      {SVG_LOGO}
      <span class="brand-text">
        <span class="brand-text__name">Babylon</span>
        <span class="brand-text__tag">CAFE</span>
      </span>
    </a>
    <nav class="nav-desktop" aria-label="Ana navigasyon">
      <a href="index.html#hero">Ana Sayfa</a>
      <a href="index.html#menu">Menü</a>
      <a href="index.html#iletisim">İletişim</a>
    </nav>
    <button type="button" class="menu-toggle" aria-expanded="false" aria-controls="mobile-nav" aria-label="Menüyü aç">
      <span></span><span></span><span></span>
    </button>
  </header>

  <nav id="mobile-nav" class="nav-drawer" aria-hidden="true" aria-label="Mobil menü">
    <a href="index.html#hero">Ana Sayfa</a>
    <a href="index.html#menu">Menü</a>
    <a href="index.html#iletisim">İletişim</a>
  </nav>

  <main class="category-page">
    <a class="menu-doc__back" href="index.html#menu">← Ana menüye dön</a>
    <div class="category-hero" role="img" aria-hidden="true"></div>
    <h1 class="category-page__title">{esc(title)}</h1>
    <p class="category-page__intro">{esc(intro)}</p>
{body_products}
{note_block}
  </main>
{SCRIPT}
</body>
</html>
"""


def note_only_page(
    filename: str, title: str, banner: str, body: str, body_is_html: bool = False
) -> str:
    body_content = body if body_is_html else esc(body)
    return f"""<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover" />
  <title>{esc(title)} — Babylon Cafe</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&family=Playfair+Display:wght@500;600&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="assets/menu-doc.css" />
  <style>
    :root {{
      --category-banner: url("{esc(banner)}");
    }}
  </style>
</head>
<body>
  <header class="site-header">
    <img class="brand-logo" src="assets/logo.webp" alt="Babylon Cafe logo" />
      {SVG_LOGO}
      <span class="brand-text">
        <span class="brand-text__name">Babylon</span>
        <span class="brand-text__tag">CAFE</span>
      </span>
    </a>
    <nav class="nav-desktop" aria-label="Ana navigasyon">
      <a href="index.html#hero">Ana Sayfa</a>
      <a href="index.html#menu">Menü</a>
      <a href="index.html#iletisim">İletişim</a>
    </nav>
    <button type="button" class="menu-toggle" aria-expanded="false" aria-controls="mobile-nav" aria-label="Menüyü aç">
      <span></span><span></span><span></span>
    </button>
  </header>

  <nav id="mobile-nav" class="nav-drawer" aria-hidden="true" aria-label="Mobil menü">
    <a href="index.html#hero">Ana Sayfa</a>
    <a href="index.html#menu">Menü</a>
    <a href="index.html#iletisim">İletişim</a>
  </nav>

  <main class="category-page">
    <a class="menu-doc__back" href="index.html#menu">← Ana menüye dön</a>
    <div class="category-hero" role="img" aria-hidden="true"></div>
    <h1 class="category-page__title">{esc(title)}</h1>
    <div class="menu-doc__section" style="margin-top:0.5rem">
      <div class="menu-doc__note" style="margin:0;font-size:1rem;font-style:normal;line-height:1.6">{body_content}</div>
    </div>
  </main>
{SCRIPT}
</body>
</html>
"""


def main() -> None:
    pages: list[tuple[str, str]] = []

    pages.append(
        (
            "kampanyalar.html",
            note_only_page(
                "kampanyalar.html",
                "Kampanyalar",
                "assets/kampanyalar.png",
                "Günün kampanyası ve set menüler düzenli olarak güncellenir. "
                'Güncel teklifler için <a href="tel:+905326977333">+90 532 697 73 33</a> veya '
                '<a href="https://instagram.com" target="_blank" rel="noopener">Instagram</a> üzerinden iletişime geçebilirsiniz.',
                body_is_html=True,
            ),
        )
    )

    pages.append(
        (
            "baslangic.html",
            note_only_page(
                "baslangic.html",
                "Başlangıç",
                "assets/baslangic.png",
                "Meze ve başlangıç tabakları günlük değişebilir. "
                "Güncel liste ve fiyatlar için garsonunuza danışın veya kasayı sorun.",
            ),
        )
    )

    makarnalar = [
        ("Ton balıklı penne", "390 ₺"),
        ("Kremalı mantar tavuklu penne", "380 ₺"),
        ("Spaghetti Napoliten", "340 ₺"),
        ("Köri soslu tavuklu penne", "380 ₺"),
        ("Spaghetti Bolonez", "390 ₺"),
        ("Penne sebze", "310 ₺"),
        ("Tavuklu brokolili penne", "340 ₺"),
        ("Tavuklu fettucini Alfredo", "400 ₺"),
        ("Penne all’arrabbiata", "340 ₺"),
        ("Acılı sebzeli penne", "340 ₺"),
    ]
    pages.append(
        (
            "makarnalar.html",
            build_page(
                "makarnalar.html",
                "Makarnalar",
                "assets/makarnalar.png",
                "makarnalar",
                "Her ürün kartındaki fotoğraf: assets/makarnalar/item-01.jpg … item-10.jpg dosyalarını ekleyin (sıra listedeki sırayla).",
                [(None, makarnalar)],
            ),
        )
    )

    pages.append(
        (
            "salatalar.html",
            note_only_page(
                "salatalar.html",
                "Salatalar",
                "assets/salata.png",
                "Salata çeşitleri mevsime göre değişir. "
                "Güncel tabaklar ve fiyatlar için lütfen garsona veya kasaya sorun.",
            ),
        )
    )

    ev_sections: list[tuple[str | None, list[tuple[str, str]]]] = [
        (
            "Kırmızı etler",
            [
                ("Izgara servis köfte", "600 ₺"),
                ("Köfte çökertme", "640 ₺"),
                ("Köfte fajita", "600 ₺"),
                ("Beğendili kasap köfte", "680 ₺"),
            ],
        ),
        (
            "Tavuk yemekleri",
            [
                ("Noodle tavuklu", "380 ₺"),
                ("Köri soslu tavuk", "430 ₺"),
                ("Kremalı mantarlı tavuk", "430 ₺"),
                ("Tavuk şnitzel", "410 ₺"),
                ("Mantar soslu şnitzel", "520 ₺"),
                ("Tavuk schnitzel", "400 ₺"),
                ("Tavuk çökertme", "450 ₺"),
                ("Tavuk fajita", "450 ₺"),
                ("Piliç ızgara", "430 ₺"),
                ("Mantar soslu piliç ızgara", "450 ₺"),
                ("Sweet chili soslu tavuk", "430 ₺"),
                ("Barbekü soslu tavuk", "430 ₺"),
                ("Tavuklu quesadilla", "450 ₺"),
                ("Köri soslu quesadilla", "450 ₺"),
                ("Barbekü soslu quesadilla", "450 ₺"),
                ("Acılı (Mexican) quesadilla", "450 ₺"),
            ],
        ),
    ]
    pages.append(
        (
            "ev-yemekleri.html",
            build_page(
                "ev-yemekleri.html",
                "Ev yemekleri",
                "assets/ev-yemekleri.png",
                "ev-yemekleri",
                "Fotoğraflar: assets/ev-yemekleri/item-01.jpg … item-20.jpg (önce kırmızı et, sonra tavuk sırasıyla).",
                ev_sections,
            ),
        )
    )

    pages.append(
        (
            "kahvaltilar.html",
            note_only_page(
                "kahvaltilar.html",
                "Kahvaltılar",
                "assets/kahvalti.png",
                "Serpme ve tabak kahvaltı seçenekleri ile fiyatlar kasada güncellenir. "
                "Detay için işletmeyi arayın veya mekânda menüyü isteyin.",
            ),
        )
    )

    burgers = [
        ("Hamburger", "410 ₺"),
        ("Tavuk burger", "380 ₺"),
        ("Special burger (double)", "600 ₺"),
        ("Babylon special burger", "450 ₺"),
        ("Mantar soğan cheddar", "460 ₺"),
        ("Cheese burger", "450 ₺"),
        ("Babylon çıtır tavuk burger", "430 ₺"),
    ]
    pages.append(
        (
            "hamburger.html",
            build_page(
                "hamburger.html",
                "Hamburger",
                "assets/hamburger.png",
                "hamburger",
                "Fotoğraflar: assets/hamburger/item-01.jpg … item-07.jpg.",
                [(None, burgers)],
            ),
        )
    )

    pizzas = [
        ("Pizza karışık", "400 ₺"),
        ("Pizza margarita", "330 ₺"),
    ]
    pages.append(
        (
            "pizza.html",
            build_page(
                "pizza.html",
                "Pizza",
                "assets/pizza.png",
                "pizza",
                "Fotoğraflar: assets/pizza/item-01.jpg ve item-02.jpg.",
                [(None, pizzas)],
            ),
        )
    )

    wraps = [
        ("Tavuklu schnitzel wrap", "390 ₺"),
        ("Izgara tavuk wrap", "390 ₺"),
        ("Barbekü soslu tavuk wrap", "420 ₺"),
        ("Köri soslu tavuk wrap", "420 ₺"),
        ("Acı soslu tavuk wrap", "420 ₺"),
    ]
    pages.append(
        (
            "tost-cesitleri.html",
            build_page(
                "tost-cesitleri.html",
                "Tost çeşitleri & wrap",
                "assets/tost-cesitleri.png",
                "tost-cesitleri",
                "Wrap fotoğrafları: assets/tost-cesitleri/item-01.jpg … item-05.jpg. "
                "Klasik tost çeşitleri için kasadan fiyat alabilirsiniz.",
                [(None, wraps)],
                None,
            ),
        )
    )

    pages.append(
        (
            "nargile.html",
            note_only_page(
                "nargile.html",
                "Nargile",
                "assets/nargile.png",
                "Tütün ve aromalı seçenekler masa başında güncellenir. "
                "Fiyat ve markalar için lütfen garsona sorun.",
            ),
        )
    )

    soguk_sections: list[tuple[str | None, list[tuple[str, str]]]] = [
        (
            "Gazlı & soğuk içecekler",
            [
                ("Su", "50 ₺"),
                ("Sade soda", "70 ₺"),
                ("Coca Cola", "100 ₺"),
                ("Churchill", "110 ₺"),
                ("Sprite", "100 ₺"),
                ("Cappy", "100 ₺"),
                ("Fanta", "100 ₺"),
                ("Fuse Tea", "100 ₺"),
                ("Cola Zero", "100 ₺"),
                ("Ayran", "100 ₺"),
                ("Şişe Cola", "100 ₺"),
                ("Meyveli soda", "100 ₺"),
                ("Redbull", "160 ₺"),
                ("Şalgam", "90 ₺"),
                ("Çilekli limonata", "220 ₺"),
                ("El yapımı limonata", "200 ₺"),
                ("Redbull kokteyl", "350 ₺"),
            ],
        ),
        (
            "Taze meyve suları",
            [
                ("Portakal suyu", "200 ₺"),
                ("Nar portakal", "230 ₺"),
                ("Nar suyu", "220 ₺"),
                ("Limonata", "200 ₺"),
            ],
        ),
        (
            "Milkshake",
            [
                ("Karamelli milkshake", "180 ₺"),
                ("Çikolatalı milkshake", "180 ₺"),
                ("Çilekli milkshake", "180 ₺"),
                ("Muzlu milkshake", "180 ₺"),
                ("Vanilyalı milkshake", "180 ₺"),
                ("Ahududu milkshake", "180 ₺"),
                ("Babylon special milkshake", "200 ₺"),
                ("Oreolu milkshake", "190 ₺"),
            ],
        ),
        (
            "Frozen",
            [
                ("Çilekli frozen", "170 ₺"),
                ("Karpuz çilek frozen", "170 ₺"),
                ("Kavun frozen", "170 ₺"),
                ("Böğürtlen frozen", "200 ₺"),
                ("Yaban mersini frozen", "200 ₺"),
                ("Frambuaz frozen", "200 ₺"),
                ("Ananas frozen", "185 ₺"),
                ("Mango frozen", "185 ₺"),
                ("Orman meyveli frozen", "185 ₺"),
            ],
        ),
        (
            "Frappe",
            [
                ("Çilekli frappe", "170 ₺"),
                ("Çikolatalı frappe", "170 ₺"),
                ("Fıstıklı frappe", "190 ₺"),
                ("Kavunlu frappe", "170 ₺"),
                ("Oreo frappe", "190 ₺"),
            ],
        ),
        (
            "Babylon kokteyller",
            [
                ("Babylon Rosalinda", "350 ₺"),
                ("Babylon Coco Melon", "200 ₺"),
                ("Tropik esinti", "200 ₺"),
                ("Babylon White Angel", "260 ₺"),
                ("Magic of Green", "260 ₺"),
                ("Bubble Paradise", "200 ₺"),
                ("Gökkuşağı punch", "240 ₺"),
            ],
        ),
        (
            "Smoothie",
            [
                ("Böğürtlen smoothie", "200 ₺"),
                ("Frambuaz smoothie", "200 ₺"),
                ("Orman meyveli smoothie", "190 ₺"),
                ("Çilekli smoothie", "190 ₺"),
                ("Vanilyalı smoothie", "190 ₺"),
                ("Mango smoothie", "190 ₺"),
                ("Ananas smoothie", "190 ₺"),
                ("Karadut smoothie", "190 ₺"),
            ],
        ),
    ]
    pages.append(
        (
            "soguk-icecekler.html",
            build_page(
                "soguk-icecekler.html",
                "Soğuk içecekler",
                "assets/soguk-icecekler.png",
                "soguk-icecekler",
                "Tüm alt gruplar için fotoğraflar tek klasörde: assets/soguk-icecekler/item-01.jpg … item-58.jpg (sayfa yukarıdan aşağı sırayla).",
                soguk_sections,
            ),
        )
    )

    sicak_sections: list[tuple[str | None, list[tuple[str, str]]]] = [
        (
            "Çay & bitki çayları",
            [
                ("Çay", "40 ₺"),
                ("Fincan çay", "80 ₺"),
                ("Yeşil çay", "150 ₺"),
                ("Ballı süt", "150 ₺"),
                ("Nane limon", "150 ₺"),
                ("Elma tarçın", "150 ₺"),
                ("Kuşburnu", "150 ₺"),
                ("Ihlamur", "170 ₺"),
                ("Papatya çayı", "150 ₺"),
                ("Kış çayı", "170 ₺"),
                ("Kaçak çay", "45 ₺"),
                ("Ada çayı", "150 ₺"),
            ],
        ),
        (
            "Filtre kahveler",
            [
                ("Sade filtre kahve", "140 ₺"),
                ("Sütlü filtre kahve", "150 ₺"),
                ("Aromalı filtre kahve", "150 ₺"),
            ],
        ),
        (
            "Kahveler",
            [
                ("Türk kahvesi", "120 ₺"),
                ("Doble Türk kahvesi", "150 ₺"),
                ("Tarzı hususi", "140 ₺"),
                ("Damla sakızlı Türk kahvesi", "150 ₺"),
                ("Dağ çilekli Türk kahvesi", "135 ₺"),
                ("Osmanlı dibek kahvesi", "120 ₺"),
                ("Menengiç kahvesi", "140 ₺"),
                ("Sütlü Türk kahvesi", "160 ₺"),
                ("Türk kahvesi sade", "120 ₺"),
                ("Türk kahvesi şekerli", "120 ₺"),
                ("Tarzı hususi orta", "140 ₺"),
                ("Tarzı hususi şekerli", "140 ₺"),
            ],
        ),
    ]
    pages.append(
        (
            "sicak-icecekler.html",
            build_page(
                "sicak-icecekler.html",
                "Sıcak içecekler",
                "assets/sicak-icecekler.png",
                "sicak-icecekler",
                "Fotoğraflar: assets/sicak-icecekler/item-01.jpg … item-27.jpg (çaylar, filtre, kahve sırasıyla).",
                sicak_sections,
            ),
        )
    )

    for fname, html in pages:
        (ROOT / fname).write_text(html, encoding="utf-8")
        print("Wrote", fname)

    # Create empty asset folders for uploads
    for d in (
        "makarnalar",
        "ev-yemekleri",
        "hamburger",
        "pizza",
        "tost-cesitleri",
        "soguk-icecekler",
        "sicak-icecekler",
    ):
        p = ROOT / "assets" / d
        p.mkdir(parents=True, exist_ok=True)
    print("Done.")


if __name__ == "__main__":
    main()
