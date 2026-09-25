# Compuertas Lógicas y Chips Serie 74XX — Versión Mejorada

Presentación de **Electrónica Digital** ampliada de 13 a **100 diapositivas**, con diseño 16:9,
imágenes y diagramas técnicos nuevos, y **transiciones + animaciones de entrada nativas de
PowerPoint** en las 100 láminas.

## Archivos entregables

| Archivo | Contenido |
|---|---|
| `Compuertas Lógicas y Chips Serie 74XX - Versión Mejorada.pptx` | **Versión 1 (tema oscuro)**: 100 diapositivas, 16:9, transiciones y animaciones, notas del expositor |
| `Compuertas Lógicas y Chips Serie 74XX - Versión Mejorada (Fondo Claro).pptx` | **Versión 2 (tema claro)**: mismo contenido y mismas animaciones, pensada para proyector con mucha luz o para imprimir |
| `_preview/animacion_diapositiva_013.gif` y `..._084.gif` | **GIF animados** que muestran las entradas por clic de una diapositiva (para revisar la animación sin abrir PowerPoint) |
| `Compuertas Lógicas y Chips Serie 74XX - Vista Previa (100 diapositivas).pdf` | Vista previa imprimible del deck completo (render de alta fidelidad) |
| `_preview/slide_001.jpg … slide_100.jpg` | Vista previa de la versión oscura (una imagen por diapositiva) |
| `_preview_claro/slide_001.jpg … slide_100.jpg` | Vista previa de la versión clara |
| `_preview/indice_general.jpg` y `_preview_claro/indice_general.jpg` | Hojas de contactos con las 100 láminas de cada versión |
| `Compuertas Lógicas y Chips Serie 74XX (1).pptx` | Archivo original del usuario (13 diapositivas), conservado sin cambios |

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
  verdad, **pinouts DIP-14** (7400, 7402, 7404, 7408, 7432, 7486, 74266), diagramas de tiempos,
  márgenes de ruido, fan-out, medio/full adder, sumador de 4 bits, MUX, decodificador,
  codificador, display de 7 segmentos, latch SR, flip-flop D, contadores, registro de
  desplazamiento, familias lógicas, montaje en protoboard, ESD y más.
* Fotografías del archivo original del usuario (chips DIP, panel didáctico, oblea de silicio,
  placa con integrados), con su crédito correspondiente.

## Cómo regenerar la presentación

```bash
cd build
python3 gfx.py                   # regenera los 57 diagramas del tema oscuro (_assets/gen)
python3 build_all.py             # versión 1 (oscura): PPTX + vista previa en _preview/
python3 build_all.py --light     # versión 2 (clara): PPTX + vista previa en _preview_claro/
python3 build_all.py --gif       # añade los GIF que muestran las animaciones
python3 build_all.py --pptx      # solo el PPTX
python3 build_all.py --preview   # solo las imágenes de vista previa
```

Los diagramas del tema claro se regeneran automáticamente al construir con `--light`
(se guardan en `_assets/gen_light` con la paleta clara).

Requiere `python-pptx` y `Pillow`. La capa de diseño (`layouts.py`, `deck.py`) es común a los dos
"backends" (`canvas.py`): el mismo código produce el PPTX animado y la imagen de vista previa,
por lo que la vista previa reproduce fielmente el resultado final.

| Módulo | Responsabilidad |
|---|---|
| `theme.py` | Paleta, tipografías, geometría y acentos por sección |
| `canvas.py` | Primitivas de dibujo con doble backend (PPTX / PIL) |
| `layouts.py` | Arquetipos visuales (tarjetas, tablas, rejillas, líneas de tiempo…) |
| `deck.py` | Composición de cada tipo de diapositiva y grupos de animación |
| `gfx.py` | Generación de los diagramas técnicos en PNG |
| `content1…content7.py` | Texto y datos de las 100 diapositivas |
| `anim.py` | Transiciones y animaciones OOXML (timing nativo de PowerPoint) |
| `build_all.py` | Ensamblado final del PPTX y de la vista previa |

## Nota sobre los datos técnicos

Los parámetros eléctricos provienen de hojas de datos de la subfamilia **74LS** (VCC = 5 V,
VIH ≥ 2.0 V, VIL ≤ 0.8 V, VOL ≤ 0.4 V, VOH ≥ 2.4 V, tPD ≈ 8–15 ns, fan-out 10). Para uso
industrial se recomienda verificarlos contra la hoja de datos del fabricante específico antes de
publicarlos en un reporte técnico.
