#!/usr/bin/env python


from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def menu_citas():
    return InlineKeyboardMarkup([
        # Fila 1: Dos botones (50% de ancho cada uno)
        [
            InlineKeyboardButton("📅 Agendar Cita", callback_data="agendar"),
            InlineKeyboardButton("👁️ Ver Mis Citas", callback_data="ver_citas")
        ],
        [
            InlineKeyboardButton("❌ Cancelar Cita", callback_data="cancelar")
        ]
    ])
