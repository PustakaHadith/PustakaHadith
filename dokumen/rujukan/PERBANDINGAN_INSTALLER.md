# Perbandingan Dua Hala Tuju Installer — bahan perbincangan

**Tarikh:** 16 Ogos 2026  
**Status:** ✅ Disahkan dengan pembetulan — bahan perbincangan, bukan dokumen kawalan  
**Dokumen kawalan:** `PLAN_BINA_EDARAN.md`

**Tujuan:** memaparkan dua hala tuju sebelah-menyebelah. Cadangan teknikal
sudah ditetapkan sebagai PyInstaller dahulu, Nuitka fallback; keputusan skop
pengguna dalam Fasa 0 masih perlu diluluskan. Dokumen ini tidak mengubah kod
atau menjalankan binaan.

---

## 1. Dua hala tuju

| | Hala tuju A | Hala tuju B |
|---|---|---|
| **Asal dokumen** | `Pustaka_Hadis_Dokumentasi_Khas` (15 Ogos) — diserap ke root 16 Ogos | Plan root asal `PLAN_BINA_EDARAN.md` (15 Ogos, sebelum serapan) + `INSTALLER.md` (11 Ogos) |
| **Alat bina** | PyInstaller 6.22 `onedir` | Nuitka `--standalone` |
| **Edaran utama** | MSIX → Microsoft Store | Inno Setup EXE → GitHub Releases |
| **Edaran sekunder** | Inno EXE (penguji / mesin tanpa Store) | Tiada secara lalai; MSIX hanya jika kemudian beralih ke hala tuju A |
| **Alat lain** | Nuitka = fallback ber-gate | PyInstaller masih boleh digunakan jika Nuitka gagal gate |

Kedua-dua hala tuju **bersetuju** pada:

- `hadis.db` tidak dibundel (pengguna sync sendiri) — keputusan pengguna sedia ada.
- Laluan data boleh tulis ke `%LOCALAPPDATA%\PustakaHadis`.
- x64 sahaja untuk keluaran pertama.
- Repo persendirian sehingga lesen data selesai.
- Bundel model e5 + indeks FAISS untuk profil ujian (awam menunggu lesen).

---

## 2. Perbandingan faktor demi faktor

| Faktor | Hala tuju A (PyInstaller → MSIX/Store) | Hala tuju B (Nuitka → Inno/GitHub) |
|---|---|---|
| **Sokongan Python 3.14** | PyInstaller 6.22: rasmi (3.8–3.15) | Nuitka 4.1: 3.14 masih "eksperimen" dalam nota keluaran |
| **PyQt5 + QThread** | PyInstaller senarai PyQt5 sebagai binding disokong | Dokumentasi rasmi Nuitka: PyQt5 "relatively problematic" — callback/threading; projek ini banyak guna QThread |
| **Transformasi kod** | Bungkus CPython runtime + bytecode + DLL/pyd (kurang ubah semantik) | Terjemah Python → C (prestasi berpotensi, satu lapisan transformasi tambahan) |
| **Diagnosis** | `--onedir --console` → warn/xref, traceback terus, pantas | Kompilasi C lebih berat sebelum masalah import/plugin/DLL boleh dinilai |
| **Saiz binaan** | Dilaporkan ~787 MB bagi folder debug `onedir` **tidak mampat**; perlu sahkan melalui artifak | Anggaran ~520 MB **mampat**; belum diukur — tidak boleh dibanding terus dengan angka 787 MB |
| **Startup** | Memadai dengan `onedir` (belum diukur) | Berpotensi lebih pantas (belum diukur) |
| **Torch/FAISS** | Perlu hook + ujian DLL (`c10.dll` isu lazim direkod) | Berpotensi lebih baik, tetap perlu ujian |
| **Tandatangan** | Microsoft menandatangani MSIX selepas lulus pensijilan Store | EXE perlu sijil Authenticode sendiri atau terima SmartScreen |
| **SmartScreen** | Tiada amaran biasa melalui Store | "Unknown publisher" / "Windows protected your PC" jika tidak ditandatangani |
| **Hosting** | Microsoft Store | GitHub Releases (2 GB/fail, percuma) |
| **Update** | Diurus Store (pemeriksaan + pasang automatik) | Perlu bina sistem update sendiri (semakan versi, muat turun, checksum, rollback) |
| **Pensijilan** | Pensijilan Store (masa + syarat listing) | Tiada pensijilan; edar serta-merta |
| **Nyahpasang** | Terurus (pakej vs data pengguna dipisah); perlu uji uninstall tidak padam data | Uninstaller Inno standard |
| **Kos** | Pendaftaran Partner Center baharu percuma untuk Individual dan Company melalui aliran baharu; Microsoft menandatangani MSIX Store | GitHub percuma; sijil Authenticode berbayar jika mahu Publisher dipercayai pada EXE |
| **Kebebasan edaran** | Terikat gating Store (listing, polisi, masa pensijilan) | Edar bila-bila, kawalan penuh |
| **Sasaran pengguna** | Aplikasi agama awam — kepercayaan pemasangan tinggi, minta API key + muat turun data | Penguji dalaman + pengguna yang sedia menerima amaran SmartScreen |

---

## 3. Fakta diukur vs belum diukur

**Dilaporkan telah diukur (16 Ogos, mesin pembangun; belum disahkan bebas
kerana folder `dist`, log binaan dan `warn-*.txt` tidak dilampirkan):**

- Binaan diagnostik PyInstaller 6.22 onedir console: dilaporkan siap ~33
  minit, folder ~787 MB, app dibuka tanpa traceback dan keluar bersih.
- Dakwaan kandungan `warn-PyInstaller` perlu disahkan semula apabila log
  sebenar disertakan.

Angka 787 MB ialah folder `onedir` tidak mampat. Jangan banding terus dengan
anggaran installer Nuitka 520 MB yang mampat.
- `main.py` tiada `multiprocessing.freeze_support()` — perlu ditambah sebelum
  binaan keluaran (mana-mana alat).
- Binaan Nuitka **belum dibuat** (sesi 15 Ogos terputus sebelum Fasa 2 Nuitka).

**Belum diukur (perlu bina diagnostik dahulu):**

- Saiz sebenar binaan Nuitka.
- Masa startup kedua-dua binaan.
- Tingkah laku torch/FAISS/QThread pada Windows bersih (tanpa Python).
- Prestasi DLL self-heal (`_baik_pulih_dll_qt_torch`) dalam binaan frozen.

---

## 4. Keputusan Fasa 0 — soalan untuk pengguna

Enam keputusan skop (dari `PLAN_BINA_EDARAN.md` §8) yang perlu dijawab
sebelum Fasa 1. **Tiada satu pun diluluskan lagi.**

1. **Bundel model + indeks untuk profil ujian** — adakah binaan ujian perlu
   membawa model e5 + indeks FAISS? (elak muat turun/bina berjam-jam; awam
   menunggu lesen)
2. **Microsoft Store = saluran utama?** — adakah awak bersedia bergantung pada
   akaun Partner Center + pensijilan Store sebagai laluan utama? Atau GitHub
   sahaja dahulu?
3. **Inno EXE = saluran sekunder/penguji?** — perlukah EXE untuk penguji
   dalaman dan mesin tanpa Store?
4. **Akaun/identiti Partner Center** — adakah awak ada akaun pembangun
   Microsoft? Nama Publisher yang dikehendaki?
5. **Portable ZIP** — adakah versi mudah alih (tanpa pemasangan) perlu selepas
   MSIX lulus?
6. **Wizard permulaan** — bila perlu dibina: sebelum beta, atau selepas
   installer asas terbukti berfungsi?

**Urutan alat bina telah diputuskan secara teknikal:** uji PyInstaller dahulu.
Nuitka hanya dicetuskan jika PyInstaller gagal selepas hook, metadata, binding
Qt dan DLL diperbetulkan serta kegagalan direkod. Tidak perlu membina kedua-
duanya secara penuh serentak. Kelulusan pengguna Fasa 0 masih diperlukan
untuk memulakan perubahan kod.

---

## 5. Ruang keputusan

Keputusan pengguna akan direkod di bawah ini apabila perbincangan selesai:

- [x] Cadangan teknikal alat bina: **A dahulu; B hanya fallback ber-gate**.
- [x] Pengguna meluluskan/mengubah cadangan alat bina: **DILULUSKAN 19 Ogos 2026**.
- [x] Saluran utama (Store / GitHub / lain-lain): **Microsoft Store (MSIX)**.
- [x] Jawapan 6 soalan Fasa 0 (rujuk §4):
      1. Bundel model + indeks untuk profil ujian — **Ya**.
      2. Store = saluran utama — **Ya**.
      3. Inno EXE = sekunder/penguji — **Ya**.
      4. Akaun Partner Center — **WAJIB di Fasa 5; daftar sekarang (percuma) +
         tempah nama Pustaka Hadith; nama Publisher pilihan pengguna**.
      5. Portable ZIP — **Ya untuk penguji dalaman sahaja**.
      6. Wizard permulaan — **Bina sebelum beta**.
- [x] Tarikh keputusan pengguna: **19 Ogos 2026**.

---

## 6. Kos penuh setahun (anggaran, 16 Ogos 2026)

**Nota penting:** Microsoft membuang yuran pendaftaran Individual pada
September 2025 dan yuran Company pada Mei 2026 melalui aliran pendaftaran
baharu. Kedua-dua jenis akaun kini percuma, tetapi pengesahan identiti/perniagaan
masih diperlukan. Harga sijil Authenticode di bawah ialah anggaran pasaran,
bukan sebut harga; vendor, HSM/token dan tempoh boleh mengubah jumlah.
Anggaran Ringgit dalam dokumen asal: 1 USD ≈ RM 4.3.

Rujukan rasmi:

- `https://blogs.windows.com/windowsdeveloper/2025/09/10/free-developer-registration-for-individual-developers-on-microsoft-store/`
- `https://blogs.windows.com/windowsdeveloper/2026/05/07/publish-to-microsoft-store-as-a-company-now-with-free-registration-and-faster-onboarding/`
- `https://learn.microsoft.com/windows/apps/package-and-deploy/code-signing-options`

| Perkara | Hala tuju A (Store) | Hala tuju B (GitHub EXE) |
|---|---|---|
| Pendaftaran pembangun | **RM 0** (yuran US$19 dibuang, Sept 2025) | RM 0 |
| Sijil tanda tangan | **Tiada** — Microsoft menandatangani MSIX selepas lulus | **Tanpa sijil: RM 0** tetapi SmartScreen kekal; **OV/standard: ~US$220–290/tahun (~RM 950–1,250)**; **EV: ~US$280–535/tahun (~RM 1,200–2,300)** |
| Hosting | Percuma (Store) | Percuma (GitHub Releases) |
| Update automatik | Termasuk (Store) | Perlu bina sendiri (kos pembangunan, bukan lesen) |
| Pensijilan | Masa (hari), bukan wang; listing perlu ikon/screenshot/dasar privasi | Tiada pensijilan |
| **Jumlah tahun pertama** | **~RM 0** (hanya masa pensijilan + kos pembangunan yang sama bagi kedua-dua hala tuju) | **~RM 0–2,300/tahun** bergantung pilihan sijil |
| **Tahun berikutnya** | ~RM 0 | ~RM 950–2,300/tahun jika sijil dikekalkan |

**Perbezaan kos sebenar:** hala tuju A tiada kos lesen langsung. Hala tuju B
percuma jika terima SmartScreen, atau ~RM 1,000–2,300 setahun untuk sijil.

**Laluan tengah yang mungkin (belum diputuskan):** hala tuju B tanpa sijil
(bina reputasi SmartScreen melalui banyak muat turun + sifar pengesanan AV),
atau hala tuju A dengan GitHub sebagai penguji dalaman dahulu.

---

## 7. Pengalaman pengguna akhir langkah demi langkah

### Hala tuju A — Microsoft Store

1. Buka **Microsoft Store** (sudah terbina dalam Windows 10/11).
2. Cari **"Pustaka Hadith"** → halaman listing (ikon, screenshot, penerangan, dasar privasi).
3. Klik **Dapatkan** → pemasangan automatik, **tiada amaran SmartScreen**.
4. Buka app → wizard permulaan (keputusan Fasa 0 #6): deklarasi → kunci API
   → sync koleksi (~12 minit, bar kemajuan, boleh dijeda) → siap.
5. Guna aplikasi seperti biasa.
6. **Update automatik** — Store memasang versi baharu; pengguna tidak perlu
   berbuat apa-apa.
7. Nyahpasang dari Tetapan → Apl; data pengguna (`%LOCALAPPDATA%`) perlu
   dikendalikan dengan teliti (uji uninstall tidak memadam data).

**Ringkasan pengguna:** ~4 langkah, sifar amaran keselamatan, update tidak
kelihatan. Paling hampir dengan "klik satu fail, terpasang".

### Hala tuju B — GitHub EXE

1. Buka pautan **GitHub Releases** (dari hadis.my / dokumentasi).
2. Muat turun **PustakaHadis-Setup-x64.exe** (anggaran lama ~520 MB;
   belum diukur daripada binaan Nuitka sebenar).
3. **SmartScreen** muncul: *"Windows protected your PC"* — pengguna perlu
   klik **More info → Run anyway** (kecuali EXE ditandatangani + reputasi
   dibina; walaupun ditandatangani OV, amaran reputasi mungkin masih muncul
   pada awal).
4. Jalankan wizard **Inno Setup** (Bahasa Melayu) → pilih folder → pasang
   (per-user, tanpa admin).
5. Buka app → wizard permulaan yang sama seperti A.
6. **Update manual** — pengguna perlu tahu versi baharu wujud, muat turun
   semula dan pasang; atau projek bina sistem update sendiri.
7. Nyahpasang dari Tetapan → Apl (uninstaller Inno); data pengguna sama
   perlu diuji.

**Ringkasan pengguna:** ~6–7 langkah termasuk amaran keselamatan yang boleh
menakutkan pengguna awam; lebih diterima untuk penguji dalaman yang faham.

### Perbandingan ringkas

| Titik | A (Store) | B (GitHub EXE) |
|---|---|---|
| Langkah ke app berjalan | ~4 | ~6–7 |
| Amaran keselamatan | Tiada | SmartScreen (kecuali sijil + reputasi) |
| Update | Automatik | Manual atau bina sendiri |
| Kesesuaian | Pengguna awam | Penguji dalaman / pengguna teknikal |

---

## 8. Ringkasan untuk perbincangan

- **Wang:** A = RM 0 lesen (yuran Store dibuang 2025); B = RM 0 tanpa sijil
  (SmartScreen) atau ~RM 1,000–2,300/tahun dengan sijil.
- **Kepercayaan:** A = amaran sifar, tanda tangan Microsoft; B = amaran
  SmartScreen pada awal, reputasi perlu dibina.
- **Kawalan:** B = edar serta-merta, tiada gating; A = terikat pensijilan
  Store tetapi mendapat hosting + update automatik.
- **Fakta belum diukur:** saiz/startup Nuitka, ukuran mampat PyInstaller dan
  tingkah laku kedua-dua pakej pada Windows bersih.
- **Cadangan teknikal:** A dahulu; B hanya fallback jika A gagal gate.
- **Keputusan pengguna:** enam keputusan skop Fasa 0 masih menunggu jawapan.

Dokumen kawalan kekal `PLAN_BINA_EDARAN.md`; dokumen ini tidak menggantikan
gate atau meluluskan perubahan kod.

---

## 9. Keputusan Pengesahan

| Bahagian | Keputusan |
|---|---|
| Sokongan Python 3.14 PyInstaller | ✅ Disahkan melalui dokumentasi rasmi |
| Amaran Python 3.14/PyQt5 Nuitka | ✅ Disahkan melalui dokumentasi rasmi |
| Pendaftaran Store percuma | ✅ Disahkan untuk Individual dan Company melalui aliran baharu |
| Store hosting/signing/update MSIX | ✅ Disahkan melalui Microsoft |
| PyInstaller ~33 minit / 787 MB | 🟡 Laporan pengguna/dokumen; artifak dan log belum dilampirkan |
| Nuitka ~520 MB | 🟡 Anggaran mampat; belum dibina |
| Harga sijil | 🟡 Anggaran pasaran; perlu sebut harga ketika membeli |
| Keputusan alat bina | ✅ A dahulu, B fallback; kelulusan pengguna Fasa 0 masih perlu |

**Verdik:** dokumen boleh digunakan sebagai bahan perbincangan selepas
pembetulan di atas. Jangan gunakan angka 787 MB berbanding 520 MB sebagai
bukti kelebihan saiz sehingga kedua-duanya diukur pada bentuk yang sama
(folder tidak mampat atau installer mampat).
