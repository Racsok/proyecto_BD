#!/usr/bin/env python

from typing import List, Optional
from datetime import date, datetime
from sqlalchemy import ForeignKey, String, Numeric, CheckConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class Rol(Base):
    __tablename__ = "roles"
    
    id_rol: Mapped[int] = mapped_column(primary_key=True)
    nombre_rol: Mapped[str] = mapped_column(String(50), nullable=False)
    
    # Restricción de check para los nombres de roles
    __table_args__ = (
        CheckConstraint(nombre_rol.in_(['PACIENTE', 'ADMINISTRATIVO', 'MEDICO']), name='check_rol_nombre'),
    )

    # Relación inversa
    usuarios: Mapped[List["Usuario"]] = relationship(back_populates="rol")

class Usuario(Base):
    __tablename__ = "usuarios"

    id_usuario: Mapped[int] = mapped_column(primary_key=True)
    primer_nombre: Mapped[str] = mapped_column(String(50))
    segundo_nombre: Mapped[Optional[str]] = mapped_column(String(50))
    primer_apellido: Mapped[str] = mapped_column(String(50))
    segundo_apellido: Mapped[Optional[str]] = mapped_column(String(50))
    tipo_documento: Mapped[str] = mapped_column(String(50))
    numero_documento: Mapped[str] = mapped_column(String(10), unique=True)
    correo: Mapped[Optional[str]] = mapped_column(String(100), unique=True)
    numero_telefono: Mapped[Optional[str]] = mapped_column(String(7))
    numero_celular: Mapped[Optional[str]] = mapped_column(String(10))
    fecha_nacimiento: Mapped[date] = mapped_column()
    departamento: Mapped[str] = mapped_column(String(100))
    municipio: Mapped[str] = mapped_column(String(100))
    direccion: Mapped[str] = mapped_column(String(200))
    
    rol_id: Mapped[int] = mapped_column(ForeignKey("roles.id_rol"))

    # Relaciones
    rol: Mapped["Rol"] = relationship(back_populates="usuarios")
    medico: Mapped[Optional["Medico"]] = relationship(back_populates="usuario")
    citas_como_paciente: Mapped[List["Cita"]] = relationship(back_populates="paciente")

class Especialidad(Base):
    __tablename__ = "especialidades"

    id_especialidad: Mapped[int] = mapped_column(primary_key=True)
    nombre_especialidad: Mapped[str] = mapped_column(String(100), unique=True)

    medicos: Mapped[List["Medico"]] = relationship(back_populates="especialidad")

class Medico(Base):
    __tablename__ = "medicos"

    id_medico: Mapped[int] = mapped_column(primary_key=True)
    fecha_ingreso: Mapped[date] = mapped_column()
    numero_tarjeta_profesional: Mapped[str] = mapped_column(String(10), unique=True)
    
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id_usuario"))
    especialidad_id: Mapped[int] = mapped_column(ForeignKey("especialidades.id_especialidad"))

    # Relaciones
    usuario: Mapped["Usuario"] = relationship(back_populates="medico")
    especialidad: Mapped["Especialidad"] = relationship(back_populates="medicos")
    citas: Mapped[List["Cita"]] = relationship(back_populates="medico")

class Consultorio(Base):
    __tablename__ = "consultorios"

    id_consultorio: Mapped[int] = mapped_column(primary_key=True)
    nombre_consultorio: Mapped[str] = mapped_column(String(100), unique=True)

class Cita(Base):
    __tablename__ = "citas"

    id_cita: Mapped[int] = mapped_column(primary_key=True)
    fecha_cita: Mapped[datetime] = mapped_column()
    estado_cita: Mapped[str] = mapped_column(String(50), server_default='PROGRAMADA')
    valor: Mapped[float] = mapped_column(Numeric(10))
    
    medico_id: Mapped[int] = mapped_column(ForeignKey("medicos.id_medico"))
    paciente_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id_usuario"))
    consultorio_id: Mapped[int] = mapped_column(ForeignKey("consultorios.id_consultorio"))

    # Relaciones
    medico: Mapped["Medico"] = relationship(back_populates="citas")
    paciente: Mapped["Usuario"] = relationship(back_populates="citas_como_paciente")
