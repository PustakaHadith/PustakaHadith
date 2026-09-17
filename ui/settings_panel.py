"""Panel tetapan gelongsor â€” muncul dari tepi kanan.

Menggantikan halaman tetapan skrin penuh yang terlalu besar.
Corak sama seperti apl Quran moden: ikon gear â†’ panel gelongsor masuk,
tekan "Selesai" â†’ gelongsor keluar.

Panel ini hanya membina UI. Semua logik kekal dalam PustakaApp
(_step, _set, _set_font, _sync_settings).
"""

from __future__ import annotations

from PyQt5.QtCore import (
    QEasingCurve, QEvent, QPropertyAnimation, QRect, Qt, QTimer, pyqtSignal,
)
from PyQt5.QtGui import QColor, QPainter, QPixmap
from PyQt5.QtWidgets import (
    QComboBox, QFrame, QGraphicsDropShadowEffect, QGridLayout,
    QHBoxLayout, QLabel, QPushButton, QScrollArea,
    QSizePolicy, QVBoxLayout, QWidget,
)

from ui.widgets import BackgroundCanvas
from ui.deklarasi import DeklarasiDialog
from ui.theme import (
    AMBER_BG, AMBER_BORDER, AMBER_TEXT, BORDER, CARD_BG, CARD_BG_HOVER,
    DEFAULT_TEMA, FONT_SCALE_LABELS, HEADER_BG, PAGE_BG,
    RADIUS_SM, TEAL, TEAL_LIGHT, TEAL_PALE, TEXT_FAINT,
    TEXT_MUTED, TEXT_PRIMARY, TEXT_SECONDARY,
)

PANEL_W = 380
ANIM_MS = 220


class Overlay(QWidget):
    """Latar gelap separa lutsinar; klik untuk tutup."""

    clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)
        # Tema terang perlu overlay lebih lembut â€” rgba(0,0,0,110) di atas
        # latar putih kelihatan seperti kelabu kotor.
        from ui.theme import is_dark
        alpha = 110 if is_dark() else 60
        self.setStyleSheet(f"background-color: rgba(0, 0, 0, {alpha});")
        self.hide()

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.clicked.emit()
        super().mouseReleaseEvent(e)


class SettingsPanel(QFrame):
    """Panel gelongsor dari kanan.

    Isyarat:
        closed â€” dipancar selepas animasi tutup selesai
    """

    closed = pyqtSignal()

    def __init__(self, app, parent=None):
        super().__init__(parent)
        self.app = app                 # rujukan PustakaApp
        self._open = False
        self._anim = None

        self.setObjectName("settingsPanel")
        self.setStyleSheet(f"""
            QFrame#settingsPanel {{
                background-color: {HEADER_BG};
                border-left: 1px solid {BORDER};
            }}
        """)
        self.setFixedWidth(PANEL_W)
        # Cache latar glob (25 Ogos) â€” lukis semula HANYA pada resize.
        self._cache_latar: tuple[int, int, QPixmap] | None = None

        sh = QGraphicsDropShadowEffect(self)
        sh.setBlurRadius(28)
        sh.setXOffset(-6)
        sh.setYOffset(0)
        sh.setColor(QColor(0, 0, 0, 150))
        self.setGraphicsEffect(sh)

        self._build()
        self.hide()

    def paintEvent(self, e):
        """Latar glob (25 Ogos, permintaan pengguna) â€” sama dengan
        halaman Utama/rak: glob + scrim pada tema AQUA; tema lain kekal
        permukaan HEADER_BG biasa (super() melukis QSS dahulu, imej
        dilukis ATASNYA; anak-anak panel sentiasa dilukis selepas ini).

        QFrame#settingsPanel QSS border-left kekal dilukis oleh super()
        tetapi ditutup imej â€” jadi border dilukis semula di hujung kanan
        di sini supaya pemisah panel/utama kekal kelihatan.
        """
        super().paintEvent(e)
        import ui.theme as _t
        if not _t.ada_latar_imej():
            return
        w, h = max(1, self.width()), max(1, self.height())
        c = self._cache_latar
        if c is None or c[0] != w or c[1] != h:
            # Peta dunia rangkaian â€” 26 Ogos, permintaan pengguna:
            # imej ini untuk Tetapan (dan Makluman) SAHAJA.
            from ui.widgets import lukis_latar_dunia
            c = (w, h, lukis_latar_dunia(w, h))
            self._cache_latar = c
        p = QPainter(self)
        p.drawPixmap(0, 0, c[2])
        # Border kiri panel â€” imej menutup QSS border, lukis semula
        # garis kiri sahaja (bukan bingkai penuh).
        p.setPen(QColor(_t.BORDER))
        p.drawLine(0, 0, 0, h - 1)
        p.end()

    # â”€â”€ susun atur â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # tajuk
        head = QWidget()
        head.setFixedHeight(52)
        hl = QHBoxLayout(head)
        hl.setContentsMargins(20, 0, 12, 0)
        t = QLabel("Tetapan")
        t.setStyleSheet(f"font-size: 16px; font-weight: 700; "
                        f"color: {TEXT_PRIMARY};")
        hl.addWidget(t)
        hl.addStretch()
        x = QPushButton("âœ•")
        x.setFixedSize(30, 30)
        x.setCursor(Qt.PointingHandCursor)
        x.setStyleSheet(f"""
            QPushButton {{ background: transparent; border: none;
                           color: {TEXT_MUTED}; font-size: 15px; }}
            QPushButton:hover {{ color: {TEAL}; }}
        """)
        x.clicked.connect(self.close_panel)
        hl.addWidget(x)
        root.addWidget(head)
        root.addWidget(self._hline())

        # kandungan boleh skrol
        sa = QScrollArea()
        sa.setWidgetResizable(True)
        sa.setFrameShape(QFrame.NoFrame)
        sa.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        sa.setStyleSheet("background: transparent;")
        root.addWidget(sa, 1)
        self._sa = sa

        # Butang terapung "â†‘ ke atas" (Sesi 34) â€” corak sama halaman
        # kitab/carian: kelihatan bila kandungan panel panjang dan
        # pengguna skrol ke bawah; klik untuk kembali ke atas dengan
        # animasi lancar. Guna objectName "backTop" (QSS theme.py).
        if getattr(self, "_top_timer", None) is not None:
            self._top_timer.stop()
        self._top_btn = QPushButton("â†‘")
        self._top_btn.setObjectName("backTop")
        self._top_btn.setToolTip("Ke atas â€” tetapan")
        self._top_btn.setCursor(Qt.PointingHandCursor)
        self._top_btn.setFixedSize(44, 44)
        self._top_btn.setParent(sa)
        self._top_btn.clicked.connect(self._skrol_atas_lancar)
        self._top_btn.hide()
        sa.verticalScrollBar().valueChanged.connect(self._kemas_butang_atas)
        _orig_resize = sa.resizeEvent

        def _on_resize(e):
            _orig_resize(e)
            self._kemas_butang_atas()

        sa.resizeEvent = _on_resize

        inner = QWidget()
        inner.setStyleSheet("background: transparent;")
        sa.setWidget(inner)
        self.body = QVBoxLayout(inner)
        self.body.setContentsMargins(18, 16, 18, 16)
        self.body.setSpacing(18)

        self._sec_tema()
        self._sec_paparan()
        self._sec_bacaan()
        self._sec_tentang()
        self.body.addStretch(1)

        # kaki
        root.addWidget(self._hline())
        foot = QWidget()
        foot.setFixedHeight(60)
        fl = QHBoxLayout(foot)
        fl.setContentsMargins(18, 0, 18, 0)

        rst = QPushButton("Set Semula")
        rst.setCursor(Qt.PointingHandCursor)
        rst.setStyleSheet(f"""
            QPushButton {{ background: transparent; border: none;
                           color: {TEXT_MUTED}; font-size: 12px; }}
            QPushButton:hover {{ color: {TEAL}; }}
        """)
        rst.clicked.connect(self._reset)
        fl.addWidget(rst)
        fl.addStretch()

        done = QPushButton("Selesai")
        done.setCursor(Qt.PointingHandCursor)
        done.setFixedSize(96, 34)
        done.setStyleSheet(f"""
            QPushButton {{ background-color: {TEAL}; color: {PAGE_BG};
                           border: none; border-radius: 8px;
                           font-size: 13px; font-weight: 700; }}
            QPushButton:hover {{ background-color: {TEAL_LIGHT}; }}
        """)
        done.clicked.connect(self.close_panel)
        fl.addWidget(done)
        root.addWidget(foot)

    # â”€â”€ pembantu â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    def _hline(self):
        f = QFrame()
        f.setFixedHeight(1)
        f.setStyleSheet(f"background-color: {BORDER}; border: none;")
        return f

    def _group(self, title: str) -> QVBoxLayout:
        wrap = QVBoxLayout()
        wrap.setSpacing(8)
        lb = QLabel(title.upper())
        lb.setStyleSheet(f"font-size: 10px; font-weight: 700; "
                         f"color: {TEXT_FAINT}; letter-spacing: 0.6px;")
        wrap.addWidget(lb)
        self.body.addLayout(wrap)
        return wrap

    def _row(self, parent: QVBoxLayout, label: str) -> QHBoxLayout:
        r = QWidget()
        r.setStyleSheet("background: transparent;")
        rl = QHBoxLayout(r)
        rl.setContentsMargins(0, 0, 0, 0)
        rl.setSpacing(8)
        l = QLabel(label)
        l.setStyleSheet(f"font-size: 12px; color: {TEXT_SECONDARY};")
        rl.addWidget(l)
        rl.addStretch()
        parent.addWidget(r)
        return rl

    def _combo(self, parent, label, items, current=None, on_change=None,
               width=170):
        rl = self._row(parent, label)
        cb = QComboBox()
        cb.setFixedWidth(width)
        cb.setCursor(Qt.PointingHandCursor)
        cb.setStyleSheet(f"""
            QComboBox {{ background-color: {CARD_BG}; color: {TEXT_PRIMARY};
                         border: 1px solid {BORDER}; border-radius: 6px;
                         padding: 5px 9px; font-size: 11px; }}
            QComboBox:hover {{ border-color: {TEAL_PALE}; }}
            QComboBox::drop-down {{ border: none; width: 18px; }}
            QComboBox QAbstractItemView {{
                background-color: {CARD_BG}; color: {TEXT_PRIMARY};
                border: 1px solid {BORDER};
                selection-background-color: {TEAL_PALE};
                selection-color: {TEAL}; padding: 3px; }}
        """)
        for it in items:
            if isinstance(it, (tuple, list)):
                cb.addItem(it[0], it[1])
            else:
                cb.addItem(it)
        if current is not None:
            i = cb.findData(current)
            if i < 0:
                i = cb.findText(str(current))
            if i >= 0:
                cb.setCurrentIndex(i)
        if on_change:
            cb.currentIndexChanged.connect(lambda: on_change(cb))
        rl.addWidget(cb)
        return cb

    def _stepper(self, parent, label, key):
        """Baris âˆ’ nilai + (guna app._step yang sedia ada)."""
        rl = self._row(parent, label)
        val = QLabel("")
        val.setFixedWidth(74)
        val.setAlignment(Qt.AlignCenter)
        val.setStyleSheet(f"font-size: 11px; font-weight: 700; "
                          f"color: {TEXT_PRIMARY};")

        def mk(txt, d):
            b = QPushButton(txt)
            b.setFixedSize(26, 26)
            b.setCursor(Qt.PointingHandCursor)
            b.setStyleSheet(f"""
                QPushButton {{ background-color: {CARD_BG};
                               border: 1px solid {BORDER};
                               border-radius: 6px; color: {TEXT_SECONDARY};
                               font-size: 13px; font-weight: 700; }}
                QPushButton:hover {{ border-color: {TEAL};
                                     color: {TEAL}; }}
            """)
            b.clicked.connect(lambda: (self.app._step(key, d), self.sync()))
            return b

        rl.addWidget(mk("âˆ’", -1))
        rl.addWidget(val)
        rl.addWidget(mk("+", 1))
        self._stepper_labels[key] = val

    # â”€â”€ bahagian â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    def _sec_tema(self):
        """Pemilih tema â€” butang segmen, bukan dropdown.

        Dua pilihan sahaja; segmen lebih pantas dan menunjukkan
        keadaan semasa tanpa perlu dibuka.
        """
        g = self._group("Tema")

        grid = QWidget()
        grid.setStyleSheet("background: transparent;")
        gl = QGridLayout(grid)
        gl.setContentsMargins(0, 0, 0, 0)
        gl.setSpacing(8)

        cur = self.app.settings.get("theme", DEFAULT_TEMA)
        self._theme_btns = {}

        # 3 tema (25 Ogos): AQUA (lalai baharu) + Neutral gelap/terang.
        # Tema dark/light (kertas hangat) kekal boleh dipilih melalui
        # 'Ikut sistem'/fail tetapan â€” panel memaparkan yang kerap diguna.
        for key, label, pos in (("aqua", "â—ˆ  Aqua", (0, 0)),
                                ("neutral", "ðŸŒ™  Neutral", (0, 1)),
                                ("lightneutral", "â˜€  Neutral terang",
                                 (0, 2))):
            b = QPushButton(label)
            b.setCursor(Qt.PointingHandCursor)
            b.setFixedHeight(36)
            b.clicked.connect(lambda _, k=key: self._pick_theme(k))
            gl.addWidget(b, pos[0], pos[1], 1, 1)
            self._theme_btns[key] = b

        self._paint_theme_btns(cur)
        g.addWidget(grid)

    def _paint_theme_btns(self, active: str):
        for k, b in self._theme_btns.items():
            on = k == active
            b.setStyleSheet(f"""
                QPushButton {{
                    background-color: {TEAL if on else CARD_BG};
                    color: {PAGE_BG if on else TEXT_SECONDARY};
                    border: 1px solid {TEAL if on else BORDER};
                    border-radius: 8px; font-size: 12px;
                    font-weight: {700 if on else 600};
                }}
                QPushButton:hover {{
                    border-color: {TEAL};
                    color: {PAGE_BG if on else TEAL};
                }}
            """)

    def _pick_theme(self, name: str):
        if name == self.app.settings.get("theme", DEFAULT_TEMA):
            return
        self._paint_theme_btns(name)
        # Panel dibina semula oleh set_theme; tangguh supaya klik selesai
        QTimer.singleShot(0, lambda: self.app.set_theme(name))

    def _sec_paparan(self):
        self._stepper_labels = {}
        g = self._group("Paparan")
        self._stepper(g, "Saiz teks Arab", "ar")
        self._stepper(g, "Saiz terjemahan", "tr")

        self.cb_font = self._combo(
            g, "Fon Arab", self.app._fonts, self.app.ar_font,
            lambda cb: (setattr(self.app, "ar_font", cb.currentText()),
                        self.app._set("arabic_font", cb.currentText()),
                        self.app._refresh_current()),
            width=190)

        if not any(k in f for f in self.app._fonts
                   for k in ("KFGQPC", "Scheherazade", "Amiri",
                             "Naskh", "Arabic")):
            w = QLabel("âš  Tiada fon Arab khusus dikesan. Pasang Amiri "
                       "atau Scheherazade New untuk paparan terbaik.")
            w.setWordWrap(True)
            w.setStyleSheet(
                f"background-color: {AMBER_BG}; color: {AMBER_TEXT};"
                f"border: 1px solid {AMBER_BORDER}; border-radius: 6px;"
                f"padding: 9px; font-size: 10px;")
            g.addWidget(w)

    def _sec_bacaan(self):
        g = self._group("Bacaan")
        self._combo(
            g, "Bahasa dimuat",
            [("Semua bahasa", "both"),
             ("Melayu sahaja", "bm_only"),
             ("Indonesia sahaja", "ind_only")],
            self.app.settings.get("language_pref", "both"),
            lambda cb: self.app._set("language_pref", cb.currentData()))

        # Simbol selawat. Lalai SIMBOL ï·º (jika fon ada glif) -- ligatur
        # mengandungi lafaz penuh, bukan singkatan dua huruf seperti
        # "SAW", jadi ia tidak termasuk dalam tegahan Ibn Salah dan
        # al-Sakhawi terhadap penyingkatan. Bentuk penuh kekal tersedia.
        _pilihan = [("Penuh (rumi)", False)]
        if getattr(self.app, "_ada_glif_selawat", False):
            _pilihan.append(("Simbol â€” \ufdfa", True))
        self._combo(
            g, "Selawat",
            [(t, v) for t, v in _pilihan],
            bool(self.app.settings.get("simbol_selawat", True)),
            lambda cb: self.app._set_simbol_selawat(cb.currentData()))

        self._combo(
            g, "Hadis per halaman",
            [(str(n), n) for n in (10, 20, 30, 50, 100)],
            self.app.per_page(),
            lambda cb: self.app._set("per_page", cb.currentData()),
            width=100)

    def _sec_tentang(self):
        """Butang 'Tentang' -- buka deklarasi penuh (tujuan, sumber,
        batasan, sokongan). Corak butang sama seperti Tetapan API."""
        g = self._group("Tentang")

        row = QWidget()
        row.setStyleSheet("background: transparent;")
        rl = QHBoxLayout(row)
        rl.setContentsMargins(0, 0, 0, 0)
        rl.setSpacing(8)

        btn = QPushButton("  â„¹ï¸   Tentang PustakaHadith")
        btn.setCursor(Qt.PointingHandCursor)
        btn.setFixedHeight(38)
        btn.setStyleSheet(f"""
            QPushButton {{ background-color: {CARD_BG}; color: {TEXT_SECONDARY};
                           border: 1px solid {BORDER}; border-radius: 8px;
                           font-size: 12px; font-weight: 600;
                           text-align: left; padding-left: 10px; }}
            QPushButton:hover {{ background-color: {CARD_BG_HOVER};
                                 border-color: {TEAL_PALE};
                                 color: {TEXT_PRIMARY}; }}
        """)
        btn.clicked.connect(
            lambda: DeklarasiDialog(penuh=True, parent=self.app).exec_())
        rl.addWidget(btn, 1)

        arrow = QLabel("â€º")
        arrow.setStyleSheet(f"color: {TEXT_FAINT}; font-size: 16px;")
        rl.addWidget(arrow)
        g.addWidget(row)





    def _reset(self):
        a = self.app
        # Keputusan Sesi 55 lanjutan: lalai teks Arab = Kecil (0).
        a.ui_idx, a.ar_idx, a.tr_idx = 1, 0, 1
        a.settings.update({"font_scale_idx": 1, "arabic_font_idx": 0,
                           "translation_font_idx": 1,
                           "language_pref": "both", "per_page": 20})
        from ui.app_qt import _write_json, SETTINGS
        _write_json(SETTINGS, a.settings)
        from ui.theme import build_qss, FONT_SCALES
        a.setStyleSheet(build_qss(FONT_SCALES[a.ui_idx]))
        a._refresh_current()
        self.sync()
        a.toast.show_msg("Tetapan diset semula")

    def sync(self):
        """Segarkan nilai yang dipapar."""
        for k, idx in (("ui", self.app.ui_idx), ("ar", self.app.ar_idx),
                       ("tr", self.app.tr_idx)):
            if k in self._stepper_labels:
                self._stepper_labels[k].setText(FONT_SCALE_LABELS[idx])

    # â”€â”€ animasi â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    def open_panel(self):
        if self._open:
            return
        self._open = True
        self.sync()
        p = self.parentWidget()
        top = self.app._chrome_top()
        h = p.height() - top

        self.overlay.setGeometry(0, top, p.width(), h)
        self.overlay.show()
        self.overlay.raise_()

        self.setGeometry(p.width(), top, PANEL_W, h)
        self.show()
        self.raise_()
        self._animate(p.width() - PANEL_W)

    def close_panel(self):
        if not self._open:
            return
        self._open = False
        p = self.parentWidget()
        self._animate(p.width(), on_done=self._after_close)

    def _after_close(self):
        self.hide()
        self.overlay.hide()
        self.closed.emit()

    def _animate(self, x_end, on_done=None):
        g = self.geometry()
        self._anim = QPropertyAnimation(self, b"geometry", self)
        self._anim.setDuration(ANIM_MS)
        self._anim.setEasingCurve(QEasingCurve.OutCubic)
        self._anim.setStartValue(g)
        self._anim.setEndValue(QRect(x_end, g.y(), PANEL_W, g.height()))
        if on_done:
            self._anim.finished.connect(on_done)
        self._anim.start()

    def relayout(self):
        """Panggil dari resizeEvent tetingkap."""
        if not self._open:
            return
        p = self.parentWidget()
        top = self.app._chrome_top()
        h = p.height() - top
        self.overlay.setGeometry(0, top, p.width(), h)
        self.setGeometry(p.width() - PANEL_W, top, PANEL_W, h)

    def is_open(self) -> bool:
        return self._open

    def _kemas_butang_atas(self):
        """Tunjuk/sembunyi butang â†‘ mengikut kedudukan skrol (Sesi 34).

        Corak sama halaman kitab/carian: butang hanya berguna bila
        kandungan panel melebihi viewport dan pengguna sudah skrol ke
        bawah (melebihi 250px). Di kedudukan atas ia disembunyikan.
        """
        b = getattr(self, "_top_btn", None)
        sa = getattr(self, "_sa", None)
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
        """Skrol lancar ke atas panel tetapan â€” animasi QTimer.

        Langkah mengecil (jarak dibahagi 15) supaya pergerakan kelihatan
        perlahan berhampiran sasaran. Timer disimpan pada `self` supaya
        panggilan kedua menghentikan animasi pertama.
        """
        bar = self._sa.verticalScrollBar()
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
