#!/usr/bin/env python
from pyrogram.client import Client
from pyrogram import  filters
from pyrogram.types import CallbackQuery, ForceReply
from datetime import datetime

# Importa tu sesión de BD (ajusta según tu archivo de conexión)
from conexion.conexion import SessionLocal 
from src.agendar.repositorio_citas import RepositorioCitas
from src.utils.teclados import teclado_especialidades, teclado_medicos
from utils.logger import config_logger 

logger = config_logger(__name__)

# 1. Escuchar el botón "agendar" del menú principal
@Client.on_callback_query(filters.regex("^agendar$"))
async def iniciar_agendamiento(client: Client, callback_query: CallbackQuery):
    logger.info(f"Usuario {callback_query.from_user.id} inició proceso de agendamiento")
    
    db = SessionLocal()
    repo = RepositorioCitas(db)
    especialidades = repo.obtener_especialidades()
    
    await callback_query.message.edit_text(
        "⚕️ **Paso 1:** Por favor, selecciona la especialidad requerida:",
        reply_markup=teclado_especialidades(especialidades)
    )
    db.close()

# 2. Escuchar la selección de la especialidad (Regex captura "esp_1", "esp_2", etc.)
@Client.on_callback_query(filters.regex(r"^esp_(\d+)$"))
async def seleccionar_medico(client: Client, callback_query: CallbackQuery):
    # Extraemos el ID de la especialidad desde el callback_data
    especialidad_id = int(callback_query.matches[0].group(1))
    
    db = SessionLocal()
    repo = RepositorioCitas(db)
    medicos = repo.obtener_medicos_por_especialidad(especialidad_id)
    
    if not medicos:
        await callback_query.answer("No hay médicos disponibles para esta especialidad.", show_alert=True)
        return

    await callback_query.message.edit_text(
        "👨‍⚕️ **Paso 2:** Selecciona el especialista:",
        reply_markup=teclado_medicos(medicos)
    )
    db.close()

# 3. Escuchar la selección del médico y pedir la fecha
@Client.on_callback_query(filters.regex(r"^med_(\d+)$"))
async def seleccionar_fecha_hora(client: Client, callback_query: CallbackQuery):
    medico_id = int(callback_query.matches[0].group(1))
    
    # Eliminamos el teclado inline para limpiar el chat
    await callback_query.message.delete()
    
    # Usamos pyromod (chat.ask) para solicitar la fecha y hora
    respuesta_fecha = await callback_query.message.chat.ask(
        "📅 **Paso 3:** Escribe la fecha y hora de tu cita en formato `YYYY-MM-DD HH:MM`\n\n"
        "Ejemplo: `2026-05-20 14:30`",
        reply_markup=ForceReply(placeholder="2026-05-20 14:30")
    )
    
    try:
        # Validar y convertir la cadena de texto a un objeto datetime
        fecha_cita = datetime.strptime(respuesta_fecha.text, "%Y-%m-%d %H:%M")
        
        # OJO: Validar la restricción SQL chk_fecha_cita_valida (fecha_cita >= CURRENT_TIMESTAMP)
        if fecha_cita <= datetime.now():
            await respuesta_fecha.reply("❌ La fecha debe ser en el futuro. Intenta agendar nuevamente.")
            return

        db = SessionLocal()
        repo = RepositorioCitas(db)
        
        # NOTA: Debes obtener el paciente_id del usuario actual. 
        # Si guardaste el ID en tu clase Autenticar, úsalo aquí. Por ahora simulo el ID 1.
        paciente_id = 1 
        
        cita = repo.crear_cita(paciente_id=paciente_id, medico_id=medico_id, fecha_cita=fecha_cita)
        
        await respuesta_fecha.reply(
            f"✅ **¡Cita Agendada con Éxito!**\n\n"
            f"🆔 Número de cita: {cita.id_cita}\n"
            f"🗓 Fecha: {cita.fecha_cita.strftime('%Y-%m-%d %H:%M')}\n"
            f"💰 Valor: ${cita.valor}"
        )
        db.close()

    except ValueError:
        logger.error("Formato de fecha inválido")
        await respuesta_fecha.reply("❌ Formato de fecha incorrecto. Debes seguir el formato YYYY-MM-DD HH:MM.")
    except Exception as e:
        logger.error(f"Error al guardar la cita en DB: {e}")
        await respuesta_fecha.reply("❌ Ocurrió un error al agendar la cita. Por favor intenta más tarde.")


