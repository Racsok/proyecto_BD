
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
    def validar_documento(self, documento: str):
        db = SessionLocal()
        try:
            # Buscamos el primer usuario que coincida con el número de documento
            logger.info(f"se esta validando el id {documento}")
            usuario = db.query(Usuario).filter(Usuario.numero_documento == documento).first()
        
            if usuario:
                return "eres cliente"
        
            return "no eres cliente"
        finally:
            db.close()


