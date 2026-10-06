# CS-Limpio

[Versión en español](README.es.md)

Removes the "Scanned with CamScanner" badge from scanned PDFs. Runs on your machine, no account, no upload, no AI.

## How it works

CamScanner adds the badge as a **separate small image object** in the bottom-right corner of every page. CS-Limpio deletes that object, so your scan is left byte-for-byte untouched: no re-encoding, no white patch, same page size.

If a page has no such object (older files where the badge is baked into the scan), the corner zone is whitened with a true redaction (pixels removed, not covered).

## Install

```bash
pip install git+https://github.com/RuntotheSun4/CS-Limpio
```

Or just download `cs_limpio.py` and run it with Python 3.9+ and `pip install pymupdf`.

## Use

```bash
cs-limpio scan.pdf
```

Writes `scan-limpio.pdf` next to the original. The original is never modified, and an existing output is never overwritten.

```
scan-limpio.pdf: 63 pages, 63 badge objects removed, 0 corners whitened
```

Options:

| Option | What it does |
|---|---|
| `--salida out.pdf` | Output path |
| `--zona x0,y0,x1,y1` | Badge zone as page fractions. Default `0.80,0.93,1,1` (bottom-right corner) |

## Scope

PDF only. One badge, fixed corner. No GUI (yet). Feature requests welcome as issues.

## License

MIT.
