#!/usr/bin/env python

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from src.utils.logger import config_logger

logger = config_logger(__name__)
class Configuracion(BaseSettings):
    # tipo de variables
    bot_token: str = Field(default=...)

    # Lee el el archivo .env automaticamente
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

# Se crea una instancia
logger.info(f"Variables de entorno cargadas correctamente.")
config = Configuracion()
