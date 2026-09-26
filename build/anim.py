# -*- coding: utf-8 -*-
"""Transiciones de diapositiva y animaciones de entrada (timing OOXML nativo)."""
from lxml import etree

NSMAP = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}
P = NSMAP["p"]
_MC = "http://schemas.openxmlformats.org/markup-compatibility/2006"
_P14 = "http://schemas.microsoft.com/office/powerpoint/2010/main"

# Prefijos estables al serializar (PowerPoint rechaza ns0/ns1 en algunos casos).
etree.register_namespace("a", NSMAP["a"])
etree.register_namespace("p", P)
etree.register_namespace("r", NSMAP["r"])
etree.register_namespace("mc", _MC)
etree.register_namespace("p14", _P14)


def _q(tag):
    return "{%s}%s" % (P, tag)


TRANSITIONS = {
    "fade": '<p:transition xmlns:p="%s" spd="med" advClick="1"><p:fade/></p:transition>' % P,
    "wipe": '<p:transition xmlns:p="%s" spd="med" advClick="1"><p:wipe dir="l"/></p:transition>' % P,
    "push": '<p:transition xmlns:p="%s" spd="med" advClick="1"><p:push dir="u"/></p:transition>' % P,
    "cover": '<p:transition xmlns:p="%s" spd="med" advClick="1"><p:cover dir="d"/></p:transition>' % P,
    "split": '<p:transition xmlns:p="%s" spd="med" advClick="1"><p:split orient="horz" dir="out"/></p:transition>' % P,
    # p14:switch no está en el esquema de p:transition. Sin AlternateContent
    # y mc:Ignorable, PowerPoint pide reparar el archivo al abrirlo.
    "zoom": (
        '<p:transition xmlns:p="%s" xmlns:mc="%s" xmlns:p14="%s" spd="med" advClick="1">'
        '<mc:AlternateContent>'
        '<mc:Choice Requires="p14"><p14:switch/></mc:Choice>'
        '<mc:Fallback><p:fade/></mc:Fallback>'
        '</mc:AlternateContent></p:transition>' % (P, _MC, _P14)
    ),
}


def _declare_p14(slide):
    """Declara mc/p14 en la raíz y marca p14 como ignorable."""
    sld = slide._element
    nsmap = dict(sld.nsmap)
    nsmap["mc"] = _MC
    nsmap["p14"] = _P14
    ign_attr = "{%s}Ignorable" % _MC
    parts = (sld.get(ign_attr) or "").split()
    if "p14" not in parts:
        parts.append("p14")
    new = etree.Element(sld.tag, nsmap=nsmap)
    for key, val in sld.attrib.items():
        if key != ign_attr:
            new.set(key, val)
    new.set(ign_attr, " ".join(p for p in parts if p))
    for child in list(sld):
        new.append(child)
    parent = sld.getparent()
    if parent is not None:
        parent.replace(sld, new)
    slide._element = new
    part = getattr(slide, "part", None)
    if part is not None:
        part._element = new


def set_transition(slide, kind="fade"):
    """Inserta la transición en el orden correcto del esquema (después de clrMapOvr)."""
    xml = TRANSITIONS.get(kind, TRANSITIONS["fade"])
    node = etree.fromstring(xml)
    if kind == "zoom" or node.find(".//{%s}switch" % _P14) is not None:
        _declare_p14(slide)
    sld = slide._element
    clr = sld.find(_q("clrMapOvr"))
    if clr is not None:
        clr.addnext(node)
    else:
        cSld = sld.find(_q("cSld"))
        cSld.addnext(node)


# ------------------------------------------------------------------ animaciones
_EFFECT = {
    # efecto -> (animEffect filter, animación adicional)
    # {i} e {i2} son ids de cTn distintos: PowerPoint exige que sean únicos.
    "fade": ('<p:animEffect transition="in" filter="fade"><p:cBhvr><p:cTn id="{i}" dur="{d}"/>'
             '<p:tgtEl><p:spTgt spid="{s}"/></p:tgtEl></p:cBhvr></p:animEffect>', None),
    "rise": ('<p:animEffect transition="in" filter="fade"><p:cBhvr><p:cTn id="{i}" dur="{d}"/>'
             '<p:tgtEl><p:spTgt spid="{s}"/></p:tgtEl></p:cBhvr></p:animEffect>',
             '<p:anim calcmode="lin" valueType="num"><p:cBhvr additive="base"><p:cTn id="{i}" dur="{d}" '
             'fill="hold"/><p:tgtEl><p:spTgt spid="{s}"/></p:tgtEl><p:attrNameLst><p:attrName>ppt_y</p:attrName>'
             '</p:attrNameLst></p:cBhvr><p:tavLst><p:tav tm="0"><p:val><p:fltVal val="0.06"/></p:val></p:tav>'
             '<p:tav tm="100000"><p:val><p:fltVal val="0"/></p:val></p:tav></p:tavLst></p:anim>'),
    "wipe": ('<p:animEffect transition="in" filter="wipe(left)"><p:cBhvr><p:cTn id="{i}" dur="{d}"/>'
             '<p:tgtEl><p:spTgt spid="{s}"/></p:tgtEl></p:cBhvr></p:animEffect>'
             '<p:animEffect transition="in" filter="fade"><p:cBhvr><p:cTn id="{i2}" dur="{d}"/>'
             '<p:tgtEl><p:spTgt spid="{s}"/></p:tgtEl></p:cBhvr></p:animEffect>', None),
    "zoom": ('<p:animEffect transition="in" filter="fade"><p:cBhvr><p:cTn id="{i}" dur="{d}"/>'
             '<p:tgtEl><p:spTgt spid="{s}"/></p:tgtEl></p:cBhvr></p:animEffect>'
             '<p:animScale><p:cBhvr><p:cTn id="{i2}" dur="{d}" fill="hold"/>'
             '<p:tgtEl><p:spTgt spid="{s}"/></p:tgtEl></p:cBhvr><p:from x="90000" y="90000"/>'
             '<p:to x="100000" y="100000"/></p:animScale>', None),
    "dissolve": ('<p:animEffect transition="in" filter="dissolve"><p:cBhvr><p:cTn id="{i}" dur="{d}"/>'
                 '<p:tgtEl><p:spTgt spid="{s}"/></p:tgtEl></p:cBhvr></p:animEffect>', None),
}


def add_animation(slide, groups, base_dur=420):
    """groups: lista de dicts {ids:[shape_id...], effect, delay, trigger}.

    El primer grupo arranca automáticamente al entrar la diapositiva; los demás
    avanzan con clic (o automáticamente si trigger == 'auto').
    """
    groups = [g for g in groups if g.get("ids")]
    if not groups:
        return
    nid = [1]

    def nxt():
        nid[0] += 1
        return nid[0]

    seq_id = nxt()

    def effect_xml(effect, spid, start_delay, dur):
        tpl, extra = _EFFECT.get(effect, _EFFECT["fade"])
        out = tpl.format(i=nxt(), i2=nxt(), s=spid, d=dur)
        out = ('<p:set><p:cBhvr><p:cTn id="%d" dur="1" fill="hold">'
               '<p:stCondLst><p:cond delay="0"/></p:stCondLst></p:cTn>'
               '<p:tgtEl><p:spTgt spid="%d"/></p:tgtEl>'
               '<p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst>'
               '</p:cBhvr><p:to><p:strVal val="visible"/></p:to></p:set>' % (nxt(), spid)) + out
        if extra:
            out += extra.format(i=nxt(), s=spid, d=dur)
        return ('<p:par><p:cTn id="%d" fill="hold"><p:stCondLst><p:cond delay="%d"/></p:stCondLst>'
                '<p:childTnLst>%s</p:childTnLst></p:cTn></p:par>' % (nxt(), start_delay, out))

    seq_children = []
    for i, g in enumerate(groups):
        effect = g.get("effect", "fade")
        delay = int(g.get("delay", 110))
        trigger = g.get("trigger", "click")
        inner = []
        for j, spid in enumerate(g["ids"]):
            inner.append(effect_xml(effect, spid, j * delay, base_dur))
        inner_xml = "".join(inner)
        if i == 0:
            cond = '<p:cond delay="0"/>'
        elif trigger == "auto":
            cond = '<p:cond delay="%d"/>' % int(g.get("wait", 320))
        else:
            cond = '<p:cond delay="indefinite"/>'   # avanza con el clic del presentador
        seq_children.append(
            '<p:par><p:cTn id="%d" fill="hold"><p:stCondLst>%s</p:stCondLst>'
            '<p:childTnLst><p:par><p:cTn id="%d" fill="hold"><p:stCondLst><p:cond delay="0"/>'
            '</p:stCondLst><p:childTnLst>%s</p:childTnLst></p:cTn></p:par></p:childTnLst>'
            '</p:cTn></p:par>' % (nxt(), cond, nxt(), inner_xml))

    timing = (
        '<p:timing xmlns:p="{p}" xmlns:a="{a}"><p:tnLst><p:par><p:cTn id="1" dur="indefinite" '
        'restart="never" nodeType="tmRoot"><p:childTnLst><p:seq concurrent="1" nextAc="seek">'
        '<p:cTn id="{seq}" dur="indefinite" nodeType="mainSeq"><p:childTnLst>{kids}</p:childTnLst></p:cTn>'
        '<p:prevCondLst><p:cond evt="onPrev" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:prevCondLst>'
        '<p:nextCondLst><p:cond evt="onNext" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:nextCondLst>'
        '</p:seq></p:childTnLst></p:cTn></p:par></p:tnLst></p:timing>'
    ).format(p=P, a=NSMAP["a"], seq=seq_id, kids="".join(seq_children))

    slide._element.append(etree.fromstring(timing))


def set_notes(slide, text):
    if not text:
        return
    tf = slide.notes_slide.notes_text_frame
    tf.text = text
    for p in tf.paragraphs:
        for r in p.runs:
            r.font.size = None
