from flask import Blueprint

prod_bp = Blueprint('prod', __name__)

from . import routes  # Import routes to register them
