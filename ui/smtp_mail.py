"""Hantar e-mel terus melalui SMTP — digunakan oleh dialog 'Lapor Ralat'.

Pelayan & kredential dibaca dari tetapan apl (diisi sekali oleh
pembangun di Tetapan → Pelayan E-mel). Tiada kredential di-hardcode.

Keperluan: akaun e-mel yang membenarkan SMTP (cth. Gmail dengan
"kata laluan apl"). Gmail menguatkuasakan 'From' = akaun yang login,
jadi e-mel pelapor dimasukkan ke dalam badan oleh pemanggil.
"""

from __future__ import annotations

import smtplib
import ssl
from email.message import EmailMessage


def hantar_emel_smtp(kepada: str, subjek: str, badan: str, cfg: dict) -> None:
    """Hantar e-mel. Melemparkan pengecualian jika gagal.

    cfg: {"host", "port", "user", "pass", "from" (pilihan)}.
    """
    host = (cfg.get("host") or "").strip()
    user = (cfg.get("user") or "").strip()
    pw = cfg.get("pass") or ""
    if not host or not user or not pw:
        raise ValueError("Tetapan SMTP tidak lengkap")
    try:
        port = int(cfg.get("port", 587) or 587)
    except (TypeError, ValueError):
        port = 587
    daripada = (cfg.get("from") or user).strip()

    msg = EmailMessage()
    msg["Subject"] = subjek
    msg["From"] = daripada
    msg["To"] = kepada
    msg.set_content(badan)

    context = ssl.create_default_context()
    with smtplib.SMTP(host, port, timeout=20) as srv:
        srv.ehlo()
        srv.starttls(context=context)
        srv.ehlo()
        srv.login(user, pw)
        srv.send_message(msg)
