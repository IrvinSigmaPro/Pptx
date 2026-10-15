# -*- coding: utf-8 -*-
"""Puertos de Comunicación de PC — Bloques 4-7 y cierre."""
import os
import theme
from ports_content1 import P, F, ficha

SLIDES = [
    # ================================================================== 30
    dict(kind="section", section=4, transition="zoom",
         img=F("sec_red.jpg"),
         topics=[
             "Ethernet RJ-45: el conector de red alámbrica con LEDs de estado",
             "Velocidades de Fast Ethernet a 10 Gbps y categorías de cable UTP",
             "Módem RJ-11: la línea telefónica analógica y el dial-up",
             "SFP/SFP+: transceptores modulares de fibra óptica para servidores"],
         notes="Las redes definen la conectividad moderna; diferenciar bien RJ-45 y RJ-11."),

    # ================================================================== 31
    ficha(4, "Ethernet / RJ-45",
          "Puerto de red alámbrica para redes locales (LAN), el más presente en oficinas.",
          "rj45",
          ident="Conector rectangular **ligeramente más ancho que un puerto telefónico** "
                "(8P8C: 8 posiciones, 8 contactos dorados), con **pestaña de traba plástica** y "
                "dos LEDs integrados: **verde** (enlace) y **naranja/ámbar** (actividad).",
          vel="**Fast Ethernet 100 Mbps · Gigabit 1 Gbps · 2.5G/5G/10G** (2.5 a 10 Gbps). "
              "4 pares trenzados (UTP) Cat5e/6/6a/8 · 100 m por segmento.",
          uso="Conexión a Internet de alta velocidad mediante cable de red (UTP), switches, "
              "routers, NAS, cámaras IP y PoE para alimentar dispositivos.",
          note="Datos que faltan: PoE (802.3af/at/bt) entrega hasta 60-100 W por el mismo cable. "
               "Los LEDs varían por fabricante (verde=1 Gbps, ámbar=100 Mbps o actividad). "
               "Cableado T568A/T568B.",
          notes="En el laboratorio: comprobar el LED de enlace verde es el primer diagnóstico "
                "de una conexión de red.",
          transition="fade"),

    # ================================================================== 32
    dict(kind="table", section=4, transition="wipe",
         title="Ethernet · Velocidades y categorías de cable",
         lead="La velocidad depende tanto del estándar como de la categoría del cable UTP.",
         header=["Estándar", "Velocidad", "Cable mínimo", "Pares usados", "Distancia máx."],
         widths=[2.35, 1.85, 2.15, 2.15, 3.79],
         row_h=0.395, size=10.5,
         rows=[
             ["10BASE-T", "10 Mbps", "Cat 3", "2 de 4", "100 m"],
             ["100BASE-TX (Fast)", "100 Mbps", "Cat 5e", "2 de 4", "100 m"],
             ["1000BASE-T (Gigabit)", "1 Gbps", "Cat 5e/6", "4 de 4", "100 m"],
             ["2.5GBASE-T / 5GBASE-T", "2.5 / 5 Gbps", "Cat 5e / 6", "4 de 4", "100 m"],
             ["10GBASE-T", "10 Gbps", "Cat 6a (6: 55 m)", "4 de 4", "100 m"],
             ["PoE 802.3af / at / bt", "15.4 / 30 / 60-100 W", "Cat 5e o superior", "pares libres o datos", "100 m"]],
         note="Cat 6a blindado (STP) es obligatorio para 10 Gbps a 100 m en entornos con "
              "interferencias. El conector siempre es RJ-45: cambia el cable interior.",
         notes="Relacionar con los LEDs del puerto: enlace verde fijo = capa física correcta."),

    # ================================================================== 33
    dict(kind="bullets", section=4, transition="wipe",
         title="RJ-45 vs RJ-11 · No confundir",
         lead="La diferencia de tamaño ha provocado miles de conectores rotos.",
         img=P("rj_compare.png"),
         caption="RJ-45 (8P8C, red) frente a RJ-11 (6P2C, teléfono): mismo lenguaje, tamaño distinto.",
         img_mode="contain",
         size=11.5, per=2,
         items=[
             "El **RJ-45** (8P8C) tiene **8 contactos** y una abertura más ancha; el **RJ-11** "
             "(6P2C/6P4C) solo usa **2 o 4 contactos** y es más estrecho.",
             "**Nunca fuerces** un RJ-45 en un RJ-11: aunque el cable entre parcialmente, "
             "los contactos se doblan y el módem puede quedar inservible.",
             "Identificación por etiqueta: los módems marcan los jacks como **«LINE»** (entrada "
             "de la compañía telefónica) y **«PHONE»** (teléfono derivado).",
             "El RJ-45 lleva **cable UTP de 4 pares**; el RJ-11, **par telefónico** de 2 hilos "
             "(24-26 AWG).",
             "Velocidades: hasta **10 Gbps** (RJ-45) frente a **56 kbps** dial-up o 24 Mbps "
             "ADSL2+ (RJ-11 con splitter).",
             "En equipos antiguos los dos puertos se situaban juntos en la tarjeta PCI del módem; "
             "el color transparente/blanco ayudaba a distinguirlos del negro de la red."],
         notes="Demostrar con conectores físicos la diferencia de anchura es la forma más "
               "eficaz de fijarlo."),

    # ================================================================== 34
    ficha(4, "Módem / RJ-11",
          "Puerto para la línea telefónica analógica clásica: la puerta del Internet de los 90.",
          "rj11",
          ident="Conector **idéntico al RJ-45 pero de menor tamaño físico** (6P2C/6P4C). En "
                "tarjetas internas o módems PCI era de color **transparente / blanco** o estaba "
                "rotulado con la palabra **«LINE»**.",
          vel="Hasta **56 kbps** (V.90/V.92, dial-up tradicional). Fax a 14.4-33.6 kbps. "
              "Con ADSL2+ y splitter: hasta 24 Mbps de bajada por el mismo par.",
          uso="Internet telefónico, envío de fax y líneas dedicadas de alarmas, TPV y telemetría. "
              "Tensión de línea: -48 V DC con timbre de ~90 V AC.",
          note="Datos que faltan: 2 hilos (par telefónico). El jack «PHONE» deriva el mismo "
               "conector al teléfono interno. Con fibra FTTH el módem se sustituye por un ONT "
               "con puerto RJ-45.",
          notes="El dial-up ocupaba la línea telefónica: por eso aparecieron los módems de "
                "segunda línea y más tarde ADSL con splitter.",
          transition="fade"),

    # ================================================================== 35
    ficha(4, "SFP / SFP+",
          "Bahía modular para conexiones de fibra óptica o redes de alta densidad.",
          "sfp",
          ident="**Ranura metálica rectangular profunda** (cage) con una pequeña **palanca o "
                "pestillo** (bail latch) de metal o plástico, usualmente **azul, negro o "
                "metálico** según la velocidad. Los módulos llevan conectores LC duplex.",
          vel="**SFP (1 Gbps) · SFP+ (10 Gbps) · SFP28 (25 Gbps) · QSFP+ (40 Gbps)**. "
              "El QSFP28 alcanza 100 Gbps y el QSFP-DD 400 Gbps en switches de alta gama.",
          uso="Servidores de red empresarial y switches de alta gama: fibra monomodo (hasta "
              "80-120 km, cable amarillo) o multimodo (300-550 m, cable aqua OM3/OM4) y DAC "
              "de cobre para 1-7 m.",
          note="Datos que faltan: están estandarizados por el acuerdo MSA (multi-fabricante), son "
               "hot-swap y ofrecen diagnóstico DDM/DOM (potencia óptica, temperatura). "
               "Longitudes de onda típicas: 850 / 1310 / 1550 nm.",
          notes="El color del cable de fibra indica el tipo: amarillo = monomodo, aqua/óptico "
                "túrbido = multimodo.",
          transition="fade"),

    # ================================================================== 36
    dict(kind="table", section=4, transition="wipe",
         title="Familia SFP/QSFP · Transceptores modulares",
         lead="El mismo factor de forma, cuatro velocidades y formatos de unión (aggregation).",
         header=["Formato", "Velocidad", "Uso típico", "Fibra / cobre", "Notas"],
         widths=[1.55, 1.45, 2.75, 2.75, 3.79],
         row_h=0.395, size=10.5,
         rows=[
             ["SFP", "1 Gbps", "access switches, servidores", "LC multimodo/monomodo", "sucesor del GBIC"],
             ["SFP+", "10 Gbps", "datacenters y campus", "LC o DAC SFP+ 10G", "el más extendido"],
             ["SFP28", "25 Gbps", "top-of-rack moderno", "LC OM4 / monomodo", "25G por carril"],
             ["QSFP+", "40 Gbps", "agregación de switches", "MPO/MTP o DAC", "4 carriles de 10 G"],
             ["QSFP28", "100 Gbps", "núcleo de red", "MPO/MTP 24 fibras", "4 carriles de 25 G"],
             ["QSFP-DD", "400 Gbps", "spine de datacenter", "MPO 16 fibras", "doble densidad"]],
         note="Los transceptores son caros y específicos de distancia/longitud de onda: "
              "elegir mal el módulo produce errores CRC o sin enlace. Las tablas de "
              "compatibilidad del fabricante son imprescindibles.",
         notes="Cerrar el bloque de redes con la escala de velocidades del datacenter moderno."),

    # ================================================================== 37
    dict(kind="section", section=5, transition="zoom",
         img=F("sec_audio.jpg"),
         topics=[
             "Jack de 3.5 mm con código de colores para audio estéreo y micrófono",
             "S/PDIF óptico (TOSLINK): audio digital por pulsos de luz",
             "S/PDIF coaxial: audio digital por cable de 75 ohmios"],
         notes="El audio analógico convive con el digital: reconocer los colores es la clave."),

    # ================================================================== 38
    ficha(5, "Jack de Audio de 3.5 mm",
          "Conector analógico estándar para sonido estéreo y micrófonos.",
          "audio_jacks",
          ident="**Orificio circular pequeño** con código de colores PC99: **verde** (salida/"
                "auriculares), **rosado/magenta** (micrófono), **azul claro** (line-in), "
                "**naranja** (central/subwoofer), **negro** (traseros) y **gris** (surround "
                "lateral).",
          vel="Transmisión **analógica en tiempo real**, sin latencia de datos digitales. "
              "Impedancias habituales de 16-600 Ω; nivel de línea ~1 Vrms.",
          uso="Sistemas de sonido, diademas (headsets), micrófonos, altavoces 2.0/5.1/7.1 y "
              "equipos de música portátil. Existente también en 6.35 mm (1/4\") para audio pro.",
          note="Datos que faltan: TRS (3 polos: punta/anillo/camisa) para estéreo y TRRS (4 "
               "polos, con micrófono) en teléfonos; estándares CTIA y OMTP, incompatibles entre "
               "sí sin adaptador. Cable no balanceado 3-10 m.",
          notes="Repasar el código de colores completo — el gris de los laterales es el que "
                "más se olvida.",
          transition="fade"),

    # ================================================================== 39
    dict(kind="table", section=5, transition="wipe",
         title="Código de colores de los jacks de audio",
         lead="Convención PC99 de Intel/Microsoft para las tarjetas de sonido y placas madre.",
         header=["Color", "Función", "Símbolo habitual", "Señal", "Ejemplo de uso"],
         widths=[1.55, 2.75, 2.35, 2.25, 3.39],
         row_h=0.395, size=10.5,
         rows=[
             ["Verde", "salida de línea / altavoces", "altavoz o auricular", "salida estéreo", "auriculares, altavoces 2.0"],
             ["Rosado / magenta", "entrada de micrófono", "micrófono", "entrada mono (-10 dBV)", "diademas, micrófonos PC"],
             ["Azul claro", "entrada de línea", "flecha entrando", "entrada estéreo", "reproductor, mezcladora"],
             ["Naranja", "central y subwoofer", "altavoz + sub", "salida 5.1/7.1", "home cinema PC"],
             ["Negro", "altavoces traseros", "altavoz trasero", "salida surround", "configuración 5.1"],
             ["Gris", "altavoces laterales", "altavoz lateral", "salida surround", "configuración 7.1"]],
         note="En los portátiles el jack único es TRRS (combo) y la tarjeta de sonido conmuta "
              "función según lo que se conecte. En audio profesional (6.35 mm) los colores "
              "desaparecen y se etiqueta por canal.",
         notes="Tabla práctica: recorrerla con la placa madre real de referencia si existe."),

    # ================================================================== 40
    ficha(5, "S/PDIF Óptico (TOSLINK)",
          "Puerto de audio digital mediante pulsos de luz por fibra óptica.",
          "toslink",
          ident="Conector **cuadrado pequeño con esquinas biseladas** y una **tapa protectora "
                "abatible** de plástico negro. Al encender el equipo emite un **brillo de luz "
                "roja** en su interior. Variante mini-óptico de 3.5 mm en equipos compactos.",
          vel="Transmisión digital de audio multicanal **sin pérdida por interferencia "
              "eléctrica**: PCM estéreo hasta 96 kHz y envolvente comprimido (Dolby Digital, "
              "DTS) 5.1/7.1. En audio pro: protocolo ADAT (8 canales a 48 kHz).",
          uso="Barras de sonido, receptores AV y sistemas de cine en casa avanzados; equipos "
              "donde haya bucles de masa o interferencias eléctricas.",
          note="Datos que faltan: fibra óptica plástica de 5-10 m (hasta 30 m de calidad). "
               "Inmune a EMI y a bucles de tierra; algo más de jitter que el coaxial. "
               "Estándar EIAJ CP-3407 (Toshiba, 1983).",
          notes="La luz roja visible es un buen indicador de funcionamiento; si no brilla, "
                "el equipo está apagado o el cable está roto.",
          transition="fade"),

    # ================================================================== 41
    ficha(5, "S/PDIF Coaxial",
          "Interfaz de audio digital mediante cable coaxial de 75 ohmios.",
          "spdif_coax",
          ident="Conector circular tipo **RCA hembra** identificado por un color **naranja "
                "brillante o negro** distintivo en su borde plástico. En equipos profesionales "
                "se usa conector **BNC**.",
          vel="Ancho de banda digital adecuado para audio envolvente comprimido (**Dolby "
              "Digital / DTS**), PCM hasta 24 bit / 192 kHz. Señal de 0.5 Vp-p, 75 Ω.",
          uso="Receptores de audio digital, amplificadores de alta fidelidad, DACs externos y "
              "equipos de sonido doméstico premium.",
          note="Datos que faltan: el cable coaxial de vídeo RCA (75 Ω) vale para este puerto. "
               "Distancia práctica: ~10 m. Misma interfaz S/PDIF que el TOSLINK: solo cambia "
               "el medio (eléctrico frente a óptico).",
          notes="Comparar con el TOSLINK: mismo protocolo, distinta inmunidad al ruido.",
          transition="fade"),

    # ================================================================== 42
    dict(kind="twocol", section=5, transition="wipe",
         title="S/PDIF: TOSLINK vs Coaxial",
         lead="Dos medios, un mismo protocolo digital de audio.",
         left=dict(title="TOSLINK (óptico)", accent="green", items=[
             "Transporta audio por **pulsos de luz** sobre fibra óptica.",
             "**Inmune** a interferencias electromagnéticas y a bucles de tierra.",
             "Conector cuadrado con tapa; luz roja visible (~650 nm).",
             "Alcance típico **5-10 m** (30 m con fibra de calidad).",
             "Ideal si hay zumbido o ruido eléctrico en el sistema."]),
         right=dict(title="S/PDIF coaxial (eléctrico)", accent="orange", items=[
             "Transporta audio por **cable coaxial de 75 Ω** (RCA naranja o negro).",
             "Menor jitter que el óptico; señal de 0.5 Vp-p.",
             "Usa el mismo cable RCA de vídeo si es necesario.",
             "Alcance típico **~10 m** con cable de calidad.",
             "Ideal para equipos cercanos y enlaces simples."]),
         note="Ambos llevan los mismos formatos (PCM, Dolby Digital, DTS): la elección depende "
              "del ruido eléctrico del entorno y de la distancia. Para audio sin pérdida "
              "multicanal moderno (TrueHD, Atmos), HDMI es la vía recomendada.",
         notes="Conclusión práctica: coaxial para calidad eléctrica pura; óptico para aislar "
               "masas y evitar zumbidos."),

    # ================================================================== 43
    dict(kind="section", section=6, transition="zoom",
         img=F("sec_almacen.jpg"),
         topics=[
             "eSATA / eSATAp: discos externos a velocidad nativa SATA",
             "Lectores de tarjetas SD y microSD en el panel frontal",
             "Estándares UHS-I/II/III y SD Express de las tarjetas modernas"],
         notes="Almacenamiento externo: cuando USB no era suficientemente rápido nació eSATA."),

    # ================================================================== 44
    ficha(6, "eSATA / eSATAp",
          "Conexión externa para discos duros basada en el protocolo SATA interno.",
          "esata",
          ident="Conector **plano y alargado** similar al SATA interno pero con **guías de "
                "plástico más robustas y metálicas** en los laterales. Color **negro oscuro** "
                "con la serigrafía **«eSATA»**. La variante eSATAp añade hilos de alimentación.",
          vel="**eSATA 1.5 / 3 / 6 Gbps** (SATA I/II/III): velocidad nativa del bus interno, "
              "sin la sobrecarga del protocolo USB. Cable máximo 2 m.",
          uso="Conexión de discos de almacenamiento externo (HDD/SSD) con rendimiento idéntico "
              "al interno: copias de seguridad, clonación de discos y estaciones de trabajo.",
          note="Datos que faltan: el eSATA **no aporta alimentación** (requiere fuente externa); "
               "eSATAp (power over eSATA) añade 5 V/12 V desde un combo USB. Hot-swap "
               "requiere modo AHCI. Desplazado por USB 3.0 desde 2010.",
          notes="El gran defecto del eSATA era la falta de alimentación; por eso se inventó "
                "eSATAp, el conector combo que se ve en placas de 2008-2012.",
          transition="fade"),

    # ================================================================== 45
    dict(kind="cards", section=6, transition="wipe",
         title="eSATA frente a USB 3.0 · ¿qué conviene?",
         lead="La comparación que decidió el futuro del almacenamiento externo.",
         cols=3,
         cards=[
             dict(title="Velocidad real", accent="blue",
                  body="eSATA 6 Gbps y USB 3.0 5 Gbps son comparables en la práctica; con UASP "
                       "el USB iguala al SATA. El SATA interno SSD supera ambos desde 2011 "
                       "(SATA III queda en ~550 MB/s)."),
             dict(title="Alimentación", accent="green",
                  body="USB alimenta el disco (4.5-100 W con PD); eSATA no, salvo eSATAp. "
                       "Un disco de 3.5\" con eSATA puro necesita fuente externa obligatoria."),
             dict(title="Compatibilidad", accent="orange",
                  body="USB existe en todo; eSATA solo en placas y laptops de 2005-2015. "
                       "Un combo eSATAp acepta tanto USB como eSATA en el mismo hueco."),
             dict(title="Hot-swap", accent="purple",
                  body="Ambos lo soportan; eSATA requiere controlador en modo AHCI y drivers "
                       "del chipset; USB lo trae por diseño desde siempre."),
             dict(title="Uso actual", accent="pink",
                  body="eSATA: equipos legacy y estaciones de trabajo. USB 3.x/4 y "
                       "Thunderbolt dominan el almacenamiento externo moderno."),
             dict(title="Veredicto", accent="cyan",
                  body="Hoy se prefiere USB 3.2/USB4 por versatilidad; eSATA solo tiene sentido "
                       "manteniendo equipos que ya lo incluyen.")],
         notes="Conclusión de bloque: eSATA fue una solución excelente a un problema que USB 3.0 "
               "acabó resolviendo de forma más universal."),

    # ================================================================== 46
    ficha(6, "Lectores de Tarjetas (SD / microSD)",
          "Puertos de lectura directa para tarjetas de memoria flash.",
          "sdcard",
          ident="**Ranuras finas rectangulares** en el panel frontal o lateral del chasis, a "
                "veces marcadas con **iconos impresos de tarjetas SD**. La tarjeta SD lleva "
                "**pestaña de bloqueo (LOCK)** gris en el lateral; la microSD no.",
          vel="Según el estándar de la tarjeta: **UHS-I 104 MB/s · UHS-II 312 MB/s · "
              "UHS-III 624 MB/s · SD Express 985 MB/s** (y más, con PCIe).",
          uso="Transferencia rápida de fotos y archivos desde cámaras, drones, teléfonos y "
              "consolas. Los lectores internos se conectan por USB 2.0/3.0 a la placa.",
          note="Datos que faltan: SD (≤2 GB), SDHC (≤32 GB), SDXC (≤2 TB), SDUC (≤128 TB). "
               "Clases de velocidad V10/V30/V60/V90 (vídeo) y A1/A2 (apps). UHS-II añade una "
               "segunda fila de contactos al dorso.",
          notes="Enseñar la diferencia física: una microSD UHS-II tiene contactos extra y solo "
                "rinde a tope en un lector UHS-II.",
          transition="fade"),

    # ================================================================== 47
    dict(kind="table", section=6, transition="wipe",
         title="Tarjetas SD · Familias, velocidades y clases",
         lead="Qué significa cada sigla impresa en la tarjeta.",
         header=["Estándar", "Capacidad", "Velocidad de bus", "Clase de vídeo", "Uso típico"],
         widths=[1.95, 1.85, 2.55, 2.25, 3.69],
         row_h=0.395, size=10.5,
         rows=[
             ["SD (1997)", "hasta 2 GB", "12.5-25 MB/s", "—", "cámaras antiguas"],
             ["SDHC (2006)", "4-32 GB", "UHS-I 104 MB/s", "V10 / V30", "vídeo Full HD"],
             ["SDXC (2009)", "64 GB-2 TB", "UHS-II 312 MB/s", "V60 / V90", "vídeo 4K"],
             ["SDXC UHS-III", "64 GB-2 TB", "624 MB/s", "V90", "vídeo 4K/8K, ráfagas RAW"],
             ["SD Express", "64 GB-2 TB", "985 MB/s - 4 GB/s", "V90 / WP", "cámaras 8K, laptops"],
             ["SDUC (2018)", "2-128 TB", "SD Express", "V90", "futuro, equipos pro"]],
         note="La letra A (A1/A2) define rendimiento de aplicaciones (IOPS), y la V (V30…) la "
              "velocidad sostenida de escritura de vídeo. Para grabar vídeo 4K, V30 es el mínimo "
              "recomendado real.",
         notes="Las clases se acumulan: una SDXC UHS-II V90 es compatible con lectores UHS-I "
               "(a velocidad UHS-I)."),

    # ================================================================== 48
    dict(kind="section", section=7, transition="zoom",
         img=F("sec_irda.jpg"),
         topics=[
             "IrDA: comunicación inalámbrica direccional por luz infrarroja",
             "Velocidades SIR, FIR y VFIR y su sustitución por Bluetooth",
             "Tablas maestras, chuleta de colores y repaso final de la guía"],
         notes="Último bloque: el único puerto inalámbrico de la guía y el repaso general."),

    # ================================================================== 49
    ficha(7, "IrDA (Infrared Data Association)",
          "Puerto inalámbrico direccional por luz infrarroja, el Bluetooth de los años 90.",
          "irda",
          ident="**Pequeña ventana rectangular u ovalada de plástico translúcido** de color "
                "**rojo oscuro, morado o ahumado oscuro**, situada en el panel frontal de la PC "
                "o en el lateral de la laptop. No tiene pines: es un transceptor óptico.",
          vel="Desde **115.2 kbps (SIR)** hasta **4 Mbps (FIR)** y 16 Mbps (VFIR); negociación "
              "inicial a 9600 bps. Cono de ~30° y alcance de 0-1 m con alineación directa.",
          uso="Sincronización con agendas electrónicas (PDA), teléfonos de la época y equipos "
              "antiguos de los años 90: Palm, Pocket PC, portátiles con IrDA 1.1.",
          note="Datos que faltans: requiere **línea de visión** (se bloquea con el dedo o polvo). "
               "Longitud de onda 850-900 nm. Estándares IrDA-Data, IrDA-Control e IrSimple. "
               "Desplazado por Bluetooth y Wi-Fi Direct desde 2005.",
          notes="Demostrar el funcionamiento: la cámara del teléfono ve la luz infrarroja "
                "parpadeante del mando a distancia aunque el ojo no la perciba.",
          transition="fade"),

    # ================================================================== 50
    dict(kind="table", section=7, transition="wipe",
         title="IrDA · Modos de operación",
         lead="Un mismo puerto, cuatro velocidades y una única limitación física: la línea de visión.",
         header=["Modo", "Velocidad", "Año", "Distancia / ángulo", "Notas"],
         widths=[1.75, 1.75, 1.05, 2.85, 4.89],
         row_h=0.42, size=10.5,
         rows=[
             ["SIR", "9.6 kbps - 115.2 kbps", "1993", "1 m · 30°", "compatible con UART clásico"],
             ["MIR", "1.152 Mbps", "1996", "1 m · 30°", "intermedio, poco usado"],
             ["FIR", "4 Mbps", "1998", "1 m · 30°", "el modo más habitual en PCs"],
             ["VFIR", "16 Mbps", "2001", "1 m · 30°", "muy raro en equipos domésticos"],
             ["GigaIR", "hasta 1 Gbps", "2007+", "0.2 m", "experimental, no desplegado"]],
         note="IrDA gastaba muy poca energía y no requería emparejamiento, pero la necesidad de "
              "apuntar y la poca distancia lo condenaron cuando Bluetooth (1-100 m, "
              "omnidireccional) maduró.",
         notes="Cierre técnico de IrDA: hoy solo aparece en equipos industriales y retro."),

    # ================================================================== 51
    dict(kind="table", section=1, transition="wipe",
         title="Tabla maestra · Velocidades de todos los puertos",
         lead="Una sola vista de las 23 interfaces de esta guía, de menor a mayor velocidad.",
         header=["Puerto", "Velocidad típica / máx.", "Tipo", "Aparición", "Estado hoy"],
         widths=[2.55, 3.05, 1.95, 1.55, 3.19],
         row_h=0.315, size=9.5,
         rows=[
             ["Módem RJ-11", "56 kbps", "serie", "1990s", "legado / ADSL"],
             ["IrDA", "115.2 kbps - 4 Mbps", "inalámbrico IR", "1993", "obsoleto"],
             ["RS-232", "115.2 kbps (921.6 kbps)", "serie", "1969", "industria"],
             ["LPT", "50 KB/s - 2+ MB/s", "paralelo 8 bits", "1970s", "obsoleto"],
             ["Game Port", "muestreo analógico", "analógico", "1980s", "obsoleto"],
             ["FireWire", "400 - 800 Mbps", "serie isócrono", "1995", "obsoleto"],
             ["USB 2.0", "480 Mbps", "serie", "2000", "activo (periféricos)"],
             ["Fast Ethernet", "100 Mbps", "red", "1995", "activo"],
             ["Gigabit Ethernet", "1 Gbps", "red", "1999", "estándar"],
             ["USB 3.2 / USB4", "10 - 40 Gbps", "serie", "2013-2019", "estándar"],
             ["Thunderbolt 3/4/5", "40 - 120 Gbps", "híbrido PCIe+DP", "2015-2023", "gama alta"],
             ["10 GbE / SFP+", "10 Gbps", "red", "2006", "profesional"],
             ["HDMI 2.1", "48 Gbps", "video/audio", "2017", "estándar TV"],
             ["DisplayPort 2.1", "80 Gbps", "video/audio", "2022", "estándar PC"],
             ["eSATA 6 Gbps", "6 Gbps", "almacenamiento", "2004", "legado"]],
         note="Lectura rápida: para datos, USB4/Thunderbolt; para video, DP 2.1 y HDMI 2.1; "
              "para red, 2.5-10 GbE o SFP+; para legacy, RS-232 y RJ-11 siguen presentes.",
         notes="Tabla-resumen de toda la guía; ideal para repaso antes de un examen o "
               "certificación de hardware."),

    # ================================================================== 52
    dict(kind="grid", section=1, transition="wipe",
         title="Chuleta de colores de identificación",
         lead="Lo primero que se mira al conectar un cable: el color.",
         cols=3,
         items=[
             dict(name="USB blanco / gris", desc="USB 1.0-1.1 · 12 Mbps · teclados y ratones antiguos.",
                  tag="LENGÜETA INTERIOR", accent="cyan"),
             dict(name="USB negro", desc="USB 2.0 · 480 Mbps · el color más común de memorias.",
                  tag="LENGÜETA INTERIOR", accent="cyan"),
             dict(name="USB azul", desc="USB 3.0/3.1 Gen 1 · 5 Gbps · con logotipo SS.",
                  tag="LENGÜETA INTERIOR", accent="blue"),
             dict(name="USB rojo / turquesa", desc="USB 3.1 Gen 2/3.2 · 10 Gbps · placas gaming.",
                  tag="LENGÜETA INTERIOR", accent="red"),
             dict(name="PS/2 verde", desc="Ratón — exclusivo, nunca teclado.",
                  tag="MINI-DIN 6", accent="green"),
             dict(name="PS/2 morado", desc="Teclado — exclusivo, nunca ratón.",
                  tag="MINI-DIN 6", accent="purple"),
             dict(name="VGA azul", desc="Monitor analógico · 15 pines en 3 filas.",
                  tag="D-SUB HD15", accent="blue"),
             dict(name="LPT burdeos", desc="Impresora paralela · 25 pines (PC99).",
                  tag="D-SUB 25", accent="pink"),
             dict(name="Game Port dorado", desc="Joystick / MIDI en tarjetas de sonido.",
                  tag="D-SUB 15", accent="orange"),
             dict(name="RCA amarillo", desc="Video compuesto SD · 1 Vp-p 75 Ω.",
                  tag="RCA", accent="orange"),
             dict(name="Audio verde/rosado/azul", desc="Salida / micrófono / line-in (PC99).",
                  tag="JACK 3.5 MM", accent="green"),
             dict(name="RCA naranja", desc="S/PDIF coaxial · audio digital 75 Ω.",
                  tag="RCA", accent="orange"),
             dict(name="LED verde RJ-45", desc="Enlace de red establecido.",
                  tag="ETHERNET", accent="green"),
             dict(name="LED ámbar RJ-45", desc="Actividad de datos (o 100 Mbps).",
                  tag="ETHERNET", accent="orange"),
             dict(name="TOSLINK rojo", desc="Luz visible del audio óptico (~650 nm).",
                  tag="FIBRA ÓPTICA", accent="red"),
             dict(name="Fibra amarilla", desc="Monomodo (larga distancia).",
                  tag="SFP / LC", accent="orange"),
             dict(name="Fibra aqua", desc="Multimodo OM3/OM4 (datacenter).",
                  tag="SFP / LC", accent="teal"),
             dict(name="IrDA rojo oscuro", desc="Ventana infrarroja translúcida.",
                  tag="IRDA", accent="red")],
         note="Atajo mental: azul = rápido (USB 3), verde = ratón/enlace, amarillo = video "
              "compuesto o fibra monomodo, rojo = luz óptica o USB 3.2.",
         notes="Chuleta final para memorizar por asociación de colores."),

    # ================================================================== 53
    dict(kind="cards", section=1, transition="wipe",
         title="No confundir · Pares que se parecen",
         lead="Los errores de identificación más frecuentes en el taller.",
         cols=2,
         cards=[
             dict(title="RJ-45 vs RJ-11", accent="green",
                  body="Mismo lenguaje, distinto tamaño: **8 contactos** (red) frente a "
                       "**2-4 contactos** (teléfono). Forzar uno en el otro dobla los contactos."),
             dict(title="USB-C vs Thunderbolt", accent="purple",
                  body="Conector **idéntico**. Solo el **icono del rayo ⚡** y la documentación "
                       "confirman Thunderbolt; un USB-C normal no mueve eGPU ni 2 pantallas."),
             dict(title="HDMI vs DisplayPort", accent="blue",
                  body="HDMI: **dos esquinas biseladas** abajo, sin pestillo. DP: **una esquina "
                       "biselada** y **pestillo de seguridad** arriba."),
             dict(title="USB-A 2.0 vs 3.0", accent="cyan",
                  body="Misma forma: solo el **color interior** (negro vs azul) y los 5 contactos "
                       "extra del USB 3.0 los delatan. Usar el 3.0 en puerto 2.0 pierde velocidad."),
             dict(title="DVI-I vs DVI-D", accent="orange",
                  body="DVI-I tiene **4 pines analógicos** alrededor de la blade y adapta a VGA "
                       "pasivamente; DVI-D no, y forzarlo daña los contactos."),
             dict(title="Mini-B vs Micro-B", accent="pink",
                  body="Mini-B es más grueso y trapezoidal; Micro-B, fino con rebeles. Son "
                       "físicamente incompatibles aunque ambos sean USB.")],
         note="Regla de oro: si el conector no entra con suavidad, no es el correcto. "
              "La fuerza nunca es parte del estándar.",
         notes="Repaso de los pares de conectores que más errores generan en soporte técnico."),

    # ================================================================== 54
    dict(kind="timeline", section=1, transition="wipe",
         title="Línea de tiempo · Cuatro décadas de conectividad",
         lead="Cómo evolucionaron los puertos desde el teclado DIN hasta USB4 y Thunderbolt 5.",
         body_size=10.2, label_size=9.5,
         steps=[
             ("1984-87", "DIN-5 en los IBM AT y el nacimiento del PS/2 con código de colores "
                         "verde/morado."),
             ("1986-95", "RS-232 y LPT dominan periféricos; llega VGA (1987) y el Game Port "
                         "de las Sound Blaster."),
             ("1995-96", "FireWire (IEEE 1394) y Fast Ethernet 100BASE-TX; se lanza USB 1.0."),
             ("1998-2000", "USB 1.1 y 2.0 unifican periféricos; Gigabit Ethernet; S-Video y "
                           "compuesto en su apogeo TV."),
             ("2002-06", "HDMI (2002), DisplayPort (2006) y eSATA (2004): el video se digitaliza."),
             ("2008-13", "USB 3.0 (5 Gbps), Thunderbolt 1-2, SFP+ 10 GbE y HDMI 2.0 (4K60)."),
             ("2014-17", "USB-C y Thunderbolt 3 se imponen; DP 1.4 y HDMI 2.1 (48 Gbps)."),
             ("2019-23", "USB4 (40 Gbps), DP 2.0/2.1 (80 Gbps), Thunderbolt 5 y SD Express.")],
         sidebar=[dict(title="Constante histórica", accent="cyan",
                       body="Cada generación multiplica por 10 el ancho de banda de la anterior "
                            "pero mantiene compatibilidad hacia atrás con adaptadores."),
                  dict(title="Tendencia actual", accent="green",
                       body="Convergencia en USB-C: datos, video, audio y hasta 240 W en un "
                            "solo conector reversible.")],
         notes="Recorrido cronológico para situar cada puerto en su época."),

    # ================================================================== 55
    dict(kind="glossary", section=1, transition="wipe",
         title="Glosario técnico",
         lead="Los términos esenciales que aparecen en las hojas de datos de estos puertos.",
         cols=3,
         terms=[
             ("Hot-plug", "Conexión y desconexión del periférico con el equipo encendido."),
             ("Half / Full duplex", "Comunicación en un sentido o en ambos a la vez."),
             ("TMDS", "Transmisión diferencial minimizada: capa física de DVI y HDMI."),
             ("Display Stream Compression", "Compresión visual sin pérdida perceptible (DSC)."),
             ("ARC / eARC", "Canal de retorno de audio del TV al receptor por HDMI."),
             ("CEC", "Control remoto único de todos los dispositivos HDMI interconectados."),
             ("HDCP", "Cifrado de contenido protegido en HDMI/DisplayPort."),
             ("Adaptive-Sync", "Sincronización variable de refresco (FreeSync/G-Sync Compatible)."),
             ("MST / SST", "Multi-Stream (cadena de monitores) / Single-Stream en DisplayPort."),
             ("UASP", "Protocolo SCSI sobre USB para discos externos más rápidos."),
             ("USB Power Delivery", "Negociación de hasta 240 W por USB-C (5-48 V)."),
             ("Alt Mode", "Modo alternativo: video o Thunderbolt por el cable USB-C."),
             ("PoE", "Alimentación sobre cable Ethernet (hasta 60-100 W)."),
             ("UTP / STP", "Cable de par trenzado sin/sin blindaje para red."),
             ("T568A / T568B", "Orden de hilos estándar en los conectores RJ-45."),
             ("SFP / QSFP", "Transceptores modulares de fibra óptica (1-400 Gbps)."),
             ("LC / MPO", "Conectores de fibra dúplex pequeños / multifibra de datacenter."),
             ("DDC / EDID", "Identificación del monitor por el cable (plug & play de video)."),
             ("Y/C (S-Video)", "Luminancia y crominancia separadas para mejor imagen."),
             ("TRS / TRRS", "Conector de audio de 3 o 4 polos (con micrófono)."),
             ("CTIA / OMTP", "Estándares de cableado de los jacks TRRS, incompatibles entre sí."),
             ("S/PDIF", "Interfaz de audio digital de Sony/Philips (óptica o coaxial)."),
             ("UHS-I/II/III", "Estándares de bus de tarjetas SD (104-624 MB/s)."),
             ("IrDA SIR/FIR", "Infrarrojo lento (115.2 kbps) y rápido (4 Mbps).")],
         note="Glosario pensado como referencia rápida durante la exposición y el estudio.",
         notes="Invitar a consultar el glosario durante la presentación; no hace falta "
               "memorizarlo."),

    # ================================================================== 56
    dict(kind="contact", section=1, transition="fade",
         img=F("hero_ports.jpg"),
         title="Guía completa y detallada",
         subtitle="Puertos de Comunicación de PC · 23 interfaces · 7 bloques",
         body="Identifica cada puerto por su forma y color, conoce su velocidad real y elige "
              "siempre el cable correcto. Esta guía cubre desde el DIN de 1984 hasta Thunderbolt 5 "
              "y SD Express, con los datos técnicos que suelen faltar: potencia, longitudes, "
              "pinout y versiones.",
         chips=["USB", "RS-232", "LPT", "Thunderbolt", "FireWire", "PS/2", "VGA", "DVI",
                "HDMI", "DisplayPort", "RJ-45", "SFP", "Jack 3.5 mm", "TOSLINK", "eSATA",
                "IrDA"],
         foot="Puertos de Comunicación de PC · Guía Completa y Detallada · 2026",
         notes="Cierre: resumir que la identificación visual (forma + color) resuelve el 90 % de "
               "los casos, y que las versiones determinan la velocidad real."),
]
