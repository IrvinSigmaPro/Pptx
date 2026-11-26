#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera los diagramas del reporte de Fotosíntesis con Pillow."""
import math, os
from PIL import Image, ImageDraw, ImageFont

OUT = os.path.join(os.path.dirname(__file__), "assets")
os.makedirs(OUT, exist_ok=True)

FD = "/usr/share/fonts/truetype/dejavu/"
def F(size, bold=False):
    return ImageFont.truetype(FD + ("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"), size)

VERDE_OSC = (27, 94, 32)
VERDE = (46, 125, 50)
VERDE_CLARO = (102, 187, 106)
VERDE_PALIDO = (200, 230, 201)
CREMA = (247, 251, 243)
TEXTO = (26, 46, 26)
NARANJA = (249, 168, 37)
AZUL = (21, 101, 192)
GRIS = (97, 97, 97)

def save(img, name):
    p = os.path.join(OUT, name)
    img.save(p)
    print("OK", p, img.size)
    return p

def rounded(draw, box, r, fill=None, outline=None, width=1):
    draw.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)

def text_center(draw, xy, s, font, fill=TEXTO):
    draw.text(xy, s, font=font, fill=fill, anchor="mm")

def wrap(draw, s, font, maxw):
    words, lines, cur = s.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines

def arrow(draw, p1, p2, color=VERDE, width=4, head=14):
    draw.line([p1, p2], fill=color, width=width)
    ang = math.atan2(p2[1]-p1[1], p2[0]-p1[0])
    for da in (math.radians(150), math.radians(-150)):
        draw.line([p2, (p2[0]+head*math.cos(ang+da), p2[1]+head*math.sin(ang+da))], fill=color, width=width)

# ---------------------------------------------------------------- cloroplasto
def cloroplasto():
    W, H = 1700, 1050
    img = Image.new("RGB", (W, H), (255, 255, 255))
    d = ImageDraw.Draw(img)
    cx, cy, rx, ry = 850, 520, 560, 330
    # sombra
    d.ellipse([cx-rx+18, cy-ry+26, cx+rx+18, cy+ry+26], fill=(220, 230, 215))
    # membrana externa / interna
    d.ellipse([cx-rx, cy-ry, cx+rx, cy+ry], fill=(232, 245, 224), outline=VERDE_OSC, width=6)
    d.ellipse([cx-rx+26, cy-ry+26, cx+rx-26, cy+ry-26], fill=(247, 251, 243), outline=VERDE, width=4)
    # estroma (fondo)
    d.ellipse([cx-rx+34, cy-ry+34, cx+rx-34, cy+ry-34], fill=(241, 248, 233))
    # grana: pilas de tilacoides
    grana = [(560, 420), (760, 560), (980, 430), (1120, 580), (680, 660), (900, 680)]
    for gx, gy in grana:
        for i in range(5):
            y = gy - 34 + i*17
            d.ellipse([gx-95, y-13, gx+95, y+13], fill=(165, 214, 167), outline=VERDE_OSC, width=2)
    # lamelas (conexiones)
    for (x1, y1), (x2, y2) in [((560,420),(760,560)), ((760,560),(980,430)), ((980,430),(1120,580)), ((760,560),(680,660)), ((980,430),(900,680))]:
        d.line([(x1, y1), (x2, y2)], fill=VERDE_CLARO, width=10)
    # almidón, ADN, ribosomas
    for (x, y, r) in [(640, 520, 26), (1050, 520, 22), (850, 470, 18)]:
        d.ellipse([x-r, y-r, x+r, y+r], fill=(255, 241, 180), outline=(200, 160, 40), width=2)
    d.ellipse([830, 610, 880, 640], fill=(187, 222, 251), outline=AZUL, width=2)
    d.line([(855, 625), (920, 600)], fill=AZUL, width=3)
    for i in range(14):
        a = i/14*2*math.pi
        x = cx + (rx-70)*math.cos(a)*0.92; y = cy + (ry-60)*math.sin(a)*0.92
        d.ellipse([x-9, y-9, x+9, y+9], fill=(255, 213, 179), outline=(200, 120, 40), width=1)
    # etiquetas con líneas guía
    labels = [
        ("Membrana externa", (cx-rx, cy-120), (180, 150)),
        ("Membrana interna", (cx-rx+30, cy+40), (180, 300)),
        ("Espacio intermembrana", (cx-260, cy-ry+28), (430, 90)),
        ("Tilacoide", (560, 386), (150, 250)),
        ("Grana (plural: granos)", (980, 396), (1250, 200)),
        ("Lamela", (860, 490), (1300, 380)),
        ("Estroma", (700, 760), (300, 900)),
        ("Almidón", (640, 494), (240, 620)),
        ("ADN circular", (855, 625), (1150, 820)),
        ("Ribosomas", (cx+430, cy-180), (1450, 560)),
    ]
    for txt, (px, py), (lx, ly) in labels:
        d.line([(px, py), (lx, ly)], fill=GRIS, width=2)
        d.ellipse([px-5, py-5, px+5, py+5], fill=GRIS)
        f = F(30, True)
        lines = wrap(d, txt, f, 330)
        for i, ln in enumerate(lines):
            d.text((lx, ly + i*36), ln, font=f, fill=TEXTO)
    text_center(d, (850, 60), "Estructura del cloroplasto (vista en corte)", F(44, True), VERDE_OSC)
    text_center(d, (850, 1000), "Reactor celular de la fotosíntesis: fase luminosa en tilacoides y ciclo de Calvin en el estroma.", F(28), GRIS)
    return save(img, "cloroplasto.png")

# ---------------------------------------------------------------- correlación
def correlacion():
    W, H = 1700, 1050
    img = Image.new("RGB", (W, H), (255, 255, 255))
    d = ImageDraw.Draw(img)
    text_center(d, (850, 55), "Diagrama de correlación: la fotosíntesis", F(42, True), VERDE_OSC)
    cx, cy = 850, 540
    # caja central
    rounded(d, [cx-230, cy-85, cx+230, cy+85], 28, fill=VERDE_OSC)
    text_center(d, (cx, cy-28), "FOTOSÍNTESIS", F(46, True), (255, 255, 255))
    text_center(d, (cx, cy+28), "proceso autotrófico", F(28), (220, 240, 220))
    ramas = [
        ("Energía solar\n(luz)", (300, 220), NARANJA),
        ("Agua (H₂O)\nraíz → hoja", (300, 470), AZUL),
        ("Dióxido de carbono\n(CO₂) del aire", (300, 720), (120, 120, 120)),
        ("Clorofila y\ncloroplasto", (300, 920), VERDE),
        ("Fase luminosa\n(tilacoide)", (1400, 220), (230, 126, 34)),
        ("Ciclo de Calvin\n(estroma)", (1400, 470), (106, 27, 110)),
        ("Glucosa (energía\nquímica)", (1400, 720), (173, 20, 87)),
        ("Oxígeno (O₂)\nliberado", (1400, 920), (21, 101, 192)),
    ]
    for txt, (bx, by), col in ramas:
        rounded(d, [bx-215, by-72, bx+215, by+72], 22, fill=(255, 255, 255), outline=col, width=5)
        for i, ln in enumerate(txt.split("\n")):
            text_center(d, (bx, by-24+i*46), ln, F(32, True), TEXTO)
        arrow(d, (cx + (230 if bx > cx else -230), cy), (bx + (-215 if bx > cx else 215), by), color=col, width=4)
    text_center(d, (850, 1005), "Correlación: sin luz, agua, CO₂ y clorofila no hay producción de glucosa ni de oxígeno.", F(28), GRIS)
    return save(img, "correlacion.png")

# ---------------------------------------------------------------- fase luminosa
def fase_luminosa():
    W, H = 1700, 1050
    img = Image.new("RGB", (W, H), (255, 255, 255))
    d = ImageDraw.Draw(img)
    text_center(d, (850, 55), "Fase luminosa (fotoquímica) — membrana del tilacoide", F(40, True), VERDE_OSC)
    # membrana
    d.rectangle([120, 300, 1580, 760], fill=(255, 248, 220), outline=NARANJA, width=5)
    text_center(d, (850, 335), "MEMBRANA DEL TILACOIDE", F(30, True), (180, 120, 0))
    text_center(d, (850, 725), "LUMEN (interior)", F(28, True), (180, 120, 0))
    # sol
    sx, sy = 250, 180
    for a in range(0, 360, 30):
        x2 = sx + 95*math.cos(math.radians(a)); y2 = sy + 95*math.sin(math.radians(a))
        d.line([(sx+55*math.cos(math.radians(a)), sy+55*math.sin(math.radians(a))), (x2, y2)], fill=NARANJA, width=6)
    d.ellipse([sx-55, sy-55, sx+55, sy+55], fill=NARANJA)
    text_center(d, (sx, sy), "LUZ", F(30, True), (255, 255, 255))
    # complejos
    def complejo(x, nombre, color):
        d.rectangle([x-100, 470, x+100, 590], fill=color, outline=VERDE_OSC, width=3)
        for i, ln in enumerate(nombre.split("\n")):
            text_center(d, (x, 515+i*34), ln, F(24, True), (255, 255, 255))
    complejo(420, "FOTOSISTEMA II", (230, 126, 34))
    complejo(760, "CITOCROMO\nb₆f", (106, 27, 110))
    complejo(1100, "FOTOSISTEMA I", (21, 101, 192))
    # ATP sintasa
    d.ellipse([1330, 430, 1470, 570], fill=(173, 20, 87))
    text_center(d, (1400, 485), "ATP", F(28, True), (255, 255, 255))
    text_center(d, (1400, 520), "SINTASA", F(24, True), (255, 255, 255))
    # flujo de electrones
    arrow(d, (505, 530), (675, 530), color=(173, 20, 87), width=6)
    arrow(d, (845, 530), (1015, 530), color=(173, 20, 87), width=6)
    # H2O -> O2
    rounded(d, [180, 800, 520, 920], 18, fill=(227, 242, 253), outline=AZUL, width=4)
    text_center(d, (350, 845), "2 H₂O → O₂ + 4 H⁺ + 4 e⁻", F(30, True), AZUL)
    text_center(d, (350, 885), "fotólisis del agua", F(26), GRIS)
    arrow(d, (420, 590), (420, 800), color=AZUL, width=5)
    # productos
    rounded(d, [1180, 800, 1580, 920], 18, fill=(232, 245, 224), outline=VERDE_OSC, width=4)
    text_center(d, (1380, 845), "ATP + NADPH", F(34, True), VERDE_OSC)
    text_center(d, (1380, 885), "energía para el ciclo de Calvin", F(25), GRIS)
    arrow(d, (1400, 570), (1400, 800), color=VERDE_OSC, width=5)
    # H+ gradiente
    for x in (300, 500, 700, 900, 1100, 1300):
        text_center(d, (x, 680), "H⁺", F(30, True), (180, 120, 0))
    text_center(d, (850, 1005), "La luz excita la clorofila: se libera O₂, se acumulan H⁺ y se producen ATP y NADPH.", F(28), GRIS)
    return save(img, "fase_luminosa.png")

# ---------------------------------------------------------------- ciclo de Calvin
def calvin():
    W, H = 1700, 1050
    img = Image.new("RGB", (W, H), (255, 255, 255))
    d = ImageDraw.Draw(img)
    text_center(d, (850, 55), "Ciclo de Calvin (fase oscura) — en el estroma", F(40, True), VERDE_OSC)
    cx, cy, R = 850, 540, 300
    d.ellipse([cx-R, cy-R, cx+R, cy+R], outline=VERDE, width=6)
    d.ellipse([cx-R+14, cy-R+14, cx+R-14, cy+R-14], outline=VERDE_CLARO, width=2)
    pasos = [
        ("1. FIJACIÓN\nCO₂ + RuBP —RuBisCO→\n3-PGA", (cx, cy-R), VERDE_OSC),
        ("2. REDUCCIÓN\n3-PGA → G3P\n(usa ATP + NADPH)", (cx+R, cy), (230, 126, 34)),
        ("3. SALIDA\nG3P → glucosa,\nalmidón y celulosa", (cx, cy+R), (173, 20, 87)),
        ("4. REGENERACIÓN\nG3P → RuBP\n(usa ATP)", (cx-R, cy), (106, 27, 110)),
    ]
    for txt, (bx, by), col in pasos:
        rounded(d, [bx-230, by-78, bx+230, by+78], 22, fill=(255, 255, 255), outline=col, width=5)
        for i, ln in enumerate(txt.split("\n")):
            text_center(d, (bx, by-52+i*42), ln, F(29, True), TEXTO)
    # flechas circulares
    for a0 in (200, 290, 20, 110):
        a1 = a0 + 55
        p1 = (cx + (R-40)*math.cos(math.radians(a0)), cy + (R-40)*math.sin(math.radians(a0)))
        p2 = (cx + (R-40)*math.cos(math.radians(a1)), cy + (R-40)*math.sin(math.radians(a1)))
        arrow(d, p1, p2, color=VERDE, width=5)
    text_center(d, (cx, cy-30), "CICLO DE", F(40, True), VERDE_OSC)
    text_center(d, (cx, cy+20), "CALVIN", F(40, True), VERDE_OSC)
    text_center(d, (cx, cy+70), "no necesita luz directa,", F(26), GRIS)
    text_center(d, (cx, cy+105), "pero sí ATP y NADPH", F(26), GRIS)
    text_center(d, (850, 1005), "Por cada 3 CO₂ fijados se produce 1 G3P; 6 G3P forman 1 glucosa.", F(28), GRIS)
    return save(img, "calvin.png")

# ---------------------------------------------------------------- gases CO2/O2
def gases():
    W, H = 1700, 1050
    img = Image.new("RGB", (W, H), (255, 255, 255))
    d = ImageDraw.Draw(img)
    text_center(d, (850, 55), "Participación del CO₂ y del O₂ en la fotosíntesis", F(40, True), VERDE_OSC)
    # hoja
    d.ellipse([450, 250, 1250, 800], fill=(232, 245, 224), outline=VERDE_OSC, width=6)
    d.line([(850, 280), (850, 770)], fill=VERDE, width=6)
    for i in range(6):
        y = 340 + i*70
        d.line([(850, y), (600, y-40)], fill=VERDE_CLARO, width=4)
        d.line([(850, y), (1100, y-40)], fill=VERDE_CLARO, width=4)
    text_center(d, (850, 525), "HOJA", F(44, True), VERDE_OSC)
    text_center(d, (850, 575), "cloroplastos", F(30), GRIS)
    # estomas
    for (x, y) in [(520, 700), (1180, 700)]:
        d.ellipse([x-45, y-18, x+45, y+18], fill=(255, 255, 255), outline=VERDE_OSC, width=3)
    text_center(d, (520, 760), "estoma", F(24), GRIS)
    text_center(d, (1180, 760), "estoma", F(24), GRIS)
    # CO2 entrada
    rounded(d, [80, 180, 400, 300], 18, fill=(245, 245, 245), outline=(120, 120, 120), width=4)
    text_center(d, (240, 225), "CO₂", F(44, True), (80, 80, 80))
    text_center(d, (240, 265), "entra del aire", F(26), GRIS)
    arrow(d, (400, 240), (520, 680), color=(120, 120, 120), width=6)
    # O2 salida
    rounded(d, [1300, 180, 1620, 300], 18, fill=(227, 242, 253), outline=AZUL, width=4)
    text_center(d, (1460, 225), "O₂", F(44, True), AZUL)
    text_center(d, (1460, 265), "sale a la atmósfera", F(26), GRIS)
    arrow(d, (1180, 680), (1300, 240), color=AZUL, width=6)
    # agua
    rounded(d, [80, 820, 400, 940], 18, fill=(227, 242, 253), outline=AZUL, width=4)
    text_center(d, (240, 865), "H₂O", F(40, True), AZUL)
    text_center(d, (240, 905), "sube de la raíz", F(26), GRIS)
    arrow(d, (400, 880), (560, 760), color=AZUL, width=6)
    # glucosa
    rounded(d, [1300, 820, 1620, 940], 18, fill=(255, 243, 224), outline=NARANJA, width=4)
    text_center(d, (1460, 865), "GLUCOSA", F(36, True), (180, 120, 0))
    text_center(d, (1460, 905), "energía almacenada", F(26), GRIS)
    arrow(d, (1140, 760), (1300, 880), color=NARANJA, width=6)
    text_center(d, (850, 1005), "6 CO₂ + 6 H₂O + luz → C₆H₁₂O₆ + 6 O₂  (ecuación general)", F(30, True), VERDE_OSC)
    return save(img, "gases.png")

# ---------------------------------------------------------------- cadena trófica
def cadena():
    W, H = 1700, 1050
    img = Image.new("RGB", (W, H), (255, 255, 255))
    d = ImageDraw.Draw(img)
    text_center(d, (850, 55), "Infografía: los autótrofos en las cadenas tróficas", F(40, True), VERDE_OSC)
    # sol
    sx, sy = 850, 200
    for a in range(0, 360, 30):
        d.line([(sx+60*math.cos(math.radians(a)), sy+60*math.sin(math.radians(a))),
                (sx+105*math.cos(math.radians(a)), sy+105*math.sin(math.radians(a)))], fill=NARANJA, width=6)
    d.ellipse([sx-60, sy-60, sx+60, sy+60], fill=NARANJA)
    text_center(d, (sx, sy), "SOL", F(30, True), (255, 255, 255))
    niveles = [
        ("PRODUCTORES\n(autótrofos)", "plantas, algas,\ncianobacterias", VERDE_OSC, 100),
        ("HERBÍVOROS\n(consumidores 1°)", "conejo, venado,\ninsectos", (230, 126, 34), 10),
        ("CARNÍVOROS\n(consumidores 2°)", "zorro, águila,\nserpiente", (173, 20, 87), 1),
        ("DESCOMP.\n(hongos y bacterias)", "reciclan nutrientes\ny devuelven CO₂", (106, 27, 110), 0.1),
    ]
    x0, y0, w, h, gap = 120, 360, 340, 230, 60
    for i, (t, sub, col, pct) in enumerate(niveles):
        x = x0 + i*(w+gap)
        rounded(d, [x, y0, x+w, y0+h], 24, fill=(255, 255, 255), outline=col, width=6)
        for j, ln in enumerate(t.split("\n")):
            text_center(d, (x+w/2, y0+55+j*42), ln, F(30, True), col)
        for j, ln in enumerate(sub.split("\n")):
            text_center(d, (x+w/2, y0+150+j*36), ln, F(26), TEXTO)
        text_center(d, (x+w/2, y0+h+35), f"≈ {pct}% de la energía", F(24, True), GRIS)
        if i < len(niveles)-1:
            arrow(d, (x+w+8, y0+h/2), (x+w+gap-8, y0+h/2), color=VERDE_OSC, width=6)
            text_center(d, (x+w+gap/2, y0+h/2-30), "flujo de", F(20), GRIS)
            text_center(d, (x+w+gap/2, y0+h/2-5), "energía", F(20), GRIS)
    arrow(d, (850, 310), (850, 355), color=NARANJA, width=6)
    text_center(d, (850, 700), "Sin fotosíntesis no hay entrada de energía a la cadena trófica:", F(30, True), VERDE_OSC)
    bullets = [
        "•  Los productores capturan la energía solar y la convierten en energía química (glucosa).",
        "•  Esa energía se transfiere de nivel en nivel; en cada paso se pierde ≈ 90% como calor.",
        "•  Los descomponedores devuelven CO₂, agua y nutrientes al suelo y al aire: el ciclo se reinicia.",
    ]
    for i, b in enumerate(bullets):
        d.text((180, 760+i*55), b, font=F(28), fill=TEXTO)
    text_center(d, (850, 1005), "La fotosíntesis es la puerta de entrada de la energía en casi todos los ecosistemas.", F(28), GRIS)
    return save(img, "cadena.png")

# ---------------------------------------------------------------- modelo 3D (foto)
def modelo3d():
    W, H = 1700, 1050
    img = Image.new("RGB", (W, H), (245, 243, 238))
    d = ImageDraw.Draw(img)
    # mesa / fondo
    d.rectangle([0, 720, W, H], fill=(210, 200, 185))
    d.rectangle([0, 700, W, 730], fill=(190, 180, 165))
    # base de unicel/cartón
    d.rounded_rectangle([420, 640, 1280, 760], radius=18, fill=(250, 250, 250), outline=(180, 180, 180), width=3)
    # cloroplasto 3D "maqueta": elipsoide con volumen
    cx, cy, rx, ry = 850, 470, 430, 250
    for i in range(30, 0, -1):
        t = i/30
        col = (int(120+60*(1-t)), int(190+40*(1-t)), int(110+40*(1-t)))
        d.ellipse([cx-rx, cy-ry+int(40*t), cx+rx, cy+ry+int(40*t)], fill=col)
    d.ellipse([cx-rx, cy-ry, cx+rx, cy+ry], fill=(140, 200, 130), outline=(60, 110, 60), width=5)
    d.ellipse([cx-rx+30, cy-ry+30, cx+rx-30, cy+ry-30], fill=(170, 220, 160), outline=(90, 150, 90), width=3)
    # grana en relieve
    for (gx, gy) in [(700, 420), (850, 500), (1000, 430), (780, 560), (950, 570)]:
        for i in range(4):
            y = gy-24+i*16
            d.ellipse([gx-70, y-10, gx+70, y+10], fill=(90, 160, 90), outline=(50, 110, 50), width=2)
    # brillo 3D
    d.ellipse([cx-260, cy-190, cx-40, cy-90], fill=(200, 235, 195))
    # etiquetas de la maqueta
    for txt, (px, py), (lx, ly) in [
        ("Membrana (plastilina verde)", (cx-rx+40, cy-60), (120, 180)),
        ("Grana (monedas apiladas)", (700, 396), (120, 320)),
        ("Estroma (relleno suave)", (850, 500), (1330, 300)),
        ("Base de unicel", (600, 700), (120, 900)),
    ]:
        d.line([(px, py), (lx, ly)], fill=(80, 80, 80), width=3)
        d.ellipse([px-6, py-6, px+6, py+6], fill=(80, 80, 80))
        d.text((lx, ly), txt, font=F(28, True), fill=TEXTO)
    text_center(d, (850, 60), "Evidencia fotográfica — maqueta / modelo 3D del cloroplasto", F(38, True), VERDE_OSC)
    text_center(d, (850, 1000), "Sustituir por la fotografía real de la maqueta elaborada en clase (o del video).", F(26), GRIS)
    return save(img, "modelo3d.png")

if __name__ == "__main__":
    cloroplasto(); correlacion(); fase_luminosa(); calvin(); gases(); cadena(); modelo3d()
    print("Diagramas listos en", OUT)
