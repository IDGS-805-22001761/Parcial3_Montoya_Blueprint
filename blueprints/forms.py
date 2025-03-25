from flask_wtf import FlaskForm
from wtforms import FieldList, FormField, RadioField, StringField, IntegerField, TextAreaField
from wtforms import validators

class UserForm(FlaskForm):
    nombre = StringField('nombre', [
        validators.DataRequired(message='El campo es requerido'),
        validators.Length(min=4, max=10, message='Ingresa un nombre válido')
    ])
    apaterno = StringField('apaterno')
    amaterno = StringField('amaterno')
    dia = IntegerField('dia')
    mes = IntegerField('mes')
    anio = IntegerField('anio')
    grupo = StringField('grupo')

class RespuestaForm(FlaskForm):
    respuesta = StringField('Respuesta', [
        validators.DataRequired(message='La respuesta es requerida')
    ])
    correcta = RadioField('Correcta', choices=[('si', 'Sí'), ('no', 'No')], default='no')

class PreguntaForm(FlaskForm):
    pregunta = TextAreaField('Pregunta', [
        validators.DataRequired(message='La pregunta es requerida')
    ])
    respuestas = FieldList(FormField(RespuestaForm), min_entries=4, max_entries=4)

class SeleccionarPreguntasForm(FlaskForm):
    cantidad_preguntas = IntegerField('Número de preguntas', [
        validators.DataRequired(message='Debes indicar un número'),
        validators.NumberRange(min=1, max=10, message='Debe ser entre 1 y 10')
    ])

class ExamenForm(FlaskForm):
    materia = StringField('Materia', [
        validators.DataRequired(message='El nombre de la materia es requerido')
    ])
    preguntas = FieldList(FormField(PreguntaForm), min_entries=1, max_entries=10)
    
class AlumnoExamenForm(FlaskForm):
    nombre = StringField('Nombre', [
        validators.DataRequired(message='El nombre es requerido')
    ])
    grupo = StringField('Grupo', [
        validators.DataRequired(message='El grupo es requerido')
    ])