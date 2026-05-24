# PROYECTO FINAL BASES DE DATOS  
# Chatbot para Gestión de Citas Médicas

Sistema desarrollado para la gestión de citas médicas mediante un chatbot de Telegram. El proyecto permite a pacientes solicitar, consultar y cancelar citas médicas, mientras que médicos y administradores pueden consultar información relacionada con las citas programadas y reportes del sistema.

El sistema está orientado a automatizar procesos de atención en un centro médico, reduciendo tiempos de espera y facilitando la gestión de información médica mediante una arquitectura basada en Python, Telegram Bot API y PostgreSQL.

---

# Integrantes

- Juan David Orduz Sastoque — 20221020096
- Steven Navarro Parrales — 20221020048
- Oscar Manuel Contreras Gacha — 20221020052

---

# Requisitos Previos

## Software requerido

- Python 3.12+
- PostgreSQL 15+
- Git
- VS Code o IntelliJ IDEA

## Dependencias del sistema

```bash
python3.12-dev
build-essential
psycopg2-binary
libpq-dev
```

---

# Estructura del Repositorio

```bash
proyecto_BD/
│
├── sql/                     # Scripts SQL de creación de tablas, vistas y datos de prueba
├── src/
│   ├── autenticacion/
│   ├── config/
│   ├── database/
│   ├── handlers/
│   │   ├── admin/
│   │   ├── medico/
│   │   └── paciente/
│   ├── keyboards/
│   ├── models/
│   ├── repositories/
│   └── utils/
│
├── .env                     # Variables de entorno
├── .gitignore
├── requirements.txt
├── main.py
└── README.md
```

---

# Instalación y Configuración

## 1. Clonar el proyecto

```bash
git clone https://github.com/Racsok/proyecto_BD.git
cd proyecto_BD
```

---

## 2. Crear entorno virtual

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows CMD

```bash
venv\Scripts\activate
```

### Windows PowerShell

```bash
.\venv\Scripts\Activate.ps1
```

---

## 3. Instalar dependencias

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 4. Configurar PostgreSQL

Crear una base de datos en PostgreSQL:

```sql
CREATE DATABASE centro_medico;
```

---

## 5. Ejecutar scripts SQL

Ejecutar los scripts ubicados en la carpeta `/sql/` para crear:

- Tablas
- Restricciones
- Relaciones
- Vistas
- Datos de prueba

---

## 6. Configurar variables de entorno

Crear un archivo `.env` en la raíz del proyecto:

```env
BOT_TOKEN=TOKEN_DEL_BOT
DATABASE_URL=postgresql+psycopg2://usuario:password@localhost:5432/centro_medico
```

---

## 7. Ejecutar el sistema

```bash
python main.py
```

---

# Arquitectura del Sistema

El sistema no utiliza una API REST tradicional. La comunicación se realiza mediante un chatbot desarrollado con la librería `python-telegram-bot`.

## Flujo del sistema

1. El usuario interactúa con el chatbot desde Telegram.
2. Telegram envía eventos al bot mediante la Bot API.
3. Los handlers procesan las acciones del usuario.
4. SQLAlchemy ejecuta consultas sobre PostgreSQL.
5. El sistema responde directamente en el chat.

---

# Conexión con la Base de Datos

La conexión se realiza mediante SQLAlchemy ORM utilizando variables de entorno.

## Configuración de conexión

```python
engine = create_engine(
    variables.DATABASE_URL,
    pool_pre_ping=True
)
```

## Creación de sesiones

```python
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
```

---

# Diagrama Entidad-Relación

El diagrama ER del proyecto se presenta a continuación:

<p align="center">
  <img src="docs/Diagrama ER.png" width="900">
</p>

## Entidades principales

- Usuarios
- Roles
- Médicos
- Especialidades
- Consultorios
- Citas
- Administradores

---

# Comunicación del Sistema

El sistema utiliza handlers conversacionales y callbacks de Telegram para gestionar las operaciones.

| Acción del chatbot | Tipo de interacción | Descripción técnica |
|---|---|---|
| Agendar cita | CallbackQueryHandler | Ejecuta consultas SQL para obtener especialidades, médicos y horarios disponibles, e inserta nuevas citas en PostgreSQL. |
| Consultar citas | Handler conversacional | Realiza consultas `SELECT` sobre tablas y vistas de citas programadas. |
| Cancelar cita | Handler conversacional | Actualiza el estado de la cita a `CANCELADA` mediante SQLAlchemy ORM. |
| Consultar horarios | CallbackQueryHandler | Consulta horarios ocupados y genera horarios disponibles dinámicamente. |
| Ver citas asignadas | CallbackQueryHandler | Consulta citas programadas del médico autenticado usando relaciones ORM. |
| Ver reporte de citas completadas | CallbackQueryHandler | Consulta la vista `VistaReporteCitasCompletadas` para generar reportes administrativos. |
| Validar sesión y permisos | Handler conversacional | Verifica autenticación y roles antes de ejecutar operaciones médicas o administrativas. |

---

# Requerimientos Funcionales Implementados

- Solicitud de citas médicas mediante chatbot.
- Consulta de disponibilidad de horarios.
- Consulta de citas programadas.
- Cancelación de citas médicas.
- Consulta de citas asignadas para médicos.
- Consulta de reportes administrativos.
- Validación de sesiones y roles.
- Gestión de especialidades médicas.
- Gestión de médicos y consultorios.

---

# Tecnologías Utilizadas

| Tecnología | Uso |
|---|---|
| Python | Lenguaje principal del sistema |
| PostgreSQL | Base de datos relacional |
| SQLAlchemy | ORM para acceso a datos |
| python-telegram-bot | Comunicación con Telegram |
| Pydantic | Configuración y validación |
| dotenv | Manejo de variables de entorno |

---

# Archivo .gitignore Recomendado

```gitignore
# Entornos virtuales
venv/
.env

# Python
__pycache__/
*.pyc

# VS Code
.vscode/

# IntelliJ
.idea/

# Logs
*.log

# Archivos temporales
*.tmp
```

---

# Licencia

Proyecto académico desarrollado para la asignatura de Bases de Datos  
Universidad Distrital Francisco José de Caldas — 2026.