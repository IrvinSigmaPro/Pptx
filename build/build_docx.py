# -*- coding: utf-8 -*-
"""Genera la guía en Word (.docx), 20 páginas, con diagramas y fotografías.

Uso:  python3 build_docx.py
"""
import os
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "_assets", "docx_imgs")
PHOTOS = os.path.join(ROOT, "_assets", "ports_photos")
OUT = os.path.join(ROOT, "Puertos de Comunicación de PC - Guía Completa (Word).docx")

NAVY = RGBColor(0x0D, 0x2B, 0x45)
ACC = RGBColor(0x0E, 0x7C, 0x94)      # cian profundo
GRAY = RGBColor(0x55, 0x63, 0x72)
RED = RGBColor(0xC0, 0x39, 0x2B)


def img(name):
    return os.path.join(IMG, name if name.endswith(".jpg") else name + ".jpg")


def photo(name):
    return os.path.join(PHOTOS, name if name.endswith(".jpg") else name + ".jpg")


doc = Document()

# ------------------------------------------------------------------ estilos
st = doc.styles["Normal"]
st.font.name = "Calibri"
st.font.size = Pt(10.5)
st.font.color.rgb = RGBColor(0x22, 0x2B, 0x35)
st.paragraph_format.space_after = Pt(5)
st.paragraph_format.line_spacing = 1.06

for name, size, color in (("Heading 1", 19, NAVY), ("Heading 2", 13.5, ACC),
                          ("Heading 3", 11.5, NAVY)):
    s = doc.styles[name]
    s.font.name = "Calibri"
    s.font.size = Pt(size)
    s.font.color.rgb = color
    s.font.bold = True
    s.paragraph_format.space_before = Pt(6)
    s.paragraph_format.space_after = Pt(4)

for sec in doc.sections:
    sec.top_margin = Inches(0.72)
    sec.bottom_margin = Inches(0.62)
    sec.left_margin = Inches(0.85)
    sec.right_margin = Inches(0.85)


# ------------------------------------------------------------------ helpers
def shade(cell, hexcolor):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hexcolor)
    tcPr.append(shd)


def set_cell_text(cell, text, bold=False, color=None, size=9.5, align=None):
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(1)
    p.paragraph_format.space_before = Pt(1)
    if align:
        p.alignment = align
    run = p.add_run(text)
    run.font.size = Pt(size)
    run.font.bold = bold
    if color:
        run.font.color.rgb = color


def para(text, size=10.5, bold=False, color=None, align=None, space=4, italic=False):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space)
    if align:
        p.alignment = align
    r = p.add_run(text)
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.italic = italic
    if color:
        r.font.color.rgb = color
    return p


def rich(text, size=10.5):
    """Párrafo con **negritas** incrustadas."""
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(4)
    parts = text.split("**")
    for i, part in enumerate(parts):
        if not part:
            continue
        r = p.add_run(part)
        r.font.size = Pt(size)
        r.font.bold = (i % 2 == 1)
    return p


def bullets(items, size=10.2):
    for it in items:
        p = doc.add_paragraph(style="List Bullet")
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.space_before = Pt(0)
        for i, part in enumerate(it.split("**")):
            if not part:
                continue
            r = p.add_run(part)
            r.font.size = Pt(size)
            r.font.bold = (i % 2 == 1)


def table(headers, rows, widths, header_fill="0E7C94", font=9.2):
    t = doc.add_table(rows=1, cols=len(headers))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, w in enumerate(widths):
        for c in t.columns[i].cells:
            c.width = Inches(w)
    for i, htxt in enumerate(headers):
        cell = t.rows[0].cells[i]
        shade(cell, header_fill)
        set_cell_text(cell, htxt, bold=True, color=RGBColor(0xFF, 0xFF, 0xFF), size=font)
    for r in rows:
        cells = t.add_row().cells
        for i, val in enumerate(r):
            set_cell_text(cells[i], str(val), size=font,
                          bold=(i == 0), color=NAVY if i == 0 else None)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    return t


def image(path, width, caption=None, align=WD_ALIGN_PARAGRAPH.CENTER):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_after = Pt(2)
    p.add_run().add_picture(path, width=Inches(width))
    if caption:
        c = doc.add_paragraph()
        c.alignment = WD_ALIGN_PARAGRAPH.CENTER
        c.paragraph_format.space_after = Pt(6)
        r = c.add_run(caption)
        r.font.size = Pt(8.5)
        r.font.italic = True
        r.font.color.rgb = GRAY


def images_side(a, wa, b, wb, cap_a=None, cap_b=None):
    t = doc.add_table(rows=2, cols=2)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, (path, w) in enumerate(((a, wa), (b, wb))):
        cell = t.rows[0].cells[i]
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        cell.paragraphs[0].add_run().add_picture(path, width=Inches(w))
        if (cap_a, cap_b)[i]:
            p = t.rows[1].cells[i].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run((cap_a, cap_b)[i])
            r.font.size = Pt(8)
            r.font.italic = True
            r.font.color.rgb = GRAY
    doc.add_paragraph().paragraph_format.space_after = Pt(2)


def note(text, label="DATO CLAVE"):
    t = doc.add_table(rows=1, cols=1)
    t.style = "Table Grid"
    cell = t.rows[0].cells[0]
    shade(cell, "EAF3F7")
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run(label + ": ")
    r.font.size = Pt(9)
    r.font.bold = True
    r.font.color.rgb = ACC
    r = p.add_run(text)
    r.font.size = Pt(9)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)


def page():
    doc.add_page_break()


def h2(text):
    doc.add_heading(text, level=2)


def h3(text):
    doc.add_heading(text, level=3)


def footer():
    for sec in doc.sections:
        p = sec.footer.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run("Puertos de Comunicación de PC · Guía Completa y Detallada  ·  página ")
        r.font.size = Pt(8)
        r.font.color.rgb = GRAY
        fld = OxmlElement("w:fldSimple")
        fld.set(qn("w:instr"), "PAGE")
        p._p.append(fld)


# ============================================================ P1 · Portada
para("GUÍA COMPLETA Y DETALLADA", size=11, bold=True, color=ACC,
     align=WD_ALIGN_PARAGRAPH.CENTER, space=2)
para("Puertos de Comunicación de PC", size=28, bold=True, color=NAVY,
     align=WD_ALIGN_PARAGRAPH.CENTER, space=2)
para("Identificación visual, códigos de colores, velocidades, versiones y usos",
     size=12.5, color=GRAY, align=WD_ALIGN_PARAGRAPH.CENTER, space=10)
image(photo("hero_ports"), 6.4, "Panel trasero de una placa madre actual: USB-A, USB-C, HDMI, "
                                "DisplayPort, RJ-45 y jacks de audio.")
para("Recorrido por los 23 puertos clásicos y modernos de una computadora —USB, RS-232, LPT, "
     "Thunderbolt, FireWire, PS/2, DIN, Game Port, VGA, DVI, HDMI, DisplayPort, S-Video, video "
     "compuesto, RJ-45, RJ-11, SFP, audio de 3.5 mm, TOSLINK, S/PDIF, eSATA, tarjetas SD e "
     "IrDA— con diagramas de identificación y los datos técnicos que suelen faltar: potencia, "
     "longitudes de cable, pinout y estándares.", size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY)
table(["23 puertos documentados", "7 bloques temáticos", "25+ diagramas", "Datos 2026"],
      [["Cada uno con imagen y ficha técnica", "De datos a infrarrojos",
        "Con colores reales de identificación", "Versiones hasta USB4 v2 / TB5 / DP 2.1"]],
      [1.7, 1.7, 1.7, 1.7], font=9)
page()

# ============================================================ P2 · Índice
doc.add_heading("Índice de contenidos", level=1)
table(["#", "Sección", "Contenido"],
      [["1", "Puertos de uso general y datos",
        "USB · RS-232 · LPT · Thunderbolt · FireWire"],
       ["2", "Entrada de periféricos", "PS/2 · DIN-5 (teclado AT) · Game Port (DA-15)"],
       ["3", "Puertos de video y pantalla",
        "VGA · DVI · HDMI · DisplayPort · S-Video · Video compuesto"],
       ["4", "Red y comunicaciones", "Ethernet RJ-45 · Módem RJ-11 · SFP/SFP+"],
       ["5", "Puertos de audio", "Jack 3.5 mm · S/PDIF óptico (TOSLINK) · S/PDIF coaxial"],
       ["6", "Almacenamiento y expansión", "eSATA/eSATAp · Lectores de tarjetas SD/microSD"],
       ["7", "Infrarrojos y repaso", "IrDA · tablas maestras · chuleta de colores · glosario"]],
      [0.4, 2.2, 4.2])
h2("Cómo usar esta guía")
bullets([
    "Cada puerto se presenta con su **descripción general**, su **aspecto visual y color de "
    "identificación**, su **velocidad** y su **uso**, más los datos técnicos que suelen faltar.",
    "Los **diagramas** muestran la forma real del conector con su color de identificación "
    "(lengüetas USB, azul de VGA, burdeos del LPT, verde/morado del PS/2, amarillo del RCA...).",
    "Las **tablas** recogen versiones y velocidades reales: consúltalas antes de comprar cables "
    "o adaptadores.",
    "La **chuleta de colores** del final resume los códigos de identificación para el taller."])
note("Si el conector no entra con suavidad, no es el correcto: la fuerza nunca forma parte del "
     "estándar.", "REGLA DE ORO")
page()

# ============================================================ P3 · USB identificación
doc.add_heading("1 · Puertos de uso general y datos", level=1)
h2("1.1 USB (Universal Serial Bus)")
rich("**Descripción general:** interfaz estándar universal para la transmisión de datos, "
     "alimentación eléctrica y video. Sustituyó al puerto serie, al paralelo y al PS/2 con un "
     "único estándar hot-plug e interoperable, y hoy carga incluso portátiles con USB Power "
     "Delivery de hasta 240 W.")
image(img("usb_colors"), 5.6, "Identificación de USB por el color de la lengüeta interior y forma "
                              "del conector Type-C.")
h3("Aspecto visual y color de identificación")
bullets([
    "**USB 1.0 / 1.1:** interior de plástico habitualmente **blanco o gris**.",
    "**USB 2.0:** interior de plástico de color **negro** (el más extendido).",
    "**USB 3.0 / 3.1 Gen 1:** interior **azul** o con el logotipo **SS** (SuperSpeed).",
    "**USB 3.1 Gen 2 / 3.2 Gen 2:** interior **rojo o turquesa (teal)**, típico de placas gaming.",
    "**USB Tipo C:** conector **ovalado, simétrico y reversible**, a menudo con icono de **rayo** "
    "(Thunderbolt) o **DP** grabado al lado.",
    "Algunos fabricantes usan colores propios (naranja para carga): el color es convención, "
    "no norma."])
page()

# ============================================================ P4 · USB conectores y velocidades
h2("1.1 USB · Conectores y velocidades")
image(img("usb_types"), 5.3, "Familia de conectores USB: Type-A, Type-B, Mini-B, Micro-B y Type-C.")
table(["Estándar", "Año", "Velocidad", "Nombre comercial", "Color típico"],
      [["USB 1.0 / 1.1", "1996-98", "1.5 - 12 Mbps", "Low / Full Speed", "blanco / gris"],
       ["USB 2.0", "2000", "480 Mbps", "High Speed", "negro"],
       ["USB 3.0 / 3.1 Gen 1", "2008", "5 Gbps", "SuperSpeed (SS)", "azul"],
       ["USB 3.1 Gen 2 / 3.2 Gen 2", "2013", "10 Gbps", "SuperSpeed+ 10 Gbps", "rojo o turquesa"],
       ["USB 3.2 Gen 2x2", "2017", "20 Gbps", "SuperSpeed+ 20 Gbps", "rojo (pocos equipos)"],
       ["USB4", "2019", "40 Gbps", "USB4 Gen 3x2", "interior negro (USB-C)"],
       ["USB4 v2.0", "2022", "80 - 120 Gbps", "asimétrico (120/40)", "USB-C ⚡"]],
      [1.55, 0.7, 1.15, 1.85, 1.55])
rich("**Datos que faltan:** USB 2.0 entrega 5 V/500 mA (2.5 W), USB 3.x 900 mA (4.5 W) y USB-C PD "
     "hasta **240 W**. Longitud de cable: 5 m (USB 2.0), 2-3 m (USB 3.x pasivo), 0.8-2 m "
     "(USB4/Thunderbolt a velocidad máxima). Contactos: 4 (USB 2.0), 9 (USB 3.x Type-A) y 24 "
     "(Type-C reversible). Con UASP los discos externos ganan un 20-30 % de velocidad real.")
note("«USB 3.1 Gen 1» es exactamente lo mismo que USB 3.0 (5 Gbps): solo cambia el nombre "
     "comercial. La velocidad la marca siempre el extremo más lento del enlace.")
page()

# ============================================================ P5 · RS-232 + LPT
h2("1.2 Puerto Serie (RS-232 / DB-9)")
rich("**Descripción general:** puerto de comunicación **asíncrona de transmisión bit a bit** "
     "(estándar RS-232 desde 1969), el preferido de la industria por su robustez eléctrica.")
image(img("dsub9"), 2.9)
bullets([
    "**Aspecto visual:** conector macho en forma de «D» de 9 pines (DE-9, llamado «DB-9»). "
    "Frecuentemente de color **turquesa / azul verdoso o gris metálico** en placas antiguas; "
    "en tarjetas modernas, cabecera interna negra rotulada «COM».",
    "**Velocidad:** típicamente hasta **115.2 kbps** (hasta 921.6 kbps con UART avanzados). "
    "Niveles de señal de **±3 a ±15 V** (típico ±12 V); cable de hasta 15 m.",
    "**Uso:** consolas de red (Cisco), dispositivos médicos, módems antiguos, PLCs e industria.",
    "**Pinout:** 1 DCD · 2 RXD · 3 TXD · 4 DTR · 5 GND · 6 DSR · 7 RTS · 8 CTS · 9 RI "
    "(basta con TXD, RXD y GND)."])
h2("1.3 Puerto Paralelo (LPT / DB-25)")
rich("**Descripción general:** puerto para transmitir datos de forma simultánea (**8 bits a la "
     "vez**, estándar IEEE 1284).")
bullets([
    "**Aspecto visual:** conector hembra grande en «D» de 25 pines, de tono tradicional "
    "**burdeos / rojo oscuro o rosa** en gabinetes AT/ATX (código de color PC99).",
    "**Velocidad:** de 50 KB/s (modo SPP) hasta más de **2 MB/s** con los modos EPP/ECP (con DMA).",
    "**Uso:** impresoras matriciales y de chorro, escáneres antiguos, unidades ZIP, dongles de "
    "licencia y programadores de EPROM. Cable de 10-15 m; puerto base 0x378."])
page()

# ============================================================ P6 · Thunderbolt + FireWire
h2("1.4 Thunderbolt")
rich("**Descripción general:** interfaz de ultra alta velocidad que combina **PCI Express y "
     "DisplayPort** (más alimentación) en un solo cable.")
images_side(img("thunderbolt"), 3.15, img("firewire"), 3.15,
            "Thunderbolt: USB-C o Mini DP con icono de rayo ⚡ obligatorio.",
            "FireWire: conectores con borde en «V» y logo de tres ramas.")
bullets([
    "**Aspecto visual:** en versiones recientes comparte el diseño físico del **USB Tipo C**, "
    "pero se distingue **obligatoriamente** por un pequeño **icono de rayo** grabado junto al "
    "puerto (Thunderbolt 1 y 2 usaban Mini DisplayPort, también con rayo).",
    "**Velocidad:** Thunderbolt 1 = 10 Gbps · 2 = 20 Gbps · 3 y 4 = 40 Gbps · 5 = hasta "
    "**80 Gbps (120 Gbps asimétricos)**. Alimentación hasta 240 W; cadenas de hasta 6 dispositivos.",
    "**Uso:** tarjetas gráficas externas (eGPU), almacenamiento masivo profesional, docks y "
    "monitores 4K/8K. Cable pasivo: 0.8 m a velocidad máxima; activo/óptico hasta 60 m."])
h2("1.5 FireWire (IEEE 1394)")
rich("**Descripción general:** bus serie de alta velocidad desarrollado por **Apple** (1995), con "
     "modo isócrono para vídeo en tiempo real.")
bullets([
    "**Aspecto visual:** conector rectangular con un borde en ángulo o forma de «V»; detalles "
    "en dorado o marcos plateados con el **logo de FireWire** (círculo con tres ramas). "
    "Versiones de 6 pines (con alimentación), 4 pines (i.LINK) y 9 pines (1394b).",
    "**Velocidad:** FireWire 400 (400 Mbps) y FireWire 800 (800 Mbps). Hasta 63 dispositivos "
    "en cadena, hot-swap y cable de 4.5 m (100 m con fibra).",
    "**Uso:** videocámaras DV, discos duros externos de audio/vídeo e interfaces de audio "
    "profesional. Retirado por Apple en 2011; su relevo lo tomaron USB 2.0/3.0, eSATA y "
    "Thunderbolt."])
page()

# ============================================================ P7 · PS/2 + DIN-5
doc.add_heading("2 · Puertos de entrada de periféricos", level=1)
h2("2.1 Puerto PS/2")
rich("**Descripción general:** conector circular **mini-DIN de 6 pines** para periféricos de "
     "control (IBM PS/2, 1987), con identificación por código de colores universal estricto.")
images_side(img("ps2"), 3.3, img("din5"), 2.35,
            "PS/2: morado = teclado, verde = ratón; azul = combo en portátiles.",
            "DIN-5 de teclado AT: conector plateado de 5 pines en media luna.")
bullets([
    "**Aspecto visual:** puerto redondo pequeño con 6 agujeros internos y guía. "
    "**Verde: exclusivo para el ratón. Morado / violeta: exclusivo para el teclado.**",
    "**Velocidad:** comunicación directa de **baja latencia** por interrupciones de hardware "
    "(IRQ 1 teclado, IRQ 12 ratón), a 10-16.7 kHz, con +5 V.",
    "**Uso:** teclados y ratones de conexión directa. Muy apreciado en teclados mecánicos por "
    "su NKRO nativo. De los 6 pines solo 4 son activos (DATA, CLK, +5 V, GND); no es hot-plug "
    "en BIOS antiguos."])
h2("2.2 Conector DIN de 5 pines (teclado AT)")
bullets([
    "**Descripción general:** antiguo puerto para teclados de las PCs de la **era IBM AT** "
    "(mediados de los 80).",
    "**Aspecto visual:** conector circular grande de color **plateado metálico** con un anillo "
    "guía y los pines en forma de media luna (no confundir con el mini-DIN de PS/2).",
    "**Velocidad / uso:** baja velocidad síncrona (reloj de 10-16.7 kHz) para pulsaciones de "
    "teclas. Pinout AT: 1 CLK · 2 DATA · 3 RESET · 4 GND · 5 +5 V."])
page()

# ============================================================ P8 · Game Port + VGA
h2("2.3 Puerto de Juegos (Game Port / DA-15)")
image(img("gameport"), 2.55)
bullets([
    "**Descripción general:** puerto **analógico** para mandos de juego y dispositivos musicales.",
    "**Aspecto visual:** conector hembra en forma de «D» de 15 pines (DA-15, dos filas 8+7), "
    "típicamente pintado de **amarillo dorado** o integrado en las tarjetas de sonido clásicas "
    "(Creative Sound Blaster).",
    "**Velocidad / uso:** muestreo analógico de baja velocidad: 4 ejes (potenciómetros de "
    "100 kΩ) y 4 botones, sin detección automática. Joysticks y teclados sintetizadores **MIDI** "
    "mediante adaptador a dos DIN-5 (31.25 kbaud). Reemplazado por USB HID hacia el año 2000."])
doc.add_heading("3 · Puertos de video y pantalla", level=1)
h2("3.1 VGA (Video Graphics Array)")
rich("**Descripción general:** interfaz gráfica **analógica** tradicional (señal RGBHV de "
     "0.7 Vp-p, 75 Ω), con comunicación DDC/EDID para plug & play del monitor.")
image(img("vga"), 2.95, "VGA: conector trapezoidal azul de 15 pines en tres filas, con tornillos.")
bullets([
    "**Aspecto visual:** conector trapezoidal de **15 pines en tres filas**, con tornillos de "
    "sujeción manual. Su elemento identificador universal es el **color azul** del interior "
    "de plástico (código PC99).",
    "**Velocidad:** limitado por la señal analógica; optimizado para 640×480 o 1024×768 y capaz "
    "de hasta 1920×1200 @ 60 Hz con buen cable (3-15 m).",
    "**Uso:** monitores CRT, proyectores analógicos y pantallas industriales. Convierte cada "
    "señal a analógico (DAC), por lo que aparece ghosting en cables largos."])
page()

# ============================================================ P9 · DVI + HDMI
h2("3.2 DVI (Digital Visual Interface)")
rich("**Descripción general:** interfaz para transmisión de video **digital o híbrido** "
     "(análogo-digital) mediante enlaces TMDS.")
image(img("dvi"), 4.35, "DVI-I: rejilla de pines digitales, barra lateral (blade) y pines "
                       "analógicos C1-C5; interior blanco o gris claro.")
bullets([
    "**Aspecto visual:** conector rectangular largo con una **barra horizontal (blade)** a un "
    "costado; interior **blanco o gris claro**. Variantes: **DVI-D** (solo digital), **DVI-A** "
    "(solo analógico) e **DVI-I** (integrado, con 4 pines analógicos, adaptable a VGA pasivamente).",
    "**Velocidad:** hasta 4.95 Gbps (Single Link) o 9.9 Gbps (Dual Link, 2560×1600 @ 60 Hz); "
    "HDCP opcional y cable de 5-10 m. **Uso:** monitores LCD de primera generación; un "
    "adaptador DVI→HDMI es pasivo y solo transporta video."])
h2("3.3 HDMI (High-Definition Multimedia Interface)")
rich("**Descripción general:** estándar de **audio y video digital de alta definición** (2002).")
image(img("hdmi"), 4.3, "HDMI: Type A estándar, Mini (C) y Micro (D); esquinas biseladas "
                        "inferiores y marco cromado.")
bullets([
    "**Aspecto visual:** conector delgado con **esquinas biseladas inferiores**, enmarcado en "
    "metal cromado; interior generalmente **negro** sin código de color, identificado por el "
    "**logotipo HDMI grabado**.",
    "**Velocidad:** HDMI 1.4 = 10.2 Gbps (4K @ 30 Hz) · 2.0 = 18 Gbps (4K @ 60 Hz) · "
    "2.1 = **48 Gbps** (8K @ 60 Hz / 4K @ 120 Hz).",
    "**Uso:** televisores y cine en casa: ARC/eARC devuelve audio al receptor; CEC gobierna "
    "todo con un mando; HDCP 2.3 cifra el contenido; HDR10/Dolby Vision y VRR/ALLM para "
    "juegos."])
page()

# ============================================================ P10 · DisplayPort + S-Video + compuesto
h2("3.4 DisplayPort")
image(img("dp"), 4.6, "DisplayPort: una sola esquina biselada y pestillo de seguridad; "
                      "Mini DisplayPort sin pestillo.")
bullets([
    "**Aspecto visual:** rectangular con **solo una esquina biselada** y un **botón o pestillo "
    "de seguridad** superior para liberar el cable; interior **negro**. Variante Mini DisplayPort.",
    "**Velocidad:** DP 1.2 = 21.6 Gbps · DP 1.4 = 32.4 Gbps · DP 2.0/2.1 = hasta **80 Gbps** "
    "(UHBR20). 20 pines; audio de 8 canales a 192 kHz.",
    "**Uso:** monitores gaming de alta tasa de refresco (144-540 Hz), estaciones gráficas y "
    "cadenas de monitores (MST). Adaptive-Sync (FreeSync/G-Sync) y DP Alt Mode por USB-C."])
h2("3.5 S-Video y 3.6 Video Compuesto (RCA)")
images_side(img("svideo"), 2.35, img("composite"), 2.15,
            "S-Video: mini-DIN negro de 4 o 7 pines con pivote guía.",
            "Compuesto: RCA amarillo inequívoco (con rojo/blanco de audio).")
bullets([
    "**S-Video:** separa **luminancia (Y)** y **crominancia (C)** para evitar el «dot crawl» "
    "del compuesto. Definición estándar (480i/576i), 5-10 m de cable; sin audio.",
    "**Video compuesto:** señal analógica básica multiplexada (NTSC 480i / PAL 576i, 1 Vp-p, "
    "75 Ω) identificada por el **color amarillo** del RCA. Usado en capturadoras antiguas, "
    "consolas retro y CCTV. Es la peor calidad de video de esta guía."])
table(["Puerto", "Tipo", "Identificación rápida", "Máximo práctico", "Estado"],
      [["VGA", "analógico", "trapezoidal azul · 15 pines", "1920×1200 @ 60 Hz", "legado"],
       ["DVI", "digital/híbrido", "blanco · barra lateral", "2560×1600 (Dual Link)", "en desuso"],
       ["HDMI", "digital A/V", "bisel inferior · cromado", "8K @ 60 / 4K @ 120 Hz", "estándar TV"],
       ["DisplayPort", "digital A/V", "1 esquina + pestillo", "8K @ 60 · 4K @ 240 Hz", "estándar PC"],
       ["S-Video", "analógico", "mini-DIN negro", "480i / 576i", "obsoleto"],
       ["Compuesto", "analógico", "RCA amarillo", "480i / 576i", "obsoleto"]],
      [1.2, 1.15, 1.95, 1.65, 0.85])
page()

# ============================================================ P11 · RJ-45
doc.add_heading("4 · Puertos de red y comunicaciones", level=1)
h2("4.1 Ethernet / RJ-45")
rich("**Descripción general:** puerto de **red alámbrica** para redes locales (LAN) mediante "
     "cable UTP de par trenzado.")
image(img("rj45"), 2.7, "RJ-45 (8P8C) con pestaña de traba y LEDs de enlace y actividad.")
bullets([
    "**Aspecto visual:** conector rectangular ligeramente **más ancho que un puerto telefónico** "
    "(8P8C), con **pestaña de traba** plástica y dos LEDs integrados: **verde** (enlace) y "
    "**naranja/ámbar** (actividad).",
    "**Velocidad:** Fast Ethernet 100 Mbps · Gigabit 1 Gbps (1000 Mbps) · 2.5G / 5G / 10G "
    "Ethernet (de 2.5 a 10 Gbps). 100 m por segmento; cableado T568A/T568B.",
    "**Uso:** conexión a Internet de alta velocidad, switches, routers, NAS y PoE "
    "(802.3af/at/bt) que alimenta cámaras IP y puntos de acceso por el mismo cable."])
table(["Estándar", "Velocidad", "Cable mínimo", "Distancia"],
      [["10BASE-T", "10 Mbps", "Cat 3", "100 m"],
       ["100BASE-TX (Fast)", "100 Mbps", "Cat 5e", "100 m"],
       ["1000BASE-T (Gigabit)", "1 Gbps", "Cat 5e/6", "100 m"],
       ["2.5G / 5GBASE-T", "2.5 / 5 Gbps", "Cat 5e / 6", "100 m"],
       ["10GBASE-T", "10 Gbps", "Cat 6a (6: 55 m)", "100 m"],
       ["PoE 802.3af / at / bt", "15.4 / 30 / 60-100 W", "Cat 5e o superior", "100 m"]],
      [1.9, 1.5, 1.75, 1.65])
page()

# ============================================================ P12 · RJ-11 + SFP
h2("4.2 Módem / RJ-11")
images_side(img("rj11"), 2.25, img("rj_compare"), 3.6,
            "RJ-11: más estrecho; jacks «LINE» y «PHONE».",
            "RJ-45 ≠ RJ-11: mismo lenguaje, tamaño distinto — nunca forzar uno en el otro.")
bullets([
    "**Descripción general:** puerto para la **línea telefónica analógica** clásica (dial-up).",
    "**Aspecto visual:** conector idéntico al RJ-45 pero de **menor tamaño físico** (6P2C/6P4C). "
    "En módems PCI era de color transparente / blanco o estaba rotulado con la palabra **«LINE»**.",
    "**Velocidad:** hasta **56 kbps** (V.90/V.92); fax a 14.4-33.6 kbps; ADSL2+ hasta 24 Mbps "
    "con splitter.",
    "**Uso:** Internet telefónico, envío de fax, alarmas y TPV. Par telefónico de 2 hilos; "
    "tensión de línea -48 V DC con timbre de ~90 V AC."])
h2("4.3 SFP / SFP+")
image(img("sfp"), 4.4, "Bahía (cage) metálica con módulo y palanca; fibra LC duplex "
                       "amarilla (monomodo) o aqua (multimodo).")
bullets([
    "**Aspecto visual:** **ranura metálica rectangular profunda** con una pequeña **palanca o "
    "pestillo** (azul, negro o metálico según la velocidad); los módulos usan conectores LC duplex.",
    "**Velocidad:** SFP (1 Gbps) · SFP+ (10 Gbps) · SFP28 (25 Gbps) · QSFP+ (40 Gbps) · "
    "QSFP28 (100 Gbps) · QSFP-DD (400 Gbps).",
    "**Uso:** servidores y switches empresariales: fibra monomodo (hasta 80-120 km) o multimodo "
    "(300-550 m) y cables DAC de cobre (1-7 m). Hot-swap, estándar MSA y diagnóstico DDM/DOM."])
page()

# ============================================================ P13 · Jack 3.5
doc.add_heading("5 · Puertos de audio", level=1)
h2("5.1 Jack de Audio de 3.5 mm")
rich("**Descripción general:** conector **analógico** estándar para sonido estéreo y micrófonos, "
     "el más usado en sistemas de sonido, diademas y micrófonos.")
image(img("audio_jacks"), 5.9, "Código de colores PC99 de los jacks de 3.5 mm y conector "
                               "TRS (3 polos) / TRRS (4 polos con micrófono).")
table(["Color", "Función", "Señal", "Ejemplo de uso"],
      [["Verde", "salida de línea / altavoces", "salida estéreo", "auriculares, altavoces 2.0"],
       ["Rosado / magenta", "entrada de micrófono", "entrada mono (-10 dBV)", "diademas, micrófonos"],
       ["Azul claro", "entrada de línea (Line-in)", "entrada estéreo", "reproductor, mezcladora"],
       ["Naranja", "altavoz central y subwoofer", "salida 5.1/7.1", "home cinema PC"],
       ["Negro", "altavoces traseros (Surround)", "salida surround", "configuración 5.1"],
       ["Gris", "altavoces laterales", "salida surround", "configuración 7.1"]],
      [1.25, 2.15, 1.7, 1.7])
rich("**Velocidad:** transmisión analógica en **tiempo real**, sin latencia de datos digitales. "
     "Impedancias de 16-600 Ω; nivel de línea ~1 Vrms. Los conectores **TRS** llevan 3 polos "
     "(estéreo) y los **TRRS** 4 polos (con micrófono), con estándares **CTIA y OMTP** "
     "incompatibles entre sí. También existe el formato de 6.35 mm (1/4\") del audio "
     "profesional.")
page()

# ============================================================ P14 · TOSLINK + SPDIF
h2("5.2 S/PDIF Óptico (TOSLINK)")
images_side(img("toslink"), 2.35, img("spdif_coax"), 2.15,
            "TOSLINK: conector cuadrado con tapa; luz roja (~650 nm) al activarse.",
            "S/PDIF coaxial: RCA naranja o negro de 75 Ω.")
bullets([
    "**Descripción general:** puerto de **audio digital mediante pulsos de luz** por fibra óptica.",
    "**Aspecto visual:** conector cuadrado pequeño con **esquinas biseladas** y una **tapa "
    "protectora abatible**; al encender el equipo emite un **brillo de luz roja** en su interior. "
    "Variante mini-óptica de 3.5 mm en equipos compactos.",
    "**Velocidad:** audio multicanal digital sin pérdida por interferencia eléctrica: PCM "
    "estéreo hasta 96 kHz y envolvente comprimido (Dolby Digital / DTS) 5.1-7.1; ADAT de 8 "
    "canales en audio profesional. Fibra de 5-10 m (hasta 30 m de calidad).",
    "**Uso:** barras de sonido y sistemas de cine en casa avanzados; entornos con bucles de "
    "masa o interferencias (inmune a EMI)."])
h2("5.3 S/PDIF Coaxial")
bullets([
    "**Descripción general:** interfaz de **audio digital mediante cable coaxial de 75 ohmios**.",
    "**Aspecto visual:** conector circular tipo **RCA hembra**, identificado por un color "
    "**naranja brillante o negro** distintivo en su borde plástico (BNC en equipos pro).",
    "**Velocidad / uso:** ancho de banda adecuado para audio envolvente comprimido (Dolby "
    "Digital / DTS) y PCM de 24 bit/192 kHz. Señal de 0.5 Vp-p; ~10 m de cable (un cable RCA "
    "de vídeo de 75 Ω vale). Mismo protocolo S/PDIF que el TOSLINK: solo cambia el medio "
    "(eléctrico frente a óptico)."])
note("Coaxial: menos jitter, más simple. Óptico: inmune a ruido eléctrico y bucles de tierra. "
     "Para audio sin pérdida multicanal moderno (TrueHD/Atmos), HDMI es la vía recomendada.")
page()

# ============================================================ P15 · eSATA + SD
doc.add_heading("6 · Puertos de almacenamiento y expansión", level=1)
h2("6.1 eSATA / eSATAp")
rich("**Descripción general:** conexión externa para discos duros basada en el **protocolo SATA "
     "interno**, sin la sobrecarga del protocolo USB.")
image(img("esata"), 2.95, "eSATA: conector plano y alargado con guías metálicas robustas; "
                         "serigrafía «eSATA».")
bullets([
    "**Aspecto visual:** conector **plano y alargado** similar al SATA interno pero con guías "
    "de plástico más robustas y metálicas; color **negro oscuro** con la serigrafía «eSATA». "
    "La variante **eSATAp** añade hilos de alimentación (5-12 V).",
    "**Velocidad:** eSATA 1.5 / 3 / 6 Gbps (SATA I/II/III), a velocidad nativa del bus interno. "
    "Cable máximo de 2 m; hot-swap con controlador en modo AHCI.",
    "**Uso:** conexión de discos externos con rendimiento idéntico al interno. El eSATA puro "
    "**no aporta alimentación** (requiere fuente externa); desplazado por USB 3.0 desde 2010."])
h2("6.2 Lectores de Tarjetas (SD / microSD)")
image(img("sdcard"), 3.85, "Tarjeta SD con pestaña LOCK, microSD y ranura del lector.")
bullets([
    "**Aspecto visual:** **ranuras finas rectangulares** en el panel frontal o lateral del "
    "chasis, con iconos impresos de tarjetas. La SD lleva **pestaña de bloqueo (LOCK)**; "
    "la microSD no.",
    "**Velocidad:** UHS-I 104 MB/s · UHS-II 312 MB/s · UHS-III 624 MB/s · SD Express 985 MB/s+. "
    "Familias: SD (≤2 GB), SDHC (≤32 GB), SDXC (≤2 TB) y SDUC (≤128 TB); clases V10-V90 (vídeo) "
    "y A1/A2 (apps).",
    "**Uso:** transferencia rápida de fotos y archivos desde cámaras, drones, teléfonos y "
    "consolas; los lectores internos se conectan por USB 2.0/3.0."])
page()

# ============================================================ P16 · IrDA + tabla maestra
doc.add_heading("7 · Infrarrojos y repaso", level=1)
h2("7.1 IrDA (Infrared Data Association)")
image(img("irda"), 2.7, "IrDA: ventana de plástico translúcido rojo oscuro/morado con cono "
                        "de luz direccional.")
bullets([
    "**Descripción general:** puerto **inalámbrico direccional por luz infrarroja**, el "
    "«Bluetooth» de los años 90 para agendas electrónicas (PDA) y equipos de la época.",
    "**Aspecto visual:** pequeña **ventana rectangular u ovalada de plástico translúcido** de "
    "color **rojo oscuro, morado o ahumado oscuro** en el panel frontal de la PC o laptop. "
    "Sin pines: es un transceptor óptico.",
    "**Velocidad:** desde 115.2 kbps (SIR) hasta 4 Mbps (FIR) y 16 Mbps (VFIR); negociación "
    "inicial a 9600 bps. Cono de ~30° y alcance de **0-1 m con línea de visión directa** "
    "(850-900 nm). Desplazado por Bluetooth y Wi-Fi desde 2005."])
h3("Modos de operación IrDA")
table(["Modo", "Velocidad", "Año", "Notas"],
      [["SIR", "9.6 kbps - 115.2 kbps", "1993", "compatible con UART clásico"],
       ["MIR", "1.152 Mbps", "1996", "intermedio, poco usado"],
       ["FIR", "4 Mbps", "1998", "el modo más habitual en PCs"],
       ["VFIR", "16 Mbps", "2001", "muy raro en equipos domésticos"],
       ["GigaIR", "hasta 1 Gbps", "2007+", "experimental, no desplegado"]],
      [1.0, 1.75, 0.75, 3.3])
page()

# ============================================================ P17 · Tabla maestra
h2("Tabla maestra · Velocidades de todos los puertos")
para("Una sola vista de las interfaces de esta guía, de menor a mayor velocidad.",
     size=9.5, color=GRAY, italic=True)
table(["Puerto", "Velocidad típica / máx.", "Tipo", "Aparición", "Estado hoy"],
      [["Módem RJ-11", "56 kbps", "serie", "1990s", "legado / ADSL"],
       ["IrDA", "115.2 kbps - 4 Mbps", "inalámbrico IR", "1993", "obsoleto"],
       ["RS-232", "115.2 kbps (921.6 kbps)", "serie", "1969", "industria"],
       ["LPT", "50 KB/s - 2+ MB/s", "paralelo 8 bits", "1970s", "obsoleto"],
       ["Game Port", "muestreo analógico", "analógico", "1980s", "obsoleto"],
       ["FireWire", "400 - 800 Mbps", "serie isócrono", "1995", "obsoleto"],
       ["Fast Ethernet", "100 Mbps", "red", "1995", "activo"],
       ["USB 2.0", "480 Mbps", "serie", "2000", "activo (periféricos)"],
       ["Gigabit Ethernet", "1 Gbps", "red", "1999", "estándar"],
       ["eSATA 6 Gbps", "6 Gbps", "almacenamiento", "2004", "legado"],
       ["USB 3.2 / USB4", "10 - 40 Gbps", "serie", "2013-19", "estándar"],
       ["Thunderbolt 3/4/5", "40 - 120 Gbps", "híbrido PCIe+DP", "2015-23", "gama alta"],
       ["10 GbE / SFP+", "10 Gbps", "red", "2006", "profesional"],
       ["HDMI 2.1", "48 Gbps", "video/audio", "2017", "estándar TV"],
       ["DisplayPort 2.1", "80 Gbps", "video/audio", "2022", "estándar PC"]],
      [1.55, 1.75, 1.35, 0.85, 1.3])
page()

# ============================================================ P18 · Chuleta de colores
h2("Chuleta de colores de identificación")
para("Lo primero que se mira al conectar un cable: el color.", size=9.5, color=GRAY, italic=True)
table(["Color / elemento", "Qué indica", "Dónde se ve"],
      [["USB blanco / gris", "USB 1.0-1.1 · 12 Mbps", "lengüeta interior del conector"],
       ["USB negro", "USB 2.0 · 480 Mbps", "lengüeta interior del conector"],
       ["USB azul (+ SS)", "USB 3.0/3.1 Gen 1 · 5 Gbps", "lengüeta interior del conector"],
       ["USB rojo / turquesa", "USB 3.1 Gen 2 / 3.2 · 10 Gbps", "lengüeta interior del conector"],
       ["PS/2 verde", "Ratón (exclusivo)", "puerto mini-DIN de 6"],
       ["PS/2 morado", "Teclado (exclusivo)", "puerto mini-DIN de 6"],
       ["VGA azul", "Monitor analógico · 15 pines", "interior del conector HD15"],
       ["LPT burdeos", "Impresora paralela · 25 pines", "interior del DB-25 (PC99)"],
       ["Game Port dorado", "Joystick / MIDI", "tarjeta de sonido (DA-15)"],
       ["RCA amarillo", "Video compuesto SD", "conector RCA"],
       ["Audio verde / rosado / azul", "Salida / micrófono / line-in", "jacks de 3.5 mm (PC99)"],
       ["RCA naranja", "S/PDIF coaxial · 75 Ω", "conector RCA de audio digital"],
       ["LED verde RJ-45", "Enlace de red establecido", "puerto Ethernet"],
       ["LED ámbar RJ-45", "Actividad de datos (o 100 Mbps)", "puerto Ethernet"],
       ["Luz roja TOSLINK", "Audio óptico activo (~650 nm)", "conector de fibra óptica"],
       ["Fibra amarilla / aqua", "Monomodo (larga dist.) / multimodo", "cables SFP / LC"],
       ["Ventana rojo oscuro", "Puerto infrarrojo IrDA", "panel frontal de la PC"]],
      [1.95, 2.6, 2.25])
page()

# ============================================================ P19 · No confundir
h2("No confundir · Pares que se parecen")
bullets([
    "**RJ-45 vs RJ-11:** mismo lenguaje, distinto tamaño — 8 contactos (red) frente a 2-4 "
    "(teléfono). Forzar uno en el otro dobla los contactos.",
    "**USB-C vs Thunderbolt:** conector idéntico; solo el **icono del rayo ⚡** y la "
    "documentación confirman Thunderbolt. Un USB-C normal no mueve eGPU ni dos pantallas.",
    "**HDMI vs DisplayPort:** HDMI tiene **dos esquinas biseladas abajo** y sin pestillo; "
    "DisplayPort tiene **una esquina biselada** y **pestillo de seguridad** arriba.",
    "**USB-A 2.0 vs 3.0:** misma forma; solo el color interior (negro vs azul) y los 5 contactos "
    "extra del 3.0 los delatan.",
    "**DVI-I vs DVI-D:** el DVI-I tiene 4 pines analógicos alrededor de la blade y adapta a VGA "
    "pasivamente; el DVI-D no.",
    "**Mini-B vs Micro-B:** Mini-B es más grueso y trapezoidal; Micro-B, fino con rebeles. "
    "Físicamente incompatibles."])
h2("Datos que suelen faltar · Resumen")
table(["Parámetro", "Valores prácticos"],
      [["Alimentación USB", "2.5 W (2.0) → 4.5 W (3.x) → 7.5 W (BC 1.2) → 240 W (USB-C PD 3.1)"],
       ["Longitudes de cable", "USB 2.0: 5 m · USB 3.x: 2-3 m · USB4/TB: 0.8-2 m · red: 100 m · "
        "RS-232: 15 m · S/PDIF: 10 m · eSATA: 2 m"],
       ["PoE (Ethernet)", "802.3af 15.4 W · 802.3at 30 W · 802.3bt 60-100 W"],
       ["Audio TRRS", "CTIA (estándar de smartphones) y OMTP (antiguo): incompatibles entre sí"],
       ["Video SD", "Compuesto: 480i/576i multiplexado · S-Video: 480i/576i con Y/C separados"]],
      [1.75, 5.05])
page()

# ============================================================ P20 · Glosario
h2("Glosario técnico")
table(["Término", "Definición"],
      [["Hot-plug", "Conexión y desconexión del periférico con el equipo encendido."],
       ["TMDS", "Transmisión diferencial minimizada: capa física de DVI y HDMI."],
       ["ARC / eARC", "Canal de retorno de audio del TV al receptor por HDMI (eARC: sin pérdida)."],
       ["CEC", "Control remoto único de todos los dispositivos HDMI interconectados."],
       ["HDCP", "Cifrado de contenido protegido en HDMI/DisplayPort (2.3 para 4K)."],
       ["DSC", "Display Stream Compression: compresión visual sin pérdida perceptible."],
       ["Adaptive-Sync", "Sincronización variable de refresco (FreeSync / G-Sync Compatible)."],
       ["MST / SST", "Multi-Stream (cadena de monitores) / Single-Stream en DisplayPort."],
       ["UASP", "Protocolo SCSI sobre USB: discos externos un 20-30 % más rápidos."],
       ["USB Power Delivery", "Negociación de hasta 240 W por USB-C (5-48 V)."],
       ["Alt Mode", "Modo alternativo USB-C: video (DP/HDMI) o Thunderbolt por el mismo cable."],
       ["PoE", "Power over Ethernet: alimentación por cable de red (hasta 60-100 W)."],
       ["T568A / T568B", "Orden de hilos estándar en los conectores RJ-45."],
       ["SFP / QSFP", "Transceptores modulares de fibra óptica (1-400 Gbps)."],
       ["LC / MPO", "Conectores de fibra dúplex pequeños / multifibra de datacenter."],
       ["DDC / EDID", "Identificación del monitor por el cable (plug & play de video)."],
       ["Y/C (S-Video)", "Luminancia y crominancia separadas para mejor imagen."],
       ["TRS / TRRS", "Conector de audio de 3 o 4 polos (con micrófono)."],
       ["S/PDIF", "Interfaz de audio digital de Sony/Philips (óptica o coaxial)."],
       ["UHS-I/II/III", "Estándares de bus de tarjetas SD (104-624 MB/s)."],
       ["IrDA SIR/FIR", "Infrarrojo lento (115.2 kbps) y rápido (4 Mbps)."]],
      [1.75, 5.05], font=9)
para("Fin de la guía · Puertos de Comunicación de PC — Guía Completa y Detallada · 2026",
     size=9, color=GRAY, align=WD_ALIGN_PARAGRAPH.CENTER)

footer()
doc.save(OUT)
print("Word escrito en:", OUT)
