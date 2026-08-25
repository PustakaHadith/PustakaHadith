"""Halaman Utama — Split Command Center (25 Ogos 2026).

REKA BENTUK BAHARU (UIUX_PustakaHadith/SELECTED_UIUX.md): dua panel
kaca sebelah-menyebelah menggantikan pola lama "hero tengah → grid 9
kad" yang menyerupai hadis.my.

  KIRI  : eyebrow → tajuk hero → kiraan → carian (+Cari berasingan)
          → chip topik → 3 jalan pantas → Petikan Hari Ini
  KANAN : HARI INI + tarikh → Terakhir dibaca (sejarah bacaan)
          → Tersimpan → Rawak → Pilihan Hari Ini (hadis harian)

Susun atur ini digunakan untuk SEMUA tema (keputusan 25 Ogos): tema
AQUA menambah latar glob (BackgroundCanvas) + panel kaca alpha 20/255;
tema lain memaparkan panel permukaan pepejal biasa tanpa latar imej.

Halaman ini TELUS (QScrollArea#homeScroll / QWidget#homeBody) supaya
latar root kelihatan. Halaman lain kekal opaque.

GANDINGAN RENTAS MIXIN: `_page_home` memanggil `open_kitab` tidak lagi;
ia memanggil `go`, `_from_home_search` → `_buka_hadis_terus` (PagesKitab/
PagesCarian) dan `_do_search` (PagesCarian), `_random` (PagesDetail),
`_total_of` (app_qt). Mesti digabungkan bersama semua mixin.

Peraturan tema: modul ini TIDAK import warna dari `ui.theme` (hanya
COLLECTION_META, metadata kitab), namun didaftar dalam `_THEMED_MODULES`
(ui/theme.py) untuk konsisten dengan modul UI yang lain.
"""

from __future__ import annotations

import datetime

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QFrame, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget,
)

from ui.helpers import _parse_lompat, read_history
from ui.pages import SearchBar
from ui.theme import COLLECTION_META
from ui.widgets import (
    BackgroundCanvas, ClickCard, attach_copy_menu, elide, make_scroll,
)
from ui.workers import HadithWorker

# Chip topik pantas → query carian. Statik, mengikut mockup (v9).
TOPIK = (("Niat", "niat"), ("Solat", "solat"), ("Puasa", "puasa"),
         ("Adab", "adab"), ("Keluarga", "keluarga"))

# Petikan Hari Ini — kurasi statik (tiada DB): giliran ikut hari tahun.
# Sumber ringkas; teks diringkaskan untuk paparan panel.
PETIKAN = (
    ("“Sesiapa yang menempuh jalan untuk mencari ilmu, Allah mudahkan "
     "baginya jalan menuju syurga.”", "Sahih Muslim 2699"),
    ("“Sesungguhnya setiap amalan bergantung pada niatnya.”",
     "Sahih al-Bukhari 1"),
    ("“Penyempurnaan kejadian seorang mukmin ialah akhlak yang baik.”",
     "Sunan at-Tirmidzi 1162"),
    ("“Dunia ini penghalang, dan sebaik-baik penghalang ialah akhlak "
     "yang baik.”", "Sahih Muslim 2664"),
    ("“Sesiapa yang tidak bersyukur kepada manusia, dia juga tidak "
     "bersyukur kepada Allah.”", "Sunan Abu Daud 4811"),
    ("“Mudah-mudahan Allah menerangi wajah orang yang mendengar "
     "perkataanku lalu menyampaikannya.”", "Sunan Ibnu Majah 231"),
    ("“Jangan marah.”", "Sahih al-Bukhari 6116"),
)


class PagesHome:
    def _buang_bayang_semua(self):
        """Tiada lagi kad berbayang (grid 9 kad dibuang, 25 Ogos).

        Kaedah KEKAL sebagai no-op kerana `go()` (app_qt.py) memanggilnya
        sebelum setCurrentIndex — buang panggilan itu juga jika suatu hari
        kaedah ini dibuang.
        """

    # ── HALAMAN: Utama ───────────────────────────────────────────────
    def _page_home(self):
        # Halaman = BackgroundCanvas (glob AQUA / warna pepejal tema
        # lain) — BUKAN QScrollArea terus. Latar kekal TETAP semasa
        # kandungan diskrol (kesan "parallax" semula jadi). Skrol
        # berlaku pada QScrollArea TELUS di dalamnya.
        kanvas = BackgroundCanvas()
        self.stack.addWidget(kanvas)
        sa = make_scroll(kanvas)
        # TELUS: QSS `QScrollArea#homeScroll` + viewport — latar kanvas
        # kelihatan di belakang kandungan.
        sa.setObjectName("homeScroll")
        body = QWidget()
        body.setObjectName("homeBody")
        sa.setWidget(body)
        bl = QVBoxLayout(body)
        bl.setContentsMargins(24, 20, 24, 20)
        bl.setSpacing(0)

        baris = QWidget()
        hl = QHBoxLayout(baris)
        hl.setContentsMargins(0, 0, 0, 0)
        hl.setSpacing(16)
        hl.addWidget(self._panel_kiri(), 62)
        hl.addWidget(self._panel_kanan(), 38)
        bl.addWidget(baris)
        bl.addStretch(1)

        # Kanvas perlu tahu saiz viewport — QScrollArea mengisi kanvas;
        # kanvas dilukis pada saiz penuhnya sendiri.
        vl = QVBoxLayout(kanvas)
        vl.setContentsMargins(0, 0, 0, 0)
        vl.addWidget(sa)

        self._render_sejarah()

    # ── panel kiri ───────────────────────────────────────────────────
    def _panel_kiri(self) -> QFrame:
        panel = QFrame()
        panel.setObjectName("glassPanel")
        v = QVBoxLayout(panel)
        v.setContentsMargins(28, 24, 28, 20)
        v.setSpacing(10)

        eyebrow = QLabel("ILMU  ·  WARISAN  ·  JARINGAN GLOBAL")
        eyebrow.setObjectName("eyebrow")
        v.addWidget(eyebrow)

        h1 = QLabel("Hadis Merentas Masa,\nHidup Dalam Era Digital.")
        h1.setObjectName("homeH1")
        h1.setWordWrap(True)
        v.addWidget(h1)

        self._home_count = QLabel("Memuatkan koleksi…")
        self._home_count.setObjectName("muted")
        v.addWidget(self._home_count)
        v.addSpacing(6)

        self.home_search = SearchBar(
            "Cari hadis, topik atau nombor… (cth. bukhari 433, B433)",
            with_chips=False)
        self.home_search.setMaximumWidth(760)
        attach_copy_menu(self.home_search.input)
        self.home_search.btn.clicked.connect(self._from_home_search)
        self.home_search.input.returnPressed.connect(self._from_home_search)
        v.addWidget(self.home_search)

        v.addSpacing(4)
        cap = QLabel("CADANGAN TOPIK")
        cap.setObjectName("panelSection")
        v.addWidget(cap)
        baris_topik = QWidget()
        tl = QHBoxLayout(baris_topik)
        tl.setContentsMargins(0, 0, 0, 0)
        tl.setSpacing(8)
        for label, q in TOPIK:
            b = QPushButton(label)
            b.setObjectName("chipTopik")
            b.setCursor(Qt.PointingHandCursor)
            b.clicked.connect(lambda _, kq=q: self._carian_topik(kq))
            tl.addWidget(b)
        tl.addStretch(1)
        v.addWidget(baris_topik)

        v.addSpacing(6)
        baris_pantas = QWidget()
        ql = QHBoxLayout(baris_pantas)
        ql.setContentsMargins(0, 0, 0, 0)
        ql.setSpacing(10)
        ql.addWidget(self._kad_pantas(
            "Jelajah 9 Kitab", "Buka rak digital", self.go, "rak"), 1)
        ql.addWidget(self._kad_pantas(
            "Carian Makna", "Temui hadis berkaitan",
            self._pergi_carian), 1)
        ql.addWidget(self._kad_pantas(
            "Sambung", "Kembali membaca", self._sambung_baca), 1)
        v.addWidget(baris_pantas)

        v.addSpacing(8)
        v.addWidget(self._kad_petikan())

        v.addSpacing(8)
        kaki = QLabel("9 kitab utama  ·  carian kata & makna (AI)  ·  "
                      "luar talian")
        kaki.setObjectName("faint")
        v.addWidget(kaki)
        return panel

    def _kad_pantas(self, tajuk: str, sub: str, cb, *args) -> QFrame:
        kad = ClickCard()
        kad.setObjectName("quickCard")
        kad.clicked.connect(lambda: cb(*args))
        h = QVBoxLayout(kad)
        h.setContentsMargins(14, 12, 14, 12)
        h.setSpacing(3)
        t = QLabel(tajuk)
        t.setObjectName("h3")
        s = QLabel(sub)
        s.setObjectName("muted")
        h.addWidget(t)
        h.addWidget(s)
        return kad

    def _kad_petikan(self) -> QFrame:
        idx = datetime.date.today().timetuple().tm_yday % len(PETIKAN)
        teks, sumber = PETIKAN[idx]
        kad = QFrame()
        kad.setObjectName("sideCard")
        v = QVBoxLayout(kad)
        v.setContentsMargins(16, 12, 16, 12)
        v.setSpacing(4)
        cap = QLabel("PETIKAN HARI INI")
        cap.setObjectName("panelSection")
        v.addWidget(cap)
        t = QLabel(teks)
        t.setObjectName("petikanText")
        t.setWordWrap(True)
        v.addWidget(t)
        s = QLabel(f"— {sumber}")
        s.setObjectName("faint")
        v.addWidget(s)
        return kad

    # ── panel kanan ──────────────────────────────────────────────────
    def _panel_kanan(self) -> QFrame:
        panel = QFrame()
        panel.setObjectName("glassPanel")
        v = QVBoxLayout(panel)
        v.setContentsMargins(24, 24, 24, 20)
        v.setSpacing(10)

        atas = QWidget()
        al = QHBoxLayout(atas)
        al.setContentsMargins(0, 0, 0, 0)
        hari = QLabel("HARI INI")
        hari.setObjectName("panelSection")
        al.addWidget(hari)
        tarikh = QLabel("·  " + datetime.date.today().strftime("%d %b %Y"))
        tarikh.setObjectName("faint")
        al.addWidget(tarikh)
        al.addStretch(1)
        v.addWidget(atas)

        t = QLabel("Sambung perjalanan ilmu")
        t.setObjectName("panelTitle")
        v.addWidget(t)

        # Kad "terakhir dibaca" — kandungan dibina semula oleh
        # _render_sejarah() (dipanggil pada binaan + setiap go("home")).
        self._kad_terakhir = QFrame()
        v.addWidget(self._kad_terakhir)

        n_simpan = len(self.bookmarks) if getattr(self, "bookmarks", None) \
            else 0
        v.addWidget(self._kad_sisi(
            str(n_simpan), "Tersimpan", "Rujukan pilihan anda",
            self.go, "saved"))
        v.addWidget(self._kad_sisi(
            "⚄", "Rawak", "Terokai hadis rawak", self._random))

        v.addStretch(1)

        # Pilihan Hari Ini — disembunyi sehingga hadis harian sampai
        # (worker DB). Gagal/DB kosong = kekal tersembunyi, halaman
        # tetap berfungsi.
        self._kad_pilihan = QFrame()
        self._kad_pilihan.setObjectName("sideCard")
        pv = QVBoxLayout(self._kad_pilihan)
        pv.setContentsMargins(16, 12, 16, 12)
        pv.setSpacing(4)
        cap = QLabel("PILIHAN HARI INI")
        cap.setObjectName("panelSection")
        pv.addWidget(cap)
        self._pilihan_tajuk = QLabel("")
        self._pilihan_tajuk.setObjectName("h3")
        self._pilihan_tajuk.setWordWrap(True)
        pv.addWidget(self._pilihan_tajuk)
        self._pilihan_petik = QLabel("")
        self._pilihan_petik.setObjectName("muted")
        self._pilihan_petik.setWordWrap(True)
        pv.addWidget(self._pilihan_petik)
        baris = QWidget()
        bl = QHBoxLayout(baris)
        bl.setContentsMargins(0, 0, 0, 0)
        bl.addStretch(1)
        self._btn_teroka = QPushButton("Teroka →")
        self._btn_teroka.setObjectName("primary")
        self._btn_teroka.setCursor(Qt.PointingHandCursor)
        self._btn_teroka.clicked.connect(self._buka_pilihan)
        bl.addWidget(self._btn_teroka)
        pv.addWidget(baris)
        self._kad_pilihan.setVisible(False)
        self._pilihan_h = None
        v.addWidget(self._kad_pilihan)
        return panel

    def _kad_sisi(self, badge: str, tajuk: str, sub: str,
                  cb, *args) -> ClickCard:
        kad = ClickCard()
        kad.setObjectName("sideCard")
        kad.clicked.connect(lambda: cb(*args))
        h = QHBoxLayout(kad)
        h.setContentsMargins(14, 12, 14, 12)
        h.setSpacing(12)
        b = QLabel(badge)
        b.setObjectName("badgeNumb")
        b.setAlignment(Qt.AlignCenter)
        b.setFixedSize(46, 46)
        h.addWidget(b)
        kol = QVBoxLayout()
        kol.setSpacing(2)
        t = QLabel(tajuk)
        t.setObjectName("h3")
        s = QLabel(sub)
        s.setObjectName("muted")
        s.setWordWrap(True)
        kol.addWidget(t)
        kol.addWidget(s)
        h.addLayout(kol, 1)
        panah = QLabel("→")
        panah.setObjectName("muted")
        h.addWidget(panah)
        return kad

    def _render_sejarah(self):
        """Bina semula kad 'Terakhir dibaca' daripada sejarah bacaan.

        Dipanggil pada binaan halaman dan setiap kali pengguna kembali
        ke Utama (go("home")) supaya kad sentiasa segar. Kosong → kad
        ajakan "Mula baca" menuju Jelajah Kitab. Kedua-dua keadaan guna
        kad sisi yang sama — hanya badge/tajuk/sub/tindakan berbeza.
        """
        kad = getattr(self, "_kad_terakhir", None)
        if kad is None:
            return
        hist = read_history()
        e = hist[0] if hist else None
        if e and e.get("slug") in COLLECTION_META:
            meta = COLLECTION_META[e["slug"]]
            baharu = self._kad_sisi(
                str(e.get("n", "?")), "Terakhir dibaca",
                f"{meta.get('short', e['slug'])} · "
                f"{elide(e.get('label', ''), 40)}",
                self._buka_hadis_terus, e["slug"], int(e.get("n", 1)),
                "home")
        else:
            baharu = self._kad_sisi(
                "📖", "Mula baca",
                "Belum ada sejarah — jelajah 9 kitab untuk mula",
                self.go, "rak")
        # Ganti widget pada kedudukan kad lama dalam layout induk.
        induk = kad.parentWidget()
        if induk is None:
            return
        lo = induk.layout()
        idx = lo.indexOf(kad)
        lo.insertWidget(idx, baharu)
        kad.setParent(None)
        kad.deleteLater()
        self._kad_terakhir = baharu

    # ── tindakan ─────────────────────────────────────────────────────
    def _from_home_search(self):
        q = self.home_search.text()
        if not q:
            return
        # Carian pantas (sama seperti halaman Carian): 'bukhari 433' atau
        # '433' SAHAJA -> buka butiran hadis TERUS (Sesi 38). Nombor
        # sahaja guna kitab terakhir dibuka; butang Kembali menuju Utama.
        j = _parse_lompat(q, default_slug=self._kitab_slug)
        if j:
            slug, n = j
            self._buka_hadis_terus(slug, n, dari="home")
            return
        self.search_bar.input.setText(q)
        if self.search_bar.chips:
            self.search_bar.chips.set_active(None, emit=False)
        self.go("search")
        self._do_search(1)

    def _carian_topik(self, q: str):
        self.search_bar.input.setText(q)
        self.go("search")
        self._do_search(1)

    def _pergi_carian(self):
        self.go("search")
        self.search_bar.input.setFocus()

    def _sambung_baca(self):
        hist = read_history()
        if hist and hist[0].get("slug"):
            e = hist[0]
            self._buka_hadis_terus(e["slug"], int(e.get("n", 1)),
                                   dari="home")
        else:
            self.go("rak")

    # ── Pilihan Hari Ini (hadis harian, deterministik ikut tarikh) ──
    def _fetch_pilihan_hari(self):
        """Ambil hadis harian: indeks = hari_tahun * 37 mod jumlah Bukhari.

        Deterministik — semua pengguna nampak hadis yang sama pada hari
        yang sama. Dipanggil dari `_on_collections` (jumlah diperlukan).
        Gagal senyap: kad kekal tersembunyi.
        """
        total = self._total_of("bukhari")
        if not isinstance(total, int) or total <= 0:
            return
        doy = datetime.date.today().timetuple().tm_yday
        hid = (doy * 37) % total + 1
        self._tok_pilihan = getattr(self, "_tok_pilihan", 0) + 1
        self._run(HadithWorker(self.api, "bukhari", hid, None,
                               self._tok_pilihan),
                  self._on_pilihan_hari, lambda m: None)

    def _on_pilihan_hari(self, h, tok):
        if tok != getattr(self, "_tok_pilihan", -1) or not h:
            return
        self._pilihan_h = h
        meta = COLLECTION_META.get(h.get("collection", ""), {})
        self._pilihan_tajuk.setText(
            f"{meta.get('name', 'Hadis')} No. {h.get('id', '?')}")
        petik = elide((h.get("melayu") or h.get("arab") or "").strip(), 150)
        self._pilihan_petik.setText(petik)
        self._kad_pilihan.setVisible(True)

    def _buka_pilihan(self):
        h = getattr(self, "_pilihan_h", None)
        if not h:
            return
        self.open_detail(h, "home")
