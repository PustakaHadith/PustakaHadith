# Permohonan Kebenaran — Terjemahan Inggeris Musnad Ahmad

**Tarikh draf:** 15 Ogos 2026  
**Projek:** PustakaHadith — aplikasi desktop Windows berbahasa Melayu  
**Status:** **DITUTUP — English koleksi Ahmad diabaikan secara kekal (27 Ogos 2026).**
Tiada perancangan menghantar permohonan ke Darussalam/Sunnah.com; teks Inggeris
Ahmad tidak akan disertakan dalam mana-mana keluaran. Tab English Ahmad kekal kelabu.
Dokumen ini disimpan sebagai rekod keputusan sahaja.

---

## 1. Kesimpulan Lesen

### Sunnah.com

Halaman rasmi `https://sunnah.com/about#Reproduction` menyatakan:

> “We do not permit the scraping of our data, nor mass reproduction of entire
> books or collections on other websites.”

Mereka membenarkan hadis individu/pilihan untuk tujuan pengajaran, tetapi
mengarahkan permintaan data kepada API. Halaman pembangun membenarkan
permohonan kunci API melalui isu GitHub dan menyebut permintaan *offline dump*.

### AhmedBaset/hadith-json

`package.json` menyatakan `ISC`, tetapi repositori tidak mempunyai fail
`LICENSE`, dan README menyatakan data itu hasil scrape sunnah.com. Lesen
metadata pakej pihak ketiga tidak semestinya memberikan hak terhadap teks
terjemahan yang dimiliki sumber/penerbit asal.

### Darussalam

Terjemahan Musnad Ahmad diterbitkan Darussalam dan halaman hak cipta buku
menyatakan “All Rights Reserved” serta melarang pengeluaran semula tanpa
kebenaran terdahulu. Oleh itu kebenaran Darussalam juga perlu diminta, kecuali
sunnah.com dapat membuktikan lesen mereka merangkumi pengedaran luar talian
oleh pihak ketiga.

**Keputusan:** 1,345 pemetaan boleh disimpan sebagai bahan teknikal, tetapi
teks Inggeris tidak boleh dimasukkan ke keluaran awam tanpa kebenaran jelas.

---

## 2. Permohonan kepada Sunnah.com

**Saluran:**

- Borang/isu API: `https://github.com/sunnah-com/api/issues/new?template=request-for-api-access.md`
- Halaman pembangun: `https://sunnah.com/developers`
- Hubungan: `https://sunnah.com/contact`

### Tajuk

```text
Request for API/offline redistribution permission — PustakaHadith (Malay Windows app)
```

### Teks permohonan

```text
Assalamu alaikum wa rahmatullahi wa barakatuh,

I am developing PustakaHadith, a free Windows desktop application for Malay-
speaking users. The application provides offline access to nine major hadith
collections, with Arabic and Malay text sourced separately from hadis.my.

I would like to request permission to use the English translation of the
available Musnad Ahmad entries from Sunnah.com. The current verified scope is
approximately 1,359 English entries. The application is intended to work
offline, so I specifically need clarification on whether the English text may
be stored and distributed inside the application database.

The project will:
- remain free to users;
- display clear attribution to Sunnah.com, the translator and Darussalam;
- preserve references and grades without alteration;
- include a source link where practical;
- not claim ownership of the translation;
- follow any required correction/update process.

Could you please clarify:
1. Whether your API currently provides the Musnad Ahmad English entries;
2. Whether API data may be cached and redistributed for offline use;
3. Whether your permission covers the underlying Darussalam/Nasir Khattab
   translation, or whether separate permission from Darussalam is required;
4. The exact attribution wording and any other conditions;
5. Whether a non-commercial offline data dump or written licence can be
   provided for this purpose.

No English Musnad Ahmad text will be included in a public release until the
permission position is clear.

Jazakum Allahu khairan.
```

---

## 3. Permohonan kepada Darussalam

**Hubungan rasmi yang ditemui:**

- `sales@darussalamstore.com`
- `sales@darussalam.com`
- `sales@darussalam.uk`

Minta penerima memanjangkan mesej kepada bahagian hak cipta/permissions jika
alamat tersebut hanya mengurus jualan.

### Tajuk

```text
Permission request — English Translation of Musnad Imam Ahmad in a free Malay desktop application
```

### Teks permohonan

```text
Assalamu alaikum wa rahmatullahi wa barakatuh,

I am requesting written permission concerning the English Translation of
Musnad Imam Ahmad bin Hanbal, translated by Nasiruddin Al-Khattab and edited by
Huda Al-Khattab, published by Darussalam.

I am developing PustakaHadith, a free Windows desktop application for Malay-
speaking users. It contains Arabic and Malay text for nine major collections
and is designed for offline study. I would like to include the available
English Musnad Ahmad translations as an optional language layer.

The currently contemplated initial scope is approximately 1,359 entries from
the early volumes. The text would be stored locally so the application can
work without an internet connection.

Please advise whether Darussalam is willing to grant permission for:
- reproduction and distribution of these English translations inside the
  free desktop application;
- offline storage in the application's SQLite database;
- distribution worldwide through a project download or Microsoft Store;
- future inclusion of further translated volumes, subject to your approval.

The application will provide prominent attribution to Darussalam,
Nasiruddin Al-Khattab and Huda Al-Khattab, preserve references and grades, and
follow any correction or branding requirements specified by Darussalam.

Please also advise:
1. The required attribution wording;
2. Whether the permission is limited to non-commercial distribution;
3. Whether there is a licence fee or written agreement;
4. Whether permission may cover all currently published English volumes;
5. Whether distribution through Microsoft Store is permitted if the app
   remains free.

No translated text will be included in a public release unless written
permission is granted.

Jazakum Allahu khairan.
```

---

## 4. Maklumat yang Perlu Disimpan

Simpan bersama rekod projek:

- tarikh permohonan;
- alamat e-mel/URL isu;
- salinan teks dihantar;
- nombor tiket/isu;
- jawapan penuh;
- nama dan jawatan pemberi kebenaran;
- skop jilid/hadis;
- syarat atribusi;
- syarat komersial/nonkomersial;
- tempoh dan wilayah lesen;
- sama ada Microsoft Store dibenarkan.

Jangan anggap ketiadaan jawapan sebagai kebenaran.

---

## 5. Keputusan Muktamad (27 Ogos 2026)

Diputuskan: **abaikan English koleksi Ahmad secara kekal**, tiada rancangan
memohon kebenaran bertulis Darussalam/Sunnah.com.

1. Tab English Ahmad kekal kelabu (tiada teks Inggeris Ahmad dalam apl).
2. Jangan masukkan teks Inggeris Ahmad ke `terjemahan_eng` produksi.
3. Pemetaan SHA/nombor (1,345–1,359 entri) disimpan untuk audit dalaman sahaja.
4. Ini **membuang lesen Ahmad sebagai blocker** Fasa 6/7 — MSIX & Store boleh
   diteruskan tanpanya.
5. Jika pada masa hadapan mahu sertakan, buka semula permohonan §2–§3.

---

## 6. Rujukan

- `https://sunnah.com/about#Reproduction`
- `https://sunnah.com/developers`
- `https://github.com/sunnah-com/api`
- `https://github.com/AhmedBaset/hadith-json`
- `https://darussalampublishers.com/contact-us/`
- `https://darussalam.com/english-translation-of-musnad-imam-ahmad-bin-hanbal-vol-5-hadith-6031-7624/`

*Rujukan silang: `dokumen/audit/AHMAD_DIGITAL.md` dan `AHMAD_HOCR.md`.*
