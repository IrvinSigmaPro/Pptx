# -*- coding: utf-8 -*-
"""Sección 3 — Hoja de datos, tiempos y parámetros eléctricos."""
import os
from theme import SRC, GEN


def p(n):
    return os.path.join(GEN, n + ".png")


def s(n):
    return os.path.join(SRC, n)


SLIDES = [
    dict(kind="section", section=3, transition="zoom",
         img=p("sec_data"), topics=[
             "Cómo leer una hoja de datos: absolute maximum ratings y recommended operating conditions",
             "Parámetros eléctricos DC: VIL, VIH, VOL, VOH, IIH, IIL, IOH, IOL",
             "Tiempos de conmutación: tPLH, tPHL, tPD, tiempos de subida y bajada",
             "Fan-out, fan-in y cálculo de cargas conectadas a una salida",
             "Familias lógicas TTL y CMOS: comparación de velocidad, consumo y compatibilidad",
             "Encapsulados, nomenclatura, temperatura y protección electrostática"],
         notes="Apertura del bloque 3."),

    # ---------------------------------------------------------------- portada datasheet
    dict(kind="gallery", section=3, transition="fade",
         title="Anatomía de una hoja de datos (datasheet)",
         lead="Todo manual del fabricante sigue la misma estructura; reconocerla ahorra horas de trabajo.",
         cols=1, accent="purple",
         photos=[(p("pin_7400"), "Ejemplo real: el datasheet del 7400 siempre incluye "
                                 "descripción general, tabla de función, diagrama de pines, "
                                 "esquema lógico y tablas de parámetros eléctricos.")],
         items=["**1. Descripción general:** nombre comercial, función y número de compuertas del "
                "integrado.",
                "**2. Diagrama de conexiones (pinout):** dibujo del encapsulado con el nombre de "
                "cada pin; es la primera hoja que se consulta.",
                "**3. Tabla de función / tabla de verdad:** indica la salida para cada combinación "
                "de entradas, incluyendo los estados de alta impedancia (Z) o prohibidos (X).",
                "**4. Esquema lógico equivalente:** muestra la estructura interna y sirve para "
                "entender entradas flotantes y corrientes de entrada.",
                "**5. Absolute maximum ratings:** límites que NO deben alcanzarse nunca "
                "(típicamente −0.5 V a +7 V en VCC).",
                "**6. Recommended operating conditions:** rango en el que el fabricante garantiza "
                "el funcionamiento (4.75 V a 5.25 V, 0 °C a 70 °C).",
                "**7. Parámetros eléctricos (DC):** VIL, VIH, VOL, VOH, corrientes de entrada y "
                "salida.",
                "**8. Parámetros de conmutación (AC):** tPLH, tPHL, tiempos de subida y bajada, "
                "frecuencia máxima.",
                "**9. Curvas típicas y notas de aplicación:** gráficas de comportamiento frente a "
                "temperatura, carga y tensión de alimentación."],
         note="Consejo profesional: antes de cablear se leen SOLO tres cosas: el pinout, la tabla "
              "de función y el rango de VCC. El resto se consulta cuando aparece un problema real.",
         notes="Mostrar un datasheet impreso si es posible."),

    # ---------------------------------------------------------------- absolut. max
    dict(kind="table", section=3, transition="wipe",
         title="Límites absolutos máximos (Absolute Maximum Ratings)",
         lead="Valores que destruyen el chip si se superan, aunque sea por un instante.",
         header=["Parámetro", "Símbolo", "Valor límite", "Consecuencia si se supera"],
         widths=[0.30, 0.14, 0.20, 0.36], accent="red", size=10.8, row_h=0.50,
         rows=[["Tensión de alimentación", "VCC", "−0.5 V a +7.0 V",
                "Destrucción del chip: superar 7 V perfora las uniones internas"],
               ["Tensión de entrada", "VI", "−0.5 V a +5.5 V",
                "Corriente excesiva por los diodos de protección de entrada"],
               ["Corriente de salida", "IO", "±25 mA por pin (LS)",
                "Sobrecalentamiento del transistor de salida y pérdida de nivel"],
               ["Temperatura de almacenamiento", "Tstg", "−65 °C a +150 °C",
                "Daño mecánico y del encapsulado por dilatación"],
               ["Temperatura de la unión", "TJ", "+150 °C máximo",
                "Falla térmica inmediata y pérdida de las características"],
               ["Temperatura de soldadura (10 s)", "TL", "+260 °C",
                "Deformación del plástico y desplazamiento de los pines"],
               ["Disipación del encapsulado", "PD", "≈ 500 mW (DIP-14)",
                "Aumento de temperatura interno por encima de lo tolerado"]],
         note="Advertencia de taller: invertir la alimentación (VCC a GND y GND a VCC) es la "
              "causa número uno de chips muertos en prácticas estudiantiles. Antes de conectar la "
              "fuente, verificar con el multímetro en modo continuidad que VCC y GND no estén en "
              "corto.",
         note_label="¡CUIDADO!", notes="Enfatizar la verificación previa del cableado."),

    # ---------------------------------------------------------------- eléctricos DC
    dict(kind="table", section=3, transition="wipe",
         title="Parámetros eléctricos recomendados (DC) del 74LS00",
         lead="Las condiciones en las que el fabricante garantiza los niveles lógicos.",
         header=["Parámetro", "Pin", "Mín.", "Típ.", "Máx.", "Unidad", "Qué significa"],
         widths=[0.10, 0.09, 0.09, 0.09, 0.09, 0.09, 0.45], accent="purple", size=10.2, row_h=0.40,
         rows=[["VCC", "14", "4.75", "5.0", "5.25", "V", "Tensión de alimentación garantizada"],
               ["VIH", "entrada", "2.0", "—", "—", "V", "Mínima tensión que se lee como nivel alto"],
               ["VIL", "entrada", "—", "—", "0.8", "V", "Máxima tensión que se lee como nivel bajo"],
               ["VOH", "salida", "2.7", "3.4", "—", "V", "Mínima tensión entregada como nivel alto"],
               ["VOL", "salida", "—", "0.25", "0.5", "V", "Máxima tensión entregada como '0'"],
               ["IIH", "entrada", "—", "—", "20", "µA", "Corriente que absorbe una entrada en alto"],
               ["IIL", "entrada", "—", "—", "−0.4", "mA", "Corriente que entrega una entrada en bajo"],
               ["IOH", "salida", "—", "−0.4", "−0.8", "mA", "Corriente máxima entregada en nivel alto"],
               ["IOL", "salida", "—", "8.0", "16", "mA", "Corriente máxima absorbida en nivel bajo"],
               ["IOS", "salida", "−20", "—", "−100", "mA", "Corriente de cortocircuito momentánea"],
               ["ICC", "VCC", "—", "1.6", "3.4", "mA", "Consumo total del integrado en reposo"]],
         note="Contraste clave: el TTL absorbe 16 mA en bajo pero solo entrega 0.4 mA en alto. "
              "Por eso se encienden LEDs y se manejan cargas conectándolas entre la salida y VCC "
              "(lógica de sumidero), no entre la salida y GND.",
         note_label="LECTURA DE LA TABLA", notes="Explicar por qué el LED va a VCC en TTL."),

    dict(kind="gallery", section=3, transition="fade",
         title="Tiempo de propagación y límites de frecuencia",
         lead="El retardo entre causa y efecto que define la velocidad máxima del circuito.",
         cols=2, accent="orange",
         photos=[(p("prop_delay"), "El retardo de propagación tPD se mide entre el 50 % del "
                                   "flanco de entrada y el 50 % del flanco correspondiente de "
                                   "salida."),
                 (p("time_nand"), "En cadenas largas de compuertas los retardos se suman; el "
                                  "circuito puede dejar de funcionar si el pulso es más corto "
                                  "que el retardo acumulado.")],
         items=["**tPLH:** retardo de propagación de nivel bajo a nivel alto (salida subiendo).",
                "**tPHL:** retardo de propagación de nivel alto a nivel bajo (salida bajando).",
                "**tPD promedio:** 8 a 15 ns en la subfamilia 74LS; en 74HC baja a 8 ns y en 74F "
                "llega a 3 ns.",
                "**Frecuencia máxima:** en un contador de n etapas, fMÁX ≈ 1 / (2·n·tPD). Para 4 "
                "etapas y tPD = 10 ns, fMÁX ≈ 12.5 MHz.",
                "**Tiempo de subida/bajada:** 15 ns típicos en LS; afectan la integridad de la "
                "señal en pistas largas.",
                "**Riesgos (hazards):** diferencias de retardo entre rutas pueden producir pulsos "
                "falsos; se corrigen con un capacitor o añadiendo un registro.",
                "**Diseño seguro:** si se necesita alta velocidad, usar 74F, 74ACT o cambiar a "
                "una tecnología moderna de 3.3 V."],
         note="Un circuito digital no es 'instantáneo': cada compuerta cobra un peaje de "
              "nanosegundos. En osciloscopios educativos el retardo es invisible, pero en "
              "diseños de decenas de MHz se vuelve el factor dominante.",
         notes="Relacionar tPD con la frecuencia máxima de un contador."),

    # ---------------------------------------------------------------- AC table
    dict(kind="table", section=3, transition="wipe",
         title="Parámetros de conmutación (AC) comparados por subfamilia",
         lead="El mismo chip cambia de velocidad y consumo según la tecnología usada.",
         header=["Subfamilia", "tPD típico (ns)", "fMÁX típica", "IOH/IOL (mA)", "Consumo por compuerta"],
         widths=[0.20, 0.18, 0.18, 0.18, 0.26], accent="orange", size=10.8, row_h=0.42,
         rows=[["74 (estándar)", "10", "25 MHz", "−0.4 / 16", "10 mW"],
               ["74L (bajo consumo)", "33", "8 MHz", "−0.2 / 3.6", "1 mW"],
               ["74LS (Schottky baja potencia)", "9.5", "30 MHz", "−0.4 / 8", "2 mW"],
               ["74S (Schottky)", "3", "60 MHz", "−1 / 20", "20 mW"],
               ["74ALS (avanzada)", "4", "50 MHz", "−0.4 / 8", "1.2 mW"],
               ["74F (rápida)", "3", "100 MHz", "−1 / 20", "4.5 mW"],
               ["74HC (CMOS alta velocidad)", "8", "40 MHz", "−4 / 4", "0.02 mW"],
               ["74HCT (CMOS compatible TTL)", "9", "35 MHz", "−4 / 4", "0.02 mW"],
               ["74AHC / 74LVC (modernos)", "3", ">100 MHz", "±8 / ±8", "≈ 0 en reposo"]],
         note="Criterio de elección: si el circuito es lento y alimentado por batería, elegir HC; "
              "si debe convivir con lógica TTL, elegir LS o HCT; si se requiere velocidad, F o "
              "LVC. Nunca mezclar HC con LS sin revisar los umbrales.",
         note_label="CRITERIO DE DISEÑO", notes="Explicar que 74HC a 5 V tiene umbrales 2.5 V."),

    dict(kind="gallery", section=3, transition="fade",
         title="Fan-out: cuántas entradas soporta una salida",
         lead="El límite práctico que explica por qué un LED se atenúa cuando se conectan más cargas.",
         cols=2, accent="green",
         photos=[(p("fanout"), "Una salida TTL estándar puede gobernar hasta 10 entradas de la "
                               "misma familia sin salir de los niveles garantizados."),
                 (p("power_setup"), "Montaje típico: 5 V estables, capacitor de desacople de "
                                    "100 nF junto al chip y resistencia en serie con el LED de "
                                    "salida.")],
         items=["**Definición:** número máximo de entradas de la misma familia que una salida "
                "puede controlar respetando VOH y VOL.",
                "**Cálculo en alto:** 10 entradas × 20 µA = 200 µA, menor que IOH de 400 µA "
                "garantizados.",
                "**Cálculo en bajo:** 10 entradas × 0.4 mA = 4 mA, menor que IOL de 8 mA.",
                "**Fan-out en TTL estándar:** 10. En 74LS también 10; en 74HC depende de la "
                "corriente de entrada (típicamente 10 a 20).",
                "**Si se excede el fan-out:** los niveles se degradan, aparecen errores "
                "intermitentes y aumenta la temperatura del chip.",
                "**Solución:** añadir un buffer (7404, 7407, 74LS244) o dividir la carga en dos "
                "salidas distintas.",
                "**Separar fan-out de carga resistiva:** encender un LED exige 10 mA y consume "
                "casi todo el presupuesto de corriente de una salida TTL: conviene usar "
                "transistor o driver dedicado."],
         note="Ejemplo concreto: la salida de un 74LS00 puede encender un LED de 10 mA o "
              "alimentar 10 entradas lógicas, pero no ambas cosas sin exceder el límite de "
              "corriente.",
         notes="Explicar el cálculo numérico completo."),

    dict(kind="cards", section=3, transition="fade",
         title="Familias lógicas: TTL vs. CMOS y sus variantes",
         lead="La misma función lógica, distintas tripas: velocidad, consumo y robustez.",
         cols=2,
         cards=[dict(title="TTL bipolar (74XX, 74LS, 74S, 74F)", accent="orange", num="TTL",
                     body="Usa transistores de unión bipolar (BJT). Es rápida, robusta y muy "
                          "tolerante a ESD, pero consume corriente de forma continua y exige una "
                          "alimentación muy estable de 5 V."),
                dict(title="CMOS (74HC, 74HCT, 4000)", accent="cyan", num="CMOS",
                     body="Usa pares de transistores MOSFET complementarios. Consumo casi nulo en "
                          "reposo, margen de ruido mayor y rango de alimentación amplio (2 V a 6 "
                          "V), pero es sensible a la electricidad estática."),
                dict(title="BiCMOS y variantes modernas", accent="purple", num="Bi",
                     body="Combinan entrada CMOS con salida bipolar para lograr velocidad TTL y "
                          "consumo CMOS: familias 74ABT, 74ACT, 74LVC. Son las que se usan hoy en "
                          "placas comerciales."),
                dict(title="Lógica de 3 estados y colector abierto", accent="green", num="Z",
                     body="Las salidas de tres estados (Z) permiten conectar varios chips a un "
                          "mismo bus apagándolos por el pin OE. Las de colector abierto permiten "
                          "lógica cableada con una resistencia pull-up compartida.")],
         note="Regla de oro de compatibilidad: una salida TTL alimenta con seguridad una entrada "
              "CMOS-HCT; una salida CMOS-HC alimenta sin problemas una entrada TTL, pero una "
              "entrada HC no reconoce bien una salida TTL estándar por el umbral desplazado.",
         note_label="REGLA DE COMPATIBILIDAD", notes="Explicar por qué existe el HCT."),

    dict(kind="gallery", section=3, transition="fade",
         title="Tabla gráfica de familias y consumo",
         lead="Comparación visual de velocidad y disipación por compuerta.",
         cols=2, accent="cyan",
         photos=[(p("families"), "Gráfica comparativa: las familias modernas (ALS, F, HC) logran "
                                 "relaciones velocidad/consumo muy superiores a la TTL original."),
                 (p("family_tree"), "Árbol de la familia 74XX: la estructura del código permite "
                                    "identificar la tecnología, la función y el encapsulado.")],
         items=["**TTL original (1963):** 10 ns y 10 mW por compuerta; hoy obsoleta pero "
                "didáctica.",
                "**74L:** redujo el consumo a costa de velocidad; se usó en equipos portátiles de "
                "los años setenta.",
                "**74LS (1977):** el equilibrio histórico; sigue fabricándose y es el estándar de "
                "la enseñanza.",
                "**74S y 74F:** para computadoras de los años ochenta; 20 mW por compuerta.",
                "**74ALS:** versión mejorada del LS, con menor consumo y mayor velocidad.",
                "**74HC / HCT:** la generación CMOS actual, con consumo prácticamente nulo en "
                "reposo.",
                "**74AHC / LVC:** optimizadas para 3.3 V y 1.8 V, con frecuencias de más de 100 "
                "MHz."],
         note="El dato moderno convive con el histórico: los chips modernos consumen "
              "millonésimas de vatio por compuerta, pero el principio lógico y la tabla de verdad "
              "son exactamente los mismos que en 1963.",
         notes="Relacionar consumo con aplicaciones portátiles."),

    dict(kind="table", section=3, transition="wipe",
         title="Nomenclatura de encapsulados y cómo pedir el chip correcto",
         lead="El sufijo del código indica el tipo de encapsulado, no la función lógica.",
         header=["Sufijo típico", "Encapsulado", "Pines disponibles", "Uso recomendado"],
         widths=[0.16, 0.22, 0.20, 0.42], accent="purple", size=10.8, row_h=0.42,
         rows=[["N", "DIP plástico (DIP-14/16)", "14, 16, 20, 24", "Protoboard y prácticas de laboratorio"],
               ["D", "SOIC SMD", "14, 16", "Placas comerciales de inserción superficial"],
               ["PW / TSSOP", "TSSOP muy delgado", "14, 16", "Equipos compactos y portátiles"],
               ["DB / SSOP", "SSOP", "16, 20", "Instrumentación y módulos industriales"],
               ["FK", "LCCC cerámico", "20, 28", "Uso militar y aeroespacial (serie 54XX)"],
               ["J / W", "Cerámico DIP", "14, 16", "Ambientes de temperatura extrema"],
               ["Sin sufijo", "Según fabricante", "Variable", "Consultar siempre el datasheet"]],
         note="Cómo leer un código completo: **SN74LS00N** = Semiconductor Network, familia 74, "
              "tecnología LS (Schottky de baja potencia), función 00 (NAND cuádruple), "
              "encapsulado N (DIP plástico).",
         note_label="LECTURA DEL CÓDIGO", notes="Practicar la lectura con varios códigos reales."),

    dict(kind="gallery", section=3, transition="fade",
         title="Estructura interna: del transistor a la compuerta",
         lead="Por qué el TTL absorbe mejor que entrega, y por qué el CMOS casi no consume.",
         cols=2, accent="teal",
         photos=[(p("cmos"), "Estructura CMOS de un inversor: el transistor PMOS conduce en el "
                             "nivel alto y el NMOS en el bajo, nunca ambos a la vez."),
                 (p("fabrication"), "Del silicio al circuito impreso: oblea, litografía, "
                                    "encapsulado y montaje final en placa."),
                 (s("image16.png"), "Oblea de silicio (wafer) con cientos de circuitos "
                                    "integrados antes de cortarse en dados. Imagen: "
                                    "magnific.com.")],
         items=["**Etapa de entrada TTL:** un transistor multiemisor que se comporta como '1' "
                "flotante y consume corriente cuando la entrada está en bajo (IIL = 0.4 mA).",
                "**Etapa de salida TTL (totem-pole):** dos transistores en serie; el inferior "
                "(NPN) absorbe corriente con eficiencia, el superior entrega muy poca.",
                "**Estructura CMOS:** par complementario NMOS/PMOS; en estado estable uno de los "
                "dos está apagado y no circula corriente.",
                "**Corriente de conmutación CMOS:** solo fluye durante las transiciones, y crece "
                "con la frecuencia: P ≈ C·V²·f.",
                "**Protección de entrada:** los chips CMOS incluyen diodos hacia VCC y GND que "
                "absorben descargas pequeñas, pero no resisten ESD fuerte.",
                "**Encapsulado:** el die de silicio se pega al marco y se conecta por hilos de "
                "oro (wire bonding) a los pines; el plástico lo sella."],
         note="Consecuencia práctica: en TTL, conectar la carga entre la salida y VCC (sumidero); "
              "en CMOS da igual porque entrega y absorbe corriente de forma simétrica.",
         notes="Explicar la diferencia con un diagrama de transistores si hay tiempo."),

    dict(kind="table", section=3, transition="wipe",
         title="Comparación TTL vs. CMOS: qué mirar antes de elegir",
         lead="Tabla de decisión entre las dos tecnologías.",
         header=["Criterio", "TTL (74LS)", "CMOS (74HC / HCT)", "Comentario práctico"],
         widths=[0.22, 0.24, 0.24, 0.30], accent="teal", size=10.8, row_h=0.44,
         rows=[["Tensión de alimentación", "5 V ± 5 %", "2 V a 6 V", "CMOS tolera fuentes variables"],
               ["Umbral de entrada (VIH)", "2.0 V", "3.5 V a 5 V (HC) / 2.0 V (HCT)",
                "HC no reconoce bien una salida TTL"],
               ["Margen de ruido", "0.4 V", "1.5 V o más", "CMOS es mucho más inmune al ruido"],
               ["Consumo en reposo", "1.6 mA por chip", "≈ 1 µA por chip", "Decisivo en equipos a batería"],
               ["Disipación por compuerta", "2 mW", "0.02 mW", "CMOS disipa 100 veces menos"],
               ["Velocidad (tPD)", "9.5 ns", "8 ns", "Comparables en la práctica"],
               ["Corriente de salida", "±8 mA", "±4 mA", "TTL LS maneja más corriente"],
               ["Sensibilidad a ESD", "Baja", "Alta", "CMOS exige pulsera y tapete"],
               ["Entradas flotantes", "Se leen como '1' por diseño", "Prohibidas: oscilan",
                "En CMOS hay que fijar siempre la entrada"],
               ["Compatibilidad con TTL", "Nativa", "Requiere versión HCT", "Elegir HCT para mezclar"]],
         note="Elección estándar en prácticas: 74LS cuando se necesita corriente y robustez; "
              "74HC cuando se busca bajo consumo y mayor margen de ruido; 74HCT cuando hay que "
              "mezclar ambos mundos.",
         note_label="DECISIÓN PRÁCTICA", notes="Puede usarse como rúbrica de comparación."),

    dict(kind="gallery", section=3, transition="fade",
         title="Protección electrostática (ESD) y cuidado del integrado",
         lead="El enemigo invisible: una descarga que no se siente puede dañar un chip CMOS.",
         cols=2, accent="purple",
         photos=[(p("esd"), "Buenas prácticas: pulsera antiestática, tapete disipativo, "
                            "almacenamiento en tubo conductivo y nunca insertar el chip con la "
                            "alimentación encendida."),
                 (s("image6.png"), "Integrados en encapsulado DIP: los pines son el punto de "
                                   "entrada de las descargas electrostáticas durante el manejo.")],
         items=["**Origen de la descarga:** el cuerpo humano acumula hasta 10 kV; el movimiento "
                "sobre una alfombra puede superar los 20 kV.",
                "**Umbral de daño:** los chips CMOS modernos pueden dañarse con tensiones de "
                "apenas 50 V en una entrada, muy por debajo del nivel perceptible.",
                "**Daño latente:** el chip puede quedar degradado y fallar días después, con "
                "comportamiento errático difícil de diagnosticar.",
                "**Pulsera antiestática:** debe incluir resistencia de 1 MΩ para seguridad "
                "eléctrica del usuario.",
                "**Almacenamiento:** tubos plásticos conductivos o bolsas metalizadas; nunca "
                "espuma común sin protección.",
                "**Al soldar:** usar cautín con conexión a tierra y evitar chips con la "
                "alimentación activa.",
                "**Verificación:** si un chip se comporta de forma errática y el cableado ya se "
                "revisó, sustituirlo por otro es la prueba definitiva."],
         note="En el laboratorio de la escuela las descargas se acumulan con la ropa de invierno y "
              "el calzado con suela de goma: la pulsera antiestática no es un adorno, evita "
              "perder un chip de la práctica.",
         notes="Incluir la rutina de manejo al inicio de cada práctica."),
]
