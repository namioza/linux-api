from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Register Blueprints
    from app.routes.system_routes import system_bp
    from app.routes.hardware_routes import hardware_bp

    app.register_blueprint(system_bp, url_prefix='/api')
    app.register_blueprint(hardware_bp, url_prefix='/api')

    return app
