
from flask import Flask
from app import api_bp
from flask_cors import CORS

def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)
    app.register_blueprint(api_bp, url_prefix='/api')
    CORS(app)
    return app
    
    





if __name__ == "__main__":
    app = create_app("config")
    app.run(debug=True)