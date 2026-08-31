"""Halaman Carian (keyword + semantik) — mixin PustakaApp (Sesi 30).

Dipisahkan dari `ui/app_qt.py`. Kelas `PagesCarian` menyediakan kaedah
halaman carian: bar carian, lompat pantas, carian gabungan (FTS5
keyword + semantik AI), draf jawapan dan paparan hasil. Digabungkan ke
`PustakaApp` melalui MRO: `class PustakaApp(PagesKitab, PagesCarian,
QMainWindow)`.

PENTING — tema: modul ini import WARNA dari `ui.theme`
(AMBER_BG/AMBER_TEXT/AMBER_BORDER) untuk lencana amaran. Ia MESTI
didaftar dalam `_THEMED_MODULES` (ui/theme.py) supaya `apply_theme()`
menyalin nilai terkini ke ruang namanya semasa tukar tema.

GANDINGAN RENTAS MIXIN: modul ini TIDAK berdiri sendiri — `_hantar_carian`
memanggil `_buka_hadis_terus` (carian khusus kitab + nombor terus ke
butiran, Sesi 38) yang memanggil `_sahkan_lompat` yang tinggal dalam
`PagesKitab`. Mesti digabungkan bersama:
`PustakaApp(PagesKitab, PagesCarian, QMainWindow)`.
"""

from __future__ import annotations

import time

from PyQt5.QtCore import QEvent, Qt, QTimer
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import (
    QFrame, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QScrollArea, QShortcut, QSizePolicy, QVBoxLayout, QWidget,
)

from ui.helpers import _clear, _parse_lompat, read_history
from ui.pages import Hero, Pager, SearchBar, empty_state
from ui.deklarasi import SEMAKHADIS_URL
from ui.theme import (
    AMBER_BG, AMBER_BORDER, AMBER_TEXT, COLLECTION_META, GUTTER, TEXT_MUTED,
    ada_latar_imej,
)
from ui.widgets import (
    BackgroundCanvas, ClickCard, attach_copy_menu, elide,
    hadith_card_dwibahasa, make_scroll, text_browser,
)
from ui.workers import SearchWorker, SemanticWorker

# Bilangan kad setiap halaman pada panel hasil carian (paginasi klien).
CARIAN_PER_PAGE = 24


class PagesCarian:
    # ── HALAMAN: Carian ──────────────────────────────────────────────
    def _page_search(self):
        # Latar: BackgroundCanvas (glob AQUA / warna pepejal tema lain) —
        # pola sama Utama/rak/kitab. Skrol berlaku pada QScrollArea TELUS
        # di dalamnya supaya glob kekal TETAP (parallax) semasa skrol.
        kanvas = BackgroundCanvas()
        self.stack.addWidget(kanvas)
        sa = make_scroll(kanvas)
        sa.setObjectName("homeScroll")
        self._search_sa = sa

        # Butang terapung "↑ ke atas" (Sesi 34) — sama seperti halaman
        # kitab: kelihatan bila pengguna skrol ke bawah senarai hasil;
        # klik untuk kembali ke atas dengan animasi lancar. Guna
        # objectName "backTop" (QSS dalam theme.py) yang sama supaya
        # gaya konsisten merentas kedua-dua halaman.
        if getattr(self, "_top_timer_carian", None) is not None:
            self._top_timer_carian.stop()
        self._search_top_btn = QPushButton("↑")
        self._search_top_btn.setObjectName("backTop")
        self._search_top_btn.setToolTip("Ke atas — hadis pertama")
        self._search_top_btn.setCursor(Qt.PointingHandCursor)
        self._search_top_btn.setFixedSize(44, 44)
        self._search_top_btn.setParent(sa)
        self._search_top_btn.clicked.connect(self._skrol_atas_lancar_carian)
        self._search_top_btn.hide()
        sa.verticalScrollBar().valueChanged.connect(
            self._kemas_butang_atas_carian)
        _orig_resize = sa.resizeEvent

        def _on_resize(e):
            _orig_resize(e)
            self._kemas_butang_atas_carian()

        sa.resizeEvent = _on_resize

        body = QWidget()
        body.setObjectName("homeBody")
        sa.setWidget(body)
        bl = QVBoxLayout(body)
        bl.setContentsMargins(0, 0, 0, 16)
        bl.setSpacing(0)

        hero = Hero("Pencarian Hadis", compact=True)
        # Aqua Glass: hero telus supaya glob tembus (hanya teks atas glob).
        if ada_latar_imej():
            hero.setStyleSheet(
                "QFrame#hero { background: transparent; border: none; }")
        self.search_bar = SearchBar("Cari hadis… (cth. bukhari 433, B433)")
        self.search_bar.setMaximumWidth(900)
        w = QWidget()
        wl = QHBoxLayout(w)
        wl.setContentsMargins(0, 0, 0, 0)
        wl.addStretch(1)
        wl.addWidget(self.search_bar, 20)
        wl.addStretch(1)
        hero.body.addWidget(w)
        bl.addWidget(hero)

        attach_copy_menu(self.search_bar.input)
        self.search_bar.btn.clicked.connect(self._hantar_carian)
        self.search_bar.input.returnPressed.connect(self._hantar_carian)
        self.search_bar.input.textChanged.connect(self._on_carian_text_changed)
        if getattr(self, "_esc_sc", None) is None:
            self._esc_sc = QShortcut(Qt.Key_Escape, self)
            self._esc_sc.activated.connect(
                lambda: (self.search_bar.input.clear(),
                         self.search_bar.input.setFocus()))
        if self.search_bar.chips:
            self.search_bar.chips.changed.connect(
                lambda _: self._do_search(1) if self._search_q else None)

        # Kekalkan jarak tepi supaya split (sidebar + panel) seragam dengan
        # halaman Senarai Hadis.
        bl.setContentsMargins(24, 16, 24, 16)

        # ── Toolbar: togol kaedah + status (jam berputar) ─────────────
        self._carian_bab = None
        self._carian_hasil = []
        self._carian_bab_rows = []
        self._carian_tapis = "semua"
        self._carian_urutan = "asc"

        tb = QWidget()
        tl = QHBoxLayout(tb)
        tl.setContentsMargins(0, 0, 0, 0)
        tl.setSpacing(10)
        self.search_info = QLabel("")
        self.search_info.setObjectName("muted")
        self.search_info.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        tl.addWidget(self.search_info)
        self._carian_sibuk = QLabel("🕐")
        self._carian_sibuk.setStyleSheet("font-size: 16px;")
        self._carian_sibuk.hide()
        self._jam = ["🕐", "🕑", "🕒", "🕓", "🕔", "🕕",
                     "🕖", "🕗", "🕘", "🕙", "🕚", "🕛"]
        self._jam_i = 0
        if getattr(self, "_carian_timer", None) is not None:
            self._carian_timer.stop()
        self._carian_timer = QTimer(self)
        self._carian_timer.setInterval(120)
        self._carian_timer.timeout.connect(self._putar_jam)
        tl.addWidget(self._carian_sibuk)
        tl.addStretch(1)
        bl.addWidget(tb)

        # ── Split: sidebar (bab) + panel (hasil), macam Senarai Hadis ─
        baris = QWidget()
        hl = QHBoxLayout(baris)
        hl.setContentsMargins(0, 0, 0, 0)
        hl.setSpacing(16)
        self._carian_side_frame = self._bina_carian_sidebar()
        hl.addWidget(self._carian_side_frame)
        hl.addWidget(self._bina_carian_panel(), 1)
        hl.setAlignment(Qt.AlignTop)
        bl.addWidget(baris)

        # Kanvas perlu mengisi ruang: letakkan scroll-area telus di dalamnya.
        vl = QVBoxLayout(kanvas)
        vl.setContentsMargins(0, 0, 0, 0)
        vl.addWidget(sa)

        # Keadaan awal (tiada carian): placeholder di panel.
        self._carian_list.addWidget(
            empty_state("🔍", "Cari hadis",
                        "Masukkan kata kunci untuk mencari dalam 62,169 hadis."))

    def _bina_togol_kaedah(self) -> QWidget:
        """Baris togol kaedah carian: Kata kunci / Makna / Kedua-dua.

        Pilihan disimpan ke `carian_mod` (user_settings.json) dan dibaca
        semula bila halaman dibina semula (tukar tema). Lalai "kedua".
        """
        row = QWidget()
        rl = QHBoxLayout(row)
        rl.setContentsMargins(0, 0, 0, 0)
        rl.setSpacing(8)
        label = QLabel("Kaedah carian")
        label.setObjectName("muted")
        rl.addWidget(label)
        self._mod_chips = {}
        for val, txt in (("kata", "Kata kunci"), ("makna", "Makna"),
                         ("kedua", "Kedua-dua")):
            b = QPushButton(txt)
            b.setObjectName("filterChip")
            b.setCursor(Qt.PointingHandCursor)
            b.clicked.connect(lambda _, v=val: self._set_mod_carian(v))
            self._mod_chips[val] = b
            rl.addWidget(b)
        rl.addStretch(1)
        self._kemas_mod_carian()
        return row

    def _kemas_mod_carian(self):
        """Tanda butang aktif ikut `carian_mod` (unpolish/polish = segar)."""
        aktif = self.settings.get("carian_mod", "kedua")
        for v, b in self._mod_chips.items():
            b.setObjectName("filterChip_active" if v == aktif else "filterChip")
            b.style().unpolish(b)
            b.style().polish(b)

    def _set_mod_carian(self, v: str):
        """Tukar kaedah carian + kekalkan pilihan dalam tetapan."""
        if self.settings.get("carian_mod", "kedua") == v:
            return
        self.settings["carian_mod"] = v
        try:
            from ui.pages_tetapan import SETTINGS, _write_json
            _write_json(SETTINGS, self.settings)
        except Exception:
            pass
        self._kemas_mod_carian()
        # Cari semula dengan mod baharu bila ada query aktif.
        if getattr(self, "_search_q", ""):
            self._do_search(1)

    def _tambah_kad_carian(self, h, slug, hid):
        """Tambah satu kad dwibahasa ke panel hasil carian (lajur tunggal).

        `h` dinormalisasi (salinan) supaya `id`/`collection` wujud untuk
        kad, simpan (🔖) dan buka butiran. Kitab ditunjukkan dalam meta kad.
        """
        h = dict(h)
        h.setdefault("collection", slug)
        h.setdefault("id", hid)
        name = COLLECTION_META.get(slug, {}).get("name", slug)
        c = hadith_card_dwibahasa(
            h, name, self.ar_scale, arabic_font=self.ar_font,
            tersimpan=self._is_saved(slug, hid),
            papar_melayu=self._papar_melayu)
        c._hid = hid
        c.clicked.connect(lambda hh=h: self.open_detail(hh, "search"))
        c.simpan_clicked.connect(
            lambda _, hh=h, cc=c, s=slug, i=hid:
            self._carian_toggle_simpan(hh, cc, s, i))
        self._carian_list.addWidget(c)

    def _on_carian_text_changed(self, teks):
        """Medan kosong (✕ asli / Esc / padam) -> kosongkan hasil."""
        if not teks:
            self._carian_clear()

    def _carian_clear(self):
        self._search_q = ""
        self._search_slug = None
        self._search_page = 1
        self._carian_bab = None
        self._carian_hasil = []
        self._clear_carian_list()
        self._carian_reset_sidebar()
        self._carian_kemas_info(None, 0)
        self.search_info.setText("")
        try:
            self._carian_pager.hide()
        except Exception:
            pass

    def _clear_carian_list(self):
        """Buang semua widget hasil carian dari panel (kekalkan pager)."""
        lay = self._carian_list
        while lay.count():
            it = lay.takeAt(0)
            w = it.widget()
            if w is not None:
                w.deleteLater()

    def _carian_reset_sidebar(self):
        """Kosongkan senarai bab (stretch diletak di bawah oleh pemanggil)."""
        bek = getattr(self, "_carian_bab_bekas", None)
        if bek is None:
            return
        while bek.count():
            it = bek.takeAt(0)
            w = it.widget()
            if w is not None:
                w.deleteLater()

    def _bina_carian_sidebar(self) -> QFrame:
        # Padanan struktur sidebar page Senarai Hadis (_kitab_sidebar):
        # kad info + "BAB DALAM KEPUTUSAN" + go box lompat no. hadis.
        s = QFrame()
        s.setObjectName("glassPanel")
        s.setFixedWidth(300)
        sl = QVBoxLayout(s)
        sl.setContentsMargins(16, 14, 16, 14)
        sl.setSpacing(10)

        ek = QLabel("HASIL CARIAN")
        ek.setObjectName("panelSection")
        sl.addWidget(ek, 0, Qt.AlignLeft)

        kad = QFrame()
        kad.setObjectName("sideCard")
        kl = QHBoxLayout(kad)
        kl.setContentsMargins(12, 10, 12, 10)
        kl.setSpacing(12)
        lencana = QLabel("🔍")
        lencana.setObjectName("noBadge")
        lencana.setFixedSize(46, 46)
        lencana.setAlignment(Qt.AlignCenter)
        kl.addWidget(lencana, 0, Qt.AlignTop)
        info = QWidget()
        il = QVBoxLayout(info)
        il.setContentsMargins(0, 0, 0, 0)
        il.setSpacing(1)
        self._carian_q_lbl = QLabel("—")
        self._carian_q_lbl.setObjectName("h3")
        self._carian_q_lbl.setWordWrap(True)
        il.addWidget(self._carian_q_lbl)
        self._carian_scope_lbl = QLabel("Semua kitab")
        self._carian_scope_lbl.setObjectName("muted")
        il.addWidget(self._carian_scope_lbl)
        self._carian_total_lbl = QLabel("Cari untuk melihat bab")
        self._carian_total_lbl.setObjectName("muted")
        il.addWidget(self._carian_total_lbl)
        kl.addWidget(info, 1)
        sl.addWidget(kad)

        ek_bab = QLabel("BAB DALAM KEPUTUSAN")
        ek_bab.setObjectName("panelSection")
        sl.addWidget(ek_bab, 0, Qt.AlignLeft)

        skrol = QScrollArea()
        skrol.setObjectName("babScroll")
        skrol.setWidgetResizable(True)
        skrol.setFrameShape(QFrame.NoFrame)
        skrol.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        bekas = QWidget()
        self._carian_bab_bekas = QVBoxLayout(bekas)
        self._carian_bab_bekas.setContentsMargins(0, 0, 0, 0)
        self._carian_bab_bekas.setSpacing(4)
        self._carian_bab_bekas.addStretch(1)
        skrol.setWidget(bekas)
        self._carian_bab_skrol = skrol
        sl.addWidget(skrol, 1)

        return s

    def _carian_kemas_info(self, q, total):
        if q is None:
            self._carian_q_lbl.setText("—")
            self._carian_total_lbl.setText("Cari untuk melihat bab")
            self._carian_scope_lbl.setText("Semua kitab")
            return
        self._carian_q_lbl.setText(f"'{q}'")
        self._carian_scope_lbl.setText(
            COLLECTION_META.get(self._search_slug, {}).get("name", "Semua kitab")
            if self._search_slug else "Semua kitab")
        self._carian_total_lbl.setText(f"{total:,} hadis ditemui")

    def _carian_bina_bab_rows(self):
        """Bina semula senarai bab dalam sidebar dari `self._carian_hasil`.

        Widget scroll-area DIBINA SEMULA setiap carian supaya kandungan
        baharu benar-benar dipapar (elak isu layout tidak segar bila
        dikemas kini lewat).
        """
        try:
            from api.hadis_api import nama_bab_bm
            agg = {}
            for it in self._carian_hasil:
                key = (it["collection"], it["book"])
                agg.setdefault(key, [0, it.get("nama_bab")])
                agg[key][0] += 1
            self._carian_bab_rows = []
            bekas = QWidget()
            bek = QVBoxLayout(bekas)
            bek.setContentsMargins(0, 0, 0, 0)
            bek.setSpacing(4)
            self._carian_tambah_bab_row(bek, None, "Semua hasil",
                                        len(self._carian_hasil))
            order = list(COLLECTION_META)
            for key in sorted(
                    agg,
                    key=lambda k: (order.index(k[0]) if k[0] in order else 99,
                                   k[1] or 0)):
                cnt, en = agg[key]
                nm = nama_bab_bm(key[0], key[1], en)
                short = COLLECTION_META.get(key[0], {}).get("short", key[0])
                self._carian_tambah_bab_row(bek, key, f"{short} · {nm}", cnt)
            bek.addStretch(1)
            self._carian_bab_bekas = bek
            self._carian_bab_skrol.setWidget(bekas)
            self._carian_bab_skrol.show()
        except Exception:
            pass

    def _carian_tambah_bab_row(self, bek, key, nama, kiraan):
        row = ClickCard()
        row.setObjectName(
            "babRow_active" if key == self._carian_bab else "babRow")
        rl = QHBoxLayout(row)
        rl.setContentsMargins(10, 7, 10, 7)
        rl.setSpacing(6)
        nl = QLabel(elide(nama, 52))
        nl.setToolTip(nama)
        nl.setWordWrap(True)
        rl.addWidget(nl, 1)
        cl = None
        if isinstance(kiraan, int):
            cl = QLabel(f"{kiraan:,}")
            cl.setObjectName("teal" if key == self._carian_bab else "faint")
            rl.addWidget(cl)
        row.clicked.connect(lambda k=key: self._carian_pilih_bab(k))
        self._carian_bab_rows.append((key, row, cl))
        bek.addWidget(row)

    def _carian_pilih_bab(self, key):
        if self._carian_bab == key:
            return
        self._carian_bab = key
        self._kemas_carian_bab_rows()
        self._carian_page = 1
        self._carian_render_panel(self._kw_meta, self._sem_res, self._kw_res, 1)

    def _tukar_carian_page(self, p):
        """Paginasi klien ke atas hasil sedia ada (tiada carian semula)."""
        self._carian_render_panel(self._kw_meta, self._sem_res, self._kw_res, p)

    def _kemas_carian_bab_rows(self):
        for key, row, cl in getattr(self, "_carian_bab_rows", []):
            aktif = (key == self._carian_bab)
            row.setObjectName("babRow_active" if aktif else "babRow")
            row.style().unpolish(row)
            row.style().polish(row)
            if cl is not None:
                cl.setObjectName("teal" if aktif else "faint")
                cl.style().unpolish(cl)
                cl.style().polish(cl)

    def _carian_set_tapis(self, kunci):
        if self._carian_tapis == kunci:
            return
        self._carian_tapis = kunci
        for k, b in self._carian_chip_btns.items():
            b.setObjectName(
                "filterChip_active" if k == kunci else "filterChip")
            b.style().unpolish(b)
            b.style().polish(b)
        self._carian_page = 1
        self._carian_render_panel(self._kw_meta, self._sem_res, self._kw_res, 1)

    def _carian_toggle_urutan(self):
        self._carian_urutan = "desc" if self._carian_urutan == "asc" else "asc"
        self._carian_urut_btn.setText(
            "Nombor ↓" if self._carian_urutan == "asc" else "Nombor ↑")
        self._carian_render_panel(self._kw_meta, self._sem_res, self._kw_res, 1)

    def _carian_lompat(self):
        """Lompat ke no. hadis (padanan go-box Senarai Hadis)."""
        try:
            n = int(self._carian_go_box.text())
        except (ValueError, TypeError):
            return
        slug = self._search_slug
        h = self.api.get_hadis_by_id(slug, n) if slug else None
        if h is None:
            for col in COLLECTION_META:
                h = self.api.get_hadis_by_id(col, n)
                if h:
                    slug = col
                    break
        if h:
            self.open_detail(h, "carian")

    def _bina_carian_panel(self) -> QWidget:
        # Padanan persis panel page Senarai Hadis (_kitab_panel) supaya
        # hasil carian kelihatan SAMA dengan page Senarai Hadis.
        p = QFrame()
        p.setObjectName("glassPanel")
        pl = QVBoxLayout(p)
        pl.setContentsMargins(18, 16, 18, 14)
        pl.setSpacing(10)

        kepala = QWidget()
        kl = QHBoxLayout(kepala)
        kl.setContentsMargins(0, 0, 0, 0)
        kl.setSpacing(8)
        kiri = QWidget()
        kv = QVBoxLayout(kiri)
        kv.setContentsMargins(0, 0, 0, 0)
        kv.setSpacing(2)
        ek_sen = QLabel("SENARAI CARIAN")
        ek_sen.setObjectName("panelSection")
        kv.addWidget(ek_sen)
        sub = QLabel("Terjemahan di kiri  ·  Petikan teks Arab di kanan")
        sub.setObjectName("muted")
        kv.addWidget(sub)
        kl.addWidget(kiri, 1)

        self._carian_urut_btn = QPushButton(
            "Nombor ↓" if self._carian_urutan == "asc" else "Nombor ↑")
        self._carian_urut_btn.setCursor(Qt.PointingHandCursor)
        self._carian_urut_btn.setObjectName("filterChip")
        self._carian_urut_btn.setToolTip("Tukar susunan nombor hadis")
        self._carian_urut_btn.clicked.connect(self._carian_toggle_urutan)
        kl.addWidget(self._carian_urut_btn)
        pl.addWidget(kepala)

        self._carian_container = QWidget()
        self._carian_list = QVBoxLayout(self._carian_container)
        self._carian_list.setContentsMargins(0, 0, 0, 0)
        self._carian_list.setSpacing(12)
        pl.addWidget(self._carian_container)

        kaki = QWidget()
        fl = QHBoxLayout(kaki)
        fl.setContentsMargins(0, 0, 0, 0)
        fl.setSpacing(8)
        self._carian_kaki = QLabel("")
        self._carian_kaki.setObjectName("muted")
        fl.addWidget(self._carian_kaki)
        fl.addStretch(1)
        self._carian_halaman = QLabel("")
        self._carian_halaman.setObjectName("muted")
        fl.addWidget(self._carian_halaman)
        pl.addWidget(kaki)

        self._carian_pager = Pager(lambda pg: self._tukar_carian_page(pg))
        self._carian_pager.hide()
        pl.addWidget(self._carian_pager)
        return p

    def _carian_render_panel(self, meta, sem, kw, page=1):
        self._clear_carian_list()
        scope = ""
        if self._search_slug:
            scope = f" dalam {COLLECTION_META[self._search_slug]['name']}"

        # Senarai penuh (sudah ditapis bab jika ada). Paginasi di KLIEN
        # ke atas hasil sedia ada — sidebar bab & tapis kekal lengkap.
        if self._carian_bab is None:
            semua = self._carian_hasil
        else:
            semua = [x for x in self._carian_hasil
                     if (x["collection"], x["book"]) == self._carian_bab]

        # Tapis (Semua / Tersimpan / Belum dibaca) + susunan nombor —
        # sama seperti page Senarai Hadis.
        if self._carian_tapis == "tersimpan":
            semua = [x for x in semua
                     if self._is_saved(x["collection"], x["hid"])]
        elif self._carian_tapis == "belum":
            dibaca = {(e.get("slug"), e.get("n")) for e in read_history()}
            semua = [x for x in semua
                     if (x["collection"], x["hid"]) not in dibaca]
        if self._carian_urutan == "desc":
            semua = sorted(semua, key=lambda x: x["hid"], reverse=True)
        else:
            semua = sorted(semua, key=lambda x: x["hid"])

        per = CARIAN_PER_PAGE
        last = max(1, -(-len(semua) // per)) if semua else 1
        page = max(1, min(page, last))
        self._carian_page = page

        if not semua:
            self._carian_list.addWidget(
                empty_state("🔍", "Tiada hasil",
                            f"Tiada hadis sepadan '{self._search_q}'{scope}."))
            pautan = QLabel(
                "Tiada hadis sepadan dalam 9 kitab ini. Hadis yang anda "
                "cari mungkin bukan daripada koleksi ini — "
                f"<a href=\"{SEMAKHADIS_URL}\">semak di SemakHadis.com</a>")
            pautan.setWordWrap(True)
            pautan.setTextFormat(Qt.RichText)
            pautan.setOpenExternalLinks(True)
            pautan.setTextInteractionFlags(Qt.TextBrowserInteraction)
            pautan.setAlignment(Qt.AlignCenter)
            pautan.setStyleSheet(
                f"font-size: 12px; color: {TEXT_MUTED}; "
                f"a {{ color: {AMBER_TEXT}; }}")
            self._carian_list.addWidget(pautan)
            self._carian_pager.set_state(1, 1)
            self._carian_pager.hide()
            self._search_sa.verticalScrollBar().setValue(0)
            return

        papar = semua[(page - 1) * per: page * per]

        if self._carian_bab is not None:
            self.search_info.setText(
                f"{len(semua):,} hadis dalam bab dipilih "
                f"(daripada {len(self._carian_hasil):,} dijumpai)")
        else:
            total = meta.get("total", len(self._carian_hasil))
            if meta.get("fallback"):
                self.search_info.setText(
                    f"'{self._search_q}'{scope} — {total:,} padanan kata "
                    "longgar (tiada hadis mengandungi SEMUA perkataan)")
            else:
                self.search_info.setText(
                    f"'{self._search_q}'{scope} — {total:,} hadis ditemui")

        for it in papar:
            self._tambah_kad_carian(it["h"], it["collection"], it["hid"])

        mula = (page - 1) * per + 1
        tamat = min(mula + per - 1, len(semua)) if semua else 0
        self._carian_kaki.setText(
            f"Menunjukkan {mula}–{tamat} daripada {len(semua):,} hadis")
        self._carian_halaman.setText(f"Halaman {page} / {last}")

        if len(semua) > per:
            self._carian_pager.set_state(page, last)
            self._carian_pager.show()
        else:
            self._carian_pager.hide()
        self._search_sa.verticalScrollBar().setValue(0)

    def _carian_toggle_simpan(self, h, card, slug, hid):
        """Butang Simpan pada kad carian — toggle tanda buku, segar ikon."""
        self._toggle_save(h)
        card.simpan_btn.set_active(self._is_saved(slug, hid))

    def _hantar_carian(self):
        """Hantar carian dari bar carian (butang/Enter).

        Sebelum carian biasa, cuba tafsir sebagai lompat terus: 'bukhari
        433' atau '433' (chip kitab terpilih, atau kitab terakhir dibuka).
        Carian KHUSUS seperti ini membuka butiran hadis TERUS (Sesi 38)
        — pengguna mahukan hadis itu, bukan senarai. Carian umum (cth.
        'hukum riba') kekal memaparkan senarai hasil carian.
        """
        q = self.search_bar.text()
        if not q:
            return
        j = _parse_lompat(q, default_slug=self.search_bar.slug()
                          or self._kitab_slug)
        if j:
            slug, n = j
            self._buka_hadis_terus(slug, n)
            return
        self._do_search(1)

    def _buka_hadis_terus(self, slug: str, n: int, dari: str = "search"):
        """Buka butiran hadis No. n dalam slug TERUS, tanpa senarai.

        Pintasan '433' (halaman Utama atau Carian): pengguna mahukan
        hadis itu, bukan senarai kitab. Sahkan julat dahulu (murah),
        beri toast maklum balas, kemudian muat dan buka butiran. Butang
        Kembali menuju ke halaman `dari` ('home' atau 'search').
        """
        nama = COLLECTION_META.get(slug, {}).get("name", slug)
        r = self._sahkan_lompat(slug, n, nama)
        if r is None:
            return
        self._detail_from = dari
        # Toast "Membuka…" kekal sehingga butiran dibuka (open_by_ref
        # menyembunyikannya) — muatan hadis asynchronous, jadi tempoh
        # tetap boleh terlepas sebelum butiran siap dipapar. Tetapi
        # untuk muatan pantas (DB tempatan), ia tidak boleh hilang
        # serta-merta: simpan masa mula supaya open_by_ref menjamin
        # minimum 1800ms paparan (pengguna sempat baca maklum balas).
        self._buka_toast_t0 = time.monotonic()
        self.toast.show_msg(f"📖 Membuka {nama} No. {n}…", 0)
        self.open_by_ref(slug, n, dari)

    def _do_search(self, page=1):
        q = self.search_bar.text()
        if not q:
            return
        self._search_q = q
        self._search_slug = self.search_bar.slug()
        self._search_page = page
        self._tok += 1
        tok = self._tok

        mod = self.settings.get("carian_mod", "kedua")
        self._sem_res = None
        self._kw_res = None
        self._kw_meta = {}
        self._sem_gagal = None
        self._carian_bab = None
        self._carian_page = 1
        self._clear_carian_list()
        self._carian_reset_sidebar()
        self._carian_q_lbl.setText(f"'{q}'")
        self._carian_scope_lbl.setText(
            COLLECTION_META.get(self._search_slug, {}).get("name", "Semua kitab")
            if self._search_slug else "Semua kitab")
        self._carian_total_lbl.setText("Mencari…")
        self.search_info.setText(f"Mencari '{q}'…")
        self._carian_sibuk.show()
        self._carian_timer.start()

        # Kaedah carian (togol 3-mod):
        #   kata  -> hanya SearchWorker (FTS5), tiada draf AI
        #   makna -> hanya SemanticWorker (draf + hasil makna)
        #   kedua -> kedua-dua serentak (gelagat asal)
        # Enjin yang dilangkau ditetapkan senarai kosong serta-merta supaya
        # _tampal_gabungan tetap tamat (menunggu KEDUA-dua hasil).
        if mod in ("kata", "kedua"):
            kw_worker = self._run(
                SearchWorker(self.api, q, self._search_slug, page,
                             self.per_page(), self.lang_param, tok),
                self._on_search,
                # SearchWorker.failed = pyqtSignal(str) -- satu argumen,
                # jadi tok ditangkap dalam lambda (bukan disambung terus).
                on_fail=lambda m: self._on_search_failed(m, tok))
            # Tampal paparan hanya selepas worker benar-benar tamat
            # (finished), BUKAN dari callback done -- mengelak akses
            # serentak ke model torch (0xC0000409) semasa QThread masih
            # menamatkan run().
            kw_worker.finished.connect(lambda: self._tampal_gabungan(tok))
        else:
            self._kw_res = []
            self._kw_meta = {}

        if mod in ("makna", "kedua"):
            self._run_semantic_search(q, tok)
        else:
            self._sem_res = []

    def _run_semantic_search(self, query: str, tok: int):
        """Jalankan carian semantik di background thread (Lazy Loading).

        `SemanticWorker` kini di `ui/workers.py` (13 Ogos 2026) --
        mewarisi `_Base` dan `cancel()`, bukan lagi kelas dalaman
        `QThread` tanpa `cancel()`. Rujuk komen kelas dalam workers.py
        untuk sebab pemindahan (PERUBAHAN_7OGOS.md, "Pepijat kedua").

        Signal baharu: `model_loading_started(int token)` dipancar
        SEBELUM muat model (pada carian makna pertama). UI papar
        "Memuatkan AI..." inline.
        """
        worker = SemanticWorker(query, top_k=20, min_score=0.6, token=tok)
        worker.done.connect(lambda results, t: self._on_semantic_search(results, t))
        worker.failed.connect(lambda msg, t: self._on_semantic_failed(msg, t))
        # Model loading indicator (Lazy Loading)
        worker.model_loading_started.connect(lambda t: self._on_model_loading(t))
        self._workers.append(worker)
        worker.finished.connect(lambda: self._workers.remove(worker)
                                if worker in self._workers else None)
        # Papar gabungan hanya selepas run() QThread pulang sepenuhnya --
        # bukan dari callback done (yang masih dalam run() worker).
        worker.finished.connect(lambda: self._tampal_gabungan(tok))
        worker.start()

    def _on_semantic_search(self, results, tok):
        if tok != self._tok:
            return
        self._sem_res = results or []

    def _on_semantic_failed(self, msg, tok):
        if tok != self._tok:
            return
        self._sem_res = []
        self._sem_gagal = msg

    def _on_model_loading(self, tok):
        """Dipanggil SEBELUM model dimuat (Lazy Loading) — papar inline."""
        if tok != self._tok:
            return
        self._carian_sibuk.setText("🤖 Memuatkan model AI…")
        self._carian_sibuk.show()
        if not self._carian_timer.isActive():
            self._carian_timer.start(120)

    def _on_search(self, items, meta, tok):
        if tok != self._tok:
            return
        self._kw_res = items or []
        self._kw_meta = meta or {}

    def _on_search_failed(self, msg, tok):
        """Carian kata kunci gagal -- tandakan selesai supaya paparan
        gabungan boleh tamat dan indikator jam disembunyikan (bukan
        tersangkut selama-lamanya pada \"Mencari…\"). Simetri dengan
        `_on_semantic_failed` yang menetapkan `_sem_res = []`.
        """
        if tok != self._tok:
            return
        self._kw_res = []
        self._on_error(msg)

    def _putar_jam(self):
        """Putar emoji jam 🕐→🕛 (120ms) semasa carian berjalan.

        Pengawal `isVisible()`: timer lama yang masih berjalan selepas
        pembinaan semula tema tidak mengemas kini label baharu secara
        serentak (jam tidak berputar laju dua kali ganda).
        """
        if not self._carian_sibuk.isVisible():
            return
        self._jam_i = (self._jam_i + 1) % len(self._jam)
        self._carian_sibuk.setText(self._jam[self._jam_i])

    def _kemas_butang_atas_carian(self):
        """Tunjuk/sembunyi butang ↑ halaman Carian ikut skrol (Sesi 34).

        Corak sama seperti _kemas_butang_atas pada halaman kitab: butang
        hanya berguna bila senarai melebihi viewport dan pengguna sudah
        skrol ke bawah (melebihi 250px). Kedudukan dikira semula pada
        setiap skrol dan ubah saiz tetingkap.
        """
        b = getattr(self, "_search_top_btn", None)
        sa = getattr(self, "_search_sa", None)
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

    def _skrol_atas_lancar_carian(self):
        """Skrol lancar ke atas senarai hasil — animasi QTimer ~250ms.

        Corak sama seperti _skrol_atas_lancar pada halaman kitab:
        langkah mengecil supaya pergerakan kelihatan perlahan berhampiran
        sasaran; timer disimpan pada `self` supaya panggilan kedua
        menghentikan animasi pertama.
        """
        bar = self._search_sa.verticalScrollBar()
        mula = bar.value()
        if mula <= 0:
            return
        t = getattr(self, "_top_timer_carian", None)
        if t is not None:
            t.stop()
        t = QTimer(self)
        self._top_timer_carian = t
        langkah = max(1, mula // 15)

        def _langkah():
            if t is not self._top_timer_carian:
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

    def _tampal_gabungan(self, tok):
        if tok != self._tok:
            return
        if self._sem_res is None or self._kw_res is None:
            return
        self._carian_sibuk.hide()
        self._carian_timer.stop()

        # Bina senarai hasil tunggal (dedupe semantik + keyword).
        self._carian_hasil = []
        seen = set()
        for r in self._sem_res:
            slug, hid = r["collection"], r["hadis_id"]
            key = (slug, hid)
            if key in seen:
                continue
            seen.add(key)
            h = self.api.get_hadis_by_id(slug, hid)
            if h:
                self._carian_hasil.append({
                    "h": h, "collection": slug, "hid": hid,
                    "book": h.get("book"), "nama_bab": h.get("nama_bab"),
                })
        for h in self._kw_res:
            slug = h.get("collection", "")
            # search_hadis pulang `id` (bukan `hadis_id`) — guna mana-mana
            # yang ada supaya penapis dedupe tidak melanggar hasil sekitar
            # satu koleksi (bug: hadis_id sentiasa None -> 1 kad/koleksi).
            hid = h.get("hadis_id") or h.get("id")
            key = (slug, hid)
            if key in seen:
                continue
            seen.add(key)
            self._carian_hasil.append({
                "h": h, "collection": slug, "hid": hid,
                "book": h.get("book"), "nama_bab": h.get("nama_bab"),
            })

        if getattr(self, "_sem_gagal", None):
            self.toast.show_msg(f"⚠️ Carian makna: {self._sem_gagal}", 4000)
            self._sem_gagal = None

        # Sidebar bab + info + panel hasil (susun macam Senarai Hadis).
        self._carian_bina_bab_rows()
        self._carian_kemas_info(self._search_q, len(self._carian_hasil))
        self._carian_render_panel(self._kw_meta, self._sem_res, self._kw_res)
        self._laras_tinggi(self._search_sa)
