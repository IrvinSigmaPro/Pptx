#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Compone las imágenes del reporte en placas de página completa (sin huecos)."""
import os
from PIL import Image

BASE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(BASE, "assets")
FOTOS = os.path.join(BASE, "fotos")
PLACAS = os.path.join(ASSETS, "placas")
os.makedirs(PLACAS, exist_ok=True)

W, H = 1300, 1720       # proporción de una página carta con márgenes de 1"
M, G = 6, 14            # margen interno y separación entre imágenes


def plate(items, nombre):
    """items: lista de (ruta, peso). Reparte el alto según los pesos."""
    imgs, pesos = [], []
    for ruta, peso in items:
        im = Image.open(ruta).convert("RGB")
        imgs.append(im)
        pesos.append(peso)
    total_peso = sum(pesos)
    avail = H - 2 * M - G * (len(imgs) - 1)
    piezas = []
    for im, peso in zip(imgs, pesos):
        h = avail * peso / total_peso
        a = im.width / im.height
        w = a * h
        if w > W - 2 * M:
            w = W - 2 * M
            h = w / a
        piezas.append(im.resize((max(1, int(w)), max(1, int(h))), Image.LANCZOS))
    total_alto = sum(p.height for p in piezas) + G * (len(piezas) - 1)
    lienzo = Image.new("RGB", (W, H), (255, 255, 255))
    y = (H - total_alto) // 2
    for p in piezas:
        lienzo.paste(p, ((W - p.width) // 2, y))
        y += p.height + G
    out = os.path.join(PLACAS, nombre)
    lienzo.save(out, "JPEG", quality=88, optimize=True)
    print("OK", nombre, lienzo.size, round(os.path.getsize(out) / 1024), "KB")


# recorte de detalle de la maqueta (el cloroplasto modelado)
maqueta = Image.open(os.path.join(FOTOS, "maqueta_cloroplasto.jpg")).convert("RGB")
w, h = maqueta.size
zoom = maqueta.crop((int(w * 0.17), int(h * 0.33), int(w * 0.80), int(h * 0.72)))
zoom.save(os.path.join(FOTOS, "maqueta_detalle.jpg"), "JPEG", quality=88, optimize=True)

placa_a1 = [(os.path.join(FOTOS, "evidencia_1_proceso.jpg"), 1.0),
            (os.path.join(FOTOS, "cloroplasto_nota.jpg"), 1.0)]
plate(placa_a1, "a1_proceso_cloroplasto.jpg")

placa_a2 = [(os.path.join(ASSETS, "correlacion.png"), 1.0),
            (os.path.join(ASSETS, "cloroplasto.png"), 1.0)]
plate(placa_a2, "a2_correlacion_estructura.jpg")

plate([(os.path.join(FOTOS, "evidencia_2_justificacion.jpg"), 1.0)], "b1_justificacion.jpg")

plate([(os.path.join(FOTOS, "maqueta_cloroplasto.jpg"), 1.0),
       (os.path.join(FOTOS, "maqueta_detalle.jpg"), 1.0)], "c1_maqueta.jpg")

plate([(os.path.join(ASSETS, "fase_luminosa.png"), 1.0),
       (os.path.join(ASSETS, "calvin.png"), 1.0)], "c2_fases.jpg")

# nota 1 primero, nota 2 después (orden pedido)
plate([(os.path.join(FOTOS, "procesos_co2_1.jpg"), 1.5),
       (os.path.join(FOTOS, "relacion_fases_2.jpg"), 1.0)], "c3_notas_co2_o2.jpg")

plate([(os.path.join(ASSETS, "infografia_p1.png"), 1.0)], "d1_infografia_1.jpg")
plate([(os.path.join(ASSETS, "infografia_p2.png"), 1.0)], "d2_infografia_2.jpg")
plate([(os.path.join(FOTOS, "evidencia_5_conclusion.jpg"), 1.0)], "d3_conclusion.jpg")

print("todas las placas generadas")
