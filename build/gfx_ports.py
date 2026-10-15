# -*- coding: utf-8 -*-
"""Diagramas técnicos de puertos de comunicación (PNG con transparencia).

Los conectores se dibujan con sus COLORES FÍSICOS REALES (azul USB 3.0, burdeos
LPT, amarillo RCA, verde/morado PS/2, ...) ya que son el código de identificación
principal. Las etiquetas usan la paleta activa (oscuro/claro).
"""
import os, math
from gfx import Draw, GEN
import theme

# ---------------------------------------------------------------- colores reales
C_WHITE_USB = "#E9E9E9"   # USB 1.x / DVI / plástico blanco
C_BLACK_USB = "#1C1C1C"   # USB 2.0
C_BLUE_USB  = "#2050C8"   # USB 3.0 (azul característico)
C_RED_USB   = "#C22B25"   # USB 3.1 Gen 2
C_TEAL_USB  = "#0E8B8B"   # USB 3.2 / teal
C_METAL     = "#A8B2C0"   # carcasa metálica cromada
C_METAL_D   = "#6E7887"
C_GOLD      = "#D4A017"   # contactos dorados / game port
C_TEAL_SUB  = "#2E8F8F"   # RS-232 turquesa
C_BURGUNDY  = "#7E2436"   # LPT burdeos (PC99)
C_VGA_BLUE  = "#2E5ACC"   # VGA azul
C_GREEN_PS  = "#2FA84F"   # PS/2 ratón
C_PURPLE_PS = "#7A3BB5"   # PS/2 teclado
C_JACK_GRN  = "#3ECB52"   # salida altavoces
C_JACK_PNK  = "#E7548C"   # micrófono
C_JACK_BLU  = "#4FA3E3"   # line-in
C_JACK_ORG  = "#E8862A"   # central/subwoofer / S/PDIF coaxial
C_JACK_BLK  = "#222222"   # traseros
C_JACK_GRY  = "#9AA3B0"   # surround lateral
C_YELLOW    = "#E8C020"   # compuesto RCA
C_LED_GRN   = "#2FE06A"
C_LED_AMB   = "#F5A623"
C_TOS_RED   = "#FF4038"   # luz TOSLINK / IrDA
C_IRDA      = "#8A1420"
C_SFP_MET   = "#8C98A8"
C_SFP_BAIL  = "#2050C8"


# ---------------------------------------------------------------- utilidades
def _panel(d, title, sub=None):
    d.rrect(0.05, 0.05, d.wi - 0.10, d.hi - 0.10, fill=None, line="line", lw=1.0, r=0.12)
    d.text(0.18, 0.12, title, 9.5, "txt3", True, mono=True)
    if sub:
        d.text(d.wi - 0.18, 0.12, sub, 9, "txt3", False, mono=True, align="r")


def _tag(d, x, y, s, color="txt3", size=8.5):
    d.text(x, y, s, size, color, False, mono=True, align="c")


def _usb_a(d, x, y, w, h, tongue, label, metal=C_METAL):
    """Conector USB-A macho (vista frontal del plug) con lengüeta de color."""
    d.rrect(x, y, w, h, fill=metal, line="txt3", lw=1.0, r=0.045)
    pad = 0.045
    d.rrect(x + pad, y + pad, w - 2 * pad, h - 2 * pad, fill=C_BLACK_USB, r=0.03)
    d.rrect(x + w * 0.14, y + h * 0.22, w * 0.72, h * 0.42, fill=tongue, r=0.02)
    for i in range(4):
        cx = x + w * 0.22 + i * w * 0.19
        d.rect(cx - 0.012, y + h * 0.28, 0.024, h * 0.30, fill=C_GOLD)
    d.text(x + w / 2, y + h + 0.10, label, 8.5, "txt2", True, align="c")


def _usb_c(d, x, y, w, h, label):
    """Conector USB-C (óvalo simétrico reversible)."""
    d.rrect(x, y, w, h, fill=C_METAL, line="txt3", lw=1.0, r=h / 2.0)
    d.rrect(x + 0.06, y + 0.065, w - 0.12, h - 0.13, fill=C_BLACK_USB, r=(h - 0.13) / 2.0)
    n = 12
    for i in range(n):
        cx = x + w * 0.16 + i * (w * 0.68 / (n - 1))
        d.rect(cx - 0.010, y + h * 0.36, 0.020, h * 0.28, fill=C_GOLD)
    d.text(x + w / 2, y + h + 0.10, label, 8.5, "txt2", True, align="c")


def _dsub(d, x, y, w, h, shell, rows, holes, label, sub=None, hole_r=0.038,
          metal=True, hole_fill=None):
    """Conector D-sub: cuerpo trapezoidal 'D' con pines/huecos."""
    # escudo metálico en forma de D
    pts = [(x + 0.16, y), (x + w - 0.16, y), (x + w, y + h * 0.16),
           (x + w - 0.10, y + h), (x + 0.10, y + h), (x, y + h * 0.16)]
    pts.append(pts[0])
    d.poly(pts, line="txt3", lw=1.2, fill=shell)
    ix, iy = x + 0.14, y + 0.12
    iw, ih = w - 0.28, h - 0.24
    pts2 = [(ix + 0.12, iy), (ix + iw - 0.12, iy), (ix + iw, iy + ih * 0.18),
            (ix + iw - 0.08, iy + ih), (ix + 0.08, iy + ih), (ix, iy + ih * 0.18)]
    pts2.append(pts2[0])
    d.poly(pts2, line=None, lw=0, fill=C_BLACK_USB if hole_fill is None else hole_fill)
    # pines
    for r, cnt in enumerate(rows):
        rowy = iy + ih * (0.32 + 0.36 * r)
        span = iw * 0.74
        start = ix + (iw - span) / 2.0 + span / (2 * cnt)
        for i in range(cnt):
            cx = start + i * (span / max(1, cnt - 1)) if cnt > 1 else ix + iw / 2
            d.circle(cx, rowy, hole_r, fill=C_GOLD, line="txt3", lw=0.6)
    d.text(x + w / 2, y + h + 0.12, label, 9, "txt2", True, align="c")
    if sub:
        d.text(x + w / 2, y + h + 0.32, sub, 8, "txt3", False, mono=True, align="c")


def _minidin(d, cx, cy, r, pins, body, label, sub=None, key=True):
    """Mini-DIN circular (PS/2, S-Video): cuerpo + pines alrededor."""
    d.circle(cx, cy, r, fill=body, line="txt3", lw=1.1)
    d.circle(cx, cy, r * 0.82, fill=C_BLACK_USB)
    if key:
        d.rect(cx - r * 0.10, cy - r * 0.92, r * 0.20, r * 0.30, fill=body)
    for i in range(pins):
        ang = -math.pi / 2 + (i + 1) * (2 * math.pi / (pins + 1))
        px = cx + r * 0.52 * math.cos(ang)
        py = cy + r * 0.52 * math.sin(ang)
        d.circle(px, py, r * 0.115, fill=C_GOLD)
    d.circle(cx, cy + r * 0.30, r * 0.13, fill=C_GOLD)  # pin guía central-abajo
    d.text(cx, cy + r + 0.14, label, 9, "txt2", True, align="c")
    if sub:
        d.text(cx, cy + r + 0.34, sub, 8, "txt3", False, mono=True, align="c")


def _rj(d, x, y, w, h, contacts, label, sub=None, leds=False, latch=True, shell=None):
    """Conector RJ (RJ-45 / RJ-11) frontal con contactos dorados."""
    shell = shell or C_METAL
    d.rrect(x, y, w, h, fill=shell, line="txt3", lw=1.0, r=0.05)
    d.rrect(x + 0.08, y + 0.10, w - 0.16, h * 0.52, fill=C_BLACK_USB, r=0.03)
    span = (w - 0.30) * 0.80
    start = x + (w - span) / 2.0
    for i in range(contacts):
        cx = start + i * (span / max(1, contacts - 1))
        d.rect(cx - 0.017, y + 0.16, 0.034, h * 0.38, fill=C_GOLD)
    if latch:
        d.rrect(x + w * 0.32, y + h * 0.66, w * 0.36, h * 0.18, fill=C_BLACK_USB, r=0.03)
    if leds:
        d.circle(x + 0.16, y + h * 0.20, 0.055, fill=C_LED_GRN)
        d.circle(x + w - 0.16, y + h * 0.20, 0.055, fill=C_LED_AMB)
    d.text(x + w / 2, y + h + 0.12, label, 9, "txt2", True, align="c")
    if sub:
        d.text(x + w / 2, y + h + 0.32, sub, 8, "txt3", False, mono=True, align="c")


def _jack(d, cx, cy, r, color, label, sub=None):
    """Jack hembra circular (audio 3.5 mm, RCA)."""
    d.circle(cx, cy, r, fill=color, line="txt3", lw=1.0)
    d.circle(cx, cy, r * 0.72, fill=C_BLACK_USB)
    d.circle(cx, cy, r * 0.38, fill=color)
    d.circle(cx, cy, r * 0.22, fill=C_BLACK_USB)
    d.text(cx, cy + r + 0.12, label, 8.5, "txt2", True, align="c")
    if sub:
        d.text(cx, cy + r + 0.31, sub, 7.5, "txt3", False, mono=True, align="c")


# ================================================================ diagramas
def usb_colors():
    d = Draw(5.8, 3.3)
    _panel(d, "USB · LENGÜETA INTERIOR = VERSIÓN", "código de colores")
    items = [(C_WHITE_USB, "USB 1.0 / 1.1", "blanco o gris"),
             (C_BLACK_USB, "USB 2.0", "negro"),
             (C_BLUE_USB, "USB 3.0 / 3.1 G1", "azul · SS"),
             (C_RED_USB, "USB 3.1 G2 / 3.2", "rojo o turquesa")]
    for i, (col, lab, sub) in enumerate(items):
        x = 0.45 + i * 1.32
        _usb_a(d, x, 0.75, 1.05, 0.72, col, "")
        d.text(x + 0.525, 1.62, lab, 7.6, "txt2", True, align="c")
        d.text(x + 0.525, 1.82, sub, 7.6, "txt3", False, mono=True, align="c")
    _usb_c(d, 2.05, 2.35, 1.70, 0.60, "USB Tipo C")
    d.text(3.95, 2.42, "óvalo · simétrico · reversible", 8.5, "txt2")
    d.text(3.95, 2.62, "icono ⚡ (Thunderbolt) o DP al lado", 8.5, "txt3")
    d.text(0.45, 2.42, "USB-A macho", 8.5, "txt3", mono=True)
    d.save("usb_colors")


def usb_types():
    d = Draw(5.8, 2.9)
    _panel(d, "USB · FAMILIA DE CONECTORES", "A / B / Mini / Micro / C")
    # Type A hembra
    d.rrect(0.45, 0.85, 1.15, 0.72, fill=C_METAL, line="txt3", lw=1.0, r=0.05)
    d.rrect(0.55, 1.02, 0.95, 0.38, fill=C_BLACK_USB, r=0.03)
    d.rrect(0.68, 1.10, 0.69, 0.22, fill=C_BLUE_USB, r=0.02)
    d.text(1.02, 1.72, "Type A", 8.5, "txt2", True, align="c")
    # Type B
    pts = [(2.15, 0.85), (3.15, 0.85), (3.15, 1.57), (2.15, 1.57), (2.15, 0.85)]
    d.poly(pts, line="txt3", lw=1.0, fill=C_METAL)
    d.rrect(2.32, 1.02, 0.66, 0.38, fill=C_BLACK_USB, r=0.04)
    d.text(2.65, 1.72, "Type B", 8.5, "txt2", True, align="c")
    # Mini-B
    pts = [(3.75, 0.92), (4.62, 0.85), (4.62, 1.57), (3.75, 1.57), (3.75, 0.92)]
    d.poly(pts, line="txt3", lw=1.0, fill=C_METAL)
    d.rrect(3.88, 1.03, 0.58, 0.36, fill=C_BLACK_USB, r=0.03)
    d.text(4.18, 1.72, "Mini-B", 8.5, "txt2", True, align="c")
    # Micro-B
    pts = [(5.05, 0.98), (5.55, 0.88), (5.55, 1.52), (5.05, 1.62), (5.05, 0.98)]
    d.poly(pts, line="txt3", lw=1.0, fill=C_METAL)
    d.rect(5.15, 1.10, 0.32, 0.30, fill=C_BLACK_USB)
    d.text(5.30, 1.72, "Micro-B", 8.5, "txt2", True, align="c")
    # fila inferior: C + notas
    _usb_c(d, 0.45, 2.10, 1.45, 0.55, "Type C")
    d.text(2.15, 2.14, "· A y B: equipos fijos (PC, disco, impresora)", 8.5, "txt2")
    d.text(2.15, 2.36, "· Mini/Micro: cámaras y móviles (Micro = USB 2.0/3.0)", 8.5, "txt2")
    d.text(2.15, 2.58, "· C: 24 pines, reversible, sustituye a todos los anteriores", 8.5, "txt2")
    d.save("usb_types")


def dsub9():
    d = Draw(3.4, 2.7)
    _panel(d, "RS-232", "DE-9 · macho")
    _dsub(d, 0.85, 0.75, 1.75, 1.05, C_TEAL_SUB, [5, 4], 9, "DB-9 / DE-9",
          "turquesa o gris metálico")
    d.text(1.72, 2.30, "1 DCD · 2 RXD · 3 TXD · 4 DTR · 5 GND", 7.6, "txt3", mono=True, align="c")
    d.text(1.72, 2.50, "6 DSR · 7 RTS · 8 CTS · 9 RI", 7.6, "txt3", mono=True, align="c")
    d.save("dsub9")


def dsub25():
    d = Draw(3.6, 2.7)
    _panel(d, "LPT / PARALELO", "DB-25 · hembra")
    _dsub(d, 0.70, 0.70, 2.20, 1.15, C_BURGUNDY, [13, 12], 25, "DB-25",
          "burdeos / rojo oscuro", hole_r=0.030)
    d.text(1.80, 2.34, "8 líneas de datos + handshake (IEEE 1284)", 7.6, "txt3", mono=True, align="c")
    d.text(1.80, 2.53, "color PC99: burdeos", 7.6, "txt3", mono=True, align="c")
    d.save("dsub25")


def thunderbolt():
    d = Draw(5.2, 2.8)
    _panel(d, "THUNDERBOLT", "PCIe + DisplayPort")
    # puerto USB-C con rayo
    _usb_c(d, 0.60, 0.95, 1.75, 0.62, "USB-C (TB3/4/5)")
    # icono rayo
    bx, by = 2.75, 0.92
    d.poly([(bx, by), (bx + 0.30, by), (bx + 0.14, by + 0.26), (bx + 0.36, by + 0.26),
            (bx + 0.08, by + 0.66), (bx + 0.17, by + 0.36), (bx, by + 0.36)], line=C_GOLD, lw=1.2,
           fill=C_GOLD)
    d.text(3.35, 1.05, "icono ⚡ junto al puerto", 8.5, "txt2")
    d.text(3.35, 1.28, "obligatorio para reconocerlo", 8.5, "txt3")
    # mini DP con rayo
    d.rrect(0.60, 1.95, 1.35, 0.52, fill=C_METAL, line="txt3", lw=1.0, r=0.05)
    d.rrect(0.72, 2.07, 1.11, 0.28, fill=C_BLACK_USB, r=0.03)
    d.text(1.28, 2.58, "Mini DP (TB1 / TB2)", 8.5, "txt2", True, align="c")
    d.poly([(2.35, 1.92), (2.65, 1.92), (2.49, 2.18), (2.71, 2.18), (2.43, 2.58),
            (2.52, 2.28), (2.35, 2.28)], line=C_GOLD, lw=1.2, fill=C_GOLD)
    d.text(3.35, 2.05, "cadena de 6 dispositivos", 8.5, "txt2")
    d.text(3.35, 2.28, "eGPU · docks · 4K / 8K", 8.5, "txt3")
    d.save("thunderbolt")


def firewire():
    d = Draw(5.0, 2.8)
    _panel(d, "FIREWIRE · IEEE 1394", "Apple 1995")
    # conector 6 pines (borde en V)
    pts = [(0.55, 0.90), (1.95, 0.90), (1.95, 1.62), (1.25, 1.40), (0.55, 1.62), (0.55, 0.90)]
    d.poly(pts, line="txt3", lw=1.1, fill=C_METAL)
    for i in range(3):
        d.circle(0.95 + i * 0.35, 1.12, 0.055, fill=C_GOLD)
        d.circle(0.95 + i * 0.35, 1.42, 0.055, fill=C_GOLD)
    d.text(1.25, 1.84, "6 pines · 1394a (+30 V)", 8, "txt2", True, align="c")
    # conector 4 pines i.LINK
    pts = [(2.65, 0.98), (3.75, 0.98), (3.75, 1.55), (3.20, 1.38), (2.65, 1.55), (2.65, 0.98)]
    d.poly(pts, line="txt3", lw=1.1, fill=C_METAL)
    d.circle(3.00, 1.16, 0.05, fill=C_GOLD)
    d.circle(3.40, 1.16, 0.05, fill=C_GOLD)
    d.circle(3.00, 1.40, 0.05, fill=C_GOLD)
    d.circle(3.40, 1.40, 0.05, fill=C_GOLD)
    d.text(3.20, 1.84, "4 pines · i.LINK (sin V)", 8, "txt2", True, align="c")
    # logo FireWire: círculo con tres ramas
    cx, cy = 4.45, 1.22
    d.circle(cx, cy, 0.30, fill=None, line=C_GOLD, lw=1.6)
    for a in (-1.2, 0.0, 1.2):
        d.line(cx, cy, cx + 0.26 * math.cos(a - math.pi / 2), cy + 0.26 * math.sin(a - math.pi / 2),
               C_GOLD, 1.6)
    d.text(cx, 1.72, "logo FireWire", 8, "txt3", align="c")
    d.text(0.55, 2.34, "400 Mbps (1394a) · 800 Mbps (1394b) · 63 dispositivos en cadena", 8.2, "txt2")
    d.text(0.55, 2.55, "conector con borde en V · logo de círculo con tres ramas", 8.2, "txt3")
    d.save("firewire")


def ps2():
    d = Draw(5.2, 2.9)
    _panel(d, "PS/2 · MINI-DIN 6", "PC99 · 1987")
    _minidin(d, 1.25, 1.35, 0.62, 6, C_PURPLE_PS, "TECLADO", "morado / violeta")
    _minidin(d, 3.05, 1.35, 0.62, 6, C_GREEN_PS, "RATÓN", "verde")
    # puerto combo
    d.circle(4.55, 1.35, 0.62, fill="#5B8FD9", line="txt3", lw=1.1)
    d.circle(4.55, 1.35, 0.51, fill=C_BLACK_USB)
    for i in range(6):
        ang = -math.pi / 2 + (i + 1) * (2 * math.pi / 7)
        d.circle(4.55 + 0.32 * math.cos(ang), 1.35 + 0.32 * math.sin(ang), 0.07, fill=C_GOLD)
    d.text(4.55, 2.12, "COMBO (portátiles)", 8, "txt2", True, align="c")
    d.text(4.55, 2.32, "teclado + ratón", 7.5, "txt3", mono=True, align="c")
    d.text(0.55, 2.52, "6 pines (4 activos: DATA, CLK, +5 V, GND) · IRQ 1 teclado · IRQ 12 ratón",
           8.2, "txt2")
    d.save("ps2")


def din5():
    d = Draw(3.3, 2.9)
    _panel(d, "DIN-5 · TECLADO AT", "IBM 1984")
    cx, cy, r = 1.65, 1.35, 0.72
    d.circle(cx, cy, r, fill=C_METAL, line="txt3", lw=1.2)
    d.circle(cx, cy, r * 0.80, fill="#3A4250")
    for i in range(5):
        ang = math.radians(200 + i * 35)
        d.circle(cx + r * 0.48 * math.cos(ang), cy + r * 0.48 * math.sin(ang), 0.085,
                 fill=C_GOLD, line="txt3", lw=0.6)
    d.arc(cx - r * 0.30, cy - r * 0.30, r * 0.60, r * 0.60, 200, 340, color="txt3", lw=1.2)
    d.text(cx, cy + r + 0.16, "5 pines en media luna · plateado", 8.5, "txt2", True, align="c")
    d.text(cx, 2.42, "1 CLK · 2 DATA · 3 RESET · 4 GND · 5 +5 V", 7.8, "txt3", mono=True, align="c")
    d.text(cx, 2.61, "anillo guía · síncrono 10-16 kHz", 7.8, "txt3", mono=True, align="c")
    d.save("din5")


def gameport():
    d = Draw(3.8, 2.9)
    _panel(d, "GAME PORT · DA-15", "tarjetas de sonido")
    _dsub(d, 0.75, 0.80, 2.30, 1.15, C_GOLD, [8, 7], 15, "DA-15 hembra",
          "amarillo dorado", hole_r=0.032)
    d.text(1.90, 2.38, "4 ejes analógicos (100 kΩ) · 4 botones · +5 V", 7.6, "txt3", mono=True, align="c")
    d.text(1.90, 2.57, "adaptador MIDI: 15 pines → 2 × DIN-5 (31.25 kbaud)", 7.6, "txt3", mono=True, align="c")
    d.save("gameport")


def vga():
    d = Draw(4.6, 3.1)
    _panel(d, "VGA · HD15 / DE-15", "analógico RGBHV")
    # cuerpo D azul
    x, y, w, h = 0.75, 0.80, 3.10, 1.35
    pts = [(x + 0.35, y), (x + w - 0.35, y), (x + w, y + 0.30), (x + w - 0.18, y + h),
           (x + 0.18, y + h), (x, y + 0.30)]
    pts.append(pts[0])
    d.poly(pts, line="txt3", lw=1.2, fill=C_METAL)
    ix, iy, iw, ih = x + 0.22, y + 0.16, w - 0.44, h - 0.36
    pts2 = [(ix + 0.16, iy), (ix + iw - 0.16, iy), (ix + iw, iy + 0.18),
            (ix + iw - 0.10, iy + ih), (ix + 0.10, iy + ih), (ix, iy + 0.18)]
    pts2.append(pts2[0])
    d.poly(pts2, line=None, lw=0, fill=C_VGA_BLUE)
    for r in range(3):
        for i in range(5):
            cx = ix + iw * (0.16 + i * 0.17)
            cy = iy + ih * (0.22 + r * 0.28)
            d.circle(cx, cy, 0.042, fill=C_GOLD, line="txt3", lw=0.5)
    # tornillos
    for sx in (x - 0.02, x + w - 0.10):
        d.rrect(sx, y + 0.35, 0.12, 0.62, fill=C_METAL_D, r=0.03)
        d.circle(sx + 0.06, y + 0.66, 0.035, fill="#454E5C")
    d.text(x + w / 2, y + h + 0.16, "15 pines · 3 filas de 5 · interior AZUL", 9, "txt2", True, align="c")
    d.text(2.30, 2.72, "tornillos de sujeción manual a los lados · 0.7 Vp-p 75 Ω · DDC/EDID",
           8, "txt3", mono=True, align="c")
    d.save("vga")


def dvi():
    d = Draw(5.6, 3.2)
    _panel(d, "DVI · DVI-I / DVI-D / DVI-A", "interior blanco")
    x, y, w, h = 0.60, 0.85, 4.40, 1.45
    d.rrect(x, y, w, h, fill=C_WHITE_USB, line="txt3", lw=1.1, r=0.06)
    d.rrect(x + 0.18, y + 0.16, w - 1.15, h - 0.32, fill=C_BLACK_USB, r=0.03)
    # rejilla de pines 8+8 (dos bloques de 3x3 sin el central) simplificada a 8+8
    for blk in range(2):
        for r in range(3):
            for i in range(3):
                if blk == 1 and r == 1 and i == 1:
                    continue
                cx = x + 0.42 + blk * 1.55 + i * 0.36
                cy = y + 0.36 + r * 0.36
                d.rect(cx - 0.065, cy - 0.065, 0.13, 0.13, fill=C_GOLD)
    # barra horizontal (blade)
    d.rrect(x + 3.42, y + 0.30, 0.16, h - 0.60, fill=C_METAL_D, r=0.03)
    # pines analógicos C1-C5 (DVI-I)
    for i in range(4):
        d.circle(x + 3.68 + (i % 2) * 0.26, y + 0.42 + (i // 2) * 0.62, 0.062, fill=C_GOLD,
                 line="txt3", lw=0.5)
    d.text(x + w / 2, y + h + 0.16, "DVI-I: pines analógicos C1–C5 + barra (blade)", 9, "txt2",
           True, align="c")
    d.text(0.60, 2.72, "DVI-D solo digital · DVI-A solo analógico · DVI-I integrado (adapta a VGA pasivamente)",
           8.5, "txt2")
    d.text(0.60, 2.92, "Single Link 4.95 Gbps · Dual Link 9.9 Gbps (2560×1600) · HDCP opcional",
           8.5, "txt3")
    d.save("dvi")


def hdmi():
    d = Draw(5.8, 2.9)
    _panel(d, "HDMI · CONECTORES", "audio + video digital")
    # Type A
    x, y, w, h = 0.55, 0.85, 2.25, 0.85
    pts = [(x + 0.18, y), (x + w - 0.18, y), (x + w, y + h * 0.35), (x + w - 0.10, y + h),
           (x + 0.10, y + h), (x, y + h * 0.35)]
    pts.append(pts[0])
    d.poly(pts, line="txt3", lw=1.1, fill=C_METAL)
    pts2 = [(x + 0.30, y + 0.14), (x + w - 0.30, y + 0.14), (x + w - 0.22, y + 0.34),
            (x + w - 0.32, y + h - 0.18), (x + 0.32, y + h - 0.18), (x + 0.22, y + 0.34)]
    pts2.append(pts2[0])
    d.poly(pts2, line=None, lw=0, fill=C_BLACK_USB)
    for i in range(10):
        d.rect(x + 0.42 + i * 0.145, y + 0.30, 0.030, 0.30, fill=C_GOLD)
    d.text(1.68, 1.92, "Type A estándar (19 pines)", 8.5, "txt2", True, align="c")
    # Mini (C)
    pts = [(3.25, 0.95), (4.30, 0.95), (4.30, 1.58), (3.25, 1.58), (3.25, 0.95)]
    d.poly(pts, line="txt3", lw=1.0, fill=C_METAL)
    d.rrect(3.38, 1.08, 0.79, 0.36, fill=C_BLACK_USB, r=0.03)
    d.text(3.78, 1.92, "Mini HDMI (C)", 8.5, "txt2", True, align="c")
    # Micro (D)
    pts = [(4.65, 1.05), (5.55, 1.05), (5.55, 1.50), (4.65, 1.50), (4.65, 1.05)]
    d.poly(pts, line="txt3", lw=1.0, fill=C_METAL)
    d.rrect(4.76, 1.15, 0.68, 0.26, fill=C_BLACK_USB, r=0.03)
    d.text(5.10, 1.92, "Micro HDMI (D)", 8.5, "txt2", True, align="c")
    d.text(0.55, 2.30, "esquinas biseladas inferiores · marco cromado · interior negro · logotipo grabado",
           8.5, "txt2")
    d.text(0.55, 2.52, "HDMI 1.4: 10.2 Gbps · 2.0: 18 Gbps · 2.1: 48 Gbps (8K/4K120) · ARC/eARC · CEC · HDCP",
           8.5, "txt3")
    d.save("hdmi")


def dp():
    d = Draw(5.2, 2.9)
    _panel(d, "DISPLAYPORT", "VESA · 20 pines")
    x, y, w, h = 0.60, 0.95, 2.60, 1.05
    # una esquina biselada (superior derecha)
    pts = [(x, y), (x + w - 0.28, y), (x + w, y + 0.28), (x + w, y + h), (x, y + h)]
    pts.append(pts[0])
    d.poly(pts, line="txt3", lw=1.1, fill=C_METAL)
    pts2 = [(x + 0.12, y + 0.12), (x + w - 0.36, y + 0.12), (x + w - 0.16, y + 0.32),
            (x + w - 0.16, y + h - 0.12), (x + 0.12, y + h - 0.12)]
    pts2.append(pts2[0])
    d.poly(pts2, line=None, lw=0, fill=C_BLACK_USB)
    for i in range(10):
        d.rect(x + 0.26 + i * 0.20, y + 0.28, 0.032, 0.42, fill=C_GOLD)
    # pestillo superior
    d.rrect(x + w * 0.30, y - 0.16, w * 0.34, 0.16, fill=C_METAL_D, r=0.03)
    d.text(x + w / 2, y + h + 0.18, "pestillo de seguridad + 1 esquina biselada", 8.5, "txt2", True,
           align="c")
    # mini DP
    d.rrect(3.65, 1.15, 1.25, 0.62, fill=C_METAL, line="txt3", lw=1.0, r=0.05)
    d.rrect(3.78, 1.28, 0.99, 0.36, fill=C_BLACK_USB, r=0.03)
    d.text(4.28, 1.92, "Mini DisplayPort", 8.5, "txt2", True, align="c")
    d.text(0.60, 2.32, "DP 1.2: 21.6 Gbps · DP 1.4: 32.4 Gbps · DP 2.0/2.1: 80 Gbps (UHBR20)",
           8.5, "txt2")
    d.text(0.60, 2.54, "MST (cadena de monitores) · Adaptive-Sync · DP Alt Mode en USB-C · DSC",
           8.5, "txt3")
    d.save("dp")


def svideo():
    d = Draw(3.1, 2.9)
    _panel(d, "S-VIDEO", "Y/C separados")
    _minidin(d, 1.55, 1.28, 0.62, 4, C_JACK_BLK, "mini-DIN 4 o 7 pines", "negro · pivote guía")
    d.text(1.55, 2.42, "Y (luminancia) + C (crominancia) + 2 GND", 7.6, "txt3", mono=True, align="c")
    d.text(1.55, 2.61, "SD 480i/576i · mejor que compuesto", 7.6, "txt3", mono=True, align="c")
    d.save("svideo")


def composite():
    d = Draw(2.9, 2.7)
    _panel(d, "VIDEO COMPUESTO", "RCA amarillo")
    _jack(d, 1.45, 1.16, 0.55, C_YELLOW, "RCA AMARILLO", "video compuesto")
    d.text(1.45, 2.30, "1 Vp-p · 75 Ω · NTSC 480i / PAL 576i", 8, "txt3", mono=True, align="c")
    d.text(1.45, 2.50, "rojo/blanco = audio estéreo", 8, "txt3", mono=True, align="c")
    d.save("composite")


def rj45():
    d = Draw(3.6, 3.1)
    _panel(d, "ETHERNET · RJ-45", "8P8C · UTP")
    _rj(d, 1.00, 0.85, 1.60, 1.35, 8, "RJ-45", "pestaña de traba", leds=True)
    d.text(1.80, 2.62, "LED verde = enlace · LED naranja = actividad", 8, "txt3", mono=True, align="c")
    d.text(1.80, 2.80, "100 Mbps · 1 Gbps · 2.5/5/10 Gbps", 8, "txt3", mono=True, align="c")
    d.save("rj45")


def rj_compare():
    d = Draw(5.4, 3.0)
    _panel(d, "RJ-45 vs RJ-11", "no forzar nunca")
    _rj(d, 0.70, 0.85, 1.75, 1.30, 8, "RJ-45 (red)", "8P8C · más ancho", leds=True)
    _rj(d, 3.15, 0.98, 1.30, 1.05, 4, "RJ-11 (teléfono)", "6P2C · más estrecho",
        leds=False, shell=C_WHITE_USB)
    d.text(2.70, 1.45, "≠", 22, "red", True, align="c")
    d.text(0.70, 2.58, "RJ-45: cable UTP Cat5e/6 · hasta 10 Gbps · PoE · 100 m", 8.2, "txt2")
    d.text(0.70, 2.78, "RJ-11: par telefónico · 56 kbps dial-up · jacks 'LINE' / 'PHONE'",
           8.2, "txt2")
    d.save("rj_compare")


def rj11():
    d = Draw(3.2, 2.9)
    _panel(d, "MÓDEM · RJ-11", "línea telefónica")
    _rj(d, 0.95, 0.95, 1.30, 1.10, 4, "RJ-11 (6P2C/6P4C)", "más estrecho que RJ-45",
        leds=False, shell=C_WHITE_USB)
    d.text(1.60, 2.42, "rotulado 'LINE' / 'PHONE' · transparente o blanco", 7.6, "txt3", mono=True, align="c")
    d.text(1.60, 2.61, "56 kbps (V.90/V.92) · fax · ADSL2+ hasta 24 Mbps", 7.6, "txt3", mono=True, align="c")
    d.save("rj11")


def sfp():
    d = Draw(5.0, 2.9)
    _panel(d, "SFP / SFP+ · TRANSCEPTOR", "fibra óptica")
    # ranura / cage
    d.rrect(0.55, 0.95, 2.60, 1.10, fill=C_SFP_MET, line="txt3", lw=1.1, r=0.05)
    d.rrect(0.75, 1.12, 2.20, 0.76, fill=C_BLACK_USB, r=0.03)
    d.text(1.85, 2.22, "bahía (cage) metálica", 8.5, "txt2", True, align="c")
    # módulo con bail latch
    d.rrect(3.45, 1.05, 1.15, 0.90, fill=C_METAL_D, line="txt3", lw=1.0, r=0.04)
    d.rrect(3.55, 1.20, 0.42, 0.60, fill=C_BLACK_USB, r=0.03)
    d.rrect(4.28, 1.28, 0.42, 0.44, fill=C_SFP_BAIL, r=0.06)   # palanca
    d.text(4.02, 2.22, "módulo + palanca", 8.5, "txt2", True, align="c")
    # fibra LC duplex
    d.line(1.85, 0.95, 1.85, 0.55, "#E8C84A", 2.2)
    d.line(2.15, 0.95, 2.15, 0.55, "#E8C84A", 2.2)
    d.circle(1.85, 0.50, 0.055, fill="#E8C84A")
    d.circle(2.15, 0.50, 0.055, fill="#E8C84A")
    d.text(2.00, 0.30, "LC duplex", 8, "txt3", mono=True, align="c")
    d.text(0.55, 2.52, "SFP 1 Gbps · SFP+ 10 Gbps · SFP28 25 Gbps · QSFP+ 40 · QSFP28 100 · QSFP-DD 400",
           8.2, "txt2")
    d.save("sfp")


def audio_jacks():
    d = Draw(6.2, 3.0)
    _panel(d, "JACK 3.5 mm · CÓDIGO DE COLORES", "PC99")
    items = [(C_JACK_GRN, "VERDE", "salida"),
             (C_JACK_PNK, "ROSADO", "micrófono"),
             (C_JACK_BLU, "AZUL", "line-in"),
             (C_JACK_ORG, "NARANJA", "central/sub"),
             (C_JACK_BLK, "NEGRO", "traseros"),
             (C_JACK_GRY, "GRIS", "lateral")]
    for i, (col, lab, sub) in enumerate(items):
        x = 0.78 + i * 0.90
        _jack(d, x, 1.18, 0.33, col, lab)
        d.text(x, 1.78, sub, 7.2, "txt3", align="c")
    # conector TRS/TRRS
    d.line(1.30, 2.35, 3.70, 2.35, "txt2", 2.2)
    for gx, lab in ((1.55, "PUNTA"), (2.15, "ANILLO"), (2.75, "ANILLO"), (3.45, "CASA")):
        d.rect(gx, 2.20, 0.045, 0.30, fill="txt3")
        d.text(gx, 2.58, lab, 7, "txt3", mono=True, align="c")
    d.text(4.30, 2.22, "TRS = 3 polos (estéreo)", 8.5, "txt2")
    d.text(4.30, 2.44, "TRRS = 4 polos (+ micrófono)", 8.5, "txt2")
    d.text(4.30, 2.66, "estándares CTIA / OMTP", 8.5, "txt3")
    d.save("audio_jacks")


def toslink():
    d = Draw(3.4, 2.9)
    _panel(d, "S/PDIF ÓPTICO", "TOSLINK")
    x, y, w, h = 0.95, 0.95, 1.50, 1.20
    d.rrect(x, y, w, h, fill=C_JACK_BLK, line="txt3", lw=1.1, r=0.10)
    # esquinas biseladas
    d.poly([(x + 0.16, y + 0.16), (x + w - 0.16, y + 0.16), (x + w - 0.16, y + h - 0.16),
            (x + 0.16, y + h - 0.16)], line="txt3", lw=1.0, fill="#2A0E0E")
    d.circle(x + w / 2, y + h / 2, 0.30, fill=C_TOS_RED)
    d.circle(x + w / 2, y + h / 2, 0.16, fill="#FF8A82")
    d.text(1.70, 2.32, "tapa abatible · brillo ROJO (~650 nm)", 8, "txt3", mono=True, align="c")
    d.text(1.70, 2.50, "fibra óptica plástica · inmune a EMI", 8, "txt3", mono=True, align="c")
    d.text(1.70, 2.68, "PCM 96 kHz · Dolby Digital / DTS 5.1-7.1", 8, "txt3", mono=True, align="c")
    d.save("toslink")


def spdif_coax():
    d = Draw(2.9, 2.9)
    _panel(d, "S/PDIF COAXIAL", "RCA 75 Ω")
    _jack(d, 1.45, 1.12, 0.52, C_JACK_ORG, "RCA NARANJA", "o negro")
    d.text(1.45, 2.24, "coaxial 75 Ω · 0.5 Vp-p", 8, "txt3", mono=True, align="c")
    d.text(1.45, 2.43, "PCM 24 bit / 96-192 kHz · DTS / Dolby", 8, "txt3", mono=True, align="c")
    d.text(1.45, 2.62, "BNC en equipos profesionales", 8, "txt3", mono=True, align="c")
    d.save("spdif_coax")


def esata():
    d = Draw(4.2, 2.9)
    _panel(d, "eSATA / eSATAp", "SATA externo")
    # conector eSATA tipo L
    x, y = 0.75, 1.05
    pts = [(x, y), (x + 2.10, y), (x + 2.10, y + 0.85), (x + 0.65, y + 0.85),
           (x + 0.65, y + 0.55), (x, y + 0.55)]
    pts.append(pts[0])
    d.poly(pts, line="txt3", lw=1.1, fill=C_METAL)
    d.rrect(x + 0.12, y + 0.12, 1.85, 0.32, fill=C_BLACK_USB, r=0.02)
    for i in range(7):
        d.rect(x + 0.24 + i * 0.24, y + 0.18, 0.038, 0.20, fill=C_GOLD)
    d.text(x + 1.05, y + 1.05, "guías metálicas robustas · serigrafía 'eSATA'", 8.5, "txt2",
           True, align="c")
    d.text(2.10, 2.52, "1.5 / 3 / 6 Gbps · sin alimentación (eSATAp añade 5-12 V)", 8, "txt3",
           mono=True, align="c")
    d.text(2.10, 2.70, "cable máx 2 m · hot-swap con AHCI", 8, "txt3", mono=True, align="c")
    d.save("esata")


def sdcard():
    d = Draw(4.8, 2.9)
    _panel(d, "TARJETAS SD / MICROSD", "lectores")
    # SD
    x, y, w, h = 0.65, 0.85, 1.75, 1.15
    d.rrect(x, y, w, h, fill=C_JACK_BLK, line="txt3", lw=1.0, r=0.05)
    # esquina biselada
    d.poly([(x, y), (x + 0.30, y), (x, y + 0.30)], line=None, lw=0, fill="#111111")
    d.rrect(x + 0.10, y + 0.12, 0.16, 0.34, fill=C_JACK_GRY, r=0.02)   # pestaña lock
    for i in range(8):
        d.rect(x + 0.42 + i * 0.145, y + h - 0.24, 0.085, 0.14, fill=C_GOLD)
    d.text(x + w / 2, y + h + 0.14, "SD · pestaña LOCK", 8.5, "txt2", True, align="c")
    # microSD
    x2, y2, w2, h2 = 2.85, 1.10, 1.05, 0.72
    d.rrect(x2, y2, w2, h2, fill=C_JACK_BLK, line="txt3", lw=1.0, r=0.05)
    for i in range(8):
        d.rect(x2 + 0.14 + i * 0.10, y2 + h2 - 0.17, 0.055, 0.10, fill=C_GOLD)
    d.text(x2 + w2 / 2, y2 + h2 + 0.14, "microSD", 8.5, "txt2", True, align="c")
    # ranura
    d.rrect(4.15, 1.15, 0.42, 0.62, fill=C_METAL_D, line="txt3", lw=0.8, r=0.03)
    d.text(4.36, 1.90, "ranura", 7.5, "txt3", mono=True, align="c")
    d.text(0.65, 2.40, "UHS-I 104 · UHS-II 312 · UHS-III 624 MB/s · SD Express 985+ MB/s",
           8.0, "txt2")
    d.text(0.65, 2.62, "SD 2 GB · SDHC 32 GB · SDXC 2 TB · SDUC 128 TB · V10/V30/V60/V90",
           8.0, "txt3")
    d.save("sdcard")


def irda():
    d = Draw(3.6, 2.9)
    _panel(d, "IrDA · INFRARROJO", "direccional")
    # ventana IrDA
    x, y, w, h = 1.15, 1.05, 1.30, 0.55
    d.rrect(x, y, w, h, fill=C_IRDA, line="txt3", lw=1.0, r=0.12)
    d.rrect(x + 0.12, y + 0.10, w - 0.24, h - 0.20, fill="#B22333", r=0.08)
    # cono de luz
    d.line(x + 0.20, y + h, x + 0.20, y + h + 0.85, C_TOS_RED, 1.4, dash=True)
    d.line(x + w - 0.20, y + h, x + w + 0.35, y + h + 0.85, C_TOS_RED, 1.4, dash=True)
    d.text(1.80, 2.55, "cono ~30° · alcance 0-1 m · línea de visión", 8, "txt3", mono=True, align="c")
    d.text(1.80, 2.73, "SIR 115.2 kbps · FIR 4 Mbps · VFIR 16 Mbps", 8, "txt3", mono=True, align="c")
    d.save("irda")


def port_panels():
    """Portadas de sección: mosaico esquemático de conectores (decorativo)."""
    pass


ALL = [usb_colors, usb_types, dsub9, dsub25, thunderbolt, firewire, ps2, din5, gameport,
       vga, dvi, hdmi, dp, svideo, composite, rj45, rj11, rj_compare, sfp, audio_jacks,
       toslink, spdif_coax, esata, sdcard, irda]


def generate():
    for fn in ALL:
        fn()
        print("   diagrama:", fn.__name__)


if __name__ == "__main__":
    import sys
    pal = sys.argv[1] if len(sys.argv) > 1 else "dark"
    theme.set_palette(pal)
    theme.set_gen("gen_ports_light" if pal == "light" else "gen_ports")
    generate()
