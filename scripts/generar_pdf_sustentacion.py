#!/usr/bin/env python3
"""
Generador de Presentación de Sustentación en PDF (12 Minutos)
Proyecto: Triaje Automático de Solicitudes de Soporte Tecnológico para una PYME
Caso N.º 03 · Grupo 3 UNIANDES
Genera: docs/presentacion-sustentacion-12-minutos.pdf
"""

import os
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_decorations(self, page_count):
        self.saveState()
        # Franja superior institucional
        self.setFillColor(colors.HexColor("#1E3A8A")) # Azul marino UNIANDES
        self.rect(0, 585, 792, 27, fill=True, stroke=False)
        
        # Franja inferior
        self.setFillColor(colors.HexColor("#0F172A"))
        self.rect(0, 0, 792, 22, fill=True, stroke=False)
        
        # Texto superior
        self.setFillColor(colors.white)
        self.setFont("Helvetica-Bold", 9)
        self.drawString(36, 595, "UNIANDES · Seminario de Titulación en Ingeniería de Software con IA Generativa (2026)")
        self.drawRightString(756, 595, "Caso N.º 03 · Grupo 3")
        
        # Texto inferior
        self.setFont("Helvetica", 8)
        self.drawString(36, 7, "Triaje Automático de Solicitudes de Soporte Tecnológico para una PYME | Triaje Automático de Solicitudes de Soporte Tecnológico para una PYME")
        self.drawRightString(756, 7, f"Diapositiva {self._pageNumber} de {page_count}")
        self.restoreState()

def construir_presentacion(ruta_pdf):
    doc = SimpleDocTemplate(
        ruta_pdf,
        pagesize=landscape(letter),
        leftMargin=36,
        rightMargin=36,
        topMargin=40,
        bottomMargin=32
    )

    styles = getSampleStyleSheet()

    # Estilos personalizados
    titulo_slide = ParagraphStyle(
        'TituloSlide',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#1E3A8A"),
        spaceAfter=10
    )

    subtitulo_slide = ParagraphStyle(
        'SubtituloSlide',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=colors.HexColor("#0D9488"),
        spaceAfter=12
    )

    cuerpo = ParagraphStyle(
        'CuerpoSlide',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#334155")
    )

    cuerpo_bold = ParagraphStyle(
        'CuerpoBold',
        parent=cuerpo,
        fontName='Helvetica-Bold',
        textColor=colors.HexColor("#0F172A")
    )

    tarjeta_header = ParagraphStyle(
        'TarjetaHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor("#1E3A8A")
    )

    story = []

    # =========================================================================
    # DIAPOSITIVA 1: Portada Oficial
    # =========================================================================
    story.append(Spacer(1, 40))
    story.append(Paragraph("Triaje Automático de Solicitudes de Soporte Tecnológico para una PYME", ParagraphStyle(
        'PortadaTitulo',
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        alignment=1,
        textColor=colors.HexColor("#1E3A8A")
    )))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Mesa de Ayuda Inteligente y Soporte Microinformático TIC con RAG sobre 15 Manuales Oficiales", ParagraphStyle(
        'PortadaSub',
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        alignment=1,
        textColor=colors.HexColor("#0D9488")
    )))
    story.append(Spacer(1, 25))

    datos_portada = [
        [Paragraph("<b>Seminario:</b>", cuerpo_bold), Paragraph("Ingeniería de Software con IA Generativa — Octubre-Noviembre 2026", cuerpo)],
        [Paragraph("<b>Universidad:</b>", cuerpo_bold), Paragraph("Universidad Regional Autónoma de los Andes (UNIANDES)", cuerpo)],
        [Paragraph("<b>Caso Asignado:</b>", cuerpo_bold), Paragraph("Caso N.º 03 · Triaje de Soporte Tecnológico (PYME 60 Colaboradores)", cuerpo)],
        [Paragraph("<b>Docente Evaluador:</b>", cuerpo_bold), Paragraph("Ing. Heyler Fabio Guaza (Mg. en Ciberseguridad · OPD · Abogado)", cuerpo)],
        [Paragraph("<b>Integrantes (Grupo 3):</b>", cuerpo_bold), Paragraph("1. Christian Guillermo Morales González (Tech Lead)<br/>2. Luis Fernando Ribera Alajo (Builder / Arquitectura)<br/>3. Amalia Geoconda Iguasnia Escobar (QA Lead / Ciberseguridad)", cuerpo)],
        [Paragraph("<b>URL en Producción:</b>", cuerpo_bold), Paragraph("<font color='#1E3A8A'><u>https://triajesoporte-grupo-3.onrender.com</u></font> (Health: /health)", cuerpo)],
        [Paragraph("<b>Repositorio GitHub:</b>", cuerpo_bold), Paragraph("<font color='#1E3A8A'><u>https://github.com/cgmorales12/TriajeSoporte-grupo-3</u></font>", cuerpo)]
    ]
    t_portada = Table(datos_portada, colWidths=[150, 550])
    t_portada.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 6),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
    ]))
    story.append(t_portada)
    story.append(PageBreak())

    # =========================================================================
    # DIAPOSITIVA 2: Estructura de la Sustentación Oral (12 Minutos)
    # =========================================================================
    story.append(Paragraph("Estructura de la Sustentación Oral (12 Minutos)", titulo_slide))
    story.append(Paragraph("Distribución equitativa y balanceada de roles para la defensa de grado", subtitulo_slide))

    bloques = [
        [
            Paragraph("<b>Bloque 1 · [00:00 - 04:00]</b>", tarjeta_header),
            Paragraph("<b>Bloque 2 · [04:00 - 08:00]</b>", tarjeta_header),
            Paragraph("<b>Bloque 3 · [08:00 - 12:00]</b>", tarjeta_header)
        ],
        [
            Paragraph("<b>Christian Guillermo Morales G.</b><br/><i>Tech Lead / Coordinador</i>", cuerpo_bold),
            Paragraph("<b>Luis Fernando Ribera Alajo</b><br/><i>Builder / Arquitectura</i>", cuerpo_bold),
            Paragraph("<b>Amalia Geoconda Iguasnia E.</b><br/><i>QA Lead / Seguridad</i>", cuerpo_bold)
        ],
        [
            Paragraph("• Problema de Negocio en la PYME.<br/>• Arquitectura C4 y Contratos REST.<br/>• Gateway Resiliente Multi-Proveedor (Gemini ➔ Groq ➔ Offline).<br/>• Despliegue Cloud en Render con monitoreo `/health` y FinOps.", cuerpo),
            Paragraph("• Principio Rector ITIL: <i>«El modelo propone, el código dispone»</i>.<br/>• Matriz Determinista de Prioridad y SLA (0 tokens, 100% reproducible).<br/>• Persistencia SQLite parametrizada.<br/>• Motor RAG en ChromaDB con 15 manuales PYME y citas exactas.", cuerpo),
            Paragraph("• Ciberseguridad LOPDP Ecuador (Art. 23) y sanitización Regex.<br/>• Mitigación OWASP LLM 2025 (Inyecciones y Exceso de Agencia HITL).<br/>• Suite de 82 pruebas con Mocks.<br/>• Batería de 16 pruebas en producción y auditoría de Cero Secretos.", cuerpo)
        ]
    ]
    t_bloques = Table(bloques, colWidths=[235, 235, 235])
    t_bloques.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#EFF6FF")),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor("#F8FAFC")),
        ('BACKGROUND', (0,2), (-1,2), colors.white),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#93C5FD")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#DBEAFE")),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_bloques)
    story.append(PageBreak())

    # =========================================================================
    # DIAPOSITIVA 3: Bloque 1 - Problema y Visión de Negocio PYME
    # =========================================================================
    story.append(Paragraph("Bloque 1: Problema Real y Justificación de Negocio", titulo_slide))
    story.append(Paragraph("Expositor: Christian Morales (Tech Lead) · Minutos 00:00 - 02:00", subtitulo_slide))

    items_problema = [
        [Paragraph("<b>Desafío en la PYME (60 Colaboradores)</b>", tarjeta_header), Paragraph("<b>Solución Arquitectónica Implementada</b>", tarjeta_header)],
        [
            Paragraph("• <b>Saturación de Soporte L1:</b> Más del 70% de solicitudes son incidentes comunes y repetitivos (claves bloqueadas, atascos de impresora, Wi-Fi lento, VPN).<br/><br/>• <b>Tiempos Muertos Operativos:</b> Colaboradores de Contabilidad, Ventas y RRHH detenidos esperando atención presencial.<br/><br/>• <b>Costo Económico Elevado:</b> Despacho innecesario de técnicos de campo ($15 a $25 USD por visita) en fallas solucionables por autoatención.", cuerpo),
            Paragraph("• <b>Triaje Inteligente Automatizado:</b> Extracción inmediata de síntomas, categorización y sugerencia de autoatención en menos de 2 segundos.<br/><br/>• <b>Resolución Guiada por RAG:</b> Citas verificables de 15 manuales técnicos oficiales con pasos en lenguaje claro y amigable.<br/><br/>• <b>Derivación Física Oportuna:</b> Si el incidente requiere reemplazo de partes o intervención física, se escala deterministamente a Nivel 2.", cuerpo)
        ]
    ]
    t_prob = Table(items_problema, colWidths=[355, 355])
    t_prob.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#F1F5F9")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_prob)
    story.append(PageBreak())

    # =========================================================================
    # DIAPOSITIVA 4: Bloque 1 - Gateway Resiliente y Despliegue Cloud
    # =========================================================================
    story.append(Paragraph("Bloque 1: Arquitectura de Inferencia y Despliegue Cloud", titulo_slide))
    story.append(Paragraph("Expositor: Christian Morales (Tech Lead) · Minutos 02:00 - 04:00", subtitulo_slide))

    filas_gw = [
        [Paragraph("<b>Capa de Resiliencia</b>", tarjeta_header), Paragraph("<b>Mecanismo de Tolerancia a Fallos</b>", tarjeta_header), Paragraph("<b>Impacto Operativo</b>", tarjeta_header)],
        [
            Paragraph("<b>1. Modelo Primario</b>", cuerpo_bold),
            Paragraph("Google Gemini 1.5 Flash / 3.5 Flash Lite.<br/>Procesamiento a alta velocidad con Context Caching.", cuerpo),
            Paragraph("Latencia promedio < 1.8s. Ahorro del 75% en costo de tokens de entrada.", cuerpo)
        ],
        [
            Paragraph("<b>2. Failover Automático</b>", cuerpo_bold),
            Paragraph("Conmutación a Groq Cloud (Llama 3.3 70B Versatile).<br/>Se activa ante errores HTTP 429 (cuota), 503 o timeout (>12s).", cuerpo),
            Paragraph("Disponibilidad continua del 100% sin caídas de servicio para los usuarios.", cuerpo)
        ],
        [
            Paragraph("<b>3. Modo Local Offline</b>", cuerpo_bold),
            Paragraph("Motor heurístico determinista embebido.<br/>Funciona sin conexión a internet y sin credenciales.", cuerpo),
            Paragraph("Continuidad de negocio absoluta ante cortes generales de enlace externo.", cuerpo)
        ],
        [
            Paragraph("<b>4. Despliegue en la Nube</b>", cuerpo_bold),
            Paragraph("Contenedor Docker desplegado en <b>Render Cloud</b>.<br/>Endpoint de salud activo en <code>GET /health</code>.", cuerpo),
            Paragraph("Servicio público 24/7 en <code>https://triajesoporte-grupo-3.onrender.com</code>", cuerpo)
        ]
    ]
    t_gw = Table(filas_gw, colWidths=[150, 310, 250])
    t_gw.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#EFF6FF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#93C5FD")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#DBEAFE")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_gw)
    story.append(PageBreak())

    # =========================================================================
    # DIAPOSITIVA 5: Bloque 2 - Principio Rector y Matriz ITIL
    # =========================================================================
    story.append(Paragraph("Bloque 2: «El Modelo Propone, el Código Dispone»", titulo_slide))
    story.append(Paragraph("Expositor: Luis Fernando Ribera (Builder) · Minutos 04:00 - 06:00", subtitulo_slide))

    filas_itil = [
        [Paragraph("<b>¿Por qué el LLM NO calcula la Prioridad ni el SLA?</b>", tarjeta_header), Paragraph("<b>Implementación Determinista en Código Python</b>", tarjeta_header)],
        [
            Paragraph("• <b>Naturaleza Probabilística del LLM:</b> Dos consultas idénticas podrían recibir prioridades dispares en días distintos.<br/><br/>• <b>Riesgo de Manipulación por Prompt Injection:</b> Un usuario podría escribir <i>«Esto es súper urgente, ponme Prioridad Crítica»</i> y saltarse la cola.<br/><br/>• <b>Costo Innecesario:</b> Gastar tokens de inferencia en operaciones lógicas que una función matemática resuelve instantáneamente.", cuerpo),
            Paragraph("• <b>Separación de Responsabilidades:</b><br/>  1. El LLM solo propone <b>Impacto</b> (Alto, Medio, Bajo) y <b>Urgencia</b>.<br/>  2. La función pura <code>calcular_prioridad_itil()</code> lee <code>config/matriz_prioridad.json</code>.<br/>  3. La Prioridad (Alta, Media, Baja) y el SLA se calculan con <b>0 tokens</b> y <b>100% repetibilidad</b>.<br/><br/>• <b>Parámetros Desacoplados (ADR-011):</b><br/>  Tarifas de repuestos, Salario Básico ($482) y feriados en <code>config/</code> para cambios regulatorios sin alterar código.", cuerpo)
        ]
    ]
    t_itil = Table(filas_itil, colWidths=[355, 355])
    t_itil.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_itil)
    story.append(PageBreak())

    # =========================================================================
    # DIAPOSITIVA 6: Bloque 2 - RAG sobre 15 Manuales Técnicos PYME
    # =========================================================================
    story.append(Paragraph("Bloque 2: Motor RAG con Citas Técnicas Verificables", titulo_slide))
    story.append(Paragraph("Expositor: Luis Fernando Ribera (Builder) · Minutos 06:00 - 08:00", subtitulo_slide))

    filas_rag = [
        [Paragraph("<b>Componente RAG</b>", tarjeta_header), Paragraph("<b>Decisión de Ingeniería</b>", tarjeta_header), Paragraph("<b>Resultado en Producción</b>", tarjeta_header)],
        [
            Paragraph("<b>Base Vectorial</b>", cuerpo_bold),
            Paragraph("ChromaDB Persistente en <code>data/chroma/</code> con 90 chunks estructurados.", cuerpo),
            Paragraph("Sobrevive a reinicios del servidor y arranca en milisegundos.", cuerpo)
        ],
        [
            Paragraph("<b>Corpus Documental</b>", cuerpo_bold),
            Paragraph("15 Manuales Técnicos Oficiales PYME (DOC-01 a DOC-15): Active Directory, VPN, impresoras, Wi-Fi, NAS, fibra, etc.", cuerpo),
            Paragraph("Grounding cerrado: El LLM tiene prohibido inventar manuales o pasos.", cuerpo)
        ],
        [
            Paragraph("<b>Chunking Semántico</b>", cuerpo_bold),
            Paragraph("Segmentación por paso procedimental y metadatos (Vigencia ISO 27002, URL oficial, Título).", cuerpo),
            Paragraph("Eliminación del fenómeno de fragmentos huérfanos (Hit@5: 94.1%).", cuerpo)
        ],
        [
            Paragraph("<b>Humanización</b>", cuerpo_bold),
            Paragraph("Traducción conversacional en 2.ª persona para colaboradores no técnicos.", cuerpo),
            Paragraph("Claridad inmediata: Separa autoatención de soporte presencial.", cuerpo)
        ]
    ]
    t_rag = Table(filas_rag, colWidths=[150, 310, 250])
    t_rag.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#F1F5F9")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_rag)
    story.append(PageBreak())

    # =========================================================================
    # DIAPOSITIVA 7: Bloque 3 - Ciberseguridad y LOPDP Ecuador
    # =========================================================================
    story.append(Paragraph("Bloque 3: Ciberseguridad y Protección de Datos (LOPDP)", titulo_slide))
    story.append(Paragraph("Expositora: Amalia Geoconda Iguasnia (QA / Seguridad) · Minutos 08:00 - 10:00", subtitulo_slide))

    filas_sec = [
        [Paragraph("<b>Principio Legal / OWASP</b>", tarjeta_header), Paragraph("<b>Mecanismo de Defensa en el Código</b>", tarjeta_header), Paragraph("<b>Certificación de Seguridad</b>", tarjeta_header)],
        [
            Paragraph("<b>LOPDP Art. 23<br/>Anonimización de Claves</b>", cuerpo_bold),
            Paragraph("Expresiones regulares interceptan contraseñas o PINs ingresados por error en la descripción y los reemplazan por <code>[CONFIDENCIAL_REMOVIDO]</code>.", cuerpo),
            Paragraph("Cero fugas de credenciales a proveedores externos o base de datos.", cuerpo)
        ],
        [
            Paragraph("<b>LOPDP Art. 10<br/>Minimización de Datos</b>", cuerpo_bold),
            Paragraph("Solo se solicitan 3 datos laborales (nombre, correo corporativo y departamento). Prohibida la captura de cédulas o datos biométricos.", cuerpo),
            Paragraph("Cumplimiento estricto de privacidad por diseño y por defecto.", cuerpo)
        ],
        [
            Paragraph("<b>OWASP LLM01<br/>Prompt Injection</b>", cuerpo_bold),
            Paragraph("Aislamiento estricto de la entrada del usuario con delimitadores XML <code>&lt;solicitud&gt;...&lt;/solicitud&gt;</code>.", cuerpo),
            Paragraph("Neutraliza intentos de secuestro de rol (ej: Modo Dios, DOC-99).", cuerpo)
        ],
        [
            Paragraph("<b>OWASP LLM05<br/>Improper Output Handling</b>", cuerpo_bold),
            Paragraph("Esquemas Pydantic V2 cerrados con <code>model_config = ConfigDict(extra='forbid')</code>.", cuerpo),
            Paragraph("Rechazo tajante de campos maliciosos o respuestas no tipificadas.", cuerpo)
        ]
    ]
    t_sec = Table(filas_sec, colWidths=[170, 310, 230])
    t_sec.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#EFF6FF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#93C5FD")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#DBEAFE")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_sec)
    story.append(PageBreak())

    # =========================================================================
    # DIAPOSITIVA 8: Bloque 3 - Control de Agencia (HITL) y Pruebas
    # =========================================================================
    story.append(Paragraph("Bloque 3: Control de Agencia (HITL) y Resultados QA", titulo_slide))
    story.append(Paragraph("Expositora: Amalia Geoconda Iguasnia (QA / Seguridad) · Minutos 10:00 - 12:00", subtitulo_slide))

    filas_qa = [
        [Paragraph("<b>Control de Exceso de Agencia (OWASP LLM08 - HITL)</b>", tarjeta_header), Paragraph("<b>Batería de Pruebas y Certificación de Calidad</b>", tarjeta_header)],
        [
            Paragraph("• <b>Compuerta Human-in-the-Loop Obligatoria:</b><br/>  El modelo de IA propone la solución y categoría, pero <b>no se registra en la base de datos ni se compromete el SLA</b> sin la confirmación explícita del operador humano o colaborador.<br/><br/>• <b>Modal Interactivo en Frontend:</b><br/>  Permite al usuario revisar la autoatención antes de crear el ticket. Si resuelve el problema, cancela la solicitud, ahorrando costos a la empresa.<br/><br/>• <b>Rate Limiting Token Bucket (RFC 6585):</b><br/>  15 fichas por IP recargables cada 3s para prevenir ataques de denegación de servicio (HTTP 429).", cuerpo),
            Paragraph("• <b>82 Pruebas Unitarias Automatizadas (Pytest):</b><br/>  100% aprobadas con Mocks deterministas ($0.00 USD de costo y 0 tokens consumidos).<br/><br/>• <b>16 Pruebas en Vivo contra la Nube (<code>docs/08-pruebas.md</code>):</b><br/>  Ejecutadas contra Render Cloud incluyendo inyecciones de prompt (neutralizadas) y monitoreo de salud.<br/><br/>• <b>Auditoría Cero Secretos en Git:</b><br/>  100% de cumplimiento: <code>.env</code> protegido en <code>.gitignore</code>, sin claves en el código ni en el historial de commits.", cuerpo)
        ]
    ]
    t_qa = Table(filas_qa, colWidths=[355, 355])
    t_qa.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_qa)
    story.append(PageBreak())

    # =========================================================================
    # DIAPOSITIVA 9: Métricas Comparativas Semana 3 vs Semana 4
    # =========================================================================
    story.append(Paragraph("Evaluación Cuantitativa y Comparativa de Madurez", titulo_slide))
    story.append(Paragraph("Consolidación de resultados frente a la rúbrica de titulación", subtitulo_slide))

    filas_comp = [
        [Paragraph("<b>Dimensión Evaluada</b>", tarjeta_header), Paragraph("<b>Meta Exigida</b>", tarjeta_header), Paragraph("<b>Semana 3 (Línea Base)</b>", tarjeta_header), Paragraph("<b>Versión Final (Semana 4)</b>", tarjeta_header), Paragraph("<b>Veredicto</b>", tarjeta_header)],
        [
            Paragraph("<b>Recuperación RAG (hit@5)</b>", cuerpo_bold),
            Paragraph("≥ 85.0%", cuerpo),
            Paragraph("92.0%", cuerpo),
            Paragraph("<b>94.1%</b> (15 manuales)", cuerpo_bold),
            Paragraph("<font color='#059669'><b>SUPERADA</b></font>", cuerpo)
        ],
        [
            Paragraph("<b>Tasa de Alucinación</b>", cuerpo_bold),
            Paragraph("0.0%", cuerpo),
            Paragraph("0.0%", cuerpo),
            Paragraph("<b>0.0% estricto</b>", cuerpo_bold),
            Paragraph("<font color='#059669'><b>CUMPLIDA</b></font>", cuerpo)
        ],
        [
            Paragraph("<b>Determinismo ITIL y SLA</b>", cuerpo_bold),
            Paragraph("100.0%", cuerpo),
            Paragraph("100.0%", cuerpo),
            Paragraph("<b>100.0%</b> (Matriz JSON)", cuerpo_bold),
            Paragraph("<font color='#059669'><b>CUMPLIDA</b></font>", cuerpo)
        ],
        [
            Paragraph("<b>Errores Silenciosos</b>", cuerpo_bold),
            Paragraph("0 estricto", cuerpo),
            Paragraph("0", cuerpo),
            Paragraph("<b>0</b> (Cero errores)", cuerpo_bold),
            Paragraph("<font color='#059669'><b>CUMPLIDA</b></font>", cuerpo)
        ],
        [
            Paragraph("<b>Pruebas Automatizadas</b>", cuerpo_bold),
            Paragraph("100.0%", cuerpo),
            Paragraph("82 unitarias", cuerpo),
            Paragraph("<b>82 unitarias + 16 en la nube</b>", cuerpo_bold),
            Paragraph("<font color='#059669'><b>CUMPLIDA</b></font>", cuerpo)
        ],
        [
            Paragraph("<b>Entorno de Despliegue</b>", cuerpo_bold),
            Paragraph("Producción Cloud", cuerpo),
            Paragraph("Localhost:8000", cuerpo),
            Paragraph("<b>Render Cloud (/health 200)</b>", cuerpo_bold),
            Paragraph("<font color='#059669'><b>CUMPLIDA</b></font>", cuerpo)
        ]
    ]
    t_comp = Table(filas_comp, colWidths=[160, 95, 140, 195, 120])
    t_comp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#EFF6FF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#93C5FD")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#DBEAFE")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_comp)
    story.append(PageBreak())

    # =========================================================================
    # DIAPOSITIVA 10: Conclusiones y Demostración en Vivo
    # =========================================================================
    story.append(Paragraph("Conclusiones y Demostración Práctica en Vivo", titulo_slide))
    story.append(Paragraph("Apertura de la sesión de preguntas del tribunal evaluador", subtitulo_slide))

    filas_cierre = [
        [Paragraph("<b>Logros Destacados del Proyecto</b>", tarjeta_header), Paragraph("<b>Enlaces y Recursos de Auditoría</b>", tarjeta_header)],
        [
            Paragraph("1. <b>Arquitectura Robusta y Determinista:</b> El sistema demuestra que un modelo probabilístico puede gobernarse eficazmente mediante código estricto y configuraciones desacopladas.<br/><br/>2. <b>Cero Alucinaciones y Citas Verificables:</b> 100% de trazabilidad procedimental hacia fuentes oficiales con soporte para normas de seguridad ISO/IEC 27002.<br/><br/>3. <b>Enfoque Human-in-the-Loop y Ciberseguridad:</b> Pleno blindaje ante inyecciones de prompt (OWASP LLM01) y respeto irrestricto a la privacidad (LOPDP Ecuador).<br/><br/>4. <b>Impacto Real en la PYME:</b> Reducción estimada de hasta un 60% en la saturación de tickets presenciales gracias a la autoatención amigable.", cuerpo),
            Paragraph("• <b>Tablero Kanban en Producción:</b><br/>  <font color='#1E3A8A'><u>https://triajesoporte-grupo-3.onrender.com/tablero</u></font><br/><br/>• <b>Endpoint de Salud Operativo:</b><br/>  <font color='#1E3A8A'><u>https://triajesoporte-grupo-3.onrender.com/health</u></font><br/><br/>• <b>Documentación Swagger OpenAPI:</b><br/>  <font color='#1E3A8A'><u>https://triajesoporte-grupo-3.onrender.com/docs</u></font><br/><br/>• <b>Repositorio GitHub Oficial:</b><br/>  <font color='#1E3A8A'><u>https://github.com/cgmorales12/TriajeSoporte-grupo-3</u></font><br/><br/><i>¡Estamos listos para la demostración en vivo y sus preguntas!</i>", cuerpo)
        ]
    ]
    t_cierre = Table(filas_cierre, colWidths=[355, 355])
    t_cierre.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_cierre)

    # Construir documento PDF con canvas numerado
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF generado exitosamente en: {ruta_pdf}")

if __name__ == "__main__":
    salida = os.path.join("docs", "presentacion-sustentacion-12-minutos.pdf")
    construir_presentacion(salida)
    # Crear copia con nombre alternativo para máxima compatibilidad
    copia = os.path.join("docs", "08-presentacion-sustentacion.pdf")
    construir_presentacion(copia)

