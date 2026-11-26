#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera el reporte en texto (DOCX) de la fotosíntesis."""
import os

BASE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(BASE, "assets")

TABLA = [
    ("Característica", "Organismos autótrofos", "Organismos heterótrofos"),
    ("Definición",
     "Seres vivos capaces de sintetizar su propia materia orgánica a partir de sustancias inorgánicas.",
     "Seres vivos que no pueden sintetizar su alimento y deben tomarlo ya elaborado del medio."),
    ("Obtención del alimento",
     "Producen su propio alimento mediante la fotosíntesis (plantas, algas) o la quimiosíntesis (algunas bacterias).",
     "Obtienen su alimento consumiendo a otros seres vivos, sus restos o sus productos."),
    ("Fuente de energía",
     "Energía luminosa del Sol (fotótrofos) o energía química de compuestos inorgánicos (quimiótrofos).",
     "Energía química almacenada en los enlaces de la materia orgánica que ingieren."),
    ("Materia prima",
     "Dióxido de carbono, agua y sales minerales tomados directamente del ambiente.",
     "Materia orgánica ya elaborada: carbohidratos, grasas y proteínas de otros organismos."),
    ("Estructuras que intervienen",
     "Cloroplastos con clorofila, estomas, raíces y vasos conductores.",
     "Aparato digestivo, boca, dientes, enzimas digestivas; en hongos, hifas absortivas."),
    ("Proceso característico",
     "Fotosíntesis (fase luminosa y ciclo de Calvin) o quimiosíntesis.",
     "Digestión, absorción y respiración celular para liberar la energía del alimento."),
    ("Productos principales",
     "Glucosa y oxígeno; almacenan la energía en forma de almidón, celulosa o aceites.",
     "Dióxido de carbono, agua, urea y calor; utilizan la energía para crecer y moverse."),
    ("Dependencia de otros organismos",
     "No dependen de otros seres vivos para alimentarse: son autosuficientes.",
     "Dependen directa o indirectamente de los autótrofos para obtener alimento y oxígeno."),
    ("Nivel trófico",
     "Productores: ocupan el primer nivel de las cadenas y redes tróficas.",
     "Consumidores (herbívoros, carnívoros, omnívoros) y descomponedores: segundo nivel en adelante."),
    ("Papel en el ciclo del carbono",
     "Fijan el CO₂ atmosférico y lo incorporan a la materia orgánica: son un sumidero de carbono.",
     "Liberan CO₂ a la atmósfera mediante la respiración y la descomposición."),
    ("Movilidad",
     "En su mayoría sésiles (fijos al sustrato), aunque algunas algas y bacterias se desplazan.",
     "En su mayoría móviles; se trasladan en busca de alimento, refugio o pareja."),
    ("Ejemplos",
     "Plantas, algas, fitoplancton, cianobacterias y bacterias fotosintéticas o quimiosintéticas.",
     "Animales, hongos, protozoarios, bacterias descomponedoras y el ser humano."),
    ("Importancia ecológica",
     "Base de todas las cadenas tróficas: producen oxígeno, capturan CO₂ y originan la materia orgánica de los ecosistemas.",
     "Regulan las poblaciones de otros organismos, dispersan semillas, polinizan y reciclan nutrientes."),
]

REFS = [
    "Alberts, B., Johnson, A., Lewis, J., Morgan, D., Raff, M., Roberts, K., & Walter, P. (2022). Molecular biology of the cell (8th ed.). W. W. Norton & Company.",
    "Campbell, N. A., Urry, L. A., Cain, M. L., Wasserman, S. A., Minorsky, P. V., & Reece, J. B. (2017). Campbell biology (11th ed.). Pearson.",
    "Comisión Nacional para el Conocimiento y Uso de la Biodiversidad. (2023). Fotosíntesis. https://www.biodiversidad.gob.mx",
    "Raven, P. H., Evert, R. F., & Eichhorn, S. E. (2005). Biology of plants (7th ed.). W. H. Freeman and Company.",
    "Taiz, L., Zeiger, E., Møller, I. M., & Murphy, A. (2018). Plant physiology and development (7th ed.). Sinauer Associates.",
    "Urry, L. A., Cain, M. L., Wasserman, S. A., Minorsky, P. V., & Reece, J. B. (2021). Biology 2e. OpenStax. https://openstax.org/details/books/biology-2e",
]


def build_docx(path):
    from docx import Document
    from docx.shared import Pt, Inches as DInches, RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.enum.table import WD_TABLE_ALIGNMENT
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement

    Pt = Pt
    DPt = Pt
    DRGB = RGBColor

    def shd(cell, hexcolor):
        tcPr = cell._tc.get_or_add_tcPr()
        shd_el = OxmlElement("w:shd")
        shd_el.set(qn("w:val"), "clear")
        shd_el.set(qn("w:color"), "auto")
        shd_el.set(qn("w:fill"), hexcolor)
        tcPr.append(shd_el)

    FOTOS = os.path.join(BASE, "fotos")
    PLACAS = os.path.join(ASSETS, "placas")

    doc = Document()
    for sec in doc.sections:
        sec.left_margin = DInches(0.75)
        sec.right_margin = DInches(0.75)
        sec.top_margin = DInches(0.8)
        sec.bottom_margin = DInches(0.8)
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = DPt(12)
    st.paragraph_format.space_after = DPt(6)
    st.paragraph_format.line_spacing = 1.15

    def h(text, level=1):
        p = doc.add_heading(text, level=level)
        for r in p.runs:
            r.font.color.rgb = DRGB(0x1B, 0x5E, 0x20)
        return p

    def p(text, bold=False, italic=False, align=None):
        par = doc.add_paragraph()
        run = par.add_run(text)
        run.bold = bold
        run.italic = italic
        if align:
            par.alignment = align
        return par

    def bullets(items):
        for it in items:
            doc.add_paragraph(it, style="List Bullet")

    def numbered(items):
        for it in items:
            doc.add_paragraph(it, style="List Number")

    def figure(fname, caption, width=6.0, folder=ASSETS, rotate=0):
        """Inserta una imagen ajustada al ancho, sin pie de foto."""
        ruta = os.path.join(folder, fname)
        if not os.path.exists(ruta):
            return
        par = doc.add_paragraph()
        par.alignment = WD_ALIGN_PARAGRAPH.CENTER
        par.paragraph_format.space_after = DPt(10)
        par.add_run().add_picture(ruta, width=DInches(width))

    # ---------------------------------------------------------------- portada
    t = doc.add_paragraph()
    t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = t.add_run("La fotosíntesis y su importancia\npara la transferencia de energía")
    r.bold = True
    r.font.size = DPt(24)
    r.font.color.rgb = DRGB(0x1B, 0x5E, 0x20)
    p("Reporte integrado", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    p("Fase luminosa, ciclo de Calvin y el cloroplasto como reactor celular", italic=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    p("Integración del reporte: introducción, metodología, justificación, desarrollo, resultados, análisis, conclusión y bibliografía en formato APA.", align=WD_ALIGN_PARAGRAPH.CENTER)

    # ---------------------------------------------------------------- índice
    h("Índice")
    bullets([
        "A. Introducción",
        "B. Justificación",
        "C. Desarrollo",
        "D. Resultados, análisis y conclusión",
        "E. Bibliografía",
    ])

    # ---------------------------------------------------------------- A
    doc.add_page_break()
    h("A. Introducción")
    figure("a1_proceso_cloroplasto.jpg", "", width=6.5, folder=PLACAS)
    doc.add_page_break()
    figure("a2_correlacion_estructura.jpg", "", width=7.0, folder=PLACAS)

    # ---------------------------------------------------------------- B
    doc.add_page_break()
    h("B. Justificación")
    figure("b1_justificacion.jpg", "", width=6.5, folder=PLACAS)

    # ---------------------------------------------------------------- C
    doc.add_page_break()
    h("C. Desarrollo")
    h("C.1. Estructura tridimensional del cloroplasto", level=2)
    figure("c1_maqueta.jpg", "", width=6.3, folder=PLACAS)
    doc.add_page_break()
    h("C.2. Procesos bioquímicos: fase luminosa y ciclo de Calvin", level=2)
    figure("c2_fases.jpg", "", width=6.6, folder=PLACAS)
    doc.add_page_break()
    h("C.3. Participación del dióxido de carbono y del oxígeno", level=2)
    figure("c3_notas_co2_o2.jpg", "", width=5.9, folder=PLACAS)
    h("C.4. Video explicativo de 2 a 3 minutos", level=2)
    p("Enlace del video: ______________________________________________", align=WD_ALIGN_PARAGRAPH.CENTER)

    # ---------------------------------------------------------------- D
    doc.add_page_break()
    h("D. Resultados, análisis y conclusión")
    h("D.1. Tabla comparativa: organismos autótrofos y heterótrofos", level=2)
    table = doc.add_table(rows=1, cols=3)
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = table.rows[0].cells
    for i, val in enumerate(TABLA[0]):
        hdr[i].text = ""
        cp = hdr[i].paragraphs[0]
        cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = cp.add_run(val)
        r.bold = True
        r.font.size = Pt(10.5)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        shd(hdr[i], "1B5E20")
    for k, row in enumerate(TABLA[1:]):
        cells = table.add_row().cells
        for i, val in enumerate(row):
            cells[i].text = ""
            cp = cells[i].paragraphs[0]
            cp.paragraph_format.space_after = Pt(4)
            cp.paragraph_format.space_before = Pt(2)
            r = cp.add_run(val)
            r.font.size = Pt(10)
            if i == 0:
                r.bold = True
                r.font.color.rgb = RGBColor(0x1B, 0x5E, 0x20)
            if k % 2 == 1:
                shd(cells[i], "EAF3E6")
    for r in table.rows:
        r.cells[0].width = DInches(1.45)
        r.cells[1].width = DInches(2.75)
        r.cells[2].width = DInches(2.75)
    doc.add_page_break()
    h("D.2. Infografía: los autótrofos en las cadenas tróficas", level=2)
    figure("d1_infografia_1.jpg", "", width=6.5, folder=PLACAS)
    doc.add_page_break()
    figure("d2_infografia_2.jpg", "", width=7.0, folder=PLACAS)
    doc.add_page_break()
    h("D.3. Conclusión", level=2)
    figure("d3_conclusion.jpg", "", width=6.5, folder=PLACAS)

    # ---------------------------------------------------------------- E

    # ---------------------------------------------------------------- E
    doc.add_page_break()
    h("E. Bibliografía")
    for ref in REFS:
        par = doc.add_paragraph(ref)
        par.paragraph_format.left_indent = DInches(0.5)
        par.paragraph_format.first_line_indent = DInches(-0.5)

    doc.save(path)
    print("DOCX:", path)


if __name__ == "__main__":
    build_docx(os.path.join(BASE, "..", "Reporte-Fotosintesis.docx"))
