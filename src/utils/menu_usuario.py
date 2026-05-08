#!/usr/bin/env python3

from src.keyboards.btn_menu_citas import menu_citas_medico, menu_citas_paciente

async def mostrar_menu_principal(mensaje, rol_id: int):

    if rol_id == 1:
        await mensaje.reply_text(
            "¿Qué deseas hacer ahora?",
            reply_markup=menu_citas_paciente()
        )

    elif rol_id == 3:
        await mensaje.reply_text(
            "¿Qué deseas hacer ahora?",
            reply_markup=menu_citas_medico()
        )