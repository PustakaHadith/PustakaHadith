"""QThread pekerja — semua panggilan API/DB keluar dari thread UI.

Corak: cipta pekerja, sambung isyarat, simpan rujukan, mula.
Pemanggil MESTI simpan rujukan (cth. self._worker) atau Python akan
kutip sampah objek itu dan Qt akan crash.
"""

from __future__ import annotations

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt5.QtCore import QObject, QThread, pyqtSignal

from utils.bahasa import terjemah_ralat


class _Base(QThread):
    failed = pyqtSignal(str)

    def __init__(self, api, parent=None):
        super().__init__(parent)
        self.api = api
        self._cancelled = False

    def cancel(self):
        self._cancelled = True


class CollectionsWorker(_Base):
    done = pyqtSignal(list)

    def run(self):
        try:
            r = self.api.get_collections()
            if not self._cancelled:
                self.done.emit(r or [])
        except Exception as e:
            if not self._cancelled:
                self.failed.emit(terjemah_ralat(e))


class ListWorker(_Base):
    """Muat satu halaman hadis. Emit (senarai, meta, token).

    book/order/ids/exclude_ids: penapis halaman Senarai Hadis (26 Ogos)
    — dihantar terus ke get_hadis_list (DB tempatan sahaja).
    """
    done = pyqtSignal(list, dict, int)

    def __init__(self, api, slug, page, limit, lang=None, token=0, parent=None,
                 book=None, order: str = "asc", ids: list | None = None,
                 exclude_ids: list | None = None):
        super().__init__(api, parent)
        self.slug, self.page, self.limit, self.lang = slug, page, limit, lang
        self.token = token
        self.book, self.order = book, order
        self.ids, self.exclude_ids = ids, exclude_ids

    def run(self):
        try:
            r = self.api.get_hadis_list(self.slug, page=self.page,
                                        limit=self.limit, lang=self.lang,
                                        book=self.book, order=self.order,
                                        ids=self.ids,
                                        exclude_ids=self.exclude_ids)
            if not self._cancelled:
                self.done.emit(r.get("hadis", []), r.get("meta", {}), self.token)
        except Exception as e:
            if not self._cancelled:
                self.failed.emit(terjemah_ralat(e))


class SearchWorker(_Base):
    done = pyqtSignal(list, dict, int)

    def __init__(self, api, query, slug, page, limit, lang=None, token=0, parent=None):
        super().__init__(api, parent)
        self.query, self.slug = query, slug
        self.page, self.limit, self.lang = page, limit, lang
        self.token = token

    def run(self):
        try:
            r = self.api.search_hadis(self.query, slug=self.slug, page=self.page,
                                      limit=self.limit, lang=self.lang)
            if not self._cancelled:
                self.done.emit(r.get("hadis", []), r.get("meta", {}), self.token)
        except Exception as e:
            if not self._cancelled:
                self.failed.emit(terjemah_ralat(e))


class HadithWorker(_Base):
    """Ambil satu hadis. Emit (hadis|{}, token)."""
    done = pyqtSignal(dict, int)

    def __init__(self, api, slug, hid, lang=None, token=0, parent=None):
        super().__init__(api, parent)
        self.slug, self.hid, self.lang = slug, hid, lang
        self.token = token

    def run(self):
        try:
            h = self.api.get_hadis_by_id(self.slug, self.hid, lang=self.lang)
            if not self._cancelled:
                self.done.emit(h or {}, self.token)
        except Exception as e:
            if not self._cancelled:
                self.failed.emit(terjemah_ralat(e))


class RandomWorker(_Base):
    done = pyqtSignal(dict)

    def run(self):
        try:
            r = self.api.get_random_hadis(count=1)
            if not self._cancelled:
                self.done.emit(r[0] if r else {})
        except Exception as e:
            if not self._cancelled:
                # Semua worker lain guna `terjemah_ralat(e)` supaya ralat
                # dipapar dalam Bahasa Melayu; RandomWorker tertinggal
                # guna `str(e)` mentah -- butang Rawak sahaja yang boleh
                # memapar mesej ralat Inggeris kepada pengguna.
                self.failed.emit(terjemah_ralat(e))


class SemanticWorker(_Base):
    """Carian semantik (makna) — QThread.

    Dipindah dari `ui/pages_carian.py` (13 Ogos 2026) supaya mewarisi
    `_Base` dan memperoleh `cancel()`. Sebelum ini ditakrif SEBAGAI
    kelas dalaman method `_run_semantic_search()`, warisi `QThread`
    terus tanpa `cancel()` -- `app_qt.py::closeEvent()` terpaksa jaga
    `hasattr(w, "cancel")` khas untuknya (rujuk PERUBAHAN_7OGOS.md,
    "Pepijat kedua": AttributeError semasa Qt meruntuhkan tetingkap
    muncul sebagai fail-fast 0xC0000409).

    `api` tidak digunakan (carian semantik panggil terus
    `core.semantic_search`, bukan lapisan HadisAPI) tetapi kekal
    sebagai parameter supaya tandatangan `_Base.__init__` konsisten.

    Isyarat baharu (Lazy Loading):
    - `model_loading_started(int token)` -- dipancar SEBELUM muat model
      (pada carian makna pertama). UI boleh papar "Memuatkan AI...".
    """
    done = pyqtSignal(object, int)
    failed = pyqtSignal(str, int)
    model_loading_started = pyqtSignal(int)  # token

    def __init__(self, query, top_k=20, min_score=0.6, token=0, parent=None):
        super().__init__(api=None, parent=parent)
        self.query, self.top_k, self.min_score = query, top_k, min_score
        self.token = token

    def run(self):
        try:
            # Semak sama ada model perlu dimuat (lazy load)
            from core.semantic_search import _model
            if _model is None:
                self.model_loading_started.emit(self.token)
            from core.semantic_search import semantic_search
            results = semantic_search(
                self.query, top_k=self.top_k, min_score=self.min_score)
            if not self._cancelled:
                self.done.emit(results, self.token)
        except Exception as e:
            if not self._cancelled:
                self.failed.emit(terjemah_ralat(e), self.token)


class PreloadWorker(QThread):
    """Pra-muat model + indeks carian makna dalam QThread background.

    MENGAPA QThread DAN BUKAN THREAD UTAMA
    --------------------------------------
    Diukur (PERUBAHAN_7OGOS.md):

        pra-muat thread utama -> encode QThread  = CRASH 0xC0000409
        pra-muat QThread      -> encode QThread  = OK

    Memuat dalam thread utama juga membekukan UI ~30s (import torch ~21s
    + muat model ~5s).

    Dimulakan selepas `CollectionsWorker` selesai supaya tetingkap sudah
    kelihatan. Pemanggil MESTI simpan rujukan (cth. `self._preload`).
    """

    siap = pyqtSignal(bool)          # True = model sedia, False = dilangkau
    kemajuan = pyqtSignal(str)       # fasa semasa (untuk skrin pemula)

    def run(self):
        try:
            self.kemajuan.emit("Memeriksa indeks carian makna…")
            from core.semantic_search import is_index_ready
            if not is_index_ready():
                self.siap.emit(False)
                return
            from core import semantic_search as ss
            # Import sentence_transformers + muat model = ~24s (import
            # ST ~19s adalah had persekitaran). Isyarat fasa membolehkan
            # skrin pemula memaparkan kemajuan supaya apl tidak kelihatan
            # beku.
            self.kemajuan.emit("Memuatkan model carian makna…")
            ss._load_model()
            self.kemajuan.emit("Memuatkan indeks carian…")
            ss._load_index()
            self.kemajuan.emit("Menetapkan pemetaan hadis…")
            ss._load_id_map()
            self.siap.emit(True)
        except Exception:
            # Kegagalan pra-muat TIDAK fatal: `SemanticWorker` akan cuba
            # memuat sendiri kemudian (dilindungi oleh `_model_lock`).
            self.siap.emit(False)
