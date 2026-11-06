# Inventario de Fuentes Técnicas Estándar: Triaje Automático de Solicitudes de Soporte Tecnológico para una PYME (Corpus RAG)

## 1. Identificación y Alcance del Corpus
* **Proyecto:** Triaje Automático de Solicitudes de Soporte Tecnológico para una PYME
* **Caso de Estudio Oficial:** Caso N.º 03 (Grupo 3 UNIANDES)
* **Objetivo del Corpus:** Proveer una base de conocimiento técnica oficial, estandarizada y aplicable a **cualquier Pequeña o Mediana Empresa (PYME)** para alimentar el sistema RAG en ChromaDB. Garantiza diagnósticos de Nivel 1 rigurosos con citas verificables (código de documento y paso operativo exacto).

---

## 2. Criterios de Selección y Curaduría de Fuentes para PYMEs
1. **Universalidad y Estándares de la Industria:** Los manuales abarcan las tecnologías de ofimática y red universales en entornos corporativos (Microsoft Active Directory, VPN SSL/IPsec, SMB 3.0, IEEE 802.3 Ethernet, Wi-Fi Alliance WPA3-Enterprise, ISO/IEC 27002, ITIL v4).
2. **Formato Estructurado:** 15 documentos en Markdown local (`data/raw/DOC-*.md`) normalizados con metadatos obligatorios: `documento`, `sección`, `vigencia` y `url`.
3. **Estrategia de Fragmentación (Chunking):** Fragmentación semántica guiada por pasos operativos (`### Paso N: Título`). Total: **90 fragmentos estructurados** indexados en la colección persistente `manuales_tecnicos` de ChromaDB.
4. **Independencia de Negocio:** No se asume una empresa en particular; cualquier PYME puede adaptar o incorporar sus propios manuales en `data/raw/` y re-ejecutar `python scripts/ingest.py`.

---

## 3. Matriz de los 15 Manuales Técnicos Estándar para Cualquier PYME

| ID | Documento / Guía Técnica | Ámbito Operativo PYME | URL Oficial / Estándar de Referencia | Vigencia | Fragmentos |
| :---: | :--- | :--- | :--- | :---: | :---: |
| **DOC-01** | Restablecimiento de Contraseñas de Dominio Windows y Correo | Cuentas y Accesos | [Microsoft Active Directory DS](https://learn.microsoft.com/es-es/windows-server/identity/ad-ds/) | 2026 | 6 |
| **DOC-02** | Configuración de VPN Corporativa para Teletrabajo (FortiClient) | Acceso Remoto Seguro | [Fortinet FortiClient Docs](https://docs.fortinet.com/product/forticlient/) | 2026 | 6 |
| **DOC-03** | Solución de Problemas en Impresoras Departamentales de Red | Hardware de Oficina | [HP Network Printing Solutions](https://support.hp.com/es-es/document/ish_2026_impresoras_red) | 2026 | 6 |
| **DOC-04** | Procedimiento de Acceso y Mapeo de Carpetas Compartidas (SMB/NAS) | Servidor de Archivos | [Windows File Server SMB](https://learn.microsoft.com/es-es/windows-server/storage/file-server/) | 2026 | 6 |
| **DOC-05** | Manual de Usuario y Solución de Bloqueos en ERP / Sistema Contable | Software Contable | [Facturación Electrónica SRI](https://www.sri.gob.ec/facturacion-electronica) | 2026 | 6 |
| **DOC-06** | Política de Uso Aceptable de Activos y Ciberseguridad (ISO 27002) | Seguridad de Información | [Norma ISO/IEC 27002](https://www.iso.org/standard/75652.html) | 2026 | 6 |
| **DOC-07** | Diagnóstico y Solución de Conexión a Internet y Red Cableada | Redes LAN Ethernet | [IEEE 802.3 Ethernet](https://standards.ieee.org/ieee/802.3/) | 2026 | 6 |
| **DOC-08** | Conexión Segura al Wi-Fi Corporativo y Red de Invitados | Redes Inalámbricas | [Wi-Fi Alliance Security](https://www.wi-fi.org/discover-wi-fi/security) | 2026 | 6 |
| **DOC-09** | Gestión de Antivirus Endpoint y Actualizaciones de Seguridad del SO | Ciberseguridad Endpoint | [Microsoft Threat Protection](https://learn.microsoft.com/es-es/windows/security/threat-protection/) | 2026 | 6 |
| **DOC-10** | Diagnóstico de Fallas en la Estación de Trabajo (PC / Laptop) | Soporte a Equipos | [Windows Client Troubleshooting](https://learn.microsoft.com/es-es/troubleshoot/windows-client/performance/) | 2026 | 6 |
| **DOC-11** | Guía de Configuración y Solución en Cliente de Correo Outlook | Correo y Productividad | [Microsoft Outlook Support](https://support.microsoft.com/es-es/office/configuracion-de-correo-outlook) | 2026 | 6 |
| **DOC-12** | Procedimiento para Solicitud de Nuevos Accesos y Alta de Personal | Onboarding / Identidad | [Azure AD Governance](https://learn.microsoft.com/es-es/azure/active-directory/governance/) | 2026 | 6 |
| **DOC-13** | Procedimiento de Respaldo y Recuperación de Archivos (VSS) | Continuidad de Negocio | [Microsoft File Recovery](https://support.microsoft.com/es-es/office/recuperar-versiones-anteriores) | 2026 | 6 |
| **DOC-14** | Configuración de Periféricos, Pantallas Múltiples y Docking Station | Puesto de Trabajo | [Windows Multi-Display Guide](https://support.microsoft.com/es-es/windows/como-usar-varios-monitores-en-windows) | 2026 | 6 |
| **DOC-15** | Matriz de Priorización ITIL y Protocolo de Escalamiento a Nivel 2 | Gestión de Incidentes | [AXELOS ITIL v4 Standard](https://www.axelos.com/certifications/itil-service-management) | 2026 | 6 |

---

## 4. Almacenamiento en el Repositorio
Todos los manuales residen en `data/raw/` como archivos Markdown estructurados:
```text
data/raw/
├── DOC-01_restablecimiento_contrasenas.md
├── DOC-02_configuracion_vpn_corporativa.md
├── DOC-03_impresoras_red_departamentales.md
├── DOC-04_acceso_carpetas_compartidas_smb.md
├── DOC-05_sistema_contable_erp.md
├── DOC-06_politica_seguridad_iso27002.md
├── DOC-07_conectividad_red_cableada_oficina.md
├── DOC-08_wifi_corporativo_credenciales.md
├── DOC-09_antivirus_actualizaciones_so.md
├── DOC-10_falla_estacion_trabajo_pc.md
├── DOC-11_configuracion_cliente_correo.md
├── DOC-12_solicitud_nuevos_accesos.md
├── DOC-13_respaldo_recuperacion_archivos.md
├── DOC-14_perifericos_pantallas_oficina.md
└── DOC-15_matriz_itil_gestion_incidentes.md
```
*(Total: 15 manuales, 90 fragmentos vectorizados y persistidos en ChromaDB en `data/chroma/`).*
