#!/usr/bin/env python3
"""PustakaHadith — entry point (PyQt5)."""
import ctypes
import ctypes.wintypes
import multiprocessing
import os
import shutil
import sys
import traceback

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)

_DLL_RUNTIME = (
    "concrt140.dll", "msvcp140.dll", "msvcp140_1.dll",
    "msvcp140_2.dll", "vcruntime140.dll", "vcruntime140_1.dll",
)
_MINIMA_MINOR = 40


def _versi_fail(laluan: str):
    try:
        ver = ctypes.windll.version
        saiz = ver.GetFileVersionInfoSizeW(laluan, None)
        if not saiz:
            return None
        buf = ctypes.create_string_buffer(saiz)
        if not ver.GetFileVersionInfoW(laluan, 0, saiz, buf):
            return None
        ptr = ctypes.c_void_p()
        panjang = ctypes.wintypes.UINT()
        if not ver.VerQueryValueW(buf, "\\", ctypes.byref(ptr),
                                  ctypes.byref(panjang)):
            return None
        if not panjang.value:
            return None

        class _FFI(ctypes.Structure):
            _fields_ = [
                ("dwSignature", ctypes.wintypes.DWORD),
                ("dwStrucVersion", ctypes.wintypes.DWORD),
                ("dwFileVersionMS", ctypes.wintypes.DWORD),
                ("dwFileVersionLS", ctypes.wintypes.DWORD),
            ]

        info = ctypes.cast(ptr, ctypes.POINTER(_FFI)).contents
        return (info.dwFileVersionMS >> 16, info.dwFileVersionMS & 0xFFFF)
    except Exception:
        return None


def _perlu_alih(versi) -> bool:
    if versi is None:
        return False
    major, minor = versi
    return major == 14 and minor < _MINIMA_MINOR


def _baik_pulih_dll_qt_torch(senyap: bool = False) -> int:
    if sys.platform != "win32":
        return 0

    def _lapor(msg):
        if not senyap:
            print(f"[dll] {msg}", file=sys.stderr)

    try:
        import site
        calon = []
        for asas in site.getsitepackages() + [site.getusersitepackages()]:
            laluan = os.path.join(asas, "PyQt5", "Qt5", "bin")
            if os.path.isdir(laluan):
                calon.append(laluan)
        if not calon:
            return 0
    except Exception as e:
        _lapor(f"tidak dapat mencari site-packages: {e}")
        return 0

    bak = os.path.join(os.environ.get("TEMP", os.path.expanduser("~")),
                       "qt_dll_lama")
    dialih = 0
    for qt_bin in calon:
        for nama in _DLL_RUNTIME:
            src = os.path.join(qt_bin, nama)
            if not os.path.isfile(src):
                continue
            versi = _versi_fail(src)
            if not _perlu_alih(versi):
                continue
            try:
                os.makedirs(bak, exist_ok=True)
                shutil.move(src, os.path.join(bak, nama))
                dialih += 1
            except Exception:
                pass
    return dialih


_baik_pulih_dll_qt_torch()

from PyQt5.QtGui import QIcon                 # noqa: E402
from PyQt5.QtWidgets import QApplication      # noqa: E402
from PyQt5.QtCore import QTimer              # noqa: E402

from ui.app_qt import PustakaApp              # noqa: E402


def main():
    # Wajib untuk binaan frozen (PyInstaller) — torch/sentence-transformers
    # mungkin menggunakan multiprocessing (INSTALLER.md §6).
    multiprocessing.freeze_support()

    if sys.platform == "win32":
        try:
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
                "PustakaHadith.App")
        except Exception:
            pass

    app = QApplication(sys.argv)
    app.setApplicationName("PustakaHadith")
    app.setOrganizationName("PustakaHadith")
    app.setQuitOnLastWindowClosed(False)

    ico = os.path.join(BASE, "app.ico")
    if os.path.exists(ico):
        app.setWindowIcon(QIcon(ico))

    from ui.disclaimer import papar_disclaimer    # noqa: E402

    # STEP 1: Disclaimer DULU — wajib baca sebelum guna aplikasi.
    # exec_() blok sehingga "Faham" diklik.
    papar_disclaimer()

    # STEP 2: Buka tetingkap utama LANGSUNG (Lazy Loading).
    # Model AI dimuat HANYA pada carian makna pertama, bukan pada startup.
    w = PustakaApp()
    if os.path.exists(ico):
        w.setWindowIcon(QIcon(ico))
    w.show()

    return app.exec_()


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        sys.exit(1)
