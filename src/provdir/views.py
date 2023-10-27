"""
Flame Check
Views for the Provider Directory API testing
"""

# Imports
import requests
from flask import (
    render_template, Blueprint, request, redirect, url_for
)

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


# Route - Test HealthcareService Search Paramters
@provdir_bp.route('/healthcareservice_test', methods=['GET'])
def healthcareservice_test():
    """Test HealthcareService Search Parameters"""
    # Get the base URL from the query string
    base_url = request.args.get('base_url')

    # Navigate to the endpoint and store the first entry in the results
    results = {}
    try:
        response = requests.get(
            base_url + "fhirprovdir/HealthcareService", timeout=15)
        response.raise_for_status()
        data = response.json()
        first_entry = data['entry'][0]
        try:
            results['location'] = first_entry['resource']['location'][0]['reference']
        except KeyError:
            results['location'] = "Location not found"
        try:
            results['organization'] = first_entry['resource']['providedBy']['reference']
        except KeyError:
            results['organization'] = "Organization not found"
        try:
            results['endpoint'] = first_entry['resource']['endpoint'][0]['reference']
        except KeyError:
            results['endpoint'] = "Endpoint not found"
        try:
            results['name'] = first_entry['resource']['name']
        except KeyError:
            results['name'] = "Name not found"
        try:
            results['service-category'] = first_entry['resource']['category'][0]['coding'][0]['code']
        except KeyError:
            results['service-category'] = "Service Category not found"
        try:
            results['service-type'] = first_entry['resource']['extension'][0]['extension'][0]['valueCodeableConcept']['coding'][0]['code']
        except KeyError:
            results['service-type'] = "Service Type not found"
        try:
            results['specialty'] = first_entry['resource']['specialty'][0]['coding'][0]['code']
        except KeyError:
            results['specialty'] = "Specialty not found"
        try:
            results['_id'] = first_entry['resource']['id']
        except KeyError:
            results['_id'] = "ID not found"
        try:
            results['_lastUpdated'] = first_entry['resource']['meta']['lastUpdated']
        except KeyError:
            results['_lastUpdated'] = "Last Updated not found"
    except requests.exceptions.RequestException as e:
        results['error'] = f"Failed: {e}"

    return render_template('provdir/test_results.html',
                           results=results)
