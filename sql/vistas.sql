-- vistas
-- Esta vista le permite a un paciente ver sus citas programadas, para que pueda estar pendiente y asistir al consultorio correcto en la fecha correcta.
create view v_pacientes as
SELECT * FROM USUARIOS U
WHERE rol_id = (SELECT id_rol FROM ROLES WHERE nombre_rol = 'PACIENTE');


create view v_medicos AS
SELECT 
	M.id_medico, 
	M.numero_tarjeta_profesional, 
	U.primer_nombre AS primer_nombre_medico,
	U.segundo_nombre AS segundo_nombre_medico,
	U.primer_apellido AS primer_apellido_medico,
	U.segundo_apellido AS segundo_apellido_medico,
	E.nombre_especialidad AS especialidad
FROM MEDICOS M
INNER JOIN ESPECIALIDADES E ON M.especialidad_id = E.id_especialidad
INNER JOIN USUARIOS U ON M.usuario_id = U.id_usuario;


CREATE VIEW v_citas_programadas AS
SELECT 
	C.id_cita,
	P.id_usuario AS paciente_id,
	M.id_medico,
	M.primer_nombre_medico,
	M.segundo_nombre_medico,
	M.primer_apellido_medico,
	M.segundo_apellido_medico,
	M.especialidad,
	P.primer_nombre AS primer_nombre_paciente, 
	P.segundo_nombre AS segundo_nombre_paciente, 
	P.primer_apellido AS primer_apellido_paciente, 
	P.segundo_apellido AS segundo_apellido_paciente, 
	C.fecha_cita,
	C.valor,
	C.estado_cita,
	CO.nombre_consultorio
FROM v_pacientes P
INNER JOIN CITAS C ON P.id_usuario = C.paciente_id
INNER JOIN v_medicos M ON C.medico_id = M.id_medico
INNER JOIN CONSULTORIOS CO ON C.consultorio_id = CO.id_consultorio
WHERE C.estado_cita = 'PROGRAMADA'
ORDER BY C.fecha_cita ASC;


--  Esta vista le permite al administrador observar todas las citas completadas, asociando al médico
-- (nombre, número tarjeta profesional y especialidad) con las citas (fecha, valor) y los pacientes (nombre, tipo de documento y número de documento)

CREATE VIEW v_reportes_citas_completadas AS
SELECT 
	M.primer_nombre_medico,
	M.segundo_nombre_medico,
	M.primer_apellido_medico,
	M.segundo_apellido_medico,
	M.numero_tarjeta_profesional,
	M.especialidad,
	P.primer_nombre AS primer_nombre_paciente, 
	P.segundo_nombre AS segundo_nombre_paciente, 
	P.primer_apellido AS primer_apellido_paciente, 
	P.segundo_apellido AS segundo_apellido_paciente,
	P.tipo_documento AS tipo_documento_paciente,
	P.numero_documento AS numero_documento_paciente,
	C.fecha_cita,
	C.valor
FROM v_pacientes P
INNER JOIN CITAS C ON P.id_usuario = C.paciente_id
INNER JOIN v_medicos M ON C.medico_id = M.id_medico
WHERE C.estado_cita = 'COMPLETADA'
ORDER BY C.fecha_cita DESC;

