#!/usr/bin/env python3
from pyrogram.client import Client
from pyrogram import filters
from pyrogram.types import ForceReply

from utils.logger import config_logger 

logger =config_logger(__name__)

@Client.on_message(filters.command("start") & filters.private)
async def start_privado(client, message):
    logger.info(f"Usuario {message.from_user.id} inició el bot")
    
    # Saludo inicial
    texto_bienvenida = (
        f"Hola {message.from_user.first_name} 👋, bienvenido al sistema de citas.\n\n"
        "Para comenzar con tu agendamiento, por favor **escribe tu número de documento**:"
    )
    
    # Usamos ForceReply para que el bot "espere" la respuesta a este mensaje
    await message.reply_text(
        text=texto_bienvenida,
        reply_markup=ForceReply(placeholder="Ej: 10203040")
    )


# Este manejador captura la respuesta al mensaje anterior
@Client.on_message(filters.private & filters.reply)
async def capturar_documento(client, message):
    # Verificamos que el usuario esté respondiendo al mensaje del documento
    if "escribe tu número de documento" in message.reply_to_message.text:
        documento = message.text
        
        if documento.isdigit():
            # Aquí es donde luego conectarás con la DB de tus compañeros
            await message.reply_text(
                f"✅ Documento {documento} recibido.\n\n"
                "Ahora, ¿para qué **especialidad** deseas agendar?"
            )
            # Aquí saltaremos al paso de los botones de especialidades
        else:
            await message.reply_text(
                "❌ Error: El documento debe contener solo números. Inténtalo de nuevo enviando /start",
                reply_markup=ForceReply(placeholder="Solo números")
            )
