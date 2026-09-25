# -*- coding: utf-8 -*-
"""Ensambla la presentación completa: PPTX con animaciones + vista previa en imágenes.

Uso:
    python3 build_all.py            # construye el PPTX y la vista previa
    python3 build_all.py --pptx     # solo el PPTX
    python3 build_all.py --preview  # solo las imágenes de vista previa
"""
import os, sys, time
import theme
from theme import SLIDE_W, SLIDE_H, SECTION, PREVIEW, ROOT
from pptx import Presentation
from pptx.util import Inches

import content1, content2, content3, content4, content5, content6, content7
from canvas import PptxCanvas, PilCanvas
import deck as deckmod
import anim

OUT = os.path.join(ROOT, "Compuertas Lógicas y Chips Serie 74XX - Versión Mejorada.pptx")


def build_specs():
    specs = []
    specs += content1.SLIDES
    specs += content2.SLIDES
    specs += content3.SLIDES + content7.AFTER_3
    specs += content4.SLIDES + content7.AFTER_4
    specs += content5.SLIDES + content7.AFTER_5
    specs += content6.SLIDES
    return specs


def meta_for(spec):
    acc, num, name = SECTION[spec.get("section", 1)]
    return {"accent": acc, "num": num, "name": name}


# --------------------------------------------------------------------- PPTX
def build_pptx(specs, path):
    prs = Presentation()
    prs.slide_width = Inches(SLIDE_W)
    prs.slide_height = Inches(SLIDE_H)
    blank = prs.slide_layouts[6]
    total = len(specs)
    for i, spec in enumerate(specs, 1):
        slide = prs.slides.add_slide(blank)
        meta = meta_for(spec)
        c = PptxCanvas(slide, SLIDE_W, SLIDE_H, accent=meta["accent"], total=total)
        groups = deckmod.render(c, meta, i, total, spec)
        anim.set_transition(slide, spec.get("transition", "fade"))
        if spec.get("anim", True):
            anim.add_animation(slide, groups)
        anim.set_notes(slide, spec.get("notes", ""))
        if i % 20 == 0:
            print("   ... %d/%d diapositivas" % (i, total))
    from pptx.oxml.ns import qn
    core = prs.core_properties
    core.title = "Compuertas Lógicas y Chips Serie 74XX"
    core.subject = "Electrónica Digital · Serie 74XX"
    core.author = "Presentación ampliada"
    core.comments = ("Versión ampliada a %d diapositivas con transiciones y animaciones de "
                     "entrada en cada lámina." % total)
    prs.save(path)
    return total


# ------------------------------------------------------------------ PREVIEW
def build_preview(specs):
    os.makedirs(PREVIEW, exist_ok=True)
    for f in os.listdir(PREVIEW):
        if f.endswith((".png", ".jpg")):
            os.remove(os.path.join(PREVIEW, f))
    total = len(specs)
    for i, spec in enumerate(specs, 1):
        meta = meta_for(spec)
        c = PilCanvas(SLIDE_W, SLIDE_H, total=total, accent=meta["accent"])
        deckmod.render(c, meta, i, total, spec)
        img = c.finish()
        img.save(os.path.join(PREVIEW, "slide_%03d.jpg" % i), quality=82, optimize=True)
        if i % 20 == 0:
            print("   ... preview %d/%d" % (i, total))
    return total


def main():
    t0 = time.time()
    specs = build_specs()
    total = len(specs)
    print("Total de diapositivas: %d" % total)
    args = sys.argv[1:]
    do_pptx = ("--pptx" in args) or not args
    do_prev = ("--preview" in args) or not args
    if do_pptx:
        build_pptx(specs, OUT)
        print("PPTX escrito en: %s" % OUT)
    if do_prev:
        build_preview(specs)
        print("Vista previa en: %s" % PREVIEW)
    print("Listo en %.1f s" % (time.time() - t0))


if __name__ == "__main__":
    main()
