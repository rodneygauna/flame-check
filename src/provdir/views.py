"""
Flame Check
View for the Provider Directory section of the app.
"""

# Imports
from flask import render_template, Blueprint


# Blueprint
provdir_bp = Blueprint('provdir', __name__)


# Route - Landing Page
@provdir_bp.route('/provdir')
def index():
    """Landing Page"""

    return render_template('provdir/index.html',
                           title='Flame Check - Provider Directory')
