#!/usr/bin/env python
from pyrogram.client import Client
from pyrogram import filters
from pyrogram.types import CallbackQuery
from conexion.conexion import SessionLocal 
from src.agendar.repositorio_citas import RepositorioCitas
from utils.logger import config_logger 
from src.autenticacion.autenticar import Autenticar
au = Autenticar()

logger = config_logger(__name__)

@Client.on_callback_query(filters.regex("^ver_citas$"))
async def mostrar_citas_paciente(client: Client, callback_query: CallbackQuery):
    logger.info(f"Usuario {callback_query.from_user.id} consultó sus citas")
    
    datos_usuario = au.obtener_usuario(callback_query.from_user.id)
    
    if not datos_usuario:
        await callback_query.answer("⚠️ Sesión expirada. Por favor usa /start", show_alert=True)
        return

    paciente_id = datos_usuario["id_usuario"]

    db = SessionLocal()
    repo = RepositorioCitas(db)
    
    citas = repo.obtener_citas_paciente(paciente_id)

    if not citas:
        logger.info("El usuario no tiene citas")
        await callback_query.message.edit_text(
            "📋 No tienes citas programadas actualmente.",
            reply_markup=None
        )
        return
    logger.info("El usuario tiene citas")

    texto_citas = "🗓 **Tus Citas Programadas:**\n\n"
    for cita in citas:
        # Accedemos a la relación médico -> usuario para obtener el nombre
        nombre_medico = f"{cita.medico.usuario.primer_nombre} {cita.medico.usuario.primer_apellido}"
        especialidad = cita.medico.especialidad.nombre_especialidad
        
        texto_citas += (
            f"🆔 **ID:** `{cita.id_cita}`\n"
            f"👨‍⚕️ **Médico:** {nombre_medico} ({especialidad})\n"
            f"📅 **Fecha:** {cita.fecha_cita.strftime('%Y-%m-%d %H:%M')}\n"
            f"📍 **Estado:** {cita.estado_cita}\n"
            f"----------------------------\n"
        )
    db.close()

    await callback_query.message.edit_text(texto_citas)
