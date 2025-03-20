from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Alumno(db.Model):
    __tablename__ = 'alumno'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    apaterno = db.Column(db.String(50))
    amaterno = db.Column(db.String(50))
    nacimiento = db.Column(db.Date)
    grupo = db.Column(db.String(10))
    created_date = db.Column(db.DateTime, default=datetime.datetime.now)
    examenes = db.relationship('Examen', secondary='alumno_examen', back_populates='alumnos')

class Examen(db.Model):
    __tablename__ = 'examen'
    id = db.Column(db.Integer, primary_key=True)
    materia = db.Column(db.String(50))
    preguntas = db.relationship('Pregunta', backref='examen', lazy=True)
    created_date = db.Column(db.DateTime, default=datetime.datetime.now)
    alumnos = db.relationship('Alumno', secondary='alumno_examen', back_populates='examenes')

class Pregunta(db.Model):
    __tablename__ = 'pregunta'
    id = db.Column(db.Integer, primary_key=True)
    pregunta = db.Column(db.String(200))
    examen_id = db.Column(db.Integer, db.ForeignKey('examen.id'))
    created_date = db.Column(db.DateTime, default=datetime.datetime.now)
    respuestas = db.relationship('Respuesta', backref='pregunta', lazy=True)

class Respuesta(db.Model):
    __tablename__ = 'respuesta'
    id = db.Column(db.Integer, primary_key=True)
    respuesta = db.Column(db.String(200))
    respuesta_correcta = db.Column(db.Boolean)
    pregunta_id = db.Column(db.Integer, db.ForeignKey('pregunta.id'))
    created_date = db.Column(db.DateTime, default=datetime.datetime.now)

alumno_examen = db.Table('alumno_examen',
    db.Column('alumno_id', db.Integer, db.ForeignKey('alumno.id'), primary_key=True),
    db.Column('examen_id', db.Integer, db.ForeignKey('examen.id'), primary_key=True),
    db.Column('calificacion', db.Float)
)

