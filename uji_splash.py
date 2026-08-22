"""Ujian hujung-ke-hujung: splash -> fasa pramuat -> model sedia.

Sahkan rantaian penuh (Sesi 28): SplashPermula dipaparkan, PustakaApp
menghantar fasa pramuat (kemajuan_pramuat) dari PreloadWorker, dan
siap_pramuat melaporkan model sedia selepas muat (~24s; boleh jadi
lebih lama bila antivirus/CPU sibuk). Ujian keluar AWAL sebaik
siap_pramuat berbunyi -- bukan menunggu pemasa tetap.
"""
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
os.environ["QT_QPA_PLATFORM"] = "offscreen"

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication

app = QApplication([])

from ui.splash import SplashPermula
from ui.app_qt import PustakaApp

splash = SplashPermula()
splash.show()

w = PustakaApp()
fasa = []


def catat(t):
    if t:
        fasa.append(t)


def selesai(ok, sebab="siap_pramuat"):
    print("fasa diterima:", fasa)
    print("model_sedia:", ok, f"({sebab})")
    lulus = bool(ok) and len(fasa) >= 2
    print("HASIL:", "LULUS" if lulus else "GAGAL")
    splash.close()
    w.close()
    app.quit()
    sys.exit(0 if lulus else 1)


w.kemajuan_pramuat.connect(catat)
w.siap_pramuat.connect(selesai)

# Jaga-jaga: jika pramuat tersangkut (cth. muat turun pertama), tutup
# selepas 70s. Biasanya siap ~24s dan pemasa ini tidak sempat berbunyi.
QTimer.singleShot(70000, lambda: selesai(w._model_sedia, "pemasa 70s"))
app.exec_()
