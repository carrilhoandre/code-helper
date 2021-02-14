from flask import render_template
from . import routes
from flask_jwt_extended import (
    jwt_required
)

@routes.route('/')
@jwt_required
def index():
    return 'Welcome to Code Helper'