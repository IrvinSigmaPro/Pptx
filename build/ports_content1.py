# -*- coding: utf-8 -*-
"""Puertos de Comunicación de PC — Bloque 1: portada, índice y puertos de datos."""
import os
import theme

PHOTOS = os.path.join(theme.ASSETS, "ports_photos")


def P(name):
    if name.endswith(".png"):
        name = name[:-4]
    return os.path.join(theme.GEN, name + ".png")


def F(name):
    return os.path.join(PHOTOS, name)


DECK_FOOT = "Puertos de Comunicación de PC · Guía Completa y Detallada"


def ficha(section, title, lead, diagram, ident, vel, uso, note, notes, transition="wipe",
          accent=None):
    """Lámina tipo ficha: diagrama del conector + 3 tarjetas + nota de datos."""
    spec = dict(kind="pinout", section=section, transition=transition,
                title=title, lead=lead, pinout=P(diagram),
                facts_title="IDENTIFICACIÓN VISUAL Y COLOR", facts=ident,
                pins_title="VELOCIDAD Y ESTÁNDARES", pins=vel,
                data_title="USO Y DATOS ADICIONALES", data=uso,
                note=note, note_label="FICHA TÉCNICA", notes=notes)
    if accent:
        spec["accent"] = accent
    return spec


SLIDES = [
    # ------------------------------------------------------------------ 1
    dict(kind="hero", section=1, transition="fade",
         img=F("hero_ports.jpg"),
         kicker="GUÍA COMPLETA Y DETALLADA · HARDWARE · IDENTIFICACIÓN Y ESPECIFICACIONES",
         title="Puertos de Comunicación de PC",
         subtitle="Guía completa y detallada de todas las interfaces de una computadora: forma, "
                  "color de identificación, velocidades, versiones y usos reales.",
         body="Recorrido por los 23 puertos clásicos y modernos —USB, RS-232, LPT, Thunderbolt, "
              "FireWire, PS/2, DIN, Game Port, VGA, DVI, HDMI, DisplayPort, S-Video, compuesto, "
              "RJ-45, RJ-11, SFP, audio 3.5 mm, TOSLINK, S/PDIF, eSATA, tarjetas SD e IrDA— "
              "con diagramas de identificación, códigos de colores y datos técnicos completos.",
         stats=[("23", "puertos documentados a detalle"),
                ("7", "bloques temáticos"),
                ("25+", "diagramas de identificación"),
                ("100+", "datos técnicos verificables")],
         foot=DECK_FOOT + " · 2026",
         notes="Presentación de apertura. Explicar el objetivo: identificar cualquier puerto por su "
               "forma y color, y conocer su velocidad, versiones y usos. Cada lámina tiene "
               "transiciones y animaciones de entrada."),

    # ------------------------------------------------------------------ 2
    dict(kind="toc", section=1, transition="fade",
         title="Contenido de la guía",
         lead="Siete bloques temáticos, de los puertos de datos generales a las interfaces inalámbricas.",
         items=[("01", "Puertos de uso general y datos",
                 "USB, RS-232, LPT, Thunderbolt y FireWire: transmisión de datos, alimentación y video.",
                 "Diapositivas 3 – 14"),
                ("02", "Entrada de periféricos",
                 "PS/2, conector DIN de 5 pines y Game Port: teclados, ratones, joysticks y MIDI.",
                 "Diapositivas 15 – 18"),
                ("03", "Puertos de video y pantalla",
                 "VGA, DVI, HDMI, DisplayPort, S-Video y video compuesto: del CRT al 8K.",
                 "Diapositivas 19 – 29"),
                ("04", "Red y comunicaciones",
                 "Ethernet RJ-45, módem RJ-11 y bahías SFP/QSFP: LAN, fibra óptica y telefonía.",
                 "Diapositivas 30 – 36"),
                ("05", "Puertos de audio",
                 "Jack 3.5 mm con código de colores, S/PDIF óptico TOSLINK y S/PDIF coaxial.",
                 "Diapositivas 37 – 42"),
                ("06", "Almacenamiento y expansión",
                 "eSATA/eSATAp y lectores de tarjetas SD/microSD con velocidades UHS y SD Express.",
                 "Diapositivas 43 – 47"),
                ("07", "Infrarrojos y repaso final",
                 "Puerto IrDA, tablas maestras, chuleta de colores, línea de tiempo y glosario.",
                 "Diapositivas 48 – 56")],
         notes="Usar esta lámina como mapa de navegación. Los bloques 1 y 3 son los más extensos."),

    # ------------------------------------------------------------------ 3
    dict(kind="section", section=1, transition="zoom",
         img=F("sec_datos.jpg"),
         topics=[
             "USB: el estándar universal de datos, alimentación y video",
             "Puerto serie RS-232 (DE-9) para industria, consolas y equipos médicos",
             "Puerto paralelo LPT (DB-25) de la era de las impresoras matriciales",
             "Thunderbolt: PCI Express y DisplayPort en un solo cable",
             "FireWire (IEEE 1394): el bus isócrono de Apple para vídeo"],
         notes="Apertura del bloque 1. Los cinco puertos que definieron la conectividad de datos "
               "desde los años 80 hasta hoy."),

    # ------------------------------------------------------------------ 4
    dict(kind="bullets", section=1, transition="wipe",
         title="USB (Universal Serial Bus)",
         lead="Interfaz estándar universal para transmisión de datos, alimentación y video.",
         img=F("p_usb.jpg"),
         caption="Puertos USB-A (azul = USB 3.0) y USB-C en el panel trasero de una placa madre actual.",
         img_mode="cover",
         size=11.2, per=2,
         items=[
             "Sustituyó en un solo estándar al **puerto serie, al paralelo, al PS/2 y a los "
             "conectores propietarios** de los periféricos: teclados, ratones, memorias, discos "
             "externos, impresoras, cámaras y accesorios diversos.",
             "Es **hot-plug** (conexión en caliente) e **interoperable**: el mismo cable sirve "
             "para alimentar, transferir datos y, con modos alternativos, transportar video.",
             "Define también el **suministro de energía**: de 2.5 W (USB 2.0) hasta **240 W con "
             "USB Power Delivery 3.1**, lo que hoy carga incluso portátiles.",
             "La identificación de versión se hace por el **color del interior del conector** y por "
             "los logotipos grabados (⚡ rayo, SS, tridente USB).",
             "Familia física de conectores: **Type-A, Type-B, Mini-B, Micro-B y Type-C** "
             "(reversible de 24 pines).",
             "Presentado en **1996** (USB 1.0, 1.5 Mbps); hoy **USB4** alcanza hasta 120 Gbps en "
             "modo asimétrico."],
         note="Dato faltante: el conector USB-C no distingue versión por color — consulta los "
              "logotipos ⚡ (Thunderbolt) o SS (SuperSpeed) grabados junto al puerto.",
         notes="Empezar por el puerto más común. Preguntar al grupo quién sabe qué significa el "
               "interior azul de un USB."),

    # ------------------------------------------------------------------ 5
    dict(kind="bullets", section=1, transition="wipe",
         title="USB · Colores de identificación",
         lead="El color de la lengüeta interior del conector indica, por convención, la versión.",
         img=P("usb_colors.png"),
         caption="Código de colores del interior de los conectores USB-A y forma del USB-C.",
         img_mode="contain",
         size=11.5, per=2,
         items=[
             "**Blanco o gris** — USB 1.0 / 1.1 (hasta 12 Mbps): los primeros periféricos, "
             "teclados y ratones.",
             "**Negro** — USB 2.0 (hasta 480 Mbps): el color más extendido en memorias y "
             "periféricos básicos.",
             "**Azul** (o logotipo **SS**) — USB 3.0 / 3.1 Gen 1 (5 Gbps): discos duros externos "
             "y memorias rápidas.",
             "**Rojo o turquesa (teal)** — USB 3.1 Gen 2 / 3.2 Gen 2 (10 Gbps): típico de placas "
             "gaming y estaciones de trabajo.",
             "**USB Tipo C** — ovalado, simétrico y **reversible**; a menudo con icono de **rayo** "
             "(Thunderbolt) o **DP** (DisplayPort Alt Mode) al lado.",
             "Algunos fabricantes usan colores propios (naranja para carga, verde para teclados "
             "de consola): el color es convención, no norma."],
         notes="Recordar que el color identifica la versión en conectores Type-A; en USB-C hay que "
               "leer la serigrafía o la documentación del equipo."),

    # ------------------------------------------------------------------ 6
    dict(kind="bullets", section=1, transition="wipe",
         title="USB · Familia de conectores",
         lead="Cinco formas físicas que cubren desde equipos fijos hasta dispositivos móviles.",
         img=P("usb_types.png"),
         caption="Type-A, Type-B, Mini-B, Micro-B y Type-C: geometrías no intercambiables.",
         img_mode="contain",
         size=11.5, per=2,
         items=[
             "**Type-A** — el conector plano rectangular del PC: teclados, ratones, memorias y "
             "hubs. Interior con 4 contactos (2.0) o 9 (3.x).",
             "**Type-B** — cuadrado con chaflán superior: impresoras, escáneres, discos externos "
             "y tarjetas de audio.",
             "**Mini-B** — versión reducida de 5 pines: cámaras fotográficas, GPS y discos "
             "portátiles de la década de 2000.",
             "**Micro-B** — fino, con rebeles: teléfonos y tablets (USB 2.0 o 3.0); el conector "
             "más frágil de la familia.",
             "**Type-C** — óvalo de **24 pines reversible** que sustituye a todos los anteriores: "
             "datos, video (DP/HDMI), audio y hasta 240 W de alimentación.",
             "Compatibilidad: un cable A→C sirve para cualquier dispositivo C, pero la **velocidad "
             "máxima la define la versión** de ambos extremos."],
         notes="Enseñar los conectores físicos si hay oportunidad; la diferencia entre Mini-B y "
               "Micro-B es la más difícil de reconocer a simple vista."),

    # ------------------------------------------------------------------ 7
    dict(kind="table", section=1, transition="wipe",
         title="USB · Versiones y velocidades",
         lead="De 1.5 Mbps en 1996 a 120 Gbps en modo asimétrico con USB4 v2.0.",
         header=["Estándar", "Año", "Velocidad", "Nombre comercial", "Color típico"],
         widths=[2.15, 0.85, 2.05, 3.75, 3.45],
         row_h=0.385, size=11,
         rows=[
             ["USB 1.0", "1996", "1.5 Mbps", "Low Speed", "blanco / gris"],
             ["USB 1.1", "1998", "12 Mbps", "Full Speed", "blanco / gris"],
             ["USB 2.0", "2000", "480 Mbps", "High Speed", "negro"],
             ["USB 3.0 / 3.1 Gen 1", "2008", "5 Gbps", "SuperSpeed (SS)", "azul"],
             ["USB 3.1 Gen 2 / 3.2 Gen 2", "2013", "10 Gbps", "SuperSpeed+ 10 Gbps", "rojo o turquesa"],
             ["USB 3.2 Gen 2x2", "2017", "20 Gbps", "SuperSpeed+ 20 Gbps", "rojo (pocos equipos)"],
             ["USB4", "2019", "40 Gbps", "USB4 Gen 3x2", "interior negro (USB-C)"],
             ["USB4 v2.0", "2022", "80 / 120 Gbps", "asimétrico (120/40)", "USB-C ⚡"]],
         note="Ojo con la nomenclatura: «USB 3.1 Gen 1» es exactamente lo mismo que USB 3.0 "
              "(5 Gbps). Solo cambia el nombre comercial, no la velocidad real.",
         notes="Tabla clave de la sección. Destacar el lío de nombres comerciales de 2013-2017 y "
               "que la velocidad la marca el más lento de los dos extremos."),

    # ------------------------------------------------------------------ 8
    dict(kind="cards", section=1, transition="wipe",
         title="USB · Potencia, longitudes y datos que faltan",
         lead="Lo que no se ve en el conector: energía, distancia máxima y modos de trabajo.",
         cols=3,
         cards=[
             dict(title="Alimentación (Power Delivery)", accent="green",
                  body="USB 2.0: 5 V / 500 mA (2.5 W). USB 3.x: 900 mA (4.5 W). BC 1.2: 1.5 A. "
                       "USB-C PD: 5-48 V hasta **240 W** (EPR) para cargar portátiles."),
             dict(title="Longitud máxima de cable", accent="orange",
                  body="USB 2.0: 5 m. USB 3.x: 2-3 m pasivos. USB4/Thunderbolt: 0.8 m a velocidad "
                       "máxima (2 m limitado). Con repetidores activos u ópticos se superan 30 m."),
             dict(title="Contactos internos", accent="cyan",
                  body="USB 2.0: 4 pines (VBUS, D-, D+, GND). USB 3.x Type-A: 9 pines. "
                       "USB-C: 24 pines con 4 pares diferenciales de datos y reversibilidad física."),
             dict(title="Modos alternativos (Alt Mode)", accent="purple",
                  body="DisplayPort Alt Mode (video hasta 8K), HDMI Alt Mode y tunelizado de "
                       "Thunderbolt 3/4: el mismo USB-C lleva video, datos y energía a la vez."),
             dict(title="Transferencia de almacenamiento", accent="pink",
                  body="BOT (Bulk-Only Transport, clásico) y **UASP** (SCSI sobre USB), que "
                       "aporta ~20-30 % más de velocidad real en discos externos modernos."),
             dict(title="Compatibilidad y etiquetado", accent="blue",
                  body="Todos los USB son retrocompatibles hacia abajo, pero a la velocidad del "
                       "más lento. Los logos certificados (SS, SS 10, ⚡) garantizan el estándar "
                       "del cable.")],
         note="Regla práctica: un cable «cargador» barato de gasolinera puede cargar el teléfono "
              "pero transferir datos a 2.0 o bloquear modos de video — revisar la serigrafía.",
         notes="Completar la ficha del USB con estos datos que suelen faltar en las guías básicas."),

    # ------------------------------------------------------------------ 9
    dict(kind="bullets", section=1, transition="wipe",
         title="Puerto Serie (RS-232 / DB-9)",
         lead="Comunicación asíncrona de transmisión bit a bit, el estándar industrial desde 1969.",
         img=F("p_rs232.jpg"),
         caption="Puerto serie DE-9 (macho) de color turquesa, aún presente en placas industriales.",
         img_mode="cover",
         size=11.5, per=2,
         items=[
             "El estándar **RS-232** define niveles eléctricos, temporización y protocolo para "
             "comunicación **asíncrona** entre DTE (equipo terminal) y DCE (módem).",
             "Conector clásico en forma de **«D» de 9 pines (DE-9 macho)**, llamado "
             "erróneamente «DB-9». En placas antiguas era de color **turquesa / azul verdoso** "
             "o **gris metálico**; en tarjetas modernas aparece como cabecera interna negra.",
             "Velocidad típica hasta **115.2 kbps** en configuraciones estándar (921.6 kbps con "
             "UART avanzados).",
             "Sigue vivo en **consolas de red (Cisco rollover), PLCs industriales, equipos "
             "médicos, balanzas, GPS de precisión y módems antiguos**.",
             "Señal con tensiones de **±3 V a ±15 V** (típico ±12 V): más robusta al ruido que "
             "los 5 V de TTL, con cable de hasta 15 m."],
         notes="Mencionar que los servicios técnicos de red aún piden «cable de consola» RS-232: "
               "es de los pocos puertos que no desaparece."),

    # ------------------------------------------------------------------ 10
    ficha(1, "RS-232 · Pinout y características eléctricas",
          "Nueve líneas con función definida; solo tres son imprescindibles (TXD, RXD, GND).",
          "dsub9",
          ident="Conector **macho** en «D» de 9 pines (DE-9). Color **turquesa / azul verdoso** "
                "o gris metálico en placas antiguas; serigrafía «COM» o «Serial».",
          vel="Hasta **115.2 kbps** habitual (921.6 kbps con UART 16C950). Asíncrono 7N1/8N1. "
              "Niveles RS-232: ±3…±15 V. Cable máx. 15 m.",
          uso="Consolas de red, dispositivos médicos, módems antiguos, PLCs e industria. "
              "Pines clave: 2 RXD, 3 TXD, 5 GND (7 RTS, 8 CTS para flujo).",
          note="Variantes hermanas: RS-422 y RS-485 usan señal diferencial y alcanzan 1.2 km y "
               "10 Mbps, habituales en automatización industrial.",
          notes="Desglosar el significado de DTE/DCE y el cable null modem (cruza TXD↔RXD).",
          transition="fade"),

    # ------------------------------------------------------------------ 11
    ficha(1, "Puerto Paralelo (LPT / DB-25)",
          "Transmisión simultánea de 8 bits a la vez, el reino de las impresoras hasta los 2000.",
          "dsub25",
          ident="Conector **hembra** grande en «D» de 25 pines. Tradicionalmente de tono "
                "**burdeos / rojo oscuro o rosa** en gabinetes AT/ATX (código de color PC99).",
          vel="De **50 KB/s** (modo SPP) hasta más de **2 MB/s** con modos EPP/ECP. Estándar "
              "IEEE 1284. Cable máx. 10-15 m.",
          uso="Impresoras matriciales y de chorro, escáneres antiguos, unidades ZIP, dongles de "
              "licencia y programadores de EPROM. Dirección base 0x378.",
          note="ECP usa DMA y compresión RLE; EPP fue la evolución para discos y escáneres. Ambos "
               "convivieron con los modos clásicos SPP/PS2 en el mismo conector.",
          notes="Comparar la velocidad con USB 2.0 para explicar por qué el paralelo desapareció."),

    # ------------------------------------------------------------------ 12
    ficha(1, "Thunderbolt",
          "Ultra alta velocidad: combina PCI Express, DisplayPort y alimentación en un solo cable.",
          "thunderbolt",
          ident="En versiones recientes comparte el diseño del **USB Tipo C**, distinguiéndose "
                "obligatoriamente por un pequeño **icono de rayo** grabado junto al puerto. "
                "Thunderbolt 1 y 2 usaban Mini DisplayPort, también con rayo.",
          vel="**TB1: 10 Gbps · TB2: 20 Gbps · TB3 y TB4: 40 Gbps · TB5: hasta 80 Gbps** "
              "(120 Gbps en modo asimétrico). Tuneliza PCIe + DP + USB + PD.",
          uso="Tarjetas gráficas externas (eGPU), almacenamiento profesional, docks y monitores "
              "4K/8K. Daisy-chain de hasta 6 dispositivos; hasta 240 W de carga (TB5/PD).",
          note="Cable pasivo: 0.8 m a 40 Gbps (2 m a 20 Gbps). Los cables activos u ópticos "
               "alcanzan 2-60 m manteniendo el ancho de banda completo.",
          notes="Thunderbolt 4 exige 40 Gbps y 2 pantallas 4K; Thunderbolt 5 (2023) duplica el "
                "ancho de banda para pantallas 8K y flujos de trabajo de creación.",
          transition="fade"),

    # ------------------------------------------------------------------ 13
    dict(kind="table", section=1, transition="wipe",
         title="Thunderbolt · Evolución de versiones",
         lead="Cuatro generaciones con el mismo concepto: PCIe y DisplayPort multiplexados.",
         header=["Versión", "Año", "Ancho de banda", "Conector", "Pantallas / capacidades"],
         widths=[1.75, 0.85, 1.95, 2.35, 5.39],
         row_h=0.42, size=10.5,
         rows=[
             ["Thunderbolt 1", "2011", "10 Gbps", "Mini DisplayPort", "1× 2560×1600 · PCIe 2.0 x4"],
             ["Thunderbolt 2", "2013", "20 Gbps", "Mini DisplayPort", "1× 4K · agrega dos enlaces"],
             ["Thunderbolt 3", "2015", "40 Gbps", "USB-C", "2× 4K · eGPU · PD hasta 100 W"],
             ["Thunderbolt 4", "2020", "40 Gbps", "USB-C", "2× 4K o 1× 8K · docks · PD 100 W"],
             ["Thunderbolt 5", "2023", "80 / 120 Gbps", "USB-C", "2× 8K · PCIe 5.0 · PD hasta 240 W"]],
         note="El icono del rayo es obligatorio: muchos puertos USB-C solo son USB (sin PCIe ni "
              "DisplayPort) y se confunden con Thunderbolt por la forma idéntica del conector.",
         notes="Enfatizar que Thunderbolt 4 y USB4 comparten tecnología, pero Thunderbolt exige "
               "certificación Intel/USB-IF con mínimos más estrictos."),

    # ------------------------------------------------------------------ 14
    ficha(1, "FireWire (IEEE 1394)",
          "Bus serie de alta velocidad desarrollado por Apple, pensado para vídeo en tiempo real.",
          "firewire",
          ident="Conector rectangular con un **borde en ángulo o forma de «V»**. Detalles en "
                "**dorado** o marcos metálicos plateados con el **logo de FireWire** (círculo con "
                "tres ramas). 6 pines (Mac) o 4 pines (i.LINK, sin alimentación).",
          vel="**FireWire 400 (400 Mbps)** y **FireWire 800 (800 Mbps)**. Modo isócrono garantiza "
              "ancho de banda para vídeo sin interrupciones. Cable 4.5 m (100 m con fibra).",
          uso="Videocámaras DV, discos duros externos de audio/video, interfaces de audio "
              "profesionales. Hasta 63 dispositivos en cadena, peer-to-peer y hot-swap.",
          note="Apple lo retiró en 2011; su relevo lo tomaron USB 2.0/3.0, eSATA y Thunderbolt. "
               "Los equipos de edición de vídeo de los 2000 lo estandarizaron (i.LINK de Sony).",
          notes="El modo isócrono de FireWire era su gran ventaja sobre USB 2.0 para vídeo; "
                "hoy ese rol lo cumple USB con UVC o Thunderbolt.",
          transition="fade"),
]
