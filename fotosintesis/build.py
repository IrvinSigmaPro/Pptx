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

    doc = Document()
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

    def figure(fname, caption):
        # Espacio reservado para la figura (sin imagen incrustada).
        p(f"[Espacio para la figura: {caption}]", italic=True, align=WD_ALIGN_PARAGRAPH.CENTER)

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
        "Metodología",
        "B. Justificación",
        "C. Desarrollo",
        "D. Resultados, análisis y conclusión",
        "E. Bibliografía",
        "Glosario",
    ])

    # ---------------------------------------------------------------- A
    h("A. Introducción")
    p("La fotosíntesis es uno de los procesos bioquímicos más importantes para la vida en la Tierra. Consiste en la conversión de la energía luminosa del Sol en energía química, almacenada en moléculas de glucosa, a partir de dióxido de carbono y agua. Gracias a este proceso, los organismos autótrofos —plantas, algas y algunas bacterias— producen su propio alimento y, al mismo tiempo, liberan el oxígeno que la mayoría de los seres vivos necesita para respirar. Sin fotosíntesis no existiría oxígeno en la atmósfera ni flujo de energía en los ecosistemas.")
    p("La ecuación general de la fotosíntesis es la siguiente: 6 CO₂ + 6 H₂O + luz solar → C₆H₁₂O₆ (glucosa) + 6 O₂. En esta ecuación, el dióxido de carbono (CO₂) proviene del aire y entra por los estomas de la hoja; el agua (H₂O) es absorbida por las raíces y transportada hasta las hojas; la luz solar es captada por el pigmento verde clorofila; y como productos se obtienen la glucosa, que es la energía química utilizable por la célula, y el oxígeno (O₂), que se libera a la atmósfera.")
    p("El reactor celular donde se lleva a cabo la fotosíntesis es el cloroplasto, un orgánulo presente en las células de las plantas y de las algas. En las bacterias fotosintéticas, que no poseen cloroplastos, el proceso ocurre en la membrana plasmática. Dentro del cloroplasto se distinguen dos fases relacionadas: la fase luminosa o fotoquímica, que ocurre en la membrana de los tilacoides y requiere luz directa, y el ciclo de Calvin o fase oscura, que ocurre en el estroma y no necesita luz directa, aunque sí depende de los productos de la fase luminosa.")
    p("El estudio de la fotosíntesis se desarrolló a lo largo de varios siglos. En el siglo XVIII, Joseph Priestley demostró que las plantas «restauraban» el aire alterado por la respiración de los animales; Jan Ingenhousz comprobó que este efecto solo ocurría en presencia de luz; Nicolas-Théodore de Saussure estableció que el agua y el dióxido de carbono son las materias primas del proceso; y en el siglo XX, Melvin Calvin describió el ciclo que lleva su nombre y explica cómo se fija el carbono. Estos antecedentes muestran que la fotosíntesis es el resultado de una larga historia de investigación científica.")
    p("En síntesis, la fotosíntesis correlaciona la energía solar, el agua, el dióxido de carbono y la clorofila para producir glucosa y oxígeno. El diagrama de correlación de la Figura 1 resume esta relación: sin ninguno de estos factores el proceso no puede realizarse, y sus productos sostienen la vida de los organismos autótrofos y heterótrofos.")
    figure("correlacion.png", "Figura 1. Diagrama de correlación sobre la fotosíntesis: factores necesarios y productos del proceso.")
    p("El cloroplasto, como reactor de la fotosíntesis, recibe materia (dióxido de carbono y agua) y energía (luz solar), y produce glucosa y oxígeno. Su estructura interna está organizada para que ambas fases del proceso ocurran de manera ordenada: la fase luminosa en los tilacoides y el ciclo de Calvin en el estroma (Figura 2).")
    figure("cloroplasto.png", "Figura 2. Estructura del cloroplasto, reactor celular de la fotosíntesis.")

    # ---------------------------------------------------------------- metodología
    h("Metodología")
    p("Para la elaboración de este reporte se siguió una metodología de investigación documental y de trabajo práctico, organizada en las siguientes etapas:")
    numbered([
        "Investigación documental: se consultaron libros de texto de biología y fisiología vegetal (Campbell et al., 2017; Taiz et al., 2018; Raven et al., 2005), así como fuentes institucionales confiables (CONABIO, OpenStax).",
        "Elaboración de diagramas propios: se diseñaron diagramas de correlación, de la estructura del cloroplasto, de la fase luminosa, del ciclo de Calvin y del intercambio de gases, para explicar el proceso con apoyos visuales.",
        "Construcción de una estructura tridimensional: se elaboró una maqueta del cloroplasto con materiales reciclados (plastilina, unicel y cartón) para representar su forma y sus estructuras internas.",
        "Análisis comparativo: se compararon las características de los organismos autótrofos y heterótrofos en una tabla, y se analizó la participación de los autótrofos en las cadenas tróficas.",
        "Redacción y revisión: el texto se redactó en lenguaje formal, con coherencia y sin errores, integrando ejemplos pertinentes, y las fuentes se registraron en formato APA.",
    ])

    # ---------------------------------------------------------------- B
    h("B. Justificación")
    h("B.1. Importancia de la transferencia de energía", level=2)
    p("La fotosíntesis es la única vía por la que la energía solar entra a los ecosistemas. Convierte energía luminosa en energía química (glucosa), que puede almacenarse en forma de almidón o celulosa y transferirse de un organismo a otro a través de las cadenas tróficas. En cada eslabón de la cadena —productores, herbívoros, carnívoros y descomponedores— se transfiere aproximadamente el 10 % de la energía, y el resto se pierde como calor. Por ello, la fotosíntesis es el fundamento de todo flujo de energía en la biosfera.")
    p("Ejemplo claro: el pasto de un potrero capta la energía del Sol mediante la fotosíntesis; una vaca se alimenta de ese pasto y transfiere parte de la energía a su cuerpo; el ser humano consume carne o leche de la vaca y recibe esa misma energía originada en el Sol. Otro ejemplo: los combustibles fósiles como el carbón y el petróleo provienen de restos de organismos fotosintéticos que vivieron hace millones de años, por lo que la energía que utilizamos hoy también proviene, en última instancia, de la fotosíntesis.")
    h("B.2. Importancia de la captura de dióxido de carbono", level=2)
    p("Durante la fotosíntesis, las plantas capturan dióxido de carbono de la atmósfera y lo incorporan a sus tejidos. Los bosques, las selvas y los océanos —gracias al fitoplancton— absorben grandes cantidades de CO₂, lo que ayuda a mitigar el cambio climático y a regular la temperatura del planeta. Cuando los organismos mueren y se descomponen, parte de ese carbono queda almacenado en el suelo o en los sedimentos.")
    p("Ejemplo claro: la selva amazónica y los bosques de México capturan millones de toneladas de CO₂ al año; asimismo, las algas microscópicas del océano realizan cerca de la mitad de la fotosíntesis mundial. Proteger estos ecosistemas es, por tanto, una medida directa contra el calentamiento global.")
    h("B.3. Importancia de la liberación de oxígeno", level=2)
    p("La fotosíntesis liberó el oxígeno que hoy compone la atmósfera. Hace aproximadamente 2 400 millones de años, las cianobacterias comenzaron a producir oxígeno mediante la fotosíntesis, y este gas transformó la atmósfera y permitió la evolución de los organismos aerobios. Actualmente, la fotosíntesis renueva el oxígeno que consumen los seres vivos en la respiración y en la combustión.")
    p("Ejemplo claro: una sola hectárea de bosque puede liberar en un año el oxígeno suficiente para decenas de personas, y los bosques y océanos del planeta producen el oxígeno que respiran todos los seres humanos. Sin la liberación continua de oxígeno, la vida tal como la conocemos no sería posible.")

    # ---------------------------------------------------------------- C
    h("C. Desarrollo")
    h("C.1. Estructura tridimensional del cloroplasto", level=2)
    p("El cloroplasto es un orgánulo de forma ovalada, de 4 a 6 micrómetros de longitud, rodeado por dos membranas. Su forma tridimensional —un elipsoide con estructuras internas ordenadas— maximiza la superficie disponible para captar la luz y realizar las reacciones químicas. Cada célula vegetal puede contener entre 10 y 100 cloroplastos, según la especie y la intensidad de la luz.")
    p("La membrana externa es permeable y delimita el orgánulo; la membrana interna regula el paso de sustancias; y entre ambas se encuentra el espacio intermembrana. En el interior se encuentra el estroma, un fluido que contiene el ADN circular del cloroplasto, ribosomas propios y gránulos de almidón. Sumergidos en el estroma se encuentran los tilacoides, sacos aplanados cuya membrana contiene la clorofila y las proteínas de la fase luminosa. Los tilacoides se agrupan en pilas llamadas grana (singular: grano) y se conectan entre sí mediante lamelas, que permiten el flujo de electrones y protones entre las pilas.")
    p("La siguiente tabla resume las partes del cloroplasto y su función:")
    table = doc.add_table(rows=1, cols=2)
    table.style = "Light Grid Accent 1"
    hdr = table.rows[0].cells
    hdr[0].text = "Estructura"
    hdr[1].text = "Función en la fotosíntesis"
    for a, b in [
        ("Membrana externa", "Delimita el cloroplasto; es permeable a moléculas pequeñas."),
        ("Membrana interna", "Regula el intercambio de sustancias con el estroma."),
        ("Espacio intermembrana", "Región entre ambas membranas."),
        ("Tilacoide", "Saco membranoso donde ocurre la fase luminosa; contiene clorofila."),
        ("Grana", "Pilas de tilacoides que aumentan la superficie de captura de luz."),
        ("Lamela", "Conexión entre grana; transporta electrones y protones."),
        ("Estroma", "Fluido donde ocurre el ciclo de Calvin; contiene ADN, ribosomas y almidón."),
    ]:
        cells = table.add_row().cells
        cells[0].text = a
        cells[1].text = b
    h("C.2. Procesos bioquímicos: fase luminosa y ciclo de Calvin", level=2)
    p("La fase luminosa ocurre en la membrana del tilacoide y requiere luz directa. Sus pasos principales son los siguientes:")
    numbered([
        "Absorción de la luz: la clorofila de los fotosistemas II y I absorbe la energía luminosa y excita sus electrones.",
        "Fotólisis del agua: el agua se descompone y se liberan oxígeno (O₂), protones (H⁺) y electrones. El oxígeno liberado proviene del agua, no del dióxido de carbono.",
        "Cadena de transporte de electrones: los electrones viajan desde el fotosistema II hasta el fotosistema I, pasando por el citocromo b₆f, y liberan energía en el proceso.",
        "Formación de NADPH: en el fotosistema I, los electrones excitados se utilizan para formar NADPH.",
        "Quimiosmosis y síntesis de ATP: los protones se acumulan en el interior del tilacoide y, al salir por la ATP sintasa, proporcionan la energía para producir ATP, la «moneda energética» de la célula.",
    ])
    figure("fase_luminosa.png", "Figura 3. Fase luminosa en la membrana del tilacoide: fotosistemas, cadena de transporte y síntesis de ATP y NADPH.")
    p("El ciclo de Calvin ocurre en el estroma y no necesita luz directa, pero sí depende del ATP y el NADPH producidos en la fase luminosa. Sus pasos principales son los siguientes:")
    numbered([
        "Fijación del carbono: la enzima RuBisCO incorpora una molécula de CO₂ a una molécula de 5 carbonos (RuBP), formando un compuesto inestable que se divide en dos moléculas de 3-PGA.",
        "Reducción: con la energía del ATP y el NADPH, el 3-PGA se transforma en moléculas de G3P, precursoras de la glucosa.",
        "Salida del producto: parte del G3P sale del ciclo y se utiliza para formar glucosa, almidón y celulosa.",
        "Regeneración: el resto del G3P se utiliza para reconstruir la RuBP, de modo que el ciclo puede continuar. Por cada 3 CO₂ fijados se obtiene 1 G3P, y 6 G3P forman 1 molécula de glucosa.",
    ])
    figure("calvin.png", "Figura 4. Ciclo de Calvin en el estroma: fijación, reducción, salida y regeneración.")
    h("C.3. Participación del dióxido de carbono y del oxígeno", level=2)
    p("El dióxido de carbono entra a la hoja por los estomas, pequeños poros regulados por las células oclusivas, y es la fuente de carbono para construir la glucosa. El agua es absorbida por las raíces y asciende hasta las hojas por el xilema. En el cloroplasto, el agua aporta los electrones y el hidrógeno necesarios, y su oxígeno es liberado. El oxígeno producido sale por los estomas hacia la atmósfera, y la glucosa se utiliza de inmediato en la respiración o se almacena como almidón y celulosa. De este modo, la planta realiza un intercambio de gases que equilibra la atmósfera: captura CO₂ y libera O₂ (Figura 5).")
    figure("gases.png", "Figura 5. Participación del dióxido de carbono y del oxígeno en la fotosíntesis.")
    h("C.4. Evidencia fotográfica de la maqueta / modelo 3D del cloroplasto", level=2)
    p("Para explicar los procesos bioquímicos de manera tridimensional, se elaboró una maqueta del cloroplasto con materiales reciclados: la membrana se representó con plastilina verde, los grana con monedas apiladas, las lamelas con tiras del mismo material, el estroma con un relleno suave y la base con unicel. La fotografía de la Figura 6 muestra la maqueta terminada y rotulada. [Sustituir por la fotografía real de la maqueta elaborada en clase.]")
    figure("modelo3d.png", "Figura 6. Maqueta tridimensional del cloroplasto (evidencia fotográfica).")
    h("C.5. Video explicativo de 2 a 3 minutos", level=2)
    p("Como evidencia adicional del aprendizaje, se elaboró un video corto de 2 a 3 minutos de duración, con el siguiente guion:")
    numbered([
        "Introducción al tema (15 segundos): qué es la fotosíntesis y por qué es importante.",
        "Recorrido por la maqueta del cloroplasto (45 segundos): señalando membranas, grana, tilacoides, lamelas y estroma.",
        "Fase luminosa y ciclo de Calvin (60 segundos): explicación de ambas fases y de sus productos.",
        "Participación del CO₂ y del O₂ (30 segundos): intercambio de gases por los estomas.",
        "Cierre (20 segundos): importancia de la fotosíntesis para la transferencia de energía en la cadena trófica.",
    ])
    p("Enlace del video: [pegar aquí el enlace de YouTube o Drive]. Las imágenes del video se integran también en este apartado, como se solicitó.", italic=True)

    # ---------------------------------------------------------------- D
    h("D. Resultados, análisis y conclusión")
    h("D.1. Tabla comparativa: organismos autótrofos y heterótrofos", level=2)
    p("La siguiente tabla compara las características principales de los organismos autótrofos y heterótrofos.")
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
    # anchos de columna
    for r in table.rows:
        r.cells[0].width = DInches(1.35)
        r.cells[1].width = DInches(2.55)
        r.cells[2].width = DInches(2.55)
    p("Tabla 1. Comparación de las características de los organismos autótrofos y heterótrofos.", italic=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    h("D.2. Infografía: los autótrofos en las cadenas tróficas", level=2)
    doc.add_picture(os.path.join(ASSETS, "infografia.png"), width=DInches(4.6))
    p("Figura 7. Infografía: participación de los organismos autótrofos en las cadenas tróficas.", italic=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    h("D.3. Análisis", level=2)
    p("La comparación de la Tabla 1 muestra diferencias claras: los organismos autótrofos producen su propio alimento mediante la fotosíntesis y los heterótrofos dependen de otros seres vivos. Esta diferencia explica por qué los autótrofos ocupan el primer nivel trófico y sostienen a todos los demás: sin productores no habría alimento para los herbívoros, ni para los carnívoros, ni para los descomponedores.")
    p("La estructura del cloroplasto está adaptada a su función como reactor: la gran superficie de tilacoides agrupados en grana maximiza la captura de luz para la fase luminosa, y el estroma amplio proporciona el espacio y las enzimas —como la RuBisCO— para fijar el dióxido de carbono en el ciclo de Calvin. La participación del CO₂ y del O₂ confirma que la fotosíntesis equilibra la atmósfera: captura el gas que los seres vivos liberan al respirar y libera el oxígeno que estos necesitan.")
    p("La maqueta tridimensional facilitó la comprensión de procesos que no se observan a simple vista, ya que permitió visualizar la organización interna del cloroplasto y relacionar cada estructura con su función. Los resultados confirman que la fotosíntesis es el proceso central de la transferencia de energía en los ecosistemas.")
    h("D.4. Conclusión", level=2)
    p("La fotosíntesis es el proceso mediante el cual los organismos autótrofos convierten la energía solar en energía química dentro del cloroplasto. La fase luminosa, en los tilacoides, produce ATP, NADPH y oxígeno; el ciclo de Calvin, en el estroma, fija el dióxido de carbono y forma glucosa. Su importancia para la transferencia de energía en la cadena trófica es fundamental: los productores fotosintéticos son la puerta de entrada de la energía a los ecosistemas, y sin ellos no habría alimento ni oxígeno para los organismos heterótrofos. Además, la captura de CO₂ y la liberación de O₂ hacen de la fotosíntesis un proceso indispensable para el equilibrio del clima y de la atmósfera del planeta.")

    # ---------------------------------------------------------------- E
    h("E. Bibliografía")
    for ref in REFS:
        par = doc.add_paragraph(ref)
        par.paragraph_format.left_indent = DInches(0.5)
        par.paragraph_format.first_line_indent = DInches(-0.5)

    # ---------------------------------------------------------------- glosario
    h("Glosario")
    bullets([
        "Autótrofo: organismo que produce su propio alimento, como las plantas, las algas y las cianobacterias.",
        "Heterótrofo: organismo que obtiene su alimento de otros seres vivos, como los animales, los hongos y el ser humano.",
        "Clorofila: pigmento verde que absorbe la luz solar para la fotosíntesis.",
        "Tilacoide: saco membranoso del cloroplasto donde ocurre la fase luminosa.",
        "Grana: pilas de tilacoides (singular: grano).",
        "Estroma: fluido del cloroplasto donde ocurre el ciclo de Calvin.",
        "RuBisCO: enzima que fija el dióxido de carbono en el ciclo de Calvin.",
        "Cadena trófica: ruta por la que fluye la energía de un organismo a otro en un ecosistema.",
        "Fotólisis: descomposición del agua por acción de la luz, con liberación de oxígeno.",
    ])

    doc.save(path)
    print("DOCX:", path)


if __name__ == "__main__":
    build_docx(os.path.join(BASE, "..", "Reporte-Fotosintesis.docx"))
