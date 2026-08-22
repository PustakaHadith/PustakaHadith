"""Deklarasi PustakaHadith — skrin permulaan (sekali) + halaman Tentang.

Teks diambil daripada `DEKLARASI.md` (8 Ogos 2026): apa aplikasi ini
dan apa ia BUKAN, batasan, sumber & atribusi, dan sokongan. Bahagian
"Kedudukan berbanding platform lain" dalam DEKLARASI.md ialah rujukan
dalaman sahaja -- TIDAK dipapar dalam aplikasi.

`DeklarasiDialog(penuh=False)` ialah dialog mod -- teks pendek dengan
butang "Faham" (larian pertama) atau teks penuh dengan butang "Tutup"
(halaman Tentang). Bendera `deklarasi_dibaca` disimpan dalam
user_settings.json supaya dialog pendek hanya muncul SEKALI.
"""

from __future__ import annotations

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (
    QDialog, QFrame, QHBoxLayout, QLabel, QPushButton, QScrollArea,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget,
)

from ui.theme import (
    AMBER_TEXT, BORDER, CARD_BG, HEADER_BG, PAGE_BG, TEAL, TEAL_LIGHT,
    TEXT_FAINT, TEXT_MUTED, TEXT_PRIMARY,
)

DEKLARASI_FLAG = "deklarasi_dibaca"
SEMAKHADIS_URL = "https://semakhadis.com"
HADISMY_URL = "https://hadis.my"
FAWAZ_URL = "https://github.com/fawazahmed0/hadith-api"


# ── binaan baris ────────────────────────────────────────────────────
def _lbl(teks="", saiz=13, warna=None, tebal=False, atas=0, bawah=0):
    if warna is None:
        warna = TEXT_PRIMARY
    l = QLabel(teks)
    l.setWordWrap(True)
    l.setTextInteractionFlags(Qt.TextSelectableByMouse)
    gaya = f"font-size: {saiz}px; color: {warna};"
    if tebal:
        gaya += " font-weight: 700;"
    if atas or bawah:
        gaya += f" margin-top: {atas}px; margin-bottom: {bawah}px;"
    l.setStyleSheet(gaya)
    return l


def _tajuk(v: QVBoxLayout, teks: str):
    v.addWidget(_lbl(teks, saiz=20, warna=TEAL, tebal=True, atas=6, bawah=2))


def _kepala(v: QVBoxLayout, teks: str, warna=None):
    if warna is None:
        warna = TEXT_PRIMARY
    v.addWidget(_lbl(teks, saiz=14, warna=warna, tebal=True, atas=10, bawah=2))


def _perenggan(v: QVBoxLayout, teks: str, warna=None):
    if warna is None:
        warna = TEXT_PRIMARY
    v.addWidget(_lbl(teks, saiz=13, warna=warna))


def _peluru(v: QVBoxLayout, teks: str, warna=None):
    if warna is None:
        warna = TEXT_PRIMARY
    v.addWidget(_lbl("•  " + teks, saiz=13, warna=warna))


def _pautan(v: QVBoxLayout, teks_html: str):
    l = QLabel(teks_html)
    l.setWordWrap(True)
    l.setTextFormat(Qt.RichText)
    l.setOpenExternalLinks(True)
    l.setTextInteractionFlags(Qt.TextBrowserInteraction)
    l.setStyleSheet(f"font-size: 13px; color: {TEXT_PRIMARY}; "
                    f"a {{ color: {TEAL_LIGHT}; }}")
    v.addWidget(l)


# ── dialog ──────────────────────────────────────────────────────────
class DeklarasiDialog(QDialog):
    """Dialog deklarasi: pendek (larian pertama) atau penuh (Tentang)."""

    def __init__(self, penuh: bool = False, parent=None):
        super().__init__(parent)
        self.setModal(True)
        self.setWindowTitle("Tentang PustakaHadith" if penuh
                            else "PustakaHadith")
        self.setMinimumWidth(560)
        self.setMaximumWidth(640)
        self.setStyleSheet(f"QDialog {{ background: {PAGE_BG}; }}")

        akar = QVBoxLayout(self)
        akar.setContentsMargins(0, 0, 0, 0)
        akar.setSpacing(0)

        sa = QScrollArea()
        sa.setWidgetResizable(True)
        sa.setFrameShape(QFrame.NoFrame)
        sa.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        sa.setStyleSheet("background: transparent;")
        akar.addWidget(sa, 1)

        isi = QWidget()
        isi.setStyleSheet("background: transparent;")
        sa.setWidget(isi)
        v = QVBoxLayout(isi)
        v.setContentsMargins(26, 22, 26, 18)
        v.setSpacing(10)

        if penuh:
            self._bina_penuh(v)
        else:
            self._bina_pendek(v)

        bar = QWidget()
        bar.setStyleSheet(
            f"background: {CARD_BG}; border-top: 1px solid {BORDER};")
        bl = QHBoxLayout(bar)
        bl.setContentsMargins(20, 12, 20, 12)
        bl.addStretch(1)
        btn = QPushButton("Tutup" if penuh else "Faham")
        btn.setCursor(Qt.PointingHandCursor)
        btn.setMinimumWidth(110)
        btn.setFixedHeight(38)
        btn.setStyleSheet(f"""
            QPushButton {{ background-color: {TEAL}; color: #FFFFFF;
                           border: none; border-radius: 8px;
                           font-size: 13px; font-weight: 700; }}
            QPushButton:hover {{ background-color: {TEAL_LIGHT}; }}
        """)
        btn.clicked.connect(self.accept)
        bl.addWidget(btn)
        akar.addWidget(bar)

    # ── teks pendek — skrin permulaan ───────────────────────────────
    def _bina_pendek(self, v: QVBoxLayout):
        v.addWidget(_lbl("PustakaHadith", saiz=22, warna=TEAL, tebal=True))
        v.addWidget(_lbl("Rujukan digital 9 kitab hadis dalam Bahasa "
                         "Melayu", saiz=13, warna=TEXT_MUTED, bawah=8))
        _perenggan(v, "Aplikasi ini menghimpunkan 62,169 hadis "
                      "daripada sembilan kitab utama — Bukhari, Muslim, "
                      "Abu Daud, Tirmidzi, An-Nasa'i, Ibnu Majah, Ahmad, "
                      "Ad-Darimi, dan Muwatta Malik — lengkap dengan teks "
                      "Arab, terjemahan, transliterasi, dan carian.")
        _perenggan(v, "Ia dibina untuk pelajar, pengkaji, peminat hadis, "
                      "dan pengguna awam yang mahu merujuk hadis dengan "
                      "cepat.")
        _kepala(v, "Aplikasi ini BUKAN:")
        _peluru(v, "Bukan sumber fatwa. Ia tidak memberi hukum. Untuk "
                   "keputusan agama, rujuk ulama bertauliah.")
        _pautan(v, "•  Bukan alat semakan hadis palsu. Ia memaparkan "
                   "hadis daripada sembilan kitab tersebut sahaja. Untuk "
                   "menyemak hadis yang beredar di media sosial, gunakan "
                   f"<a href=\"{SEMAKHADIS_URL}\">SemakHadis.com</a> "
                   "(pautan disediakan dalam aplikasi).")
        _peluru(v, "Bukan pengganti guru. Memahami hadis memerlukan ilmu "
                   "alat — konteks, sanad, dan kaedah usul. Aplikasi "
                   "hanya menyediakan teks.")
        _perenggan(v, "Tentang darjat hadis: penilaian yang dipaparkan "
                      "datang daripada ulama hadis moden. Ulama boleh "
                      "berbeza pendapat tentang hadis yang sama. Aplikasi "
                      "memaparkan setiap penilaian sebagaimana adanya, "
                      "tanpa memilih antara mereka.", warna=TEXT_MUTED)

    # ── teks penuh — halaman Tentang ────────────────────────────────
    def _bina_penuh(self, v: QVBoxLayout):
        v.addWidget(_lbl("Tentang PustakaHadith", saiz=22, warna=TEAL,
                         tebal=True))
        v.addWidget(_lbl("Versi 1.0 — aplikasi desktop percuma, berjalan "
                         "sepenuhnya luar talian.", saiz=13,
                         warna=TEXT_MUTED, bawah=6))

        _kepala(v, "Tujuan")
        _perenggan(v, "Menyediakan rujukan hadis yang pantas, lengkap, "
                      "dan boleh dipercayai dalam Bahasa Melayu untuk "
                      "pelajar, pengkaji, peminat hadis, dan pengguna "
                      "awam.")

        _kepala(v, "Kandungan")
        data = [
            ("Hadis", "62,169 daripada 9 kitab (kutub al-tis'ah)"),
            ("Teks Arab", "penuh dengan tashkeel"),
            ("Terjemahan Melayu", "62,169 (100%)"),
            ("Terjemahan Indonesia", "62,169 (100%)"),
            ("Terjemahan Inggeris", "31,833 (51%)"),
            ("Huraian ringkas", "4,237 hadis"),
            ("Darjat ulama", "mengikut ketersediaan sumber"),
            ("Transliterasi", "dijana automatik"),
            ("Carian", "kata kunci + carian makna"),
        ]
        tbl = QTableWidget(len(data), 2)
        tbl.setEditTriggers(QTableWidget.NoEditTriggers)
        tbl.setSelectionMode(QTableWidget.NoSelection)
        tbl.verticalHeader().setVisible(False)
        tbl.horizontalHeader().setVisible(False)
        tbl.setColumnWidth(0, 180)
        tbl.setColumnWidth(1, 340)
        tbl.setShowGrid(True)
        tbl.setStyleSheet(
            f"QTableWidget {{ background: transparent; border: 1px solid {BORDER};"
            f" gridline-color: {BORDER}; font-size: 13px; }}"
            f" QTableWidget::item {{ padding: 6px 10px; }}"
        )
        for i, (kiri, kanan) in enumerate(data):
            ki = QTableWidgetItem(kiri)
            ki.setForeground(QColor(TEXT_FAINT))
            ki.setFlags(Qt.ItemIsEnabled)
            kn = QTableWidgetItem(kanan)
            kn.setForeground(QColor(TEXT_PRIMARY))
            kn.setFlags(Qt.ItemIsEnabled)
            tbl.setItem(i, 0, ki)
            tbl.setItem(i, 1, kn)
            row_h = tbl.rowHeight(i)
            if row_h < 34:
                tbl.setRowHeight(i, 34)
        tbl.setMinimumHeight(len(data) * 34 + 4)
        v.addWidget(tbl)

        _kepala(v, "Sumber dan atribusi")
        sumber = [
            ("Teks hadis, terjemahan\nMelayu & Indonesia",
             f"<a href=\"{HADISMY_URL}\" style='color:{TEAL_LIGHT}'>" f"hadis.my</a> — API Hadis Malaysia"),
            ("Terjemahan Inggeris\n& darjat ulama",
             f"<a href=\"{FAWAZ_URL}\" style='color:{TEAL_LIGHT}'>" f"fawazahmed0/hadith-api</a> (domain awam)"),
            ("Huraian ringkas",
             f"<a href=\"{SEMAKHADIS_URL}\" style='color:{TEAL_LIGHT}'>" f"SemakHadis.com</a> — atribusi pada setiap huraian"),
        ]
        stbl = QTableWidget(len(sumber), 2)
        stbl.setEditTriggers(QTableWidget.NoEditTriggers)
        stbl.setSelectionMode(QTableWidget.NoSelection)
        stbl.verticalHeader().setVisible(False)
        stbl.horizontalHeader().setVisible(False)
        stbl.setColumnWidth(0, 180)
        stbl.setColumnWidth(1, 340)
        stbl.setShowGrid(True)
        stbl.setStyleSheet(
            f"QTableWidget {{ background: transparent; border: 1px solid {BORDER};"
            f" gridline-color: {BORDER}; font-size: 13px; }}"
            f" QTableWidget::item {{ padding: 6px 10px; }}"
            f" a {{ color: {TEAL_LIGHT}; }}"
        )
        for i, (kiri, kanan) in enumerate(sumber):
            ki = QTableWidgetItem(kiri)
            ki.setForeground(QColor(TEXT_FAINT))
            ki.setFlags(Qt.ItemIsEnabled)
            kn = QTableWidgetItem()
            kn.setText(kanan)
            kn.setFlags(Qt.ItemIsEnabled)
            # Pautan HTML perlu QLabel
            lbl = QLabel(kanan)
            lbl.setWordWrap(True)
            lbl.setTextFormat(Qt.RichText)
            lbl.setOpenExternalLinks(True)
            lbl.setTextInteractionFlags(Qt.TextBrowserInteraction)
            lbl.setStyleSheet(f"font-size:13px; color:{TEXT_PRIMARY};"
                              f" background:transparent; border:none;"
                              f" a{{color:{TEAL_LIGHT};}}")
            stbl.setItem(i, 0, ki)
            stbl.setCellWidget(i, 1, lbl)
            stbl.setRowHeight(i, 40)
        stbl.setMinimumHeight(len(sumber) * 40 + 4)
        v.addWidget(stbl)
        _perenggan(v, "Ucapan terima kasih kepada semua pihak di atas. "
                      "Tanpa kerja mereka, aplikasi ini tidak wujud.",
                   warna=TEXT_MUTED)

        _kepala(v, "Batasan — sila baca", warna=AMBER_TEXT)
        _peluru(v, "Bukan sumber fatwa. Aplikasi memaparkan teks hadis "
                   "dan penilaian ulama. Ia tidak memberi hukum, tidak "
                   "menjawab persoalan fiqh, dan tidak boleh dijadikan "
                   "asas keputusan agama. Rujuk ulama bertauliah.")
        _peluru(v, "Bukan alat semakan hadis palsu. Aplikasi ini terhad "
                   "kepada sembilan kitab hadis yang disebut. Hadis yang "
                   "beredar melalui WhatsApp, media sosial, atau ceramah "
                   "mungkin tidak berasal daripada kitab-kitab ini. "
                   "Untuk menyemaknya, gunakan SemakHadis.com — pangkalan "
                   "data khusus hadis daif dan palsu dalam Bahasa Melayu.")
        _peluru(v, "Darjat hadis: ulama berbeza pendapat. Satu hadis "
                   "boleh dinilai sahih oleh seorang ulama dan daif oleh "
                   "yang lain. Aplikasi memaparkan setiap penilaian "
                   "sebagaimana adanya dan tidak memilih antara mereka "
                   "— pemilihan (tarjih) adalah kerja ulama, bukan "
                   "perisian.")
        _peluru(v, "Carian makna dijana mesin. Ciri \"Carian Makna\" "
                   "menggunakan model bahasa untuk mencari hadis mengikut "
                   "maksud soalan. Ia alat carian, bukan tafsiran. "
                   "Hasilnya perlu disemak sendiri.")
        _peluru(v, "Terjemahan mungkin tidak lengkap. Sebilangan kecil "
                   "hadis mempunyai terjemahan yang tidak menyeluruh "
                   "dalam sumber asal. Bandingkan dengan teks Arab jika "
                   "ragu.")

        _kepala(v, "Sokongan")
        _perenggan(v, "Aplikasi ini percuma dan akan kekal percuma. "
                      "Penyelenggaraan bergantung kepada sumbangan "
                      "sukarela.")
