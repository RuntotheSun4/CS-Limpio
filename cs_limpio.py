"""CS-Limpio: removes the "Scanned with CamScanner" badge from a scanned PDF.

CamScanner places the badge as a separate small image object in the bottom-right
corner of every page. We delete that object, so the scan itself is untouched
(no re-encoding, no white patch). If a page has no such object (badge baked into
the scan), we fall back to a white redaction over the corner zone.

Usage:
    cs-limpio scan.pdf                 -> writes scan-limpio.pdf next to it
    cs-limpio scan.pdf --salida out.pdf
    cs-limpio scan.pdf --zona 0.80,0.93,1,1   (page fractions x0,y0,x1,y1)
"""
import argparse
import sys
from pathlib import Path

import pymupdf

# Badge zone as fractions of the page (x0, y0, x1, y1). Measured on CamScanner
# output: badge at (500,802)-(580,832) on a 595x842 page.
ZONA_DEFECTO = (0.80, 0.93, 1.0, 1.0)
# ponytail: any image smaller than 5 % of the page sitting in the zone is the badge.
AREA_MAX = 0.05


def zona_rect(page, zona):
    w, h = page.rect.width, page.rect.height
    return pymupdf.Rect(zona[0] * w, zona[1] * h, zona[2] * w, zona[3] * h)


def imagenes_marca(page, zona):
    """xrefs of small images that intersect the badge zone."""
    z = zona_rect(page, zona)
    area_pagina = page.rect.width * page.rect.height
    xrefs = []
    for img in page.get_images(full=True):
        xref = img[0]
        for r in page.get_image_rects(xref):
            if r.intersects(z) and (r.width * r.height) < AREA_MAX * area_pagina:
                xrefs.append(xref)
                break
    return xrefs


def limpiar(entrada, salida, zona=ZONA_DEFECTO):
    """Clean `entrada` into `salida`. Returns (pages, cleaned_as_object, cleaned_by_redaction)."""
    doc = pymupdf.open(entrada)
    borrados = set()
    limpio = respaldo = 0
    for page in doc:
        xrefs = imagenes_marca(page, zona)
        if xrefs:
            for xref in xrefs:
                if xref not in borrados:
                    page.delete_image(xref)  # object is shared, so one call clears every page
                    borrados.add(xref)
            limpio += 1
        else:
            page.add_redact_annot(zona_rect(page, zona), fill=(1, 1, 1))
            page.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_PIXELS)
            respaldo += 1
    doc.save(salida, garbage=4)  # no deflate: leave every stream byte as it was
    n = len(doc)
    doc.close()
    return n, limpio, respaldo


def main(argv=None):
    ap = argparse.ArgumentParser(prog="cs-limpio", description=__doc__.split("\n")[0])
    ap.add_argument("pdf", type=Path)
    ap.add_argument("--salida", type=Path, help="output path (default: <name>-limpio.pdf)")
    ap.add_argument("--zona", default=",".join(map(str, ZONA_DEFECTO)),
                    help="badge zone as page fractions x0,y0,x1,y1 (default %(default)s)")
    a = ap.parse_args(argv)

    salida = a.salida or a.pdf.with_name(a.pdf.stem + "-limpio.pdf")
    if salida.exists():
        sys.exit(f"{salida} already exists; not overwriting.")
    zona = tuple(float(v) for v in a.zona.split(","))
    if len(zona) != 4:
        sys.exit("--zona needs four numbers: x0,y0,x1,y1")

    n, limpio, respaldo = limpiar(a.pdf, salida, zona)
    print(f"{salida}: {n} pages, {limpio} badge objects removed, {respaldo} corners whitened")
    if respaldo:
        print("note: pages without a badge object got a white corner instead (check them).")


if __name__ == "__main__":
    main()
