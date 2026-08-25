"""Widget boleh guna semula — gaya hadis.my."""

from __future__ import annotations

import os

from PyQt5.QtCore import QEvent, QObject, QSize, Qt, QTimer, pyqtSignal
from PyQt5.QtGui import (QColor, QFont, QIcon, QLinearGradient, QPainter,
                         QPixmap, QTextOption)
from PyQt5.QtWidgets import (
    QApplication, QFrame, QHBoxLayout, QLabel, QLineEdit, QMenu,
    QPushButton, QScrollArea, QSizePolicy, QTextBrowser, QVBoxLayout,
    QWidget,
)

from .theme import (
    ARABIC_FONTS, CARD_BG, CONTENT_MAX_W, GUTTER, PAGE_BG, TEAL,
    TEXT_MUTED, TEXT_PRIMARY, TEXT_SECONDARY, ada_latar_imej,
)

# Latar imej (tema AQUA sahaja) — aset baca sahaja di ASSET_DIR. Jika
# fail hilang, BackgroundCanvas fallback kepada warna PAGE_BG pepejal
# (apl tetap berfungsi; tiada ranap).
# _LATAR_GLOB  : halaman Utama + rak (glob + manuskrip + garis masa)
# _LATAR_DUNIA : Makluman (deklarasi) + panel Tetapan SAHAJA — peta
#                dunia rangkaian (26 Ogos, permintaan pengguna)
_LATAR_GLOB = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "latar_globe_timeline.png",
)
_LATAR_DUNIA = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "latar_globe_dunia.png",
)


def lukis_latar(w: int, h: int, laluan: str | None = None) -> QPixmap:
    """Lukis latar penuh (imej + scrim) ke pixmap — kongsi semua permukaan.

    Dipakai oleh BackgroundCanvas (halaman Utama/rak) DAN SettingsPanel
    (paintEvent) supaya kedua-duanya sentiasa serupa. Tema bukan-AQUA:
    warna PAGE_BG sahaja (pemanggil boleh langkau panggilan ini).

    laluan: laluan imej alternatif (None = glob lalai Utama/rak).
    """
    pm = QPixmap(w, h)
    pm.fill(QColor(PAGE_BG))
    p = QPainter(pm)
    p.setRenderHint(QPainter.SmoothPixmapTransform)
    imej = _imej_glob(laluan or _LATAR_GLOB)
    if imej is not None and not imej.isNull():
        # Skala "cover": isi penuh, kekal nisbah, potong lebihan.
        iw, ih = imej.width(), imej.height()
        skala = max(w / iw, h / ih)
        tw, th = int(iw * skala), int(ih * skala)
        diskala = imej.scaled(tw, th, Qt.KeepAspectRatio,
                              Qt.SmoothTransformation)
        p.drawPixmap((w - tw) // 2, (h - th) // 2, diskala)
        # Scrim RENDAH (26 Ogos, permintaan pengguna: "glassy") —
        # diredupkan daripada alpha 150/200 supaya glob lebih jelas
        # menembusi permukaan seperti kaca. Cukup gelap untuk teks:
        # imej glob asasnya navy gelap (#0d1b2a); zon paling terang
        # hanyalah nod/garis rangkaian kecil.
        p.fillRect(0, 0, w, h, QColor(6, 14, 22, 85))
        g = QLinearGradient(0, 0, w * 0.85, 0)
        g.setColorAt(0.0, QColor(6, 14, 22, 120))
        g.setColorAt(0.55, QColor(6, 14, 22, 60))
        g.setColorAt(1.0, QColor(6, 14, 22, 10))
        p.fillRect(0, 0, w, h, g)
    p.end()
    return pm


def _imej_glob(laluan: str) -> QPixmap | None:
    """Muat pixmap latar sekali (cache per laluan)."""
    pm = _GLOB_CACHE.get(laluan)
    if pm is None:
        if os.path.exists(laluan):
            pm = QPixmap(laluan)
        else:
            pm = QPixmap()
        _GLOB_CACHE[laluan] = pm
    return pm or None

_GLOB_CACHE: dict[str, QPixmap] = {}


def lukis_latar_dunia(w: int, h: int) -> QPixmap:
    """Latar peta dunia rangkaian — Makluman + panel Tetapan SAHAJA."""
    return lukis_latar(w, h, _LATAR_DUNIA)


class BackgroundCanvas(QWidget):
    """Widget akar yang melukis latar imej glob untuk tema AQUA.

    TEMA BUKAN-AQUA: isi PAGE_BG sahaja (sifar kosong, penampilan lama
    dikekalkan). TEMA AQUA: glob diskala "cover" + scrim gelap supaya
    SEMUA teks kekal >= 4.5:1 walaupun di zon glob paling terang —
    panel kaca alpha 20/255 sahaja TIDAK cukup menjamin kontras.

    PENTING QSS: widget ini SENGAJA tidak set WA_StyledBackground, jadi
    peraturan QSS `QWidget#page {{ background-color: ... }}` TIDAK
    dilukis di sini — paintEvent di bawah mengawal sepenuhnya. Cache
    QPixmap ikut (lebar, tinggi): skala semula HANYA pada resize, bukan
    setiap paint (elak kedip & CPU).

    dunia=True: guna latar peta dunia rangkaian (Makluman + Tetapan
    sahaja, 26 Ogos permintaan pengguna) — bukan glob Utama/rak.
    """

    def __init__(self, parent=None, dunia: bool = False):
        super().__init__(parent)
        self._dunia = dunia
        self._cache: tuple[int, int, QPixmap] | None = None

    def paintEvent(self, e):
        w, h = max(1, self.width()), max(1, self.height())
        if not ada_latar_imej():
            # Tema lain: warna pepejal — tiada perlu cache pixmap.
            p = QPainter(self)
            p.fillRect(self.rect(), QColor(PAGE_BG))
            p.end()
            return
        c = self._cache
        if c is None or c[0] != w or c[1] != h:
            if self._dunia:
                c = (w, h, lukis_latar_dunia(w, h))
            else:
                c = (w, h, lukis_latar(w, h))
            self._cache = c
        p = QPainter(self)
        p.drawPixmap(0, 0, c[2])
        p.end()


def elide(text: str, n: int) -> str:
    text = " ".join((text or "").split())
    return text if len(text) <= n else text[:n].rstrip() + "…"


# Nombor buku (reference.book CDN) bagi bab tafsir Al-Quran. Digunakan
# untuk tag "Bab Tafsir" pada hadis dalam bab-bab ini sahaja. Kunci
# ialah slug hadis.db (bukan slug CDN -- lihat PETA_KITAB).
BAB_TAFSIR: dict[str, int] = {
    "bukhari": 65,
    "muslim": 56,
    "tirmidzi": 47,
}


def _ialah_bab_tafsir(collection, book) -> bool:
    """Adakah buku ini bab tafsir Al-Quran (tag 'Bab Tafsir' dipapar)?

    `BAB_TAFSIR` memetakan koleksi -> nombor buku tafsir. Logik ini
    dahulu dibenamkan di DUA tempat (kad hasil carian + halaman
    butiran); kini fungsi tulen — diuji unit (semak.py 8t) supaya
    kedua-dua paparan tidak hanyut.
    """
    return bool(collection and book and BAB_TAFSIR.get(collection) == book)


def _pilih_terjemahan(melayu, indonesia, english) -> str:
    """Petikan terjemahan kad — keutamaan bahasa: Melayu > Indonesia > English.

    Pulang teks pertama yang bukan kosong (strip); '' jika tiada.
    Dahulu dibenamkan dalam `hadith_card`; kini fungsi tulen — diuji
    unit (semak.py 8u) supaya keutamaan bahasa tidak berubah tanpa
    disedari (cth. English naik mendahului Melayu).
    """
    for t in (melayu, indonesia, english):
        if t and t.strip():
            return t.strip()
    return ""


def _papar_chip(show_chip: bool, kitab_name) -> bool:
    """Chip nama kitab pada kad dipapar bila diminta DAN nama ada.

    Dahulu dibenamkan sebagai `if show_chip and kitab_name:` dalam
    `hadith_card`; kini fungsi tulen — diuji unit (semak.py 8v).
    """
    return bool(show_chip and kitab_name)


def make_scroll(parent=None) -> QScrollArea:
    sa = QScrollArea(parent)
    sa.setWidgetResizable(True)
    sa.setFrameShape(QFrame.NoFrame)
    sa.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    sa.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
    return sa


def centered_column(parent=None) -> tuple[QWidget, QVBoxLayout]:
    """Lajur kandungan berpusat dengan lebar maksimum — seperti hadis.my."""
    outer = QWidget(parent)
    outer.setObjectName("page")
    # PENTING: polisi lalai `Preferred` membenarkan Qt MENGECUTKAN
    # widget ini di bawah sizeHint-nya. Diukur pada senarai 20 hadis:
    # ia mahu 3531px tetapi hanya diberi 2689px -- 842px dirampas oleh
    # addStretch(1) pada layout akar, dan QScrollArea menjadikan ruang
    # itu kawasan boleh skrol yang KOSONG.
    #
    # `Maximum` menegak: sizeHint ialah HAD ATAS -- Qt tidak akan
    # membesarkan outer melebihi kandungannya, jadi tiada ruang skrol
    # kosong tercipta.
    #
    # Lesson #4 memberi amaran `Maximum` boleh meruntuhkan tinggi ke 0
    # sebelum susun atur pertama. Diuji semula (tetingkap 640x480 ->
    # 1240x700, semua 7 halaman): TIADA yang runtuh. Amaran itu terpakai
    # kepada `inner`, bukan `outer` -- inner mengandungi layout kandungan
    # sebenar, outer hanya pembungkus mendatar.
    outer.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
    ol = QHBoxLayout(outer)
    ol.setContentsMargins(GUTTER, 0, GUTTER, 0)
    ol.addStretch(1)

    inner = QWidget()
    inner.setObjectName("page")
    inner.setMaximumWidth(CONTENT_MAX_W)
    # `Preferred` menegak (bukan `Minimum`): membenarkan Qt memberi
    # inner TEPAT sizeHint-nya. `Minimum` menjadikan sizeHint sebagai
    # had bawah sahaja, jadi inner boleh membesar melebihi kandungan
    # dan mencipta ruang skrol kosong.
    #
    # JANGAN guna `Maximum` -- Qt akan meruntuhkan tinggi ke 0 sebelum
    # susun atur pertama dan halaman kelihatan KOSONG.
    inner.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
    il = QVBoxLayout(inner)
    il.setContentsMargins(0, 0, 0, 0)
    il.setSpacing(12)

    ol.addWidget(inner, stretch=20)
    ol.addStretch(1)
    return outer, il


def divider() -> QFrame:
    f = QFrame()
    f.setObjectName("divider")
    # 2px supaya jelas kelihatan dalam mod terang (1px terlalu nipis)
    f.setFixedHeight(2)
    return f


def arabic_browser(text: str = "", scale: float = 1.0,
                   font_family: str | None = None) -> QTextBrowser:
    """Paparan teks Arab — PADAN TEPAT dengan make_arabic_browser() asal.

    Urutan panggilan adalah KRITIKAL. Jangan ubah tanpa uji pada Windows:
      1. setLayoutDirection + setAlignment DAHULU (widget masih kosong)
      2. setPlainText SELEPAS itu — sekali sahaja
      3. JANGAN panggil setAlignment lagi selepas teks dimasukkan
      4. JANGAN guna setDefaultTextOption / setWrapMode / setTextWidth
      5. JANGAN auto-saiz tinggi — gunakan setMinimumHeight sahaja

    Setiap satu di atas pernah dicuba dan menyebabkan perkataan songsang.
    """
    tb = QTextBrowser()
    tb.setLayoutDirection(Qt.RightToLeft)
    tb.setAlignment(Qt.AlignRight | Qt.AlignAbsolute)
    tb.setReadOnly(True)
    tb.setOpenExternalLinks(False)
    tb.setFrameShape(QFrame.NoFrame)
    tb.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    tb.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)

    fam = font_family or ARABIC_FONTS[0]
    pt = max(11, int(19 * scale))
    fnt = QFont(fam, pt)
    tb.document().setDefaultFont(fnt)
    tb.setFont(fnt)
    tb.setStyleSheet(
        f'QTextBrowser {{ font-family: "{fam}"; font-size: {pt}pt;'
        f" background: transparent; border: none; }}")

    if text:
        tb.setPlainText(text)

    # Tinggi ikut kandungan. Ukur pada QFontMetrics + document CLONE —
    # JANGAN setTextWidth pada dokumen hidup (merosakkan susunan bidi).
    if text:
        def _fit():
            w = tb.viewport().width()
            if w < 50:
                return
            doc = tb.document().clone()
            doc.setDefaultFont(fnt)
            doc.setTextWidth(w)
            h = int(doc.size().height()) + 10
            if abs(tb.height() - h) > 4:
                tb.setFixedHeight(max(48, h))


        _orig_resize = tb.resizeEvent

        def _on_resize(e):
            _orig_resize(e)
            _fit()

        tb.resizeEvent = _on_resize
        QTimer.singleShot(0, _fit)
        tb.setMinimumHeight(48)
    else:
        tb.setMinimumHeight(60)
    return tb


def set_arabic(tb: QTextBrowser, text: str) -> None:
    tb.setPlainText(text or "")


def text_browser(text: str = "", scale: float = 1.0,
                 color: str | None = None,
                 markdown: bool = False,
                 justify: bool = False) -> QTextBrowser:
    # PENTING: jangan letak `color=TEXT_SECONDARY` sebagai nilai lalai.
    # Python nilaikan nilai lalai SEKALI pada masa import, jadi warna
    # tema gelap terkunci selama-lamanya — dalam mod terang teks
    # terjemahan jadi kelabu pucat atas kad putih (tidak nampak).
    # Baca warna semasa daripada modul tema pada setiap panggilan.
    if color is None:
        import ui.theme as _t
        color = _t.THEMES[_t.CURRENT_THEME]["TEXT_SECONDARY"]
    tb = QTextBrowser()
    tb.setReadOnly(True)
    tb.setFrameShape(QFrame.NoFrame)
    tb.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    tb.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    tb.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
    pt = max(8, int(10.5 * scale))
    f = QFont("Segoe UI", pt)
    tb.setFont(f)
    tb.document().setDefaultFont(f)
    tb.setStyleSheet(
        f"QTextBrowser {{ color: {color}; font-family: 'Segoe UI';"
        f" font-size: {pt}pt; background: transparent; border: none; }}")
    # `justify=True` untuk teks terjemahan (keputusan pengguna 13 Ogos):
    # selaraskan teks kiri-kanan penuh (text-align: justify) melalui
    # QTextOption dokumen -- berfungsi dengan setPlainText, tanpa perlu
    # HTML escape.
    if justify:
        tb.document().setDefaultTextOption(QTextOption(Qt.AlignJustify))
    if text:
        # `markdown=True` untuk teks yang memang ditulis dalam Markdown
        # (cth. draf jawapan AI). Tanpa ia, penanda `**` dipapar mentah.
        # Lalai kekal plain supaya pemanggil sedia ada tidak berubah --
        # teks hadis mengandungi aksara yang Markdown akan salah tafsir.
        if markdown:
            tb.setMarkdown(text)
        else:
            tb.setPlainText(text)
    _autosize(tb)
    return tb


def _autosize(tb: QTextBrowser) -> None:
    """Tinggi mengikut kandungan — elak skrol dalam skrol."""
    def fit():
        doc = tb.document()
        doc.setTextWidth(max(1, tb.viewport().width()))
        h = int(doc.size().height()) + 8
        tb.setFixedHeight(max(28, h))

    tb.document().contentsChanged.connect(fit)
    orig = tb.resizeEvent

    def on_resize(e):
        orig(e)
        fit()

    tb.resizeEvent = on_resize
    fit()


class ClickCard(QFrame):
    """Kad boleh klik dengan hover — elak isu SIP mousePressEvent.

    Hover latar/sempadan datang daripada QSS (`QFrame#card:hover`).
    NOTA 16 Ogos: QGraphicsDropShadowEffect TIDAK dirender pada widget
    dengan latar QSS (diukur fizikal: 0 piksel bayang) -- kesan timbul
    kad kitab dilakukan oleh pembungkus lutsinar `BungkusTimbul`
    (ui/pages_home.py), bukan di sini.
    """

    clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("card")
        self.setCursor(Qt.PointingHandCursor)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton and self.rect().contains(e.pos()):
            self.clicked.emit()
        super().mouseReleaseEvent(e)


def hadith_card(hadis: dict, kitab_name: str = "", scale: float = 1.0,
                show_chip: bool = True, arabic_font: str | None = None,
                arab_chars: int = 150, trans_chars: int = 190,
                papar_melayu=None) -> ClickCard:
    """Kad senarai hadis — susunan sama seperti hadis.my.

    [chip kitab]  No. 1                              Baca →
    نص عربي مقتطف …
    Petikan terjemahan Melayu …
    """
    card = ClickCard()
    lo = QVBoxLayout(card)
    lo.setContentsMargins(20, 16, 20, 16)
    lo.setSpacing(10)

    # Baris atas
    top = QWidget()
    tl = QHBoxLayout(top)
    tl.setContentsMargins(0, 0, 0, 0)
    tl.setSpacing(10)

    if _papar_chip(show_chip, kitab_name):
        chip = QLabel(kitab_name)
        chip.setObjectName("chip")
        tl.addWidget(chip)

    no = QLabel(f"No. {hadis.get('id', '')}")
    no.setObjectName("hadisNo")
    tl.addWidget(no)

    # Nama bab (Fasa 3) -- Inggeris apa adanya dari CDN, dipotong untuk
    # kekal dalam satu baris. Tiada terjemahan: kami papar mentah.
    bab = (hadis.get("nama_bab") or "").strip()
    if bab:
        bl = QLabel(elide(bab, 44))
        bl.setObjectName("babName")
        bl.setToolTip(bab)
        tl.addWidget(bl)

    tl.addStretch()

    # Tag untuk hadis dalam bab tafsir Al-Quran sahaja.
    if _ialah_bab_tafsir(hadis.get("collection"), hadis.get("book")):
        tag = QLabel("Bab Tafsir")
        tag.setObjectName("chip")
        tl.addWidget(tag)

    baca = QLabel("Baca →")
    baca.setObjectName("bacaLink")
    tl.addWidget(baca)
    lo.addWidget(top)

    # Arab
    arab = (hadis.get("arab") or "").strip()
    if arab:
        al = QLabel(elide(arab, arab_chars))
        al.setWordWrap(True)
        al.setAlignment(Qt.AlignRight)
        al.setLayoutDirection(Qt.RightToLeft)
        fam = arabic_font or ARABIC_FONTS[0]
        al.setStyleSheet(
            f'font-family: "{fam}"; font-size: {int(17 * scale)}px;'
            f"color: {TEXT_PRIMARY}; line-height: 190%;"
        )
        lo.addWidget(al)

    # Terjemahan — utamakan Melayu
    _ms = (hadis.get("melayu") or "").strip()
    if _ms:
        # "Shallallahu" (Indonesia) -> "Sallallahu" (DBP). Paparan
        # sahaja; teks tersimpan tidak diubah. Lihat utils/bahasa.py
        from utils.bahasa import betulkan_melayu
        _ms = betulkan_melayu(_ms)
        if papar_melayu is not None:
            _ms = papar_melayu(_ms)
    trans = _pilih_terjemahan(_ms, hadis.get("indonesia"),
                              hadis.get("english"))
    if trans:
        tlbl = QLabel(elide(trans, trans_chars))
        tlbl.setWordWrap(True)
        tlbl.setStyleSheet(
            f"font-size: {int(12.5 * scale)}px; color: {TEXT_SECONDARY};"
            f"line-height: 155%;"
        )
        lo.addWidget(tlbl)

    return card


class FilterChips(QWidget):
    """Bar penapis kitab mendatar — meniru hadis.my."""

    changed = pyqtSignal(object)   # slug atau None

    def __init__(self, meta: dict, parent=None):
        super().__init__(parent)
        self._active = None
        self._btns: dict = {}

        lo = QHBoxLayout(self)
        lo.setContentsMargins(0, 0, 0, 0)
        lo.setSpacing(6)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

        for slug, label in [(None, "Semua")] + [
            (s, m.get("short", m["name"])) for s, m in meta.items()
        ]:
            b = QPushButton(label)
            b.setObjectName("filterChip")
            b.setCursor(Qt.PointingHandCursor)
            b.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
            b.clicked.connect(lambda _, s=slug: self.set_active(s))
            lo.addWidget(b)
            self._btns[slug] = b
        lo.addStretch()
        self.set_active(None, emit=False)

    def set_active(self, slug, emit: bool = True):
        self._active = slug
        for s, b in self._btns.items():
            b.setObjectName("filterChip_active" if s == slug else "filterChip")
            b.style().unpolish(b)
            b.style().polish(b)
        if emit:
            self.changed.emit(slug)

    def active(self):
        return self._active


class Toast(QLabel):
    """Maklum balas ringkas — 'Disalin!' dsb."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet(
            f"background-color: {CARD_BG}; color: {TEAL};"
            f"border: 1px solid {TEAL}; border-radius: 8px;"
            f"padding: 10px 20px; font-size: 12px; font-weight: 600;"
        )
        self._hide_timer = None
        self.hide()

    def show_msg(self, text: str, ms: int = 1800):
        """Paparkan toast. `ms=0` bermakna kekal sehingga `hide()` dipanggil
        (digunakan untuk maklum balas "Membuka…" semasa muatan async).

        Timer auto-hide disimpan dan DIBATALKAN apabila toast baharu
        dipaparkan — jika tidak, timer lama (cth. "Disalin!" 1800ms)
        masih aktif dan menutup toast baharu yang kekal lebih awal.
        """
        from PyQt5.QtCore import QTimer
        if self._hide_timer is not None:
            self._hide_timer.stop()
            self._hide_timer = None
        self.setText(text)
        self.adjustSize()
        if self.parent():
            p = self.parent()
            self.move((p.width() - self.width()) // 2, p.height() - self.height() - 40)
        self.show()
        self.raise_()
        if ms > 0:
            t = QTimer(self)
            t.setSingleShot(True)
            t.timeout.connect(self.hide)
            t.start(ms)
            self._hide_timer = t

# ══════════════════════════════════════════════════════════════════════
def gear_icon(size: int = 22, color: str = None) -> QIcon:
    """Ikon gear vektor — tajam pada semua saiz & DPI.

    Emoji ⚙ bergantung fon sistem dan sering render kecil/pudar atau
    jadi kotak tofu. SVG ini konsisten merentas platform.
    """
    from ui.theme import TEXT_MUTED
    col = color or TEXT_MUTED
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"
      fill="none" stroke="{col}" stroke-width="1.9"
      stroke-linecap="round" stroke-linejoin="round">
      <circle cx="12" cy="12" r="3.1"/>
      <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83
               l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21
               a2 2 0 1 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33
               l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82
               1.65 1.65 0 0 0-1.51-1H3a2 2 0 1 1 0-4h.09A1.65 1.65 0 0 0 4.6 9
               a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06
               a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 1 1 4 0
               v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06
               a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9
               a1.65 1.65 0 0 0 1.51 1H21a2 2 0 1 1 0 4h-.09
               a1.65 1.65 0 0 0-1.51 1z"/>
    </svg>"""
    pm = QPixmap()
    pm.loadFromData(svg.encode("utf-8"), "SVG")
    return QIcon(pm.scaled(size, size, Qt.KeepAspectRatio,
                           Qt.SmoothTransformation))


class GearButton(QPushButton):
    """Butang gear dengan warna hover yang betul (QIcon tidak ikut QSS)."""

    def __init__(self, parent=None, size: int = 22):
        super().__init__(parent)
        from ui.theme import TEAL, TEXT_MUTED
        self._n = gear_icon(size, TEXT_MUTED)
        self._h = gear_icon(size, TEAL)
        self.setIcon(self._n)
        self.setIconSize(QSize(size, size))
        self.setFixedSize(size + 16, size + 12)
        self.setCursor(Qt.PointingHandCursor)
        self.setToolTip("Tetapan")

    def enterEvent(self, e):
        self.setIcon(self._h)
        super().enterEvent(e)

    def leaveEvent(self, e):
        self.setIcon(self._n)
        super().leaveEvent(e)


class _CopyMenuFilter(QObject):
    """Pintas QEvent.ContextMenu sebelum Qt sempat papar menu lalainya.

    KENAPA eventFilter, bukan setContextMenuPolicy?
    Untuk QAbstractScrollArea (QTextBrowser/QTextEdit), Qt boleh papar
    menu terbina "Copy / Select All" walaupun policy sudah ditetapkan —
    bergantung widget mana yang menerima acara dahulu. eventFilter
    memintas acara pada punca dan memulangkan True supaya Qt BERHENTI
    memprosesnya. Ini tidak boleh dipintas.

    Nota: JANGAN override contextMenuEvent melalui umpukan lambda —
    itu mencetuskan SIP TypeError (lihat lessons learned #2).
    """

    def __init__(self, target, extra=None):
        super().__init__(target)
        self.target = target
        self.extra = extra or []

    def eventFilter(self, obj, ev):
        if ev.type() == QEvent.ContextMenu:
            self._popup(ev.globalPos())
            return True                      # halang menu lalai Qt
        return False

    def _popup(self, gpos):
        from ui.theme import (BORDER, CARD_BG, TEAL, TEAL_PALE,
                              TEXT_FAINT, TEXT_PRIMARY)
        w = self.target
        m = QMenu(w)
        m.setStyleSheet(f"""
            QMenu {{ background-color: {CARD_BG}; color: {TEXT_PRIMARY};
                     border: 1px solid {BORDER}; border-radius: 6px;
                     padding: 5px; font-size: 12px; }}
            QMenu::item {{ padding: 7px 26px 7px 14px; border-radius: 4px;
                           color: {TEXT_PRIMARY}; }}
            QMenu::item:selected {{ background-color: {TEAL_PALE};
                                    color: {TEAL}; }}
            QMenu::item:disabled {{ color: {TEXT_FAINT}; }}
            QMenu::separator {{ height: 1px; background: {BORDER};
                                margin: 5px 10px; }}
        """)

        is_line = isinstance(w, QLineEdit)
        if is_line:
            has_sel = w.hasSelectedText()
            editable = not w.isReadOnly()
        else:
            cur = w.textCursor() if hasattr(w, "textCursor") else None
            has_sel = bool(cur and cur.hasSelection())
            editable = not getattr(w, "isReadOnly", lambda: True)()

        # Potong — hanya untuk medan yang boleh diedit
        if editable and hasattr(w, "cut"):
            a = m.addAction("Potong")
            a.setEnabled(has_sel)
            a.triggered.connect(w.cut)

        a1 = m.addAction("Salin")
        a1.setEnabled(has_sel)
        a1.triggered.connect(w.copy)

        if editable and hasattr(w, "paste"):
            a = m.addAction("Tampal")
            a.setEnabled(bool(QApplication.clipboard().text()))
            a.triggered.connect(w.paste)

        def copy_all():
            txt = getattr(w, "_raw", None)
            if txt is None:
                txt = (w.toPlainText() if hasattr(w, "toPlainText")
                       else w.text())
            QApplication.clipboard().setText(txt)

        m.addAction("Salin semua").triggered.connect(copy_all)

        if hasattr(w, "selectAll"):
            m.addSeparator()
            m.addAction("Pilih semua").triggered.connect(w.selectAll)

        if self.extra:
            m.addSeparator()
            for label, fn in self.extra:
                m.addAction(label).triggered.connect(fn)

        m.exec_(gpos)


def attach_copy_menu(widget, extra=None):
    """Pasang menu klik-kanan Melayu pada widget teks.

    Memasang eventFilter pada widget DAN viewport supaya acara
    ditangkap tidak kira mana satu menerimanya dahulu.
    """
    f = _CopyMenuFilter(widget, extra)
    widget._copy_filter = f                  # elak dikutip sampah
    widget.installEventFilter(f)

    # matikan menu terbina Qt sebagai lapisan kedua
    widget.setContextMenuPolicy(Qt.PreventContextMenu)

    # QLineEdit tiada viewport(); QTextBrowser ada.
    vp = widget.viewport() if hasattr(widget, "viewport") else None
    if vp is not None:
        vp.installEventFilter(f)
        vp.setContextMenuPolicy(Qt.PreventContextMenu)
    return widget


class BookCover(QFrame):
    """Ilustrasi buku ringkas SENDIRI — kad warna kitab + tajuk Arab.

    Keputusan Sesi 15: JANGAN guna cover penerbit (lesen tidak disahkan,
    cuma 2/9 kitab, resolusi rendah). Sebaliknya kita lukis buku sendiri:
    100% milik sendiri, tiada risiko lesen, resolusi bebas. Dipapar
    sekali sahaja di header halaman senarai kitab, bukan pada setiap kad.
    """

    def __init__(self, meta: dict, scale: float = 1.0, parent=None):
        super().__init__(parent)
        self.setObjectName("bookCover")
        warna = meta.get("warna", TEAL)
        self.setFixedSize(int(108 * scale), int(148 * scale))

        lo = QHBoxLayout(self)
        lo.setContentsMargins(0, 0, 0, 0)
        lo.setSpacing(0)

        # Tulang buku (spine) — jalur lebih gelap di kiri
        tulang = QLabel()
        tulang.setFixedWidth(int(12 * scale))
        c = QColor(warna)
        c = c.darker(115)
        tulang.setStyleSheet(
            f"background-color: {c.name()};"
            f"border-top-left-radius: {int(8*scale)}px;"
            f"border-bottom-left-radius: {int(8*scale)}px;")

        # Muka buku — tajuk Arab + nama ringkas
        muka = QWidget()
        muka.setStyleSheet(f"background-color: {warna};")
        ml = QVBoxLayout(muka)
        ml.setContentsMargins(int(10 * scale), int(10 * scale),
                              int(10 * scale), int(10 * scale))
        ml.setSpacing(int(6 * scale))
        ml.addStretch(1)

        arab = QLabel(meta.get("arabic", ""))
        arab.setAlignment(Qt.AlignCenter)
        arab.setWordWrap(True)
        fam = ARABIC_FONTS[0]
        arab.setStyleSheet(
            f'font-family: "{fam}"; font-size: {int(19 * scale)}px;'
            f'color: #FFFFFF; font-weight: 600; line-height: 140%;')
        ml.addWidget(arab)

        nama = QLabel(meta.get("short", ""))
        nama.setAlignment(Qt.AlignCenter)
        nama.setStyleSheet(
            f"font-size: {int(9 * scale)}px; color: #FFFFFF;"
            f"font-weight: 600; letter-spacing: 1px;")
        ml.addWidget(nama)
        ml.addStretch(1)

        lo.addWidget(tulang)
        lo.addWidget(muka, 1)
        lo.addWidget(tulang)  # tulang kanan — simetri buku


class Collapsible(QWidget):
    """Bahagian boleh kembang — tertutup secara lalai.

    Prinsip "pengguna campuran": paparan asal kekal bersih untuk orang
    awam; bahan teknikal (transliterasi, sanad, syarah Arab) disorok di
    belakang tajuk boleh klik. Penuntut ilmu jumpa bila cari.

    Kandungan dibina MALAS (lazy) melalui `builder` — supaya hadis yang
    tidak pernah dibuka tidak membazir masa transliterasi.
    """

    def __init__(self, tajuk: str, builder=None, parent=None):
        super().__init__(parent)
        self._builder = builder
        self._dibina = False
        self._terbuka = False
        self._tajuk = tajuk

        lo = QVBoxLayout(self)
        lo.setContentsMargins(0, 0, 0, 0)
        lo.setSpacing(0)

        self.btn = QPushButton()
        self.btn.setObjectName("collapse")
        self.btn.setCursor(Qt.PointingHandCursor)
        self.btn.setCheckable(True)
        self.btn.clicked.connect(self._toggle)
        lo.addWidget(self.btn)

        self.isi = QWidget()
        self._isi_lo = QVBoxLayout(self.isi)
        self._isi_lo.setContentsMargins(2, 8, 2, 2)
        self._isi_lo.setSpacing(8)
        self.isi.setVisible(False)
        lo.addWidget(self.isi)

        self._kemas_label()

    def _kemas_label(self):
        panah = "\u25be" if self._terbuka else "\u25b8"   # ▾ / ▸
        self.btn.setText(f"  {panah}  {self._tajuk}")

    def _toggle(self):
        self._terbuka = not self._terbuka
        if self._terbuka and not self._dibina:
            self._dibina = True
            if self._builder:
                try:
                    self._builder(self._isi_lo)
                except Exception as e:
                    lbl = QLabel(f"Tidak dapat dipaparkan: {e}")
                    lbl.setObjectName("muted")
                    lbl.setWordWrap(True)
                    self._isi_lo.addWidget(lbl)
        self.isi.setVisible(self._terbuka)
        self._kemas_label()

    def buka(self):
        if not self._terbuka:
            self.btn.setChecked(True)
            self._toggle()
