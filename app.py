from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

import config
import models
import routes