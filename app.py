from flask import Flask, render_template
from flask_wtf import CSRFProtect
from flask_login import LoginManager
from blueprints.config import DevelopmentConfig
from blueprints.models import db
from blueprints.auth import auth_bp
from blueprints.alumnos import alumnos_bp
from blueprints.profesores import profesores_bp
from blueprints.models import User
from blueprints.examen import examen_bp
import logging

logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf = CSRFProtect(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

app.register_blueprint(auth_bp)
app.register_blueprint(alumnos_bp)
app.register_blueprint(profesores_bp)
app.register_blueprint(examen_bp)

if __name__ == '__main__':
    csrf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    logger.info("La aplicación Flask ha iniciado correctamente.")
    app.run()