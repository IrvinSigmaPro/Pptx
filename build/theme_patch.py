# -*- coding: utf-8 -*-
"""Paletas del tema: versión oscura (original) y versión clara (v2)."""
import os

PALETTES = {
    "dark": None,   # se usa COL tal como está definido arriba (valores por defecto)
    "light": {
        "bg":      "F5F8FC",
        "bg2":     "EAF0F8",
        "panel":   "FFFFFF",
        "panel2":  "E6EDF7",
        "card":    "FFFFFF",
        "card2":   "EDF3FA",
        "line":    "D3DEEB",
        "line2":   "AEC0D6",
        "txt":     "0D1A2B",
        "txt2":    "2C3E56",
        "txt3":    "61738C",
        "white":   "FFFFFF",
        "cyan":    "0E7C94",
        "orange":  "C2690A",
        "purple":  "6D46E0",
        "green":   "0E8A5F",
        "pink":    "C42B6B",
        "blue":    "1E5FD0",
        "red":     "C8322B",
        "yellow":  "9A7008",
        "teal":    "0C7C74",
        "indigo":  "4149C8",
    },
}
CURRENT = "dark"


def set_palette(name):
    """Cambia la paleta activa (modifica COL en sitio para todos los módulos)."""
    global CURRENT
    from theme import COL
    base = {
        "dark": {"bg": "0A101E", "bg2": "0D1526", "panel": "111C31", "panel2": "16233C",
                 "card": "131E33", "card2": "18253F", "line": "26334F", "line2": "3A4C71",
                 "txt": "EDF3FC", "txt2": "C0CDE2", "txt3": "8B9CBB", "white": "FFFFFF",
                 "cyan": "22D3EE", "orange": "F59E0B", "purple": "A78BFA", "green": "34D399",
                 "pink": "F472B6", "blue": "60A5FA", "red": "F87171", "yellow": "FDE047",
                 "teal": "2DD4BF", "indigo": "818CF8"},
        "light": PALETTES["light"],
    }[name]
    COL.update(base)
    CURRENT = name
    return name


def is_dark():
    return CURRENT == "dark"
