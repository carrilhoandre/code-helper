from flask import render_template
from . import routes

@routes.route('/')
def index():
    return 'Welcome to Code Helper'