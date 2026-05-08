-- =========================================
-- INSERTS DE PRUEBA - CENTRO_MEDICO
-- =========================================

-- ROLES
INSERT INTO roles (nombre_rol) VALUES
('PACIENTE'),
('ADMINISTRATIVO'),
('MEDICO');

-- USUARIOS
INSERT INTO usuarios (
primer_nombre, segundo_nombre, primer_apellido, segundo_apellido,
tipo_documento, numero_documento, correo,
numero_telefono, numero_celular,
fecha_nacimiento, departamento, municipio, direccion, rol_id
) VALUES

-- PACIENTES
('Juan', 'Carlos', 'Perez', 'Lopez',
'CC', '1000000001', 'juan@gmail.com',
'4567890', '3001111111',
'1998-05-12', 'Antioquia', 'Medellin', 'Cra 10 #20-30', 1),

('Maria', 'Elena', 'Gomez', 'Diaz',
'CC', '1000000002', 'maria@gmail.com',
'4567891', '3002222222',
'1995-09-20', 'Antioquia', 'Envigado', 'Calle 50 #40-10', 1),

('Luis', NULL, 'Ramirez', NULL,
'CC', '1000000003', 'luis@gmail.com',
'4567892', '3003333333',
'2000-03-15', 'Antioquia', 'Bello', 'Cra 12 #30-15', 1),

-- ADMINISTRATIVO
('Sandra', NULL, 'Morales', NULL,
'CC', '1000000004', 'sandra@gmail.com',
'4567893', '3004444444',
'1990-11-08', 'Antioquia', 'Medellin', 'Cra 45 #12-99', 2),

-- MEDICOS
('Carlos', 'Andres', 'Restrepo', NULL,
'CC', '1000000005', 'carlos@gmail.com',
'4567894', '3005555555',
'1980-07-25', 'Antioquia', 'Medellin', 'Calle 80 #10-20', 3),

('Ana', NULL, 'Martinez', NULL,
'CC', '1000000006', 'ana@gmail.com',
'4567895', '3006666666',
'1985-01-10', 'Antioquia', 'Itagui', 'Cra 70 #11-22', 3);

-- ESPECIALIDADES
INSERT INTO especialidades (nombre_especialidad) VALUES
('Medicina General'),
('Pediatria'),
('Cardiologia'),
('Dermatologia');

-- MEDICOS
INSERT INTO medicos (
fecha_ingreso,
numero_tarjeta_profesional,
usuario_id,
especialidad_id
) VALUES
('2015-06-01', 'TP10001', 5, 1),
('2018-03-10', 'TP10002', 6, 3);

-- CONSULTORIOS
INSERT INTO consultorios (nombre_consultorio) VALUES
('Consultorio 101'),
('Consultorio 102'),
('Consultorio 201');

-- CITAS
INSERT INTO citas (
fecha_cita,
estado_cita,
valor,
medico_id,
paciente_id,
consultorio_id
) VALUES

('2026-05-10 08:00:00', 'PROGRAMADA', 120000, 1, 1, 1),
('2026-05-10 09:00:00', 'PROGRAMADA', 120000, 1, 2, 1),
('2026-05-11 10:30:00', 'COMPLETADA', 180000, 2, 3, 2),
('2026-05-12 14:00:00', 'CANCELADA', 120000, 1, 1, 3);

-- ADMINISTRADORES
INSERT INTO administradores (
contrasenia,
usuario_id
) VALUES
('admin123', 4);

