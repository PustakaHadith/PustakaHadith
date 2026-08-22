"""Fasa 2 — transliterasi Arab → Rumi."""
from utils.bahasa import terjemah_ralat
from utils.transliteration import transliterate, transliterate_malay_style

_EMPTY = {"rumi": "", "rumi_malay_style": "", "status": "kosong"}


def transliterate_arabic(text):
    if not text or not text.strip():
        return dict(_EMPTY)
    cleaned = " ".join(text.split())
    try:
        return {
            "rumi": transliterate(cleaned),
            "rumi_malay_style": transliterate_malay_style(cleaned),
            "status": "berjaya",
        }
    except Exception as e:
        return {"rumi": "", "rumi_malay_style": "",
                "status": "ralat", "error": terjemah_ralat(e)}
