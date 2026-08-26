"""Halaman Tersimpan (penanda buku) — mixin PustakaApp (Sesi 30).

Dipisahkan dari `ui/app_qt.py`. Kelas `PagesTersimpan` menyediakan
halaman "Hadis Tersimpan": senarai penanda buku (`self.bookmarks`)
dipaparkan sebagai kad hadis. Digabungkan ke `PustakaApp` melalui MRO:
`class PustakaApp(..., PagesTersimpan, ..., QMainWindow)`.

GANDINGAN RENTAS MIXIN: modul ini TIDAK berdiri sendiri —
`_render_saved` memanggil `open_by_ref` (buka butiran hadis) yang
tinggal dalam `PagesDetail`. Mesti digabungkan bersama PagesDetail.

Peraturan tema: modul ini TIDAK import warna dari `ui.theme` (hanya
widget), namun didaftar dalam `_THEMED_MODULES` (ui/theme.py) untuk
konsisten dengan modul UI yang lain.
"""

from __future__ import annotations

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import (
    QHBoxLayout, QLabel, QPushButton, QSizePolicy, QVBoxLayout, QWidget,
)

from ui.helpers import _clear
from ui.pages import Hero, empty_state
from ui.theme import ada_latar_imej
from ui.widgets import BackgroundCanvas, hadith_card_dwibahasa, make_scroll


class PagesTersimpan:
    def _page_saved(self):
        # Latar: BackgroundCanvas (glob garisan masa AQUA / warna pepejal
        # tema lain) — pola sama Utama/Carian/Senarai. Skrol telus di
        # dalam supaya glob kekal TETAP semasa skrol.
        kanvas = BackgroundCanvas()
        self.stack.addWidget(kanvas)
        sa = make_scroll(kanvas)
        sa.setObjectName("savedScroll")
        self._tersimpan_sa = sa

        # Butang terapung "↑ ke atas" (Sesi 34) — corak sama halaman
        # kitab/carian: kelihatan bila senarai tanda buku panjang dan
        # pengguna skrol ke bawah; klik untuk kembali ke atas dengan
        # animasi lancar. Anak kepada QScrollArea supaya ia terapung.
        if getattr(self, "_top_timer_tersimpan", None) is not None:
            self._top_timer_tersimpan.stop()
        self._tersimpan_top_btn = QPushButton("↑")
        self._tersimpan_top_btn.setObjectName("backTop")
        self._tersimpan_top_btn.setToolTip("Ke atas — hadis pertama")
        self._tersimpan_top_btn.setCursor(Qt.PointingHandCursor)
        self._tersimpan_top_btn.setFixedSize(44, 44)
        self._tersimpan_top_btn.setParent(sa)
        self._tersimpan_top_btn.clicked.connect(
            self._skrol_atas_lancar_tersimpan)
        self._tersimpan_top_btn.hide()
        sa.verticalScrollBar().valueChanged.connect(
            self._kemas_butang_atas_tersimpan)
        _orig_resize = sa.resizeEvent

        def _on_resize(e):
            _orig_resize(e)
            self._kemas_butang_atas_tersimpan()

        sa.resizeEvent = _on_resize

        body = QWidget()
        body.setObjectName("homeBody")
        sa.setWidget(body)
        bl = QVBoxLayout(body)
        bl.setContentsMargins(0, 0, 0, 16)
        bl.setSpacing(0)

        hero = Hero("Hadis Tersimpan", compact=True)
        # Aqua Glass: hero telus supaya glob tembus (hanya teks atas glob).
        if ada_latar_imej():
            hero.setStyleSheet(
                "QFrame#hero { background: transparent; border: none; }")
        self._saved_sub = QLabel("")
        self._saved_sub.setObjectName("muted")
        self._saved_sub.setAlignment(Qt.AlignCenter)
        hero.body.addWidget(self._saved_sub)
        bl.addWidget(hero)

        # Lajur kandungan berpusat (TELUS — biar glob AQUA kelihatan).
        col = QWidget()
        col.setObjectName("homeBody")
        col.setMaximumWidth(960)
        col.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        cl = QVBoxLayout(col)
        cl.setContentsMargins(0, 18, 0, 0)
        cl.setSpacing(0)
        self._saved_col = cl
        wrap = QWidget()
        wl = QHBoxLayout(wrap)
        wl.setContentsMargins(0, 0, 0, 0)
        wl.addStretch(1)
        wl.addWidget(col, 0, Qt.AlignTop)
        wl.addStretch(1)
        bl.addWidget(wrap)

        vl = QVBoxLayout(kanvas)
        vl.setContentsMargins(0, 0, 0, 0)
        vl.addWidget(sa)

    def _render_saved(self):
        _clear(self._saved_col)
        n = len(self.bookmarks)
        self._saved_sub.setText(
            f"{n} hadis disimpan" if n else "Tiada hadis disimpan")

        if not self.bookmarks:
            # stretch=1 supaya empty_state mengisi & berpusat menegak
            self._saved_col.addWidget(empty_state(
                "⭐", "Belum ada hadis tersimpan",
                "Buka mana-mana hadis dan tekan Simpan."), 1)
            return

        for b in reversed(self.bookmarks):
            slug = b.get("slug")
            hid = b.get("id")
            h = {"collection": slug, "id": hid,
                  "arab": b.get("arab", ""), "melayu": b.get("melayu", ""),
                  "indonesia": b.get("indonesia", ""),
                  "book": b.get("book"), "nama_bab": b.get("nama_bab", "")}
            c = hadith_card_dwibahasa(
                h, b.get("kitab_name", ""), self.ar_scale,
                arabic_font=self.ar_font, tersimpan=True,
                papar_melayu=self._papar_melayu)
            c._hid = hid
            c.clicked.connect(
                lambda s=slug, i=hid: self.open_by_ref(s, i))
            c.simpan_clicked.connect(
                lambda _, s=slug, i=hid: self._bookmark_toggle(s, i))
            self._saved_col.addWidget(c)
        self._saved_col.addStretch(1)

    def _bookmark_toggle(self, slug, hid):
        """Buang/masuk semula tanda buku terus dari halaman Tersimpan."""
        self._toggle_save({"collection": slug, "id": hid})
        self._render_saved()

    def _kemas_butang_atas_tersimpan(self):
        """Tunjuk/sembunyi butang ↑ mengikut kedudukan skrol (Sesi 34).

        Corak sama halaman kitab/carian: butang hanya berguna bila
        senarai melebihi viewport dan pengguna sudah skrol ke bawah
        (melebihi 250px). Di kedudukan atas ia disembunyikan supaya
        tidak menghalang kandungan.
        """
        b = getattr(self, "_tersimpan_top_btn", None)
        sa = getattr(self, "_tersimpan_sa", None)
        if b is None or sa is None:
            return
        bar = sa.verticalScrollBar()
        if bar.maximum() <= 0 or bar.value() < 250:
            b.hide()
            return
        m = 18
        b.move(sa.viewport().width() - b.width() - m,
               sa.viewport().height() - b.height() - m)
        b.show()
        b.raise_()

    def _skrol_atas_lancar_tersimpan(self):
        """Skrol lancar ke atas senarai tanda buku — animasi QTimer.

        Langkah mengecil (jarak dibahagi 15) supaya pergerakan kelihatan
        perlahan berhampiran sasaran. Timer disimpan pada `self` supaya
        panggilan kedua menghentikan animasi pertama.
        """
        bar = self._tersimpan_sa.verticalScrollBar()
        mula = bar.value()
        if mula <= 0:
            return
        t = getattr(self, "_top_timer_tersimpan", None)
        if t is not None:
            t.stop()
        t = QTimer(self)
        self._top_timer_tersimpan = t
        langkah = max(1, mula // 15)

        def _langkah():
            if t is not self._top_timer_tersimpan:
                return
            v = bar.value()
            if v <= langkah:
                bar.setValue(0)
                t.stop()
            else:
                bar.setValue(v - langkah)

        t.setInterval(16)
        t.timeout.connect(_langkah)
        t.start()
