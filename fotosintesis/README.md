# Reporte integrado: La fotosíntesis y su importancia para la transferencia de energía

## Entregable

| Archivo | Contenido |
|---|---|
| `../Reporte-Fotosintesis.docx` | **Reporte en texto**: secciones A–E de la guía, espacios marcados para las figuras 1–6, **infografía incrustada en la sección D.2**, 2 tablas y bibliografía en formato APA |
| `../Infografia-Fotosintesis.png` | **Infografía vertical** (estilo Canva): participación de los organismos autótrofos en las cadenas tróficas |

## Contenido del reporte

- **A. Introducción**: proceso de la fotosíntesis con precisión, ecuación general, historia del estudio, diagrama de correlación, fase luminosa, ciclo de Calvin y el cloroplasto como reactor.
- **Metodología**: investigación documental, diagramas propios, maqueta tridimensional, análisis comparativo y redacción formal.
- **B. Justificación**: transferencia de energía, captura de CO₂ y liberación de O₂, cada una con ejemplos claros.
- **C. Desarrollo**: estructura tridimensional del cloroplasto (con tabla de partes y funciones), procesos bioquímicos paso a paso (fase luminosa y ciclo de Calvin), participación del CO₂ y el O₂, evidencia fotográfica de la maqueta/modelo 3D (sustituir por la foto real) y video de 2 a 3 minutos con guion (pegar el enlace).
- **D. Resultados, análisis y conclusión**: tabla comparativa autótrofos vs. heterótrofos, análisis y conclusión. Infografía pendiente.
- **E. Bibliografía**: formato APA (7.ª edición).
- **Glosario**: 9 términos clave.

## Cómo regenerar el documento

```bash
cd fotosintesis
python3 gfx.py     # regenera los diagramas en assets/
python3 build.py   # genera ../Reporte-Fotosintesis.docx
```

Requiere `python-pptx`, `Pillow` y `python-docx`.
