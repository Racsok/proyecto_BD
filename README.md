# PROYECTO BASE DE DATOS
## INTEGRANTES
* Oscar Manuel Contreras Gacha 
* Steven Navarro Parrales
* Juan David Orduz Sastoque

## requerimientos
python3.12-dev
build-essential
psycopg2-binary
libpq-dev


## Clonación del Proyecto
Primero, obtén una copia local del repositorio ejecutando el siguiente comando en tu terminal:

```bash:
git clone https://github.com/Racsok/proyecto_BD.git
cd proyecto_BD
```
## Configuración del Entorno Virtual
Para mantener las dependencias aisladas y evitar conflictos con otros proyectos, es necesario crear un entorno virtual de Python.

1. Crear el entorno virtual:
Ejecuta el siguiente comando en la raíz de tu proyecto:
```bash:
python3 -m venv venv
```

2. Activar el entorno:
Dependiendo de tu sistema operativo, usa el comando correspondiente:

   * En Linux (antiX, Lubuntu, etc.) o macOS:
   ```bash:
    source venv/bin/activate
   ```

   * En Windows (Símbolo del sistema):
   ```bash:
   venv\Scripts\activate
   ```

   * En Windows (PowerShell):
   ```bash:
   .\venv\Scripts\Activate.ps1
   ```
## Instalación de Dependencias
Con el entorno virtual activado, procede a instalar todas las librerías necesarias que se encuentran en el archivo ```requirements.txt``` usando ```pip``` o ```pip3```:
```bash:
pip install --upgrade pip
pip install -r requirements.txt
```
