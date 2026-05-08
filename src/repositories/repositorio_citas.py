#!/usr/bin/env python3
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import Session
from src.models.entidades import Especialidad, Medico, Cita, Consultorio
from src.utils.logger import config_logger

logger = config_logger(__name__)
class RepositorioCitas:

    def __init__(self, db_session: Session):
        self.db = db_session

    # OBTENER ESPECIALIDADES
    def obtener_especialidades(self) -> list[Especialidad]:

        stmt = select(Especialidad)

        return list(
            self.db.scalars(stmt).all()
        )

    # OBTENER MÉDICOS POR ESPECIALIDAD
    def obtener_medicos_por_especialidad(self, especialidad_id: int) -> list[Medico]:

        stmt = (
            select(Medico).where(
                Medico.especialidad_id == especialidad_id
            )
        )

        return list(
            self.db.scalars(stmt).all()
        )
    
    # CREAR CITA
    def crear_cita(self, paciente_id: int, medico_id: int, fecha_cita: datetime) -> Cita:

        try:
            # Obtener consultorio disponible
            stmt = select(Consultorio)

            consultorio = self.db.scalar(stmt)

            if not consultorio:
                raise Exception(
                    "No existen consultorios"
                )

            # Crear cita
            nueva_cita = Cita(
                fecha_cita=fecha_cita,
                estado_cita="PROGRAMADA",
                valor=50000.00,
                medico_id=medico_id,
                paciente_id=paciente_id,
                consultorio_id=
                consultorio.id_consultorio
            )

            self.db.add(nueva_cita)

            self.db.commit()

            self.db.refresh(nueva_cita)

            logger.info(f"Cita creada: {nueva_cita.id_cita}")

            return nueva_cita

        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creando cita: {e}")
            raise

    
    # OBTENER CITAS DEL PACIENTE
    def obtener_citas_paciente(self, paciente_id: int) -> list[Cita]:

        stmt = (
            select(Cita)
            .where(
                Cita.paciente_id == paciente_id
            )
            .where(
                Cita.estado_cita == "PROGRAMADA"
            )
            .order_by(
                Cita.fecha_cita.asc()
            )
        )

        return list(
            self.db.scalars(stmt).all()
        )

    
    # OBTENER CITAS DEL MÉDICO
    def obtener_citas_medico(self, medico_id: int) -> list[Cita]:

        stmt = (
            select(Cita)
            .where(
                Cita.medico_id == medico_id
            )
            .where(
                Cita.estado_cita == "PROGRAMADA"
            )
            .order_by(
                Cita.fecha_cita.asc()
            )
        )

        return list(
            self.db.scalars(stmt).all()
        )

    
    # CANCELAR CITA
    def cancelar_cita(self, cita_id: int, paciente_id: int) -> bool:

        try:
            stmt = (
                select(Cita)
                .where(
                    Cita.id_cita == cita_id
                )
                .where(
                    Cita.paciente_id == paciente_id
                )
            )

            cita = self.db.scalar(stmt)

            if not cita:
                logger.warning(f"No se encontró la cita {cita_id}")
                return False

            cita.estado_cita = "CANCELADA"

            self.db.commit()

            logger.info(f"Cita cancelada: {cita_id}")

            return True

        except Exception as e:
            self.db.rollback()
            logger.error(f"Error cancelando cita: {e}")
            return False