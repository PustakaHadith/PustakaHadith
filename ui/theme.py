"""Tema PustakaHadith — diselaraskan dengan gaya hadis.my.

Perubahan berbanding tema lama:
  • Kad hadis: nombor + petikan Arab + petikan Melayu, "Baca →" di kanan
  • Sempadan lembut, jejari 12px, hover teal halus
  • Chip kitab mendatar (macam bar penapis hadis.my)
  • Skala jenis konsisten, tiada nilai px bertaburan
"""

from __future__ import annotations

# ── Palet ──────────────────────────────────────────────────────────────
# Dua set warna. `apply_theme()` menyalin set yang dipilih ke dalam
# ruang nama SETIAP modul UI — perlu kerana `from theme import CARD_BG`
# mengikat nilai pada masa import, jadi mutate ui.theme sahaja TIDAK cukup.

# Palet KERTAS HANGAT mockup (Sesi 55, DITERIMA PAKAI 12 Ogos 2026 —
# sebelum ini DITOLAK kerana teks sekunder terang gagal AA; sekarang
# hue hangat mockup diambil, tetapi teks sekunder/kapsyen digelapkan
# sedikit supaya kekal AA — lihat rekod Sesi 55). Aksen hijau mockup
# (bukan TEAL) — konsisten dengan breadcrumb/bar-bawah mockup.
# Malam 14 Ogos: TEXT_MUTED/FAINT dinaikkan supaya SEMUA tier teks
# ≥ 4.5:1 (WCAG AA) pada permukaan — dikunci semak kontras (13).
DARK = {
    "PAGE_BG": "#1E1D1A", "SURFACE": "#1E1D1A",
    "CARD_BG": "#282721", "CARD_BG_HOVER": "#2F2E28",
    "HEADER_BG": "#23221D",

    "TEAL": "#5CBF85", "TEAL_LIGHT": "#7FD39A", "TEAL_PALE": "#2A3B2F",
    "TEAL_DARK": "#0F2417", "TEAL_GLOW": "#3A6B4A",

    "TEXT_PRIMARY": "#E8E4DA", "TEXT_SECONDARY": "#A39C8C",
    "TEXT_MUTED": "#9C9589", "TEXT_FAINT": "#928D80",

    "BORDER": "#3B3932", "BORDER_LIGHT": "#4A473E",

    "AMBER_BG": "#3A3120", "AMBER_BORDER": "#5C5030", "AMBER_TEXT": "#E0B35C",
    "RED_BG": "#3B2523", "RED_BORDER": "#5C3A42", "RED_TEXT": "#E08A80",
    "GREEN_BG": "#2A3B2F", "GREEN_BORDER": "#3D5540", "GREEN_TEXT": "#7FD39A",
    "WA_GREEN": "#25D366", "WA_GREEN_DARK": "#1DA851",
    # Kunci panel kaca (Split Command Center, 25 Ogos): tema bukan-AQUA
    # tiada latar imej, jadi panel = permukaan pepejal biasa.
    "PANEL_BG": "#282721", "BORDER_GLASS": "#3B3932",
}

# Palet NEUTRAL (lalai, malam 14 Ogos 2026) — gelap neutral gaya
# Windows: permukaan kelabu tulen, teks putih penuh, tiada hue hangat.
# Keputusan pengguna untuk pengguna awam: kontras tinggi + biasa dilihat
# (Windows/telefon mod gelap). TEAL hijau kekal sebagai aksen jenama;
# warna cip semantik sama dengan kertas. Semua tier teks ≥ 4.5:1.
NEUTRAL = {
    "PAGE_BG": "#1F1F1F", "SURFACE": "#1F1F1F",
    "CARD_BG": "#252526", "CARD_BG_HOVER": "#2D2D2D",
    "HEADER_BG": "#232324",

    "TEAL": "#5CBF85", "TEAL_LIGHT": "#7FD39A", "TEAL_PALE": "#2A3B2F",
    "TEAL_DARK": "#0F2417", "TEAL_GLOW": "#3A6B4A",

    "TEXT_PRIMARY": "#FFFFFF", "TEXT_SECONDARY": "#C6C6C6",
    "TEXT_MUTED": "#9C9C9C", "TEXT_FAINT": "#8E8E8E",

    "BORDER": "#3B3B3B", "BORDER_LIGHT": "#4A4A4A",

    "AMBER_BG": "#3A3120", "AMBER_BORDER": "#5C5030", "AMBER_TEXT": "#E0B35C",
    "RED_BG": "#3B2523", "RED_BORDER": "#5C3A42", "RED_TEXT": "#E08A80",
    "GREEN_BG": "#2A3B2F", "GREEN_BORDER": "#3D5540", "GREEN_TEXT": "#7FD39A",
    "WA_GREEN": "#25D366", "WA_GREEN_DARK": "#1DA851",
    "PANEL_BG": "#252526", "BORDER_GLASS": "#3B3B3B",
}

# Palet NEUTRAL TERANG (malam 14 Ogos 2026) — pasangan terang kepada
# NEUTRAL: permukaan kelabu/putih tulen, teks hitam neutral, TIADA hue
# hangat. Untuk pengguna mod terang yang mahu kontras sama dengan
# Neutral gelap. Semua tier teks ≥ 4.5:1 (paling ketat FAINT pada
# HEADER_BG 4.51:1) — dikunci semak kontras (13).
LIGHT_NEUTRAL = {
    "PAGE_BG": "#F4F4F4", "SURFACE": "#F4F4F4",
    "CARD_BG": "#FFFFFF", "CARD_BG_HOVER": "#F6F6F6",
    "HEADER_BG": "#ECECEC",

    "TEAL": "#1A6B3C", "TEAL_LIGHT": "#2D7A4A", "TEAL_PALE": "#E9F2EA",
    "TEAL_DARK": "#123F24", "TEAL_GLOW": "#7FBC92",

    "TEXT_PRIMARY": "#1A1A1A", "TEXT_SECONDARY": "#444444",
    "TEXT_MUTED": "#595959", "TEXT_FAINT": "#6B6B6B",

    "BORDER": "#D9D9D9", "BORDER_LIGHT": "#C4C4C4",

    "AMBER_BG": "#FDF3E0", "AMBER_BORDER": "#E0C88A", "AMBER_TEXT": "#965A00",
    "RED_BG": "#FDEAEA", "RED_BORDER": "#EAB4AE", "RED_TEXT": "#B3261E",
    "GREEN_BG": "#E9F2EA", "GREEN_BORDER": "#B7D4BD", "GREEN_TEXT": "#1A6B3C",
    "WA_GREEN": "#25D366", "WA_GREEN_DARK": "#1DA851",
    "PANEL_BG": "#FFFFFF", "BORDER_GLASS": "#D9D9D9",
}

# Tema terang — palet kertas hangat mockup. Teks utama mockup #2B2B2B
# kekal; sekunder/kapsyen mockup (#7A7468/#9A937F) GAGAL AA (4.11/2.72)
# jadi digelapkan kepada #5F594D/#6E685A (6.16/4.91) — hue hangat sama,
# kontras cukup. Faint kekal pucat mengikut reka bentuk.
LIGHT = {
    "PAGE_BG": "#F4F1EA", "SURFACE": "#F4F1EA",
    "CARD_BG": "#FFFFFF", "CARD_BG_HOVER": "#FAF8F2",
    "HEADER_BG": "#FDFCF8",

    "TEAL": "#1A6B3C", "TEAL_LIGHT": "#2D7A4A", "TEAL_PALE": "#E9F2EA",
    "TEAL_DARK": "#123F24", "TEAL_GLOW": "#7FBC92",

    "TEXT_PRIMARY": "#2B2B2B", "TEXT_SECONDARY": "#5F594D",
    "TEXT_MUTED": "#6E685A", "TEXT_FAINT": "#6D6858",

    # BORDER gelap sedikit supaya garis 1px (divider, kad, kotak input)
    # jelas kelihatan atas kertas — #E4DFD3 kad, #CFC8B8 butang.
    "BORDER": "#E4DFD3", "BORDER_LIGHT": "#CFC8B8",

    "AMBER_BG": "#FDF3E0", "AMBER_BORDER": "#E0C88A", "AMBER_TEXT": "#965A00",
    "RED_BG": "#FDEAEA", "RED_BORDER": "#EAB4AE", "RED_TEXT": "#B3261E",
    "GREEN_BG": "#E9F2EA", "GREEN_BORDER": "#B7D4BD", "GREEN_TEXT": "#1A6B3C",
    "WA_GREEN": "#25D366", "WA_GREEN_DARK": "#1DA851",
    "PANEL_BG": "#FFFFFF", "BORDER_GLASS": "#E4DFD3",
}

# Palet AQUA (25 Ogos 2026, keputusan UI/UX PustakaHadith) — tema ke-5,
# identiti baharu yang BEBAS daripada gaya hadis.my. Latar globe/jaringan
# dilukis oleh ui.widgets.BackgroundCanvas HANYA bila tema ini aktif;
# panel kaca (QFrame#glassPanel) menggunakan alpha sebenar 20/255 tanpa
# blur (SELECTED_UIUX.md). Semua tier teks >= 4.5:1 (dikira WCAG):
# TEXT_PRIMARY #EAF6F6 / PAGE_BG #0A1520 = 15.9:1; TEXT_SECONDARY 9.5:1;
# TEXT_MUTED 6.8:1; TEXT_FAINT 5.6:1. Atas CARD_BG #10222F (panel/kad):
# PRIMARY 14.7:1; MUTED 6.0:1; FAINT 4.9:1; TEAL 7.9:1 — semua lulus AA.
AQUA = {
    "PAGE_BG": "#0A1520", "SURFACE": "#0A1520",
    "CARD_BG": "#10222F", "CARD_BG_HOVER": "#16303F",
    "HEADER_BG": "#0C1A26",

    "TEAL": "#3EC9B0", "TEAL_LIGHT": "#6FDCC8", "TEAL_PALE": "#123A38",
    "TEAL_DARK": "#06251F", "TEAL_GLOW": "#1F6B5C",

    "TEXT_PRIMARY": "#EAF6F6", "TEXT_SECONDARY": "#9FBFCB",
    "TEXT_MUTED": "#7FA3B0", "TEXT_FAINT": "#6E93A1",

    "BORDER": "#1D3A4A", "BORDER_LIGHT": "#274B5E",

    # Panel kaca — alpha sebenar 20/255 (8%), tanpa blur. Border kaca
    # teal halus alpha 60/255.
    "PANEL_BG": "rgba(13, 42, 60, 20)", "BORDER_GLASS": "rgba(62, 201, 176, 60)",

    "AMBER_BG": "#3A3120", "AMBER_BORDER": "#5C5030", "AMBER_TEXT": "#E0B35C",
    "RED_BG": "#3B2523", "RED_BORDER": "#5C3A42", "RED_TEXT": "#E08A80",
    "GREEN_BG": "#123A38", "GREEN_BORDER": "#1F6B5C", "GREEN_TEXT": "#3EC9B0",
    "WA_GREEN": "#25D366", "WA_GREEN_DARK": "#1DA851",
}

THEMES = {"light": LIGHT, "dark": DARK, "neutral": NEUTRAL,
          "lightneutral": LIGHT_NEUTRAL, "aqua": AQUA}
CURRENT_THEME = "dark"

# Tema lalai pengguna BAHARU (25 Ogos): AQUA — identiti baharu. Dipakai
# oleh app_qt (PustakaApp) dan settings_panel (pemilih tema). Pengguna
# sedia ada yang telah memilih tema kekal tema mereka (kunci "theme"
# tersimpan dalam user_settings.json).
DEFAULT_TEMA = "aqua"

# Kunci "sistem" — bukan palet, tetapi mod yang mengikuti mod gelap
# Windows. Bukan dalam THEMES supaya ia tidak dilayan sebagai palet;
# `tema_efektif()` menyelesaikannya kepada palet sebenar.
KUNCI_SISTEM = "sistem"


def windows_gelap() -> bool:
    """True jika Windows dalam mod gelap (AppsUseLightTheme = 0).

    Baca registry HKCU ... Themes Personalize (AppsUseLightTheme).
    Jika gagal (bukan Windows / tiada kunci / ralat lain) lalai kepada
    gelap — supaya app tidak pernah memilih terang secara tidak
    sengaja pada sistem yang tidak dapat dibaca. Dipanggil oleh
    `tema_efektif()`.
    """
    try:
        import winreg
        k = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize")
        try:
            v, _ = winreg.QueryValueEx(k, "AppsUseLightTheme")
        finally:
            k.Close()
        return int(v) == 0
    except Exception:
        return True


def tema_efektif(kunci: str) -> str:
    """Kunci tema pengguna -> nama palet SEBENAR.

    "sistem" diselesaikan kepada "neutral" (Windows gelap) atau
    "lightneutral" (Windows terang); kunci lain dipulangkan jika sah
    (kekal dalam THEMES), selain itu lalai "neutral".
    """
    if kunci == KUNCI_SISTEM:
        return "neutral" if windows_gelap() else "lightneutral"
    return kunci if kunci in THEMES else "neutral"

# Modul yang mengimport warna secara terus — mesti dikemas kini bersama.
_THEMED_MODULES = ("ui.theme", "ui.widgets", "ui.pages",
                   "ui.app_qt", "ui.settings_panel", "ui.splash",
                   "ui.pages_kitab", "ui.pages_carian",
                   "ui.pages_detail", "ui.pages_tersimpan",
                   "ui.pages_tetapan", "ui.pages_home",
                   "ui.pages_rak", "ui.deklarasi")


def apply_theme(name: str = "dark") -> dict:
    """Tukar palet aktif. Pulangkan dict warna yang digunakan.

    Menyalin setiap warna ke dalam ruang nama semua modul UI supaya
    `from theme import CARD_BG` yang sedia ada menunjuk nilai baharu.
    """
    import sys as _sys
    global CURRENT_THEME
    name = tema_efektif(name)   # "sistem" -> neutral/lightneutral
    pal = THEMES.get(name, DARK)
    CURRENT_THEME = name if name in THEMES else "dark"

    for mod_name in _THEMED_MODULES:
        mod = _sys.modules.get(mod_name)
        if mod is None:
            continue
        for k, v in pal.items():
            setattr(mod, k, v)
        setattr(mod, "BORDER_FOCUS", pal["TEAL"])
    return pal


def is_dark() -> bool:
    return CURRENT_THEME in ("dark", "neutral", "aqua")


def ada_latar_imej() -> bool:
    """True jika tema aktif melukis latar imej (glob) pada BackgroundCanvas.

    Dipanggil oleh ui.widgets.BackgroundCanvas dan halaman utama (untuk
    memutuskan ketelusan viewport). Tema lain = permukaan pepejal QSS.
    """
    return CURRENT_THEME == "aqua"


# ── Palet (kertas hangat mockup) ─────────────────────────────────────
PAGE_BG        = "#1E1D1A"
SURFACE        = "#1E1D1A"
CARD_BG        = "#282721"
CARD_BG_HOVER  = "#2F2E28"
HEADER_BG      = "#23221D"

TEAL           = "#5CBF85"
TEAL_LIGHT     = "#7FD39A"
TEAL_PALE      = "#2A3B2F"
TEAL_DARK      = "#0F2417"
TEAL_GLOW      = "#3A6B4A"

TEXT_PRIMARY   = "#E8E4DA"
TEXT_SECONDARY = "#A39C8C"
TEXT_MUTED     = "#9C9589"
TEXT_FAINT     = "#928D80"

BORDER         = "#3B3932"
BORDER_LIGHT   = "#4A473E"
BORDER_FOCUS   = TEAL

AMBER_BG       = "#3A3120"
AMBER_BORDER   = "#5C5030"
AMBER_TEXT     = "#E0B35C"

RED_BG         = "#3B2523"
RED_BORDER     = "#5C3A42"
RED_TEXT       = "#E08A80"

GREEN_BG       = "#2A3B2F"
GREEN_BORDER   = "#3D5540"
GREEN_TEXT     = "#7FD39A"

# ── Metrik ─────────────────────────────────────────────────────────────
HEADER_HEIGHT  = 60
CONTENT_MAX_W  = 1080      # lebar kandungan berpusat, macam hadis.my
GUTTER         = 32
RADIUS         = 12
RADIUS_SM      = 8

FONT_SCALES = [0.85, 1.0, 1.15, 1.3, 1.5]
FONT_SCALE_LABELS = ["Kecil", "Sederhana", "Besar", "Besar+", "Besar++"]

# Calon fon Arab, ikut keutamaan. Yang TIDAK dipasang akan ditapis oleh
# available_arabic_fonts() — Qt menggantikan fon hilang secara SENYAP, jadi
# tanpa penapisan pengguna menyangka pemilih fon rosak.
ARABIC_FONT_CANDIDATES = [
    "KFGQPC Uthmanic Script HAFS",
    "KFGQPC HAFS Uthmanic Script",
    "Scheherazade New",
    "Scheherazade",
    "Amiri",
    "Amiri Quran",
    "Noto Naskh Arabic",
    "Traditional Arabic",
    "Simplified Arabic",
    "Arabic Typesetting",
    "Segoe UI",
]

_ARABIC_CACHE: list | None = None


def available_arabic_fonts() -> list:
    """Fon Arab yang BENAR-BENAR dipasang pada sistem ini.

    Memerlukan QApplication wujud. Jika tiada satu pun calon dijumpai,
    pulangkan fon lalai sistem supaya UI tetap berfungsi.
    """
    global _ARABIC_CACHE
    if _ARABIC_CACHE is not None:
        return _ARABIC_CACHE
    try:
        from PyQt5.QtGui import QFontDatabase
        fams = set(QFontDatabase().families())
        found = [f for f in ARABIC_FONT_CANDIDATES if f in fams]
        if not found:
            # Cari apa-apa fon yang menyokong tulisan Arab
            db = QFontDatabase()
            found = [f for f in db.families(QFontDatabase.Arabic)][:6]
        _ARABIC_CACHE = found or ["Sans Serif"]
    except Exception:
        _ARABIC_CACHE = list(ARABIC_FONT_CANDIDATES)
    return _ARABIC_CACHE


def default_arabic_font() -> str:
    return available_arabic_fonts()[0]


def font_installed(name: str) -> bool:
    try:
        from PyQt5.QtGui import QFontDatabase
        return name in set(QFontDatabase().families())
    except Exception:
        return True


# Keserasian ke belakang — modul lama mengimport ARABIC_FONTS
ARABIC_FONTS = ARABIC_FONT_CANDIDATES

UI_FONT = "Segoe UI"

COLLECTION_META = {
    "bukhari":    {"name": "Sahih al-Bukhari", "short": "Bukhari", "icon": "📘", "author": "Imam al-Bukhari",
                   "desc": "Hadis sahih oleh Imam al-Bukhari.",
                   "arabic": "صحيح البخاري", "warna": "#2E7D6B"},
    "muslim":     {"name": "Sahih Muslim", "short": "Muslim",    "icon": "📕", "author": "Imam Muslim",
                   "desc": "Hadis sahih oleh Imam Muslim.",
                   "arabic": "صحيح مسلم", "warna": "#2E5D8C"},
    "abu-daud":   {"name": "Sunan Abu Daud", "short": "Abu Daud",  "icon": "📙", "author": "Imam Abu Daud",
                   "desc": "Kompilasi hadis oleh Imam Abu Daud.",
                   "arabic": "سنن أبي داود", "warna": "#A96B2F"},
    "tirmidzi":   {"name": "Jami At-Tirmidzi", "short": "Tirmidzi","icon": "📗", "author": "Imam Tirmidzi",
                   "desc": "Kompilasi hadis oleh Imam Tirmidzi.",
                   "arabic": "جامع الترمذي", "warna": "#8C3A4A"},
    "nasai":      {"name": "Sunan An-Nasai", "short": "An-Nasai",  "icon": "📒", "author": "Imam An-Nasai",
                   "desc": "Kompilasi hadis oleh Imam An-Nasai.",
                   "arabic": "سنن النسائي", "warna": "#6B4E8C"},
    "ibnu-majah": {"name": "Sunan Ibnu Majah", "short": "Ibnu Majah","icon": "📔", "author": "Imam Ibnu Majah",
                   "desc": "Kompilasi hadis oleh Imam Ibnu Majah.",
                   "arabic": "سنن ابن ماجه", "warna": "#A08A2E"},
    "malik":      {"name": "Muwatta' Malik", "short": "Malik",  "icon": "📓", "author": "Imam Malik bin Anas",
                   "desc": "Hadis dan fatwa oleh Imam Malik.",
                   "arabic": "موطأ مالك", "warna": "#3A4A6B"},
    "ahmad":      {"name": "Musnad Ahmad", "short": "Ahmad",    "icon": "📚", "author": "Imam Ahmad bin Hanbal",
                   "desc": "Hadis oleh Imam Ahmad bin Hanbal.",
                   "arabic": "مسند أحمد", "warna": "#3F6B3A"},
    "darimi":     {"name": "Musnad Darimi", "short": "Darimi",   "icon": "📕", "author": "Imam ad-Darimi",
                   "desc": "Kompilasi hadis oleh Imam ad-Darimi.",
                   "arabic": "سنن الدارمي", "warna": "#4E6B7A"},
}


def build_qss(scale: float = 1.0) -> str:
    """Jana QSS untuk tema AKTIF.

    Warna dibaca dari THEMES[CURRENT_THEME], bukan dari pemalar modul —
    supaya fungsi ini sentiasa mencerminkan tema semasa walaupun
    dipanggil selepas apply_theme().
    """
    def s(px: float) -> str:
        return f"{max(1, int(px * scale))}px"

    _p = THEMES.get(CURRENT_THEME, DARK)
    PAGE_BG = _p["PAGE_BG"]; SURFACE = _p["SURFACE"]
    CARD_BG = _p["CARD_BG"]; CARD_BG_HOVER = _p["CARD_BG_HOVER"]
    HEADER_BG = _p["HEADER_BG"]
    TEAL = _p["TEAL"]; TEAL_LIGHT = _p["TEAL_LIGHT"]
    TEAL_PALE = _p["TEAL_PALE"]; TEAL_DARK = _p["TEAL_DARK"]
    TEAL_GLOW = _p["TEAL_GLOW"]
    TEXT_PRIMARY = _p["TEXT_PRIMARY"]; TEXT_SECONDARY = _p["TEXT_SECONDARY"]
    TEXT_MUTED = _p["TEXT_MUTED"]; TEXT_FAINT = _p["TEXT_FAINT"]
    BORDER = _p["BORDER"]; BORDER_LIGHT = _p["BORDER_LIGHT"]
    BORDER_FOCUS = _p["TEAL"]

    return f"""
* {{ outline: none; }}

QMainWindow, QWidget#page, QScrollArea {{
    background-color: {PAGE_BG};
    color: {TEXT_PRIMARY};
    font-family: "{UI_FONT}";
}}
QWidget {{ color: {TEXT_PRIMARY}; font-family: "{UI_FONT}"; }}

QLabel            {{ background: transparent; border: none; }}
QLabel#h1         {{ font-size: {s(30)}; font-weight: 700; color: {TEXT_PRIMARY}; }}
QLabel#h2         {{ font-size: {s(21)}; font-weight: 700; color: {TEXT_PRIMARY}; }}
QLabel#h3         {{ font-size: {s(15)}; font-weight: 600; color: {TEXT_PRIMARY}; }}
QLabel#body       {{ font-size: {s(13)}; color: {TEXT_SECONDARY}; }}
QLabel#muted      {{ font-size: {s(12)}; color: {TEXT_MUTED}; }}
QLabel#faint      {{ font-size: {s(11)}; color: {TEXT_FAINT}; }}
QLabel#teal       {{ font-size: {s(13)}; color: {TEAL}; font-weight: 600; }}
QLabel#quote      {{ font-size: {s(13)}; color: {TEXT_MUTED}; font-style: italic; }}

/* Label nombor hadis — "No. 1" */
QLabel#hadisNo {{
    font-size: {s(11)}; font-weight: 700; color: {TEXT_MUTED};
    letter-spacing: 0.5px;
}}
/* Nama bab hadis (Fasa 3) */
QLabel#babName {{
    font-size: {s(11)}; font-weight: 500; color: {TEXT_MUTED};
    font-style: italic;
}}
QLabel#bacaLink {{ font-size: {s(12)}; font-weight: 600; color: {TEAL}; }}

/* Chip kitab */
QLabel#chip {{
    background-color: {TEAL_PALE}; color: {TEAL};
    font-size: {s(10)}; font-weight: 700;
    padding: {s(3)} {s(10)}; border-radius: {s(10)};
}}

QTextBrowser {{
    background: transparent; color: {TEXT_PRIMARY};
    border: none; selection-background-color: {TEAL_PALE};
}}

QLineEdit {{
    background-color: {CARD_BG}; color: {TEXT_PRIMARY};
    border: 1px solid {BORDER}; border-radius: {s(RADIUS_SM)};
    padding: {s(10)} {s(14)}; font-size: {s(14)};
}}
QLineEdit:focus {{ border: 1px solid {BORDER_FOCUS}; background-color: {CARD_BG_HOVER}; }}
QLineEdit::placeholder {{ color: {TEXT_FAINT}; }}

QPushButton {{
    background-color: {CARD_BG}; color: {TEXT_SECONDARY};
    border: 1px solid {BORDER}; border-radius: {s(RADIUS_SM)};
    padding: {s(8)} {s(18)}; font-size: {s(12)}; font-weight: 600;
}}
QPushButton:hover  {{ background-color: {CARD_BG_HOVER}; border-color: {TEAL_GLOW}; color: {TEXT_PRIMARY}; }}
QPushButton:pressed{{ background-color: {TEAL_DARK}; }}
QPushButton:disabled {{ color: {TEXT_FAINT}; border-color: {BORDER}; }}

QPushButton#primary {{
    background-color: {TEAL}; color: {PAGE_BG};
    border: none; font-weight: 700; padding: {s(10)} {s(24)}; font-size: {s(13)};
}}
QPushButton#primary:hover   {{ background-color: {TEAL_LIGHT}; }}
QPushButton#primary:pressed {{ background-color: {TEAL_GLOW}; }}

QPushButton#nav {{
    background: transparent; border: none; color: {TEXT_MUTED};
    padding: {s(8)} {s(14)}; font-size: {s(13)}; font-weight: 500;
    border-radius: {s(6)};
}}
QPushButton#nav:hover {{ color: {TEAL}; background-color: {TEAL_PALE}; }}

QPushButton#nav_active {{
    background: transparent; border: none; color: {TEAL};
    padding: {s(8)} {s(14)}; font-size: {s(13)}; font-weight: 700;
    border-bottom: 2px solid {TEAL}; border-radius: 0;
}}

/* Chip penapis kitab — bar mendatar seperti hadis.my */
QPushButton#filterChip {{
    background-color: {CARD_BG}; color: {TEXT_MUTED};
    border: 1px solid {BORDER}; border-radius: {s(4)};
    padding: {s(6)} {s(12)}; font-size: {s(12)}; font-weight: 600;
}}
QPushButton#filterChip:hover {{ border-color: {TEAL_GLOW}; color: {TEXT_PRIMARY}; }}
QPushButton#filterChip_active {{
    background-color: {TEAL}; color: #ffffff;
    border: 1px solid {TEAL_GLOW}; border-radius: {s(4)};
    padding: {s(6)} {s(12)}; font-size: {s(12)}; font-weight: 700;
}}

QPushButton#ghost {{
    background: transparent; border: 1px solid {BORDER};
    color: {TEXT_MUTED}; padding: {s(6)} {s(12)}; font-size: {s(11)};
}}
QPushButton#ghost:hover {{ color: {TEAL}; border-color: {TEAL_GLOW}; }}

/* Tajuk bahagian boleh kembang — sengaja rendah kontras supaya tidak
   menarik perhatian orang awam, tetapi mudah dijumpai bila dicari. */
QPushButton#collapse {{
    background: transparent; border: none; text-align: left;
    color: {TEXT_MUTED}; padding: {s(7)} {s(4)};
    font-size: {s(11)}; font-weight: 600;
}}
QPushButton#collapse:hover {{ color: {TEAL}; }}

QPushButton#stepper {{
    background: transparent; border: 1px solid {BORDER};
    color: {TEXT_MUTED}; border-radius: {s(5)};
    padding: 0; font-size: {s(13)}; font-weight: 700;
    min-width: {s(24)}; max-width: {s(24)}; min-height: {s(24)};
}}
QPushButton#stepper:hover {{ color: {TEAL}; border-color: {TEAL}; }}

QComboBox {{
    background-color: {CARD_BG}; color: {TEXT_PRIMARY};
    border: 1px solid {BORDER}; border-radius: {s(RADIUS_SM)};
    padding: {s(8)} {s(12)}; font-size: {s(12)};
}}
QComboBox:hover  {{ border-color: {TEAL_GLOW}; }}
QComboBox:focus  {{ border-color: {BORDER_FOCUS}; }}
QComboBox::drop-down {{ border: none; width: {s(22)}; }}
QComboBox QAbstractItemView {{
    background-color: {CARD_BG}; color: {TEXT_PRIMARY};
    border: 1px solid {BORDER_LIGHT}; border-radius: {s(6)};
    selection-background-color: {TEAL_PALE}; selection-color: {TEAL};
    padding: {s(4)};
}}

/* Menu konteks — WAJIB global.
   Tanpa ini, mana-mana menu terbina Qt (QLineEdit, QTextEdit) muncul
   sebagai kotak PUTIH sistem dengan teks putih = tidak terbaca. */
QMenu {{
    background-color: {CARD_BG}; color: {TEXT_PRIMARY};
    border: 1px solid {BORDER}; border-radius: {s(6)};
    padding: {s(5)}; font-size: {s(12)};
}}
QMenu::item {{
    padding: {s(7)} {s(26)} {s(7)} {s(14)};
    border-radius: {s(4)}; color: {TEXT_PRIMARY};
}}
QMenu::item:selected {{ background-color: {TEAL_PALE}; color: {TEAL}; }}
QMenu::item:disabled {{ color: {TEXT_FAINT}; }}
QMenu::separator {{ height: 1px; background: {BORDER}; margin: {s(5)} {s(10)}; }}

QToolTip {{
    background-color: {CARD_BG}; color: {TEXT_PRIMARY};
    border: 1px solid {BORDER}; border-radius: {s(4)};
    padding: {s(5)} {s(8)}; font-size: {s(11)};
}}

QScrollBar:vertical {{ background: transparent; width: {s(10)}; margin: 0; }}
QScrollBar::handle:vertical {{
    background: {BORDER_LIGHT}; border-radius: {s(5)}; min-height: {s(40)};
}}
QScrollBar::handle:vertical:hover {{ background: {TEXT_FAINT}; }}
QScrollBar::add-line, QScrollBar::sub-line {{ height: 0; width: 0; }}
QScrollBar::add-page, QScrollBar::sub-page {{ background: transparent; }}

/* Kad hadis */
QFrame#card {{
    background-color: {CARD_BG};
    border: 1px solid {BORDER};
    border-radius: {s(RADIUS)};
}}
QFrame#card:hover {{
    background-color: {CARD_BG_HOVER};
    border: 1px solid {TEAL};
}}
QFrame#panel {{
    background-color: {CARD_BG};
    border: 1px solid {BORDER};
    border-radius: {s(RADIUS)};
}}
QFrame#hero {{ background-color: {HEADER_BG}; border: none; }}
/* Bar tetap di bawah halaman huraian -- di luar kawasan skrol supaya
   butang Kembali sentiasa kelihatan. */
QFrame#bottombar {{
    background-color: {HEADER_BG};
    border: none; border-top: 1px solid {BORDER};
}}

/* Butang terapung "ke atas" — senarai hadis (Sesi 34). Bulat, di
   sudut kanan bawah viewport; kelihatan hanya bila pengguna skrol
   ke bawah. Styling di sini (bukan inline) supaya pages_kitab.py
   kekal bebas import warna. */
QPushButton#backTop {{
    background-color: {CARD_BG}; color: {TEAL};
    border: 1px solid {BORDER}; border-radius: {s(22)};
    font-size: {s(18)}; font-weight: 700;
}}
QPushButton#backTop:hover   {{ background-color: {CARD_BG_HOVER}; border-color: {TEAL_GLOW}; }}
QPushButton#backTop:pressed {{ background-color: {TEAL_DARK}; }}

QFrame#divider {{ background-color: {BORDER}; border: none; max-height: 2px; }}

/* ── Halaman Utama Split Command Center (25 Ogos 2026) ─────────────
   PANEL_BG/BORDER_GLASS: AQUA = rgba kaca alpha 20/255 (kelihatan
   latar glob di belakang); tema lain = permukaan pepejal biasa.
   Halaman utama (scroll + viewport + body) TELUS supaya latar
   BackgroundCanvas kelihatan — hanya pada halaman ini. */
QFrame#glassPanel {{
    background-color: {PANEL_BG};
    border: 1px solid {BORDER_GLASS};
    border-radius: {s(14)};
}}
QScrollArea#homeScroll, QWidget#homeBody {{ background: transparent; }}
QScrollArea#homeScroll > QWidget > QWidget {{ background: transparent; }}

QLabel#eyebrow {{
    font-size: {s(11)}; font-weight: 700; color: {TEAL};
    letter-spacing: 2px;
}}
QLabel#homeH1 {{
    font-size: {s(34)}; font-weight: 800; color: {TEXT_PRIMARY};
}}
QLabel#panelTitle {{
    font-size: {s(19)}; font-weight: 700; color: {TEXT_PRIMARY};
}}
QLabel#panelSection {{
    font-size: {s(11)}; font-weight: 700; color: {TEAL};
    letter-spacing: 1px;
}}
QLabel#rakNombor {{
    font-size: {s(42)}; font-weight: 800; color: {TEAL};
}}

/* Chip topik (Niat, Solat, …) — kotak sama saiz, sudut sederhana */
QPushButton#chipTopik {{
    background-color: {CARD_BG}; color: {TEXT_SECONDARY};
    border: 1px solid {BORDER}; border-radius: {s(8)};
    padding: {s(8)} {s(18)}; font-size: {s(12)}; font-weight: 600;
}}
QPushButton#chipTopik:hover {{
    border-color: {TEAL}; color: {TEAL}; background-color: {CARD_BG_HOVER};
}}

/* Kad jalan pantas & kad panel kanan */
QFrame#quickCard {{
    background-color: {CARD_BG};
    border: 1px solid {BORDER};
    border-left: 3px solid {TEAL};
    border-radius: {s(8)};
}}
QFrame#quickCard:hover {{
    background-color: {CARD_BG_HOVER}; border-color: {TEAL};
}}
QFrame#sideCard {{
    background-color: {CARD_BG};
    border: 1px solid {BORDER};
    border-radius: {s(10)};
}}
QFrame#sideCard:hover {{
    background-color: {CARD_BG_HOVER}; border-color: {TEAL_GLOW};
}}
QLabel#badgeNumb {{
    background-color: {TEAL_PALE}; color: {TEAL};
    font-size: {s(16)}; font-weight: 800;
    border-radius: {s(8)};
}}
QLabel#petikanText {{
    font-size: {s(14)}; font-weight: 600; color: {TEXT_PRIMARY};
}}

/* ── Halaman Senarai Hadis (26 Ogos 2026) ────────────────────────── */
QFrame#kadDwi {{
    background-color: {CARD_BG};
    border: 1px solid {BORDER};
    border-radius: {s(12)};
}}
QFrame#kadDwi:hover {{
    background-color: {CARD_BG_HOVER}; border-color: {TEAL};
}}
QLabel#noBadge {{
    background-color: {TEAL_PALE}; color: {TEAL};
    font-size: {s(17)}; font-weight: 800;
    border: 1px solid {BORDER_GLASS}; border-radius: {s(10)};
}}
QFrame#lineV {{ background-color: {BORDER}; border: none; max-width: 1px; }}
QFrame#babRow {{
    background-color: transparent; border: 1px solid transparent;
    border-radius: {s(8)};
}}
QFrame#babRow:hover {{ background-color: {CARD_BG_HOVER}; }}
QFrame#babRow_active {{
    background-color: {CARD_BG_HOVER}; border: 1px solid {TEAL};
    border-radius: {s(8)};
}}
QPushButton#simpanChip {{
    background-color: transparent; color: {TEXT_MUTED};
    border: 1px solid {BORDER}; border-radius: {s(15)};
    font-size: {s(13)};
}}
QPushButton#simpanChip:hover {{ border-color: {TEAL}; }}
QPushButton#simpanChip_aktif {{
    background-color: {TEAL_PALE}; border: 1px solid {TEAL};
    border-radius: {s(15)}; font-size: {s(13)};
}}
QScrollArea#babScroll, QScrollArea#babScroll > QWidget > QWidget {{
    background: transparent;
}}
"""
