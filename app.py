from flask import Flask
from flask_jwt_extended import JWTManager

from database import init_database
from components import auth_blueprint, user_blueprint


init_database()  # Initialize the database and create tables

app = Flask(__name__)
app.config.from_prefixed_env()

jwt_manager = JWTManager(app)

app.register_blueprint(auth_blueprint, url_prefix="/api/auth")
app.register_blueprint(user_blueprint, url_prefix="/api/users")


@app.route("/")
def root():
    return "Hello, there! You're in the Auth API root."
