from flask import Blueprint
routes = Blueprint('routes', __name__)

from .index import *
from .project import *
from .user import *