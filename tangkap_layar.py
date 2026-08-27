import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PyQt5.QtWidgets import QApplication
import ui.app_qt as a

OUT = "dokumen/penerbitan/tangkapan"
os.makedirs(OUT, exist_ok=True)

app = QApplication(sys.argv)
w = a.PustakaApp()
w.resize(1280, 820)
w.show()
QApplication.processEvents()
time.sleep(1.0)

def grab(name, wait=0.6):
    QApplication.processEvents()
    time.sleep(wait)
    QApplication.processEvents()
    if hasattr(w, "_force_relayout"):
        try:
            w._force_relayout()
        except Exception:
            pass
    QApplication.processEvents()
    pix = w.grab()
    path = os.path.join(OUT, name)
    pix.save(path, "PNG")
    print("saved", path, pix.width(), "x", pix.height())

try:
    w.go("home"); grab("01_utama.png")
except Exception as e:
    print("home err", repr(e))
try:
    w.go("rak"); grab("02_rak_digital.png")
except Exception as e:
    print("rak err", repr(e))
try:
    w.open_kitab("bukhari"); w.go("kitab"); grab("03_kitab_bukhari.png", 1.4)
except Exception as e:
    print("kitab err", repr(e))
try:
    w.open_by_ref("bukhari", 1); w.go("detail"); grab("04_detail_bukhari_1.png", 1.4)
except Exception as e:
    print("detail err", repr(e))
try:
    w.go("search"); grab("05_carian.png")
except Exception as e:
    print("search err", repr(e))
try:
    w.go("saved"); grab("06_simpan_sejarah.png")
except Exception as e:
    print("saved err", repr(e))
w.close()
print("SELESAI")
