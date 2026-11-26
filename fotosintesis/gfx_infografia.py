#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Infografía vertical: participación de los organismos autótrofos en las cadenas tróficas."""
import math, os
from PIL import Image, ImageDraw, ImageFont

OUT = os.path.join(os.path.dirname(__file__), "assets")
os.makedirs(OUT, exist_ok=True)
FD = "/usr/share/fonts/truetype/dejavu/"
def F(size, bold=False):
    return ImageFont.truetype(FD + ("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"), size)

VOSC = (20, 70, 32); V = (46, 125, 50); VC = (129, 199, 132)
CREMA = (247, 251, 243); TXT = (26, 46, 26); GRIS = (97, 97, 97)
NAR = (245, 150, 30); AZUL = (21, 101, 192); ROJO = (198, 40, 40)
MORADO = (106, 27, 110); ROSA = (173, 20, 87); CAFE = (109, 76, 65)

W, H = 1240, 4210
img = Image.new("RGB", (W, H), CREMA)
d = ImageDraw.Draw(img)

def wrap(s, font, maxw):
    words, lines, cur = s.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines

def tc(xy, s, font, fill=TXT):
    d.text(xy, s, font=font, fill=fill, anchor="mm")

def card(y0, y1, num, titulo, color=VOSC, tsize=38):
    d.rounded_rectangle([60, y0, W-60, y1], radius=28, fill=(255, 255, 255), outline=color, width=4)
    d.ellipse([92, y0+26, 168, y0+102], fill=color)
    tc((130, y0+64), str(num), F(42, True), (255, 255, 255))
    d.text((192, y0+36), titulo, font=F(tsize, True), fill=color)
    return y0 + 122

def body(y, s, size=27, maxw=W-230, x=105, color=TXT):
    for ln in wrap(s, F(size), maxw):
        d.text((x, y), ln, font=F(size), fill=color)
        y += size + 13
    return y

def bullets(y, items, size=25, maxw=W-290, x=130):
    for it in items:
        lines = wrap(it, F(size), maxw)
        d.ellipse([x-26, y+9, x-14, y+21], fill=V)
        for ln in lines:
            d.text((x, y), ln, font=F(size), fill=TXT)
            y += size + 11
        y += 8
    return y

def hoja(cx, cy, s=1.0, color=V):
    d.ellipse([cx-52*s, cy-72*s, cx+52*s, cy+72*s], fill=color)
    d.line([(cx, cy+72*s), (cx, cy-72*s)], fill=(255, 255, 255), width=max(2, int(4*s)))
    d.line([(cx, cy+88*s), (cx, cy+120*s)], fill=VOSC, width=max(3, int(6*s)))

def sol_icono(cx, cy, r=42):
    for a in range(0, 360, 30):
        d.line([(cx+(r+7)*math.cos(math.radians(a)), cy+(r+7)*math.sin(math.radians(a))),
                (cx+(r+28)*math.cos(math.radians(a)), cy+(r+28)*math.sin(math.radians(a)))], fill=NAR, width=6)
    d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=NAR)
    tc((cx, cy), "SOL", F(21, True), (255, 255, 255))

def flecha(x0, x1, y, color=VOSC, w=5):
    d.line([(x0, y), (x1-12, y)], fill=color, width=w)
    d.polygon([(x1, y), (x1-14, y-7), (x1-14, y+7)], fill=color)

# ================================================================ encabezado
d.rectangle([0, 0, W, 340], fill=VOSC)
sol_icono(1115, 120, 42)
tc((560, 70), "LOS AUTÓTROFOS", F(58, True), (255, 255, 255))
tc((560, 152), "en las cadenas tróficas", F(40, True), (178, 223, 138))
tc((560, 212), "Los productores: la puerta de entrada de la energía", F(24), (206, 232, 190))
for i, c in enumerate([VC, (178, 223, 138), NAR, (255, 255, 255)]):
    d.rounded_rectangle([270 + i*150, 256, 270 + i*150 + 110, 268], radius=6, fill=c)
tc((560, 305), "BIOLOGÍA  ·  INFOGRAFÍA", F(21, True), (138, 190, 130))

# ================================================================ 1 cadena trófica
y = card(380, 720, 1, "¿Qué es una cadena trófica?")
y = body(y, "Es la secuencia por la que la materia y la energía pasan de un ser vivo a otro mediante la alimentación. Cada eslabón ocupa un nivel trófico.")
y += 8
d.rounded_rectangle([100, y, 1140, y+130], radius=18, fill=(232, 245, 233))
etas = [("SOL", NAR), ("PASTO", V), ("CONEJO", (216, 122, 24)), ("ZORRO", ROSA)]
x = 135
for i, (t, c) in enumerate(etas):
    d.ellipse([x, y+42, x+56, y+98], fill=c)
    tc((x+28, y+70), t[:1], F(26, True), (255, 255, 255))
    d.text((x+70, y+70), t, font=F(22, True), fill=c, anchor="lm")
    x += 70 + d.textlength(t, font=F(22, True))
    if i < 3:
        flecha(x+18, x+70, y+70, VOSC, 4)
        x += 88

# ================================================================ 2 autótrofos
y = card(750, 1250, 2, "¿Quiénes son los autótrofos?")
hoja(200, y+80, 0.7)
tc((200, y+195), "PLANTAS", F(23, True), VOSC)
tc((200, y+228), "bosques, pastos", F(20), GRIS)
for i in range(5):
    d.ellipse([360+i*34, y+25, 404+i*34, y+160], fill=VC, outline=VOSC, width=2)
tc((440, y+195), "ALGAS", F(23, True), VOSC)
tc((440, y+228), "marinas y dulces", F(20), GRIS)
for i in range(6):
    d.ellipse([610+i*22, y+40+i*4, 634+i*22, y+64+i*4], fill=(178, 223, 138), outline=V, width=2)
tc((690, y+195), "FITOPLANCTON", F(23, True), VOSC)
tc((690, y+228), "base de los océanos", F(20), GRIS)
bcx, bcy = 940, y+90
d.ellipse([bcx-52, bcy-52, bcx+52, bcy+52], fill=(255, 213, 179), outline=(200, 120, 40), width=3)
for a in range(0, 360, 45):
    d.line([(bcx+56*math.cos(math.radians(a)), bcy+56*math.sin(math.radians(a))),
            (bcx+74*math.cos(math.radians(a)), bcy+74*math.sin(math.radians(a)))], fill=(200, 120, 40), width=4)
tc((940, y+195), "CIANOBACTERIAS", F(23, True), VOSC)
tc((940, y+228), "agua y suelo", F(20), GRIS)
y = body(y+265, "Todos fabrican su propio alimento a partir de materia inorgánica: son los PRODUCTORES del ecosistema.", size=25)

# ================================================================ 3 niveles tróficos
y = card(1280, 1760, 3, "Los niveles tróficos")
niveles = [
    ("PRODUCTORES", "autótrofos · nivel 1", VOSC),
    ("HERBÍVOROS", "consumidores 1°", (216, 122, 24)),
    ("CARNÍVOROS", "consumidores 2°", ROSA),
    ("SUPERDEPRED.", "consumidores 3°", MORADO),
    ("DESCOMPONED.", "hongos y bacterias", CAFE),
]
bw, gap = 190, 32
total = 5*bw + 4*gap
x0 = (W - total) // 2
for i, (t, sub, c) in enumerate(niveles):
    x = x0 + i*(bw+gap)
    d.rounded_rectangle([x, y, x+bw, y+180], radius=16, fill=(255, 255, 255), outline=c, width=4)
    d.rounded_rectangle([x, y, x+bw, y+44], radius=16, fill=c)
    d.rectangle([x, y+30, x+bw, y+44], fill=c)
    fs = 16
    while d.textlength(t, font=F(fs, True)) > bw - 14 and fs > 10:
        fs -= 1
    tc((x+bw//2, y+23), t, F(fs, True), (255, 255, 255))
    for j, ln in enumerate(wrap(sub, F(18), bw-20)):
        d.text((x+bw//2, y+78+j*24), ln, font=F(18), fill=GRIS, anchor="ma")
    tc((x+bw//2, y+148), str(i+1) if i < 4 else "♻", F(30, True), c)
    if i < 4:
        flecha(x+bw+3, x+bw+gap-3, y+90, VOSC, 4)
y = body(y+205, "Los autótrofos forman el primer nivel: sin ellos, los demás niveles no tendrían de dónde obtener energía.", size=25)

# ================================================================ 4 papel clave
y = card(1790, 2180, 4, "¿Cómo participan los autótrofos?")
y = body(y, "Transforman materia inorgánica en materia orgánica rica en energía. Esa es su función como productores:", size=25)
y += 12
cw, aw = 300, 46
x0 = (W - (3*cw + 2*aw)) // 2
d.rounded_rectangle([x0, y, x0+cw, y+120], radius=16, fill=(236, 244, 236), outline=GRIS, width=3)
tc((x0+cw//2, y+42), "MATERIA INORGÁNICA", F(21, True), GRIS)
tc((x0+cw//2, y+80), "CO₂ + H₂O + luz", F(22, True), TXT)
flecha(x0+cw+4, x0+cw+aw-4, y+60, NAR, 5)
x1 = x0 + cw + aw
d.rounded_rectangle([x1, y, x1+cw, y+120], radius=16, fill=(255, 248, 220), outline=NAR, width=4)
tc((x1+cw//2, y+42), "FOTOSÍNTESIS", F(23, True), (170, 110, 0))
tc((x1+cw//2, y+80), "en el cloroplasto", F(21), GRIS)
flecha(x1+cw+4, x1+cw+aw-4, y+60, NAR, 5)
x2 = x1 + cw + aw
d.rounded_rectangle([x2, y, x2+cw, y+120], radius=16, fill=(232, 245, 233), outline=V, width=4)
tc((x2+cw//2, y+42), "MATERIA ORGÁNICA", F(21, True), VOSC)
tc((x2+cw//2, y+80), "glucosa + O₂", F(22, True), TXT)

# ================================================================ 5 flujo de energía
y = card(2210, 2730, 5, "Flujo de energía: la regla del 10 %")
cx = 400
base_y, lvl_h = y + 265, 62
for i, (t, pct, col) in enumerate([
        ("PRODUCTORES", "100 %", (27, 94, 32)),
        ("HERBÍVOROS", "10 %", (56, 142, 60)),
        ("CARNÍVOROS", "1 %", (129, 199, 132)),
        ("SUPERDEPREDADORES", "0,1 %", (197, 225, 194))]):
    hw_b = 190 - i * 42
    hw_t = 190 - (i + 1) * 42
    yb, yt = base_y - i*lvl_h, base_y - (i+1)*lvl_h
    d.polygon([(cx-hw_b, yb), (cx+hw_b, yb), (cx+hw_t, yt), (cx-hw_t, yt)], fill=col,
              outline=(255, 255, 255), width=3)
    tc((cx, (yb+yt)//2), f"{pct}", F(24, True), (255, 255, 255) if i < 2 else VOSC)
# etiquetas a la derecha
lx = cx + 230
for i, (t, pct, col) in enumerate([
        ("PRODUCTORES", "autótrofos", (27, 94, 32)),
        ("HERBÍVOROS", "consumidores 1°", (56, 142, 60)),
        ("CARNÍVOROS", "consumidores 2°", (129, 199, 132)),
        ("SUPERDEPRED.", "consumidores 3°", (197, 225, 194))]):
    yy = base_y - i*lvl_h - lvl_h//2
    d.ellipse([lx-14, yy-14, lx+14, yy+14], fill=col, outline=VOSC if i > 1 else None, width=2)
    d.text((lx+28, yy-22), t, font=F(22, True), fill=VOSC)
    d.text((lx+28, yy+4), pct, font=F(20), fill=GRIS)
yy = base_y + 22
d.line([(90, yy), (1150, yy)], fill=(200, 200, 200), width=2)
body(yy+16, "En cada salto se pierde cerca del 90 % de la energía como calor: por eso las pirámides tienen pocos depredadores y muchas plantas.", size=24)

# ================================================================ 6 ejemplos
y = card(2760, 3350, 6, "Ejemplos de cadenas tróficas")
ejemplos = [
    ("TERRESTRE", ["Pasto", "Conejo", "Zorro", "Bacterias"], (46, 125, 50)),
    ("ACUÁTICA", ["Fitoplancton", "Zooplanct.", "Pez", "Tiburón"], (21, 101, 192)),
    ("CHAPARRAL", ["Hierba", "Saltamontes", "Rana", "Serpiente"], (198, 40, 40)),
]
cw2, aw2 = 205, 42
x0 = (W - (4*cw2 + 3*aw2)) // 2
for nombre, eslabones, col in ejemplos:
    d.text((100, y+2), nombre, font=F(22, True), fill=col)
    y += 40
    for i, e in enumerate(eslabones):
        x = x0 + i*(cw2+aw2)
        d.rounded_rectangle([x, y, x+cw2, y+64], radius=30, fill=(255, 255, 255), outline=col, width=3)
        tc((x+cw2//2, y+32), e, F(21, True), col)
        if i < 3:
            flecha(x+cw2+4, x+cw2+aw2-4, y+32, col, 4)
    y += 88
y = body(y-4, "En todas, el primer eslabón es un organismo autótrofo: es el único que introduce energía nueva al ecosistema.", size=25)

# ================================================================ 7 red trófica / importancia
y = card(3380, 3790, 7, "De la cadena a la red trófica")
y = body(y, "En la naturaleza las cadenas se entrecruzan y forman una red trófica: un mismo organismo puede ocupar varios niveles. Los autótrofos son siempre la base de esa red.", size=25)
y += 6
d.rounded_rectangle([100, y, 1140, y+132], radius=18, fill=(232, 245, 233))
d.text((120, y+18), "Si desaparecen los productores…", font=F(23, True), fill=ROJO)
items = ["los herbívoros se quedan sin alimento",
         "se derrumba toda la cadena",
         "el oxígeno atmosférico disminuye"]
for i, it in enumerate(items):
    d.text((140, y+52 + i*26), "• " + it, font=F(18), fill=TXT)

# ================================================================ 8 conclusión
y = card(3820, 4140, 8, "Conclusión")
y = body(y, "Los autótrofos son los productores del ecosistema: capturan la energía del Sol y la convierten en alimento disponible para todos los demás seres vivos. Su participación en las cadenas tróficas hace posible la vida tal como la conocemos.", size=26)

# ================================================================ pie
d.rectangle([0, H-110, W, H], fill=VOSC)
tc((620, H-55), "Los autótrofos: la puerta de entrada de la energía a los ecosistemas", F(27, True), (255, 255, 255))

p = os.path.join(OUT, "infografia.png")
img.save(p)
print("OK", p, img.size)
