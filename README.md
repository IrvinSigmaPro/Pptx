# Presentaciones generadas — Pptx

Repositorio de presentaciones técnicas con **transiciones, animaciones de entrada y notas del
expositor** generadas de forma programática (python-pptx + PIL para vista previa).

---

# 1 · Puertos de Comunicación de PC — Guía Completa y Detallada

Guía completa de los **23 puertos de comunicación** de una computadora, con **imágenes y
diagramas de identificación de cada puerto**, su **código de colores** y los datos técnicos que
suelen faltar: potencia, longitudes máximas de cable, pinout, versiones y estándares.

## Archivos entregables

| Archivo | Contenido |
|---|---|
| `Puertos de Comunicación de PC - Guía Completa.pptx` | **Presentación final (tema oscuro)**: 56 diapositivas, 16:9, transiciones y animaciones, notas del expositor |
| `Puertos de Comunicación de PC - Guía Completa (Fondo Claro).pptx` | Versión con **tema claro** para proyector e impresión |
| `Puertos de Comunicación de PC - Vista Previa.pdf` | Vista previa imprimible (tema oscuro) |
| `Puertos de Comunicación de PC - Vista Previa (Fondo Claro).pdf` | Vista previa imprimible (tema claro) |
| `_preview_puertos/slide_001.jpg … slide_056.jpg` | Vista previa individual de cada diapositiva |
| `_preview_puertos/indice_general.jpg` | Hoja de contactos con las 56 láminas |

## Estructura del contenido (7 bloques)

| Sección | Diapositivas | Tema |
|---|---|---|
| 01 | 1 – 14 | Uso general y datos: USB (tipos, colores, versiones, potencia), RS-232, LPT, Thunderbolt, FireWire |
| 02 | 15 – 18 | Entrada de periféricos: PS/2 (verde/morado), DIN-5 AT, Game Port DA-15 y MIDI |
| 03 | 19 – 29 | Video: VGA, DVI, HDMI (+versiones y funciones), DisplayPort, S-Video, compuesto y tabla comparativa |
| 04 | 30 – 36 | Red: RJ-45, categorías de cable/PoE, RJ-11, SFP/SFP+ y familia QSFP |
| 05 | 37 – 42 | Audio: jack 3.5 mm (código de colores), TOSLINK y S/PDIF coaxial |
| 06 | 43 – 47 | Almacenamiento: eSATA/eSATAp, lectores SD/microSD, UHS y SD Express |
| 07 | 48 – 56 | IrDA, tabla maestra de velocidades, chuleta de colores, «no confundir», línea de tiempo y glosario |

## Imágenes y diagramas

* **25 diagramas técnicos** dibujados a medida (`build/gfx_ports.py`) con los **colores reales de
  identificación**: lengüetas USB (blanca/negra/azul/roja), PS/2 verde y morado, VGA azul,
  LPT burdeos, RCA amarillo, jacks de audio por color, LEDs de RJ-45, luz roja de TOSLINK/IrDA, etc.
* **Fotografías** de portada, secciones y puertos concretos (`_assets/ports_photos/`).
* Cada puerto tiene su **ficha**: diagrama + identificación visual y color + velocidad y
  estándares + uso y datos adicionales + nota técnica con lo que suelen omitir las guías.

## Reproducir el build

```bash
python3 -m venv .venv && .venv/bin/pip install python-pptx Pillow lxml
cd build
.venv/bin/python gfx_ports.py dark     # diagramas (tema oscuro)
.venv/bin/python gfx_ports.py light    # diagramas (tema claro)
.venv/bin/python build_ports.py        # PPTX + vista previa + PDF (oscuro)
.venv/bin/python build_ports.py --light
```

---

# 2 · Compuertas Lógicas y Chips Serie 74XX — Versión Mejorada

Presentación de **Electrónica Digital** ampliada de 13 a **100 diapositivas**, con diseño 16:9,
imágenes y diagramas técnicos nuevos, y **transiciones + animaciones de entrada nativas de
PowerPoint** en las 100 láminas.

## Archivos entregables

| Archivo | Contenido |
|---|---|
| `Compuertas Lógicas y Chips Serie 74XX - Versión Mejorada.pptx` | **Presentación final**: 100 diapositivas, 16:9, transiciones y animaciones, notas del expositor en cada lámina |
| `Compuertas Lógicas y Chips Serie 74XX - Vista Previa (100 diapositivas).pdf` | Vista previa imprimible del deck completo (render de alta fidelidad) |
| `_preview/slide_001.jpg … slide_100.jpg` | Vista previa individual de cada diapositiva (para revisar sin abrir PowerPoint) |
| `_preview/indice_general.jpg` | Hoja de contactos con las 100 láminas |
| `Compuertas Lógicas y Chips Serie 74XX (1).pptx` | Archivo original del usuario (13 diapositivas), conservado sin cambios |


## Descarga directa (GitHub)

| Versión | Enlace |
|---|---|
| **Tema oscuro (animado)** — `PPT-Compuertas-74XX-100-diapositivas-animado.pptx` | https://github.com/IrvinSigmaPro/Pptx/raw/arena/01a0d8f4-pptx/PPT-Compuertas-74XX-100-diapositivas-animado.pptx |
| **Tema claro para proyector** — `PPT-Compuertas-74XX-100-diapositivas-FONDO-CLARO.pptx` | https://github.com/IrvinSigmaPro/Pptx/raw/arena/01a0d8f4-pptx/PPT-Compuertas-74XX-100-diapositivas-FONDO-CLARO.pptx |
| PDF vista previa (oscuro) | https://github.com/IrvinSigmaPro/Pptx/raw/arena/01a0d8f4-pptx/PDF-Vista-Previa-100-diapositivas.pdf |
| PDF vista previa (claro) | https://github.com/IrvinSigmaPro/Pptx/raw/arena/01a0d8f4-pptx/PDF-Vista-Previa-FONDO-CLARO.pdf |
| GIF de animaciones de ejemplo | https://github.com/IrvinSigmaPro/Pptx/raw/arena/01a0d8f4-pptx/GIF-animacion-ejemplo-1.gif |

## Estructura del contenido (6 bloques)

| Sección | Diapositivas | Tema |
|---|---|---|
| 01 | 1 – 24 | Fundamentos: binario, códigos, niveles lógicos TTL, márgenes de ruido, Boole, De Morgan, Karnaugh, formas canónicas |
| 02 | 25 – 50 | Compuertas y chips: AND 7408, OR 7432, NOT 7404, NAND 7400, NOR 7402, XOR 7486, XNOR 74266 (símbolo, tabla, pinout, tiempos, aplicaciones) |
| 03 | 51 – 65 | Hoja de datos: límites máximos, parámetros DC/AC, tPD, fan-out, familias TTL/CMOS, encapsulados, ESD |
| 04 | 66 – 81 | Aplicaciones: combinacional vs. secuencial, medio sumador, sumador completo y de 4 bits, multiplexores, decodificadores, codificadores, display 7 segmentos, latch SR, flip-flop D, contadores, registros y memorias |
| 05 | 82 – 92 | Laboratorio: materiales, montaje en protoboard, medición, punta lógica, diagnóstico de fallas, retos y buenas prácticas |
| 06 | 93 – 100 | Repaso: resumen de compuertas, tabla maestra, catálogo 74XX, glosario (36 términos), fuentes y cierre |

## Transiciones y animaciones

* **Transición por diapositiva**: `fade`, `wipe`, `push`, `split` y `zoom` (según el tipo de lámina:
  las portadas de sección usan zoom, las tablas usan wipe).
* **Animaciones de entrada**: 524 pasos de exposición en total, máximo 6 clics por diapositiva.
  El encabezado entra automáticamente y el contenido avanza con **clic** (también se puede usar
  la barra espaciadora); efectos aplicados: *fade*, *rise*, *wipe* y *zoom*.
* **Notas del expositor** en las 100 diapositivas.

## Imágenes y diagramas

* 47 diagramas técnicos generados para esta guía: símbolos ANSI de las 7 compuertas, tablas de
  verdad, diagramas de tiempo, pinouts DIP-14 de los chips 74XX, sumadores, multiplexores,
  decodificadores, flip-flops, contadores y memorias.
* Fotografías y renders de laboratorio, protoboard y encapsulados.

## Reproducir el build

```bash
cd build
.venv/bin/python build_all.py            # PPTX + vista previa (tema oscuro)
.venv/bin/python build_all.py --light    # tema claro
```
