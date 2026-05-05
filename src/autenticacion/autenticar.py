
#!/usr/bin/env python3
from pyrogram.types.messages_and_media import document
from sqlalchemy.orm import Session
from sqlalchemy import select
from src.entidades.entidades import Usuario 
from conexion.conexion import SessionLocal
from utils.logger import config_logger

logger =config_logger(__name__)


class SingletonMeta(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Autenticar(metaclass=SingletonMeta):
    def __init__(self):
        # Diccionario para guardar {telegram_id: objeto_usuario}
        self.usuarios_activos = {}


    def validar_documento(self, telegram_id: int, documento: str):
        db = SessionLocal()
        try:
            # Buscamos el primer usuario que coincida con el número de documento
            logger.info(f"se esta validando el id {documento}")
            usuario = db.query(Usuario).filter(Usuario.numero_documento == documento).first()

            if usuario:
                logger.info(f"Usuario encontrado: {usuario.primer_nombre}, Rol: {usuario.rol.nombre_rol}")
                
                # GUARDAR EN SESIÓN: Vinculamos el ID de Telegram con los datos de DB
                self.usuarios_activos[telegram_id] = {
                    "id_usuario": usuario.id_usuario,
                    "rol_id": usuario.rol.id_rol,
                    "nombre": usuario.primer_nombre
                }
                return usuario.rol.id_rol
            
            logger.warning(f"Documento {documento} no encontrado en la base de datos.")
            return -1 # Usuario no encontrado
        finally:
            db.close()

    def obtener_usuario(self, telegram_id: int):
        return self.usuarios_activos.get(telegram_id)


