# -*- coding: utf-8 -*-
"""Sección 6 — Repaso, glosario, catálogo ampliado y cierre."""
import os
from theme import SRC, GEN


def p(n):
    return os.path.join(GEN, n + ".png")


def s(n):
    return os.path.join(SRC, n)


SLIDES = [
    dict(kind="section", section=6, transition="zoom",
         img=p("sec_rep"), topics=[
             "Resumen comparativo de las siete compuertas y sus tablas de verdad",
             "Tabla maestra de chips, funciones y equivalencias entre subfamilias",
             "Catálogo ampliado de la Serie 74XX: contadores, registros, memorias y periféricos",
             "Glosario técnico completo con más de 30 términos esenciales",
             "Fuentes de consulta y verificación de datos",
             "Retos de repaso y cierre de la presentación"],
         notes="Apertura del bloque 6."),

    dict(kind="bullets", section=6, transition="wipe",
         title="Resumen ejecutivo: las siete compuertas en una mirada",
         lead="Todo el bloque de compuertas condensado para repasar antes del examen.",
         two_col=True, per=3, size=11.6, gap=0.08,
         items=["**AND (7408):** Y = A·B. Salida '1' solo si TODAS las entradas están en '1'. "
                "Se usa como habilitador y para confirmar condiciones múltiples.",
                "**OR (7432):** Y = A + B. Salida '1' si AL MENOS UNA entrada está en '1'. "
                "Se usa en alarmas y unión de condiciones.",
                "**NOT (7404):** Y = A'. Invierte el nivel. Genera variables negadas y forma "
                "osciladores y antirrebotes.",
                "**NAND (7400):** Y = (A·B)'. Salida '0' solo si TODAS las entradas están en '1'. "
                "Compuerta universal preferida en TTL.",
                "**NOR (7402):** Y = (A+B)'. Salida '1' solo si TODAS las entradas están en '0'. "
                "Compuerta universal natural en CMOS.",
                "**XOR (7486):** Y = A ⊕ B. Salida '1' si las entradas DIFIEREN. Base de "
                "sumadores, paridad y comparadores.",
                "**XNOR (74266):** Y = (A ⊕ B)'. Salida '1' si las entradas COINCIDEN. Comparador "
                "de igualdad; requiere pull-up por ser colector abierto.",
                "**Regla de oro:** cualquier función lógica se implementa SOLO con NAND o SOLO "
                "con NOR. Ese es el teorema práctico más útil de toda la electrónica digital.",
                "**Jerarquía de estudio:** entender la tabla de verdad, después la expresión "
                "booleana y por último el chip y su pinout.",
                "**Verificación obligatoria:** toda compuerta debe probarse con las cuatro "
                "combinaciones (o dos, en el caso del inversor) antes de integrarla al diseño."],
         note="Autoevaluación: sin mirar la tabla, escribir las cuatro combinaciones de la XOR y "
              "de la XNOR. Si se confunden, revisar el detalle de por qué una es la negación de "
              "la otra.",
         notes="Ideal como diapositiva de repaso previa al examen."),

    dict(kind="table", section=6, transition="wipe",
         title="Tabla maestra: chips, funciones y equivalencias",
         lead="Todo lo esencial en una sola lámina de consulta rápida.",
         header=["Compuerta", "Chip TTL", "Expresión", "Salida = 1 cuando", "Equivalencias directas"],
         widths=[0.12, 0.13, 0.16, 0.28, 0.31], accent="cyan", size=10.2, row_h=0.44,
         rows=[["AND", "7408", "Y = A · B", "A = 1 y B = 1", "74LS08 · ALS08 · F08 · HC08 · HCT08"],
               ["OR", "7432", "Y = A + B", "A = 1 o B = 1 (o ambos)",
                "74LS32 · ALS32 · F32 · HC32 · HCT32"],
               ["NOT", "7404", "Y = A'", "A = 0", "74LS04 · 74LS05 (OC) · 74LS14 (Schmitt)"],
               ["NAND", "7400", "Y = (A · B)'", "No todas las entradas son '1'",
                "74LS00 · 74LS03 (OC) · 74132 (Schmitt)"],
               ["NOR", "7402", "Y = (A + B)'", "Todas las entradas son '0'",
                "74LS02 · 74LS27 (3 entradas) · 74LS33 (OC)"],
               ["XOR", "7486", "Y = A ⊕ B", "Las entradas son diferentes",
                "74LS86 · 74LS386 (3 entradas) · 74LS280 (paridad)"],
               ["XNOR", "74266", "Y = (A ⊕ B)'", "Las entradas son iguales",
                "74LS266 (OC) · 74HC7266 (sin OC)"],
               ["Sumador", "7483 / 74181", "S = A + B + Cin", "No aplica: es aritmético",
                "74LS83 · 74LS283 (4 bits) · 74LS181 (ALU completa)"],
               ["Contador", "74161 / 7490", "Cuenta en binario o BCD", "No aplica: es secuencial",
                "74LS161 · 74LS163 (síncrono) · 74LS90 · 74LS390"],
               ["Registro", "74164 / 74194", "Serie→paralelo / universal",
                "No aplica: es secuencial", "74LS164 · 74LS165 · 74LS194 · 74LS373"]],
         note="Compatible con las siete compuertas estudiadas: **todo chip de la Serie 74XX "
              "mantiene su patrón de pines dentro de la misma función**, solo cambia la "
              "tecnología (LS, ALS, F, HC, HCT) y con ella la velocidad, el consumo y las "
              "corrientes de entrada.",
         note_label="COMPATIBILIDAD GARANTIZADA", notes="Puede imprimirse como hoja de fórmulas."),

    dict(kind="grid", section=6, transition="fade",
         title="Catálogo ampliado de la Serie 74XX (parte 1: lógica y aritmética)",
         lead="Los integrados que conviene conocer después de las siete compuertas básicas.",
         cols=3, accent="orange",
         items=[dict(name="7411", desc="Tres compuertas AND de 3 entradas en un DIP-14.",
                     tag="Lógica", accent="cyan"),
                dict(name="7420", desc="Dos compuertas NAND de 4 entradas: ideal para decodificar "
                                       "direcciones.", tag="Lógica", accent="green"),
                dict(name="7430", desc="NAND de 8 entradas; detecta cuando un byte completo vale "
                                       "todos unos.", tag="Lógica", accent="green"),
                dict(name="7427", desc="Tres NOR de 3 entradas, muy usadas en lógica CMOS.",
                     tag="Lógica", accent="pink"),
                dict(name="74133", desc="NAND de 13 entradas: verifica 13 condiciones simultáneas.",
                     tag="Lógica", accent="green"),
                dict(name="74280", desc="Generador y verificador de paridad de 9 bits.",
                     tag="Paridad", accent="blue"),
                dict(name="7483", desc="Sumador binario completo de 4 bits con acarreo.",
                     tag="Aritmética", accent="cyan"),
                dict(name="74283", desc="Sumador de 4 bits con acarreo rápido anticipado.",
                     tag="Aritmética", accent="cyan"),
                dict(name="74181", desc="ALU de 4 bits: 16 operaciones lógicas y 16 aritméticas.",
                     tag="ALU", accent="orange"),
                dict(name="74182", desc="Unidad de acarreo anticipado para cadenas rápidas.",
                     tag="ALU", accent="orange"),
                dict(name="7485", desc="Comparador de magnitud de 4 bits (A > B, A = B, A < B).",
                     tag="Comparación", accent="purple"),
                dict(name="74688", desc="Comparador de 8 bits pensado para direcciones de memoria.",
                     tag="Comparación", accent="purple")],
         note="Estos chips amplían las siete compuertas básicas: con ellos se construyen "
              "sumadores de palabras completas, comparadores y decodificadores de direcciones.",
         notes="Mostrar solo los más relevantes según el nivel del grupo."),

    dict(kind="grid", section=6, transition="fade",
         title="Catálogo ampliado (parte 2: secuencial, memoria e interfaz)",
         lead="Contadores, registros, memorias y chips de bus.",
         cols=3, accent="teal",
         items=[dict(name="7474", desc="Dos flip-flops D con preset y clear, disparados por "
                                       "flanco.", tag="Secuencial", accent="indigo"),
                dict(name="74107", desc="Dos flip-flops JK maestro-esclavo.", tag="Secuencial",
                     accent="indigo"),
                dict(name="74161", desc="Contador binario síncrono de 4 bits con carga paralela.",
                     tag="Contador", accent="teal"),
                dict(name="74163", desc="Igual al 74161 pero con reinicio totalmente síncrono.",
                     tag="Contador", accent="teal"),
                dict(name="7490", desc="Contador de décadas: divide entre 2 y entre 5 (BCD).",
                     tag="Contador", accent="teal"),
                dict(name="74164", desc="Registro de desplazamiento de 8 bits serie→paralelo.",
                     tag="Registro", accent="blue"),
                dict(name="74194", desc="Registro universal de 4 bits: desplaza en ambos sentidos.",
                     tag="Registro", accent="blue"),
                dict(name="74189", desc="RAM estática de 64 bits organizada en 16 × 4.",
                     tag="Memoria", accent="yellow"),
                dict(name="74288", desc="PROM bipolar de 32 palabras × 8 bits (lógica "
                                        "programable).", tag="Memoria", accent="yellow"),
                dict(name="74245", desc="Transceptor octal de bus con control de dirección.",
                     tag="Bus", accent="green"),
                dict(name="74373", desc="Latch octal transparente con salidas de 3 estados.",
                     tag="Bus", accent="green"),
                dict(name="7447", desc="Decodificador BCD a 7 segmentos, salidas activas en bajo.",
                     tag="Display", accent="red")],
         note="Con estos integrados se puede construir un sistema digital completo de 8 bits: "
              "contador de programa, registros, memoria y decodificación de direcciones, igual "
              "que las primeras computadoras personales.",
         notes="Contextualizar: estos chips formaron las primeras computadoras."),

    dict(kind="glossary", section=6, transition="fade",
         title="Glosario técnico (parte 1)",
         lead="Terminología esencial que aparece en hojas de datos y exámenes.",
         cols=3, accent="blue",
         terms=[("Anódico/Cátodo", "Terminales del LED: el cátodo va al lado negativo; invertirlo "
                                   "impide el encendido."),
                ("Biestable (flip-flop)", "Circuito con memoria que cambia solo en el flanco de "
                                          "reloj."),
                ("Colector abierto", "Salida que solo puede llevar la línea a '0'; requiere "
                                     "resistencia pull-up externa."),
                ("Compuerta", "Circuito elemental que realiza una operación lógica booleana."),
                ("Datasheet", "Hoja de datos del fabricante con especificaciones eléctricas y "
                              "funcionales."),
                ("DIP", "Dual In-line Package: encapsulado de dos filas de pines para protoboard."),
                ("E/S (I/O)", "Entrada/Salida: pines que pueden recibir o entregar señales."),
                ("Fan-out", "Número de entradas que puede gobernar una salida sin degradar "
                            "niveles."),
                ("Flanco", "Transición momentánea de 0 a 1 (subida) o de 1 a 0 (bajada)."),
                ("Glitch", "Pulso espurio producido por diferencias de retardo entre rutas."),
                ("Latch", "Memoria sensible al nivel, transparente mientras el enable está "
                          "activo."),
                ("LSB / MSB", "Bit menos significativo y bit más significativo de una palabra."),
                ("Nivel activo", "Estado ('1' o '0') que hace que una señal cumpla su función."),
                ("Pull-up", "Resistencia a VCC que fija el nivel alto cuando la salida está en "
                            "alta impedancia."),
                ("Tres estados", "Salida que puede estar en '1', en '0' o en alta impedancia (Z)."),
                ("TTL", "Transistor-Transistor Logic: familia bipolar de 5 V, base de la Serie "
                        "74XX."),
                ("CMOS", "Lógica de transistores MOSFET complementarios: bajo consumo, "
                         "alimentación flexible."),
                ("VIL / VIH", "Tensiones máximas y mínimas que la entrada reconoce como '0' y "
                              "'1'.")],
         note="Estos términos aparecen constantemente en hojas de datos, foros y exámenes: "
              "conviene dominarlos antes de leer cualquier datasheet en inglés.",
         notes="Puede dividirse en dos sesiones."),

    dict(kind="glossary", section=6, transition="fade",
         title="Glosario técnico (parte 2)",
         lead="Segunda tanda de conceptos clave.",
         cols=3, accent="purple",
         terms=[("VOL / VOH", "Tensiones máximas y mínimas garantizadas a la salida en nivel bajo "
                              "y alto."),
                ("IOH / IOL", "Corriente máxima que la salida entrega en alto y absorbe en bajo."),
                ("tPD", "Retardo de propagación: tiempo entre el cambio de entrada y el de "
                        "salida."),
                ("tPLH / tPHL", "Retardo de subida y de bajada, respectivamente."),
                ("Margen de ruido", "Diferencia entre lo que una salida entrega y lo que una "
                                    "entrada exige."),
                ("VCC / VDD", "Nomenclatura de la alimentación positiva en TTL y CMOS."),
                ("GND", "Referencia común de tierra; en DIP-14 corresponde al pin 7."),
                ("Habilitación (OE)", "Pin que activa la salida de un chip; activo en bajo en la "
                                      "mayoría."),
                ("Multiplexor", "Circuito que selecciona una de varias entradas y la envía a una "
                                "salida."),
                ("Decodificador", "Circuito que activa una salida según el código binario de "
                                  "entrada."),
                ("Acarreo (carry)", "Bit que se propaga a la etapa siguiente en una suma."),
                ("Complemento a dos", "Forma de representar números negativos: invertir bits y "
                                      "sumar 1."),
                ("SOP / POS", "Suma de productos y producto de sumas: formas canónicas de una "
                              "función."),
                ("Minitérmino", "Producto que vale 1 en exactamente una fila de la tabla de "
                                "verdad."),
                ("Karnaugh", "Método gráfico de simplificación por agrupamiento de unos."),
                ("ESD", "Descarga electrostática: causa frecuente de daño en chips CMOS."),
                ("Schmitt trigger", "Entrada con histéresis que limpia señales ruidosas o "
                                    "lentas (7414)."),
                ("Ripple carry", "Sumador donde el acarreo se propaga en cadena etapa por etapa.")],
         note="Consejo de estudio: no memorizar el glosario completo, sino entender cómo se "
              "relaciona cada término con una decisión de diseño concreta.",
         notes="Cerrar el bloque teórico con esta lámina."),

    dict(kind="cards", section=6, transition="fade",
         title="Fuentes de consulta y verificación",
         lead="Dónde comprobar cada dato antes de cablear o de publicar.",
         cols=2,
         cards=[dict(title="Hojas de datos oficiales", accent="cyan", num="PDF",
                     body="Texas Instruments (SN74LS00), ON Semiconductor, NXP y ST publican "
                          "datasheets gratuitos con todos los parámetros. Es la única fuente que "
                          "se considera válida para un reporte técnico."),
                dict(title="Bibliografía clásica", accent="orange", num="LIB",
                     body="**Digital Fundamentals** (Thomas Floyd), **Sistemas Digitales: "
                          "Principios y Aplicaciones** (Tocci), **Diseño Digital** (Morris Mano): "
                          "los tres cubren compuertas, familias y práctica."),
                dict(title="Simuladores y herramientas", accent="green", num="SIM",
                     body="Logisim Evolution, Tinkercad Circuits, Multisim, Proteus, KiCad y "
                          "Falstad permiten validar el diseño antes del montaje físico."),
                dict(title="Recursos audiovisuales", accent="purple", num="WEB",
                     body="Canales técnicos como The Engineering Mindset, All About Circuits, "
                          "Electronics Tutorials y el canal oficial de Texas Instruments."),
                dict(title="Crédito de las imágenes", accent="pink", num="IMG",
                     body="Fotografías originales del autor de la presentación y de las fuentes "
                          "citadas en la diapositiva de referencias (electronics-lab.com, "
                          "hackster.io). Diagramas técnicos generados para esta guía."),
                dict(title="Verificación de datos", accent="blue", num="CHK",
                     body="Todos los parámetros se tomaron de las hojas de datos de la serie "
                          "74LS y se recomienda verificarlos contra el PDF del fabricante antes "
                          "de usarlos en un diseño industrial.")],
         note="Dato verificable en todos los datasheets: VCC nominal de 5 V, VIH mínima de 2 V y "
              "VIL máxima de 0.8 V. Son los tres números que jamás cambian en la familia TTL "
              "estándar.",
         notes="Recomendar la lectura de Floyd para profundizar."),

    dict(kind="gallery", section=6, transition="fade",
         title="Del transistor al microprocesador: la vigencia de la Serie 74XX",
         lead="Cierre técnico: por qué seguir estudiando integrados de 1963 en pleno siglo XXI.",
         cols=2, accent="cyan",
         photos=[(s("hero_chip.png"), "Integrado 74LS00 real sobre placa: la misma función "
                                      "lógica que ejecutan los miles de millones de compuertas "
                                      "de un procesador actual."),
                 (p("fabrication"), "El proceso de fabricación de integrados ha escalado durante "
                                    "más de sesenta años, pero el álgebra de Boole que lo "
                                    "gobierna es la misma.")],
         items=["**Escalabilidad conceptual:** un microprocesador no es más que millones de "
                "compuertas NAND, NOR y biestables interconectados.",
                "**Valor didáctico:** con un chip de 5 pesos se puede ver, medir y tocar el "
                "principio que rige a la electrónica digital.",
                "**Aplicaciones actuales:** los integrados 74XX siguen usándose en conversión de "
                "niveles, control de LEDs, temporización simple, prototipos educativos y "
                "reparación de equipos.",
                "**Compatibilidad histórica:** el mismo código de función (00, 08, 32, 86) "
                "sobrevive desde 1963 con el mismo pinout.",
                "**Competencia moderna:** el microcontrolador reemplaza muchas funciones, pero no "
                "enseña con la misma claridad el funcionamiento interno.",
                "**Cierre:** comprender la lógica digital a nivel de compuerta es la base para "
                "entender las FPGAs, los procesadores y cualquier sistema digital moderno."],
         note="La electrónica digital no se volvió obsoleta: se volvió invisible dentro de "
              "chips cada vez más integrados, con la misma lógica de 0 y 1 en su interior.",
         notes="Cerrar con una reflexión sobre el aprendizaje."),

    dict(kind="bullets", section=6, transition="wipe",
         title="Autoevaluación: 12 preguntas para repasar",
         lead="Intenta responder sin mirar las diapositivas anteriores.",
         two_col=True, per=4, size=11.4, gap=0.06,
         items=["1. ¿Cuál es la diferencia entre una señal analógica y una digital?",
                "2. ¿Qué tensión se considera un nivel alto garantizado en TTL?",
                "3. ¿Qué significa el margen de ruido de 0.4 V en TTL?",
                "4. ¿Por qué la compuerta NAND es universal?",
                "5. ¿Cuál es la diferencia entre VIL y VOL?",
                "6. ¿Qué chip implementa la función XOR y cuántas compuertas tiene?",
                "7. ¿Cuál es la diferencia entre el 7400 y el 7402, además de la función?",
                "8. ¿Por qué el 74266 requiere una resistencia pull-up?",
                "9. ¿Qué significa fan-out y cuánto vale en TTL estándar?",
                "10. ¿Cómo se construye un medio sumador con compuertas?",
                "11. ¿Cuál es la diferencia entre un latch y un flip-flop?",
                "12. ¿Qué se verifica primero cuando un circuito digital no funciona?"],
         note="Respuestas clave: (2) 2.0 V, (3) la tolerancia a interferencia, (5) VIL es un "
              "umbral de entrada y VOL una garantía de salida, (8) su salida es de colector "
              "abierto, (9) 10 entradas, (12) la alimentación.",
         note_label="RESPUESTAS", notes="Repartir como cuestionario escrito.") ,

    dict(kind="contact", section=6, transition="fade",
         title="¿Preguntas o dudas?",
         subtitle="Electrónica Digital · Compuertas Lógicas y Chips Serie 74XX",
         body="Guía técnica ampliada con fundamentos, compuertas, hojas de datos, aplicaciones, "
              "práctica de laboratorio, glosario y recursos. Todas las diapositivas incluyen "
              "transición y entradas animadas para exposición por bloques.",
         chips=["TTL 74XX", "7400 · 7408 · 7432", "7402 · 7486 · 74266", "Lógica combinacional",
                "Lógica secuencial", "Laboratorio"],
         img=s("image14.png"),
         foot="Compuertas Lógicas y Chips Serie 74XX · Guía técnica ampliada · 2026",
         notes="Agradecer la atención y abrir la ronda de preguntas."),
]
