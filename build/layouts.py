# -*- coding: utf-8 -*-
"""Composición de diapositivas: marco, decoración y arquetipos de contenido."""
from theme import (COL, SLIDE_W, SLIDE_H, MARGIN, FOOTER_Y, SECTION)

CONTENT_TOP = 1.50
CONTENT_BOT = 6.80

DECK_TITLE = "Compuertas Lógicas y Chips Serie 74XX"


# --------------------------------------------------------------------- helpers
def _wrap_groups(els, per_group, trigger="click", effect="fade", delay=110, first_auto=False):
    """Reparte elementos en grupos de animación."""
    groups = []
    if not els:
        return groups
    chunks = [els[i:i + per_group] for i in range(0, len(els), per_group)]
    for i, ch in enumerate(chunks):
        groups.append({
            "items": ch,
            "trigger": "auto" if (i == 0 and first_auto) else trigger,
            "delay": delay,
            "effect": effect,
            "first": i == 0,
        })
    return groups


def frame(c, meta, idx, total, title=None, lead=None, kicker=None, effect="fade"):
    """Pinta fondo, encabezado, pie y barra de progreso. Devuelve (els, groups)."""
    accent = meta["accent"]
    num = meta["num"]

    # fondo
    c.rect(0, 0, SLIDE_W, SLIDE_H, fill="bg", kind="bg")
    c.blob(SLIDE_W - 1.1, 0.35, 3.0, accent, alpha=0.16)
    c.blob(0.15, SLIDE_H - 0.4, 2.4, accent, alpha=0.07)
    # barra superior de acento
    head = []
    head.append(c.rect(0, 0, SLIDE_W, 0.055, fill=accent, kind="deco"))
    head.append(c.rect(0, 0.055, 2.2, 0.012, fill=accent, kind="deco", alpha=0.35))

    if title:
        # etiqueta de sección
        lab = "%s · %s" % (num, meta["name"].upper())
        head.append(c.rect(MARGIN, 0.30, 0.045, 0.30, fill=accent, kind="deco"))
        head.append(c.text(MARGIN + 0.12, 0.34, 6.6, 0.24, lab, size=9.5, color=accent,
                           bold=True, font="mono", spacing=1.0))
        head.append(c.text(MARGIN, 0.60, SLIDE_W - 2 * MARGIN - 1.0, 0.52, title,
                           size=27, color="txt", bold=True, font="head", spacing=0.95))
        y = 1.12
        if lead:
            head.append(c.text(MARGIN, y, SLIDE_W - 2 * MARGIN - 0.2, 0.30, lead,
                               size=12, color="txt3", spacing=1.05))
        if kicker:
            head.append(c.text(SLIDE_W - MARGIN - 1.2, 0.32, 1.2, 0.28, kicker,
                               size=9.5, color="txt3", font="mono", align="r", spacing=1.0))

    # pie
    foot = []
    foot.append(c.line(MARGIN, FOOTER_Y, SLIDE_W - MARGIN, FOOTER_Y, color="line", lw=0.75))
    foot.append(c.text(MARGIN, FOOTER_Y + 0.07, 7.0, 0.24, DECK_TITLE, size=8.5, color="txt3", spacing=1.0))
    foot.append(c.text(SLIDE_W - MARGIN - 2.0, FOOTER_Y + 0.07, 2.0, 0.24,
                       "%02d / %d" % (idx, total), size=8.5, color="txt3", font="mono",
                       align="r", spacing=1.0))
    bar_w = (SLIDE_W - 2 * MARGIN) * (idx / float(total))
    c.rect(MARGIN, SLIDE_H - 0.10, SLIDE_W - 2 * MARGIN, 0.035, fill="line", alpha=0.55, kind="deco")
    c.rect(MARGIN, SLIDE_H - 0.10, max(0.05, bar_w), 0.035, fill=accent, kind="deco")

    groups = [{"items": head, "trigger": "auto", "delay": 0, "effect": effect, "first": True}]
    return head, foot, groups


def card(c, x, y, w, h, title, body, accent="cyan", icon=None, num=None, size=11.5,
         title_size=13.5, align="l"):
    """Tarjeta con franja de acento, título y cuerpo. Devuelve elementos."""
    els = []
    els.append(c.rect(x, y, w, h, fill="card", line="line", lw=0.75, radius=0.10, kind="card"))
    els.append(c.rect(x, y + 0.12, 0.035, min(0.42, h - 0.24), fill=accent, kind="deco"))
    tx = x + 0.20
    tw = w - 0.40
    ty = y + 0.16
    if num:
        els.append(c.text(x + 0.16, y + 0.13, 0.5, 0.22, num, size=9, color=accent,
                          bold=True, font="mono", spacing=1.0))
    if icon:
        els.append(c.text(x + w - 0.42, y + 0.12, 0.3, 0.24, icon, size=12, color=accent,
                          align="r", spacing=1.0))
    els.append(c.text(tx, ty, tw, 0.30, title, size=title_size, color="txt", bold=True, spacing=0.98))
    els.append(c.text(tx, ty + 0.34, tw, h - 0.55, body, size=size, color="txt2", spacing=1.10))
    return els


def bullet_list(c, x, y, w, body_h, items, size=12.5, accent="cyan", gap=0.10, spacing=1.12,
                bullet=True, color="txt2"):
    """Lista de viñetas; cada elemento es un cuadro independiente (animable)."""
    els = []
    # ajuste automático: si el contenido no cabe, se reduce el tamaño de fuente
    if body_h and body_h > 0.2:
        probe = 0.0
        for it in items:
            txt = it[1] if isinstance(it, tuple) else it
            hh, _ = measure_box(txt, w - 0.30, size, spacing)
            probe += hh + gap
        while probe > body_h - 0.02 and size > 8.4:
            size -= 0.25
            gap = max(0.02, gap - 0.004)
            spacing = max(0.98, spacing - 0.006)
            probe = 0.0
            for it in items:
                txt = it[1] if isinstance(it, tuple) else it
                hh, _ = measure_box(txt, w - 0.30, size, spacing)
                probe += hh + gap
    cy = y
    for it in items:
        lvl = 0
        txt = it
        if isinstance(it, tuple):
            lvl, txt = it
        ix = x + (0.26 if lvl else 0.0)
        iw = w - (0.26 if lvl else 0.0) - 0.05
        h, _ = measure_box(txt, iw, size, spacing)
        if bullet and lvl == 0:
            c.circle(x + 0.075, cy + 0.105, 0.045, fill=accent)
        elif bullet:
            c.rect(x + 0.02, cy + 0.085, 0.075, 0.045, fill=accent, alpha=0.6)
        els.append(c.text(ix + (0.19 if bullet else 0), cy, iw - (0.19 if bullet else 0), h,
                          txt, size=size, color=color, spacing=spacing))
        cy += h + gap
    return els


def measure_box(text, w, size, spacing=1.12):
    from canvas import measure
    return measure(text, w, size, spacing=spacing)


def note_bar(c, x, y, w, h, text, accent="cyan", size=11, label="NOTA TÉCNICA"):
    els = [c.rect(x, y, w, h, fill="panel", line="line", lw=0.75, radius=0.08, kind="note")]
    els.append(c.rect(x, y + 0.10, 0.035, h - 0.20, fill=accent, kind="deco"))
    els.append(c.text(x + 0.18, y + 0.10, 2.2, 0.20, label, size=8.5, color=accent,
                      bold=True, font="mono", spacing=1.0))
    els.append(c.text(x + 0.18, y + 0.30, w - 0.36, h - 0.42, text, size=size, color="txt2", spacing=1.10))
    return els


def chips_row(c, x, y, w, items, accent="cyan", size=9.5, h=0.30):
    """Fila de etiquetas centrada que se ajusta al ancho disponible."""
    if not items:
        return []
    els = []
    gap = 0.10
    factor, pad, s = 0.105, 0.24, size
    for _ in range(40):
        widths = [max(0.52, factor * len(t) + pad) for t in items]
        total = sum(widths) + gap * (len(items) - 1)
        if total <= w:
            break
        factor *= 0.94
        pad = max(0.14, pad * 0.94)
        s = max(7.5, s - 0.15)
    cx = x + max(0.0, (w - total) / 2.0)
    for t, pw in zip(items, widths):
        els.append(c.rect(cx, y, pw, h, fill="panel2", line=accent, lw=0.75, radius=0.14, kind="chip"))
        els.append(c.text(cx, y, pw, h, t, size=s, color=accent, font="mono",
                          align="c", anchor="m", spacing=1.0))
        cx += pw + gap
    return els


def table_block(c, x, y, w, header, rows, widths=None, size=11, accent="cyan", row_h=0.30,
                head_h=0.34, align=None):
    """Tabla con encabezado y franjas. Devuelve lista de filas (cada fila = elementos)."""
    if widths is None:
        widths = [1.0 / len(header)] * len(header)
    cw = [w * f for f in widths]
    out = []
    head = []
    head.append(c.rect(x, y, w, head_h, fill=accent, kind="thead", alpha=0.92))
    cx = x
    for i, htxt in enumerate(header):
        head.append(c.text(cx + 0.08, y, cw[i] - 0.16, head_h, htxt, size=size, color="bg",
                           bold=True, anchor="m", align="l" if (align is None or align[i] == "l") else align[i],
                           spacing=1.0))
        cx += cw[i]
    out.append(head)
    ry = y + head_h
    for r, row in enumerate(rows):
        rw = []
        if r % 2 == 0:
            rw.append(c.rect(x, ry, w, row_h, fill="panel", kind="trow", alpha=0.55))
        cx = x
        for i, cell in enumerate(row):
            col = "txt" if i == 0 else "txt2"
            rw.append(c.text(cx + 0.08, ry, cw[i] - 0.16, row_h, cell, size=size, color=col,
                             anchor="m", font="mono" if (i > 0 and len(cell) < 12 and any(ch.isdigit() for ch in cell)) else "body",
                             align="l" if (align is None or align[i] == "l") else align[i], spacing=1.0))
            cx += cw[i]
        out.append(rw)
        ry += row_h
    c.rect(x, y, w, ry - y, fill=None, line="line", lw=0.75, radius=0.06, kind="tframe")
    return out


def kpi_row(c, x, y, w, stats, accent="cyan", h=1.05, size=11):
    """Fila de indicadores: (valor, etiqueta)."""
    els = []
    n = len(stats)
    gap = 0.16
    cw = (w - gap * (n - 1)) / n
    for i, (val, lab) in enumerate(stats):
        cx = x + i * (cw + gap)
        els.append(c.rect(cx, y, cw, h, fill="card", line="line", lw=0.75, radius=0.08, kind="kpi"))
        els.append(c.text(cx + 0.14, y + 0.12, cw - 0.28, 0.40, val, size=21, color=accent,
                          bold=True, font="mono", spacing=0.95))
        els.append(c.text(cx + 0.14, y + 0.56, cw - 0.28, h - 0.62, lab, size=size,
                          color="txt3", spacing=1.05))
    return els


def photo_grid(c, x, y, w, h, photos, cols=None, gap=0.16, caption_h=0.42, size=9.2):
    """Rejilla de fotografías con pie de foto; elige el número de columnas que mejor aprovecha el área."""
    els = []
    n = len(photos)
    if cols is None:
        try:
            from PIL import Image as _I
            aspects = []
            for ph_ in photos:
                iw, ih = _I.open(ph_[0]).size
                aspects.append(iw / float(ih))
            best, cols_best = -1.0, 1
            for cc in range(1, n + 1):
                rr = (n + cc - 1) // cc
                cwd = (w - gap * (cc - 1)) / cc
                cht = (h - gap * (rr - 1)) / rr - caption_h - 0.10
                if cht <= 0.2:
                    continue
                util = 0.0
                for a in aspects:
                    util += min(a, cwd / cht) / max(a, cwd / cht)
                util /= len(aspects)
                if util > best:
                    best, cols_best = util, cc
            cols = cols_best
        except Exception:
            cols = 2 if n > 1 else 1
    rows = (n + cols - 1) // cols
    cwid = (w - gap * (cols - 1)) / cols
    chgt = (h - gap * (rows - 1)) / rows
    for i, (path, cap) in enumerate(photos):
        r, cc = divmod(i, cols)
        px_ = x + cc * (cwid + gap)
        py = y + r * (chgt + gap)
        els.append(c.rect(px_, py, cwid, chgt, fill="card", line="line", lw=0.75, radius=0.08, kind="pcard"))
        els.append(c.image(path, px_ + 0.07, py + 0.07, cwid - 0.14, chgt - caption_h - 0.10,
                           mode="auto", radius=0.06))
        els.append(c.text(px_ + 0.14, py + chgt - caption_h + 0.02, cwid - 0.28, caption_h - 0.08,
                          cap, size=size, color="txt3", spacing=1.02))
    return els


def timeline(c, x, y, w, steps, accent="cyan", step_h=0.72, label_size=9, body_size=11):
    """Línea de tiempo vertical con nodos numerados."""
    els = []
    c.line(x + 0.155, y + 0.2, x + 0.155, y + step_h * (len(steps) - 1) + 0.2, color="line2", lw=1.25)
    for i, (lab, txt) in enumerate(steps):
        cy = y + i * step_h
        els.append(c.circle(x + 0.155, cy + 0.16, 0.145, fill="card", line=accent, lw=1.25))
        els.append(c.text(x - 0.08, cy + 0.16 - 0.10, 0.47, 0.20, str(i + 1), size=9.5,
                          color=accent, bold=True, font="mono", align="c", spacing=1.0))
        els.append(c.text(x + 0.46, cy - 0.02, 1.9, 0.24, lab, size=label_size, color=accent,
                          bold=True, font="mono", spacing=1.0))
        els.append(c.text(x + 0.46, cy + 0.22, w - 0.56, step_h - 0.28, txt, size=body_size,
                          color="txt2", spacing=1.08))
    return els


def two_col(c, x, y, w, h, left, right, gap=0.24, accent_l="cyan", accent_r="orange"):
    """Dos paneles comparativos: (título, [viñetas])."""
    els = []
    cw = (w - gap) / 2
    for i, (pan, acc) in enumerate(((left, accent_l), (right, accent_r))):
        px_ = x + i * (cw + gap)
        tit, items = pan
        els.append(c.rect(px_, y, cw, h, fill="card", line="line", lw=0.75, radius=0.10, kind="panel"))
        els.append(c.rect(px_, y, cw, 0.44, fill="panel2", radius=0.10, kind="panelhead"))
        els.append(c.text(px_ + 0.18, y, cw - 0.36, 0.44, tit, size=13, color=acc, bold=True,
                          anchor="m", spacing=1.0))
        els += bullet_list(c, px_ + 0.20, y + 0.60, cw - 0.40, h - 0.75, items,
                           size=11.5, accent=acc, gap=0.09)
    return els


def code_line(c, x, y, w, expr, accent="cyan", size=15, h=0.62, sub=None):
    els = [c.rect(x, y, w, h, fill="bg2", line=accent, lw=1.0, radius=0.08, kind="expr")]
    els.append(c.text(x + 0.22, y, w - 0.44, h, expr, size=size, color=accent, bold=True,
                      font="mono", anchor="m", align="c", spacing=1.0))
    if sub:
        els.append(c.text(x + 0.22, y + h + 0.06, w - 0.44, 0.26, sub, size=10.5,
                          color="txt3", align="c", spacing=1.0))
    return els
