"""
Initialization and configuration for the application.
"""

# Imports
from flask import Flask


# Flask initialization
app = Flask(__name__)


# Flask Blueprints - Imports
from src.core.views import core_bp
from src.providerdirectory.views import provdir_bp
from src.drugformulary.views import drugformulary_bp


# Flask Blueprints - Register
app.register_blueprint(core_bp)
app.register_blueprint(provdir_bp)
app.register_blueprint(drugformulary_bp)
