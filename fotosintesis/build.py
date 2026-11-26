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

    doc = Document()
    for sec in doc.sections:
        sec.left_margin = DInches(1.0)
        sec.right_margin = DInches(1.0)
        sec.top_margin = DInches(0.9)
        sec.bottom_margin = DInches(0.9)
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
        """Inserta una imagen ajustada al ancho de la caja de texto."""
        ruta = os.path.join(folder, fname)
        if not os.path.exists(ruta):
            p(f"[Espacio para la figura: {caption}]", italic=True, align=WD_ALIGN_PARAGRAPH.CENTER)
            return
        if rotate:
            from PIL import Image as _Im
            tmp = ruta.replace(".png", f"_r{rotate}.png")
            if not os.path.exists(tmp):
                _Im.open(ruta).rotate(rotate, expand=True).save(tmp)
            ruta = tmp
        par = doc.add_paragraph()
        par.alignment = WD_ALIGN_PARAGRAPH.CENTER
        par.paragraph_format.space_after = DPt(4)
        par.add_run().add_picture(ruta, width=DInches(width))
        cap = p(caption, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER)
        for r in cap.runs:
            r.font.size = DPt(9.5)
            r.font.color.rgb = DRGB(0x55, 0x55, 0x55)
        cap.paragraph_format.space_after = DPt(14)

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
    doc.add_page_break()

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
    h("A. Introducción")
    figure("evidencia_1_proceso.jpg", "Figura 1. El proceso de la fotosíntesis: introducción, fase luminosa y ciclo de Calvin.", folder=FOTOS, width=5.2)
    figure("correlacion.png", "Figura 2. Diagrama de correlación sobre la fotosíntesis: factores necesarios y productos del proceso.", width=6.2)
    figure("evidencia_4_cloroplasto.jpg", "Figura 3. El cloroplasto: doble membrana, tilacoides, grana y estroma.", folder=FOTOS, width=5.2)
    figure("cloroplasto.png", "Figura 4. Estructura del cloroplasto, reactor celular de la fotosíntesis.", width=6.2)

    # ---------------------------------------------------------------- B
    h("B. Justificación")
    figure("evidencia_2_justificacion.jpg", "Figura 5. Justificación: transferencia de energía, captura de dióxido de carbono y liberación de oxígeno.", folder=FOTOS, width=5.2)

    # ---------------------------------------------------------------- C
    h("C. Desarrollo")
    h("C.1. Estructura tridimensional del cloroplasto", level=2)
    figure("maqueta_cloroplasto.jpg", "Figura 6. Estructura tridimensional del cloroplasto: maqueta elaborada y rotulada (evidencia fotográfica).", folder=FOTOS, width=6.2)
    h("C.2. Procesos bioquímicos: fase luminosa y ciclo de Calvin", level=2)
    figure("fase_luminosa.png", "Figura 7. Fase luminosa en la membrana del tilacoide: fotosistemas, cadena de transporte y síntesis de ATP y NADPH.", width=6.2)
    figure("calvin.png", "Figura 8. Ciclo de Calvin en el estroma: fijación, reducción y regeneración.", width=6.2)
    h("C.3. Participación del dióxido de carbono y del oxígeno", level=2)
    figure("evidencia_3_procesos_co2.jpg", "Figura 9. Procesos bioquímicos y dióxido de carbono: fijación, reducción, regeneración y participación del oxígeno.", folder=FOTOS, width=5.2)
    figure("gases.png", "Figura 10. Participación del dióxido de carbono y del oxígeno en la fotosíntesis.", width=6.2)
    h("C.4. Evidencia fotográfica de la maqueta / modelo 3D del cloroplasto", level=2)
    figure("evidencia_4_cloroplasto.jpg", "Figura 11. Apunte de la estructura tridimensional del cloroplasto.", folder=FOTOS, width=5.2)
    h("C.5. Video explicativo de 2 a 3 minutos", level=2)
    p("Enlace del video: ______________________________________________", align=WD_ALIGN_PARAGRAPH.CENTER)

    # ---------------------------------------------------------------- D
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
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        shd(hdr[i], "1B5E20")
    for k, row in enumerate(TABLA[1:]):
        cells = table.add_row().cells
        for i, val in enumerate(row):
            cells[i].text = ""
            cp = cells[i].paragraphs[0]
            r = cp.add_run(val)
            r.font.size = Pt(9)
            if i == 0:
                r.bold = True
                r.font.color.rgb = RGBColor(0x1B, 0x5E, 0x20)
            if k % 2 == 1:
                shd(cells[i], "EAF3E6")
    for r in table.rows:
        r.cells[0].width = DInches(1.35)
        r.cells[1].width = DInches(2.55)
        r.cells[2].width = DInches(2.55)
    p("Tabla 1. Comparación de las características de los organismos autótrofos y heterótrofos.", italic=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    h("D.2. Infografía: los autótrofos en las cadenas tróficas", level=2)
    figure("infografia_p1.png", "Figura 12. Infografía (parte 1 de 2): cadenas tróficas, autótrofos, niveles tróficos y participación.", width=4.7)
    figure("infografia_p2.png", "Figura 13. Infografía (parte 2 de 2): flujo de energía, ejemplos de cadenas, red trófica y conclusión.", width=4.7)
    h("D.3. Conclusión", level=2)
    figure("evidencia_5_conclusion.jpg", "Figura 14. Conclusión: la fotosíntesis y su importancia para la transferencia de energía en la cadena trófica.", folder=FOTOS, width=5.2)

    # ---------------------------------------------------------------- E

    # ---------------------------------------------------------------- E
    h("E. Bibliografía")
    for ref in REFS:
        par = doc.add_paragraph(ref)
        par.paragraph_format.left_indent = DInches(0.5)
        par.paragraph_format.first_line_indent = DInches(-0.5)

    doc.save(path)
    print("DOCX:", path)


if __name__ == "__main__":
    build_docx(os.path.join(BASE, "..", "Reporte-Fotosintesis.docx"))
