"""Halaman Senarai Hadis — mixin PustakaApp (reka bentuk 26 Ogos 2026).

Susun atur Split Command Center (mockup terkunci): banner kaca +
sidebar "KITAB SEMASA / PILIH BAB" + panel senarai dwibahasa, di atas
BackgroundCanvas (glob AQUA; tema lain permukaan pepejal) — pola sama
halaman Utama/rak. Kad dwibahasa (terjemahan kiri | Arab kanan) hanya
di halaman ini (keputusan pengguna).

Dipisahkan dari `ui/app_qt.py` (Sesi 30 refactor). Kelas `PagesKitab`
digabungkan ke `PustakaApp` melalui MRO. Kaedah di sini bergantung pada
state/kaedah `self` (PustakaApp): stack, _run, _tok, _kitab_*, toast,
per_page(), ar_scale, ar_font, _papar_melayu, _total_of, open_detail,
go, bookmarks, search_bar, _do_search, _toggle_save.

GANDINGAN RENTAS MIXIN: kaedah lompat di sini (`_sahkan_lompat`,
`_lompat_ke`, `_kira_halaman_lompat`) turut dipanggil oleh `PagesCarian`
(`_buka_hadis_terus`, `_hantar_carian`) dan halaman Utama
(`_from_home_search`). Jangan alih keluar kaedah ini tanpa mengemas
pemanggilnya. Nama atribut `_kitab_root`, `_kitab_container`,
`_kitab_list`, `_kitab_pager`, `_kitab_go_box`, `_kitab_sa` KEKAL —
skrip uji visual & semak.py merujuknya.

Modul ini TIDAK import warna dari `ui.theme` (hanya COLLECTION_META,
metadata kitab) tetapi didaftar dalam `_THEMED_MODULES` supaya kekal
konsisten dengan modul UI lain.
"""

from __future__ import annotations

from PyQt5.QtCore import QPoint, Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import (
    QFrame, QHBoxLayout, QLabel, QLineEdit, QPushButton, QScrollArea,
    QVBoxLayout, QWidget,
)

from ui.helpers import PAGES, _clear, click_sound, read_history
from ui.pages import Pager, _label_kiraan, empty_state
from ui.theme import COLLECTION_META
from ui.widgets import (
    BackgroundCanvas, ClickCard, attach_copy_menu, elide,
    hadith_card_dwibahasa, make_scroll,
)
from ui.workers import ListWorker


def _julat_lompat(total) -> str:
    """Placeholder kotak 'Lompat No. hadis'; 'No. hadis' jika tidak diketahui.

    Dahulu dibenamkan dalam `_render_kitab_shell`; kini fungsi tulen
    — diuji unit (semak.py 8w).
    """
    if not isinstance(total, int):
        return "No. hadis"
    return f"0–{total}"


class _Pautan(QLabel):
    """Pautan teks kecil boleh klik ("← Kembali ke rak" dsb.)."""

    clicked = pyqtSignal()

    def __init__(self, teks: str, parent=None):
        super().__init__(teks, parent)
        self.setObjectName("bacaLink")
        self.setCursor(Qt.PointingHandCursor)

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton and self.rect().contains(e.pos()):
            self.clicked.emit()
        super().mouseReleaseEvent(e)


class PagesKitab:
    # ── HALAMAN: Senarai Hadis ───────────────────────────────────────
    def _page_kitab(self):
        # Pola sama Utama/rak (25 Ogos): BackgroundCanvas akar, skrol
        # telus di atasnya — glob AQUA kelihatan di belakang panel kaca.
        kanvas = BackgroundCanvas()
        self.stack.addWidget(kanvas)
        sa = make_scroll(kanvas)
        sa.setObjectName("homeScroll")          # QSS telus sama dgn Utama
        body = QWidget()
        body.setObjectName("homeBody")
        sa.setWidget(body)
        vl = QVBoxLayout(kanvas)
        vl.setContentsMargins(0, 0, 0, 0)
        vl.addWidget(sa)

        self._kitab_sa = sa
        self._kitab_root = QVBoxLayout(body)
        self._kitab_root.setContentsMargins(24, 20, 24, 20)
        self._kitab_root.setSpacing(14)

        # Butang terapung "↑ ke atas" (Sesi 34) — kelihatan bila pengguna
        # skrol ke bawah senarai hadis; klik untuk kembali ke hadis
        # pertama dengan animasi lancar. Anak kepada QScrollArea supaya
        # ia terapung di atas kandungan; dikemas pada setiap skrol dan
        # ubah saiz (lihat _kemas_butang_atas).
        if getattr(self, "_top_timer", None) is not None:
            self._top_timer.stop()
        self._kitab_top_btn = QPushButton("↑")
        self._kitab_top_btn.setObjectName("backTop")
        self._kitab_top_btn.setToolTip("Ke atas — hadis pertama")
        self._kitab_top_btn.setCursor(Qt.PointingHandCursor)
        self._kitab_top_btn.setFixedSize(44, 44)
        self._kitab_top_btn.setParent(sa)
        self._kitab_top_btn.clicked.connect(self._skrol_atas_lancar)
        self._kitab_top_btn.hide()
        sa.verticalScrollBar().valueChanged.connect(self._kemas_butang_atas)
        _orig_resize = sa.resizeEvent

        def _on_resize(e):
            _orig_resize(e)
            self._kemas_butang_atas()

        sa.resizeEvent = _on_resize

        # State penapis (reset bila kitab lain dibuka — lihat open_kitab)
        self._kitab_bab = None          # book terpilih (None = semua)
        self._kitab_tapis = "semua"     # semua | tersimpan | belum
        self._kitab_urutan = "asc"      # asc | desc
        self._kitab_bab_data: list = []

    def open_kitab(self, slug, page=1):
        click_sound()
        if slug != getattr(self, "_kitab_slug", None):
            # Kitab baharu: reset penapis supaya pengguna sentiasa mula
            # dengan pandangan penuh (keputusan spec 26 Ogos).
            self._kitab_bab = None
            self._kitab_tapis = "semua"
            self._kitab_urutan = "asc"
        self._kitab_slug = slug
        self._kitab_page = page
        self.go("kitab")
        self._render_kitab_shell()
        self._load_kitab_page(page)

    # ── bina shell: banner + sidebar + panel senarai ─────────────────
    def _render_kitab_shell(self):
        _clear(self._kitab_root)
        meta = COLLECTION_META.get(self._kitab_slug, {})
        total = self._total_of(self._kitab_slug)
        # Placeholder kotak nombor memerlukan julat sebenar. Jika
        # koleksi belum dimuat (permulaan/offline), kira terus dari
        # pangkalan data — sama seperti _kira_halaman_lompat.
        if not isinstance(total, int) and self.api.offline:
            try:
                total = self.api.max_hadis_id(self._kitab_slug)
            except Exception:
                pass

        # Senarai buku/kitab dalam koleksi (DB tempatan sahaja; kosong
        # bila dalam talian tanpa DB — bahagian bab disembunyi).
        self._kitab_bab_data = self.api.get_bab_list(self._kitab_slug) \
            if getattr(self.api, "conn", None) else []

        self._kitab_root.addWidget(self._kitab_banner(meta, total))
        baris = QWidget()
        hl = QHBoxLayout(baris)
        hl.setContentsMargins(0, 0, 0, 0)
        hl.setSpacing(16)
        hl.addWidget(self._kitab_sidebar(meta, total))
        hl.addWidget(self._kitab_panel(), 1)
        # TIADA addStretch pada _kitab_root — senarai 25 kad melebihi
        # viewport; stretch menuntut ruang tetap dan menjadikan kawasan
        # bawah pager kawasan skrol KOSONG (diukur, Sesi 34).
        self._kitab_root.addWidget(baris)

    # ── banner atas ──────────────────────────────────────────────────
    def _kitab_banner(self, meta: dict, total) -> QFrame:
        b = QFrame()
        b.setObjectName("glassPanel")
        h = QHBoxLayout(b)
        h.setContentsMargins(24, 16, 24, 16)
        h.setSpacing(16)

        kiri = QWidget()
        kl = QVBoxLayout(kiri)
        kl.setContentsMargins(0, 0, 0, 0)
        kl.setSpacing(2)
        nama = meta.get("name", self._kitab_slug)
        eyebrow = QLabel(f"JELAJAH KITAB  /  {nama.upper()}")
        eyebrow.setObjectName("eyebrow")
        kl.addWidget(eyebrow)
        t = QLabel("Senarai Hadis")
        t.setObjectName("homeH1")
        kl.addWidget(t)
        mtxt = nama
        kiraan = _label_kiraan(total, "hadis", "")
        if kiraan:
            mtxt += f"  ·  {kiraan}"
        if self._kitab_bab_data:
            mtxt += f"  ·  {len(self._kitab_bab_data)} kitab"
        m = QLabel(mtxt)
        m.setObjectName("muted")
        kl.addWidget(m)
        h.addWidget(kiri, 1)

        # Carian dalam kitab — buka Pencarian dengan slug dikunci
        # (keputusan pengguna 26 Ogos; ciri sedia ada diguna semula).
        self._kitab_carian = QLineEdit()
        self._kitab_carian.setPlaceholderText(
            f"Cari dalam {meta.get('short', nama)}…")
        self._kitab_carian.setFixedWidth(280)
        self._kitab_carian.setMinimumHeight(40)
        self._kitab_carian.setClearButtonEnabled(True)
        attach_copy_menu(self._kitab_carian)
        self._kitab_carian.returnPressed.connect(self._kitab_hantar_carian)
        h.addWidget(self._kitab_carian)

        btn = QPushButton("Cari")
        btn.setObjectName("primary")
        btn.setCursor(Qt.PointingHandCursor)
        btn.setMinimumHeight(40)
        btn.clicked.connect(self._kitab_hantar_carian)
        h.addWidget(btn)
        return b

    def _kitab_hantar_carian(self):
        q = self._kitab_carian.text().strip()
        if not q:
            return
        # Kunci skop kitab pada halaman Pencarian (chip aktif).
        if getattr(self, "search_bar", None) is not None \
                and self.search_bar.chips is not None:
            self.search_bar.chips.set_active(self._kitab_slug, emit=False)
        self.search_bar.input.setText(q)
        self.go("search")
        self._do_search(1)

    # ── sidebar kiri ─────────────────────────────────────────────────
    def _kitab_sidebar(self, meta: dict, total) -> QFrame:
        s = QFrame()
        s.setObjectName("glassPanel")
        s.setFixedWidth(300)
        sl = QVBoxLayout(s)
        sl.setContentsMargins(16, 14, 16, 14)
        sl.setSpacing(10)

        kiraan = _label_kiraan(total, "hadis", "")

        ek_kitab = QLabel("KITAB SEMASA")
        ek_kitab.setObjectName("panelSection")
        sl.addWidget(ek_kitab, 0, Qt.AlignLeft)

        # Kad kitab semasa: lencana kod + nama + kiraan
        kad = QFrame()
        kad.setObjectName("sideCard")
        kl = QHBoxLayout(kad)
        kl.setContentsMargins(12, 10, 12, 10)
        kl.setSpacing(12)
        no_urut = list(COLLECTION_META).index(self._kitab_slug) + 1 \
            if self._kitab_slug in COLLECTION_META else 0
        kod = meta.get("short", self._kitab_slug)[:2].upper()
        lencana = QLabel(f"""<div align="center">
<span style="font-size:9px;letter-spacing:1px;">{kod}</span><br>
<span style="font-size:15px;font-weight:800;">{no_urut:02d}</span></div>""")
        lencana.setObjectName("noBadge")
        lencana.setFixedSize(46, 46)
        lencana.setAlignment(Qt.AlignCenter)
        kl.addWidget(lencana, 0, Qt.AlignTop)
        info = QWidget()
        il = QVBoxLayout(info)
        il.setContentsMargins(0, 0, 0, 0)
        il.setSpacing(1)
        nm = QLabel(meta.get("name", self._kitab_slug))
        nm.setObjectName("h3")
        nm.setWordWrap(True)
        il.addWidget(nm)
        if kiraan:
            k1 = QLabel(kiraan)
            k1.setObjectName("muted")
            il.addWidget(k1)
        if self._kitab_bab_data:
            k2 = QLabel(f"{len(self._kitab_bab_data)} kitab")
            k2.setObjectName("muted")
            il.addWidget(k2)
        kl.addWidget(info, 1)
        sl.addWidget(kad)

        ke_rak = _Pautan("← Kembali ke rak")
        ke_rak.clicked.connect(lambda: self.go("rak"))
        sl.addWidget(ke_rak, 0, Qt.AlignLeft)

        # ── PILIH BAB (sembunyi bila tiada data bab) ─────────────────
        if self._kitab_bab_data:
            ek_bab = QLabel("PILIH BAB")
            ek_bab.setObjectName("panelSection")
            sl.addWidget(ek_bab, 0, Qt.AlignLeft)
            skrol = QScrollArea()
            skrol.setObjectName("babScroll")
            skrol.setWidgetResizable(True)
            skrol.setFrameShape(QFrame.NoFrame)
            skrol.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            skrol.setMaximumHeight(238)
            bekas = QWidget()
            bl = QVBoxLayout(bekas)
            bl.setContentsMargins(0, 0, 0, 0)
            bl.setSpacing(4)
            self._kitab_bab_rows: list = []
            self._tambah_bab_row(bl, None, "Semua hadis",
                                 total if isinstance(total, int) else
                                 sum(b["kiraan"] for b in self._kitab_bab_data))
            for b in self._kitab_bab_data:
                self._tambah_bab_row(bl, b.get("book"),
                                     b.get("nama_bab") or f"Buku {b.get('book')}",
                                     b.get("kiraan", 0))
            bl.addStretch(1)
            skrol.setWidget(bekas)
            sl.addWidget(skrol)

        # ── LOMPAT NO. HADIS (dipindah ke sidebar; Ctrl+G kekal) ─────
        ek_lompat = QLabel("LOMPAT NO. HADIS")
        ek_lompat.setObjectName("panelSection")
        sl.addWidget(ek_lompat, 0, Qt.AlignLeft)
        self._kitab_go_box = QLineEdit()
        self._kitab_go_box.setPlaceholderText(_julat_lompat(total))
        self._kitab_go_box.setToolTip(
            "Taip nombor hadis lalu tekan Enter — contoh: 7008\n"
            "(pintasan: Ctrl+G)")
        self._kitab_go_box.setAlignment(Qt.AlignCenter)
        self._kitab_go_box.setValidator(QIntValidator(1, 999999, self))
        self._kitab_go_box.returnPressed.connect(self._hantar_go_box)
        sl.addWidget(self._kitab_go_box)

        sl.addStretch(1)
        if self._kitab_bab_data:
            semua = _Pautan(f"Lihat semua {len(self._kitab_bab_data)} kitab →")
            semua.clicked.connect(lambda: self.go("rak"))
            sl.addWidget(semua, 0, Qt.AlignLeft)
        return s

    def _tambah_bab_row(self, bl: QVBoxLayout, book, nama: str, kiraan):
        row = ClickCard()
        row.setObjectName(
            "babRow_active"
            if book == self._kitab_bab else "babRow")
        rl = QHBoxLayout(row)
        rl.setContentsMargins(10, 7, 10, 7)
        rl.setSpacing(6)
        nl = QLabel(elide(nama, 22))
        nl.setToolTip(nama)
        rl.addWidget(nl, 1)
        if isinstance(kiraan, int):
            cl = QLabel(f"{kiraan:,}")
            cl.setObjectName("faint" if book != self._kitab_bab else "teal")
            rl.addWidget(cl)
        row.clicked.connect(lambda bk=book: self._kitab_pilih_bab(bk))
        self._kitab_bab_rows.append((book, row))
        bl.addWidget(row)

    def _kitab_pilih_bab(self, book):
        if self._kitab_bab == book:
            return
        self._kitab_bab = book
        self._kemas_bab_rows()
        self._load_kitab_page(1)

    def _kemas_bab_rows(self):
        for book, row in getattr(self, "_kitab_bab_rows", []):
            aktif = book == self._kitab_bab
            row.setObjectName("babRow_active" if aktif else "babRow")
            row.style().unpolish(row)
            row.style().polish(row)

    # ── panel senarai kanan ──────────────────────────────────────────
    def _kitab_panel(self) -> QFrame:
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
        ek_sen = QLabel("SENARAI DWIBAHASA")
        ek_sen.setObjectName("panelSection")
        kv.addWidget(ek_sen)
        sub = QLabel("Terjemahan di kiri  ·  Petikan teks Arab di kanan")
        sub.setObjectName("muted")
        kv.addWidget(sub)
        kl.addWidget(kiri, 1)

        # Chips penapis — Semua / Tersimpan / Belum dibaca (berfungsi)
        # + togol susunan nombor. Dalam talian tanpa DB: dinyahaktif.
        self._kitab_chip_btns: dict = {}
        for kunci, label in (("semua", "Semua"),
                             ("tersimpan", "Tersimpan"),
                             ("belum", "Belum dibaca")):
            cb = QPushButton(label)
            cb.setCursor(Qt.PointingHandCursor)
            cb.setObjectName(
                "filterChip_active" if kunci == self._kitab_tapis
                else "filterChip")
            cb.clicked.connect(lambda _, k=kunci: self._kitab_set_tapis(k))
            if kunci != "semua" and not getattr(self.api, "conn", None):
                cb.setEnabled(False)
                cb.setToolTip("Perlu pangkalan data tempatan")
            kl.addWidget(cb)
            self._kitab_chip_btns[kunci] = cb
        self._kitab_urut_btn = QPushButton(
            "Nombor ↓" if self._kitab_urutan == "asc" else "Nombor ↑")
        self._kitab_urut_btn.setCursor(Qt.PointingHandCursor)
        self._kitab_urut_btn.setObjectName("filterChip")
        self._kitab_urut_btn.setToolTip("Tukar susunan nombor hadis")
        self._kitab_urut_btn.clicked.connect(self._kitab_toggle_urutan)
        kl.addWidget(self._kitab_urut_btn)
        pl.addWidget(kepala)

        # Bungkus senarai dalam QWidget, bukan addLayout terus.
        # QWidget mempunyai sizeHint sendiri yang boleh diukur; layout
        # telanjang tidak, jadi QScrollArea tidak dapat tahu tinggi
        # sebenar kandungan dan menganggarkan berlebihan.
        self._kitab_container = QWidget()
        self._kitab_list = QVBoxLayout(self._kitab_container)
        self._kitab_list.setContentsMargins(0, 0, 0, 0)
        self._kitab_list.setSpacing(12)
        pl.addWidget(self._kitab_container)

        # Kaki: maklumat julat + halaman (mockup 26 Ogos)
        kaki = QWidget()
        fl = QHBoxLayout(kaki)
        fl.setContentsMargins(0, 0, 0, 0)
        fl.setSpacing(8)
        self._kitab_kaki = QLabel("")
        self._kitab_kaki.setObjectName("muted")
        fl.addWidget(self._kitab_kaki)
        fl.addStretch(1)
        self._kitab_halaman = QLabel("")
        self._kitab_halaman.setObjectName("muted")
        fl.addWidget(self._kitab_halaman)
        pl.addWidget(kaki)

        self._kitab_pager = Pager(lambda pg: self._load_kitab_page(pg))
        pl.addWidget(self._kitab_pager)
        return p

    def _kitab_set_tapis(self, kunci: str):
        if self._kitab_tapis == kunci:
            return
        self._kitab_tapis = kunci
        for k, b in self._kitab_chip_btns.items():
            b.setObjectName(
                "filterChip_active" if k == kunci else "filterChip")
            b.style().unpolish(b)
            b.style().polish(b)
        self._load_kitab_page(1)

    def _kitab_toggle_urutan(self):
        self._kitab_urutan = "desc" if self._kitab_urutan == "asc" else "asc"
        self._kitab_urut_btn.setText(
            "Nombor ↓" if self._kitab_urutan == "asc" else "Nombor ↑")
        self._load_kitab_page(1)

    # ── muat data ────────────────────────────────────────────────────
    def _load_kitab_page(self, page):
        self._kitab_page = page
        self._tok += 1
        tok = self._tok
        _clear(self._kitab_list)
        lbl = QLabel("Memuatkan…")
        lbl.setObjectName("muted")
        lbl.setAlignment(Qt.AlignCenter)
        self._kitab_list.addWidget(lbl)

        # Penapis chips (26 Ogos): Tersimpan = tanda buku kitab ini;
        # Belum dibaca = tiada dalam sejarah bacaan (≤50 terkini).
        ids = exclude = None
        slug = self._kitab_slug
        if self._kitab_tapis == "tersimpan":
            ids = [b.get("id") for b in self.bookmarks
                   if b.get("slug") == slug]
        elif self._kitab_tapis == "belum":
            exclude = [e.get("n") for e in read_history()
                       if e.get("slug") == slug]

        self._run(ListWorker(self.api, slug, page, self.per_page(),
                             self.lang_param, tok, book=self._kitab_bab,
                             order=self._kitab_urutan, ids=ids,
                             exclude_ids=exclude),
                  self._on_kitab_page)

    def _on_kitab_page(self, items, meta, tok):
        if tok != self._tok:
            return
        _clear(self._kitab_list)
        short = COLLECTION_META.get(self._kitab_slug, {}).get(
            "short", self._kitab_slug)
        if not items:
            msg = {"tersimpan": ("🔖", "Tiada hadis tersimpan",
                                 "Tandai hadis dalam kitab ini untuk "
                                 "melihatnya di sini."),
                   "belum": ("📖", "Semua telah dibaca",
                             "Tiada hadis belum dibaca pada penapis ini.")}
            e, t, d = msg.get(self._kitab_tapis,
                              ("📭", "Tiada hadis", "Koleksi ini kosong."))
            self._kitab_list.addWidget(empty_state(e, t, d))
            self._kitab_kaki.setText("")
            self._kitab_pager.set_state(1, 1)
            self._laras_tinggi(self._kitab_sa)
            return
        for h in items:
            h.setdefault("collection", self._kitab_slug)
            c = hadith_card_dwibahasa(
                h, short, self.ar_scale, arabic_font=self.ar_font,
                tersimpan=self._is_saved(self._kitab_slug, h.get("id")),
                papar_melayu=self._papar_melayu)
            c._hid = h.get("id")
            c.clicked.connect(lambda hh=h: self.open_detail(hh, "kitab"))
            c.simpan_clicked.connect(
                lambda _, hh=h: self._kitab_toggle_simpan(hh))
            self._kitab_list.addWidget(c)
        total = meta.get("total", 0)
        mula = (self._kitab_page - 1) * meta.get("per_page",
                                                 self.per_page()) + 1
        tamat = mula + len(items) - 1
        self._kitab_kaki.setText(
            f"Menunjukkan {mula}–{tamat} daripada {total:,} hadis")
        last = meta.get("last_page", 1)
        self._kitab_halaman.setText(
            f"Halaman {meta.get('current_page', 1)} / {last}")
        self._kitab_pager.set_state(meta.get("current_page", 1), last)
        self._laras_tinggi(self._kitab_sa)
        # Lompatan "Pergi ke nombor hadis": skrol ke kad sasaran supaya
        # pengguna terus nampak hadis yang diminta. Skrol manual dan
        # BUKAN ensureWidgetVisible (yang hanya mendedahkan bahagian
        # bawah kad di tepi viewport); di sini kad diletak ~1/3 dari atas.
        sasaran = self._kitab_go_to_hid
        self._kitab_go_to_hid = None
        bar = self._kitab_sa.verticalScrollBar()
        if sasaran is None:
            bar.setValue(0)
            return
        if bar.maximum() > 0:
            self._skrol_ke_kad(sasaran)
            return
        # Julat scrollbar hanya dikemas secara TAK SEGERAK, selepas
        # QScrollArea menerima resize event kandungan (layout selesai).
        # Memanggil setValue sebelum julat wujud akan terampas ke 0 --
        # kad sasaran langsung tidak kelihatan (diukur: Bukhari #500,
        # halaman 25, y=2910, viewport 738; tanpa ini skrol kekal 0).
        # Tunggu isyarat rangeChanged, kemudian skrol ke sasaran.
        def _bila_range(_mn, mx):
            if mx <= 0:
                return
            try:
                bar.rangeChanged.disconnect(_bila_range)
            except TypeError:
                pass
            self._skrol_ke_kad(sasaran)

        bar.rangeChanged.connect(_bila_range)

    def _kitab_toggle_simpan(self, h: dict):
        """Butang 🔖 pada kad — toggle tanda buku, muat semula halaman.

        Muat semula (bukan kemas widget tunggal) supaya chip "Tersimpan"
        dan keadaan 🔖 semua kad sentiasa konsisten dengan bookmarks.
        """
        self._toggle_save(h)
        self._load_kitab_page(self._kitab_page)

    def _skrol_ke_kad(self, sasaran: int):
        """Skrol senarai kitab supaya kad sasaran kelihatan ~1/3 dari atas.

        Dipanggil selepas layout selesai (julat scrollbar wujud) --
        lihat _on_kitab_page. Jika kad tidak dijumpai, skrol ke atas.
        """
        bar = self._kitab_sa.verticalScrollBar()
        for i in range(self._kitab_list.count()):
            it = self._kitab_list.itemAt(i)
            c = it.widget() if it else None
            if c is not None and getattr(c, "_hid", None) == sasaran:
                y = c.mapTo(self._kitab_sa.widget(), QPoint(0, 0)).y()
                bar.setValue(max(0, y - bar.pageStep() // 3))
                return
        bar.setValue(0)

    def _kira_halaman_lompat(self, slug: str, n: int):
        """Kira halaman yang mengandungi hadis No. n dalam kitab slug.

        Pulangkan (page, total). Kedudukan dikira dari BILANGAN hadis
        dengan id lebih kecil (bukan aritmetik mudah) -- tepat walaupun
        ada id yang hilang. Dalam mod dalam talian, penomboran hadis.my
        selanjar, jadi aritmetik mudah sudah memadai. total=0 bermakna
        had tidak diketahui.
        """
        per = self.per_page()
        total = self._total_of(slug) or 0
        if self.api.offline:
            try:
                total = self.api.max_hadis_id(slug) or total
            except Exception:
                pass
        page = (n - 1) // per + 1
        if self.api.offline:
            try:
                off = self.api.conn.execute(
                    "SELECT COUNT(*) FROM hadis "
                    "WHERE collection=? AND hadis_id<?",
                    (slug, n)).fetchone()[0]
                page = off // per + 1
            except Exception:
                pass
        return page, total

    def _sahkan_lompat(self, slug: str, n: int, nama: str):
        """Sahkan nombor hadis dalam julat kitab.

        Pulangkan (page, total) jika sah (atau julat tidak diketahui);
        papar toast dan pulangkan None jika jelas di luar julat. Dipakai
        oleh _lompat_hadis, _lompat_ke dan _buka_hadis_terus supaya
        logik julat tidak hanyut di tiga tempat.
        """
        page, total = self._kira_halaman_lompat(slug, n)
        if total and not (1 <= n <= total):
            self.toast.show_msg(f"⚠️ Hadis No. {n} tiada dalam {nama} "
                                f"(1–{total}).")
            return None
        return page, total

    def _lompat_hadis(self, n: int):
        """Lompat ke nombor hadis dalam kitab aktif (kotak sidebar)."""
        slug = self._kitab_slug
        nama = COLLECTION_META.get(slug, {}).get("name", slug)
        r = self._sahkan_lompat(slug, n, nama)
        if r is None:
            return
        page, _ = r
        self._kitab_go_to_hid = n
        self.toast.show_msg(f"📖 Hadis No. {n} — halaman {page}")
        self._load_kitab_page(page)

    def _hantar_go_box(self):
        """Hantar kotak carian nombor hadis — terus buka detail (bukan list).

        Pengguna mahu masukkan nombor hadis dan terus melihat butiran,
        bukan skrol ke kad dalam senarai. Guna _buka_hadis_terus (Sesi 38)
        yang sahkan julat dahulu, beri toast, kemudian muat butiran.
        """
        n = self._kitab_go_box.text().strip()
        if not n:
            return
        self._kitab_go_box.clear()
        try:
            n = int(n)
        except ValueError:
            return
        self._buka_hadis_terus(self._kitab_slug, n, dari="kitab")

    def _kemas_butang_atas(self):
        """Tunjuk/sembunyi butang ↑ mengikut kedudukan skrol (Sesi 34).

        Butang hanya berguna bila senarai melebihi viewport dan pengguna
        sudah skrol ke bawah (melebihi 250px). Di kedudukan atas ia
        disembunyikan supaya tidak menghalang kandungan. Kedudukan
        dikira semula pada setiap skrol dan ubah saiz tetingkap.
        """
        b = getattr(self, "_kitab_top_btn", None)
        sa = getattr(self, "_kitab_sa", None)
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

    def _skrol_atas_lancar(self):
        """Skrol lancar ke atas senarai — animasi QTimer ~250ms.

        Langkah mengecil (jarak dibahagi 15) supaya pergerakan kelihatan
        perlahan berhampiran sasaran. Timer disimpan pada `self` supaya
        panggilan kedua menghentikan animasi pertama.
        """
        bar = self._kitab_sa.verticalScrollBar()
        mula = bar.value()
        if mula <= 0:
            return
        t = getattr(self, "_top_timer", None)
        if t is not None:
            t.stop()
        t = QTimer(self)
        self._top_timer = t
        langkah = max(1, mula // 15)

        def _langkah():
            if t is not self._top_timer:
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

    def _lompat_ke(self, slug: str, n: int):
        """Lompat ke hadis No. n dalam kitab slug (dari carian pantas)."""
        nama = COLLECTION_META.get(slug, {}).get("name", slug)
        r = self._sahkan_lompat(slug, n, nama)
        if r is None:
            return
        page, _ = r
        self._kitab_go_to_hid = n
        self.toast.show_msg(f"📖 {nama} No. {n} — halaman {page}")
        self.open_kitab(slug, page)

    def _focus_lompat(self):
        """Pintasan Ctrl+G: fokus ke kotak carian nombor di sidebar.

        Jika belum di halaman kitab, buka kitab aktif dahulu (senarai
        dimuat semula); kemudian skrol kotak ke dalam pandangan dan
        fokuskan input supaya pengguna terus taip nombor.
        """
        if self.stack.currentIndex() != PAGES["kitab"]:
            self.open_kitab(self._kitab_slug, self._kitab_page)
        kotak = getattr(self, "_kitab_go_box", None)
        if kotak is None:
            return
        # Tunggu susun atur selesai (kotak mungkin baharu dibina semula
        # oleh open_kitab di atas) sebelum skrol & fokus.
        QTimer.singleShot(0, lambda: self._fokus_go_box(kotak))

    def _fokus_go_box(self, kotak):
        # Kotak ditangkap sebelum QTimer.singleShot(0); jika UI dibina
        # semula dalam pada itu (cth. tukar tema -> deleteLater), widget
        # lama sudah mati -- jangan sentuh objek SIP tertunda padam.
        if kotak is not getattr(self, "_kitab_go_box", None):
            return
        sa = getattr(self, "_kitab_sa", None)
        if sa is not None:
            sa.ensureWidgetVisible(kotak, 0, 60)
        kotak.setFocus(Qt.ShortcutFocusReason)
        kotak.selectAll()
