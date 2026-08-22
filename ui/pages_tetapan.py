"""Halaman Tetapan — mixin PustakaApp (Sesi 30).

Dipisahkan dari `ui/app_qt.py`. Kelas `PagesTetapan` menyediakan
halaman Tetapan: sambungan API (URL + kunci), saiz paparan (stepper),
fon Arab, bahasa dimuat, hadis per halaman, dan penyimpanan tetap ke
`user_settings.json`. Digabungkan ke `PustakaApp` melalui MRO:
`class PustakaApp(..., PagesTetapan, QMainWindow)`.

PENTING — tema: modul ini import WARNA dari `ui.theme`
(AMBER_*/RED_TEXT/GREEN_TEXT/TEXT_MUTED) untuk amaran fon dan status
API. Ia MESTI didaftar dalam `_THEMED_MODULES` (ui/theme.py) supaya
`apply_theme()` menyalin nilai terkini ke ruang namanya semasa tukar
tema.

GANDINGAN RENTAS MIXIN: modul ini TIDAK berdiri sendiri — kaedahnya
memanggil atribut teras `PustakaApp` (`self.settings`, `self.api`,
`self._run`, `self._refresh_current`, `self.per_page()`,
`self._on_collections`) dan `CollectionsWorker`. Mesti digabungkan
bersama PustakaApp penuh.
"""

from __future__ import annotations

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QComboBox, QFrame, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QWidget,
)

from ui.helpers import SETTINGS, _write_json
from ui.theme import (
    AMBER_BG, AMBER_BORDER, AMBER_TEXT, FONT_SCALES, FONT_SCALE_LABELS,
    GREEN_TEXT, RED_TEXT, TEXT_MUTED, build_qss,
)
from ui.widgets import centered_column, make_scroll
from ui.workers import CollectionsWorker


class PagesTetapan:
    # ── Tetapan ──────────────────────────────────────────────────────
    def _page_settings(self):
        sa = make_scroll()
        self.stack.addWidget(sa)
        body = QWidget()
        body.setObjectName("page")
        sa.setWidget(body)
        root = QVBoxLayout(body)
        root.setContentsMargins(0, 0, 0, 16)

        col, cl = centered_column()
        cl.setContentsMargins(0, 28, 0, 0)
        t = QLabel("Tetapan")
        t.setObjectName("h1")
        cl.addWidget(t)
        cl.addSpacing(10)

        # API
        api = QFrame()
        api.setObjectName("panel")
        al = QVBoxLayout(api)
        al.setContentsMargins(24, 20, 24, 20)
        al.setSpacing(10)
        h = QLabel("Sambungan API")
        h.setObjectName("h3")
        al.addWidget(h)

        self.in_url = QLineEdit(self.settings.get(
            "api_url", "https://service.hadis.my/api/v1"))
        self.in_key = QLineEdit(self.settings.get("api_key", ""))
        self.in_key.setEchoMode(QLineEdit.Password)
        for lab, w in [("URL", self.in_url), ("API Key", self.in_key)]:
            r = QWidget()
            rl = QHBoxLayout(r)
            rl.setContentsMargins(0, 0, 0, 0)
            l = QLabel(lab)
            l.setObjectName("body")
            l.setFixedWidth(90)
            rl.addWidget(l)
            rl.addWidget(w, 1)
            al.addWidget(r)

        self.api_status = QLabel("")
        self.api_status.setObjectName("faint")
        al.addWidget(self.api_status)

        sb = QPushButton("Simpan & Uji")
        sb.setObjectName("primary")
        sb.setCursor(Qt.PointingHandCursor)
        sb.clicked.connect(self._save_api)
        al.addWidget(sb, alignment=Qt.AlignLeft)
        cl.addWidget(api)

        # Paparan
        disp = QFrame()
        disp.setObjectName("panel")
        dl = QVBoxLayout(disp)
        dl.setContentsMargins(24, 20, 24, 20)
        dl.setSpacing(10)
        h2 = QLabel("Paparan")
        h2.setObjectName("h3")
        dl.addWidget(h2)

        self._steppers = {}
        for key, label in [("ui", "Saiz UI"), ("ar", "Saiz teks Arab"),
                           ("tr", "Saiz terjemahan")]:
            r = QWidget()
            rl = QHBoxLayout(r)
            rl.setContentsMargins(0, 0, 0, 0)
            l = QLabel(label)
            l.setObjectName("body")
            rl.addWidget(l)
            rl.addStretch()
            val = QLabel("")
            val.setObjectName("muted")
            val.setMinimumWidth(90)
            val.setAlignment(Qt.AlignRight)
            rl.addWidget(val)
            for txt, d in [("−", -1), ("+", 1)]:
                b = QPushButton(txt)
                b.setObjectName("stepper")
                b.setCursor(Qt.PointingHandCursor)
                b.clicked.connect(lambda _, k=key, dd=d: self._step(k, dd))
                rl.addWidget(b)
            dl.addWidget(r)
            self._steppers[key] = val

        # Fon Arab
        r = QWidget()
        rl = QHBoxLayout(r)
        rl.setContentsMargins(0, 0, 0, 0)
        l = QLabel("Fon Arab")
        l.setObjectName("body")
        rl.addWidget(l)
        rl.addStretch()
        self.cb_font = QComboBox()
        self.cb_font.addItems(self._fonts)
        i = self.cb_font.findText(self.ar_font)
        if i >= 0:
            self.cb_font.setCurrentIndex(i)
        self.cb_font.setMinimumWidth(240)
        self.cb_font.currentTextChanged.connect(self._set_font)
        rl.addWidget(self.cb_font)
        dl.addWidget(r)

        # Bahasa
        r2 = QWidget()
        rl2 = QHBoxLayout(r2)
        rl2.setContentsMargins(0, 0, 0, 0)
        l2 = QLabel("Bahasa dimuat")
        l2.setObjectName("body")
        rl2.addWidget(l2)
        rl2.addStretch()
        self.cb_lang = QComboBox()
        self.cb_lang.addItem("Semua bahasa", "both")
        self.cb_lang.addItem("Melayu sahaja (jimat data)", "bm_only")
        self.cb_lang.addItem("Indonesia sahaja", "ind_only")
        j = self.cb_lang.findData(self.settings.get("language_pref", "both"))
        if j >= 0:
            self.cb_lang.setCurrentIndex(j)
        self.cb_lang.setMinimumWidth(240)
        self.cb_lang.currentIndexChanged.connect(
            lambda: self._set("language_pref", self.cb_lang.currentData()))
        rl2.addWidget(self.cb_lang)
        dl.addWidget(r2)

        # Per halaman
        r3 = QWidget()
        rl3 = QHBoxLayout(r3)
        rl3.setContentsMargins(0, 0, 0, 0)
        l3 = QLabel("Hadis per halaman")
        l3.setObjectName("body")
        rl3.addWidget(l3)
        rl3.addStretch()
        self.cb_pp = QComboBox()
        for n in (10, 20, 30, 50, 100):
            self.cb_pp.addItem(str(n), n)
        k = self.cb_pp.findData(self.per_page())
        if k >= 0:
            self.cb_pp.setCurrentIndex(k)
        self.cb_pp.setMinimumWidth(240)
        self.cb_pp.currentIndexChanged.connect(
            lambda: self._set("per_page", self.cb_pp.currentData()))
        rl3.addWidget(self.cb_pp)
        dl.addWidget(r3)
        cl.addWidget(disp)

        real = [f for f in self._fonts
                if any(k in f for k in ("KFGQPC", "Scheherazade", "Amiri",
                                        "Naskh", "Arabic"))]
        if not real:
            warn = QLabel(
                "⚠ Tiada fon Arab khusus dikesan. Teks Arab akan dipapar "
                "dengan fon lalai sistem dan mungkin kurang cantik.\n"
                "Pasang Amiri atau Scheherazade New (percuma) untuk paparan "
                "terbaik, kemudian mulakan semula aplikasi.")
            warn.setWordWrap(True)
            warn.setStyleSheet(
                f"background-color: {AMBER_BG}; color: {AMBER_TEXT};"
                f"border: 1px solid {AMBER_BORDER}; border-radius: 8px;"
                f"padding: 12px; font-size: 11px;")
            dl.addWidget(warn)

        self._info = QLabel("")
        self._info.setObjectName("faint")
        cl.addWidget(self._info)
        root.addWidget(col)
        root.addStretch(1)        # elak kandungan meregang -- lihat 8c
        self._sync_settings()

    def _sync_settings(self):
        if not hasattr(self, "_steppers"):
            return
        for k, idx in [("ui", self.ui_idx), ("ar", self.ar_idx),
                       ("tr", self.tr_idx)]:
            self._steppers[k].setText(FONT_SCALE_LABELS[idx])
        mode = "Luar talian (SQLite)" if getattr(self.api, "offline", False) \
            else "Dalam talian (API)"
        quota = ""
        if self.api.daily_remaining is not None:
            quota = f" · kuota harian: {self.api.daily_remaining:,}"
        self._info.setText(f"Mod: {mode}{quota}")

    def _step(self, key, d):
        attr = {"ui": "ui_idx", "ar": "ar_idx", "tr": "tr_idx"}[key]
        n = getattr(self, attr) + d
        if not (0 <= n < len(FONT_SCALES)):
            return
        setattr(self, attr, n)
        self.settings[{"ui": "font_scale_idx", "ar": "arabic_font_idx",
                       "tr": "translation_font_idx"}[key]] = n
        _write_json(SETTINGS, self.settings)
        if key == "ui":
            self.setStyleSheet(build_qss(FONT_SCALES[n]))
        self._refresh_current()
        self._sync_settings()

    def _set(self, key, val):
        self.settings[key] = val
        _write_json(SETTINGS, self.settings)
        self.toast.show_msg("Tetapan disimpan")

    def _set_simbol_selawat(self, guna: bool):
        """Tukar antara bentuk penuh dan ligatur ﷺ, dan lukis semula."""
        self._set("simbol_selawat", bool(guna))
        self._refresh_current()

    def _set_font(self, name):
        self.ar_font = name
        self._set("arabic_font", name)
        self._refresh_current()

    def _save_api(self):
        url = self.in_url.text().strip()
        key = self.in_key.text().strip()
        try:
            from config import valid_key_format
            if key and not valid_key_format(key):
                self.api_status.setText(
                    "⚠ Format tidak sah — HADIS_XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX")
                self.api_status.setStyleSheet(f"color: {RED_TEXT};")
                return
        except ImportError:
            pass

        self.settings["api_url"] = url
        self.settings["api_key"] = key
        _write_json(SETTINGS, self.settings)
        self.api.base_url = url.rstrip("/")
        self.api.set_key(key)
        self.api_status.setText("Menguji…")
        self.api_status.setStyleSheet(f"color: {TEXT_MUTED};")

        def ok(cols):
            self.collections = cols or []
            self._on_collections(cols)
            self.api_status.setText(f"✓ Berjaya — {len(cols)} koleksi")
            self.api_status.setStyleSheet(f"color: {GREEN_TEXT};")
            self._sync_settings()

        def bad(msg):
            self.api_status.setText(f"✕ {msg}")
            self.api_status.setStyleSheet(f"color: {RED_TEXT};")

        self._run(CollectionsWorker(self.api), ok, bad)
