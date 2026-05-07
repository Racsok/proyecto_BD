#!/usr/bin/env python3
from sqlalchemy import select
from src.models.entidades import Usuario
from src.database.conexion import SessionLocal
from src.utils.logger import config_logger


logger = config_logger(__name__)

class Autenticar:

    def __init__(self):
        # Usuarios autenticados en memoria
        # {telegram_id: datos_usuario}
        self.usuarios_activos: dict[int, dict] = {}

    def validar_documento(self, telegram_id: int,documento: str) -> int:

        db = SessionLocal()

        try:
            logger.info(f"Validando documento: {documento}")

            stmt = select(Usuario).where(
                Usuario.numero_documento == documento
            )

            usuario = db.scalar(stmt)

            if usuario:
                logger.info(f"Usuario encontrado: "f"{usuario.primer_nombre} "f"{usuario.primer_apellido}")

                # Guardar usuario autenticado en memoria
                self.usuarios_activos[telegram_id] = {
                    "id_usuario": usuario.id_usuario,
                    "rol_id": usuario.rol.id_rol,
                    "nombre": (
                        f"{usuario.primer_nombre} "
                        f"{usuario.primer_apellido}"
                    ),
                    "documento": usuario.numero_documento
                }

                return usuario.rol.id_rol

            logger.warning(f"Documento {documento} no encontrado")

            return -1

        except Exception as e:
            logger.error(
                f"Error validando documento: {e}"
            )
            return -1

        finally:
            db.close()

    def obtener_usuario(self,telegram_id: int) -> dict | None:
        return self.usuarios_activos.get(
            telegram_id
        )

    def cerrar_sesion(self,telegram_id: int) -> bool:
        if telegram_id in self.usuarios_activos:
            del self.usuarios_activos[telegram_id]

            logger.info(f"Sesión cerrada para "f"{telegram_id}")

            return True

        return False

    def esta_autenticado(self,telegram_id: int) -> bool:
        return telegram_id in self.usuarios_activos