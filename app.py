# app.py
from flask import Flask
from flask_cors import CORS
from models import db
from routes.user_routes import users_bp
from routes.documentation_routes import documentation_bp
from routes.prompt_generator_routes import prompt_generator_bp
from flask_jwt_extended import JWTManager

def create_app():
    app = Flask(__name__)

    CORS(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:DSM2001dsm*@localhost/genify'

    # Configuration for JWT
    app.config['JWT_SECRET_KEY'] = 'yX*F2wRpE78Ct!LkG$mjQvZpF9p#bS%z'  # Change this to a secret key
    jwt = JWTManager(app)

    
    db.init_app(app)  # Register SQLAlchemy extension with the Flask app

    with app.app_context():
        db.create_all()

    app.register_blueprint(users_bp)
    app.register_blueprint(documentation_bp)
    app.register_blueprint(prompt_generator_bp)


    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
