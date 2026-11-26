#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Infografía vertical estilo Canva: autótrofos en las cadenas tróficas."""
import math, os
from PIL import Image, ImageDraw, ImageFont

OUT = os.path.join(os.path.dirname(__file__), "assets")
os.makedirs(OUT, exist_ok=True)
FD = "/usr/share/fonts/truetype/dejavu/"
def F(size, bold=False):
    return ImageFont.truetype(FD + ("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"), size)

W, H = 1240, 2770
VOSC = (27, 94, 32); V = (46, 125, 50); VC = (102, 187, 106)
CREMA = (247, 251, 243); TXT = (26, 46, 26)
GRIS = (97, 97, 97); NAR = (249, 168, 37); AZUL = (21, 101, 192)
ROJO = (198, 40, 40); MORADO = (106, 27, 110); ROSA = (173, 20, 87)

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
    d.ellipse([95, y0+28, 175, y0+108], fill=color)
    tc((135, y0+68), str(num), F(44, True), (255, 255, 255))
    d.text((200, y0+40), titulo, font=F(tsize, True), fill=color)
    return y0 + 125

def body(y, s, size=28, maxw=W-220, x=110, color=TXT):
    for ln in wrap(s, F(size), maxw):
        d.text((x, y), ln, font=F(size), fill=color)
        y += size + 12
    return y

def sol(cx, cy, r=52):
    for a in range(0, 360, 30):
        d.line([(cx+(r+8)*math.cos(math.radians(a)), cy+(r+8)*math.sin(math.radians(a))),
                (cx+(r+34)*math.cos(math.radians(a)), cy+(r+34)*math.sin(math.radians(a)))], fill=NAR, width=7)
    d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=NAR)
    tc((cx, cy), "SOL", F(26, True), (255, 255, 255))

def hoja(cx, cy, s=1.0, color=V):
    d.ellipse([cx-55*s, cy-75*s, cx+55*s, cy+75*s], fill=color)
    d.line([(cx, cy+75*s), (cx, cy-75*s)], fill=(255, 255, 255), width=max(2, int(4*s)))
    d.line([(cx, cy+95*s), (cx, cy+130*s)], fill=VOSC, width=max(3, int(6*s)))

def gota(cx, cy, s=1.0):
    d.ellipse([cx-45*s, cy-10*s, cx+45*s, cy+80*s], fill=AZUL)
    d.polygon([(cx-45*s, cy+5*s), (cx+45*s, cy+5*s), (cx, cy-75*s)], fill=AZUL)
    d.ellipse([cx-22*s, cy+15*s, cx-2*s, cy+45*s], fill=(187, 222, 251))

def nube(cx, cy, txt, color):
    d.ellipse([cx-70, cy-35, cx+70, cy+35], fill=color)
    d.ellipse([cx-45, cy-60, cx+15, cy+10], fill=color)
    d.ellipse([cx-5, cy-55, cx+55, cy+10], fill=color)
    tc((cx, cy+2), txt, F(30, True), (255, 255, 255))

# ---------------------------------------------------------------- encabezado
d.rectangle([0, 0, W, 330], fill=VOSC)
sol(1120, 150, 50)
tc((560, 100), "FOTOSÍNTESIS", F(78, True), (255, 255, 255))
tc((560, 180), "La participación de los organismos autótrofos", F(32, True), (200, 230, 201))
tc((560, 228), "en las cadenas tróficas", F(32, True), (200, 230, 201))
tc((560, 290), "La energía del Sol convertida en vida", F(26), (165, 214, 167))

# ---------------------------------------------------------------- 1 ¿Qué es?
y = card(370, 640, 1, "¿Qué es la fotosíntesis?")
y = body(y, "Proceso por el que las plantas, las algas y algunas bacterias convierten la luz del Sol en energía química (glucosa).")
tc((620, y+30), "6 CO₂ + 6 H₂O + luz  →  C₆H₁₂O₆ + 6 O₂", F(34, True), VOSC)

# ---------------------------------------------------------------- 2 ¿Quiénes?
y = card(680, 1090, 2, "¿Quiénes la realizan? (autótrofos)")
hoja(250, y+95, 0.75)
tc((250, y+250), "PLANTAS", F(26, True), VOSC)
for i in range(5):
    d.ellipse([470+i*38, y+40, 520+i*38, y+190], fill=VC, outline=VOSC, width=2)
tc((565, y+250), "ALGAS", F(26, True), VOSC)
bcx, bcy = 860, y+115
d.ellipse([bcx-60, bcy-60, bcx+60, bcy+60], fill=(255, 213, 179), outline=(200, 120, 40), width=3)
for a in range(0, 360, 45):
    d.line([(bcx+64*math.cos(math.radians(a)), bcy+64*math.sin(math.radians(a))),
            (bcx+84*math.cos(math.radians(a)), bcy+84*math.sin(math.radians(a)))], fill=(200, 120, 40), width=4)
tc((860, y+250), "CIANOBACTERIAS", F(26, True), VOSC)

# ---------------------------------------------------------------- 3 Elementos
y = card(1130, 1460, 3, "Elementos necesarios")
sol(200, y+80, 42)
tc((200, y+170), "LUZ SOLAR", F(24, True), VOSC)
gota(460, y+75, 0.85)
tc((460, y+170), "AGUA (H₂O)", F(24, True), VOSC)
nube(720, y+80, "CO₂", (120, 120, 120))
tc((720, y+170), "DIÓXIDO DE CARBONO", F(24, True), VOSC)
d.ellipse([960, y+25, 1060, y+125], fill=V)
tc((1010, y+75), "Cl", F(36, True), (255, 255, 255))
tc((1010, y+170), "CLOROFILA", F(24, True), VOSC)

# ---------------------------------------------------------------- 4 Etapas
y = card(1500, 1830, 4, "Sus dos etapas")
d.rounded_rectangle([110, y, 580, y+190], radius=20, fill=(255, 248, 220), outline=NAR, width=3)
tc((345, y+40), "FASE LUMINOSA", F(30, True), (180, 120, 0))
tc((345, y+85), "En los tilacoides", F(24), GRIS)
tc((345, y+125), "Produce ATP, NADPH", F(24), TXT)
tc((345, y+160), "y libera O₂", F(24), TXT)
d.rounded_rectangle([660, y, 1130, y+190], radius=20, fill=(243, 229, 245), outline=MORADO, width=3)
tc((895, y+40), "CICLO DE CALVIN", F(30, True), MORADO)
tc((895, y+85), "En el estroma", F(24), GRIS)
tc((895, y+125), "Fija el CO₂ y forma", F(24), TXT)
tc((895, y+160), "glucosa", F(24), TXT)

# ---------------------------------------------------------------- 5 Productos
y = card(1870, 2160, 5, "Productos")
d.rounded_rectangle([110, y, 580, y+150], radius=20, fill=(255, 243, 224), outline=NAR, width=3)
tc((345, y+50), "GLUCOSA", F(36, True), (180, 120, 0))
tc((345, y+100), "energía química", F(24), GRIS)
d.rounded_rectangle([660, y, 1130, y+150], radius=20, fill=(227, 242, 253), outline=AZUL, width=3)
tc((895, y+50), "OXÍGENO (O₂)", F(36, True), AZUL)
tc((895, y+100), "se libera al aire", F(24), GRIS)

# ---------------------------------------------------------------- 6 Cadena trófica
y = card(2200, 2620, 6, "Transferencia de energía (cadena trófica)", color=ROJO, tsize=34)
niveles = [
    ("PRODUCTORES", "plantas y algas", VOSC, "100%"),
    ("HERBÍVOROS", "conejo, venado", (230, 126, 34), "10%"),
    ("CARNÍVOROS", "zorro, águila", ROSA, "1%"),
    ("DESCOMP.", "hongos, bacterias", MORADO, "0,1%"),
]
x = 110
for i, (t, sub, col, pct) in enumerate(niveles):
    d.rounded_rectangle([x, y, x+225, y+190], radius=18, fill=(255, 255, 255), outline=col, width=4)
    tc((x+112, y+45), t, F(24, True), col)
    tc((x+112, y+85), sub, F(20), TXT)
    tc((x+112, y+140), "≈ " + pct, F(26, True), GRIS)
    if i < 3:
        d.line([(x+232, y+95), (x+258, y+95)], fill=VOSC, width=5)
        d.polygon([(x+258, y+95), (x+246, y+87), (x+246, y+103)], fill=VOSC)
    x += 265
y += 225
body(y, "Los autótrofos son la puerta de entrada de la energía: sin ellos no hay alimento para ningún otro ser vivo.", size=24)

# ---------------------------------------------------------------- pie
d.rectangle([0, H-110, W, H], fill=VOSC)
tc((620, H-55), "La fotosíntesis: la energía del Sol convertida en vida", F(30, True), (255, 255, 255))

p = os.path.join(OUT, "infografia.png")
img.save(p)
print("OK", p, img.size)
