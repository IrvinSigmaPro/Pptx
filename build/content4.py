# -*- coding: utf-8 -*-
"""Sección 4 — Aplicaciones reales de la Serie 74XX."""
import os
from theme import SRC, GEN


def p(n):
    return os.path.join(GEN, n + ".png")


def s(n):
    return os.path.join(SRC, n)


SLIDES = [
    dict(kind="section", section=4, transition="zoom",
         img=p("sec_apps"), topics=[
             "Lógica combinacional vs. secuencial: la diferencia esencial",
             "Sumadores: medio sumador, sumador completo y 74LS83/74LS283 en cascada",
             "Multiplexores, decodificadores y codificadores (74LS151, 74LS138, 74LS148)",
             "Displays de 7 segmentos y decodificadores BCD (74LS47 / 74LS48)",
             "Memoria de un bit: latch SR, flip-flop D y registros (74LS74, 74LS164)",
             "Contadores binarios y memorias de la familia 74LS"],
         notes="Apertura del bloque 4."),

    dict(kind="gallery", section=4, transition="fade",
         title="Lógica combinacional vs. lógica secuencial",
         lead="Con memoria o sin memoria: la división fundamental de los circuitos digitales.",
         cols=1, accent="green",
         photos=[(p("comb_vs_seq"), "El circuito combinacional responde solo a las entradas "
                                    "presentes; el secuencial guarda un estado previo y depende "
                                    "de él."),
                 (s("image7.png"), "Panel didáctico de laboratorio (2019): símbolos reales de "
                                   "compuertas, multiplexor, decodificador, codificador, "
                                   "flip-flops y sumador de 4 bits. Fotografía del autor.")],
         items=["**Circuito combinacional:** la salida depende EXCLUSIVAMENTE de las entradas "
                "actuales. No tiene memoria ni reloj.",
                "Ejemplos combinacionales: compuertas sueltas, comparadores, sumadores, "
                "multiplexores, decodificadores (7400, 7408, 7486, 74138).",
                "**Circuito secuencial:** la salida depende de las entradas Y del estado anterior, "
                "almacenado en biestables.",
                "Ejemplos secuenciales: latches, flip-flops, contadores, registros y memorias "
                "(7474, 74161, 74164, 74189).",
                "**El reloj** sincroniza los cambios de estado: sin flanco no hay cambio, y eso "
                "elimina los glitches de la lógica combinacional intermedia.",
                "**Diseño mixto:** en la práctica todo sistema digital combina ambos mundos: la "
                "lógica combinacional decide, el registro memoriza.",
                "**Dos tipos de máquina de estados:** Moore (la salida depende del estado), "
                "Mealy (depende de estado y entradas)."],
         note="Ejercicio mental: un semáforo con temporizador es secuencial; detectar si dos "
              "números binarios son iguales con XOR y AND es combinacional.",
         notes="Dar varios ejemplos y pedir a los alumnos que clasifiquen."),

    dict(kind="gallery", section=4, transition="fade",
         title="Medio sumador (Half Adder) con compuertas",
         lead="La célula aritmética mínima: una XOR y una AND bastan para sumar dos bits.",
         cols=1, accent="blue",
         photos=[(p("half_adder"), "Medio sumador: S = A ⊕ B entrega la suma y C = A·B el "
                                   "acarreo. Es el circuito aritmético más simple que existe.")],
         items=["**Suma (S):** A ⊕ B. Es '1' cuando las entradas son diferentes, lo que equivale "
                "a 1 + 0 o 0 + 1.",
                "**Acarreo (C):** A · B. Solo hay acarreo cuando ambas entradas son '1' (1 + 1 = "
                "10₂).",
                "**Limitación:** no considera un acarreo entrante, por lo que no se puede "
                "encadenar directamente.",
                "**Tabla de verdad:** 0+0=00, 0+1=01, 1+0=01, 1+1=10. El resultado se lee como "
                "C seguido de S.",
                "**Implementación:** un 7486 (XOR) y un 7408 (AND) forman el circuito completo; "
                "también se hace con 5 compuertas NAND del 7400.",
                "**Uso:** es la primera práctica de aritmética digital y el bloque de "
                "construcción del sumador completo.",
                "**Verificación:** probar las cuatro combinaciones con LEDs y comprobar que solo "
                "1+1 produce acarreo."],
         note="Del medio sumador al procesador: encadenando sumadores completos se construye la "
              "unidad aritmética lógica (ALU) que suma, resta y compara en cualquier CPU.",
         notes="Pedir a los alumnos que implementen el medio sumador con solo 7400."),

    dict(kind="gallery", section=4, transition="fade",
         title="Sumador completo (Full Adder)",
         lead="Añade el acarreo entrante y permite encadenar sumadores para palabras de varios bits.",
         cols=1, accent="teal",
         photos=[(p("full_adder"), "Sumador completo: dos XOR para la suma, dos AND para los "
                                   "acarreos parciales y una OR para el acarreo de salida.")],
         items=["**Entradas:** A, B y Cin (acarreo entrante de la etapa anterior).",
                "**Suma:** S = A ⊕ B ⊕ Cin. Es '1' cuando el número de entradas altas es IMPAR.",
                "**Acarreo de salida:** Cout = A·B + Cin·(A ⊕ B). Se activa cuando al menos dos "
                "entradas son '1'.",
                "**Componentes:** dos XOR (una del 7486), dos AND y una OR (7408 + 7432), o "
                "nueve compuertas NAND del 7400.",
                "**Integrado dedicado:** el 74LS83 (y el 74LS283) contiene un sumador completo de "
                "4 bits con acarreo rápido en un solo chip.",
                "**Aplicación:** es el bloque básico de las ALU; con 32 de ellos se construye un "
                "sumador de 32 bits como el de un procesador sencillo.",
                "**Resta:** invirtiendo B y poniendo Cin = 1 se obtiene A − B mediante "
                "complemento a dos."],
         note="Cálculo del retardo en cascada: cuatro sumadores completos encadenados acumulan "
              "4 × tPD de acarreo, lo que limita la frecuencia máxima de la suma.",
         notes="Mostrar el diagrama y explicar el acarreo rápido."),

    dict(kind="gallery", section=4, transition="fade",
         title="Sumador binario de 4 bits en cascada",
         lead="Cómo se suman palabras completas y por qué el acarreo se propaga como una onda.",
         cols=1, accent="cyan",
         photos=[(p("ripple_adder"), "Sumador de acarreo ondulante: cada etapa entrega su acarreo "
                                     "a la siguiente; se implementa con 74LS83 o con cuatro "
                                     "sumadores completos.")],
         items=["**Arquitectura ripple-carry:** el acarreo viaja de la etapa menos significativa "
                "a la más significativa, como en una suma hecha a mano.",
                "**Resultado:** 4 bits de suma (S0–S3) más el acarreo final C4, que indica "
                "desbordamiento de la palabra.",
                "**Ejemplo:** 1011₂ + 0110₂ = 10001₂ (11 + 6 = 17, con acarreo de salida).",
                "**Integrado 74LS83:** contiene el sumador de 4 bits completo y permite encadenar "
                "dos chips para obtener 8 bits.",
                "**Prestaciones:** máxima frecuencia de operación limitada por el tiempo de "
                "propagación del acarreo (unos 20 ns por etapa en 74LS83).",
                "**Alternativa rápida:** el 74LS283 usa lógica de anticipación de acarreo, mucho "
                "más rápida que el encadenamiento simple.",
                "**Aplicación histórica:** los primeros microprocesadores usaban el 74181 (ALU de "
                "4 bits) y el 74182 (unidad de acarreo anticipado) para construir sus CPU."],
         note="El 74181 es una ALU completa de 4 bits que realiza 16 operaciones lógicas y 16 "
              "aritméticas; fue pieza clave de las minicomputadoras de los años setenta y del "
              "primer computador personal.",
         notes="Este bloque conecta la electrónica digital con la arquitectura de computadoras."),

    dict(kind="gallery", section=4, transition="fade",
         title="Multiplexor: seleccionar una señal entre muchas",
         lead="El 'conmutador digital' que permite compartir un canal de datos.",
         cols=1, accent="purple",
         photos=[(p("mux4"), "Multiplexor 4:1: las líneas de selección S1 y S0 eligen cuál de las "
                             "cuatro entradas llega a la salida única.")],
         items=["**Definición:** circuito combinacional que conecta una de 2^n entradas a la "
                "salida única, según el código de selección.",
                "**MUX 4:1:** 4 entradas de datos, 2 líneas de selección, 1 salida. Ecuación: "
                "Y = D0·S1'S0' + D1·S1'S0 + D2·S1S0' + D3·S1S0.",
                "**Integrados comerciales:** 74LS151 (8:1), 74LS153 (dos de 4:1), 74LS157 "
                "(cuádruple 2:1).",
                "**Aplicación 1:** compartir un bus. Varias fuentes de datos eligen su turno para "
                "transmitir por un solo cable.",
                "**Aplicación 2:** implementar cualquier función lógica de n variables con un "
                "multiplexor de 2^n entradas, conectando las entradas a 0 y 1 según la tabla de "
                "verdad.",
                "**Aplicación 3:** multiplexar displays de 7 segmentos para ahorrar pines y "
                "corriente.",
                "**Selección de datos:** los procesadores usan multiplexores para escoger "
                "resultados de la ALU, entradas de registros y direcciones de memoria."],
         note="Truco de diseño: un multiplexor 74LS151 puede implementar cualquier función "
              "booleana de 3 variables sin simplificar. Es la solución más rápida cuando no se "
              "quiere aplicar Karnaugh.",
         notes="Explicar el uso del MUX como implementación universal."),

    dict(kind="gallery", section=4, transition="fade",
         title="Decodificador 3 a 8 (74LS138)",
         lead="Convierte un código binario en la activación de una sola línea de salida.",
         cols=1, accent="orange",
         photos=[(p("decoder38"), "Decodificador 3:8: para cada combinación de A2 A1 A0 se activa "
                                  "exactamente una de las ocho salidas, siempre y cuando las "
                                  "entradas de habilitación lo permitan.")],
         items=["**Función:** recibe 3 bits de dirección y activa una de 8 salidas (activas en "
                "bajo en el 74LS138).",
                "**Entradas de habilitación:** G1, G2A y G2B permiten encadenar decodificadores "
                "para construir decodificadores de 4, 5 o más bits.",
                "**Aplicación 1 — decodificador de direcciones:** selecciona chips de memoria o "
                "periféricos en un bus.",
                "**Aplicación 2 — expansión de puertos:** activa un dispositivo a la vez.",
                "**Aplicación 3 — decodificador BCD:** los 74LS42 y 74LS47 decodifican "
                "directamente de BCD.",
                "**Encadenamiento:** dos 74LS138 más un inversor forman un decodificador de 4 "
                "bits con 16 salidas.",
                "**Verificación:** medir con la punta lógica que solo una salida cambia por cada "
                "combinación de entradas."],
         note="En placas comerciales el decodificador de direcciones es el que decide qué chip "
              "responde; un error de un bit aquí provoca conflictos de bus y fallas difíciles de "
              "detectar.",
         notes="Insistir en las salidas activas en bajo del 74LS138."),

    dict(kind="gallery", section=4, transition="fade",
         title="Codificador 8 a 3 (74LS148) y teclados",
         lead="El proceso inverso: convertir la línea activa en su número binario.",
         cols=1, accent="pink",
         photos=[(p("encoder83"), "Codificador prioritario 8:3: cuando hay varias entradas "
                                  "activas, la salida corresponde a la de mayor prioridad, y "
                                  "GS indica que existe al menos una entrada activa.")],
         items=["**Función:** convierte 8 líneas de entrada en 3 bits de salida que expresan la "
                "posición de la línea activa.",
                "**Prioridad:** si varias entradas están activas, gana la de número mayor (el "
                "74LS148 es prioritario).",
                "**Entradas/salidas de control:** EI (enable input), EGS (group select) y EO "
                "(enable output) permiten encadenar varios chips.",
                "**Aplicación clásica — teclados matriciales:** 16 teclas con 74LS148 y "
                "codificación binaria a un microcontrolador.",
                "**Aplicación — interrupciones:** identifica cuál periférico pidió atención.",
                "**Combinación codificador + decodificador:** base de la transmisión reducida de "
                "señales en sistemas con muchos sensores.",
                "**Ejercicio de laboratorio:** encender un display de 7 segmentos con la salida "
                "del codificador para mostrar la posición activa."],
         note="Al emparejar un codificador 74LS148 con un decodificador 74LS138 se obtiene un "
              "'cable de señales comprimido': 8 líneas se transmiten por 3 cables y se reconstruyen "
              "al otro extremo.",
         notes="Comparar el codificador con el decodificador."),

    dict(kind="gallery", section=4, transition="fade",
         title="Display de 7 segmentos con el 74LS47",
         lead="De un número BCD a un dígito visible: la interfaz visual más usada en prácticas.",
         cols=1, accent="red",
         photos=[(p("sevenseg"), "Decodificador BCD a 7 segmentos 74LS47: recibe cuatro bits y "
                                 "controla los siete segmentos, con salidas activas en bajo "
                                 "para el display de ánodo común.")],
         items=["**Función:** convierte un dato BCD (0000 a 1001) en las siete señales de un "
                "display de 7 segmentos.",
                "**74LS47 vs. 74LS48:** el 47 tiene salidas activas en bajo (ánodo común) y "
                "requiere resistencias limitadoras; el 48 es activo en alto (cátodo común) e "
                "incluye salidas para probar el display.",
                "**Pines de control:** LT (lamp test) prueba todos los segmentos, BI/RBO apaga el "
                "display y RBI permite suprimir ceros a la izquierda.",
                "**Resistencias:** 330 Ω por segmento con VCC = 5 V y corriente de 8 mA por "
                "segmento.",
                "**Multiplexado:** encender solo un dígito a la vez y repetir rápidamente reduce "
                "el número de decodificadores necesarios.",
                "**Expansión:** varios 74LS47 con contadores 74LS90 forman un contador decimal de "
                "varios dígitos.",
                "**Verificación:** introducir 0000–1001 y comprobar que aparecen los dígitos 0 "
                "al 9 en orden."],
         note="Cuidado con el 74LS47: al ser de colector abierto, los segmentos requieren "
              "resistencia limitadora externa; sin ella se quemarían los segmentos del display.",
         note_label="PRECAUCIÓN", notes="Explicar ánodo común vs. cátodo común."),

    dict(kind="gallery", section=4, transition="fade",
         title="Memoria de un bit: el latch SR con NAND",
         lead="El circuito que da memoria a la lógica: retroalimentación cruzada entre dos compuertas.",
         cols=1, accent="green",
         photos=[(p("latch_sr"), "Latch SR construido con dos compuertas NAND (7400) "
                                 "retroalimentadas: la salida se mantiene después de retirar la "
                                 "señal que la provocó.")],
         items=["**Funcionamiento:** S = 0 (set) lleva Q a '1'; R = 0 (reset) lleva Q a '0'; "
                "S = R = 1 mantiene el estado anterior.",
                "**Estado prohibido:** S = R = 0 simultáneos producen Q = Q' = 1, estado "
                "inconsistente que debe evitarse.",
                "**Retroalimentación:** la clave es que la salida de cada compuerta alimenta la "
                "entrada de la otra.",
                "**Antirrebote:** un interruptor conectado a un latch SR entrega una sola "
                "transición limpia por cada pulsación.",
                "**Versión NOR:** con el 7402 el set y el reset son activos en alto, y el estado "
                "prohibido es S = R = 1.",
                "**Latches comerciales:** 74LS279 (cuádruple SR) y 74LS373 (latch octal con "
                "habilitación).",
                "**Diferencia con el flip-flop:** el latch es transparente mientras la "
                "habilitación está activa; el flip-flop solo cambia en el flanco del reloj."],
         note="La memoria digital nace de la retroalimentación: dos compuertas que se miran entre "
              "sí mantienen un bit indefinidamente mientras haya alimentación.",
         notes="Armar el latch en el pizarrón y seguir el estado paso a paso."),

    dict(kind="gallery", section=4, transition="fade",
         title="Flip-flop D disparado por flanco (74LS74)",
         lead="La memoria sincronizada con el reloj: la base de registros, contadores y RAM.",
         cols=1, accent="indigo",
         photos=[(p("ff_d"), "Flip-flop D: la entrada D se copia a la salida Q únicamente en el "
                             "flanco de subida del reloj; el resto del tiempo la salida se "
                             "mantiene.")],
         items=["**Función:** Q toma el valor de D en el instante del flanco (típicamente de "
                "subida) del reloj.",
                "**Entradas de control:** preset (PRE) y clear (CLR) activos en bajo permiten "
                "fijar el estado sin reloj.",
                "**Tabla de verdad:** sin flanco, Q no cambia; con flanco ascendente, Q = D.",
                "**Divisor de frecuencia:** conectando Q' a D, el flip-flop divide la frecuencia "
                "del reloj entre dos.",
                "**Registro de 4 bits:** cuatro flip-flops D comparten el mismo reloj y "
                "almacenan una palabra completa.",
                "**Integrados:** 74LS74 (dos D con preset y clear), 74LS175 (cuádruple D), "
                "74LS374 (octal con salidas de tres estados).",
                "**Sincronía:** al cambiar los estados solo en el flanco, el sistema elimina los "
                "glitches de la lógica combinacional."],
         note="Regla de oro de la electrónica secuencial: 'la lógica combinacional decide, el "
              "flip-flop memoriza en el flanco'. Con esa idea se diseña cualquier máquina de "
              "estados.",
         notes="Mostrar el diagrama de tiempos del reloj y Q."),

    dict(kind="gallery", section=4, transition="fade",
         title="Contadores binarios (74LS161 / 74LS163)",
         lead="Flip-flops encadenados que cuentan pulsos: el reloj más común de los sistemas digitales.",
         cols=1, accent="teal",
         photos=[(p("counter4"), "Contador binario de 4 bits: cada etapa divide entre dos la "
                                 "frecuencia de la anterior, recorriendo los 16 estados del "
                                 "0000 al 1111.")],
         items=["**Modo de operación:** cada flanco de reloj incrementa el valor binario en una "
                "unidad: 0000, 0001, 0010… hasta 1111 y regresa a 0000.",
                "**Módulo:** un contador de n bits completa 2^n estados. Con 4 bits el módulo es "
                "16 (0 a 15).",
                "**Contador de décadas:** el 74LS90 y el 74LS390 cuentan de 0 a 9, ideales para "
                "displays decimales.",
                "**Carga y reinicio:** el 74LS163 tiene carga síncrona (LOAD) para programar el "
                "valor inicial y construir módulos arbitrarios.",
                "**Cascada:** encadenando dos contadores de 4 bits se obtiene uno de 8 bits con "
                "256 estados.",
                "**Aplicaciones:** relojes y temporizadores digitales, divisores de frecuencia, "
                "generadores de direcciones de memoria y máquinas de estados.",
                "**Práctica clásica:** contador de 0 a 99 con dos 74LS90 y dos displays de 7 "
                "segmentos."],
         note="División de frecuencia: si el reloj de entrada es de 1 MHz, un contador de 4 bits "
              "entrega 62.5 kHz en su bit más significativo; cada flip-flop divide entre dos.",
         notes="Relacionar con temporizadores y relojes digitales."),

    dict(kind="gallery", section=4, transition="fade",
         title="Registro de desplazamiento (74LS164 / 74LS194)",
         lead="Bits que se mueven en cadena: conversión serie-paralelo y memoria de datos.",
         cols=1, accent="blue",
         photos=[(p("shiftreg"), "Registro de desplazamiento: los datos entran en serie por un "
                                 "extremo y avanzan una posición en cada pulso de reloj.")],
         items=["**Funcionamiento:** en cada flanco de reloj cada flip-flop copia el contenido del "
                "anterior, y el nuevo bit entra por la izquierda.",
                "**Serie → paralelo:** recibe bits uno a uno y después los presenta todos juntos "
                "en sus salidas (74LS164).",
                "**Paralelo → serie:** el 74LS165 carga 8 bits a la vez y los transmite uno por "
                "uno.",
                "**Universal (74LS194):** permite desplazar a derecha, a izquierda, cargar en "
                "paralelo y mantener estado.",
                "**Aplicación 1:** comunicación serie donde un solo cable transmite varios bits "
                "consecutivos.",
                "**Aplicación 2:** barrido de displays y matrices de LED (efecto de barrido "
                "visual).",
                "**Aplicación 3:** multiplicación y división binaria por potencias de dos: "
                "desplazar a la izquierda multiplica, a la derecha divide."],
         note="Desplazar un byte a la izquierda equivale a multiplicar por 2 (siempre que no se "
              "pierda el bit más significativo) y desplazarlo a la derecha equivale a dividir "
              "entre 2.",
         notes="Mostrar la relación con la multiplicación binaria."),

    dict(kind="gallery", section=4, transition="fade",
         title="Memorias y dispositivos de la familia 74XX",
         lead="Antes de los microcontroladores, la familia 74XX ya incluía memoria y periféricos.",
         cols=1, accent="yellow",
         photos=[(p("memory"), "Catálogo de memorias y periféricos: RAM 74LS189, PROM 74LS288, "
                               "registros de banco, transceptores y comparadores de bus."),
                 (s("image1.png"), "Placa de circuito impreso con integrados montados: los "
                                   "circuitos digitales modernos siguen usando la misma lógica "
                                   "de compuertas en su interior. Imagen: electronics-lab.com.")],
         items=["**74LS189 — RAM estática de 64 bits:** organizada como 16 palabras de 4 bits, "
                "con entradas de dirección A0–A3 y datos D0–D3.",
                "**74LS288 / 74LS289 — PROM:** memoria de solo lectura programable por el usuario, "
                "usada para tablas de conversión y microcódigo.",
                "**74LS670 — registro de banco 4×4:** permite escritura y lectura en direcciones "
                "independientes (memoria de doble puerto primitiva).",
                "**74LS373 / 74LS374 — latch y flip-flop octal:** almacenan un byte completo con "
                "salidas de tres estados.",
                "**74LS245 — transceptor octal:** controla la dirección del flujo de datos en un "
                "bus (A→B o B→A).",
                "**74LS688 — comparador de 8 bits:** genera una señal de coincidencia cuando la "
                "dirección del bus es igual a la configurada.",
                "**Aplicación histórica:** con estos chips se construían computadoras completas de "
                "8 bits y tarjetas de E/S para microprocesadores como el Z80 o el 8085."],
         note="Estos chips permiten entender cómo funciona internamente una memoria: selección de "
              "chip, dirección, lectura/escritura y salidas de tres estados para compartir el bus "
              "de datos.",
         notes="Conectar con la arquitectura de computadoras."),

    dict(kind="bullets", section=4, transition="wipe",
         title="Arquitectura de un sistema digital con 74XX",
         lead="Cómo se ensamblan todas las piezas para construir un sistema completo.",
         sidebar=[dict(title="Bus de datos", accent="cyan",
                       body="8 líneas compartidas por todos los chips. Solo el dispositivo "
                            "seleccionado activa sus salidas de tres estados (74LS245, 74LS374)."),
                  dict(title="Bus de direcciones", accent="orange",
                       body="Selecciona la posición de memoria o el periférico. El 74LS138 "
                            "decodifica la dirección y activa el chip correspondiente."),
                  dict(title="Bus de control", accent="green",
                       body="Señales de reloj, lectura/escritura (RD/WR) e interrupciones que "
                            "coordinan el momento exacto de cada operación.")],
         items=["**Unidad de proceso:** registros (74LS374), ALU (74LS181) y contador de programa "
                "(74LS161).",
                "**Decodificación:** el 74LS138 traduce la dirección en la activación de un chip "
                "concreto.",
                "**Memoria:** RAM 74LS189 y PROM 74LS288 para datos y microcódigo.",
                "**Entrada/salida:** buffers (74LS244), latches (74LS373) y transceptores "
                "(74LS245).",
                "**Sincronización:** un oscilador (cristal de cuarzo con 7404) genera el reloj "
                "maestro del sistema.",
                "**Inicialización:** la señal RESET activa en bajo limpia todos los registros y "
                "coloca el contador de programa en cero.",
                "**Concepto clave:** estos tres buses (datos, direcciones y control) siguen siendo "
                "la arquitectura de cualquier computadora actual, solo que integrada en un solo "
                "chip."],
         note="El bus de tres estados es la clave de la arquitectura: sin la capacidad de "
              "desconectar salidas (estado Z) sería imposible compartir un mismo conjunto de "
              "líneas entre muchos integrados.",
         notes="Puede ser el puente hacia la siguiente unidad: microcontroladores."),

    dict(kind="gallery", section=4, transition="fade",
         title="Flujo de diseño: del enunciado al circuito montado",
         lead="Metodología ordenada que evita el 90 % de los errores en el laboratorio.",
         cols=1, accent="green",
         photos=[(p("design_flow"), "Seis pasos: especificar, tabular, simplificar, seleccionar "
                                    "chips, simular y montar. Saltarse un paso se paga con horas "
                                    "de depuración.")],
         items=["**1. Especificar:** definir con precisión entradas, salidas y comportamiento "
                "esperado; anotar niveles activos.",
                "**2. Tabla de verdad:** listar todas las combinaciones (2^n filas) y tabular cada "
                "salida.",
                "**3. Simplificar:** aplicar Boole, De Morgan o Karnaugh hasta la expresión "
                "mínima.",
                "**4. Seleccionar chips:** contar compuertas por tipo y elegir integrados con el "
                "menor número de paquetes.",
                "**5. Simular:** verificar en Logisim, Multisim, Proteus o Tinkercad antes de "
                "tomar el cautín.",
                "**6. Montar y medir:** cablear por etapas, alimentar y comprobar cada bloque con "
                "la punta lógica antes de avanzar.",
                "**Documentar:** anotar el diagrama final, el pinout usado y las mediciones "
                "obtenidas para reproducir el montaje."],
         note="Errores más frecuentes: empezar a cablear sin simplificar, olvidar la alimentación, "
              "confundir el orden de los pines del 7402 y dejar entradas CMOS flotantes.",
         notes="Usar esta lista como rúbrica de proyecto."),
]
