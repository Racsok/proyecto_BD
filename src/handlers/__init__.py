from src.handlers.callbacks.menu_citas_callback import menu_citas_handler
from src.handlers.private.start import conv_start
from src.handlers.private.agendar_citas import conv_agendar_cita
from src.handlers.private.ver_citas import ver_citas_handler
from src.handlers.private.cancelar_citas import cancelar_citas_handler, confirmar_cancelacion_handler


def registrar_handlers(app):

    # Conversaciones
    app.add_handler(conv_start)
    app.add_handler(conv_agendar_cita)
    app.add_handler(ver_citas_handler)
    app.add_handler(cancelar_citas_handler)
    app.add_handler(confirmar_cancelacion_handler)

    # Callbacks
    app.add_handler(menu_citas_handler)