#!/usr/bin/env python

import os
from dotenv import load_dotenv

# Carga el archivo .env
load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")

variables = Settings()
