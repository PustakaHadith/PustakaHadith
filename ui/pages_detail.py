"""Halaman Detail (butiran hadis) — mixin PustakaApp (Sesi 30 refactor).

Dipisahkan dari `ui/app_qt.py`. Kelas `PagesDetail` menyediakan kaedah
halaman butiran hadis: render butiran, huraian SemakHadis/HadeethEnc,
syarah klasik, penilaian ulama (darjat), transliterasi, tab bahasa
(Melayu/Indonesia/English), salin/kongsi (bahasa semasa), TTS, rawak
serta penanda buku. Digabungkan ke `PustakaApp`
melalui MRO: `class PustakaApp(PagesKitab, PagesCarian, PagesDetail,
QMainWindow)`.

GANDINGAN RENTAS MIXIN: modul ini TIDAK berdiri sendiri — ia bergantung
pada state dan kaedah pada `self` (PustakaApp): stack, go, _run, _tok,
api, toast, settings, ar_scale, ar_font, tr_scale, _total_of,
_laras_tinggi, _ada_glif_selawat, _kitab_slug/_kitab_page, bookmarks.
Sebaliknya, `PagesKitab` dan `PagesCarian` memanggil `open_detail`,
`open_by_ref` dan `_papar_melayu` yang disediakan DI SINI — jangan alih
keluar kaedah ini tanpa mengemas pemanggilnya.

PENTING — tema: modul ini import WARNA dari `ui.theme` (TEXT_SECONDARY
untuk baris darjat). Ia MESTI didaftar dalam `_THEMED_MODULES`
(ui/theme.py) supaya `apply_theme()` menyalin nilai terkini ke ruang
namanya semasa tukar tema.

Pemalar LANG_LABEL / _ATRIBUSI_INGGERIS / _ATRIBUSI_SEMA / _ATRIBUSI_HE
tinggal di `ui/helpers.py` dan diimport DI SINI sahaja -- `ui.app_qt`
tidak mengimport semula (tiada pemanggil luar untuk nama-nama itu).
"""

from __future__ import annotations

import time
import webbrowser
from datetime import datetime

from PyQt5.QtCore import QUrl, Qt, QTimer
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import (
    QApplication, QFrame, QHBoxLayout, QLabel, QMenu, QPushButton,
    QStackedWidget, QVBoxLayout, QWidget,
)

from api.hadis_api import nama_bab_bm  # noqa: E402

from ui.helpers import (
    BOOKMARKS, _ATRIBUSI_HE, _ATRIBUSI_INGGERIS,
    _ATRIBUSI_SEMA, _HAD_PETIK_RINGKAS, _HAD_WA, _clear, _write_json,
    click_sound, record_reading, sunnah_url,
)
from ui.pages import LangTabs, breadcrumb
from ui.theme import (
    AMBER_BG, AMBER_BORDER, AMBER_TEXT,
    COLLECTION_META, CONTENT_MAX_W, GREEN_BG, GREEN_BORDER, GREEN_TEXT,
    GUTTER, RED_BG, RED_BORDER, RED_TEXT, TEAL, TEXT_SECONDARY,
)
from ui.widgets import (
    BAB_TAFSIR, BackgroundCanvas, Collapsible, IconActionButton,
    _ialah_bab_tafsir, arabic_browser, attach_copy_menu, centered_column,
    elide, make_scroll, text_browser,
)
from ui.workers import HadithWorker, RandomWorker
from ui.lapor_ralat import LaporRalatDialog
from utils.bahasa import betulkan_melayu, guna_simbol_selawat

# Destinasi butang Kembali mengikut halaman asal (_detail_from).
# Nilai = (label tooltip, page_key). 'kitab' ISTIMEWA: ia membuka
# senarai kitab pada halaman yang sama melalui `open_kitab` (bukan
# `go()` sahaja) — lihat `_render_detail`. Nilai `_detail_from` yang
# tidak dikenali jatuh ke 'home' (BACK_PETA["home"]).
BACK_PETA = {
    "home": ("Utama", "home"),
    "search": ("Hasil carian", "search"),
    "saved": ("Tersimpan", "saved"),
    "kitab": ("Senarai kitab", "kitab"),
}


def _warnai_cip(chip: QLabel, warna: tuple | None) -> None:
    """Guna warna ikut makna pada QLabel cip (keputusan Sesi 55 #5).

    Kekalkan objectName "chip" (ujian sedia ada mencari nama itu)
    tetapi timpa palet TEAL lalai QSS dengan warna makna. Gaya
    widget-aras mengatasi QSS app-aras; bila `warna` ialah None cip
    kekal TEAL (neutral). Nilai dibaca daripada modul tema pada masa
    render, jadi tema terang/gelap mendapat palet masing-masing.
    """
    if warna is None:
        return
    bg, txt, bd = warna
    chip.setStyleSheet(
        f"background-color: {bg}; color: {txt};"
        f" border: 1px solid {bd}; border-radius: 10px;"
        f" padding: 3px 10px; font-size: 10px; font-weight: 700;")


def _warna_cip(teks: str) -> tuple | None:
    """Warna cip ikut makna klasifikasi/darjat (keputusan Sesi 55 #5).

    Mockup menetapkan palet cip: HIJAU = sahih/sah (Sahih, Muttafaq
    'alayh, Hasan, صحيح, حسن), MERAH = palsu/ditolak (Palsu, Mawdu',
    Batil, Dusta, Munkar, موضوع, باطل, منكر), AMBER = lemah (Lemah,
    Daif, Syaz, Mudraj, ضعيف). Nilai tanpa padanan kekal neutral
    (TEAL lalai QSS) supaya klasifikasi baru tidak salah warna.
    """
    t = (teks or "").lower()
    if any(k in t for k in ("palsu", "mawdu", "batil", "dusta",
                            "tiada asal", "munkar", "موضوع",
                            "باطل", "منكر")):
        return (RED_BG, RED_TEXT, RED_BORDER)
    if any(k in t for k in ("lemah", "daif", "da'if", "syaz",
                            "shaz", "shadz", "mudraj", "ضعيف")):
        return (AMBER_BG, AMBER_TEXT, AMBER_BORDER)
    if any(k in t for k in ("sahih", "muttafaq", "hasan", "sabit",
                            "صحيح", "حسن")):
        return (GREEN_BG, GREEN_TEXT, GREEN_BORDER)
    return None


def _label_sebelum(hid) -> str | None:
    """Label butang Sebelum ('‹ No. N') pada bar navigasi bawah.

    Pulang None jika butang tidak sepatutnya dipapar: `hid` bukan int
    atau <= 1 (hadis pertama tiada pendahulu). Sebelumnya dibenamkan
    dalam `_render_detail`; kini fungsi tulen — diuji unit (semak.py
    8q) supaya syarat paparan tidak rosak tanpa disedari.
    """
    if not isinstance(hid, int) or hid <= 1:
        return None
    return f"‹ No. {hid - 1}"


def _label_seterusnya(hid, max_id) -> str | None:
    """Label butang Seterusnya ('No. N ›') pada bar navigasi bawah.

    Pulang None jika butang tidak sepatutnya dipapar: `hid` bukan int,
    atau `max_id` diketahui dan `hid >= max_id` (hadis terakhir).
    `max_id == 0` bermakna "had tidak diketahui" -> butang tetap
    dipapar. Sebelumnya dibenamkan dalam `_render_detail`; kini fungsi
    tulen — diuji unit (semak.py 8q).
    """
    if not isinstance(hid, int):
        return None
    if max_id and hid >= max_id:
        return None
    return f"No. {hid + 1} ›"


def _label_simpan(saved: bool) -> str:
    """Label butang Simpan/Tersimpan mengikut keadaan simpan.

    '⭐ Tersimpan' bila hadis sudah disimpan; '☆ Simpan' jika belum.
    Sebelumnya dibenamkan dalam `_render_detail` dan `_toggle_save`
    (3 tempat); kini fungsi tulen — diuji unit (semak.py 8r) supaya
    dua keadaan tidak tertukar tanpa disedari.
    """
    return "⭐ Tersimpan" if saved else "☆ Simpan"


def _tab_lalai(pref: str, avail: set) -> str:
    """Bahasa tab lalai mengikut keutamaan pengguna + ketersediaan.

    `pref == 'ind_only'` -> 'indonesia'; selainnya 'melayu'. Jika
    bahasa pilihan itu tidak tersedia, guna bahasa pertama yang
    tersedia; jika tiada langsung, pulang 'melayu' (pemanggil
    kosongkan). Sebelumnya dibenamkan dalam `_render_detail`; kini
    fungsi tulen — diuji unit (semak.py 8s).
    """
    first = "indonesia" if pref == "ind_only" else "melayu"
    if first not in avail:
        first = next(iter(avail), "melayu")
    return first


class PagesDetail:
    # ── HALAMAN: Detail ──────────────────────────────────────────────
    def _page_detail(self):
        # Bar navigasi DILEKATKAN di bawah, sama seperti halaman
        # Huraian. Sebabnya: hadis pendek menghasilkan kandungan 481px
        # dalam viewport 669px -- 188px ruang kosong terapung di bawah
        # butang. Melekatkan bar menghilangkan ruang itu sepenuhnya dan
        # butang sentiasa di tempat yang sama.
        luar = BackgroundCanvas(dunia=True)
        luar.setObjectName("detailPage")
        self.stack.addWidget(luar)
        ll = QVBoxLayout(luar)
        ll.setContentsMargins(0, 0, 0, 0)
        ll.setSpacing(0)

        sa = make_scroll(luar)
        sa.setObjectName("detailScroll")
        sa.setStyleSheet("background: transparent;")
        ll.addWidget(sa, 1)
        self._detail_sa = sa

        # Butang terapung "↑ ke atas" (Sesi 34) — corak sama halaman
        # kitab/carian: kelihatan bila kandungan hadis panjang (syarah,
        # darjat, huraian) dan pengguna skrol ke bawah; klik untuk
        # kembali ke teks hadis dengan animasi lancar. Anak kepada
        # QScrollArea supaya ia terapung di atas kandungan.
        if getattr(self, "_top_timer_detail", None) is not None:
            self._top_timer_detail.stop()
        self._detail_top_btn = QPushButton("↑")
        self._detail_top_btn.setObjectName("backTop")
        self._detail_top_btn.setToolTip("Ke atas — teks hadis")
        self._detail_top_btn.setCursor(Qt.PointingHandCursor)
        self._detail_top_btn.setFixedSize(44, 44)
        self._detail_top_btn.setParent(sa)
        self._detail_top_btn.clicked.connect(self._skrol_atas_lancar_detail)
        self._detail_top_btn.hide()
        sa.verticalScrollBar().valueChanged.connect(
            self._kemas_butang_atas_detail)
        _orig_resize = sa.resizeEvent

        def _on_resize(e):
            _orig_resize(e)
            self._kemas_butang_atas_detail()
            self._kemas_tajuk_detail()
            self._kemas_panel_detail()
            # Laluan kedua tertangguh: saiz sebenar mungkin belum
            # diterapkan semasa resizeEvent (halaman baru dipaparkan).
            QTimer.singleShot(0, self._kemas_semua_detail)

        sa.resizeEvent = _on_resize

        body = QWidget()
        body.setObjectName("detailBody")
        body.setStyleSheet("background: transparent;")
        sa.setWidget(body)
        self._detail_root = QVBoxLayout(body)
        self._detail_root.setContentsMargins(0, 0, 0, 12)
        self._detail_root.setSpacing(0)

        self._detail_bar = QFrame()
        self._detail_bar.setObjectName("bottombar")
        self._detail_nav = QHBoxLayout(self._detail_bar)
        self._detail_nav.setContentsMargins(28, 8, 28, 8)
        self._detail_nav.setSpacing(8)
        ll.addWidget(self._detail_bar)

    def open_detail(self, h, from_page="kitab"):
        click_sound()
        self._detail_from = from_page
        slug = h.get("collection", self._kitab_slug)
        h = dict(h)
        h["collection"] = slug
        # Darjat (Sesi 17) MESTI ada pada render pertama. Data senarai
        # tidak menyertakannya; tanpanya `_render_detail` tidak memaparkan
        # bahagian "Penilaian ulama (darjat)" sehingga worker selesai --
        # pengguna nampak ia "hilang" jika worker lambat. Baca dari DB
        # tempatan (laju, ada indeks) sebelum render.
        if "darjat" not in h:
            try:
                h["darjat"] = self.api._darjat_luar(slug, h.get("id"))
            except Exception:
                h["darjat"] = []
        # Huraian SemakHadis (BM) juga dibaca sebelum render -- sama
        # sebabnya: pengguna tidak sepatutnya nampak ia "muncul" lambat.
        if "sema" not in h:
            try:
                h["sema"] = self.api._sema_luar(slug, h.get("id"))
            except Exception:
                h["sema"] = None
        # HadeethEnc (BM) ialah sandaran: bila SemakHadis tiada, cuba
        # huraian HadeethEnc yang dipadan melalui matn Arab (jadual
        # `hadethenc` + cache .cache_he/). Dibaca sebelum render supaya
        # tidak "muncul" lambat.
        if "he" not in h:
            try:
                h["he"] = self.api._he_luar(slug, h.get("id"))
            except Exception:
                h["he"] = None
        self._detail_h = h
        self.go("detail")
        self._render_detail(h)
        # segarkan dari sumber (dapat semua bahasa)
        self._tok += 1
        tok = self._tok
        self._run(HadithWorker(self.api, slug, h.get("id"), None, tok),
                  self._on_detail_full, lambda m: None)

    def _on_detail_full(self, h, tok):
        if tok != self._tok or not h:
            return
        h = dict(h)
        h.setdefault("collection", self._detail_h.get("collection"))
        if h.get("id") == self._detail_h.get("id"):
            # `get_hadis_by_id` tidak membawa `he` (elak baca fail cache
            # .cache_he/ pada SETIAP panggilan -- ia dipanggil untuk
            # setiap kad hasil carian). Kekalkan daripada render awal
            # yang dibaca oleh `open_detail`.
            if "he" not in h:
                h["he"] = self._detail_h.get("he")
            self._detail_h = h
            self._render_detail(h)

    def open_by_ref(self, slug, hid, from_page=None):
        if from_page is not None:
            self._detail_from = from_page
        self._tok += 1
        tok = self._tok

        import time

        def _selesai(h, t):
            if not (h and t == self._tok):
                self.toast.show_msg("Hadis tidak dijumpai")
                return
            self.open_detail(h, self._detail_from)
            # Sembunyikan toast "Membuka…" (ms=0 daripada
            # _buka_hadis_terus) sebaik butiran siap dipapar — tetapi
            # jamin minimum 1800ms paparan supaya pengguna sempat baca
            # maklum balas walaupun muatan pantas. Hanya toast itu;
            # jangan sentuh toast lain (cth. "Disalin!").
            if (self.toast.isVisible()
                    and self.toast.text().startswith("📖 Membuka")
                    and hasattr(self, "_buka_toast_t0")):
                baki = 1800 - int((time.monotonic()
                                   - self._buka_toast_t0) * 1000)
                if baki > 0:
                    QTimer.singleShot(baki, self.toast.hide)
                else:
                    self.toast.hide()

        self._run(HadithWorker(self.api, slug, hid, None, tok), _selesai)

    def _render_detail(self, h):
        _clear(self._detail_root)
        slug = h.get("collection", "")
        meta = COLLECTION_META.get(slug, {})
        hid = h.get("id")
        # Sejarah bacaan (panel "Sambung perjalanan ilmu", 25 Ogos):
        # rekod automatik pada SETIAP render butiran — titik hook tunggal
        # (open_detail, _on_detail_full, pemulihan tema semua lalu di sini).
        # Label = nama bab jika ada, else potongan terjemahan. Gagal senyap.
        try:
            _label = (nama_bab_bm(slug, h.get("book"), "")
                      or elide((h.get("melayu") or "").strip(), 48))
            record_reading(slug, hid, _label)
        except Exception:
            pass

        col, cl = centered_column()
        cl.setContentsMargins(0, 18, 0, 0)
        cl.addWidget(breadcrumb([
            ("Utama", lambda: self.go("home")),
            (meta.get("name", slug), lambda: self.open_kitab(slug)),
            (f"No. {hid}", None)]))

        # Tajuk + tindakan. Lebar luas -> satu baris (tajuk kiri, butang
        # kanan). Lebar sempit -> tajuk baris pertama (membalut), butang
        # baris kedua. Sebabnya (diukur 18 Ogos, DPI 150%): satu baris
        # mahu ~1210px min — lebih daripada viewport 890px pada tetingkap
        # 900x560/1024x600 -> panel dua lajur melimpah dan teks Arab
        # (lajur kanan) terpotong oleh hbar tersembunyi. Butang dipindah
        # antara dua baris (addWidget auto-reparent), jadi susun atur luas
        # kekal satu baris seperti dahulu.
        tajuk_bar = QWidget()
        tl = QVBoxLayout(tajuk_bar)
        tl.setContentsMargins(0, 0, 0, 0)
        tl.setSpacing(6)

        self._tajuk_r1 = QHBoxLayout()
        self._tajuk_r1.setContentsMargins(0, 0, 0, 0)
        self._tajuk_r1.setSpacing(8)

        t = QLabel(f'{meta.get("name", slug)} — Hadis No. {hid}')
        t.setObjectName("h2")
        t.setWordWrap(True)
        self._tajuk_label = t
        self._tajuk_r1.addWidget(t, 1)
        self._tajuk_r1.addStretch(0)

        # Kawasan butang tindakan dengan DUA baris (responsif 18 Ogos):
        # baris 1 = butang yang muat, baris 2 = baki (bila lajur sempit
        # -- fon besar/DPI tinggi -- satu baris 4 butang boleh melebihi
        # lebar tersedia). `_kemas_butang_tindakan` memindahkan butang
        # antara baris; corak sama LangTabs/tab Arab.
        self._tajuk_butang = QWidget()
        tbl = QVBoxLayout(self._tajuk_butang)
        tbl.setContentsMargins(0, 0, 0, 0)
        tbl.setSpacing(4)
        self._tajuk_btn_r1 = QHBoxLayout()
        self._tajuk_btn_r1.setContentsMargins(0, 0, 0, 0)
        self._tajuk_btn_r1.setSpacing(8)
        self._tajuk_btn_r2 = QHBoxLayout()
        self._tajuk_btn_r2.setContentsMargins(0, 0, 0, 0)
        self._tajuk_btn_r2.setSpacing(8)
        tbl.addLayout(self._tajuk_btn_r1)
        tbl.addLayout(self._tajuk_btn_r2)
        # Bar tindakan dipindahkan ke bar bawah (ikon: WhatsApp / Salin /
        # Dengar / Simpan). Baris atas tajuk tidak lagi memaparkan butang
        # tindakan — elak berulang dengan bar bawah (keputusan pengguna).
        self._tajuk_btns = []
        self._tajuk_btn_n1 = 0
        self._tajuk_r1.addWidget(self._tajuk_butang)

        # Baris kedua (sempit): stretch + butang, dijajarkan kanan.
        # Kosong (tinggi 0) bila lebar luas.
        self._tajuk_r2 = QHBoxLayout()
        self._tajuk_r2.setContentsMargins(0, 0, 0, 0)
        self._tajuk_r2.setSpacing(8)
        self._tajuk_r2.addStretch(1)

        tl.addLayout(self._tajuk_r1)
        # Label jelas (pilihan B, 27 Ogos): nombor hadis ikut edisi
        # terjemahan sumber, bukan penomoran sunnah.com / hadith.my.
        cap = QLabel("No. rujukan PustakaHadith · mengikut edisi terjemahan "
                     "sumber (mungkin berbeza dari penomoran sunnah.com / hadith.my)")
        cap.setObjectName("muted")
        cap.setWordWrap(True)
        tl.addWidget(cap)
        tl.addLayout(self._tajuk_r2)
        self._tajuk_sempit = None
        self._kemas_tajuk_detail()
        self._kemas_panel_detail()

        cl.addWidget(tajuk_bar)
        cl.addSpacing(8)

        # Nama bab -- terjemahan BM (Kaedah B) dengan fallback EN dari CDN.
        # Baris berasingan supaya tidak bersesak dengan tajuk.
        bab = nama_bab_bm(slug, h.get("book"), h.get("nama_bab") or "").strip()
        if bab:
            bab_bar = QWidget()
            bbl = QHBoxLayout(bab_bar)
            bbl.setContentsMargins(0, 0, 0, 0)
            bbl.setSpacing(8)
            if _ialah_bab_tafsir(h.get("collection"), h.get("book")):
                tag = QLabel("Bab Tafsir")
                tag.setObjectName("chip")
                bbl.addWidget(tag)
            lbl = QLabel(f"Bab: {bab}")
            lbl.setObjectName("babName")
            lbl.setWordWrap(True)
            bbl.addWidget(lbl, 1)
            bbl.addStretch()
            cl.addWidget(bab_bar)
            cl.addSpacing(4)

        arab = (h.get("arab") or "").strip()
        avail = {k for k in ("melayu", "indonesia", "english")
                 if (h.get(k) or "").strip()}

        # Panel DUA LAJUR (keputusan Sesi 55; susunan RTL 14 Ogos):
        # TERJEMAHAN di KIRI, teks Arab asal di KANAN — menghormati
        # status teks Arab (bahasa sumber) yang lazim dibaca kanan-ke-
        # kiri; terjemahan di kiri sebagai pembaca. Lajur Arab: tab
        # ARAB/TRANSLITERASI di atas kandungan (teks Arab ATAU
        # transliterasi dua gaya). Lajur terjemahan: tab bahasa
        # (Melayu/Indonesia/English) + kotak terjemahan.
        panel_dua = QFrame()
        panel_dua.setObjectName("panel")
        # Luar: VBox = [lajur (HBox), bar tindakan]. Bar di ARAS PANEL
        # (lebar penuh) supaya 'Lapor ralat | Kongsi | Salin' sentiasa
        # SEBARIS — regresi 18 Ogos: wordWrap dalam lajur membuatnya
        # membalut ke 4 baris pada semua saiz tetingkap (label tersekat
        # 153px). Dengan lebar penuh panel ia muat pada sebarang saiz.
        pva = QVBoxLayout(panel_dua)
        pva.setContentsMargins(24, 18, 24, 18)
        pva.setSpacing(12)
        pl_wrap = QWidget()
        pl = QHBoxLayout(pl_wrap)
        pl.setContentsMargins(0, 0, 0, 0)
        pl.setSpacing(18)
        pva.addWidget(pl_wrap)
        self._panel_lo = pva
        self._panel_lajur = pl
        self._panel_sempit = None

        # ── Lajur Arab (di KANAN, ditambah selepas terjemahan) ──
        kol_arab = QVBoxLayout()
        kol_arab.setSpacing(6)

        tab_ar = QWidget()
        tab_ar_lo = QVBoxLayout(tab_ar)
        tab_ar_lo.setContentsMargins(0, 0, 0, 0)
        tab_ar_lo.setSpacing(4)
        self._tab_ar_r1 = QHBoxLayout()
        self._tab_ar_r1.setContentsMargins(0, 0, 0, 0)
        self._tab_ar_r1.setSpacing(6)
        self._tab_ar_r2 = QHBoxLayout()
        self._tab_ar_r2.setContentsMargins(0, 0, 0, 0)
        self._tab_ar_r2.setSpacing(6)
        tab_ar_lo.addLayout(self._tab_ar_r1)
        tab_ar_lo.addLayout(self._tab_ar_r2)
        self._btn_arab = QPushButton("ARAB")
        self._btn_arab.setObjectName("filterChip_active")
        self._btn_arab.setCursor(Qt.PointingHandCursor)
        self._btn_arab.clicked.connect(
            lambda: self._set_arab_tab("arab"))
        self._btn_translit = QPushButton("TRANSLITERASI")
        self._btn_translit.setObjectName("filterChip")
        self._btn_translit.setCursor(Qt.PointingHandCursor)
        self._btn_translit.clicked.connect(
            lambda: self._set_arab_tab("transliterasi"))
        # Cermin RTL: tab dijajarkan ke KANAN (sebelah teks Arab).
        # Responsif (18 Ogos): bila lajur sempit, TRANSLITERASI bungkus
        # ke baris kedua (masih kanan) -- corak sama LangTabs/tajuk.
        self._tab_ar_r1.addStretch()
        self._tab_ar_r1.addWidget(self._btn_arab)
        self._tab_ar_r1.addWidget(self._btn_translit)
        self._tab_ar_r2.addStretch()
        self._tab_ar = tab_ar
        self._tab_ar_lo = tab_ar_lo
        self._tab_ar_n_baris1 = 2
        kol_arab.addWidget(tab_ar)

        # Kandungan lajur Arab: QStackedWidget halaman 0 = teks Arab,
        # halaman 1 = transliterasi (dibina malas bila tab dipilih).
        self._ar_stack = QStackedWidget()
        if arab:
            _ab = arabic_browser(arab, self.ar_scale, self.ar_font)
            _ab._raw = arab                    # untuk "Salin semua"
            attach_copy_menu(_ab, extra=[
                ("Salin teks Arab sahaja",
                 lambda: QApplication.clipboard().setText(arab)),
            ])
            self._ar_stack.addWidget(_ab)
        else:
            _e = QLabel("Teks Arab tidak tersedia.")
            _e.setObjectName("muted")
            _e.setWordWrap(True)
            self._ar_stack.addWidget(_e)
        self._translit_dibina = False
        self._translit_page = QWidget()
        self._translit_lo = QVBoxLayout(self._translit_page)
        self._translit_lo.setContentsMargins(0, 0, 0, 0)
        self._translit_lo.setSpacing(6)
        self._ar_stack.addWidget(self._translit_page)
        self._ar_stack.setCurrentIndex(0)
        kol_arab.addWidget(self._ar_stack, 1)

        # ── Lajur terjemahan (di KIRI) ──
        kol_terjemahan = QVBoxLayout()
        kol_terjemahan.setSpacing(6)

        self._lang_tabs = LangTabs(self._switch_lang)
        self._lang_tabs.set_available(avail)
        kol_terjemahan.addWidget(self._lang_tabs)

        self._trans_box = QFrame()
        self._trans_lo = QVBoxLayout(self._trans_box)
        self._trans_lo.setContentsMargins(0, 0, 0, 0)
        self._trans_lo.setSpacing(6)
        kol_terjemahan.addWidget(self._trans_box, 1)

        # Bar tindakan bawah TERJEMAHAN sebagai IKON (bukan teks) --
        # kemas & konsisten dengan butang gear (IconActionButton).
        # Keputusan pengguna: 4 butang ikon monokrom —
        #   whatsapp (Kongsi via WhatsApp) · salin (menu popup 3 pilihan)
        #   dengar (TTS) · simpan (penanda buku, keadaan aktif terisi).
        # Tooltip kekal supaya fungsi jelas walaupun ikon.
        bar_ar = QWidget()
        bar_lo = QHBoxLayout(bar_ar)
        bar_lo.setContentsMargins(0, 0, 0, 0)
        bar_lo.setSpacing(8)
        # Lajur terjemahan di KIRI -> ikon dijajarkan ke KIRI (baris
        # latin dibaca kiri-ke-kanan). addStretch di kanan.
        b_wa = IconActionButton("whatsapp", "Kongsi via WhatsApp")
        b_wa.clicked.connect(self._share_bahasa_semasa)
        b_salin = IconActionButton("salin", "Salin")
        b_salin.clicked.connect(self._menu_salin)
        b_dengar = IconActionButton("dengar", "Dengar (TTS)")
        b_dengar.clicked.connect(lambda: self._tts(self._detail_h))
        b_simpan = IconActionButton(
            "simpan", "Simpan",
            active_inner=('<path d="M6 4h12a1 1 0 0 1 1 1v15l-7-4-7 4V5a1 1 '
                          '0 0 1 1-1z"/>'))
        b_simpan.clicked.connect(lambda: self._toggle_save(self._detail_h))
        self._save_btn_icon = b_simpan
        b_simpan.set_active(self._is_saved(h.get("collection"), h.get("id")))
        bar_lo.addWidget(b_wa)
        bar_lo.addWidget(b_salin)
        bar_lo.addWidget(b_dengar)
        bar_lo.addWidget(b_simpan)
        bar_lo.addStretch(1)
        pva.addWidget(bar_ar)

        pl.addLayout(kol_terjemahan, 1)   # kiri dahulu
        pl.addLayout(kol_arab, 1)         # Arab di kanan
        cl.addWidget(panel_dua)

        pref = self.settings.get("language_pref", "both")
        first = _tab_lalai(pref, avail)
        self._lang_tabs.set_active(first, emit=False)
        self._switch_lang(first)

        # Huraian SemakHadis (Fasa 4) -- syarah Bahasa Melayu sebenar
        # (terjemahan + komentar + status hadis), dipadan ikut teks Arab.
        # Lebih utama daripada syarah Arab klasik: letak di sini, terbuka
        # secara lalai supaya pengguna yang mencari huraian terus nampak.
        sema = h.get("sema")
        if sema:
            cl.addSpacing(2)
            kol = Collapsible(
                f"Huraian (SemakHadis · {sema.get('klasifikasi') or 'tanpa status'})",
                lambda lo, s=sema: self._bina_sema(lo, s))
            kol.buka()
            cl.addWidget(kol)
        else:
            # Sandaran HadeethEnc -- untuk hadis yang tiada huraian
            # SemakHadis tetapi dipadan kepada HadeethEnc (211 hadis).
            he = h.get("he")
            if he and (he.get("hadeeth") or he.get("explanation")):
                cl.addSpacing(2)
                kol = Collapsible(
                    f"Huraian (HadeethEnc · {he.get('grade') or 'tanpa status'})",
                    lambda lo, s=he: self._bina_he(lo, s))
                kol.buka()
                cl.addWidget(kol)

        # Syarah klasik (Fasa 4B) -- Arab gundul, panjang, Bukhari
        # sahaja. Tertutup lalai: rujukan pilihan untuk pembaca Arab,
        # bukan huraian utama. Dibina malas.
        if self._ada_syarah(slug, hid):
            cl.addSpacing(2)
            cl.addWidget(Collapsible(
                "Syarah klasik (Arab)",
                lambda lo, sg=slug, i=hid: self._bina_syarah(lo, sg, i)))

        # Penilaian ulama moden (Sesi 14) -- papar mentah, tanpa
        # tafsiran. DIPAPAR TERBUKA (keputusan Sesi 55 #4, berbeza
        # daripada Sesi 14 yang tertutup): mockup bukharin1/nasai2117/
        # abudaud4177 memaparkan darjat TERBUKA di bawah huraian.
        cl.addSpacing(2)
        kol_darjat = Collapsible(
            "Penilaian ulama (darjat)",
            lambda lo, sg=slug, i=hid: self._bina_darjat(lo, sg, i))
        kol_darjat.buka()
        cl.addWidget(kol_darjat)

        # Navigasi -- ditulis ke bar TETAP di luar kawasan skrol.
        _clear(self._detail_nav)
        nl = self._detail_nav

        # Label seragam "Kembali" -- sama seperti halaman Huraian.
        # DESTINASI kekal berbeza mengikut halaman asal; tooltip
        # memberitahu ke mana ia pergi tanpa memanjangkan butang.
        # Peta BACK_PETA diuji unit (semak.py 8p) supaya setiap
        # _detail_from memetakan ke halaman yang betul.
        tujuan, page_key = BACK_PETA.get(self._detail_from,
                                         BACK_PETA["home"])
        if page_key == "kitab":
            fn = lambda: self.open_kitab(slug, self._kitab_page)
        else:
            fn = lambda: self.go(page_key)
        bb = QPushButton("\u2039  Kembali")
        bb.setToolTip(f"Kembali ke {tujuan}")
        bb.setObjectName("ghost")
        bb.setCursor(Qt.PointingHandCursor)
        bb.clicked.connect(fn)
        nl.addWidget(bb)
        nl.addStretch()

        nl.addSpacing(12)

        # JANGAN panggil api.max_hadis_id() di sini. Dalam mod dalam
        # talian ia melakukan permintaan rangkaian pada thread UI --
        # diukur 1.10s beku setiap kali hadis dibuka (throttle 1.1s).
        # Guna `collections` yang sudah dimuat secara tak segerak; jika
        # belum ada, 0 bermakna "had tidak diketahui" dan butang
        # Seterusnya tetap dipapar.
        max_id = self._total_of(slug) or 0
        if self.api.offline:
            try:
                max_id = self.api.max_hadis_id(slug) or max_id
            except Exception:
                pass

        lbl_sebelum = _label_sebelum(hid)
        if lbl_sebelum:
            p = QPushButton(lbl_sebelum)
            p.setObjectName("ghost")
            p.setCursor(Qt.PointingHandCursor)
            p.clicked.connect(lambda: self.open_by_ref(slug, hid - 1))
            nl.addWidget(p)
        lbl_seterusnya = _label_seterusnya(hid, max_id)
        if lbl_seterusnya:
            n = QPushButton(lbl_seterusnya)
            n.setObjectName("ghost")
            n.setCursor(Qt.PointingHandCursor)
            n.clicked.connect(lambda: self.open_by_ref(slug, hid + 1))
            nl.addWidget(n)

        self._detail_root.addWidget(col)
        self._detail_root.addStretch(1)
        self._kemas_panel_detail()
        # Laluan kedua tertangguh (lihat _kemas_semua_detail): reflow
        # dengan saiz SEBENAR selepas halaman dipaparkan.
        QTimer.singleShot(0, self._kemas_semua_detail)
        self._detail_sa.verticalScrollBar().setValue(0)

    def _set_arab_tab(self, mode: str):
        """Tukar kandungan lajur Arab: 'arab' atau 'transliterasi'.

        Keputusan Sesi 55: lajur Arab ada tab ARAB/TRANSLITERASI. Teks
        Arab ialah halaman lalai (0); transliterasi dibina MALAS pada
        buka pertama (halaman 1) supaya hadis yang tidak pernah dibuka
        tidak membazir masa transliterasi — sama seperti Collapsible.
        """
        self._ar_stack.setCurrentIndex(1 if mode == "transliterasi" else 0)
        # Kemas gaya tab aktif
        for b, m in ((self._btn_arab, "arab"),
                     (self._btn_translit, "transliterasi")):
            b.setObjectName("filterChip_active" if m == mode
                            else "filterChip")
            b.style().unpolish(b)
            b.style().polish(b)
        if mode == "transliterasi" and not self._translit_dibina:
            self._translit_dibina = True
            self._bina_translit(self._translit_lo,
                                (self._detail_h.get("arab") or "").strip())

    def _bina_translit(self, lo, arab):
        """Bina kandungan bahagian transliterasi (dipanggil bila dibuka).

        Dua gaya: akademik (dengan diakritik) + gaya Melayu (tanpa).
        Gaya Melayu didahulukan -- lebih mudah dibaca pengguna tempatan.
        """
        try:
            from core.phase2_transliterasi import transliterate_arabic
            r = transliterate_arabic(arab)
        except Exception as e:
            lbl = QLabel(f"Transliterasi tidak tersedia: {e}")
            lbl.setObjectName("muted")
            lbl.setWordWrap(True)
            lo.addWidget(lbl)
            return

        box = QFrame()
        box.setObjectName("panel")
        bl = QVBoxLayout(box)
        bl.setContentsMargins(24, 16, 24, 18)
        bl.setSpacing(4)
        # AlignTop: elak panel dipusatkan menegak dalam lajur yang lebih
        # tinggi (corak sama pembaikan Sesi 55 pada kotak terjemahan).
        lo.addWidget(box, 0, Qt.AlignTop)
        lo = bl                      # tulis kandungan ke dalam panel

        baris = [
            ("Gaya Melayu", r.get("rumi_malay_style", "")),
            ("Akademik", r.get("rumi", "")),
        ]
        ada = False
        for tajuk, teks in baris:
            teks = (teks or "").strip()
            if not teks:
                continue
            ada = True
            # Simbol selawat ﷺ (Sesi 34) — konsisten dengan paparan
            # Melayu: bila pengguna memilih simbol, selawat dalam rumi
            # (gaya Melayu + akademik) turut diganti dengan ligatur.
            if (self.settings.get("simbol_selawat", True)
                    and self._ada_glif_selawat):
                teks = guna_simbol_selawat(teks)
            cap = QLabel(tajuk.upper())
            cap.setObjectName("faint")
            lo.addWidget(cap, 0, Qt.AlignTop)

            tb = text_browser(teks, self.tr_scale, justify=True)
            tb._raw = teks
            attach_copy_menu(tb)
            lo.addWidget(tb, 0, Qt.AlignTop)

        if not ada:
            lbl = QLabel("Transliterasi tidak tersedia untuk teks ini.")
            lbl.setObjectName("muted")
            lbl.setWordWrap(True)
            lo.addWidget(lbl, 0, Qt.AlignTop)
        # Ruang menegak berlebihan MESTI tinggal DI BAWAH kandungan
        # (bukan memusatkan) -- corak sama pembaikan Sesi 55.
        lo.addStretch(1)

    def _ada_syarah(self, slug, hid) -> bool:
        """Semakan murah: adakah syarah wujud? Elak bina Collapsible kosong."""
        conn = getattr(self.api, "conn", None)
        if conn is None:
            return False
        try:
            r = conn.execute(
                "SELECT 1 FROM syarah WHERE collection=? AND hadis_id=? LIMIT 1",
                (slug, hid)).fetchone()
        except Exception:
            return False        # jadual belum wujud
        return bool(r)

    def _bina_syarah(self, lo, slug, hid):
        """Isi bahagian syarah (dipanggil hanya bila dibuka)."""
        try:
            from core.syarah_source import ambil
            senarai = ambil(self.api.conn, slug, hid)
        except Exception as e:
            lbl = QLabel(f"Syarah tidak tersedia: {e}")
            lbl.setObjectName("muted")
            lbl.setWordWrap(True)
            lo.addWidget(lbl)
            return

        if not senarai:
            lbl = QLabel("Tiada syarah untuk hadis ini.")
            lbl.setObjectName("muted")
            lo.addWidget(lbl)
            return

        for sy in senarai:
            box = QFrame()
            box.setObjectName("panel")
            bl = QVBoxLayout(box)
            bl.setContentsMargins(24, 16, 24, 18)
            bl.setSpacing(6)

            tajuk = QLabel(f'{sy["nama"]} — {sy["pengarang"]}')
            tajuk.setObjectName("faint")
            tajuk.setWordWrap(True)
            bl.addWidget(tajuk)

            teks = sy["teks"]
            # Median 1,971 aksara; ada yang 72,688. Potong supaya
            # susun atur tidak runtuh, sediakan salinan penuh via menu.
            HAD = 4000
            papar = teks[:HAD] + (" …" if len(teks) > HAD else "")
            tb = arabic_browser(papar, self.ar_scale, self.ar_font)
            tb._raw = teks
            attach_copy_menu(tb, extra=[
                ("Salin syarah penuh",
                 lambda t=teks: QApplication.clipboard().setText(t)),
            ])
            bl.addWidget(tb)

            if len(teks) > HAD:
                lagi = QLabel(f"Dipendekkan daripada {len(teks):,} aksara. "
                              "Klik kanan → Salin syarah penuh.")
                lagi.setObjectName("faint")
                lagi.setWordWrap(True)
                bl.addWidget(lagi)

            lesen = QLabel(sy["lesen"])
            lesen.setObjectName("faint")
            lesen.setWordWrap(True)
            bl.addWidget(lesen)

            lo.addWidget(box)

    def _bina_sema(self, lo, sema):
        """Isi bahagian huraian SemakHadis (BM) — dipanggil bila dibuka.

        Kandungan: tajuk, terjemahan BM, takhrij (intro), komentar BM,
        dan atribusi. Teks komentar boleh panjang (ada yang >5,000
        aksara) -- potong untuk paparan, salinan penuh via menu.

        Semua teks Melayu melalui `_papar_melayu` (ejaan DBP + simbol
        selawat) -- konsisten dengan paparan hadis utama dan Salin/
        Kongsi. Penukaran pada teks PENUH dahulu, kemudian potong,
        supaya "Salin komentar penuh" selaras dengan paparan.
        """
        box = QFrame()
        box.setObjectName("panel")
        bl = QVBoxLayout(box)
        bl.setContentsMargins(24, 16, 24, 18)
        bl.setSpacing(6)
        lo.addWidget(box)
        bl2 = bl                      # tulis ke dalam panel

        tajuk = (sema.get("tajuk") or "").strip()
        if tajuk:
            t = QLabel(self._papar_melayu(tajuk))
            t.setObjectName("h3")
            t.setWordWrap(True)
            bl2.addWidget(t)

        klas = (sema.get("klasifikasi") or "").strip()
        if klas:
            chip = QLabel(klas)
            chip.setObjectName("chip")
            _warnai_cip(chip, _warna_cip(klas))
            bl2.addWidget(chip)

        mt = self._papar_melayu((sema.get("malay_text") or "").strip())
        if mt:
            cap = QLabel("TERJEMAHAN".upper())
            cap.setObjectName("faint")
            bl2.addWidget(cap)
            tb = text_browser(mt, self.tr_scale, justify=True)
            tb._raw = mt
            attach_copy_menu(tb)
            bl2.addWidget(tb)

        intro = self._papar_melayu((sema.get("intro") or "").strip())
        if intro:
            cap = QLabel("TAKHIJ".upper())
            cap.setObjectName("faint")
            bl2.addWidget(cap)
            tb = text_browser(intro, self.tr_scale, justify=True)
            tb._raw = intro
            attach_copy_menu(tb)
            bl2.addWidget(tb)

        syarah = self._papar_melayu((sema.get("syarah") or "").strip())
        if syarah:
            cap = QLabel("KOMENTAR".upper())
            cap.setObjectName("faint")
            bl2.addWidget(cap)
            HAD = 8000
            papar = syarah[:HAD] + (" …" if len(syarah) > HAD else "")
            tb = text_browser(papar, self.tr_scale, justify=True)
            tb._raw = syarah
            attach_copy_menu(tb, extra=[
                ("Salin komentar penuh",
                 lambda s=syarah: QApplication.clipboard().setText(s)),
            ])
            bl2.addWidget(tb)
            if len(syarah) > HAD:
                lagi = QLabel(f"Dipendekkan daripada {len(syarah):,} aksara. "
                              "Klik kanan → Salin komentar penuh.")
                lagi.setObjectName("faint")
                lagi.setWordWrap(True)
                bl2.addWidget(lagi)

        lesen = QLabel(sema.get("lesen") or _ATRIBUSI_SEMA)
        lesen.setObjectName("faint")
        lesen.setWordWrap(True)
        bl2.addWidget(lesen)

    def _bina_he(self, lo, he):
        """Isi bahagian huraian HadeethEnc (BM) — sandaran Fasa 4.

        Kandungan: tajuk, terjemahan BM (hadeeth), penjelasan
        (explanation), pengajaran (hints), darjat (grade), dan atribusi.
        Kandungan HadeethEnc TIDAK diubah -- atribusi wajib mengikut
        syarat HadeethEnc.com (projek IslamHouse).
        """
        box = QFrame()
        box.setObjectName("panel")
        bl = QVBoxLayout(box)
        bl.setContentsMargins(24, 16, 24, 18)
        bl.setSpacing(6)
        lo.addWidget(box)
        bl2 = bl                      # tulis ke dalam panel

        tajuk = (he.get("tajuk") or "").strip()
        if tajuk:
            t = QLabel(tajuk)
            t.setObjectName("h3")
            t.setWordWrap(True)
            bl2.addWidget(t)

        grade = (he.get("grade") or "").strip()
        if grade:
            chip = QLabel(grade)
            chip.setObjectName("chip")
            _warnai_cip(chip, _warna_cip(grade))
            bl2.addWidget(chip)

        mt = (he.get("hadeeth") or "").strip()
        if mt:
            cap = QLabel("TERJEMAHAN".upper())
            cap.setObjectName("faint")
            bl2.addWidget(cap)
            tb = text_browser(mt, self.tr_scale, justify=True)
            tb._raw = mt
            attach_copy_menu(tb)
            bl2.addWidget(tb)

        ex = (he.get("explanation") or "").strip()
        if ex:
            cap = QLabel("PENJELASAN".upper())
            cap.setObjectName("faint")
            bl2.addWidget(cap)
            tb = text_browser(ex, self.tr_scale, justify=True)
            tb._raw = ex
            attach_copy_menu(tb)
            bl2.addWidget(tb)

        hints = [str(x).strip() for x in (he.get("hints") or []) if str(x).strip()]
        if hints:
            cap = QLabel("PENGAJARAN".upper())
            cap.setObjectName("faint")
            bl2.addWidget(cap)
            teks = "\n".join(hints)
            tb = text_browser(teks, self.tr_scale, justify=True)
            tb._raw = teks
            attach_copy_menu(tb)
            bl2.addWidget(tb)

        lesen = QLabel(_ATRIBUSI_HE)
        lesen.setObjectName("faint")
        lesen.setWordWrap(True)
        bl2.addWidget(lesen)

    def _bina_darjat(self, lo, slug, hid):
        """Isi bahagian penilaian ulama (dipanggil hanya bila dibuka).

        Prinsip Sesi 14: papar SEMUA nama + teks darjat apa adanya --
        tiada normalisasi, tiada warna, tiada ikon, tiada susunan
        keutamaan. Susunan ialah susunan simpanan CDN.
        """
        try:
            senarai = self.api._darjat_luar(slug, hid)
        except Exception as e:
            lbl = QLabel(f"Penilaian tidak tersedia: {e}")
            lbl.setObjectName("muted")
            lbl.setWordWrap(True)
            lo.addWidget(lbl)
            return

        if not senarai:
            lbl = QLabel("Tiada penilaian ulama untuk hadis ini dalam sumber.")
            lbl.setObjectName("muted")
            lbl.setWordWrap(True)
            lo.addWidget(lbl)
            return

        box = QFrame()
        box.setObjectName("panel")
        bl = QVBoxLayout(box)
        bl.setContentsMargins(24, 16, 24, 18)
        bl.setSpacing(10)

        for p in senarai:
            baris = QLabel(f"{p['nama']} — {p['darjat']}")
            baris.setWordWrap(True)
            baris.setStyleSheet(f"font-size: 13px; color: {TEXT_SECONDARY};")
            bl.addWidget(baris)

        nota = QLabel(
            "Penilaian ini daripada ulama hadis moden. Ulama boleh "
            "berbeza pendapat. Rujuk ahli ilmu untuk kepastian.")
        nota.setObjectName("quote")
        nota.setWordWrap(True)
        bl.addWidget(nota)

        sumber = QLabel("Sumber: fawazahmed0/hadith-api (Unlicense)")
        sumber.setObjectName("faint")
        sumber.setWordWrap(True)
        bl.addWidget(sumber)

        lo.addWidget(box)

    def _papar_melayu(self, teks: str) -> str:
        """Sediakan teks Melayu untuk paparan.

        Dua langkah: betulkan ejaan Indonesia, kemudian (jika dipilih)
        ganti frasa selawat dengan ligatur Arab ﷺ.

        Ligatur BUKAN singkatan -- ia satu titik kod yang mengandungi
        lafaz penuh, jadi ia tidak termasuk dalam tegahan ulama
        terhadap "SAW". Tetapi ia hanya diguna jika fon sistem
        benar-benar ada glifnya; jika tidak pengguna nampak tofu.
        """
        t = betulkan_melayu(teks)
        if self.settings.get("simbol_selawat", True) and self._ada_glif_selawat:
            t = guna_simbol_selawat(t)
        return t

    def _switch_lang(self, key):
        _clear(self._trans_lo)

        txt = (self._detail_h.get(key) or "").strip()
        self._lang_key = key
        # Betulkan ejaan Indonesia yang tertinggal ("Shallallahu" ->
        # "Sallallahu"). PAPARAN sahaja -- teks dalam hadis.db kekal
        # asal. Diukur: 66% hadis terjejas, dan HANYA satu perkataan
        # itu berubah pada 500 sampel.
        if key == "melayu":
            txt = self._papar_melayu(txt)
        # Keputusan mockup (Sesi 55): paparan bahasa tunggal = TAB + teks
        # SAHAJA. Label LANG_LABEL dan baris Salin/Kongsi TIDAK wujud di
        # bawah tab -- ia menolak teks terjemahan ke bawah sehingga tidak
        # sama paras dengan teks Arab di lajur kiri. Tindakan kekal di
        # bar tajuk (WhatsApp/Kongsi + Salin) dan menu klik kanan.
        # Tab "Sebelah" (bandingan) juga DIBUANG -- bukan dalam mockup,
        # dan terjemahan di dalamnya tidak sama paras dengan teks Arab.
        if txt:
            _tb = text_browser(txt, self.tr_scale, justify=True)
            _tb._raw = txt
            attach_copy_menu(_tb)
            self._trans_lo.addWidget(_tb, 0, Qt.AlignTop)

            # Atribusi wajib: Melayu/Indonesia dari hadis.my; Inggeris
            # dari sumber luar yang dipadan melalui teks Arab.
            if key == "english":
                src = QLabel(_ATRIBUSI_INGGERIS)
                src.setObjectName("faint")
                src.setWordWrap(True)
                self._trans_lo.addWidget(src, 0, Qt.AlignTop)
        else:
            e = QLabel("Terjemahan tidak tersedia untuk hadis ini.")
            e.setObjectName("muted")
            e.setWordWrap(True)
            self._trans_lo.addWidget(e, 0, Qt.AlignTop)
        # SAMA PARAS (keputusan Sesi 55, ditegaskan semula): bila lajur
        # Arab lebih tinggi, ruang menegak berlebihan dalam `_trans_box`
        # MESTI tinggal DI BAWAH teks terjemahan, bukan memusatkannya --
        # Qt memusatkan widget saiz tetap dalam QVBoxLayout bila ada
        # ruang lebih, menyebabkan teks terjemahan jatuh ke tengah dan
        # tidak sama paras dengan teks Arab di lajur kiri (mengganggu
        # pembaca). addStretch menyerap ruang itu di bahagian bawah.
        self._trans_lo.addStretch(1)

    def _kepala_hadis(self) -> str:
        """Tajuk rujukan hadis: '{nama kitab} No. {nombor}'.

        Satu sumber kebenaran untuk `_teks_bahasa_semasa` supaya tajuk
        tidak hanyut.
        """
        h = self._detail_h or {}
        nama = COLLECTION_META.get(h.get("collection", ""), {}).get("name", "")
        return f"{nama} No. {h.get('id')}"

    def _teks_bahasa_semasa(self, had: int = 0) -> str:
        """Gabung tajuk + Arab penuh + terjemahan bahasa yang dipapar.

        Digunakan oleh "📋 Salin" ke papan klip (Arab penuh, berguna
        untuk rujukan sendiri) -- kongsi WhatsApp kini TERUS guna format
        "Ringkas" (Sesi 36). Arab dipapar TERUS tanpa label [ARAB];
        terjemahan
        dilabel [TERJEMAHAN] (bukan nama bahasa) supaya format mesej
        konsisten untuk semua bahasa. `_papar_melayu` dipakai pada teks
        Melayu. `had` mengehadkan panjang (untuk WhatsApp) -- 0 = tiada
        had.
        """
        h = self._detail_h or {}
        key = self._lang_key or "melayu"
        teks = (h.get(key) or "").strip()
        if not teks:
            return self._kepala_hadis()
        if key == "melayu":
            teks = self._papar_melayu(teks)
        arab = (h.get("arab") or "").strip()
        hasil = (f"{self._kepala_hadis()}\n\n{arab}"
                 f"\n\n[TERJEMAHAN]\n{teks}")
        if had and len(hasil) > had:
            hasil = hasil[:had] + "…"
        return hasil

    def _petik_ringkas(self, teks: str,
                       had: int = _HAD_PETIK_RINGKAS) -> str:
        """Petikan Arab (~10 baris, sepadan contoh pengguna) untuk kongsi
        "Ringkas".

        Potong pada sempadan ruang/ayat terakhir dalam had supaya teks
        tidak putus di tengah perkataan; "…" ditambah bila terpotong.
        Ini pengganti format petikan lama (dibuang Sesi 35) -- kini
        HANYA untuk pilihan kongsi "Ringkas", bukan format tunggal.
        """
        teks = (teks or "").strip()
        if not teks or len(teks) <= had:
            return teks
        potong = teks[:had]
        i = max(potong.rfind(p) for p in (".", "؟", "!", " "))
        if i > 0:
            return potong[:i].rstrip() + "…"
        return potong + "…"

    def _teks_kongsi_ringkas(self) -> str:
        """Kongsi WhatsApp "Ringkas": tajuk + petikan Arab + terjemahan penuh.

        Petikan Arab ~10 baris (~700 aksara) supaya KEDUA-DUA Arab dan
        terjemahan kelihatan dalam gelembung WhatsApp. Untuk hadis
        panjang, "Read more" asli WhatsApp muncul di hujung terjemahan
        (ketuk untuk baca baki -- keseluruhan mesej). Penerima boleh
        baca terjemahan penuh sahaja atau petikan Arab sahaja. Format
        label sama dengan `_teks_bahasa_semasa`: Arab terus tanpa label;
        terjemahan dilabel [TERJEMAHAN]. Di hujung mesej ditambah
        pautan "Baca penuh" sunnah.com (bila padanan wujud) supaya
        penerima boleh buka hadis penuh di pelayar; tiada pautan untuk
        kitab yang tiada sumber (ahmad, darimi).
        """
        h = self._detail_h or {}
        key = self._lang_key or "melayu"
        teks = (h.get(key) or "").strip()
        if not teks:
            return self._kepala_hadis()
        if key == "melayu":
            teks = self._papar_melayu(teks)
        petik = self._petik_ringkas(h.get("arab") or "")
        bahagian = [self._kepala_hadis()]
        if petik:
            bahagian.append(petik)
        bahagian.append(f"[TERJEMAHAN]\n{teks}")
        return self._teks_baca_penuh("\n\n".join(bahagian))

    def _teks_baca_penuh(self, teks: str) -> str:
        """Tambah baris 'Baca penuh' sunnah.com pada teks kongsi Ringkas.

        Pautan ditambah bila padanan wujud (lihat `sunnah_url`); tanpa
        padanan, teks pulang tanpa perubahan supaya mesej tidak rosak.
        """
        h = self._detail_h or {}
        url = sunnah_url(h.get("collection", ""), h.get("id"))
        if not url:
            return teks
        return f"{teks}\n\nBaca penuh: {url}"

    def _buka_wa(self, teks: str) -> None:
        """Buka wa.me dengan teks kongsi -- had keselamatan `_HAD_WA`.

        Pautan "Baca penuh" (jika ada) DIKEKALKAN walaupun mesej
        dipotong -- ia yang memberi akses teks penuh kepada penerima
        (Sesi 36; pepijat dijumpai semasa demo output sebenar: pautan
        terpotong oleh had, kini dikekalkan).
        """
        kata = "Baca penuh: "
        badan, sep, link = teks.rpartition(f"\n\n{kata}")
        if not sep:
            badan, link = teks, ""
        else:
            link = kata + link
        if len(badan) > _HAD_WA:
            badan = badan[: _HAD_WA] + "…"
        teks = f"{badan}\n\n{link}" if link else badan
        webbrowser.open(
            "https://wa.me/?text=" + QUrl.toPercentEncoding(teks).data().decode())

    def _share_bahasa_semasa(self):
        """Kongsi bahasa semasa melalui WhatsApp (wa.me) -- terus Ringkas.

        Keputusan pengguna (Sesi 36): TIADA menu pilihan -- kongsi
        sentiasa guna format "Ringkas" (petikan Arab + terjemahan penuh
        + pautan "Baca penuh"). WhatsApp memaparkan SATU "Read more"
        asli untuk mesej panjang (di hujung terjemahan untuk hadis
        panjang); tiada bahagian boleh-kembang berasingan.
        """
        self._buka_wa(self._teks_kongsi_ringkas())

    # ── Tindakan ─────────────────────────────────────────────────────
    def _copy(self, h):
        name = COLLECTION_META.get(h.get("collection", ""), {}).get("name", "")
        parts = [f"{name} No. {h.get('id')}", h.get("arab", ""),
                 self._papar_melayu(h.get("melayu", ""))]
        QApplication.clipboard().setText("\n\n".join(p for p in parts if p))
        self.toast.show_msg("Disalin ke papan klip")

    def _lapor_ralat(self):
        """Buka dialog 'Lapor Ralat' untuk e-mel laporan ke pembangun.

        Pautan 'Lapor ralat' pada bar tindakan bawah terjemahan
        (sebaris 'Kongsi | Salin') membuka dialog e-mel, bukan sunnah.com.
        """
        dlg = LaporRalatDialog(app=self, parent=self)
        dlg.exec_()

    def _menu_salin(self):
        """Menu popup 'Salin' (pautan teks) bawah terjemahan.

        Pilihan: Arab sahaja, terjemahan bahasa semasa, atau semuanya
        (rujukan + Arab + terjemahan). Menu dipaparkan pada KEDUDUKAN
        KURSOR -- bukan di bawah pautan -- supaya sentiasa kelihatan
        walaupun bar berada di hujung skrol (punca "3 pilihan tak
        fungsi" sebelum ini: menu dibuka di bawah butang yang mungkin
        di luar skrin).
        """
        h = self._detail_h or {}
        key = self._lang_key or "melayu"
        tr = (h.get(key) or "").strip()
        if key == "melayu":
            tr = self._papar_melayu(tr)
        arab = (h.get("arab") or "").strip()

        m = QMenu(self)
        if arab:
            m.addAction("Salin Arab sahaja", lambda: self._salin_ke(
                arab, "Arab disalin"))
        if tr:
            m.addAction("Salin terjemahan (bahasa semasa)",
                        lambda: self._salin_ke(tr, "Terjemahan disalin"))
        m.addAction("Salin Arab + terjemahan semasa",
                    self._salin_arab_terjemahan)
        m.exec_(QCursor.pos())

    def _salin_ke(self, teks: str, mesej: str):
        QApplication.clipboard().setText(teks)
        self.toast.show_msg(mesej)

    def _salin_arab_terjemahan(self):
        """Salin Arab + terjemahan bahasa SEMASA (tanpa rujukan).

        Pilihan ke-3 menu Salin (keputusan pengguna 13 Ogos): bukan
        "semuanya" (rujukan + Arab + terjemahan) -- hanya Arab +
        terjemahan bahasa yang aktif sekarang.
        """
        h = self._detail_h or {}
        key = self._lang_key or "melayu"
        tr = (h.get(key) or "").strip()
        if key == "melayu":
            tr = self._papar_melayu(tr)
        arab = (h.get("arab") or "").strip()
        QApplication.clipboard().setText(
            "\n\n".join(p for p in (arab, tr) if p))
        self.toast.show_msg("Disalin: Arab + terjemahan")

    def _tts(self, h):
        txt = (h.get("arab") or h.get("melayu") or "").strip()
        if not txt:
            return
        try:
            import win32com.client
            sp = win32com.client.Dispatch("SAPI.SpVoice")
            sp.Speak(txt, 1)          # 1 = async, UI tidak beku
            self.toast.show_msg("Membaca…")
        except Exception:
            self.toast.show_msg("TTS tidak tersedia pada sistem ini", 2500)

    def _random(self):
        self._random_toast_t0 = time.monotonic()
        self.toast.show_msg("\U0001F3B2  Membuka hadis rawak…", 0)
        self._run(RandomWorker(self.api), self._on_random)

    def _on_random(self, h):
        if not h:
            self.toast.show_msg("Tiada hadis rawak dijumpai", 2500)
            return
        self.open_detail(h, "home")
        # Sembunyi toast "Membuka…" selepas detail mula dipapar; jamin
        # paparan minimum supaya pengguna sempat baca maklum balas.
        baki = 1200 - int((time.monotonic() - self._random_toast_t0) * 1000)
        if baki > 0:
            QTimer.singleShot(baki, self.toast.hide)
        else:
            self.toast.hide()

    # ── Tersimpan ────────────────────────────────────────────────────
    def _is_saved(self, slug, hid):
        return any(b.get("slug") == slug and b.get("id") == hid
                   for b in self.bookmarks)

    def _toggle_save(self, h):
        slug, hid = h.get("collection"), h.get("id")
        if self._is_saved(slug, hid):
            self.bookmarks = [b for b in self.bookmarks
                              if not (b.get("slug") == slug and b.get("id") == hid)]
            self.toast.show_msg("Dibuang dari tersimpan")
        else:
            self.bookmarks.append({
                "slug": slug, "id": hid,
                "arab": h.get("arab", ""), "melayu": h.get("melayu", ""),
                "indonesia": h.get("indonesia", ""),
                "book": h.get("book"), "nama_bab": h.get("nama_bab", ""),
                "kitab_name": COLLECTION_META.get(slug, {}).get("name", slug),
                "saved_at": datetime.now().isoformat(timespec="seconds")})
            self.toast.show_msg("Disimpan")
        _write_json(BOOKMARKS, self.bookmarks)
        # _save_btn hanya wujud di halaman detail; abaikan di halaman
        # lain (cth. Tersimpan) yang memanggil _toggle_save.
        btn = getattr(self, "_save_btn", None)
        if btn is not None:
            btn.setText(_label_simpan(self._is_saved(slug, hid)))
        icon = getattr(self, "_save_btn_icon", None)
        if icon is not None:
            icon.set_active(self._is_saved(slug, hid))

    def _kemas_butang_atas_detail(self):
        """Tunjuk/sembunyi butang ↑ mengikut kedudukan skrol (Sesi 34).

        Corak sama halaman kitab/carian: butang hanya berguna bila
        kandungan hadis melebihi viewport dan pengguna sudah skrol ke
        bawah (melebihi 250px). Di kedudukan atas ia disembunyikan.
        """
        b = getattr(self, "_detail_top_btn", None)
        sa = getattr(self, "_detail_sa", None)
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

    def _kemas_butang_tindakan(self, lebar: float):
        """Bungkus butang tindakan ke dua baris bila ruang sempit.

        n = butang terbanyak yang muat pada baris 1 (minimum 1); baki
        ke baris 2, kedua-duanya dijajarkan kanan. Idempoten -- butang
        hanya dipindah antara layout, tiada pembinaan semula.
        """
        btns = self._tajuk_btns
        if not btns:
            return
        n = 0
        jumlah = 0
        for b in btns:
            w = b.sizeHint().width()
            if n:
                w += self._tajuk_btn_r1.spacing()
            if jumlah + w > lebar:
                break
            jumlah += w
            n += 1
        n = max(1, n)
        if n == self._tajuk_btn_n1:
            return
        self._tajuk_btn_n1 = n
        r1, r2 = self._tajuk_btn_r1, self._tajuk_btn_r2
        while r1.count():
            r1.takeAt(0)
        while r2.count():
            r2.takeAt(0)
        for b in btns[:n]:
            r1.addWidget(b)
        r1.addStretch(1)
        for b in btns[n:]:
            r2.addWidget(b)
        r2.addStretch(1)
        r1.invalidate()
        r2.invalidate()
        lo = self._tajuk_butang.layout()
        lo.invalidate()
        lo.activate()

    def _kemas_tajuk_detail(self):
        """Susun baris tajuk ikut lebar viewport (responsif 18 Ogos).

        Lebar luas -> satu baris (tajuk + butang tindakan). Lebar sempit
        -> tajuk pada baris pertama (membalut), butang pada baris kedua
        dijajarkan kanan. Butang dipindah antara dua baris (addWidget
        auto-reparent) — tiada widget dibina semula. Ambang dinamik:
        lebar satu baris = sizeHint tajuk + sizeHint butang, jadi ia
        ikut DPI/fon secara automatik (bukan pemalar). Di samping itu
        `_kemas_butang_tindakan` membungkus butang 2x2 bila baris kedua
        sendiri tidak muat (fon 1.5x + DPI 150% + tetingkap minimum).
        """
        sa = getattr(self, "_detail_sa", None)
        r1 = getattr(self, "_tajuk_r1", None)
        butang = getattr(self, "_tajuk_butang", None)
        if sa is None or r1 is None or butang is None:
            return
        label = getattr(self, "_tajuk_label", None)
        lebar_satu = 8  # spacing
        if label is not None:
            lebar_satu += label.sizeHint().width()
        # Lebar butang SATU baris (jumlah semua butang) -- bukan
        # sizeHint semasa (yang mungkin 2x2 dari keadaan sempit dulu).
        btns = getattr(self, "_tajuk_btns", [])
        if btns:
            lebar_satu += (sum(b.sizeHint().width() for b in btns)
                           + self._tajuk_btn_r1.spacing()
                           * (len(btns) - 1))
        # Tajuk_bar berada dalam `centered_column` (gutter 2xGUTTER,
        # had CONTENT_MAX_W) — bandingkan dengan lebar YANG TERSEDIA
        # untuknya, bukan viewport penuh.
        maks = min(sa.viewport().width() - 2 * GUTTER, CONTENT_MAX_W)
        sempit = maks < lebar_satu
        if sempit != self._tajuk_sempit:
            self._tajuk_sempit = sempit
            if sempit:
                self._tajuk_r1.removeWidget(butang)
                self._tajuk_r2.addWidget(butang)
            else:
                self._tajuk_r2.removeWidget(butang)
                self._tajuk_r1.addWidget(butang)
            butang.show()
        if sempit:
            self._kemas_butang_tindakan(maks)
        else:
            self._kemas_butang_tindakan(10 ** 9)
        wdg = sa.widget()
        lay = wdg.layout() if wdg is not None else None
        if lay is not None:
            lay.invalidate()
            lay.activate()

    def _kemas_tab_arab(self, lebar: float):
        """Bungkus tab ARAB/TRANSLITERASI ke dua baris bila lajur sempit.

        Sama corak `LangTabs.kemas_lebar`: n = tab terbanyak yang muat
        pada baris 1 (minimum 1); baki ke baris 2, kedua-duanya
        dijajarkan kanan (cermin RTL). Idempoten.
        """
        btns = [self._btn_arab, self._btn_translit]
        n = 0
        jumlah = 0
        for b in btns:
            w = b.sizeHint().width()
            if n:
                w += self._tab_ar_r1.spacing()
            if jumlah + w > lebar:
                break
            jumlah += w
            n += 1
        n = max(1, n)
        if n == self._tab_ar_n_baris1:
            return
        self._tab_ar_n_baris1 = n
        r1, r2 = self._tab_ar_r1, self._tab_ar_r2
        while r1.count():
            r1.takeAt(0)
        while r2.count():
            r2.takeAt(0)
        r1.addStretch()
        for b in btns[:n]:
            r1.addWidget(b)
        r2.addStretch()
        for b in btns[n:]:
            r2.addWidget(b)
        r1.invalidate()
        r2.invalidate()
        lo = self._tab_ar_lo
        lo.invalidate()
        lo.activate()

    def _kemas_panel_detail(self):
        """Susun panel dua lajur ikut lebar tersedia (responsif 18 Ogos).

        Kandungan minimum panel (tab bahasa + tab ARAB/TRANSLITERASI +
        kotak teks) boleh melebihi lebar tersedia pada kombinasi ekstrem
        (fon >1.15x + DPI tinggi + tetingkap minimum) -> skrol mengufuk
        tersembunyi, teks Arab (lajur kanan) terpotong. Tiga langkah:
        1) bungkus baris tab ikut lebar lajur SEMASA (idempoten);
        2) ketatkan margin panel (24/18+18 -> 16/12+10) bila masih
        sempit, longgarkan bila cukup;
        3) ulang susun tab dengan margin baharu. Corak sama
        `_kemas_tajuk_detail` (ukur vs lebar tersedia dalam
        centered_column).
        """
        sa = getattr(self, "_detail_sa", None)
        plo = getattr(self, "_panel_lo", None)
        if sa is None or plo is None:
            return
        maks = min(sa.viewport().width() - 2 * GUTTER, CONTENT_MAX_W)
        m = plo.contentsMargins()
        plaj = getattr(self, "_panel_lajur", plo)
        kol = max(1, (maks - m.left() - m.right() - plaj.spacing()) / 2)
        # 1. bungkus tab ikut lebar lajur semasa (tiada kesan bila muat)
        self._lang_tabs.kemas_lebar(kol)
        self._kemas_tab_arab(kol)
        # 2. ketatkan/longgarkan margin panel bila perlu
        sempit = maks < plo.minimumSize().width()
        if sempit != self._panel_sempit:
            self._panel_sempit = sempit
            if sempit:
                plo.setContentsMargins(16, 12, 16, 12)
                plo.setSpacing(8)
            else:
                plo.setContentsMargins(24, 18, 24, 18)
                plo.setSpacing(12)
            plo.invalidate()
            plo.activate()
            # 3. ulang susun tab dengan margin baharu
            m2 = plo.contentsMargins()
            kol2 = max(1, (maks - m2.left() - m2.right()
                           - plaj.spacing()) / 2)
            self._lang_tabs.kemas_lebar(kol2)
            self._kemas_tab_arab(kol2)
        wdg = sa.widget()
        lay = wdg.layout() if wdg is not None else None
        if lay is not None:
            lay.invalidate()
            lay.activate()

    def _kemas_semua_detail(self):
        """Laluan reflow kedua (tertangguh) — jalankan SELEPAS halaman
        dipaparkan pada saiz sebenar.

        `_render_detail` berjalan semasa halaman mungkin masih pada
        geometri basi (QStackedWidget tidak mengubah saiz halaman
        tersembunyi) -> pengiraan reflow guna viewport yang terlalu
        besar dan baris tab/butang tidak membungkus. QTimer.singleShot(0)
        menjalankan semula reflow selepas halaman dipaparkan; saiz
        sebenar -> bungkusan betul -> kandungan muat -> julat skrol
        dikemas.
        """
        self._kemas_tajuk_detail()
        self._kemas_panel_detail()

    def _skrol_atas_lancar_detail(self):
        """Skrol lancar ke atas teks hadis — animasi QTimer.

        Langkah mengecil (jarak dibahagi 15) supaya pergerakan kelihatan
        perlahan berhampiran sasaran. Timer disimpan pada `self` supaya
        panggilan kedua menghentikan animasi pertama.
        """
        bar = self._detail_sa.verticalScrollBar()
        mula = bar.value()
        if mula <= 0:
            return
        t = getattr(self, "_top_timer_detail", None)
        if t is not None:
            t.stop()
        t = QTimer(self)
        self._top_timer_detail = t
        langkah = max(1, mula // 15)

        def _langkah():
            if t is not self._top_timer_detail:
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
