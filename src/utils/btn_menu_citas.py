#!/usr/bin/env python
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def menu_citas():
    return InlineKeyboardMarkup([
        # Fila 1: Dos botones (50% de ancho cada uno)
        [
            InlineKeyboardButton("📅 Agendar Cita", callback_data="agendar"),
            InlineKeyboardButton("ℹ️ Información", callback_data="info_cita")
        ],
        # Fila 2: Un solo botón (Ocupará el 100% del ancho)
        [
            InlineKeyboardButton("❌ Cancelar Cita", callback_data="cancelar")
        ]
    ])
