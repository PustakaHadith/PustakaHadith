"""Skrin pemula (splash) — laporan fasa muat supaya apl tidak kelihatan beku.

Model carian makna dimuat dalam QThread latar belakang; pada mesin ini
import `sentence_transformers` ~19s + muat model ~5s (had persekitaran
Windows, diukur Sesi 26/27). Splash memaparkan fasa semasa daripada
`PreloadWorker.kemajuan` dengan bar kemajuan beranimasi, dan boleh
dilangkau dengan klik -- tetingkap utama tetap terbuka di belakang dan
pramuat berterusan dalam QThread.

Aliran (main.py):
    splash = SplashPermula(); splash.show()
    w = PustakaApp()
    w.kemajuan_pramuat.connect(splash.set_fasa)
    w.siap_pramuat.connect(splash.tutup_sedia)
    splash.diklik.connect(buka_tetingkap)
"""

from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtWidgets import (
    QHBoxLayout, QLabel, QProgressBar, QVBoxLayout, QWidget,
)

from VERSI import VERSI                                    # noqa: E402
from config import SETTINGS_PATH                          # noqa: E402
from ui.theme import apply_theme                           # noqa: E402


def _tema_tersimpan() -> str:
    """Baca tema pengguna (neutral/dark/light/lightneutral/sistem).

    Lalai 'neutral' (14 Ogos 2026) — pengguna awam biasa dengan mod
    gelap neutral Windows/telefon; kertas hangat menjadi pilihan.
    'sistem' (Ikut sistem) diselesaikan oleh apply_theme() mengikut
    mod gelap Windows semasa.
    """
    try:
        with open(SETTINGS_PATH, encoding="utf-8") as f:
            return (json.load(f) or {}).get("theme", "neutral") or "neutral"
    except Exception:
        return "neutral"


class SplashPermula(QWidget):
    """Tetingkap kecil tanpa bingkai dengan bar kemajuan beranimasi.

    Isyarat:
        diklik  -- pengguna klik di mana-mana (langkau, buka tetingkap)
    Kaedah:
        set_fasa(teks)   -- kemas kini label fasa
        tutup_sedia()    -- papar "Sedia!" lalu tutup selepas seketika
    """

    diklik = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        # Guna tema PENGUNA supaya splash sepadan dengan tetingkap utama
        # (PustakaApp akan panggil apply_theme sekali lagi -- idempoten).
        self._pal = apply_theme(_tema_tersimpan())
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setFixedSize(480, 300)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet(self._qss())
        self._bina()
        self._pindah_tengah()

    # ── binaan ─────────────────────────────────────────────────────────
    def _qss(self) -> str:
        p = self._pal
        return f"""
        #splash_kad {{
            background: {p["CARD_BG"]};
            border: 1px solid {p["BORDER"]};
            border-radius: 18px;
        }}
        #splash_judul {{
            color: {p["TEXT_PRIMARY"]};
            font-size: 22px;
            font-weight: 700;
        }}
        #splash_sub {{
            color: {p["TEXT_MUTED"]};
            font-size: 12px;
        }}
        #splash_fasa {{
            color: {p["TEAL_LIGHT"]};
            font-size: 13px;
        }}
        #splash_hint {{
            color: {p["TEXT_FAINT"]};
            font-size: 11px;
        }}
        QProgressBar {{
            background: {p["TEAL_DARK"] if "TEAL_DARK" in p else p["PAGE_BG"]};
            border: 1px solid {p["BORDER"]};
            border-radius: 7px;
            height: 14px;
            text-align: center;
            color: {p["TEXT_PRIMARY"]};
            font-size: 9px;
        }}
        QProgressBar::chunk {{
            background: {p["TEAL"]};
            border-radius: 6px;
        }}
        """

    def _bina(self):
        kad = QWidget(self)
        kad.setObjectName("splash_kad")
        kad.setGeometry(12, 12, 456, 276)

        v = QVBoxLayout(kad)
        v.setContentsMargins(28, 26, 28, 22)
        v.setSpacing(10)

        # Tajuk — gaya sama header apl: "Pustaka" bold + "Hadith" light + v1.0
        pal = self._pal
        teal = pal.get("TEAL", "#5CBF85")
        teal_l = pal.get("TEAL_LIGHT", "#7FD39A")
        muted = pal.get("TEXT_MUTED", "#9C9589")
        self._judul = QLabel(
            f'<span style="font-size:21px;font-weight:800;color:{teal};">Pustaka</span>'
            f'<span style="font-size:21px;font-weight:300;color:{teal_l};">Hadis</span>'
            f'<span style="font-size:12px;font-weight:400;color:{muted};"> v{VERSI}</span>')
        self._judul.setTextFormat(Qt.RichText)
        self._judul.setAlignment(Qt.AlignCenter)
        v.addWidget(self._judul)

        self._sub = QLabel(f"Versi {VERSI} — carian kata kunci + makna (AI)")
        self._sub.setObjectName("splash_sub")
        self._sub.setAlignment(Qt.AlignCenter)
        v.addWidget(self._sub)

        v.addStretch(1)

        self._fasa = QLabel("Menyediakan…")
        self._fasa.setObjectName("splash_fasa")
        self._fasa.setAlignment(Qt.AlignCenter)
        v.addWidget(self._fasa)

        # Bar 0..0 = mod sibuk (beranimasi berterusan). Fasa teks memberi
        # rasa kemajuan sebenar tanpa mengukur peratus yang tidak wujud.
        self._bar = QProgressBar()
        self._bar.setRange(0, 0)
        v.addWidget(self._bar)

        v.addStretch(1)

        self._hint = QLabel("Menyediakan model carian makna… klik untuk teruskan")
        self._hint.setObjectName("splash_hint")
        self._hint.setAlignment(Qt.AlignCenter)
        v.addWidget(self._hint)

    def _pindah_tengah(self):
        from PyQt5.QtWidgets import QApplication
        skr = QApplication.primaryScreen()
        if skr is None:
            return
        geo = skr.availableGeometry()
        self.move(geo.center().x() - self.width() // 2,
                  geo.center().y() - self.height() // 2)

    # ── antara muka awam ───────────────────────────────────────────────
    def set_fasa(self, teks: str):
        """Kemas kini label fasa semasa (dipanggil dari worker QThread)."""
        if teks:
            self._fasa.setText(teks)

    def tutup_sedia(self):
        """Papar \"Sedia!\" seketika lalu tutup (dipanggil bila pramuat siap)."""
        if not self.isVisible():
            return
        self._fasa.setText("Sedia! ✔")
        self._bar.setRange(0, 1)
        self._bar.setValue(1)
        QTimer.singleShot(500, self.close)

    # ── interaksi ──────────────────────────────────────────────────────
    def mousePressEvent(self, e):  # noqa: N802
        """Klik di mana-mana = langkau dan buka tetingkap utama."""
        self.diklik.emit()
        super().mousePressEvent(e)
