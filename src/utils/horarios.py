from datetime import datetime, timedelta


def generar_horas_disponibles(horas_ocupadas: list[str]):

    inicio = datetime.strptime(
        "08:00",
        "%H:%M"
    )

    fin = datetime.strptime(
        "17:00",
        "%H:%M"
    )

    horas_disponibles = []

    actual = inicio

    while actual < fin:

        hora = actual.strftime(
            "%H:%M"
        )

        if hora not in horas_ocupadas:

            horas_disponibles.append(
                hora
            )

        actual += timedelta(
            hours=1
        )

    return horas_disponibles