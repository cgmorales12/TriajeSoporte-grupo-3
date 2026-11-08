import sqlite3

con = sqlite3.connect("data/triaje_soporte.db")
con.execute(
    "UPDATE tickets SET nombre_cliente = ?, email_cliente = ? WHERE ticket_codigo = ?",
    ("Christian Morales (Coordinación Técnica - Puesto 01)", "christian.morales@empresa.com", "TCK-N01-AD")
)
con.execute(
    "UPDATE tickets SET nombre_cliente = ?, email_cliente = ? WHERE ticket_codigo = ?",
    ("Luis Fernando Ribera (Arquitectura de Software - Puesto 02)", "fernando.ribera@empresa.com", "TCK-E01-BSOD")
)
con.execute(
    "UPDATE tickets SET nombre_cliente = ?, email_cliente = ? WHERE ticket_codigo = ?",
    ("Amalia Geoconda Iguasnia (Aseguramiento de Calidad - Puesto 06)", "amalia.iguasnia@empresa.com", "TCK-R01-AD")
)
con.commit()
print("Tickets en BD local actualizados correctamente!")

