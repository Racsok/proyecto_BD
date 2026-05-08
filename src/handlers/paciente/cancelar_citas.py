#!/usr/bin/env python3

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes, CallbackQueryHandler
from src.database.conexion import SessionLocal
from src.repositories.repositorio_citas import RepositorioCitas
from src.autenticacion.sesion import autenticador as au
from src.utils.logger import config_logger
from src.utils.menu_usuario import mostrar_menu_principal

logger = config_logger(__name__)

# LISTAR CITAS PARA CANCELAR
async def listar_citas_para_cancelar(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    logger.info(f"Usuario {query.from_user.id} quiere cancelar citas")

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

    paciente_id = datos_usuario[
        "id_usuario"
    ]

    db = SessionLocal()

    try:
        repo = RepositorioCitas(db)

        citas = repo.obtener_citas_paciente(
            paciente_id
        )

        # Sin citas
        if not citas:
            await query.answer(
                "No tienes citas "
                "para cancelar.",
                show_alert=True
            )
            return

        
        # Construir botones
        botones = []

        for cita in citas:
            fecha_str = (
                cita.fecha_cita.strftime(
                    "%Y-%m-%d %H:%M"
                )
            )

            nombre_medico = (
                cita.medico
                .usuario
                .primer_apellido
            )

            botones.append([
                InlineKeyboardButton(
                    text=(
                        f"❌ {fecha_str} - "
                        f"Dr. {nombre_medico}"
                    ),
                    callback_data=
                    f"conf_canc_{cita.id_cita}"
                )
            ])

        # Mostrar lista
        await query.edit_message_text(
            "🗑 Selecciona la cita "
            "que deseas cancelar:",

            reply_markup=
            InlineKeyboardMarkup(botones)
        )

    except Exception as e:
        logger.error(f"Error listando citas: {e}")

        await query.edit_message_text(
            "❌ Error obteniendo citas."
        )

        await mostrar_menu_principal(
            query.message,
            datos_usuario["rol_id"]
        )

    finally:
        db.close()



# CONFIRMAR CANCELACIÓN
async def confirmar_cancelacion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    query = update.callback_query

    await query.answer()

    # Obtener ID cita
    cita_id = int(
        query.data.split("_")[2]
    )
    
    # Obtener usuario autenticado
    datos_usuario = au.obtener_usuario(
        query.from_user.id
    )

    if not datos_usuario:
        await query.answer(
            "⚠️ Sesión expirada",
            show_alert=True
        )
        return

    paciente_id = datos_usuario[
        "id_usuario"
    ]

    db = SessionLocal()

    try:
        repo = RepositorioCitas(db)
        exito = repo.cancelar_cita(
            cita_id=cita_id,
            paciente_id=paciente_id
        )

        # Cancelación exitosa
        if exito:
            logger.info(f"Cita cancelada: {cita_id}")

            await query.edit_message_text(
                f"✅ La cita ha sido cancelada."
            )

            await mostrar_menu_principal(
                query.message,
                datos_usuario["rol_id"]
            )

            return

        # No se pudo cancelar
        await query.answer(
            "No se pudo cancelar la cita.",
            show_alert=True
        )

        await mostrar_menu_principal(
            query.message,
            datos_usuario["rol_id"]
        )

    except Exception as e:
        logger.error(f"Error cancelando cita: {e}")

        await query.edit_message_text(
            "❌ Error cancelando cita."
        )

        await mostrar_menu_principal(
            query.message,
            datos_usuario["rol_id"]
        )

    finally:
        db.close()



# HANDLERS EXPORTABLES
cancelar_citas_handler = CallbackQueryHandler(
    listar_citas_para_cancelar,
    pattern="^cancelar$"
)

confirmar_cancelacion_handler = CallbackQueryHandler(
    confirmar_cancelacion,
    pattern=r"^conf_canc_\d+$"
)