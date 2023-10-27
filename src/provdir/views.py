# Imports
import requests
from flask import render_template, Blueprint, request, redirect, url_for, jsonify

# Blueprint
provdir_bp = Blueprint('provdir', __name__)


# Route - Landing Page
@provdir_bp.route('/provdir', methods=['GET', 'POST'])
def index():
    """Landing Page"""

    connection_result = None
    connection_successful = False

    if request.method == 'POST':
        base_url = request.form.get('base_url')

        # Ensure the URL starts with https://
        if not base_url.startswith('https://'):
            base_url = f"https://{base_url}"
        # Ensure the URL ends with a slash
        if not base_url.endswith('/'):
            base_url += '/'

        api_endpoint = f"{base_url}fhirprovdir/Practitioner"

        try:
            response = requests.get(
                api_endpoint,
                timeout=10
            )
            response.raise_for_status()
            connection_result = "Connection successful (HTTP 200 OK)"
            connection_successful = True
        except requests.exceptions.RequestException as e:
            connection_result = f"Connection failed: {e}"

        if connection_successful:
            return redirect(url_for('provdir.test_endpoints',
                                    base_url=base_url))

    return render_template('provdir/index.html',
                           title='Flame Check - Provider Directory',
                           connection_result=connection_result)


# Route - Test Endpoints
@provdir_bp.route('/test_endpoints', methods=['GET'])
def test_endpoints():
    """Test Provider Directory Endpoints"""
    # Get the base URL from the query string
    base_url = request.args.get('base_url')

    # Endpoints to test
    endpoints = [
        'Practitioner',
        'Organization',
        'Location',
        'HealthcareService',
        'Endpoint',
        'PractitionerRole'
    ]

    # Store results in a dictionary
    results = {}

    for endpoint in endpoints:
        try:
            response = requests.get(
                base_url + f"fhirprovdir/{endpoint}", timeout=15)
            response.raise_for_status()
            data = response.json()
            total = data['total']
            # Return the data and total to results
            results[endpoint] = total
        except requests.exceptions.RequestException as e:
            results[endpoint] = f"Failed: {e}"

    return render_template('provdir/test_results.html',
                           results=results)
