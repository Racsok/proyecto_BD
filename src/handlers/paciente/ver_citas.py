#!/usr/bin/env python3
from telegram import Update
from telegram.ext import ContextTypes, CallbackQueryHandler
from src.database.conexion import SessionLocal
from src.repositories.repositorio_citas import RepositorioCitas
from src.autenticacion.sesion import autenticador as au
from src.utils.logger import config_logger


logger = config_logger(__name__)

# MOSTRAR CITAS DEL PACIENTE
async def mostrar_citas_paciente(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    # Obligatorio responder callback
    await query.answer()

    logger.info(f"Usuario {query.from_user.id} consultó sus citas")

    # Obtener usuario autenticado
    datos_usuario = au.obtener_usuario(
        query.from_user.id
    )

    if not datos_usuario:
        await query.answer(
            "⚠️ Sesión expirada. "
            "Usa /start",
            show_alert=True
        )

        return

    paciente_id = datos_usuario[
        "id_usuario"
    ]

    db = SessionLocal()

    try:
        repo = RepositorioCitas(db)

        citas = repo.obtener_citas_paciente(
            paciente_id
        )

        # Usuario sin citas
        if not citas:
            logger.info(
                "Usuario sin citas"
            )
            await query.edit_message_text(
                "📋 No tienes "
                "citas programadas."
            )
            return

        logger.info(f"Total citas: {len(citas)}")

        
        # Construir respuesta
        texto_citas = (
            "🗓 Tus Citas Programadas:\n\n"
        )

        for cita in citas:
            nombre_medico = (
                f"{cita.medico.usuario.primer_nombre} {cita.medico.usuario.primer_apellido}"
            )
            especialidad = (
                cita.medico
                .especialidad
                .nombre_especialidad
            )
            texto_citas += (
                f"👨‍⚕️ Médico: "
                f"{nombre_medico}\n"
                f"🩺 Especialidad: "
                f"{especialidad}\n"
                f"📅 Fecha: "
                f"{cita.fecha_cita.strftime('%Y-%m-%d %H:%M')}\n"
                f"📍 Estado: "
                f"{cita.estado_cita}\n"
                f"──────────────────\n"
            )

        # Mostrar citas
        await query.edit_message_text(
            texto_citas
        )

    except Exception as e:
        logger.error(
            f"Error mostrando citas: {e}"
        )
        await query.edit_message_text(
            "❌ Error obteniendo citas."
        )

    finally:
        db.close()

# HANDLER EXPORTABLE
ver_citas_paciente_handler = CallbackQueryHandler(
    mostrar_citas_paciente,
    pattern="^ver_citas_paciente$"
)