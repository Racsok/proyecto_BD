#!/usr/bin/env python3

from datetime import datetime
from telegram import Update, ForceReply
from telegram.ext import ContextTypes, ConversationHandler, CallbackQueryHandler, MessageHandler, filters
from src.database.conexion import SessionLocal
from src.repositories.repositorio_citas import RepositorioCitas
from src.keyboards.teclados import teclado_especialidades, teclado_medicos
from src.autenticacion.sesion import autenticador as au
from src.utils.logger import config_logger


logger = config_logger(__name__)

# ESTADOS
SELECCION_MEDICO = 1
INGRESAR_FECHA = 2


# INICIAR AGENDAMIENTO
async def iniciar_agendamiento(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    logger.info(f"Usuario {query.from_user.id} "f"inició agendamiento")

    datos_usuario = au.obtener_usuario(
        query.from_user.id
    )

    if not datos_usuario:
        await query.answer(
            "⚠️ Sesión expirada",
            show_alert=True
        )

        return ConversationHandler.END

    db = SessionLocal()

    try:
        repo = RepositorioCitas(db)

        especialidades = (
            repo.obtener_especialidades()
        )

        await query.edit_message_text(
            "⚕️ Paso 1:\n\n"
            "Selecciona una especialidad:",
            reply_markup=teclado_especialidades(
                especialidades
            )
        )

        return SELECCION_MEDICO

    finally:
        db.close()



# SELECCIONAR MÉDICO
async def seleccionar_medico(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    especialidad_id = int(
        query.data.split("_")[1]
    )

    db = SessionLocal()

    try:
        repo = RepositorioCitas(db)

        medicos = (
            repo.obtener_medicos_por_especialidad(
                especialidad_id
            )
        )

        if not medicos:

            await query.answer(
                "No hay médicos disponibles",
                show_alert=True
            )

            return SELECCION_MEDICO

        await query.edit_message_text(
            "👨‍⚕️ Paso 2:\n\n"
            "Selecciona un médico:",
            reply_markup=teclado_medicos(
                medicos
            )
        )

        return INGRESAR_FECHA

    finally:
        db.close()



# PEDIR FECHA
async def pedir_fecha(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    medico_id = int(
        query.data.split("_")[1]
    )

    context.user_data["medico_id"] = medico_id

    await query.message.reply_text(
        "📅 Paso 3:\n\n"
        "Escribe la fecha y hora "
        "en formato:\n\n"
        "YYYY-MM-DD HH:MM\n\n"
        "Ejemplo:\n"
        "2026-05-20 14:30",
        reply_markup=ForceReply(
            input_field_placeholder=
            "2026-05-20 14:30"
        )
    )

    return INGRESAR_FECHA



# GUARDAR CITA
async def guardar_cita(update: Update, context: ContextTypes.DEFAULT_TYPE):

    texto_fecha = update.message.text

    try:

        fecha_cita = datetime.strptime(
            texto_fecha,
            "%Y-%m-%d %H:%M"
        )

        if fecha_cita <= datetime.now():

            await update.message.reply_text(
                "❌ La fecha debe "
                "ser futura."
            )

            return INGRESAR_FECHA

        datos_usuario = au.obtener_usuario(
            update.effective_user.id
        )

        paciente_id = datos_usuario[
            "id_usuario"
        ]

        medico_id = context.user_data[
            "medico_id"
        ]

        db = SessionLocal()

        try:

            repo = RepositorioCitas(db)

            cita = repo.crear_cita(
                paciente_id=paciente_id,
                medico_id=medico_id,
                fecha_cita=fecha_cita
            )

            await update.message.reply_text(
                "✅ ¡Cita agendada!\n\n"
                f"🆔 ID: {cita.id_cita}\n"
                f"🗓 Fecha: "
                f"{cita.fecha_cita.strftime('%Y-%m-%d %H:%M')}\n"
                f"💰 Valor: ${cita.valor}"
            )

        finally:
            db.close()

        return ConversationHandler.END

    except ValueError:

        logger.error(
            "Formato de fecha inválido"
        )

        await update.message.reply_text(
            "❌ Formato inválido.\n\n"
            "Usa:\n"
            "YYYY-MM-DD HH:MM"
        )

        return INGRESAR_FECHA

    except Exception as e:

        logger.error(
            f"Error guardando cita: {e}"
        )

        await update.message.reply_text(
            "❌ Error agendando cita."
        )

        return ConversationHandler.END



# CONVERSATION HANDLER
conv_agendar_cita = ConversationHandler(
    entry_points=[

        CallbackQueryHandler(
            iniciar_agendamiento,
            pattern="^agendar$"
        )
    ],

    states={
        SELECCION_MEDICO: [

            CallbackQueryHandler(
                seleccionar_medico,
                pattern=r"^esp_\d+$"
            )
        ],
        INGRESAR_FECHA: [

            CallbackQueryHandler(
                pedir_fecha,
                pattern=r"^med_\d+$"
            ),

            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                guardar_cita
            )
        ]
    },
    fallbacks=[],
    per_message=False
)