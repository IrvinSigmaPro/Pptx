# -*- coding: utf-8 -*-
"""Diapositivas adicionales de refuerzo (completan las 100)."""
import os
import theme
from theme import SRC


def p(n):
    return os.path.join(theme.GEN, n + ".png")


def s(n):
    return os.path.join(SRC, n)


AFTER_3 = [
    dict(kind="cards", section=3, transition="fade",
         title="Notas de aplicación del datasheet",
         lead="Recomendaciones que los fabricantes repiten página tras página y que evitan fallas reales.",
         cols=2,
         cards=[dict(title="Desacople obligatorio", accent="cyan", num="1",
                     body="Un capacitor de 100 nF entre VCC y GND por cada integrado, colocado a "
                          "menos de 2 cm del chip. Sin él, las corrientes de conmutación bajan "
                          "VCC momentáneamente y aparecen escrituras erróneas en registros."),
                dict(title="Entradas no utilizadas", accent="orange", num="2",
                     body="Nunca dejar entradas al aire. En TTL se pueden dejar flotando (se leen "
                          "como '1'), pero en CMOS oscilan y duplican el consumo. Conectar a VCC "
                          "o a GND según convenga a la función."),
                dict(title="Protección de salidas", accent="green", num="3",
                     body="No conectar dos salidas directamente entre sí: si una intenta poner "
                          "'1' y la otra '0' se produce un cortocircuito (corriente IOS de hasta "
                          "100 mA) y el chip se calienta. Usar salidas de tres estados."),
                dict(title="Carga capacitiva", accent="purple", num="4",
                     body="Al manejar cables largos o entradas de muchos chips, la capacidad "
                          "acumulada redondea los flancos y aumenta el retardo real. Añadir "
                          "buffers o resistencias en serie de 100 Ω."),
                dict(title="Umbrales de entrada", accent="pink", num="5",
                     body="Mantener las señales por debajo de VIL o por encima de VIH de forma "
                          "estable. Una señal que oscila cerca del umbral causa salidas "
                          "indefinidas y consumo elevado."),
                dict(title="Temperatura y disipación", accent="blue", num="6",
                     body="La potencia disipada eleva la temperatura de la unión. En "
                          "encapsulados DIP, más de 500 mW exige ventilación o reducción de la "
                          "frecuencia de conmutación.")],
         note="Todos los fabricantes incluyen estas seis notas en la sección de aplicación del "
              "datasheet: son la diferencia entre un prototipo que funciona y uno que falla de "
              "forma intermitente.",
         note_label="RESUMEN DE LA HOJA DE DATOS",
         notes="Relacionar cada nota con un error de laboratorio típico."),

    dict(kind="gallery", section=3, transition="fade",
         title="El datasheet como documento legal: absolute vs. recommended",
         lead="La diferencia entre 'aguanta' y 'funciona garantizado'.",
         cols=2, accent="red",
         photos=[(p("families"), "Curvas típicas: el fabricante publica gráficas de retardo y "
                                 "corriente frente a temperatura, tensión y carga."),
                 (p("family_tree"), "El mismo número de función mantiene su comportamiento a "
                                    "través de todas las subfamilias: solo cambian los valores "
                                    "de velocidad y consumo.")],
         items=["**Absolute maximum ratings:** límites de supervivencia. Alcanzarlos no garantiza "
                "funcionamiento, solo indica que el chip no debería destruirse de inmediato.",
                "**Recommended operating conditions:** rango en el que TODOS los parámetros de "
                "las tablas eléctricas se cumplen.",
                "**Valores 'típicos':** promedio estadístico de la producción; no son valores "
                "garantizados y no deben usarse para diseño crítico.",
                "**Valores 'máximos' y 'mínimos':** los únicos que se pueden usar para garantizar "
                "un diseño ante variación de lote, temperatura y tensión.",
                "**Rango de temperatura:** 74XX comercial de 0 °C a 70 °C; 54XX militar de −55 °C "
                "a +125 °C.",
                "**Notas al pie:** contienen condiciones de medición (carga, VCC, temperatura) "
                "sin las cuales cualquier número se malinterpreta."],
         note="En un reporte técnico se citan los valores mínimos y máximos, nunca los típicos: "
              "'el tPD típico es 9.5 ns' es información, pero el diseño debe soportar el máximo "
              "garantizado de 15 ns.",
         note_label="RIGOR DE INGENIERÍA", notes="Mostrar cómo citar correctamente un datasheet."),
]

AFTER_4 = [
    dict(kind="gallery", section=4, transition="fade",
         title="Multiplicador binario con sumadores y desplazamientos",
         lead="Cómo nace la multiplicación de compuertas AND, sumadores y registros.",
         cols=1, accent="pink",
         photos=[(p("ripple_adder"), "Multiplicación binaria: cada bit del multiplicador genera "
                                     "una fila de productos parciales (AND) que se suman "
                                     "desplazadas una posición.")],
         items=["**Producto parcial:** el AND de cada bit del multiplicador con todos los bits del "
                "multiplicando (4 AND por fila en 4 bits).",
                "**Desplazamiento:** cada fila se corre una posición a la izquierda, igual que en "
                "la multiplicación decimal hecha a mano.",
                "**Suma:** los productos parciales se acumulan con sumadores de 4 bits "
                "(74LS83/74LS283) encadenados.",
                "**Costo:** un multiplicador de 4 × 4 bits necesita 16 compuertas AND y 3 "
                "sumadores de 4 bits.",
                "**División:** se realiza con restas sucesivas y desplazamientos, empleando el "
                "mismo principio con lógica de comparación.",
                "**Aplicación:** las ALU modernas implementan multiplicadores por hardware en "
                "cascada (árboles de Wallace) con la misma idea básica."],
         note="Este bloque explica por qué la XOR y la AND conviven en la aritmética: la XOR "
              "calcula la suma sin acarreo, la AND calcula cuándo hay acarreo, y la OR los une.",
         notes="Conectar con el bloque de sumadores."),

    dict(kind="gallery", section=4, transition="fade",
         title="Comparadores de magnitud y detectores de igualdad",
         lead="Cómo decide un circuito digital si un número es mayor, igual o menor que otro.",
         cols=1, accent="purple",
         photos=[(p("memory"), "Comparadores 74LS85 (4 bits) y 74LS688 (8 bits): entregan tres "
                               "salidas de decisión (mayor, igual, menor) y se pueden encadenar "
                               "para palabras más largas.")],
         items=["**Comparador de igualdad:** se construye con compuertas XNOR (74266) más una "
                "gran AND, o directamente con el 74LS688.",
                "**Comparador de magnitud:** el 74LS85 entrega A > B, A = B y A < B para palabras "
                "de 4 bits, con entradas de cascada.",
                "**Cascada:** uniendo varios 74LS85 se comparan palabras de 8, 12, 16 bits o más.",
                "**Aplicación 1:** control de temperatura o nivel donde se activa una alarma al "
                "superar un umbral.",
                "**Aplicación 2:** direccionamiento de memoria: el 74LS688 compara el bus de "
                "direcciones con un valor fijo y activa el chip select.",
                "**Aplicación 3:** detección de fin de conteo, comparación de contraseñas y "
                "validación de datos recibidos.",
                "**Igualdad con XNOR:** dos números binarios son iguales si todas las XNOR de sus "
                "bits correspondientes valen '1'."],
         note="Regla de diseño: para comparar solo igualdad basta con XNOR y AND; si se necesita "
              "saber cuál es mayor, hay que usar un comparador de magnitud dedicado como el "
              "74LS85, porque la lógica combinacional equivalente crece muy rápido.",
         notes="Explicar por qué la comparación de magnitud requiere más lógica."),
]

AFTER_5 = [
    dict(kind="steps", section=5, transition="fade",
         title="Práctica guiada 1: medio sumador en protoboard",
         lead="Procedimiento completo de la primera práctica de aritmética digital.",
         accent="blue", img=p("half_adder"),
         steps=[dict(text="Identificar y colocar el 7486 (XOR) y el 7408 (AND) respetando la "
                          "muesca; conectar VCC (pin 14) y GND (pin 7) en ambos chips."),
                dict(text="Instalar un capacitor de desacople de 100 nF entre VCC y GND junto a "
                          "cada integrado."),
                dict(text="Cablear dos interruptores (o puentes) como entradas A y B hacia las "
                          "entradas 1 y 2 de la XOR y también de la AND."),
                dict(text="Conectar la salida de la XOR (pin 3) a un LED verde: representa la "
                          "suma S."),
                dict(text="Conectar la salida de la AND (pin 3) a un LED rojo: representa el "
                          "acarreo C."),
                dict(text="Verificar la tabla de verdad completa: 00 → S=0, C=0; 01 → S=1, C=0; "
                          "10 → S=1, C=0; 11 → S=0, C=1."),
                dict(text="Anotar los valores medidos con el multímetro para cada combinación y "
                          "registrarlos en la tabla del reporte.")],
         warn="Recordar la lógica de sumidero del TTL: conectar el LED entre VCC y la salida, "
              "nunca entre la salida y GND, porque el chip absorbe corriente mucho mejor de lo "
              "que la entrega.",
         notes="Primera práctica; insistir en la verificación de alimentación."),

    dict(kind="steps", section=5, transition="fade",
         title="Práctica guiada 2: contador decimal con display",
         lead="Contador de 0 a 9 con salida visual en display de 7 segmentos.",
         accent="red", img=p("sevenseg"),
         steps=[dict(text="Colocar un 74LS90 (contador de décadas) y un 74LS47 (decodificador BCD "
                          "a 7 segmentos) con su alimentación y desacople."),
                dict(text="Conectar la salida del contador (QA, QB, QC, QD) a las entradas A, B, "
                          "C, D del decodificador."),
                dict(text="Unir cada salida del decodificador (a–g) a su segmento con una "
                          "resistencia de 330 Ω en serie."),
                dict(text="Aplicar pulsos manuales al pin de reloj del contador con un pulsador "
                          "antirrebote o con una señal de baja frecuencia."),
                dict(text="Verificar que el display cuenta 0, 1, 2… 9 y regresa a 0 al siguiente "
                          "pulso."),
                dict(text="Añadir un segundo contador en cascada y obtener un contador de 0 a 99 "
                          "con dos displays."),
                dict(text="Documentar el consumo total del montaje midiendo la corriente de la "
                          "fuente para dimensionarla correctamente.")],
         warn="El 74LS47 tiene salidas de colector abierto: sin las resistencias limitadoras de "
              "330 Ω los segmentos del display recibirán corriente excesiva y se quemarán.",
         notes="Práctica integradora del bloque secuencial y de display."),
]
