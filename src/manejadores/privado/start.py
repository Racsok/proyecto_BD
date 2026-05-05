#!/usr/bin/env python3
from pyrogram.client import Client
from pyrogram import filters
from pyrogram.types import ForceReply

from src.utils.btn_menu_citas import menu_citas
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
    tipo_cliente = au.validar_documento(message.from_user.id, respuesta.text)
    logger.info(f"tipo cliente {tipo_cliente} tipodato {type(tipo_cliente)}")
    match tipo_cliente:
        case 1: # PACIENTE
            await message.reply(
                f"✅ ¡Bienvenido {au.obtener_usuario(message.from_user.id)['nombre']}! ¿Qué deseas hacer hoy?",
                reply_markup=menu_citas()             
            )
    





