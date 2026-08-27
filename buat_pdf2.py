import os, re, shutil, markdown
from html.parser import HTMLParser
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
    TableStyle, Image, ListFlowable, ListItem, Preformatted, HRFlowable)
from reportlab.lib.utils import ImageReader

TMP = r"C:\ph_aset"
os.makedirs(TMP, exist_ok=True)
BASE = os.path.abspath("dokumen/surat/hadis.my")
LOGO = os.path.abspath("dokumen/surat/hadis.my/logo_PustakaHadith.png")

TEAL = colors.HexColor("#1A6B3C")
GREY = colors.HexColor("#555555")
CELL = colors.HexColor("#F2F2F2")

body = ParagraphStyle("body", fontName="Helvetica", fontSize=9.5, leading=13,
                      spaceAfter=4)
h1 = ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=15, leading=18,
                    textColor=TEAL, spaceBefore=10, spaceAfter=6)
h2 = ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=12, leading=15,
                    textColor=TEAL, spaceBefore=9, spaceAfter=4)
h3 = ParagraphStyle("h3", fontName="Helvetica-Bold", fontSize=10.5, leading=13,
                    textColor=TEAL, spaceBefore=7, spaceAfter=3)
quote = ParagraphStyle("quote", parent=body, leftIndent=12, textColor=GREY,
                       fontName="Helvetica-Oblique")
code_st = ParagraphStyle("code", fontName="Courier", fontSize=8, leading=10,
                         backColor=colors.HexColor("#F4F4F4"), borderPadding=4,
                         spaceAfter=4)
cell_st = ParagraphStyle("cell", fontName="Helvetica", fontSize=8.5, leading=11)
cell_hd = ParagraphStyle("cellh", parent=cell_st, fontName="Helvetica-Bold",
                         textColor=colors.white)

INLINE_OPEN = {"b": "<b>", "strong": "<b>", "i": "<i>", "em": "<i>", "u": "<u>"}
INLINE_CLOSE = {"b": "</b>", "strong": "</b>", "i": "</i>", "em": "</i>", "u": "</u>"}


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


class Conv(HTMLParser):
    def __init__(self, base_dir):
        super().__init__(convert_charrefs=True)
        self.base = base_dir
        self.out = []
        self.buf = None          # current block inline buffer (str) or None
        self.mode = None         # 'p','h1'..'h3','quote','pre'
        self.list_items = None   # list of Paragraph when in ul/ol
        self.list_kind = None
        self.rows = None
        self.cur_row = None
        self.cell = None

    def _open(self, tag, attrs):
        if tag in INLINE_OPEN:
            self.buf += INLINE_OPEN[tag]
        elif tag == "a":
            href = dict(attrs).get("href", "#")
            self.buf += '<a href="%s">' % esc(href)
        elif tag == "br":
            self.buf += "<br/>"
        elif tag == "code":
            self.buf += '<font face="Courier">'
        elif tag == "span" or tag == "div":
            pass

    def _close(self, tag):
        if tag in INLINE_CLOSE:
            self.buf += INLINE_CLOSE[tag]
        elif tag == "a":
            self.buf += "</a>"
        elif tag == "code":
            self.buf += "</font>"
        elif tag in ("span", "div"):
            pass

    def _flush(self):
        if self.buf is None:
            return
        txt = self.buf.strip()
        if txt:
            st = {"p": body, "h1": h1, "h2": h2, "h3": h3, "quote": quote}[self.mode]
            self.out.append(Paragraph(txt, st))
        self.buf = None

    def handle_starttag(self, tag, attrs):
        if tag in ("h1", "h2", "h3", "p", "blockquote"):
            self._flush()
            self.mode = {"h1": "h1", "h2": "h2", "h3": "h3",
                         "p": "p", "blockquote": "quote"}[tag]
            self.buf = ""
        elif tag == "pre":
            self._flush(); self.mode = "pre"; self.buf = ""
        elif tag == "ul":
            self.list_kind = "bullet"; self.list_items = []
        elif tag == "ol":
            self.list_kind = "1"; self.list_items = []
        elif tag == "li":
            self.buf = ""
        elif tag == "table":
            self.rows = []; self.cur_row = []
        elif tag in ("td", "th"):
            self.cell = ""
        elif tag == "img":
            self._img(dict(attrs))
        elif tag == "hr":
            self.out.append(HRFlowable(width="100%", thickness=0.6,
                                       color=colors.HexColor("#CCCCCC"),
                                       spaceBefore=4, spaceAfter=4))
        elif self.buf is not None:
            self._open(tag, attrs)
        # else: ignore stray tags

    def handle_endtag(self, tag):
        if tag in ("h1", "h2", "h3", "p", "blockquote", "pre"):
            if self.mode == "pre":
                self.out.append(Preformatted(self.buf, code_st))
                self.buf = None; self.mode = None
            else:
                self._flush()
        elif tag == "li":
            if self.list_items is not None:
                self.list_items.append(Paragraph(self.buf.strip(), body))
            self.buf = None
        elif tag in ("ul", "ol"):
            if self.list_items:
                items = [ListItem(p, leftIndent=10) for p in self.list_items]
                self.out.append(ListFlowable(items, bulletType=self.list_kind,
                                             start="1"))
            self.list_items = None; self.list_kind = None
        elif tag == "tr":
            if self.cur_row:
                self.rows.append(self.cur_row); self.cur_row = []
        elif tag in ("td", "th"):
            self.cur_row.append(self.cell); self.cell = None
        elif tag == "table":
            self._table()
        elif self.buf is not None:
            self._close(tag)

    def handle_data(self, data):
        if self.cell is not None:
            self.cell += esc(data)
        elif self.buf is not None:
            self.buf += esc(data)

    def _img(self, attrs):
        src = attrs.get("src", "")
        if not src or src.lower().startswith("http"):
            return
        p = os.path.normpath(os.path.join(self.base, src))
        if not os.path.exists(p):
            return
        try:
            iw, ih = ImageReader(p).getSize()
        except Exception:
            return
        maxw = 16 * cm
        maxh = 22 * cm
        r = min(maxw / iw, maxh / ih, 1.0)
        self.out.append(Image(p, width=iw * r, height=ih * r))
        self.out.append(Spacer(1, 4))

    def _table(self):
        if not self.rows:
            self.rows = None
            return
        data = []
        for r in self.rows:
            data.append([Paragraph(c, cell_st) for c in r])
        t = Table(data, repeatRows=1, hAlign="LEFT")
        style = [("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#BBBBBB")),
                 ("VALIGN", (0, 0), (-1, -1), "TOP"),
                 ("LEFTPADDING", (0, 0), (-1, -1), 4),
                 ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                 ("TOPPADDING", (0, 0), (-1, -1), 3),
                 ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]
        if data:
            style.append(("BACKGROUND", (0, 0), (-1, 0), TEAL))
            for c in range(len(data[0])):
                data[0][c] = Paragraph(data[0][c].text, cell_hd)
        t.setStyle(TableStyle(style))
        self.out.append(t)
        self.rows = None


def md_to_flows(md_path, with_logo):
    txt = open(md_path, encoding="utf-8").read()
    html = markdown.markdown(txt, extensions=["tables", "fenced_code"])
    c = Conv(os.path.dirname(md_path))
    c.feed(html)
    flows = []
    if with_logo and os.path.exists(LOGO):
        iw, ih = ImageReader(LOGO).getSize()
        r = min((5 * cm) / iw, 1.0)
        flows.append(Image(LOGO, width=iw * r, height=ih * r))
        flows.append(Spacer(1, 8))
    flows += c.out
    return flows


def conv(md_rel, out_name, with_logo):
    md_path = os.path.abspath(os.path.join(BASE, md_rel))
    flows = md_to_flows(md_path, with_logo)
    out = os.path.join(BASE, out_name)
    doc = SimpleDocTemplate(out, pagesize=A4, leftMargin=2 * cm,
                            rightMargin=2 * cm, topMargin=2 * cm,
                            bottomMargin=2 * cm,
                            title=os.path.splitext(out_name)[0])
    try:
        doc.build(flows)
    except PermissionError:
        out2 = os.path.join(BASE, "SURAT_HADISMY_kemas.pdf")
        print("  (SURAT_HADISMY.pdf terkunci) tulis ke", out2)
        flows = md_to_flows(md_path, with_logo)  # bina semula (build pertama mutate flow)
        doc = SimpleDocTemplate(out2, pagesize=A4, leftMargin=2 * cm,
                                rightMargin=2 * cm, topMargin=2 * cm,
                                bottomMargin=2 * cm,
                                title=os.path.splitext(out_name)[0])
        doc.build(flows)
        out = out2
    print("PDF", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    conv("SURAT_HADISMY.md", "SURAT_HADISMY.pdf", True)
    conv("EMEL_HADISMY.md", "EMEL_HADISMY.pdf", True)
    conv("../sokongan/DASAR_PRIVASI.md", "DASAR_PRIVASI.pdf", False)
    conv("../sokongan/PAUTAN_SOKONGAN.md", "PAUTAN_SOKONGAN.pdf", False)
