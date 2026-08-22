"""Dialog disclaimer PustakaHadith — papar sekali pada larian pertama.

Teks daripada dokumen/rujukan/DEKLARASI.md (skrin permulaan).
Selepas pengguna klik 'Faham', dialog tidak muncul lagi.
"""

from __future__ import annotations

import json
import os

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QDialog, QLabel, QPushButton, QTextEdit, QVBoxLayout,
)

from ui.theme import apply_theme
from ui.splash import _tema_tersimpan
from VERSI import VERSI
from config import SETTINGS_PATH  # laluan pusat (INSTALLER.md §3)

_SETTINGS = SETTINGS_PATH


def _sudah_baca() -> bool:
    """True jika pengguna sudah klik 'Faham'."""
    try:
        with open(_SETTINGS, encoding="utf-8") as f:
            return (json.load(f) or {}).get("disclaimer_dibaca", False)
    except Exception:
        return False


def _simpan_dibaca():
    """Tandakan disclaimer sudah dibaca dalam user_settings.json."""
    data = {}
    try:
        with open(_SETTINGS, encoding="utf-8") as f:
            data = json.load(f) or {}
    except Exception:
        pass
    data["disclaimer_dibaca"] = True
    try:
        with open(_SETTINGS, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception:
        pass


TEKS = (
    "PustakaHadith\n\n"
    "Rujukan digital 9 kitab hadis dalam Bahasa Melayu\n\n"
    "Aplikasi ini menghimpunkan 62,169 hadis daripada sembilan kitab "
    "utama — Bukhari, Muslim, Abu Daud, Tirmidzi, An-Nasa'i, Ibnu Majah, "
    "Ahmad, Ad-Darimi, dan Muwatta Malik — lengkap dengan teks Arab, "
    "terjemahan, transliterasi, dan carian.\n\n"
    "Ia dibina untuk pelajar, pengkaji, peminat hadis, dan pengguna awam "
    "yang mahu merujuk hadis dengan cepat.\n\n"
    "Aplikasi ini BUKAN:\n\n"
    "• Bukan sumber fatwa. Ia tidak memberi hukum. Untuk keputusan "
    "agama, rujuk ulama bertauliah.\n\n"
    "• Bukan alat semakan hadis palsu. Ia memaparkan hadis daripada "
    "sembilan kitab tersebut sahaja. Untuk menyemak hadis yang beredar di "
    "media sosial, gunakan SemakHadis.com.\n\n"
    "• Bukan pengganti guru. Memahami hadis memerlukan ilmu alat — "
    "konteks, sanad, dan kaedah usul. Aplikasi hanya menyediakan teks.\n\n"
    "Tentang darjat hadis: penilaian yang dipaparkan datang daripada "
    "ulama hadis moden. Ulama boleh berbeza pendapat tentang hadis yang "
    "sama. Aplikasi memaparkan setiap penilaian sebagaimana adanya, tanpa "
    "memilih antara mereka."
)


class DisclaimerDialog(QDialog):
    """Dialog disclaimer — papar sekali pada larian pertama."""

    def __init__(self):
        super().__init__(None)
        self.setWindowTitle("PustakaHadith — Makluman")
        self.setMinimumSize(520, 580)
        self.resize(540, 600)
        self.setWindowFlags(
            Qt.Dialog | Qt.WindowStaysOnTopHint
        )
        self._bina()
        self._pusatkan()

    def _pusatkan(self):
        screen = QApplication.primaryScreen()
        if screen:
            geo = screen.availableGeometry()
            x = (geo.width() - self.width()) // 2 + geo.x()
            y = (geo.height() - self.height()) // 2 + geo.y()
            self.move(x, y)

    def _bina(self):
        lo = QVBoxLayout(self)
        lo.setContentsMargins(28, 24, 28, 20)
        lo.setSpacing(12)

        p = apply_theme(_tema_tersimpan())
        BG = p.get("CARD_BG", "#1E1D1A")
        FG = p.get("TEXT_PRIMARY", "#E8E4DA")
        self.setStyleSheet(f"QDialog {{ background-color: {BG}; color: {FG}; }}")

        teal = p.get("TEAL", "#5CBF85")
        teal_l = p.get("TEAL_LIGHT", "#7FD39A")
        muted = p.get("TEXT_MUTED", "#9C9589")
        tajuk = QLabel(
            f'<span style="font-size:21px;font-weight:800;color:{teal};">Pustaka</span>'
            f'<span style="font-size:21px;font-weight:300;color:{teal_l};">Hadith</span>'
            f'<span style="font-size:12px;font-weight:400;color:{muted};"> v{VERSI}</span>')
        tajuk.setTextFormat(Qt.RichText)
        tajuk.setAlignment(Qt.AlignCenter)
        lo.addWidget(tajuk)

        teks = QTextEdit()
        teks.setPlainText(TEKS)
        teks.setReadOnly(True)
        teks.setStyleSheet(
            f"font-size: 13px; line-height: 1.5; padding: 8px; color: {FG};"
            f"background: transparent; border: none;"
        )
        lo.addWidget(teks, 1)

        btn = QPushButton("Faham")
        btn.setMinimumHeight(40)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet(
            "QPushButton { background-color: #1a7a5c; color: white;"
            "border-radius: 8px; font-size: 14px; font-weight: 600;"
            "padding: 8px 24px; }"
            "QPushButton:hover { background-color: #15634a; }"
        )
        btn.clicked.connect(self._terima)
        lo.addWidget(btn)

    def _terima(self):
        _simpan_dibaca()
        self.accept()


def papar_disclaimer(parent=None) -> bool:
    """Papar dialog setiap kali larian. True jika dialog dipapar.

    parent=None supaya dialog berdiri sendiri di tengah skrin.
    exec_() blok sehingga pengguna klik 'Faham'.
    """
    dlg = DisclaimerDialog()
    dlg.exec_()
    return True
