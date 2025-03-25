from flask import Blueprint, render_template, request, redirect, url_for, flash
from blueprints.models import Profesor, db
import logging

logger = logging.getLogger(__name__)

profesores_bp = Blueprint('profesores', __name__, url_prefix='/profesores')

@profesores_bp.route('/')
def listar_profesores():
    profesores = Profesor.query.all()
    return render_template('listar_profesores.html', profesores=profesores)

@profesores_bp.route('/agregar', methods=['GET', 'POST'])
def agregar_profesor():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellidos = request.form.get('apellidos')
        email = request.form.get('email')

        profesor = Profesor(nombre=nombre, apellidos=apellidos, email=email)
        db.session.add(profesor)
        db.session.commit()
        logger.info(f"Profesor agregado: {nombre} {apellidos}, Email: {email}")
        flash("Profesor agregado correctamente.")
        return redirect(url_for('profesores.listar_profesores'))
    return render_template('agregar_profesor.html')

@profesores_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_profesor(id):
    profesor = Profesor.query.get_or_404(id)
    if request.method == 'POST':
        profesor.nombre = request.form.get('nombre')
        profesor.apellidos = request.form.get('apellidos')
        profesor.email = request.form.get('email')

        db.session.commit()
        logger.info(f"Profesor actualizado: {profesor.nombre} {profesor.apellidos}, Email: {profesor.email}")
        flash("Profesor actualizado correctamente.")
        return redirect(url_for('profesores.listar_profesores'))
    return render_template('editar_profesor.html', profesor=profesor)

@profesores_bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_profesor(id):
    profesor = Profesor.query.get_or_404(id)
    db.session.delete(profesor)
    db.session.commit()
    logger.info(f"Profesor eliminado: {profesor.nombre} {profesor.apellidos}, Email: {profesor.email}")
    flash("Profesor eliminado correctamente.")
    return redirect(url_for('profesores.listar_profesores'))