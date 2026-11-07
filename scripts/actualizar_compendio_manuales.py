# -*- coding: utf-8 -*-
"""
Genera el Compendio Oficial de Estudio a partir de los 15 manuales PYME en data/raw/
Asegura codificación UTF-8 pura, tablas de metadatos e índices navegables.
"""

import os
import glob

BASE_DIR = os.path.dirname(__file__)
RAW_DIR = os.path.join(BASE_DIR, "..", "data", "raw")
OUT_DIR = os.path.join(BASE_DIR, "..", "material_estudio")
OUT_MANUALES = os.path.join(OUT_DIR, "15_manuales_tecnicos")
os.makedirs(OUT_MANUALES, exist_ok=True)

archivos = sorted(glob.glob(os.path.join(RAW_DIR, "DOC-*.md")))
print(f"Encontrados {len(archivos)} manuales en {RAW_DIR}")

compendio_lines = [
    "# COMPENDIO OFICIAL: LOS 15 MANUALES TÉCNICOS DE SOPORTE TIC PARA PYME\n",
    "**Proyecto:** Triaje Automático de Solicitudes de Soporte Tecnológico para una PYME (Caso N.º 03 · Grupo 3)  \n",
    "**Seminario de Titulación:** Ingeniería de Software con IA Generativa — UNIANDES (2026)  \n",
    "**Docente Evaluador:** Heyler Fabio Guaza (Ing. Informático · Mg. en Ciberseguridad · OPD · Abogado)  \n",
    "**Repositorio Oficial:** https://github.com/cgmorales12/TriajeSoporte-grupo-3  \n",
    "**URL en Producción:** https://triajesoporte-grupo-3.onrender.com  \n\n",
    "---\n\n",
    "## Índice General de Manuales Técnicos (Base de Conocimiento RAG)\n\n"
]

manuales_data = []
for ruta in archivos:
    with open(ruta, "r", encoding="utf-8") as f:
        contenido = f.read()
    
    nombre_base = os.path.basename(ruta)
    doc_id = nombre_base.split("_")[0]
    
    # Extraer título de la primera línea
    lineas = contenido.strip().split("\n")
    titulo_linea = lineas[0].replace("#", "").strip()
    
    compendio_lines.append(f"- **{doc_id}**: {titulo_linea}\n")
    manuales_data.append((doc_id, nombre_base, titulo_linea, contenido))
    
    # Copiar también a 15_manuales_tecnicos
    ruta_indiv = os.path.join(OUT_MANUALES, nombre_base)
    with open(ruta_indiv, "w", encoding="utf-8") as f_out:
        f_out.write(contenido)

compendio_lines.append("\n---\n\n")

for doc_id, nombre_base, titulo_linea, contenido in manuales_data:
    compendio_lines.append(f"{contenido}\n\n---\n\n")

compendio_path = os.path.join(OUT_DIR, "00_COMPENDIO_15_MANUALES_OFICIALES.md")
with open(compendio_path, "w", encoding="utf-8") as f:
    f.writelines(compendio_lines)

print(f"✅ Compendio generado con éxito en: {compendio_path}")
print(f"✅ {len(manuales_data)} manuales individuales sincronizados en: {OUT_MANUALES}")
