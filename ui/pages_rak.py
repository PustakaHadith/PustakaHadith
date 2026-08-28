"""Halaman Rak Digital 9 Kitab — mixin PustakaApp (25 Ogos 2026).

REKA BENTUK (UIUX_PustakaHadith/SELECTED_UIUX.md — "Rak Digital
Interaktif"): sembilan kitab dipaparkan sebagai JILID pada satu rak —
bukan grid kad 3×3. Klik jilid → pratonton kitab pada panel kiri;
butang `Buka kitab` membuka senarai hadis.

Susun atur digunakan untuk SEMUA tema: AQUA menunjukkan latar glob
(BackgroundCanvas) + panel kaca; tema lain = permukaan pepejal biasa.

GANDINGAN RENTAS MIXIN: memanggil `go`, `open_kitab`, `_total_of`,
`_do_search`, `search_bar` (PagesCarian), `api` (app_qt). Mesti
digabungkan bersama semua mixin halaman.

Peraturan tema: modul ini TIDAK import warna dari `ui.theme` (hanya
COLLECTION_META — metadata kitab, bukan warna tema), namun didaftar
dalam `_THEMED_MODULES` untuk konsisten.
"""

from __future__ import annotations

from PyQt5.QtCore import (
    QEasingCurve, QRectF, Qt, QPropertyAnimation, pyqtProperty, pyqtSignal,
)
from PyQt5.QtGui import QColor, QFont, QPainter
from PyQt5.QtWidgets import (
    QFrame, QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QWidget,
)

from ui.helpers import PAGES, _parse_lompat, read_history
from ui.theme import COLLECTION_META
from ui.widgets import BackgroundCanvas, attach_copy_menu, elide, make_scroll

# Saiz jilid pada rak (px, sebelum skala fon). Tinggi tetap — rak mesti
# kelihatan seperti barisan buku sebenar.
_LEBAR_JILID = 66
_TINGGI_JILID = 350


class JilidRak(QFrame):
    """Satu jilid buku pada rak — dilukis penuh dalam paintEvent.

    MENGAPA LUKISAN CUSTOM: teks menegak pada batang buku tiada widget
    siap dalam Qt. paintEvent melukis: rounded rect warna kitab,
    singkatan di atas, nama menegak di tengah, kiraan hadis di pangkal.
    Dipilih = border terang + opasiti penuh; tidak = 60% + pudar.

    ANIMASI TIMBUL (26 Ogos, permintaan pengguna): hover mengangkat
    jilid ~10px dengan bayang lembut di bawah — jilid "dicabut sedikit"
    dari rak. Dilaksanakan sebagai QPropertyAnimation pada sifat custom
    `angkat` (0.0–1.0) yang dicairkan dalam paintEvent. SENGAJA tidak
    guna QGraphicsDropShadowEffect: efek grafik aktif semasa navigasi
    halaman pernah mencetuskan ranap native (access violation, diukur
    16 Ogos — lihat ui/pages_home.py sejarah BungkusTimbul).
    """

    clicked = pyqtSignal(str)

    def __init__(self, slug: str, parent=None):
        super().__init__(parent)
        self._slug = slug
        self._meta = COLLECTION_META.get(slug, {})
        self._dipilih = False
        self._hover = False
        self._kiraan = ""
        self._angkat_v = 0.0          # 0 = di rak; 1 = terangkat penuh
        self.setFixedSize(_LEBAR_JILID, _TINGGI_JILID)
        self.setCursor(Qt.PointingHandCursor)
        self._anim = QPropertyAnimation(self, b"angkat", self)
        self._anim.setDuration(150)
        self._anim.setEasingCurve(QEasingCurve.OutCubic)
        singkatan = {
            "bukhari": "BU", "muslim": "MU", "abu-daud": "AD",
            "tirmidzi": "TI", "nasai": "AN", "ibnu-majah": "IM",
            "malik": "MW", "ahmad": "AH", "darimi": "DA",
        }
        self._singkatan = singkatan.get(slug, slug[:2].upper())

    # Sifat animasi — QPropertyAnimation menulis melalui setter ini;
    # setter mencetuskan repaint setiap frame.
    @pyqtProperty(float)
    def angkat(self) -> float:
        return self._angkat_v

    @angkat.setter
    def angkat(self, v: float):
        self._angkat_v = max(0.0, min(1.0, float(v)))
        self.update()

    def _terbangkan(self, sasaran: float):
        self._anim.stop()
        self._anim.setStartValue(self._angkat_v)
        self._anim.setEndValue(sasaran)
        self._anim.start()

    def set_dipilih(self, ya: bool):
        if self._dipilih != ya:
            self._dipilih = ya
            self.update()
        # Jilid dipilih KEKAL terangkat (permintaan pengguna) — bukan
        # sekadar naik bila hover. Bila dinyahpilih & tidak di-hover,
        # jatuhkan semula ke rak.
        if ya:
            self._terbangkan(1.0)
        elif not self._hover:
            self._terbangkan(0.0)

    def set_kiraan(self, n):
        self._kiraan = f"{n:,}" if isinstance(n, int) else ""
        self.update()

    def enterEvent(self, e):
        self._hover = True
        self._terbangkan(1.0)
        super().enterEvent(e)

    def leaveEvent(self, e):
        self._hover = False
        self._terbangkan(0.0)
        super().leaveEvent(e)

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton and self.rect().contains(e.pos()):
            self.clicked.emit(self._slug)
        super().mouseReleaseEvent(e)

    def keyPressEvent(self, e):
        # Enter/buka pada jilid fokus — aksesibiliti papan kekunci.
        if e.key() in (Qt.Key_Return, Qt.Key_Enter):
            self.clicked.emit(self._slug)
        else:
            super().keyPressEvent(e)

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        w, h = self.width(), self.height()
        a = self._angkat_v

        # Jilid terangkat sehingga ~10px; bayang di bawah menggelap
        # dan melebar apabila jilid makin tinggi (kesan "dicabut").
        naik = 10.0 * a

        # Geometri spina: RUANG KEPALA 12px di atas — batang jilid
        # bergerak dalam 12-naik .. h-4 dan TIDAK PERNAH terpotong
        # pada batas widget walaupun terangkat penuh (pembetulan:
        # dahulu top margin 6px < angkat 10px -> hujung atas terpotong).
        atas_spina = 12.0 - naik
        tinggi_spina = h - 16.0
        bawah = atas_spina + tinggi_spina

        asas = QColor(self._meta.get("warna", "#2E7D6B"))
        if self._dipilih:
            fill = QColor(asas)
            border = QColor("#FF9F1C")        # oren menonjol (pilihan)
            lebar_border = 3
        elif self._hover or a > 0.01:
            fill = QColor(asas).lighter(115)
            border = QColor(asas).lighter(150)
            lebar_border = 2
        else:
            fill = QColor(asas.red(), asas.green(), asas.blue(), 165)
            border = QColor(asas.darker(130))
            lebar_border = 1

        # Bayang lembut di pangkal — hanya apabila terangkat; sentiasa
        # di BAWAH tapak jilid supaya tidak dilindungi jilid sendiri.
        if a > 0.01:
            p.setPen(Qt.NoPen)
            bayang = QColor(0, 0, 0, int(70 * a))
            p.setBrush(bayang)
            lebar_bayang = (w - 10) + 8 * a
            p.drawRoundedRect(
                QRectF((w - lebar_bayang) / 2, bawah - 2 + 4 * a,
                       lebar_bayang, 5),
                3, 3)

        # Lingkaran bercahaya oren bila dipilih — tanda pilihan menonjol
        # (menggantikan garis putih lama). Di belakang batang jilid.
        if self._dipilih:
            p.setPen(Qt.NoPen)
            p.setBrush(QColor(255, 159, 28, 55))
            p.drawRoundedRect(
                QRectF(0, atas_spina - 2, w, tinggi_spina + 4), 10, 10)

        # Batang jilid — naik mengikut `a`.
        p.setPen(Qt.NoPen)
        p.setBrush(fill)
        p.drawRoundedRect(QRectF(2, atas_spina, w - 4, tinggi_spina), 8, 8)

        # Gurusan buku: garis menegak halus dekat tepi kiri/kanan.
        p.setPen(QColor(255, 255, 255, 40))
        p.drawLine(int(w * 0.18), int(atas_spina) + 8,
                   int(w * 0.18), int(bawah) - 8)
        p.drawLine(int(w * 0.82), int(atas_spina) + 8,
                   int(w * 0.82), int(bawah) - 8)

        # Singkatan di atas (mendatar).
        p.setPen(QColor(255, 255, 255, 230 if self._dipilih else 200))
        f = QFont(self.font())
        f.setPointSize(11)
        f.setBold(True)
        p.setFont(f)
        p.drawText(QRectF(0, atas_spina + 6, w, 22),
                   Qt.AlignCenter, self._singkatan)

        # Nama kitab MENEGAK (baca dari bawah ke atas) di tengah.
        f2 = QFont(self.font())
        f2.setPointSize(10)
        f2.setBold(self._dipilih)
        p.setFont(f2)
        p.save()
        p.translate(w / 2, atas_spina + tinggi_spina / 2)
        p.rotate(-90)
        teks = self._meta.get("short", self._slug)
        p.setPen(QColor(255, 255, 255, 235 if self._dipilih else 205))
        p.drawText(QRectF(-h / 2, -12, h, 24),
                   Qt.AlignCenter, teks)
        p.restore()

        # Kiraan hadis di pangkal (mendatar).
        if self._kiraan:
            f3 = QFont(self.font())
            f3.setPointSize(8)
            p.setFont(f3)
            p.setPen(QColor(255, 255, 255, 190))
            p.drawText(QRectF(0, bawah - 24, w, 18),
                       Qt.AlignCenter, self._kiraan)

        # Border — dipilih/hover lebih jelas.
        p.setBrush(Qt.NoBrush)
        p.setPen(QColor(border))
        pen = p.pen()
        pen.setWidth(lebar_border)
        p.setPen(pen)
        p.drawRoundedRect(QRectF(2, atas_spina, w - 4, tinggi_spina), 8, 8)


class PagesRak:
    # ── HALAMAN: Rak Digital 9 Kitab ─────────────────────────────────
    def _page_rak(self):
        kanvas = BackgroundCanvas()
        self.stack.addWidget(kanvas)
        sa = make_scroll(kanvas)
        sa.setObjectName("homeScroll")          # QSS telus sama dgn Utama
        body = QWidget()
        body.setObjectName("homeBody")
        sa.setWidget(body)
        vl = QVBoxLayout(kanvas)
        vl.setContentsMargins(0, 0, 0, 0)
        vl.addWidget(sa)

        bl = QVBoxLayout(body)
        bl.setContentsMargins(24, 20, 24, 20)
        bl.setSpacing(14)

        bl.addWidget(self._rak_banner())
        baris = QWidget()
        hl = QHBoxLayout(baris)
        hl.setContentsMargins(0, 0, 0, 0)
        hl.setSpacing(16)
        hl.addWidget(self._rak_pratonton(), 38)
        hl.addWidget(self._rak_rak(), 62)
        bl.addWidget(baris)
        # Halaman rak muat tanpa skrol pada 730px — stretch menyerap
        # ruang lebihan di bawah (kandungan < viewport).
        bl.addStretch(1)

        self._rak_pilih("bukhari")

    # ── banner atas ──────────────────────────────────────────────────
    def _rak_banner(self) -> QFrame:
        b = QFrame()
        b.setObjectName("glassPanel")
        h = QHBoxLayout(b)
        h.setContentsMargins(24, 16, 24, 16)
        h.setSpacing(16)

        kiri = QWidget()
        kl = QVBoxLayout(kiri)
        kl.setContentsMargins(0, 0, 0, 0)
        kl.setSpacing(2)
        eyebrow = QLabel("PUSTAKA DIGITAL  /  9 SUMBER UTAMA")
        eyebrow.setObjectName("eyebrow")
        kl.addWidget(eyebrow)
        t = QLabel("Rak Digital 9 Kitab")
        t.setObjectName("panelTitle")
        kl.addWidget(t)
        s = QLabel("Pilih sebuah jilid untuk pratonton; "
                   "buka apabila anda bersedia membaca.")
        s.setObjectName("muted")
        kl.addWidget(s)
        h.addWidget(kiri, 1)

        self._rak_carian = QLineEdit()
        self._rak_carian.setPlaceholderText("Cari kitab atau nombor… "
                                            "(cth. bukhari 433)")
        self._rak_carian.setFixedWidth(300)
        self._rak_carian.setMaximumHeight(40)
        attach_copy_menu(self._rak_carian)
        self._rak_carian.returnPressed.connect(self._rak_hantar_carian)
        h.addWidget(self._rak_carian)

        btn = QPushButton("Cari")
        btn.setObjectName("primary")
        btn.setCursor(Qt.PointingHandCursor)
        btn.setMinimumHeight(40)
        btn.clicked.connect(self._rak_hantar_carian)
        h.addWidget(btn)
        return b

    def _rak_hantar_carian(self):
        q = self._rak_carian.text().strip()
        if not q:
            return
        # Lompat 'bukhari 433' / '433' → butiran terus (pola sama Utama).
        j = _parse_lompat(q, default_slug=self._kitab_slug)
        if j:
            slug, n = j
            self._buka_hadis_terus(slug, n, dari="home")
            return
        self.search_bar.input.setText(q)
        self.go("search")
        self._do_search(1)

    # ── panel kiri: pratonton kitab dipilih ──────────────────────────
    def _rak_pratonton(self) -> QFrame:
        panel = QFrame()
        panel.setObjectName("glassPanel")
        self._rak_pv = QVBoxLayout(panel)
        self._rak_pv.setContentsMargins(24, 20, 24, 16)
        self._rak_pv.setSpacing(6)
        return panel

    def _rak_isi_pratonton(self, slug: str):
        """Bina semula kandungan panel pratonton untuk kitab `slug`."""
        meta = COLLECTION_META.get(slug, {})
        total = self._total_of(slug)
        lay = self._rak_pv
        while lay.count():
            it = lay.takeAt(0)
            w = it.widget()
            if w:
                w.setParent(None)
                w.deleteLater()

        cap = QLabel("KITAB DIPILIH")
        cap.setObjectName("eyebrow")
        lay.addWidget(cap)

        no = QLabel(f"{list(COLLECTION_META).index(slug) + 1:02d}")
        no.setObjectName("rakNombor")
        lay.addWidget(no)

        nama = QLabel(meta.get("name", slug))
        nama.setObjectName("panelTitle")
        nama.setWordWrap(True)
        lay.addWidget(nama)

        pengarang = QLabel(meta.get("author", ""))
        pengarang.setObjectName("teal")
        lay.addWidget(pengarang)

        desc = QLabel(meta.get("desc", ""))
        desc.setObjectName("body")
        desc.setWordWrap(True)
        lay.addWidget(desc)
        lay.addSpacing(6)

        kiraan = (f"{total:,} hadis" if isinstance(total, int)
                  else "Kiraan dimuat…")
        stat = QLabel(kiraan)
        stat.setObjectName("h3")
        lay.addWidget(stat)
        lay.addSpacing(6)

        # Terakhir dibaca kitab ini (sejarah bacaan, 25 Ogos).
        cap2 = QLabel("TERAKHIR DIBACA")
        cap2.setObjectName("panelSection")
        lay.addWidget(cap2)
        akhir = "Belum dibaca — jilid ini masih menunggu anda."
        for e in read_history():
            if e.get("slug") == slug:
                akhir = (f"Hadis #{e.get('n', '?')} · "
                         f"{elide(e.get('label', ''), 36)}")
                break
        lbl = QLabel(akhir)
        lbl.setObjectName("muted")
        lbl.setWordWrap(True)
        lay.addWidget(lbl)

        lay.addSpacing(10)
        baris_btn = QWidget()
        bl2 = QHBoxLayout(baris_btn)
        bl2.setContentsMargins(0, 0, 0, 0)
        bl2.setSpacing(8)
        buka = QPushButton("Buka kitab →")
        buka.setObjectName("primary")
        buka.setCursor(Qt.PointingHandCursor)
        buka.setMinimumHeight(40)
        buka.clicked.connect(lambda _, s=slug: self.open_kitab(s))
        bl2.addWidget(buka)
        bab = QPushButton("Lihat bab")
        bab.setCursor(Qt.PointingHandCursor)
        bab.setMinimumHeight(40)
        # Senarai hadis memaparkan nama bab pada setiap kad — buka kitab
        # (paparan bab khusus = cadangan fasa akan datang).
        bab.clicked.connect(lambda _, s=slug: self.open_kitab(s))
        bl2.addWidget(bab)
        lay.addWidget(baris_btn)

        lay.addSpacing(6)
        kembali = QLabel(f"<a href='#' style='color:{self._rak_pautan()}'>"
                         "← Kembali ke halaman utama</a>")
        kembali.setObjectName("muted")
        kembali.linkActivated.connect(lambda _: self.go("home"))
        lay.addWidget(kembali)
        lay.addStretch(1)

    def _rak_pautan(self) -> str:
        """Warna pautan ikut tema — baca semasa (elak nilai basi)."""
        import ui.theme as _t
        return getattr(_t, "TEAL", "#3EC9B0")

    # ── panel kanan: rak jilid ───────────────────────────────────────
    def _rak_rak(self) -> QFrame:
        panel = QFrame()
        panel.setObjectName("glassPanel")
        v = QVBoxLayout(panel)
        v.setContentsMargins(24, 20, 24, 14)
        v.setSpacing(8)

        atas = QWidget()
        al = QHBoxLayout(atas)
        al.setContentsMargins(0, 0, 0, 0)
        cap = QLabel("RAK KITAB")
        cap.setObjectName("eyebrow")
        al.addWidget(cap)
        al.addStretch(1)
        self._rak_kira_label = QLabel("01 / 09")
        self._rak_kira_label.setObjectName("faint")
        al.addWidget(self._rak_kira_label)
        v.addWidget(atas)

        hint = QLabel("Klik mana-mana jilid untuk melihat butiran — "
                      "atau guna kekunci ← →")
        hint.setObjectName("faint")
        v.addWidget(hint)

        rak = QWidget()
        self._rak_layout = QHBoxLayout(rak)
        self._rak_layout.setContentsMargins(8, 14, 8, 0)
        self._rak_layout.setSpacing(10)
        self._rak_layout.setAlignment(Qt.AlignCenter)
        self._rak_jilid = {}
        for slug in COLLECTION_META:
            j = JilidRak(slug)
            j.clicked.connect(self._rak_pilih)
            j.set_kiraan(self._total_of(slug))
            self._rak_layout.addWidget(j)
            self._rak_jilid[slug] = j
        v.addWidget(rak, 1)

        # Garis rak + penunjuk segitiga di bawah jilid dipilih.
        self._rak_garis = QFrame()
        self._rak_garis.setFixedHeight(3)
        self._rak_garis.setStyleSheet("background: transparent;")
        v.addWidget(self._rak_garis)

        bawah = QWidget()
        bl3 = QHBoxLayout(bawah)
        bl3.setContentsMargins(0, 2, 0, 0)
        petunjuk = QLabel("Pilih jilid dengan tetikus atau kekunci ← →; "
                          "Buka kitab untuk mula membaca")
        petunjuk.setObjectName("faint")
        bl3.addWidget(petunjuk)
        bl3.addStretch(1)
        sejajar = QLabel("9 jilid · satu rak")
        sejajar.setObjectName("faint")
        bl3.addWidget(sejajar)
        v.addWidget(bawah)

        # Fokus papan kekunci: ← → tukar pilihan, Enter buka —
        # dikendalikan oleh PustakaApp.keyPressEvent (PagesRak).
        return panel

    # ── interaksi ────────────────────────────────────────────────────
    def _rak_pilih(self, slug: str):
        """Pilih jilid `slug`: kemas kini spina + panel pratonton."""
        if slug not in COLLECTION_META:
            return
        self._rak_slug = slug
        idx = list(COLLECTION_META).index(slug)
        self._rak_kira_label.setText(f"{idx + 1:02d} / 09")
        for s, j in self._rak_jilid.items():
            j.set_dipilih(s == slug)
        self._rak_isi_pratonton(slug)

    def _rak_update_kiraan(self):
        """Kiraan hadis setiap jilid — dipanggil dari _on_collections."""
        for s, j in getattr(self, "_rak_jilid", {}).items():
            j.set_kiraan(self._total_of(s))
        # Pratonton mungkin memaparkan "Kiraan dimuat…" — segar.
        if getattr(self, "_rak_slug", None):
            self._rak_isi_pratonton(self._rak_slug)

    def keyPressEvent(self, e):
        # Navigasi papan kekunci pada halaman rak (← → pilih, Enter buka).
        if self.stack.currentIndex() == PAGES["rak"] \
                and getattr(self, "_rak_slug", None) is not None:
            senarai = list(COLLECTION_META)
            idx = senarai.index(self._rak_slug)
            if e.key() == Qt.Key_Left:
                self._rak_pilih(senarai[(idx - 1) % len(senarai)])
                return
            if e.key() == Qt.Key_Right:
                self._rak_pilih(senarai[(idx + 1) % len(senarai)])
                return
            if e.key() in (Qt.Key_Return, Qt.Key_Enter):
                self.open_kitab(self._rak_slug)
                return
        super().keyPressEvent(e)
