"""Halaman Kitab + lompat ke hadis — mixin PustakaApp (Sesi 30 refactor).

Dipisahkan dari `ui/app_qt.py`. Kelas `PagesKitab` menyediakan kaedah
halaman kitab dan lompat nombor hadis; digabungkan ke `PustakaApp`
melalui MRO: `class PustakaApp(PagesKitab, PagesCarian, QMainWindow)`.

Kaedah di sini bergantung pada state dan kaedah pada `self` (PustakaApp):
stack, _run, _tok, _kitab_*, toast, per_page(), ar_scale, ar_font,
_papar_melayu, _total_of, open_detail, go.

GANDINGAN RENTAS MIXIN: kaedah lompat di sini (`_sahkan_lompat`,
`_lompat_ke`, `_kira_halaman_lompat`) turut dipanggil oleh `PagesCarian`
(`_buka_hadis_terus`, `_hantar_carian`) dan halaman Utama
(`_from_home_search`). Jangan alih keluar kaedah ini tanpa mengemas
pemanggilnya.

Modul ini TIDAK import warna dari `ui.theme` (hanya COLLECTION_META,
metadata kitab) tetapi didaftar dalam `_THEMED_MODULES` supaya kekal
konsisten dengan modul UI lain.
"""

from __future__ import annotations

from PyQt5.QtCore import QPoint, Qt, QTimer
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import (
    QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget,
)

from ui.helpers import PAGES, _clear, click_sound
from ui.pages import Hero, Pager, _label_kiraan, breadcrumb, empty_state
from ui.theme import COLLECTION_META
from ui.widgets import BookCover, centered_column, hadith_card, make_scroll
from ui.workers import ListWorker


def _julat_lompat(total) -> str:
    """Placeholder kotak 'Lompat No. hadis'; 'No. hadis' jika tidak diketahui.

    Dahulu dibenamkan dalam `_render_kitab_shell`; kini fungsi tulen
    — diuji unit (semak.py 8w).
    """
    if not isinstance(total, int):
        return "No. hadis"
    return f"0–{total}"


class PagesKitab:
    # ── HALAMAN: Kitab ───────────────────────────────────────────────
    def _page_kitab(self):
        sa = make_scroll()
        self.stack.addWidget(sa)
        self._kitab_sa = sa

        # Butang terapung "↑ ke atas" (Sesi 34) — kelihatan bila pengguna
        # skrol ke bawah senarai hadis; klik untuk kembali ke hadis
        # pertama dengan animasi lancar. Anak kepada QScrollArea supaya
        # ia terapung di atas kandungan; dikemas pada setiap skrol dan
        # ubah saiz (lihat _kemas_butang_atas).
        if getattr(self, "_top_timer", None) is not None:
            self._top_timer.stop()
        self._kitab_top_btn = QPushButton("↑")
        self._kitab_top_btn.setObjectName("backTop")
        self._kitab_top_btn.setToolTip("Ke atas — hadis pertama")
        self._kitab_top_btn.setCursor(Qt.PointingHandCursor)
        self._kitab_top_btn.setFixedSize(44, 44)
        self._kitab_top_btn.setParent(sa)
        self._kitab_top_btn.clicked.connect(self._skrol_atas_lancar)
        self._kitab_top_btn.hide()
        sa.verticalScrollBar().valueChanged.connect(self._kemas_butang_atas)
        _orig_resize = sa.resizeEvent

        def _on_resize(e):
            _orig_resize(e)
            self._kemas_butang_atas()

        sa.resizeEvent = _on_resize

        body = QWidget()
        body.setObjectName("page")
        sa.setWidget(body)
        self._kitab_root = QVBoxLayout(body)
        self._kitab_root.setContentsMargins(0, 0, 0, 16)
        self._kitab_root.setSpacing(0)

    def open_kitab(self, slug, page=1):
        click_sound()
        self._kitab_slug = slug
        self._kitab_page = page
        self.go("kitab")
        self._render_kitab_shell()
        self._load_kitab_page(page)

    def _render_kitab_shell(self):
        _clear(self._kitab_root)
        meta = COLLECTION_META.get(self._kitab_slug, {})
        total = self._total_of(self._kitab_slug)
        # Placeholder kotak nombor memerlukan julat sebenar. Jika
        # koleksi belum dimuat (permulaan/offline), kira terus dari
        # pangkalan data — sama seperti _kira_halaman_lompat.
        if not isinstance(total, int) and self.api.offline:
            try:
                total = self.api.max_hadis_id(self._kitab_slug)
            except Exception:
                pass

        # Ilustrasi buku (Sesi 15/18) -- kad warna kitab + tajuk Arab,
        # 100% milik sendiri. Dipapar SEKALI di dalam banner halaman
        # kitab, di sebelah kiri tajuk (bukan blok berasingan antara
        # breadcrumb dan senarai).
        cover = BookCover(meta, self.ar_scale) if meta.get("arabic") else None
        self._kitab_root.addWidget(Hero(
            f'{meta.get("icon","")}  {meta.get("name", self._kitab_slug)}',
            meta.get("desc", ""),
            subtitle=_label_kiraan(total, "hadis", ""),
            compact=True,
            side=cover))

        col, cl = centered_column()
        cl.setContentsMargins(0, 18, 0, 0)
        cl.addWidget(breadcrumb([("Utama", lambda: self.go("home")),
                                 (meta.get("name", self._kitab_slug), None)]))

        # Kotak carian nombor hadis (Sesi 34) — lompat terus ke hadis
        # kesukaan tanpa skrol. Placeholder kabur menunjukkan julat
        # kitab semasa (cth. "0–7008" untuk Bukhari). Kotak "Pergi"
        # lama di pager bawah DIBUANG (Sesi 34) — lompat nombor kini
        # melalui kotak atas ini sahaja, memanggil _lompat_hadis yang
        # menyahkan julat + skrol ke kad.
        go_baris = QWidget()
        gl = QHBoxLayout(go_baris)
        gl.setContentsMargins(0, 0, 0, 0)
        gl.setSpacing(8)
        gl.addStretch(1)
        lbl = QLabel("Lompat No. hadis:")
        lbl.setObjectName("muted")
        gl.addWidget(lbl)
        self._kitab_go_box = QLineEdit()
        self._kitab_go_box.setPlaceholderText(_julat_lompat(total))
        self._kitab_go_box.setToolTip(
            "Taip nombor hadis lalu tekan Enter — contoh: 7008\n"
            "(pintasan: Ctrl+G)")
        self._kitab_go_box.setFixedWidth(120)
        self._kitab_go_box.setAlignment(Qt.AlignCenter)
        self._kitab_go_box.setValidator(QIntValidator(1, 999999, self))
        self._kitab_go_box.returnPressed.connect(self._hantar_go_box)
        gl.addWidget(self._kitab_go_box)
        gl.addStretch(1)
        cl.addWidget(go_baris)

        # Bungkus senarai dalam QWidget, bukan addLayout terus.
        # QWidget mempunyai sizeHint sendiri yang boleh diukur; layout
        # telanjang tidak, jadi QScrollArea tidak dapat tahu tinggi
        # sebenar kandungan dan menganggarkan berlebihan.
        self._kitab_container = QWidget()
        self._kitab_list = QVBoxLayout(self._kitab_container)
        self._kitab_list.setContentsMargins(0, 0, 0, 0)
        self._kitab_list.setSpacing(10)
        cl.addWidget(self._kitab_container)

        self._kitab_pager = Pager(lambda p: self._load_kitab_page(p))
        cl.addWidget(self._kitab_pager)
        # JANGAN addStretch(1) di sini. Diukur: apabila kandungan
        # melebihi viewport, stretch tetap menuntut ruang (794px) dan
        # QScrollArea menjadikannya kawasan BOLEH SKROL yang kosong --
        # pengguna skrol ke bawah dan jumpa ruang lompong.
        #
        # `col` sudah Expanding menegak, jadi ia mengisi viewport bila
        # kandungan pendek. Stretch tidak diperlukan langsung.
        # TIADA addStretch: diukur 572px kawasan skrol KOSONG di bawah
        # pager (kandungan tamat y=2742, body=3314). Hero tidak lagi
        # meregang kerana tingginya dikunci dalam Hero.resizeEvent.
        self._kitab_root.addWidget(col)

    def _load_kitab_page(self, page):
        self._kitab_page = page
        self._tok += 1
        tok = self._tok
        _clear(self._kitab_list)
        lbl = QLabel("Memuatkan…")
        lbl.setObjectName("muted")
        lbl.setAlignment(Qt.AlignCenter)
        self._kitab_list.addWidget(lbl)

        self._run(ListWorker(self.api, self._kitab_slug, page,
                             self.per_page(), self.lang_param, tok),
                  self._on_kitab_page)

    def _on_kitab_page(self, items, meta, tok):
        if tok != self._tok:
            return
        _clear(self._kitab_list)
        name = COLLECTION_META.get(self._kitab_slug, {}).get("name", "")
        if not items:
            self._kitab_list.addWidget(
                empty_state("📭", "Tiada hadis", "Koleksi ini kosong."))
            return
        for h in items:
            h.setdefault("collection", self._kitab_slug)
            c = hadith_card(h, name, self.ar_scale, show_chip=False,
                            arabic_font=self.ar_font,
                            papar_melayu=self._papar_melayu)
            c._hid = h.get("id")
            c.clicked.connect(lambda hh=h: self.open_detail(hh, "kitab"))
            self._kitab_list.addWidget(c)
        self._kitab_pager.set_state(meta.get("current_page", 1),
                                    meta.get("last_page", 1))
        self._laras_tinggi(self._kitab_sa)
        # Lompatan "Pergi ke nombor hadis": skrol ke kad sasaran supaya
        # pengguna terus nampak hadis yang diminta. Skrol manual dan
        # BUKAN ensureWidgetVisible (yang hanya mendedahkan bahagian
        # bawah kad di tepi viewport); di sini kad diletak ~1/3 dari atas.
        sasaran = self._kitab_go_to_hid
        self._kitab_go_to_hid = None
        bar = self._kitab_sa.verticalScrollBar()
        if sasaran is None:
            bar.setValue(0)
            return
        if bar.maximum() > 0:
            self._skrol_ke_kad(sasaran)
            return
        # Julat scrollbar hanya dikemas secara TAK SEGERAK, selepas
        # QScrollArea menerima resize event kandungan (layout selesai).
        # Memanggil setValue sebelum julat wujud akan terampas ke 0 --
        # kad sasaran langsung tidak kelihatan (diukur: Bukhari #500,
        # halaman 25, y=2910, viewport 738; tanpa ini skrol kekal 0).
        # Tunggu isyarat rangeChanged, kemudian skrol ke sasaran.
        def _bila_range(_mn, mx):
            if mx <= 0:
                return
            try:
                bar.rangeChanged.disconnect(_bila_range)
            except TypeError:
                pass
            self._skrol_ke_kad(sasaran)

        bar.rangeChanged.connect(_bila_range)

    def _skrol_ke_kad(self, sasaran: int):
        """Skrol senarai kitab supaya kad sasaran kelihatan ~1/3 dari atas.

        Dipanggil selepas layout selesai (julat scrollbar wujud) --
        lihat _on_kitab_page. Jika kad tidak dijumpai, skrol ke atas.
        """
        bar = self._kitab_sa.verticalScrollBar()
        for i in range(self._kitab_list.count()):
            it = self._kitab_list.itemAt(i)
            c = it.widget() if it else None
            if c is not None and getattr(c, "_hid", None) == sasaran:
                y = c.mapTo(self._kitab_sa.widget(), QPoint(0, 0)).y()
                bar.setValue(max(0, y - bar.pageStep() // 3))
                return
        bar.setValue(0)

    def _kira_halaman_lompat(self, slug: str, n: int):
        """Kira halaman yang mengandungi hadis No. n dalam kitab slug.

        Pulangkan (page, total). Kedudukan dikira dari BILANGAN hadis
        dengan id lebih kecil (bukan aritmetik mudah) -- tepat walaupun
        ada id yang hilang. Dalam mod dalam talian, penomboran hadis.my
        selanjar, jadi aritmetik mudah sudah memadai. total=0 bermakna
        had tidak diketahui.
        """
        per = self.per_page()
        total = self._total_of(slug) or 0
        if self.api.offline:
            try:
                total = self.api.max_hadis_id(slug) or total
            except Exception:
                pass
        page = (n - 1) // per + 1
        if self.api.offline:
            try:
                off = self.api.conn.execute(
                    "SELECT COUNT(*) FROM hadis "
                    "WHERE collection=? AND hadis_id<?",
                    (slug, n)).fetchone()[0]
                page = off // per + 1
            except Exception:
                pass
        return page, total

    def _sahkan_lompat(self, slug: str, n: int, nama: str):
        """Sahkan nombor hadis dalam julat kitab.

        Pulangkan (page, total) jika sah (atau julat tidak diketahui);
        papar toast dan pulangkan None jika jelas di luar julat. Dipakai
        oleh _lompat_hadis, _lompat_ke dan _buka_hadis_terus supaya
        logik julat tidak hanyut di tiga tempat.
        """
        page, total = self._kira_halaman_lompat(slug, n)
        if total and not (1 <= n <= total):
            self.toast.show_msg(f"⚠️ Hadis No. {n} tiada dalam {nama} "
                                f"(1–{total}).")
            return None
        return page, total

    def _lompat_hadis(self, n: int):
        """Lompat ke nombor hadis dalam kitab aktif (kotak atas senarai)."""
        slug = self._kitab_slug
        nama = COLLECTION_META.get(slug, {}).get("name", slug)
        r = self._sahkan_lompat(slug, n, nama)
        if r is None:
            return
        page, _ = r
        self._kitab_go_to_hid = n
        self.toast.show_msg(f"📖 Hadis No. {n} — halaman {page}")
        self._load_kitab_page(page)

    def _hantar_go_box(self):
        """Hantar kotak carian nombor hadis — terus buka detail (bukan list).

        Pengguna mahu masukkan nombor hadis dan terus melihat butiran,
        bukan skrol ke kad dalam senarai. Guna _buka_hadis_terus (Sesi 38)
        yang sahkan julat dahulu, beri toast, kemudian muat butiran.
        """
        n = self._kitab_go_box.text().strip()
        if not n:
            return
        self._kitab_go_box.clear()
        try:
            n = int(n)
        except ValueError:
            return
        self._buka_hadis_terus(self._kitab_slug, n, dari="kitab")

    def _kemas_butang_atas(self):
        """Tunjuk/sembunyi butang ↑ mengikut kedudukan skrol (Sesi 34).

        Butang hanya berguna bila senarai melebihi viewport dan pengguna
        sudah skrol ke bawah (melebihi 250px). Di kedudukan atas ia
        disembunyikan supaya tidak menghalang kandungan. Kedudukan
        dikira semula pada setiap skrol dan ubah saiz tetingkap.
        """
        b = getattr(self, "_kitab_top_btn", None)
        sa = getattr(self, "_kitab_sa", None)
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
        """Skrol lancar ke atas senarai — animasi QTimer ~250ms.

        Langkah mengecil (jarak dibahagi 15) supaya pergerakan kelihatan
        perlahan berhampiran sasaran. Timer disimpan pada `self` supaya
        panggilan kedua menghentikan animasi pertama.
        """
        bar = self._kitab_sa.verticalScrollBar()
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

    def _lompat_ke(self, slug: str, n: int):
        """Lompat ke hadis No. n dalam kitab slug (dari carian pantas)."""
        nama = COLLECTION_META.get(slug, {}).get("name", slug)
        r = self._sahkan_lompat(slug, n, nama)
        if r is None:
            return
        page, _ = r
        self._kitab_go_to_hid = n
        self.toast.show_msg(f"📖 {nama} No. {n} — halaman {page}")
        self.open_kitab(slug, page)

    def _focus_lompat(self):
        """Pintasan Ctrl+G: fokus ke kotak carian nombor di atas senarai.

        Jika belum di halaman kitab, buka kitab aktif dahulu (senarai
        dimuat semula); kemudian skrol kotak ke dalam pandangan dan
        fokuskan input supaya pengguna terus taip nombor.
        """
        if self.stack.currentIndex() != PAGES["kitab"]:
            self.open_kitab(self._kitab_slug, self._kitab_page)
        kotak = getattr(self, "_kitab_go_box", None)
        if kotak is None:
            return
        # Tunggu susun atur selesai (kotak mungkin baharu dibina semula
        # oleh open_kitab di atas) sebelum skrol & fokus.
        QTimer.singleShot(0, lambda: self._fokus_go_box(kotak))

    def _fokus_go_box(self, kotak):
        # Kotak ditangkap sebelum QTimer.singleShot(0); jika UI dibina
        # semula dalam pada itu (cth. tukar tema -> deleteLater), widget
        # lama sudah mati -- jangan sentuh objek SIP tertunda padam.
        if kotak is not getattr(self, "_kitab_go_box", None):
            return
        sa = getattr(self, "_kitab_sa", None)
        if sa is not None:
            sa.ensureWidgetVisible(kotak, 0, 60)
        kotak.setFocus(Qt.ShortcutFocusReason)
        kotak.selectAll()
