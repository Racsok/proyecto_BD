#!/usr/bin/env python3

from typing import List, Optional
from datetime import date, datetime
from sqlalchemy import String, Numeric, ForeignKey, CheckConstraint, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


# BASE
class Base(DeclarativeBase):
    pass


# ROLES
class Rol(Base):

    __tablename__ = "roles"

    id_rol: Mapped[int] = mapped_column(primary_key=True)
    nombre_rol: Mapped[str] = mapped_column(String(50), nullable=False)

    __table_args__ = (
        CheckConstraint(
            "nombre_rol IN ('PACIENTE', 'ADMINISTRATIVO', 'MEDICO')",
            name="chk_roles_validos"
        ),
    )

    # Relaciones
    usuarios: Mapped[List["Usuario"]] = relationship(
        back_populates="rol"
    )


# USUARIOS
class Usuario(Base):

    __tablename__ = "usuarios"

    id_usuario: Mapped[int] = mapped_column(primary_key=True)
    primer_nombre: Mapped[str] = mapped_column(String(50),nullable=False)
    segundo_nombre: Mapped[Optional[str]] = mapped_column(String(50),nullable=True)
    primer_apellido: Mapped[str] = mapped_column(String(50),nullable=False)
    segundo_apellido: Mapped[Optional[str]] = mapped_column(String(50),nullable=True)
    tipo_documento: Mapped[str] = mapped_column(String(50),nullable=False)
    numero_documento: Mapped[str] = mapped_column(String(20),unique=True,nullable=False)
    correo: Mapped[Optional[str]] = mapped_column(String(100),unique=True,nullable=True)
    numero_telefono: Mapped[Optional[str]] = mapped_column(String(15),nullable=True)
    numero_celular: Mapped[Optional[str]] = mapped_column(String(15),nullable=True)
    fecha_nacimiento: Mapped[date] = mapped_column(nullable=False)
    departamento: Mapped[str] = mapped_column(String(100),nullable=False)
    municipio: Mapped[str] = mapped_column(String(100),nullable=False)
    direccion: Mapped[str] = mapped_column(String(200),nullable=False)
    rol_id: Mapped[int] = mapped_column(ForeignKey("roles.id_rol"),nullable=False)

    __table_args__ = (

        CheckConstraint(
            "tipo_documento IN ('CC', 'TI', 'CE')",
            name="chk_tipo_documento_valido"
        ),

        CheckConstraint(
            "fecha_nacimiento < CURRENT_DATE",
            name="chk_fecha_nacimiento_valida"
        ),
    )

    # Relaciones
    rol: Mapped["Rol"] = relationship(
        back_populates="usuarios"
    )

    medico: Mapped[Optional["Medico"]] = relationship(
        back_populates="usuario",
        uselist=False
    )

    administrador: Mapped[Optional["Administrador"]] = relationship(
        back_populates="usuario",
        uselist=False
    )

    citas_como_paciente: Mapped[List["Cita"]] = relationship(
        back_populates="paciente"
    )



# ESPECIALIDADES
class Especialidad(Base):

    __tablename__ = "especialidades"

    id_especialidad: Mapped[int] = mapped_column(primary_key=True)
    nombre_especialidad: Mapped[str] = mapped_column(String(100),unique=True,nullable=False)

    # Relaciones
    medicos: Mapped[List["Medico"]] = relationship(
        back_populates="especialidad"
    )



# MEDICOS
class Medico(Base):

    __tablename__ = "medicos"

    id_medico: Mapped[int] = mapped_column(primary_key=True)
    fecha_ingreso: Mapped[date] = mapped_column(nullable=False)
    numero_tarjeta_profesional: Mapped[str] = mapped_column(String(20),unique=True,nullable=False)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id_usuario"),nullable=False)
    especialidad_id: Mapped[int] = mapped_column(ForeignKey("especialidades.id_especialidad"),nullable=False)

    __table_args__ = (

        CheckConstraint(
            "fecha_ingreso < CURRENT_DATE",
            name="chk_fecha_ingreso_valida"
        ),
    )

    # Relaciones
    usuario: Mapped["Usuario"] = relationship(
        back_populates="medico"
    )

    especialidad: Mapped["Especialidad"] = relationship(
        back_populates="medicos"
    )

    citas: Mapped[List["Cita"]] = relationship(
        back_populates="medico"
    )



# CONSULTORIOS
class Consultorio(Base):

    __tablename__ = "consultorios"

    id_consultorio: Mapped[int] = mapped_column(primary_key=True)
    nombre_consultorio: Mapped[str] = mapped_column(String(100),unique=True,nullable=False)

    # Relaciones
    citas: Mapped[List["Cita"]] = relationship(
        back_populates="consultorio"
    )



# CITAS
class Cita(Base):

    __tablename__ = "citas"

    id_cita: Mapped[int] = mapped_column(primary_key=True)
    fecha_cita: Mapped[datetime] = mapped_column(nullable=False)
    estado_cita: Mapped[str] = mapped_column(String(50),nullable=False,server_default=text("'PROGRAMADA'"))
    valor: Mapped[float] = mapped_column(Numeric(10, 2),nullable=False)
    medico_id: Mapped[int] = mapped_column(ForeignKey("medicos.id_medico"),nullable=False)
    paciente_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id_usuario"),nullable=False)
    consultorio_id: Mapped[int] = mapped_column(ForeignKey("consultorios.id_consultorio"),nullable=False)

    __table_args__ = (

        CheckConstraint(
            "estado_cita IN ('PROGRAMADA', 'CANCELADA', 'COMPLETADA')",
            name="chk_estado_valido"
        ),

        CheckConstraint(
            "valor >= 0",
            name="chk_valor_positivo"
        ),
    )

    # Relaciones
    medico: Mapped["Medico"] = relationship(
        back_populates="citas"
    )

    paciente: Mapped["Usuario"] = relationship(
        back_populates="citas_como_paciente"
    )

    consultorio: Mapped["Consultorio"] = relationship(
        back_populates="citas"
    )



# ADMINISTRADORES
class Administrador(Base):

    __tablename__ = "administradores"

    id_administrador: Mapped[int] = mapped_column(primary_key=True)
    contrasenia: Mapped[str] = mapped_column(String(50),nullable=False)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id_usuario"),nullable=False)

    # Relaciones
    usuario: Mapped["Usuario"] = relationship(
        back_populates="administrador"
    )

# VISTA PARA VER CITAS PROGRAMADAS POR PACIENTE
class VistaCitasProgramadas(Base):

    __tablename__ = "v_citas_programadas"

    id_cita: Mapped[int] = mapped_column(primary_key=True)
    paciente_id: Mapped[int]
    id_medico: Mapped[int]
    primer_nombre_medico: Mapped[str]
    segundo_nombre_medico: Mapped[str | None]
    primer_apellido_medico: Mapped[str]
    segundo_apellido_medico: Mapped[str | None]
    especialidad: Mapped[str]
    primer_nombre_paciente: Mapped[str]
    segundo_nombre_paciente: Mapped[str | None]
    primer_apellido_paciente: Mapped[str]
    segundo_apellido_paciente: Mapped[str | None]
    fecha_cita: Mapped[datetime]
    valor: Mapped[float]
    estado_cita: Mapped[str]
    nombre_consultorio: Mapped[str]