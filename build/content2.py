# -*- coding: utf-8 -*-
"""Sección 2 — Compuertas lógicas y chips 74XX."""
import os
import theme
from theme import SRC


def p(n):
    return os.path.join(theme.GEN, n + ".png")


def s(n):
    return os.path.join(SRC, n)


SLIDES = [
    # ------------------------------------------------------------------ sección
    dict(kind="section", section=2, transition="zoom",
         img=p("sec_gates"), topics=[
             "Símbolo ANSI, expresión booleana y tabla de verdad de cada compuerta",
             "Chip comercial que la implementa: 7408, 7432, 7404, 7400, 7402, 7486 y 74266",
             "Distribución de pines (pinout) y función de cada patita del DIP-14",
             "Diagramas de tiempo: retardo tPD, flancos y glitches",
             "Aplicaciones típicas y equivalencias entre subfamilias del mismo número",
             "Compuertas universales: cómo construir cualquier función con solo NAND o solo NOR"],
         notes="Apertura del bloque 2."),

    # ------------------------------------------------------------------ OR
    dict(kind="gate", section=2, transition="fade",
         title="Compuerta OR (Chip 7432)",
         lead="La compuerta de la suma lógica: basta una entrada activa para activar la salida.",
         accent="orange", chip="74LS32 / 7432", chip_name="Quad 2-Input Positive-OR Gate",
         symbol=p("gate_or"),
         chip_facts=["4 compuertas OR independientes en un DIP-14",
                     "Salida = 1 si AL MENOS UNA entrada = 1",
                     "tPD típico 10 ns (74LS) · 14 ns (7400)",
                     "Se usa en alarmas y condiciones 'o'"],
         expr="Y = A + B   (se lee: A o B)",
         truth_title="TABLA DE VERDAD · 7432",
         truth_header=["A", "B", "Y = A+B"],
         truth=[["0", "0", "0"], ["0", "1", "1"], ["1", "0", "1"], ["1", "1", "1"]],
         truth_widths=[0.34, 0.34, 0.32],
         times=p("time_or"),
         how="La salida baja a '0' únicamente cuando ambas entradas están en '0'. Cualquier "
             "entrada en alto la mantiene en '1'. Representa la unión de condiciones: 'si el "
             "sensor A o el sensor B detectan movimiento, suena la alarma'. También se usa como "
             "suma en álgebra de Boole y como OR de bits en máscaras.",
         apps="Alarmas multisensor, mezcla de señales de reloj de dos fuentes, unión de "
              "interrupciones, detección de cualquier falla (OR de banderas de error), arranque "
              "con dos botones alternativos y etapas finales de un comparador.",
         notes="El 74LS32 es tan común que los 'OR de emergencia' en un tablero casi siempre se "
               "hacen con un 7400 por equivalencia de De Morgan."),

    dict(kind="pinout", section=2, transition="fade",
         title="Pinout del 7432 y alternativas OR",
         lead="Distribución de pines idéntica a la del 7408, aunque la función es la suma lógica.",
         accent="orange", pinout=p("pin_7432"),
         facts_title="Descripción general",
         facts="Cuádruple compuerta OR de dos entradas, tecnología TTL original y disponible en "
               "las subfamilias LS, ALS, F, HC y HCT. Conserva el mismo mapa de pines que el "
               "7408, por lo que ambos son intercambiables físicamente, no funcionalmente.",
         pins_title="Distribución de pines",
         pins="1A=1, 1B=2, 1Y=3 | 2A=4, 2B=5, 2Y=6 | GND=7 | 3Y=8, 3A=9, 3B=10 | 4Y=11, 4A=12, "
              "4B=13 | VCC=14. Igual que en el 7408, las salidas 3 y 4 quedan en los pines 8 y 11.",
         data_title="Parámetros clave del datasheet",
         data="VCC 4.75–5.25 V · VOH mín 2.7 V · VOL máx 0.5 V · IOL 8 mA · tPD 10/15 ns (74LS32) · "
              "consumo típico 11 mW por compuerta · corriente de entrada 20 µA en alto, 0.4 mA en "
              "bajo.",
         note="Sustitución directa: 74LS32 ↔ 74ALS32 ↔ 74F32 ↔ 74HC32 ↔ 74HCT32. Si el circuito "
              "está hecho con el 74HC32 y se cambia a 74LS32, hay que verificar las corrientes de "
              "entrada porque las familias LS cargan más la señal que las HC.",
         notes="Comparar lado a lado con el 7408."),

    dict(kind="gallery", section=2, transition="fade",
         title="OR en operación: tiempos y comportamiento real",
         lead="Cómo se ve la suma lógica en el osciloscopio y qué cuidar al montarla.",
         cols=2, accent="orange",
         photos=[(p("time_or"), "Diagrama de tiempos del 7432: la salida Y sube con cualquier "
                                "entrada alta y solo cae cuando ambas entradas bajan."),
                 (p("pin_7432"), "Mapa de pines del 7432: cuatro compuertas OR independientes "
                                 "con VCC en el pin 14 y GND en el pin 7.")],
         items=["**Forma de onda:** Y = 0 solo en el primer tramo, cuando A = B = 0; en el resto "
                "permanece alta.",
                "**Transición dominante:** cualquier flanco de subida en A o en B produce una "
                "transición en Y (tPLH).",
                "**Cuidado con el glitch:** al cambiar ambas entradas casi al mismo tiempo se "
                "generan pulsos estrechos de duración tPD.",
                "**Práctica sugerida:** aplicar dos señales de reloj de distintas frecuencias y "
                "observar la suma lógica en el osciloscopio.",
                "**Aplicación inmediata:** OR de dos interruptores para encender una misma carga "
                "desde dos puntos del tablero."],
         note="El OR de señales de reloj de frecuencias distintas produce ruido de alta "
              "frecuencia: en sistemas reales se multiplexa en lugar de sumar con OR.",
         notes="Mostrar la diferencia entre suma booleana y suma aritmética."),

    # ------------------------------------------------------------------ NOT
    dict(kind="gate", section=2, transition="fade",
         title="Compuerta NOT / Inversor (Chip 7404)",
         lead="El inversor: una sola entrada y el complemento exacto en la salida.",
         accent="purple", chip="74LS04 / 7404", chip_name="Hex Inverter",
         symbol=p("gate_not"),
         chip_facts=["6 inversores independientes en un DIP-14",
                     "Y = complemento exacto de A",
                     "Se usa para generar variables negadas A', B'",
                     "Base de osciladores y antirrebote"],
         expr="Y = A'   (se lee: A negada)",
         truth_title="TABLA DE VERDAD · 7404",
         truth_header=["A", "Y = A'"],
         truth=[["0", "1"], ["1", "0"]],
         truth_widths=[0.5, 0.5],
         times=None,
         how="Entrega en su salida el nivel contrario al de la entrada. Es indispensable para "
             "generar las variables negadas que aparecen en cualquier función simplificada y "
             "para restaurar niveles degradados por la carga. Su estructura interna es un "
             "transistor con resistencia pull-up (en TTL) o un par CMOS complementario.",
         apps="Generación de variables complementarias, osciladores de reloj (con cristal o RC), "
              "antirrebote de interruptores, conformación de pulsos, buffers con inversión y "
              "construcción de compuertas lógicas a partir de NAND o NOR.",
         notes="También existe el 7406 (colector abierto, 30 V) y el 7414 (Schmitt trigger) para "
               "entradas lentas o ruidosas."),

    dict(kind="pinout", section=2, transition="fade",
         title="Pinout del 7404 y variantes de inversor",
         lead="El chip más sencillo de la familia, pero con la variante Schmitt que salva montajes reales.",
         accent="purple", pinout=p("pin_7404"),
         facts_title="Descripción general",
         facts="Seis inversores independientes en DIP-14. El 7414 ofrece la misma función con "
               "histéresis de Schmitt (umbrales separados de subida y bajada), ideal para señales "
               "lentas, con rebote o con ruido, y el 7406 con salida de colector abierto para "
               "manejar cargas de hasta 30 V.",
         pins_title="Distribución de pines",
         pins="1A=1, 1Y=2 | 2A=3, 2Y=4 | 3A=5, 3Y=6 | GND=7 | 4Y=8, 4A=9 | 5Y=10, 5A=11 | "
              "6Y=12, 6A=13 | VCC=14. Cada par de pines consecutivos es un inversor completo.",
         data_title="Parámetros clave del datasheet",
         data="VCC 4.75–5.25 V · tPD 8/12 ns (74LS04) · 74LS14 con histéresis VT+ 1.6 V y VT– 0.8 V · "
              "IOH −0.4 mA, IOL 8 mA · fan-out 10 entradas TTL estándar.",
         note="Un inversor libre sirve como oscilador: 74LS04 + cristal de cuarzo y dos "
              "capacitores forman el reloj base de muchos circuitos digitales educativos.",
         notes="Mencionar el uso del 7404 para eliminar rebote eléctrico."),

    # ------------------------------------------------------------------ NAND
    dict(kind="gate", section=2, transition="fade",
         title="Compuerta NAND (Chip 7400)",
         lead="La compuerta universal: con ella sola se construye cualquier función lógica.",
         accent="green", chip="74LS00 / 7400", chip_name="Quad 2-Input Positive-NAND Gate",
         symbol=p("gate_nand"),
         chip_facts=["4 compuertas NAND en un DIP-14",
                     "Salida = 0 SOLO si A = B = 1",
                     "Es la compuerta universal por excelencia",
                     "Primer integrado lógico de la historia (1961)"],
         expr="Y = (A · B)'   (se lee: A por B negado)",
         truth_title="TABLA DE VERDAD · 7400",
         truth_header=["A", "B", "Y = (A·B)'"],
         truth=[["0", "0", "1"], ["0", "1", "1"], ["1", "0", "1"], ["1", "1", "0"]],
         truth_widths=[0.34, 0.34, 0.32],
         times=p("time_nand"),
         how="Es una AND seguida de un inversor. Su salida permanece en '1' salvo en el único "
             "caso en que todas las entradas están en alto, donde cae a '0'. Debido a que la "
             "salida típica de un TTL 'sumidera' mejor corriente que la que entrega, el NAND es "
             "la compuerta más usada como etapa de potencia hacia LEDs y cargas.",
         apps="Memorias latch y flip-flops, osciladores digitales, decodificadores, lógica "
              "universal, antirrebote, control de habilitación activa en bajo y práctica totalidad "
              "de los circuitos combinacionales didácticos.",
         notes="El 74LS00 se fabrica desde 1961 y puede que sea el integrado lógico más vendido de "
               "la historia."),

    dict(kind="pinout", section=2, transition="fade",
         title="Pinout del 7400: el chip más versátil",
         lead="El candidato número uno para el laboratorio: cuatro compuertas universales.",
         accent="green", pinout=p("pin_7400"),
         facts_title="Descripción general",
         facts="Cuatro compuertas NAND de dos entradas. Es el integrado lógico más usado en "
               "prácticas de electrónica digital por su versatilidad: permite implementar AND, "
               "OR, NOT, XOR y cualquier función simplificada sin necesidad de otros chips.",
         pins_title="Distribución de pines",
         pins="1A=1, 1B=2, 1Y=3 | 2A=4, 2B=5, 2Y=6 | GND=7 | 3Y=8, 3A=9, 3B=10 | 4Y=11, 4A=12, "
              "4B=13 | VCC=14. Idéntico al del 7408 y 7432; solo cambia la función interna.",
         data_title="Parámetros clave del datasheet",
         data="VCC 4.75–5.25 V · VOH mín 2.4 V (a −0.4 mA) · VOL máx 0.4 V (a 16 mA, subfamilia LS) · "
              "tPD 9/10 ns (74LS00) · tiempo de subida de salida 15 ns · disipación 10 mW por "
              "compuerta.",
         note="El 74LS00 y el 74LS03 comparten pinout: el segundo tiene salidas de colector "
              "abierto, útiles para conectar varias salidas en un mismo punto (lógica cableada).",
         notes="Recordar la convención: pin 1 junto a la muesca, lado izquierdo."),

    dict(kind="gallery", section=2, transition="fade",
         title="NAND universal: convertir una compuerta en todas",
         lead="Con solo 7400 se construyen AND, OR, NOT y cualquier función simplificada.",
         cols=2, accent="green",
         photos=[(p("nand_universal"), "Las tres conversiones básicas con NAND: NOT y AND "
                                       "resuelven con una compuerta más un inversor, mientras "
                                       "que OR necesita tres compuertas."),
                 (p("time_nand"), "Diagrama de tiempos del 7400: la salida solo cae cuando "
                                  "ambas entradas están simultáneamente en alto.")],
         items=["**NOT con NAND:** unir las dos entradas de una misma compuerta. Y = (A·A)' = A'.",
                "**AND con NAND:** NAND seguido de un inversor (otra NAND con las entradas "
                "unidas). Ocupa dos de las cuatro compuertas del chip.",
                "**OR con NAND:** invertir cada entrada y luego aplicar NAND: Y = ((A'·B')' = A + B.",
                "**NOR con NAND:** construir el OR y añadir un inversor; requiere cuatro "
                "compuertas.",
                "**XOR con NAND:** necesita cuatro compuertas NAND de dos entradas y permite "
                "comprobar la potencia real de la compuerta universal.",
                "**Ventaja de taller:** un solo tipo de chip en el estante resuelve todas las "
                "funciones y reduce el inventario de refacciones."],
         note="Con las cuatro compuertas del 7400 se implementa una función completa: por eso el "
              "enunciado clásico de examen 'implemente esta tabla de verdad solo con 7400' es "
              "perfectamente resoluble.",
         notes="Este es un ejercicio típico de examen y de práctica de laboratorio."),

    # ------------------------------------------------------------------ NOR
    dict(kind="gate", section=2, transition="fade",
         title="Compuerta NOR (Chip 7402)",
         lead="La segunda compuerta universal: inversa de la suma lógica.",
         accent="pink", chip="74LS02 / 7402", chip_name="Quad 2-Input Positive-NOR Gate",
         symbol=p("gate_nor"),
         chip_facts=["4 compuertas NOR en un DIP-14",
                     "Salida = 1 SOLO si A = B = 0",
                     "Pinout distinto al del 7400 y 7408",
                     "Preferida en familias CMOS"],
         expr="Y = (A + B)'   (se lee: A o B negado)",
         truth_title="TABLA DE VERDAD · 7402",
         truth_header=["A", "B", "Y = (A+B)'"],
         truth=[["0", "0", "1"], ["0", "1", "0"], ["1", "0", "0"], ["1", "1", "0"]],
         truth_widths=[0.34, 0.34, 0.32],
         times=p("time_nor"),
         how="Es una OR seguida de un inversor: la salida solo permanece alta cuando todas las "
             "entradas están en bajo. En las familias CMOS el NOR es la estructura más natural "
             "de fabricar (menos transistores) y por eso se prefiere en el diseño de circuitos "
             "integrados; en TTL sucede lo contrario, el NAND es más eficiente.",
         apps="Circuitos secuenciales, protección con enclavamiento de seguridad, detección de "
              "condición nula (ningún sensor activo), osciladores e implementación universal de "
              "funciones en lógica CMOS.",
         notes="Corregir el error clásico: en el 7402 las SALIDAS están en los pines 1, 4, 10 y "
               "13, no las entradas."),

    dict(kind="pinout", section=2, transition="fade",
         title="Pinout del 7402: cuidado con el orden invertido",
         lead="El único de la familia básica que cambia la posición de las salidas.",
         accent="pink", pinout=p("pin_7402"),
         facts_title="Descripción general",
         facts="Cuádruple compuerta NOR de dos entradas. A diferencia del 7400, 7408 y 7432, en "
               "el 7402 las salidas ocupan los pines 1, 4, 10 y 13, y las entradas los pines "
               "2-3, 5-6, 8-9 y 11-12. Es la causa más frecuente de error de cableado.",
         pins_title="Distribución de pines",
         pins="1Y=1, 1A=2, 1B=3 | 2Y=4, 2A=5, 2B=6 | GND=7 | 3A=8, 3B=9, 3Y=10 | 4A=11, 4B=12, "
              "4Y=13 | VCC=14.",
         data_title="Parámetros clave del datasheet",
         data="VCC 4.75–5.25 V · tPD 10/12 ns (74LS02) · IOL 8 mA en LS (16 mA en la versión "
              "7402 original) · entrada de corriente 20 µA en alto y 0.4 mA en bajo · consumo "
              "típico 8 mW por compuerta.",
         note="Truco para no equivocarse: en el 7402 la salida siempre es el pin IMPAR exterior "
              "(1, 4, 10, 13) y las entradas quedan hacia el centro del chip.",
         note_label="HOJA DE DATOS", notes="Repasar el pinout completo con el diagrama."),

    dict(kind="gallery", section=2, transition="fade",
         title="NOR en operación y su uso como compuerta universal",
         lead="Tiempos, tabla y equivalencias para construir cualquier función con 7402.",
         cols=2, accent="pink",
         photos=[(p("time_nor"), "Diagrama de tiempos del 7402: la salida es alta solo mientras "
                                 "ambas entradas permanecen en bajo."),
                 (p("pin_7402"), "Mapa de pines del 7402: las salidas se ubican en los pines "
                                 "impares extremos; las entradas, hacia el interior.")],
         items=["**NOT con NOR:** unir las entradas. Y = (A + A)' = A'.",
                "**OR con NOR:** NOR seguida de un inversor.",
                "**AND con NOR:** invertir las entradas y aplicar NOR: Y = ((A' + B')' = A·B.",
                "**NAND con NOR:** construir el AND y añadir el inversor.",
                "**Comparación práctica:** para hacer un OR, el 7400 necesita tres compuertas y "
                "el 7402 solo dos; para hacer un AND ocurre lo contrario.",
                "**Regla de decisión:** elegir el chip universal que consuma menos compuertas "
                "para la función dominante del diseño."],
         note="En la práctica se compra el chip que resuelve el diseño con menos integrados y "
              "menos cableado: contar compuertas antes de ir a la tienda de electrónica.",
         notes="Comparar el conteo de compuertas entre NAND y NOR."),

    # ------------------------------------------------------------------ XOR
    dict(kind="gate", section=2, transition="fade",
         title="Compuerta XOR / EX-OR (Chip 7486)",
         lead="La compuerta de la diferencia: se activa cuando las entradas no coinciden.",
         accent="blue", chip="74LS86 / 7486", chip_name="Quad 2-Input Exclusive-OR Gate",
         symbol=p("gate_xor"),
         chip_facts=["4 compuertas XOR en un DIP-14",
                     "Salida = 1 si las entradas son DIFERENTES",
                     "Base de sumadores y detectores de paridad",
                     "A ⊕ A = 0 · A ⊕ 1 = A'"],
         expr="Y = A ⊕ B = A'B + AB'",
         truth_title="TABLA DE VERDAD · 7486",
         truth_header=["A", "B", "Y = A ⊕ B"],
         truth=[["0", "0", "0"], ["0", "1", "1"], ["1", "0", "1"], ["1", "1", "0"]],
         truth_widths=[0.34, 0.34, 0.32],
         times=p("time_xor"),
         how="La salida es '1' cuando las entradas difieren y '0' cuando coinciden. "
             "Matemáticamente equivale a la suma módulo 2 sin acarreo, y por eso es la compuerta "
             "clave del medio sumador. Su símbolo lleva una línea adicional en el dorso de la "
             "curva para distinguirla del OR convencional.",
         apps="Sumadores binarios (half-adder y full-adder), generadores y verificadores de "
              "paridad, comparadores de desigualdad, generadores de pseudo-aleatoriedad "
              "(LFSR), detección de cambio de estado y multiplicación en GF(2).",
         notes="La XOR es lineal sobre GF(2): encadenar XOR equivale a sumar en aritmética "
               "módulo 2."),

    dict(kind="pinout", section=2, transition="fade",
         title="Pinout del 7486 y crecimiento a 4 entradas",
         lead="Cuatro puertas XOR de 2 entradas que se combinan para formar XOR de más entradas.",
         accent="blue", pinout=p("pin_7486"),
         facts_title="Descripción general",
         facts="Cuádruple compuerta XOR de dos entradas en DIP-14, con el mismo mapa de pines "
               "que el 7408, 7400 y 7432. Existen versiones de tres entradas (74LS386) y el "
               "74LS280, que es un generador/verificador de paridad de 9 bits.",
         pins_title="Distribución de pines",
         pins="1A=1, 1B=2, 1Y=3 | 2A=4, 2B=5, 2Y=6 | GND=7 | 3Y=8, 3A=9, 3B=10 | 4Y=11, 4A=12, "
              "4B=13 | VCC=14.",
         data_title="Parámetros clave del datasheet",
         data="VCC 4.75–5.25 V · tPD 10/13 ns (74LS86) · IOL 8 mA · VOH mín 2.7 V · "
              "funcionamiento garantizado de 0 a 70 °C (74LS86) o −55 a 125 °C (5486 militar).",
         note="XOR de 4 entradas: encadenar tres compuertas XOR (Y = A ⊕ B ⊕ C ⊕ D). La salida "
              "es '1' cuando el número de entradas altas es IMPAR: es exactamente el cálculo del "
              "bit de paridad impar.",
         notes="Relacionar la XOR con el bit de paridad."),

    dict(kind="gallery", section=2, transition="fade",
         title="XOR en aplicaciones: suma, paridad y control",
         lead="La compuerta que aparece en todo circuito aritmético y de comunicación.",
         cols=2, accent="blue",
         photos=[(p("time_xor"), "Diagrama de tiempos del 7486: la salida conmuta cada vez que "
                                 "una de las entradas cambia de estado, y cae cuando ambas "
                                 "coinciden."),
                 (p("half_adder"), "Medio sumador construido con una XOR (para la suma S) y una "
                                   "AND (para el acarreo C): la célula aritmética mínima.")],
         items=["**Suma binaria:** S = A ⊕ B entrega el bit de suma sin considerar el acarreo "
                "entrante.",
                "**Paridad:** encadenar XOR de todos los bits de un byte genera el bit de "
                "paridad impar en un solo chip.",
                "**Comparador de diferencia:** dos palabras iguales dan 0 en todas sus XOR; "
                "cualquier diferencia produce al menos un 1.",
                "**Interruptor controlado:** con una XOR la salida repite A cuando B = 0, y la "
                "invierte cuando B = 1 (inversor conmutable).",
                "**Generador pseudoaleatorio:** realimentar varias etapas de un registro de "
                "desplazamiento con una XOR (LFSR).",
                "**Verificación de transmisión:** el receptor recalcula la paridad con XOR y la "
                "compara con la recibida para detectar errores."],
         note="La XOR es la única compuerta cuya tabla coincide con la suma módulo 2: de ahí su "
              "papel central en la aritmética binaria y en la detección de errores.",
         notes="Mostrar el medio sumador con la XOR y la AND."),

    # ------------------------------------------------------------------ XNOR
    dict(kind="gate", section=2, transition="fade",
         title="Compuerta XNOR / NEX-OR (Chip 74266)",
         lead="La compuerta de la coincidencia: se activa cuando las entradas son iguales.",
         accent="yellow", chip="74LS266 / 74266", chip_name="Quad 2-Input Exclusive-NOR (Open Collector)",
         symbol=p("gate_xnor"),
         chip_facts=["4 compuertas XNOR en un DIP-14",
                     "Salida = 1 si A = B (ambas 0 o ambas 1)",
                     "Salidas de COLECTOR ABIERTO",
                     "Requiere resistencia pull-up (4.7 kΩ)"],
         expr="Y = (A ⊕ B)' = A·B + A'·B'",
         truth_title="TABLA DE VERDAD · 74266",
         truth_header=["A", "B", "Y = (A ⊕ B)'"],
         truth=[["0", "0", "1"], ["0", "1", "0"], ["1", "0", "0"], ["1", "1", "1"]],
         truth_widths=[0.34, 0.34, 0.32],
         times=p("time_xnor"),
         how="Es una XOR con la salida invertida: produce '1' cuando las dos entradas coinciden. "
             "Su salida es de colector abierto, lo que significa que solo puede llevar la línea a "
             "'0' y necesita una resistencia externa de pull-up (típicamente 4.7 kΩ a VCC) para "
             "alcanzar el nivel alto. Esto permite conectar varias salidas al mismo nodo.",
         apps="Detectores de igualdad lógica, comparadores de magnitud (bits iguales en "
              "posiciones altas), verificadores de código binario, control de paridad par y "
              "circuitos de coincidencia de direcciones.",
         notes="Alternativa moderna: el 74HC7266 tiene salidas CMOS normales (sin colector "
               "abierto) y es mucho más cómodo de usar."),

    dict(kind="pinout", section=2, transition="fade",
         title="Pinout del 74266 y el detalle del colector abierto",
         lead="El único chip de la familia básica que exige resistencias pull-up externas.",
         accent="yellow", pinout=p("pin_74266"),
         facts_title="Descripción general",
         facts="Cuádruple compuerta XNOR con salidas de colector abierto en DIP-14. Al no tener "
               "transistor de pull-up interno, la salida queda en alta impedancia cuando "
               "debería estar en '1' y cae a '0' cuando la función se cumple.",
         pins_title="Distribución de pines",
         pins="1Y=1, 1A=2, 1B=3 | 2Y=4, 2A=5, 2B=6 | GND=7 | 3A=8, 3B=9, 3Y=10 | 4A=11, 4B=12, "
              "4Y=13 | VCC=14. Mismo patrón de salidas impares que el 7402.",
         data_title="Parámetros clave del datasheet",
         data="VCC 4.75–5.25 V · VOL máx 0.4 V con IOL 16 mA · corriente de fuga en alta 100 µA · "
              "tPD 15/20 ns · pull-up recomendada de 4.7 kΩ a 5 V para hasta 10 cargas TTL.",
         note="Cálculo del pull-up: con una carga de 10 entradas TTL (0.4 mA cada una), la "
              "resistencia máxima es R = (VCC − VOHmín) / ITOTAL = (5 − 2.4) / 0.004 = 650 Ω. "
              "En la práctica se usa 4.7 kΩ porque el fan-out real rara vez es el máximo.",
         note_label="HOJA DE DATOS", notes="Practicar el cálculo del pull-up."),

    dict(kind="gallery", section=2, transition="fade",
         title="XNOR en operación: comparación de igualdad",
         lead="Tiempos y montaje de la compuerta de coincidencia.",
         cols=2, accent="yellow",
         photos=[(p("time_xnor"), "Diagrama de tiempos del 74266: la salida permanece alta "
                                  "mientras ambas entradas tienen el mismo valor lógico."),
                 (p("pin_74266"), "Mapa de pines del 74266: salidas en los pines impares y "
                                  "colector abierto que exige pull-up externa.")],
         items=["**Comparador de 1 bit:** la salida es '1' cuando los bits comparados son "
                "iguales; en cascada (con AND) se comparan palabras completas.",
                "**Pull-up obligatoria:** sin resistencia a VCC la salida nunca llega al nivel "
                "alto y el circuito parece 'muerto'.",
                "**Lógica cableada:** al ser colector abierto, varias salidas XNOR pueden unirse "
                "en un solo nodo para obtener una función AND cableada.",
                "**Verificación práctica:** medir la salida con el multímetro en las cuatro "
                "combinaciones; si nunca hay '1', falta la resistencia de pull-up.",
                "**Alternativa:** usar el 74HC7266 si se necesita una XNOR con salida estándar."],
         note="Error típico de laboratorio: conectar el 74266 como si fuera un 7486. La tabla es "
              "inversa y la salida necesita pull-up, por lo que el circuito se comporta de "
              "manera desconcertante.",
         notes="Reforzar la lectura de la hoja de datos."),

    # ------------------------------------------------------------------ comparativa
    dict(kind="table", section=2, transition="wipe",
         title="Comparativa total de los chips estudiados",
         lead="Referencia rápida: función, compuertas por chip, tabla y aplicación principal.",
         header=["Chip", "Función", "Compuertas", "Salida = 1 cuando…", "Aplicación estrella"],
         widths=[0.10, 0.16, 0.11, 0.30, 0.33], accent="cyan", size=10.8, row_h=0.46,
         rows=[["7408", "AND", "4 × 2 entradas", "Todas las entradas están en '1'",
                "Doble confirmación de condiciones y máscaras de bits"],
               ["7432", "OR", "4 × 2 entradas", "Al menos una entrada está en '1'",
                "Alarmas multisensor y unión de señales"],
               ["7404", "NOT", "6 inversores", "La entrada está en '0'",
                "Generar variables negadas y osciladores"],
               ["7400", "NAND", "4 × 2 entradas", "No todas las entradas están en '1'",
                "Lógica universal, latches y antirrebote"],
               ["7402", "NOR", "4 × 2 entradas", "Ninguna entrada está en '1'",
                "Lógica universal en CMOS y seguridades"],
               ["7486", "XOR", "4 × 2 entradas", "Las entradas son diferentes",
                "Sumadores y bit de paridad"],
               ["74266", "XNOR", "4 × 2 entradas", "Las entradas son iguales",
                "Comparadores de igualdad (con pull-up)"],
               ["7414", "NOT Schmitt", "6 inversores", "La entrada supera el umbral VT+",
                "Señales lentas o con rebote y ruido"],
               ["74132", "NAND Schmitt", "4 × 2 entradas", "No todas las entradas en '1'",
                "Conformado de pulsos y osciladores RC"]],
         note="Todos los chips de la tabla existen en las subfamilias 74LS, 74ALS, 74F, 74HC y "
              "74HCT con el MISMO pinout: se puede cambiar la tecnología sin rediseñar el "
              "circuito, ajustando solo la corriente y la velocidad.",
         note_label="COMPATIBILIDAD", notes="Repartir como hoja de consulta impresa."),

    dict(kind="cards", section=2, transition="fade",
         title="Cómo leer cualquier símbolo de compuerta",
         lead="Formas, burbujas y etiquetas: el lenguaje gráfico universal de la lógica.",
         cols=2,
         cards=[dict(title="Forma y función", accent="cyan", num="1",
                     body="Rectángulo con frente curvo = AND. Escudo puntiagudo = OR. Triángulo "
                          "pequeño = buffer o NOT. La forma indica la operación aunque falte la "
                          "etiqueta."),
                dict(title="La burbuja de inversión", accent="pink", num="2",
                     body="Un círculo pequeño en la salida invierte el resultado: AND→NAND, "
                          "OR→NOR, XOR→XNOR, buffer→NOT. En una entrada, la burbuja indica que "
                          "ese pin es activo en bajo."),
                dict(title="Doble curva en el dorso", accent="blue", num="3",
                     body="La línea extra en la parte de atrás del símbolo identifica "
                          "exclusividad: XOR y XNOR. Sin ella, el símbolo sería un OR o un NOR "
                          "convencional."),
                dict(title="Etiquetas de pines", accent="green", num="4",
                     body="Sobre las líneas de entrada se escriben las variables (A, B, CIN, CLK) "
                          "y sobre la salida el nombre de la función (Y, S, COUT, Q). En equipos "
                          "reales, una barra sobre el nombre indica nivel bajo activo."),
                dict(title="Compuertas de 3 o más entradas", accent="purple", num="5",
                     body="Se dibujan más líneas de entrada sobre el mismo símbolo. Existen "
                          "AND de 3 entradas (7411), NAND de 8 (7430), OR de 4 (7402 "
                          "ampliado), etcétera."),
                dict(title="Símbolos IEC vs. ANSI", accent="orange", num="6",
                     body="El símbolo ANSI (americano) usa formas; el IEC (europeo) usa "
                          "rectángulos con el operador dentro (&, ≥1, =1). Ambos describen la "
                          "misma función y aparecen en distintos libros.")],
         note="Regla mnemotécnica: 'burbuja a la salida, resultado invertido; burbuja a la "
              "entrada, señal activa en bajo'. Con esa sola idea se lee cualquier esquema "
              "comercial.",
         notes="Mostrar los símbolos IEC en el pizarrón."),

    # ------------------------------------------------------------------ lógica universal
    dict(kind="twocol", section=2, transition="wipe",
         title="NAND vs. NOR: ¿cuál elegir como compuerta universal?",
         lead="Ambas construyen cualquier función; la decisión es de economía de compuertas.",
         accent="green",
         left=dict(title="Compuerta NAND (7400)", accent="green", items=[
             "**NOT:** 1 compuerta · **AND:** 2 · **OR:** 3 · **NOR:** 4.",
             "Natural en TTL porque el transistor de salida sumidera corriente con eficiencia.",
             "Menor retardo de propagación en la familia LS (9 ns típicos).",
             "Es la compuerta básica de los latches SR y de la memoria estática.",
             "Ideal cuando el diseño tiene muchas **AND y condiciones de habilitación**.",
             "Disponible también con colector abierto (7403) y Schmitt trigger (74132)."]),
         right=dict(title="Compuerta NOR (7402)", accent="pink", items=[
             "**NOT:** 1 compuerta · **OR:** 2 · **AND:** 3 · **NAND:** 4.",
             "Natural en CMOS por su estructura de pares complementarios.",
             "Menor consumo en reposo en tecnologías HC/HCT.",
             "Base del flip-flop y de los enclavamientos de seguridad industriales.",
             "Ideal cuando el diseño tiene muchas **OR y detección de condición nula**.",
             "Cuidado con su **pinout invertido**: es la fuente principal de errores de cableado."]),
         note="En un diseño real se cuentan las compuertas de cada tipo que exige la función y se "
              "elige el chip universal que menos integrados requiera. Comprometerse con un tipo "
              "de chip simplifica el armado y el diagnóstico.",
         notes="Pedir a los alumnos que cuenten compuertas en un ejemplo."),

    dict(kind="bullets", section=2, transition="wipe",
         title="Notación, familias equivalentes y sustituciones seguras",
         lead="Cómo comprar, sustituir e identificar un integrado TTL en la tienda o el laboratorio.",
         sidebar=[dict(title="Rango comercial vs. militar", accent="cyan",
                       body="Serie **74XX**: 0 °C a +70 °C, encapsulado plástico. Serie **54XX**: "
                            "−55 °C a +125 °C, encapsulado cerámico. El número y el pinout son "
                            "idénticos; solo cambia el rango y el precio."),
                  dict(title="Lectura de la fecha y el fabricante", accent="green",
                       body="En el cuerpo del chip se graban el logotipo del fabricante, el "
                            "código completo (SN74LS00N) y un código de fecha (por ejemplo 9708: "
                            "año 1997, semana 8)."),
                  dict(title="Encapsulados más comunes", accent="purple",
                       body="**N** = DIP plástico, **D** = SOIC, **PW** = TSSOP, **FK** = LCCC. "
                            "Para protoboard se requiere DIP de 0.3 pulgadas de ancho.")],
         items=["**Estructura del código:** 74 + subfamilia + número de función + tipo de "
                "encapsulado. Ejemplo: 74LS00N = familia 74, tecnología LS, función NAND cuádruple, "
                "encapsulado DIP.",
                "**El número define la función, no la tecnología:** 7400, 74LS00, 74ALS00, "
                "74F00, 74HC00 y 74HCT00 son todos NAND cuádruples con el mismo pinout.",
                "**Sustitución segura:** cambiar un LS por un ALS o un HC es válido si se "
                "respetan las corrientes de entrada; LS se cambia por HC solo si el circuito no "
                "depende de la corriente de entrada TTL.",
                "**Sustitución NO segura:** reemplazar un 7402 por otro chip cuádruple sin "
                "revisar el pinout; el 7402 tiene las salidas en pines distintos.",
                "**74HC vs. 74HCT:** los HC tienen umbrales CMOS (2.5 V) y los HCT umbrales "
                "compatibles TTL (1.6 V); en un circuito TTL debe usarse HCT o LS.",
                "**Chips con colector abierto (7403, 7405, 74266):** siempre requieren "
                "resistencia de pull-up; sin ella no entregan nivel alto.",
                "**Chips con buffer de tres estados (74125, 74126, 74125, 74LS244):** se usan "
                "para compartir un bus de datos entre varias fuentes sin cortocircuito.",
                "**Consumo y velocidad:** un 74LS típico consume 2 mW por compuerta y un 74HC "
                "prácticamente nada en reposo, pero el HC es más sensible a ESD."],
         notes="Llevar a clase un par de chips para leer el código real."),
]
