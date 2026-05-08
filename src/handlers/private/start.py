from telegram import Update,ForceReply
from telegram.ext import ContextTypes,ConversationHandler,CommandHandler,MessageHandler,filters
from src.keyboards.btn_menu_citas import menu_admin, menu_citas_paciente, menu_citas_medico
from src.autenticacion.sesion import autenticador as au
from src.utils.logger import config_logger

logger = config_logger(__name__)

# Estados de conversación
DOCUMENTO = 1
PASSWORD_ADMIN = 2

# INICIAR CONVERSACIÓN
async def start_privado(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Cerrar sesión previa
    au.cerrar_sesion(
        update.effective_user.id
    )

    await update.message.reply_text(
        f"Hola {update.effective_user.first_name} 👋, "
        "bienvenido al sistema de citas.\n\n"
        "Para comenzar con el servicio, "
        "por favor escribe tu número de documento:",
        reply_markup=ForceReply(
            input_field_placeholder="Ej: 1020304050"
        )
    )

    return DOCUMENTO

# RECIBIR DOCUMENTO Y VALIDAR USUARIO
async def recibir_documento(update: Update, context: ContextTypes.DEFAULT_TYPE):

    documento = update.message.text

    tipo_cliente = au.validar_documento(
        update.effective_user.id,
        documento
    )

    logger.info(f"tipo cliente {tipo_cliente} tipodato {type(tipo_cliente)}")

    # Validar tipo de cliente y responder
    match tipo_cliente:

        # PACIENTE
        case 1:  
            usuario = au.obtener_usuario(
                update.effective_user.id
            )

            await update.message.reply_text(
                f"✅ ¡Bienvenido {usuario['nombre']}! "
                "¿Qué deseas hacer hoy?",
                reply_markup=menu_citas_paciente()
            )
            return ConversationHandler.END
        
        # ADMINISTRATIVO
        case 99:
            await update.message.reply_text(
                "🔐 Usuario administrativo "
                "detectado.\n\n"
                "Por favor escribe "
                "tu contraseña:",
                reply_markup=ForceReply(
                    input_field_placeholder=
                    "Contraseña"
                )
            )
            return PASSWORD_ADMIN

        # MÉDICO
        case 3:
            usuario = au.obtener_usuario(
                update.effective_user.id
            )
            await update.message.reply_text(
                f"✅ ¡Bienvenido Dr. {usuario['nombre']}! "
                "¿Qué deseas hacer hoy?",
                reply_markup=menu_citas_medico()
            )
            return ConversationHandler.END

        # NINGUNO O DESCONOCIDO
        case _:
            await update.message.reply_text(
                "❌ Documento no válido. Por favor, intenta de nuevo."
            )
            return DOCUMENTO

# VALIDAR PASSWORD ADMIN
async def validar_password_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):

    password = update.message.text.strip()

    valido = au.validar_password_admin(
        update.effective_user.id,
        password
    )

    if not valido:
        await update.message.reply_text(
            "❌ Contraseña incorrecta.\n\n"
            "Intenta nuevamente:"
        )
        return PASSWORD_ADMIN

    usuario = au.obtener_usuario(
        update.effective_user.id
    )

    await update.message.reply_text(
        f"✅ Bienvenido "
        f"{usuario['nombre']}.\n\n"
        "¿Qué deseas hacer hoy?",
        reply_markup=menu_admin()
    )

    return ConversationHandler.END

# Handler completo de conversación
conv_start = ConversationHandler(
    entry_points=[
        CommandHandler("start", start_privado)
    ],
    states={
        DOCUMENTO: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                recibir_documento
            )
        ],
         PASSWORD_ADMIN: [
            MessageHandler(
                filters.TEXT &
                ~filters.COMMAND,
                validar_password_admin
            )
        ]
    },
    fallbacks=[],
    per_message=False
)

