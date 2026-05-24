-- =========================================
-- INSERTS DE PRUEBA - CENTRO_MEDICO
-- =========================================

-- =========================================
-- ROLES
-- =========================================
INSERT INTO roles (nombre_rol) VALUES
('PACIENTE'),
('ADMINISTRATIVO'),
('MEDICO');

-- =========================================
-- USUARIOS
-- =========================================
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

('Camila', 'Andrea', 'Torres', 'Ruiz',
'CC', '1000000007', 'camila@gmail.com',
'4567896', '3007777777',
'1997-02-14', 'Antioquia', 'Medellin', 'Cra 15 #20-10', 1),

('Andres', NULL, 'Castro', 'Mendez',
'CC', '1000000008', 'andres@gmail.com',
'4567897', '3008888888',
'1993-06-21', 'Antioquia', 'Bello', 'Calle 22 #40-50', 1),

('Valentina', 'Sofia', 'Herrera', NULL,
'CC', '1000000009', 'valentina@gmail.com',
'4567898', '3009999999',
'2001-08-30', 'Antioquia', 'Envigado', 'Cra 90 #10-12', 1),

('Mateo', NULL, 'Jimenez', 'Ortiz',
'CC', '1000000010', 'mateo@gmail.com',
'4567899', '3011111111',
'1996-01-18', 'Antioquia', 'Itagui', 'Calle 100 #30-40', 1),

('Laura', 'Paola', 'Vargas', 'Gil',
'CC', '1000000011', 'laura@gmail.com',
'4567800', '3012222222',
'1994-12-11', 'Antioquia', 'Sabaneta', 'Cra 77 #45-80', 1),

-- ADMINISTRATIVOS
('Sandra', NULL, 'Morales', NULL,
'CC', '1000000004', 'sandra@gmail.com',
'4567893', '3004444444',
'1990-11-08', 'Antioquia', 'Medellin', 'Cra 45 #12-99', 2),

('Ricardo', NULL, 'Lopez', 'Garcia',
'CC', '1000000016', 'ricardo@gmail.com',
'4567805', '3017777777',
'1988-10-10', 'Antioquia', 'Medellin', 'Cra 99 #88-77', 2),

-- MEDICOS
('Carlos', 'Andres', 'Restrepo', NULL,
'CC', '1000000005', 'carlos@gmail.com',
'4567894', '3005555555',
'1980-07-25', 'Antioquia', 'Medellin', 'Calle 80 #10-20', 3),

('Ana', NULL, 'Martinez', NULL,
'CC', '1000000006', 'ana@gmail.com',
'4567895', '3006666666',
'1985-01-10', 'Antioquia', 'Itagui', 'Cra 70 #11-22', 3),

('Jorge', 'Ivan', 'Salazar', NULL,
'CC', '1000000012', 'jorge@gmail.com',
'4567801', '3013333333',
'1978-04-12', 'Antioquia', 'Medellin', 'Cra 40 #20-90', 3),

('Patricia', NULL, 'Mejia', 'Lopez',
'CC', '1000000013', 'patricia@gmail.com',
'4567802', '3014444444',
'1982-09-25', 'Antioquia', 'Envigado', 'Calle 60 #70-10', 3),

('Felipe', 'Andres', 'Rojas', NULL,
'CC', '1000000014', 'felipe@gmail.com',
'4567803', '3015555555',
'1987-03-08', 'Antioquia', 'Bello', 'Cra 12 #80-20', 3),

('Natalia', 'Maria', 'Suarez', 'Diaz',
'CC', '1000000015', 'natalia@gmail.com',
'4567804', '3016666666',
'1990-07-17', 'Antioquia', 'Itagui', 'Calle 33 #22-11', 3);

-- =========================================
-- ESPECIALIDADES
-- =========================================
INSERT INTO especialidades (
nombre_especialidad
) VALUES
('Medicina General'),
('Pediatria'),
('Cardiologia'),
('Dermatologia');

-- =========================================
-- MEDICOS
-- =========================================
INSERT INTO medicos (
fecha_ingreso,
numero_tarjeta_profesional,
usuario_id,
especialidad_id
) VALUES
('2015-06-01', 'TP10001', 11, 1),
('2018-03-10', 'TP10002', 12, 3),
('2016-02-01', 'TP10003', 13, 2),
('2019-05-15', 'TP10004', 14, 4),
('2020-08-20', 'TP10005', 15, 1),
('2017-11-11', 'TP10006', 16, 3);

-- =========================================
-- CONSULTORIOS
-- =========================================
INSERT INTO consultorios (
nombre_consultorio
) VALUES
('Consultorio 101'),
('Consultorio 102'),
('Consultorio 201'),
('Consultorio 202'),
('Consultorio 203'),
('Consultorio 301'),
('Consultorio 302'),
('Consultorio Pediatria'),
('Consultorio Cardiologia'),
('Consultorio Dermatologia');

-- =========================================
-- CITAS
-- =========================================
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
('2026-05-12 14:00:00', 'CANCELADA', 120000, 1, 1, 3),

('2026-05-13 08:00:00', 'PROGRAMADA', 120000, 3, 4, 4),
('2026-05-13 09:00:00', 'PROGRAMADA', 150000, 4, 5, 5),
('2026-05-13 10:00:00', 'PROGRAMADA', 180000, 5, 6, 6),
('2026-05-13 11:00:00', 'PROGRAMADA', 120000, 6, 7, 7),

('2026-05-14 08:30:00', 'PROGRAMADA', 120000, 1, 8, 1),
('2026-05-14 09:30:00', 'PROGRAMADA', 180000, 2, 4, 2),
('2026-05-14 10:30:00', 'PROGRAMADA', 150000, 4, 5, 5),

('2026-05-15 14:00:00', 'COMPLETADA', 120000, 3, 6, 4),
('2026-05-15 15:00:00', 'CANCELADA', 180000, 6, 7, 7),
('2026-05-16 16:00:00', 'PROGRAMADA', 120000, 5, 8, 6);

-- =========================================
-- ADMINISTRADORES
-- =========================================
INSERT INTO administradores (
contrasenia,
usuario_id
) VALUES
('admin123', 9),
('admin456', 10);