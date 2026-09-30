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
from ui.widgets import BackgroundCanvas
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
        # Saiz: LEBAR KEKAL ASAL 540 (arahan 28 Sep: jangan lebarkan);
        # tinggi dikunci dlm julat 2%~5% drp asal 600 → 612..630.
        self._lebar = 540
        self.setMinimumSize(self._lebar, 320)
        self.resize(self._lebar, 600)
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
        # Latar (25 Ogos, permintaan pengguna): kandungan dialog duduk
        # atas BackgroundCanvas — peta dunia rangkaian pada tema AQUA
        # (imej berbeza daripada Utama/rak, 26 Ogos), warna pepejal pada
        # tema lain. TekstEdit/butang sudah telus.
        p = apply_theme(_tema_tersimpan())
        BG = p.get("CARD_BG", "#1E1D1A")
        FG = p.get("TEXT_PRIMARY", "#E8E4DA")
        self.setStyleSheet(f"QDialog {{ background-color: {BG}; color: {FG}; }}")

        kanvas = BackgroundCanvas(self, dunia=True)
        lo = QVBoxLayout(kanvas)
        lo.setContentsMargins(28, 24, 28, 20)
        lo.setSpacing(12)
        luar = QVBoxLayout(self)
        luar.setContentsMargins(0, 0, 0, 0)
        luar.addWidget(kanvas)

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
        # Buang arrow skroll (arahan 28 Sep) — lebar dipaku dulu supaya
        # pengiraan tinggi document dlm `_bina` ikut bungkusan sebenar.
        teks.setFixedWidth(self._lebar - lo.contentsMargins().left()
                           - lo.contentsMargins().right())
        teks.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        teks.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
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

        # Tinggi dialog: kekal asal 600 + 2%~5% (612..630 — arahan
        # 28 Sep: "panjangkan sedikit") supaya ayat habis tanpa skroll.
        # Ruang selamat: jika teks melebihi ruang (skrin kecil), skroll
        # Hidup semula supaya teks tetap terbaca sampai habis.
        teks.document().adjustSize()
        doc_h = int(teks.document().size().height()) + 20  # padding 8*2
        tetap = (tajuk.sizeHint().height() + lo.spacing() * 2
                 + btn.sizeHint().height()
                 + lo.contentsMargins().top()
                 + lo.contentsMargins().bottom())
        tinggi = max(620, min(630, tetap + doc_h))
        h_teks = tinggi - tetap
        if doc_h > h_teks:
            teks.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        teks.setFixedHeight(h_teks)
        self.setFixedSize(self._lebar, tinggi)

    def _terima(self):
        _simpan_dibaca()
        self.accept()


def _boleh_papar() -> bool:
    """True jika tetapan 'makluman_papar' benarkan popup (lalai True)."""
    try:
        with open(_SETTINGS, encoding="utf-8") as f:
            return bool((json.load(f) or {}).get("makluman_papar", True))
    except Exception:
        return True


def papar_disclaimer(parent=None) -> bool:
    """Papar dialog setiap kali larian (ikut tetapan). True jika dipapar.

    Arahan 28 Sep — user boleh ON/OFF popup "Makluman" drp Tetapan
    (settings_panel, kunci `makluman_papar`; lalai True = papar).
    parent=None supaya dialog berdiri sendiri di tengah skrin.
    exec_() blok sehingga pengguna klik 'Faham'.
    """
    if not _boleh_papar():
        return False
    dlg = DisclaimerDialog()
    dlg.exec_()
    return True
