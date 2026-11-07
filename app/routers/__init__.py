"""
Módulo de enrutadores modulares de FastAPI - Triaje Automático de Solicitudes de Soporte Tecnológico para una PYME
"""
from app.routers.tickets import router as tickets_router
from app.routers.salud import router as salud_router
from app.routers.auth import router as auth_router
from app.routers.manuales import router as manuales_router
from app.routers.principal import router as principal_router

__all__ = ["tickets_router", "salud_router", "auth_router", "manuales_router", "principal_router"]

