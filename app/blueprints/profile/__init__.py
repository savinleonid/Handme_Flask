from flask import Blueprint

prof_bp = Blueprint('prof', __name__)

from . import routes  # Import routes to register them
