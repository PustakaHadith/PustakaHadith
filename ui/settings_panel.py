"""Panel tetapan gelongsor — muncul dari tepi kanan.

Menggantikan halaman tetapan skrin penuh yang terlalu besar.
Corak sama seperti apl Quran moden: ikon gear → panel gelongsor masuk,
tekan "Selesai" → gelongsor keluar.

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

PANEL_W = 340
PANEL_W_MIN = 340
PANEL_W_MAX = 520
ANIM_MS = 220


class Overlay(QWidget):
    """Latar gelap separa lutsinar; klik untuk tutup."""

    clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)
        # Tema terang perlu overlay lebih lembut — rgba(0,0,0,110) di atas
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
        closed — dipancar selepas animasi tutup selesai
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
        self.setFixedWidth(PANEL_W_MIN)
        # Cache latar glob (25 Ogos) — lukis semula HANYA pada resize.
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
        """Latar glob (25 Ogos, permintaan pengguna) — sama dengan
        halaman Utama/rak: glob + scrim pada tema AQUA; tema lain kekal
        permukaan HEADER_BG biasa (super() melukis QSS dahulu, imej
        dilukis ATASNYA; anak-anak panel sentiasa dilukis selepas ini).

        QFrame#settingsPanel QSS border-left kekal dilukis oleh super()
        tetapi ditutup imej — jadi border dilukis semula di hujung kanan
        di sini supaya pemisah panel/utama kekal kelihatan.
        """
        super().paintEvent(e)
        import ui.theme as _t
        if not _t.ada_latar_imej():
            return
        w, h = max(1, self.width()), max(1, self.height())
        c = self._cache_latar
        if c is None or c[0] != w or c[1] != h:
            # Peta dunia rangkaian — 26 Ogos, permintaan pengguna:
            # imej ini untuk Tetapan (dan Makluman) SAHAJA.
            from ui.widgets import lukis_latar_dunia
            c = (w, h, lukis_latar_dunia(w, h))
            self._cache_latar = c
        p = QPainter(self)
        p.drawPixmap(0, 0, c[2])
        # Border kiri panel — imej menutup QSS border, lukis semula
        # garis kiri sahaja (bukan bingkai penuh).
        p.setPen(QColor(_t.BORDER))
        p.drawLine(0, 0, 0, h - 1)
        p.end()

    # ── susun atur ────────────────────────────────────────────────────
    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # tajuk
        head = QWidget()
        head.setFixedHeight(52)
        hl = QHBoxLayout(head)
        hl.setContentsMargins(14, 0, 10, 0)
        t = QLabel("Tetapan")
        t.setStyleSheet(f"font-size: 16px; font-weight: 700; "
                        f"color: {TEXT_PRIMARY};")
        hl.addWidget(t)
        hl.addStretch()
        x = QPushButton("✕")
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

        # Butang terapung "↑ ke atas" (Sesi 34) — corak sama halaman
        # kitab/carian: kelihatan bila kandungan panel panjang dan
        # pengguna skrol ke bawah; klik untuk kembali ke atas dengan
        # animasi lancar. Guna objectName "backTop" (QSS theme.py).
        if getattr(self, "_top_timer", None) is not None:
            self._top_timer.stop()
        self._top_btn = QPushButton("↑")
        self._top_btn.setObjectName("backTop")
        self._top_btn.setToolTip("Ke atas — tetapan")
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
        self.body.setContentsMargins(14, 12, 14, 12)
        self.body.setSpacing(12)

        self._sec_tema()
        self._build_settings_grid()
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

    # ── pembantu ──────────────────────────────────────────────────────
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

    def _sec_tema(self):
        """Pemilih tema — butang segmen, bukan dropdown."""
        g = self._group("Tema")

        row = QWidget()
        row.setStyleSheet("background: transparent;")
        hl = QHBoxLayout(row)
        hl.setContentsMargins(0, 0, 0, 0)
        hl.setSpacing(6)

        cur = self.app.settings.get("theme", DEFAULT_TEMA)
        self._theme_btns = {}

        for key, label in (("aqua", "◎ Aqua"),
                           ("neutral", "🌙 Neutral"),
                           ("lightneutral", "☀ Neutral terang")):
            b = QPushButton(label)
            b.setCursor(Qt.PointingHandCursor)
            b.setFixedHeight(32)
            b.clicked.connect(lambda _, k=key: self._pick_theme(k))
            hl.addWidget(b)
            self._theme_btns[key] = b

        self._paint_theme_btns(cur)
        g.addWidget(row)

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
                    padding: 4px 10px;
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
        QTimer.singleShot(0, lambda: self.app.set_theme(name))

    @staticmethod
    def _combo_ss():
        return f"""
            QComboBox {{ background-color: {CARD_BG}; color: {TEXT_PRIMARY};
                         border: 1px solid {BORDER}; border-radius: 6px;
                         padding: 4px 8px; font-size: 11px; }}
            QComboBox:hover {{ border-color: {TEAL_PALE}; }}
            QComboBox::drop-down {{ border: none; width: 18px; }}
            QComboBox QAbstractItemView {{
                background-color: {CARD_BG}; color: {TEXT_PRIMARY};
                border: 1px solid {BORDER};
                selection-background-color: {TEAL_PALE};
                selection-color: {TEAL}; padding: 3px; }}"""

    @staticmethod
    def _stepper_btn_ss():
        return f"""
            QPushButton {{ background-color: {CARD_BG};
                           border: 1px solid {BORDER};
                           border-radius: 5px; color: {TEXT_SECONDARY};
                           font-size: 12px; font-weight: 700; }}
            QPushButton:hover {{ border-color: {TEAL}; color: {TEAL}; }}"""

    def _build_settings_grid(self):
        """Satu grid tunggal untuk Paparan + Bacaan."""
        self._stepper_labels = {}

        wrap = QWidget()
        wrap.setStyleSheet("background: transparent;")
        gl = QGridLayout(wrap)
        gl.setContentsMargins(0, 0, 0, 0)
        gl.setSpacing(6)
        gl.setColumnStretch(1, 1)

        r = 0
        ss = self._combo_ss()

        def _label(row, text):
            l = QLabel(text)
            l.setStyleSheet(f"font-size: 11px; color: {TEXT_SECONDARY};")
            gl.addWidget(l, row, 0)

        def _combo(row, items, current_data=None, on_change=None):
            cb = QComboBox()
            cb.setStyleSheet(ss)
            cb.setCursor(Qt.PointingHandCursor)
            for it in items:
                if isinstance(it, (tuple, list)):
                    cb.addItem(it[0], it[1])
                else:
                    cb.addItem(it)
            if current_data is not None:
                i = cb.findData(current_data)
                if i < 0:
                    i = cb.findText(str(current_data))
                if i >= 0:
                    cb.setCurrentIndex(i)
            if on_change:
                cb.currentIndexChanged.connect(lambda: on_change(cb))
            gl.addWidget(cb, row, 1)
            return cb

        def _stepper(row, key):
            w = QWidget()
            w.setStyleSheet("background: transparent;")
            hl = QHBoxLayout(w)
            hl.setContentsMargins(0, 0, 0, 0)
            hl.setSpacing(4)
            val = QLabel("")
            val.setFixedWidth(65)
            val.setAlignment(Qt.AlignCenter)
            val.setStyleSheet(f"font-size: 11px; font-weight: 700; "
                              f"color: {TEXT_PRIMARY};")
            for txt, d in (("−", -1), ("+", 1)):
                b = QPushButton(txt)
                b.setFixedSize(24, 24)
                b.setCursor(Qt.PointingHandCursor)
                b.setStyleSheet(self._stepper_btn_ss())
                b.clicked.connect(lambda checked=False, dd=d:
                                 (self.app._step(key, dd), self.sync()))
                hl.addWidget(b)
            hl.addWidget(val)
            hl.addStretch()
            gl.addWidget(w, row, 1)
            self._stepper_labels[key] = val

        # ── Paparan ──
        sec = QLabel("PAPARAN")
        sec.setStyleSheet(f"font-size: 10px; font-weight: 700; "
                          f"color: {TEXT_FAINT}; letter-spacing: 0.6px;")
        gl.addWidget(sec, r, 0, 1, 2)
        r += 1

        _label(r, "Saiz teks Arab")
        _stepper(r, "ar")
        r += 1

        _label(r, "Saiz terjemahan")
        _stepper(r, "tr")
        r += 1

        _label(r, "Fon Arab")
        cb_f = _combo(r, [(f, f) for f in self.app._fonts],
                      current_data=self.app.ar_font,
                      on_change=lambda cb: (
                          setattr(self.app, "ar_font", cb.currentText()),
                          self.app._set("arabic_font", cb.currentText()),
                          self.app._refresh_current()))
        self.cb_font = cb_f
        r += 1

        if not any(k in f for f in self.app._fonts
                   for k in ("KFGQPC", "Scheherazade", "Amiri",
                             "Naskh", "Arabic")):
            w = QLabel("⚠ Tiada fon Arab khusus dikesan.")
            w.setWordWrap(True)
            w.setStyleSheet(
                f"background-color: {AMBER_BG}; color: {AMBER_TEXT};"
                f"border: 1px solid {AMBER_BORDER}; border-radius: 6px;"
                f"padding: 9px; font-size: 10px;")
            gl.addWidget(w, r, 0, 1, 2)
            r += 1

        # ── Bacaan ──
        sec2 = QLabel("BACAAN")
        sec2.setStyleSheet(f"font-size: 10px; font-weight: 700; "
                           f"color: {TEXT_FAINT}; letter-spacing: 0.6px;")
        gl.addWidget(sec2, r, 0, 1, 2)
        r += 1

        _label(r, "Bahasa dimuat")
        _combo(r, [("Semua bahasa", "both"),
                   ("Melayu sahaja", "bm_only"),
                   ("Indonesia sahaja", "ind_only")],
               current_data=self.app.settings.get("language_pref", "both"),
               on_change=lambda cb: self.app._set(
                   "language_pref", cb.currentData()))
        r += 1

        _label(r, "Selawat")
        _pilihan = [("Penuh (rumi)", False)]
        if getattr(self.app, "_ada_glif_selawat", False):
            _pilihan.append(("Simbol — \ufdfa", True))
        _combo(r, [(t, v) for t, v in _pilihan],
               current_data=bool(self.app.settings.get(
                   "simbol_selawat", True)),
               on_change=lambda cb: self.app._set_simbol_selawat(
                   cb.currentData()))
        r += 1

        _label(r, "Hadis per halaman")
        _combo(r, [(str(n), n) for n in (10, 20, 30, 50, 100)],
               current_data=self.app.per_page(),
               on_change=lambda cb: self.app._set(
                   "per_page", cb.currentData()))
        r += 1

        self.body.addWidget(wrap)

    def _sec_tentang(self):
        """Butang 'Tentang' -- buka deklarasi penuh."""
        g = self._group("Tentang")

        row = QWidget()
        row.setStyleSheet("background: transparent;")
        rl = QHBoxLayout(row)
        rl.setContentsMargins(0, 0, 0, 0)
        rl.setSpacing(8)

        btn = QPushButton("ℹ Tentang PustakaHadith")
        btn.setCursor(Qt.PointingHandCursor)
        btn.setFixedHeight(34)
        btn.setStyleSheet(f"""
            QPushButton {{ background-color: {CARD_BG}; color: {TEXT_SECONDARY};
                           border: 1px solid {BORDER}; border-radius: 8px;
                           font-size: 12px; font-weight: 600;
                           padding: 4px 14px; }}
            QPushButton:hover {{ background-color: {CARD_BG_HOVER};
                                 border-color: {TEAL_PALE};
                                 color: {TEXT_PRIMARY}; }}
        """)
        btn.clicked.connect(
            lambda: DeklarasiDialog(penuh=True, parent=self.app).exec_())
        rl.addWidget(btn)
        rl.addStretch()

        arrow = QLabel("›")
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

    # ── animasi ───────────────────────────────────────────────────────
    def _lebar_panel(self) -> int:
        """Lebar panel adaptif — ikut lebar tetingkap (Sesi 24, fix
        'kandungan terkeluar ke kiri' dalam fullscreen).

        Panel 380px kaku TIDAK muat baris 'label + combo(240) + stepper'
        bila tetingkap lebar. Kira 38% lebar induk, had minima PANEL_W_MIN
        dan maksima PANEL_W_MAX supaya baris sentiasa muat penuh.
        """
        p = self.parentWidget()
        w = p.width() if p is not None else PANEL_W_MIN
        return max(PANEL_W_MIN, min(PANEL_W_MAX, int(w * 0.28)))

    # ── animasi ──────────────────────────────────────────────────
    def open_panel(self):
        if self._open:
            return
        self._open = True
        self.sync()
        p = self.parentWidget()
        top = self.app._chrome_top()
        h = p.height() - top
        w = self._lebar_panel()

        self.setFixedWidth(w)
        self.overlay.setGeometry(0, top, p.width(), h)
        self.overlay.show()
        self.overlay.raise_()

        self.setGeometry(p.width(), top, w, h)
        self.show()
        self.raise_()
        self._animate(p.width() - w)

    def close_panel(self):
        if not self._open:
            return
        self._open = False
        p = self.parentWidget()
        p_w = self._lebar_panel()
        self._animate(p.width(), p_w=p_w, on_done=self._after_close)

    def _after_close(self):
        self.hide()
        self.overlay.hide()
        self.closed.emit()

    def _animate(self, x_end, p_w=None, on_done=None):
        g = self.geometry()
        p_w = p_w if p_w is not None else g.width()
        self._anim = QPropertyAnimation(self, b"geometry", self)
        self._anim.setDuration(ANIM_MS)
        self._anim.setEasingCurve(QEasingCurve.OutCubic)
        self._anim.setStartValue(g)
        self._anim.setEndValue(QRect(x_end, g.y(), p_w, g.height()))
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
        w = self._lebar_panel()
        self.setFixedWidth(w)
        for o in (self, self.overlay):
            if o.width() < PANEL_W_MIN and o is self:
                pass
        self.overlay.setGeometry(0, top, p.width(), h)
        self.setGeometry(p.width() - w, top, w, h)

    def is_open(self) -> bool:
        return self._open

    def _kemas_butang_atas(self):
        """Tunjuk/sembunyi butang ↑ mengikut kedudukan skrol (Sesi 34).

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
        """Skrol lancar ke atas panel tetapan — animasi QTimer.

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
