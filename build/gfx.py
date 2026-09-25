# -*- coding: utf-8 -*-
"""Generación de diagramas técnicos (PNG con transparencia) usados en el deck."""
import os, math
from PIL import Image, ImageDraw, ImageFilter
import theme
from theme import COL, hexcol, PIL_FONT, PXIN

GEN = os.path.join(theme.ASSETS, "gen")
SCALE = 3  # supersampling


# =============================================================== mini librería
class Draw:
    def __init__(self, w_in, h_in, bg=None):
        self.wi, self.hi = w_in, h_in
        self.W, self.H = int(w_in * PXIN * SCALE), int(h_in * PXIN * SCALE)
        self.img = Image.new("RGBA", (self.W, self.H),
                             hexcol(bg, 255) if bg else (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.img)

    def P(self, v):
        return v * PXIN * SCALE

    def font(self, size_pt, bold=False, mono=False):
        path = PIL_FONT[("mono" if mono else "body", bold)]
        return _f(path, int(size_pt * PXIN * SCALE / 72.0))

    def rrect(self, x, y, w, h, fill=None, line=None, lw=1.2, r=0.08):
        xy = [self.P(x), self.P(y), self.P(x + w), self.P(y + h)]
        if fill:
            self.d.rounded_rectangle(xy, radius=self.P(r), fill=hexcol(fill, 255 if True else None))
        if line:
            self.d.rounded_rectangle(xy, radius=self.P(r), outline=hexcol(line), width=max(1, int(self.P(lw / 72.0))))

    def rect(self, x, y, w, h, fill=None, line=None, lw=1.2):
        xy = [self.P(x), self.P(y), self.P(x + w), self.P(y + h)]
        if fill:
            self.d.rectangle(xy, fill=hexcol(fill))
        if line:
            self.d.rectangle(xy, outline=hexcol(line), width=max(1, int(self.P(lw / 72.0))))

    def circle(self, cx, cy, r, fill=None, line=None, lw=1.2):
        xy = [self.P(cx - r), self.P(cy - r), self.P(cx + r), self.P(cy + r)]
        if fill:
            self.d.ellipse(xy, fill=hexcol(fill))
        if line:
            self.d.ellipse(xy, outline=hexcol(line), width=max(1, int(self.P(lw / 72.0))))

    def line(self, x1, y1, x2, y2, color="txt2", lw=1.4, dash=False):
        if dash:
            n = max(2, int(math.hypot(x2 - x1, y2 - y1) / 0.075))
            for i in range(n):
                t0, t1 = i / n, (i + 0.5) / n
                self.d.line([self.P(x1 + (x2 - x1) * t0), self.P(y1 + (y2 - y1) * t0),
                             self.P(x1 + (x2 - x1) * t1), self.P(y1 + (y2 - y1) * t1)],
                            fill=hexcol(color), width=max(1, int(self.P(lw / 72.0))))
        else:
            self.d.line([self.P(x1), self.P(y1), self.P(x2), self.P(y2)],
                        fill=hexcol(color), width=max(1, int(self.P(lw / 72.0))))

    def poly(self, pts, line="txt2", lw=1.4, fill=None):
        p = [(self.P(a), self.P(b)) for a, b in pts]
        if fill:
            self.d.polygon(p, fill=hexcol(fill))
        if line:
            self.d.line(p, fill=hexcol(line), width=max(1, int(self.P(lw / 72.0))), joint="curve")

    def arc(self, x, y, w, h, a0, a1, color="txt2", lw=1.4):
        self.d.arc([self.P(x), self.P(y), self.P(x + w), self.P(y + h)], a0, a1,
                   fill=hexcol(color), width=max(1, int(self.P(lw / 72.0))))

    def text(self, x, y, s, size=8, color="txt2", bold=False, mono=False, align="l", anchor="t"):
        f = self.font(size, bold, mono)
        w = f.getlength(s) / (PXIN * SCALE)
        if align == "c":
            x -= w / 2.0
        elif align == "r":
            x -= w
        asc, desc = f.getmetrics()
        lh = (asc + desc) / (PXIN * SCALE)
        if anchor == "m":
            y -= lh / 2.0
        elif anchor == "b":
            y -= lh
        self.d.text((self.P(x), self.P(y)), s, font=f, fill=hexcol(color))

    def arrow(self, x1, y1, x2, y2, color="cyan", lw=1.4, head=0.075):
        self.line(x1, y1, x2, y2, color, lw)
        ang = math.atan2(y2 - y1, x2 - x1)
        for da in (2.6, -2.6):
            self.line(x2, y2, x2 + head * math.cos(ang + da), y2 + head * math.sin(ang + da), color, lw)

    def blob(self, cx, cy, r, color, alpha=40):
        img = Image.new("RGBA", (int(self.P(r * 2)), int(self.P(r * 2))), (0, 0, 0, 0))
        dr = ImageDraw.Draw(img)
        dr.ellipse([0, 0, img.width - 1, img.height - 1], fill=hexcol(color, alpha))
        img = img.filter(ImageFilter.GaussianBlur(self.P(r) * 0.5))
        self.img.alpha_composite(img, (int(self.P(cx) - img.width / 2), int(self.P(cy) - img.height / 2)))

    def save(self, name):
        os.makedirs(GEN, exist_ok=True)
        path = os.path.join(GEN, name if name.endswith(".png") else name + ".png")
        self.img.resize((self.img.width // 1, self.img.height // 1), Image.LANCZOS).save(path)
        return path


_fc = {}


def _f(path, px):
    if (path, px) not in _fc:
        from PIL import ImageFont
        _fc[(path, px)] = ImageFont.truetype(path, max(6, int(px)))
    return _fc[(path, px)]


# ============================================================ bloques comunes
def _qbez(p0, p1, c, n=16):
    pts = []
    for i in range(n + 1):
        t = i / float(n)
        u = 1 - t
        pts.append((u * u * p0[0] + 2 * u * t * c[0] + t * t * p1[0],
                    u * u * p0[1] + 2 * u * t * c[1] + t * t * p1[1]))
    return pts


def _or_outline(x, y, w, h):
    """Contorno del símbolo OR: dorso cóncavo y punta a la derecha."""
    x0 = x + w * 0.12
    tip = (x + w, y + h / 2.0)
    top = _qbez((x0, y), tip, (x + w * 0.60, y + h * 0.06))
    bot = _qbez(tip, (x0, y + h), (x + w * 0.60, y + h * 0.94))
    back = _qbez((x0, y + h), (x0, y), (x - w * 0.05, y + h / 2.0))
    return top + bot + back


def draw_gate(d, kind, x, y, w, h, accent="cyan", labels=("A", "B"), out="Y", lw=1.6,
              show_name=False, name_size=8, two_in=True):
    """Símbolo ANSI de compuerta. x,y = esquina superior izquierda del cuerpo."""
    body_c = "card2"
    if kind in ("and", "nand"):
        pts = [(x, y), (x + w * 0.60, y)]
        for i in range(0, 25):
            th = -math.pi / 2 + math.pi * i / 24.0
            pts.append((x + w * 0.60 + (w * 0.40) * math.cos(th), y + h / 2 + (h / 2) * math.sin(th)))
        pts += [(x + w * 0.60, y + h), (x, y + h)]
        d.poly(pts, line=accent, lw=lw, fill=body_c)
        tip_x = x + w
    elif kind in ("or", "nor", "xor", "xnor"):
        if kind in ("xor", "xnor"):
            d.poly(_or_outline(x - w * 0.13, y, w, h), line=accent, lw=lw * 0.9)
        d.poly(_or_outline(x, y, w, h), line=accent, lw=lw, fill=body_c)
        tip_x = x + w
    else:  # not / buffer
        d.poly([(x, y), (x + w, y + h / 2), (x, y + h)], line=accent, lw=lw, fill=body_c)
        tip_x = x + w
    # burbuja de inversión
    if kind in ("nand", "nor", "xnor", "not"):
        r = h * 0.075
        d.circle(tip_x + r + 0.012, y + h / 2, r, fill="bg", line=accent, lw=lw)
        tip_x += 2 * r + 0.024
    # entradas / salidas
    if two_in:
        ys = (y + h * 0.30, y + h * 0.70)
        for i, yy in enumerate(ys):
            d.line(x - 0.30, yy, x + 0.02, yy, "txt2", lw)
            if i < len(labels) and labels[i]:
                d.text(x - 0.34, yy, labels[i], 9, "txt", True, mono=True, align="r", anchor="m")
    else:
        yy = y + h / 2
        d.line(x - 0.30, yy, x + 0.02, yy, "txt2", lw)
        if labels and labels[0]:
            d.text(x - 0.34, yy, labels[0], 9, "txt", True, mono=True, align="r", anchor="m")
    d.line(tip_x, y + h / 2, tip_x + 0.30, y + h / 2, "txt2", lw)
    if out:
        d.text(tip_x + 0.34, y + h / 2, out, 9, "txt", True, mono=True, anchor="m")
    if show_name:
        d.text(x + w / 2, y + h + 0.10, kind.upper(), name_size, accent, True, mono=True, align="c")
    return tip_x


def waveform(d, x, y, w, h, bits, label, color="cyan", lw=1.7, label_size=9.5):
    """Dibuja una señal digital a partir de una lista de bits ('0'/'1'/'x')."""
    n = len(bits)
    step = w / float(n)
    lvl_hi, lvl_lo = y, y + h
    pts = []
    for i, b in enumerate(bits):
        if b == "x":
            continue
        yy = lvl_hi if b == "1" else lvl_lo
        pts.append((x + i * step, yy))
        pts.append((x + (i + 1) * step, yy))
    d.poly(pts, line=color, lw=lw)
    for i in range(1, n):
        xx = x + i * step
        d.line(xx, lvl_lo + 0.02, xx, lvl_hi - 0.02, "line", 0.7, dash=True)
    d.text(x - 0.14, y + h / 2, label, label_size, color, True, mono=True, align="r", anchor="m")


def dip_package(d, x, y, w, h, accent="cyan", pin_labels=None, title=None, gate=None,
                n_pins=14, in_labels=None):
    """Dibuja un encapsulado DIP con muesca, pines y etiquetas."""
    body_w, body_h = w * 0.72, h
    bx = x + (w - body_w) / 2.0
    d.rrect(bx, y, body_w, body_h, fill="card2", line=accent, lw=1.5, r=0.06)
    d.circle(bx + body_w / 2, y + 0.10, 0.055, fill=None, line=accent, lw=1.3)
    d.arc(bx + body_w / 2 - 0.16, y - 0.05, 0.32, 0.30, 180, 360, color=accent, lw=1.4)
    half = n_pins // 2
    ph = body_h / float(half + 1)
    for i in range(half):        # lado izquierdo: 1..half
        yy = y + ph * (i + 0.5) + ph * 0.35
        d.rect(bx - 0.16, yy - 0.014, 0.16, 0.028, fill="txt3")
        num = str(i + 1)
        lab = (pin_labels or {}).get(num, "")
        d.text(bx - 0.20, yy, num, 8.5, "txt2", True, mono=True, align="r", anchor="m")
        if lab:
            d.text(bx + 0.08, yy, lab, 8.5, "txt", False, mono=True, anchor="m")
    for i in range(half):        # lado derecho: n_pins..half+1
        yy = y + body_h - ph * (i + 0.5) - ph * 0.35
        d.rect(bx + body_w, yy - 0.014, 0.16, 0.028, fill="txt3")
        num = str(n_pins - i)
        lab = (pin_labels or {}).get(num, "")
        d.text(bx + body_w + 0.20, yy, num, 8.5, "txt2", True, mono=True, anchor="m")
        if lab:
            d.text(bx + body_w - 0.08, yy, lab, 8.5, "txt", False, mono=True, align="r", anchor="m")
    if title:
        d.text(x + w / 2, y - 0.26, title, 11, accent, True, mono=True, align="c")
    ay = y + body_h * 0.30
    if gate:
        for k, g in enumerate(gate):
            draw_gate(d, g, bx + body_w * 0.24, y + body_h * (0.16 + 0.5 * k if len(gate) > 1 else 0.28),
                      body_w * 0.52, body_h * (0.22 if len(gate) > 1 else 0.34), accent=accent,
                      labels=("", ""), out="", lw=1.3, two_in=True)
    return bx, body_w


# ================================================================ los diagramas
def gates():
    order = [("and", "Bullet"), ("or", None), ("not", None), ("nand", None), ("nor", None),
             ("xor", None), ("xnor", None), ("buffer", None)]
    for kind, _ in order:
        d = Draw(2.05, 1.30)
        k = "buffer" if kind == "buffer" else kind
        acc = {"and": "cyan", "or": "orange", "not": "purple", "nand": "green",
               "nor": "pink", "xor": "blue", "xnor": "yellow", "buffer": "teal"}[kind]
        draw_gate(d, k, 0.42, 0.22, 1.20, 0.86, accent=acc, lw=1.9,
                  labels=("A", "B"), out="Y", two_in=(kind != "not" and kind != "buffer"))
        d.text(1.02, 1.16, {"buffer": "BUFFER / 7407", "and": "AND · 7408", "or": "OR · 7432",
                            "not": "NOT · 7404", "nand": "NAND · 7400", "nor": "NOR · 7402",
                            "xor": "XOR · 7486", "xnor": "XNOR · 74266"}[kind],
               9.5, acc, True, mono=True, align="c")
        d.save("gate_" + kind)


def waveform_set():
    patterns = {
        "and":  ("00110011", "00001111", "00000011"),
        "or":   ("00110011", "00001111", "00111111"),
        "nand": ("00110011", "00001111", "11111100"),
        "nor":  ("00110011", "00001111", "11000000"),
        "xor":  ("00110011", "00001111", "00111100"),
        "xnor": ("00110011", "00001111", "11000011"),
    }
    for k, (a, b, y) in patterns.items():
        d = Draw(5.6, 1.85)
        acc = {"and": "cyan", "or": "orange", "nand": "green", "nor": "pink",
               "xor": "blue", "xnor": "yellow"}[k]
        d.text(0.05, 0.02, "DIAGRAMA DE TIEMPOS · " + k.upper(), 9, acc, True, mono=True)
        y0 = 0.34
        for i, (bits, lab, col) in enumerate([(a, "A", "txt2"), (b, "B", "txt2"), (y, "Y", acc)]):
            waveform(d, 0.62, y0 + i * 0.48, 4.72, 0.28, bits, lab, col, 1.7)
        d.line(0.62, y0 - 0.06, 0.62, y0 + 3 * 0.48 - 0.16, "line", 1.0)
        d.save("time_" + k)


def pinouts():
    chips = {
        "7400": dict(title="7400 · Quad 2-Entradas NAND", gate=["nand", "nand", "nand", "nand"],
                     labels={"1": "1A", "2": "1B", "3": "1Y", "4": "2A", "5": "2B", "6": "2Y",
                             "7": "GND", "8": "3Y", "9": "3A", "10": "3B", "11": "4Y",
                             "12": "4A", "13": "4B", "14": "VCC"}, acc="green"),
        "7408": dict(title="7408 · Quad 2-Entradas AND", gate=["and", "and", "and", "and"],
                     labels={"1": "1A", "2": "1B", "3": "1Y", "4": "2A", "5": "2B", "6": "2Y",
                             "7": "GND", "8": "3Y", "9": "3A", "10": "3B", "11": "4Y",
                             "12": "4A", "13": "4B", "14": "VCC"}, acc="cyan"),
        "7432": dict(title="7432 · Quad 2-Entradas OR", gate=["or", "or", "or", "or"],
                     labels={"1": "1A", "2": "1B", "3": "1Y", "4": "2A", "5": "2B", "6": "2Y",
                             "7": "GND", "8": "3Y", "9": "3A", "10": "3B", "11": "4Y",
                             "12": "4A", "13": "4B", "14": "VCC"}, acc="orange"),
        "7402": dict(title="7402 · Quad 2-Entradas NOR", gate=["nor", "nor", "nor", "nor"],
                     labels={"1": "1Y", "2": "1A", "3": "1B", "4": "2Y", "5": "2A", "6": "2B",
                             "7": "GND", "8": "3A", "9": "3B", "10": "3Y", "11": "4A",
                             "12": "4B", "13": "4Y", "14": "VCC"}, acc="pink"),
        "7486": dict(title="7486 · Quad 2-Entradas XOR", gate=["xor", "xor", "xor", "xor"],
                     labels={"1": "1A", "2": "1B", "3": "1Y", "4": "2A", "5": "2B", "6": "2Y",
                             "7": "GND", "8": "3Y", "9": "3A", "10": "3B", "11": "4Y",
                             "12": "4A", "13": "4B", "14": "VCC"}, acc="blue"),
        "74266": dict(title="74266 · Quad XNOR (colector abierto)", gate=["xnor", "xnor", "xnor", "xnor"],
                      labels={"1": "1Y", "2": "1A", "3": "1B", "4": "2Y", "5": "2A", "6": "2B",
                              "7": "GND", "8": "3A", "9": "3B", "10": "3Y", "11": "4A",
                              "12": "4B", "13": "4Y", "14": "VCC"}, acc="yellow"),
        "7404": dict(title="7404 · Hex Inversor", gate=["not", "not", "not", "not"],
                     labels={"1": "1A", "2": "1Y", "3": "2A", "4": "2Y", "5": "3A", "6": "3Y",
                             "7": "GND", "8": "4Y", "9": "4A", "10": "5Y", "11": "5A",
                             "12": "6Y", "13": "6A", "14": "VCC"}, acc="purple"),
    }
    for name, cfg in chips.items():
        d = Draw(4.1, 3.4)
        d.rrect(0.05, 0.05, 4.0, 3.3, fill="panel", line="line", lw=1.0, r=0.10)
        dip_package(d, 0.30, 0.62, 3.5, 2.35, accent=cfg["acc"], pin_labels=cfg["labels"],
                    title=cfg["title"], gate=None)
        # cuatro símbolos de compuerta dentro del cuerpo
        bx = 0.30 + (3.5 - 3.5 * 0.72) / 2.0
        bw = 3.5 * 0.72
        for k, g in enumerate(cfg["gate"]):
            col, row = k % 2, k // 2
            gx = bx + bw * (0.14 + 0.5 * col)
            gy = 0.62 + 2.35 * (0.10 + 0.48 * row)
            draw_gate(d, g, gx, gy, bw * 0.30, 2.35 * 0.19, accent=cfg["acc"], lw=1.1,
                      labels=("", ""), out="", two_in=(g != "not"))
        d.text(2.05, 3.22, "VCC = pin 14  ·  GND = pin 7  ·  encapsulado DIP-14", 9,
               "txt3", False, mono=True, align="c")
        d.save("pin_" + name)


def adders():
    # medio sumador
    d = Draw(4.5, 2.5, bg="panel")
    # (entradas A y B dibujadas por draw_gate)
    d.text(0.12, 0.08, "MEDIO SUMADOR (HALF ADDER)", 9.5, "cyan", True, mono=True)
    draw_gate(d, "xor", 1.35, 0.45, 1.25, 0.75, accent="blue", labels=("A", "B"), out="S", lw=1.7)
    draw_gate(d, "and", 1.35, 1.45, 1.25, 0.75, accent="cyan", labels=("A", "B"), out="C", lw=1.7)
    d.line(0.62, 0.73, 1.05, 0.73, "txt2", 1.5)
    d.line(1.05, 0.73, 1.05, 1.73, "txt2", 1.5)
    d.line(1.05, 1.73, 1.05, 1.73, "txt2", 1.5)
    d.line(0.62, 1.73, 1.05, 1.73, "txt2", 1.5)
    d.line(1.05, 0.73, 1.05, 1.73, "txt2", 1.5)
    d.text(3.0, 0.72, "S = A ⊕ B  (suma)", 10, "blue", True, mono=True, anchor="m")
    d.text(3.0, 1.72, "C = A · B  (acarreo)", 10, "cyan", True, mono=True, anchor="m")
    d.text(0.12, 2.22, "S = 1 cuando las entradas difieren · C = 1 solo si A = B = 1", 9, "txt3")
    d.save("half_adder")

    # sumador completo
    d = Draw(6.0, 2.6, bg="panel")
    d.text(0.12, 0.08, "SUMADOR COMPLETO (FULL ADDER) — 2 XOR + 2 AND + 1 OR", 9.5, "cyan", True, mono=True)
    draw_gate(d, "xor", 1.25, 0.42, 1.05, 0.66, accent="blue", labels=("A", "B"), out="", lw=1.5)
    draw_gate(d, "xor", 3.10, 0.42, 1.05, 0.66, accent="teal", labels=("X", "Cin"), out="S", lw=1.5)
    d.line(2.60, 0.75, 2.80, 0.75, "txt2", 1.4)
    d.text(2.70, 0.60, "X", 8.5, "txt3", False, mono=True, align="c")
    draw_gate(d, "and", 1.25, 1.45, 1.05, 0.66, accent="cyan", labels=("A", "B"), out="", lw=1.5)
    draw_gate(d, "and", 3.10, 1.45, 1.05, 0.66, accent="cyan", labels=("", "Cin"), out="", lw=1.5)
    d.line(2.10, 0.75, 2.10, 1.78, "txt2", 1.4)
    d.line(2.10, 1.78, 2.10, 1.78, "txt2", 1.4)
    d.line(2.10, 0.75, 3.10 - 0.30, 0.75, "txt2", 1.4)
    d.line(2.10, 1.78, 3.10 - 0.30, 1.78, "txt2", 1.4)
    d.line(2.10, 0.75, 2.10, 1.78, "txt2", 1.4)
    draw_gate(d, "or", 4.85, 1.45, 0.85, 0.66, accent="orange", labels=("", ""), out="Cout", lw=1.5)
    d.line(4.15, 1.78, 4.55, 1.78, "txt2", 1.4)
    d.line(4.15, 1.78, 4.15, 1.62, "txt2", 1.4)
    d.line(4.15, 1.62, 4.55, 1.62, "txt2", 1.4)
    d.text(0.12, 2.22, "S = A ⊕ B ⊕ Cin   ·   Cout = A·B + Cin·(A ⊕ B)", 10, "txt", True, mono=True)
    d.save("full_adder")

    # sumador 4 bits en cascada
    d = Draw(7.2, 1.9, bg="panel")
    d.text(0.12, 0.06, "SUMADOR EN CASCADA DE 4 BITS (ACARREO ONDULANTE) · 74LS83 / 74LS283", 9.5,
           "cyan", True, mono=True)
    for i in range(4):
        x = 0.55 + i * 1.62
        d.rrect(x, 0.55, 1.30, 0.82, fill="card2", line="cyan", lw=1.4, r=0.06)
        d.text(x + 0.65, 0.72, "FA%d" % i, 10, "cyan", True, mono=True, align="c")
        d.text(x + 0.65, 1.05, "S%d" % i, 9, "txt2", False, mono=True, align="c")
        d.line(x - 0.36, 0.78, x + 0.02, 0.78, "txt2", 1.3)
        d.text(x - 0.38, 0.78, "A%d" % i, 8.5, "txt3", False, mono=True, align="r", anchor="m")
        d.line(x - 0.36, 1.14, x + 0.02, 1.14, "txt2", 1.3)
        d.text(x - 0.38, 1.14, "B%d" % i, 8.5, "txt3", False, mono=True, align="r", anchor="m")
        d.line(x + 0.65, 1.37, x + 0.65, 1.62, "txt2", 1.3)
        if i < 3:
            d.arrow(x + 1.30, 0.96, x + 1.62, 0.96, "orange", 1.4)
    d.text(6.55, 0.96, "C", 9, "orange", True, mono=True, align="r", anchor="m")
    d.text(0.55, 1.66, "C0 = 0", 8.5, "txt3", False, mono=True)
    d.save("ripple_adder")


def mux_demux():
    # multiplexor 4:1
    d = Draw(5.2, 2.6, bg="panel")
    d.text(0.12, 0.06, "MULTIPLEXOR 4:1 · 74LS153 (doble) / 74LS151 (8:1)", 9.5, "purple", True, mono=True)
    d.rrect(1.55, 0.45, 1.75, 1.55, fill="card2", line="purple", lw=1.6, r=0.08)
    d.text(2.42, 0.62, "MUX 4:1", 10.5, "purple", True, mono=True, align="c")
    for i in range(4):
        yy = 0.95 + i * 0.26
        d.line(1.10, yy, 1.55, yy, "txt2", 1.3)
        d.text(1.06, yy, "D%d" % i, 8.5, "txt3", False, mono=True, align="r", anchor="m")
    d.line(3.30, 1.22, 3.85, 1.22, "purple", 1.6)
    d.text(3.90, 1.22, "Y", 10, "purple", True, mono=True, anchor="m")
    d.line(2.42, 2.00, 2.42, 2.35, "txt2", 1.3)
    d.text(2.42, 2.36, "S1 S0  (selección)", 8.5, "txt3", False, mono=True, align="c")
    d.text(0.12, 2.42, "Y = D0·S1'S0' + D1·S1'S0 + D2·S1S0' + D3·S1S0", 9, "txt", True, mono=True)
    d.save("mux4")

    # decodificador 3:8
    d = Draw(5.2, 3.0, bg="panel")
    d.text(0.12, 0.06, "DECODIFICADOR 3 A 8 · 74LS138", 9.5, "orange", True, mono=True)
    d.rrect(1.60, 0.42, 1.80, 2.10, fill="card2", line="orange", lw=1.6, r=0.08)
    d.text(2.50, 0.56, "3:8 DEC", 10.5, "orange", True, mono=True, align="c")
    for i in range(3):
        yy = 0.95 + i * 0.26
        d.line(1.10, yy, 1.60, yy, "txt2", 1.3)
        d.text(1.06, yy, "A%d" % i, 8.5, "txt3", False, mono=True, align="r", anchor="m")
    for i in range(8):
        yy = 0.62 + i * 0.21
        d.line(3.40, yy, 3.90, yy, "txt2", 1.2)
        d.text(3.94, yy, "Y%d" % i, 8, "txt3", False, mono=True, anchor="m")
    d.text(0.12, 2.68, "Activa UNA sola salida (la que corresponde al código binario de entrada).", 9, "txt3")
    d.save("decoder38")

    # codificador 8:3
    d = Draw(4.8, 2.4, bg="panel")
    d.text(0.12, 0.06, "CODIFICADOR 8 A 3 · 74LS148 (prioritario)", 9.5, "pink", True, mono=True)
    d.rrect(1.55, 0.45, 1.70, 1.55, fill="card2", line="pink", lw=1.6, r=0.08)
    d.text(2.40, 0.62, "8:3 ENC", 10.5, "pink", True, mono=True, align="c")
    for i in range(8):
        yy = 0.88 + i * 0.145
        d.line(1.15, yy, 1.55, yy, "txt2", 1.1)
        d.text(1.11, yy, "D%d" % i, 7.5, "txt3", False, mono=True, align="r", anchor="m")
    for i in range(3):
        yy = 1.05 + i * 0.24
        d.line(3.25, yy, 3.70, yy, "pink", 1.4)
        d.text(3.75, yy, "A%d" % i, 9, "pink", True, mono=True, anchor="m")
    d.text(0.12, 2.08, "Convierte la línea activa en su número binario (GS indica 'hay entrada activa').", 9, "txt3")
    d.save("encoder83")


def sequential():
    # latch SR con NAND
    d = Draw(4.4, 2.4, bg="panel")
    d.text(0.12, 0.06, "LATCH SR CON PUERTAS NAND (memoria de 1 bit)", 9.5, "green", True, mono=True)
    draw_gate(d, "nand", 1.55, 0.50, 1.15, 0.70, accent="green", labels=("S", "Q'"), out="Q", lw=1.5)
    draw_gate(d, "nand", 1.55, 1.50, 1.15, 0.70, accent="green", labels=("R", "Q"), out="Q'", lw=1.5)
    d.poly([(3.05, 0.85), (3.75, 0.85), (3.75, 1.85), (2.75, 1.85)], line="cyan", lw=1.5)
    d.poly([(3.05, 1.85), (3.60, 1.85), (3.60, 0.85), (2.75, 0.85)], line="orange", lw=1.5)
    d.text(0.12, 2.18, "S=0, R=1 → Q=1 (set) · S=1, R=0 → Q=0 (reset) · S=R=1 → mantiene", 8.8, "txt3")
    d.save("latch_sr")

    # flip-flop D con reloj
    d = Draw(5.0, 2.2, bg="panel")
    d.text(0.12, 0.06, "FLIP-FLOP D DISPARADO POR FLANCO · 74LS74 (doble D) / 74LS175", 9.5, "indigo", True, mono=True)
    d.rrect(1.35, 0.55, 1.45, 1.10, fill="card2", line="indigo", lw=1.6, r=0.06)
    d.text(2.07, 0.68, "D  FF", 10, "indigo", True, mono=True, align="c")
    d.text(2.07, 1.20, "CLK ▷", 8.5, "txt3", False, mono=True, align="c")
    d.line(0.75, 0.85, 1.35, 0.85, "txt2", 1.4); d.text(0.70, 0.85, "D", 9.5, "txt", True, mono=True, align="r", anchor="m")
    d.line(2.80, 0.85, 3.45, 0.85, "indigo", 1.5); d.text(3.50, 0.85, "Q", 9.5, "indigo", True, mono=True, anchor="m")
    d.line(2.80, 1.35, 3.45, 1.35, "txt2", 1.3); d.text(3.50, 1.35, "Q'", 9.5, "txt2", False, mono=True, anchor="m")
    d.line(0.75, 1.35, 1.35, 1.35, "txt2", 1.4); d.text(0.70, 1.35, "CLK", 9.5, "txt", True, mono=True, align="r", anchor="m")
    waveform(d, 0.75, 1.68, 3.6, 0.20, "0101010101", "CLK", "txt3", 1.4)
    waveform(d, 0.75, 1.92, 3.6, 0.20, "0011001100", "Q", "indigo", 1.4)
    d.save("ff_d")

    # contador 4 bits
    d = Draw(5.6, 2.2, bg="panel")
    d.text(0.12, 0.06, "CONTADOR BINARIO DE 4 BITS · 74LS161 / 74LS163 / 74LS393", 9.5, "teal", True, mono=True)
    for i in range(4):
        x = 0.55 + i * 1.25
        d.rrect(x, 0.55, 0.95, 0.80, fill="card2", line="teal", lw=1.4, r=0.06)
        d.text(x + 0.47, 0.68, "T-FF", 9, "teal", True, mono=True, align="c")
        d.text(x + 0.47, 1.05, "Q%d" % i, 9, "txt2", False, mono=True, align="c")
        if i < 3:
            d.arrow(x + 0.95, 0.95, x + 1.25, 0.95, "line2", 1.3)
    d.text(0.55, 1.52, "Secuencia: 0000 → 0001 → 0010 → ... → 1111 → 0000 (16 estados, módulo 16)", 9, "txt3")
    d.text(0.55, 1.80, "El 74LS163 se reinicia con LOAD síncrono; el 74LS390 es décadas dobles para displays.", 9, "txt3")
    d.save("counter4")

    # registro de desplazamiento
    d = Draw(5.6, 2.0, bg="panel")
    d.text(0.12, 0.06, "REGISTRO DE DESPLAZAMIENTO 74LS164 (entrada serie → salida paralelo)", 9.5, "blue", True, mono=True)
    for i in range(4):
        x = 0.65 + i * 1.20
        d.rrect(x, 0.60, 0.90, 0.70, fill="card2", line="blue", lw=1.4, r=0.06)
        d.text(x + 0.45, 0.95, "FF%d" % i, 9.5, "blue", True, mono=True, align="c")
        d.text(x + 0.45, 1.36, "Q%d" % i, 8.5, "txt3", False, mono=True, align="c")
        if i < 3:
            d.arrow(x + 0.90, 0.95, x + 1.20, 0.95, "line2", 1.3)
    d.arrow(0.20, 0.95, 0.65, 0.95, "cyan", 1.4)
    d.text(0.20, 0.72, "Datos serie", 8.5, "cyan", False, mono=True, align="l")
    d.text(0.65, 1.62, "Con 8 bits: 16 LEDs, displays o expansión de puertos. Base de los registros de corrimiento.", 9, "txt3")
    d.save("shiftreg")


def seven_seg():
    d = Draw(4.6, 3.0, bg="panel")
    d.text(0.12, 0.06, "DECODIFICADOR BCD A 7 SEGMENTOS · 74LS47 / 74LS48", 9.5, "red", True, mono=True)
    d.rrect(0.35, 0.60, 1.5, 1.15, fill="card2", line="red", lw=1.5, r=0.06)
    d.text(1.10, 0.75, "74LS47", 10, "red", True, mono=True, align="c")
    d.text(1.10, 1.05, "BCD → 7 seg", 8.5, "txt3", False, mono=True, align="c")
    d.text(1.10, 1.32, "a b c d e f g", 8, "txt3", False, mono=True, align="c")
    for i in range(4):
        yy = 0.75 + i * 0.20
        d.line(0.20, yy, 0.35, yy, "txt2", 1.2)
        d.text(0.18, yy, "D%d" % i, 7.5, "txt3", False, mono=True, align="r", anchor="m")
    d.line(1.85, 1.10, 2.35, 1.10, "red", 1.4)
    # display
    dx, dy = 2.45, 0.55
    seg = {"a": (dx + 0.12, dy + 0.02, 0.60, 0.10), "b": (dx + 0.72, dy + 0.14, 0.10, 0.62),
           "c": (dx + 0.72, dy + 0.86, 0.10, 0.62), "d": (dx + 0.12, dy + 1.50, 0.60, 0.10),
           "e": (dx + 0.02, dy + 0.86, 0.10, 0.62), "f": (dx + 0.02, dy + 0.14, 0.10, 0.62),
           "g": (dx + 0.12, dy + 0.76, 0.60, 0.10)}
    for k, (sx, sy, sw, sh) in seg.items():
        on = k in "abcdef"      # muestra el dígito "0"
        d.rrect(sx, sy, sw, sh, fill=("red" if on else "line"), r=0.02)
    d.rrect(dx - 0.10, dy - 0.10, 0.94, 1.80, fill=None, line="line2", lw=1.4, r=0.06)
    d.text(dx + 0.37, dy + 1.80, "dígito 0", 8.5, "txt3", False, mono=True, align="c")
    d.text(0.12, 2.55, "Entradas BCD 0000–1001 → dígitos 0–9. Salidas activas en bajo en el 74LS47.", 9, "txt3")
    d.save("sevenseg")


def electrical():
    # márgenes de ruido
    d = Draw(6.4, 2.9, bg="panel")
    d.text(0.12, 0.06, "NIVELES LÓGICOS Y MARGEN DE RUIDO EN TTL (VCC = 5 V)", 9.5, "cyan", True, mono=True)
    x0, yv, wv = 1.15, 0.55, 4.55
    d.rect(x0, yv, wv, 0.30, fill="card2", line="line2", lw=1.0)
    def vx(v):
        return x0 + wv * (v / 5.0)
    bands = [(0.0, 0.8, "red", "BAJO garantizado (VIL ≤ 0.8 V)"),
             (0.8, 2.0, "yellow", "zona prohibida"),
             (2.0, 5.0, "green", "ALTO garantizado (VIH ≥ 2.0 V)")]
    for a, b, col, lab in bands:
        d.rect(vx(a), yv, vx(b) - vx(a), 0.30, fill=col)
    d.circle(vx(0.4), yv + 0.15, 0.045, fill="bg", line="txt")
    d.circle(vx(2.4), yv + 0.15, 0.045, fill="bg", line="txt")
    d.text(vx(0.4), yv + 0.24, "VOL máx 0.4 V", 8.5, "txt", False, mono=True, align="c")
    d.text(vx(2.4), yv + 0.24, "VOH mín 2.4 V", 8.5, "txt", False, mono=True, align="c")
    for v, lab in ((0, "0 V"), (1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5 V")):
        d.line(vx(v), yv + 0.30, vx(v), yv + 0.38, "line2", 1.0)
        d.text(vx(v), yv + 0.40, lab, 8, "txt3", False, mono=True, align="c")
    d.text(0.12, 1.28, "Margen de ruido:", 10, "cyan", True)
    d.text(0.12, 1.52, "NM(0)  = VIL(máx) − VOL(máx) = 0.8 V − 0.4 V = 0.4 V", 9.8, "txt2", False, mono=True)
    d.text(0.12, 1.76, "NM(1)  = VOH(mín) − VIH(mín) = 2.4 V − 2.0 V = 0.4 V", 9.8, "txt2", False, mono=True)
    d.text(0.12, 2.10, "Todo voltaje entre 0.8 V y 2.0 V es indeterminado: puede leerse 0 o 1, y produce", 9, "txt3")
    d.text(0.12, 2.32, "oscilaciones, consumo excesivo y calentamiento del integrado.", 9, "txt3")
    d.save("noise_margin")

    # retardo de propagación
    d = Draw(6.4, 2.4, bg="panel")
    d.text(0.12, 0.06, "TIEMPO DE PROPAGACIÓN (tPD) Y FLANCOS", 9.5, "orange", True, mono=True)
    waveform(d, 0.80, 0.48, 4.9, 0.32, "11000011", "Entrada", "txt2", 1.7)
    waveform(d, 0.80, 1.16, 4.9, 0.32, "11110000", "Salida", "orange", 1.7)
    step = 4.9 / 8.0
    d.line(0.80 + step, 0.48, 0.80 + step, 1.48, "cyan", 1.2, dash=True)
    d.line(0.80 + step * 1.55, 0.48, 0.80 + step * 1.55, 1.48, "orange", 1.2, dash=True)
    d.arrow(0.80 + step, 1.60, 0.80 + step * 1.55, 1.60, "txt3", 1.2)
    d.text(0.80 + step * 1.27, 1.72, "tPD = 8 ns … 15 ns (74LS)", 9.5, "txt", True, mono=True, align="c")
    d.text(0.12, 2.06, "El retardo limita la frecuencia máxima de operación: fMÁX ≈ 1 / (2·n·tPD) en cadenas en cascada.", 9, "txt3")
    d.save("prop_delay")

    # fan-out
    d = Draw(5.6, 2.8, bg="panel")
    d.text(0.12, 0.06, "FAN-OUT: UNA SALIDA ALIMENTA 10 ENTRADAS TTL ESTÁNDAR", 9.5, "green", True, mono=True)
    d.rrect(0.35, 1.05, 1.05, 0.70, fill="card2", line="green", lw=1.5, r=0.06)
    d.text(0.87, 1.40, "Salida", 9, "green", True, mono=True, align="c", anchor="m")
    for i in range(5):
        for j in range(2):
            yy = 0.35 + i * 0.50 + j * 0.20
            xx = 3.35 + j * 1.05
            d.rrect(xx, yy, 0.85, 0.17, fill="card", line="line2", lw=1.0, r=0.04)
            d.line(1.40, 1.40, 1.55, 1.40, "green", 1.4)
            d.line(1.55, 1.40, 1.55, yy + 0.085, "line2", 1.0)
            d.line(1.55, yy + 0.085, xx, yy + 0.085, "line2", 1.0)
    d.text(0.12, 2.55, "IOH/IOL: 0.4 mA / 16 mA (74LS). Cada entrada consume 20 µA (alta) y 0.4 mA (baja).", 9, "txt3")
    d.text(3.35, 0.15, "10 cargas TTL", 9, "txt3", False, mono=True, align="c")
    d.save("fanout")

    # alimentación y desacople
    d = Draw(5.4, 2.6, bg="panel")
    d.text(0.12, 0.06, "MONTAJE BÁSICO: 5 V, DESACOPLE, PULL-UP Y LED", 9.5, "yellow", True, mono=True)
    d.line(0.55, 2.05, 4.95, 2.05, "txt2", 1.6)                 # GND
    d.line(0.55, 0.45, 4.95, 0.45, "red", 1.6)                  # VCC
    d.text(4.99, 0.45, "+5 V", 9, "red", False, mono=True, anchor="m")
    d.text(4.99, 2.05, "GND", 9, "txt3", False, mono=True, anchor="m")
    d.rrect(1.15, 0.85, 1.25, 0.85, fill="card2", line="cyan", lw=1.5, r=0.06)
    d.text(1.77, 1.27, "74LS00", 9.5, "cyan", True, mono=True, align="c", anchor="m")
    d.line(1.77, 0.85, 1.77, 0.45, "line2", 1.2)
    d.line(1.77, 1.70, 1.77, 2.05, "line2", 1.2)
    # capacitor de desacople
    d.line(3.10, 0.45, 3.10, 0.95, "line2", 1.2)
    d.line(2.85, 0.95, 3.35, 0.95, "yellow", 2.0)
    d.line(2.85, 1.10, 3.35, 1.10, "yellow", 2.0)
    d.line(3.10, 1.10, 3.10, 2.05, "line2", 1.2)
    d.text(3.45, 1.02, "100 nF cerámico", 8.5, "yellow", False, mono=True)
    # led
    d.rrect(4.05, 1.05, 0.45, 0.55, fill="card", line="line2", lw=1.0, r=0.04)
    d.text(4.27, 1.32, "R", 8.5, "txt2", False, mono=True, align="c", anchor="m")
    d.poly([(4.20, 1.72), (4.45, 1.72), (4.33, 1.98)], line="green", lw=1.3, fill="green")
    d.text(2.85, 2.22, "R = (VCC − VF) / IF  ≈  (5 V − 2 V) / 10 mA = 300 Ω  →  330 Ω comercial", 9, "txt3")
    d.save("power_setup")

    # ESD y manejo
    d = Draw(5.0, 2.5, bg="panel")
    d.text(0.12, 0.06, "MANEJO SEGURO DE INTEGRADOS (ESD / CMOS)", 9.5, "purple", True, mono=True)
    items = ["Pulsera antiestática conectada a tierra (1 MΩ)",
             "Tapete disipativo y mesa sin plásticos",
             "Almacenar en tubo/bolsa conductiva antiestática",
             "Nunca insertar ni retirar el chip con la alimentación activa"]
    for i, t in enumerate(items):
        yy = 0.45 + i * 0.42
        d.rrect(0.30, yy + 0.05, 0.16, 0.16, fill="purple", r=0.03)
        d.text(0.60, yy, t, 9.5, "txt2")
    d.text(0.30, 2.15, "Los CMOS (74HC/74HCT) toleran menos descargas: el daño puede ser latente y aparecer después.", 8.8, "txt3")
    d.save("esd")


def families():
    d = Draw(6.8, 3.0, bg="panel")
    d.text(0.12, 0.06, "FAMILIAS LÓGICAS: VELOCIDAD, CONSUMO Y FAN-OUT", 9.5, "cyan", True, mono=True)
    data = [("74xx (TTL)", 10, 10), ("74L (bajo consumo)", 33, 2), ("74LS (Schottky baja pot.)", 9.5, 2),
            ("74S (Schottky)", 3, 20), ("74ALS (avanzada)", 4, 1.2), ("74F (rápida)", 3, 4.5),
            ("74HC (CMOS alta vel.)", 8, 0.02), ("74HCT (CMOS compatible TTL)", 9, 0.02)]
    y = 0.45
    for name, tpd, pw in data:
        d.text(2.35, y + 0.13, name, 9, "txt2", False, mono=True, align="r", anchor="m")
        bl = 3.4 * min(1.0, tpd / 33.0)
        d.rect(2.50, y + 0.05, 3.4, 0.16, fill="panel2", line=None)
        d.rrect(2.50, y + 0.05, max(0.06, bl), 0.16, fill="orange", r=0.02)
        d.text(6.02, y + 0.13, "%.1f ns" % tpd, 8.5, "orange", True, mono=True, anchor="m")
        d.text(6.75, y + 0.13, "%.2f mW" % pw, 8.5, "txt3", False, mono=True, align="r", anchor="m")
        y += 0.30
    d.text(0.12, 2.86, "tPD típico por compuerta (barra) y disipación por compuerta (mW). Valores de hojas de datos típicas.", 8.5, "txt3")
    d.save("families")

    d = Draw(6.6, 2.6, bg="panel")
    d.text(0.12, 0.06, "ÁRBOL DE LA SERIE 74XX: SUBFAMILIAS Y COMPATIBILIDAD DE PINES", 9.5, "green", True, mono=True)
    d.rrect(2.55, 0.45, 1.5, 0.42, fill="card2", line="green", lw=1.5, r=0.06)
    d.text(3.30, 0.66, "TTL 74XX", 10, "green", True, mono=True, align="c", anchor="m")
    subs = ["74L · 74H (históricos)", "74LS · 74ALS (bajo consumo)", "74S · 74F (alta velocidad)",
            "74HC · 74HCT (CMOS compatible)", "74AHC · 74LVC (modernos, 3.3 V)"]
    for i, s in enumerate(subs):
        yy = 1.05 + i * 0.28
        d.line(3.30, 0.87, 3.30, yy + 0.12, "line2", 1.0)
        d.line(3.30, yy + 0.12, 3.85, yy + 0.12, "line2", 1.0)
        d.rrect(3.90, yy, 2.55, 0.24, fill="card", line="line", lw=0.8, r=0.04)
        d.text(4.05, yy + 0.12, s, 8.8, "txt2", False, mono=True, anchor="m")
    d.text(0.12, 2.42, "Sufijo por encapsulado: 74LS00N (DIP), 74LS00D (SOIC), 74LS00PW (TSSOP).", 9, "txt3")
    d.save("family_tree")


def misc():
    # tabla de verdad genérica (imagen decorativa de fondo de sección)
    d = Draw(4.2, 2.4, bg="panel")
    d.text(0.12, 0.06, "TABLA DE VERDAD: FORMA CANÓNICA", 9.5, "yellow", True, mono=True)
    hdr = ["A", "B", "Y"]
    for i, h in enumerate(hdr):
        d.rect(0.45 + i * 0.75, 0.45, 0.75, 0.32, fill="yellow")
        d.text(0.825 + i * 0.75, 0.61, h, 9.5, "bg", True, mono=True, align="c", anchor="m")
    rows = [("0", "0", "0"), ("0", "1", "1"), ("1", "0", "1"), ("1", "1", "1")]
    for r, row in enumerate(rows):
        for i, c in enumerate(row):
            yy = 0.77 + r * 0.30
            d.rect(0.45 + i * 0.75, yy, 0.75, 0.30, fill=("panel2" if r % 2 == 0 else "card"),
                   line=None)
            d.text(0.825 + i * 0.75, yy + 0.15, c, 9, "txt", False, mono=True, align="c", anchor="m")
    d.text(0.45, 2.02, "Y = A'B + AB' + AB  ≡  A + B", 10, "yellow", True, mono=True)
    d.save("truth_example")

    # tarjeta / pesos binarios
    d = Draw(6.2, 1.8, bg="panel")
    d.text(0.12, 0.06, "PESOS BINARIOS EN UNA PALABRA DE 8 BITS", 9.5, "cyan", True, mono=True)
    weights = [128, 64, 32, 16, 8, 4, 2, 1]
    for i, wt in enumerate(weights):
        x = 0.40 + i * 0.70
        d.rrect(x, 0.42, 0.60, 0.52, fill=("cyan" if wt >= 16 else "card2"), line="cyan", lw=1.2, r=0.05)
        d.text(x + 0.30, 0.68, str(wt), 8.5, "bg" if wt >= 16 else "txt", True, mono=True, align="c", anchor="m")
        d.text(x + 0.30, 1.02, "b%d" % (7 - i), 8, "txt3", False, mono=True, align="c")
    d.text(0.40, 1.34, "Ejemplo: 1011 0011₂ = 128 + 32 + 16 + 2 + 1 = 179₁₀   ·   Bit 7 = MSB, Bit 0 = LSB", 9.5, "txt2", False, mono=True)
    d.save("binary_weights")

    # karnaugh
    d = Draw(4.4, 2.8, bg="panel")
    d.text(0.12, 0.06, "MAPA DE KARNAUGH 4x4 Y AGRUPAMIENTOS", 9.5, "orange", True, mono=True)
    cols = ["00", "01", "11", "10"]
    for i, cl in enumerate(cols):
        d.text(0.75 + i * 0.80, 0.42, cl, 9, "txt2", True, mono=True, align="c")
    for j, rw in enumerate(cols):
        d.text(0.48, 0.72 + j * 0.42 + 0.20, rw, 9, "txt2", True, mono=True, align="c", anchor="m")
    grid = [["1", "1", "0", "0"], ["0", "1", "1", "0"], ["0", "1", "1", "0"], ["0", "0", "0", "0"]]
    for j, row in enumerate(grid):
        for i, val in enumerate(row):
            xx = 0.75 + i * 0.80
            yy = 0.62 + j * 0.42
            d.rect(xx, yy, 0.80, 0.42, fill=("card2" if val == "1" else "card"), line="line2", lw=0.9)
            d.text(xx + 0.40, yy + 0.21, val, 10, "cyan" if val == "1" else "txt3", True, mono=True, align="c", anchor="m")
    # grupo 2x2 y grupo 2x1
    d.rrect(1.55, 0.62, 1.60, 1.26, fill=None, line="green", lw=2.0, r=0.10)
    d.rrect(2.35, 1.88, 0.80, 0.42, fill=None, line="orange", lw=2.0, r=0.10)
    d.text(0.30, 2.32, "Grupo de 4 unos → elimina 2 variables (B).  Grupo de 2 → elimina 1 variable.", 8.8, "txt3")
    d.save("kmap")

    # NAND universal
    d = Draw(6.4, 2.3, bg="panel")
    d.text(0.12, 0.06, "NAND COMO COMPUERTA UNIVERSAL (7400)", 9.5, "green", True, mono=True)
    # NOT
    draw_gate(d, "nand", 0.55, 0.55, 0.80, 0.50, accent="green", labels=("A", "A"), out="A'", lw=1.3)
    d.text(1.05, 1.16, "NOT", 9.5, "green", True, mono=True, align="c")
    # AND
    draw_gate(d, "nand", 2.55, 0.50, 0.80, 0.50, accent="green", labels=("A", "B"), out="", lw=1.3)
    draw_gate(d, "not", 3.75, 0.58, 0.42, 0.34, accent="green", labels=("", ""), out="A·B" if False else "Y", lw=1.3, two_in=False)
    d.line(3.35, 0.75, 3.75, 0.75, "txt2", 1.2)
    d.text(3.20, 1.16, "AND", 9.5, "green", True, mono=True, align="c")
    # OR
    draw_gate(d, "nand", 5.05, 0.45, 0.80, 0.42, accent="green", labels=("A", "A"), out="", lw=1.3)
    draw_gate(d, "nand", 5.05, 0.95, 0.80, 0.42, accent="green", labels=("B", "B"), out="", lw=1.3)
    draw_gate(d, "nand", 6.30, 0.70, 0.80, 0.45, accent="green", labels=("", ""), out="A+B", lw=1.3)
    d.line(5.85, 0.66, 6.10, 0.66, "txt2", 1.2)
    d.line(6.10, 0.66, 6.10, 0.92, "txt2", 1.2)
    d.line(6.10, 0.92, 6.30, 0.92, "txt2", 1.2)
    d.line(5.85, 1.16, 6.10, 1.16, "txt2", 1.2)
    d.line(6.10, 1.16, 6.10, 0.92, "txt2", 1.2)
    d.text(6.35, 1.30, "OR", 9.5, "green", True, mono=True, align="c")
    d.text(0.12, 2.02, "Con solo NAND (o NOR) se construye cualquier función lógica: AND = NAND + inversor, OR = NAND con entradas invertidas.", 8.8, "txt3")
    d.save("nand_universal")

    # álgebra de Boole / De Morgan
    d = Draw(6.4, 2.6, bg="panel")
    d.text(0.12, 0.06, "LEYES DE DE MORGAN Y PROPIEDADES DEL ÁLGEBRA DE BOOLE", 9.5, "blue", True, mono=True)
    rules = [("(A · B)' = A' + B'", "El complemento de un producto es la suma de los complementos."),
             ("(A + B)' = A' · B'", "El complemento de una suma es el producto de los complementos."),
             ("A + A'B = A + B", "Absorción: permite simplificar y ahorrar compuertas."),
             ("A·B + A·C = A(B + C)", "Factorización: reduce el número de integrados."),
             ("A + 0 = A  ·  A · 1 = A", "Elementos neutros de la suma y el producto lógico."),
             ("A + A' = 1  ·  A · A' = 0", "Complementación: base del principio de los bloques de conmutación.")]
    y = 0.45
    for a, b in rules:
        d.text(0.30, y, a, 10, "blue", True, mono=True)
        d.text(2.75, y + 0.02, b, 9, "txt3")
        y += 0.36
    d.save("de_morgan")

    # CMOS
    d = Draw(5.4, 2.5, bg="panel")
    d.text(0.12, 0.06, "ESTRUCTURA CMOS: PAR COMPLEMENTARIO NMOS / PMOS", 9.5, "teal", True, mono=True)
    d.text(0.30, 0.45, "VDD (+3.3 V … +5 V)", 9, "red", False, mono=True)
    d.line(0.30, 0.68, 4.45, 0.68, "red", 1.4)
    d.rrect(2.10, 0.80, 0.95, 0.45, fill="card2", line="teal", lw=1.4, r=0.05)
    d.text(2.57, 1.02, "PMOS", 9, "teal", True, mono=True, align="c", anchor="m")
    d.line(2.57, 0.68, 2.57, 0.80, "line2", 1.2)
    d.line(2.57, 1.25, 2.57, 1.55, "line2", 1.2)
    d.rrect(2.10, 1.55, 0.95, 0.45, fill="card2", line="pink", lw=1.4, r=0.05)
    d.text(2.57, 1.77, "NMOS", 9, "pink", True, mono=True, align="c", anchor="m")
    d.line(2.57, 2.00, 2.57, 2.25, "line2", 1.2)
    d.line(0.30, 2.25, 4.45, 2.25, "txt3", 1.4)
    d.line(1.20, 1.00, 1.95, 1.00, "cyan", 1.3); d.text(1.15, 1.00, "VIN", 9, "cyan", True, mono=True, align="r", anchor="m")
    d.line(1.20, 1.77, 1.95, 1.77, "cyan", 1.3); d.text(1.15, 1.77, "VIN", 9, "cyan", True, mono=True, align="r", anchor="m")
    d.line(3.05, 1.40, 3.90, 1.40, "green", 1.3); d.text(3.95, 1.40, "VOUT", 9, "green", True, mono=True, anchor="m")
    d.text(0.30, 2.32, "Solo circula corriente durante la conmutación → consumo casi nulo en reposo (µW).", 8.8, "txt3")
    d.save("cmos")

    # fabricación
    d = Draw(6.4, 2.1, bg="panel")
    d.text(0.12, 0.06, "DEL SILICIO AL CIRCUITO IMPRESO", 9.5, "purple", True, mono=True)
    steps = [("Oblea de silicio", "Crecimiento y corte del lingote"), ("Litografía", "Fotolitos y grabado por capas"),
             ("Oblea con dies", "Cientos de circuitos por oblea"), ("Encapsulado DIP/SOIC", "Wire bonding y sellado"),
             ("PCB / protoboard", "Soldadura y montaje final")]
    for i, (t, s) in enumerate(steps):
        x = 0.25 + i * 1.25
        d.rrect(x, 0.50, 1.10, 0.62, fill="card2", line="purple", lw=1.2, r=0.06)
        d.text(x + 0.55, 0.68, t, 8.5, "purple", True, mono=True, align="c")
        d.text(x + 0.55, 0.95, s, 7.8, "txt3", False, mono=True, align="c")
        if i < 4:
            d.arrow(x + 1.11, 0.81, x + 1.24, 0.81, "line2", 1.2)
    d.text(0.25, 1.35, "El mismo dato de 1970 sigue vigente: escalar el transistor reduce tamaño, costo y consumo,", 9, "txt3")
    d.text(0.25, 1.58, "pero aumenta la sensibilidad a ESD y exige 5 V (o 3.3 V) muy estables y bien desacoplados.", 9, "txt3")
    d.save("fabrication")

    # lógica combinacional vs secuencial
    d = Draw(6.0, 2.3, bg="panel")
    d.text(0.12, 0.06, "COMBINACIONAL vs SECUENCIAL", 9.5, "blue", True, mono=True)
    d.rrect(0.35, 0.55, 2.45, 0.85, fill="card2", line="cyan", lw=1.4, r=0.06)
    d.text(1.57, 0.72, "CIRCUITO COMBINACIONAL", 9, "cyan", True, mono=True, align="c")
    d.text(1.57, 0.98, "Y depende SOLO de las entradas actuales", 8.6, "txt3", False, mono=True, align="c")
    d.text(1.57, 1.20, "Ej.: 7400, 7408, 7486, 74138", 8.6, "txt2", False, mono=True, align="c")
    d.rrect(3.20, 0.55, 2.45, 0.85, fill="card2", line="indigo", lw=1.4, r=0.06)
    d.text(4.42, 0.72, "CIRCUITO SECUENCIAL", 9, "indigo", True, mono=True, align="c")
    d.text(4.42, 0.98, "La salida depende de entradas Y del estado previo", 8.6, "txt3", False, mono=True, align="c")
    d.text(4.42, 1.20, "Ej.: 7474, 74161, 74194, 74164", 8.6, "txt2", False, mono=True, align="c")
    d.arrow(2.85, 0.97, 3.15, 0.97, "line2", 1.3)
    d.text(0.35, 1.55, "La retroalimentación (memoria) es la diferencia esencial: sin reloj no hay estado, y sin estado no hay contador ni memoria.", 9, "txt3")
    d.text(0.35, 1.85, "En el laboratorio: el combinacional responde al instante; el secuencial cambia solo en el flanco de reloj.", 9, "txt3")
    d.save("comb_vs_seq")

    # probador lógico
    d = Draw(5.4, 2.3, bg="panel")
    d.text(0.12, 0.06, "PUNTAS LÓGICAS Y DIAGNÓSTICO RÁPIDO", 9.5, "orange", True, mono=True)
    d.rrect(1.20, 0.50, 0.70, 1.30, fill="card2", line="orange", lw=1.4, r=0.08)
    d.text(1.55, 0.70, "LED", 8.5, "red", True, mono=True, align="c")
    d.text(1.55, 0.95, "LED", 8.5, "green", True, mono=True, align="c")
    d.text(1.55, 1.20, "LED", 8.5, "yellow", True, mono=True, align="c")
    d.poly([(1.55, 1.80), (1.55, 2.05)], line="orange", lw=1.6)
    d.line(1.55, 2.05, 1.55, 2.20, "txt2", 1.6)
    d.text(2.05, 0.62, "Rojo = nivel BAJO (0)", 9, "txt2")
    d.text(2.05, 0.94, "Verde = nivel ALTO (1)", 9, "txt2")
    d.text(2.05, 1.26, "Ámbar = pulso / indeterminado", 9, "txt2")
    d.text(2.05, 1.58, "Pitido continuo = corto o pin sin contacto", 9, "txt2")
    d.text(0.30, 2.02, "Antes de medir: verificar GND y VCC en los pines 7 y 14, después seguir la señal de entrada a salida.", 8.8, "txt3")
    d.save("probe")

    # memoria
    d = Draw(6.2, 2.6, bg="panel")
    d.text(0.12, 0.06, "MEMORIAS Y DISPOSITIVOS RELACIONADOS (FAMILIA 74XX Y 74LS)", 9.5, "yellow", True, mono=True)
    rows = [("74LS189", "RAM estática 64 bits (16×4)", "Escritura/lectura por dirección"),
            ("74LS288 / 74LS289", "PROM 32×8 / 256×4", "Memoria fija programable"),
            ("74LS670", "Registro de 4×4 (banco)", "Escritura y lectura independientes"),
            ("74LS373 / 74LS374", "Latch / flip-flop octal", "Puertos y buses de datos"),
            ("74LS245", "Transceptor octal de bus", "Dirección de bus con OE"),
            ("74LS688", "Comparador de 8 bits", "Direcciones de memoria")]
    y = 0.45
    for a, b, c in rows:
        d.text(0.28, y, a, 9, "yellow", True, mono=True)
        d.text(1.95, y, b, 9, "txt2", False, mono=True)
        d.text(4.35, y, c, 8.8, "txt3")
        y += 0.33
    d.save("memory")

    # flujo de diseño
    d = Draw(6.4, 2.4, bg="panel")
    d.text(0.12, 0.06, "FLUJO DE DISEÑO DIGITAL: DEL ENUNCIADO AL CIRCUITO", 9.5, "green", True, mono=True)
    steps = [("1. Especificar", "Entradas, salidas y comportamiento"),
             ("2. Tabla de verdad", "Todas las combinaciones posibles"),
             ("3. Simplificar", "Boole / Karnaugh / De Morgan"),
             ("4. Elegir chips", "7400, 7408, 7486, 74138…"),
             ("5. Simular", "Logisim, Multisim, Tinkercad"),
             ("6. Montar y medir", "Protoboard, punta lógica, osciloscopio")]
    for i, (a, b) in enumerate(steps):
        col, row = i % 3, i // 3
        x = 0.28 + col * 2.10
        y = 0.45 + row * 0.95
        d.rrect(x, y, 1.90, 0.78, fill="card2", line="green", lw=1.2, r=0.06)
        d.text(x + 0.14, y + 0.10, a, 9, "green", True, mono=True)
        d.text(x + 0.14, y + 0.34, b, 8.3, "txt3", False, mono=True)
    d.text(0.28, 2.24, "Documentar cada paso evita el error más común en el laboratorio: cablear sin haber simplificado la función.", 8.8, "txt3")
    d.save("design_flow")

    # protoboard
    d = Draw(5.6, 2.6, bg="panel")
    d.text(0.12, 0.06, "MONTAJE EN PROTOBOARD CON 74LS00 Y LEDs", 9.5, "cyan", True, mono=True)
    d.rrect(0.30, 0.50, 4.10, 1.85, fill="card", line="line2", lw=1.3, r=0.06)
    for i in range(2):
        d.line(0.40, 0.66 + i * 1.55, 4.30, 0.66 + i * 1.55, "red" if i == 0 else "txt3", 2.2)
        d.line(0.40, 0.80 + i * 1.55, 4.30, 0.80 + i * 1.55, "blue" if i == 0 else "txt3", 2.2)
    d.rect(0.55, 1.15, 1.70, 0.90, fill="card2", line="cyan", lw=1.3)
    d.text(1.40, 1.60, "74LS00", 9, "cyan", True, mono=True, align="c", anchor="m")
    for k, col in enumerate(("green", "green", "red")):
        d.circle(2.85 + k * 0.40, 1.15, 0.09, fill=col)
        d.rrect(2.76 + k * 0.40, 1.28, 0.18, 0.30, fill="card2", line="line2", lw=0.8, r=0.02)
    d.text(3.60, 1.05, "LEDs de\nsalida", 8.5, "txt3", False, mono=True)
    d.text(2.85, 1.62, "330 Ω", 8.5, "txt3", False, mono=True)
    d.text(0.30, 2.42, "Regla práctica: un chip por franja, alimentación primero, y NUNCA dejar entradas CMOS al aire.", 8.8, "txt3")
    d.save("breadboard")


def hero_sections():
    """Ilustraciones grandes para las portadas de sección."""
    specs = [("sec_fund", "cyan", "01"), ("sec_gates", "orange", "02"),
             ("sec_data", "purple", "03"), ("sec_apps", "green", "04"),
             ("sec_lab", "pink", "05"), ("sec_rep", "blue", "06")]
    for name, acc, num in specs:
        d = Draw(4.2, 4.2)
        d.blob(2.1, 2.1, 1.9, acc, 60)
        d.circle(2.1, 2.1, 1.45, fill=None, line=acc, lw=1.2)
        d.circle(2.1, 2.1, 1.10, fill=None, line=acc, lw=0.8)
        for i in range(8):
            ang = math.pi * 2 * i / 8.0
            d.circle(2.1 + 1.45 * math.cos(ang), 2.1 + 1.45 * math.sin(ang), 0.055, fill=acc)
        d.text(2.1, 2.1, num, 60, acc, True, mono=True, align="c", anchor="m")
        d.text(2.1, 3.35, "SERIE 74XX", 12, "txt3", True, mono=True, align="c")
        d.save(name)


def build_all():
    gates(); waveform_set(); pinouts(); adders(); mux_demux(); sequential()
    seven_seg(); electrical(); families(); misc(); hero_sections()
    files = sorted(os.listdir(GEN))
    return files


if __name__ == "__main__":
    fs = build_all()
    print("Diagramas generados:", len(fs))
    for f in fs:
        print("  ", f)
