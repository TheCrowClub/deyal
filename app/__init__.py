from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = "ThereISN0SecR3tKey"
from app import routes
