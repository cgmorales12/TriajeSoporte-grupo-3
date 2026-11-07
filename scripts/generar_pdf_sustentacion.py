#!/usr/bin/env python3
"""
Generador de Presentación de Sustentación en PDF (12 Minutos)
Proyecto: Triaje Automático de Solicitudes de Soporte Tecnológico para una PYME
Caso N.º 03 · Grupo 3 UNIANDES
Genera: docs/presentacion-sustentacion-12-minutos.pdf y docs/08-presentacion-sustentacion.pdf
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
        self.drawString(36, 7, "Triaje Automático de Solicitudes de Soporte Tecnológico para una PYME | Caso N.º 03 · Grupo 3 UNIANDES")
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
        fontSize=19,
        leading=23,
        textColor=colors.HexColor("#1E3A8A"),
        spaceAfter=6
    )

    subtitulo_slide = ParagraphStyle(
        'SubtituloSlide',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor("#0D9488"),
        spaceAfter=10
    )

    cuerpo = ParagraphStyle(
        'CuerpoSlide',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
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
        fontSize=10.5,
        leading=13.5,
        textColor=colors.HexColor("#1E3A8A")
    )

    story = []

    # =========================================================================
    # DIAPOSITIVA 1: Portada Oficial
    # =========================================================================
    story.append(Spacer(1, 35))
    story.append(Paragraph("Triaje Automático de Solicitudes de Soporte Tecnológico para una PYME", ParagraphStyle(
        'PortadaTitulo',
        fontName='Helvetica-Bold',
        fontSize=23,
        leading=27,
        alignment=1,
        textColor=colors.HexColor("#1E3A8A")
    )))
    story.append(Spacer(1, 8))
    story.append(Paragraph("Mesa de Ayuda Inteligente y Soporte Microinformático TIC con RAG sobre 15 Manuales Oficiales", ParagraphStyle(
        'PortadaSub',
        fontName='Helvetica-Bold',
        fontSize=12.5,
        leading=16,
        alignment=1,
        textColor=colors.HexColor("#0D9488")
    )))
    story.append(Spacer(1, 20))

    datos_portada = [
        [Paragraph("<b>Seminario:</b>", cuerpo_bold), Paragraph("Ingeniería de Software con IA Generativa — Octubre-Noviembre 2026", cuerpo)],
        [Paragraph("<b>Universidad:</b>", cuerpo_bold), Paragraph("Universidad Regional Autónoma de los Andes (UNIANDES)", cuerpo)],
        [Paragraph("<b>Caso Asignado:</b>", cuerpo_bold), Paragraph("Caso N.º 03 · Triaje de Soporte Tecnológico (PYME 60 Colaboradores)", cuerpo)],
        [Paragraph("<b>Docente Evaluador:</b>", cuerpo_bold), Paragraph("Ing. Heyler Fabio Guaza (Mg. en Ciberseguridad · OPD · Abogado)", cuerpo)],
        [Paragraph("<b>Integrantes (Grupo 3):</b>", cuerpo_bold), Paragraph("1. Christian Guillermo Morales González (Tech Lead / Coordinador)<br/>2. Luis Fernando Ribera Alajo (Builder / Arquitectura)<br/>3. Amalia Geoconda Iguasnia Escobar (QA Lead / Ciberseguridad)", cuerpo)],
        [Paragraph("<b>URL en Producción:</b>", cuerpo_bold), Paragraph("<font color='#1E3A8A'><u>https://triajesoporte-grupo-3.onrender.com</u></font> (Health: /health)", cuerpo)],
        [Paragraph("<b>Repositorio GitHub:</b>", cuerpo_bold), Paragraph("<font color='#1E3A8A'><u>https://github.com/cgmorales12/TriajeSoporte-grupo-3</u></font>", cuerpo)]
    ]
    t_portada = Table(datos_portada, colWidths=[150, 550])
    t_portada.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 5.5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
    ]))
    story.append(t_portada)
    story.append(PageBreak())

    # =========================================================================
    # DIAPOSITIVA 2: Cronograma Oficial Minuto a Minuto (12 Minutos Exactos)
    # =========================================================================
    story.append(Paragraph("Estructura de la Sustentación Oral (12 Minutos Exactos)", titulo_slide))
    story.append(Paragraph("Cronograma coordinado y balanceado de exposición ante el tribunal evaluador", subtitulo_slide))

    bloques = [
        [
            Paragraph("<b>Tramo 1 y 2 · [00:00 - 05:00]</b>", tarjeta_header),
            Paragraph("<b>Tramo Central · [05:00 - 07:00]</b>", tarjeta_header),
            Paragraph("<b>Tramo Central · [07:00 - 10:00]</b>", tarjeta_header),
            Paragraph("<b>Tramo 3 Cierre · [10:00 - 12:00]</b>", tarjeta_header)
        ],
        [
            Paragraph("<b>Christian Morales G.</b><br/><i>Tech Lead / Coordinador</i>", cuerpo_bold),
            Paragraph("<b>Luis Fernando Ribera</b><br/><i>Builder / Arquitectura</i>", cuerpo_bold),
            Paragraph("<b>Amalia Iguasnia E.</b><br/><i>QA Lead / Seguridad</i>", cuerpo_bold),
            Paragraph("<b>Christian Morales G.</b><br/><i>Tech Lead / Cierre</i>", cuerpo_bold)
        ],
        [
            Paragraph("• Dolor real en la PYME (60 colaboradores, 1 solo técnico).<br/>• <b>Demo en vivo en Render:</b><br/>  - Caso 1: VPN (DOC-02) RAG.<br/>  - Caso 2: Menú almuerzo (Abstención 0 citas).<br/>  - <b>Transición a Vista TIC.</b><br/>  - Caso 3: Daño hardware (HITL).", cuerpo),
            Paragraph("• Modelo C4 y AnyIO (40 hilos).<br/>• <b>Principio Determinista ITIL:</b><br/>  - Matriz en JSON externo.<br/>  - Función pura en Python.<br/>  - <b>Costo CERO tokens</b>.<br/>• Persistencia SQLite parametrizada.<br/>• Auto-siembra de 20 tickets en Render efímero.", cuerpo),
            Paragraph("• <b>Suite 83 pruebas Pytest:</b><br/>  - 100% verde con Mocks.<br/>  - Aislamiento en conftest.py.<br/>• <b>Smoke tests en vivo p95: 2.2s</b> («El promedio engaña»).<br/>• <b>Ciberseguridad LOPDP Art. 23:</b><br/>  - Anonimización regex de claves.<br/>  - Token Bucket (HTTP 429).<br/>  - Pydantic extra='forbid'.", cuerpo),
            Paragraph("• <b>Retoma en min 10:00:</b><br/>  - Abre Dashboard Fase 5.<br/>• <b>5 KPIs de Impacto:</b><br/>  - 73.3% autoatención L1.<br/>  - MTTR de 45m a 3.8m.<br/>  - 4.5 hrs/día liberadas.<br/>  - <b>Ahorro $16,987 USD/año</b>.<br/>• <b>Honestidad técnica:</b><br/>  - Límites ADR-004 (Postgres).", cuerpo)
        ]
    ]
    t_bloques = Table(bloques, colWidths=[180, 180, 180, 180])
    t_bloques.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#EFF6FF")),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor("#F8FAFC")),
        ('BACKGROUND', (0,2), (-1,2), colors.white),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#93C5FD")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#DBEAFE")),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_bloques)
    story.append(PageBreak())

    # =========================================================================
    # DIAPOSITIVA 3: Bloque 1 - Problema Real de la PYME y Principio Rector
    # =========================================================================
    story.append(Paragraph("Bloque 1: Problema Real de la PYME y Principio Rector", titulo_slide))
    story.append(Paragraph("Expositor: Christian Morales (Tech Lead) · Minutos 00:00 - 01:00", subtitulo_slide))

    items_problema = [
        [Paragraph("<b>El Dolor Crítico en la PYME (60 Colaboradores)</b>", tarjeta_header), Paragraph("<b>Principio Rector de Ingeniería Implementado</b>", tarjeta_header)],
        [
            Paragraph("• <b>1 Solo Técnico de TI Desbordado:</b> La empresa cuenta con un técnico microinformático que pierde más del <b>56% de su jornada laboral (4.5 horas/día)</b> atendiendo solicitudes repetitivas de oficina.<br/><br/>"
                      "• <b>Cuello de Botella Operativo:</b> Bloqueos de contraseña en Active Directory, configuración de VPNs para teletrabajo, atascos de impresoras y sesiones colgadas en el ERP generaban un tiempo medio de resolución (MTTR) de <b>45 minutos a 4 horas por incidente</b>.<br/><br/>"
                      "• <b>Impacto Financiero:</b> Detención de colaboradores en Contabilidad, Ventas y RRHH, con un costo manual elevado de <b>$18.00 USD por ticket</b>.", cuerpo),
            Paragraph("• <b>«El Modelo Propone, el Código Dispone»:</b><br/>"
                      "  El LLM es un componente probabilístico, falible y costoso. Todo su comportamiento está gobernado por código backend determinista, esquemas estrictos y reglas inviolables.<br/><br/>"
                      "• <b>Las Cuatro Máximas de Arquitectura:</b><br/>"
                      "  1. <i>El modelo propone</i> la extracción de síntomas en lenguaje natural.<br/>"
                      "  2. <i>El código dispone</i> las acciones operativas y validaciones.<br/>"
                      "  3. <i>La configuración gobierna</i> las prioridades y SLAs a <b>costo 0 tokens</b>.<br/>"
                      "  4. <i>El humano autoriza</i> antes de despachar o persistir (HITL · OWASP LLM08).", cuerpo)
        ]
    ]
    t_prob = Table(items_problema, colWidths=[355, 355])
    t_prob.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#F1F5F9")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 9),
    ]))
    story.append(t_prob)
    story.append(PageBreak())

    # =========================================================================
    # DIAPOSITIVA 4: Bloque 1 - Demo en Vivo y Dualidad de Vistas (RBAC)
    # =========================================================================
    story.append(Paragraph("Bloque 1: Demostración en Vivo y Dualidad de Vistas", titulo_slide))
    story.append(Paragraph("Expositor: Christian Morales (Tech Lead) · Minutos 01:00 - 05:00 · URL en Producción (Render)", subtitulo_slide))

    filas_demo = [
        [Paragraph("<b>Entorno / Vista</b>", tarjeta_header), Paragraph("<b>Caso Evaluado en Vivo (1 Clic)</b>", tarjeta_header), Paragraph("<b>Comportamiento Verificado en Pantalla</b>", tarjeta_header)],
        [
            Paragraph("<b>👤 Vista Usuario</b><br/><i>Portal Limpio para los 60 Colaboradores</i>", cuerpo_bold),
            Paragraph("<b>Caso 1: Autoatención Nivel 1</b><br/>Preset <code>[🌐 Fallo VPN FortiClient (DOC-02)]</code>", cuerpo),
            Paragraph("Respuesta en 1 a 2 segundos con RAG. Muestra tiempo estimado en lenguaje amigable (4 horas), pasos recomendados y <b>enlace oficial directo clicable a FortiClient VPN ↗</b>.", cuerpo)
        ],
        [
            Paragraph("<b>👤 Vista Usuario</b><br/><i>Diseño UX sin jerga técnica</i>", cuerpo_bold),
            Paragraph("<b>Caso 2: Fuera de Alcance</b><br/>Preset <code>[🍱 Menú Almuerzo (Abstención)]</code>", cuerpo),
            Paragraph("Regla determinista de silencio: devuelve <b>0 citas técnicas</b>, se abstiene de inventar recetas y orienta a RRHH/Secretaría, <b>bloqueando la creación de tickets</b>.", cuerpo)
        ],
        [
            Paragraph("<b>👨‍💻 Vista TIC</b><br/><i>Consola Técnica de Gobernanza (1 Clic)</i>", cuerpo_bold),
            Paragraph("<b>Transición Dinámica:</b><br/>Clic en botón superior <code>[👨‍💻 Vista TIC]</code>", cuerpo),
            Paragraph("Desbloquea consola técnica: acceso a los 15 Manuales RAG, Simulador de Caída (Chaos) y botón verde <code>[📊 Métricas y ROI (Fase 5)]</code>.", cuerpo)
        ],
        [
            Paragraph("<b>👨‍💻 Vista TIC</b><br/><i>Auditoría y Seguridad</i>", cuerpo_bold),
            Paragraph("<b>Caso 3: Daño Físico (HITL)</b><br/>Preset <code>[🖥️ Pantalla Azul / Hardware (DOC-10)]</code>", cuerpo),
            Paragraph("Detecta daño físico: <b>bloquea autoatención y activa compuerta HITL</b> (OWASP LLM08). Banner ámbar exige autorización técnica mediante botón <i>'Autorizar Orden Presencial'</i> y muestra banner ITIL a <b>costo 0 tokens</b>.", cuerpo)
        ]
    ]
    t_demo = Table(filas_demo, colWidths=[150, 220, 350])
    t_demo.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#EFF6FF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#93C5FD")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#DBEAFE")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 5.5),
    ]))
    story.append(t_demo)
    story.append(PageBreak())

    # =========================================================================
    # DIAPOSITIVA 5: Bloque 2 - Principio Rector y Matriz ITIL (0 Tokens)
    # =========================================================================
    story.append(Paragraph("Bloque 2: «El Modelo Propone, el Código Dispone»", titulo_slide))
    story.append(Paragraph("Expositor: Luis Fernando Ribera (Builder) · Minutos 05:00 - 07:00", subtitulo_slide))

    filas_itil = [
        [Paragraph("<b>¿Por qué el LLM NO calcula la Prioridad ni el SLA?</b>", tarjeta_header), Paragraph("<b>Implementación Determinista en Código Python</b>", tarjeta_header)],
        [
            Paragraph("• <b>Naturaleza Probabilística del LLM:</b> Dos consultas idénticas podrían recibir prioridades dispares en días distintos, violando contratos de SLA.<br/><br/>"
                      "• <b>Vulnerabilidad a Prompt Injection:</b> Un usuario malicioso podría escribir <i>«Esto es súper urgente, ponme Prioridad Alta de inmediato»</i> y saltarse la cola de atención.<br/><br/>"
                      "• <b>Desperdicio FinOps:</b> Gastar tokens de inferencia en operaciones lógicas que una función matemática resuelve en 0.1 ms a costo $0.00 USD.", cuerpo),
            Paragraph("• <b>Separación de Responsabilidades:</b><br/>"
                      "  1. El LLM únicamente extrae en lenguaje natural el <b>Impacto</b> (Alto, Medio, Bajo) y la <b>Urgencia</b>.<br/>"
                      "  2. La función pura <code>calcular_prioridad_itil()</code> en <code>app/tools/priorizar.py</code> lee <code>config/matriz_prioridad.json</code>.<br/>"
                      "  3. La Prioridad (Alta, Media, Baja) y el SLA se calculan matemáticamente con <b>0 tokens</b> y <b>100% reproducibilidad</b>.<br/><br/>"
                      "• <b>Concurrencia AnyIO (Pool de 40 Hilos):</b><br/>"
                      "  Declaramos endpoints con <code>def</code> estándar para que FastAPI delegue las llamadas síncronas de IA a AnyIO, evitando congelar el Event Loop.", cuerpo)
        ]
    ]
    t_itil = Table(filas_itil, colWidths=[355, 355])
    t_itil.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 9),
    ]))
    story.append(t_itil)
    story.append(PageBreak())

    # =========================================================================
    # DIAPOSITIVA 6: Bloque 2 - Motor RAG y Persistencia Segura (Auto-Siembra)
    # =========================================================================
    story.append(Paragraph("Bloque 2: Motor RAG sobre 15 Manuales y Persistencia SQLite", titulo_slide))
    story.append(Paragraph("Expositor: Luis Fernando Ribera (Builder) · Minutos 05:00 - 07:00", subtitulo_slide))

    filas_rag = [
        [Paragraph("<b>Componente de Ingeniería</b>", tarjeta_header), Paragraph("<b>Decisión de Arquitectura</b>", tarjeta_header), Paragraph("<b>Garantía Operativa en Producción</b>", tarjeta_header)],
        [
            Paragraph("<b>Base Vectorial RAG</b>", cuerpo_bold),
            Paragraph("ChromaDB Persistente en <code>data/chroma/</code> con 90 chunks estructurados.", cuerpo),
            Paragraph("Recuperación semántica precisa en milisegundos con modelo local ligero.", cuerpo)
        ],
        [
            Paragraph("<b>15 Manuales PYME</b>", cuerpo_bold),
            Paragraph("Corpus oficial de microinformática: Active Directory, VPN, impresoras, Wi-Fi, NAS, fibra, etc.", cuerpo),
            Paragraph("Grounding procedimental estricto: Citas exactas (DOC-01 a DOC-15) con paso exacto y vigencia ISO 27002.", cuerpo)
        ],
        [
            Paragraph("<b>Persistencia SQLite</b>", cuerpo_bold),
            Paragraph("Base transaccional embebida en <code>data/triaje_soporte.db</code> con consultas parametrizadas <code>?</code>.", cuerpo),
            Paragraph("Protección por diseño contra Inyección SQL (OWASP A03 / Top 10) y latencia de disco < 0.8 ms.", cuerpo)
        ],
        [
            Paragraph("<b>Patrón Auto-Siembra</b><br/><i>(Contenedor Efímero)</i>", cuerpo_bold),
            Paragraph("Evento <code>lifespan</code> en <code>app/main.py</code>: si <code>COUNT(*) == 0</code>, ejecuta <code>app/datos_semilla.py</code>.", cuerpo),
            Paragraph("Garantiza que el tribunal siempre encuentre <b>20 tickets estructurados</b> (5 por columna Kanban) tras reinicios de Render.", cuerpo)
        ]
    ]
    t_rag = Table(filas_rag, colWidths=[160, 290, 270])
    t_rag.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#F1F5F9")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 5.5),
    ]))
    story.append(t_rag)
    story.append(PageBreak())

    # =========================================================================
    # DIAPOSITIVA 7: Bloque 3 - Ciberseguridad LOPDP Ecuador y OWASP LLM
    # =========================================================================
    story.append(Paragraph("Bloque 3: Ciberseguridad y Protección de Datos (LOPDP)", titulo_slide))
    story.append(Paragraph("Expositora: Amalia Geoconda Iguasnia (QA / Seguridad) · Minutos 07:00 - 10:00", subtitulo_slide))

    filas_sec = [
        [Paragraph("<b>Principio Legal / OWASP</b>", tarjeta_header), Paragraph("<b>Mecanismo de Defensa en el Backend</b>", tarjeta_header), Paragraph("<b>Certificación de Ciberseguridad</b>", tarjeta_header)],
        [
            Paragraph("<b>LOPDP Art. 23<br/>Anonimización de Claves</b>", cuerpo_bold),
            Paragraph("Expresiones regulares interceptan contraseñas o PINs ingresados por error en la descripción y los reemplazan por <code>[CONFIDENCIAL_REMOVIDO]</code>.", cuerpo),
            Paragraph("Cero fugas de credenciales a proveedores de IA externos o base de datos.", cuerpo)
        ],
        [
            Paragraph("<b>LOPDP Art. 10<br/>Minimización de Datos</b>", cuerpo_bold),
            Paragraph("Solo se solicitan 3 identificadores laborales (nombre, correo corporativo y departamento). Prohibida la captura de cédulas o datos biométricos.", cuerpo),
            Paragraph("Cumplimiento estricto de privacidad por diseño y por defecto en el formulario.", cuerpo)
        ],
        [
            Paragraph("<b>Rate Limiting<br/>Token Bucket (RFC 6585)</b>", cuerpo_bold),
            Paragraph("Algoritmo de 10 fichas por IP con recarga de 1 ficha cada 6 segundos para mitigar abusos y saturación de cuota.", cuerpo),
            Paragraph("Respuesta estándar <code>HTTP 429 Too Many Requests</code> con encabezado <code>Retry-After: N</code>.", cuerpo)
        ],
        [
            Paragraph("<b>OWASP LLM01 / LLM05<br/>Inyecciones y Esquemas</b>", cuerpo_bold),
            Paragraph("Delimitación semántica <code>&lt;solicitud&gt;...&lt;/solicitud&gt;</code> y esquemas Pydantic V2 cerrados con <code>extra='forbid'</code>.", cuerpo),
            Paragraph("Rechazo tajante con <code>HTTP 422</code> ante atributos arbitrarios o campos alucinados.", cuerpo)
        ]
    ]
    t_sec = Table(filas_sec, colWidths=[170, 300, 250])
    t_sec.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#EFF6FF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#93C5FD")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#DBEAFE")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 5.5),
    ]))
    story.append(t_sec)
    story.append(PageBreak())

    # =========================================================================
    # DIAPOSITIVA 8: Bloque 3 - Suite de 83 Pruebas y Latencia p95 (SRE)
    # =========================================================================
    story.append(Paragraph("Bloque 3: Suite de 83 Pruebas Pytest y Latencia p95", titulo_slide))
    story.append(Paragraph("Expositora: Amalia Geoconda Iguasnia (QA / Seguridad) · Minutos 07:00 - 10:00", subtitulo_slide))

    filas_qa = [
        [Paragraph("<b>Suite de 83 Pruebas Unitarias e Integradas (Pytest)</b>", tarjeta_header), Paragraph("<b>Pruebas de Humo en Producción y Latencia SRE (Tema 5)</b>", tarjeta_header)],
        [
            Paragraph("• <b>100% de Pruebas Aprobadas (83/83 passed):</b><br/>"
                      "  - <code>test_endpoints.py</code>: 43 pruebas de API, contratos RFC 9457 y failover.<br/>"
                      "  - <code>test_construccion_prompts.py</code>: 11 pruebas R.E.C.E.T.A. y LOPDP.<br/>"
                      "  - <code>test_herramientas_agente.py</code>: 29 pruebas deterministas ITIL y HITL.<br/><br/>"
                      "• <b>Costo $0.00 USD con Mocks:</b><br/>"
                      "  Aislamiento con <code>monkeypatch</code> que simula Gemini/Groq sin gastar saldo ni depender de internet.<br/><br/>"
                      "• <b>Aislamiento de Base de Datos:</b><br/>"
                      "  Fixture <code>aislar_base_datos_tests</code> en <code>tests/conftest.py</code> genera una BD SQLite temporal que se destruye al terminar, protegiendo los 20 tickets oficiales.", cuerpo),
            Paragraph("• <b>Formato Oficial Tema 5:</b><br/>"
                      "  <i>«Una línea por caso, una línea de resultado»</i> en <code>tests/smoke.py</code>.<br/>"
                      "  PASA 1. [salud] GET /health -> 200 · 0.3s<br/>"
                      "  PASA 2. [caso] POST /chat (VPN) -> 200 · 1.2s<br/>"
                      "  PASA 3. [caso] POST /chat (AD) -> 200 · 0.8s<br/>"
                      "  PASA 4. [fuera] POST /chat (Fuera) -> 200 · 0.2s<br/>"
                      "  PASA 5. [inyeccion] POST /chat -> 200 · 0.2s<br/>"
                      "  PASA 6. [invalida] POST /chat -> 422 · 0.2s<br/>"
                      "  <b>RESULTADO: 6/6 pasan (100%) · p95: 2.2 s</b><br/><br/>"
                      "• <b>Premisa SRE: «El promedio engaña»:</b><br/>"
                      "  El p95 certifica que el <b>95% de los colaboradores</b> reciben solución en menos de 2.5s, sin esconder picos lentos.", cuerpo)
        ]
    ]
    t_qa = Table(filas_qa, colWidths=[355, 355])
    t_qa.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_qa)
    story.append(PageBreak())

    # =========================================================================
    # DIAPOSITIVA 9: Tramo 3 Cierre - Fase 5: Métricas de Impacto y ROI PYME
    # =========================================================================
    story.append(Paragraph("Fase 5: Métricas Ejecutivas y Retorno de Inversión (ROI)", titulo_slide))
    story.append(Paragraph("Expositor: Christian Morales (Tech Lead) · Minutos 10:00 - 12:00 · Modal Dashboard Ejecutivo", subtitulo_slide))

    filas_roi = [
        [
            Paragraph("<b>1. Autoatención Nivel 1</b>", tarjeta_header),
            Paragraph("<b>2. Reducción de MTTR</b>", tarjeta_header),
            Paragraph("<b>3. Tiempo Libre Técnico</b>", tarjeta_header),
            Paragraph("<b>4. Ahorro Anual PYME</b>", tarjeta_header),
            Paragraph("<b>5. Latencia p95 (SRE)</b>", tarjeta_header)
        ],
        [
            Paragraph("<font size='16' color='#15803D'><b>73.3%</b></font><br/>Meta UNIANDES: ≥ 70%<br/><font color='#16A34A'><b>CUMPLE CON ÉXITO</b></font>", cuerpo),
            Paragraph("<font size='16' color='#0284C7'><b>3.8 min</b></font><br/>Antes: 45 min manuales<br/><font color='#0284C7'><b>-91.5% REDUCCIÓN</b></font>", cuerpo),
            Paragraph("<font size='16' color='#D97706'><b>4.5 hrs/día</b></font><br/>56% jornada laboral<br/><font color='#D97706'><b>CAPACIDAD LIBERADA</b></font>", cuerpo),
            Paragraph("<font size='16' color='#7C3AED'><b>$16,987 USD</b></font><br/>Ticket $18 a $3.40<br/><font color='#7C3AED'><b>ALTO RETORNO (ROI)</b></font>", cuerpo),
            Paragraph("<font size='16' color='#BE185D'><b>2.2 s</b></font><br/>El promedio engaña<br/><font color='#BE185D'><b>95% &lt; 2.5s GARANTIZADO</b></font>", cuerpo)
        ],
        [
            Paragraph("<b>Resolución sin Humanos:</b> 73 de cada 100 consultas se resuelven en Nivel 1 mediante manuales RAG y citas verificables.", cuerpo),
            Paragraph("<b>Agilidad para el Empleado:</b> Fin de las esperas prolongadas; colaboradores de ventas y contabilidad retoman sus labores al instante.", cuerpo),
            Paragraph("<b>Enfoque Estratégico:</b> El técnico dedica su tiempo a ciberseguridad, servidores y proyectos de infraestructura PYME.", cuerpo),
            Paragraph("<b>Ahorro Cuantificable:</b> Reduce visitas presenciales innecesarias ($15 a $25 USD) eliminando costos ocultos operativos.", cuerpo),
            Paragraph("<b>Experiencia Homogénea:</b> Monitoreo de colas y percentiles para asegurar que ningún usuario quede abandonado en la cola.", cuerpo)
        ]
    ]
    t_roi = Table(filas_roi, colWidths=[144, 144, 144, 144, 144])
    t_roi.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#EFF6FF")),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor("#F8FAFC")),
        ('BACKGROUND', (0,2), (-1,2), colors.white),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#93C5FD")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#DBEAFE")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_roi)
    story.append(PageBreak())

    # =========================================================================
    # DIAPOSITIVA 10: Conclusiones, Transparencia Técnica (ADR-004) y Cierre
    # =========================================================================
    story.append(Paragraph("Conclusiones, Transparencia Técnica y Ronda de Preguntas", titulo_slide))
    story.append(Paragraph("Cierre formal de la defensa de grado · Minuto 12:00", subtitulo_slide))

    filas_cierre = [
        [Paragraph("<b>Transparencia Técnica y Limitaciones (ADR-004)</b>", tarjeta_header), Paragraph("<b>Enlaces Oficiales y Recursos de Auditoría</b>", tarjeta_header)],
        [
            Paragraph("1. <b>Fronteras Actuales del MVP (SQLite Mono-Instancia):</b><br/>"
                      "   Reconocemos con honestidad que operamos sobre un microcontenedor con SQLite local efímero. Para los 60 colaboradores actuales responde en < 0.8 ms a costo cero.<br/><br/>"
                      "2. <b>Escalamiento Futuro a PostgreSQL Gestionado:</b><br/>"
                      "   Si la empresa creciera a 500+ colaboradores y requiriera balanceo horizontal multi-instancia, el archivo SQLite fragmentaría el estado. Dejamos formalmente documentada y desacoplada la migración en <b>ADR-004</b> hacia Supabase o AWS RDS.<br/><br/>"
                      "3. <b>Principio Rector 100% Cumplido:</b><br/>"
                      "   <i>«El modelo propone, el código dispone, la configuración gobierna y el humano autoriza»</i>.", cuerpo),
            Paragraph("• <b>Tablero Kanban en Producción:</b><br/>"
                      "  <font color='#1E3A8A'><u>https://triajesoporte-grupo-3.onrender.com/tablero</u></font><br/><br/>"
                      "• <b>Endpoint de Salud Operativo:</b><br/>"
                      "  <font color='#1E3A8A'><u>https://triajesoporte-grupo-3.onrender.com/health</u></font><br/><br/>"
                      "• <b>Documentación Swagger OpenAPI:</b><br/>"
                      "  <font color='#1E3A8A'><u>https://triajesoporte-grupo-3.onrender.com/docs</u></font><br/><br/>"
                      "• <b>Repositorio GitHub Oficial:</b><br/>"
                      "  <font color='#1E3A8A'><u>https://github.com/cgmorales12/TriajeSoporte-grupo-3</u></font><br/><br/>"
                      "<b>¡Muchas gracias! Quedamos a disposición del distinguido tribunal para la ronda de preguntas.</b>", cuerpo)
        ]
    ]
    t_cierre = Table(filas_cierre, colWidths=[355, 355])
    t_cierre.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 9),
    ]))
    story.append(t_cierre)

    # Construir documento PDF con canvas numerado
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF generado exitosamente en: {ruta_pdf}")

if __name__ == "__main__":
    salida = os.path.join("docs", "presentacion-sustentacion-12-minutos.pdf")
    construir_presentacion(salida)
    copia = os.path.join("docs", "08-presentacion-sustentacion.pdf")
    construir_presentacion(copia)
