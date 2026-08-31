"""Halaman Simpan & Sejarah — mixin PustakaApp.

Susun atur SERAGAM dengan Senarai Hadis (pages_kitab.py): banner kaca +
sidebar "SIMPAN MENGIKUT KITAB" (kiraan per kitab, boleh klik untuk
tapIS) + panel senarai dwibahasa memenuhi lebar tetingkap (tiada lajur
tengah sempit). Dua tab: Tersimpan | Telah dibaca.

Tulis semula (Sesi ini) untuk membaiki dua masalah pengguna:
  • Ruang kosong kiri/kanan — lajur memenuhi ruang (seperti _kitab_panel).
  • Ikon Simpan tidak seragam — guna IconActionButton "simpan" (SVG sama
    seperti halaman detail), bukan emoji 🔖.

Latar: BackgroundCanvas (glob AQUA). Kaedah awam kekal: _page_saved
(dipanggil sekali bila halaman dibina) dan _render_saved (dipanggil oleh
go("saved") setiap navigasi) — tiada perubahan pada pemanggil luar.
"""

from __future__ import annotations

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import (
    QCheckBox, QFrame, QHBoxLayout, QLabel, QPushButton, QScrollArea,
    QSizePolicy, QVBoxLayout, QWidget,
)

from ui.helpers import _clear, read_history, remove_reading
from ui.pages import empty_state
from ui.theme import COLLECTION_META
from ui.widgets import (
    BackgroundCanvas, ClickCard, IconActionButton,
    hadith_card_dwibahasa, make_scroll,
)

class PagesTersimpan:
    # ── HALAMAN: Simpan & Sejarah ──────────────────────────────────────
    def _page_saved(self):
        # Pola sama _page_kitab: BackgroundCanvas akar, skrol telus di
        # atasnya — glob AQUA kelihatan di belakang panel kaca.
        kanvas = BackgroundCanvas()
        self.stack.addWidget(kanvas)
        sa = make_scroll(kanvas)
        sa.setObjectName("savedScroll")
        sa.setStyleSheet("background: transparent;")
        # Pastikan kandungan bermula di ATAS (bukan memusat menegak bila
        # senarai pendek — yang kelihatan "cacat" pada tab kosong).
        sa.setAlignment(Qt.AlignTop)
        self._tersimpan_sa = sa
        body = QWidget()
        body.setObjectName("homeBody")
        sa.setWidget(body)
        vl = QVBoxLayout(kanvas)
        vl.setContentsMargins(0, 0, 0, 0)
        vl.addWidget(sa)

        self._saved_root = QVBoxLayout(body)
        self._saved_root.setContentsMargins(24, 20, 24, 20)
        self._saved_root.setSpacing(14)

        # Butang terapung "↑ ke atas" (sama _kitab / corak Sesi 34).
        if getattr(self, "_top_timer_tersimpan", None) is not None:
            self._top_timer_tersimpan.stop()
        self._tersimpan_top_btn = QPushButton("↑")
        self._tersimpan_top_btn.setObjectName("backTop")
        self._tersimpan_top_btn.setToolTip("Ke atas — hadis pertama")
        self._tersimpan_top_btn.setCursor(Qt.PointingHandCursor)
        self._tersimpan_top_btn.setFixedSize(44, 44)
        self._tersimpan_top_btn.setParent(sa)
        self._tersimpan_top_btn.clicked.connect(
            self._skrol_atas_lancar_tersimpan)
        self._tersimpan_top_btn.hide()
        sa.verticalScrollBar().valueChanged.connect(
            self._kemas_butang_atas_tersimpan)
        _orig_resize = sa.resizeEvent

        def _on_resize(e):
            _orig_resize(e)
            self._kemas_butang_atas_tersimpan()

        sa.resizeEvent = _on_resize

        # State tab / penapis (kekal merentas navigasi).
        self._saved_tab = "simpan"
        self._saved_filter_slug = None
        self._sejarah_checks = []
        self._sejarah_all_chk = None
        self._sejarah_buang_btn = None

        # Kandungan awal (juga di-render semula oleh go("saved")).
        self._render_saved()

    def _render_saved(self):
        _clear(self._saved_root)
        self._sejarah_checks = []
        self._saved_root.addWidget(self._saved_banner())
        baris = QWidget()
        hl = QHBoxLayout(baris)
        hl.setContentsMargins(0, 0, 0, 0)
        hl.setSpacing(16)
        hl.addWidget(self._saved_sidebar(), 0)
        hl.addWidget(self._saved_panel(), 1)
        # TIADA addStretch pada _saved_root — senarai melebihi viewport;
        # stretch menuntut ruang tetap dan menjadikan kawasan bawah kosong.
        self._saved_root.addWidget(baris)
        # ISI senarai — _render_saved hanya bina shell (banner + sidebar +
        # panel). Tanpa panggilan ini senarai kekal KOSONG sehingga pengguna
        # klik sidebar ("Semua kitab") melalui _saved_pilih_kitab. Ini punca
        # "tab Tersimpan kosong" dan "senarai jadi kosong bila buang bookmark".
        self._render_senarai_simpan()

    # ── banner atas ────────────────────────────────────────────────────
    def _saved_banner(self) -> QFrame:
        b = QFrame()
        b.setObjectName("glassPanel")
        h = QHBoxLayout(b)
        h.setContentsMargins(24, 16, 24, 16)
        h.setSpacing(16)

        kiri = QWidget()
        kl = QVBoxLayout(kiri)
        kl.setContentsMargins(0, 0, 0, 0)
        kl.setSpacing(2)
        eyebrow = QLabel("KOLEKSI PERIBADI  ·  SIMPAN & SEJARAH")
        eyebrow.setObjectName("eyebrow")
        kl.addWidget(eyebrow)
        t = QLabel("Simpan & Sejarah")
        t.setObjectName("homeH1")
        kl.addWidget(t)
        n_bm = len(self.bookmarks)
        n_rd = len(read_history())
        m = QLabel(f"{n_bm:,} tersimpan  ·  {n_rd:,} dibaca")
        m.setObjectName("muted")
        kl.addWidget(m)
        h.addWidget(kiri, 1)
        return b

    # ── sidebar kiri ───────────────────────────────────────────────────
    def _kira_per_kitab(self) -> dict:
        """Kiraan entri mengikut kitab untuk tab aktif."""
        src = read_history() if self._saved_tab == "baca" else self.bookmarks
        out: dict = {}
        for e in src:
            s = e.get("slug")
            if s:
                out[s] = out.get(s, 0) + 1
        return out

    def _saved_sidebar(self) -> QFrame:
        s = QFrame()
        s.setObjectName("glassPanel")
        s.setFixedWidth(300)
        sl = QVBoxLayout(s)
        sl.setContentsMargins(16, 14, 16, 14)
        sl.setSpacing(10)

        ek = QLabel("SIMPAN MENGIKUT KITAB"
                    if self._saved_tab == "simpan"
                    else "DIBACA MENGIKUT KITAB")
        ek.setObjectName("panelSection")
        sl.addWidget(ek, 0, Qt.AlignLeft)

        per = self._kira_per_kitab()
        self._saved_rows = []
        self._tambah_side_row(sl, None, "Semua kitab",
                              sum(per.values()),
                              self._saved_filter_slug is None)
        for slug in COLLECTION_META:
            n = per.get(slug, 0)
            # Sembunyi kitab kosong, KECUALI yang sedang ditapis (supaya
            # pengguna boleh buang tapis kembali ke "Semua").
            if n == 0 and self._saved_filter_slug != slug:
                continue
            nama = COLLECTION_META[slug].get("name", slug)
            self._tambah_side_row(sl, slug, nama, n,
                                  self._saved_filter_slug == slug)
        sl.addStretch(1)
        return s

    def _tambah_side_row(self, sl, slug, nama, kiraan, aktif):
        row = ClickCard()
        row.setObjectName("babRow_active" if aktif else "babRow")
        rl = QHBoxLayout(row)
        rl.setContentsMargins(10, 7, 10, 7)
        rl.setSpacing(6)
        nl = QLabel(nama)
        nl.setToolTip(nama)
        rl.addWidget(nl, 1)
        if isinstance(kiraan, int):
            cl = QLabel(f"{kiraan:,}")
            cl.setObjectName("faint" if not aktif else "teal")
            rl.addWidget(cl)
        row.clicked.connect(lambda s=slug: self._saved_pilih_kitab(s))
        self._saved_rows.append((slug, row))
        sl.addWidget(row)

    def _saved_pilih_kitab(self, slug):
        if self._saved_filter_slug == slug:
            return
        self._saved_filter_slug = slug
        self._kemas_side_rows()
        self._render_senarai_simpan()

    def _kemas_side_rows(self):
        for slug, row in getattr(self, "_saved_rows", []):
            aktif = slug == self._saved_filter_slug
            row.setObjectName("babRow_active" if aktif else "babRow")
            row.style().unpolish(row)
            row.style().polish(row)

    # ── panel kanan ────────────────────────────────────────────────────
    def _saved_panel(self) -> QFrame:
        p = QFrame()
        p.setObjectName("glassPanel")
        pl = QVBoxLayout(p)
        pl.setContentsMargins(18, 16, 18, 14)
        pl.setSpacing(10)

        # Kepala: tajuk + chips tab.
        kepala = QWidget()
        kl = QHBoxLayout(kepala)
        kl.setContentsMargins(0, 0, 0, 0)
        kl.setSpacing(8)
        kiri = QWidget()
        kv = QVBoxLayout(kiri)
        kv.setContentsMargins(0, 0, 0, 0)
        kv.setSpacing(2)
        ek_sen = QLabel("SENARAI" if self._saved_tab == "simpan"
                        else "SEJARAH BACAAN")
        ek_sen.setObjectName("panelSection")
        kv.addWidget(ek_sen)
        sub = QLabel("Terjemahan di kiri  ·  Petikan teks Arab di kanan")
        sub.setObjectName("muted")
        kv.addWidget(sub)
        kl.addWidget(kiri, 1)

        self._saved_chip_btns = {}
        for kunci, label in (("simpan", "Tersimpan"),
                             ("baca", "Telah dibaca")):
            cb = QPushButton(label)
            cb.setCursor(Qt.PointingHandCursor)
            cb.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
            cb.setObjectName("filterChip_active" if kunci == self._saved_tab
                             else "filterChip")
            cb.clicked.connect(lambda _, k=kunci: self._pilih_tab_simpan(k))
            kl.addWidget(cb)
            self._saved_chip_btns[kunci] = cb
        pl.addWidget(kepala)

        # Kontena senarai (mengisi lebar panel).
        self._saved_container = QWidget()
        self._saved_list = QVBoxLayout(self._saved_container)
        self._saved_list.setContentsMargins(0, 0, 0, 0)
        self._saved_list.setSpacing(12)
        pl.addWidget(self._saved_container)
        return p

    def _pilih_tab_simpan(self, tab):
        if self._saved_tab == tab:
            return
        self._saved_tab = tab
        self._saved_filter_slug = None
        for k, b in self._saved_chip_btns.items():
            b.setObjectName("filterChip_active" if k == tab else "filterChip")
            b.style().unpolish(b)
            b.style().polish(b)
        self._render_saved()

    # ── isi senarai ────────────────────────────────────────────────────
    def _render_senarai_simpan(self):
        _clear(self._saved_list)
        if self._saved_tab == "baca":
            self._isi_sejarah()
        else:
            self._isi_bookmarks()
        self._laras_tinggi(self._tersimpan_sa)

    def _isi_bookmarks(self):
        item = [b for b in self.bookmarks
                if self._saved_filter_slug in (None, b.get("slug"))]
        item = sorted(item, key=lambda x: x.get("saved_at") or "",
                      reverse=True)
        if not item:
            self._saved_list.addWidget(empty_state(
                "⭐", "Belum ada hadis tersimpan",
                "Buka mana-mana hadis dan tekan Simpan."), 1)
            return
        for b in item:
            slug = b.get("slug")
            hid = b.get("id")
            h = {"collection": slug, "id": hid,
                 "arab": b.get("arab", ""), "melayu": b.get("melayu", ""),
                 "indonesia": b.get("indonesia", ""),
                 "book": b.get("book"), "nama_bab": b.get("nama_bab", "")}
            c = hadith_card_dwibahasa(
                h, b.get("kitab_name", ""), self.ar_scale,
                arabic_font=self.ar_font, tersimpan=True,
                papar_melayu=self._papar_melayu,
                tarikh_simpan=b.get("saved_at"))
            c.simpan_btn.clicked.connect(
                lambda _, cc=c, hh=h: self._toggle_simpan_kad(cc, hh))
            c._hid = hid
            c.clicked.connect(
                lambda s=slug, i=hid: self.open_by_ref(s, i, "saved"))
            self._saved_list.addWidget(c)
        self._saved_list.addStretch(1)

    def _isi_sejarah(self):
        hist = [e for e in read_history()
                if self._saved_filter_slug in (None, e.get("slug"))]
        hist = sorted(hist, key=lambda x: x.get("read_at") or "",
                      reverse=True)
        if not hist:
            self._saved_list.addWidget(empty_state(
                "📖", "Belum ada sejarah bacaan",
                "Buka mana-mana hadis — ia direkodkan di sini."), 1)
            return

        # Bar kawalan buang pukal.
        bar = QWidget()
        bl = QHBoxLayout(bar)
        bl.setContentsMargins(0, 0, 0, 0)
        bl.setSpacing(10)
        self._sejarah_all_chk = QCheckBox("Pilih semua")
        self._sejarah_all_chk.setCursor(Qt.PointingHandCursor)
        self._sejarah_all_chk.stateChanged.connect(self._sejarah_pilih_semua)
        bl.addWidget(self._sejarah_all_chk)
        bl.addStretch(1)
        self._sejarah_buang_btn = QPushButton("🗑  Buang dipilih (0)")
        self._sejarah_buang_btn.setObjectName("ghost")
        self._sejarah_buang_btn.setCursor(Qt.PointingHandCursor)
        self._sejarah_buang_btn.setEnabled(False)
        self._sejarah_buang_btn.clicked.connect(self._sejarah_buang_pilih)
        bl.addWidget(self._sejarah_buang_btn)
        self._saved_list.addWidget(bar)

        for e in hist:
            slug = e.get("slug")
            nid = e.get("n")
            h = self.api.get_hadis_by_id(slug, nid)
            if not h:
                continue
            h["collection"] = slug
            h["id"] = nid
            c = hadith_card_dwibahasa(
                h, COLLECTION_META.get(slug, {}).get("name", slug),
                self.ar_scale, arabic_font=self.ar_font,
                tersimpan=self._is_saved(slug, nid),
                papar_melayu=self._papar_melayu,
                tarikh_simpan=e.get("read_at"), tarikh_label="dibaca")
            c._hid = nid
            c.clicked.connect(
                lambda s=slug, i=nid: self.open_by_ref(s, i, "saved"))
            c.simpan_btn.hide()   # sejarah tiada butang Simpan
            chk = QCheckBox()
            chk.setCursor(Qt.PointingHandCursor)
            chk.stateChanged.connect(self._sejarah_kemas_buang)
            self._sejarah_checks.append((chk, slug, nid))
            row = QWidget()
            rl = QHBoxLayout(row)
            rl.setContentsMargins(0, 0, 0, 0)
            rl.setSpacing(10)
            rl.addWidget(chk, 0, Qt.AlignTop)
            rl.addWidget(c, 1)
            self._saved_list.addWidget(row)
        self._saved_list.addStretch(1)
        self._sejarah_kemas_buang()

    def _toggle_simpan_kad(self, card, h):
        """Toggle tanda buku terus dari kad (seperti _kitab_toggle_simpan).

        Bila dibuang, re-render untuk kemas kiraan sidebar + banner.
        """
        self._toggle_save(h)
        saved = self._is_saved(h.get("collection"), h.get("id"))
        card.simpan_btn.set_active(saved)
        if not saved:
            self._render_saved()

    # ── buang pukal sejarah ────────────────────────────────────────────
    def _sejarah_pilih_semua(self, state):
        for chk, _, _ in list(getattr(self, "_sejarah_checks", [])):
            try:
                chk.setChecked(state == Qt.Checked)
            except RuntimeError:
                continue
        self._sejarah_kemas_buang()

    def _sejarah_kemas_buang(self):
        btn = getattr(self, "_sejarah_buang_btn", None)
        if btn is None:
            return
        checks = getattr(self, "_sejarah_checks", [])
        k = 0
        for chk, _, _ in checks:
            try:
                if chk.isChecked():
                    k += 1
            except RuntimeError:
                continue
        btn.setText(f"🗑  Buang dipilih ({k})")
        btn.setEnabled(k > 0)
        all_chk = getattr(self, "_sejarah_all_chk", None)
        if all_chk is not None:
            total = len(checks)
            try:
                all_chk.setChecked(k == total and total > 0)
            except RuntimeError:
                pass

    def _sejarah_buang_pilih(self):
        for chk, slug, nid in list(getattr(self, "_sejarah_checks", [])):
            try:
                if chk.isChecked():
                    remove_reading(slug, nid)
            except RuntimeError:
                continue
        self._render_saved()

    # ── butang terapung ↑ (sama _kitab, Sesi 34) ──────────────────────
    def _kemas_butang_atas_tersimpan(self):
        b = getattr(self, "_tersimpan_top_btn", None)
        sa = getattr(self, "_tersimpan_sa", None)
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

    def _skrol_atas_lancar_tersimpan(self):
        bar = self._tersimpan_sa.verticalScrollBar()
        mula = bar.value()
        if mula <= 0:
            return
        t = getattr(self, "_top_timer_tersimpan", None)
        if t is not None:
            t.stop()
        t = QTimer(self)
        self._top_timer_tersimpan = t
        langkah = max(1, mula // 15)

        def _langkah():
            if t is not self._top_timer_tersimpan:
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
