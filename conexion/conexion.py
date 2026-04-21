#!/usr/bin/env python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.variables_entorno import variables

# Estructura de la URL: postgresql://usuario:contraseña@localhost:puerto/nombre_bd
DATABASE_URL = "postgresql://postgres:tu_password@localhost:5432/centro_medico"

engine = create_engine(variables.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Esto crea físicamente las tablas en tu base de datos si aún no existen
def init_db():
    # Ajustado a tu estructura: carpeta 'src' -> carpeta 'entidades' -> archivo 'entidades.py'
    from src.entidades.entidades import Base 
    Base.metadata.create_all(bind=engine)
