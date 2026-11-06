# Base de Conocimiento Técnica Estándar (Corpus RAG) — Mesa de Ayuda PYME
**Proyecto:** TecnoAula — Triaje Automático de Solicitudes de Soporte Tecnológico para PYMEs (Caso N.º 03 · Grupo 3 UNIANDES)  
**Alcance:** Catálogo universal de 15 manuales y procedimientos técnicos de soporte estándar para cualquier Pequeña o Mediana Empresa con puestos de trabajo ofimáticos, red local y servicios corporativos.

---

## 1. Inventario de los 15 Manuales Técnicos Estándar para Cualquier PYME

| Código | Título del Procedimiento | Categoría ITIL | Estándar / Referencia Técnica Oficial |
| :---: | :--- | :--- | :--- |
| **DOC-01** | Restablecimiento de Contraseñas de Dominio Windows y Correo Corporativo | Accesos y Contraseñas | Microsoft Active Directory Domain Services / Azure AD |
| **DOC-02** | Guía de Conexión y Configuración de VPN Corporativa para Teletrabajo | Redes y Conectividad | Fortinet FortiClient / OpenVPN Corporate Standards |
| **DOC-03** | Solución de Problemas en Impresoras Departamentales de Red | Hardware y Periféricos | HP Network Print Services / IP Spooler |
| **DOC-04** | Procedimiento de Acceso y Mapeo de Carpetas Compartidas en Red (SMB / NAS) | Almacenamiento y Archivos | Windows Server File Sharing SMB 3.0 / NAS |
| **DOC-05** | Manual de Usuario y Solución de Bloqueos en el Sistema Contable / ERP Interno | Software Corporativo | Facturación Electrónica SRI / ERP Transaccional SQL |
| **DOC-06** | Política de Uso Aceptable de Activos de Información y Ciberseguridad | Seguridad de la Información | ISO/IEC 27002:2022 (Control de Accesos y Escritorio Limpio) |
| **DOC-07** | Diagnóstico y Solución de Conexión a Internet y Red Cableada en Oficina | Redes y Conectividad | IEEE 802.3 Ethernet / Cableado Estructurado Categoría 6 |
| **DOC-08** | Conexión Segura al Wi-Fi Corporativo de la Oficina y Red de Visitas | Redes Inalámbricas | Wi-Fi Alliance WPA3-Enterprise / 802.1X RADIUS |
| **DOC-09** | Gestión de Antivirus Endpoint y Actualizaciones de Seguridad del SO | Seguridad y Mantenimiento | Microsoft Defender for Endpoint / Patch Management |
| **DOC-10** | Diagnóstico de Fallas en la Estación de Trabajo (PC / Laptop) | Soporte a Estaciones | Windows Client Performance Troubleshooting / BSOD Triage |
| **DOC-11** | Guía de Configuración y Solución de Problemas en Cliente de Correo Outlook | Correo y Colaboración | Microsoft 365 Exchange Online / Outlook Client |
| **DOC-12** | Procedimiento para Solicitud de Nuevos Accesos y Alta de Colaboradores | Identidad y Accesos | ITIL v4 Service Request Management / Onboarding |
| **DOC-13** | Procedimiento de Respaldo y Recuperación de Archivos de Trabajo | Respaldo y Continuidad | Shadow Copies (VSS) / OneDrive Business Backup |
| **DOC-14** | Configuración de Periféricos y Pantallas Múltiples en el Puesto de Trabajo | Hardware de Oficina | Windows Multi-Display Settings / USB-C Docking Station |
| **DOC-15** | Matriz de Priorización ITIL y Protocolo de Escalamiento a Soporte Nivel 2 | Gestión de Incidentes | ITIL v4 Incident Management Standard / SLA Matrix |

---

## 2. Flexibilidad y Adaptabilidad para Cualquier PYME
Este corpus está concebido como una plantilla base modular:
1. **Configurable por la Empresa:** Cualquier PYME puede agregar nuevos manuales en formato Markdown (.md) en este directorio sin modificar el código fuente.
2. **Re-ingesta Automatizada:** Ejecutando `python scripts/ingest.py`, el sistema extrae, fragmenta y actualiza la colección vectorial ChromaDB en cuestión de segundos.
3. **Independiente de Marca o Proveedor:** El soporte abarca tecnologías estándar del mercado presentes en la mayoría de oficinas: Windows, Linux, Microsoft 365, Active Directory, SMB, Wi-Fi Enterprise, impresoras de red y clientes VPN comunes.
