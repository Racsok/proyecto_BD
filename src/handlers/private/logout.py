#!/usr/bin/env python3

from telegram import Update
from telegram.ext import ContextTypes, CallbackQueryHandler
from src.autenticacion.sesion import autenticador as au
from src.utils.logger import config_logger

logger = config_logger(__name__)

# CERRAR SESIÓN
async def cerrar_sesion(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    telegram_id = query.from_user.id

    logger.info(f"Cerrando sesión usuario {telegram_id}")

    context.user_data.clear()

    au.cerrar_sesion(
        telegram_id
    )

    await query.edit_message_text(
        "👋 Sesión cerrada correctamente.\n\n"
        "Usa /start para volver a ingresar."
    )

# HANDLER EXPORTABLE
logout_handler = CallbackQueryHandler(
    cerrar_sesion,
    pattern="^logout$"
)