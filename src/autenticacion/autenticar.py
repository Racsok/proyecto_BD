#!/usr/bin/env python3
from sqlalchemy import select
from src.models.entidades import Usuario
from src.database.conexion import SessionLocal
from src.utils.logger import config_logger

logger = config_logger(__name__)

class Autenticar:

    def __init__(self):
        # Usuarios autenticados en memoria
        #
        # {
        #   telegram_id: {
        #       id_usuario,
        #       id_medico?,
        #       rol_id,
        #       nombre,
        #       documento
        #   }
        # }
        #

        self.usuarios_activos: dict[int, dict] = {}

    # VALIDAR DOCUMENTO
    def validar_documento(self, telegram_id: int, documento: str) -> int:

        db = SessionLocal()

        try:
            logger.info(f"Validando documento: {documento}")

            stmt = select(Usuario).where(
                Usuario.numero_documento == documento
            )

            usuario = db.scalar(stmt)

            # Usuario no encontrado
            if not usuario:
                logger.warning(f"Documento {documento} no encontrado")
                return -1

            logger.info(f"Usuario encontrado: {usuario.primer_nombre} {usuario.primer_apellido}")

            # Construir sesión
            datos_sesion = {
                "id_usuario":
                usuario.id_usuario,
                "rol_id":
                usuario.rol.id_rol,
                "nombre": (f"{usuario.primer_nombre} {usuario.primer_apellido}"),
                "documento":
                usuario.numero_documento
            }

            # Si es médico guardar id_medico
            if usuario.medico:
                datos_sesion["id_medico"] = (
                    usuario.medico.id_medico
                )
                
                logger.info(f"ID médico asociado: {usuario.medico.id_medico}")

            # Guardar sesión
            self.usuarios_activos[telegram_id] = datos_sesion

            logger.info(f"Usuario autenticado: {telegram_id}")

            return usuario.rol.id_rol

        except Exception as e:
            logger.error(f"Error validando documento: {e}")
            return -1

        finally:
            db.close()

    # OBTENER USUARIO
    def obtener_usuario(self, telegram_id: int) -> dict | None:
        return self.usuarios_activos.get(
            telegram_id
        )

    # CERRAR SESIÓN
    def cerrar_sesion(self, telegram_id: int) -> bool:

        if telegram_id not in self.usuarios_activos:
            return False

        del self.usuarios_activos[
            telegram_id
        ]

        logger.info(f"Sesión cerrada para {telegram_id}")

        return True

    # VALIDAR SESIÓN
    def esta_autenticado(self, telegram_id: int) -> bool:
        return (
            telegram_id
            in self.usuarios_activos
        )