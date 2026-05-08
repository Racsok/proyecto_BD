from src.handlers.private.start import conv_start
from src.handlers.paciente.agendar_citas import conv_agendar_cita
from src.handlers.paciente.ver_citas import ver_citas_paciente_handler
from src.handlers.medico.ver_citas import ver_citas_medico_handler
from src.handlers.paciente.cancelar_citas import cancelar_citas_handler, confirmar_cancelacion_handler
from src.handlers.private.logout import logout_handler


def registrar_handlers(app):

    # Conversaciones
    app.add_handler(conv_start)

    # Conversaciones paciente
    app.add_handler(conv_agendar_cita)
    app.add_handler(ver_citas_paciente_handler)
    app.add_handler(cancelar_citas_handler)
    app.add_handler(confirmar_cancelacion_handler)

    # Conversaciones médico
    app.add_handler(ver_citas_medico_handler)

    # Otros handlers globales 
    app.add_handler(logout_handler)
