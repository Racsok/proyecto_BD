#!/usr/bin/env python3

from datetime import datetime, timedelta
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler, CallbackQueryHandler
from src.database.conexion import SessionLocal
from src.repositories.repositorio_citas import RepositorioCitas
from src.keyboards.teclados import teclado_especialidades, teclado_medicos
from src.autenticacion.sesion import autenticador as au
from src.utils.logger import config_logger
from src.utils.menu_usuario import mostrar_menu_principal
from src.utils.horarios import generar_horas_disponibles

logger = config_logger(__name__)


# ESTADOS
SELECCION_ESPECIALIDAD = 1
SELECCION_MEDICO = 2
INGRESAR_FECHA = 3
SELECCION_HORA = 4

# INICIAR AGENDAMIENTO
async def iniciar_agendamiento(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    logger.info(f"Usuario {query.from_user.id} inició agendamiento")

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
            reply_markup=
            teclado_especialidades(
                especialidades
            )
        )

        return SELECCION_ESPECIALIDAD

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

            return SELECCION_ESPECIALIDAD

        await query.edit_message_text(
            "👨‍⚕️ Paso 2:\n\n"
            "Selecciona un médico:",
            reply_markup=
            teclado_medicos(
                medicos
            )
        )

        return SELECCION_MEDICO

    finally:
        db.close()

# VOLVER A ESPECIALIDADES
async def volver_especialidades(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    db = SessionLocal()

    try:
        repo = RepositorioCitas(db)

        especialidades = (
            repo.obtener_especialidades()
        )

        await query.edit_message_text(
            "⚕️ Paso 1:\n\n"
            "Selecciona una especialidad:",

            reply_markup=
            teclado_especialidades(
                especialidades
            )
        )

        return SELECCION_ESPECIALIDAD

    finally:
        db.close()

# PEDIR FECHA
async def pedir_fecha(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    medico_id = int(
        query.data.split("_")[1]
    )

    # Guardar médico
    context.user_data[
        "medico_id"
    ] = medico_id

    botones = []

    # Próximos 7 días
    for i in range(7):
        fecha = (
            datetime.now() +
            timedelta(days=i)
        ).strftime("%Y-%m-%d")

        botones.append([
            InlineKeyboardButton(
                text=fecha,
                callback_data=
                f"fecha_{fecha}"
            )
        ])

    await query.edit_message_text(
        "📅 Paso 3:\n\n"
        "Selecciona una fecha:",
        reply_markup=
        InlineKeyboardMarkup(
            botones
        )
    )

    return INGRESAR_FECHA

# PEDIR HORA
async def seleccionar_fecha(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    try:
        # Obtener fecha desde callback
        fecha = query.data.replace(
            "fecha_",
            ""
        )

        logger.info(f"Fecha seleccionada: {fecha}")

        # Guardar fecha temporalmente
        context.user_data[
            "fecha"
        ] = fecha

        # Obtener médico guardado
        medico_id = context.user_data[
            "medico_id"
        ]

        fecha_obj = datetime.strptime(
            fecha,
            "%Y-%m-%d"
        ).date()

        db = SessionLocal()

        try:
            repo = RepositorioCitas(db)

            # Consultar horas ocupadas
            horas_ocupadas = (
                repo.obtener_horas_ocupadas(
                    medico_id,
                    fecha_obj
                )
            )

            logger.info(f"Horas ocupadas: {horas_ocupadas}")

            # Generar horas libres
            horas_disponibles = (
                generar_horas_disponibles(
                    horas_ocupadas
                )
            )

            if not horas_disponibles:

                await query.edit_message_text(
                    "❌ No hay horarios "
                    "disponibles para "
                    "esa fecha."
                )

                return ConversationHandler.END

            # Crear botones dinámicos
            botones = []

            for hora in horas_disponibles:

                botones.append([
                    InlineKeyboardButton(
                        text=hora,
                        callback_data=
                        f"hora_{hora}"
                    )
                ])

            await query.edit_message_text(
                "🕐 Paso 4:\n\n"
                "Selecciona una hora:",
                reply_markup=
                InlineKeyboardMarkup(
                    botones
                )
            )

            return SELECCION_HORA

        finally:
            db.close()

    except Exception as e:

        logger.error(
            f"Error seleccionando fecha: {e}"
        )

        await query.edit_message_text(
            "❌ Error obteniendo "
            "horarios disponibles."
        )

        return ConversationHandler.END
    
# GUARDAR CITA
async def guardar_cita(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    try:
        # Obtener hora seleccionada
        hora = query.data.replace(
            "hora_",
            ""
        )

        # Obtener datos temporales
        fecha = context.user_data[
            "fecha"
        ]

        medico_id = context.user_data[
            "medico_id"
        ]

        # Construir datetime completo
        fecha_cita = datetime.strptime(
            f"{fecha} {hora}",
            "%Y-%m-%d %H:%M"
        )

        # Validar fecha futura
        if fecha_cita <= datetime.now():
            await query.edit_message_text(
                "❌ La fecha debe "
                "ser futura."
            )

            return ConversationHandler.END

        # Obtener usuario autenticado
        datos_usuario = au.obtener_usuario(
            update.effective_user.id
        )

        if not datos_usuario:
            await query.edit_message_text(
                "⚠️ Sesión expirada."
            )
            return ConversationHandler.END

        paciente_id = datos_usuario[
            "id_usuario"
        ]

        db = SessionLocal()

        try:
            repo = RepositorioCitas(db)

            # Crear cita
            cita = repo.crear_cita(
                paciente_id=paciente_id,
                medico_id=medico_id,
                fecha_cita=fecha_cita
            )

            await query.edit_message_text(
                "✅ ¡Cita agendada!\n\n"
                f"🗓 Fecha: "
                f"{cita.fecha_cita.strftime('%Y-%m-%d %H:%M')}\n"
                f"💰 Valor: "
                f"${cita.valor}"
            )

        finally:
            db.close()

        # Limpiar datos temporales
        context.user_data.clear()

        # Mostrar menú nuevamente
        await mostrar_menu_principal(
            query.message,
            datos_usuario["rol_id"]
        )

        return ConversationHandler.END

    except Exception as e:
        logger.error(f"Error guardando cita: {e}")

        await query.edit_message_text(
            "❌ Error agendando cita."
        )

        return ConversationHandler.END

# CANCELAR FLUJO
async def cancelar_flujo(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Obtener usuario autenticado
    datos_usuario = au.obtener_usuario(
        update.effective_user.id
    )

    if not datos_usuario:
        await query.message.reply_text(
            "⚠️ Sesión expirada."
        )

        return ConversationHandler.END

    query = update.callback_query

    await query.answer()

    await query.edit_message_text(
        "❌ Agendamiento cancelado."
    )

    await mostrar_menu_principal(
            query.message,
            datos_usuario["rol_id"]
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
        # SELECCIONAR ESPECIALIDAD
        SELECCION_ESPECIALIDAD: [
            CallbackQueryHandler(
                seleccionar_medico,
                pattern=r"^esp_\d+$"
            )
        ],
        # SELECCIONAR MÉDICO
        SELECCION_MEDICO: [
            CallbackQueryHandler(
                pedir_fecha,
                pattern=r"^med_\d+$"
            ),
            CallbackQueryHandler(
                volver_especialidades,
                pattern="^volver_especialidades$"
            )
        ],
        # INGRESAR FECHA
        INGRESAR_FECHA: [
            CallbackQueryHandler(
                seleccionar_fecha,
                pattern=r"^fecha_\d{4}-\d{2}-\d{2}$"
            )
        ],
        # SELECCIONAR HORA
        SELECCION_HORA: [
            CallbackQueryHandler(
                guardar_cita,
                pattern=r"^hora_\d{2}:\d{2}$"
            )
        ]
    },
    fallbacks=[
        CallbackQueryHandler(
            cancelar_flujo,
            pattern="^cancelar_flujo$"
        )
    ],
    per_message=False
)