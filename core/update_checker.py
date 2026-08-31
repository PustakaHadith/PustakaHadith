"""Update checker - semak versi terkini di GitHub & sediakan pautan kemas kini.

Tambahan murni untuk app. SEMUA panggilan rangkaian GAGAL SENYAP
(kembali None) supaya app tidak terjejas bila tiada internet / API
terhad. Logik versi tulen diasingkan (`banding_versi`) untuk ujian unit.
"""
from __future__ import annotations

import re

import requests

# TODO: set kepada "owner/PustakaHadith" sebenar bila repo di-push ke GitHub.
REPO = "PustakaHadith/PustakaHadith"
API_URL = f"https://api.github.com/repos/{REPO}/releases/latest"
MASA_TAMAU = 10


def _norm(v: str) -> tuple:
    """Tukar "v1.0.2" / "1.0" kepada tuple int, cth (1, 0, 2)."""
    v = (v or "").lstrip().lstrip("vV").strip()
    return tuple(int(x) for x in re.findall(r"\d+", v))


def banding_versi(v_sekarang: str, v_terkini: str) -> int:
    """-1 = terkini lebih baharu, 0 = sama, 1 = semasa lebih baharu/setara.

    Perbandingan leksikografi tuple supaya "1.0.1" > "1.0" dan
    "1.10" > "1.9".
    """
    a, b = _norm(v_sekarang), _norm(v_terkini)
    if a == b:
        return 0
    n = max(len(a), len(b))
    a2 = a + (0,) * (n - len(a))
    b2 = b + (0,) * (n - len(b))
    return -1 if a2 < b2 else 1


def semak_versi_terkini(timeout: int = MASA_TAMAU) -> dict | None:
    """Ambil rilis terkini dari GitHub. Pulangkan dict atau None.

    dict = {"tag": str, "installer_url": str, "page_url": str}
    """
    try:
        r = requests.get(
            API_URL,
            timeout=timeout,
            headers={"Accept": "application/vnd.github+json"},
        )
        if r.status_code != 200:
            return None
        d = r.json()
        tag = d.get("tag_name") or d.get("name") or ""
        if not tag:
            return None
        html = d.get("html_url", "")
        installer = ""
        for a in (d.get("assets") or []):
            if (a.get("name") or "").lower().endswith(".exe"):
                installer = a.get("browser_download_url", "")
                break
        return {"tag": tag, "installer_url": installer, "page_url": html}
    except Exception:
        return None
