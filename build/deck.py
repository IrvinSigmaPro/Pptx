# -*- coding: utf-8 -*-
"""Arquetipos de diapositiva: cada uno devuelve (elementos, grupos de animación)."""
import os
from theme import COL, SLIDE_W, SLIDE_H, MARGIN, GEN, SRC, FOOTER_Y
import layouts as L
from layouts import (frame, card, bullet_list, note_bar, chips_row, table_block, kpi_row,
                     photo_grid, timeline, two_col, code_line, measure_box)

W_FULL = SLIDE_W - 2 * MARGIN
X0 = MARGIN
Y0 = 1.50
BOT = 6.78


# ------------------------------------------------------------------ utilidades
class Groups:
    """Acumula grupos de animación por rol."""

    def __init__(self):
        self.groups = []
        self.base = []

    def head(self, els, effect="fade"):
        self.base = list(els)

    def play(self, els, effect="fade", delay=110, trigger="click", wait=300, per=1):
        if not els:
            return
        chunks = [els[i:i + per] for i in range(0, len(els), per)]
        for i, ch in enumerate(chunks):
            self.groups.append({"items": ch, "effect": effect, "delay": delay,
                                "trigger": trigger, "wait": wait, "first": not self.base and i == 0})

    def result(self):
        out = []
        if self.base:
            out.append({"items": self.base, "effect": "fade", "delay": 0, "trigger": "auto", "first": True})
        out += self.groups
        return out


MAX_STEPS = 7          # pasos de clic por diapositiva (evita presentaciones interminables)


def clean(groups, max_steps=MAX_STEPS):
    """Convierte grupos con elementos en grupos con ids y fusiona pasos sobrantes."""
    out = []
    for g in groups:
        ids = []
        for e in g["items"]:
            if isinstance(e, dict) and "id" in e:
                ids.append(e["id"])
            elif isinstance(e, list):
                for x in e:
                    if isinstance(x, dict) and "id" in x:
                        ids.append(x["id"])
        if ids:
            out.append({"ids": ids, "effect": g.get("effect", "fade"), "delay": g.get("delay", 110),
                        "trigger": g.get("trigger", "click"), "wait": g.get("wait", 300)})
    # fusiona los últimos grupos hasta respetar el máximo de pasos
    while len(out) > max_steps:
        last = out.pop()
        prev = out[-1]
        prev = {"ids": prev["ids"] + last["ids"], "effect": prev["effect"],
                "delay": min(prev["delay"], last["delay"]),
                "trigger": prev["trigger"], "wait": prev["wait"]}
        out[-1] = prev
    return out


# ============================================================ tipos de lámina
def slide_hero(c, meta, idx, total, p):
    g = Groups()
    img = p.get("img")
    c.rect(0, 0, SLIDE_W, SLIDE_H, fill="bg", kind="bg")
    if img:
        c.image(img, 6.30, 0, SLIDE_W - 6.30, SLIDE_H, mode="cover")
        c.rect(6.30, 0, SLIDE_W - 6.30, SLIDE_H, fill="bg", alpha=0.30, kind="deco")
        c.rect(6.30, 0, 0.60, SLIDE_H, fill="bg", alpha=0.86, kind="deco")
    c.blob(2.4, 5.9, 3.0, meta["accent"], alpha=0.14)
    c.rect(0, 0, SLIDE_W, 0.07, fill=meta["accent"], kind="deco")
    head = [c.text(X0, 0.85, 6.0, 0.3, p["kicker"], size=11, color=meta["accent"], bold=True,
                   font="mono", spacing=1.0)]
    head.append(c.text(X0, 1.28, 6.2, 2.1, p["title"], size=44, color="txt", bold=True, spacing=0.90))
    head.append(c.text(X0, 3.62, 5.9, 1.0, p["subtitle"], size=14.5, color="txt2", spacing=1.12))
    head.append(c.rect(X0, 4.72, 1.5, 0.05, fill=meta["accent"], kind="deco"))
    head.append(c.text(X0, 4.92, 5.9, 0.9, p["body"], size=11.5, color="txt3", spacing=1.14))
    g.head(head)
    kp = kpi_row(c, X0, 5.75, 6.1, p["stats"], accent=meta["accent"], h=1.0, size=9.5)
    g.play(kp, effect="rise", per=4)
    c.line(X0, FOOTER_Y, SLIDE_W - MARGIN, FOOTER_Y, color="line", lw=0.75)
    c.text(X0, FOOTER_Y + 0.07, 8.0, 0.24, p.get("foot", "Electrónica Digital · Guía técnica de la Serie 74XX"),
           size=8.5, color="txt3", spacing=1.0)
    c.text(SLIDE_W - MARGIN - 2.0, FOOTER_Y + 0.07, 2.0, 0.24, "%02d / %d" % (idx, total),
           size=8.5, color="txt3", font="mono", align="r", spacing=1.0)
    return clean(g.result())


def slide_section(c, meta, idx, total, p):
    g = Groups()
    head, foot, _ = frame(c, meta, idx, total)
    g.head(head)
    acc = meta["accent"]
    c.rect(0, 1.30, SLIDE_W, SLIDE_H - 1.30, fill="bg2", alpha=0.6, kind="deco")
    big = [c.text(X0, 1.75, 4.6, 1.9, meta["num"], size=88, color=acc, bold=True, font="mono", spacing=0.9)]
    big.append(c.text(X0, 3.62, 6.4, 1.0, meta["name"], size=30, color="txt", bold=True, spacing=0.95))
    big.append(c.rect(X0, 4.78, 1.8, 0.05, fill=acc, kind="deco"))
    g.play(big, effect="rise", trigger="auto")
    if p.get("img"):
        g.play([c.image(p["img"], 8.35, 1.75, 4.45, 4.45, mode="contain")], effect="zoom")
    items = bullet_list(c, X0, 5.05, 7.4, 1.6, p["topics"], size=11.5, accent=acc, gap=0.06, spacing=1.05)
    g.play(items, effect="rise", per=2)
    return clean(g.result())


def slide_toc(c, meta, idx, total, p):
    g = Groups()
    head, foot, _ = frame(c, meta, idx, total, title=p["title"], lead=p.get("lead"))
    g.head(head)
    items = p["items"]
    cols, gap = 3, 0.20
    cw = (W_FULL - gap * (cols - 1)) / cols
    ch = 1.62
    els = []
    for i, (num, name, desc, rng) in enumerate(items):
        r, cc = divmod(i, cols)
        x = X0 + cc * (cw + gap)
        y = Y0 + 0.10 + r * (ch + 0.22)
        els.append(c.rect(x, y, cw, ch, fill="card", line="line", lw=0.75, radius=0.10, kind="card"))
        els.append(c.rect(x, y, 0.05, ch, fill=meta["accent"], kind="deco"))
        els.append(c.text(x + 0.22, y + 0.16, 1.0, 0.34, num, size=22, color=meta["accent"],
                          bold=True, font="mono", spacing=0.95))
        els.append(c.text(x + 0.95, y + 0.20, cw - 1.15, 0.5, name, size=13.5, color="txt",
                          bold=True, spacing=1.0))
        els.append(c.text(x + 0.22, y + 0.78, cw - 0.44, 0.6, desc, size=10.5, color="txt2", spacing=1.08))
        els.append(c.text(x + 0.22, y + ch - 0.32, cw - 0.44, 0.24, rng, size=9, color="txt3",
                          font="mono", spacing=1.0))
    g.play(els, effect="rise", per=len(els) // 6 + 1, wait=260)
    return clean(g.result())


def slide_cards(c, meta, idx, total, p):
    """Rejilla de tarjetas (2, 3, 4 o 6 por fila)."""
    g = Groups()
    head, foot, _ = frame(c, meta, idx, total, title=p["title"], lead=p.get("lead"), kicker=p.get("kicker"))
    g.head(head)
    items = p["cards"]
    cols = p.get("cols", 2 if len(items) <= 4 else 3)
    rows = (len(items) + cols - 1) // cols
    gap = p.get("gap", 0.22)
    note_h = 0.95 if p.get("note") else 0.0
    avail = BOT - Y0 - (note_h + 0.16 if note_h else 0.0)
    cw = (W_FULL - gap * (cols - 1)) / cols
    ch = (avail - gap * (rows - 1)) / rows
    els = []
    for i, cd in enumerate(items):
        r, cc = divmod(i, cols)
        x = X0 + cc * (cw + gap)
        y = Y0 + r * (ch + gap)
        col = cd.get("accent", meta["accent"])
        if cd.get("wide"):
            x, cw2 = X0, W_FULL
        else:
            cw2 = cw
        e = card(c, x, y, cw2, ch, cd["title"], cd["body"], accent=col, num=cd.get("num"),
                 icon=cd.get("icon"), size=cd.get("size", 11.5), title_size=cd.get("title_size", 13.5))
        el = e[0]
        els.append(e)
        if cd.get("list"):
            els.append(bullet_list(c, x + 0.22, y + 1.00, cw2 - 0.44, ch - 1.1, cd["list"],
                                   size=10.5, accent=col, gap=0.05, spacing=1.05))
    per = p.get("per", 1)
    g.play(els, effect=p.get("effect", "rise"), per=per, wait=p.get("wait", 220))
    if p.get("note"):
        nb = note_bar(c, X0, BOT - note_h, W_FULL, note_h, p["note"], accent=meta["accent"],
                      label=p.get("note_label", "NOTA TÉCNICA"), size=10.5)
        g.play(nb, effect="fade")
    return clean(g.result())


def slide_bullets(c, meta, idx, total, p):
    g = Groups()
    head, foot, _ = frame(c, meta, idx, total, title=p["title"], lead=p.get("lead"), kicker=p.get("kicker"))
    g.head(head)
    acc = p.get("accent", meta["accent"])
    img = p.get("img")
    sidebar = p.get("sidebar")
    width = W_FULL if not (img or sidebar) else (W_FULL - 5.9 - 0.3 if img else W_FULL - 4.4 - 0.3)
    if p.get("two_col"):
        half = (W_FULL - 0.34) / 2.0
        n = (len(p["items"]) + 1) // 2
        left = bullet_list(c, X0, Y0, half, BOT - Y0, p["items"][:n], size=p.get("size", 12.2),
                           accent=acc, gap=p.get("gap", 0.11), spacing=p.get("spacing", 1.12))
        right = bullet_list(c, X0 + half + 0.34, Y0, half, BOT - Y0, p["items"][n:],
                            size=p.get("size", 12.2), accent=acc, gap=p.get("gap", 0.11),
                            spacing=p.get("spacing", 1.12))
        g.play(left + right, effect="rise", per=p.get("per", 2), wait=240)
    else:
        items = bullet_list(c, X0, Y0, width, BOT - Y0, p["items"], size=p.get("size", 12.5),
                            accent=acc, gap=p.get("gap", 0.12), spacing=p.get("spacing", 1.14))
        g.play(items, effect="rise", per=p.get("per", 2), wait=240)
    if img:
        ix = X0 + width + 0.30
        g.play([c.rect(ix - 0.06, Y0 - 0.06, 5.9 + 0.12, BOT - Y0 + 0.12, fill="card", line="line",
                       lw=0.75, radius=0.10, kind="card"),
                c.image(img, ix, Y0, 5.78, BOT - Y0 - (0.56 if p.get("caption") else 0.0),
                        mode=p.get("img_mode", "cover"), radius=0.08),
                c.text(ix, BOT - 0.50, 5.78, 0.46, p.get("caption", ""), size=9,
                       color="txt3", spacing=1.02)],
               effect="fade")
    if sidebar:
        sx = X0 + width + 0.30
        panels = []
        for i, sd in enumerate(sidebar):
            ph = (BOT - Y0 - 0.20 * (len(sidebar) - 1)) / len(sidebar)
            py = Y0 + i * (ph + 0.20)
            panels += card(c, sx, py, 4.35, ph, sd["title"], sd["body"],
                           accent=sd.get("accent", acc), size=sd.get("size", 11))
        g.play(panels, effect="rise", per=6, wait=220)
    if p.get("note"):
        nb = note_bar(c, X0, BOT - 0.92, W_FULL, 0.92, p["note"], accent=acc,
                      label=p.get("note_label", "NOTA"), size=10.5)
        g.play(nb)
    return clean(g.result())


def slide_table(c, meta, idx, total, p):
    g = Groups()
    head, foot, _ = frame(c, meta, idx, total, title=p["title"], lead=p.get("lead"), kicker=p.get("kicker"))
    g.head(head)
    acc = p.get("accent", meta["accent"])
    rows = p["rows"]
    n = len(rows)
    note_h = 0.9 if p.get("note") else 0.0
    avail = BOT - Y0 - (note_h + 0.16 if note_h else 0.0) - 0.42
    head_h = 0.36
    row_h = min(p.get("row_h", 0.34), (avail) / max(1, n))
    size = p.get("size", 11.5)
    blocks = table_block(c, X0, Y0, W_FULL, p["header"], rows, widths=p.get("widths"),
                         size=size, accent=acc, row_h=row_h, head_h=head_h, align=p.get("align"))
    # sub-encabezados: filas que empiezan con "##"
    for i, b in enumerate(blocks):
        g.play(b, effect="wipe" if i == 0 else "fade", per=1, wait=110 if i else 0,
               trigger="auto" if i == 0 else "click")
    if p.get("note"):
        nb = note_bar(c, X0, BOT - note_h, W_FULL, note_h, p["note"], accent=acc,
                      label=p.get("note_label", "LECTURA DE LA TABLA"), size=10.5)
        g.play(nb)
    return clean(g.result())


def slide_gate(c, meta, idx, total, p):
    """Lámina principal de una compuerta: símbolo, expresión, tabla de verdad y tiempos."""
    g = Groups()
    acc = p.get("accent", meta["accent"])
    head, foot, _ = frame(c, meta, idx, total, title=p["title"], lead=p.get("lead"),
                          kicker=p.get("kicker"))
    g.head(head)
    # ---- columna izquierda: símbolo, chip, expresión
    sym_h = 2.30
    sym_w = sym_h * (2.05 / 1.30)
    els = [c.rect(X0, Y0, 6.05, 3.00, fill="card", line="line", lw=0.75, radius=0.10, kind="card")]
    els.append(c.image(p["symbol"], X0 + 0.14, Y0 + 0.18, sym_w, sym_h, mode="contain"))
    els.append(c.text(X0 + 3.78, Y0 + 0.18, 2.14, 0.28, p["chip"], size=10, color=acc, bold=True,
                      font="mono", spacing=1.0))
    els.append(c.text(X0 + 3.78, Y0 + 0.50, 2.14, 0.30, p["chip_name"], size=11, color="txt", bold=True))
    els += bullet_list(c, X0 + 3.78, Y0 + 0.90, 2.14, 1.96, p["chip_facts"], size=9.2, accent=acc,
                       gap=0.03, spacing=1.02)
    els.append(c.rect(X0, Y0 + 3.14, 6.05, 0.66, fill="bg2", line=acc, lw=1.0, radius=0.08, kind="expr"))
    els.append(c.text(X0 + 0.20, Y0 + 3.14, 5.65, 0.66, p["expr"], size=15.5, color=acc, bold=True,
                      font="mono", align="c", anchor="m", spacing=1.0))
    g.play(els, effect="rise", per=2, wait=140)
    # ---- columna derecha: tabla de verdad
    rh, hh = 0.285, 0.32
    th = 0.46 + hh + len(p["truth"]) * rh
    tb = [c.rect(6.85, Y0, 5.97, th + 0.14, fill="card", line="line", lw=0.75, radius=0.10, kind="card"),
          c.text(7.03, Y0 + 0.12, 5.6, 0.26, p["truth_title"], size=10.5, color=acc, bold=True,
                 font="mono", spacing=1.0)]
    blocks = table_block(c, 7.03, Y0 + 0.46, 5.61, p["truth_header"], p["truth"],
                         widths=p.get("truth_widths"), size=10.5, accent=acc, row_h=rh, head_h=hh)
    tb.append(blocks[0])
    g.play(tb, effect="fade")
    g.play(blocks[1:], effect="fade", per=2, wait=120)
    # ---- columna derecha: tiempos o espacio de verificación
    ytimes = Y0 + th + 0.36
    htimes = 5.30 - ytimes
    if p.get("times") and htimes > 1.1:
        els2 = [c.rect(6.85, ytimes, 5.97, htimes, fill="card", line="line", lw=0.75, radius=0.10,
                       kind="card"),
                c.image(p["times"], 6.97, ytimes + 0.10, 5.73, htimes - 0.20, mode="contain")]
        g.play(els2, effect="fade")
    else:
        info = [c.rect(6.85, ytimes, 5.97, max(1.2, htimes), fill="card", line="line", lw=0.75,
                       radius=0.10, kind="card")]
        info.append(c.text(7.05, ytimes + 0.14, 5.55, 0.26, "CÓMO VERIFICARLO EN EL LABORATORIO",
                           size=10, color=acc, bold=True, font="mono", spacing=1.0))
        info += bullet_list(c, 7.05, ytimes + 0.48, 5.55, max(0.9, htimes - 0.60),
                            p.get("verify", ["Aplicar cada combinación de entrada de la tabla de "
                                             "verdad y medir la salida con la punta lógica.",
                                             "Comprobar VCC = 5 V en el pin 14 y GND en el pin 7 "
                                             "antes de interpretar cualquier resultado.",
                                             "Registrar las mediciones en el reporte de práctica."]),
                            size=9.6, accent=acc, gap=0.06, spacing=1.06)
        g.play(info, effect="fade")
    # ---- franja inferior: funcionamiento y aplicaciones
    yb = 5.55
    half = (W_FULL - 0.24) / 2.0
    cards = []
    cards += card(c, X0, yb, half, 1.22, "Funcionamiento", p["how"], accent=acc, size=10.5, title_size=12)
    cards += card(c, X0 + half + 0.24, yb, half, 1.22, "Aplicaciones típicas", p["apps"], accent=acc,
                  size=10.5, title_size=12)
    g.play(cards, effect="rise", per=8, wait=200)
    return clean(g.result())


def slide_pinout(c, meta, idx, total, p):
    """Lámina de chip: pinout, descripción de pines y notas de hoja de datos."""
    g = Groups()
    acc = p.get("accent", meta["accent"])
    head, foot, _ = frame(c, meta, idx, total, title=p["title"], lead=p.get("lead"), kicker=p.get("kicker"))
    g.head(head)
    g.play([c.rect(X0, Y0, 6.1, 4.42, fill="card", line="line", lw=0.75, radius=0.10, kind="card"),
            c.image(p["pinout"], X0 + 0.32, Y0 + 0.20, 5.46, 4.02, mode="contain")], effect="zoom")
    right = []
    right += card(c, 6.85, Y0, 5.97, 1.38, p["facts_title"], p["facts"], accent=acc, size=10.2,
                  title_size=11.5)
    right += card(c, 6.85, Y0 + 1.52, 5.97, 1.38, p["pins_title"], p["pins"], accent=acc, size=10.2,
                  title_size=11.5)
    right += card(c, 6.85, Y0 + 3.04, 5.97, 1.38, p["data_title"], p["data"], accent=acc, size=10.2,
                  title_size=11.5)
    g.play(right, effect="rise", per=4, wait=220)
    if p.get("note"):
        nb = note_bar(c, X0, 6.15, W_FULL, 0.62, p["note"], accent=acc, label=p.get("note_label", "HOJA DE DATOS"), size=10)
        g.play(nb)
    return clean(g.result())


def slide_gallery(c, meta, idx, total, p):
    g = Groups()
    head, foot, _ = frame(c, meta, idx, total, title=p["title"], lead=p.get("lead"), kicker=p.get("kicker"))
    g.head(head)
    acc = p.get("accent", meta["accent"])
    n = len(p["photos"])
    cols = p.get("cols", 2)
    grid_w = W_FULL if not p.get("items") else W_FULL - 4.6
    rows = (n + cols - 1) // cols
    grid_h = BOT - Y0 - (0.9 if p.get("note") else 0.0)
    els = photo_grid(c, X0, Y0, grid_w, grid_h, p["photos"], cols=p.get("cols"), gap=0.18,
                     caption_h=0.46, size=9.2)
    g.play(els, effect="fade", per=3, wait=200)
    if p.get("items"):
        sx = X0 + grid_w + 0.28
        bl = bullet_list(c, sx, Y0, 4.3, grid_h, p["items"], size=10.5, accent=acc, gap=0.08,
                         spacing=1.08)
        g.play(bl, effect="rise", per=2, wait=200)
    if p.get("note"):
        nb = note_bar(c, X0, BOT - 0.9, W_FULL, 0.9, p["note"], accent=acc,
                      label=p.get("note_label", "OBSERVACIÓN"), size=10.5)
        g.play(nb)
    return clean(g.result())


def slide_timeline(c, meta, idx, total, p):
    g = Groups()
    head, foot, _ = frame(c, meta, idx, total, title=p["title"], lead=p.get("lead"), kicker=p.get("kicker"))
    g.head(head)
    acc = p.get("accent", meta["accent"])
    steps = p["steps"]
    col_w = 7.5 if p.get("img") or p.get("sidebar") else W_FULL
    step_h = min(0.78, (BOT - Y0) / max(1, len(steps)))
    els = timeline(c, X0, Y0, col_w, steps, accent=acc, step_h=step_h,
                   label_size=p.get("label_size", 9.5), body_size=p.get("body_size", 11))
    g.play(els, effect="rise", per=2, wait=170)
    if p.get("img"):
        g.play([c.rect(8.5, Y0, 4.32, BOT - Y0 - 0.5, fill="card", line="line", lw=0.75, radius=0.10,
                       kind="card"),
                c.image(p["img"], 8.62, Y0 + 0.12, 4.08, BOT - Y0 - 0.74, mode="contain")],
               effect="fade")
    if p.get("sidebar"):
        panels = []
        xs = 8.5
        for i, sd in enumerate(p["sidebar"]):
            ph = (BOT - Y0 - 0.2 * (len(p["sidebar"]) - 1)) / len(p["sidebar"])
            panels += card(c, xs, Y0 + i * (ph + 0.2), 4.32, ph, sd["title"], sd["body"],
                           accent=sd.get("accent", acc), size=10.5)
        g.play(panels, effect="rise", per=5, wait=200)
    return clean(g.result())


def slide_twocol(c, meta, idx, total, p):
    g = Groups()
    head, foot, _ = frame(c, meta, idx, total, title=p["title"], lead=p.get("lead"), kicker=p.get("kicker"))
    g.head(head)
    acc = p.get("accent", meta["accent"])
    note_h = 0.9 if p.get("note") else 0.0
    els = two_col(c, X0, Y0, W_FULL, BOT - Y0 - (note_h + 0.2 if note_h else 0.0),
                  (p["left"]["title"], p["left"]["items"]),
                  (p["right"]["title"], p["right"]["items"]),
                  accent_l=p["left"].get("accent", acc), accent_r=p["right"].get("accent", "orange"))
    g.play(els[:3], effect="rise", per=3)
    g.play(els[3:len(els) // 2], effect="rise", per=3, wait=200)
    g.play(els[len(els) // 2:], effect="rise", per=3, wait=200)
    if p.get("note"):
        nb = note_bar(c, X0, BOT - note_h, W_FULL, note_h, p["note"], accent=acc,
                      label=p.get("note_label", "CONCLUSIÓN"), size=10.5)
        g.play(nb)
    return clean(g.result())


def slide_kpis(c, meta, idx, total, p):
    g = Groups()
    head, foot, _ = frame(c, meta, idx, total, title=p["title"], lead=p.get("lead"), kicker=p.get("kicker"))
    g.head(head)
    acc = p.get("accent", meta["accent"])
    kp = kpi_row(c, X0, Y0, W_FULL, p["stats"], accent=acc, h=1.15, size=10.5)
    g.play(kp, effect="rise", per=2)
    y = Y0 + 1.32
    if p.get("cards"):
        cards = []
        cols = 3 if len(p["cards"]) == 3 else 2
        cw = (W_FULL - 0.22 * (cols - 1)) / cols
        for i, cd in enumerate(p["cards"]):
            r, cc = divmod(i, cols)
            ph = 1.62
            cards += card(c, X0 + cc * (cw + 0.22), y + r * (ph + 0.20), cw, ph, cd["title"],
                          cd["body"], accent=cd.get("accent", acc), size=10.5)
        g.play(cards, effect="rise", per=5, wait=220)
    if p.get("items"):
        items = bullet_list(c, X0, y, W_FULL, BOT - y, p["items"], size=12, accent=acc, gap=0.10)
        g.play(items, effect="rise", per=2, wait=220)
    return clean(g.result())


def slide_grid(c, meta, idx, total, p):
    """Rejilla compacta (p. ej. catálogo de chips): nombre mono + descripción + clave."""
    g = Groups()
    head, foot, _ = frame(c, meta, idx, total, title=p["title"], lead=p.get("lead"), kicker=p.get("kicker"))
    g.head(head)
    acc = p.get("accent", meta["accent"])
    items = p["items"]
    cols = p.get("cols", 3)
    rows = (len(items) + cols - 1) // cols
    note_h = 0.9 if p.get("note") else 0.0
    avail = BOT - Y0 - (note_h + 0.16 if note_h else 0.0)
    gap = 0.16
    cw = (W_FULL - gap * (cols - 1)) / cols
    ch = (avail - gap * (rows - 1)) / rows
    els = []
    for i, it in enumerate(items):
        r, cc = divmod(i, cols)
        x = X0 + cc * (cw + gap)
        y = Y0 + r * (ch + gap)
        col = it.get("accent", acc)
        els.append(c.rect(x, y, cw, ch, fill="card", line="line", lw=0.75, radius=0.10, kind="card"))
        els.append(c.rect(x, y, 0.045, ch, fill=col, kind="deco"))
        els.append(c.text(x + 0.18, y + 0.10, cw - 0.36, 0.26, it["name"], size=12, color=col,
                          bold=True, font="mono", spacing=1.0))
        els.append(c.text(x + 0.18, y + 0.38, cw - 0.36, ch - 0.74, it["desc"], size=10,
                          color="txt2", spacing=1.06))
        if it.get("tag"):
            els.append(c.text(x + 0.18, y + ch - 0.30, cw - 0.36, 0.22, it["tag"], size=8.5,
                              color=col, font="mono", spacing=1.0))
    g.play(els, effect="rise", per=max(2, len(els) // 8), wait=200)
    if p.get("note"):
        nb = note_bar(c, X0, BOT - note_h, W_FULL, note_h, p["note"], accent=acc,
                      label=p.get("note_label", "CÓMO ELEGIR"), size=10.5)
        g.play(nb)
    return clean(g.result())


def slide_quiz(c, meta, idx, total, p):
    g = Groups()
    head, foot, _ = frame(c, meta, idx, total, title=p["title"], lead=p.get("lead"), kicker=p.get("kicker"))
    g.head(head)
    acc = p.get("accent", meta["accent"])
    q = [c.rect(X0, Y0, W_FULL, 1.05, fill="panel", line=acc, lw=1.0, radius=0.10, kind="card"),
         c.text(X0 + 0.24, Y0 + 0.14, W_FULL - 0.48, 0.78, p["question"], size=14.5, color="txt",
                bold=True, spacing=1.05)]
    g.play(q, effect="rise")
    opts = p["options"]
    cw = (W_FULL - 0.22) / 2.0
    ch = 0.86
    els = []
    for i, o in enumerate(opts):
        r, cc = divmod(i, 2)
        x = X0 + cc * (cw + 0.22)
        y = Y0 + 1.25 + r * (ch + 0.16)
        els.append(c.rect(x, y, cw, ch, fill="card", line="line", lw=0.75, radius=0.08, kind="card"))
        els.append(c.circle(x + 0.34, y + ch / 2, 0.17, fill=acc, alpha=0.9))
        els.append(c.text(x + 0.34 - 0.17, y + ch / 2 - 0.14, 0.34, 0.28, o["key"], size=12,
                          color="bg", bold=True, font="mono", align="c", anchor="m", spacing=1.0))
        els.append(c.text(x + 0.62, y + 0.10, cw - 0.80, ch - 0.20, o["text"], size=11.5,
                          color="txt2", spacing=1.08, anchor="m"))
    g.play(els, effect="fade", per=2, wait=200)
    if p.get("answer"):
        nb = note_bar(c, X0, Y0 + 3.42, W_FULL, BOT - (Y0 + 3.42), p["answer"], accent=acc,
                      label=p.get("note_label", "RESPUESTA Y EXPLICACIÓN"), size=10.5)
        g.play(nb)
    return clean(g.result())


def slide_glossary(c, meta, idx, total, p):
    g = Groups()
    head, foot, _ = frame(c, meta, idx, total, title=p["title"], lead=p.get("lead"), kicker=p.get("kicker"))
    g.head(head)
    acc = p.get("accent", meta["accent"])
    terms = p["terms"]
    cols = p.get("cols", 3)
    rows = (len(terms) + cols - 1) // cols
    gap = 0.18
    cw = (W_FULL - gap * (cols - 1)) / cols
    ch = (BOT - Y0 - gap * (rows - 1)) / rows
    els = []
    for i, (t, d) in enumerate(terms):
        r, cc = divmod(i, cols)
        x = X0 + cc * (cw + gap)
        y = Y0 + r * (ch + gap)
        els.append(c.rect(x, y, cw, ch, fill="card", line="line", lw=0.75, radius=0.08, kind="card"))
        els.append(c.text(x + 0.16, y + 0.10, cw - 0.32, 0.26, t, size=11, color=acc, bold=True,
                          spacing=1.0))
        els.append(c.text(x + 0.16, y + 0.36, cw - 0.32, ch - 0.44, d, size=9.2, color="txt2",
                          spacing=1.06))
    g.play(els, effect="fade", per=max(2, len(els) // 6), wait=170)
    if p.get("note"):
        nb = note_bar(c, X0, BOT - 0.86, W_FULL, 0.86, p["note"], accent=acc, label="RECORDATORIO",
                      size=10.5)
        g.play(nb)
    return clean(g.result())


def slide_steps(c, meta, idx, total, p):
    """Procedimiento numerado (laboratorio) con diagrama opcional."""
    g = Groups()
    head, foot, _ = frame(c, meta, idx, total, title=p["title"], lead=p.get("lead"), kicker=p.get("kicker"))
    g.head(head)
    acc = p.get("accent", meta["accent"])
    steps = p["steps"]
    has_img = bool(p.get("img"))
    col_w = (W_FULL - 5.0 - 0.3) if has_img else (W_FULL - 0.3) / 2.0
    cols = 1 if has_img else 2
    n = (len(steps) + cols - 1) // cols
    els = []
    for i, s in enumerate(steps):
        cc, r = divmod(i, n)
        x = X0 + cc * (col_w + 0.3)
        y = Y0 + r * ((BOT - Y0) / n)
        h = (BOT - Y0) / n - 0.08
        col = s.get("accent", acc)
        els.append(c.rect(x, y, col_w, h, fill="card", line="line", lw=0.75, radius=0.08, kind="card"))
        els.append(c.circle(x + 0.30, y + h / 2, 0.155, fill=col, alpha=0.9))
        els.append(c.text(x + 0.30 - 0.155, y + h / 2 - 0.125, 0.31, 0.25, str(i + 1), size=10,
                          color="bg", bold=True, font="mono", align="c", anchor="m", spacing=1.0))
        els.append(c.text(x + 0.56, y + 0.06, col_w - 0.70, h - 0.12, s["text"], size=10.5,
                          color="txt2", spacing=1.06, anchor="m"))
    g.play(els, effect="rise", per=3, wait=200)
    if has_img:
        ix = X0 + col_w + 0.30
        avail_h = BOT - Y0 - (1.02 if p.get("warn") else 0.10)
        try:
            from PIL import Image as _I
            iw, ih = _I.open(p["img"]).size
            ar = iw / float(ih)
        except Exception:
            ar = 1.6
        card_h = min(avail_h, 4.46 / ar + 0.30)
        top = Y0 + (avail_h - card_h) / 2.0
        g.play([c.rect(ix, top, 4.7, card_h, fill="card", line="line", lw=0.75, radius=0.10,
                       kind="card"),
                c.image(p["img"], ix + 0.12, top + 0.12, 4.46, card_h - 0.24, mode="contain")],
               effect="fade")
    if p.get("warn"):
        nb = note_bar(c, X0, BOT - 0.86, W_FULL, 0.86, p["warn"], accent="red",
                      label=p.get("warn_label", "PRECAUCIÓN"), size=10.5)
        g.play(nb)
    return clean(g.result())


def slide_contact(c, meta, idx, total, p):
    g = Groups()
    c.rect(0, 0, SLIDE_W, SLIDE_H, fill="bg", kind="bg")
    if p.get("img"):
        c.image(p["img"], 0, 0, SLIDE_W, SLIDE_H, mode="cover")
        c.rect(0, 0, SLIDE_W, SLIDE_H, fill="bg", alpha=0.70, kind="deco")
    c.blob(6.6, 3.9, 3.4, meta["accent"], alpha=0.16)
    c.rect(0, 0, SLIDE_W, 0.07, fill=meta["accent"], kind="deco")
    els = [c.text(X0, 1.75, W_FULL, 0.9, p["title"], size=44, color="txt", bold=True,
                  align="c", spacing=0.95),
           c.text(X0, 2.85, W_FULL, 0.5, p["subtitle"], size=16, color=meta["accent"], bold=True,
                  align="c", spacing=1.05),
           c.rect(SLIDE_W / 2 - 0.9, 3.52, 1.8, 0.05, fill=meta["accent"], kind="deco"),
           c.text(X0 + 2.0, 3.75, W_FULL - 4.0, 1.0, p["body"], size=12.5, color="txt2",
                  align="c", spacing=1.2)]
    g.play(els, effect="rise", per=1, wait=260)
    g.play(chips_row(c, X0, 5.20, W_FULL, p.get("chips", []), accent=meta["accent"],
                     size=10, h=0.38), effect="rise", per=3, wait=200)
    c.line(X0, FOOTER_Y, SLIDE_W - MARGIN, FOOTER_Y, color="line", lw=0.75)
    c.text(X0, FOOTER_Y + 0.07, 8.0, 0.24, p.get("foot", "Electrónica Digital · Guía técnica de la Serie 74XX"),
           size=8.5, color="txt3", spacing=1.0)
    c.text(SLIDE_W - MARGIN - 2.0, FOOTER_Y + 0.07, 2.0, 0.24, "%02d / %d" % (idx, total),
           size=8.5, color="txt3", font="mono", align="r", spacing=1.0)
    return clean(g.result())


RENDERERS = {
    "hero": slide_hero,
    "section": slide_section,
    "toc": slide_toc,
    "cards": slide_cards,
    "bullets": slide_bullets,
    "table": slide_table,
    "gate": slide_gate,
    "pinout": slide_pinout,
    "gallery": slide_gallery,
    "timeline": slide_timeline,
    "twocol": slide_twocol,
    "kpis": slide_kpis,
    "grid": slide_grid,
    "quiz": slide_quiz,
    "glossary": slide_glossary,
    "steps": slide_steps,
    "contact": slide_contact,
}


def render(c, meta, idx, total, spec):
    fn = RENDERERS[spec["kind"]]
    return fn(c, meta, idx, total, spec)
