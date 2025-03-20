import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import CSRFProtect
from config import DevelopmentConfig
import forms
from models import Examen, Pregunta, Respuesta, db, Alumno, alumno_examen, User
from sqlalchemy.orm import joinedload
from flask_login import LoginManager, login_user, logout_user, login_required

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf = CSRFProtect(app)
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:  
            login_user(user)
            return redirect(url_for('index'))
        flash('Usuario o contraseña incorrectos')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/crearExamen", methods=["GET", "POST"])
@login_required
def crearExamen():
    seleccionar_form = forms.SeleccionarPreguntasForm()
    create_forms = forms.ExamenForm()

    if "cantidad_preguntas" in request.form and seleccionar_form.validate():
        num_preguntas = seleccionar_form.cantidad_preguntas.data
        create_forms.preguntas.entries = []
        for _ in range(num_preguntas):
            create_forms.preguntas.append_entry()

    if request.method == "POST" and create_forms.validate():
        materia = create_forms.materia.data
        examen = Examen(materia=materia)
        db.session.add(examen)
        db.session.commit()  

        for pregunta_form in create_forms.preguntas:
            pregunta = Pregunta(
                pregunta=pregunta_form.pregunta.data,
                examen_id=examen.id  
            )
            db.session.add(pregunta)
            db.session.flush()  

            for respuesta_form in pregunta_form.respuestas:
                respuesta = Respuesta(
                    respuesta=respuesta_form.respuesta.data,
                    respuesta_correcta=(respuesta_form.correcta.data == "si"),
                    pregunta_id=pregunta.id  
                )
                db.session.add(respuesta)

        db.session.commit()  

        alumnos = Alumno.query.all()
        for alumno in alumnos:
            alumno.examenes.append(examen)
        db.session.commit()

        flash("Examen creado correctamente")
        return redirect(url_for("index"))

    return render_template("crearExamen.html", seleccionar_form=seleccionar_form, form=create_forms)

@app.route("/agregarAlumno", methods=["GET", "POST"])
def agregar():
    create_forms = forms.UserForm(request.form)
    if request.method == 'POST' and create_forms.validate():
        alumno = Alumno(
            nombre=create_forms.nombre.data,
            apaterno=create_forms.apaterno.data,
            amaterno=create_forms.amaterno.data,
            nacimiento=datetime.date(create_forms.anio.data, create_forms.mes.data, create_forms.dia.data),
            grupo=create_forms.grupo.data
        )
        db.session.add(alumno)
        db.session.commit()
        flash("Alumno agregado correctamente")
        return redirect(url_for("index"))
    return render_template("crearAlumno.html", form=create_forms)

@app.route("/hacerExamen", methods=["GET", "POST"])
def hacerExamen():
    alumno_form = forms.AlumnoExamenForm(request.form)
    alumno = None
    examenes_pendientes = []

    if request.method == "POST" and alumno_form.validate():
        nombre = alumno_form.nombre.data
        grupo = alumno_form.grupo.data

        alumno = (
            Alumno.query.options(
                joinedload(Alumno.examenes)
                .joinedload(Examen.preguntas)
                .joinedload(Pregunta.respuestas)
            )
            .filter_by(nombre=nombre, grupo=grupo)
            .first()
        )

        if alumno:
            examenes_pendientes = [
                examen 
                for examen in alumno.examenes 
                if not db.session.query(
                    alumno_examen.c.calificacion
                ).filter(
                    alumno_examen.c.examen_id == examen.id,
                    alumno_examen.c.alumno_id == alumno.id
                ).scalar()
            ]
        else:
            flash("Alumno no encontrado")

    return render_template(
        "hacerExamen.html", 
        form=alumno_form, 
        alumno=alumno, 
        examenes=examenes_pendientes  
    )

@app.route("/resolverExamen/<int:examen_id>", methods=["POST"])
def resolverExamen(examen_id):
    examen = Examen.query.get(examen_id)
    alumno_id = request.form.get('alumno_id')
    alumno = Alumno.query.get(alumno_id)
    calificacion = 0
    total_preguntas = len(examen.preguntas)
    
    for pregunta in examen.preguntas:
        respuesta_id = request.form.get(f'pregunta_{pregunta.id}')
        respuesta = Respuesta.query.get(respuesta_id)
        if respuesta and respuesta.respuesta_correcta:
            calificacion += 1
    
    calificacion_final = (calificacion / total_preguntas) * 10
    db.session.execute(alumno_examen.update().where(
        (alumno_examen.c.alumno_id == alumno.id) & 
        (alumno_examen.c.examen_id == examen.id)
    ).values(calificacion=calificacion_final))
    db.session.commit()
    
    flash(f"Examen completado. Calificación: {calificacion_final}")
    return redirect(url_for("index"))

@app.route("/calificaciones", methods=["GET", "POST"])
def calificaciones():
    grupos = Alumno.query.with_entities(Alumno.grupo).distinct().all()
    selected_grupo = request.form.get('grupo')
    calificaciones = []

    if selected_grupo:
        calificaciones = db.session.query(
            Alumno.nombre,
            Examen.materia,
            alumno_examen.c.calificacion
        ).join(alumno_examen, Alumno.id == alumno_examen.c.alumno_id).join(Examen, Examen.id == alumno_examen.c.examen_id).filter(Alumno.grupo == selected_grupo).all()

    return render_template("calificaciones.html", grupos=grupos, calificaciones=calificaciones, selected_grupo=selected_grupo)

if __name__ == '__main__':
    csrf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run()
