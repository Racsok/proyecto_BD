#!/usr/bin/env python3

from telegram import Update
from telegram.ext import ContextTypes, CallbackQueryHandler
from src.database.conexion import SessionLocal
from src.repositories.repositorio_citas import RepositorioCitas
from src.autenticacion.sesion import autenticador as au
from src.utils.logger import config_logger
from src.utils.menu_usuario import mostrar_menu_principal

logger = config_logger(__name__)

# MOSTRAR CITAS DEL MÉDICO
async def mostrar_citas_medico(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    query = update.callback_query

    await query.answer()

    logger.info(f"Usuario {query.from_user.id} consultó sus citas")

    # Obtener usuario autenticado
    datos_usuario = au.obtener_usuario(
        query.from_user.id
    )

    if not datos_usuario:
        await query.answer(
            "⚠️ Sesión expirada.\n"
            "Usa /start",

            show_alert=True
        )
        return

    # Obtener ID médico
    medico_id = datos_usuario["id_medico"]

    db = SessionLocal()

    try:
        repo = RepositorioCitas(db)

        citas = repo.obtener_citas_medico(
            medico_id
        )

        # Sin citas
        if not citas:
            logger.info("Médico sin citas")

            await query.edit_message_text(
                "📋 No tienes citas programadas."
            )
            await mostrar_menu_principal(
                query.message,
                datos_usuario["rol_id"]
            )
            return

        logger.info(f"Total citas: {len(citas)}")

        # Construir respuesta
        texto_citas = (
            "🗓 Tus Citas Programadas:\n\n"
        )

        for cita in citas:
            # Nombre paciente
            nombre_paciente = (
                f"{cita.paciente.primer_nombre} {cita.paciente.primer_apellido}"
            )

            # Especialidad
            especialidad = (
                cita.medico
                .especialidad
                .nombre_especialidad
            )

            texto_citas += (
                f"🧑 Paciente: "
                f"{nombre_paciente}\n"
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

        await mostrar_menu_principal(
            query.message,
            datos_usuario["rol_id"]
        )

    except Exception as e:
        logger.error(
            f"Error mostrando citas: {e}"
        )
        await query.edit_message_text(
            "❌ Error obteniendo citas."
        )

        await mostrar_menu_principal(
            query.message,
            datos_usuario["rol_id"]
        )

    finally:
        db.close()



# HANDLER EXPORTABLE
ver_citas_medico_handler = CallbackQueryHandler(
    mostrar_citas_medico,
    pattern="^ver_citas_medico$"
)