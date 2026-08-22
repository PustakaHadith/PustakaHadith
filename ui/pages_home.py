"""Halaman Utama — mixin PustakaApp (Sesi 30).

Dipisahkan dari `ui/app_qt.py`. Kelas `PagesHome` menyediakan halaman
Utama: hero dengan bar carian pantas, kiraan koleksi dan grid 9 kad
kitab. Digabungkan ke `PustakaApp` melalui MRO:
`class PustakaApp(..., PagesHome, QMainWindow)`.

GANDINGAN RENTAS MIXIN: modul ini TIDAK berdiri sendiri —
`_page_home` memanggil `open_kitab` (PagesKitab) dan `_from_home_search`
memanggil `_buka_hadis_terus` (PagesKitab/PagesCarian; carian khusus
kitab + nombor terus ke butiran, Sesi 38) serta `_do_search`
(PagesCarian). Mesti digabungkan bersama semua mixin halaman.

Peraturan tema: modul ini TIDAK import warna dari `ui.theme` (hanya
COLLECTION_META, metadata kitab), namun didaftar dalam `_THEMED_MODULES`
(ui/theme.py) untuk konsisten dengan modul UI yang lain.
"""

from __future__ import annotations

from PyQt5.QtCore import QEvent, Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (
    QFrame, QGraphicsDropShadowEffect, QGridLayout, QHBoxLayout, QLabel,
    QVBoxLayout, QWidget,
)

from ui.helpers import _parse_lompat
from ui.pages import Hero, KitabCard, SearchBar, _campur
from ui.theme import COLLECTION_META, TEAL, is_dark
from ui.widgets import attach_copy_menu, centered_column, make_scroll


class BungkusTimbul(QFrame):
    """Pembungkus lutsinar yang memberi kesan timbul (bayang) pada hover.

    MENGAPA BUNGKUS: QGraphicsDropShadowEffect TIDAK dirender pada widget
    dengan latar QSS (`QFrame#card`) -- diukur fizikal 16 Ogos: 0 piksel
    bayang. Efek berfungsi bila dipasang pada widget TANPA stylesheet;
    di sini pembungkus lutsinar membawa efek, kad QSS kekal di dalam.
    """

    def __init__(self, child: QWidget, warna=None, parent=None):
        super().__init__(parent)
        self.setStyleSheet("")
        lo = QVBoxLayout(self)
        # Margin bawah 13px memberi ruang glow; atas/kiri/kanan 2px kekal
        # asal supaya halaman utama muat 730px (semak.py: +3px/baris sahaja).
        lo.setContentsMargins(2, 2, 2, 12)
        lo.addWidget(child)
        self._bayang = None
        self._kanak = child
        # Tema gelap: bayang HITAM atas latar gelap tidak kelihatan
        # (diukur fizikal 16 Ogos) -- pilih glow untuk tema gelap,
        # bayang hitam klasik untuk tema terang. Glow ikut warna kitab
        # (border kad) supaya hover koheren: Bukhari hijau, Muslim biru.
        self._gelap = is_dark()
        self._warna = warna or TEAL
        # PENTING: kad (anak) menutupi pembungkus, jadi peristiwa
        # Enter/Leave tetikus pergi ke KAD, bukan pembungkus -- bayang
        # hanya muncul jika tetikus tepat di margin 6px (diukur fizikal
        # 16 Ogos: 0 piksel berbeza selepas hover kad). Penapis peristiwa
        # pada kad membolehkan hover kad mencetuskan kesan timbul.
        child.installEventFilter(self)

    def _cipta_efek(self):
        """Cipta + pasang efek bayang/glow (sekali sahaja sehingga dibuang)."""
        if self._bayang is None:
            self._bayang = QGraphicsDropShadowEffect(self)
            if self._gelap:
                # Glow ikut warna kitab (dicerahkan) -- kelihatan atas
                # latar gelap, kesan "timbul" jelas. Ditala fizikal 16
                # Ogos: alpha 200 + blur 8 + offset (0,1) memberi cincin
                # jelas (#304d3c untuk Bukhari).
                c = QColor(_campur(self._warna, (255, 255, 255), 0.5))
                c.setAlpha(200)
                self._bayang.setBlurRadius(8)
                self._bayang.setOffset(0, 1)
            else:
                # Bayang hitam klasik atas permukaan terang.
                c = QColor(0, 0, 0, 150)
                self._bayang.setBlurRadius(16)
                self._bayang.setOffset(0, 4)
            self._bayang.setColor(c)
            self.setGraphicsEffect(self._bayang)

    def eventFilter(self, obj, ev):
        # Hover pada KAD (bukan margin pembungkus) -> kesan timbul.
        if obj is self._kanak:
            if ev.type() == QEvent.Enter:
                self._cipta_efek()
            elif ev.type() == QEvent.Leave:
                self._buang_bayang()
        return super().eventFilter(obj, ev)

    def _buang_bayang(self):
        """Buang efek bayang dengan selamat.

        setGraphicsEffect(None) SUDAH memadam efek lama (Qt ambil milik +
        padam bila diganti) -- jangan panggil deleteLater kedua.
        PENTING: efek MESTI dibuang sebelum navigasi halaman. Efek
        QGraphicsEffect yang aktif semasa QStackedWidget.setCurrentIndex
        menyembunyikan halaman mencetuskan ranap native (access
        violation, diukur fizikal 16 Ogos: klik kad Muslim selepas hover
        -> open_kitab -> go() -> setCurrentIndex ranap).
        """
        if self._bayang is not None:
            self.setGraphicsEffect(None)
            self._bayang = None

    def enterEvent(self, e):
        # Fallback margin pembungkus (jarang berlaku -- kad menutupi).
        self._cipta_efek()
        super().enterEvent(e)

    def leaveEvent(self, e):
        self._buang_bayang()
        super().leaveEvent(e)

    def hideEvent(self, e):
        # Halaman bertukar (QStackedWidget menyembunyikan halaman lama) --
        # buang efek sebelum ia disembunyikan untuk elak ranap native.
        self._buang_bayang()
        super().hideEvent(e)


class PagesHome:
    def _buang_bayang_semua(self):
        """Buang efek bayang pada SEMUA pembungkus kad kitab.

        Dipanggil dari `go()` SEBELUM setCurrentIndex -- laluan navigasi
        tunggal. Efek QGraphicsEffect yang aktif pada kad semasa halaman
        ditukar mencetuskan ranap native (access violation dalam
        QStackedWidget.setCurrentIndex; diukur fizikal 16 Ogos: hover + 
        klik kad Muslim ranap).
        """
        for b in getattr(self, "_kitab_bungkus", ()):
            b._buang_bayang()

    # ── HALAMAN: Utama ───────────────────────────────────────────────
    def _page_home(self):
        sa = make_scroll()
        self.stack.addWidget(sa)
        body = QWidget()
        body.setObjectName("page")
        sa.setWidget(body)
        bl = QVBoxLayout(body)
        bl.setContentsMargins(0, 0, 0, 14)
        bl.setSpacing(0)

        hero = Hero("Portal & Aplikasi Carian Hadis",
                    '"Sesungguhnya amal itu bergantung kepada niat."\n'
                    '(Riwayat al-Bukhari & Muslim)',
                    compact=True)
        self.home_search = SearchBar("Cari hadis… (cth. bukhari 433, B433)")
        self.home_search.setMaximumWidth(900)
        w = QWidget()
        wl = QHBoxLayout(w)
        wl.setContentsMargins(0, 0, 0, 0)
        wl.addStretch(1)
        wl.addWidget(self.home_search, 20)
        wl.addStretch(1)
        hero.body.addWidget(w)

        self._home_count = QLabel("Memuatkan koleksi…")
        self._home_count.setObjectName("faint")
        self._home_count.setAlignment(Qt.AlignCenter)
        hero.body.addWidget(self._home_count)
        bl.addWidget(hero)

        attach_copy_menu(self.home_search.input)
        self.home_search.btn.clicked.connect(self._from_home_search)
        self.home_search.input.returnPressed.connect(self._from_home_search)

        col, cl = centered_column()
        cl.setContentsMargins(0, 8, 0, 0)
        t = QLabel("Koleksi Kitab Hadis")
        t.setObjectName("h2")
        t.setAlignment(Qt.AlignCenter)
        cl.addWidget(t)
        cl.addSpacing(4)

        grid = QGridLayout()
        grid.setSpacing(5)
        self._kitab_cards = {}
        self._kitab_bungkus = []
        for i, (slug, meta) in enumerate(COLLECTION_META.items()):
            c = KitabCard(slug, meta, self._total_of(slug))
            b = BungkusTimbul(c, warna=meta.get("warna"))
            # Efek bayang MESTI dibuang sebelum navigasi -- efek aktif
            # pada kad yang diklik (hover) mencetuskan ranap native dalam
            # QStackedWidget.setCurrentIndex (diukur fizikal 16 Ogos).
            # Perlindungan di `go()` melalui `_buang_bayang_semua()`.
            c.clicked.connect(lambda s=slug: self.open_kitab(s))
            self._kitab_bungkus.append(b)
            # Pembungkus lutsinar supaya kesan timbul (bayang) pada hover
            # dirender -- QSS kad tidak menyokong QGraphicsDropShadowEffect.
            grid.addWidget(b, i // 3, i % 3)
            self._kitab_cards[slug] = c
        cl.addLayout(grid)
        bl.addWidget(col)
        bl.addStretch(1)

    def _from_home_search(self):
        q = self.home_search.text()
        if not q:
            return
        # Carian pantas (sama seperti halaman Carian): 'bukhari 433' atau
        # '433' SAHAJA -> buka butiran hadis TERUS (Sesi 38) — carian
        # khusus membawa terus ke detail, bukan senarai. Nombor sahaja
        # guna chip kitab terpilih, jika ada, atau kitab terakhir dibuka;
        # butang Kembali menuju ke Utama.
        j = _parse_lompat(q, default_slug=self.home_search.slug()
                          or self._kitab_slug)
        if j:
            slug, n = j
            self._buka_hadis_terus(slug, n, dari="home")
            return
        self.search_bar.input.setText(q)
        if self.search_bar.chips:
            self.search_bar.chips.set_active(self.home_search.slug(), emit=False)
        self.go("search")
        self._do_search(1)
