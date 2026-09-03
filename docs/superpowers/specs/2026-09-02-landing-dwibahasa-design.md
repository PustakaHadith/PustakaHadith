# Reka Bentuk: Landing Page Dwibahasa (MS/EN)

Tarikh: 2026-09-02
Projek: Landing page PustakaHadith — `D:\Pustaka Quran Hadis\Pustaka\landing-page\index.html`

## Objektif
Satu fail `index.html` dengan toggle bahasa Melayu/Inggeris serta-merta (tanpa muat semula), auto-detect pelayar, dan ingatan pilihan pengguna.

## Keputusan (kelulusan pengguna)
- **Pendekatan**: Toggle satu halaman (`data-i18n` + objek `TRANS`).
- **Bahasa lalai**: Auto-detect pelayar (`navigator.language` bermula "en" → EN, selain → MS).
- **Ingatan**: Pilihan manual disimpan dalam `localStorage`; auto-detect hanya apabila tiada simpanan.
- **Nama kitab**: Kekalkan nama Latin lazim (Bukhari, Muslim, Abu Daud...); tajuk Arab kekal.
- **Meta dinamik**: `<title>`, `og:title`, `og:description`, `og:locale` ikut bahasa semasa.

## Struktur
1. **Atribut teks**: Setiap elemen teks `data-i18n="kunci"`.
2. **Objek terjemahan**: `TRANS = { "kunci": { "ms": "...", "en": "..." } }` dalam `<script>`.
3. **Butang bahasa**: "MS | EN" di navbar; aktif = teal, tidak aktif = pudar; `aria-pressed`.
4. **Logik**:
   - `resolusiLang()` → localStorage `ph-lang`; jika tiada → auto-detect.
   - `terapkanLang(lang)` → set teks semua `[data-i18n]`, `document.documentElement.lang`, dan meta dinamik.
   - Klik butang → tukar + simpan.

## Skop terjemahan
Semua 11 seksyen: navbar, hero, tangkap layar (tab + kapsyen), ciri utama, rak 9 kitab (label sahaja), disklaimer, statistik, muat turun, hubungi, footer, + alt/aria-label. Teks meta dll.

## Bukan skop (YAGNI)
- Tiada URL `/en` berasingan.
- Tiada `hreflang`.
- Nama & tajuk Arab tidak diterjemah.

## Ujian
- Buka fail → bahasa auto ikut pelayar.
- Klik MS/EN → semua teks bertukar segera, meta bertukar.
- Muat semula → kekal bahasa pilihan.
- Saiz fail masih satu `index.html` untuk upload FTP; laluan imej relatif tidak terjejas.

## Deploy
Upload semula `index.html` ke `ftpupload.net/htdocs/` (FTP) selepas siap.