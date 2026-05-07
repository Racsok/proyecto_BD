#!/usr/bin/env python3

from telegram import Update
from telegram.ext import ContextTypes,CallbackQueryHandler
from src.utils.logger import config_logger


logger = config_logger(__name__)

# CALLBACK DEL MENÚ PRINCIPAL
async def menu_citas_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    # Obligatorio responder callback
    await query.answer()

    logger.info(f"Callback recibido: {query.data}")

    match query.data:

        # AGENDAR
        case "agendar":
            await query.edit_message_text(
                "📅 Vamos a agendar tu cita."
            )

        # VER CITAS
        case "ver_citas":
            await query.edit_message_text(
                "👁️ Estas son tus citas."
            )

        # CANCELAR
        case "cancelar":
            await query.edit_message_text(
                "❌ ¿Qué cita deseas cancelar?"
            )

        # CALLBACK NO RECONOCIDO
        case _:
            logger.warning(f"Callback desconocido: {query.data}")

            await query.edit_message_text(
                "⚠️ Opción no válida."
            )


# HANDLER EXPORTABLE
menu_citas_handler = CallbackQueryHandler(
    menu_citas_callback
)