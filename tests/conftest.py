import os
import tempfile
import pytest

# Configurar base de datos SQLite temporal y aislada para la suite de pruebas
# Evita contaminar la base de datos de producción con registros de test
_test_db_file = tempfile.NamedTemporaryFile(suffix="_test.db", delete=False)
_test_db_path = _test_db_file.name
_test_db_file.close()

os.environ["CONECTATEC_DB_PATH"] = _test_db_path

from app.database import inicializar_bd

@pytest.fixture(scope="session", autouse=True)
def aislar_base_datos_tests():
    """Inicializa el esquema en la base de datos temporal y la destruye al finalizar."""
    inicializar_bd()
    yield
    try:
        if os.path.exists(_test_db_path):
            os.remove(_test_db_path)
    except Exception:
        pass
