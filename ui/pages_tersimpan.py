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
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QWidget

from ui.helpers import _clear
from ui.pages import Hero, empty_state
from ui.widgets import centered_column, hadith_card, make_scroll


class PagesTersimpan:
    def _page_saved(self):
        sa = make_scroll()
        self.stack.addWidget(sa)
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
        body.setObjectName("page")
        sa.setWidget(body)
        self._saved_root = QVBoxLayout(body)
        self._saved_root.setContentsMargins(0, 0, 0, 16)
        self._saved_root.setSpacing(0)

    def _render_saved(self):
        _clear(self._saved_root)
        self._saved_root.addWidget(Hero(
            "Hadis Tersimpan",
            subtitle=f"{len(self.bookmarks)} hadis disimpan", compact=True))

        col, cl = centered_column()
        cl.setContentsMargins(0, 18, 0, 0)
        if not self.bookmarks:
            # stretch=1 supaya empty_state mengisi & berpusat menegak
            cl.addWidget(empty_state(
                "⭐", "Belum ada hadis tersimpan",
                "Buka mana-mana hadis dan tekan Simpan."), 1)
        else:
            for b in reversed(self.bookmarks):
                h = {"id": b.get("id"), "collection": b.get("slug"),
                     "arab": b.get("arab", ""), "melayu": b.get("melayu", ""),
                     "indonesia": b.get("indonesia", ""),
                     "book": b.get("book"), "nama_bab": b.get("nama_bab", "")}
                c = hadith_card(h, b.get("kitab_name", ""), self.ar_scale,
                                show_chip=True, arabic_font=self.ar_font,
                                papar_melayu=self._papar_melayu)
                c.clicked.connect(
                    lambda s=b.get("slug"), i=b.get("id"): self.open_by_ref(s, i))
                cl.addWidget(c)
        # Bila kosong, kolum mesti MENGEMBANG supaya empty_state
        # berpusat; bila ada tanda buku, stretch biasa di hujung.
        if not self.bookmarks:
            self._saved_root.addWidget(col, 1)
        else:
            self._saved_root.addWidget(col)
            self._saved_root.addStretch(1)

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
