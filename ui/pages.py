"""Pembina halaman — Utama, Kitab, Carian. Gaya hadis.my."""

from __future__ import annotations

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QSizePolicy,
    QCheckBox, QFrame, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget,
)

from .theme import (
    CARD_BG, CARD_BG_HOVER, COLLECTION_META, HEADER_BG, RADIUS, TEAL,
    TEAL_PALE, TEXT_FAINT, TEXT_MUTED, TEXT_PRIMARY, TEXT_SECONDARY,
    is_dark,
)
from .widgets import ClickCard, FilterChips, divider


def _campur(hex_warna: str, sasaran: tuple, peratus: float) -> str:
    """Campur warna hex dengan warna sasaran (putih/hitam) untuk hover.

    Tema gelap: cerahkan (campur putih) supaya border hover lebih
    terang atas latar gelap; tema terang: gelapkan (campur hitam)
    supaya lebih kontras atas kad putih.
    """
    h = hex_warna.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    tr, tg, tb = sasaran
    nr = int(r + (tr - r) * peratus)
    ng = int(g + (tg - g) * peratus)
    nb = int(b + (tb - b) * peratus)
    return f"#{nr:02x}{ng:02x}{nb:02x}"


class Hero(QFrame):
    """Blok hero dengan tajuk, petikan, dan bar carian."""

    def __init__(self, title: str, quote: str = "", subtitle: str = "",
                 compact: bool = False, side=None, parent=None):
        super().__init__(parent)
        self.setObjectName("hero")
        # Hero mesti Fixed menegak — kalau tidak ia meregang mengisi
        # semua ruang kosong dan menolak kandungan ke bawah skrin.
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        lo = QVBoxLayout(self)
        lo.setSizeConstraint(QVBoxLayout.SetMinAndMaxSize)
        # Padding 48px atas+bawah menjadikan Hero 295px pada halaman
        # utama -- kad kitab tertolak keluar skrin laptop 768px.
        # Diukur: 30px cukup lapang tanpa membazir 36px setiap sisi.
        pad = 20 if compact else 30
        lo.setContentsMargins(32, pad, 32, pad)
        lo.setSpacing(8)
        lo.setAlignment(Qt.AlignCenter)

        # Side widget (cth. ilustrasi buku) di sebelah kiri tajuk dalam
        # banner. Tanpa `side`, tingkah laku lama (berpusat) kekal.
        t = QLabel(title)
        t.setObjectName("h1")
        t.setAlignment(Qt.AlignCenter)

        if side is not None:
            baris = QWidget()
            rl = QHBoxLayout(baris)
            rl.setContentsMargins(0, 0, 0, 0)
            rl.setSpacing(24)
            rl.setAlignment(Qt.AlignCenter)
            rl.addWidget(side)
            teks = QVBoxLayout()
            teks.setSpacing(8)
            teks.setAlignment(Qt.AlignVCenter)
            t.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            teks.addWidget(t)
            if quote:
                q = QLabel(quote)
                q.setObjectName("quote")
                q.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                q.setWordWrap(True)
                teks.addWidget(q)
            if subtitle:
                s = QLabel(subtitle)
                s.setObjectName("faint")
                s.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                teks.addWidget(s)
            rl.addLayout(teks)
            lo.addWidget(baris)
        else:
            lo.addWidget(t)
            if quote:
                q = QLabel(quote)
                q.setObjectName("quote")
                q.setAlignment(Qt.AlignCenter)
                q.setWordWrap(True)
                lo.addWidget(q)

        self.body = QVBoxLayout()
        self.body.setSpacing(12)
        lo.addLayout(self.body)

        if side is None and subtitle:
            s = QLabel(subtitle)
            s.setObjectName("faint")
            s.setAlignment(Qt.AlignCenter)
            lo.addWidget(s)

    def resizeEvent(self, e):
        """Kunci tinggi mengikut LEBAR semasa, setiap kali ia berubah.

        `addStretch(1)` pada layout akar halaman dibuang kerana ia
        mencipta 572px kawasan skrol kosong (diukur: kandungan tamat
        y=2742 tetapi body=3314). Tanpa stretch, Hero menjadi
        satu-satunya widget Expanding dan meregang 101px -> 657px.

        Mengunci berdasarkan `heightForWidth` pada lebar SEMASA:
        - `sizeHint()` sahaja tidak cukup -- ia dikira pada lebar lama
        - `QTimer.singleShot(0)` gagal -- dipanggil sebelum saiz stabil
        - kunci sekali sahaja gagal -- tetingkap boleh diubah saiz
        """
        super().resizeEvent(e)
        lay = self.layout()
        if lay is None:
            return
        lebar = self.width()
        if lebar <= 0 or lebar == getattr(self, "_lebar_dikunci", -1):
            return
        self._lebar_dikunci = lebar
        # Buka kunci supaya sizeHint dikira semula pada lebar baharu
        self.setMinimumHeight(0)
        self.setMaximumHeight(16777215)
        h = lay.sizeHint().height()
        if h > 0:
            self.setFixedHeight(h)


class SearchBar(QWidget):
    """Input carian + chip penapis kitab. Carian semantik sentiasa aktif."""

    def __init__(self, placeholder="Cari hadis...", with_chips=True, parent=None):
        super().__init__(parent)
        lo = QVBoxLayout(self)
        lo.setContentsMargins(0, 0, 0, 0)
        lo.setSpacing(8)

        row = QWidget()
        rl = QHBoxLayout(row)
        rl.setContentsMargins(0, 0, 0, 0)
        rl.setSpacing(8)

        self.input = QLineEdit()
        self.input.setPlaceholderText(placeholder)
        self.input.setMinimumHeight(40)
        self.input.setClearButtonEnabled(True)
        rl.addWidget(self.input, stretch=1)

        self.btn = QPushButton("Cari")
        self.btn.setObjectName("primary")
        self.btn.setMinimumHeight(40)
        self.btn.setMinimumWidth(96)
        self.btn.setCursor(Qt.PointingHandCursor)
        rl.addWidget(self.btn)
        lo.addWidget(row)

        self.chips = None
        if with_chips:
            self.chips = FilterChips(COLLECTION_META)
            lo.addWidget(self.chips)

    def text(self) -> str:
        return self.input.text().strip()

    def slug(self):
        return self.chips.active() if self.chips else None

    def is_semantic(self) -> bool:
        return True

    def set_semantic_enabled(self, enabled: bool):
        pass


def _label_kiraan(total, kata: str, fallback: str) -> str:
    """'7,008 hadis' untuk int (koma ribuan); `fallback` sebaliknya.

    Fungsi kongsi untuk banner kitab (pages_kitab.py, `kata="hadis"`,
    fallback '') dan kad koleksi (`KitabCard`, `kata="Hadis"`, fallback
    '— Hadis') — kedua-duanya memformat jumlah hadis dengan koma ribuan
    dan pagar `isinstance(total, int)` (data belum dimuat -> None).
    Dahulu dua fungsi berasingan (`_subtitle_hadis` / `_label_kad_hadis`)
    yang hanya beza pada kata dan teks gantian; disatukan supaya
    sempadan int dan format koma tidak hanyut antara tapak — diuji
    unit (semak.py 8w/8x).
    """
    if not isinstance(total, int):
        return fallback
    return f"{total:,} {kata}"


class KitabCard(ClickCard):
    """Kad koleksi pada halaman utama (mockup 16 Ogos, tala lanjut).

    Reka bentuk: BORDER keliling kad ikut warna kitab (2px) — identiti
    kitab jelas tanpa jalur atas. Bila hover, border bertukar warna
    ikut kitab (cerah dalam tema gelap, gelap dalam tema terang) +
    glow pembungkus. Nama + deskripsi + badge kiraan + "Buka →".
    Ketinggian kekal padat supaya 3 baris kad muat skrin laptop 768px.
    """

    def __init__(self, slug: str, meta: dict, total=None, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(114)
        warna = meta.get("warna") or TEAL
        if is_dark():
            hover_warna = _campur(warna, (255, 255, 255), 0.45)
        else:
            hover_warna = _campur(warna, (0, 0, 0), 0.30)
        # QSS lokal kad: latar + radius ikut tema; border keliling warna
        # kitab; :hover border ikut warna kitab (terang/gelap). Radius
        # tetap 12px (beza skala fon kecil, tidak ketara).
        self.setStyleSheet(
            f"QFrame#card {{ background-color: {CARD_BG}; "
            f"border: 2px solid {warna}; border-radius: {RADIUS}px; }}"
            f"QFrame#card:hover {{ background-color: {CARD_BG_HOVER}; "
            f"border: 2px solid {hover_warna}; border-radius: {RADIUS}px; }}")

        lo = QVBoxLayout(self)
        lo.setContentsMargins(0, 0, 0, 0)
        lo.setSpacing(0)

        body = QWidget()
        bl = QVBoxLayout(body)
        bl.setContentsMargins(15, 12, 15, 12)
        bl.setSpacing(3)

        name = QLabel(meta["name"])
        name.setObjectName("h3")
        bl.addWidget(name)

        desc = QLabel(meta["desc"])
        desc.setObjectName("faint")
        desc.setWordWrap(True)
        bl.addWidget(desc)

        ft = QHBoxLayout()
        ft.setContentsMargins(0, 4, 0, 0)
        self._cnt = QLabel(_label_kiraan(total, "Hadis", "— Hadis"))
        self._cnt.setObjectName("chip")
        ft.addWidget(self._cnt)
        ft.addStretch(1)
        buka = QLabel("Buka →")
        buka.setStyleSheet(
            f"color: {TEAL}; font-size: 12px; font-weight: 600;")
        ft.addWidget(buka)
        bl.addLayout(ft)

        lo.addWidget(body, 1)

    def set_total(self, n):
        self._cnt.setText(_label_kiraan(n, "Hadis", "— Hadis"))


class Pager(QWidget):
    """Kawalan halaman: ‹ Sebelum · 3 / 71 · Seterusnya ›

    Menggantikan corak "Baca Lagi" yang memuat semula segalanya.
    Lompat ke nombor hadis kini melalui kotak carian nombor di atas
    senarai (Sesi 34) — pager ini hanya kawalan halaman.
    """

    def __init__(self, on_page, parent=None):
        super().__init__(parent)
        self._on_page = on_page
        self._page = 1
        self._last = 1
        # Fixed menegak -- sama sebab seperti breadcrumb: pager
        # meregang 52px -> 226px apabila menyerap ruang lebihan.
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

        lo = QHBoxLayout(self)
        lo.setContentsMargins(0, 12, 0, 12)
        lo.setSpacing(8)
        lo.addStretch()

        self.first = QPushButton("« Pertama")
        self.prev = QPushButton("‹ Sebelum")
        self.info = QLabel("")
        self.next = QPushButton("Seterusnya ›")
        self.last = QPushButton("Akhir »")

        for b in (self.first, self.prev, self.next, self.last):
            b.setObjectName("ghost")
            b.setCursor(Qt.PointingHandCursor)

        self.info.setObjectName("muted")
        self.info.setAlignment(Qt.AlignCenter)
        self.info.setMinimumWidth(110)

        self.first.clicked.connect(lambda: self._go(1))
        self.prev.clicked.connect(lambda: self._go(self._page - 1))
        self.next.clicked.connect(lambda: self._go(self._page + 1))
        self.last.clicked.connect(lambda: self._go(self._last))

        for w in (self.first, self.prev, self.info, self.next, self.last):
            lo.addWidget(w)

        lo.addStretch()

    def _go(self, p: int):
        p = max(1, min(p, self._last))
        if p != self._page:
            self._page = p
            self._on_page(p)

    def set_state(self, page: int, last: int):
        self._page, self._last = page, max(1, last)
        self.info.setText(f"{page} / {self._last}")
        self.first.setEnabled(page > 1)
        self.prev.setEnabled(page > 1)
        self.next.setEnabled(page < self._last)
        self.last.setEnabled(page < self._last)
        self.setVisible(self._last > 1)


class LangTabs(QWidget):
    """Pemilih bahasa untuk halaman detail: Melayu | Indonesia | English.

    Tiga tab sahaja -- keputusan mockup Sesi 55. Tab "Sebelah"
    (bandingan Melayu vs Indonesia) DIBUANG: ia bukan dalam mockup,
    dan teks terjemahan di dalamnya tidak sama paras dengan teks Arab.
    """

    def __init__(self, on_change, parent=None):
        super().__init__(parent)
        self._on_change = on_change
        self._active = "melayu"
        self._btns = {}
        self._susunan = ["melayu", "indonesia", "english"]
        # 0 (bukan len) supaya kemas_lebar PERTAMA sentiasa membina
        # baris — butang hanya dimasukkan ke layout dalam kemas_lebar.
        self._n_baris1 = 0

        # DUA baris (responsif 18 Ogos): baris 1 = tab utama, baris 2 =
        # baki tab bila lajur terlalu sempit (fon besar/DPI tinggi).
        # `kemas_lebar()` memindahkan tab antara baris -- corak sama
        # `_kemas_tajuk_detail` (removeWidget/addWidget auto-reparent).
        lo = QVBoxLayout(self)
        lo.setContentsMargins(0, 0, 0, 0)
        lo.setSpacing(4)
        self._r1 = QHBoxLayout()
        self._r1.setContentsMargins(0, 0, 0, 0)
        self._r1.setSpacing(6)
        self._r2 = QHBoxLayout()
        self._r2.setContentsMargins(0, 0, 0, 0)
        self._r2.setSpacing(6)
        lo.addLayout(self._r1)
        lo.addLayout(self._r2)

        for key, label in [("melayu", "Melayu"),
                           ("indonesia", "Indonesia"),
                           ("english", "English")]:
            b = QPushButton(label)
            b.setObjectName("filterChip")
            b.setCursor(Qt.PointingHandCursor)
            b.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
            b.clicked.connect(lambda _, k=key: self.set_active(k))
            self._btns[key] = b
        self.kemas_lebar(10 ** 6)
        self.set_active("melayu", emit=False)

    def kemas_lebar(self, lebar: float):
        """Susun tab ikut lebar tersedia: satu baris bila cukup, bungkus
        baki tab ke baris 2 (dijajarkan kanan) bila sempit.

        n = bilangan tab terbanyak yang muat pada baris 1; minimum 1
        (tab pertama kekal kelihatan walau apa pun). Idempoten -- tiada
        kerja bila n tidak berubah. Butang kekal (bukan dibina semula),
        hanya dipindah antara layout.
        """
        n = 0
        jumlah = 0
        for k in self._susunan:
            w = self._btns[k].sizeHint().width()
            if n:
                w += self._r1.spacing()
            if jumlah + w > lebar:
                break
            jumlah += w
            n += 1
        n = max(1, n)
        if n == self._n_baris1:
            return
        self._n_baris1 = n
        while self._r1.count():
            self._r1.takeAt(0)
        while self._r2.count():
            self._r2.takeAt(0)
        for k in self._susunan[:n]:
            self._r1.addWidget(self._btns[k])
        self._r1.addStretch(1)
        for k in self._susunan[n:]:
            self._r2.addWidget(self._btns[k])
        self._r2.addStretch(1)
        self._r1.invalidate()
        self._r2.invalidate()
        lo = self.layout()
        lo.invalidate()
        lo.activate()

    def set_active(self, key: str, emit: bool = True):
        self._active = key
        for k, b in self._btns.items():
            b.setObjectName("filterChip_active" if k == key else "filterChip")
            b.style().unpolish(b)
            b.style().polish(b)
        if emit:
            self._on_change(key)

    def set_available(self, keys: set):
        """Kelabukan bahasa yang tiada data."""
        for k, b in self._btns.items():
            b.setEnabled(k in keys)

    def active(self) -> str:
        return self._active


def empty_state(icon: str, title: str, subtitle: str = "") -> QWidget:
    """Paparan 'tiada apa-apa di sini'.

    Widget ini MENGEMBANG menegak dan memusatkan kandungannya. Sebelum
    ini ia Fixed dan melekat di atas, meninggalkan 401px kosong di
    bawah pada halaman Tersimpan yang kosong -- kelihatan seperti
    paparan rosak, bukan keadaan kosong yang disengajakan.
    """
    w = QWidget()
    w.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    lo = QVBoxLayout(w)
    # JANGAN guna lo.setAlignment(Qt.AlignCenter): ia meruntuhkan
    # layout kepada tinggi kandungan dan MELEKATKANNYA di atas --
    # 223px kekal kosong di bawah. Stretch atas+bawah memusatkan
    # dengan betul dalam ruang yang ada.
    lo.setContentsMargins(0, 20, 0, 20)
    lo.setSpacing(10)
    lo.addStretch(1)

    i = QLabel(icon)
    i.setStyleSheet("font-size: 52px;")
    i.setAlignment(Qt.AlignCenter)
    lo.addWidget(i)

    t = QLabel(title)
    t.setObjectName("h3")
    t.setAlignment(Qt.AlignCenter)
    lo.addWidget(t)

    if subtitle:
        s = QLabel(subtitle)
        s.setObjectName("muted")
        s.setAlignment(Qt.AlignCenter)
        s.setWordWrap(True)
        lo.addWidget(s)

    lo.addStretch(1)
    return w


def breadcrumb(items: list) -> QWidget:
    """items = [(label, callback|None), ...]; item akhir = teks biasa."""
    w = QWidget()
    # Fixed menegak: tanpa ini breadcrumb menyerap ruang lebihan
    # layout dan meregang 30px -> 227px (diukur), menolak senarai
    # hadis jauh ke bawah.
    w.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
    lo = QHBoxLayout(w)
    lo.setContentsMargins(0, 8, 0, 8)
    lo.setSpacing(4)

    for i, (label, cb) in enumerate(items):
        if i:
            sep = QLabel("›")
            sep.setObjectName("faint")
            lo.addWidget(sep)
        if cb:
            b = QPushButton(label)
            b.setObjectName("nav")
            b.setCursor(Qt.PointingHandCursor)
            b.clicked.connect(lambda _, c=cb: c())
            lo.addWidget(b)
        else:
            l = QLabel(label)
            l.setObjectName("h3")
            lo.addWidget(l)
    lo.addStretch()
    return w
