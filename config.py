import os
from sqlalchemy import create_engine
import urllib 

class Config(object):
    SECRET_KEY = 'mysecretkey'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    SECRET_KEY = "una_clave_secreta_compleja_y_aleatoria"
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@localhost/alumnos'
    SQLALCHEMY_TRACK_MODIFICATIONS = False