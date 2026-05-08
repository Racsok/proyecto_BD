#!/usr/bin/env python3
from telegram import (InlineKeyboardMarkup, InlineKeyboardButton)
from src.models.entidades import (Especialidad, Medico)


# TECLADO ESPECIALIDADES
def teclado_especialidades(especialidades: list[Especialidad]) -> InlineKeyboardMarkup:
    botones = []

    for esp in especialidades:
        botones.append([
            InlineKeyboardButton(
                text=esp.nombre_especialidad,
                callback_data=
                f"esp_{esp.id_especialidad}"
            )
        ])

    botones.append([
        InlineKeyboardButton(
            text="❌ Cancelar",
            callback_data="cancelar_flujo"
        )
    ])

    return InlineKeyboardMarkup(
        botones
    )


# TECLADO MÉDICOS
def teclado_medicos(medicos: list[Medico]) -> InlineKeyboardMarkup:
    botones = []

    for medico in medicos:
        nombre_completo = (
            f"Dr. {medico.usuario.primer_nombre} {medico.usuario.primer_apellido}"
        )

        botones.append([
            InlineKeyboardButton(
                text=nombre_completo,
                callback_data=
                f"med_{medico.id_medico}"
            )
        ])

    botones.append([
        InlineKeyboardButton(
            text="⬅️ Volver",
            callback_data="volver_especialidades"
        )
    ])

    return InlineKeyboardMarkup(
        botones
    )

# TECLADO DE HORAS
def teclado_horas(horas_disponibles: list[str]):

    botones = []

    for hora in horas_disponibles:
        botones.append([
            InlineKeyboardButton(
                text=hora,
                callback_data=
                f"hora_{hora}"
            )
        ])

    return InlineKeyboardMarkup(
        botones
    )