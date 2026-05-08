#!/usr/bin/env python
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def menu_citas_paciente():
    return InlineKeyboardMarkup([
        # Fila 1: Dos botones (50% de ancho cada uno)
        [
            InlineKeyboardButton("📅 Agendar Cita", callback_data="agendar"),
            InlineKeyboardButton("👁️ Ver Mis Citas", callback_data="ver_citas_paciente")
        ],
        [
            InlineKeyboardButton("❌ Cancelar Cita", callback_data="cancelar")
        ],
        [
            InlineKeyboardButton(
                "🚪 Cerrar Sesión",
                callback_data="logout"
            )
        ]
    ])

def menu_citas_medico():
    return InlineKeyboardMarkup([
        # Fila 1: Un botón (100% de ancho)
        [
            InlineKeyboardButton("📋 Ver Citas Programadas", callback_data="ver_citas_medico")
        ],
        [
            InlineKeyboardButton(
                "🚪 Cerrar Sesión",
                callback_data="logout"
            )
        ]
    ])