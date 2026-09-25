# -*- coding: utf-8 -*-
"""Sección 5 — Práctica de laboratorio y diagnóstico de fallas."""
import os
import theme
from theme import SRC


def p(n):
    return os.path.join(theme.GEN, n + ".png")


def s(n):
    return os.path.join(SRC, n)


SLIDES = [
    dict(kind="section", section=5, transition="zoom",
         img=p("sec_lab"), topics=[
             "Materiales y equipo indispensable para armar circuitos con la Serie 74XX",
             "Montaje paso a paso en protoboard con alimentación y desacople correctos",
             "Medición con multímetro, punta lógica y osciloscopio",
             "Procedimiento de verificación por bloques y tabla de verdad real",
             "Diagnóstico sistemático de fallas: síntoma, causa probable y solución",
             "Buenas prácticas, seguridad y reglas de oro del laboratorio digital"],
         notes="Apertura del bloque 5."),

    dict(kind="cards", section=5, transition="fade",
         title="Materiales y equipo del laboratorio",
         lead="Lo que se necesita sobre la mesa antes de empezar a cablear.",
         cols=3,
         cards=[dict(title="Protoboard", num="830", accent="cyan",
                     body="Tablero de conexiones sin soldadura con dos buses de alimentación y "
                          "64 columnas de 5 contactos. Permite modificar el circuito sin "
                          "desoldar."),
                dict(title="Fuente de 5 V", num="1 A", accent="orange",
                     body="Fuente regulada de 5 V DC con limitación de corriente. Nunca usar "
                          "fuentes sin regular ni baterías sin protección contra polaridad "
                          "inversa."),
                dict(title="Juego de cables", num="#22", accent="green",
                     body="Cables rígidos calibre 22 de distintos colores: rojo para VCC, negro "
                          "para GND y colores para señales. Colores consistentes simplifican el "
                          "diagnóstico."),
                dict(title="Multímetro digital", num="V/A/Ω", accent="purple",
                     body="Para medir VCC, los niveles de salida y detectar continuidad. Imprescin"
                          "dible antes de energizar el circuito."),
                dict(title="Punta lógica", num="LED", accent="pink",
                     body="Instrumento de dos LEDs (rojo/verde) que permite observar el nivel "
                          "lógico de cualquier pin sin detener el circuito."),
                dict(title="LEDs y resistencias", num="330 Ω", accent="blue",
                     body="LEDs como indicadores visuales de estado. Resistencia de 330 Ω para "
                          "limitar la corriente a unos 10 mA por LED."),
                dict(title="Chips de la Serie 74XX", num="DIP-14", accent="teal",
                     body="7400, 7408, 7432, 7404, 7402, 7486. Conviene tener dos de cada uno: "
                          "uno puede dañarse durante la práctica."),
                dict(title="Extractor de chips", num="DIP", accent="indigo",
                     body="Herramienta para retirar integrados sin doblar los pines. Retirar un "
                          "chip a mano es la forma más común de romper una patita."),
                dict(title="Hojas de datos impresas", num="PDF", accent="yellow",
                     body="Pinout impreso de cada chip que se va a usar. Consultarlo en pantalla "
                          "mientras se cablea provoca errores de orientación.")],
         note="Recuerda: el 80 % de las fallas en prácticas escolares provienen de alimentación "
              "mal conectada, cables flojos o entradas flotantes, no de chips dañados.",
         notes="Revisar la lista antes de entrar al laboratorio."),

    dict(kind="steps", section=5, transition="fade",
         title="Montaje paso a paso en protoboard",
         lead="Procedimiento probado para armar un circuito digital sin sorpresas.",
         accent="cyan",
         img=p("breadboard"),
         steps=[dict(text="Colocar el integrado a caballo sobre el canal central de la "
                          "protoboard, con la muesca hacia la izquierda y contando pines desde "
                          "esa referencia."),
                dict(text="Conectar primero la alimentación: VCC (pin 14) al bus rojo y GND "
                          "(pin 7) al bus azul. Verificar continuidad con el multímetro antes de "
                          "encender."),
                dict(text="Instalar el capacitor de desacople de 100 nF cerámico entre VCC y GND "
                          "lo más cerca posible del chip."),
                dict(text="Cablear las entradas de las compuertas a interruptores o a VCC/GND "
                          "mediante resistencias, nunca dejarlas al aire."),
                dict(text="Conectar las salidas a LEDs con resistencia limitadora de 330 Ω en "
                          "serie, respetando la polaridad del LED (ánodo al positivo)."),
                dict(text="Encender la fuente y verificar con el multímetro que VCC mida entre "
                          "4.75 y 5.25 V en el pin 14 del chip."),
                dict(text="Probar la tabla de verdad completa: aplicar cada combinación de "
                          "entradas y anotar el estado del LED de salida comparándolo con la "
                          "tabla esperada."),
                dict(text="Documentar: fotografiar el montaje, anotar el pinout usado y registrar "
                          "las mediciones para el reporte de práctica.")],
         warn="Nunca insertar o retirar un integrado con la alimentación encendida, y nunca "
              "conectar el chip invertido: la polaridad inversa es la causa número uno de chip "
              "dañado en el laboratorio.",
         notes="Reforzar la verificación de VCC antes de conectar señales."),

    dict(kind="gallery", section=5, transition="fade",
         title="Alimentación, desacople y manejo de cargas",
         lead="El montaje eléctrico básico que garantiza que la lógica funcione.",
         cols=1, accent="yellow",
         photos=[(p("power_setup"), "Esquema básico: alimentación de 5 V, capacitor de desacople "
                                    "de 100 nF junto al chip, resistencia limitadora y LED de "
                                    "salida.")],
         items=["**VCC = 5 V ± 5 %:** por debajo de 4.75 V los niveles lógicos dejan de estar "
                "garantizados y aparecen fallas intermitentes.",
                "**Capacitor de desacople:** 100 nF cerámico entre VCC y GND por cada chip, con "
                "pines cortos, para absorber los picos de corriente de la conmutación.",
                "**Cálculo del LED:** R = (VCC − VF) / IF = (5 V − 2 V) / 10 mA = 300 Ω → valor "
                "comercial 330 Ω.",
                "**Lógica de sumidero en TTL:** conectar el LED entre VCC y la salida (no entre "
                "salida y GND), porque el TTL absorbe mucha más corriente de la que entrega.",
                "**Entradas flotantes:** en TTL una entrada al aire se lee como '1'; en CMOS "
                "oscila y provoca consumo excesivo. Siempre fijar la entrada con resistencia o "
                "puente.",
                "**Pull-up en colector abierto:** 4.7 kΩ entre la salida y VCC para los chips "
                "7403, 7405 y 74266.",
                "**Resistencia en serie en entradas:** añadir 1 kΩ cuando la señal viene de un "
                "cable largo para limitar la corriente de los diodos de protección."],
         note="Comprobación rápida con el multímetro: con el circuito encendido y sin señales, "
              "medir VCC en el pin 14 de cada chip. Si hay 5 V en el bus pero no en el chip, hay "
              "un cable roto o un contacto flojo.",
         notes="Explicar el uso del capacitor de desacople y por qué es indispensable."),

    dict(kind="steps", section=5, transition="fade",
         title="Medición y verificación con instrumentos",
         lead="Cómo comprobar el funcionamiento real de una compuerta paso a paso.",
         accent="purple", img=p("probe"),
         steps=[dict(text="Antes de energizar: medir continuidad entre VCC y GND para descartar "
                          "un cortocircuito (una lectura baja indica error de cableado)."),
                dict(text="Encender la fuente y verificar 5 V entre el pin 14 y el pin 7 del "
                          "integrado, usando el pin 7 como referencia de tierra."),
                dict(text="Con el multímetro en modo tensión DC, medir cada entrada: un '0' real "
                          "debe estar por debajo de 0.8 V y un '1' por encima de 2.0 V."),
                dict(text="Medir la salida en cada combinación de entrada: menos de 0.4 V indica "
                          "'0' y más de 2.7 V indica '1'."),
                dict(text="Usar la punta lógica para verificar varias señales a la vez: LED rojo = "
                          "nivel bajo, verde = nivel alto, ámbar = pulso."),
                dict(text="Con el osciloscopio medir los tiempos de propagación y observar los "
                          "flancos reales, especialmente si el circuito trabaja con reloj."),
                dict(text="Anotar todas las mediciones en una tabla y compararlas con la hoja de "
                          "datos: cualquier discrepancia mayor revela un problema físico.")],
         warn="Si la salida permanece en un valor intermedio (entre 0.8 V y 2.0 V), el circuito "
              "está mal: puede haber un cortocircuito entre salidas, una carga excesiva o el chip "
              "dañado. Apagar y revisar antes de continuar.",
         notes="Relacionar cada medición con VIL/VIH/VOL/VOH."),

    dict(kind="gallery", section=5, transition="fade",
         title="Uso de la punta lógica y el osciloscopio",
         lead="Instrumentos que muestran el comportamiento dinámico del circuito.",
         cols=1, accent="orange",
         photos=[(p("probe"), "Punta lógica: tres LEDs indican nivel alto, bajo o tren de pulsos. "
                              "Es el instrumento más rápido para recorrer un circuito cableado.")],
         items=["**Punta lógica:** sonda con LED rojo (nivel bajo), verde (nivel alto) y ámbar "
                "(pulsos). Detecta también circuitos abiertos.",
                "**Multímetro:** mide tensiones DC exactas; imprescindible para verificar niveles "
                "en lugar de confiar en el brillo de un LED.",
                "**Osciloscopio:** muestra la forma de onda, mide retardos y revela glitches que "
                "ningún LED puede mostrar.",
                "**Frecuencímetro:** comprueba la frecuencia real de salida de osciladores y "
                "contadores.",
                "**Analizador lógico:** registra varias líneas a la vez y permite ver la "
                "secuencia completa de un bus.",
                "**Consejo de medición:** usar siempre la punta de tierra corta; cables largos de "
                "tierra introducen ruido y falsas lecturas.",
                "**Seguridad de la sonda:** no tocar con la punta dos pines simultáneamente "
                "(puede provocar cortocircuito)."],
         note="Secuencia de diagnóstico recomendada: primero la punta lógica para ubicar el "
              "bloque muerto, después el multímetro para medir tensiones y por último el "
              "osciloscopio si el problema es de tiempos.",
         notes="Mostrar los instrumentos reales si están disponibles."),

    dict(kind="table", section=5, transition="wipe",
         title="Diagnóstico de fallas: síntoma, causa y solución",
         lead="Tabla de consulta rápida para resolver los problemas más comunes del laboratorio.",
         header=["Síntoma observado", "Causa probable", "Verificación", "Solución"],
         widths=[0.24, 0.26, 0.24, 0.26], accent="red", size=10.2, row_h=0.60,
         rows=[["La salida nunca cambia de estado",
                "Falta alimentación, GND desconectado o pin invertido",
                "Medir VCC entre el pin 14 y el pin 7",
                "Reconectar alimentación y verificar orientación del chip"],
               ["Siempre hay '0' en la salida esperada",
                "Cortocircuito de la salida a GND o carga excesiva (fan-out excedido)",
                "Medir la salida con el circuito sin carga",
                "Retirar la carga, repartir en dos salidas o añadir un buffer"],
               ["Siempre hay '1' en la salida esperada",
                "Entrada flotante o salida al aire",
                "Medir cada entrada con el multímetro",
                "Fijar las entradas con puente a VCC/GND o resistencia de 1 kΩ"],
               ["Funciona a veces y a veces no",
                "Cable flojo, falso contacto en el protoboard o rebote del interruptor",
                "Mover ligeramente cada cable y observar el LED",
                "Reasentar cables, usar otro tramo del protoboard, implementar antirrebote"],
               ["El chip se calienta",
                "Alimentación invertida, cortocircuito interno o sobrecarga",
                "Apagar de inmediato y medir continuidad entre pines",
                "Sustituir el chip y revisar el cableado antes de volver a energizar"],
               ["El LED brilla muy poco o ilegible",
                "Resistencia demasiado alta o corriente insuficiente (IOH bajo)",
                "Medir la corriente y calcular R = (VCC − VF)/IF",
                "Usar 330 Ω o un driver con transistor para cargas mayores"],
               ["El contador salta números",
                "Rebote en la señal de reloj o ruido en la entrada",
                "Observar la señal de reloj en el osciloscopio",
                "Añadir 74LS14 (Schmitt), filtro RC o desacople de 100 nF"],
               ["El circuito funciona pero se detiene solo",
                "Fuente insuficiente, rizado o sobrecalentamiento",
                "Medir VCC con el osciloscopio en modo AC",
                "Cambiar de fuente, añadir capacitores de mayor valor"]],
         note="Método sistemático: dividir el circuito en bloques, verificar cada bloque aislado "
              "con la tabla de verdad, y solo después buscar fallas de integración entre bloques.",
         note_label="MÉTODO DE TRABAJO", notes="Puede entregarse como guía impresa de laboratorio."),

    dict(kind="quiz", section=5, transition="fade",
         title="Reto rápido: identifica la falla",
         lead="Aplica lo aprendido antes de leer la respuesta.",
         accent="pink",
         question="Un alumno monta un 74LS00 y observa que la salida del pin 3 permanece en 0.2 V "
                  "sin importar el estado de las entradas 1 y 2. El chip está bien alimentado y "
                  "no se calienta. ¿Cuál es la causa más probable?",
         options=[dict(key="A", text="El chip está invertido y el pin 3 no es una salida"),
                   dict(key="B", text="El LED de la salida no tiene resistencia limitadora"),
                   dict(key="C", text="El LED está conectado con lógica de sumidero a VCC"),
                   dict(key="D", text="La fuente entrega 5.5 V en lugar de 5 V")],
         answer="Respuesta correcta: C. En TTL el LED debe conectarse entre VCC y la salida "
                "(lógica de sumidero). Si se conecta entre la salida y GND, el pin debe ENTREGAR "
                "corriente, algo que un TTL hace muy mal: la salida se queda cerca de 0.4 V y "
                "nunca alcanza el nivel alto. Explicación complementaria: la opción A es "
                "incorrecta porque el 7400 tiene salidas en los pines 3, 6, 8 y 11; la B y la D "
                "afectan al LED y a los márgenes, pero no explican un nivel permanentemente bajo.",
         notes="Usar esta diapositiva para discutir la lógica de sumidero."),

    dict(kind="quiz", section=5, transition="fade",
         title="Reto rápido: tabla de verdad y equivalencias",
         lead="Segunda pregunta de verificación.",
         accent="green",
         question="¿Cuál es la salida del circuito formado por una compuerta AND (7408) cuyas "
                  "entradas A y B están conectadas a las salidas de dos inversores que reciben, a "
                  "su vez, las señales A y B originales?",
         options=[dict(key="A", text="Y = A · B (coincide con el AND original)"),
                   dict(key="B", text="Y = (A · B)' (se comporta como un NAND)"),
                   dict(key="C", text="Y = A' · B' (un NOR lógico con entradas invertidas)"),
                   dict(key="D", text="Y = A ⊕ B (una XOR)")],
         answer="Respuesta correcta: C. Al invertir ambas entradas antes del AND se obtiene Y = "
                "A'·B', que por el teorema de De Morgan es igual a (A + B)'. Es decir, el "
                "conjunto se comporta como una compuerta NOR. Consecuencia práctica: cualquier "
                "función se puede construir con chips de AND y NOT, y este ejercicio muestra cómo "
                "cambiar la función sin cambiar de chip.",
         notes="Este ejercicio enlaza el bloque de compuertas con el de álgebra de Boole."),

    dict(kind="quiz", section=5, transition="fade",
         title="Reto rápido: hoja de datos",
         lead="Tercera pregunta de verificación.",
         accent="purple",
         question="En la hoja de datos del 74LS00 se lee IOL(máx) = 8 mA e IIL(máx) = 0.4 mA por "
                  "entrada. ¿Cuántas entradas de la misma familia puede gobernar una salida sin "
                  "exceder las especificaciones?",
         options=[dict(key="A", text="8 entradas, porque IOL es de 8 mA"),
                   dict(key="B", text="20 entradas, porque cada entrada consume 0.4 mA"),
                   dict(key="C", text="10 entradas, por el fan-out estándar TTL"),
                   dict(key="D", text="4 entradas, porque IOL se reparte entre dos compuertas")],
         answer="Respuesta correcta: B por cálculo directo (8 mA ÷ 0.4 mA = 20) y C por la "
                "definición clásica del fan-out TTL (10 cargas). El fan-out garantizado de 10 "
                "incluye un margen de seguridad del 100 %: la hoja de datos fija 10 porque además "
                "hay que respetar el límite en nivel alto (IOH = 0.4 mA ÷ 20 µA = 20 entradas) y "
                "los retardos por capacidad de carga. Moraleja: el cálculo eléctrico da 20, pero "
                "el límite de diseño recomendado es 10.",
         notes="Explicar la diferencia entre límite eléctrico y límite de diseño."),

    dict(kind="bullets", section=5, transition="wipe",
         title="Buenas prácticas y reglas de oro del laboratorio",
         lead="Hábitos que evitan perder componentes, tiempo y calificaciones.",
         two_col=True, per=3, size=11.8, gap=0.09,
         items=["**Antes de energizar:** verificar con el multímetro que VCC y GND no están en "
                "corto y que cada chip está bien orientado.",
                "**Un color por función:** rojo para VCC, negro para GND, amarillo para reloj y "
                "colores libres para señales; documentar la convención.",
                "**Cables cortos:** recorridos largos captan ruido y se desconectan con "
                "facilidad.",
                "**Nunca dejar entradas al aire:** en CMOS provocan oscilación y consumo, en TTL "
                "el estado es indefinido en la práctica si hay ruido.",
                "**Un bloque a la vez:** cablear, probar y solo entonces continuar con el "
                "siguiente bloque del diseño.",
                "**Cuidar los chips:** no insertarlos invertidos, usar extractor y aplicar la "
                "pulsera antiestática.",
                "**Etiquetar los cables:** una cinta o una etiqueta en la señal de reloj y en las "
                "salidas ahorra horas de diagnóstico.",
                "**No exceder el fan-out:** repartir la carga y usar buffers cuando se manejan "
                "LEDs, displays o relés.",
                "**Documentar de inmediato:** anotar los valores medidos en el momento, no al "
                "final de la sesión.",
                "**Mantener el orden:** mesa limpia, componentes en su caja y herramientas en su "
                "lugar; el desorden se traduce en errores humanos."],
         note="Regla del laboratorio: si el circuito no funciona, primero se verifica la "
              "alimentación, después el reloj y por último la lógica. En ese orden se localiza más "
              "del 90 % de las fallas.",
         note_label="REGLA PRÁCTICA", notes="Puede convertirse en rúbrica de evaluación de práctica."),

    dict(kind="twocol", section=5, transition="wipe",
         title="Simulación antes del montaje físico",
         lead="Verificar en software cuesta minutos; depurar en hardware cuesta horas.",
         accent="cyan",
         left=dict(title="Herramientas recomendadas", accent="cyan", items=[
             "**Logisim / Logisim Evolution (gratuito):** ideal para compuertas, sumadores, "
             "multiplexores y máquinas de estado; incluye diagramas de tiempo.",
             "**Tinkercad Circuits (navegador):** permite simular Arduino y circuitos "
             "básicos con aspecto realista del protoboard.",
             "**Proteus / Multisim:** simuladores profesionales con bibliotecas completas de "
             "la Serie 74XX y análisis de tiempos.",
             "**LTspice / Falstad (en línea):** análisis de señales y simulación rápida de "
             "compuertas.",
             "**KiCad:** diseño de esquemático y PCB para llevar el circuito a placa "
             "definitiva."]),
         right=dict(title="Qué conviene simular", accent="green", items=[
             "**Tabla de verdad completa:** aplicar todas las combinaciones y comparar con lo "
             "esperado antes de cablear.",
             "**Retardos y glitches:** verificar que los pulsos no se pierdan por tiempos de "
             "propagación.",
             "**Contadores y máquinas de estados:** comprobar la secuencia completa y el retorno "
             "al estado inicial.",
             "**Carga y fan-out teórico:** estimar cuántas entradas cuelgan de cada salida.",
             "**Consumo estimado:** sumar corrientes para dimensionar la fuente del montaje."]),
         note="La simulación no reemplaza la medición real: no modela bien el ruido, las "
              "capacidades parásitas del protoboard, los rebotes mecánicos ni las tolerancias de "
              "los componentes. Pero evita los errores de diseño, que son los más costosos.",
         notes="Mostrar un esquema simulado si hay equipo disponible."),
]
