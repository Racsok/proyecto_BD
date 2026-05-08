#!/usr/bin/env python3

from telegram import Update
from telegram.ext import ContextTypes, CallbackQueryHandler
from src.database.conexion import SessionLocal
from src.repositories.repositorio_citas import RepositorioCitas
from src.autenticacion.sesion import autenticador as au
from src.utils.logger import  config_logger
from src.utils.menu_usuario import mostrar_menu_principal

logger = config_logger(__name__)


# VER REPORTE CITAS COMPLETADAS
async def ver_reporte_citas_completadas(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    logger.info(f"Admin {query.from_user.id} consultó reporte")

    # VALIDAR SESIÓN
    datos_usuario = au.obtener_usuario(
        query.from_user.id
    )

    if not datos_usuario:
        await query.answer(
            "⚠️ Sesión expirada.",
            show_alert=True
        )
        return

    # VALIDAR ROL ADMIN
    if datos_usuario["rol_id"] != 2:
        await query.answer(
            "⛔ No autorizado.",
            show_alert=True
        )
        return

    db = SessionLocal()

    try:
        repo = RepositorioCitas(db)

        reportes = (
            repo.obtener_reporte_citas_completadas()
        )

        # SIN DATOS
        if not reportes:
            await query.edit_message_text(
                "📋 No existen "
                "citas completadas."
            )

            await mostrar_menu_principal(
                query.message,
                datos_usuario["rol_id"]
            )

            return

        logger.info(f"Total reportes: {len(reportes)}")

        texto = (
            "📊 REPORTE CITAS "
            "COMPLETADAS\n\n"
        )

        for reporte in reportes:

            nombre_medico = (
                f"{reporte.primer_nombre_medico} "
                f"{reporte.primer_apellido_medico}"
            )

            nombre_paciente = (
                f"{reporte.primer_nombre_paciente} "
                f"{reporte.primer_apellido_paciente}"
            )

            texto += (
                f"👨‍⚕️ Médico: "
                f"{nombre_medico}\n"
                f"🩺 Especialidad: "
                f"{reporte.especialidad}\n"
                f"🪪 TP: "
                f"{reporte.numero_tarjeta_profesional}\n\n"
                f"🧑 Paciente: "
                f"{nombre_paciente}\n"
                f"📄 Documento: "
                f"{reporte.tipo_documento_paciente} "
                f"{reporte.numero_documento_paciente}\n\n"
                f"📅 Fecha: "
                f"{reporte.fecha_cita.strftime('%Y-%m-%d %H:%M')}\n"
                f"💰 Valor: "
                f"${reporte.valor}\n"
                f"──────────────────\n"
            )

        # Telegram tiene límite ~4096 chars
        if len(texto) > 4000:
            texto = texto[:3900] + "\n..."

        await query.edit_message_text(
            texto
        )

        # Mostrar menú nuevamente
        await mostrar_menu_principal(
            query.message,
            datos_usuario["rol_id"]
        )

    except Exception as e:
        logger.error(f"Error generando reporte: {e}")

        await query.edit_message_text(
            "❌ Error obteniendo "
            "reporte."
        )

        await mostrar_menu_principal(
            query.message,
            datos_usuario["rol_id"]
        )

    finally:
        db.close()


# HANDLER EXPORTABLE
reporte_citas_completadas_handler = (
    CallbackQueryHandler(
        ver_reporte_citas_completadas,
        pattern="^reporte_citas_completadas$"
    )
)