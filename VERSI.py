"""Cap versi tunggal untuk seluruh projek.

MASALAH YANG DISELESAIKAN
-------------------------
Pengguna menjalankan salinan LAMA kod sebanyak tiga kali berturut-turut
tanpa dapat mengesannya. Puncanya ZIP mengandungi folder `hadis/`
bersarang, jadi mengekstraknya ke folder projek menghasilkan
`pustaka\\hadis\\core\\...` sedangkan skrip berjalan dari
`pustaka\\core\\...`. Fail lama tidak pernah diganti dan setiap laporan
kelihatan sah.

Modul ini memberi satu tempat untuk menyemak. Setiap skrip utama
mencetak `VERSI` pada baris pertama outputnya.
"""

from __future__ import annotations

VERSI = "1.0"

# Ciri yang mesti wujud pada versi ini. `semak_versi.py` mengesahkannya
# supaya "fail tidak diganti" gagal dengan KUAT, bukan senyap.
CIRI = (
    ("api.hadis_api", "bina_huraian_he"),
    ("core.eng_source", "JACCARD_MIN"),
    ("core.eng_source", "JACCARD_IND"),
    ("core.eng_source", "kunci_indonesia"),
    ("core.eng_source", "bina_indeks_ind"),
    ("core.eng_source", "padan_ind_kabur"),
    ("core.syarah_source", "nisbah_keyakinan"),
    ("core.syarah_source", "diagnos_hanyut"),
    ("core.syarah_source", "_MS"),
    ("core.hadeethenc_api", "JACCARD_MATN"),
    ("core.hadeethenc_api", "bina_indeks"),
    ("core.hadeethenc_api", "padan"),
    ("core.hadeethenc_api", "huraian"),
    ("core.hadeethenc_api", "senarai_id_ms"),
    ("core.sema_source", "JACCARD_MATN"),
    ("core.sema_source", "bina_indeks"),
    ("core.sema_source", "padan"),
    ("core.sema_source", "matn_bersih"),
    ("utils.bahasa", "betulkan_melayu"),
    ("utils.bahasa", "simbol_boleh_dipapar"),
    ("db", "_to_match_query"),          # v1.2: fallback OR bila FTS5 AND 0 hasil
    ("db", "_terms"),                   # v1.2: pembobotan ranking fallback OR
    ("ui.splash", "SplashPermula"),     # v1.3: skrin pemula + fasa pramuat
)
