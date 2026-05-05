#!/usr/bin/env python
from pyrogram.client import Client
from pyrogram import filters
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from conexion.conexion import SessionLocal 
from src.agendar.repositorio_citas import RepositorioCitas
from src.autenticacion.autenticar import Autenticar
au = Autenticar()

# 1. Listar citas para cancelar
@Client.on_callback_query(filters.regex("^cancelar$"))
async def listar_citas_para_cancelar(client: Client, callback_query: CallbackQuery):
    datos_usuario = au.obtener_usuario(callback_query.from_user.id)
    
    if not datos_usuario:
        await callback_query.answer("⚠️ Sesión expirada. Por favor usa /start", show_alert=True)
        return

    paciente_id = datos_usuario["id_usuario"]

    db = SessionLocal()
    repo = RepositorioCitas(db)
    
    citas = repo.obtener_citas_paciente(paciente_id)

    if not citas:
        await callback_query.answer("No tienes citas para cancelar.", show_alert=True)
        return

    botones = []
    for cita in citas:
        fecha_str = cita.fecha_cita.strftime('%m/%d %H:%M')
        # El callback_data llevará el ID de la cita para procesarlo luego
        botones.append([InlineKeyboardButton(
            f"❌ Cita {fecha_str} - {cita.medico.usuario.primer_apellido}", 
            callback_data=f"conf_canc_{cita.id_cita}"
        )])

    db.close()
    await callback_query.message.edit_text(
        "🗑 **Selecciona la cita que deseas cancelar:**",
        reply_markup=InlineKeyboardMarkup(botones)
    )

# 2. Procesar la cancelación efectiva
@Client.on_callback_query(filters.regex(r"^conf_canc_(\d+)$"))
async def confirmar_cancelacion(client: Client, callback_query: CallbackQuery):
    cita_id = int(callback_query.matches[0].group(1))
    paciente_id = 2
    
    db = SessionLocal()
    repo = RepositorioCitas(db)
    
    exito = repo.cancelar_cita(cita_id, paciente_id)
    
    if exito:
        await callback_query.message.edit_text(f"✅ La cita con ID `{cita_id}` ha sido cancelada exitosamente.")
    else:
        await callback_query.answer("No se pudo cancelar la cita.", show_alert=True)
    db.close()
