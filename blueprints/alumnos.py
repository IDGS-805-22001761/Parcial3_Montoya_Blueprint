from flask import Blueprint, render_template, request, redirect, url_for, flash
import blueprints.forms as forms
from blueprints.models import Alumno, db
import datetime
import logging

logger = logging.getLogger(__name__)

alumnos_bp = Blueprint('alumnos', __name__, url_prefix='/alumnos')

@alumnos_bp.route('/agregar', methods=['GET', 'POST'])
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
        logger.info(f"Alumno agregado: {alumno.nombre} {alumno.apaterno} {alumno.amaterno}, Grupo: {alumno.grupo}")
        flash("Alumno agregado correctamente")
        return redirect(url_for('index'))
    return render_template("crearAlumno.html", form=create_forms)