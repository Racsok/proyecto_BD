#!/usr/bin/env python

# src/base_datos/crud_citas.py
from sqlalchemy.orm import Session
from src.entidades.entidades import Especialidad, Medico, Cita, Consultorio 
from datetime import datetime

class RepositorioCitas:
    def __init__(self, db_session: Session):
        self.db = db_session

    def obtener_especialidades(self):
        return self.db.query(Especialidad).all()

    def obtener_medicos_por_especialidad(self, especialidad_id: int):
        return self.db.query(Medico).filter(Medico.especialidad_id == especialidad_id).all()

    def crear_cita(self, paciente_id: int, medico_id: int, fecha_cita: datetime) -> Cita:
        # Asignamos un consultorio por defecto para el ejemplo (o puedes buscar el asignado al médico)
        consultorio = self.db.query(Consultorio).first() 
        
        nueva_cita = Cita(
            fecha_cita=fecha_cita,
            estado_cita='PROGRAMADA',
            valor=50000.0, # Valor quemado para el ejemplo, ajustable a tu lógica
            medico_id=medico_id,
            paciente_id=paciente_id,
            consultorio_id=consultorio.id_consultorio
        )
        self.db.add(nueva_cita)
        self.db.commit()
        self.db.refresh(nueva_cita)
        return nueva_cita
