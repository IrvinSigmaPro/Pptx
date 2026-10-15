# -*- coding: utf-8 -*-
"""Puertos de Comunicación de PC — Bloque 2: periféricos de entrada · Bloque 3: video."""
import os
import theme
from ports_content1 import P, F, ficha

SLIDES = [
    # ================================================================== 15
    dict(kind="section", section=2, transition="zoom",
         img=F("sec_entrada.jpg"),
         topics=[
             "Puerto PS/2: mini-DIN con código de colores estricto (verde y morado)",
             "Conector DIN de 5 pines de los teclados de la era IBM AT",
             "Game Port (DA-15): joysticks analógicos y teclados MIDI"],
         notes="Bloque breve: los tres puertos de entrada que se usaron antes de la revolución USB."),

    # ================================================================== 16
    ficha(2, "Puerto PS/2",
          "Conector circular mini-DIN para periféricos de control, con identificación de color "
          "obligatoria.",
          "ps2",
          ident="Puerto redondo pequeño de **6 agujeros internos** con guía. Código de colores "
                "universal estricto: **VERDE = ratón** y **MORADO / VIOLETA = teclado** (norma "
                "PC99). En portátiles existe el puerto **combo** azul para ambos.",
          vel="Comunicación directa de **baja latencia** basada en interrupciones de hardware "
              "(IRQ 1 teclado, IRQ 12 ratón), a 10-16.7 kHz. **+5 V** · ~100 mA por puerto.",
          uso="Teclados y ratones de conexión directa. Muy apreciado en teclados mecánicos por "
              "su NKRO nativo y ausencia de latencia añadida por USB.",
          note="Datos que faltan: de los 6 pines solo 4 son activos (DATA, CLK, +5 V, GND). No es "
               "hot-plug en BIOS antiguos (se reconoce al arranque). Los adaptadores USB pasivos "
               "solo funcionan en puertos combo.",
          notes="Preguntar por qué algunos gamers siguen prefiriendo PS/2: sin polling, "
                "interrupción directa y sin límite de teclas simultáneas."),

    # ================================================================== 17
    ficha(2, "Conector DIN de 5 pines (teclado AT)",
          "El conector circular grande de los teclados de las PCs de la era IBM AT.",
          "din5",
          ident="Conector circular **grande de color plateado metálico** (270°, 5 pines) con un "
                "**anillo guía** y los pines dispuestos en forma de media luna. No confundir con "
                "el mini-DIN de PS/2, mucho más pequeño.",
          vel="Baja velocidad **síncrona** para pulsaciones de teclas: reloj de 10-16.7 kHz con "
              "línea de datos serie. Alimentación +5 V y señal TTL.",
          uso="Teclados de computadoras antiguas (décadas de 1980-1990): IBM PC/XT y AT, clones "
              "286/386 y teclados industriales con adaptador DIN→PS/2.",
          note="Pinout AT: 1 CLK · 2 DATA · 3 RESET · 4 GND · 5 +5 V (el IBM XT usaba otro "
               "orden). Muchos teclados DIN incluían un adaptador pasivo a PS/2.",
          notes="El conector DIN de 5 pines también se usó para MIDI en instrumentos musicales: "
                "mismo conector, protocolo distinto (31.25 kbaud).",
          transition="fade"),

    # ================================================================== 18
    ficha(2, "Puerto de Juegos (Game Port / DA-15)",
          "Puerto analógico para mandos de juego y dispositivos musicales MIDI.",
          "gameport",
          ident="Conector **hembra en forma de «D» de 15 pines** (DA-15, dos filas de 8+7). "
                "Típicamente pintado de **amarillo dorado** o integrado en las tarjetas de sonido "
                "clásicas (Creative Sound Blaster).",
          vel="Baja velocidad de **muestreo analógico** (ejes leídos por resistencias de 100 kΩ, "
              "sin digitalización interna). El adaptador MIDI trabaja a 31.25 kbaud.",
          uso="Joysticks analógicos, volantes, gamepads de la era DOS y teclados sintetizadores "
              "MIDI mediante adaptador de 15 pines a dos conectores DIN-5.",
          note="Datos que faltan: soporta 4 ejes (X, Y, rudder, throttle) y 4 botones; sin "
               "detección automática ni alimentación para periféricos complejos. Reemplazado por "
               "USB HID alrededor del año 2000.",
          notes="El gameport compartía IRQ con la tarjeta de sonido; los conflictos de recursos "
                "eran la pesadilla clásica de la era Windows 95.",
          transition="fade"),

    # ================================================================== 19
    dict(kind="section", section=3, transition="zoom",
         img=F("sec_video.jpg"),
         topics=[
             "VGA: la interfaz analógica azul de los monitores CRT",
             "DVI: el paso al video digital (DVI-D, DVI-A, DVI-I)",
             "HDMI: audio y video de alta definición para TV y cine en casa",
             "DisplayPort: el estándar de gaming y estaciones gráficas",
             "S-Video y video compuesto: las últimas señales analógicas"],
         notes="El bloque más extenso: seis puertos de video y una tabla comparativa final."),

    # ================================================================== 20
    ficha(3, "VGA (Video Graphics Array)",
          "Interfaz gráfica analógica tradicional, presente en monitores CRT y proyectores.",
          "vga",
          ident="Conector **trapezoidal de 15 pines en tres filas** (HD15/DE-15) con tornillos de "
                "sujeción manual a los lados. Su elemento identificador universal es el **color "
                "azul** del interior de plástico (código PC99).",
          vel="Señal **analógica RGBHV** (0.7 Vp-p, 75 Ω) sin compresión. Optimizado para "
              "640×480 o 1024×768; con buen cable soporta hasta **1920×1200 @ 60 Hz**.",
          uso="Monitores CRT, proyectores analógicos, pantallas de equipos industriales y "
              "KVM antiguos. Comunicación DDC/EDID para plug & play del monitor.",
          note="Datos que faltan: convierte a analógico cada señal (DAC en la GPU), por lo que "
               "aparece ghosting y reflejos en cables largos. Longitud práctica: 3-15 m.",
          notes="VGA sigue en muchos proyectores de aula; el adaptador HDMI→VGA activo necesita "
                "convertidor digital-a-analógico, no basta un cable pasivo.",
          transition="fade"),

    # ================================================================== 21
    ficha(3, "DVI (Digital Visual Interface)",
          "Interfaz para transmisión de video digital o híbrido (análogo-digital).",
          "dvi",
          ident="Conector **rectangular largo** con una **barra horizontal (blade)** a un costado "
                "y tornillos de sujeción. Interior de plástico **blanco o gris claro** (PC99). "
                "Pinout DVI-I añade 4 pines analógicos alrededor de la blade.",
          vel="Hasta **4.95 Gbps** (Single Link: 1920×1200 @ 60 Hz) o **9.9 Gbps** (Dual Link: "
              "2560×1600 @ 60 Hz) mediante enlaces TMDS de 1.65 Gbps por canal.",
          uso="Monitores planos LCD de primera generación. DVI-D solo digital; DVI-A solo "
              "analógico; DVI-I integrado, adaptable a VGA con cable pasivo. HDCP opcional.",
          note="Datos que faltan: Longitud práctica de cable 5-10 m. Un adaptador DVI→HDMI es "
               "pasivo (solo video; el audio requiere HDMI nativo). Fue el puente entre el "
               "analógico y el HDMI/DisplayPort modernos.",
          notes="Mostrar la diferencia física de pines entre DVI-I y DVI-D: los cuatro pines "
                "analógicos alrededor de la blade son la clave visual.",
          transition="fade"),

    # ================================================================== 22
    ficha(3, "HDMI (High-Definition Multimedia Interface)",
          "Estándar de audio y video digital de alta definición, el rey del salón.",
          "hdmi",
          ident="Conector **delgado con esquinas biseladas inferiores** (trapecio aplanado), "
                "enmarcado en **metal cromado**. Interior generalmente **negro**, sin código de "
                "color; se identifica por el **logotipo HDMI grabado**. Tipos: A (estándar), "
                "C (mini) y D (micro).",
          vel="**HDMI 1.4: 10.2 Gbps** (4K @ 30 Hz) · **HDMI 2.0: 18 Gbps** (4K @ 60 Hz) · "
              "**HDMI 2.1: 48 Gbps** (8K @ 60 Hz / 4K @ 120 Hz).",
          uso="Televisores, monitores, proyectores y sistemas de cine en casa. Transporta audio "
              "multicanal sin comprimir (hasta 32 canales) y video con HDR.",
          note="Datos que faltan: ARC/eARC devuelve audio del TV al receptor (eARC: 37 Mbps, "
               "Dolby TrueHD/Atmos); CEC permite controlar todo con un solo mando; HDCP 2.3 "
               "protege el contenido. Cable estándar 5 m (certificado 15 m).",
          notes="HDMI 2.1 añade VRR y ALLM (modo automático de baja latencia) — clave para "
                "consolas de nueva generación.",
          transition="fade"),

    # ================================================================== 23
    dict(kind="table", section=3, transition="wipe",
         title="HDMI · Versiones y capacidades",
         lead="Cada versión multiplica el ancho de banda y añade funciones para juegos y HDR.",
         header=["Versión", "Año", "Ancho de banda", "Máximo de video", "Funciones clave"],
         widths=[1.55, 0.85, 1.95, 3.35, 4.59],
         row_h=0.44, size=10.5,
         rows=[
             ["HDMI 1.0-1.2", "2002", "4.95 Gbps", "1080p @ 60 Hz", "audio DVD/HDPCM · HDCP 1.0"],
             ["HDMI 1.3-1.4", "2006", "10.2 Gbps", "4K @ 30 Hz", "ARC · Deep Color · 3D"],
             ["HDMI 2.0", "2013", "18 Gbps", "4K @ 60 Hz", "4:2:0 · audio 32 canales · CEC"],
             ["HDMI 2.0b", "2016", "18 Gbps", "4K @ 60 Hz", "HDR10 estático"],
             ["HDMI 2.1", "2017", "48 Gbps", "8K @ 60 / 4K @ 120 Hz", "eARC · VRR · ALLM · HDR dinámico"]],
         note="El cable es siempre el mismo conector; para 4K120/8K hace falta cable «Ultra High "
              "Speed» certificado (48 Gbps). Los cables largos de mala calidad causan destellos "
              "negros por errores de bit.",
         notes="El salto de 2.0 a 2.1 es el más grande: pasa de 18 a 48 Gbps con codificación FRL."),

    # ================================================================== 24
    dict(kind="cards", section=3, transition="wipe",
         title="HDMI · Tipos de conector y funciones avanzadas",
         lead="Lo que no dice la etiqueta del cable: formatos físicos y protocolos incluidos.",
         cols=3,
         cards=[
             dict(title="Type A (estándar)", accent="orange",
                  body="19 pines, el de televisores, monitores y consolas. Es el conector "
                       "«HDMI» sin más calificativos."),
             dict(title="Type C (Mini) y Type D (Micro)", accent="orange",
                  body="Mini HDMI: cámaras y tablets. Micro HDMI: portátiles ultradelgados y "
                       "teléfonos. Mismas señales, conector reducido."),
             dict(title="Type E (automoción)", accent="orange",
                  body="Con bloqueo anti-vibración para coches; raro en informática doméstica "
                       "pero oficial desde HDMI 1.4."),
             dict(title="ARC / eARC", accent="green",
                  body="Canal de retorno de audio: el TV envía sonido al receptor/soundbar por "
                       "el mismo cable. eARC (2.1) añade audio sin pérdida y Dolby Atmos."),
             dict(title="CEC (Consumer Electronics Control)", accent="purple",
                  body="Un solo mando gobierna TV, receptor y reproductor conectados. Cada "
                       "fabricante lo llama distinto (Anynet+, BRAVIA Sync, Simplink)."),
             dict(title="HDCP y HDR", accent="blue",
                  body="HDCP 1.4/2.2/2.3 cifra el contenido (4K exige 2.2+). HDR10, HDR10+ y "
                       "Dolby Vision amplían el rango dinámico con metadatos.")],
         note="Regla práctica: comprar cables «Ultra High Speed» certificados para 4K120; los "
              "cables de 10 m sin certificación fallan antes que los ópticos activos.",
         notes="Relacionar eARC con los soundbars modernos; sin eARC el audio HD se pierde."),

    # ================================================================== 25
    ficha(3, "DisplayPort",
          "Interfaz de video y audio digital de alto rendimiento para informática profesional y "
          "gaming.",
          "dp",
          ident="Rectangular con **solo una esquina biselada** y un **botón o pestillo de "
                "seguridad** superior para liberar el cable. Interior generalmente **negro**. "
                "Existe variante **Mini DisplayPort** (portátiles, sin pestillo).",
          vel="**DP 1.2: 21.6 Gbps** · **DP 1.4: 32.4 Gbps** · **DP 2.0/2.1: hasta 80 Gbps** "
              "(UHBR20). 20 pines · audio 8 canales a 192 kHz.",
          uso="Monitores gaming de alta tasa de refresco (144-540 Hz), estaciones gráficas "
              "avanzadas y cadenas de monitores (MST). Base del conector VESA desde 2006.",
          note="Datos que faltan: Multi-Stream (MST) encadena varios monitores por un solo "
               "puerto; Adaptive-Sync (FreeSync/G-Sync Compatible) sincroniza refresco; "
               "USB-C Alt Mode lo transporta por USB-C. Cable pasivo 2-3 m (activo/óptico 15+ m).",
          notes="DisplayPort es el preferido en PC: más ancho de banda que HDMI 2.0 y sin "
                "cuotas de licencia; HDMI domina en TV y consolas.",
          transition="fade"),

    # ================================================================== 26
    dict(kind="table", section=3, transition="wipe",
         title="DisplayPort · Versiones y modos de señal",
         lead="Nombres de modo (HBR, UHBR) que definen la velocidad real por carril.",
         header=["Versión", "Año", "Modo", "Ancho de banda", "Máximo típico"],
         widths=[1.65, 0.85, 1.75, 2.25, 5.79],
         row_h=0.42, size=10.5,
         rows=[
             ["DP 1.1", "2007", "HBR (RBR/HBR)", "8.6-10.8 Gbps", "2560×1600 @ 60 Hz"],
             ["DP 1.2", "2010", "HBR2", "17.28 / 21.6 Gbps", "4K @ 60 Hz · MST de varios monitores"],
             ["DP 1.3", "2014", "HBR3", "25.92 / 32.4 Gbps", "4K @ 120 Hz · 5K @ 60 Hz"],
             ["DP 1.4", "2016", "HBR3 + DSC", "32.4 Gbps", "8K @ 60 Hz (con compresión DSC)"],
             ["DP 2.0/2.1", "2019-22", "UHBR10/13.5/20", "40 / 54 / 80 Gbps", "8K @ 60 Hz sin comprimir · 4K @ 240 Hz"]],
         note="DSC (Display Stream Compression) comprime visualmente sin pérdida perceptible: "
              "permite 8K incluso sobre HBR3. DP 2.1 usa los mismos modos UHBR con cable "
              "«DP40» o «DP80» certificado.",
         notes="Las cifras exactas por carril: HBR2 = 5.4 Gbps × 4 carriles; UHBR20 = 20 Gbps × 4."),

    # ================================================================== 27
    ficha(3, "S-Video (Super Video)",
          "Puerto de video analógico de calidad intermedia que separa luminancia y crominancia.",
          "svideo",
          ident="Puerto **redondo pequeño de 4 o 7 pines** (mini-DIN), normalmente de color "
                "**negro** con un pequeño **pivote guía** superior. Los 7 pines permiten "
                "adaptadores a componentes YPbPr.",
          vel="Ancho de banda analógico limitado a **definición estándar (SD)**: 480i/576i "
              "(NTSC/PAL), hasta 480p en implementaciones mejoradas. ~5-7 MHz.",
          uso="Conexión de PC a televisores de tubo (CRT) y videocámaras; capturadoras de vídeo "
              "analógicas. Mejora visible sobre el compuesto.",
          note="Datos que faltan: transporta **Y (luminancia) + C (crominancia)** por separado, "
               "eliminando el «dot crawl» del compuesto. Sin audio: necesita cable aparte. "
               "Longitud práctica 5-10 m.",
          notes="Ejercicio visual: la mejora S-Video vs compuesto se nota en los bordes de "
                "texto blanco sobre fondo de color.",
          transition="fade"),

    # ================================================================== 28
    ficha(3, "Video Compuesto (RCA)",
          "Puerto analógico básico de video, el más simple y universal de la era SD.",
          "composite",
          ident="Conector circular hembra tipo jack **RCA identificado inequívocamente por el "
                "color amarillo** (código de color PC99/CEA). Suele ir acompañado de los RCA "
                "**rojo y blanco** del audio estéreo.",
          vel="Ancho de banda analógico básico: señal entrelazada **SD** (NTSC 480i / PAL 576i). "
              "1 Vp-p con impedancia de 75 Ω.",
          uso="Capturadoras de vídeo antiguas, televisores analógicas, consolas retro, CCTV y "
              "sistemas de domótica básica.",
          note="Datos que faltan: multiplexa luma y croma en una sola señal (interferencia de "
               "color y «dot crawl»). Es la peor calidad de video de esta guía. Cable 5-10 m.",
          notes="Orden histórico de calidad: compuesto < S-Video < VGA/componente < digital.",
          transition="fade"),

    # ================================================================== 29
    dict(kind="table", section=3, transition="wipe",
         title="Comparativa de puertos de video",
         lead="De la señal analógica del CRT al 8K digital: qué usar en cada caso.",
         header=["Puerto", "Tipo", "Identificación rápida", "Máximo práctico", "Estado"],
         widths=[1.95, 1.35, 3.55, 3.05, 2.39],
         row_h=0.395, size=10.5,
         rows=[
             ["VGA", "analógico", "trapezoidal azul · 15 pines", "1920×1200 @ 60 Hz", "legado (proyectores)"],
             ["DVI", "digital/híbrido", "blanco · barra lateral", "2560×1600 (Dual Link)", "en desuso"],
             ["HDMI", "digital A/V", "bisel inferior · cromado", "8K @ 60 / 4K @ 120 Hz", "estándar TV/consolas"],
             ["DisplayPort", "digital A/V", "1 esquina + pestillo", "8K @ 60 · 4K @ 240 Hz", "estándar PC"],
             ["S-Video", "analógico", "mini-DIN negro 4/7 pines", "480i / 576i (SD)", "obsoleto"],
             ["Compuesto", "analógico", "RCA amarillo", "480i / 576i (SD)", "obsoleto"]],
         note="Conversores: HDMI→DisplayPort y DP→HDMI son baratos y pasivos en un sentido; "
              "cualquier conversión a VGA requiere convertidor activo (DAC integrado).",
         notes="Tabla de cierre del bloque 3; útil para elegir el cable correcto en un "
               "mantenimiento real."),
]
