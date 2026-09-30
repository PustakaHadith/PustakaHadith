"""Halaman Utama — Split Command Center (25 Ogos 2026).

REKA BENTUK BAHARU (UIUX_PustakaHadith/SELECTED_UIUX.md): dua panel
kaca sebelah-menyebelah menggantikan pola lama "hero tengah → grid 9
kad" yang menyerupai hadis.my.

  KIRI  : eyebrow → tajuk hero → kiraan → carian (+Cari berasingan)
          → chip topik → jalan pantas → Petikan Hari Ini
  KANAN : HARI INI + tarikh → Terakhir dibaca (sejarah bacaan)
          → Tersimpan → Sejarah bacaan (Item 5) → Rawak
          → Pilihan Hari Ini (hadis harian)

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
    QApplication, QFrame, QHBoxLayout, QLabel, QPushButton, QVBoxLayout,
    QWidget,
)

from ui.helpers import (
    SETTINGS, _parse_lompat, _write_json, read_history,
)
from ui.pages import SearchBar
from ui.theme import COLLECTION_META
from ui.widgets import (
    BackgroundCanvas, ClickCard, IconActionButton, TeksGrad,
    attach_copy_menu, elide, make_scroll,
)
from ui.workers import HadithWorker
from utils.tarikh import teks_hijri, teks_melayu

# Chip topik pantas → query carian. Statik, mengikut mockup (v9).
TOPIK = (("Niat", "niat"), ("Solat", "solat"), ("Puasa", "puasa"),
         ("Adab", "adab"), ("Keluarga", "keluarga"))


def _norm_carian(q: str) -> str:
    """Kunci dedup cip "TERAKHIR" (Sesi 36): huruf kecil, buang semua
    tanda baca/simbol (/, ?, !, koma…), jmlah ruang. 'Hijrah/' →
    'hijrah'; 'Hijrah?' → 'hijrah'."""
    q = (q or "").lower()
    q = "".join(ch if ch.isalnum() or ch.isspace() else " " for ch in q)
    return " ".join(q.split())


def _jarak_edit(a: str, b: str) -> int:
    """Jarak Levenshtein; potong awal jika beza panjang > 1."""
    if a == b:
        return 0
    if abs(len(a) - len(b)) > 1:
        return 2
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1,
                           prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def _cari_sama(a: str, b: str) -> bool:
    """Dedup: norm sama, ATAU ejaan hampir sama (jarak edit ≤1,
    panjang ≥6) — 'hijarah' vs 'hijrah' (AI tetap dapat makna,
    jadi kedua-duanya direkod tanpa padanan ini)."""
    if a == b:
        return True
    if min(len(a), len(b)) < 6:
        return False
    return _jarak_edit(a, b) <= 1

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
        # stretch=1: baris panel MENGISI tinggi viewport bila tetingkap
        # membesar (buang ruang kosong bawah — Sesi 36). Bila kandungan
        # lebih tinggi dari viewport, QScrollArea ambil alih seperti biasa.
        bl.addWidget(baris, 1)

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

        # Baris 1 solid + baris 2 gradian (TeksGrad, gaya `.grad`
        # landing "Sekali Tayang.") — spacing 0 kekalkan jarak baris
        # seperti label \n asal.
        tajuk = QWidget()
        tv = QVBoxLayout(tajuk)
        tv.setContentsMargins(0, 0, 0, 0)
        tv.setSpacing(0)
        h1a = QLabel("Hadis Merentas Masa,")
        h1a.setObjectName("homeH1")
        h1a.setWordWrap(True)
        tv.addWidget(h1a)
        h1b = TeksGrad("Hidup Dalam Era Digital.")
        h1b.setObjectName("homeH1")
        h1b.setWordWrap(True)
        tv.addWidget(h1b)
        v.addWidget(tajuk)

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

        # Item 3 (Sesi 36) — carian terakhir: baris "TERAKHIR" + cip
        # di bawah input carian (mockup: niat · bukhari 433 · akhlak).
        self._home_akhir_row = QWidget()
        al = QHBoxLayout(self._home_akhir_row)
        al.setContentsMargins(0, 0, 0, 0)
        al.setSpacing(8)
        cap_a = QLabel("TERAKHIR:")
        cap_a.setObjectName("panelSection")
        al.addWidget(cap_a)
        self._home_akhir_lo = QHBoxLayout()
        self._home_akhir_lo.setSpacing(8)
        al.addLayout(self._home_akhir_lo)
        al.addStretch(1)
        v.addWidget(self._home_akhir_row)
        self._kemas_carian_akhir()

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
        # #3 (Sesi 37): kekal dua-dua dgn nav "Pencarian" TETAPI bezakan
        # fungsi — kad ini buka carian dgn mod "makna" (AI), nav buka
        # ikut mod terakhir pengguna. Duplikasi hilang, sasaran berbeza.
        ql.addWidget(self._kad_pantas(
            "Carian Makna", "Temui hadis berkaitan",
            self._pergi_carian), 1)
        # #1 (Sesi 37): kad "Sambung" dibuang (dup dgn "Terakhir
        # dibaca"). Pengganti C1 (pilihan pengguna): "Lompat Nombor" —
        # fungsi unik (Ctrl+G), buka kitab aktif + fokus kotak lompat.
        # + toast panduan (keputusan: kekal + toast, Sesi 37b).
        ql.addWidget(self._kad_pantas(
            "Lompat Nombor", "Ke hadis tepat · Ctrl+G",
            self._lompat_nombor_pantas), 1)
        v.addWidget(baris_pantas)

        v.addSpacing(8)
        v.addWidget(self._kad_petikan())

        # Regang: lebihan tinggi panel diserap di sini supaya kaki
        # kekal di bawah dan panel kaca memanjang ikut tetingkap.
        v.addStretch(1)

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
        # Giliran petikan: kekal pilihan pengguna jika ada (theme rebuild),
        # kalau tidak ikut hari tahun. Restart apl -> giliran hari semula.
        hari_idx = datetime.date.today().timetuple().tm_yday % len(PETIKAN)
        if getattr(self, "_petikan_idx", None) is None:
            self._petikan_idx = hari_idx
        idx = self._petikan_idx
        teks, sumber = PETIKAN[idx]
        # Item 4 (Sesi 36) — simpan petikan semasa supaya butang
        # salin/kongsi boleh rujuk teks yang sama dipapar.
        self._petikan_teks = teks
        self._petikan_sumber = sumber
        kad = QFrame()
        kad.setObjectName("sideCard")
        v = QVBoxLayout(kad)
        v.setContentsMargins(16, 12, 16, 12)
        v.setSpacing(4)

        # Baris atas: label + butang ikon (SERAGAM dengan bar tindakan
        # halaman hadis — IconActionButton "kongsi"/"salin" yang sama).
        baris = QWidget()
        bl = QHBoxLayout(baris)
        bl.setContentsMargins(0, 0, 0, 0)
        bl.setSpacing(4)
        cap = QLabel("PETIKAN RINGKAS HARI INI")
        cap.setObjectName("panelSection")
        bl.addWidget(cap)
        bl.addStretch(1)
        b_kongsi = IconActionButton("kongsi", "Kongsi petikan")
        b_kongsi.clicked.connect(self._kongsi_petikan)
        b_salin = IconActionButton("salin", "Salin petikan")
        b_salin.clicked.connect(self._salin_petikan)
        bl.addWidget(b_kongsi)
        bl.addWidget(b_salin)
        v.addWidget(baris)

        t = QLabel(teks)
        t.setObjectName("petikanText")
        t.setWordWrap(True)
        v.addWidget(t)
        s = QLabel(f"— {sumber}")
        s.setObjectName("faint")
        v.addWidget(s)
        # Rujuk label untuk Item 5 (muat semula tanpa bina semula kad).
        self._petikan_lbl_t = t
        self._petikan_lbl_s = s
        return kad

    def _muat_semula_petikan(self):
        """Item 5 (Sesi 36) — petik petikan SETERUSNYA serta-merta
        (giliran berkitar dalam PETIKAN). Pilihan kekal sepanjang
        session (termasuk tukar tema); restart apl kembali ke
        giliran hari."""
        self._petikan_idx = (self._petikan_idx + 1) % len(PETIKAN)
        teks, sumber = PETIKAN[self._petikan_idx]
        self._petikan_teks = teks
        self._petikan_sumber = sumber
        lbl_t = getattr(self, "_petikan_lbl_t", None)
        lbl_s = getattr(self, "_petikan_lbl_s", None)
        if lbl_t is not None:
            lbl_t.setText(teks)
        if lbl_s is not None:
            lbl_s.setText(f"— {sumber}")

    def _salin_petikan(self):
        """Item 4 — salin petikan + sumber ke papan klip."""
        QApplication.clipboard().setText(
            f'"{self._petikan_teks}" — {self._petikan_sumber}')
        self.toast.show_msg("Disalin ke papan klip")

    def _kongsi_petikan(self):
        """Item 4 + keputusan B (Sesi 36) — kongsi RINGKAS + baris
        'Info penuh' ke pustakahadith.my (arahan 28 Sep: label +
        pautan akar sahaja, format sama halaman hadis); Facebook guna
        pautan sama (bukan pautan hadis basi)."""
        teks = (f'"{self._petikan_teks}"\n'
                f'— {self._petikan_sumber}\n\n'
                f'Info penuh: https://pustakahadith.my')
        self._bina_menu_kongsi(teks, "https://pustakahadith.my")

    # ── panel kanan ──────────────────────────────────────────────────
    def _teks_tarikh(self) -> str:
        """Item 8 (Sesi 36) — tarikh baris HARI INI ikut Tetapan
        (`tarikh_paparan`): masihi (lalai) · melayu · hijri ·
        hijri_melayu."""
        hari = datetime.date.today()
        jenis = self.settings.get("tarikh_paparan", "masihi")
        if jenis == "hijri":
            return teks_hijri(hari)
        if jenis == "melayu":
            return teks_melayu(hari)
        if jenis == "hijri_melayu":
            return f"{teks_hijri(hari)} · {teks_melayu(hari)}"
        return hari.strftime("%d %b %Y")

    def _kemas_tarikh(self):
        """Segarkan label tarikh (dipanggil Tetapan → Paparan tarikh)."""
        lbl = getattr(self, "_lbl_tarikh", None)
        if lbl is not None:
            lbl.setText("·  " + self._teks_tarikh())

    def _panel_kanan(self) -> QFrame:
        panel = QFrame()
        panel.setObjectName("glassPanel")
        v = QVBoxLayout(panel)
        # SAIZ ASAL (kekal masa buka — arahan 28 Sep). Larasan lebih
        # besar hanya bila mode maximize 85% → `_saiz_kad(True)`.
        v.setContentsMargins(24, 24, 24, 20)
        v.setSpacing(10)
        self._kanan_lo = v

        atas = QWidget()
        al = QHBoxLayout(atas)
        al.setContentsMargins(0, 0, 0, 0)
        hari = QLabel("HARI INI")
        hari.setObjectName("panelSection")
        al.addWidget(hari)
        tarikh = QLabel("·  " + self._teks_tarikh())
        tarikh.setObjectName("faint")
        self._lbl_tarikh = tarikh
        al.addWidget(tarikh)
        al.addStretch(1)
        # Item 5 (Sesi 36) — muat semula petikan (ikut mockup: butang
        # di hujung kanan baris HARI INI; ikon seragam IconActionButton).
        b_muat = IconActionButton("muat", "Muat semula petikan", size=16)
        b_muat.clicked.connect(self._muat_semula_petikan)
        al.addWidget(b_muat)
        v.addWidget(atas)

        t = QLabel("Sambung perjalanan ilmu")
        t.setObjectName("panelTitle")
        v.addWidget(t)

        # Kad "terakhir dibaca" — kandungan dibina semula oleh
        # _render_sejarah() (dipanggil pada binaan + setiap go("home")).
        self._kad_terakhir = QFrame()
        v.addWidget(self._kad_terakhir)

        # #4 (Sesi 37) — kad "Tersimpan" DIBUANG: dup dgn nav "Simpan &
        # Sejarah" (kekal). Kekal kad "Sejarah bacaan" (tab khusus,
        # Item 5) di bawah "Terakhir dibaca".
        self._kad_sejarah = self._kad_sisi(
            str(len(read_history())),
            "Sejarah bacaan",
            "Semua hadis yang pernah anda baca",
            self._buka_sejarah_bacaan)
        self._kad_sejarah_badge = self._kad_sejarah.findChild(
            QLabel, "badgeNumb")
        v.addWidget(self._kad_sejarah)

        self._kad_rawak = self._kad_sisi(
            "⚄", "Rawak", "Terokai hadis rawak", self._random)
        v.addWidget(self._kad_rawak)

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
        # Theme rebuild semasa mode 85% — terap semula saiz besar.
        self._saiz_kad(getattr(self, "_kad_besar", False))
        return panel

    def _saiz_kad(self, besar: bool):
        """SAIZ KAD panel kanan — HANYA berubah pada mode maximize 85%.

        Arahan 28 Sep: masa buka semua saiz KEKAL ASAL (jgn ubah);
        larasan lebih besar (padding/badge/spacing → kad 76→86px) hanya
        bila `_toggle_maksimum` set `_pada_max=True` (85% skrin), supaya
        lopong sebelum "Pilihan Hari Ini" berkurang. Dipanggil:
        `_toggle_maksimum` (app_qt), `_panel_kanan` (rebuild tema),
        `_render_sejarah` (kad Terakhir dibina semula).
        """
        self._kad_besar = besar
        lo = getattr(self, "_kanan_lo", None)
        if lo is not None:
            if besar:
                lo.setContentsMargins(24, 26, 24, 24)
                lo.setSpacing(14)
            else:
                lo.setContentsMargins(24, 24, 24, 20)
                lo.setSpacing(10)
        kad_pilihan = getattr(self, "_kad_pilihan", None)
        if kad_pilihan is not None and kad_pilihan.layout() is not None:
            pv = kad_pilihan.layout()
            pv.setContentsMargins(*(16, 16, 16, 16) if besar
                                  else (16, 12, 16, 12))
            pv.setSpacing(6 if besar else 4)
        kad_terakhir = getattr(self, "_kad_terakhir", None)
        for kad in (kad_terakhir, getattr(self, "_kad_sejarah", None),
                    getattr(self, "_kad_rawak", None)):
            if kad is None:
                continue
            h = kad.layout()
            if h is None:      # placeholder kosong belum dirender
                continue
            h.setContentsMargins(*(16, 16, 16, 16) if besar
                                 else (14, 12, 14, 12))
            badge = kad.findChild(QLabel, "badgeNumb")
            if badge is not None:
                n = 52 if besar else 46
                badge.setFixedSize(n, n)
            # susunan h: [badge, kol(QVBoxLayout), panah]
            if h.count() > 1 and h.itemAt(1).layout() is not None:
                h.itemAt(1).layout().setSpacing(4 if besar else 2)

    def _kad_sisi(self, badge: str, tajuk: str, sub: str,
                  cb, *args) -> ClickCard:
        kad = ClickCard()
        kad.setObjectName("sideCard")
        kad.clicked.connect(lambda: cb(*args))
        h = QHBoxLayout(kad)
        # SAIZ ASAL (masa buka). Mod besar 85% → `_saiz_kad(True)`.
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
        self._kemas_kiraan_home()
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
        # Kad baharu guna saiz asal — terap semula mode 85% jika aktif.
        self._saiz_kad(getattr(self, "_kad_besar", False))

    def _kemas_kiraan_home(self):
        """Segarkan badge 'Sejarah bacaan' di halaman Utama supaya selari
        dgn halaman Simpan & Sejarah (failsync bila baca/buang dari tempat
        lain). Dipanggil setiap kali kembali ke Utama.

        Nota #4 (Sesi 37): kad 'Tersimpan' (badge bookmark) DIBUANG —
        kiraan bookmark hanya di nav 'Simpan & Sejarah' + halamannya."""
        badge2 = getattr(self, "_kad_sejarah_badge", None)
        if badge2 is not None:
            badge2.setText(str(len(read_history())))

    def _buka_sejarah_bacaan(self):
        """Item 5 (Sesi 36+) — kad 'Sejarah bacaan': buka halaman
        Simpan & Sejarah pada tab 'Telah dibaca'. Tetapan tab ditetap
        SEBELUM go() supaya _render_saved() bina shell dgn tab betul
        (chip 'Telah dibaca' aktif)."""
        if getattr(self, "_saved_tab", "simpan") != "baca":
            self._saved_tab = "baca"
            self._saved_filter_slug = None
        self.go("saved")

    # ── tindakan ─────────────────────────────────────────────────────
    def _catat_carian(self, q: str):
        """Item 3 (Sesi 36) — simpan carian terakhir (maks 5, terbaru
        dahulu).

        DIPANGGIL HANYA pada kejayaan: `_tampal_gabungan` (ada hasil)
        dan `_buka_hadis_terus` (lompat lulus sahkan). Carian salah
        (tiada padanan) TIDAK direkod.

        DEDUP BIJAK (AI semantik dapatkan makna untuk banyak variasi):
        'hijrah', 'hijrah/', 'Hijrah?' dan 'hijarah' semua dapat hasil
        — tanpa padanan, 'TERAKHIR' dipenuhi variasi ejaan sama. Simpan
        bentuk NORM (huruf kecil, tanpa tanda baca) dan buang entri
        norm-sama ATAU ejaan hampir (jarak edit ≤1, panjang ≥6).
        Nombor sahaja ('433') tidak direkod — konteks kitab tidak
        jelas."""
        norm = _norm_carian(q)
        if not norm or norm.replace(" ", "").isdigit():
            return
        senarai = self.settings.get("carian_akhir", []) or []
        senarai = [s for s in senarai
                   if not _cari_sama(_norm_carian(s), norm)]
        senarai.insert(0, norm)
        self.settings["carian_akhir"] = senarai[:5]
        _write_json(SETTINGS, self.settings)
        self._kemas_carian_akhir()

    def _kemas_carian_akhir(self):
        """Bina semula cip "TERAKHIR"; sembunyi baris jika tiada
        sejarah. Dipanggil dari _catat_carian dan semasa bina halaman."""
        lo = getattr(self, "_home_akhir_lo", None)
        if lo is None:
            return
        while lo.count():
            it = lo.takeAt(0)
            w = it.widget()
            if w is not None:
                w.deleteLater()
        senarai = self.settings.get("carian_akhir", []) or []
        row = getattr(self, "_home_akhir_row", None)
        if row is not None:
            row.setVisible(bool(senarai))
        for q in senarai:
            b = QPushButton(q if len(q) <= 20 else q[:19] + "…")
            b.setObjectName("chipTopik")
            b.setCursor(Qt.PointingHandCursor)
            b.setToolTip(q)
            b.clicked.connect(lambda _, qq=q: self._laksana_carian(qq))
            lo.addWidget(b)

    def _laksana_carian(self, q: str):
        """Klik cip "TERAKHIR" — hantar carian sama seperti dari input
        Utama (termasuk lompat terus 'bukhari 433'). Rekod TERAKHIR
        berlaku dalam `_tampal_gabungan` — HANYA jika ada hasil."""
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

    def _from_home_search(self):
        q = self.home_search.text()
        if not q:
            return
        # Carian pantas (sama seperti halaman Carian): 'bukhari 433' atau
        # '433' SAHAJA -> buka butiran hadis TERUS (Sesi 38). Nombor
        # sahaja guna kitab terakhir dibuka; butang Kembali menuju Utama.
        self._laksana_carian(q)

    def _carian_topik(self, q: str):
        self.search_bar.input.setText(q)
        self.go("search")
        self._do_search(1)

    def _pergi_carian(self):
        # #3 (Sesi 37) — kad "Carian Makna": paksa mod makna (AI) dulu
        # supaya berbeza dgn nav "Pencarian" (ikut mod terakhir pengguna).
        self._set_mod_carian("makna")
        self.go("search")
        self.search_bar.input.setFocus()

    def _lompat_nombor_pantas(self):
        """Kad "Lompat Nombor" (C1 — keputusan: KEKAL + toast panduan).

        Buka senarai kitab terakhir + fokus kotak "Lompat No. hadis"
        (sama dgn Ctrl+G), kemudian toast panduan supaya fungsi serta-
        merta jelas: taip nombor → Enter untuk skrol tepat ke hadis."""
        self._focus_lompat()
        self.toast.show_msg("Taip nombor hadis → Enter", 2500)

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
