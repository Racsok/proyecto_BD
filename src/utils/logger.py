#!/usr/bin/env python3
#PARA USAR HERRRAMIENTA LOGGING

import logging
import os

def config_logger(name, log_file="app.log", level=logging.DEBUG):
    #crear la carpeta
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_path = os.path.join(log_dir, log_file)

    #crear el logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    #Evita duplicar handlers
    if logger.handlers:
        return logger

    #Formato
    formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s')

    #handerl para archivo
    file_handler = logging.FileHandler(log_path, encoding="utf-8", mode="w")
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(formatter)

    #handler para consola
    consola_handler = logging.StreamHandler()
    consola_handler.setLevel(level)
    consola_handler.setFormatter(formatter)

    #Añadir handlers al logger
    logger.addHandler(file_handler)
    logger.addHandler(consola_handler)

    return logger
