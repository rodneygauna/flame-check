"""
Flame Check
Core views for the application
"""

# Imports
from flask import render_template, Blueprint


# Blueprint
core_bp = Blueprint('core', __name__)


# Route - Homepage
@core_bp.route('/')
def index():
    """Homepage"""

    return render_template('core/index.html',
                           title='Flame Check')
