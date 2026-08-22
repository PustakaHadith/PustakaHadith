# Penyelarasan Dokumentasi_Khas → Projek Utama (16 Ogos 2026)

> Folder `D:\Pustaka Quran Hadis\Pustaka_Hadis_Dokumentasi_Khas` ialah
> pakej dokumentasi sahaja (13 fail, tiada kod/DB/JSON/OCR) — koleksi
> dokumen daripada ZIP pembetulan + projek utama. Helaian ini merekod
> apa yang diserap, apa yang sama, dan percanggahan yang ditinggalkan.

## Diserap ke projek utama (dokumen kawalan installer — PyInstaller/MSIX)

| Fail (dokumen/rujukan/) | Sebelum (root) | Selepas | Baris |
|---|---|---|---|
| `INSTALLER.md` | 590 baris — reka bentuk awal Nuitka + Inno + GitHub (11 Ogos) | **902 baris** — panduan teknikal PyInstaller onedir → EXE → MSIX → Store (15 Ogos) | §0–§21 |
| `PLAN_BINA_EDARAN.md` | 187 baris — Nuitka + GitHub Releases, alat bina "TERBUKA" | **406 baris** — diselaraskan: PyInstaller utama, MSIX/Store utama, Nuitka fallback | Fasa 0–6 |
| `BANDING_INSTALLER.md` | "Alat bina = keputusan TERBUKA — jangan kunci" | **447 baris** — "✅ Keputusan didokumen": PyInstaller/MSIX + matriks + §10 syor empirikal (16 Ogos) | §1–§10 |

**Keputusan kunci (diserap):** alat utama **PyInstaller 6.22 onedir**
(sokongan rasmi Python 3.14 + PyQt5); edaran utama **MSIX/Microsoft
Store** (signing Microsoft, update terurus, tiada SmartScreen biasa);
Nuitka = **fallback** ber-gate; Inno/GitHub = **sekunder**. Ini membalikkan
pendirian root lama "alat bina terbuka sama rata" — didokumen dengan
rasional (§3 BANDING) + pengesahan empirikal (§10).

## Sama identik dengan projek utama (tiada tindakan)

`dokumen/audit/GTAF.md` · `AHMAD_DIGITAL.md` · `TERJEMAHAN_AHMAD_DARIMI.md`
· `CARIAN_ARAB.md` · `dokumen/rujukan/DRAF_carian_arab.md` ·
`PERMOHONAN_LESEN_AHMAD.md` — 6 fail identik.

## Percanggahan / sisa (ditinggalkan — bukan bahan projek)

1. **`AHMAD_HOCR.md` Khas = versi LAMA** — satu perkataan Indonesia yang
   semak 8m root telah betulkan (kepada "membuang"). Root kekal sebagai
   versi betul; Khas ialah arkib lama.
2. **`list-we-do.md` Khas TIADA seksyen K** (status penggabungan) — Khas
   ialah versi A–J sahaja (925 baris); salinan dalaman
   `hadis/Pustaka_Hadis_Pembetulan_Lengkap/list-we-do.md` ada seksyen K
   (status DIGABUNG) tetapi folder itu gitignored (bahan luaran).
3. **`BACA_INI.md` Khas merujuk fail yang TIADA dalam folder itu**
   (db.py, core/, ui/, JSON, OCR) — kerana folder ini dokumentasi sahaja;
   BACA_INI ialah salinan daripada ZIP penuh. Berpotensi mengelirukan
   pembaca baharu.

## Status terbuka (belum diluluskan)

- **Fasa 0 PLAN_BINA_EDARAN masih CADANGAN** — 6 keputusan skop (bundel
  model, hadis.db tidak dibundel, x64, MSIX utama, Inno sekunder, repo
  persendirian) menunggu kelulusan pengguna sebelum Fasa 1.
- **§8 baki tertangguh:** #7 kunci API hadis.my (kekal AKTIF sengaja);
  jurang Tafsir 843 dipantau.
- **Lesen Ahmad/Darimi** (#19 ⛔): menunggu jawapan sunnah.com +
  Darussalam; `PERMOHONAN_LESEN_AHMAD.md` sedia.
