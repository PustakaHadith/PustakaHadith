import os, re, shutil, markdown
from xhtml2pdf import pisa

TMP = r"C:\ph_aset"
os.makedirs(TMP, exist_ok=True)

BASE = os.path.abspath("dokumen/surat/hadis.my")
LOGO = os.path.abspath("dokumen/surat/hadis.my/logo_PustakaHadith.png")
SRC = [
    ("SURAT_HADISMY.md", "SURAT_HADISMY.pdf", True),
    ("EMEL_HADISMY.md", "EMEL_HADISMY.pdf", True),
    ("../sokongan/DASAR_PRIVASI.md", "DASAR_PRIVASI.pdf", False),
    ("../sokongan/PAUTAN_SOKONGAN.md", "PAUTAN_SOKONGAN.pdf", False),
]

def local_src(p):
    p = os.path.normpath(p)
    if os.path.exists(p):
        dst = os.path.join(TMP, os.path.basename(p))
        shutil.copy(p, dst)
        return 'src="%s"' % dst.replace("\\", "/")
    return "src=''"

def conv(md_rel, out_name, with_logo):
    md_path = os.path.abspath(os.path.join(BASE, md_rel))
    text = open(md_path, encoding="utf-8").read()
    html = markdown.markdown(text, extensions=["tables", "fenced_code"])

    def fix(m):
        src = m.group(1)
        if src.lower().startswith("http"):
            return m.group(0)
        p = os.path.normpath(os.path.join(os.path.dirname(md_path), src))
        return local_src(p)

    html = re.sub(r'src="([^"]+)"', fix, html)
    if with_logo:
        html = ('<img %s style="width:190px"/><br/><br/>'
                % local_src(LOGO)) + html

    css = ("body{font-family:Helvetica,Arial,sans-serif;font-size:11pt;color:#222;}"
           "h1,h2,h3{color:#1A6B3C;} a{color:#2D7A4A;}"
           "table{border-collapse:collapse;} td,th{border:1px solid #ccc;padding:4px 7px;}"
           "img{max-width:100%;}")
    out = os.path.join(BASE, out_name)
    with open(out, "wb") as f:
        pisa.CreatePDF(html, dest=f, default_css=css)
    print("PDF", out, os.path.getsize(out), "bytes")

for md_rel, out_name, wl in SRC:
    conv(md_rel, out_name, wl)
