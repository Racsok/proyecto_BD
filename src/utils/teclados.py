#!/usr/bin/env python
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def teclado_especialidades(especialidades):
    botones = []
    for esp in especialidades:
        # El callback_data llevará el prefijo 'esp_' seguido del ID
        botones.append([InlineKeyboardButton(esp.nombre_especialidad, callback_data=f"esp_{esp.id_especialidad}")])
    botones.append([InlineKeyboardButton("❌ Cancelar", callback_data="cancelar_flujo")])
    return InlineKeyboardMarkup(botones)

def teclado_medicos(medicos):
    botones = []
    for medico in medicos:
        # callback_data: 'med_' + ID del médico
        nombre_completo = f"Dr. {medico.usuario.primer_nombre} {medico.usuario.primer_apellido}"
        botones.append([InlineKeyboardButton(nombre_completo, callback_data=f"med_{medico.id_medico}")])
    botones.append([InlineKeyboardButton("⬅️ Volver", callback_data="agendar")])
    return InlineKeyboardMarkup(botones)
