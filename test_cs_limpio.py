"""Self-check for cs_limpio. Run: py -3.12 test_cs_limpio.py

Builds synthetic PDFs (no real scans in the repo) and checks both modes.
"""
import tempfile
from pathlib import Path

import pymupdf

from cs_limpio import ZONA_DEFECTO, limpiar, zona_rect

W, H = 595, 842


def pixmap(w, h, color):
    pm = pymupdf.Pixmap(pymupdf.csRGB, pymupdf.IRect(0, 0, w, h), False)
    pm.set_rect(pm.irect, color)
    return pm


def pdf_con_objeto(path, paginas=3):
    """Big scan image + small badge image shared by every page (CamScanner layout)."""
    doc = pymupdf.open()
    xref_marca = 0
    for _ in range(paginas):
        page = doc.new_page(width=W, height=H)
        page.insert_image(pymupdf.Rect(58, 0, 537, 790), pixmap=pixmap(400, 600, (200, 200, 200)))
        xref_marca = page.insert_image(pymupdf.Rect(500, 802, 580, 832),
                                       pixmap=pixmap(240, 90, (0, 0, 0)), xref=xref_marca)
    doc.save(path)
    doc.close()


def pdf_fundido(path):
    """One full-page scan with the badge baked into its pixels."""
    pm = pixmap(W, H, (200, 200, 200))
    pm.set_rect(pymupdf.IRect(500, 802, 580, 832), (0, 0, 0))
    doc = pymupdf.open()
    page = doc.new_page(width=W, height=H)
    page.insert_image(page.rect, pixmap=pm)
    doc.save(path)
    doc.close()


def esquina_blanca(path):
    """True if the badge zone renders pure white on every page."""
    doc = pymupdf.open(path)
    for page in doc:
        pm = page.get_pixmap(clip=zona_rect(page, ZONA_DEFECTO))
        if any(pm.pixel(x, y) != (255, 255, 255) for x in range(0, pm.width, 7) for y in range(0, pm.height, 7)):
            return False
    return True


def imagenes_grandes(path):
    doc = pymupdf.open(path)
    out = set()
    for page in doc:
        for img in page.get_images(full=True):
            info = doc.extract_image(img[0])
            if info["width"] > 300:  # the scan, not the 240 px badge
                out.add(info["image"])
    return out


def main():
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        # Case 1: badge as separate object
        src = d / "objeto.pdf"
        pdf_con_objeto(src)
        assert not esquina_blanca(src), "negative check: dirty PDF must fail the corner test"
        n, limpio, respaldo = limpiar(src, d / "objeto-limpio.pdf")
        assert (n, limpio, respaldo) == (3, 3, 0), (n, limpio, respaldo)
        assert esquina_blanca(d / "objeto-limpio.pdf")
        assert imagenes_grandes(src) == imagenes_grandes(d / "objeto-limpio.pdf"), "scan bytes must be untouched"

        # Case 2: badge baked into the scan -> white redaction
        src = d / "fundido.pdf"
        pdf_fundido(src)
        assert not esquina_blanca(src)
        n, limpio, respaldo = limpiar(src, d / "fundido-limpio.pdf")
        assert (n, limpio, respaldo) == (1, 0, 1), (n, limpio, respaldo)
        assert esquina_blanca(d / "fundido-limpio.pdf")
        # rest of the page unchanged
        a = pymupdf.open(src)[0].get_pixmap(clip=pymupdf.Rect(0, 0, 400, 700))
        b = pymupdf.open(d / "fundido-limpio.pdf")[0].get_pixmap(clip=pymupdf.Rect(0, 0, 400, 700))
        assert a.samples == b.samples
    print("ok")


if __name__ == "__main__":
    main()
