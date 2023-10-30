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
from . import (
    healthcareservice,
    practitioner,
    insuranceplan,
    location,
    organization,
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
        first_entry = healthcareservice.get_first_entry(base_url)
    except requests.exceptions.RequestException as e:
        results = {'error': str(e)}
        return render_template('provdir/test_results.html', results=results)

    # Get the various fields from the first entry
    results = {
        'location': healthcareservice.get_location(first_entry),
        'organization': healthcareservice.get_organization(first_entry),
        'endpoint': healthcareservice.get_endpoint(first_entry),
        'name': healthcareservice.get_name(first_entry),
        'service-category': healthcareservice.get_service_category(first_entry),
        'service-type': healthcareservice.get_service_type(first_entry),
        'specialty': healthcareservice.get_specialty(first_entry),
        '_id': healthcareservice.get_id(first_entry),
        '_lastUpdated': healthcareservice.get_last_updated(first_entry)
    }

    return render_template('provdir/test_results.html',
                           results=results)


# Route - Test Practitioner Search Paramters
@provdir_bp.route('/practitioner_test', methods=['GET'])
def practitioner_test():
    """Test Practitioner Search Parameters"""
    # Get the base URL from the query string
    base_url = request.args.get('base_url')

    # Get the first entry from the endpoint
    try:
        first_entry = practitioner.get_first_entry(base_url)
    except requests.exceptions.RequestException as e:
        results = {'error': str(e)}
        return render_template('provdir/test_results.html', results=results)

    # Get the various fields from the first entry
    results = {
        'name': practitioner.get_name(first_entry),
        'family-name': practitioner.get_family_name(first_entry),
        'given-name': practitioner.get_given_name(first_entry),
        '_id': practitioner.get_id(first_entry),
        '_lastUpdated': practitioner.get_last_updated(first_entry)
    }

    return render_template('provdir/test_results.html',
                           results=results)


# Route - Test InsurancePlan Search Paramters
@provdir_bp.route('/insuranceplan_test', methods=['GET'])
def insurancetype_test():
    """Test InsuranceType Search Parameters"""
    # Get the base URL from the query string
    base_url = request.args.get('base_url')

    # Get the first entry from the endpoint
    try:
        first_entry = insuranceplan.get_first_entry(base_url)
    except requests.exceptions.RequestException as e:
        results = {'error': str(e)}
        return render_template('provdir/test_results.html', results=results)

    # Get the various fields from the first entry
    results = {
        'administered-by': insuranceplan.get_administer_by(first_entry),
        'owned-by': insuranceplan.get_owned_by(first_entry),
        'coverage-area': insuranceplan.get_coverage_area(first_entry),
        'name': insuranceplan.get_name(first_entry),
        'plan-type': insuranceplan.get_plan_type(first_entry),
        'type': insuranceplan.get_type(first_entry),
        'identifier': insuranceplan.get_identifier(first_entry),
        '_id': insuranceplan.get_id(first_entry),
        '_lastUpdated': insuranceplan.get_last_updated(first_entry)
    }

    return render_template('provdir/test_results.html',
                           results=results)


# Route - Test Location Search Paramters
@provdir_bp.route('/location_test', methods=['GET'])
def location_test():
    """Test Location Search Parameters"""
    # Get the base URL from the query string
    base_url = request.args.get('base_url')

    # Get the first entry from the endpoint
    try:
        first_entry = location.get_first_entry(base_url)
    except requests.exceptions.RequestException as e:
        results = {'error': str(e)}
        return render_template('provdir/test_results.html', results=results)

    # Get the various fields from the first entry
    results = {
        'part-of': location.get_part_of(first_entry),
        'organization': location.get_organization(first_entry),
        'endpoint': location.get_endpoint(first_entry),
        'address-city': location.get_address_city(first_entry),
        'address-state': location.get_address_state(first_entry),
        'address-postalcode': location.get_address_postalcode(first_entry),
        'address': location.get_address(first_entry),
        'type': location.get_type(first_entry),
        '_id': location.get_id(first_entry),
        '_lastUpdated': location.get_last_updated(first_entry)
    }

    return render_template('provdir/test_results.html',
                           results=results)


# Route - Test Organization Search Paramters
@provdir_bp.route('/organization_test', methods=['GET'])
def organization_test():
    """Test Organization Search Parameters"""
    # Get the base URL from the query string
    base_url = request.args.get('base_url')

    # Get the first entry from the endpoint
    try:
        first_entry = organization.get_first_entry(base_url)
    except requests.exceptions.RequestException as e:
        results = {'error': str(e)}
        return render_template('provdir/test_results.html', results=results)

    # Get the various fields from the first entry
    results = {
        'part-of': organization.get_part_of(first_entry),
        'endpoint': organization.get_endpoint(first_entry),
        'address': organization.get_address(first_entry),
        'name': organization.get_name(first_entry),
        'type': organization.get_type(first_entry),
        'coverage-area': organization.get_coverage_area(first_entry),
        '_id': organization.get_id(first_entry),
        '_lastUpdated': organization.get_last_updated(first_entry)
    }

    return render_template('provdir/test_results.html',
                           results=results)
