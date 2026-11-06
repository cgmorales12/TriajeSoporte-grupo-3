# -*- coding: utf-8 -*-
"""
Generador de Documento Word (.docx y .doc) para el Compendio de Directrices y Defensa
"""
import os
import shutil
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

RUTA_MD = os.path.join(os.path.dirname(__file__), "..", "material_estudio", "AUDITORIA_DIRECTRICES_Y_DEFENSA_CASO_03.md")
RUTA_DOCX = os.path.join(os.path.dirname(__file__), "..", "material_estudio", "AUDITORIA_DIRECTRICES_Y_DEFENSA_CASO_03.docx")
RUTA_DOC = os.path.join(os.path.dirname(__file__), "..", "material_estudio", "AUDITORIA_DIRECTRICES_Y_DEFENSA_CASO_03.doc")

def aplicar_sombreado_celda(celda, color_hex):
    shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    celda._tc.get_or_add_tcPr().append(shading)

def set_bordes_celda(celda):
    tcPr = celda._tc.get_or_add_tcPr()
    tcBorders = parse_xml(f'<w:tcBorders {nsdecls("w")}>'
                          f'<w:top w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
                          f'<w:left w:val="none"/>'
                          f'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
                          f'<w:right w:val="none"/>'
                          f'</w:tcBorders>')
    tcPr.append(tcBorders)

def generar_documento():
    doc = docx.Document()
    
    # Configuración de márgenes estándar (2.5 cm)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
        # Pie de página institucional
        footer = section.footer
        f_p = footer.paragraphs[0]
        f_p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        f_run = f_p.add_run("UNIANDES · Titulación Software con IA Generativa — Caso 03 Grupo 3")
        f_run.font.name = "Calibri"
        f_run.font.size = Pt(8.5)
        f_run.font.color.rgb = RGBColor(148, 163, 184)

    # Estilo base
    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Calibri'
    style_normal.font.size = Pt(11)
    style_normal.font.color.rgb = RGBColor(30, 41, 59)

    with open(RUTA_MD, "r", encoding="utf-8") as f:
        lineas = f.readlines()

    en_tabla = False
    filas_tabla = []

    def procesar_tabla(filas):
        if not filas:
            return
        
        datos = []
        for f in filas:
            f_clean = f.strip().strip("|")
            columnas = [c.strip() for c in f_clean.split("|")]
            datos.append(columnas)
            
        num_cols = max(len(r) for r in datos)
        # Normalizar filas
        datos_norm = []
        for r in datos:
            if len(r) < num_cols:
                r = r + [""] * (num_cols - len(r))
            datos_norm.append(r)
            
        table = doc.add_table(rows=len(datos_norm), cols=num_cols)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = True
        
        for idx_row, row_data in enumerate(datos_norm):
            is_header = (idx_row == 0)
            row = table.rows[idx_row]
            for idx_col, text in enumerate(row_data):
                cell = row.cells[idx_col]
                set_bordes_celda(cell)
                if is_header:
                    aplicar_sombreado_celda(cell, "1E3A8A")
                elif idx_row % 2 == 1:
                    aplicar_sombreado_celda(cell, "F8FAFC")
                else:
                    aplicar_sombreado_celda(cell, "FFFFFF")
                
                p = cell.paragraphs[0]
                p.paragraph_format.space_before = Pt(4)
                p.paragraph_format.space_after = Pt(4)
                p.paragraph_format.line_spacing = 1.15
                
                # Quitar formato markdown básico
                clean_text = text.replace("**", "").replace("<br>", "\n").replace("`", "")
                run = p.add_run(clean_text)
                run.font.name = "Calibri"
                if is_header:
                    run.bold = True
                    run.font.size = Pt(10)
                    run.font.color.rgb = RGBColor(255, 255, 255)
                else:
                    run.font.size = Pt(9.5)
                    run.font.color.rgb = RGBColor(30, 41, 59)
        
        p_space = doc.add_paragraph()
        p_space.paragraph_format.space_after = Pt(6)

    for linea in lineas:
        l = linea.rstrip()
        
        # Detección de tablas markdown
        if l.startswith("|") and "|" in l[1:]:
            if "---" in l:
                continue # separador de tabla
            en_tabla = True
            filas_tabla.append(l)
            continue
        else:
            if en_tabla:
                procesar_tabla(filas_tabla)
                en_tabla = False
                filas_tabla = []

        if not l.strip():
            continue

        # Encabezados
        if l.startswith("# "):
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(16)
            p.paragraph_format.space_after = Pt(6)
            run = p.add_run(l[2:].strip())
            run.font.name = "Calibri"
            run.font.size = Pt(18)
            run.bold = True
            run.font.color.rgb = RGBColor(30, 58, 138)
        elif l.startswith("## "):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(14)
            p.paragraph_format.space_after = Pt(4)
            run = p.add_run(l[3:].strip())
            run.font.name = "Calibri"
            run.font.size = Pt(14)
            run.bold = True
            run.font.color.rgb = RGBColor(14, 116, 144)
        elif l.startswith("### "):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(10)
            p.paragraph_format.space_after = Pt(3)
            run = p.add_run(l[4:].strip())
            run.font.name = "Calibri"
            run.font.size = Pt(12)
            run.bold = True
            run.font.color.rgb = RGBColor(15, 23, 42)
        elif l.startswith("#### "):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(8)
            p.paragraph_format.space_after = Pt(2)
            run = p.add_run(l[5:].strip())
            run.font.name = "Calibri"
            run.font.size = Pt(11)
            run.bold = True
            run.font.color.rgb = RGBColor(51, 65, 85)
        elif l.startswith("> "):
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Inches(0.4)
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(6)
            run = p.add_run(l[2:].strip().replace("**", "").replace("*", ""))
            run.italic = True
            run.font.size = Pt(10.5)
            run.font.color.rgb = RGBColor(71, 85, 105)
        elif l.startswith("* ") or l.startswith("- "):
            p = doc.add_paragraph(style='List Bullet')
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(2)
            texto = l[2:].strip()
            partes = texto.split("**")
            for idx, part in enumerate(partes):
                run = p.add_run(part.replace("`", ""))
                if idx % 2 == 1:
                    run.bold = True
                run.font.size = Pt(10.5)
        elif l.startswith("```"):
            continue
        elif l == "---":
            continue
        else:
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.line_spacing = 1.15
            partes = l.split("**")
            for idx, part in enumerate(partes):
                run = p.add_run(part.replace("`", "").replace("*", ""))
                if idx % 2 == 1:
                    run.bold = True
                run.font.size = Pt(11)

    if en_tabla:
        procesar_tabla(filas_tabla)

    doc.save(RUTA_DOCX)
    print(f"✅ Archivo generado: {RUTA_DOCX}")
    
    shutil.copyfile(RUTA_DOCX, RUTA_DOC)
    print(f"✅ Archivo copiado: {RUTA_DOC}")

if __name__ == "__main__":
    generar_documento()
