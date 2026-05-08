-- Roles
CREATE ROLE bot_citas
WITH
LOGIN
PASSWORD '4dm1n';

-- Dar acceso
GRANT CONNECT
ON DATABASE centro_medico
TO bot_citas;

-- Dar permisos al rol:
GRANT USAGE ON SCHEMA public TO bot_citas;

GRANT SELECT ON TABLE
roles,
usuarios,
especialidades,
medicos,
consultorios
TO bot_citas;

GRANT USAGE, SELECT
ON ALL SEQUENCES IN SCHEMA public
TO bot_citas;

-- Dar permisos para citas:
GRANT SELECT, INSERT, UPDATE
ON TABLE citas
TO bot_citas;

-- Dar permiso para las vistas:
GRANT SELECT
ON v_citas_programadas
TO bot_citas;

-- Ver todos los permisos de sus usuarios:
SELECT grantee, table_name, privilege_type
FROM   information_schema.role_table_grants
WHERE  grantee IN ('bot_citas')
  AND  table_schema = 'public'
ORDER BY grantee, table_name;

-- Quitar rol:
RESET ROLE;