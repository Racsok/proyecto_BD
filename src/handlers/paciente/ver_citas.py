#!/usr/bin/env python3
from telegram import Update
from telegram.ext import ContextTypes, CallbackQueryHandler
from src.database.conexion import SessionLocal
from src.repositories.repositorio_citas import RepositorioCitas
from src.autenticacion.sesion import autenticador as au
from src.utils.logger import config_logger
from src.utils.menu_usuario import mostrar_menu_principal

logger = config_logger(__name__)


# MOSTRAR CITAS DEL PACIENTE
async def mostrar_citas_paciente(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    # Responder callback
    await query.answer()

    logger.info(
        f"Usuario {query.from_user.id} consultó sus citas")

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

        # AHORA USA LA VISTA
        citas = repo.obtener_citas_paciente(
            paciente_id
        )

        # Sin citas
        if not citas:
            logger.info("Usuario sin citas")

            await query.edit_message_text(
                "📋 No tienes "
                "citas programadas."
            )

            await mostrar_menu_principal(
                query.message,
                datos_usuario["rol_id"]
            )

            return

        logger.info(f"Total citas: {len(citas)}")

        # Construir respuesta
        lineas = [
            "🗓 Tus Citas Programadas:\n"
        ]

        for cita in citas:
            nombre_medico = (
                f"{cita.primer_nombre_medico} "
                f"{cita.primer_apellido_medico}"
            )

            lineas.append(
                f"👨‍⚕️ Médico: "
                f"{nombre_medico}\n"
                f"🩺 Especialidad: "
                f"{cita.especialidad}\n"
                f"🏥 Consultorio: "
                f"{cita.nombre_consultorio}\n"
                f"📅 Fecha: "
                f"{cita.fecha_cita.strftime('%Y-%m-%d %H:%M')}\n"
                f"💰 Valor: "
                f"${cita.valor}\n"
                f"──────────────────\n"
            )

        texto_citas = "\n".join(
            lineas
        )

        # Mostrar citas
        await query.edit_message_text(
            texto_citas
        )

        # Mostrar menú nuevamente
        await mostrar_menu_principal(
            query.message,
            datos_usuario["rol_id"]
        )

    except Exception as e:
        logger.error(f"Error mostrando citas: {e}")

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
ver_citas_paciente_handler = CallbackQueryHandler(
    mostrar_citas_paciente,
    pattern="^ver_citas_paciente$"
)