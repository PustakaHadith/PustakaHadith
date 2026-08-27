# Keputusan Alat Bina dan Edaran — PyInstaller/MSIX berbanding Nuitka/Inno

**Tarikh:** 15 Ogos 2026  
**Status:** ✅ Keputusan didokumen dan diserap ke plan kawalan  
**Dokumen kawalan:** `PLAN_BINA_EDARAN.md`  
**Panduan teknikal:** `INSTALLER.md`

---

## 1. Penjelasan Laluan Sebenar

Laluan Store yang disyorkan ialah:

```text
Kod Python
    ↓
PyInstaller 6.22 onedir
    ↓
PustakaHadis.exe + folder _internal
    ↓
MSIX
    ↓
Microsoft Store
```

`PustakaHadis.exe` di sini ialah fail aplikasi utama dalam folder `onedir`,
**bukan installer EXE tambahan**.

Inno Setup tidak diperlukan untuk laluan Store. MSIX Packaging Tool boleh
menangkap payload folder PyInstaller secara manual.

Laluan luar Store ialah:

```text
PyInstaller onedir
    ↓
Inno Setup EXE
    ↓
GitHub Releases / penguji dalaman
```

Jadi keputusan bukan “mesti melalui Inno sebelum MSIX”. Keputusannya ialah:

```text
Utama   : PyInstaller onedir → MSIX → Store
Sekunder: PyInstaller onedir → Inno EXE → GitHub/penguji
Fallback: Nuitka jika PyInstaller gagal gate fungsi sebenar
```

---

## 2. Fail yang Dibandingkan

| Fail | Peranan |
|---|---|
| `INSTALLER.md` lama | Reka bentuk awal Nuitka + Inno + GitHub |
| `INSTALLER.md` baharu | Panduan teknikal PyInstaller + MSIX + Store |
| `PLAN_BINA_EDARAN.md` asal | Fasa 0–6 berasaskan reka bentuk lama |
| `PLAN_BINA_EDARAN.md` diselaraskan | Dokumen kawalan semasa |
| `BANDING_INSTALLER.md` | Rekod sebab keputusan ini |

---

# 3. Mengapa PyInstaller Digunakan Dahulu

## 3.1 Python 3.14 disokong secara rasmi

PyInstaller menambah sokongan Python 3.14 sejak versi 6.15. Versi 6.22
menyokong Python 3.8–3.15 dan menyenaraikan PyQt5 sebagai binding yang
disokong.

Rujukan:

```text
https://pyinstaller.org/en/stable/CHANGES.html
https://pypi.org/project/pyinstaller/
```

Nuitka 4.1 menambah banyak pembetulan Python 3.14, tetapi nota keluaran rasmi
masih menyatakan sokongan 3.14 sebagai eksperimen.

Rujukan:

```text
https://nuitka.net/posts/nuitka-release-41.html
```

Pustaka Hadith menggunakan:

```text
Python 3.14
PyQt5
torch
sentence-transformers
FAISS
```

Maka PyInstaller mempunyai risiko keserasian bahasa yang lebih rendah untuk
keluaran pertama.

---

## 3.2 Nuitka mempunyai amaran rasmi tentang PyQt5 callback/threading

Halaman rasmi Nuitka menyatakan sokongan PyQt5 “relatively problematic” dan
menyenaraikan isu callback serta threading.

Rujukan:

```text
https://nuitka.net/pages/pyqt5.html
```

Pustaka Hadith banyak bergantung pada:

```text
QThread
_Base
CollectionsWorker
SearchWorker
SemanticWorker
RandomWorker
signal/slot lintas thread
pramuat model di latar
```

Kegagalan threading boleh menyebabkan:

- signal tidak sampai;
- slot berjalan pada thread salah;
- carian tergantung;
- cancel tidak berfungsi;
- aplikasi hang semasa ditutup;
- crash yang sukar diulang.

Risiko ini lebih penting daripada perbezaan kecil saiz atau masa startup.

---

## 3.3 PyInstaller kurang mengubah semantik kod

PyInstaller membungkus:

```text
CPython runtime
bytecode Python
DLL/pyd
pakej pihak ketiga
aset aplikasi
```

Nuitka menterjemah kod Python kepada C sebelum kompilasi. Kompilasi boleh
memberikan manfaat prestasi, tetapi menambah satu lagi lapisan transformasi
kepada kod PyQt signal/slot yang sudah kompleks.

Untuk keluaran pertama, keutamaan projek ialah:

```text
ketepatan → kestabilan → kebolehujian → prestasi
```

bukan prestasi dahulu.

---

## 3.4 Diagnosis PyInstaller lebih cepat

Binaan diagnostik boleh dibuat dengan:

```powershell
--onedir --console
```

PyInstaller menghasilkan:

```text
warn-PustakaHadis-Debug.txt
xref-PustakaHadis-Debug.html
folder dist yang boleh diperiksa
```

Traceback boleh dilihat terus. Selepas lulus, binaan ditukar kepada:

```powershell
--onedir --windowed
```

Nuitka memerlukan kompilasi C yang lebih berat sebelum masalah import,
plugin Qt, compiler atau DLL dapat dinilai.

---

## 3.5 `onedir` sesuai untuk torch/model besar

Jangan gunakan PyInstaller `onefile` bagi keluaran ini.

Pakej besar akan diekstrak ke folder sementara setiap pelancaran, menyebabkan:

- startup lambat;
- pemeriksaan antivirus berulang;
- penggunaan ruang sementara;
- diagnosis DLL lebih sukar;
- kemungkinan fail sementara tertinggal selepas crash.

Gunakan:

```text
dist\PustakaHadis\
├── PustakaHadis.exe
└── _internal\
```

MSIX kemudian membungkus keseluruhan folder sebagai satu unit pemasangan.

---

## 3.6 Kelebihan Nuitka masih diakui

Nuitka mungkin memberikan:

- startup lebih pantas;
- saiz runtime lebih kecil;
- kod Python dikompil;
- pengendalian sesetengah pakej native yang lebih baik.

Namun saiz Pustaka Hadith banyak didominasi oleh:

```text
torch
model e5
FAISS index
Qt
```

Oleh itu pengurangan saiz alat bina mungkin tidak besar berbanding jumlah
aset. Semua dakwaan saiz/startup mesti diukur pada binaan sebenar.

---

# 4. Bila Nuitka Digunakan

Nuitka **tidak dibuang**. Ia menjadi fallback.

Fallback hanya dicetuskan jika PyInstaller masih gagal selepas:

1. hidden imports dibetulkan;
2. hanya PyQt5 dipasang dalam venv;
3. hooks torch/transformers/faiss disertakan;
4. metadata distribution disalin;
5. konflik DLL diperiksa dengan Dependencies/ProcMon;
6. binaan diuji pada Windows bersih;
7. MRE dan log kegagalan disimpan.

Kemudian bina Nuitka dalam venv berasingan dan uji dengan gate yang sama:

- semua worker/QThread;
- carian makna;
- sync;
- tutup/relaunch;
- Windows 10/11 bersih;
- data pengguna;
- DLL.

Pilih alat yang **lulus fungsi**, bukan alat yang sekadar menghasilkan EXE.

---

# 5. Mengapa MSIX Store Menjadi Saluran Utama

## 5.1 Microsoft menandatangani pakej MSIX

Selepas MSIX lulus pensijilan Store, Microsoft menandatanganinya dengan sijil
terpercaya.

Rujukan:

```text
https://learn.microsoft.com/windows/msix/package/sign-msix-package-guide
https://learn.microsoft.com/windows/apps/publish/faq/get-started-with-the-microsoft-store
```

Untuk MSIX Store, pembangun tidak perlu membeli sijil CA/PFX/token sendiri.

Store tidak menandatangani semula EXE/MSI tradisional. EXE langsung perlu
sijil Authenticode CA sendiri untuk kepercayaan pemasangan yang setara.

---

## 5.2 GitHub bukan pengganti tandatangan kod

GitHub Releases menyediakan hosting, tetapi tidak:

- menandatangani EXE;
- memberikan Publisher yang dipercayai;
- menghapus SmartScreen;
- mengurus update Windows;
- menjalankan pensijilan aplikasi.

EXE bersih tetapi tidak ditandatangani masih boleh memaparkan:

```text
Windows protected your PC
Unknown publisher
```

Untuk aplikasi agama yang meminta API key dan memuat turun data, amaran ini
boleh menjejaskan keyakinan pengguna.

---

## 5.3 Store memberi pengalaman pemasangan lebih dipercayai

MSIX Store memberikan:

- hosting binari Microsoft;
- tandatangan Microsoft;
- update automatik;
- pemasangan per-user;
- identiti pakej tetap;
- package flighting;
- analitik Partner Center;
- nyahpasang terurus;
- integrasi Start Menu/Windows.

Rujukan:

```text
https://learn.microsoft.com/windows/apps/distribute-through-store/how-to-distribute-your-win32-app-through-microsoft-store
https://learn.microsoft.com/windows/apps/package-and-deploy/packaging/
```

---

## 5.4 Kemas kini lebih mudah

MSIX Store mengurus pemeriksaan dan pemasangan versi baharu.

Bagi Inno + GitHub, projek sendiri perlu membina:

- semakan versi;
- muat turun update;
- checksum/signature verification;
- penutupan proses;
- installer update;
- rollback kegagalan;
- hosting dan nota keluaran.

Keluaran pertama tidak perlu menambah sistem updater tersendiri jika Store
sudah menyediakan fungsi itu.

---

## 5.5 Nyahpasang dan integriti pakej

MSIX memisahkan binari aplikasi daripada data pengguna dan memastikan folder
pakej baca sahaja. Update menggantikan pakej secara terurus.

Namun projek tetap perlu:

- memindahkan DB/settings/cache ke `%LOCALAPPDATA%\PustakaHadis`;
- menguji update `1.0.0.0 → 1.0.1.0`;
- menguji uninstall/reinstall;
- menyediakan eksport bookmark/settings;
- tidak menjanjikan data kekal selepas uninstall sebelum ujian sebenar.

---

# 6. Peranan Inno Setup dan GitHub

Inno Setup/GitHub kekal sebagai saluran sekunder untuk:

- penguji dalaman;
- mesin tanpa Microsoft Store;
- diagnosis awal;
- portable/EXE jika diperlukan;
- edaran persendirian sebelum Store.

Laluan:

```text
PyInstaller onedir → Inno Setup EXE → penguji/GitHub
```

Jika EXE tidak ditandatangani CA, nota keluaran mesti mengandungi:

- amaran SmartScreen yang jujur;
- SHA-256;
- pautan VirusTotal;
- Publisher/versi;
- pautan sumber sokongan.

GitHub kekal berguna, tetapi bukan saluran kepercayaan utama.

---

# 7. Matriks Keputusan

| Faktor | PyInstaller → MSIX → Store | Nuitka → Inno → GitHub |
|---|---|---|
| Python 3.14 | Sokongan rasmi | Masih eksperimen |
| PyQt5/QThread | Hook rasmi; risiko lebih rendah | Amaran rasmi callback/threading |
| Transformasi kod | Bungkus runtime/bytecode | Kompil Python → C |
| Diagnosis | Konsol + warn/xref, cepat | Kompilasi lebih berat |
| Startup | Memadai dengan `onedir` | Berpotensi lebih pantas |
| Saiz | Berpotensi lebih besar | Berpotensi lebih kecil |
| Torch/FAISS | Perlu hook dan ujian DLL | Berpotensi baik; tetap perlu ujian |
| Signing | Microsoft tandatangan MSIX | Perlu sijil sendiri bagi EXE |
| SmartScreen | Tiada amaran biasa melalui Store | Berisiko jika tidak ditandatangani |
| Hosting | Microsoft | GitHub |
| Update | Diurus Store | Perlu dibina sendiri |
| Pensijilan | Store | Tiada pensijilan GitHub |
| Kegunaan | Laluan utama | Fallback/sekunder |

---

# 8. Keputusan Praktikal

```text
1. Selesaikan laluan %LOCALAPPDATA%.
2. Bina PyInstaller debug onedir.
3. Uji semua QThread, torch, FAISS dan DLL.
4. Uji pada Windows 10/11 bersih tanpa Python.
5. Jika lulus, bina MSIX dan hantar ke Store.
6. Jika PyInstaller gagal selepas pembetulan munasabah, cuba Nuitka.
7. Bina Inno EXE hanya sebagai saluran sekunder/penguji.
```

Pendekatan ini tidak menganggap PyInstaller pasti sempurna. Ia memilih laluan
dengan risiko awal lebih rendah, kemudian menjadikan ujian sebenar sebagai
penentu akhir.

---

# 9. Hierarki Dokumentasi

```text
PLAN_BINA_EDARAN.md  — kawalan fasa, gate dan go/no-go
INSTALLER.md         — arahan teknikal terperinci
BANDING_INSTALLER.md — alasan keputusan ini
list-we-do.md        — sejarah kerja keseluruhan
```

Jika berlaku percanggahan:

1. ikut alat/urutan `PLAN_BINA_EDARAN.md`;
2. ikut pelaksanaan dalam `INSTALLER.md`;
3. guna dokumen ini untuk memahami rasional keputusan.

---

## 10. Syor akhir (16 Ogos 2026) — pengesahan empirikal

Keputusan di atas kini disokong oleh binaan diagnostik sebenar pada mesin
pembangun (venv bersih `.venv-pyi`, Python 3.14.6, PyInstaller 6.22,
`onedir --console`):

- **Binaan siap dalam ~33 minit, ~787 MB** (binaan debug onedir);
  `warn-PyInstaller` hanya amaran biasa (fungsi multiprocessing salah
  label — bukan masalah fungsi).
- **App dibuka tanpa traceback**; konsol menunjukkan log + DLL self-heal
  aktif; keluar bersih (EXIT=0).
- **Penemuan:** `main.py` TIADA `multiprocessing.freeze_support()` — wajib
  ditambah sebelum binaan keluaran (INSTALLER.md §6).
- **Gate Fasa 2 (app dibuka pada mesin pembangun): LULUS.**

**Syor:** teruskan **PyInstaller 6.22 `onedir` sebagai alat utama** (selaras
§3–§4 di atas). Nuitka kekal fallback ber-gate. Langkah seterusnya ialah
**Fasa 1 (pisahkan laluan data ke `%LOCALAPPDATA%`)** — hanya selepas
kelulusan Fasa 0 pengguna.
