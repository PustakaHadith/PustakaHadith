"""Dialog 'Lapor Ralat' — pengguna laporkan masalah kepada pembangun.

Buka klien e-mel lalai melalui pautan `mailto:` (tiada pelayan SMTP /
kredential diperlukan). Penerima dikunci `pustakahadis@gmail.com`, tajuk
lalai "LAPOR RALAT", dan e-mel pengguna disertakan dalam badan supaya
pembangun boleh membalas.
"""

from __future__ import annotations

import webbrowser
from urllib.parse import quote

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QDialog, QHBoxLayout, QLabel, QLineEdit, QPlainTextEdit, QPushButton,
    QVBoxLayout,
)

from ui.theme import (
    BORDER, CARD_BG, CARD_BG_HOVER, PAGE_BG, TEAL, TEAL_LIGHT,
    TEXT_MUTED, TEXT_PRIMARY, TEXT_SECONDARY,
)

DEV_EMAIL = "pustakahadis@gmail.com"
SUBJEK_LALAI = "LAPOR RALAT"


class LaporRalatDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Lapor Ralat")
        self.setMinimumWidth(460)
        self.setMinimumHeight(360)
        self.setStyleSheet(f"QDialog {{ background-color: {PAGE_BG}; }}")

        v = QVBoxLayout(self)
        v.setContentsMargins(20, 18, 20, 18)
        v.setSpacing(12)

        nota = QLabel("Laporkan ralat anda di sini.")
        nota.setObjectName("muted")
        nota.setWordWrap(True)
        v.addWidget(nota)

        # Medan input: latar putih + teks HITAM (dialog mewarisi tema
        # gelap apl, jadi teks hitam mesti ditegakkan supaya kelihatan).
        in_ss = (f"background-color: #ffffff; color: #000000; "
                 f"border: 1px solid {BORDER}; border-radius: 6px; "
                 f"padding: 6px;")

        # Daripada (e-mel pengguna)
        frm = QHBoxLayout()
        fl = QLabel("Daripada (e-mel)")
        fl.setFixedWidth(120)
        self._email = QLineEdit()
        self._email.setPlaceholderText("anda@email.com")
        self._email.setStyleSheet(in_ss)
        frm.addWidget(fl)
        frm.addWidget(self._email, 1)
        v.addLayout(frm)

        # Tajuk / subjek
        sj = QHBoxLayout()
        sl = QLabel("Tajuk")
        sl.setFixedWidth(120)
        self._subjek = QLineEdit(SUBJEK_LALAI)
        self._subjek.setStyleSheet(in_ss)
        sj.addWidget(sl)
        sj.addWidget(self._subjek, 1)
        v.addLayout(sj)

        # Mesej
        self._mesej = QPlainTextEdit()
        self._mesej.setPlaceholderText("Laporkan ralat anda di sini.")
        self._mesej.setStyleSheet(in_ss)
        self._mesej.setMinimumHeight(150)
        v.addWidget(self._mesej, 1)

        # Butang
        bb = QHBoxLayout()
        bb.addStretch()
        batal = QPushButton("Batal")
        batal.setCursor(Qt.PointingHandCursor)
        batal.setFixedSize(96, 34)
        batal.setStyleSheet(
            f"QPushButton {{ background: transparent; border: 1px solid "
            f"{BORDER}; color: {TEXT_MUTED}; border-radius: 8px; "
            f"font-size: 13px; }} "
            f"QPushButton:hover {{ color: {TEAL}; border-color: {TEAL_LIGHT}; }}")
        batal.clicked.connect(self.reject)
        hantar = QPushButton("Hantar")
        hantar.setCursor(Qt.PointingHandCursor)
        hantar.setFixedSize(96, 34)
        hantar.setStyleSheet(
            f"QPushButton {{ background-color: {TEAL}; color: {PAGE_BG}; "
            f"border: none; border-radius: 8px; font-size: 13px; "
            f"font-weight: 700; }} "
            f"QPushButton:hover {{ background-color: {TEAL_LIGHT}; }}")
        hantar.clicked.connect(self._hantar)
        bb.addWidget(batal)
        bb.addWidget(hantar)
        v.addLayout(bb)

    def _hantar(self):
        email = self._email.text().strip()
        subjek = self._subjek.text().strip() or SUBJEK_LALAI
        mesej = self._mesej.toPlainText().strip()
        body = mesej
        if email:
            body = f"Daripada: {email}\n\n{body}"
        url = (f"mailto:{DEV_EMAIL}?subject={quote(subjek)}"
               f"&body={quote(body)}")
        webbrowser.open(url)
        self.accept()
