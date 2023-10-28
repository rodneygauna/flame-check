"""
Flame Check
Views for the Provider Directory API testing
"""

# Imports
import requests
from flask import (
    render_template, Blueprint, request, redirect, url_for
)

from src.provdir.test_connection import test_connection
from src.provdir.endpoint_totals import get_endpoint_total
from src.provdir.healthservice import (
    get_first_entry, get_location, get_organization, get_endpoint,
    get_name, get_service_category, get_service_type, get_specialty,
    get_id, get_last_updated
)

# Blueprint
provdir_bp = Blueprint('provdir', __name__)


# Route - Landing Page
@provdir_bp.route('/provdir', methods=['GET', 'POST'])
def index():
    """Landing Page"""

    if request.method == 'POST':
        base_url = request.form.get('base_url')

        # Ensure the URL starts with https:// and ends with a slash
        if not base_url.startswith('https://'):
            base_url = f'https://{base_url}'
        if not base_url.endswith('/'):
            base_url = f'{base_url}/'

        api_endpoint = f"{base_url}fhirprovdir/Practitioner"

        connection_result = test_connection(api_endpoint)

        if connection_result['success']:
            return redirect(url_for('provdir.test_endpoints',
                                    base_url=base_url))
        else:
            return render_template('provdir/index.html',
                                   title='Flame Check - Provider Directory',
                                   connection_result=connection_result['message'])

    return render_template('provdir/index.html',
                           title='Flame Check - Provider Directory')


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
    results = {endpoint: get_endpoint_total(
        base_url, endpoint) for endpoint in endpoints}

    return render_template('provdir/test_results.html', results=results)


# Route - Test HealthcareService Search Paramters
@provdir_bp.route('/healthcareservice_test', methods=['GET'])
def healthcareservice_test():
    """Test HealthcareService Search Parameters"""
    # Get the base URL from the query string
    base_url = request.args.get('base_url')

    # Get the first entry from the endpoint
    try:
        first_entry = get_first_entry(base_url)
    except requests.exceptions.RequestException as e:
        results = {'error': str(e)}
        return render_template('provdir/test_results.html', results=results)

    # Get the various fields from the first entry
    results = {
        'location': get_location(first_entry),
        'organization': get_organization(first_entry),
        'endpoint': get_endpoint(first_entry),
        'name': get_name(first_entry),
        'service-category': get_service_category(first_entry),
        'service-type': get_service_type(first_entry),
        'specialty': get_specialty(first_entry),
        '_id': get_id(first_entry),
        '_lastUpdated': get_last_updated(first_entry)
    }

    return render_template('provdir/test_results.html',
                           results=results)
