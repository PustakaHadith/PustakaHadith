#!/usr/bin/env python3
"""Semakan sebelum hantar pakej.

    python semak.py                   # semakan penuh (luar talian)
    python semak.py --audit-sunnah    # + audit pautan sunnah.com (rangkaian)

Menjalankan setiap semakan yang pernah menangkap pepijat sebenar dalam
projek ini. Setiap satu wujud kerana sesuatu pernah rosak -- lihat
`dokumen/manual/MULA_SINI.md` bahagian 2. `--audit-sunnah` (Sesi 36) mengesahkan pautan
"Baca penuh" terhadap halaman sunnah.com sebenar -- jaringan, jadi ia
opt-in supaya gate lalai kekal pantas dan boleh dipercayai.

Keluar 0 jika semua lulus, 1 jika ada kegagalan.
"""

from __future__ import annotations

import ast
import datetime
import glob
import io
import json
import os
import re
import subprocess
import sys
import tokenize

# Semakan yang melancarkan PustakaApp menulis user_settings.json minima
# (tanpa bendera deklarasi) dan MEMADAMKAN fail asal pengguna selepas
# ujian. Jika fail asal (dengan `deklarasi_dibaca: true`) tidak
# dipulihkan, larian app berikutnya memaparkan dialog deklarasi modal
# yang menyekat ujian offscreen (tiada pengguna untuk klik "Faham") —
# gejala: ujian "tersangkut". Simpan kandungan asal supaya boleh
# dipulihkan di akhir setiap semakan yang menyentuhnya.
_ASAL_SETTINGS = None
if os.path.exists("user_settings.json"):
    try:
        with open("user_settings.json", encoding="utf-8") as _fh:
            _ASAL_SETTINGS = _fh.read()
    except OSError:
        _ASAL_SETTINGS = None


def _pulihkan_settings():
    """Pulihkan user_settings.json ke keadaan asal (atau buang jika
    asalnya tiada) — supaya ujian app selepas semak.py tidak terjerat
    dialog deklarasi modal yang menyekat dalam mod offscreen.

    25 Ogos: cuba semula sehingga 5x pada PermissionError — Windows
    (antivirus/pemeriksa fail) kadang memegang kunci sekejap selepas
    subproses app selesai; tanpa cuba semula, larian semak gagal palsu.
    """
    import time as _time
    for _cuba in range(5):
        try:
            if _ASAL_SETTINGS is not None:
                with open("user_settings.json", "w", encoding="utf-8") as _fh:
                    _fh.write(_ASAL_SETTINGS)
            elif os.path.exists("user_settings.json"):
                os.remove("user_settings.json")
            return
        except PermissionError:
            if _cuba == 4:
                raise
            _time.sleep(0.3)

BASE = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE)

# Cache baca fail berasaskan (mtime, saiz) supaya fail yang sama tidak
# dibaca berulang kali oleh semakan berbeza (sintaks, bahasa dokumen,
# bahasa UI, susun atur). SELAMAT untuk ujian mutasi (uji_negatif_8z):
# fail yang dimutasi mendapat mtime baharu -> kunci cache berubah ->
# kandungan segar dibaca. Kunci mtime_ns + saiz mustahil bertembung
# untuk dua kandungan berbeza pada fail yang sama.
_BACA_CACHE: dict[str, tuple[int, int, str]] = {}


def _baca_cek(path: str) -> str:
    """Baca fail dengan cache (mtime, saiz); pulangkan kandungan."""
    try:
        st = os.stat(path)
        kunci = (st.st_mtime_ns, st.st_size)
    except OSError:
        raise
    lama = _BACA_CACHE.get(path)
    if lama is not None and lama[0] == kunci[0] and lama[1] == kunci[1]:
        return lama[2]
    with open(path, encoding="utf-8") as fh:
        teks = fh.read()
    _BACA_CACHE[path] = (kunci[0], kunci[1], teks)
    return teks

# Konsol Windows lalai kepada cp437/cp1252 yang TIDAK boleh mengekod
# teks Arab mahupun tanda sempang panjang. Tanpa baris ini, semak.py
# mati dengan UnicodeEncodeError sebelum sempat melapor apa-apa --
# disahkan dengan PYTHONIOENCODING=cp437.
# errors="replace" ialah jaring kedua: lebih baik papar '?' daripada
# menggugurkan keseluruhan laporan.
for _aliran in (sys.stdout, sys.stderr):
    try:
        _aliran.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

gagal: list[str] = []


LULUS_CNT = 0    # bilangan lulus() dipanggil — tuntutan README 'N semakan'
TAJUK_NAMA = []  # nama tajuk() dipanggil — untuk kira 'M bahagian'


def tajuk(t: str) -> None:
    TAJUK_NAMA.append(t)
    print(f"\n  {t}")
    print("  " + "-" * 56)


def bilangan_bahagian() -> int:
    """Bilangan bahagian bernombor biasa ('N. '), bukan sub-bahagian
    (8b–8o, 10b). Ini tuntutan README '(M bahagian)'."""
    return sum(1 for t in TAJUK_NAMA if re.match(r"^\d+\. ", t))


def lulus(msg: str) -> None:
    global LULUS_CNT
    LULUS_CNT += 1
    print(f"    OK    {msg}")


def salah(msg: str) -> None:
    print(f"    GAGAL {msg}")
    gagal.append(msg)


# ---------------------------------------------------------------- 1
def semak_crlf() -> None:
    """Fail .bat/.ps1 mesti CRLF + ASCII tulen.

    Lesson #20: LF menyebabkan cmd.exe gagal SENYAP -- blok berkurungan
    pecah, `set /p` tidak membaca input. Aksara kotak Unicode jadi
    sampah dalam codepage konsol.
    """
    tajuk("1. Skrip Windows: CRLF + ASCII")
    fail = sorted(glob.glob("*.bat") + glob.glob("*.ps1"))
    if not fail:
        salah("tiada fail .bat/.ps1 dijumpai")
        return
    for f in fail:
        d = open(f, "rb").read()
        cr, lf = d.count(b"\r"), d.count(b"\n")
        na = sum(1 for b in d if b > 127)
        if cr == lf and cr > 0 and na == 0:
            lulus(f"{f:20} CRLF={cr}")
        else:
            salah(f"{f:20} CR={cr} LF={lf} bukan-ASCII={na}")


# ---------------------------------------------------------------- 2
def semak_warna_lalai() -> None:
    """Warna sebagai nilai lalai fungsi = terkunci pada masa import.

    Lesson #17: `def f(color=TEXT_SECONDARY)` membekukan warna tema
    gelap. Mod terang jadi kelabu pucat atas putih -- hampir tidak
    kelihatan.
    """
    tajuk("2. Warna sebagai nilai lalai fungsi")
    W = {"TEXT_PRIMARY", "TEXT_SECONDARY", "TEXT_MUTED", "TEXT_FAINT",
         "CARD_BG", "CARD_BG_HOVER", "PAGE_BG", "SURFACE", "HEADER_BG",
         "TEAL", "TEAL_LIGHT", "TEAL_PALE", "BORDER", "BORDER_LIGHT"}
    jumpa = False
    for f in sorted(glob.glob("ui/*.py")):
        pokok = ast.parse(open(f, encoding="utf-8").read())
        for n in ast.walk(pokok):
            if not isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            baki = list(n.args.defaults) + [x for x in n.args.kw_defaults if x]
            for d in baki:
                for s in ast.walk(d):
                    if isinstance(s, ast.Name) and s.id in W:
                        salah(f"{f}:{n.lineno} {n.name}() color={s.id}")
                        jumpa = True
    if not jumpa:
        lulus("tiada warna dibekukan sebagai nilai lalai")


# ---------------------------------------------------------------- 3
def semak_joinpath() -> None:
    """`Join-Path $env:X` mesti berada DALAM pengawal null.

    Lesson #19: berlaku 3 kali ($env:WINDIR, $env:APPDATA x2).
    Join-Path dinilai SEBELUM Test-Path, jadi ia melontar jika null.
    """
    tajuk("3. PowerShell: Join-Path dengan env null")
    jumpa = False
    for f in sorted(glob.glob("*.ps1")):
        baris = open(f, encoding="utf-8", errors="replace").read().split("\n")
        for i, b in enumerate(baris, 1):
            if "Join-Path $env:" not in b:
                continue
            # selamat jika baris ini sendiri dalam `if ($env:X)` sebelumnya
            konteks = " ".join(baris[max(0, i - 3):i])
            var = b.split("Join-Path $env:")[1].split()[0].strip("'\" )")
            if f"$env:{var})" in konteks or f"$env:{var} " in konteks.replace(
                    "Join-Path $env:" + var, ""):
                continue
            salah(f"{f}:{i} Join-Path $env:{var} tanpa pengawal jelas")
            jumpa = True
    if not jumpa:
        lulus("semua Join-Path $env: dilindungi")


# ---------------------------------------------------------------- 4
def semak_sintaks() -> None:
    tajuk("4. Sintaks Python")
    rosak = []
    for f in _senarai_py_projek():
        if "__pycache__" in f:
            continue
        try:
            ast.parse(_baca_cek(f))
        except SyntaxError as e:
            rosak.append(f"{f}:{e.lineno} {e.msg}")
    if rosak:
        for r in rosak:
            salah(r)
    else:
        lulus("semua fail .py sah")


# ---------------------------------------------------------------- 5
def semak_import() -> None:
    tajuk("5. Import modul teras")
    sys.path.insert(0, BASE)
    for m in ("config", "db", "api.hadis_api", "core.eng_source",
              "core.phase2_transliterasi",
              "core.phase3_translate",
              "core.hadeethenc_api",
              "utils.transliteration", "sync", "sync_english",
              "sync_hadeethenc"):
        try:
            __import__(m)
            lulus(m)
        except Exception as e:
            salah(f"{m}: {type(e).__name__}: {e}")


# ---------------------------------------------------------------- 6
def semak_apl() -> None:
    """Apl mesti melancar tanpa ralat, dalam 6 mod tema (termasuk sistem)."""
    tajuk("6. Apl melancar (6 mod tema, termasuk 'sistem')")
    skrip = (
        "import sys,json,time; sys.path.insert(0,'.')\n"
        # 25 Ogos: cuba semula pada PermissionError — antivirus Windows
        # kadang memegang kunci fail sekejap selepas ia ditulis berulang.
        "for _ in range(10):\n"
        "    try:\n"
        "        _f=open('user_settings.json','w')\n"
        "        json.dump({'theme':TEMA,'api_key':'','api_url':'x'},_f)\n"
        "        _f.close(); break\n"
        "    except PermissionError:\n"
        "        time.sleep(0.3)\n"
        "from PyQt5.QtWidgets import QApplication\n"
        "from PyQt5.QtCore import QTimer\n"
        "a=QApplication([])\n"
        "from ui.app_qt import PustakaApp\n"
        "w=PustakaApp(); w.resize(1100,760); w.show()\n"
        "QTimer.singleShot(600,a.quit); a.exec_(); print('SIAP')\n"
    )
    env = dict(os.environ, QT_QPA_PLATFORM="offscreen")
    # Ujian ini melancarkan PustakaApp, yang memanggil db.init() dan
    # MENCIPTA hadis.db kosong. Di folder bersih itu menandai semak_bersih
    # kotor; rekod keadaan asal supaya artifak sendiri boleh dibuang.
    db_asal = os.path.exists("hadis.db")
    # 25 Ogos: "aqua" ditambah (tema ke-5, lalai baharu).
    for tema in ("aqua", "neutral", "dark", "lightneutral", "light",
                 "sistem"):
        try:
            r = subprocess.run(
                [sys.executable, "-c", skrip.replace("TEMA", repr(tema))],
                capture_output=True, text=True, timeout=120, env=env)
        except subprocess.TimeoutExpired:
            salah(f"tema {tema}: tergantung")
            continue
        if "SIAP" in r.stdout:
            lulus(f"tema {tema}")
        else:
            ekor = (r.stderr or "").strip().split("\n")[-1][:90]
            salah(f"tema {tema}: {ekor}")
    _pulihkan_settings()
    # Buang hadis.db yang dicipta sendiri oleh ujian ini (jika tiada sebelum).
    if not db_asal:
        for f in ("hadis.db", "hadis.db-wal", "hadis.db-shm"):
            if os.path.exists(f):
                os.remove(f)


# ---------------------------------------------------------------- 7
def semak_migrasi() -> None:
    """DB lama mesti naik taraf tanpa kehilangan data."""
    tajuk("7. Migrasi skema DB")
    import sqlite3
    import tempfile
    sys.path.insert(0, BASE)
    import db as _db

    tmp = os.path.join(tempfile.mkdtemp(), "lama.db")
    c = sqlite3.connect(tmp)
    c.executescript("""
        CREATE TABLE collections (slug TEXT PRIMARY KEY, name TEXT NOT NULL,
            author TEXT, total_hadis INTEGER);
        CREATE TABLE hadis (rowid_pk INTEGER PRIMARY KEY AUTOINCREMENT,
            collection TEXT NOT NULL, hadis_id INTEGER NOT NULL, arab TEXT,
            melayu TEXT, indonesia TEXT, UNIQUE(collection,hadis_id));
        CREATE VIRTUAL TABLE hadis_fts USING fts5(melayu, arab,
            content='hadis', content_rowid='rowid_pk',
            tokenize='unicode61 remove_diacritics 2');
        CREATE TABLE favorites (collection TEXT NOT NULL,
            hadis_id INTEGER NOT NULL, note TEXT,
            created_at TEXT DEFAULT (datetime('now')),
            PRIMARY KEY(collection,hadis_id));
    """)
    c.execute("INSERT INTO collections(slug,name) VALUES('bukhari','B')")
    c.executemany(
        "INSERT INTO hadis(collection,hadis_id,arab,melayu,indonesia) "
        "VALUES(?,?,?,?,?)",
        [("bukhari", i, f"a{i}", f"m{i}", f"i{i}") for i in range(1, 51)])
    c.execute("INSERT INTO favorites(collection,hadis_id,note) "
              "VALUES('bukhari',7,'nota saya')")
    c.commit()
    c.close()

    conn = _db.init(tmp)
    v = _db.versi(conn)
    n = conn.execute("SELECT COUNT(*) FROM hadis").fetchone()[0]
    f = conn.execute("SELECT note FROM favorites WHERE hadis_id=7").fetchone()
    ada = bool(conn.execute("SELECT name FROM sqlite_master "
                            "WHERE name='terjemahan_eng'").fetchone())
    ada_he = bool(conn.execute("SELECT name FROM sqlite_master "
                               "WHERE name='hadethenc'").fetchone())
    ulang = _db.migrasi(conn)
    conn.close()

    if v == _db.SKEMA_VERSI:
        lulus(f"versi {v}")
    else:
        salah(f"versi {v}, jangkaan {_db.SKEMA_VERSI}")
    if n == 50:
        lulus("50 hadis kekal")
    else:
        salah(f"{n} hadis (jangkaan 50)")
    if f and f[0] == "nota saya":
        lulus("favorit kekal")
    else:
        salah("favorit HILANG")
    if ada:
        lulus("terjemahan_eng dicipta")
    else:
        salah("terjemahan_eng tiada")
    if ada_he:
        lulus("hadethenc dicipta")
    else:
        salah("hadethenc tiada")
    if ulang == 0:
        lulus("idempoten")
    else:
        salah(f"migrasi berjalan semula ({ulang})")


# ---------------------------------------------------------------- 7b
# Kes ujian: (arab, rumi_melayu, rumi_ilmiah_atau_None)
# Setiap satu menguji satu peraturan tertentu. Gabungan kes saya
# (jalalah, shadda) dengan kes pengguna (tanwin, syamsiyyah).
KES_TRANSLIT = [
    # lafz al-jalalah -- BUKAN "al-lah". Regresi sebenar Sesi 7:
    # susunan aksara ialah konsonan+FATHA+SHADDA, bukan +SHADDA+FATHA.
    ("\u0627\u0644\u0644\u064E\u0651\u0647", "Allah", "All\u0101h"),
    ("\u0631\u064E\u0633\u064F\u0648\u0644\u064F "
     "\u0627\u0644\u0644\u064E\u0651\u0647\u0650",
     "rasulu Allahi", None),
    # lillah selepas kata sendi -- laluan kod BERBEZA daripada jalalah
    ("\u0627\u0644\u0652\u062D\u064E\u0645\u0652\u062F\u064F "
     "\u0644\u0650\u0644\u064E\u0651\u0647\u0650",
     "al-hamdu li-llahi", None),
    # shadda -- konsonan berganda
    ("\u062D\u064E\u062F\u064E\u0651\u062B\u064E\u0646\u064E\u0627",
     "haddathana", "\u1E25addathan\u0101"),
    ("\u0646\u0650\u064A\u064E\u0651\u0629", "niyyah", "niyyah"),
    # tanwin -- damma berganda jadi "-un"
    ("\u0645\u064F\u062D\u064E\u0645\u064E\u0651\u062F\u064C",
     "muhammadun", None),
    ("\u0645\u064E\u0633\u0652\u062C\u0650\u062F\u064C",
     "masjidun", None),
    ("\u0643\u0650\u062A\u064E\u0627\u0628\u064C", "kitabun", None),
    # huruf syamsiyyah: al- + sy = asy-  /  al- + r = ar-
    ("\u0627\u0644\u0634\u064E\u0651\u0645\u0652\u0633",
     "asy-syams", None),
    ("\u0627\u0644\u0631\u064E\u0651\u062D\u0652\u0645\u064E\u0646",
     "ar-rahman", "al-ra\u1E25man"),
    # vokal panjang + sukun
    ("\u0635\u064E\u0644\u064E\u0627\u0629", "salah", "\u1E63al\u0101h"),
    ("\u064A\u064E\u0648\u0652\u0645", "yawm", "yawm"),
]


def semak_translit() -> None:
    """Kunci tingkah laku transliterasi supaya regresi ditangkap.

    Sesi 7: jadual LAFZ_JALALAH wujud tetapi TIDAK PERNAH sepadan --
    kunci ditulis dengan susunan shadda+fatha sedangkan teks sebenar
    guna fatha+shadda. `الله` jadi "al-lahi". Ujian ini menghalang
    ia berulang.

    Nilai jangkaan diambil daripada output SELEPAS pembetulan. Jangan
    kemas kini nilai ini untuk "melepaskan" ujian -- siasat dahulu
    sama ada perubahan itu betul.
    """
    tajuk("7b. Transliterasi (kes diketahui)")
    sys.path.insert(0, BASE)
    try:
        from core.phase2_transliterasi import transliterate_arabic
    except Exception as e:
        salah(f"tidak dapat import: {e}")
        return

    for arab, melayu, ilmiah in KES_TRANSLIT:
        try:
            r = transliterate_arabic(arab)
        except Exception as e:
            salah(f"{arab}: {type(e).__name__}: {e}")
            continue
        dapat_m = (r.get("rumi_malay_style") or "").strip()
        dapat_i = (r.get("rumi") or "").strip()
        if dapat_m != melayu:
            salah(f"{arab} -> melayu '{dapat_m}' (jangka '{melayu}')")
            continue
        if ilmiah is not None and dapat_i != ilmiah:
            salah(f"{arab} -> ilmiah '{dapat_i}' (jangka '{ilmiah}')")
            continue
        lulus(f"{dapat_m}")


# ---------------------------------------------------------------- 8b
def semak_syarah() -> None:
    """Parser syarah + pengawal penomboran.

    Pengawal ialah bahagian paling penting: tanpa ia, perubahan pada
    sumber OpenITI boleh memasangkan SETIAP hadis dengan syarah yang
    salah. Diukur pada data sebenar: penomboran betul ~76%, teranjak
    14-22%.
    """
    tajuk("8b. Syarah (parser + pengawal padanan)")
    sys.path.insert(0, BASE)
    try:
        from core.syarah_source import (
            KITAB_SYARAH, bersih, hurai_hash_n, sahkan_padanan, url_kitab,
        )
    except Exception as e:
        salah(f"import core.syarah_source: {e}")
        return

    # Penanda manuskrip `ms00022` menyelit DI TENGAH ayat Arab
    # (10,952 kali dalam Fath al-Bari). Jika tidak dibuang ia
    # mencemarkan paparan dan memecahkan kata bersebelahan.
    kotor = "\u0648\u0623\u0635\u0644\u0647 ms00022 \u062f\u0645\u0634\u0642\u064a"
    if "ms00022" not in bersih(kotor):
        lulus("bersih() buang penanda manuskrip ms#####")
    else:
        salah("bersih() TIDAK buang `ms00022` — akan dipapar kepada pengguna")
    # Jangan terlalu agresif: `ms12` (2 digit) bukan penanda OpenITI
    if "ms12" in bersih("ms12"):
        lulus("bersih() tidak buang ms + 2 digit")
    else:
        salah("bersih() terlalu agresif pada `ms12`")

    # Pengesan hanyut: penomboran boleh sejajar pada AWAL kitab dan
    # tersasar progresif selepas itu. Pengawal lama menyemak 80 hadis
    # pertama sahaja -> lapor 76% "selamat" untuk sumber yang
    # sebenarnya tersasar -360 menjelang akhir Bukhari.
    try:
        import sqlite3 as _sq
        from core.syarah_source import nisbah_keyakinan
        c = _sq.connect(":memory:")
        c.execute("CREATE TABLE hadis(collection TEXT,hadis_id INT,arab TEXT)")
        # Korpus tiruan: setiap hadis ada kata jarang uniknya sendiri.
        rows, sej, hanyut = [], {}, {}
        for i in range(1, 601):
            t = (f"\u0645\u062a\u0646 \u0631\u0642\u0645{i} "
                 f"\u0643\u0644\u0645\u0629{i * 7} "
                 f"\u0644\u0641\u0638{i * 13} \u062d\u062f\u064a\u062b")
            rows.append(("bukhari", i, t))
            sej[i] = t + " \u0634\u0631\u062d"
            # hanyut: separuh kedua digeser
            hanyut[i if i < 300 else i - 100] = t + " \u0634\u0631\u062d"
        c.executemany("INSERT INTO hadis VALUES(?,?,?)", rows)
        r1 = nisbah_keyakinan(sej, c, "bukhari")
        r2 = nisbah_keyakinan(hanyut, c, "bukhari")
        if r1["lulus"]:
            lulus("pengawal TERIMA penomboran sejajar")
        else:
            salah(f"pengawal tolak sumber sah (nisbah {r1['nisbah']:.2f}x, "
                  f"stabil={r1['stabil']})")
        if not r2["lulus"]:
            lulus("pengawal TOLAK penomboran yang hanyut")
        else:
            salah("pengawal terima penomboran hanyut — syarah SALAH "
                  "akan disimpan")
    except Exception as e:
        salah(f"pengesan hanyut: {e}")

    # _skor_julat mesti sampel MERENTAS julat, bukan N pertama.
    # Ralat ini menggigit dua kali: pengawal lama (80 hadis pertama
    # -> 76% palsu) dan _skor_julat (skor julat awal sahaja).
    try:
        from core.syarah_source import _skor_julat
        # Hadis 1-100 padan sempurna; 101-1000 tidak padan langsung.
        # Sampel N-pertama -> ~100%. Sampel merentas -> ~10%.
        tk, sk = {}, {}
        for i in range(1, 1001):
            t = (f"\u0645\u062a\u0646{i} \u0643\u0644\u0645\u0629{i*7} "
                 f"\u0644\u0641\u0638{i*13} \u0631\u0642\u0645{i*3}")
            tk[i] = t
            sk[i] = (t + " \u0634\u0631\u062d") if i <= 100 else \
                    "\u0646\u0635 \u0622\u062e\u0631 \u062a\u0645\u0627\u0645\u0627"
        v = _skor_julat(tk, sk, 1, 1000, 0, had=120)
        if v < 0.35:
            lulus(f"_skor_julat sampel merentas julat ({v*100:.0f}%)")
        else:
            salah(f"_skor_julat sampel N-PERTAMA sahaja ({v*100:.0f}%) "
                  f"— skor tidak mewakili keseluruhan kitab")
    except Exception as e:
        salah(f"_skor_julat: {e}")

    for kunci, m in KITAB_SYARAH.items():
        if all(k in m for k in ("nama", "pengarang", "atas", "repo",
                                "laluan", "format")):
            lulus(f"katalog {kunci}")
        else:
            salah(f"katalog {kunci}: medan hilang")

    # repo AH dibundarkan KE ATAS: 852H -> 0875AH, bukan 0850AH
    u = url_kitab("fathbari")
    if "0875AH" in u and u.startswith("https://raw.githubusercontent.com"):
        lulus("URL fathbari (repo 0875AH)")
    else:
        salah(f"URL salah: {u}")

    kotor = "\u0642\u0648\u0644\u0647 PageV01P123 ~~\u062D\u062F\u062B\u0646\u0627"
    b = bersih(kotor)
    if "PageV" not in b and "~~" not in b and "\u062D\u062F\u062B\u0646\u0627" in b:
        lulus("bersih() kekalkan teks Arab")
    else:
        salah(f"bersih() rosak: {b!r}")

    contoh = ("#META#Header#End#\n"
              "# 1 \u0623\u0644\u0641\n~~\u0628\u0627\u0621\n"
              "# 2 \u062C\u064A\u0645\n")
    d = hurai_hash_n(contoh)
    if set(d) == {1, 2} and "~~" not in d[1]:
        lulus("hurai_hash_n() 2 seksyen")
    else:
        salah(f"hurai_hash_n() salah: {d}")

    import tempfile
    import db as _db
    tmp = os.path.join(tempfile.mkdtemp(), "sy.db")
    conn = _db.init(tmp)
    conn.execute("INSERT INTO collections(slug,name) VALUES('bukhari','B')")
    perawi = ["\u0632\u064A\u062F", "\u0639\u0645\u0631\u0648",
              "\u062E\u0627\u0644\u062F", "\u0633\u0639\u062F",
              "\u0637\u0644\u062D\u0629", "\u0628\u0644\u0627\u0644"]
    hadis, seksyen = [], {}
    for i in range(1, 41):
        a, b2 = perawi[i % 6], perawi[(i * 3) % 6]
        hadis.append(("bukhari", i,
                      f"\u062D\u062F\u062B\u0646\u0627 {a}{i} "
                      f"\u0639\u0646 {b2}{i*7}", "", ""))
        seksyen[i] = (f"\u0642\u0648\u0644\u0647 {a}{i} "
                      f"\u0647\u0648 {b2}{i*7}")
    conn.executemany(
        "INSERT INTO hadis(collection,hadis_id,arab,melayu,indonesia) "
        "VALUES(?,?,?,?,?)", hadis)
    conn.commit()

    p1, n1 = sahkan_padanan(seksyen, conn, "bukhari", sampel=30)
    p2, n2 = sahkan_padanan({k + 7: v for k, v in seksyen.items()},
                            conn, "bukhari", sampel=30)
    k1 = p1 / n1 if n1 else 0
    k2 = p2 / n2 if n2 else 0
    conn.close()

    if k1 >= 0.7:
        lulus(f"pengawal terima penomboran betul ({k1*100:.0f}%)")
    else:
        salah(f"pengawal tolak penomboran BETUL ({k1*100:.0f}%)")
    if k2 < 0.5:
        lulus(f"pengawal tolak penomboran teranjak ({k2*100:.0f}%)")
    else:
        salah(f"pengawal TERIMA penomboran salah ({k2*100:.0f}%)")


# ---------------------------------------------------------------- 8bb
def semak_bahasa() -> None:
    """Ejaan Indonesia dalam terjemahan Melayu.

    hadis.my memberi Melayu yang baik (`solat`, `bahawa`, `wuduk`)
    tetapi "Shallallahu" tertinggal secara sistematik -- 456 kali
    dalam 400 hadis sampel. DBP: ejaan betul ialah "Sallallahu".
    """
    tajuk("8bb. Pembetulan ejaan Melayu")
    sys.path.insert(0, BASE)
    try:
        from utils.bahasa import betulkan_melayu as B
    except Exception as e:
        salah(f"import utils.bahasa: {e}")
        return

    ubah = [
        ("Rasulullah Shallallahu 'alaihi wasallam",
         "Rasulullah Sallallahu 'alaihi wasallam"),
        ("Nabi shallallahu alaihi wasallam",
         "Nabi sallallahu alaihi wasallam"),
        ("Umar Radhiyallahu 'anhu", "Umar Radiallahu 'anhu"),
        ("mendirikan shalat", "mendirikan solat"),
        ("bulan Ramadhan", "bulan Ramadan"),
        ("hadits ini shahih", "hadis ini sahih"),
        ("adzan dan wudhu", "azan dan wuduk"),
        ("bahwa dia", "bahawa dia"),
    ]
    for masuk, jangka in ubah:
        r = B(masuk)
        if r == jangka:
            lulus(f"{masuk[:30]} -> {r[:34]}")
        else:
            salah(f"{masuk!r} -> {r!r} (jangka {jangka!r})")

    # Ligatur selawat: RINGKAS tetapi lafaz kekal PENUH.
    from utils.bahasa import LIGATUR_SELAWAT, guna_simbol_selawat as G
    for masuk in ("Rasulullah Shallallahu 'alaihi wasallam bersabda",
                  "Nabi sallallahu alaihi wa sallam",
                  "Baginda Sallallahu 'alaihi wasallam"):
        r = G(B(masuk))
        if LIGATUR_SELAWAT in r and "allallahu" not in r:
            lulus(f"ligatur: {r[:36]}")
        else:
            salah(f"ligatur gagal: {masuk!r} -> {r!r}")

    # Bentuk RUMI (transliterasi) -- bentuk KES penuh (damma "u" pada
    # Allāhu + fatha "a" pada sallama) ialah output SEBENAR modul
    # transliterasi. Sebelum Sesi 34 lanjutan regex hanya padan bentuk
    # pausal ("salla Allah 'alayhi wa-sallam") -- 541/541 sampel rumi
    # terlepas, ﷺ tidak pernah diganti. Semakan ini headless (tanpa
    # skrin fizikal) -- regresi regex dikesan terus di sini.
    for nama, masuk in (
            ("kes Melayu",
             "qala rasul Allah salla Allahu 'alayhi wa-sallama qala"),
            ("kes akademik",
             "qāla rasūl Allāh ṣallā Allāhu ʿalayhi wasallama qāla"),
            ("pausal Melayu",
             "qala rasul Allah salla Allah 'alayhi wa-sallam"),
            ("pausal akademik",
             "qāla rasūl Allāh ṣallā Allāh ʿalayhi wasallam")):
        r = G(B(masuk))
        if (LIGATUR_SELAWAT in r
                and re.search(r"[sṣ]all[āa]?\s+[Aa]ll[āa]h", r) is None):
            lulus(f"rumi ﷺ ({nama}): {r[:40]}")
        else:
            salah(f"rumi ﷺ gagal ({nama}): {masuk!r} -> {r!r}")

    # Bentuk ARAB penuh tertanam dalam teks Melayu: "صلى الله عليه
    # وسلم" (9,733 baris hadis.melayu). Sebelum ini regex hanya Latin
    # -- bentuk Arab kekal penuh walaupun rumi di sebelahnya ditukar.
    # Semakan ini headless mengunci regresi (alternatif Arab dibuang).
    for nama, masuk in (
            ("Arab standard", "Rasulullah صلى الله عليه وسلم bersabda"),
            ("Arab typo وسسلم", "Nabi صلى الله عليه وسسلم."),
            ("Arab tashkeel",
             "Rasulullah صَلَّى اللَّهُ عَلَيْهِ وَسَلَّمَ bersabda")):
        r = G(B(masuk))
        if (LIGATUR_SELAWAT in r
                and re.search(r"صلى الله عليه وسس?لم", r) is None):
            lulus(f"Arab ﷺ ({nama}): {r[:40]}")
        else:
            salah(f"Arab ﷺ gagal ({nama}): {masuk!r} -> {r!r}")
    # 'صلى' sebagai kata kerja (solat) atau frasa Arab lain TIDAK boleh
    # tersentuh -- hanya frasa selawat penuh yang diganti.
    for t in ("dia صلى الفجر di masjid", "اللَّهُ أَكْبَرُ"):
        if G(B(t)) == t:
            lulus(f"Arab kekal: {t[:28]!r}")
        else:
            salah(f"Arab tersilap ubah {t!r}")

    # Bentuk Melayu dengan PETIK MELENGKUNG ‘ (U+2018) / ’ (U+2019):
    # data hadis.my guna kedua-dua petik -- 3,693 sisa sebelum Sesi 34
    # lanjutan kerana regex hanya terima apostrof ASCII. Semakan ini
    # headless mengunci regresi (kelas petik dikecilkan semula).
    for nama, masuk in (
            ("Melayu ‘ U+2018",
             "Nabi Sallallahu ‘alaihi wasallam bersabda"),
            ("Melayu ’ U+2019",
             "Nabi Sallallahu ’alaihi wasallam bersabda"),
            ("Shallallahu ‘",
             "Nabi Shallallahu ‘alaihi wasallam bersabda")):
        r = G(B(masuk))
        if (LIGATUR_SELAWAT in r
                and re.search(r"[Ss]all?all?ahu", r) is None):
            lulus(f"petik ﷺ ({nama}): {r[:40]}")
        else:
            salah(f"petik ﷺ gagal ({nama}): {masuk!r} -> {r!r}")

    # nama yang mengandungi 'Salam' TIDAK boleh tersentuh
    for t in ("Abdullah bin Salam", "Assalamualaikum",
              "as-salamu 'alaykum", "Salam sejahtera"):
        if G(B(t)) == t:
            lulus(f"ligatur kekal: {t!r}")
        else:
            salah(f"ligatur tersilap ubah {t!r}")

    # JANGAN diubah -- positif palsu merosakkan makna
    kekal = ["Solat pada waktunya", "hadis ini sahih", "kalian semua",
             "Abdullah bin Salam", "Assalamualaikum", "bulan Ramadan", ""]
    for t in kekal:
        if B(t) == t:
            lulus(f"kekal: {t[:34]!r}")
        else:
            salah(f"tersilap ubah {t!r} -> {B(t)!r}")



# Frasa INGGERIS yang jelas dipapar pengguna -- TIDAK boleh wujud dalam
# STRING LITERAL mana-mana fail .py (bukan docstring/komen/SQL).
# Satu larian audit (Sesi 24) mendapati launcher.py, build_faiss_index.py
# DAN core/semantic_search.py memapar mesej Inggeris ("Python version:",
# "Loading model...", "FAISS index not found"). Kesilapan ini senyap:
# pengguna lihat mesej, tidak ada yang tersilap jalan, tetapi aplikasi
# kelihatan tidak konsisten. Frasa penuh dipilih (bukan perkataan tunggal)
# supaya tiada positif palsu pada istilah teknikal yang dibenarkan
# (API, offline, model, FAISS).
FRASA_INGGERIS = [
    "python version:", "current directory:",
    "application completed successfully",
    "error running application", "unexpected error",
    "loading model", "fetching hadis from database", "total hadis",
    "encoding texts", "embedding dimension", "total embeddings",
    "building faiss", "saving index", "saving id map",
    "total vectors", "database not found", "done!", "output:",
    "faiss index not found", "id map not found",
    "please wait", "try again", "no results", "no result",
    "not available", "unable to", "could not", "successfully",
]

# Kandungan string yang bermaksud BUKAN komunikasi pengguna: stylesheet
# QSS, SQL, atau pengecualian sistem. String yang mengandungi ini
# dikecualikan daripada semakan bahasa.
_BUKAN_KOMUNIKASI = (
    "background", "border", "color:", "font-", "padding", "margin",
    "insert into", "select ", "where ", "order by", "rowid",
    "hadis_fts", "count(*)", "json.dump", "http://", "https://",
    "sqlite", "pragma", "create table", "alter table",
)

# Folder yang bukan kod komunikasi pengguna (skrip arkib/sandaran).
_SKIP_FOLDER = ("__pycache__", "_arkib", "sandaran_", "tampalan_preload",
                ".git", ".cache", "_opencode", "Pustaka_Hadis_Pembetulan_Lengkap",
                ".venv", "build", "dist")


def _senarai_py_projek() -> list:
    """Fail .py projek sahaja — folder _SKIP_FOLDER (venv, binaan,
    arkib, .git, .cache) diprun semasa walk. glob('**/*.py') merentas
    folder ini terlalu lambat selepas .venv-pyi/build/dist wujud
    (torch = berpuluh ribu fail) — semak.py tergantung di sini."""
    hasil = []
    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs
                   if not any(s in os.path.join(root, d)
                              for s in _SKIP_FOLDER)]
        for f in files:
            if f.endswith(".py"):
                hasil.append(os.path.relpath(os.path.join(root, f), "."))
    return sorted(hasil)

def _bukan_komunikasi(f: str) -> bool:
    """Fail tidak disemak -- bukan kod komunikasi pengguna."""
    if any(d in f for d in _SKIP_FOLDER):
        return True
    # semak.py sendiri mengandungi FRASA_INGGERIS sebagai DATA rujukan
    # (bukan komunikasi pengguna) -- mengecualikannya mengelak laporan
    # diri sendiri. Fail `audit_eng.py` TETAP disemak (fail projek sah).
    return f == "semak.py"


def _semak_bahasa_fail(p: str) -> list[str]:
    """Cari frasa Inggeris dalam STRING LITERAL fail Python.

    Docstring, komen, SQL, dan stylesheet dikecualikan -- ia bukan
    komunikasi pengguna. Pulangkan senarai frasa yang dijumpai.
    """
    try:
        src = _baca_cek(p)
        pokok = ast.parse(src)
    except (OSError, SyntaxError):
        return []

    baris_doc = set()
    for n in ast.walk(pokok):
        if isinstance(n, (ast.FunctionDef, ast.ClassDef, ast.Module)) \
                and n.body and isinstance(n.body[0], ast.Expr) \
                and isinstance(n.body[0].value, ast.Constant) \
                and isinstance(n.body[0].value.value, str):
            for ln in range(n.body[0].lineno, n.body[0].end_lineno + 1):
                baris_doc.add(ln)

    jumpa = []
    for n in ast.walk(pokok):
        if not isinstance(n, ast.Constant) or not isinstance(n.value, str):
            continue
        if n.lineno in baris_doc:
            continue
        s = n.value
        # Ambang rendah supaya frasa pendek ("done!", "output:") turut
        # dikesan; had atas elak teks panjang (kandungan/terjemahan).
        if len(s) < 4 or len(s) > 180:
            continue
        low = s.lower().strip()
        if any(t in low for t in _BUKAN_KOMUNIKASI):
            continue
        for fr in FRASA_INGGERIS:
            if fr in low:
                jumpa.append(fr)
                break
    return jumpa


def semak_bahasa_ui() -> None:
    """Komunikasi aplikasi mesti dalam Bahasa Melayu (kecuali terjemahan).

    Semua mesej yang dipapar pengguna -- UI, toast, konsol pelancar,
    output skrip, pengecualian -- mesti Melayu. Setiap fail .py disemak
    (AST, docstring/SQL/stylesheet dikecualikan). Frasa Inggeris yang
    jelas ("Python version:", "Loading model...", "FAISS index not
    found") dibuang; istilah teknikal yang dibenarkan (API, offline,
    model, FAISS) kekal. Terjemahan Indonesia ialah KANDUNGAN, bukan
    komunikasi UI, jadi tidak disentuh.
    """
    tajuk("8h. Bahasa komunikasi: Melayu (kecuali terjemahan)")
    semua = []
    for p in _senarai_py_projek():
        if _bukan_komunikasi(p):
            continue
        semua.append(p)

    bersih = True
    for p in semua:
        jumpa = _semak_bahasa_fail(p)
        if jumpa:
            salah(f"{p} frasa Inggeris: {jumpa}")
            bersih = False

    if bersih:
        lulus(f"{len(semua)} fail .py tiada frasa Inggeris (komunikasi Melayu)")

    # Ralat runtime mentah (sqlite3/requests/OSError) mesti diterjemah
    # ke Melayu sebelum dipapar pengguna -- `terjemah_ralat`.
    try:
        import sqlite3 as _sq3
        from utils.bahasa import terjemah_ralat as TR
        # Exception terbina sahaja (tiada kebergantungan requests di sini);
        # requests.ConnectionError ialah subkelas ConnectionError.
        kes = [
            (_sq3.OperationalError("database is locked"),
             "Pangkalan data sedang dikunci"),
            (_sq3.OperationalError("no such table: hadis"), "Jadual tidak wujud"),
            (_sq3.OperationalError("attempt to write a readonly database"),
             "hanya boleh dibaca"),
            (ConnectionError("Connection refused"), "Sambungan ditolak"),
            (TimeoutError("Read timed out"), "Sambungan tamat masa"),
            (OSError("No such file or directory"), "Fail atau folder tidak dijumpai"),
            (OSError("Permission denied"), "Kebenaran ditolak"),
            # HTTP / API
            (Exception("500 Server Error: Internal Server Error"),
             "Ralat pelayan"),
            (Exception("Expecting value: line 1 column 1"),
             "Respons pelayan tidak sah"),
            # faiss / torch
            (ModuleNotFoundError("No module named 'faiss'"),
             "Pakej faiss tidak dipasang"),
            (MemoryError("CUDA out of memory"), "Memori GPU tidak mencukupi"),
            # Mesej yang sudah Melayu kekal seadanya
            ("Gagal menghubungi pelayan.", "Gagal menghubungi pelayan."),
            ("", "Ralat tidak diketahui."),
        ]
        if all(jangka in TR(masuk) for masuk, jangka in kes):
            lulus(f"terjemah_ralat: {len(kes)} kes ralat runtime -> Melayu")
        else:
            gagal_k = [m for m, j in kes if j not in TR(m)]
            salah(f"terjemah_ralat GAGAL untuk: {gagal_k}")
    except Exception as e:
        salah(f"semak terjemah_ralat: {e}")


def semak_peraturan_bahasa() -> None:
    """Ujian peraturan bahasa: suntik fail, sahkan dikesan, buang.

    Peraturan `_semak_bahasa_fail` mesti menangkap frasa Inggeris dalam
    fail .py BAHARU. Ujian ini mencipta fail ujian dengan frasa
    "Loading model", sahkan ia dilaporkan, kemudian memadam. Kegagalan
    peraturan (tidak dikesan) menyebabkan fail ujian KEKAL dan
    semak_bahasa_ui melaporkannya pada run seterusnya.
    """
    tajuk("8h2. Peraturan bahasa (frasa Inggeris dikesan)")
    ujian = "__uji_peraturan_bahasa__.py"
    laluan = os.path.join(BASE, ujian)
    kekal = False
    try:
        with open(laluan, "w", encoding="utf-8") as f:
            f.write('# fail ujian sementara -- mesti dikesan\n'
                    'print("Loading model: ujian")\n')
        jumpa = _semak_bahasa_fail(laluan)
        if "loading model" in jumpa:
            lulus("frasa Inggeris dalam fail baharu dikesan")
        else:
            salah("frasa Inggeris TIDAK dikesan dalam fail baharu")
            kekal = True
            print("    NOTA: fail ujian dikekalkan supaya semak_bahasa_ui "
                  "melaporkannya pada run seterusnya.")
    finally:
        if not kekal and os.path.exists(laluan):
            os.remove(laluan)


def semak_profil_model() -> None:
    """Profil muat model semantik -- kesan regresi prestasi.

    `core.semantic_search._simpan_profil` menulis masa muat setiap larian
    ke `profil_model.json`. Sesi 25-26 diukur: muat stabil 24-26s
    (import sentence_transformers ~19s adalah had persekitaran
    Windows/antivirus). 80s awal adalah transien larian pertama.
    Ambang amaran: muat >60s menandakan regresi atau persekitaran
    bermasalah -- lapor sebagai GAGAL supaya disiasat.
    """
    tajuk("8j. Profil muat model semantik (regresi prestasi)")
    laluan = os.path.join(BASE, "profil_model.json")
    if not os.path.exists(laluan):
        lulus("profil_model.json belum wujud (belum ada larian muat)")
        return
    try:
        import json as _json
        data = _json.loads(open(laluan, encoding="utf-8").read())
    except Exception as e:
        salah(f"profil_model.json tidak sah: {e}")
        return
    if not isinstance(data, list) or not data:
        salah("profil_model.json kosong / bukan senarai")
        return
    terakhir = data[-1]
    muat = terakhir.get("muat_s") or 0
    import_s = terakhir.get("import_s") or 0
    dari_cache = terakhir.get("dari_cache", True)
    cara = "cache" if dari_cache else "MUAT TURUN HF HUB"
    lulus(f"larian terkini: muat {muat:.1f}s ({cara}, import ST {import_s:.1f}s)")
    # Muat turun pertama dari HF Hub boleh ambil beberapa minit -- BUKAN
    # regresi. Hanya amaran bila muat DARI CACHE >60s.
    if muat > 60 and dari_cache:
        salah(f"muat cache {muat:.1f}s > 60s -- kemungkinan regresi "
              f"prestasi atau persekitaran bermasalah; siasat sebelum hantar")
    # Rujuk ambang stabil supaya regresi besar dapat dikesan (purata 3
    # larian terakhir; langkau rekod muat turun supaya tidak merosakkan
    # purata pada mesin baharu).
    rekod_cache = [r for r in data[-3:] if r.get("dari_cache", True)]
    if len(rekod_cache) >= 3:
        purata = sum(r.get("muat_s", 0) for r in rekod_cache) / 3
        if purata > 60:
            salah(f"purata 3 larian cache terakhir {purata:.1f}s > 60s")
        else:
            lulus(f"purata 3 larian cache terakhir {purata:.1f}s (stabil <60s)")


def _sumber_ui() -> str:
    """Sumber gabungan modul UI untuk semakan teks.

    Selepas refactor Sesi 30, kaedah halaman tinggal dalam mixin
    (ui/pages_kitab.py, ui/pages_carian.py, ui/pages_detail.py,
    ui/pages_tersimpan.py, ui/pages_tetapan.py, ui/pages_home.py) dan
    pemalar atribusi dalam ui/helpers.py. Semakan teks yang dahulu membaca app_qt.py
    sahaja kini mesti melihat semua fail supaya tidak hanyut setiap
    kali fungsi dialih.
    """
    teks = _baca_cek(os.path.join(BASE, "ui", "app_qt.py"))
    for p in ("ui/pages_kitab.py", "ui/pages_rak.py", "ui/pages_carian.py",
              "ui/pages_detail.py", "ui/pages_tersimpan.py",
              "ui/pages_tetapan.py", "ui/pages_home.py",
              "ui/helpers.py"):
        if os.path.exists(p):
            teks += "\n" + _baca_cek(p)
    return teks


def _cari_fungsi(nama: str):
    """Cari nod fungsi dalam mana-mana modul UI (mixin dahulu).

    Pulangkan (sumber, nod AST) atau None. Sebab: selepas refactor,
    `_switch_lang` dsb. tinggal dalam ui/pages_detail.py, bukan
    app_qt.py; semakan AST perlu parse fail yang benar-benar
    mengandunginya.
    """
    for p in ("ui/pages_detail.py", "ui/pages_kitab.py", "ui/pages_rak.py",
              "ui/pages_carian.py", "ui/pages_tersimpan.py",
              "ui/pages_tetapan.py", "ui/pages_home.py",
              "ui/app_qt.py"):
        if not os.path.exists(p):
            continue
        src = _baca_cek(p)
        pokok = ast.parse(src)
        fn = next((n for n in ast.walk(pokok)
                   if isinstance(n, ast.FunctionDef)
                   and n.name == nama), None)
        if fn is not None:
            return src, fn
    return None


def semak_bandingan() -> None:
    """Tab bahasa = 3 (Melayu/Indonesia/English) + teks SAMA PARAS dgn Arab.

    Keputusan mockup Sesi 55: tab "Sebelah" (bandingan Melayu vs
    Indonesia) DIBUANG -- bukan dalam mockup, dan teks terjemahan di
    dalamnya tidak sama paras dengan teks Arab. Tiga tab sahaja; teks
    terjemahan MESTI kekal separas dengan teks Arab di lajur kiri walau
    apa keadaan.
    """
    tajuk("8i. Tab bahasa (3 tab) + teks terjemahan sama paras")
    # LangTabs mesti TIDAK menawarkan tab "sebelah" -- tiga tab sahaja
    # (Melayu/Indonesia/English), sepadan dengan mockup.
    src_page = open("ui/pages.py", encoding="utf-8").read()
    if '("sebelah", "Sebelah")' not in src_page \
            and '("melayu", "Melayu")' in src_page \
            and '("indonesia", "Indonesia")' in src_page \
            and '("english", "English")' in src_page:
        lulus("LangTabs: 3 tab (Melayu/Indonesia/English), TIADA Sebelah")
    else:
        salah("LangTabs mesti 3 tab sahaja -- tab Sebelah DIBUANG")

    # `_switch_lang` TIDAK boleh ada cabang sebelah atau butang
    # "Salin semua bahasa" (semua milik tab Sebelah yang dibuang).
    src_qt = _sumber_ui()
    cari = _cari_fungsi("_switch_lang")
    if cari is None:
        salah("_switch_lang TIADA")
        return
    src_lang, fn = cari
    badan = ast.get_source_segment(src_lang, fn) or ""
    if 'key == "sebelah"' not in badan and "Salin semua bahasa" not in badan:
        lulus("_switch_lang: TIADA cabang sebelah / Salin semua bahasa")
    else:
        salah("cabang sebelah / Salin semua bahasa masih wujud -- patut "
              "dibuang")

    # "Salin semua bahasa" (_copy_semua_bahasa/_teks_semua_bahasa) ikut
    # tab Sebelah -- mesti dibuang sekali (bukan dalam mockup).
    if "_copy_semua_bahasa" not in src_qt and "_teks_semua_bahasa" not in src_qt:
        lulus("Salin semua bahasa dibuang (tiada tab Sebelah)")
    else:
        salah("_copy_semua_bahasa/_teks_semua_bahasa masih wujud")

    # Sesi 34: "Kongsi semua bahasa" DIBUANG -- pengguna kongsi mengikut
    # bahasa semasa sahaja (WhatsApp). Pastikan butang lama + fungsi
    # _share_semua_bahasa TIDAK kembali.
    if "Kongsi semua bahasa" not in badan and "_share_semua_bahasa" not in src_qt:
        lulus("Kongsi semua bahasa dibuang (kongsi ikut bahasa semasa)")
    else:
        salah("Kongsi semua bahasa masih wujud -- patut dibuang")

    # SAMA PARAS (keputusan mockup Sesi 55, ditegaskan semula): Qt
    # memusatkan widget saiz tetap dalam QVBoxLayout bila ada ruang lebih,
    # jadi teks terjemahan jatuh ke tengah -- tidak sama paras dengan teks
    # Arab. `_switch_lang` mesti AlignTop + addStretch (ruang berlebihan
    # tinggal DI BAWAH teks, bukan memusatkannya).
    if "Qt.AlignTop" in badan and "addStretch" in badan:
        lulus("paparan tunggal: teks terjemahan AlignTop + stretch bawah")
    else:
        salah("paparan tunggal mesti AlignTop + addStretch supaya sama "
              "paras dengan teks Arab")

    # Keputusan mockup (Sesi 55): paparan bahasa tunggal = TAB + teks
    # SAHAJA. Label LANG_LABEL dan baris butang Salin/Kongsi TIDAK boleh
    # wujud di bawah tab lajur terjemahan -- ia menolak teks terjemahan
    # ke bawah sehingga tidak sama paras dengan teks Arab di lajur kiri.
    # Tindakan kekal di bar tajuk (Kongsi = WhatsApp bahasa semasa, Salin)
    # dan menu klik kanan. Tab Sebelah ("Salin semua bahasa") kekal.
    if 'lbl = QLabel(LANG_LABEL.get(key, key.upper()))' not in badan:
        lulus("paparan tunggal TIADA label LANG_LABEL di bawah tab")
    else:
        salah("label LANG_LABEL kembali di bawah tab -- teks terjemahan "
              "jatuh ke bawah, tidak sama paras dengan Arab")
    if ('QPushButton("📋 Salin")' not in badan
            and 'QPushButton("💬 Kongsi")' not in badan):
        lulus("paparan tunggal TIADA baris Salin/Kongsi di bawah tab")
    else:
        salah("butang Salin/Kongsi kembali di bawah tab paparan tunggal "
              "-- teks terjemahan jatuh ke bawah")
    # _teks_bahasa_semasa ialah fungsi BERASINGAN -- semak pada sumber penuh.
    if "_teks_bahasa_semasa" in src_qt:
        lulus("Salin/Kongsi bahasa semasa berkongsi _teks_bahasa_semasa")
    else:
        salah("_teks_bahasa_semasa TIADA")
    # Kongsi WhatsApp (Sesi 36) TERUS guna format "Ringkas" -- keputusan
    # pengguna: TIADA menu pilihan (sebelum ini QMenu 4 format). Fungsi
    # petikan lama TIDAK kembali; format "Terjemahan sahaja" / "Arab
    # sahaja" dibuang (corak sama Sesi 34 buang "Kongsi semua bahasa").
    cari = _cari_fungsi("_share_bahasa_semasa")
    kongsi_langsung = False
    if cari is not None:
        badan_s = ast.get_source_segment(cari[0], cari[1]) or ""
        kongsi_langsung = ("_teks_kongsi_ringkas" in badan_s
                           and "QMenu" not in badan_s)
    if ("_petik_arab" not in src_qt and "[TERJEMAHAN]" in src_qt
            and "_teks_kongsi_ringkas" in src_qt
            and "_petik_ringkas" in src_qt
            and kongsi_langsung
            and "_teks_terjemahan_sahaja" not in src_qt
            and "_teks_arab_sahaja" not in src_qt):
        lulus("kongsi WhatsApp terus guna Ringkas (tiada menu pilihan)")
    else:
        salah("kongsi WhatsApp tidak ikut spesifikasi (terus Ringkas, format lain dibuang)")
    # Kongsi Ringkas sertakan pautan "Baca penuh" sunnah.com bila padanan
    # wujud (Sesi 36). `sunnah_url` (ui/helpers.py) dibina daripada peta
    # sunnah_map/ yang dijana bina_peta_sunnah.py -- nombor hadis hadis.my
    # berbeza daripada nombor global sunnah.com, jadi peta diperlukan.
    if "sunnah_url" in src_qt and "Baca penuh:" in src_qt \
            and "_SUNNAH_SLUG" in src_qt:
        lulus("kongsi Ringkas sertakan pautan 'Baca penuh' (sunnah.com)")
    else:
        salah("pautan 'Baca penuh' sunnah.com TIADA dalam kongsi Ringkas")


def semak_pemula() -> None:
    """Skrin pemula (splash) — sekarang hanya untuk notis/disclaimer.
    Model AI dimuat MALAS (Lazy Loading) pada carian makna pertama,
    bukan pada startup. Splash model loading DITANGGALKAN.
    """
    tajuk("8k. Skrin pemula (splash) — notis sahaja")
    # ui/splash.py masih wujud (boleh guna untuk notis lain)
    if os.path.exists("ui/splash.py"):
        src_sp = open("ui/splash.py", encoding="utf-8").read()
        if "class SplashPermula" in src_sp and "def set_fasa" in src_sp:
            lulus("ui/splash.py: SplashPermula + set_fasa (notis)")
        else:
            salah("ui/splash.py rosak: SplashPermula/set_fasa TIADA")
    else:
        salah("ui/splash.py TIADA")
    # PreloadWorker DITANGGALKAN dari startup (Lazy Loading)
    # SemanticWorker memuat model pada carian makna pertama
    src_w = open("ui/workers.py", encoding="utf-8").read()
    if "model_loading_started = pyqtSignal" in src_w \
            and "model_loading_started.emit" in src_w:
        lulus("SemanticWorker: signal model_loading_started (Lazy Load)")
    else:
        salah("SemanticWorker TIADA signal model_loading_started")
    # PustakaApp TIDAK lagi memancarkan isyarat pramuat model
    src_qt = open("ui/app_qt.py", encoding="utf-8").read()
    if "_mula_pramuat" not in src_qt and "_on_pramuat_siap" not in src_qt:
        lulus("PustakaApp: _mula_pramuat/_on_pramuat_siap DITANGGAL (Lazy Load)")
    else:
        salah("PustakaApp masih ada _mula_pramuat/_on_pramuat_siap (lama)")
    # main.py TIDAK lagi menyambung splash untuk pramuat model
    src_main = open("main.py", encoding="utf-8").read()
    if "SplashPermula" not in src_main and "kemajuan_pramuat.connect" not in src_main:
        lulus("main.py: tiada splash pramuat model (Lazy Load)")
    else:
        salah("main.py masih ada integrasi splash pramuat (lama)")
    # Kaedah mati _pra_muat_model mesti tidak wujud
    if "_pra_muat_model" in src_qt:
        salah("app_qt: kaedah mati _pra_muat_model kembali (thread utama crash)")
    else:
        lulus("app_qt: kaedah mati _pra_muat_model tidak wujud")


def semak_padanan_eng() -> None:
    """Pengesahan dua hala pada lapisan padanan `kata`.

    Skor sehala membenarkan hadis yang TIADA dalam sumber dipadan
    kepada hadis lain yang berkongsi sanad panjang. Diukur pada
    Bukhari: 35.3% positif palsu tanpa Jaccard, 5.2% dengan 0.90.

    Ujian ini guna korpus sintetik (tiada rangkaian) -- ia mengesahkan
    MEKANISME, bukan angka Bukhari sebenar.
    """
    tajuk("8c. Padanan Inggeris — pengesahan dua hala")
    sys.path.insert(0, BASE)
    try:
        from core.eng_source import (JACCARD_MIN, _bina_indeks_kata,
                                     padan_kata)
    except Exception as e:
        salah(f"import core.eng_source: {e}")
        return

    if not (0.0 < JACCARD_MIN <= 1.0):
        salah(f"JACCARD_MIN di luar julat: {JACCARD_MIN}")
        return
    lulus(f"JACCARD_MIN = {JACCARD_MIN}")

    # Sanad panjang yang DIKONGSI + matn yang BERBEZA sepenuhnya.
    sanad = ("حدثنا عبد الله بن يوسف قال اخبرنا مالك عن ابن شهاب "
             "عن ابي سلمه بن عبد الرحمن عن ابي هريره رضي الله عنه ")
    sumber = {
        1: sanad + "قال قال رسول الله صلي الله عليه وسلم من صام رمضان ايمانا واحتسابا غفر له ما تقدم من ذنبه",
        2: sanad + "قال نهي النبي صلي الله عليه وسلم عن بيع الغرر وعن بيع الحصاه في السوق",
        3: "حدثنا مسدد قال حدثنا يحيي عن شعبه عن قتاده عن انس رضي الله عنه ان النبي صلي الله عليه وسلم قال لا يومن احدكم حتي يحب لاخيه ما يحب لنفسه",
    }
    ik = _bina_indeks_kata({}, sumber)

    # (a) hadis YATIM: sanad sama, matn lain sama sekali -> mesti DITOLAK
    yatim = sanad + "قال كان النبي صلي الله عليه وسلم يعتكف العشر الاواخر من شهر رمضان حتي توفاه الله"
    if padan_kata(yatim, ik, teks_sumber=sumber) is None:
        lulus("hadis yatim (sanad dikongsi) ditolak")
    else:
        salah("hadis yatim DIPADAN — pengesahan dua hala tidak berkuat kuasa")

    # (b) hadis TULEN mesti tetap dipadan
    if padan_kata(sumber[3], ik, teks_sumber=sumber) == 3:
        lulus("hadis tulen masih dipadan")
    else:
        salah("hadis tulen HILANG — ambang terlalu ketat")

    # (ba) lapisan Indonesia mesti didahulukan dan tepat
    try:
        from core.eng_source import bina_indeks_ind, kunci_indonesia, padan
        k1 = kunci_indonesia("Telah menceritakan kepada kami [Malik] dari Nafi'.")
        k2 = kunci_indonesia("telah menceritakan kepada kami Malik dari Nafi")
        if k1 == k2:
            lulus("kunci_indonesia abai kurungan/tanda baca/saiz huruf")
        else:
            salah(f"kunci_indonesia tidak stabil: {k1!r} vs {k2!r}")

        idx = {kunci_indonesia("Rasulullah bersabda tentang niat"): 77}
        no, cara = padan("teks arab tidak dikenali", {}, {}, None,
                         ind_hadis_my="Rasulullah bersabda tentang niat",
                         indeks_ind=idx)
        if no == 77 and cara == "indo":
            lulus("lapisan `indo` didahulukan dan mengembalikan nombor")
        else:
            salah(f"lapisan indo gagal: no={no} cara={cara}")
    except Exception as e:
        salah(f"lapisan Indonesia: {e}")

    # (bc) lapisan Indonesia KABUR: selamatkan beza remeh, tolak asing
    try:
        from core.eng_source import (JACCARD_IND, bina_indeks_ind_kata,
                                     padan_ind_kabur)
        ti = {
            10: "Rasulullah bersabda barangsiapa menipu maka bukan golongan kami",
            11: "Beliau melarang jual beli gharar dan melempar batu di pasar",
            12: "Puasa Ramadan dengan iman dan mengharap pahala menghapus dosa",
        }
        ikk = bina_indeks_ind_kata(ti)
        # (i) beza tanda baca/kurungan sahaja -> mesti DIPADAN
        usik = "[Rasulullah] bersabda: barangsiapa menipu, maka bukan golongan kami!"
        if padan_ind_kabur(usik, ikk, ti) == 10:
            lulus("indo~ selamatkan beza tanda baca/kurungan")
        else:
            salah("indo~ gagal padan teks yang hanya beza tanda baca")
        # (ii) hadis ASING -> mesti DITOLAK
        asing = "Zakat fitrah satu sha kurma atau gandum sebelum solat ied"
        if padan_ind_kabur(asing, ikk, ti) is None:
            lulus("indo~ tolak hadis asing")
        else:
            salah("indo~ memadan hadis asing — ambang terlalu longgar")
        if JACCARD_IND >= 0.90:
            lulus(f"JACCARD_IND = {JACCARD_IND}")
        else:
            salah(f"JACCARD_IND terlalu rendah: {JACCARD_IND}")
    except Exception as e:
        salah(f"lapisan indo~: {e}")

    # (bb) alat audit bebas mesti wujud dan boleh diimport
    try:
        from audit_eng import SYAK, jaccard, tokens
        t1 = tokens("Telah menceritakan kepada kami Abdullah tentang solat subuh")
        t2 = tokens("Telah menceritakan kepada kami Abdullah tentang solat subuh")
        t3 = tokens("Rasulullah melarang jual beli gharar dan penipuan pasar")
        if jaccard(t1, t2) >= 0.99 and jaccard(t1, t3) < SYAK:
            lulus("audit_eng.py membezakan padanan betul vs salah")
        else:
            salah(f"audit_eng.py tidak membezakan: sama={jaccard(t1,t2):.2f} "
                  f"beza={jaccard(t1,t3):.2f}")
    except Exception as e:
        salah(f"import audit_eng: {e}")

    # (c) sync mesti PADAM baris lama, bukan hanya REPLACE -- jika
    #     tidak, terjemahan salah daripada larian lama kekal dalam DB.
    p = os.path.join(BASE, "sync_english.py")
    if os.path.exists(p):
        with open(p, encoding="utf-8") as fh:
            src = fh.read()
        if "DELETE FROM terjemahan_eng WHERE collection" in src:
            lulus("sync_english.py memadam baris lama sebelum simpan")
        else:
            salah("sync_english.py hanya REPLACE — baris salah lama kekal")

    # (d) teks_sumber mesti benar-benar dihantar oleh pemanggil
    for f in ("sync_english.py", "diagnos_padanan.py"):
        p = os.path.join(BASE, f)
        if not os.path.exists(p):
            continue
        with open(p, encoding="utf-8") as fh:
            src = fh.read()
        if "teks_sumber" in src:
            lulus(f"{f} menghantar teks_sumber")
        else:
            salah(f"{f} memanggil padan() TANPA teks_sumber "
                  f"— pengesahan dua hala dilangkau senyap")


def semak_hadeethenc() -> None:
    """HadeethEnc — padanan matn (sumber arkib).

    HadeethEnc ialah huraian Melayu SEBENAR untuk hadis yang dipadan.
    Padanan dibuat melalui MATN Arab (bukan nombor) kerana penomboran
    hadis.my dan HadeethEnc tidak sejajar. Ambang JACCARD_MATN diukur:
    betul 0.62-1.00, salah 0.04-0.48 -- 0.55 selamat di tengah.
    Sejak v1.1 HadeethEnc dipapar semula dalam UI sebagai SANDRAN
    untuk hadis yang tiada huraian SemakHadis (baca melalui
    `api.hadis_api.bina_huraian_he`); padanan matn ini juga kekal
    sebagai semakan integriti `core.hadeethenc_api`.
    """
    tajuk("8e. HadeethEnc — padanan matn")
    sys.path.insert(0, BASE)
    try:
        from core.hadeethenc_api import (JACCARD_MATN, _matn, bina_indeks,
                                         padan)
    except Exception as e:
        salah(f"import core.hadeethenc_api: {e}")
        return

    if not (0.45 <= JACCARD_MATN <= 0.65):
        salah(f"JACCARD_MATN di luar julat 0.45-0.65: {JACCARD_MATN}")
    else:
        lulus(f"JACCARD_MATN = {JACCARD_MATN}")

    # (a) `_matn` mesti MENANGGALKAN sanad. Sanad hadis.my dan
    #     HadeethEnc berbeza sepenuhnya; jika sanad dikira, padanan
    #     mati. Ujian: teks dengan sanad panjang + matn pendek.
    sanad = ("حدثنا عبد الله بن يوسف قال اخبرنا مالك عن هشام بن عروة "
             "عن ابيه عن عائشة رضي الله عنها ان رسول الله صلى الله عليه وسلم "
             "قال بروا من امي ثلاثا ثم هو لهم صدقة")
    if "عروة" not in _matn(sanad):
        lulus("_matn menanggalkan sanad")
    else:
        salah("_matn TIDAK menanggalkan sanad — padanan akan tersilap")

    # (b) padanan mesti TOLAK hadis yang tiada dalam sumber. Korpus
    #     sintetik: dua hadis, matn jelas berbeza, kunci sama.
    sumber = {
        1: "قال رسول الله صلى الله عليه وسلم من صام رمضان ايمانا واحتسابا غفر له ما تقدم من ذنبه",
        2: "قال النبي صلى الله عليه وسلم لا يومن احدكم حتي يحب لاخيه ما يحب لنفسه",
    }
    ind = bina_indeks
    teks, matn, kira, peta = {}, {}, {}, {}
    for hid, ar in sumber.items():
        na = _matn(ar)
        teks[hid], matn[hid] = na, na
    ind2 = {"teks": teks, "matn": matn,
            "indeks": {}, "kira": kira}

    # hadis TULEN mesti dipadan
    if padan(sumber[1], ind2) == (1, 1.0, "penuh"):
        lulus("hadis tulen dipadan (teks penuh sama)")
    else:
        salah("hadis tulen tidak dipadan")

    # hadis ASING yang berkongsi pembukaan matn mesti DITOLAK
    asing = "قال رسول الله صلى الله عليه وسلم من قال سبحان الله العظيم ادخل الجنة"
    if padan(asing, ind2) is None:
        lulus("hadis asing ditolak")
    else:
        salah("hadis asing DIPADAN — ambang terlalu longgar")

    # (c) sync_hadeethenc.py mesti memadam baris lama, bukan hanya REPLACE
    p = os.path.join(BASE, "sync_hadeethenc.py")
    if os.path.exists(p):
        with open(p, encoding="utf-8") as fh:
            src = fh.read()
        if "DELETE FROM hadethenc WHERE collection" in src:
            lulus("sync_hadeethenc.py memadam baris lama sebelum simpan")
        else:
            salah("sync_hadeethenc.py hanya REPLACE — baris salah lama kekal")
    else:
        salah("sync_hadeethenc.py TIADA")

    # (d) Integrasi UI (v1.1): API mesti membekalkan sandaran HadeethEnc
    #     dan UI mesti memaparkannya bila SemakHadis tiada. Kaedah
    #     `_bina_he` kini dalam ui/pages_detail.py dan pemalar
    #     `_ATRIBUSI_HE` dalam ui/helpers.py (refactor Sesi 30) --
    #     semak sumber gabungan supaya tidak hanyut.
    try:
        from api.hadis_api import HadisAPI, bina_huraian_he
        if hasattr(HadisAPI, "_he") and hasattr(HadisAPI, "_he_luar") \
                and callable(bina_huraian_he):
            lulus("HadisAPI._he / _he_luar + bina_huraian_he wujud")
        else:
            salah("HadisAPI._he / _he_luar / bina_huraian_he TIADA")
    except Exception as e:
        salah(f"import api.hadis_api: {e}")

    p_ui = os.path.join(BASE, "ui", "app_qt.py")
    if os.path.exists(p_ui):
        src = _sumber_ui()
        if "_he_luar" in src and "HadeethEnc" in src and "_bina_he" in src:
            lulus("UI memaparkan sandaran HadeethEnc")
        else:
            salah("UI TIDAK memaparkan sandaran HadeethEnc")
        # Atribusi HadeethEnc mesti melalui pemalar tunggal (konsisten
        # dengan _ATRIBUSI_SEMA / _ATRIBUSI_INGGERIS).
        if "_ATRIBUSI_HE" in src:
            lulus("atribusi HadeethEnc melalui pemalar _ATRIBUSI_HE")
        else:
            salah("atribusi HadeethEnc TIDAK melalui pemalar")
    else:
        salah("ui/app_qt.py TIADA")


def semak_sema() -> None:
    """Fasa 4 SemakHadis — padanan matn + integrasi UI.

    SemakHadis.com ialah huraian Bahasa Melayu SEBENAR (terjemahan +
    komentar + status). Padanan dibuat melalui MATN Arab (bukan nombor)
    kerana penomboran berbeza. Ambang JACCARD_MATN sama seperti
    HadeethEnc; calon kedua yang terlalu rapat DITOLAK.
    """
    tajuk("8f. SemakHadis — padanan matn + integrasi")
    sys.path.insert(0, BASE)
    try:
        from core.sema_source import (JACCARD_MATN, bina_indeks, padan,
                                      matn_bersih, _norm)
    except Exception as e:
        salah(f"import core.sema_source: {e}")
        return

    if not (0.45 <= JACCARD_MATN <= 0.65):
        salah(f"JACCARD_MATN di luar julat 0.45-0.65: {JACCARD_MATN}")
    else:
        lulus(f"JACCARD_MATN = {JACCARD_MATN}")

    # (a) matn_bersih mesti buang penanda umum supaya padanan membanding
    #     isi hadis, bukan pembukaan sanad yang berbeza antara sumber.
    mt = matn_bersih("قال رسول الله صلي الله عليه وسلم من صام رمضان ايمانا واحتسابا")
    if mt.startswith("من صام"):
        lulus("matn_bersih buang penanda umum")
    else:
        salah(f"matn_bersih tidak buang penanda: {mt[:40]}")

    # (b) padanan mesti TOLAK hadis yang tiada dalam sumber. Korpus
    #     sintetik: dua hadis, matn jelas berbeza, kunci sama.
    sumber = {
        "s1": "من صام رمضان ايمانا واحتسابا غفر له ما تقدم من ذنبه",
        "s2": "لا يومن احدكم حتي يحب لاخيه ما يحب لنفسه",
    }
    matn = {sid: set(_norm(ar).split()) for sid, ar in sumber.items()}
    peta: dict[str, set[str]] = {}
    for sid, kata in matn.items():
        for w in kata:
            if len(w) >= 3:
                peta.setdefault(w, set()).add(sid)
    ind2 = {"data": {}, "matn": matn, "indeks": peta}

    # hadis TULEN mesti dipadan
    r = padan("قال رسول الله صلى الله عليه وسلم " + sumber["s1"], ind2)
    if r and r[0] == "s1" and r[1] >= JACCARD_MATN:
        lulus("hadis tulen dipadan")
    else:
        salah(f"hadis tulen tidak dipadan: {r}")

    # hadis ASING yang berkongsi pembukaan matn mesti DITOLAK
    asing = "قال النبي صلى الله عليه وسلم من قال سبحان الله العظيم ادخل الجنة"
    if padan(asing, ind2) is None:
        lulus("hadis asing ditolak")
    else:
        salah("hadis asing DIPADAN — ambang terlalu longgar")

    # (c) sync_sema.py mesti memadam baris lama, bukan hanya REPLACE
    p = os.path.join(BASE, "sync_sema.py")
    if os.path.exists(p):
        with open(p, encoding="utf-8") as fh:
            src = fh.read()
        if "DELETE FROM semakhadis WHERE collection" in src:
            lulus("sync_sema.py memadam baris lama sebelum simpan")
        else:
            salah("sync_sema.py hanya REPLACE — baris salah lama kekal")
    else:
        salah("sync_sema.py TIADA")

    # (d) jadual semakhadis mesti wujud selepas migrasi, dan API mesti
    #     mendedahkan huraian SemakHadis melalui get_hadis_by_id.
    import tempfile as _tf
    _tmp_db = os.path.join(_tf.mkdtemp(), "semak_sema.db")
    try:
        from db import init as _init
        c = _init(_tmp_db)
        kol = [r[1] for r in c.execute("PRAGMA table_info(semakhadis)")]
        perlu = {"collection", "hadis_id", "sema_id", "jaccard",
                 "klasifikasi", "tajuk", "malay_text", "intro", "syarah"}
        if perlu.issubset(kol):
            lulus("jadual semakhadis lengkap (migrasi v7)")
        else:
            salah(f"jadual semakhadis hilang kolum: {perlu - set(kol)}")
    except Exception as e:
        salah(f"semak jadual semakhadis: {e}")

    src_api = open("api/hadis_api.py", encoding="utf-8").read()
    if "_sema_luar" in src_api and '"sema"' in src_api:
        lulus("API mendedahkan huraian SemakHadis")
    else:
        salah("API tidak mendedahkan medan sema")

    # (e) UI mesti papar huraian SemakHadis sebagai Collapsible terbuka.
    #     `_bina_sema` kini dalam ui/pages_detail.py, `_ATRIBUSI_SEMA`
    #     dalam ui/helpers.py (refactor Sesi 30) -- semak sumber gabungan.
    src_qt = _sumber_ui()
    if "Huraian (SemakHadis" in src_qt and "_bina_sema" in src_qt:
        lulus("UI papar huraian SemakHadis")
    else:
        salah("UI tiada bahagian huraian SemakHadis")

    # (f) lesen mesti dipaparkan — kandungan milik SemakHadis.com, dan
    #     atribusi mesti melalui pemalar tunggal supaya tidak hanyut.
    if "SemakHadis.com" in src_qt and "_ATRIBUSI_SEMA" in src_qt:
        lulus("atribusi SemakHadis.com dipaparkan (pemalar _ATRIBUSI_SEMA)")
    else:
        salah("UI tiada atribusi SemakHadis.com / pemalar _ATRIBUSI_SEMA")

    # (g) Teks Melayu semakhadis mesti melalui _papar_melayu -- konsisten
    #     dengan paparan hadis utama (ejaan DBP + simbol selawat), bukan
    #     papar mentah. Penukaran pada teks PENUH dahulu, potong kemudian.
    m_sema = re.search(r"def _bina_sema.*?(?=\n    def )", src_qt, re.S)
    badan_sema = m_sema.group(0) if m_sema else ""
    # Bentuk PANGGILAN (bukan sebutan dalam docstring) -- supaya regresi
    # yang hanya meninggalkan nama dalam komen tidak terlepas.
    if "self._papar_melayu(" in badan_sema:
        lulus("_bina_sema guna _papar_melayu (ejaan DBP + selawat)")
    else:
        salah("_bina_sema TIADA _papar_melayu -- semakhadis papar mentah")


def semak_gabungan() -> None:
    """Carian gabungan — fallback OR + mesej bantuan kata kunci kosong.

    Kes "hukum riba": FTS5 AND memerlukan SEMUA perkataan hadir, jadi
    carian yang setiap perkataannya wujud berasingan boleh pulang 0 hasil
    walaupun hadis berkaitan wujud. Dua lapisan penyelesaian (v1.2):
      (1) FALLBACK OR -- enjin cuba OR bila AND 0 hasil supaya kad keyword
          tetap dipapar (meta.fallback ditanda; UI papar nota "carian
          longgar");
      (2) MESEJ BANTUAN -- bila keyword 0 hasil (OR pun) tetapi AI ada
          padanan makna, UI memberitahu pengguna mengapa kad kata kunci
          kosong dan mengarahkan perhatian ke padanan makna di bawah.
    """
    tajuk("8g. Carian gabungan — fallback OR + mesej bantuan kata kunci")
    # Sesi 30 refactor: _tampal_gabungan dipindah ke ui/pages_carian.py.
    p_ui = os.path.join(BASE, "ui", "pages_carian.py")
    if not os.path.exists(p_ui):
        salah("ui/pages_carian.py TIADA")
        return
    src = open(p_ui, encoding="utf-8").read()

    marker = "Tiada padanan kata kunci yang mengandungi SEMUA"
    if marker not in src:
        salah("mesej bantuan kata kunci kosong TIADA")
        return

    # Mesej mesti berada dalam _tampal_gabungan, bukan halaman lain.
    pokok = ast.parse(src)
    fn = next((n for n in ast.walk(pokok)
               if isinstance(n, ast.FunctionDef)
               and n.name == "_tampal_gabungan"), None)
    if fn is None:
        salah("_tampal_gabungan TIADA")
        return
    badan = ast.get_source_segment(src, fn) or ""
    if marker not in badan:
        salah("mesej bantuan di luar _tampal_gabungan")
        return

    # Hanya dipapar bila kata kunci 0 hasil DAN AI ada hasil (cabang `if sem:`).
    if "not kw and not meta.get(\"total\")" in badan:
        lulus("mesej hanya bila kata kunci 0 hasil")
    else:
        salah("syarat kata kunci 0 hasil TIDAK ditemui")

    # Mesej mesti membimbing ke hasil AI yang ada di bawah.
    if "Padanan makna (AI)" in badan:
        lulus("mesej mengarah ke padanan makna (AI)")
    else:
        salah("mesej tidak mengarah ke hasil AI")

    # Mesej mesti berada dalam cabang `if sem:` -- tiada nota keliru
    # bila tiada langsung hasil. Cari nod If dengan ujian `sem` melalui
    # AST (bukan split teks -- "else:" dalam string/komen boleh menipu).
    if_sem = next((n for n in ast.walk(fn)
                   if isinstance(n, ast.If)
                   and isinstance(n.test, ast.Name)
                   and n.test.id == "sem"), None)
    if if_sem is None:
        salah("cabang `if sem:` TIADA dalam _tampal_gabungan")
    elif marker in (ast.get_source_segment(src, if_sem) or ""):
        lulus("mesej dalam cabang AI ada hasil")
    else:
        salah("mesej di luar cabang hasil AI")

    # (v1.2) Fallback OR: bila FTS5 AND pulang 0 hasil, enjin mesti cuba
    # OR supaya kad keyword tetap dipapar (kes "hukum riba"), dan UI
    # mesti memaparkan nota "carian longgar" agar pengguna faham hasil
    # di bawah mengandungi mana-mana satu perkataan, bukan SEMUA.
    try:
        from db import _to_match_query
        if " OR " in _to_match_query("hukum riba", "OR"):
            lulus("db._to_match_query sokong gabung OR")
        else:
            salah("db._to_match_query tidak menyokong gabung OR")
    except Exception as e:
        salah(f"semak db._to_match_query: {e}")

    p_api = os.path.join(BASE, "api", "hadis_api.py")
    if os.path.exists(p_api):
        with open(p_api, encoding="utf-8") as fh:
            src_api = fh.read()
        if "_to_match_query(query, \"OR\")" in src_api \
                and 'meta["fallback"] = True' in src_api:
            lulus("search_hadis fallback OR + tanda meta.fallback")
        else:
            salah("search_hadis TIADA fallback OR / tanda fallback")
    else:
        salah("api/hadis_api.py TIADA")

    if "Carian kata kunci longgar" in src and 'meta.get("fallback")' in src:
        lulus("UI papar nota carian longgar (fallback)")
    else:
        salah("UI TIADA nota carian longgar")

    # Ujian DB SINTETIK (tidak bergantung pada hadis.db edaran): bina DB
    # FTS5 kecil, isi hadis contoh, dan sahkan fallback OR berfungsi serta
    # ranking pembobotan meletakkan hadis dengan LEBIH BANYAK perkataan
    # padan di atas. Query 3 perkataan ("hukum riba faedah"): AND=0
    # (tiada hadis ada ketiga-tiganya) tetapi OR pulang 3; hadis #1
    # mengandungi 2 perkataan ('hukum'+'riba') mesti di ATAS hadis
    # satu-perkataan (#2 'faedah', #3 'riba').
    import tempfile as _tf
    tmp_db = os.path.join(_tf.mkdtemp(), "gabungan.db")
    try:
        import db as _db
        c = _db.init(tmp_db)
        c.execute("INSERT INTO collections(slug,name) VALUES('c','C')")
        c.executemany(
            "INSERT INTO hadis(collection,hadis_id,arab,melayu,indonesia) "
            "VALUES('c',?,?,?,?)",
            [
                (1, "a1", "hukum riba dalam hutang", "hukum riba hutang"),
                (2, "a2", "faedah menabung", "faedah menabung"),
                (3, "a3", "riba haram", "riba haram"),
            ],
        )
        c.commit()

        # AND 3-perkataan mesti 0 hasil; fallback OR mesti pulang hadis.
        and_n = c.execute(
            "SELECT COUNT(*) FROM hadis_fts WHERE hadis_fts MATCH ?",
            ('"hukum" AND "riba" AND "faedah"*',)).fetchone()[0]
        rows, total = _db.search(c, "hukum riba faedah")
        if and_n == 0 and total >= 1:
            lulus(f"fallback OR DB sintetik: AND=0 -> OR {total} hasil")
        else:
            salah(f"fallback OR DB sintetik: AND={and_n}, OR={total}")

        # Ranking pembobotan: hadis #1 (2 perkataan) mesti di ATAS.
        if rows and rows[0]["hadis_id"] == 1:
            lulus("pembobotan: hadis lebih banyak perkataan di atas")
        else:
            teratas = rows[0]["hadis_id"] if rows else "-"
            salah(f"pembobotan GAGAL: teratas #{teratas}, jangka #1")
        c.close()
    except Exception as e:
        salah(f"semak fallback DB sintetik: {e}")

    # Ujian data sebenar: "hukum riba" mesti pulang hasil sekarang
    # (sebelum ini 0 hasil FTS5). Jangan jalankan jika DB tiada.
    if os.path.exists(os.path.join(BASE, "hadis.db")):
        try:
            import sqlite3 as _sq
            c = _sq.connect(os.path.join(BASE, "hadis.db"))
            r = c.execute(
                "SELECT COUNT(*) FROM hadis_fts WHERE hadis_fts MATCH ?",
                ('"hukum" OR "riba"*',)).fetchone()[0]
            c.close()
            if r > 0:
                lulus(f"fallback OR 'hukum riba' pulang {r} hasil")
            else:
                salah("fallback OR 'hukum riba' 0 hasil")
        except Exception as e:
            salah(f"semak fallback data: {e}")


def semak_carian_sibuk() -> None:
    """Indikator jam berputar semasa carian (Sesi 30, komit 0c1e037).

    `_page_search` mesti mencipta label `_carian_sibuk` (emoji jam) dan
    `QTimer` yang memutar 12 muka jam melalui `_putar_jam`; `_do_search`
    mesti menunjukkan + memulakan timer; `_tampal_gabungan` mesti
    menyembunyikan + memberhentikan timer supaya jam tidak berputar
    selepas carian selesai; `_on_search_failed` mesti melengkapkan
    paparan (ikutan laluan gagal) supaya jam tidak tersangkut.
    """
    tajuk("8l. Indikator jam berputar semasa carian")
    p_ui = os.path.join(BASE, "ui", "pages_carian.py")
    if not os.path.exists(p_ui):
        salah("ui/pages_carian.py TIADA")
        return
    src = open(p_ui, encoding="utf-8").read()
    pokok = ast.parse(src)

    def badan(nama: str) -> str:
        fn = next((n for n in ast.walk(pokok)
                   if isinstance(n, ast.FunctionDef)
                   and n.name == nama), None)
        return ast.get_source_segment(src, fn) or "" if fn else ""

    # 1) Label jam + QTimer dicipta dalam _page_search
    bs = badan("_page_search")
    if "_carian_sibuk" in bs and "_carian_timer" in bs:
        lulus("_page_search mencipta label jam + QTimer")
    else:
        salah("_carian_sibuk/_carian_timer TIADA dalam _page_search")
        return

    # 2) 12 muka jam (🕐..🕛) + kaedah putaran
    if '"🕐"' in src and '"🕛"' in src and "_putar_jam" in src:
        lulus("12 muka jam + _putar_jam wujud")
    else:
        salah("muka jam/putar_jam TIADA")

    # 3) _do_search menunjukkan + memulakan timer (carian berjalan)
    bd = badan("_do_search")
    if "_carian_sibuk.show()" in bd and "_carian_timer.start()" in bd:
        lulus("_do_search menunjukkan jam + memulakan timer")
    else:
        salah("show()/start() TIADA dalam _do_search")

    # 4) _tampal_gabungan menyembunyikan + memberhentikan timer (selesai)
    bt = badan("_tampal_gabungan")
    if "_carian_sibuk.hide()" in bt and "_carian_timer.stop()" in bt:
        lulus("_tampal_gabungan menyembunyikan + memberhentikan timer")
    else:
        salah("hide()/stop() TIADA dalam _tampal_gabungan")

    # 5) Laluan gagal: _kw_res=[] supaya paparan gabungan tamat
    bf = badan("_on_search_failed")
    if "_kw_res = []" in bf:
        lulus("laluan gagal kata kunci melengkapkan carian")
    else:
        salah("_on_search_failed/_kw_res=[] TIADA")

    # 6) Ujian visual kekal wujud (uji_visual_carian.py)
    p_uji = os.path.join(BASE, "uji_visual_carian.py")
    if not os.path.exists(p_uji):
        salah("uji_visual_carian.py TIADA — jam berputar tanpa ujian visual kekal")
        return
    lulus("uji_visual_carian.py wujud")

    # 7) Ujian visual konsisten dengan pelaksanaan: mesti merujuk nama
    # widget/timer, 12 muka jam, render tetingkap (grab) dan kitaran hidup
    # carian sebenar. Kalau pelaksanaan dinamakan semula dan ujian tidak
    # diikuti, penanda ini hilang -- suite utama menandakan.
    usrc = open(p_uji, encoding="utf-8").read()
    wajib = ("_carian_sibuk", "_carian_timer", '"🕐"', '"🕛"',
             "w.grab()", "_do_search", "isVisible()")
    hilang = [m for m in wajib if m not in usrc]
    if hilang:
        salah(f"uji_visual_carian.py tidak konsisten: tiada {hilang}")
        return
    lulus("uji_visual_carian.py konsisten (label/QTimer/muka jam/grab/kitaran hidup)")


def _imabas_kata_indo(src: str, corak: re.Pattern) -> dict[str, int]:
    """Imbas komen (#) dan docstring dalam sumber kod; kembali {kata: baris}.

    String kandungan (mesej UI, data, teks terjemahan) TIDAK diimbas --
    di sana perkataan itu boleh menjadi kandungan sah, dan corak senarai
    ini sendiri mengandungi semua kata sebagai rentetan dalam semak.py.
    """
    jumpa: dict[str, int] = {}

    # Komen `#` melalui tokenize -- token COMMENT.
    for tok in tokenize.generate_tokens(io.StringIO(src).readline):
        if tok.type == tokenize.COMMENT:
            for m in corak.finditer(tok.string):
                jumpa.setdefault(m.group(0).lower(), tok.start[0])

    # Docstring melalui AST -- string pertama modul/fungsi/kelas sahaja.
    try:
        pokok = ast.parse(src)
    except SyntaxError:
        return jumpa
    for n in ast.walk(pokok):
        if isinstance(n, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef,
                          ast.ClassDef)) and n.body \
                and isinstance(n.body[0], ast.Expr) \
                and isinstance(n.body[0].value, ast.Constant) \
                and isinstance(n.body[0].value.value, str):
            for m in corak.finditer(n.body[0].value.value):
                jumpa.setdefault(m.group(0).lower(), n.body[0].lineno)
    return jumpa


def semak_bahasa_dokumen() -> None:
    """Dokumen .md mesti Bahasa Melayu Malaysia, bukan Indonesia.

    Setiap kata di sini berbunyi Indonesia dalam konteks Malaysia --
    'Pencarian' sengaja TIDAK disenaraikan kerana ia sah Melayu (Kamus
    Dewan) dan label UI app. Regresi mudah berlaku: sesi baharu menambah
    nota atau komen kod dengan kata Indonesia tanpa disedari. Skop imbas:
    dokumen .md di akar + komen/docstring fail .py (bukan string kandungan).
    Semua dokumen .md MESTI kekal Melayu Malaysia (tiada pengecualian).
    """
    tajuk("8m. Bahasa dokumen: Melayu (kata Indonesia dikesan)")

    indo = re.compile(
        r"\b(proyek|jadwal|resiko|karena|analisa|nasehat|obyek|subyek|"
        r"merubah|dikarenakan|membutuhkan|kebutuhan|menghapuskan|"
        r"menampilkan|ditampilkan|tampilan|tampilkan|tampil|pengaturan|"
        r"kecepatan|memiliki|perbaikan|berhasil|keberhasilan|sukses|"
        r"mencoba|dicoba|percobaan|dibutuhkan|berbagai|dampak|mengurangi|"
        r"pengiriman|meluncurkan|memunculkan|menyangkut|kendala|solusi|"
        r"opsional|evaluasi|mengolah|tombol|beranda|jendela|antarmuka|"
        r"tautan|pranala|situs|berkas|rekaman|mengunduh|mengunggah|"
        r"pembaruan|memperbarui|diperbarui|sinkronisasi|menyinkronkan|"
        r"kata sandi|kapan|dimana|dibawah|didalam|diatas|diantara|yaitu|"
        r"dimulai|diakhiri|bagian|sebagian|bisa|butuh|kode|akurat|akurasi|"
        r"presisi|cocok|mengecek|pengecekan|masukan|perangkat|"
        r"rekomendasi|implementasi|informasi|penelitian|peneliti|riset|"
        r"koreksi|kemana|kesini|disini|disana|kesana)\b",
        re.IGNORECASE)

    kecuali = set()
    # Skop imbas: README di akar + semua dokumen dalam dokumen/.
    # _arkib/ dan folder lain dikecualikan -- bukan dokumen hidup.
    fail = sorted(glob.glob(os.path.join(BASE, "*.md"))
                  + glob.glob(os.path.join(BASE, "dokumen", "**", "*.md"),
                              recursive=True))
    bersih = 0
    for p in fail:
        nama = os.path.basename(p)
        if nama in kecuali:
            lulus(f"{nama} dikecualikan (terjemahan Inggeris)")
            continue
        baris = _baca_cek(p).splitlines(keepends=True)
        jumpa: dict[str, int] = {}
        for no, b in enumerate(baris, 1):
            for m in indo.finditer(b):
                kata = m.group(0).lower()
                jumpa.setdefault(kata, no)
        if jumpa:
            butir = ", ".join(f"{k} (baris {v})" for k, v in jumpa.items())
            salah(f"{nama}: kata Indonesia {butir}")
        else:
            bersih += 1
            lulus(f"{nama} bersih")
    if bersih:
        lulus(f"{bersih} dokumen .md tiada kata Indonesia")

    # Fail .py: imbas komen (#) dan docstring sahaja. String kandungan
    # (mesej UI, data, teks terjemahan) dikecualikan -- di sana perkataan
    # itu boleh menjadi kandungan sah, dan corak senarai ini sendiri
    # mengandungi semua kata sebagai rentetan (bukan komen). Folder
    # arkib/sandaran/tampalan dikecualikan -- bukan kod hidup.
    fail_py = [f for f in _senarai_py_projek()
               if "__pycache__" not in f
               and not f.startswith(("_arkib", "sandaran_", "tampalan_preload"))]
    bersih_py = 0
    for p in fail_py:
        jumpa = _imabas_kata_indo(_baca_cek(p), indo)
        if jumpa:
            butir = ", ".join(f"{k} (baris {v})" for k, v in jumpa.items())
            salah(f"{p}: kata Indonesia {butir}")
        else:
            bersih_py += 1
    if bersih_py:
        lulus(f"{bersih_py} fail .py (komen/docstring) tiada kata Indonesia")


def semak_susunatur() -> None:
    """Setiap halaman mesti ada addStretch(1) pada layout akar.

    Tanpa ia, QVBoxLayout mengagihkan ruang lebihan kepada SETIAP anak.
    Hero meregang 187px -> 284px dan hasil carian tertolak ke bawah --
    pengguna nampak skrin hampir kosong. `_page_search` terlepas ini.
    """
    tajuk("8d. Susun atur: stretch pada layout akar")
    src = _sumber_ui()
    pokok = ast.parse(src)
    halaman = [n for n in ast.walk(pokok)
               if isinstance(n, ast.FunctionDef)
               and n.name.startswith("_page_")]
    if not halaman:
        salah("tiada fungsi _page_* dijumpai")
        return
    for fn in sorted(halaman, key=lambda x: x.name):
        badan = ast.get_source_segment(src, fn) or ""

        # Cari pembolehubah layout AKAR: QVBoxLayout(body).
        # Semakan longgar ("addStretch(1)" di mana-mana) memberi positif
        # palsu -- `wl.addStretch(1)` untuk memusatkan bar carian secara
        # mendatar juga dikira. Kita mesti semak layout akar SAHAJA.
        m = re.search(r"((?:self\.)?[\w.]+)\s*=\s*QVBoxLayout\(body\)", badan)
        if not m:
            lulus(f"{fn.name} (tiada layout akar)")
            continue
        akar = m.group(1)
        # Halaman yang membuang addStretch dengan SENGAJA (untuk
        # menghilangkan kawasan skrol kosong) mesti mempunyai komen
        # "TIADA addStretch" yang menerangkan sebabnya. Hero mengunci
        # tingginya sendiri dalam resizeEvent, jadi tiada yang meregang.
        # Komen mungkin berada dalam metod _render_* yang mengisi
        # layout itu, bukan dalam _page_* yang hanya menciptanya.
        nama_akar = akar.replace("self.", "")
        sengaja = ("TIADA addStretch" in badan
                   or re.search(r"TIADA addStretch[^\n]*\n(?:[^\n]*\n){0,6}?[^\n]*"
                                + re.escape(nama_akar), src) is not None)
        if sengaja:
            lulus(f"{fn.name} (sengaja tiada stretch)")
            continue
        pola = re.escape(akar) + r"\.addStretch\(1\)"
        if re.search(pola, badan):
            lulus(f"{fn.name}")
        elif akar.startswith("self."):
            # Halaman bekas kosong menyimpan layout sebagai atribut
            # (self._pipe_root) dan menambah stretch dalam _render_*.
            # Nama tempatan seperti `bl` TIDAK layak -- ia dikongsi
            # antara fungsi dan memberi positif palsu.
            if re.search(pola, src):
                lulus(f"{fn.name} (stretch dlm metod lain)")
            else:
                salah(f"{fn.name}: {akar} tiada addStretch(1)")
        else:
            salah(f"{fn.name}: {akar} tiada addStretch(1)")

    # Halaman utama mesti muat tanpa skrol pada laptop 768px.
    # Pengguna mahu kandungan utama kelihatan sebaik apl dibuka.
    # 25 Ogos: stack.widget(0) kini BackgroundCanvas (halaman utama
    # Split Command Center) — QScrollArea dijumpai melalui findChild.
    import subprocess as _sp
    uji = (
        "import sys,json,time; sys.path.insert(0,'.')\n"
        "for _ in range(10):\n"
        "    try:\n"
        "        _f=open('user_settings.json','w')\n"
        "        json.dump({'theme':'dark','api_key':'','api_url':'x'},_f)\n"
        "        _f.close(); break\n"
        "    except PermissionError:\n"
        "        time.sleep(0.3)\n"
        "from PyQt5.QtWidgets import QApplication, QScrollArea\n"
        "from PyQt5.QtCore import QTimer\n"
        "a=QApplication([])\n"
        "from ui.app_qt import PustakaApp\n"
        "w=PustakaApp(); w.resize(1240,730); w.show()\n"
        "def c():\n"
        "    sa=w.stack.widget(0).findChild(QScrollArea)\n"
        "    if sa is None:\n"
        "        print('TIADA SKROL'); return\n"
        "    print('LEBIHAN', sa.widget().height()-sa.viewport().height())\n"
        "    a.quit()\n"
        "QTimer.singleShot(700,c); a.exec_()\n"
    )
    # PustakaApp mencipta hadis.db kosong; buang artifak sendiri ini selepas.
    db_asal = os.path.exists("hadis.db")
    try:
        r = _sp.run([sys.executable, "-c", uji], capture_output=True,
                    text=True, timeout=120,
                    env=dict(os.environ, QT_QPA_PLATFORM="offscreen"))
        baris = [x for x in r.stdout.split("\n") if x.startswith("LEBIHAN")]
        if not baris:
            salah("tidak dapat mengukur tinggi halaman utama")
        else:
            lebih = int(baris[0].split()[1])
            if lebih <= 0:
                lulus("halaman utama muat 1240x730 tanpa skrol")
            else:
                salah(f"halaman utama {lebih}px terlalu tinggi pada 730px")
    except Exception as e:
        salah(f"ujian tinggi halaman utama: {e}")
    _pulihkan_settings()
    if not db_asal:
        for f in ("hadis.db", "hadis.db-wal", "hadis.db-shm"):
            if os.path.exists(f):
                os.remove(f)

    # Halaman huraian (Fasa 4) dibuang pada Sesi 18.9 -- butang
    # "📖 Huraian" dan `_page_pipeline` tidak lagi wujud. Semakan
    # "butang Kembali di luar skrol" yang lama berkaitan halaman itu
    # ditarik balik; `bottombar` masih dipakai halaman detail.

    # tetingkap mesti muat skrin kecil
    if "setMinimumSize(900, 560)" in src:
        lulus("minimum tetingkap muat 1366x768")
    else:
        salah("setMinimumSize terlalu besar untuk laptop 768px")
    if "_saiz_muat_skrin" in src:
        lulus("saiz awal ikut availableGeometry()")
    else:
        salah("saiz tetingkap tetap -- boleh terpotong")


# ---------------------------------------------------------------- 9
def semak_versi_fail() -> None:
    """VERSI.py wujud dan skrip utama mencetak capnya.

    Pengguna menjalankan kod LAMA tiga kali berturut-turut kerana ZIP
    mempunyai folder bersarang; ekstrak mendarat di tempat salah dan
    setiap laporan kelihatan sah. Cap versi menjadikan kegagalan itu
    KELIHATAN.
    """
    tajuk("10. Cap versi")
    sys.path.insert(0, BASE)
    try:
        from VERSI import CIRI, VERSI
        lulus(f"VERSI.py ada (v{VERSI})")
    except Exception as e:
        salah(f"VERSI.py: {e}")
        return

    import importlib
    hilang = []
    for modul, nama in CIRI:
        try:
            m = importlib.import_module(modul)
            if not hasattr(m, nama):
                hilang.append(f"{modul}.{nama}")
        except Exception as e:
            hilang.append(f"{modul} ({e})")
    if hilang:
        salah(f"ciri hilang: {', '.join(hilang)}")
    else:
        lulus(f"semua {len(CIRI)} ciri VERSI hadir")

    for f in ("sync_english.py", "sync_syarah.py", "sync_hadeethenc.py",
              "sync_sema.py", "audit_eng.py"):
        p = os.path.join(BASE, f)
        if not os.path.exists(p):
            continue
        with open(p, encoding="utf-8") as fh:
            src = fh.read()
        if "VERSI" in src and "{VERSI}" in src:
            lulus(f"{f} cetak cap versi")
        else:
            salah(f"{f} TIDAK cetak cap versi")

    p = os.path.join(BASE, "semak_versi.py")
    if os.path.exists(p):
        lulus("semak_versi.py disertakan")
        with open(p, encoding="utf-8") as fh:
            src = fh.read()
        # Ia tidak boleh mendakwa "TERKINI" -- ia tiada rujukan kepada
        # versi terbaru yang wujud, jadi dakwaan itu menyembunyikan
        # pemasangan lapuk (berlaku 4 kali).
        # Semak OUTPUT, bukan sumber: perkataan itu sah dalam komen.
        cetak = [ln for ln in src.splitlines()
                 if "print(" in ln and "TERKINI" in ln]
        if not cetak:
            lulus("semak_versi.py tidak mencetak dakwaan 'TERKINI'")
        else:
            salah("semak_versi.py MENCETAK 'TERKINI' — ia tidak boleh "
                  "tahu versi terbaru; dakwaan itu mengelirukan")
        # Kod baharu + DB lama = kegagalan senyap. Alat pemindahan
        # dan amaran mesti wujud.
        for nm in ("PINDAH_DATA.ps1", "semak_db.py"):
            q = os.path.join(BASE, nm)
            if not os.path.exists(q):
                salah(f"{nm} TIADA")
                continue
            if nm.endswith(".ps1"):
                with open(q, "rb") as fh:
                    b = fh.read()
                if b.count(b"\r\n") >= 10 and all(x < 128 for x in b):
                    lulus(f"{nm} ada (CRLF + ASCII)")
                else:
                    salah(f"{nm}: LF atau bukan ASCII")
            else:
                lulus(f"{nm} ada")
        if "PINDAH_DATA" in src:
            lulus("semak_versi.py beri amaran DB hilang")
        else:
            salah("semak_versi.py tiada amaran DB hilang")

        k = os.path.join(BASE, "KEMASKINI.bat")
        if os.path.exists(k):
            with open(k, "rb") as fh:
                b = fh.read()
            if b.count(b"\r\n") >= 10 and b"-Force" in b:
                lulus("KEMASKINI.bat ada (CRLF + -Force)")
            else:
                salah("KEMASKINI.bat: LF atau tiada -Force")
        else:
            salah("KEMASKINI.bat TIADA")

        if "-Force" in src:
            lulus("semak_versi.py beri arahan Expand-Archive -Force")
        else:
            salah("semak_versi.py tiada arahan ekstrak Windows")
    else:
        salah("semak_versi.py TIADA")


def semak_dokumen() -> None:
    """Dokumen tidak boleh bercanggah dengan tingkah laku kod.

    `MULA_SINI.md` pernah mengandungi "Fasa 4B TERSEKAT" pada baris 176
    dan "Fasa 4B SIAP" pada baris 214 serentak. Dokumen yang bercanggah
    lebih buruk daripada tiada dokumen: ia membuat pembaca mempercayai
    dakwaan yang salah.
    """
    tajuk("11. Dokumen konsisten")

    dok = ("dokumen/manual/MULA_SINI.md",
           "dokumen/rujukan/RANCANGAN_4FASA.md",
           "dokumen/sesi/sesi_index.md", "core/syarah_source.py")
    # Dakwaan yang telah DIBATALKAN oleh ujian pada data sebenar.
    # Jika ia muncul semula tanpa penafian, dokumen itu menyesatkan.
    batal = [
        ("diuji 5/5", "penomboran Fath al-Bari sejajar"),
        ("Disahkan 5/5", "penomboran Fath al-Bari sejajar"),
    ]
    for f in dok:
        p = os.path.join(BASE, f)
        if not os.path.exists(p):
            continue
        with open(p, encoding="utf-8") as fh:
            isi = fh.read()
        buruk = [d for d, _ in batal
                 if d in isi and "DIBATALKAN" not in isi]
        if buruk:
            salah(f"{f} masih mendakwa '{buruk[0]}' tanpa penafian")
        else:
            lulus(f"{f} tiada dakwaan terbatal")

    # Fasa 4B: status mesti SATU sahaja merentas semua dokumen.
    p = os.path.join(BASE, "dokumen/manual/MULA_SINI.md")
    if os.path.exists(p):
        with open(p, encoding="utf-8") as fh:
            isi = fh.read()
        if "Fasa 4B SIAP" in isi and "Fasa 4B) — TERSEKAT" in isi:
            salah("MULA_SINI.md kata Fasa 4B SIAP *dan* TERSEKAT")
        else:
            lulus("MULA_SINI.md status Fasa 4B konsisten")


# Bulan Melayu -> nombor (untuk tarikh 'Sesi Terakhir — 14 Ogos 2026').
_BULAN_MELAYU = {
    "januari": 1, "februari": 2, "mac": 3, "april": 4, "mei": 5,
    "jun": 6, "julai": 7, "ogos": 8, "september": 9, "oktober": 10,
    "november": 11, "disember": 12,
}
_NAMA_BULAN = {v: k.capitalize() for k, v in _BULAN_MELAYU.items()}


def _git_log_tarikh() -> str | None:
    """Tarikh commit git terbaru (YYYY-MM-DD); None bila tiada git."""
    try:
        r = subprocess.run(["git", "log", "-1", "--format=%ad",
                            "--date=short"],
                           capture_output=True, text=True, cwd=BASE,
                           timeout=15)
    except Exception:
        return None
    if r.returncode != 0:
        return None
    return r.stdout.strip() or None


def _git_semua_hash() -> list[str]:
    """Hash penuh semua commit git (terbaru dahulu); kosong tanpa git."""
    try:
        r = subprocess.run(["git", "log", "--format=%H"],
                           capture_output=True, text=True, cwd=BASE,
                           timeout=30)
    except Exception:
        return []
    if r.returncode != 0:
        return []
    return [h.strip() for h in r.stdout.splitlines() if h.strip()]


def semak_sesi_terakhir() -> None:
    """'Sesi Terakhir' dalam MULA_SINI.md tidak boleh ketinggalan git log.

    Sesi AI baharu membaca bahagian ini sebagai ringkasan kerja terkini
    — jika ia lapuk, sesi bermula dengan salah faham (contoh sebenar:
    bahagian kekal '13 Ogos' selepas kerja 14 Ogos). Peraturan:
    (1) tarikh selepas '## Sesi Terakhir — ' tidak kurang daripada
        tarikh commit git terbaru (kadar hari; kerja pada hari baharu
        MESTI dikemas kini di sini);
    (2) sekurang-kurangnya satu hash commit yang disebut dalam bahagian
        itu wujud dalam 10 commit git terbaru — bukan hanya rujukan
        sejarah purba;
    (3) setiap hash 7-heks yang disebut dalam bahagian itu wujud dalam
        sejarah git (tiada hash rekaan/tersalah taip);
    (4) tarikh tajuk TIDAK mendahului tarikh sistem hari ini (rekod
        hari baharu tidak boleh dibuka sebelum tarikh sebenar) —
        bersama (1): git ≤ tajuk ≤ hari ini.
    Tiada git (cth. edaran ZIP) -> lulus.
    """
    tajuk("12. MULA_SINI 'Sesi Terakhir' seiring git log")

    p = os.path.join(BASE, "dokumen/manual/MULA_SINI.md")
    if not os.path.exists(p):
        salah("dokumen/manual/MULA_SINI.md TIADA — bahagian 'Sesi "
              "Terakhir' hilang")
        return
    with open(p, encoding="utf-8") as fh:
        isi = fh.read()

    git_tarikh = _git_log_tarikh()
    if git_tarikh is None:
        lulus("tiada git — bandingan tarikh dilangkau")
        return
    lulus(f"commit git terbaru: {git_tarikh}")

    m = re.search(r"^## Sesi Terakhir — (\d{1,2}) (\S+) (\d{4})",
                  isi, re.M)
    if not m:
        salah("'## Sesi Terakhir — TARIKH' tidak dijumpai dalam "
              "MULA_SINI.md")
        return
    hari, bln_kata, thn = int(m.group(1)), m.group(2), int(m.group(3))
    bln = _BULAN_MELAYU.get(bln_kata.lower())
    if bln is None:
        salah(f"bulan Sesi Terakhir tidak dikenali: {bln_kata!r}")
        return
    sesi_tarikh = f"{thn:04d}-{bln:02d}-{hari:02d}"

    if sesi_tarikh < git_tarikh:
        salah(f"'Sesi Terakhir' ({sesi_tarikh}) KETINGGALAN git log "
              f"({git_tarikh}) — kemas kini MULA_SINI.md bahagian "
              f"'Sesi Terakhir' dengan kerja terkini")
    else:
        lulus(f"Sesi Terakhir ({sesi_tarikh}) seiring git log "
              f"({git_tarikh})")

    # Bahagian 'Sesi Terakhir' berakhir pada '---' pertama selepas tajuk.
    blok = isi[m.start():]
    blok = re.split(r"\n---", blok, maxsplit=1)[0]

    # Teks ringkasan (sebelum '**Sebelum ini' — riwayat lama) MESTI
    # menyebut tarikh commit terbaru, bukan hanya tajuk. Mencegah:
    # tajuk dinaik tarikh tanpa meringkaskan kerja hari itu. Baris
    # tajuk ('## Sesi Terakhir — ...') dikecualikan supaya tarikh
    # tajuk sahaja tidak memenuhi semakan ini.
    gthn, gbln, ghari = git_tarikh.split("-")
    tarikh_melayu = f"{int(ghari)} {_NAMA_BULAN.get(int(gbln), '')}"
    blok_isi = blok.split("\n", 1)[1] if "\n" in blok else ""
    ringkasan = re.split(r"\*\*Sebelum ini", blok_isi, maxsplit=1)[0]
    if (tarikh_melayu not in ringkasan
            and git_tarikh not in ringkasan
            and f"{tarikh_melayu} {gthn}" not in ringkasan):
        salah(f"'Sesi Terakhir' tidak menyebut tarikh kerja terkini "
              f"({tarikh_melayu}) dalam teks ringkasan — tambah tarikh "
              f"kerja terbaru pada ringkasan")
    else:
        lulus(f"teks ringkasan menyebut tarikh kerja terkini "
              f"({tarikh_melayu})")
    hash_disebut = set(re.findall(r"\b[0-9a-f]{7}\b", blok))

    semua = _git_semua_hash()
    if not semua:
        lulus("tiada git — semakan hash dilangkau")
        return
    terbaru10 = {h[:7] for h in semua[:10]}
    tiada = sorted(h for h in hash_disebut
                   if not any(full.startswith(h) for full in semua))
    if tiada:
        salah(f"Sesi Terakhir sebut hash tidak wujud dalam git: "
              f"{', '.join(tiada)}")
    else:
        lulus("semua hash yang disebut wujud dalam sejarah git")
    # Hanya semak "hash daripada 10 commit terbaru" jika ada sekurang-kurangnya 10 commit dalam git
    if len(semua) >= 10:
        if not (hash_disebut & terbaru10):
            salah("Sesi Terakhir tiada hash daripada 10 commit terbaru — "
                  "ringkasan ketinggalan kerja terkini")
        else:
            lulus("Sesi Terakhir sebut hash daripada 10 commit terbaru")
    else:
        lulus(f"Sesi Terakhir: hanya {len(semua)} commit dalam git (kurang 10) — semakan 10-commit dilangkau")

    # (4) Rekod tidak boleh mendahului tarikh sistem: pembukaan hari
    #     baharu MESTI menunggu tarikh sebenar (contoh sebenar: rekod
    #     hari berikutnya dibuka sedangkan jam sistem masih hari ini —
    #     git log dan tajuk rekod lari seminggu kemudian). Bersama
    #     peraturan (1), julat sah ialah git ≤ tajuk ≤ hari ini.
    hari_ini = datetime.date.today().isoformat()
    if sesi_tarikh > hari_ini:
        salah(f"'Sesi Terakhir' ({sesi_tarikh}) mendahului tarikh sistem "
              f"({hari_ini}) — rekod hari dibuka sebelum tarikh sebenar; "
              f"kemas kini ke tarikh semasa")
    else:
        lulus(f"Sesi Terakhir ({sesi_tarikh}) tidak mendahului tarikh "
              f"sistem ({hari_ini})")


def semak_kontras_tema() -> None:
    """Kontras WCAG AA semua tema — SEMUA tier teks ≥ 4.5:1.

    Malam 14 Ogos: palet ditukar (neutral lalai + kertas hangat) dan
    tier teks malap dinaikkan supaya lulus AA. Semakan ini mengunci:
    sebarang warna baharu yang jatuh di bawah 4.5:1 pada permukaan
    berkenaan → GAGAL. Liputan: teks biasa pada halaman/kad/header,
    teks semantik (ambar/merah/hijau) pada latarnya, dan aksen TEAL
    sebagai teks pautan/cip.
    """
    tajuk("13. Kontras WCAG AA semua tema (≥ 4.5:1)")

    # 5 tema: aqua (lalai baharu 25 Ogos), neutral, kertas hangat,
    # neutral terang, kertas terang
    import ui.theme as _t

    def _lum(hexa: str) -> float:
        h = hexa.lstrip("#")
        r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))

        def _f(c: float) -> float:
            return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
        return 0.2126 * _f(r) + 0.7152 * _f(g) + 0.0722 * _f(b)

    def _nisbah(a: str, b: str) -> float:
        l1, l2 = _lum(a), _lum(b)
        if l1 < l2:
            l1, l2 = l2, l1
        return (l1 + 0.05) / (l2 + 0.05)

    mula = len(gagal)
    total = 0
    for nama in ("aqua", "neutral", "dark", "lightneutral", "light"):
        p = _t.THEMES[nama]
        for perm in ("PAGE_BG", "CARD_BG", "HEADER_BG"):
            for tier in ("TEXT_PRIMARY", "TEXT_SECONDARY",
                         "TEXT_MUTED", "TEXT_FAINT"):
                n = _nisbah(p[tier], p[perm])
                total += 1
                if n < 4.5:
                    salah(f"{nama}: {tier} ({p[tier]}) pada {perm} "
                          f"({p[perm]}) = {n:.2f}:1 — bawah AA 4.5")
        for tier, bg in (("AMBER_TEXT", "AMBER_BG"),
                         ("RED_TEXT", "RED_BG"),
                         ("GREEN_TEXT", "GREEN_BG")):
            n = _nisbah(p[tier], p[bg])
            total += 1
            if n < 4.5:
                salah(f"{nama}: {tier} pada {bg} = {n:.2f}:1 — bawah AA")
        for perm in ("PAGE_BG", "CARD_BG", "TEAL_PALE"):
            n = _nisbah(p["TEAL"], p[perm])
            total += 1
            if n < 4.5:
                salah(f"{nama}: TEAL pada {perm} = {n:.2f}:1 — bawah AA")
    if len(gagal) == mula:
        lulus(f"{total} pasangan warna ≥ 4.5:1 (5 tema)")


def _senarai_untracked_git() -> list[str]:
    """Fail untracked oleh git (tidak dijejak, tidak di-ignore).

    Contoh sebenar: `4.65.0` -- output pip tersilap diubah hala ke fail
    bernama versi tqdm (tiada sambungan, bukan sebahagian projek).
    Fail baharu yang SAH mesti di-commit dahulu, atau ia dianggap sisa.
    Jika folder tiada .git, pulangkan senarai kosong.
    """
    try:
        import subprocess as _sp
        _r = _sp.run(["git", "status", "--porcelain",
                      "--untracked-files=all"],
                     capture_output=True, text=True, cwd=BASE, timeout=15)
        if _r.returncode != 0:
            return []
        return [b[3:].strip() for b in _r.stdout.splitlines()
                if b.startswith("?? ") and b[3:].strip()]
    except Exception:
        return []          # tiada git -> tiada semakan untracked


def semak_rtl_dokumen() -> None:
    """Audit susun atur RTL dalam dokumen (14 Ogos) — kunci agar tidak regresi.

    Susun atur semasa: Arab di KANAN, terjemahan di KIRI (dicerminkan
    14 Ogos). Sebarang tuntutan susun atur lama dalam TRANSFORMASI_DETAIL.md
    / MANUAL_PENGGUNAAN.md / README.md → GAGAL. `sesi_index.md` hanya
    RINGKASAN \"Sesi Terakhir\" (header sebelum tajuk bahagian pertama)
    diimbas — seluruh fail ialah arkib sejarah berketarikh di mana frasa
    lama dalam konteks sejarah dibenarkan. Nota sejarah yang MENGUTIP frasa
    lama (cth. rujukan \"Arab kiri / terjemahan kanan\" dalam nota RTL di
    atas TRANSFORMASI_DETAIL) tidak dipadan kerana corak larangan khusus
    (mengandungi \"di\" / \"membawa\" / \">\") tidak wujud dalam petikan.
    """
    tajuk("14. Audit susun atur RTL dokumen (Arab kanan)")
    corak = (
        "Arab di kiri",
        "terjemahan di kanan",
        "lajur kiri membawa teks Arab",
        "lajur kanan membawa terjemahan",
        "terjemahan > `x` Arab",
        "teks Arab di lajur kiri",
        "TRANSLITERASI** dalam lajur kiri",
    )
    masalah = []
    for fail in ("dokumen/manual/TRANSFORMASI_DETAIL.md",
                 "dokumen/manual/MANUAL_PENGGUNAAN.md",
                 "README.md",
                 "dokumen/sesi/sesi_index.md"):
        p = os.path.join(BASE, fail)
        if not os.path.exists(p):
            masalah.append(f"{fail}: TIADA")
            continue
        isi = open(p, encoding="utf-8").read()
        if fail.endswith("sesi_index.md"):
            # Arkib sejarah: hanya header "Sesi Terakhir" — seksyen
            # arkib berketarikh (sejarah reka bentuk) dikecualikan.
            isi = isi.split("\n# ", 1)[0]
        for c in corak:
            for no, baris in enumerate(isi.splitlines(), 1):
                if c in baris:
                    masalah.append(f"{fail}:{no}: {c}")
    if masalah:
        for m in masalah:
            salah(m)
    else:
        lulus("tiada tuntutan susun atur lama "
              "(Arab kiri / terjemahan kanan)")


def semak_ringkasan_keadaan() -> None:
    """Ringkasan satu muka 'Keadaan projek' (atas MULA_SINI) seiring
    'Sesi Terakhir' — tarikh + kiraan commit tidak boleh hanyut.

    Ringkasan ialah perkara PERTAMA dibaca sesi AI baharu; jika ia
    ketinggalan (tarikh lama / kiraan commit tidak dikemas selepas
    'Sesi Terakhir' berubah), sesi bermula dengan gambaran lapuk —
    masalah yang sama yang semak #12 selesaikan untuk 'Sesi Terakhir'.
    Peraturan:
    (1) seksyen '## Keadaan projek — ringkasan satu muka' wujud;
    (2) tarikh dalam tajuk ringkasan == tarikh tajuk 'Sesi Terakhir';
    (3) kiraan '**N commit**' dalam ringkasan == kiraan intro
        'Sesi Terakhir' ('Kerja ... — **N commit** (X teras + Y susulan)').
    Tiada git -> semakan tarikh dilangkau (seperti semak #12).
    """
    tajuk("15. MULA_SINI ringkasan satu muka seiring 'Sesi Terakhir'")

    p = os.path.join(BASE, "dokumen/manual/MULA_SINI.md")
    if not os.path.exists(p):
        salah("dokumen/manual/MULA_SINI.md TIADA — ringkasan hilang")
        return
    isi = open(p, encoding="utf-8").read()

    # (1) Seksyen ringkasan wujud + baca tarikh tajuknya.
    m = re.search(
        r"^## Keadaan projek — ringkasan satu muka \(akhir "
        r"(\d{1,2}) (\S+) (\d{4})\)", isi, re.M)
    if not m:
        salah("'## Keadaan projek — ringkasan satu muka' TIADA "
              "dalam MULA_SINI.md")
        return
    hari, bln_kata, thn = int(m.group(1)), m.group(2), int(m.group(3))
    bln = _BULAN_MELAYU.get(bln_kata.lower())
    if bln is None:
        salah(f"bulan ringkasan tidak dikenali: {bln_kata!r}")
        return
    r_tarikh = f"{thn:04d}-{bln:02d}-{hari:02d}"

    # (2) Tarikh ringkasan == tarikh 'Sesi Terakhir' (bukan hanya >= git;
    #     kedua-dua seksyen adalah ringkasan hidup yang mesti bergerak sama).
    ms = re.search(r"^## Sesi Terakhir — (\d{1,2}) (\S+) (\d{4})",
                   isi, re.M)
    if not ms:
        salah("'## Sesi Terakhir — TARIKH' tidak dijumpai dalam "
              "MULA_SINI.md")
        return
    s_hari, s_bln_kata, s_thn = (int(ms.group(1)), ms.group(2),
                                 int(ms.group(3)))
    s_bln = _BULAN_MELAYU.get(s_bln_kata.lower())
    if s_bln is None:
        salah(f"bulan Sesi Terakhir tidak dikenali: {s_bln_kata!r}")
        return
    s_tarikh = f"{s_thn:04d}-{s_bln:02d}-{s_hari:02d}"
    if r_tarikh != s_tarikh:
        salah(f"ringkasan ({r_tarikh}) tidak seiring 'Sesi Terakhir' "
              f"({s_tarikh}) — kemas kini kedua-dua tajuk")
    else:
        lulus(f"ringkasan ({r_tarikh}) == 'Sesi Terakhir' ({s_tarikh})")

    # (3) Kiraan commit dalam ringkasan == kiraan intro 'Sesi Terakhir'.
    blok_r = isi[m.start():]
    blok_r = re.split(r"\n---", blok_r, maxsplit=1)[0]
    blok_s = isi[ms.start():]
    blok_s = re.split(r"\n---", blok_s, maxsplit=1)[0]
    mr = re.search(r"\*\*(\d+) commit\*\*", blok_r)
    mi = re.search(r"Kerja \d{1,2} \S+ — \*\*(\d+) commit\*\*",
                   blok_s)
    r_n = mr.group(1) if mr else None
    s_n = mi.group(1) if mi else None
    if r_n != s_n:
        salah(f"ringkasan kiraan commit ({r_n or 'TIADA'}) != "
              f"'Sesi Terakhir' ({s_n or 'TIADA'}) — kemas kini "
              f"ringkasan apabila kiraan berubah")
    else:
        lulus(f"ringkasan {r_n} commit == 'Sesi Terakhir'")


def semak_peta_sunnah() -> None:
    """Peta 'Baca penuh' sunnah_map/ seiring dengan hadis.db (Sesi 36).

    `sync_english.py --peta-sunnah` menjana sunnah_map/{slug}.json.
    Jika hadis.db disinkron semula dan peta tidak dijana semula, pautan
    "Baca penuh" menjadi salah/tiada -- amaran awal di sini. Hadis.db
    tiada -> semakan dilangkau (bukan kegagalan).
    """
    tajuk("8n. Peta 'Baca penuh' sunnah.com seiring hadis.db")
    if not os.path.exists(os.path.join(BASE, "hadis.db")):
        print("    nota: hadis.db tiada -- semakan dilangkau")
        return
    try:
        import sqlite3
        conn = sqlite3.connect(os.path.join(BASE, "hadis.db"))
        try:
            kira = dict(conn.execute(
                "SELECT collection, COUNT(*) FROM hadis GROUP BY collection"))
        finally:
            conn.close()
    except Exception:
        print("    nota: tidak dapat baca hadis.db -- semakan dilangkau")
        return
    arahan = "python sync_english.py --peta-sunnah"
    for slug in ("bukhari", "muslim", "abu-daud", "tirmidzi",
                 "nasai", "ibnu-majah", "malik"):
        laluan = os.path.join(BASE, "sunnah_map", f"{slug}.json")
        n_hadis = kira.get(slug, 0)
        if not os.path.exists(laluan):
            if n_hadis:
                salah(f"peta sunnah {slug} TIADA (hadis {n_hadis:,}) -- "
                      f"jalankan {arahan}")
            continue
        try:
            with open(laluan, encoding="utf-8") as f:
                peta = json.load(f)
        except Exception:
            salah(f"peta sunnah {slug} rosak -- jalankan {arahan}")
            continue
        n = len(peta)
        if n_hadis and n < n_hadis * 0.9:
            salah(f"peta sunnah {slug} ketinggalan ({n:,}/{n_hadis:,} "
                  f"hadis) -- jalankan {arahan}")
        else:
            lulus(f"peta sunnah {slug} seiring ({n:,}/{n_hadis:,})")


# Bilangan sampel rawak audit pautan sunnah.com + jeda antara muat
# turun (sunnah.com had laju -- 20 permintaan pantas mencetuskan 403;
# jeda 3s selamat, disahkan semasa audit Sesi 36).
_AUDIT_SUNNAH_BIL = 20
_AUDIT_SUNNAH_JEDA = 3.0
_AUDIT_SUNNAH_SLUG = ("bukhari", "muslim", "abu-daud", "tirmidzi",
                      "nasai", "ibnu-majah", "malik")
_AUDIT_SUNNAH_SUN = {
    "bukhari": "bukhari", "muslim": "muslim", "abu-daud": "abudawud",
    "tirmidzi": "tirmidhi", "nasai": "nasai", "ibnu-majah": "ibnmajah",
    "malik": "malik",
}


def semak_audit_sunnah() -> None:
    """Audit pautan 'Baca penuh' sunnah.com terhadap halaman SEBENAR.

    HANYA berjalan dengan `--audit-sunnah` (lalai semak.py kekal luar
    talian -- semakan jaringan perlahan dan bergantung pada sunnah.com).
    Saiz sampel boleh ditetapkan: `python semak.py --audit-sunnah=50`
    (lalai 20; 50 = liputan lebih luas, cadangan sebelum hantar --
    ambil ~3 minit kerana jeda 3s antara muat turun).

    Sampel rawak hadis daripada sunnah_map/, muat halaman
    sunnah.com/{slug}/{book}/{hadith}, sahkan teks CDN (rujukan dalam-
    buku) hadir dalam halaman -- bandingan tanpa ruang, elak artifak
    HTML. Ralat muat turun (403/offline) dikira NOTA, bukan kegagalan:
    semakan ini hanya gagal pada ketidakpadanan yang DISAHKAN.
    """
    import html
    import random
    import time
    import urllib.request

    bil = _AUDIT_SUNNAH_BIL
    for a in sys.argv:
        if a.startswith("--audit-sunnah="):
            try:
                bil = max(1, int(a.split("=", 1)[1]))
            except ValueError:
                pass

    tajuk("8o. Audit pautan 'Baca penuh' sunnah.com (halaman sebenar)")
    try:
        from core.eng_source import normalisasi
    except Exception as e:
        salah(f"tidak dapat import core.eng_source: {e}")
        return

    # 1. Kumpul calon (slug, hadis_id, (book, hadith)) daripada sunnah_map/
    calon = []
    for slug in _AUDIT_SUNNAH_SLUG:
        laluan = os.path.join(BASE, "sunnah_map", f"{slug}.json")
        if not os.path.exists(laluan):
            continue
        try:
            with open(laluan, encoding="utf-8") as f:
                peta = json.load(f)
        except Exception:
            continue
        for hid, r in peta.items():
            if isinstance(r, dict) and r.get("book") and r.get("hadith"):
                calon.append((slug, int(hid),
                              (int(r["book"]), int(r["hadith"]))))
    if not calon:
        print("    NOTA: tiada peta sunnah_map/ -- jalankan "
              "'python sync_english.py --peta-sunnah' dahulu")
        return

    # 2. Sampel rawak (seeded -- boleh ulang)
    random.seed(42)
    sampel = random.sample(calon, min(bil, len(calon)))

    # 3. Teks CDN ikut (book, hadith) -- dimuat lambat per slug
    cdn_ref: dict[str, dict] = {}

    def _cdn_slug(slug: str) -> None:
        if slug in cdn_ref:
            return
        teks: dict = {}
        fz = _AUDIT_SUNNAH_SUN[slug]
        laluan = os.path.join(BASE, ".cache_eng", f"ara-{fz}1.json")
        if os.path.exists(laluan):
            try:
                with open(laluan, encoding="utf-8") as f:
                    d = json.load(f)
                for h in d.get("hadiths", []):
                    ref = h.get("reference") or {}
                    if ref.get("book") and ref.get("hadith"):
                        k = (int(ref["book"]), int(ref["hadith"]))
                        teks.setdefault(k, set()).add(
                            normalisasi(h.get("text", "")).replace(" ", ""))
            except Exception:
                teks = {}
        cdn_ref[slug] = teks

    def _muat(url: str) -> str:
        req = urllib.request.Request(
            url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; "
                          "Win64; x64) AppleWebKit/537.36 Chrome/120"})
        with urllib.request.urlopen(req, timeout=25) as r:
            return r.read().decode("utf-8", errors="replace")

    def _ekstrak(htm: str) -> str:
        htm = re.sub(r"(?s)<(script|style).*?</\1>", " ", htm)
        htm = re.sub(r"<[^>]+>", " ", htm)
        return html.unescape(htm)

    dipadan = tiada = nota = 0
    for slug, hid, (book, hadith) in sampel:
        sun = _AUDIT_SUNNAH_SUN[slug]
        url = f"https://sunnah.com/{sun}/{book}/{hadith}"
        time.sleep(_AUDIT_SUNNAH_JEDA)
        try:
            page = normalisasi(_ekstrak(_muat(url))).replace(" ", "")
        except Exception as e:
            nota += 1
            print(f"    NOTA: tidak dapat muat {url} ({type(e).__name__})")
            continue
        _cdn_slug(slug)
        teks = cdn_ref[slug].get((book, hadith), set())
        if any(t and t in page for t in teks):
            dipadan += 1
            lulus(f"pautan betul: {slug}#{hid} -> {url}")
        else:
            tiada += 1
            salah(f"pautan sunnah tidak padan: {slug}#{hid} -> {url} "
                  "(teks CDN tiada dalam halaman)")
    print(f"    ringkasan: {dipadan} dipadan, {tiada} tidak padan, "
          f"{nota} tidak dapat disahkan (dari {len(sampel)})")


# ---------------------------------------------------------------- 8p
def semak_peta_kembali() -> None:
    """Peta Kembali (BACK_PETA) — setiap _detail_from -> halaman betul.

    Butang Kembali pada halaman butiran memilih destinasi mengikut
    `_detail_from` (halaman asal): 'home' -> Utama, 'search' -> Hasil
    carian, 'saved' -> Tersimpan, 'kitab' -> Senarai kitab. Pemalar
    `BACK_PETA` di `ui/pages_detail.py` diuji di sini supaya sebarang
    perubahan peta tanpa disedari (cth. menukar destinasi, menambah
    page_key yang tiada dalam PAGES, menghilangkan fallback) dikesan
    segera — GUI tests uji_lompat_fungsi menyahkan kelakuan sebenar.
    """
    tajuk("8p. Peta Kembali (BACK_PETA) — destinasi butang Kembali")
    from ui.pages_detail import BACK_PETA
    from ui.helpers import PAGES

    # Setiap halaman asal yang sah mesti ada dalam peta
    for k in ("home", "search", "saved", "kitab"):
        if k in BACK_PETA:
            lulus(f"{k} -> {BACK_PETA[k][1]}")
        else:
            salah(f"{k} tiada dalam BACK_PETA")

    # Setiap page_key mesti sah dalam PAGES (kekunci halaman app)
    for k, (label, pg) in sorted(BACK_PETA.items()):
        if pg in PAGES:
            lulus(f"BACK_PETA[{k}] page '{pg}' dalam PAGES")
        else:
            salah(f"BACK_PETA[{k}] page '{pg}' BUKAN kunci PAGES")

    # Label tooltip tidak kosong (dipapar kepada pengguna)
    for k, (label, pg) in sorted(BACK_PETA.items()):
        if label and label.strip():
            lulus(f"BACK_PETA[{k}] label '{label}'")
        else:
            salah(f"BACK_PETA[{k}] label kosong")

    # Fallback: _detail_from tidak dikenali -> home (bukan error)
    tujuan, pg = BACK_PETA.get("tidak-dikenali", BACK_PETA["home"])
    if pg == "home":
        lulus(f"fallback _detail_from tidak dikenali -> {pg}")
    else:
        salah(f"fallback -> {pg}, jangkaan home")

    # Konsisten dengan ujian GUI: destinasi search mesti PAGES['search']
    # (3) dan home mesti PAGES['home'] (0) -- rujukan silang ke PAGES.
    if BACK_PETA["home"][1] == "home" and PAGES["home"] == 0:
        lulus("home -> PAGES['home'] (0)")
    else:
        salah("home tidak memetakan ke PAGES['home']")
    if BACK_PETA["search"][1] == "search" and PAGES["search"] == 3:
        lulus("search -> PAGES['search'] (3)")
    else:
        salah("search tidak memetakan ke PAGES['search']")


# ---------------------------------------------------------------- 8q
def semak_nav_sebelum_seterusnya() -> None:
    """Navigasi bawah butiran: label + syarat Sebelum/Seterusnya.

    Logik butang Sebelum/Seterusnya (dahulu dibenamkan dalam
    `_render_detail`) diekstrak kepada fungsi tulen `_label_sebelum` /
    `_label_seterusnya` di ui/pages_detail.py. Fungsi diuji unit di
    sini; semakan statik memastikan `_render_detail` masih memanggil
    fungsi (elak label/syarat dibenamkan semula dan terpisah dari
    ujian). Regresi sebenar yang ditangkap: hadis pertama papar butang
    Sebelum, atau hadis terakhir papar butang Seterusnya.
    """
    tajuk("8q. Navigasi bawah butiran: Sebelum/Seterusnya (label + syarat)")
    from ui.pages_detail import _label_sebelum, _label_seterusnya

    # --- Sebelum: hanya papar untuk hid > 1 (int) ---
    kes_sebelum = [
        ("hid=1 -> tiada Sebelum (hadis pertama)",
         _label_sebelum(1) is None),
        ("hid=2 -> '‹ No. 1'", _label_sebelum(2) == "‹ No. 1"),
        ("hid=500 -> '‹ No. 499'", _label_sebelum(500) == "‹ No. 499"),
        ("hid bukan int -> tiada Sebelum",
         _label_sebelum(None) is None and _label_sebelum("5") is None),
    ]
    for nama, ok in kes_sebelum:
        if ok:
            lulus(f"Sebelum: {nama}")
        else:
            salah(f"Sebelum: {nama}")

    # --- Seterusnya: papar kecuali di hadis terakhir (max_id diketahui) ---
    kes_seterusnya = [
        ("hid=1, max_id=0 (had tidak diketahui) -> 'No. 2 ›'",
         _label_seterusnya(1, 0) == "No. 2 ›"),
        ("hid=499, max_id=500 -> 'No. 500 ›'",
         _label_seterusnya(499, 500) == "No. 500 ›"),
        ("hid=500, max_id=500 (terakhir) -> tiada Seterusnya",
         _label_seterusnya(500, 500) is None),
        ("hid=501, max_id=500 (di luar julat) -> tiada Seterusnya",
         _label_seterusnya(501, 500) is None),
        ("hid=500, max_id=700 -> 'No. 501 ›'",
         _label_seterusnya(500, 700) == "No. 501 ›"),
        ("hid bukan int -> tiada Seterusnya",
         _label_seterusnya(None, 500) is None),
    ]
    for nama, ok in kes_seterusnya:
        if ok:
            lulus(f"Seterusnya: {nama}")
        else:
            salah(f"Seterusnya: {nama}")

    # --- _render_detail mesti guna fungsi (bukan benam label semula) ---
    # Semak BADAN _render_detail sahaja (ast.get_source_segment), bukan
    # keseluruhan fail — definisi _label_* sendiri mengandungi format
    # yang sah dan tidak sepatutnya dikira sebagai "dibenamkan".
    cari = _cari_fungsi("_render_detail")
    if cari is None:
        salah("_render_detail TIADA")
        return
    src_render, fn = cari
    badan = ast.get_source_segment(src_render, fn) or ""
    if "_label_sebelum(hid)" in badan \
            and "_label_seterusnya(hid, max_id)" in badan:
        lulus("_render_detail guna _label_sebelum/_label_seterusnya")
    else:
        salah("_render_detail TIADA guna fungsi label -- syarat dibenamkan?")
    # Label lama (format f-string dalam _render_detail) tidak kembali
    if 'f"‹ No. {hid - 1}"' not in badan \
            and 'f"No. {hid + 1} ›"' not in badan:
        lulus("tiada format label lama dibenamkan dalam _render_detail")
    else:
        salah("format label lama masih dibenamkan dalam _render_detail")


# ---------------------------------------------------------------- 8r
def semak_pemalar_render() -> None:
    """Pemalar/syarat render lain: _label_simpan + LABEL_RAWAK.

    Corak yang sama dengan 8p/8q: logik atau label yang dahulu
    dibenamkan dalam kaedah render diekstrak kepada fungsi/pemalar
    tulen dan diuji unit di sini. `_label_simpan(saved)` memetakan
    keadaan simpan kepada label butang Simpan/Tersimpan (digunakan di
    _render_detail + _toggle_save); `LABEL_RAWAK` ialah label butang
    Rawak pada bar navigasi. Semakan statik memastikan kaedah render
    masih memanggil fungsi (elak literal dibenamkan semula).
    """
    tajuk("8r. Pemalar render lain: _label_simpan + LABEL_RAWAK")
    from ui.pages_detail import _label_simpan
    from ui.app_qt import LABEL_RAWAK

    # --- _label_simpan: dua keadaan mesti betul ---
    if _label_simpan(True) == "⭐ Tersimpan":
        lulus("_label_simpan(True) -> '⭐ Tersimpan' (sudah disimpan)")
    else:
        salah(f"_label_simpan(True) -> {_label_simpan(True)!r}")
    if _label_simpan(False) == "☆ Simpan":
        lulus("_label_simpan(False) -> '☆ Simpan' (belum disimpan)")
    else:
        salah(f"_label_simpan(False) -> {_label_simpan(False)!r}")

    # --- _render_detail mesti guna fungsi (bukan benam literal semula) ---
    cari = _cari_fungsi("_render_detail")
    if cari is None:
        salah("_render_detail TIADA")
        return
    badan = ast.get_source_segment(cari[0], cari[1]) or ""
    if "_label_simpan(saved)" in badan:
        lulus("_render_detail guna _label_simpan(saved)")
    else:
        salah("_render_detail TIADA guna _label_simpan -- literal dibenamkan?")
    if '"⭐ Tersimpan" if saved else "☆ Simpan"' not in badan:
        lulus("tiada literal label Simpan dibenamkan dalam _render_detail")
    else:
        salah("literal label Simpan masih dibenamkan dalam _render_detail")

    # --- _toggle_save kemas label melalui fungsi ---
    cari = _cari_fungsi("_toggle_save")
    if cari is None:
        salah("_toggle_save TIADA")
    else:
        badan = ast.get_source_segment(cari[0], cari[1]) or ""
        if "_label_simpan(False)" in badan and "_label_simpan(True)" in badan:
            lulus("_toggle_save kemas label melalui _label_simpan")
        else:
            salah("_toggle_save TIADA guna _label_simpan -- literal?")

    # --- LABEL_RAWAK: bukan kosong + kad Rawak pada halaman utama ---
    if LABEL_RAWAK and LABEL_RAWAK.strip():
        lulus(f"LABEL_RAWAK = {LABEL_RAWAK!r} (bukan kosong)")
    else:
        salah("LABEL_RAWAK kosong")
    # 25 Ogos: butang Rawak DIPINDAHKAN dari header ke panel kanan
    # halaman utama (Split Command Center). Semakan diubah: kad Rawak
    # wujud pada ui/pages_home.py dan disambungkan ke `_random`.
    src_home = open("ui/pages_home.py", encoding="utf-8").read()
    if "Rawak" in src_home and "self._random" in src_home:
        lulus("kad Rawak (panel kanan halaman utama) sambung _random")
    else:
        salah("kad Rawak TIADA pada halaman utama")
    src_app = open("ui/app_qt.py", encoding="utf-8").read()
    # Literal label hanya dalam definisi pemalar (satu sahaja dalam fail)
    if src_app.count('"⚄  Rawak"') <= 1:
        lulus("tiada literal '⚄  Rawak' duplikat di luar pemalar")
    else:
        salah("literal '⚄  Rawak' wujud lebih dari sekali")


# ---------------------------------------------------------------- 8s
def semak_tab_lalai() -> None:
    """Pemilihan tab bahasa lalai: _tab_lalai(pref, avail).

    Logik pemilihan tab bahasa lalai pada butiran (dahulu dibenamkan
    dalam `_render_detail`): 'ind_only' -> indonesia, selainnya melayu,
    dengan fallback ke bahasa pertama yang tersedia, kemudian 'melayu'
    jika tiada langsung. Diuji unit di sini + semakan statik bahawa
    render guna fungsi (elak ternary dibenamkan semula).
    """
    tajuk("8s. Tab bahasa lalai: _tab_lalai(pref, avail)")
    from ui.pages_detail import _tab_lalai

    # NOTA: kes fallback guna set SATU elemen — next(iter(set)) tidak
    # deterministik untuk set berbilang elemen, jadi jangkaan hanya
    # jelas apabila avail mengecil kepada satu bahasa.
    kes = [
        ("pref 'both' -> melayu (tersedia)",
         _tab_lalai("both", {"melayu", "indonesia"}) == "melayu"),
        ("pref 'ind_only' -> indonesia (tersedia)",
         _tab_lalai("ind_only", {"melayu", "indonesia"}) == "indonesia"),
        ("pref 'ind_only', tiada indonesia -> guna bahasa tersedia",
         _tab_lalai("ind_only", {"english"}) == "english"),
        ("pref 'both', tiada melayu -> guna bahasa tersedia",
         _tab_lalai("both", {"indonesia"}) == "indonesia"),
        ("avail kosong -> 'melayu' (fallback)",
         _tab_lalai("both", set()) == "melayu"),
    ]
    for nama, ok in kes:
        if ok:
            lulus(nama)
        else:
            salah(nama)

    # --- _render_detail mesti guna fungsi (bukan benam ternary semula) ---
    cari = _cari_fungsi("_render_detail")
    if cari is None:
        salah("_render_detail TIADA")
        return
    badan = ast.get_source_segment(cari[0], cari[1]) or ""
    if "first = _tab_lalai(pref, avail)" in badan:
        lulus("_render_detail guna _tab_lalai(pref, avail)")
    else:
        salah("_render_detail TIADA guna _tab_lalai -- ternary dibenamkan?")
    if '("indonesia" if pref == "ind_only" else "melayu")' not in badan:
        lulus("tiada ternary pilihan tab dibenamkan dalam _render_detail")
    else:
        salah("ternary pilihan tab masih dibenamkan dalam _render_detail")


# ---------------------------------------------------------------- 8t
def semak_bab_tafsir() -> None:
    """Tag 'Bab Tafsir': _ialah_bab_tafsir(collection, book).

    Logik penentuan bab tafsir Al-Quran (dahulu dibenamkan di DUA
    tempat: kad hasil carian di ui/widgets.py + halaman butiran di
    ui/pages_detail.py) diekstrak kepada fungsi tulen
    `_ialah_bab_tafsir`. Diuji unit di sini + semakan statik bahawa
    kedua-dua tempat guna fungsi (elak duaan hanyut / dibenamkan
    semula).
    """
    tajuk("8t. Tag 'Bab Tafsir': _ialah_bab_tafsir(collection, book)")
    from ui.widgets import BAB_TAFSIR, _ialah_bab_tafsir

    kes = [
        (f"bukhari 65 -> True (BAB_TAFSIR[bukhari]={BAB_TAFSIR['bukhari']})",
         _ialah_bab_tafsir("bukhari", 65) is True),
        (f"muslim 56 -> True (BAB_TAFSIR[muslim]={BAB_TAFSIR['muslim']})",
         _ialah_bab_tafsir("muslim", 56) is True),
        (f"tirmidzi 47 -> True (BAB_TAFSIR[tirmidzi]={BAB_TAFSIR['tirmidzi']})",
         _ialah_bab_tafsir("tirmidzi", 47) is True),
        ("bukhari 1 -> False (bukan bab tafsir)",
         _ialah_bab_tafsir("bukhari", 1) is False),
        ("muslim 47 -> False (nombor milik tirmidzi)",
         _ialah_bab_tafsir("muslim", 47) is False),
        ("collection kosong / book None -> False",
         _ialah_bab_tafsir("", None) is False),
    ]
    for nama, ok in kes:
        if ok:
            lulus(nama)
        else:
            salah(nama)

    # --- Kad carian (widgets.py) guna fungsi, bukan literal ---
    src_w = open("ui/widgets.py", encoding="utf-8").read()
    if '_ialah_bab_tafsir(hadis.get("collection"), hadis.get("book"))' \
            in src_w:
        lulus("kad carian guna _ialah_bab_tafsir")
    else:
        salah("kad carian TIADA guna _ialah_bab_tafsir -- literal?")
    if 'BAB_TAFSIR.get(hadis.get("collection")) == hadis.get("book")' \
            not in src_w:
        lulus("tiada literal BAB_TAFSIR dibenamkan dalam kad carian")
    else:
        salah("literal BAB_TAFSIR masih dibenamkan dalam kad carian")

    # --- Butiran (_render_detail) guna fungsi, bukan literal ---
    cari = _cari_fungsi("_render_detail")
    if cari is None:
        salah("_render_detail TIADA")
        return
    badan = ast.get_source_segment(cari[0], cari[1]) or ""
    if '_ialah_bab_tafsir(h.get("collection"), h.get("book"))' in badan:
        lulus("_render_detail guna _ialah_bab_tafsir")
    else:
        salah("_render_detail TIADA guna _ialah_bab_tafsir -- literal?")
    if 'BAB_TAFSIR.get(h.get("collection"))' not in badan:
        lulus("tiada literal BAB_TAFSIR dibenamkan dalam _render_detail")
    else:
        salah("literal BAB_TAFSIR masih dibenamkan dalam _render_detail")


# ---------------------------------------------------------------- 8t2
def semak_draf_jawapan() -> None:
    """Draf jawapan AI: bahagian 'Carian Biasa (Keyword)' benar-benar berjalan.

    `compose_draft_answer` (core/draft_answer.py) membaca hasil padanan
    TEPAT dari `api.search_hadis`. Sebelum ini ia dipanggil dengan
    `per_page=5` (parameter sebenar ialah `limit`) dan membaca
    `exact["data"]["results"]` (struktur sebenar ialah
    `{"hadis": [...], "meta": {...}}`) -- kedua-dua kesilapan melempar
    TypeError yang ditangkap SENYAP oleh `except Exception`, jadi
    `exact_results` sentiasa kosong dan bahagian "Carian Biasa (Keyword)"
    TIDAK pernah muncul dalam kotak jawapan draf AI. Semakan ini
    mengunci corak BETUL supaya regresi dikesan.
    """
    tajuk("8t2. Draf jawapan: carian biasa (keyword) benar-benar dipapar")
    src = open("core/draft_answer.py", encoding="utf-8").read()
    if "search_hadis(query, limit=5)" in src and "per_page=5" not in src:
        lulus("search_hadis dipanggil dengan limit=5 (bukan per_page=5)")
    else:
        salah("search_hadis mesti dipanggil limit=5 -- per_page=5 melempar "
              "TypeError yang ditangkap senyap")
    if 'exact.get("hadis")' in src \
            and 'exact["data"]["results"]' not in src:
        lulus("hasil exact dibaca dari exact['hadis'] (bukan data.results)")
    else:
        salah("hasil exact mesti dibaca exact['hadis'] -- struktur pulangan "
              "search_hadis ialah {\"hadis\": [...]}")


# ---------------------------------------------------------------- 8u
def semak_pilih_terjemahan() -> None:
    """Keutamaan bahasa petikan kad: _pilih_terjemahan(...).

    Kad hasil carian memilih petikan terjemahan dengan keutamaan
    Melayu > Indonesia > English (dahulu dibenamkan sebagai rantaian
    `or` dalam `hadith_card`). Diekstrak kepada fungsi tulen
    `_pilih_terjemahan`; diuji unit di sini + semakan statik bahawa
    kad guna fungsi (elak rantaian `or` dibenamkan semula).
    """
    tajuk("8u. Keutamaan terjemahan kad: _pilih_terjemahan(...)")
    from ui.widgets import _pilih_terjemahan

    kes = [
        ("Melayu ada -> Melayu",
         _pilih_terjemahan("teks BM", "teks ID", "teks EN") == "teks BM"),
        ("Melayu kosong, Indonesia ada -> Indonesia",
         _pilih_terjemahan("", "teks ID", "teks EN") == "teks ID"),
        ("Melayu+Indonesia tiada, English ada -> English",
         _pilih_terjemahan(None, "", "teks EN") == "teks EN"),
        ("Melayu hanya ruang -> Indonesia",
         _pilih_terjemahan("   ", "teks ID", None) == "teks ID"),
        ("Semua tiada -> ''",
         _pilih_terjemahan(None, None, None) == ""),
        ("Teks dilucutkan (strip)",
         _pilih_terjemahan("  teks BM  ", "", "") == "teks BM"),
    ]
    for nama, ok in kes:
        if ok:
            lulus(nama)
        else:
            salah(nama)

    # --- hadith_card guna fungsi, bukan rantaian or ---
    src_w = open("ui/widgets.py", encoding="utf-8").read()
    if 'trans = _pilih_terjemahan(_ms, hadis.get("indonesia"),' in src_w:
        lulus("hadith_card guna _pilih_terjemahan")
    else:
        salah("hadith_card TIADA guna _pilih_terjemahan -- rantaian or?")
    if '(_ms or hadis.get("indonesia")' not in src_w:
        lulus("tiada rantaian or keutamaan dibenamkan dalam kad")
    else:
        salah("rantaian or keutamaan masih dibenamkan dalam kad")


# ---------------------------------------------------------------- 8v
def semak_elide_chip() -> None:
    """Potongan kad: elide() + syarat chip _papar_chip().

    `elide` (potongan teks kad: normalisasi ruang + potong pada
    sempadan perkataan + ellipsis) digunakan di 3 tempat dalam kad
    (bab 44, arab, terjemahan) tetapi TIADA ujian langsung — diuji di
    sini. Syarat chip `if show_chip and kitab_name:` diekstrak kepada
    `_papar_chip` + semakan statik bahawa kad guna fungsi.
    """
    tajuk("8v. Potongan kad: elide() + syarat chip _papar_chip()")
    from ui.widgets import elide, _papar_chip

    kes_elide = [
        ("teks pendek kekal penuh (tiada …)",
         elide("Teks pendek", 44) == "Teks pendek"),
        ("ruang berlebihan dinormalisasi",
         elide("a  b   c", 44) == "a b c"),
        ("teks kosong -> ''", elide("", 10) == ""),
        ("None -> ''", elide(None, 10) == ""),
        ("potong + ellipsis (n=4)",
         elide("abcdef", 4) == "abcd…"),
        ("potong pada sempadan perkataan (tiada ruang tergantung)",
         elide("abc def", 4) == "abc…"),
        ("panjang hasil <= n + 1 (ellipsis)",
         all(len(elide("x" * 200, n)) <= n + 1
             for n in (10, 44, 150, 190))),
    ]
    for nama, ok in kes_elide:
        if ok:
            lulus(f"elide: {nama}")
        else:
            salah(f"elide: {nama}")

    kes_chip = [
        ("show_chip + nama ada -> True",
         _papar_chip(True, "Sahih Bukhari") is True),
        ("nama kosong -> False", _papar_chip(True, "") is False),
        ("show_chip False -> False",
         _papar_chip(False, "Sahih Bukhari") is False),
        ("nama None -> False", _papar_chip(True, None) is False),
    ]
    for nama, ok in kes_chip:
        if ok:
            lulus(f"chip: {nama}")
        else:
            salah(f"chip: {nama}")

    # --- hadith_card guna fungsi, bukan literal ---
    # Parse ui/widgets.py terus (hadith_card tinggal DI SINI, bukan
    # mixin — _cari_fungsi tidak mencarinya) dan semak BADAN fungsi
    # sahaja, supaya sebutan dalam docstring _papar_chip sendiri tidak
    # dikira sebagai benaman.
    import ast as _ast
    src_w = open("ui/widgets.py", encoding="utf-8").read()
    pokok = _ast.parse(src_w)
    fn_kad = next((n for n in _ast.walk(pokok)
                   if isinstance(n, _ast.FunctionDef)
                   and n.name == "hadith_card"), None)
    if fn_kad is None:
        salah("hadith_card TIADA dalam ui/widgets.py")
    else:
        badan = _ast.get_source_segment(src_w, fn_kad) or ""
        if "if _papar_chip(show_chip, kitab_name):" in badan:
            lulus("hadith_card guna _papar_chip")
        else:
            salah("hadith_card TIADA guna _papar_chip -- literal?")
        if "if show_chip and kitab_name:" not in badan:
            lulus("tiada 'if show_chip and kitab_name:' dibenamkan")
        else:
            salah("syarat chip masih dibenamkan dalam hadith_card")

    # --- _warna_cip: warna cip ikut makna klasifikasi (Sesi 55 #5) ---
    # Palet HIJAU = sahih/sah, MERAH = palsu/ditolak, AMBER = lemah,
    # tiada padanan = neutral (None -> kekal TEAL). Nilai dibaca dari
    # modul tema pada masa render jadi ikut tema terang/gelap.
    from ui.pages_detail import _warna_cip
    import ui.theme as _th
    kes_warna_cip = [
        ("Muttafaq 'alayh -> HIJAU",
         _warna_cip("Muttafaq 'alayh") ==
         (_th.GREEN_BG, _th.GREEN_TEXT, _th.GREEN_BORDER)),
        ("Sahih -> HIJAU", _warna_cip("Sahih") is not None
         and _warna_cip("Sahih")[0] == _th.GREEN_BG),
        ("Hasan -> HIJAU", _warna_cip("Hasan") is not None
         and _warna_cip("Hasan")[0] == _th.GREEN_BG),
        ("صحيح (grade HE) -> HIJAU", _warna_cip("صحيح") is not None
         and _warna_cip("صحيح")[0] == _th.GREEN_BG),
        ("Palsu -> MERAH", _warna_cip("Palsu") is not None
         and _warna_cip("Palsu")[0] == _th.RED_BG),
        ("Munkar -> MERAH", _warna_cip("Munkar") is not None
         and _warna_cip("Munkar")[0] == _th.RED_BG),
        ("Batil -> MERAH", _warna_cip("Batil") is not None
         and _warna_cip("Batil")[0] == _th.RED_BG),
        ("Lemah -> AMBER", _warna_cip("Lemah") is not None
         and _warna_cip("Lemah")[0] == _th.AMBER_BG),
        ("Daif -> AMBER", _warna_cip("Daif") is not None
         and _warna_cip("Daif")[0] == _th.AMBER_BG),
        ("ضعيف -> AMBER", _warna_cip("ضعيف") is not None
         and _warna_cip("ضعيف")[0] == _th.AMBER_BG),
        ("tanpa padanan -> neutral (None)",
         _warna_cip("Disebutkan tanpa penilaian") is None),
    ]
    for nama, ok in kes_warna_cip:
        if ok:
            lulus(f"_warna_cip: {nama}")
        else:
            salah(f"_warna_cip: {nama}")


# ---------------------------------------------------------------- 8w
def semak_kitab_shell() -> None:
    """Banner + kotak lompat kitab: _label_kiraan + _julat_lompat.

    `_render_kitab_shell` (pages_kitab.py) membina banner kitab dan
    placeholder kotak 'Lompat No. hadis' — kedua-duanya memformat
    `total` hanya bila ia int (data koleksi belum dimuat -> kosong /
    "No. hadis"). Banner berkongsi `_label_kiraan` (ui/pages.py) dengan
    kad koleksi (semak 8x) — `kata="hadis"`, fallback ''. Kotak lompat
    kekal fungsi sendiri kerana formatnya julat '0–N', bukan koma
    ribuan. Diuji unit + semakan statik bahawa render guna fungsi.
    """
    tajuk("8w. Banner + kotak lompat kitab: _label_kiraan + _julat_lompat")
    from ui.pages import _label_kiraan
    from ui.pages_kitab import _julat_lompat

    kes_banner = [
        ("total=7008 -> '7,008 hadis' (koma ribuan)",
         _label_kiraan(7008, "hadis", "") == "7,008 hadis"),
        ("total=0 -> '0 hadis'",
         _label_kiraan(0, "hadis", "") == "0 hadis"),
        ("total None -> '' (koleksi belum dimuat)",
         _label_kiraan(None, "hadis", "") == ""),
        ("total bukan int -> ''",
         _label_kiraan("7008", "hadis", "") == ""),
    ]
    for nama, ok in kes_banner:
        if ok:
            lulus(f"_label_kiraan (banner): {nama}")
        else:
            salah(f"_label_kiraan (banner): {nama}")

    kes_julat = [
        ("total=7008 -> '0–7008'", _julat_lompat(7008) == "0–7008"),
        ("total=0 -> '0–0'", _julat_lompat(0) == "0–0"),
        ("total None -> 'No. hadis'", _julat_lompat(None) == "No. hadis"),
        ("total bukan int -> 'No. hadis'",
         _julat_lompat("7008") == "No. hadis"),
    ]
    for nama, ok in kes_julat:
        if ok:
            lulus(f"_julat_lompat: {nama}")
        else:
            salah(f"_julat_lompat: {nama}")

    # --- _render_kitab_shell guna fungsi kongsi, bukan literal ---
    # 26 Ogos: banner dipecahkan ke _kitab_banner(); semakan ini kini
    # mengesahkan _label_kiraan DAN _julat_lompat digunakan di mana-mana
    # dalam modul (bukan corak Hero lama yang dibuang).
    cari = _cari_fungsi("_render_kitab_shell")
    if cari is None:
        salah("_render_kitab_shell TIADA")
        return
    src_k = open("ui/pages_kitab.py", encoding="utf-8").read()
    if "_label_kiraan(total, \"hadis\", \"\")" in src_k \
            and "_julat_lompat(total)" in src_k:
        lulus("_render_kitab_shell guna _label_kiraan + _julat_lompat")
    else:
        salah("_render_kitab_shell TIADA guna fungsi -- literal?")
    # Literal format total HANYA diharamkan dalam badan _render_kitab_shell
    # (banner meta dahulu). Footer "Menunjukkan X–Y daripada Z hadis" di
    # luar metod itu adalah teks sah. Carian skop ke `badan`, bukan src_k.
    if 'f"{total:,} hadis"' not in badan and 'f"0–{total}"' not in badan:
        lulus("tiada literal format total dibenamkan dalam render")
    else:
        salah("literal format total masih dibenamkan dalam render")

    # --- fungsi lama `_subtitle_hadis` dibuang (digantikan kongsi) ---
    # Semak definisi/panggilan sahaja, bukan sebutan docstring.
    src_k = open("ui/pages_kitab.py", encoding="utf-8").read()
    if "def _subtitle_hadis" not in src_k and "_subtitle_hadis(" not in src_k:
        lulus("_subtitle_hadis dibuang dari pages_kitab")
    else:
        salah("_subtitle_hadis masih ada dalam pages_kitab")


# ---------------------------------------------------------------- 8x
def semak_kad_koleksi() -> None:
    """Kad koleksi halaman utama: _label_kiraan(total, 'Hadis', '— Hadis').

    `KitabCard` (ui/pages.py) memaparkan jumlah hadis pada kad koleksi
    — dahulu dibenamkan di DUA tempat (`__init__` + `set_total` selepas
    muat data async) dengan format `f"{total:,} Hadis" bila int, else
    "— Hadis"; kemudian fungsi sendiri `_label_kad_hadis`. Kini satu
    fungsi kongsi `_label_kiraan` (dikongsi dengan banner kitab, semak
    8w) dengan `kata="Hadis"`, fallback "— Hadis". Diuji unit + semakan
    statik bahawa kedua-dua laluan guna fungsi (elak format hanyut
    antara bina kad dan kemas kini async).
    """
    tajuk("8x. Kad koleksi utama: _label_kiraan(total, 'Hadis', '— Hadis')")
    from ui.pages import _label_kiraan

    kes = [
        ("total=7008 -> '7,008 Hadis' (koma ribuan)",
         _label_kiraan(7008, "Hadis", "— Hadis") == "7,008 Hadis"),
        ("total=0 -> '0 Hadis'",
         _label_kiraan(0, "Hadis", "— Hadis") == "0 Hadis"),
        ("total None -> '— Hadis' (belum dimuat)",
         _label_kiraan(None, "Hadis", "— Hadis") == "— Hadis"),
        ("total bukan int -> '— Hadis'",
         _label_kiraan("7008", "Hadis", "— Hadis") == "— Hadis"),
    ]
    for nama, ok in kes:
        if ok:
            lulus(nama)
        else:
            salah(nama)

    # --- KitabCard guna fungsi di KEDUA-DUA laluan, bukan literal ---
    # Parse ui/pages.py terus (KitabCard bukan mixin -- _cari_fungsi
    # tidak mencarinya) dan semak badan KELAS sahaja.
    import ast as _ast
    src_p = open("ui/pages.py", encoding="utf-8").read()
    pokok = _ast.parse(src_p)
    cls = next((n for n in _ast.walk(pokok)
                if isinstance(n, _ast.ClassDef)
                and n.name == "KitabCard"), None)
    if cls is None:
        salah("KitabCard TIADA dalam ui/pages.py")
    else:
        badan = _ast.get_source_segment(src_p, cls) or ""
        if '_label_kiraan(total, "Hadis", "— Hadis")' in badan \
                and '_label_kiraan(n, "Hadis", "— Hadis")' in badan:
            lulus("KitabCard guna _label_kiraan (bina + set_total)")
        else:
            salah("KitabCard TIADA guna _label_kiraan -- literal?")
        if 'f"{total:,} Hadis"' not in badan \
                and 'f"{n:,} Hadis"' not in badan:
            lulus("tiada literal label hadis dibenamkan dalam KitabCard")
        else:
            salah("literal label hadis masih dibenamkan dalam KitabCard")

    # --- fungsi lama `_label_kad_hadis` dibuang (digantikan kongsi) ---
    # Semak definisi/panggilan sahaja, bukan sebutan docstring.
    if "def _label_kad_hadis" not in src_p and "_label_kad_hadis(" not in src_p:
        lulus("_label_kad_hadis dibuang dari pages.py")
    else:
        salah("_label_kad_hadis masih ada dalam pages.py")

    # --- set_total / _cnt: tiada penulis atau pemanggil luar ---
    # Audit laluan kad (Sesi 54): `set_total` hanya dipanggil dari
    # `_on_collections` (app_qt.py) + ujian visual; `_cnt` (label
    # jumlah kad) hanya ditulis dalam pages.py (__init__ + set_total),
    # kedua-duanya melalui `_label_kiraan` yang berpagar isinstance.
    # Pemanggil/penulis baharu yang tidak berpagar akan GAGAL di sini.
    import glob as _glob
    luar_cnt = []
    luar_set = []
    for _p in _senarai_py_projek():
        _p = _p.replace("\\", "/")  # Windows: ui\pages.py -> ui/pages.py
        if any(_d in _p for _d in _SKIP_FOLDER) or _p == "semak.py":
            continue
        _s = open(_p, encoding="utf-8").read()
        for _m in re.finditer(r"\._cnt\s*=|._cnt\.setText\(", _s):
            if _p != "ui/pages.py":
                luar_cnt.append(f"{_p}:{_s.count(chr(10), 0, _m.start()) + 1}")
        for _m in re.finditer(r"\.set_total\(", _s):
            if _p not in ("ui/app_qt.py", "uji_visual_kiraan.py"):
                luar_set.append(f"{_p}:{_s.count(chr(10), 0, _m.start()) + 1}")
    if luar_cnt:
        salah(f"penulis _cnt di luar pages.py: {luar_cnt}")
    else:
        lulus("_cnt hanya ditulis dalam pages.py (__init__ + set_total)")
    if luar_set:
        salah(f"set_total dipanggil di luar _on_collections/ujian: {luar_set}")
    else:
        lulus("set_total hanya dari _on_collections (app_qt.py) + ujian visual")


# ---------------------------------------------------------------- 8y
def semak_visual_kiraan() -> None:
    """Ujian visual _label_kiraan (banner + kad) kekal + konsisten.

    `uji_visual_kiraan.py` mengesahkan output `_label_kiraan` pada
    WIDGET SEBENAR (kad koleksi + banner kitab) dan tangkapan skrin
    fizikal — lapisan ketiga selepas unit 8w/8x. Semakan ini mengunci
    fail itu wujud dan konsisten dengan pelaksanaan: mesti merujuk
    `_label_kiraan`, kedua-dua kata ('hadis'/'Hadis'), kad (`_cnt`),
    banner (`_kitab_root`), laluan fallback `set_total`, dan tangkapan
    skrin fizikal (ImageGrab). Kalau pelaksanaan dinamakan semula dan
    ujian tidak diikuti, penanda ini hilang -- suite utama menandakan.
    """
    tajuk("8y. Ujian visual _label_kiraan (banner + kad)")
    p_uji = os.path.join(BASE, "uji_visual_kiraan.py")
    if not os.path.exists(p_uji):
        salah("uji_visual_kiraan.py TIADA — banner/kad tanpa ujian visual")
        return
    lulus("uji_visual_kiraan.py wujud")

    usrc = open(p_uji, encoding="utf-8").read()
    wajib = ("from ui.pages import _label_kiraan", "_kitab_cards",
             "._cnt", "set_total", "_kitab_root", "_julat_lompat",
             "skrin_fizikal", "ImageGrab", "7,008")
    hilang = [m for m in wajib if m not in usrc]
    if hilang:
        salah(f"uji_visual_kiraan.py tidak konsisten: tiada {hilang}")
        return
    lulus("uji_visual_kiraan.py konsisten (fungsi/kad/banner/fallback/skrin)")


# ---------------------------------------------------------------- 8z
def semak_visual_rujukan() -> None:
    """Kesemua ujian visual skrin kekal + dirujuk dalam senarai semak.

    `uji_visual_*.py` ialah pengesahan skrin SEBENAR yang dijalankan
    manual sebelum hantar (senarai semak MANUAL_REFERENSI_DEV.md).
    Senarai tetap `UJI_VISUAL` mengunci: (1) tiap fail kekal wujud
    (pemadaman dikesan), (2) tiap fail disebut dalam bahagian "Senarai
    semak sebelum hantar" (senarai semak tidak ketinggalan), dan (3)
    fail uji_visual_* baharu di luar senarai turut dikesan (senarai
    semak perlu dikemas). Status untracked pula sudah ditanda oleh
    semakan 9.
    """
    tajuk("8z. Ujian visual skrin: kesemua fail kekal + dirujuk")
    UJI_VISUAL = ("uji_visual_bantuan.py", "uji_visual_carian.py",
                  "uji_visual_kiraan.py",
                  "uji_visual_mockup.py", "uji_visual_piksel.py",
                  "uji_visual_ralat.py", "uji_visual_sebenar.py")

    hilang = [f for f in UJI_VISUAL if not os.path.exists(f)]
    if hilang:
        salah(f"uji_visual_* dibuang: {hilang}")
    else:
        lulus(f"kesemua {len(UJI_VISUAL)} ujian visual kekal wujud")

    import glob as _glob
    wujud = sorted(os.path.basename(p)
                   for p in _glob.glob("uji_visual_*.py"))
    baharu = [f for f in wujud if f not in UJI_VISUAL]
    if baharu:
        salah(f"uji_visual_* baharu belum dalam senarai semak: {baharu}")
    else:
        lulus("tiada ujian visual di luar senarai tetap")

    # Tiap fail dirujuk dalam bahagian senarai semak pra-hantar
    if not os.path.exists("dokumen/manual/MANUAL_REFERENSI_DEV.md"):
        salah("dokumen/manual/MANUAL_REFERENSI_DEV.md TIADA — "
              "senarai semak hilang")
        return
    manual = open("dokumen/manual/MANUAL_REFERENSI_DEV.md",
                  encoding="utf-8").read()
    mula = manual.find("## 9. Senarai semak sebelum hantar")
    if mula == -1:
        salah("senarai semak pra-hantar TIADA dalam MANUAL_REFERENSI_DEV.md")
        return
    tamat = manual.find("\n## ", mula + 1)
    blok = manual[mula:tamat if tamat != -1 else len(manual)]
    tiada = [f for f in UJI_VISUAL if f not in blok]
    if tiada:
        salah(f"senarai semak pra-hantar TIADA sebut: {tiada}")
    else:
        lulus("kesemua ujian visual disebut dalam senarai semak pra-hantar")


def semak_versi_changelog() -> None:
    """Cap versi dikunci ke edaran rasmi + CHANGELOG.md selaras.

    `VERSI.py` ialah satu-satunya sumber cap versi (semakan 10
    mengesahkan CIRI). Semakan ini menambah: (1) VERSI dikunci pada
    "1.0" -- edaran rasmi semasa; naikkan di sini SENGAJA apabila
    versi baharu dilancarkan, (2) CHANGELOG.md kekal wujud, dan (3)
    setiap versi sejarah 1.0-1.3 + versi semasa ada seksyen `## x.y`
    dalam CHANGELOG.md -- menukar cap di VERSI.py tanpa menyusuli
    CHANGELOG akan GAGAL.
    """
    tajuk("10b. Cap versi dikunci + CHANGELOG.md selaras")

    sys.path.insert(0, BASE)
    try:
        from VERSI import VERSI
    except Exception as e:
        salah(f"VERSI.py: {e}")
        return
    lulus(f"VERSI.py dibaca (v{VERSI})")

    if VERSI != "1.0":
        salah(f"VERSI dikunci 1.0 (edaran rasmi), sebenar {VERSI!r}")
    else:
        lulus("VERSI == '1.0' (edaran rasmi dikunci)")

    if not os.path.exists("dokumen/perubahan/CHANGELOG.md"):
        salah("dokumen/perubahan/CHANGELOG.md TIADA -- "
              "log perubahan versi hilang")
        return
    changelog = open("dokumen/perubahan/CHANGELOG.md",
                     encoding="utf-8").read()

    seksyen = set(re.findall(r"^## (\d+\.\d+)(?:\s|$)", changelog, re.M))
    sejarah = ("1.0", "1.1", "1.2", "1.3")
    tiada = [v for v in sejarah if v not in seksyen]
    if tiada:
        salah(f"CHANGELOG.md tiada seksyen versi: {tiada}")
    else:
        lulus("seksyen versi 1.0-1.3 ada dalam CHANGELOG.md")

    if VERSI not in seksyen:
        salah(f"CHANGELOG.md tiada seksyen versi semasa (## {VERSI} ...)")
    else:
        lulus(f"CHANGELOG.md selaras dengan cap v{VERSI}")


# ---------------------------------------------------------------- 10aa
def semak_logo_palet() -> None:
    """Logo (bina_logo.py) selaras dengan palet theme.py.

    Sesi 55 (palet hangat): logo mockup mesti guna warna TEMA sebenar
    (TEAL hijau mockup, TEAL_DARK, CARD_BG, AMBER_TEXT) -- bukan hex
    TEAL biru lama. Splash ialah teks dari dict tema jadi bertukar
    automatik; logo raster dijana dari bina_logo.py. Semakan ini
    mengunci: warna logo sepadan theme.py supaya logo tidak tersasar
    jika sesiapa menukar palet kemudian.
    """
    tajuk("10aa. Logo (bina_logo.py) selaras dengan palet theme.py")

    import re as _re
    import ui.theme as _t
    try:
        bl = open(os.path.join("scripts", "bina_logo.py"),
                  encoding="utf-8").read()
    except OSError:
        salah("scripts/bina_logo.py TIADA")
        return

    def _hex_tema(k):
        return (_t.THEMES.get(_t.CURRENT_THEME) or _t.DARK).get(k, "")

    padanan = [
        # (pemboleh ubah logo, kunci theme, nama)
        ("BUKU_TEAL = ", "TEAL", "buku (hijau mockup)"),
        ("BUKU_TEAL_TERANG = ", "TEAL_LIGHT", "buku terang"),
        ("BG_GRAD_A = ", "TEAL_DARK", "latar grad atas"),
        ("BG_GRAD_B = ", "CARD_BG", "latar grad bawah"),
        ("CAHAYA = ", "AMBER_TEXT", "cahaya ambar"),
    ]
    for var, kunci, nama in padanan:
        hexa = _hex_tema(kunci)
        # cari baris "VAR = "#hex"  (nota selepas # dibenarkan)
        m = _re.search(r"^%s\"(#[0-9A-Fa-f]{6})\"" % _re.escape(var),
                       bl, _re.M)
        if not m:
            salah(f"bina_logo.py tiada {var!r}")
            continue
        if m.group(1).lower() == hexa.lower():
            lulus(f"logo {nama} = {hexa} (padan theme)")
        else:
            salah(f"logo {nama}: {m.group(1)} != tema {hexa}")

    # Ikon lama TEAL biru mesti TIDAK wujud dalam palet logo
    if re.search(r"#[0-9A-Fa-f]{6}", bl) and "#7FC4DE" in bl.upper():
        salah("bina_logo.py masih guna TEAL biru lama (#7FC4DE)")
    else:
        lulus("tiada hex TEAL biru lama dalam bina_logo.py")


def semak_deklarasi() -> None:
    """Deklarasi Pustaka Hadis dikunci: teks + cantuman UI.

    DEKLARASI.md (8 Ogos 2026) diterima pakai sebagai skrin permulaan
    (sekali) + halaman Tentang. Semakan ini mengunci: (1) ui/deklarasi.py
    wujud dengan bendera `deklarasi_dibaca`, URL SemakHadis, dan kelas
    DeklarasiDialog; (2) teks mengandungi fakta kunci (62,169, BUKAN,
    fatwa); (3) app_qt.py memanggil _tunjuk_deklarasi_pertama pada
    showEvent; (4) panel Tetapan ada butang Tentang; (5) halaman Carian
    memaut SemakHadis.com pada keadaan tiada hasil.
    """
    tajuk("8aa. Deklarasi Pustaka Hadis: teks + cantuman dikunci")

    if not os.path.exists("ui/deklarasi.py"):
        salah("ui/deklarasi.py TIADA -- deklarasi hilang")
        return
    dk = open("ui/deklarasi.py", encoding="utf-8").read()

    if 'DEKLARASI_FLAG = "deklarasi_dibaca"' in dk:
        lulus("bendera 'deklarasi_dibaca' ada")
    else:
        salah("bendera deklarasi_dibaca TIADA dalam ui/deklarasi.py")

    if "SEMAKHADIS_URL" in dk and "class DeklarasiDialog" in dk:
        lulus("URL SemakHadis + kelas DeklarasiDialog ada")
    else:
        salah("URL SemakHadis / DeklarasiDialog TIADA")

    fakta = ("62,169", "BUKAN", "SemakHadis.com", "fatwa")
    tiada = [f for f in fakta if f not in dk]
    if tiada:
        salah(f"teks deklarasi tiada fakta kunci: {tiada}")
    else:
        lulus("teks deklarasi ada fakta kunci (62,169 / BUKAN / fatwa)")

    # Atribusi: 3 sumber mesti dipapar dalam app DAN ayat penuh kekal
    # dalam DEKLARASI.md. Sejak 19 Ogos halaman Tentang ialah JADUAL 2
    # lajur (QTableWidget), jadi ayat dipecahkan kepada label sel kiri +
    # sumber pautan sel kanan. Semak label + nama sumber pada
    # ui/deklarasi.py dan ayat penuh ternormal pada DEKLARASI.md.
    def _norm_dek(s):
        s = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", s)  # pautan md -> teks
        s = s.replace("**", "").replace("`", "")
        return re.sub(r"\s+", " ", s).strip()

    if not os.path.exists("dokumen/rujukan/DEKLARASI.md"):
        salah("dokumen/rujukan/DEKLARASI.md TIADA -- deklarasi hilang")
        return
    dek = _norm_dek(open("dokumen/rujukan/DEKLARASI.md",
                         encoding="utf-8").read())
    atribusi = (
        ("Teks hadis, terjemahan", "hadis.my",
         "Teks hadis, terjemahan Melayu & Indonesia: hadis.my "
         "— API Hadis Malaysia"),
        ("Terjemahan Inggeris", "fawazahmed0/hadith-api",
         "Terjemahan Inggeris & darjat ulama: koleksi "
         "fawazahmed0/hadith-api (domain awam), berasal daripada "
         "sunnah.com"),
        ("Huraian ringkas", "SemakHadis.com",
         "Huraian ringkas: SemakHadis.com — dipaparkan tanpa sebarang "
         "pengubahsuaian, dengan atribusi pada setiap huraian"),
    )
    rosak = []
    for label, sumber, ayat in atribusi:
        if label not in dk or sumber not in dk:
            rosak.append(f"app kehilangan: {label} / {sumber}")
        if _norm_dek(ayat) not in dek:
            rosak.append("DEKLARASI.md kehilangan: " + ayat)
    if rosak:
        salah("atribusi tidak sepadan: " + "; ".join(rosak))
    else:
        lulus("atribusi 3 sumber sepadan (jadual Tentang == DEKLARASI.md)")

    # 25 Ogos: dialog deklarasi larian pertama kini di ui/disclaimer.py
    # (papar_disclaimer dipanggil dari main.py) — bukan lagi app_qt.py
    # (cantuman lama dibuang pada komit 65543f8, "dialog berganda").
    src_main = open("main.py", encoding="utf-8").read()
    src_dis = open("ui/disclaimer.py", encoding="utf-8").read()
    if "papar_disclaimer" in src_main and "DisclaimerDialog" in src_dis \
            and "_sudah_baca" in src_dis:
        lulus("deklarasi larian pertama: main.py + ui/disclaimer.py")
    else:
        salah("TIADA cantuman deklarasi pertama (main.py/disclaimer.py)")

    sp = open("ui/settings_panel.py", encoding="utf-8").read()
    if "_sec_tentang" in sp and "DeklarasiDialog" in sp \
            and "penuh=True" in sp:
        lulus("panel Tetapan: butang Tentang (deklarasi penuh)")
    else:
        salah("panel Tetapan TIADA butang Tentang")

    pc = open("ui/pages_carian.py", encoding="utf-8").read()
    if "SEMAKHADIS_URL" in pc and "semak di SemakHadis.com" in pc:
        lulus("halaman Carian: pautan SemakHadis pada tiada hasil")
    else:
        salah("halaman Carian TIADA pautan SemakHadis")


def semak_peraturan_sisa() -> None:
    """Ujian peraturan fail sisa: suntik fail, sahkan dikesan, buang.

    Peraturan `_senarai_untracked_git` mesti menangkap sebarang fail
    sisa baharu (cth. `4.65.0`). Ujian ini mencipta fail ujian, sahkan
    ia dilaporkan sebagai untracked, kemudian memadamnya. Kegagalan
    peraturan (tidak dikesan) akan menyebabkan fail ujian itu KEKAL
    dan dilaporkan semula oleh semak_bersih pada run seterusnya.
    """
    tajuk("9b. Peraturan fail sisa (untracked git)")
    # Folder pengguna (hasil ekstrak ZIP edaran) BUKAN repo git --
    # `git status` tiada, jadi peraturan untracked tidak bermakna di
    # sana. Hanya uji apabila repo git wujud (folder pembangunan).
    if not os.path.isdir(os.path.join(BASE, ".git")):
        lulus("folder bukan repo git (edaran ZIP) -- peraturan fail sisa dilangkau")
        return
    ujian = "__uji_peraturan_sisa__.tmp"
    laluan = os.path.join(BASE, ujian)
    try:
        with open(laluan, "w") as f:
            f.write("fail ujian sementara -- mesti dikesan")
        senarai = _senarai_untracked_git()
        if ujian in senarai:
            lulus("fail sisa untracked dikesan")
        else:
            salah("fail sisa untracked TIDAK dikesan")
            print("    NOTA: fail ujian dikekalkan supaya semak_bersih "
                  "melaporkannya pada run seterusnya.")
            return
    finally:
        if os.path.exists(laluan):
            os.remove(laluan)


def semak_bersih() -> None:
    tajuk("9. Fail yang tidak patut diedar")
    # Buang __pycache__ yang dicipta oleh semakan import di atas --
    # ia artifak skrip ini sendiri, bukan kesilapan pengguna.
    import shutil
    for d in glob.glob("__pycache__") + glob.glob("*/__pycache__"):
        shutil.rmtree(d, ignore_errors=True)

    kotor = []
    data_kerja = []
    for corak in ("__pycache__", "*/__pycache__", ".env"):
        kotor += glob.glob(corak)
    # Fail sisa: untracked oleh git -- lihat `_senarai_untracked_git`.
    # PENGECUALIAN: fail SAH yang belum di-commit dalam sesi ini
    # (spesifikasi mockup + ujian visual baharu) — mesti di-commit
    # sebelum hantar, bukan dibuang. Senarai ini dikemas per sesi.
    DIBENARKAN_UNTRAKCED = ("mockup/mockup_abudaud4177.html",
                            "mockup/mockup_bukhari1.html",
                            "mockup/mockup_ibnumajah2094.html",
                            "mockup/mockup_nasai2117.html",
                            "uji_visual_mockup.py", "uji_visual_piksel.py",
                            "uji_pra_hantar.py", "profil_semak.py",
                            "buka_hari.py", "ui/disclaimer.py",
                            "uji_carian_arab.py",
                            "dokumen/audit/AHMAD_DIGITAL.md",
                            "dokumen/audit/AHMAD_HOCR.md",
                            "dokumen/audit/AHMAD_HOCR_SAMPEL_5.json",
                            "dokumen/audit/CARIAN_ARAB.md",
                            "dokumen/audit/GTAF.md",
                            "dokumen/audit/TERJEMAHAN_AHMAD_DARIMI.md",
                            "dokumen/rujukan/DRAF_carian_arab.md",
                            "dokumen/rujukan/PERMOHONAN_LESEN_AHMAD.md",
                            "dokumen/rujukan/BANDING_INSTALLER.md",
                            "dokumen/rujukan/PENYELARASAN_KHAS.md",
                            "dokumen/rujukan/PERBANDINGAN_INSTALLER.md")
    untracked_asal = _senarai_untracked_git()
    untracked = [f for f in untracked_asal
                 if f not in DIBENARKAN_UNTRAKCED]
    kotor += untracked
    # Fail data kerja aktif: apps mencipta/membaca ini setiap kali
    # berjalan (pangkalan hadis, cache SemakHadis, penanda buku).
    # Ia DIBENARKAN wujud semasa pembangunan -- memadam hadis.db
    # menghapus seluruh koleksi. Hanya buang sebelum bungkus ZIP.
    # user_settings.json = data app tempatan (gitignored, dicipta semula
    # oleh app). Dulu dibuang selepas semakan pelancaran, tetapi itu
    # menghilangkan bendera `deklarasi_dibaca` -> dialog deklarasi modal
    # menyekat ujian app berikutnya dalam mod offscreen. Kini dipulihkan
    # (lihat _pulihkan_settings) dan dianggap data kerja.
    for corak in (".cache_sema", ".cache_eng", ".cache_he", "hadis.db",
                  "hadis.db-wal", "hadis.db-shm", "bookmarks.json",
                  "user_settings.json", "profil_model.json", "sunnah_map",
                  "mockup"):
        data_kerja += glob.glob(corak)
    for k in DIBENARKAN_UNTRAKCED:
        if k in untracked_asal:
            lulus(f"fail sah belum di-commit (commit sebelum hantar): {k}")
    if kotor:
        for k in kotor:
            salah(f"masih ada: {k}")
        print("\n    Bersihkan:  rm -rf " + " ".join(kotor))
    else:
        lulus("folder bersih (tiada fail artifak)")
    if data_kerja:
        for k in data_kerja:
            lulus(f"data kerja dibenarkan: {k}")
        print("    NOTA: buang fail ini sebelum bungkus ZIP untuk hantar.")
    else:
        lulus("tiada fail data kerja")


def semak_kiraan_readme() -> None:
    """README 'N semakan (M bahagian)' seiring kiraan runtime semak.py.

    Skop imbas (contoh _SKIP_FOLDER) mengubah bilangan lulus() secara
    senyap — README menjadi lapuk. Semakan ini membandingkan tuntutan
    README dengan kiraan sebenar dan GAGAL apabila berbeza, jadi README
    tidak perlu dikemas manual. Baris pengesahan semakan ini sendiri
    TIDAK dikira (dicetak terus, bukan via lulus()) — mengelak rujukan
    kendiri (README menuntut kiraan semakan aplikasi, bukan meta-semak).
    Persekitaran tidak lengkap (hadis.db tiada / --audit-sunnah) -> nota,
    bukan kegagalan (bilangan semakan berubah dengan kehadiran data).
    """
    tajuk("16. README kiraan semakan seiring semak.py")
    if LULUS_CNT == 0:
        # Dipanggil bersendirian (contoh mutasi uji_negatif): tiada
        # semakan lain dalam larian ini — tidak bermakna untuk
        # dibandingkan. Larian penuh (`python semak.py`) yang bererti.
        print("    nota: dipanggil bersendirian -- bandingan dilangkau")
        return
    if not os.path.exists(os.path.join(BASE, "hadis.db")):
        print("    nota: hadis.db tiada -- kiraan semakan berubah, "
              "semakan dilangkau")
        return
    if any(a == "--audit-sunnah" or a.startswith("--audit-sunnah=")
           for a in sys.argv):
        print("    nota: --audit-sunnah menambah semakan -- dilangkau")
        return
    p = os.path.join(BASE, "README.md")
    isi = open(p, encoding="utf-8").read()
    m = re.search(r"(\d+) semakan \((\d+) bahagian\)", isi)
    if not m:
        salah("README tiada tuntutan 'N semakan (M bahagian)'")
        return
    claim_n, claim_b = int(m.group(1)), int(m.group(2))
    sebenar_n, sebenar_b = LULUS_CNT, bilangan_bahagian()
    if claim_n != sebenar_n or claim_b != sebenar_b:
        salah(f"README kata {claim_n} semakan ({claim_b} bahagian), "
              f"semak.py lulus {sebenar_n} ({sebenar_b} bahagian) — "
              f"kemas kini README")
        return
    print(f"    OK    README {claim_n} semakan ({claim_b} bahagian) == "
          f"semak.py")


def main() -> int:
    global LULUS_CNT, TAJUK_NAMA
    LULUS_CNT, TAJUK_NAMA = 0, []
    print("\n" + "=" * 60)
    print("  SEMAKAN PRA-HANTAR — Pustaka Hadis")
    print("=" * 60)

    semak_sintaks()
    semak_import()
    semak_warna_lalai()
    semak_crlf()
    semak_joinpath()
    semak_migrasi()
    semak_translit()
    semak_syarah()
    semak_bahasa()
    semak_bahasa_ui()
    semak_peraturan_bahasa()
    semak_bandingan()
    semak_peta_sunnah()
    if any(a == "--audit-sunnah" or a.startswith("--audit-sunnah=")
           for a in sys.argv):
        semak_audit_sunnah()
    semak_pemula()
    semak_profil_model()
    semak_padanan_eng()
    semak_hadeethenc()
    semak_sema()
    semak_gabungan()
    semak_carian_sibuk()
    semak_peta_kembali()
    semak_nav_sebelum_seterusnya()
    semak_pemalar_render()
    semak_tab_lalai()
    semak_bab_tafsir()
    semak_draf_jawapan()
    semak_pilih_terjemahan()
    semak_elide_chip()
    semak_kitab_shell()
    semak_kad_koleksi()
    semak_visual_kiraan()
    semak_visual_rujukan()
    semak_deklarasi()
    semak_bahasa_dokumen()
    semak_susunatur()
    semak_apl()
    semak_versi_fail()
    semak_versi_changelog()
    semak_logo_palet()
    semak_dokumen()
    semak_sesi_terakhir()
    semak_kontras_tema()
    semak_rtl_dokumen()
    semak_ringkasan_keadaan()
    semak_peraturan_sisa()
    semak_bersih()
    semak_kiraan_readme()

    print("\n" + "=" * 60)
    if gagal:
        print(f"  {len(gagal)} KEGAGALAN — jangan hantar lagi")
        for g in gagal:
            print(f"    - {g}")
        print("=" * 60 + "\n")
        return 1
    print(f"  SEMUA LULUS — {LULUS_CNT} semakan "
          f"({bilangan_bahagian()} bahagian), selamat dihantar")
    print("=" * 60 + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
