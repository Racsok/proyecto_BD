#!/usr/bin/env python3
from pyrogram.client import Client
from pyrogram import filters
from pyrogram.types import ForceReply

from src.autenticacion.autenticar import Autenticar
au = Autenticar()

from utils.logger import config_logger 

logger =config_logger(__name__)

@Client.on_message(filters.command("start") & filters.private)
async def start_privado(client, message):
    logger.info(f"Usuario {message.from_user.id} inició el bot")
    
    # Saludo inicial
    respuesta = await message.chat.ask(
        f"Hola {message.from_user.first_name} 👋, bienvenido al sistema de citas.\n\n"
        "Para comenzar con tu agendamiento, por favor **escribe tu número de documento**:",
        reply_markup=ForceReply(placeholder="Ej: 10203040")
    )   
    
    await client.send_message(
            chat_id=message.chat.id,
            text = au.validar_documento(respuesta.text)
            )


