"""
Initialization and configuration for the application.
"""


# Imports
from flask import Flask


# Flask initialization
app = Flask(__name__)


# Flask Blueprints - Imports
from src.core.views import core_bp


# Flask Blueprints - Register
app.register_blueprint(core_bp)
