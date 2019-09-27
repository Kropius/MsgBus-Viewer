from flask import Flask, session

app = Flask(__name__)
app.config.from_pyfile('config.py')
from msgbus.routes import *
