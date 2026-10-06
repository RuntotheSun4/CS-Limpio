# CLAUDE.md — CS-Limpio (quita el letrero de CamScanner de un PDF)

> **Gobierno maestro:** antes de trabajar lee `..\..\_Sistema\` (constitución, modelos, MAPA), el **Gobierno LaRa**. Aquí solo lo propio del proyecto.

**Aquí NO eres Justo.** Es una herramienta de Héctor que lleva Claude a secas; no se ofrece trabajo jurídico ni se toca su tablero.

**Qué es:** **fábrica** (R10). Un script de Python (`cs_limpio.py`, PyMuPDF) que borra el objeto de imagen "Scanned with CamScanner" de cada página de un PDF y, si no lo encuentra, blanquea la esquina con una redacción. Diseño en `PLAN-2026-10-06.md`.

**Estado:** activo. Primera versión 2026-10-06.

**Confidencialidad (R5):** ⚠️ el repo es **PÚBLICO**. Ningún PDF de cliente entra: `.gitignore` bloquea `*.pdf`, las pruebas generan sus propios archivos sintéticos y las capturas del README también. `git status` antes de cada push. Las corridas sobre expedientes reales se hacen con `--salida` fuera de esta carpeta.

**git:** `RuntotheSun4/CS-Limpio` (público, MIT).

**Cómo se corre:** `py -3.12 cs_limpio.py archivo.pdf [--salida ruta] [--zona x0,y0,x1,y1]`. Prueba: `py -3.12 test_cs_limpio.py` (imprime `ok`).

**Reglas duras aplicables:** R5 confidencialidad · R7 nunca sobreescribir el original · R10 fábrica.
