"""PustakaHadith — tetingkap utama (PyQt5), gaya hadis.my.

Semua I/O rangkaian berjalan dalam QThread; UI tidak pernah beku.
"""

from __future__ import annotations

import os
import sys

from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import (
    QApplication, QFrame, QHBoxLayout, QLabel, QMainWindow,
    QPushButton, QShortcut, QStackedWidget, QVBoxLayout, QWidget,
)

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ui.helpers import (                                             # noqa: E402
    BOOKMARKS, LANG_PARAM, PAGES, SETTINGS, READING_HISTORY,
    backfill_reading_at, backfill_saved_at, read_history,
    _parse_lompat, _read_json, _slug_dari_awalan, _write_json,
)
from ui.pages_kitab import PagesKitab                                    # noqa: E402
from ui.pages_rak import PagesRak                                        # noqa: E402
from ui.pages_carian import PagesCarian                                  # noqa: E402
from ui.pages_detail import PagesDetail                                  # noqa: E402
from ui.pages_tersimpan import PagesTersimpan                            # noqa: E402
from ui.pages_tetapan import PagesTetapan                                # noqa: E402
from ui.pages_home import PagesHome                                      # noqa: E402
from VERSI import VERSI                                              # noqa: E402
from api.hadis_api import HadisAPI                                    # noqa: E402
from ui.theme import (                                                # noqa: E402
    DEFAULT_TEMA, available_arabic_fonts, default_arabic_font,
    FONT_SCALES, HEADER_BG, HEADER_HEIGHT, TEAL, TEAL_LIGHT, TEXT_MUTED,
    apply_theme, build_qss, is_dark, tema_efektif,
)
from ui.widgets import (                                              # noqa: E402
    BackgroundCanvas, GearButton, Toast, divider,
)
from ui.settings_panel import Overlay, SettingsPanel                  # noqa: E402

from utils.bahasa import simbol_boleh_dipapar                        # noqa: E402
from ui.workers import (                                              # noqa: E402
    CollectionsWorker, PreloadWorker,
)

# Label butang "Rawak" pada bar navigasi atas. Pemalar (bukan literal
# dibenamkan) supaya label diuji unit (semak.py 8r) dan tidak berubah
# tanpa disedari.
# 25 Ogos 2026: butang Rawak DIPINDAHKAN dari header ke panel kanan
# halaman utama (mockup Split Command Center). Pemalar dikekalkan —
# kad Rawak panel kanan memaparnya dan ujian semak.py 8r kekal sah.
LABEL_RAWAK = "⚄  Rawak"


class PustakaApp(PagesKitab, PagesRak, PagesCarian, PagesDetail,
                 PagesTersimpan, PagesTetapan, PagesHome, QMainWindow):
    # Lazy Loading: model AI dimuat pada carian makna pertama.
    # Isyarat pramuat model lama (kemajuan_pramuat, siap_pramuat) DITANGGAL.
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PustakaHadith")
        # Minimum 1000x680 terlalu besar untuk laptop 1366x768 -- selepas
        # bar tugas dan bingkai, ruang berguna tinggal ~730px. Tetingkap
        # 860px tidak muat dan pengguna nampak paparan terpotong.
        self.setMinimumSize(900, 560)
        self._saiz_muat_skrin()

        self.settings = _read_json(SETTINGS, {})
        self.bookmarks = _read_json(BOOKMARKS, [])
        self.bookmarks, _bm_changed = backfill_saved_at(
            self.bookmarks, BOOKMARKS)
        if _bm_changed:
            _write_json(BOOKMARKS, self.bookmarks)
        _hist, _hch = backfill_reading_at(read_history(), READING_HISTORY)
        if _hch:
            _write_json(READING_HISTORY, _hist)

        self.ui_idx = int(self.settings.get("font_scale_idx", 1))
        # Keputusan Sesi 55 lanjutan: lalai saiz teks Arab = KECIL (0.85)
        # supaya teks terjemahan di lajur kanan sama paras (top-aligned)
        # dengan teks Arab -- mockup bukharin1/nasai2117/abudaud4177.
        self.ar_idx = int(self.settings.get("arabic_font_idx", 0))
        self.tr_idx = int(self.settings.get("translation_font_idx", 1))
        self._fonts = available_arabic_fonts()
        saved_font = self.settings.get("arabic_font", "")
        self.ar_font = saved_font if saved_font in self._fonts \
            else default_arabic_font()

        self.api = HadisAPI(self.settings.get("api_key", ""))
        self.collections = []
        self._workers = []
        self._tok = 0
        self._lang_key = "melayu"

        self._kitab_slug = "bukhari"
        self._kitab_page = 1
        self._kitab_go_to_hid = None
        self._search_q = ""
        self._search_slug = None
        self._search_page = 1
        self._detail_h = {}
        self._detail_from = "home"
        # Semakan fon dilakukan SEKALI -- QFontMetrics.inFont() mahal
        # jika dipanggil pada setiap render kad.
        self._ada_glif_selawat = simbol_boleh_dipapar(
            self.settings.get("arabic_font", ""))

        apply_theme(self.settings.get("theme", DEFAULT_TEMA))
        self.setStyleSheet(build_qss(FONT_SCALES[self.ui_idx]))
        self._build()
        # 'Ikut sistem' — pantau mod gelap Windows (registry) tiap 2 s;
        # hanya bina semula bila palet efektif bertukar (jarang), jadi
        # app bertukar hampir serta-merta selepas Windows tukar mod.
        self._tema_sistem_timer = QTimer(self)
        self._tema_sistem_timer.timeout.connect(self._semak_tema_sistem)
        self._tema_sistem_timer.start(2_000)
        # Pintasan global: Ctrl+G -> fokus kotak 'Lompat No. hadis' di
        # atas senarai pada halaman kitab. QShortcut (bukan keyPressEvent)
        # kerana ia
        # berfungsi walau widget mana yang memegang fokus, termasuk
        # QLineEdit (yang memakan kebanyakan kekunci lain).
        self._sc_lompat = QShortcut(QKeySequence("Ctrl+G"), self)
        self._sc_lompat.activated.connect(self._focus_lompat)
        self.toast = Toast(self)

        # Panel tetapan gelongsor (menggantikan halaman penuh)
        self.settings_overlay = Overlay(self)
        self.settings_panel = SettingsPanel(self, self)
        self.settings_panel.overlay = self.settings_overlay
        self.settings_overlay.clicked.connect(self.settings_panel.close_panel)
        # Lazy Loading: model AI DITANGGUHKAN hingga carian makna pertama.
        # Startup hanya muat koleksi (CollectionsWorker). PreloadWorker
        # tidak dijalankan automatik -- _model_lock + SemanticWorker
        # handle muat serentak selamat.
        self._fetch_collections()

    def _saiz_muat_skrin(self):
        """Saiz tetingkap ikut skrin sebenar, bukan nilai tetap.

        Diuji: pada 1366x768 ruang berguna hanya ~730px tinggi selepas
        bar tugas. Tetingkap 860px menyebabkan paparan terpotong.
        """
        lebar, tinggi = 1240, 860
        try:
            g = QApplication.primaryScreen().availableGeometry()
            lebar = max(900, min(lebar, g.width() - 80))
            tinggi = max(560, min(tinggi, g.height() - 80))
        except Exception:
            pass
        self.resize(lebar, tinggi)

    # ── infrastruktur ────────────────────────────────────────────────
    @property
    def ar_scale(self):
        return FONT_SCALES[self.ar_idx]

    @property
    def tr_scale(self):
        return FONT_SCALES[self.tr_idx]

    @property
    def lang_param(self):
        return LANG_PARAM.get(self.settings.get("language_pref", "both"))

    def per_page(self):
        try:
            return max(5, min(int(self.settings.get("per_page", 20)), 100))
        except (TypeError, ValueError):
            return 20

    def _run(self, worker, on_done, on_fail=None):
        """Mula pekerja, simpan rujukan, bersihkan bila tamat."""
        self._workers.append(worker)
        worker.done.connect(on_done)
        worker.failed.connect(on_fail or self._on_error)
        worker.finished.connect(lambda: self._workers.remove(worker)
                                if worker in self._workers else None)
        worker.start()
        return worker

    def _on_error(self, msg):
        self.toast.show_msg(f"⚠ {msg}", 3000)

    def closeEvent(self, e):
        for w in list(self._workers):
            # Semua worker kini mewarisi `_Base` dan ada `cancel()` --
            # termasuk `SemanticWorker` (dipindah ke ui/workers.py pada
            # 13 Ogos 2026; sebelum itu ia QThread dalaman tanpa
            # cancel(), dan AttributeError di sini semasa Qt meruntuhkan
            # tetingkap muncul sebagai fail-fast 0xC0000409, bukan
            # sebagai jejak Python).
            if hasattr(w, "cancel"):
                w.cancel()
            w.wait(300)
        super().closeEvent(e)
        # main.py menetapkan setQuitOnLastWindowClosed(False) (tinggalan
        # zaman splash; lihat PERUBAHAN_19OGOS.md komit 3), supaya tutup
        # tetingkap utama TIDAK auto-henti app.exec_(). Tanpa ini proses
        # kekal berjalan di latar selepas window ditutup. Keluar secara
        # eksplisit di sini supaya aplikasi berakhir bersih.
        QApplication.quit()

    def resizeEvent(self, e):
        super().resizeEvent(e)
        if getattr(self, "toast", None) and self.toast.isVisible():
            self.toast.move((self.width() - self.toast.width()) // 2,
                            self.height() - self.toast.height() - 40)
        if getattr(self, "settings_panel", None):
            self.settings_panel.relayout()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape and getattr(self, "settings_panel", None) \
                and self.settings_panel.is_open():
            self.settings_panel.close_panel()
            return
        super().keyPressEvent(e)

    # ── susun atur ───────────────────────────────────────────────────
    def _build(self):
        # Root kekal QWidget#page biasa (25 Ogos): latar glob AQUA
        # dilukis oleh BackgroundCanvas DALAM halaman utama sahaja —
        # viewport QScrollArea halaman lain ternyata telus (nampak
        # glob "bocor" pada halaman kitab bila root melukis imej).
        # Root QSS PAGE_BG menjamin halaman bukan-Utama kekal opaque
        # seperti sebelum ini.
        root = QWidget()
        root.setObjectName("page")
        self.setCentralWidget(root)
        rl = QVBoxLayout(root)
        rl.setContentsMargins(0, 0, 0, 0)
        rl.setSpacing(0)

        rl.addWidget(self._header())
        rl.addWidget(divider())

        self.stack = QStackedWidget()
        rl.addWidget(self.stack, 1)

        # BETULAN 17 Ogos: QStackedWidget tidak selalu mensaiz semula
        # halaman yang baru dipaparkan selepas setCurrentIndex ATAU
        # selepas tetingkap disaiz semula (diukur fizikal: viewport
        # kekal 640x480 dalam stack 1024px -> kandungan terpotong kanan,
        # hbar tersembunyi oleh ScrollBarAlwaysOff). Setiap kali stack
        # berubah saiz, paksa halaman semasa + viewportnya mengikut.
        _orig_stack_resize = self.stack.resizeEvent

        def _on_stack_resize(e):
            _orig_stack_resize(e)
            self._paksa_saiz_halaman()

        self.stack.resizeEvent = _on_stack_resize

        # PEMBETULAN (13 Ogos 2026): `self._page_settings` dibuang dari
        # senarai ini. Halaman "Tetapan" skrin-penuh lama (PagesTetapan)
        # sudah digantikan panel gelongsor `SettingsPanel` sejak Sesi 6,
        # tetapi masih dibina (widget URL/kunci/stepper/combobox) pada
        # SETIAP pelancaran walaupun tiada laluan `go("settings")` yang
        # sampai ke situ -- disahkan `grep` merentas seluruh kod sumber.
        # Kaedah backend (`_step`, `_set`, `_set_simbol_selawat`) KEKAL
        # dipakai oleh SettingsPanel; hanya pembinaan UI lama ini yang
        # dibuang. `PAGES["settings"]` (ui/helpers.py) selamat kekal --
        # ia index 5 (terakhir), buang dari sini tidak mengubah index
        # halaman lain (home=0, kitab=1, detail=2, search=3, saved=4).
        # 25 Ogos: halaman RAK DIGITAL ditambah di HUJUNG (index 5)
        # supaya indeks halaman lama (home=0, kitab=1, detail=2,
        # search=3, saved=4) KEKAL TIDAK BERUBAH -- PAGES (ui/helpers)
        # dan semua rujukan indeks kekal sah. "settings" (6) tiada
        # halaman dibina (panel gelongsor menggantikannya); go("settings")
        # menjadi no-op selamat.
        for fn in (self._page_home, self._page_kitab, self._page_detail,
                   self._page_search, self._page_saved, self._page_rak):
            fn()

        # QStackedWidget mengira saiz halaman semasa ia belum kelihatan.
        # Pada Windows ini kadang menghasilkan halaman kosong sehingga
        # sesuatu memaksa relayout (cth. klik nav "Utama").
        self.go("home")
        QTimer.singleShot(0, self._force_relayout)

    def _header(self):
        h = QFrame()
        h.setFixedHeight(HEADER_HEIGHT)
        h.setStyleSheet(f"background-color: {HEADER_BG}; border: none;")
        lo = QHBoxLayout(h)
        lo.setContentsMargins(28, 0, 28, 0)
        lo.setSpacing(2)

        logo = QLabel(
            f'<span style="font-size:21px;font-weight:800;color:{TEAL};">Pustaka</span>'
            f'<span style="font-size:21px;font-weight:300;color:{TEAL_LIGHT};">Hadith</span>'
            f'<span style="font-size:12px;font-weight:400;color:{TEXT_MUTED};"> v{VERSI}</span>')
        logo.setTextFormat(Qt.RichText)
        logo.setCursor(Qt.PointingHandCursor)
        lo.addWidget(logo)
        lo.addSpacing(24)

        self.nav = {}
        # Nav baharu (25 Ogos, mockup Split Command Center): "Jelajah
        # Kitab" → halaman RAK DIGITAL (bukan senarai terus); "Rawak"
        # dipindah ke panel kanan halaman utama.
        for label, key in [("Utama", "home"), ("Pencarian", "search"),
                            ("Jelajah Kitab", "rak"),
                            ("Simpan & Sejarah", "saved")]:
            b = QPushButton(label)
            b.setObjectName("nav")
            b.setCursor(Qt.PointingHandCursor)
            b.clicked.connect(lambda _, k=key: self.go(k))
            lo.addWidget(b)
            self.nav[key] = b
        lo.addStretch()

        sb = GearButton(size=22)
        sb.setObjectName("nav")
        sb.clicked.connect(self.toggle_settings)
        lo.addWidget(sb)
        self._set_nav("home")
        return h

    def set_theme(self, name: str, paksa: bool = False):
        """Tukar tema pengguna; bina semula seluruh UI.

        53 panggilan setStyleSheet() inline dalam UI membaca warna pada
        masa cipta widget. Menukar QSS global sahaja TIDAK cukup — widget
        sedia ada kekal warna lama. Jadi kita bina semula seluruh UI.
        `paksa=True` digunakan oleh pemantau tema 'sistem' (Ikut sistem):
        kunci tidak berubah tetapi palet efektif mungkin bertukar bila
        Windows bertukar gelap/terang.
        """
        if not paksa and name == self.settings.get("theme", DEFAULT_TEMA):
            return
        if name != self.settings.get("theme", DEFAULT_TEMA):
            self.settings["theme"] = name
            _write_json(SETTINGS, self.settings)

        # ingat kedudukan pengguna supaya tidak hilang konteks
        idx = self.stack.currentIndex()
        page = next((k for k, v in PAGES.items() if v == idx), "home")
        detail, slug, kpage = self._detail_h, self._kitab_slug, self._kitab_page
        q, qslug, qpage = self._search_q, self._search_slug, self._search_page

        apply_theme(name)
        self.setStyleSheet(build_qss(FONT_SCALES[self.ui_idx]))

        was_open = (getattr(self, "settings_panel", None)
                    and self.settings_panel.is_open())
        if getattr(self, "settings_panel", None):
            self.settings_panel.hide()
            self.settings_overlay.hide()
            self.settings_panel.deleteLater()
            self.settings_overlay.deleteLater()

        self._build()                       # bina semula semua widget
        self.toast = Toast(self)

        from ui.settings_panel import Overlay, SettingsPanel
        self.settings_overlay = Overlay(self)
        self.settings_panel = SettingsPanel(self, self)
        self.settings_panel.overlay = self.settings_overlay
        self.settings_overlay.clicked.connect(self.settings_panel.close_panel)

        # pulihkan keadaan
        self._detail_h, self._kitab_slug, self._kitab_page = detail, slug, kpage
        self._search_q, self._search_slug, self._search_page = q, qslug, qpage
        self._on_collections(self.collections)

        if page == "detail" and detail:
            self.go("detail"); self._render_detail(detail)
        elif page == "kitab":
            self.open_kitab(slug, kpage)
        elif page == "search" and q:
            self.go("search")
            self.search_bar.input.setText(q)
            self._do_search(qpage)
        else:
            self.go(page if page in PAGES else "home")

        if was_open:
            QTimer.singleShot(60, self.settings_panel.open_panel)
        self.toast.show_msg("Tema terang" if not is_dark() else "Tema gelap")

    def _semak_tema_sistem(self):
        """Pemantau 'Ikut sistem' — tukar palet bila Windows bertukar mod.

        QTimer 10 saat; baca registry sekali (murah) dan hanya bina
        semula UI bila palet efektif berbeza. Tiada kesan bila pengguna
        tidak memilih 'sistem'.
        """
        import ui.theme as _t
        if self.settings.get("theme", DEFAULT_TEMA) != "sistem":
            return
        if _t.tema_efektif("sistem") == _t.CURRENT_THEME:
            return
        self.set_theme("sistem", paksa=True)

    def _chrome_top(self) -> int:
        """Tinggi header + pembahagi — panel bermula di bawahnya."""
        return HEADER_HEIGHT + 1

    def toggle_settings(self):
        if self.settings_panel.is_open():
            self.settings_panel.close_panel()
        else:
            self.settings_panel.open_panel()

    def _refresh_current(self):
        """Lukis semula halaman aktif supaya perubahan fon/saiz kelihatan."""
        idx = self.stack.currentIndex()
        try:
            if idx == PAGES["detail"] and self._detail_h:
                self._render_detail(self._detail_h)
            elif idx == PAGES["kitab"]:
                self._render_kitab_shell()
                self._load_kitab_page(self._kitab_page)
            elif idx == PAGES["search"] and self._search_q:
                self._do_search(self._search_page)
            elif idx == PAGES["saved"]:
                self._render_saved()
        except Exception:
            pass

    def _force_relayout(self):
        """Paksa halaman aktif mengira semula susun aturnya.

        QStackedWidget mengira geometri halaman semasa ia belum kelihatan.
        Pada Windows ini kadang menghasilkan halaman kosong sehingga sesuatu
        mencetuskan relayout (cth. pengguna klik nav "Utama").
        """
        pg = self.stack.currentWidget()
        if pg is None:
            return
        inner = pg.widget() if hasattr(pg, "widget") else None
        for wdg in (inner, pg, self.stack):
            if wdg is None:
                continue
            try:
                wdg.updateGeometry()
                lay = wdg.layout()
                if lay:
                    lay.invalidate()
                    lay.activate()
                wdg.update()
            except Exception:
                pass
        self._paksa_saiz_halaman()

    def _paksa_saiz_halaman(self):
        """Paksa halaman semasa == saiz stack dan QScrollArea mengira
        viewportnya semula (nudge resize, bukan saizkan viewport terus).

        BETULAN 17 Ogos: selepas setCurrentIndex ATAU selepas stack
        disaiz semula, QStackedWidget tidak selalu mensaiz semula halaman
        yang baru dipaparkan (geometri basi 640x480) dan viewport
        QScrollArea boleh tertinggal pada saiz lalai -> kandungan
        terpotong di kanan (hbar tersembunyi oleh ScrollBarAlwaysOff).
        Diukur fizikal: viewport 640x480 dalam stack 1024px. Dipanggil
        dari `_force_relayout` (setiap go()) + resizeEvent stack. Hanya
        bertindak bila stack bersaiz sebenar (>= minimum tetingkap
        900x560) supaya tidak meruntuh susun atur sebelum tetingkap
        dipaparkan.
        """
        s = self.stack.size()
        if s.width() < 900 or s.height() < 400:
            return
        pg = self.stack.currentWidget()
        if pg is None:
            return
        try:
            if pg.size() != s:
                # Saiz halaman berubah -> resizeEvent QScrollArea mengira
                # viewport sendiri (tolak bar skrol). JANGAN saizkan
                # viewport secara langsung -- itu menceroboh ruang bar
                # skrol dan mengubah balutan teks (diukur fizikal 17 Ogos:
                # 17% piksel berbeza).
                pg.resize(s)
            vp = pg.viewport() if hasattr(pg, "viewport") else None
            if vp is not None and vp.width() < s.width() * 0.8:
                # Viewport masih basi (640x480) walaupun halaman sudah
                # betul -> nudge -1/+1 supaya resizeEvent DITERIMA (no-op
                # resize dioptimumkan oleh Qt). Hanya bila jelas basi supaya
                # susun atur normal tidak diganggu (nudge menukar lebar
                # viewport 1px -> teks boleh membalut semula, +11px pada
                # semak #5).
                pg.resize(s.width() - 1, s.height())
                pg.resize(s.width(), s.height())
        except Exception:
            pass

    def showEvent(self, e):
        super().showEvent(e)
        if not getattr(self, "_shown_once", False):
            self._shown_once = True
            QTimer.singleShot(0, self._force_relayout)
            QTimer.singleShot(150, self._force_relayout)

    def _set_nav(self, key):
        for k, b in self.nav.items():
            b.setObjectName("nav_active" if k == key else "nav")
            b.style().unpolish(b)
            b.style().polish(b)

    def go(self, key):
        # Efek bayang kad kitab (BungkusTimbul) MESTI dibuang SEBELUM
        # setCurrentIndex -- efek QGraphicsEffect aktif semasa halaman
        # ditukar mencetuskan ranap native (access violation, diukur
        # fizikal 16 Ogos: hover kad Muslim + klik -> open_kitab ->
        # go() ranap). `_buang_bayang_semua` selamat jika halaman rumah
        # belum dibina (getattr + tiada bungkus).
        self._buang_bayang_semua()
        self.stack.setCurrentIndex(PAGES[key])
        self._set_nav(key if key in self.nav else None)
        self._force_relayout()
        if key == "saved":
            self._render_saved()
        elif key == "settings":
            self._sync_settings()
        elif key == "home" and hasattr(self, "_render_sejarah"):
            # Kad "Terakhir dibaca" sentiasa segar bila kembali ke Utama.
            self._render_sejarah()

    # ── data ─────────────────────────────────────────────────────────
    def _fetch_collections(self):
        worker = self._run(CollectionsWorker(self.api), self._on_collections,
                           lambda m: None)
        # Pra-muat model DILANGKAU pada startup (Lazy Loading).
        # Model akan dimuat secara automatik pada carian makna pertama
        # melalui SemanticWorker -> _load_model() yang dilindungi _model_lock.
        # pramuat model dinyah (Lazy Loading) — lihat _fetch_collections

    def _on_collections(self, cols):
        self.collections = cols or []
        tot = {c["slug"]: c.get("total_hadis") for c in self.collections}
        for slug, card in getattr(self, "_kitab_cards", {}).items():
            n = tot.get(slug)
            if isinstance(n, int):
                card.set_total(n)
        total = sum(v for v in tot.values() if isinstance(v, int))
        if total and hasattr(self, "_home_count"):
            self._home_count.setText(
                f"{total:,} hadis daripada {len(self.collections)} kitab")
        # Pilihan Hari Ini (panel kanan, 25 Ogos): perlukan jumlah hadis
        # Bukhari sebagai modul indeks harian. Dipanggil sekali selepas
        # koleksi sampai; kaedah wujud hanya pada halaman utama baharu.
        if hasattr(self, "_fetch_pilihan_hari"):
            self._fetch_pilihan_hari()
        # Kiraan pada jilid Rak Digital 9 Kitab (25 Ogos).
        if hasattr(self, "_rak_update_kiraan"):
            self._rak_update_kiraan()

    def _total_of(self, slug):
        for c in self.collections:
            if c["slug"] == slug:
                return c.get("total_hadis")
        return None

    @staticmethod
    def _laras_tinggi(sa):
        """Saiz semula kandungan QScrollArea kepada tinggi SEBENARNYA.

        `setWidgetResizable(True)` memberi widget kandungan tinggi
        berdasarkan minimumSize layout, termasuk tuntutan daripada item
        stretch. Hasilnya julat skrol lebih besar daripada kandungan --
        pengguna skrol ke bawah dan jumpa ruang kosong (diukur
        550-920px bergantung halaman).

        `resize(sizeHint())` selepas kandungan diisi memaksa Qt mengira
        semula berdasarkan apa yang BENAR-BENAR ada.
        """
        if sa is None:
            return
        body = sa.widget()
        if body is None or body.layout() is None:
            return
        body.layout().invalidate()
        body.layout().activate()
        body.resize(body.sizeHint())

def main():
    app = QApplication(sys.argv)
    w = PustakaApp()
    w.show()
    return app.exec_()


if __name__ == "__main__":
    sys.exit(main())
