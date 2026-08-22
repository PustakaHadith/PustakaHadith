"""Transliterasi Arab → Rumi.

DUA GAYA
--------
transliterate(text)              gaya ilmiah/ALA-LC:  ḥaddathanā, al-shams
transliterate_malay_style(text)  gaya Melayu:         haddathana, asy-syams

PRINSIP PENTING
---------------
Baris (tashkeel) MESTI dibaca, bukan dibuang. 99.9% teks dalam hadis.db
mempunyai baris penuh — itulah satu-satunya sumber maklumat vokal.
Membuang baris dahulu menjadikan transliterasi mustahil:
    حَدَّثَنَا  tanpa baris → ح د ث ن ا → "hdthna"  (salah)
    حَدَّثَنَا  dengan baris → ḥad-da-tha-nā → "haddathana"  (betul)
"""

from __future__ import annotations

import re
import unicodedata

# ── Aksara Unicode Arab ────────────────────────────────────────────────
FATHA, DAMMA, KASRA = "\u064E", "\u064F", "\u0650"
FATHATAN, DAMMATAN, KASRATAN = "\u064B", "\u064C", "\u064D"
SHADDA, SUKUN = "\u0651", "\u0652"
DAGGER_ALIF = "\u0670"       # alif khanjariyya  ٰ
TATWEEL = "\u0640"
ALIF, WAW, YA, ALIF_MAQSURA = "\u0627", "\u0648", "\u064A", "\u0649"
TA_MARBUTA = "\u0629"

HARAKAT = {FATHA, DAMMA, KASRA}
TANWIN = {FATHATAN, DAMMATAN, KASRATAN}
# Semua tanda yang boleh muncul selepas konsonan
ALL_MARKS = HARAKAT | TANWIN | {SHADDA, SUKUN, DAGGER_ALIF}

# Tanda hentian/pengulangan al-Quran & lain-lain — dibuang sepenuhnya
STRIP_CHARS = set(
    "\u0610\u0611\u0612\u0613\u0614\u0615\u0616\u0617\u0618\u0619\u061A"
    "\u06D6\u06D7\u06D8\u06D9\u06DA\u06DB\u06DC\u06DD\u06DE\u06DF"
    "\u06E0\u06E1\u06E2\u06E3\u06E4\u06E5\u06E6\u06E7\u06E8\u06E9"
    "\u06EA\u06EB\u06EC\u06ED\u200C\u200D\u200E\u200F" + TATWEEL
)

# ── Konsonan ───────────────────────────────────────────────────────────
# (ilmiah, melayu)
CONSONANTS = {
    "\u0621": ("ʾ", ""),      # ء hamzah
    "\u0622": ("ʾā", "a"),    # آ alif madda
    "\u0623": ("ʾ", ""),      # أ
    "\u0624": ("ʾ", ""),      # ؤ
    "\u0625": ("ʾ", ""),      # إ
    "\u0626": ("ʾ", ""),      # ئ
    ALIF:     ("", ""),       # ا — pembawa vokal, dikendali khas
    "\u0628": ("b", "b"),
    TA_MARBUTA: ("h", "h"),   # ة — dikendali khas di hujung
    "\u062A": ("t", "t"),
    "\u062B": ("th", "th"),   # ث
    "\u062C": ("j", "j"),
    "\u062D": ("ḥ", "h"),     # ح
    "\u062E": ("kh", "kh"),
    "\u062F": ("d", "d"),
    "\u0630": ("dh", "dz"),   # ذ
    "\u0631": ("r", "r"),
    "\u0632": ("z", "z"),
    "\u0633": ("s", "s"),
    "\u0634": ("sh", "sy"),   # ش
    "\u0635": ("ṣ", "s"),     # ص
    "\u0636": ("ḍ", "d"),     # ض
    "\u0637": ("ṭ", "t"),     # ط
    "\u0638": ("ẓ", "z"),     # ظ
    "\u0639": ("ʿ", "'"),     # ع
    "\u063A": ("gh", "gh"),
    "\u0641": ("f", "f"),
    "\u0642": ("q", "q"),
    "\u0643": ("k", "k"),
    "\u0644": ("l", "l"),
    "\u0645": ("m", "m"),
    "\u0646": ("n", "n"),
    "\u0647": ("h", "h"),
    WAW:      ("w", "w"),
    YA:       ("y", "y"),
    ALIF_MAQSURA: ("ā", "a"),  # ى
    # Parsi/Urdu — kadang muncul
    "\u067E": ("p", "p"), "\u0686": ("ch", "c"),
    "\u0698": ("zh", "z"), "\u06AF": ("g", "g"),
    "\u06A9": ("k", "k"), "\u06CC": ("y", "y"),
}

VOWELS = {FATHA: ("a", "a"), DAMMA: ("u", "u"), KASRA: ("i", "i")}
LONG = {FATHA: ("ā", "a"), DAMMA: ("ū", "u"), KASRA: ("ī", "i")}
TANWIN_OUT = {FATHATAN: ("an", "an"), DAMMATAN: ("un", "un"),
              KASRATAN: ("in", "in")}

# Huruf syamsiyyah — "al-" berasimilasi: الشَّمْس → asy-syams
SUN_LETTERS = set("\u062A\u062B\u062F\u0630\u0631\u0632\u0633\u0634"
                  "\u0635\u0636\u0637\u0638\u0644\u0646")

# Kata sendi yang disambung dengan sempang dalam gaya Melayu
PROCLITICS_MALAY = {"wa": "wa-", "fa": "fa-", "bi": "bi-",
                    "ka": "ka-", "li": "li-", "la": "la-", "sa": "sa-"}


def _normalize(text: str) -> str:
    text = unicodedata.normalize("NFC", text or "")
    return "".join(c for c in text if c not in STRIP_CHARS)


_AL = "\u0627\u0644"

# PENTING: susunan aksara dalam teks hadis.my sebenar ialah
#   konsonan + FATHA (064E) + SHADDA (0651)
# bukan konsonan + shadda + fatha. Kunci di bawah ditulis mengikut
# susunan sebenar itu. Ujian `semak.py` mengunci tingkah laku ini --
# jika susunan diterbalikkan, "اللَّهِ" jadi "al-lahi" dan bukan "Allāhi".
LAFZ_JALALAH = {
    "\u0627\u0644\u0644\u064E\u0651\u0647": ("Allāh", "Allah"),
    "\u0627\u0644\u0644\u064E\u0651\u0647\u064F": ("Allāhu", "Allahu"),
    "\u0627\u0644\u0644\u064E\u0651\u0647\u064E": ("Allāha", "Allaha"),
    "\u0627\u0644\u0644\u064E\u0651\u0647\u0650": ("Allāhi", "Allahi"),
    "\u0644\u0650\u0644\u064E\u0651\u0647\u0650": ("lillāhi", "lillahi"),
    "\u0644\u0650\u0644\u064E\u0651\u0647": ("lillāh", "lillah"),
}


# ── Kata tunggal / tanpa baris yang kerap dalam sanad ─────────────────
# Teks hadis sering tidak memberi baris pada kata pendek. Tanpa jadual ini,
# "و" (32× dalam 3,000 hadis) menjadi "w" dan bukan "wa".
STANDALONE = {
    "\u0648": ("wa", "wa"),                 # و  kata hubung
    "\u0641": ("fa", "fa"),                 # ف
    "\u062D": ("ḥ", "h"),                   # ح  penanda taḥwīl sanad
    "\u0635": ("ṣ", "s"),                   # ص  ringkasan ṣallallāhu…
    "\u0639\u0646": ("ʿan", "'an"),        # عن
    "\u0628\u0646": ("bn", "bin"),         # بن
    "\u0645\u0646": ("min", "min"),        # من
    "\u0623\u0646": ("ʾan", "an"),         # أن
    "\u0625\u0646": ("ʾin", "in"),         # إن
    "\u0647\u0648": ("huwa", "huwa"),      # هو
    "\u0647\u064A": ("hiya", "hiya"),      # هي
    "\u0644\u0647": ("lahu", "lahu"),      # له
    "\u0644\u0627": ("lā", "la"),          # لا
    "\u0645\u0627": ("mā", "ma"),          # ما
    "\u0641\u064A": ("fī", "fi"),          # في
    "\u0642\u062F": ("qad", "qad"),        # قد
    "\u062B\u0645": ("thumma", "thumma"),  # ثم
    "\u0628\u0646\u062A": ("bint", "binti"),
    "\u0627\u0628\u0646": ("ibn", "ibnu"),
    "\u0623\u0628\u0648": ("ʾabū", "abu"),
    "\u0623\u0628\u064A": ("ʾabī", "abi"),
    "\u0627\u0644\u0644\u0647": ("Allāh", "Allah"),        # الله
    "\u0642\u0627\u0644": ("qāla", "qala"),                # قال
    "\u0635\u0644\u0649": ("ṣallā", "salla"),              # صلى
    "\u0639\u0644\u064A\u0647": ("ʿalayhi", "'alayhi"),   # عليه
    "\u0648\u0633\u0644\u0645": ("wasallam", "wa-sallam"),# وسلم
    "\u062D\u062F\u062B\u0646\u0627": ("ḥaddathanā", "haddathana"),
    "\u0631\u0633\u0648\u0644": ("rasūl", "rasul"),       # رسول
    "\u0639\u0628\u062F": ("ʿabd", "abd"),                 # عبد
    "\u0623\u0646\u0633": ("ʾAnas", "Anas"),               # أنس
    "\u0623\u0646\u0627": ("ʾanā", "ana"),                 # أنا
    "\u0628\u0646\u064A": ("banī", "bani"),                # بني
    "\u0623\u0628\u064A\u0647": ("ʾabīhi", "abihi"),      # أبيه
    "\u0639\u0646\u0647": ("ʿanhu", "'anhu"),              # عنه
    "\u0639\u0646\u0647\u0627": ("ʿanhā", "'anha"),       # عنها
    "\u0628\u0639\u062F": ("baʿda", "ba'da"),              # بعد
    "\u0642\u0628\u0644": ("qabla", "qabla"),              # قبل
    "\u0639\u0644\u0649": ("ʿalā", "'ala"),                # على
    "\u0625\u0644\u0649": ("ʾilā", "ila"),                 # إلى
    "\u0623\u0648": ("ʾaw", "au"),                          # أو
    "\u062B\u0645": ("thumma", "thumma"),                   # ثم
    # Nama perawi biasa tanpa baris
    "\u0645\u0627\u0644\u0643": ("Mālik", "Malik"),
    "\u0645\u062D\u0645\u062F": ("Muḥammad", "Muhammad"),
    "\u0639\u0645\u0631": ("ʿUmar", "Umar"),
    "\u0639\u0644\u064A": ("ʿAlī", "Ali"),
    "\u0639\u062B\u0645\u0627\u0646": ("ʿUthmān", "Uthman"),
    "\u0623\u062D\u0645\u062F": ("ʾAḥmad", "Ahmad"),
    "\u064A\u062D\u064A\u0649": ("Yaḥyā", "Yahya"),
    "\u0633\u0641\u064A\u0627\u0646": ("Sufyān", "Sufyan"),
    "\u0646\u0627\u0641\u0639": ("Nāfiʿ", "Nafi'"),
    "\u0639\u0627\u0626\u0634\u0629": ("ʿĀʾishah", "Aisyah"),
    "\u0647\u0631\u064A\u0631\u0629": ("Hurayrah", "Hurairah"),
    "\u0627\u0644\u0646\u0628\u064A": ("al-Nabī", "an-Nabi"),
}


def _guess_bare(word: str, style: int) -> str:
    """Anggaran untuk kata tanpa baris: sisip 'a' antara konsonan.
    Alif/waw/ya dianggap vokal panjang."""
    out = []
    for idx, ch in enumerate(word):
        if ch == ALIF:
            out.append("ā" if style == 0 else "a")
            continue
        if ch == ALIF_MAQSURA:
            out.append("ā" if style == 0 else "a")
            continue
        base = CONSONANTS.get(ch, ("", ""))[style]
        if not base:
            continue
        # waw/ya di tengah/hujung selepas konsonan -> vokal panjang
        if ch == WAW and idx > 0 and word[idx - 1] not in (ALIF, WAW, YA):
            out.append("ū" if style == 0 else "u")
            continue
        if ch == YA and idx > 0 and word[idx - 1] not in (ALIF, WAW, YA):
            out.append("ī" if style == 0 else "i")
            continue
        out.append(base)
        nxt = word[idx + 1] if idx + 1 < len(word) else ""
        if nxt and nxt not in (ALIF, ALIF_MAQSURA, WAW, YA):
            out.append("a")
    r = "".join(out)
    return r[:-1] if r.endswith("a") and len(r) > 2 else r


_SHADDA = "\u0651"


def _susun_baris(word: str) -> str:
    """Normalkan susunan shadda supaya sentiasa SELEPAS vokal.

    Teks berbeza menulis shadda sebelum atau selepas baris vokal.
    Kedua-duanya sah Unicode dan kelihatan sama, tetapi padanan
    rentetan gagal. Fungsi ini menjadikan susunan konsisten.
    """
    if _SHADDA not in word:
        return word
    out = []
    i = 0
    while i < len(word):
        c = word[i]
        if c == _SHADDA and i + 1 < len(word) and word[i + 1] in VOWELS:
            out.append(word[i + 1])
            out.append(c)
            i += 2
            continue
        out.append(c)
        i += 1
    return "".join(out)


def _word(word: str, style: int) -> str:
    """style: 0 = ilmiah, 1 = melayu."""
    if word in STANDALONE:
        return STANDALONE[word][style]

    # Kata langsung tiada baris (0.13% data) — mustahil tahu vokal sebenar.
    # Sisip 'a' sebagai anggaran supaya boleh dibaca, bukan rentetan konsonan.
    if len(word) > 2 and not any(c in ALL_MARKS for c in word) \
            and all(c in CONSONANTS for c in word):
        return _guess_bare(word, style)
    jw = _susun_baris(word)
    if jw in LAFZ_JALALAH:
        return LAFZ_JALALAH[jw][style]
    for k, v in LAFZ_JALALAH.items():
        if jw.endswith(k) and len(jw) > len(k):
            head = _word(jw[:len(jw) - len(k)], style)
            return head + v[style]
    out: list[str] = []
    i, n = 0, len(word)
    skip_next_shadda = False

    # Kata sandang al- / ال — juga selepas kata sendi (بِالـ، وَالـ، لِلـ)
    art = ""
    pre = ""
    m0 = re.match(r"^([\u0628\u0648\u0641\u0643\u0644])([\u064E\u0650])"
                  r"(\u0627\u0644)", word)
    if m0:
        pre = CONSONANTS[m0.group(1)][style] + VOWELS[m0.group(2)][style] + "-"
        word = word[m0.end() - 2:]      # sisakan "ال"
        n = len(word)

    if word.startswith("\u0627\u0644") and n > 2:
        nxt = word[2]
        if nxt in SUN_LETTERS:
            c = CONSONANTS.get(nxt, ("", ""))[style]
            art = ("a" + c + "-") if style else "al-"
            i = 2
            skip_next_shadda = True
        else:
            art = "al-"
            i = 2
    elif word[:1] == ALIF and n > 1 and word[1] in HARAKAT:
        pass

    while i < n:
        ch = word[i]

        # Alif: panjangkan vokal sebelumnya, atau 'a' jika di awal
        if ch == ALIF:
            if out and out[-1] in ("a", "ā"):
                out[-1] = "a" if style else "a"
                if not style:
                    out[-1] = "ā"
            elif not out:
                out.append("a")
            i += 1
            continue

        if ch == DAGGER_ALIF:
            if out and out[-1] == "a":
                out[-1] = "a" if style else "ā"
            i += 1
            continue

        if ch not in CONSONANTS:
            if ch not in ALL_MARKS:
                out.append(ch)
            i += 1
            continue

        # Konsonan
        base = CONSONANTS[ch][style]
        i += 1

        # Kumpul SEMUA tanda selepas konsonan — susunannya boleh berbeza:
        #   ح + fatha            (konsonan bervokal)
        #   د + fatha + shadda   (susunan biasa dalam hadis.db)
        #   د + shadda + fatha   (susunan alternatif)
        marks = []
        while i < n and word[i] in ALL_MARKS:
            marks.append(word[i])
            i += 1

        if base:
            dbl = SHADDA in marks and not skip_next_shadda
            out.append(base + base if dbl else base)
        skip_next_shadda = False

        # Ambil vokal/tanwin daripada kumpulan tanda
        m = next((x for x in marks if x in VOWELS or x in TANWIN), None)
        if DAGGER_ALIF in marks and m is None:
            m = FATHA
            marks.append(DAGGER_ALIF)

        if m is not None:
            if m in VOWELS:
                nxt = word[i] if i < n else ""
                after = word[i + 1] if i + 1 < n else ""
                is_long = (
                    (m == FATHA and nxt in (ALIF, ALIF_MAQSURA)) or
                    (m == FATHA and DAGGER_ALIF in marks) or
                    (m == DAMMA and nxt == WAW and after not in ALL_MARKS) or
                    (m == KASRA and nxt == YA and after not in ALL_MARKS)
                )
                out.append((LONG if is_long else VOWELS)[m][style])
                if is_long and nxt in (ALIF, ALIF_MAQSURA, WAW, YA):
                    i += 1
            elif m in TANWIN:
                out.append(TANWIN_OUT[m][style])
                if i < n and word[i] in (ALIF, ALIF_MAQSURA):
                    i += 1

    return pre + art + "".join(out)


def _post(word: str, style: int) -> str:
    if not word:
        return word
    if style:  # gaya Melayu
        for p, rep in PROCLITICS_MALAY.items():
            if word.startswith(p) and len(word) > len(p) + 1 and \
                    not word.startswith(p + "-"):
                pass  # dikendali di peringkat kata, bukan di sini
    return word


def transliterate(text: str) -> str:
    """Gaya ilmiah (ALA-LC): ḥaddathanā, al-shams, ʿUmar."""
    t = _normalize(text)
    return " ".join(w for w in (_word(x, 0) for x in t.split()) if w)


def transliterate_malay_style(text: str) -> str:
    """Gaya Melayu: haddathana, asy-syams, 'Umar."""
    t = _normalize(text)
    words = [_word(x, 1) for x in t.split()]
    out = []
    for w in words:
        if not w:
            continue
        # sempang selepas kata sendi ringkas (wa, fa, bi, ka, li)
        m = re.match(r"^(wa|fa|bi|ka|li)([a-z'].{2,})$", w)
        if m and not w.startswith(("wal-", "bil-", "fal-")):
            w = f"{m.group(1)}-{m.group(2)}"
        out.append(w)
    return " ".join(out)


def romanize(text: str) -> str:
    return transliterate(text)


def strip_tashkeel(text: str) -> str:
    """Buang baris — untuk padanan/carian, BUKAN transliterasi."""
    t = _normalize(text)
    return "".join(c for c in t if c not in ALL_MARKS)


if __name__ == "__main__":
    tests = [
        "حَدَّثَنَا", "مُحَمَّدٌ", "الشَّمْس", "إِنَّمَا الْأَعْمَالُ بِالنِّيَّاتِ",
        "رَسُولُ اللَّهِ", "عَنْ أَبِي هُرَيْرَةَ", "الْحَمْدُ لِلَّهِ",
        "كِتَابٌ", "مَسْجِدٌ", "الرَّحْمَٰنِ",
    ]
    w = max(len(t) for t in tests)
    print(f"{'ARAB':<{w}}  {'ILMIAH':<32}  MELAYU")
    print("─" * (w + 70))
    for t in tests:
        print(f"{t:<{w}}  {transliterate(t):<32}  {transliterate_malay_style(t)}")
