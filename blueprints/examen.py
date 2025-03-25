from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from blueprints.models import Alumno, Examen, Pregunta, Respuesta, db
import logging

logger = logging.getLogger(__name__)

examen_bp = Blueprint('examen', __name__, url_prefix='/examen')

# Ruta para crear un examen
@examen_bp.route('/crear', methods=['GET', 'POST'])
@login_required
def crear_examen():
    if request.method == 'POST':
        materia = request.form.get('materia')
        preguntas = request.form.getlist('preguntas')
        respuestas = request.form.getlist('respuestas')

        # Crear el examen
        examen = Examen(materia=materia)
        db.session.add(examen)
        db.session.flush()  # Obtener el ID del examen antes de confirmar

        # Crear las preguntas y respuestas asociadas
        for pregunta_texto in preguntas:
            pregunta = Pregunta(pregunta=pregunta_texto, examen_id=examen.id)
            db.session.add(pregunta)
            db.session.flush()

            # Asociar respuestas a la pregunta
            for respuesta_texto in respuestas:
                respuesta = Respuesta(
                    respuesta=respuesta_texto,
                    respuesta_correcta=False,  # Cambiar según lógica
                    pregunta_id=pregunta.id
                )
                db.session.add(respuesta)

        db.session.commit()
        logger.info(f"Examen creado: {materia}")
        flash("Examen creado correctamente.")
        return redirect(url_for('examen.listar_examenes'))

    return render_template('crearExamen.html')

# Ruta para realizar un examen
@examen_bp.route('/realizar/<int:examen_id>', methods=['GET', 'POST'])
@login_required
def realizar_examen(examen_id):
    examen = Examen.query.get_or_404(examen_id)

    if request.method == 'POST':
        respuestas_usuario = request.form.getlist('respuestas')
        # Aquí puedes procesar las respuestas del usuario y calcular la calificación
        logger.info(f"Examen realizado por el usuario {current_user.id}: Examen ID {examen_id}")
        flash("Examen enviado correctamente.")
        return redirect(url_for('examen.listar_examenes'))

    return render_template('hacerExamen.html', examen=examen)

@examen_bp.route('/')
@login_required
def listar_examenes():
    examenes = Examen.query.all()
    return render_template('listarExamenes.html', examenes=examenes)

@examen_bp.route('/calificaciones', methods=['GET', 'POST'])
@login_required
def calificaciones():
    grupos = db.session.query(Pregunta.grupo).distinct().all()  # Obtén los grupos únicos
    calificaciones = []
    selected_grupo = None

    if request.method == 'POST':
        selected_grupo = request.form.get("grupo")
        if selected_grupo:
            # Consulta las calificaciones de los alumnos en el grupo seleccionado
            calificaciones = db.session.query(
                Alumno.nombre,
                Examen.materia,
                calificaciones.calificacion
            ).join(calificaciones, Alumno.id == calificaciones.alumno_id).join(
                Examen, calificaciones.examen_id == Examen.id
            ).filter(Alumno.grupo == selected_grupo).all()

    return render_template(
        'calificaciones.html',
        grupos=grupos,
        calificaciones=calificaciones,
        selected_grupo=selected_grupo
    )