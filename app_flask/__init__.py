from flask import Flask
import re

app = Flask(__name__)
app.secret_key = "Shhh, stay quiet!"

DATA_BASE = "solutiva_joint"
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+-]+@[a-zA-Z0-9._-]+.[a-zA-Z]+$')
IMAGE_FOLDER =  "app_flask/static/img/profile_pics"