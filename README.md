# Flask Login Application

Esta es una aplicación web desarrollada con Flask que permite gestionar alumnos, crear exámenes, realizar exámenes y consultar calificaciones.

## Requisitos previos

Antes de ejecutar la aplicación, asegúrate de tener instalados los siguientes componentes:

- Python 3.10 o superior
- Node.js y npm
- MySQL

## Instalación

1. Clona este repositorio en tu máquina local:

   ```bash
   git clone https://github.com/IDGS-805-22001761/Parcial3_Montoya
   cd flask-login

Instala las dependencias de Python:
'pip install -r requirements.txt'

Configura la base de datos MySQL:
Crea una base de datos llamada alumnos.
Actualiza las credenciales de la base de datos en el archivo config.py si es necesario.
Inicializa la base de datos:
'python app.py'

Esto creará las tablas necesarias en la base de datos.

Instala las dependencias de Node.js para TailwindCSS:
'npm install'

Genera los estilos CSS con TailwindCSS:
'npm run css'

Inicia la aplicación Flask:
'python app.py'

Abre tu navegador y accede a http://127.0.0.1:5000.

Funcionalidades
Inicio de sesión: Los usuarios pueden iniciar sesión con un nombre de usuario y contraseña.
Gestión de alumnos: Permite agregar nuevos alumnos al sistema.
Creación de exámenes: Los usuarios pueden crear exámenes con preguntas y respuestas.
Realización de exámenes: Los alumnos pueden realizar exámenes asignados.
Consulta de calificaciones: Los usuarios pueden consultar las calificaciones de los alumnos por grupo.

Estructura del proyecto
app.py: Archivo principal de la aplicación.
config.py: Configuración de la aplicación, incluyendo la base de datos.
forms.py: Formularios utilizados en la aplicación.
models.py: Modelos de la base de datos.
templates: Plantillas HTML para las vistas.
css: Archivos CSS generados con TailwindCSS.
Notas adicionales
Asegúrate de que el servidor MySQL esté en ejecución antes de iniciar la aplicación.
Si necesitas cambiar el puerto o la configuración, edita el archivo config.py.
¡Disfruta usando la aplicación!