CREATE DATABASE centro_medico
WITH 
OWNER = postgres
ENCODING = 'UTF8'
TEMPLATE = template0;


CREATE TABLE ROLES (
    id_rol SERIAL PRIMARY KEY,
    nombre_rol VARCHAR(50) NOT NULL,
    CONSTRAINT chk_roles_validos
        CHECK (nombre_rol IN ('PACIENTE', 'ADMINISTRATIVO', 'MEDICO'))
);

CREATE TABLE USUARIOS (
    id_usuario SERIAL PRIMARY KEY,
    primer_nombre VARCHAR(50) NOT NULL,
    segundo_nombre VARCHAR(50),
    primer_apellido VARCHAR(50) NOT NULL,
    segundo_apellido VARCHAR(50),
    tipo_documento VARCHAR(50) NOT NULL,
    numero_documento VARCHAR(10) NOT NULL,
    correo VARCHAR(100),
    numero_telefono VARCHAR(7),
    numero_celular VARCHAR(10),
    fecha_nacimiento DATE NOT NULL,
    departamento VARCHAR(100) NOT NULL,
    municipio VARCHAR(100) NOT NULL,
    direccion VARCHAR(200) NOT NULL,
    rol_id INTEGER,

    CONSTRAINT uq_usuarios_numero_documento UNIQUE (numero_documento),
    CONSTRAINT uq_usuarios_correo UNIQUE (correo),

    CONSTRAINT chk_tipo_documento_valido
        CHECK (tipo_documento IN ('CC', 'TI', 'CE')),

    CONSTRAINT chk_fecha_nacimiento_valida
        CHECK (fecha_nacimiento < CURRENT_DATE),

    CONSTRAINT fk_usuarios_rol_id
        FOREIGN KEY (rol_id)
        REFERENCES ROLES(id_rol)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

CREATE TABLE ESPECIALIDADES (
    id_especialidad SERIAL PRIMARY KEY,
    nombre_especialidad VARCHAR(100) NOT NULL,

    CONSTRAINT uq_especialidades_nombre
        UNIQUE (nombre_especialidad)
);

CREATE TABLE MEDICOS (
    id_medico SERIAL PRIMARY KEY,
    fecha_ingreso DATE NOT NULL,
    numero_tarjeta_profesional VARCHAR(10) NOT NULL,
    usuario_id INTEGER,
    especialidad_id INTEGER,

    CONSTRAINT uq_medicos_numero_tarjeta
        UNIQUE (numero_tarjeta_profesional),

    CONSTRAINT chk_fecha_ingreso_valida
        CHECK (fecha_ingreso < CURRENT_DATE),

    CONSTRAINT fk_medicos_usuario_id
        FOREIGN KEY (usuario_id)
        REFERENCES USUARIOS(id_usuario)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT fk_medicos_especialidad_id
        FOREIGN KEY (especialidad_id)
        REFERENCES ESPECIALIDADES(id_especialidad)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

CREATE TABLE CONSULTORIOS (
    id_consultorio SERIAL PRIMARY KEY,
    nombre_consultorio VARCHAR(100) NOT NULL,

    CONSTRAINT uq_consultorios_nombre
        UNIQUE (nombre_consultorio)
);

CREATE TABLE CITAS (
    id_cita SERIAL PRIMARY KEY,
    fecha_cita TIMESTAMP NOT NULL,
    estado_cita VARCHAR(50) DEFAULT 'PROGRAMADA',
    valor NUMERIC(10,2) NOT NULL,
    medico_id INTEGER,
    paciente_id INTEGER,
    consultorio_id INTEGER,

    CONSTRAINT chk_fecha_cita_valida
        CHECK (fecha_cita > CURRENT_TIMESTAMP),

    CONSTRAINT chk_estado_valido
        CHECK (estado_cita IN ('PROGRAMADA', 'CANCELADA', 'COMPLETADA')),

    CONSTRAINT chk_valor_positivo
        CHECK (valor >= 0),

    CONSTRAINT fk_citas_medicos_id
        FOREIGN KEY (medico_id)
        REFERENCES MEDICOS(id_medico)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT fk_citas_paciente_id
        FOREIGN KEY (paciente_id)
        REFERENCES USUARIOS(id_usuario)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT fk_citas_consultorio_id
        FOREIGN KEY (consultorio_id)
        REFERENCES CONSULTORIOS(id_consultorio)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

CREATE TABLE ADMINISTRADORES (
    id_administrador SERIAL PRIMARY KEY,
    contrasenia VARCHAR(50) NOT NULL,
    usuario_id INTEGER,

    CONSTRAINT fk_administradores_usuario_id
        FOREIGN KEY (usuario_id)
        REFERENCES USUARIOS(id_usuario)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);


