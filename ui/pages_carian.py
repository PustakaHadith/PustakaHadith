"""Halaman Carian (keyword + semantik) — mixin PustakaApp (Sesi 30).

Dipisahkan dari `ui/app_qt.py`. Kelas `PagesCarian` menyediakan kaedah
halaman carian: bar carian, lompat pantas, carian gabungan (FTS5
keyword + semantik AI), draf jawapan dan paparan hasil. Digabungkan ke
`PustakaApp` melalui MRO: `class PustakaApp(PagesKitab, PagesCarian,
QMainWindow)`.

PENTING — tema: modul ini import WARNA dari `ui.theme`
(AMBER_BG/AMBER_TEXT/AMBER_BORDER) untuk lencana amaran. Ia MESTI
didaftar dalam `_THEMED_MODULES` (ui/theme.py) supaya `apply_theme()`
menyalin nilai terkini ke ruang namanya semasa tukar tema.

GANDINGAN RENTAS MIXIN: modul ini TIDAK berdiri sendiri — `_hantar_carian`
memanggil `_buka_hadis_terus` (carian khusus kitab + nombor terus ke
butiran, Sesi 38) yang memanggil `_sahkan_lompat` yang tinggal dalam
`PagesKitab`. Mesti digabungkan bersama:
`PustakaApp(PagesKitab, PagesCarian, QMainWindow)`.
"""

from __future__ import annotations

import time

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import (
    QHBoxLayout, QLabel, QPushButton, QSizePolicy, QVBoxLayout, QWidget,
)

from ui.helpers import _clear, _parse_lompat
from ui.pages import Hero, Pager, SearchBar, empty_state
from ui.deklarasi import SEMAKHADIS_URL
from ui.theme import (
    AMBER_BG, AMBER_BORDER, AMBER_TEXT, COLLECTION_META, TEXT_MUTED,
    ada_latar_imej,
)
from ui.widgets import (
    BackgroundCanvas, attach_copy_menu, hadith_card_dwibahasa, make_scroll,
    text_browser,
)
from ui.workers import SearchWorker, SemanticWorker


class PagesCarian:
    # ── HALAMAN: Carian ──────────────────────────────────────────────
    def _page_search(self):
        # Latar: BackgroundCanvas (glob AQUA / warna pepejal tema lain) —
        # pola sama Utama/rak/kitab. Skrol berlaku pada QScrollArea TELUS
        # di dalamnya supaya glob kekal TETAP (parallax) semasa skrol.
        kanvas = BackgroundCanvas()
        self.stack.addWidget(kanvas)
        sa = make_scroll(kanvas)
        sa.setObjectName("homeScroll")
        self._search_sa = sa

        # Butang terapung "↑ ke atas" (Sesi 34) — sama seperti halaman
        # kitab: kelihatan bila pengguna skrol ke bawah senarai hasil;
        # klik untuk kembali ke atas dengan animasi lancar. Guna
        # objectName "backTop" (QSS dalam theme.py) yang sama supaya
        # gaya konsisten merentas kedua-dua halaman.
        if getattr(self, "_top_timer_carian", None) is not None:
            self._top_timer_carian.stop()
        self._search_top_btn = QPushButton("↑")
        self._search_top_btn.setObjectName("backTop")
        self._search_top_btn.setToolTip("Ke atas — hadis pertama")
        self._search_top_btn.setCursor(Qt.PointingHandCursor)
        self._search_top_btn.setFixedSize(44, 44)
        self._search_top_btn.setParent(sa)
        self._search_top_btn.clicked.connect(self._skrol_atas_lancar_carian)
        self._search_top_btn.hide()
        sa.verticalScrollBar().valueChanged.connect(
            self._kemas_butang_atas_carian)
        _orig_resize = sa.resizeEvent

        def _on_resize(e):
            _orig_resize(e)
            self._kemas_butang_atas_carian()

        sa.resizeEvent = _on_resize

        body = QWidget()
        body.setObjectName("homeBody")
        sa.setWidget(body)
        bl = QVBoxLayout(body)
        bl.setContentsMargins(0, 0, 0, 16)
        bl.setSpacing(0)

        hero = Hero("Pencarian Hadis", compact=True)
        # Aqua Glass: hero telus supaya glob tembus (hanya teks atas glob).
        if ada_latar_imej():
            hero.setStyleSheet(
                "QFrame#hero { background: transparent; border: none; }")
        self.search_bar = SearchBar("Cari hadis… (cth. bukhari 433, B433)")
        self.search_bar.setMaximumWidth(900)
        w = QWidget()
        wl = QHBoxLayout(w)
        wl.setContentsMargins(0, 0, 0, 0)
        wl.addStretch(1)
        wl.addWidget(self.search_bar, 20)
        wl.addStretch(1)
        hero.body.addWidget(w)
        bl.addWidget(hero)

        attach_copy_menu(self.search_bar.input)
        self.search_bar.btn.clicked.connect(self._hantar_carian)
        self.search_bar.input.returnPressed.connect(self._hantar_carian)
        if self.search_bar.chips:
            self.search_bar.chips.changed.connect(
                lambda _: self._do_search(1) if self._search_q else None)

        # Lajur kandungan berpusat (TELUS — biar glob AQUA kelihatan di
        # belakang). Tidak guna centered_column() kerana widgetnya
        # ber-objectName "page" (PAGE_BG pepejal) yang menutup glob.
        col = QWidget()
        col.setObjectName("homeBody")
        col.setMaximumWidth(960)
        col.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        cl = QVBoxLayout(col)
        cl.setContentsMargins(0, 18, 0, 0)
        cl.setSpacing(0)
        # Baris togol kaedah carian (Kata kunci / Makna / Kedua-dua).
        cl.addWidget(self._bina_togol_kaedah())
        # Baris status: teks hasil + indikator jam berputar 🕐→🕛 semasa
        # carian berjalan. Emoji (berwarna sendiri) -- tiada import warna,
        # jadi tiada keperluan pendaftaran _THEMED_MODULES.
        status_baris = QWidget()
        sl = QHBoxLayout(status_baris)
        sl.setContentsMargins(0, 0, 0, 0)
        sl.setSpacing(8)
        self.search_info = QLabel("")
        self.search_info.setObjectName("muted")
        self.search_info.setSizePolicy(QSizePolicy.Preferred,
                                       QSizePolicy.Fixed)
        sl.addWidget(self.search_info)
        self._carian_sibuk = QLabel("🕐")
        # Saiz lebih besar daripada teks status (12px) supaya kelihatan.
        self._carian_sibuk.setStyleSheet("font-size: 16px;")
        self._carian_sibuk.hide()
        # Jam berputar 🕐→🕛 (QTimer 120ms) supaya jelas carian berjalan.
        self._jam = ["🕐", "🕑", "🕒", "🕓", "🕔", "🕕",
                     "🕖", "🕗", "🕘", "🕙", "🕚", "🕛"]
        self._jam_i = 0
        # Bila tema bertukar, _page_search dibina semula -- hentikan timer
        # lama supaya tidak memutar label baharu secara serentak.
        if getattr(self, "_carian_timer", None) is not None:
            self._carian_timer.stop()
        self._carian_timer = QTimer(self)
        self._carian_timer.setInterval(120)
        self._carian_timer.timeout.connect(self._putar_jam)
        sl.addWidget(self._carian_sibuk)
        sl.addStretch(1)
        cl.addWidget(status_baris)

        self._search_container = QWidget()
        self._search_list = QVBoxLayout(self._search_container)
        self._search_list.setContentsMargins(0, 0, 0, 0)
        self._search_list.setSpacing(10)
        cl.addWidget(self._search_container)

        self._search_pager = Pager(lambda p: self._do_search(p))
        cl.addWidget(self._search_pager)
        # TIADA addStretch: struktur sama dengan _page_kitab. `col`
        # (centered_column) sudah Maximum menegak -- ia mengisi viewport
        # bila kandungan pendek, dan stretch hanya mencipta kawasan skrol
        # kosong di bawah hasil carian yang panjang.
        # Pusat menegak lajur kandungan; glob kekal kelihatan di sisi.
        wrap = QWidget()
        wl2 = QHBoxLayout(wrap)
        wl2.setContentsMargins(0, 0, 0, 0)
        wl2.addStretch(1)
        wl2.addWidget(col, 0, Qt.AlignTop)
        wl2.addStretch(1)
        bl.addWidget(wrap)

        # Kanvas perlu mengisi ruang: letakkan scroll-area telus di dalamnya.
        vl = QVBoxLayout(kanvas)
        vl.setContentsMargins(0, 0, 0, 0)
        vl.addWidget(sa)

        self._search_list.addWidget(
            empty_state("🔍", "Cari hadis",
                        "Masukkan kata kunci untuk mencari dalam 62,169 hadis."), 1)

    def _bina_togol_kaedah(self) -> QWidget:
        """Baris togol kaedah carian: Kata kunci / Makna / Kedua-dua.

        Pilihan disimpan ke `carian_mod` (user_settings.json) dan dibaca
        semula bila halaman dibina semula (tukar tema). Lalai "kedua".
        """
        row = QWidget()
        rl = QHBoxLayout(row)
        rl.setContentsMargins(0, 0, 0, 0)
        rl.setSpacing(8)
        label = QLabel("Kaedah carian")
        label.setObjectName("muted")
        rl.addWidget(label)
        self._mod_chips = {}
        for val, txt in (("kata", "Kata kunci"), ("makna", "Makna"),
                         ("kedua", "Kedua-dua")):
            b = QPushButton(txt)
            b.setObjectName("filterChip")
            b.setCursor(Qt.PointingHandCursor)
            b.clicked.connect(lambda _, v=val: self._set_mod_carian(v))
            self._mod_chips[val] = b
            rl.addWidget(b)
        rl.addStretch(1)
        self._kemas_mod_carian()
        return row

    def _kemas_mod_carian(self):
        """Tanda butang aktif ikut `carian_mod` (unpolish/polish = segar)."""
        aktif = self.settings.get("carian_mod", "kedua")
        for v, b in self._mod_chips.items():
            b.setObjectName("filterChip_active" if v == aktif else "filterChip")
            b.style().unpolish(b)
            b.style().polish(b)

    def _set_mod_carian(self, v: str):
        """Tukar kaedah carian + kekalkan pilihan dalam tetapan."""
        if self.settings.get("carian_mod", "kedua") == v:
            return
        self.settings["carian_mod"] = v
        try:
            from ui.pages_tetapan import SETTINGS, _write_json
            _write_json(SETTINGS, self.settings)
        except Exception:
            pass
        self._kemas_mod_carian()
        # Cari semula dengan mod baharu bila ada query aktif.
        if getattr(self, "_search_q", ""):
            self._do_search(1)

    def _tambah_kad_carian(self, h, slug, hid, lay):
        """Tambah satu kad dwibahasa ke layout hasil carian.

        `h` dinormalisasi (salinan) supaya `id`/`collection` wujud untuk
        kad, simpan (🔖) dan buka butiran. Kitab ditunjukkan dalam meta kad.
        """
        h = dict(h)
        h.setdefault("collection", slug)
        h.setdefault("id", hid)
        name = COLLECTION_META.get(slug, {}).get("name", slug)
        c = hadith_card_dwibahasa(
            h, name, self.ar_scale, arabic_font=self.ar_font,
            tersimpan=self._is_saved(slug, hid),
            papar_melayu=self._papar_melayu)
        c._hid = hid
        c.clicked.connect(lambda hh=h: self.open_detail(hh, "search"))
        c.simpan_clicked.connect(
            lambda _, hh=h, cc=c, s=slug, i=hid:
            self._carian_toggle_simpan(hh, cc, s, i))
        lay.addWidget(c)

    def _carian_toggle_simpan(self, h, card, slug, hid):
        """Butang 🔖 pada kad carian — toggle tanda buku, segar butang."""
        self._toggle_save(h)
        simpan = card.simpan_btn
        simpan.setObjectName(
            "simpanChip_aktif" if self._is_saved(slug, hid) else "simpanChip")
        simpan.style().unpolish(simpan)
        simpan.style().polish(simpan)

    def _hantar_carian(self):
        """Hantar carian dari bar carian (butang/Enter).

        Sebelum carian biasa, cuba tafsir sebagai lompat terus: 'bukhari
        433' atau '433' (chip kitab terpilih, atau kitab terakhir dibuka).
        Carian KHUSUS seperti ini membuka butiran hadis TERUS (Sesi 38)
        — pengguna mahukan hadis itu, bukan senarai. Carian umum (cth.
        'hukum riba') kekal memaparkan senarai hasil carian.
        """
        q = self.search_bar.text()
        if not q:
            return
        j = _parse_lompat(q, default_slug=self.search_bar.slug()
                          or self._kitab_slug)
        if j:
            slug, n = j
            self._buka_hadis_terus(slug, n)
            return
        self._do_search(1)

    def _buka_hadis_terus(self, slug: str, n: int, dari: str = "search"):
        """Buka butiran hadis No. n dalam slug TERUS, tanpa senarai.

        Pintasan '433' (halaman Utama atau Carian): pengguna mahukan
        hadis itu, bukan senarai kitab. Sahkan julat dahulu (murah),
        beri toast maklum balas, kemudian muat dan buka butiran. Butang
        Kembali menuju ke halaman `dari` ('home' atau 'search').
        """
        nama = COLLECTION_META.get(slug, {}).get("name", slug)
        r = self._sahkan_lompat(slug, n, nama)
        if r is None:
            return
        self._detail_from = dari
        # Toast "Membuka…" kekal sehingga butiran dibuka (open_by_ref
        # menyembunyikannya) — muatan hadis asynchronous, jadi tempoh
        # tetap boleh terlepas sebelum butiran siap dipapar. Tetapi
        # untuk muatan pantas (DB tempatan), ia tidak boleh hilang
        # serta-merta: simpan masa mula supaya open_by_ref menjamin
        # minimum 1800ms paparan (pengguna sempat baca maklum balas).
        self._buka_toast_t0 = time.monotonic()
        self.toast.show_msg(f"📖 Membuka {nama} No. {n}…", 0)
        self.open_by_ref(slug, n, dari)

    def _do_search(self, page=1):
        q = self.search_bar.text()
        if not q:
            return
        self._search_q = q
        self._search_slug = self.search_bar.slug()
        self._search_page = page
        self._tok += 1
        tok = self._tok

        mod = self.settings.get("carian_mod", "kedua")
        self._sem_res = None
        self._kw_res = None
        self._kw_meta = {}
        self._sem_gagal = None
        _clear(self._search_list)
        self.search_info.setText(f"Mencari '{q}'…")
        self._carian_sibuk.show()
        self._carian_timer.start()

        # Kaedah carian (togol 3-mod):
        #   kata  -> hanya SearchWorker (FTS5), tiada draf AI
        #   makna -> hanya SemanticWorker (draf + hasil makna)
        #   kedua -> kedua-dua serentak (gelagat asal)
        # Enjin yang dilangkau ditetapkan senarai kosong serta-merta supaya
        # _tampal_gabungan tetap tamat (menunggu KEDUA-dua hasil).
        if mod in ("kata", "kedua"):
            kw_worker = self._run(
                SearchWorker(self.api, q, self._search_slug, page,
                             self.per_page(), self.lang_param, tok),
                self._on_search,
                # SearchWorker.failed = pyqtSignal(str) -- satu argumen,
                # jadi tok ditangkap dalam lambda (bukan disambung terus).
                on_fail=lambda m: self._on_search_failed(m, tok))
            # Tampal paparan hanya selepas worker benar-benar tamat
            # (finished), BUKAN dari callback done -- mengelak akses
            # serentak ke model torch (0xC0000409) semasa QThread masih
            # menamatkan run().
            kw_worker.finished.connect(lambda: self._tampal_gabungan(tok))
        else:
            self._kw_res = []
            self._kw_meta = {}

        if mod in ("makna", "kedua"):
            self._run_semantic_search(q, tok)
        else:
            self._sem_res = []

    def _run_semantic_search(self, query: str, tok: int):
        """Jalankan carian semantik di background thread (Lazy Loading).

        `SemanticWorker` kini di `ui/workers.py` (13 Ogos 2026) --
        mewarisi `_Base` dan `cancel()`, bukan lagi kelas dalaman
        `QThread` tanpa `cancel()`. Rujuk komen kelas dalam workers.py
        untuk sebab pemindahan (PERUBAHAN_7OGOS.md, "Pepijat kedua").

        Signal baharu: `model_loading_started(int token)` dipancar
        SEBELUM muat model (pada carian makna pertama). UI papar
        "Memuatkan AI..." inline.
        """
        worker = SemanticWorker(query, top_k=20, min_score=0.6, token=tok)
        worker.done.connect(lambda results, t: self._on_semantic_search(results, t))
        worker.failed.connect(lambda msg, t: self._on_semantic_failed(msg, t))
        # Model loading indicator (Lazy Loading)
        worker.model_loading_started.connect(lambda t: self._on_model_loading(t))
        self._workers.append(worker)
        worker.finished.connect(lambda: self._workers.remove(worker)
                                if worker in self._workers else None)
        # Papar gabungan hanya selepas run() QThread pulang sepenuhnya --
        # bukan dari callback done (yang masih dalam run() worker).
        worker.finished.connect(lambda: self._tampal_gabungan(tok))
        worker.start()

    def _on_semantic_search(self, results, tok):
        if tok != self._tok:
            return
        self._sem_res = results or []

    def _on_semantic_failed(self, msg, tok):
        if tok != self._tok:
            return
        self._sem_res = []
        self._sem_gagal = msg

    def _on_model_loading(self, tok):
        """Dipanggil SEBELUM model dimuat (Lazy Loading) — papar inline."""
        if tok != self._tok:
            return
        self._carian_sibuk.setText("🤖 Memuatkan model AI…")
        self._carian_sibuk.show()
        if not self._carian_timer.isActive():
            self._carian_timer.start(120)

    def _on_search(self, items, meta, tok):
        if tok != self._tok:
            return
        self._kw_res = items or []
        self._kw_meta = meta or {}

    def _on_search_failed(self, msg, tok):
        """Carian kata kunci gagal -- tandakan selesai supaya paparan
        gabungan boleh tamat dan indikator jam disembunyikan (bukan
        tersangkut selama-lamanya pada \"Mencari…\"). Simetri dengan
        `_on_semantic_failed` yang menetapkan `_sem_res = []`.
        """
        if tok != self._tok:
            return
        self._kw_res = []
        self._on_error(msg)

    def _putar_jam(self):
        """Putar emoji jam 🕐→🕛 (120ms) semasa carian berjalan.

        Pengawal `isVisible()`: timer lama yang masih berjalan selepas
        pembinaan semula tema tidak mengemas kini label baharu secara
        serentak (jam tidak berputar laju dua kali ganda).
        """
        if not self._carian_sibuk.isVisible():
            return
        self._jam_i = (self._jam_i + 1) % len(self._jam)
        self._carian_sibuk.setText(self._jam[self._jam_i])

    def _kemas_butang_atas_carian(self):
        """Tunjuk/sembunyi butang ↑ halaman Carian ikut skrol (Sesi 34).

        Corak sama seperti _kemas_butang_atas pada halaman kitab: butang
        hanya berguna bila senarai melebihi viewport dan pengguna sudah
        skrol ke bawah (melebihi 250px). Kedudukan dikira semula pada
        setiap skrol dan ubah saiz tetingkap.
        """
        b = getattr(self, "_search_top_btn", None)
        sa = getattr(self, "_search_sa", None)
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

    def _skrol_atas_lancar_carian(self):
        """Skrol lancar ke atas senarai hasil — animasi QTimer ~250ms.

        Corak sama seperti _skrol_atas_lancar pada halaman kitab:
        langkah mengecil supaya pergerakan kelihatan perlahan berhampiran
        sasaran; timer disimpan pada `self` supaya panggilan kedua
        menghentikan animasi pertama.
        """
        bar = self._search_sa.verticalScrollBar()
        mula = bar.value()
        if mula <= 0:
            return
        t = getattr(self, "_top_timer_carian", None)
        if t is not None:
            t.stop()
        t = QTimer(self)
        self._top_timer_carian = t
        langkah = max(1, mula // 15)

        def _langkah():
            if t is not self._top_timer_carian:
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

    def _tampal_gabungan(self, tok):
        if tok != self._tok:
            return
        if self._sem_res is None or self._kw_res is None:
            return
        _clear(self._search_list)
        self._carian_sibuk.hide()
        self._carian_timer.stop()

        mod = self.settings.get("carian_mod", "kedua")
        sem = self._sem_res
        kw = self._kw_res
        meta = self._kw_meta
        if getattr(self, "_sem_gagal", None):
            self.toast.show_msg(f"⚠️ Carian makna: {self._sem_gagal}", 4000)
            self._sem_gagal = None
        scope = ""
        if self._search_slug:
            scope = f" dalam {COLLECTION_META[self._search_slug]['name']}"

        # Draf jawapan AI di atas (jika ada hasil semantik). Mod "kata"
        # melangkau enjin semantik -- tiada draf dipapar.
        if sem:
            from core.draft_answer import compose_draft_answer
            draft = compose_draft_answer(self._search_q, self.api,
                                         top_k=10, min_score=0.6,
                                         semantic_results=sem)
            # Bilangan kata: bila fallback OR, jumlah itu padanan LONGGAAR
            # (mana-mana satu perkataan), bukan padanan tepat SEMUA --
            # paparkan jelas supaya pengguna tidak salah faham.
            n_kata = meta.get("total", len(kw))
            if meta.get("fallback"):
                kata = f"{n_kata:,} padanan kata longgar"
            else:
                kata = f"{n_kata:,} padanan kata"
            self.search_info.setText(
                f"🤖 '{self._search_q}'{scope} — "
                f"{len(sem)} padanan makna + {kata}")
            # `markdown=True`: draf ditulis dalam Markdown (`**tebal**`).
            # Tanpa ia, penanda dipapar mentah kepada pengguna.
            draft_widget = text_browser(draft["draft_answer"], markdown=True)
            self._search_list.addWidget(draft_widget)

            # Kes "hukum riba": carian keyword (FTS5 AND semua perkataan)
            # pulang 0 hasil walaupun setiap perkataan wujud secara
            # berasingan. Beritahu pengguna mengapa kad keyword kosong dan
            # bawa perhatian ke hasil AI yang ada di bawah. Hanya relevan
            # bila enjin keyword turut dijalankan (mod kata/kerja).
            if mod in ("kata", "kedua") and not kw and not meta.get("total"):
                nota = QLabel(
                    "ℹ️ Tiada padanan kata kunci yang mengandungi SEMUA "
                    f"perkataan '{self._search_q}'. Padanan makna (AI) di "
                    "bawah dicari ikut maksud — perkataan hadis boleh "
                    "berbeza daripada soalan anda.")
                nota.setWordWrap(True)
                # Lencana AMBER (latar gelap + teks amber) — kontras baik
                # dalam KEDUA-DUA tema; teks amber sahaja pudar pada tema
                # terang. Corak sama seperti amaran fon (line ~1835).
                nota.setStyleSheet(
                    f"background-color: {AMBER_BG}; color: {AMBER_TEXT};"
                    f"border: 1px solid {AMBER_BORDER}; border-radius: 8px;"
                    f"padding: 10px; font-size: 12px;")
                self._search_list.addWidget(nota)
        else:
            total = meta.get("total", len(kw))
            if meta.get("fallback"):
                self.search_info.setText(
                    f"'{self._search_q}'{scope} — {total:,} padanan kata "
                    "longgar (tiada hadis mengandungi SEMUA perkataan)")
            else:
                self.search_info.setText(
                    f"'{self._search_q}'{scope} — {total:,} hadis ditemui")

        # Fallback OR (v1.2): FTS5 AND pulang 0 hasil untuk kes "hukum riba"
        # walaupun setiap perkataan wujud berasingan. Bila fallback aktif,
        # hasil kata di bawah mengandungi MANA-MANA satu perkataan, bukan
        # SEMUA — beritahu pengguna supaya mereka tidak keliru. Hanya
        # untuk mod yang menjalankan enjin keyword (kata/kerja).
        if mod in ("kata", "kedua") and meta.get("fallback") and kw:
            nota = QLabel(
                "ℹ️ Carian kata kunci longgar: tiada hadis mengandungi SEMUA "
                f"perkataan '{self._search_q}'. Hasil kata kunci di bawah "
                "mengandungi mana-mana satu perkataan — padanan makna (AI) "
                "mungkin lebih tepat.")
            nota.setWordWrap(True)
            nota.setStyleSheet(
                f"background-color: {AMBER_BG}; color: {AMBER_TEXT};"
                f"border: 1px solid {AMBER_BORDER}; border-radius: 8px;"
                f"padding: 10px; font-size: 12px;")
            self._search_list.addWidget(nota)

        # Kad hasis dwibahasa (terjemahan kiri, Arab kanan): semantik
        # dahulu (paling relevan ikut makna), dedupe, kemudian keyword
        # yang tidak bertindih.
        seen = set()
        for r in sem:
            slug, hid = r["collection"], r["hadis_id"]
            key = (slug, hid)
            if key in seen:
                continue
            seen.add(key)
            h = self.api.get_hadis_by_id(slug, hid)
            if h:
                self._tambah_kad_carian(h, slug, hid, self._search_list)

        # Kemudian kad keyword yang tidak bertindih dengan semantik
        for h in kw:
            slug = h.get("collection", "")
            # search_hadis pulang `id` (bukan `hadis_id`) — guna mana-mana
            # yang ada supaya penapis dedupe tidak melanggar hasil sekitar
            # satu koleksi (bug: hadis_id sentiasa None -> 1 kad/koleksi).
            hid = h.get("hadis_id") or h.get("id")
            key = (slug, hid)
            if key in seen:
                continue
            seen.add(key)
            self._tambah_kad_carian(h, slug, hid, self._search_list)

        if not seen:
            self._search_list.addWidget(
                empty_state("🔍", "Tiada hasil",
                            f"Tiada hadis sepadan '{self._search_q}'{scope}."))
            # Deklarasi (Sesi 54): tiada padanan dalam 9 kitab ini --
            # pautan ke SemakHadis.com tepat pada masanya untuk hadis
            # yang beredar (mungkin bukan daripada koleksi ini).
            pautan = QLabel(
                "Tiada hadis sepadan dalam 9 kitab ini. Hadis yang anda "
                "cari mungkin bukan daripada koleksi ini — "
                f"<a href=\"{SEMAKHADIS_URL}\">semak di SemakHadis.com</a>")
            pautan.setWordWrap(True)
            pautan.setTextFormat(Qt.RichText)
            pautan.setOpenExternalLinks(True)
            pautan.setTextInteractionFlags(Qt.TextBrowserInteraction)
            pautan.setAlignment(Qt.AlignCenter)
            pautan.setStyleSheet(
                f"font-size: 12px; color: {TEXT_MUTED}; "
                f"a {{ color: {AMBER_TEXT}; }}")
            self._search_list.addWidget(pautan)
            self._search_pager.set_state(1, 1)
            return
        self._search_pager.set_state(meta.get("current_page", 1),
                                     meta.get("last_page", 1))
        self._search_sa.verticalScrollBar().setValue(0)
        self._laras_tinggi(self._search_sa)
