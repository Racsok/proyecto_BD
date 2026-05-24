#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.config.variables_entorno import variables

# Engine de conexión
engine = create_engine(variables.DATABASE_URL, pool_pre_ping=True)

# Sesiones de base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependencia / helper para obtener sesión
def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()