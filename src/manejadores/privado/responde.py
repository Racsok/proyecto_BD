#!/usr/bin/env python
from pyrogram import Client, filters

# Este decorador se activa con cualquier mensaje de texto 
# que no sea un comando y que se envíe por privado
@Client.on_message(filters.private)
async def respuesta_eco(bot, message):
    # message.text contiene lo que el usuario escribió
    texto_usuario = message.text
    
    # Respuesta amigable
    await message.reply_text(
        f"Recibí tu mensaje: **{texto_usuario}**\n\n"
        "Estoy procesando la información para el buscador..."
    )
