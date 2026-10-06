# CS-Limpio

[English version](README.md)

Quita el letrero "Scanned with CamScanner" de los PDF escaneados. Corre en tu computadora, sin cuenta, sin subir nada y sin inteligencia artificial.

## Cómo funciona

CamScanner agrega el letrero como una **imagen chica aparte** en la esquina inferior derecha de cada página. CS-Limpio borra ese objeto, así que el escaneo queda intacto: sin recomprimir, sin parche blanco y con el mismo tamaño de hoja.

Si una página no trae ese objeto (archivos viejos donde el letrero viene fundido en la imagen), se blanquea la esquina con una redacción de verdad (se eliminan los pixeles, no se tapan).

## Instalar

```bash
pip install git+https://github.com/RuntotheSun4/CS-Limpio
```

O descarga `cs_limpio.py` y córrelo con Python 3.9 o más nuevo y `pip install pymupdf`.

## Usar

```bash
cs-limpio escaneo.pdf
```

Escribe `escaneo-limpio.pdf` junto al original. El original nunca se modifica y una salida que ya existe nunca se encima.

```
escaneo-limpio.pdf: 63 pages, 63 badge objects removed, 0 corners whitened
```

Opciones:

| Opción | Qué hace |
|---|---|
| `--salida ruta.pdf` | Dónde guardar el resultado |
| `--zona x0,y0,x1,y1` | Zona del letrero como fracciones de la página. Por defecto `0.80,0.93,1,1` (esquina inferior derecha) |

## Alcance

Solo PDF. Un letrero, en una esquina fija. Sin ventana gráfica (por ahora). Las sugerencias van como issues.

## Licencia

MIT.
