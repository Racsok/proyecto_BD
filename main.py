#!/usr/bin/env python3
from src.configuracion import config
from utils.logger import config_logger 
from pyrogram.client import Client
import pyromod

logger = config_logger(__name__)


class TGBuscador:
    def __init__(self) -> None:
        plugins = dict(root="src.manejadores") #src.manejadores.privado
        self.bot = Client("TGBuscador", api_id=config.api_id, api_hash=config.api_hash, bot_token=config.bot_token, plugins=plugins)

    def run(self):
        self.bot.run()

if __name__ == "__main__":
    bot = TGBuscador()
    logger.info("Intentando conectar con Telegram...")
    try:
        bot.run()
    except Exception as e:
        logger.error(f"Error crítico durante la ejecución: {e}")
    logger.info("Aplicación finalizada")
