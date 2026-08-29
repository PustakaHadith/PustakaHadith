"""Crash reporter — tangkap exception tak terkawal & simpan laporan.

Tambahan murni: TIADA ubah UI sedia ada. Laporan disimpan ke
%LOCALAPPDATA%\\PustakaHadith\\crash_logs supaya tidak mencemarkan
repo (DATA_DIR mungkin = folder projek bila lari dari sumber).
"""
from __future__ import annotations

import os
import sys
import traceback
import datetime
import platform

try:
    from VERSI import VERSI as VERSI_APP
except Exception:
    VERSI_APP = "?"


def _folder_lapor() -> str:
    asas = os.environ.get("LOCALAPPDATA") or os.path.expanduser("~")
    laluan = os.path.join(asas, "PustakaHadith", "crash_logs")
    os.makedirs(laluan, exist_ok=True)
    return laluan


def simpan(exc_type, exc_value, tb) -> str:
    """Simpan laporan crash; pulangkan laluan fail."""
    masa = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    laluan = os.path.join(_folder_lapor(), f"crash_{masa}.txt")
    garis = [
        "PustakaHadith - Laporan Crash",
        f"Masa   : {datetime.datetime.now().isoformat(timespec='seconds')}",
        f"Versi  : {VERSI_APP}",
        f"Python : {platform.python_version()}",
        f"OS     : {platform.system()} {platform.release()} ({platform.machine()})",
        f"Frozen : {getattr(sys, 'frozen', False)}",
        "",
        "Exception:",
        f"  {exc_type.__name__}: {exc_value}",
        "",
        "Traceback:",
        "".join(traceback.format_tb(tb)),
    ]
    try:
        with open(laluan, "w", encoding="utf-8") as f:
            f.write("\n".join(garis))
    except Exception:
        pass
    return laluan


def _papar_gagal(laluan: str) -> None:
    """Papar dialog makluman (perlu QApplication wujud)."""
    try:
        from PyQt5.QtWidgets import QApplication, QMessageBox
        app = QApplication.instance()
        if app is None:
            return
        try:
            with open(laluan, "r", encoding="utf-8") as f:
                teks = f.read()
        except Exception:
            teks = laluan
        box = QMessageBox()
        box.setIcon(QMessageBox.Critical)
        box.setWindowTitle("PustakaHadith - Ralat Tidak Dijangka")
        box.setText(
            "Aplikasi mengalami ralat tidak dijangka.\n\n"
            "Satu laporan telah disimpan. Sila salin dan hantar kepada "
            "pembangun bersama keterangan apa yang anda lakukan."
        )
        box.setDetailedText(teks[:20000])
        box.setStandardButtons(QMessageBox.Ok)
        btn_salin = box.addButton("Salin Laporan", QMessageBox.ActionRole)
        box.exec_()
        if box.clickedButton() is btn_salin:
            try:
                import pyperclip
                pyperclip.copy(teks)
            except Exception:
                pass
    except Exception:
        pass


_asal = None


def _hook(exc_type, exc_value, tb) -> None:
    try:
        laluan = simpan(exc_type, exc_value, tb)
        _papar_gagal(laluan)
    except Exception:
        pass
    if _asal is not None:
        _asal(exc_type, exc_value, tb)


def pasang_excepthook() -> None:
    """Pasang sys.excepthook supaya crash tak terkawal dilapor & dipapar."""
    global _asal
    if _asal is None:
        _asal = sys.excepthook
    sys.excepthook = _hook
