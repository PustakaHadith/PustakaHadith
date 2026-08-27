# Revoke Kunci API Terdedah

> Dua kunci telah terdedah dalam perbualan. Panduan ini menggantikannya.

## Status disemak (Sesi 9)

```
HADIS_34A8****B52E6B   AKTIF   had 10,000/hari   <- pelan DEVELOPER
HADIS_E6D6****77C8C0   AKTIF   had    200/hari   <- pelan Basic
```

**Kedua-duanya masih hidup.** Yang pertama ialah kunci Developer anda
— itu yang paling penting dibatalkan. Ia berbaloi untuk disalahguna.

Dua kunci pada dua pelan berbeza bermakna kemungkinan **dua akaun**.
Semak kedua-dua akaun Google semasa log masuk.

---

## Kenapa ini penting

Kuota dikira **per akaun**, bukan per kunci. Sesiapa yang ada kunci
anda boleh menghabiskan kuota harian anda — dan pada pelan Developer
itu 10,000 permintaan. Anda tidak akan tahu sehingga apl berhenti
berfungsi.

---

## PENTING: baca dahulu sebelum revoke

Portal hadis.my memberi **1 API key sahaja** untuk setiap pelan
(Basic, Personal, Developer — semuanya 1).

Maknanya **tiada tempoh bertindih**. Saat kunci lama mati, apl anda
mati juga sehingga kunci baharu dimasukkan.

Jadi jangan revoke di tengah-tengah sync. Buat bila anda ada 5 minit
lapang.

---

## Langkah

### 1. Log masuk

```
https://developer.hadis.my/dashboard
```

Log masuk dengan Google — akaun yang sama semasa anda daftar dahulu.

### 2. Buka halaman kunci

```
https://developer.hadis.my/dashboard/keys
```

### 3. Semak penggunaan DAHULU

Sebelum memadam, lihat statistik penggunaan.

Jika jumlah permintaan jauh lebih tinggi daripada yang anda jangka,
kunci itu mungkin sudah digunakan orang lain. Ambil tangkapan skrin
sebelum revoke — buktinya hilang selepas kunci dipadam.

### 4. Revoke / jana semula

Cari butang **Revoke**, **Regenerate**, atau **Padam**. Sahkan.

### 5. Salin kunci baharu

Kunci penuh biasanya dipapar **sekali sahaja**. Salin terus.

### 6. Masukkan ke dalam apl

Buka PustakaHadith → ikon gear → **Tetapan API** → tampal → Simpan & Uji.

Sepatutnya keluar `✓ Berjaya — 9 koleksi`.

### 7. Sahkan kunci lama sudah mati

```
python semak_kunci.py
```

Ia menguji kunci lama yang terdedah dan melaporkan sama ada ia masih
diterima pelayan.

---

## Jangan tampal kunci baharu di mana-mana

- ❌ Sembang AI (termasuk saya)
- ❌ GitHub, Pastebin, tangkapan skrin
- ❌ Argumen baris arahan — kekal dalam sejarah shell
- ✅ Panel Tetapan dalam apl
- ✅ Fail `.env` dalam folder projek
- ✅ Pembolehubah persekitaran Windows

Ketiga-tiga tempat yang dibenarkan sudah ada dalam `.gitignore`.

---

## Jika revoke tidak tersedia

Sesetengah portal kecil tiada butang revoke. Hubungi penyedia:

- **WhatsApp**: +60 19-209 2006
- **Email**: khai@webmaster.my

Contoh mesej:

> Salam. Saya perlu batalkan API key sedia ada kerana ia telah
> terdedah secara tidak sengaja, dan mohon key baharu untuk akaun
> yang sama. Terima kasih.

Jangan sertakan kunci penuh dalam email — beri 8 aksara pertama
sahaja (`HADIS_34A8CDF8...`) supaya mereka boleh kenal pasti.

---

## Selepas siap

Jalankan `python semak_kunci.py` sekali lagi. Ia sepatutnya melaporkan
**kedua-dua kunci lama DITOLAK**.
