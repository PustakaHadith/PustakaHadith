#!/usr/bin/env python3
"""Profil masa semak.py — ukur tempoh SETIAP fungsi semakan.

Jalankan selepas semak.py lulus untuk mengenal pasti semakan perlahan
(pengesan regresi prestasi: jika satu semakan melonjak, ia boleh
menjadi punca). Sama seperti main() dalam semak.py, tetapi setiap
fungsi diukur masa + kiraan GAGAL.

    python profil_semak.py [--penuh]

`--penuh`: jalankan semakan audit sunnah (perlahan, lalai dilangkau
seperti semak.py tanpa --audit-sunnah). Skrip TIDAK mengubah apa-apa
fail; ia hanya memanggil fungsi semakan yang sama seperti semak.py.
"""

import os
import sys
import time

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)

import semak

FUNGSI = [
    ("1. Sintaks Python", semak.semak_sintaks),
    ("2. Import modul", semak.semak_import),
    ("3. Warna lalai", semak.semak_warna_lalai),
    ("4. CRLF", semak.semak_crlf),
    ("5. Join-Path", semak.semak_joinpath),
    ("6. Migrasi data", semak.semak_migrasi),
    ("7. Transliterasi", semak.semak_translit),
    ("8. Syarah", semak.semak_syarah),
    ("9. Bahasa", semak.semak_bahasa),
    ("10. Bahasa UI", semak.semak_bahasa_ui),
    ("11. Peraturan bahasa", semak.semak_peraturan_bahasa),
    ("12. Bandingan", semak.semak_bandingan),
    ("13. Peta sunnah", semak.semak_peta_sunnah),
    ("14. Pemula + pramuat", semak.semak_pemula),
    ("15. Profil model", semak.semak_profil_model),
    ("16. Padanan ENG", semak.semak_padanan_eng),
    ("17. HadeethEnc", semak.semak_hadeethenc),
    ("18. SemakHadis", semak.semak_sema),
    ("19. Gabungan", semak.semak_gabungan),
    ("20. Carian sibuk", semak.semak_carian_sibuk),
    ("21. Peta kembali", semak.semak_peta_kembali),
    ("22. Nav sebelum/seterusnya", semak.semak_nav_sebelum_seterusnya),
    ("23. Pemalar render", semak.semak_pemalar_render),
    ("24. Tab lalai", semak.semak_tab_lalai),
    ("25. Bab tafsir", semak.semak_bab_tafsir),
    ("26. Pilih terjemahan", semak.semak_pilih_terjemahan),
    ("27. Elide chip + warna cip", semak.semak_elide_chip),
    ("28. Kitab shell", semak.semak_kitab_shell),
    ("29. Kad koleksi", semak.semak_kad_koleksi),
    ("30. Visual kiraan", semak.semak_visual_kiraan),
    ("31. Visual rujukan (8z)", semak.semak_visual_rujukan),
    ("32. Deklarasi", semak.semak_deklarasi),
    ("33. Bahasa dokumen", semak.semak_bahasa_dokumen),
    ("34. Susun atur", semak.semak_susunatur),
    ("35. Apl", semak.semak_apl),
    ("36. Versi fail", semak.semak_versi_fail),
    ("37. Versi changelog", semak.semak_versi_changelog),
    ("38. Logo palet", semak.semak_logo_palet),
    ("39. Dokumen", semak.semak_dokumen),
    ("40. Peraturan sisa", semak.semak_peraturan_sisa),
    ("41. Bersih", semak.semak_bersih),
]

penuh = "--penuh" in sys.argv
if penuh:
    FUNGSI.insert(14, ("14b. Audit sunnah", semak.semak_audit_sunnah))

print("=" * 62)
print("  PROFIL MASA SEMAK.PY — ukur tempoh setiap seksyen")
print("=" * 62)
jumlah = 0.0
gagal_global = 0
hasil = []
for nama, fn in FUNGSI:
    semak.gagal = []
    t0 = time.perf_counter()
    fn()
    t = time.perf_counter() - t0
    jumlah += t
    n_gagal = len(semak.gagal)
    gagal_global += n_gagal
    hasil.append((nama, t, n_gagal))
    penanda = "  GAGAL" if n_gagal else "  OK"
    print(f"{penanda} {nama:42s} {t:7.2f}s  ({n_gagal} gagal)")

print("\n" + "=" * 62)
print(f"  JUMLAH: {jumlah:.2f}s  ({gagal_global} kegagalan keseluruhan)")
# 10 teratas paling perlahan
print("  10 teratas paling perlahan:")
for nama, t, ng in sorted(hasil, key=lambda x: -x[1])[:10]:
    print(f"    {t:7.2f}s  {nama}  ({ng} gagal)")
print("=" * 62)
sys.exit(1 if gagal_global else 0)
