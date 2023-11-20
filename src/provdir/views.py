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
@provdir_bp.route('/provdir/healthcareservice_test', methods=['GET'])
def healthcareservice_test():
    """Test HealthcareService Search Parameters"""
    # Get the base URL from the query string
    base_url = request.args.get('base_url')

    # Search Parameters to test
    search_parameters = [
        'location',
        # 'coverage-area',
        'organization',
        #'endpoint',
        'name',
        'service-category',
        'service-type',
        'specialty',
        '_id',
        '_lastUpdated',
    ]

    # Navigate to the endpoint and store the first entry in the results
    results = {}
    try:
        response = requests.get(
            base_url + f"fhirprovdir/HealthcareService", timeout=15)
        response.raise_for_status()
        data = response.json()
        first_entry = data['entry'][0]
        # Return the data for the search parameters to results
        results['location'] = first_entry['location'][0]['reference']
        #results['coverage-area'] = first_entry['coverageArea'][0]['reference']
        results['organization'] = first_entry['providedBy']['reference']
        #results['endpoint'] = first_entry['endpoint'][0]['reference']
        results['name'] = first_entry['name']
        results['service-category'] = first_entry['category'][0]['coding'][0]['code']
        results['service-type'] = first_entry['extension'][0]['extension'][0]['valueCodeableConcept']['coding'][0]['code']
        results['specialty'] = first_entry['specialty'][0]['coding'][0]['code']
        results['_id'] = first_entry['id']
        results['_lastUpdated'] = first_entry['meta']['lastUpdated']
    except requests.exceptions.RequestException as e:
        results['location'] = f"Failed: {e}"
        #results['coverage-area'] = f"Failed: {e}"
        results['organization'] = f"Failed: {e}"
        #results['endpoint'] = f"Failed: {e}"
        results['name'] = f"Failed: {e}"
        results['service-category'] = f"Failed: {e}"
        results['service-type'] = f"Failed: {e}"
        results['specialty'] = f"Failed: {e}"
        results['_id'] = f"Failed: {e}"
        results['_lastUpdated'] = f"Failed: {e}"

    return render_template('provdir/test_results.html',
                           results=results)