#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tabla comparativa autótrofos vs heterótrofos, como imagen."""
import math, os
from PIL import Image, ImageDraw, ImageFont

OUT = os.path.join(os.path.dirname(__file__), "assets")
os.makedirs(OUT, exist_ok=True)
FD = "/usr/share/fonts/truetype/dejavu/"
def F(size, bold=False):
    return ImageFont.truetype(FD + ("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"), size)

VOSC = (27, 94, 32); V = (46, 125, 50)
CREMA = (247, 251, 243); BCO = (255, 255, 255)
TXT = (33, 45, 33); GRIS = (110, 110, 110)
VERDE_CL = (234, 243, 230); NAR = (230, 160, 40); AZUL = (21, 101, 192)

FILAS = [
    ("Definición",
     "Sintetizan su propia materia orgánica a partir de sustancias inorgánicas.",
     "No sintetizan su alimento; lo toman ya elaborado del medio."),
    ("Obtención del alimento",
     "Producen su alimento por fotosíntesis (plantas, algas) o quimiosíntesis (bacterias).",
     "Consumen a otros seres vivos, sus restos o sus productos."),
    ("Fuente de energía",
     "Luz solar (fotótrofos) o energía química de compuestos inorgánicos (quimiótrofos).",
     "Energía química almacenada en la materia orgánica que ingieren."),
    ("Materia prima",
     "CO₂, agua y sales minerales del ambiente.",
     "Carbohidratos, grasas y proteínas ya elaborados por otros organismos."),
    ("Estructuras implicadas",
     "Cloroplastos con clorofila, estomas, raíces y vasos conductores.",
     "Aparato digestivo, enzimas digestivas; hifas absortivas en los hongos."),
    ("Proceso característico",
     "Fotosíntesis: fase luminosa y ciclo de Calvin.",
     "Digestión, absorción y respiración celular."),
    ("Productos",
     "Glucosa y oxígeno; reservas de almidón, celulosa y aceites.",
     "CO₂, agua, urea y calor; energía para crecer y moverse."),
    ("Dependencia",
     "No dependen de otros organismos para alimentarse.",
     "Dependen de los autótrofos para obtener alimento y oxígeno."),
    ("Nivel trófico",
     "Productores: primer nivel de la cadena trófica.",
     "Consumidores y descomponedores: del segundo nivel en adelante."),
    ("Ciclo del carbono",
     "Fijan el CO₂ atmosférico: actúan como sumidero de carbono.",
     "Liberan CO₂ por la respiración y la descomposición."),
    ("Movilidad",
     "En su mayoría sésiles, fijos al sustrato.",
     "En su mayoría móviles, buscan alimento y refugio."),
    ("Ejemplos",
     "Plantas, algas, fitoplancton, cianobacterias.",
     "Animales, hongos, protozoarios, bacterias y el ser humano."),
    ("Importancia ecológica",
     "Base de las cadenas tróficas: producen O₂ y capturan CO₂.",
     "Regulan poblaciones, polinizan, dispersan semillas y reciclan nutrientes."),
]

W = 1750
MARG = 60
C0 = 330          # columna característica
C1 = (W - 2*MARG - C0) // 2
PAD = 16
F_CAR = F(24, True)
F_TXT = F(22)
LH = 28

img_tmp = Image.new("RGB", (10, 10))
dd = ImageDraw.Draw(img_tmp)

def wrap(s, font, maxw):
    out, cur = [], ""
    for w in s.split():
        t = (cur + " " + w).strip()
        if dd.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur: out.append(cur)
            cur = w
    if cur: out.append(cur)
    return out

# calcular líneas reales de cada celda
CELDAS = []
for car, a, b in FILAS:
    la = wrap(car, F_CAR, C0 - 2*PAD - 10)
    lb = wrap(a, F_TXT, C1 - 2*PAD)
    lc = wrap(b, F_TXT, C1 - 2*PAD)
    CELDAS.append((la, lb, lc))

alturas = []
for la, lb, lc in CELDAS:
    n = max(len(la), len(lb), len(lc))
    alturas.append(n * LH + 2*PAD + 14)

HEAD = 200
H = HEAD + 70 + sum(alturas) + 90 + 120
img = Image.new("RGB", (W, H), CREMA)
d = ImageDraw.Draw(img)

# encabezado superior
d.rectangle([0, 0, W, HEAD], fill=VOSC)
d.rectangle([0, HEAD-14, W, HEAD], fill=(38, 110, 42))
d.text((MARG, 46), "AUTÓTROFOS vs. HETERÓTROFOS", font=F(52, True), fill=BCO)
d.text((MARG, 116), "Comparación de sus características principales", font=F(28), fill=(198, 227, 190))
d.text((MARG, 158), "Biología  ·  Tabla comparativa", font=F(22, True), fill=(150, 200, 150))

# fila de encabezado de la tabla
y = HEAD + 40
x0 = MARG
xs = [x0, x0 + C0, x0 + C0 + C1]
cols = [C0, C1, C1]
hdr_txt = ["CARACTERÍSTICA", "ORGANISMOS AUTÓTROFOS", "ORGANISMOS HETERÓTROFOS"]
hdr_col = [VOSC, V, (120, 120, 120)]
for i in range(3):
    d.rounded_rectangle([xs[i], y, xs[i]+cols[i], y+64], radius=14, fill=hdr_col[i])
    fs = 22 if i == 0 else 20
    d.text((xs[i] + cols[i]//2, y+32), hdr_txt[i], font=F(fs, True), fill=BCO, anchor="mm")
y += 64

# filas
for k, ((la, lb, lc), hh) in enumerate(zip(CELDAS, alturas)):
    bg = BCO if k % 2 == 0 else VERDE_CL
    d.rectangle([x0, y, x0 + C0 + 2*C1, y + hh], fill=bg)
    d.line([(x0, y), (x0 + C0 + 2*C1, y)], fill=(205, 220, 200), width=2)
    d.line([(xs[1], y), (xs[1], y + hh)], fill=(205, 220, 200), width=2)
    d.line([(xs[2], y), (xs[2], y + hh)], fill=(205, 220, 200), width=2)
    d.rectangle([x0, y, x0+8, y+hh], fill=V)
    ty = y + (hh - len(la)*LH)//2
    for ln in la:
        d.text((x0 + 8 + PAD, ty), ln, font=F_CAR, fill=VOSC)
        ty += LH
    for i, lines in ((1, lb), (2, lc)):
        ty = y + (hh - len(lines)*LH)//2
        for ln in lines:
            d.text((xs[i] + PAD, ty), ln, font=F_TXT, fill=TXT)
            ty += LH
    y += hh

d.rectangle([x0, y, x0 + C0 + 2*C1, y+4], fill=VOSC)

# pie
y += 26
d.rounded_rectangle([MARG, y, W-MARG, y+96], radius=16, fill=(232, 245, 233), outline=V, width=3)
d.text((MARG+24, y+18), "En resumen:", font=F(24, True), fill=VOSC)
d.text((MARG+24, y+52),
       "Los autótrofos producen la materia orgánica y el oxígeno; los heterótrofos dependen de ellos para vivir.",
       font=F(22), fill=TXT)

d.rectangle([0, H-60, W, H], fill=VOSC)
d.text((W//2, H-30), "La fotosíntesis: base de la vida en la Tierra", font=F(24, True), fill=BCO, anchor="mm")

p = os.path.join(OUT, "tabla_comparativa.png")
img.save(p)
print("OK", p, img.size)
