#!/usr/bin/env python3
"""
Generador de Documentos Oficiales PDF desde los Manuales Técnicos en data/raw/
Proyecto: TecnoAula — Triaje Automático de Soporte para PYMEs (Caso 03 · Grupo 3 UNIANDES)
Genera 15 PDFs con diseño institucional limpio a partir de los archivos Markdown oficiales.
"""

import os
import re
import glob
import html
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.units import inch

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RAW_DIR = os.path.join(RAIZ, "data", "raw")
PDF_DIR = os.path.join(RAIZ, "data", "pdf")

os.makedirs(PDF_DIR, exist_ok=True)

def formatear_md_a_rl(texto: str) -> str:
    # Escapar entidades HTML básicas excepto lo que queramos formatear
    t = html.escape(texto)
    # Convertir **negrita** a <b>negrita</b>
    t = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', t)
    # Convertir *cursiva* a <i>cursiva</i>
    t = re.sub(r'\*(.*?)\*', r'<i>\1</i>', t)
    # Convertir `codigo` a <font face="Courier">\1</font>
    t = re.sub(r'`(.*?)`', r'<font face="Courier">\1</font>', t)
    return t

def generar_pdf_desde_md(ruta_md: str, ruta_pdf: str):
    with open(ruta_md, "r", encoding="utf-8") as f:
        lineas = f.readlines()

    doc = SimpleDocTemplate(
        ruta_pdf,
        pagesize=letter,
        rightMargin=45,
        leftMargin=45,
        topMargin=45,
        bottomMargin=45
    )

    styles = getSampleStyleSheet()

    estilo_titulo = ParagraphStyle(
        "TituloManual",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=18,
        textColor=colors.HexColor("#1e3a8a"),
        spaceAfter=10
    )

    estilo_subtitulo = ParagraphStyle(
        "SubtituloManual",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=14,
        textColor=colors.HexColor("#1e293b"),
        spaceBefore=8,
        spaceAfter=4
    )

    estilo_cuerpo = ParagraphStyle(
        "CuerpoManual",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor("#334155"),
        spaceAfter=5
    )

    estilo_meta = ParagraphStyle(
        "MetaManual",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#475569"),
        spaceAfter=3
    )

    story = []

    # Encabezado institucional
    encabezado_tabla = [
        [
            Paragraph("<b>TECNOAULA — SOPORTE TÉCNICO TI PARA PYMES</b>", ParagraphStyle("H1", fontName="Helvetica-Bold", fontSize=11, textColor=colors.HexColor("#1e3a8a"))),
            Paragraph("<b>ESTÁNDAR OPERATIVO 2026</b>", ParagraphStyle("H2", fontName="Helvetica-Bold", fontSize=9, textColor=colors.HexColor("#475569"), alignment=2))
        ]
    ]
    t_enc = Table(encabezado_tabla, colWidths=[340, 180])
    t_enc.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(t_enc)
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#2563eb"), spaceAfter=12))

    for linea in lineas:
        linea_str = linea.strip()
        if not linea_str:
            story.append(Spacer(1, 4))
            continue

        if linea_str.startswith("# "):
            titulo = formatear_md_a_rl(linea_str.replace("# ", "").strip())
            story.append(Paragraph(titulo, estilo_titulo))
        elif linea_str.startswith("## "):
            sub = formatear_md_a_rl(linea_str.replace("## ", "").strip())
            story.append(Paragraph(sub, estilo_subtitulo))
        elif linea_str.startswith("### "):
            paso = formatear_md_a_rl(linea_str.replace("### ", "").strip())
            story.append(Paragraph(f"<b>{paso}</b>", estilo_subtitulo))
        elif linea_str.startswith("**") and ("Categoría" in linea_str or "Vigencia" in linea_str or "Origen" in linea_str or "URL" in linea_str):
            meta_fmt = formatear_md_a_rl(linea_str)
            story.append(Paragraph(meta_fmt, estilo_meta))
        else:
            texto_fmt = formatear_md_a_rl(linea_str)
            story.append(Paragraph(texto_fmt, estilo_cuerpo))

    story.append(Spacer(1, 15))
    story.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor("#cbd5e1"), spaceAfter=6))
    story.append(Paragraph("TecnoAula · Caso N.º 03 · Grupo 3 UNIANDES | Documento Oficial de Consulta Técnica RAG", estilo_meta))

    doc.build(story)


def main():
    archivos_md = sorted(glob.glob(os.path.join(RAW_DIR, "DOC-*.md")))
    print(f"Generando {len(archivos_md)} PDFs desde {RAW_DIR} hacia {PDF_DIR}...")
    for ruta_md in archivos_md:
        nombre_base = os.path.basename(ruta_md).replace(".md", ".pdf")
        ruta_pdf = os.path.join(PDF_DIR, nombre_base)
        generar_pdf_desde_md(ruta_md, ruta_pdf)
        print(f"  [OK] {nombre_base}")
    print("\nTodos los PDFs oficiales de PYME fueron generados con éxito.")

if __name__ == "__main__":
    main()
