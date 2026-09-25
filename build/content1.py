# -*- coding: utf-8 -*-
"""Sección 1 — Fundamentos de la lógica digital (diapositivas 1-24)."""
import os
import theme
from theme import SRC


def p(name):
    return os.path.join(theme.GEN, name + ".png")


def s(name):
    return os.path.join(SRC, name)


SLIDES = [
    # ------------------------------------------------------------------ 1
    dict(kind="hero", section=1, transition="fade",
         img=s("hero_chip.png"),
         kicker="GUÍA TÉCNICA · ELECTRÓNICA DIGITAL · EDICIÓN AMPLIADA",
         title="Compuertas Lógicas y Chips Serie 74XX",
         subtitle="De los fundamentos de Boole al montaje real en laboratorio: teoría, hoja de datos, "
                  "diagramas de tiempo, aplicaciones y práctica guiada.",
         body="Recorrido completo por las compuertas AND, OR, NOT, NAND, NOR, XOR y XNOR; el "
              "funcionamiento interno de la familia TTL 74XX; las subfamilias 74LS, 74S, 74F, 74HC "
              "y 74HCT; los parámetros eléctricos de una hoja de datos; y los circuitos integrados "
              "que se construyen con ellos: sumadores, multiplexores, decodificadores, contadores, "
              "registros y memorias.",
         stats=[("7", "compuertas lógicas fundamentales"),
                ("6+", "chips 74XX estudiados a detalle"),
                ("40+", "diagramas, tablas y esquemas"),
                ("100", "diapositivas con transiciones y animaciones")],
         foot="Compuertas Lógicas y Chips Serie 74XX · Guía técnica ampliada · 2026",
         notes="Presentación de apertura. Cada diapositiva tiene transición y entradas animadas por "
               "clic. Comentar el alcance general: fundamentos, compuertas, hoja de datos, "
               "aplicaciones, laboratorio y repaso."),

    # ------------------------------------------------------------------ 2
    dict(kind="toc", section=1, transition="fade",
         title="Contenido de la guía",
         lead="Seis bloques temáticos que van de la teoría básica hasta la verificación en el laboratorio.",
         items=[("01", "Fundamentos de la lógica digital",
                 "Sistema binario, códigos, niveles lógicos, ruido, álgebra de Boole, De Morgan, "
                 "Karnaugh y formas canónicas.", "Diapositivas 3 – 24"),
                ("02", "Compuertas lógicas y chips 74XX",
                 "AND 7408, OR 7432, NOT 7404, NAND 7400, NOR 7402, XOR 7486 y XNOR 74266 con "
                 "símbolo, tabla de verdad y pinout.", "Diapositivas 25 – 50"),
                ("03", "Hoja de datos, tiempos y parámetros",
                 "VCC, retardo de propagación, fan-out, inmunidad al ruido, familias lógicas TTL y "
                 "CMOS, encapsulados y ESD.", "Diapositivas 51 – 65"),
                ("04", "Aplicaciones reales",
                 "Sumadores, multiplexores, decodificadores, codificadores, displays, latches, "
                 "flip-flops, contadores, registros y memorias.", "Diapositivas 66 – 81"),
                ("05", "Práctica de laboratorio y diagnóstico",
                 "Montaje en protoboard, alimentación y desacople, medición, punta lógica y "
                 "resolución de fallas paso a paso.", "Diapositivas 82 – 92"),
                ("06", "Repaso, glosario y recursos",
                 "Resumen comparativo de compuertas y chips, catálogo ampliado 74XX, glosario "
                 "técnico y fuentes de consulta.", "Diapositivas 93 – 100")],
         notes="Usar esta lámina como mapa de navegación durante toda la presentación."),

    # ------------------------------------------------------------------ 3
    dict(kind="section", section=1, transition="zoom",
         img=p("sec_fund"), topics=[
             "Qué es una señal digital y por qué domina la electrónica moderna",
             "Sistema binario, bits, bytes y códigos (BCD, Gray, ASCII)",
             "Niveles lógicos TTL: VIL, VIH, VOL, VOH y márgenes de ruido",
             "Álgebra de Boole, teoremas, De Morgan y simplificación con Karnaugh",
             "Diferencia entre lógica combinacional y lógica secuencial"],
         notes="Apertura del bloque 1."),

    # ------------------------------------------------------------------ 4
    dict(kind="bullets", section=1, transition="wipe",
         title="¿Qué es la electrónica digital?",
         lead="Una señal digital solo admite dos estados válidos y todo lo demás se interpreta como error.",
         two_col=True, per=3,
         items=["La **electrónica digital** trabaja con señales que solo pueden tomar dos valores "
                "discretos: nivel **ALTO ('1')** o nivel **BAJO ('0')**. Todo valor intermedio es "
                "una zona prohibida que el circuito no debe interpretar como dato válido.",
                "Los dos estados se representan con **tensiones eléctricas**: en la familia TTL, "
                "aproximadamente **0 V = '0'** y **5 V = '1'**; en CMOS moderno se usan 3.3 V o "
                "1.8 V con la misma idea.",
                "El estado '1' y el '0' reciben el nombre de **bit** (binary digit, dígito "
                "binario), y los bits se agrupan en **nibbles** (4 bits), **bytes** (8 bits), "
                "**palabras** (16, 32 o 64 bits) y bloques de memoria.",
                "La gran ventaja es la **inmunidad al ruido** frente a la electrónica analógica: "
                "un pequeño voltaje parásito no cambia el valor lógico, salvo que cruce el umbral "
                "de decisión.",
                "Las **compuertas lógicas** son los ladrillos elementales: implementan una función "
                "booleana con transistores y producen una salida digital a partir de una o varias "
                "entradas digitales.",
                "Con compuertas se construyen **sumadores, comparadores, contadores, memorias y "
                "microprocesadores**: un procesador moderno contiene miles de millones de "
                "compuertas elementales.",
                "La **Serie 74XX** es el catálogo de integrados lógicos más importante de la "
                "historia: desde 1963 sigue vigente por su bajo costo, disponibilidad y valor "
                "didáctico.",
                "En el laboratorio el chip se alimenta con **+5 V ± 5 %** entre los pines VCC y "
                "GND, y todas las señales de entrada y salida se miden respecto a ese GND común."],
         note="Escala de la lógica digital: un solo chip 7400 (4 compuertas) contiene 24 "
              "transistores; un microprocesador actual contiene más de 30 000 millones. El "
              "principio de funcionamiento es el mismo: manipular bits.",
         notes="Explicar la diferencia entre valor lógico y valor de tensión."),

    # ------------------------------------------------------------------ 5
    dict(kind="twocol", section=1, transition="wipe",
         title="Mundo analógico vs. mundo digital",
         lead="Comparación de los dos enfoques; la guía trabaja exclusivamente el enfoque digital.",
         accent="cyan",
         left=dict(title="Señal analógica", accent="orange", items=[
             "Toma **infinitos valores** dentro de un rango continuo (0 V … 5 V, sin escalones).",
             "Cualquier perturbación se suma al valor: **el ruido no se puede eliminar**, solo filtrar.",
             "Requiere **conversión a digital** (ADC) para ser procesada por un chip digital.",
             "Ejemplos: audio de un micrófono, salida de un termistor o de un LDR, señal de un "
             "potenciómetro.",
             "Su precisión depende de tolerancias, temperatura y calidad de los componentes.",
             "Procesarla exige amplificadores operacionales, filtros y etapas lineales."]),
         right=dict(title="Señal digital", accent="cyan", items=[
             "Solo admite **dos estados discretos** ('0' y '1'), representados por bandas de "
             "tensión.",
             "El ruido por debajo del margen de ruido **no altera** el dato transmitido.",
             "Se procesa directamente con compuertas y se **almacena** en biestables.",
             "Ejemplos: salida de una compuerta, bit de memoria, dato de un bus, estado de un "
             "contador.",
             "La exactitud se define por **niveles garantizados** en la hoja de datos (VIL, VIH).",
             "Se vuelve a convertir a analógico con un **DAC** cuando hay que mover un parlante o "
             "un motor."]),
         note="Regla práctica: el mundo físico es analógico y el mundo de los datos es digital; "
              "los chips de la Serie 74XX son el puente entre ambos cuando se combinan con "
              "sensores y convertidores.",
         notes="Dar ejemplos del aula: luz de un LED vs. intensidad de un LED."),

    # ------------------------------------------------------------------ 6
    dict(kind="cards", section=1, transition="wipe",
         title="Señales, variables y funciones lógicas",
         lead="Vocabulario mínimo indispensable antes de tocar una compuerta.",
         cols=3, effect="rise",
         cards=[dict(title="Variable de entrada", num="A/B", accent="cyan",
                     body="Símbolo cuyo valor puede ser 0 o 1. Se nombran con letras (A, B, Cin, "
                          "CLK, OE) y representan el estado de un pin físico del integrado."),
                dict(title="Función lógica", num="Y", accent="orange",
                     body="Combinación booleana de las entradas que define la salida. Se escribe "
                          "como ecuación (Y = A·B) o como tabla de verdad con todas las "
                          "combinaciones."),
                dict(title="Tabla de verdad", num="∑", accent="green",
                     body="Lista exhaustiva de entradas y salida. Con n entradas hay 2^n filas: "
                          "2, 4, 8, 16… Es la descripción más honesta del comportamiento del "
                          "circuito."),
                dict(title="Nivel activo", num="HI/LO", accent="purple",
                     body="Indica el estado que 'activa' la función. Un pin con línea superior "
                          "(OE) o asterisco es activo en bajo: hace su función con '0' lógico."),
                dict(title="Retardo (tPD)", num="ns", accent="pink",
                     body="Tiempo entre el cambio de entrada y el cambio efectivo de salida. En "
                          "74LS ronda 8–15 ns; determina la frecuencia máxima de trabajo."),
                dict(title="Fan-out", num="10", accent="blue",
                     body="Número de entradas de la misma familia que puede gobernar una sola "
                          "salida sin degradar los niveles garantizados (10 en TTL estándar).")],
         note="Con estos seis conceptos se puede leer cualquier hoja de datos de la familia 74XX, "
              "desde un 7400 hasta un 74181 (ALU de 4 bits).",
         notes="Insistir en la diferencia entre tabla de verdad (comportamiento) y ecuación "
               "(implementación)."),

    # ------------------------------------------------------------------ 7
    dict(kind="bullets", section=1, transition="wipe",
         title="Sistema de numeración binario",
         lead="Base 2: solo dos dígitos, pero infinitas combinaciones.",
         img=p("binary_weights"), img_mode="contain", caption="Pesos binarios de una palabra de 8 bits.",
         items=["El **sistema binario** es posicional en base 2: cada posición pesa una potencia "
                "de dos (1, 2, 4, 8, 16, 32, 64, 128…) en lugar de potencia de diez.",
                "**Bit menos significativo (LSB):** la posición de peso 1; **bit más significativo "
                "(MSB):** la de mayor peso de la palabra.",
                "Conversión **binario → decimal**: se multiplica cada bit por su peso y se suma. "
                "Ejemplo: 1011₂ = 8 + 2 + 1 = 11₁₀.",
                "Conversión **decimal → binario**: se divide sucesivamente entre 2 y se leen los "
                "residuos en orden inverso (método de divisiones sucesivas).",
                "**Hexadecimal (base 16)** se usa como abreviatura del binario: cada dígito hex "
                "equivale a 4 bits (un nibble) y simplifica mucho la lectura de buses y memorias.",
                "Con **n bits** se representan 2^n combinaciones distintas: 4 bits → 16 valores, "
                "8 bits → 256 valores, 10 bits → 1024, 16 bits → 65 536.",
                "Un byte admite dos lecturas: sin signo (0 … 255) o con signo en complemento a dos "
                "(–128 … +127).",
                "El complemento a dos se obtiene invirtiendo todos los bits y sumando 1; es la "
                "forma en que los procesadores restan sumando."],
         note="Aritmética de bits: sumar 1 a 1111₂ produce 0000₂ y un acarreo (overflow del nibble). "
              "Ese acarreo es exactamente lo que maneja la compuerta AND en un medio sumador.",
         notes="Practicar tres conversiones en el pizarrón."),

    # ------------------------------------------------------------------ 8
    dict(kind="table", section=1, transition="wipe",
         title="Tabla de conversiones: decimal, binario, hexadecimal y BCD",
         lead="Referencia rápida con los valores que más se usan en el laboratorio y en la lectura de buses.",
         header=["Decimal", "Binario (4 bits)", "Hexadecimal", "BCD (8421)", "Observación"],
         widths=[0.13, 0.20, 0.15, 0.22, 0.30], size=11, accent="cyan",
         rows=[["0", "0000", "0", "0000 0000", "Estado inicial de contadores y registros"],
               ["1", "0001", "1", "0000 0001", "Primer peso binario"],
               ["2", "0010", "2", "0000 0010", "Dato del ejemplo del sumador de 2 bits"],
               ["3", "0011", "3", "0000 0011", "Bits de paridad impar"],
               ["4", "0100", "4", "0000 0100", "Nibble alto del BCD"],
               ["5", "0101", "5", "0000 0101", "Peso hexadecimal"],
               ["7", "0111", "7", "0000 0111", "Dirección de memoria del 74LS189"],
               ["8", "1000", "8", "0000 1000", "Primer bit más significativo"],
               ["9", "1001", "9", "0000 1001", "Último dígito válido en BCD"],
               ["10", "1010", "A", "0001 0000", "En BCD se codifican dos nibbles"],
               ["15", "1111", "F", "0001 0101", "Nibble completo: fin de contador"],
               ["16", "1 0000", "10", "0001 0110", "Quinto bit = acarreo"],
               ["255", "1111 1111", "FF", "—", "Byte completo sin signo"],
               ["1000", "11 1110 1000", "3E8", "—", "10 bits, requiere contador de 10 bits"]],
         note="Aviso didáctico: en BCD el valor 1010₂ nunca aparece, porque los nibbles válidos son "
              "0000 a 1001. Un decodificador BCD a 7 segmentos (74LS47) marca error o 'parpadeo' "
              "ante un código BCD inválido.",
         note_label="DETALLE IMPORTANTE", notes="Mostrar cómo el hex resume el binario."),

    # ------------------------------------------------------------------ 9
    dict(kind="cards", section=1, transition="wipe",
         title="Unidades de información y su uso práctico",
         lead="El bit es la unidad mínima; las agrupaciones explican los diagramas de pines y memorias.",
         cols=3,
         cards=[dict(title="Bit", num="1 b", accent="cyan",
                     body="Un estado lógico: '0' o '1'. Es la unidad de la tabla de verdad y "
                          "equivale a una salida de compuerta."),
                dict(title="Nibble", num="4 b", accent="orange",
                     body="Cuatro bits: la mitad de un byte y el tamaño de un dígito hexadecimal. "
                          "Un decodificador BCD recibe exactamente un nibble."),
                dict(title="Byte", num="8 b", accent="green",
                     body="Ocho bits: 256 combinaciones. Es la anchura de los buses de datos de "
                          "los integrados 74LS374, 74LS245 y 74LS688."),
                dict(title="Palabra", num="16/32 b", accent="purple",
                     body="Ancho de datos del procesador. El 74LS181 (ALU) trabaja con palabras "
                          "de 4 bits y se encadenan para formar palabras mayores."),
                dict(title="Dirección", num="A0…An", accent="pink",
                     body="Conjunto de bits que identifica una posición de memoria. Con n líneas "
                          "se direccionan 2^n posiciones."),
                dict(title="Bus", num="n × bit", accent="blue",
                     body="Grupo de líneas que viajan juntas: bus de datos, de direcciones y de "
                          "control. Requieren transceptores como el 74LS245.")],
         note="Ejemplo real: el 74LS189 es una RAM de 64 bits organizada como 16 palabras × 4 bits, "
              "es decir, necesita 4 líneas de dirección (A0–A3) y 4 líneas de datos (D0–D3).",
         notes="Relacionar unidades con pines del integrado."),

    # ------------------------------------------------------------------ 10
    dict(kind="bullets", section=1, transition="wipe",
         title="Códigos digitales: BCD, Gray, ASCII y paridad",
         lead="No todo lo que se transmite es binario natural: existen códigos con reglas propias.",
         sidebar=[dict(title="BCD (8421)", accent="cyan",
                       body="Cada dígito decimal se codifica por separado con 4 bits. Ventaja: "
                            "conversión directa a displays de 7 segmentos. Desventaja: "
                            "desperdicia 6 de cada 16 códigos."),
                  dict(title="Código Gray", accent="orange",
                       body="Dos valores consecutivos difieren en un solo bit, lo que evita "
                            "falsas lecturas en decodificadores rotativos y sensores de "
                            "posición. Se usa en encoders y en tablas de Karnaugh."),
                  dict(title="ASCII", accent="green",
                       body="Código de 7 bits para caracteres: '0' = 0110000, 'A' = 1000001. Es "
                            "la base del texto que viaja por puertos serie y teclados."),
                  dict(title="Bit de paridad", accent="purple",
                       body="Bit adicional calculado con XOR que detecta un número impar de "
                            "errores en la transmisión. Se genera con 7486 o 74180.")],
         items=["**BCD natural (8421):** 47₁₀ se codifica como 0100 0111, dos nibbles "
                "independientes y no un binario único (47₁₀ = 101111₂).",
                "**BCD desempaquetado** usa 8 bits por dígito (4 de relleno); **empaquetado** "
                "aprovecha las dos mitades del byte. Los contadores 74LS390 entregan BCD "
                "empaquetado.",
                "**Exceso 3** suma 3 al BCD y sirve para operaciones aritméticas sin acarreo "
                "explícito en algunos sumadores históricos.",
                "**Código Gray de 3 bits:** 000, 001, 011, 010, 110, 111, 101, 100. La secuencia "
                "regresa al inicio cambiando un solo bit.",
                "**Paridad par:** se añade el bit necesario para que el número total de unos sea "
                "par. **Paridad impar:** se fuerza a impar. La compuerta XOR es el detector natural.",
                "**Detección vs. corrección:** la paridad detecta errores simples; los códigos "
                "Hamming detectan y corrigen, usando varias compuertas XOR en cascada.",
                "**Display de 7 segmentos:** cada segmento tiene una letra (a–g) y el 74LS47 "
                "convierte el BCD en esas siete señales.",
                "**BCD inválido:** si un contador entrega 1010₂ a un decodificador 74LS47, la "
                "salida muestra un símbolo errático; hay que verificar el conteo."],
         notes="Distinguir claramente conversión binaria de codificación BCD."),

    # ------------------------------------------------------------------ 11
    dict(kind="gallery", section=1, transition="fade",
         title="Niveles lógicos y márgenes de ruido del estándar TTL",
         lead="Los fabricantes garantizan un nivel, no un valor exacto: de ahí nace el margen de ruido.",
         cols=1, accent="cyan",
         photos=[(p("noise_margin"), "Bandas garantizadas de tensión para la familia TTL con "
                                     "alimentación de 5 V: VOL máx 0.4 V, VOH mín 2.4 V, VIL máx "
                                     "0.8 V y VIH mín 2.0 V.")],
         items=["**VIL (Voltage Input Low):** máxima tensión que el integrado reconoce como '0'. "
                "En TTL: 0.8 V. Todo valor por debajo es un '0' garantizado.",
                "**VIH (Voltage Input High):** mínima tensión que el integrado reconoce como '1'. "
                "En TTL: 2.0 V. Todo valor por encima es un '1' garantizado.",
                "**VOL (Voltage Output Low):** máxima tensión que el chip entrega como '0' "
                "cuando la salida está cargada: 0.4 V.",
                "**VOH (Voltage Output High):** mínima tensión que entrega como '1' con carga "
                "nominal: 2.4 V (típicamente 3.4 V en vacío).",
                "**Margen de ruido a nivel bajo:** NM(0) = VIL – VOL = 0.8 – 0.4 = 0.4 V. El "
                "circuito tolera hasta 400 mV de interferencia sobre un '0'.",
                "**Margen de ruido a nivel alto:** NM(1) = VOH – VIH = 2.4 – 2.0 = 0.4 V. Igual "
                "tolerancia a la interferencia sobre un '1'.",
                "**Zona indeterminada (0.8 V – 2.0 V):** el chip puede leer cualquiera de los dos "
                "valores, y si la señal oscila produce corrientes internas, calentamiento y "
                "consumo excesivo.",
                "**Entradas flotantes:** un pin TTL al aire se comporta como '1' por la estructura "
                "interna; en CMOS provoca oscilación y debe conectarse siempre a VCC o GND."],
         note="Verificación práctica: con el multímetro digital sobre un pin de salida, un '0' "
              "real debe medir por debajo de 0.4 V y un '1' por encima de 2.7 V. Valores "
              "intermedios indican carga excesiva, pin flotante o chip dañado.",
         notes="Este es uno de los conceptos más evaluados: memorizar VIL/VIH."),

    # ------------------------------------------------------------------ 12
    dict(kind="cards", section=1, transition="wipe",
         title="Inmunidad al ruido y calidad de la señal",
         lead="Por qué el mismo dato puede leerse bien o mal según el montaje físico.",
         cols=2,
         cards=[dict(title="Fuentes de ruido", accent="orange", num="1",
                     body="Conmutación de cargas inductivas, cables largos que captan campos, "
                          "rebotes mecánicos del interruptor, rizado de la fuente y acoplamiento "
                          "entre pistas paralelas del protoboard."),
                dict(title="Cómo se combate", accent="green", num="2",
                     body="Capacitor de desacople de 100 nF junto a cada chip, cables cortos, "
                          "planos de masa, resistencia pull-up en entradas lentas y separación "
                          "entre señales de reloj y datos."),
                dict(title="Rebote de interruptor", accent="cyan", num="3",
                     body="Un pulsador mecánico genera decenas de pulsos en pocos milisegundos. Se "
                          "elimina con un latch SR (7400), un filtro RC o un circuito "
                          "antirrebote con 74LS14 (Schmitt trigger)."),
                dict(title="Capacidad de entrada", accent="purple", num="4",
                     body="Cada entrada TTL presenta unos pocos picofaradios; en cargas grandes "
                          "la suma de capacidades redondea los flancos y aumenta el tiempo de "
                          "conmutación real.")],
         note="Cuando una salida debe atacar muchas entradas, el nivel '1' se degrada más que el "
              "'0' porque TTL entrega muy poca corriente en alto (IOH ≈ 0.4 mA). Es la razón "
              "técnica por la que existe el fan-out.",
         notes="Relacionar con el fan-out de la siguiente sección."),

    # ------------------------------------------------------------------ 13
    dict(kind="gate", section=1, transition="fade",
         title="Compuerta AND (Chip 7408)",
         lead="La compuerta de la coincidencia total: solo se activa cuando todas sus entradas lo están.",
         accent="cyan", chip="74LS08 / 7408", chip_name="Quad 2-Input Positive-AND Gate",
         symbol=p("gate_and"),
         chip_facts=["4 compuertas AND independientes en un DIP-14",
                     "Salida = 1 solo si TODAS las entradas = 1",
                     "tPD típico 8 ns (74LS) · 10 ns (7400)",
                     "Aplicación clásica: habilitación de señal"],
         expr="Y = A · B   (se lee: A y B)",
         truth_title="TABLA DE VERDAD · 7408",
         truth_header=["A", "B", "Y = A·B"],
         truth=[["0", "0", "0"], ["0", "1", "0"], ["1", "0", "0"], ["1", "1", "1"]],
         truth_widths=[0.34, 0.34, 0.32],
         times=p("time_and"),
         how="La salida permanece en '0' mientras cualquier entrada esté en '0'. Solo la "
             "combinación A = 1 con B = 1 eleva la salida a '1'. En la práctica funciona como "
             "una compuerta de habilitación: la señal presente en B solo pasa si la entrada de "
             "control A está en alto. Equivale a multiplicar bits y a la intersección de "
             "condiciones: 'si llueve Y hace frío, enciende la calefacción'.",
         apps="Sistemas de seguridad con doble confirmación, habilitadores de reloj (gating), "
              "máscaras de bits, inicio de un medio sumador (acarreo), validación de contraseñas "
              "y condiciones lógicas múltiples en automatización.",
         notes="El 74LS08 también se consigue como 74ALS08, 74HC08 y 74HCT08 con el mismo pinout."),

    # ------------------------------------------------------------------ 14
    dict(kind="pinout", section=1, transition="fade",
         title="Hoja de pines del 7408 y variantes de AND",
         lead="Mapa de pines, descripción funcional y datos de la hoja de datos del Quad AND de 2 entradas.",
         accent="cyan", pinout=p("pin_7408"),
         facts_title="Descripción general",
         facts="El 7408 contiene cuatro compuertas AND de dos entradas en un encapsulado DIP-14. "
               "Los pines 7 y 14 son siempre GND y VCC en los integrados TTL de 14 pines; las "
               "cuatro compuertas se distribuyen simétricamente a ambos lados del cuerpo.",
         pins_title="Distribución de pines",
         pins="1A=1, 1B=2, 1Y=3 | 2A=4, 2B=5, 2Y=6 | GND=7 | 3Y=8, 3A=9, 3B=10 | 4Y=11, 4A=12, "
              "4B=13 | VCC=14. Nota: la salida 3Y sale en el pin 8 y 4Y en el 11, patrón "
              "invertido respecto a las salidas 1Y y 2Y.",
         data_title="Parámetros clave del datasheet",
         data="VCC 4.75–5.25 V · VOH mín 2.7 V (a 0.4 mA) · VOL máx 0.5 V (a 8 mA) · IOH −0.8 mA · "
              "IOL 8 mA · tPLH/tPHL 8/12 ns (74LS08) · consumo 11 mW por compuerta · "
              "temperatura 0–70 °C.",
         note="Equivalentes en otras subfamilias con el MISMO pinout: 74LS08, 74ALS08, 74F08, "
              "74HC08, 74HCT08. El chip cuádruple puede sustituirse directamente sin rediseñar el "
              "circuito; solo cambian velocidad y consumo.",
         notes="Recordar la regla universal: pin 14 = VCC, pin 7 = GND en todos los DIP-14 TTL."),

    # ------------------------------------------------------------------ 15
    dict(kind="gallery", section=1, transition="fade",
         title="AND en operación: tiempos y montaje",
         lead="Cómo se ve el comportamiento de la compuerta AND en el osciloscopio y en la placa.",
         cols=2, accent="cyan",
         photos=[(p("time_and"), "Diagrama de tiempos del 7408: la salida Y solo sube cuando A y "
                                  "B están simultáneamente en alto; se aprecia el retardo de "
                                  "propagación tPD."),
                 (s("image6.png"), "Encapsulados DIP reales de la familia HCMOS (74HC), la "
                                   "variante CMOS compatible con TTL que hereda la pinout de la "
                                   "serie 74XX.")],
         items=["**Diagrama de tiempos:** A conmuta primero y B después; Y refleja la operación "
                "lógica con el retardo tPD.",
                "**tPLH y tPHL:** subida y bajada tienen tiempos ligeramente distintos; en 74LS08 "
                "rondan 8 ns y 12 ns.",
                "**Glitch:** si las entradas cambian con diferencia de nanosegundos, la salida "
                "puede mostrar un pulso breve no deseado (riesgo o hazard).",
                "**Montaje:** alimentar VCC = 5 V y GND; nunca dejar un pin de entrada al aire.",
                "**Medición:** con LED + resistencia de 330 Ω en la salida se observa el estado "
                "lógico sin osciloscopio.",
                "**Verificación:** aplicar las cuatro combinaciones de la tabla de verdad y "
                "comprobar que solo 1-1 produce salida alta."],
         note="Un error frecuente en el laboratorio es confundir el orden de pines: verificar "
              "siempre la muesca (pin 1 a su izquierda) y la orientación del chip antes de "
              "interpretar cualquier medición.",
         notes="Mostrar el símbolo y los tiempos juntos."),

    # ------------------------------------------------------------------ 16
    dict(kind="twocol", section=1, transition="wipe",
         title="Lógica positiva y lógica negativa",
         lead="El mismo chip cambia de significado según cómo se defina el nivel activo.",
         accent="purple",
         left=dict(title="Lógica positiva (convención normal)", accent="cyan", items=[
             "**Nivel alto = '1'** (activo), nivel bajo = '0' (inactivo).",
             "Todas las tablas de verdad de esta guía usan esta convención.",
             "Un LED conectado a la salida enciende cuando la función se cumple.",
             "Se lee como 'la salida está activa en alto' (active-high).",
             "Ejemplo: en el 7408, la salida es '1' cuando A·B = 1.",
             "Facilita el análisis booleano directo y el uso de álgebra de Boole."]),
         right=dict(title="Lógica negativa (activo en bajo)", accent="orange", items=[
             "**Nivel bajo = '1' lógico** (activo), convención que ahorra inversores.",
             "Señales como OE (output enable), CS (chip select) o RESET son activas en bajo "
             "en casi todos los integrados.",
             "Permite construir lógica más rápida: TTL 'sume' mejor que 'entrega' corriente.",
             "El 74LS47 (display) maneja segmentos activos en bajo.",
             "Exige invertir mentalmente la tabla de verdad o usar un inversor (7404).",
             "Errores típicos: olvidar el asterisco o la barra sobre el nombre del pin."]),
         note="Truco de taller: cuando un LED conectado a una salida enciende con la lógica "
              "invertida, casi siempre el pin es activo en bajo (barra superior en la hoja de "
              "datos). Verificar el nombre del pin antes de concluir que el chip está dañado.",
         notes="Explicar por qué los datasheets usan tanto la actividad en bajo."),

    # ------------------------------------------------------------------ 17
    dict(kind="table", section=1, transition="wipe",
         title="Álgebra de Boole: postulados y teoremas esenciales",
         lead="Herramientas para simplificar funciones antes de cablear un circuito.",
         header=["Nombre", "Forma con AND", "Forma con OR", "Utilidad práctica"],
         widths=[0.22, 0.24, 0.24, 0.30], accent="purple", size=11,
         rows=[["Identidad", "A · 1 = A", "A + 0 = A", "Elimina términos triviales"],
               ["Elemento nulo", "A · 0 = 0", "A + 1 = 1", "Detecta condiciones imposibles"],
               ["Idempotencia", "A · A = A", "A + A = A", "Reduce compuertas redundantes"],
               ["Complementación", "A · A' = 0", "A + A' = 1", "Base del biestable y del reloj"],
               ["Conmutativa", "A · B = B · A", "A + B = B + A", "Permite reordenar pines"],
               ["Asociativa", "(AB)C = A(BC)", "(A+B)+C = A+(B+C)", "Encadenar y agrupar"],
               ["Distributiva", "A(B + C) = AB + AC", "A + BC = (A+B)(A+C)", "Factoriza y ahorra chips"],
               ["Absorción", "A(A + B) = A", "A + AB = A", "Elimina términos absorbidos"],
               ["Redundancia", "A + A'B = A + B", "A(A' + B) = AB", "Simplificación avanzada"],
               ["Consenso", "AB + A'C + BC = AB + A'C", "—", "Elimina términos de consenso"],
               ["De Morgan 1", "(A · B)' = A' + B'", "—", "Convierte AND en OR con NAND"],
               ["De Morgan 2", "(A + B)' = A' · B'", "—", "Convierte OR en NOR"]],
         note="Regla de oro: toda función lógica se puede implementar solo con NAND o solo con NOR. "
              "Simplificar con Boole no es un ejercicio teórico: cada término eliminado es un "
              "circuito integrado menos y menos posibilidades de falla.",
         note_label="REGLA DE ORO", notes="Practicar De Morgan con un ejemplo numérico."),

    # ------------------------------------------------------------------ 18
    dict(kind="gallery", section=1, transition="fade",
         title="Leyes de De Morgan explicadas",
         lead="Las dos identidades que permiten transformar circuitos completos sin cambiar su función.",
         cols=1, accent="purple",
         photos=[(p("de_morgan"), "Formas equivalentes: el complemento de un producto es la suma "
                                  "de los complementos, y el complemento de una suma es el "
                                  "producto de los complementos.")],
         items=["**Primera ley:** (A · B)' = A' + B'. Un NAND equivale a un OR con las entradas "
                "invertidas.",
                "**Segunda ley:** (A + B)' = A' · B'. Un NOR equivale a un AND con las entradas "
                "invertidas.",
                "**Aplicación 1:** convertir un diseño de NAND a NOR sin cambiar la función "
                "lógica, solo redistribuyendo inversiones.",
                "**Aplicación 2:** aprovechar compuertas de sobra. Si quedan NAND libres en un "
                "chip, con ellas se puede construir el OR que falta.",
                "**Aplicación 3:** leer un diagrama con burbujas. Una burbuja en la salida de un "
                "símbolo se puede 'empujar' a las entradas cambiando AND por OR.",
                "**Verificación:** sustituir A = 0, B = 1 en ambas expresiones y comprobar que "
                "dan el mismo resultado (0 y 0)."],
         note="Ejercicio guiado: simplificar Y = (A + B)(B + C)(B + C'). Solución: por "
              "distributiva y absorción, Y = B + AC. Se eliminan dos compuertas y un chip.",
         notes="Mostrar la equivalencia con un par de compuertas en el pizarrón."),

    # ------------------------------------------------------------------ 19
    dict(kind="gallery", section=1, transition="fade",
         title="Mapas de Karnaugh: simplificación visual",
         lead="El método gráfico que permite agrupar unos y obtener la expresión mínima.",
         cols=1, accent="orange",
         photos=[(p("kmap"), "Mapa de 4 variables con dos agrupamientos: un grupo de cuatro unos "
                             "(elimina dos variables) y uno de dos unos (elimina una variable).")],
         items=["**Regla 1:** se agrupan '1' en rectángulos de tamaño 1, 2, 4, 8, 16… siempre "
                "potencias de dos.",
                "**Regla 2:** los grupos pueden solaparse y pueden dar vuelta por los bordes del "
                "mapa (es un cilindro, no una cuadrícula plana).",
                "**Regla 3:** dentro de cada grupo se eliminan las variables que cambian de valor "
                "y se conservan las que permanecen constantes.",
                "**Regla 4:** se buscan los grupos más grandes posibles con el menor número de "
                "grupos; luego se convierten en suma de productos (SOP).",
                "**Regla 5:** los ceros también sirven: agrupándolos se obtiene el producto de "
                "sumas (POS).",
                "**Ejemplo del gráfico:** el grupo verde de cuatro unos equivale a eliminar dos "
                "variables; el naranja de dos, una.",
                "**Para 5 o 6 variables** existen mapas de doble plano y métodos tabulares "
                "(Quine-McCluskey) cuando la función es muy grande.",
                "**Verificación final:** probar la expresión simplificada con las filas de la "
                "tabla de verdad original."],
         note="Los mapas de Karnaugh son secuenciales en el papel y se pueden programar: en el "
              "laboratorio se usa el mapa mentalmente para decidir cuántos chips de la Serie 74XX "
              "se necesitan realmente.",
         notes="Resolver un mapa completo de 3 variables en clase."),

    # ------------------------------------------------------------------ 20
    dict(kind="cards", section=1, transition="fade",
         title="Formas canónicas y síntesis de funciones",
         lead="De la tabla de verdad a la lista de compuertas, sin ambigüedad.",
         cols=3,
         cards=[dict(title="Minitérmino", num="m", accent="cyan",
                     body="Producto AND en el que cada variable aparece una vez (directa o "
                          "negada) y que vale 1 en exactamente una fila de la tabla. Notación: "
                          "m3 = A'BC."),
                dict(title="Suma de productos (SOP)", num="Σm", accent="green",
                     body="OR de todos los minitérminos que producen 1. Es la forma natural de "
                          "leer una tabla de verdad fila por fila."),
                dict(title="Maxitérmino", num="M", accent="orange",
                     body="Suma OR con una variable por término, que vale 0 en exactamente una "
                          "fila. Notación: M2 = A + B' + C."),
                dict(title="Producto de sumas (POS)", num="ΠM", accent="purple",
                     body="AND de los maxitérminos que producen 0. Suele dar menos compuertas "
                          "cuando la tabla tiene pocos ceros."),
                dict(title="SOP con NAND", num="3 niveles", accent="pink",
                     body="Cualquier SOP se implementa con dos niveles de NAND más inversores en "
                          "las variables negadas. Es la ruta típica con chips 7400."),
                dict(title="POS con NOR", num="3 niveles", accent="blue",
                     body="Cualquier POS se implementa con NOR en dos niveles (Al aplicar De "
                          "Morgan). Útil cuando el tablero tiene chips 7402 disponibles.")],
         note="Secuencia de diseño: enunciado → tabla de verdad → minitérminos → simplificación "
              "(Boole o Karnaugh) → compuertas disponibles → lista de chips → montaje. Nunca se "
              "debe empezar por el montaje.",
         notes="Insistir en que la tabla de verdad es la fuente de verdad del diseño.") ,
]
