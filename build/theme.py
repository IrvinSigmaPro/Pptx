# -*- coding: utf-8 -*-
"""Tema visual, paleta, tipografías y geometría base de la presentación."""
import os

# ---------------------------------------------------------------- geometría
IN = 914400.0                 # EMU por pulgada
PXIN = 96.0                   # px por pulgada en el renderizador de vista previa
SLIDE_W = 13.3333             # pulgadas (16:9)
SLIDE_H = 7.5
MARGIN = 0.52                 # margen lateral seguro
FOOTER_Y = 6.98

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "_assets")
SRC = os.path.join(ASSETS, "source")
GEN = os.path.join(ASSETS, "gen")
PREVIEW = os.path.join(ROOT, "_preview")

# ------------------------------------------------------------------- colores
COL = {
    "bg":      "0A101E",
    "bg2":     "0D1526",
    "panel":   "111C31",
    "panel2":  "16233C",
    "card":    "131E33",
    "card2":   "18253F",
    "line":    "26334F",
    "line2":   "3A4C71",
    "txt":     "EDF3FC",
    "txt2":    "C0CDE2",
    "txt3":    "8B9CBB",
    "white":   "FFFFFF",
    "cyan":    "22D3EE",
    "orange":  "F59E0B",
    "purple":  "A78BFA",
    "green":   "34D399",
    "pink":    "F472B6",
    "blue":    "60A5FA",
    "red":     "F87171",
    "yellow":  "FDE047",
    "teal":    "2DD4BF",
    "indigo":  "818CF8",
}

# sección -> (acento, número, nombre)
SECTION = {
    1: ("cyan",   "01", "Fundamentos de la lógica digital"),
    2: ("orange", "02", "Compuertas lógicas y chips 74XX"),
    3: ("purple", "03", "Hoja de datos, tiempos y parámetros"),
    4: ("green",  "04", "Aplicaciones reales de la Serie 74XX"),
    5: ("pink",   "05", "Práctica de laboratorio y diagnóstico"),
    6: ("blue",   "06", "Repaso, glosario y recursos"),
}

FONT_H = "Segoe UI Semibold"     # títulos
FONT_B = "Segoe UI"              # cuerpo
FONT_M = "Consolas"              # código / expresiones

# fuentes equivalentes para el renderizador de vista previa (PIL)
TTF = "/usr/share/fonts/truetype/dejavu/"
PIL_FONT = {
    ("body", False): TTF + "DejaVuSans.ttf",
    ("body", True):  TTF + "DejaVuSans-Bold.ttf",
    ("mono", False): TTF + "DejaVuSansMono.ttf",
    ("mono", True):  TTF + "DejaVuSansMono-Bold.ttf",
}


from theme_patch import set_palette, is_dark, PALETTES   # noqa: E402


def set_gen(name):
    """Cambia la carpeta de diagramas generados (gen oscura / gen_light clara)."""
    global GEN
    GEN = os.path.join(ASSETS, name)


def hexcol(name_or_hex, alpha=None):
    """Devuelve (r,g,b) o (r,g,b,a) a partir de un nombre del tema o '#RRGGBB'."""
    v = COL.get(name_or_hex, name_or_hex)
    v = v.lstrip("#")
    r, g, b = int(v[0:2], 16), int(v[2:4], 16), int(v[4:6], 16)
    if alpha is None:
        return (r, g, b)
    return (r, g, b, alpha)


def rgbname(name):
    """'22D3EE' -> RGBColor para python-pptx."""
    from pptx.dml.color import RGBColor
    v = COL.get(name, name).lstrip("#")
    return RGBColor.from_string(v.upper())
