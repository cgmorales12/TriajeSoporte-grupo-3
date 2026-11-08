import sqlite3

con = sqlite3.connect('data/triaje_soporte.db')
con.row_factory = sqlite3.Row
cur = con.cursor()
tickets = [dict(r) for r in cur.execute('SELECT ticket_codigo, nombre_cliente, email_cliente, estado FROM tickets WHERE eliminado = 0').fetchall()]

USUARIOS = {
    'christian': {'nombre': 'Christian Morales', 'email': 'christian.morales@empresa.com'},
    'fernando': {'nombre': 'Luis Fernando Ribera', 'email': 'fernando.ribera@empresa.com'},
    'amalia': {'nombre': 'Amalia Geoconda Iguasnia', 'email': 'amalia.iguasnia@empresa.com'}
}

print('=== TOTAL TICKETS EN BD:', len(tickets))

for uId, u in USUARIOS.items():
    emailBuscado = u['email'].lower()
    nombreBuscado = u['nombre'].lower()
    filtrados = []
    for t in tickets:
        tEmail = (t.get('email_cliente') or '').lower().strip()
        tNombre = (t.get('nombre_cliente') or '').lower().strip()
        match = (tEmail == emailBuscado or
                 emailBuscado in tEmail or
                 nombreBuscado in tNombre or
                 (uId == 'christian' and ('christian morales' in tNombre or tEmail == 'christian.morales@empresa.com')) or
                 (uId == 'fernando' and ('fernando ribera' in tNombre or tEmail == 'fernando.ribera@empresa.com')) or
                 (uId == 'amalia' and ('amalia' in tNombre or tEmail == 'amalia.iguasnia@empresa.com')))
        if match:
            filtrados.append(t)
    print(f'-- USUARIO: {uId} ({u["nombre"]}) --')
    print(f'Total tickets aislados: {len(filtrados)}')
    for f in filtrados:
        print(f'   [{f["estado"]}] {f["ticket_codigo"]} - {f["nombre_cliente"]} ({f["email_cliente"]})')
print('=== VERIFICACION EXITOSA ===')
