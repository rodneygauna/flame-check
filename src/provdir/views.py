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
    practitionerrole,
    insuranceplan,
    location,
    organization,
    organizationaffiliation,
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
        'OrganizationAffiliation',
        'Location',
        'HealthcareService',
        'Endpoint',
        'PractitionerRole',
        'InsurancePlan',
    ]

    # Store results in a dictionary
    results = {endpoint: get_endpoint_total(
        base_url, endpoint) for endpoint in endpoints}

    return render_template('provdir/results_endpoints.html',
                           base_url=base_url,
                           results=results)


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
        return render_template('provdir/results_search_parameters.html',
                               results=results,
                               search_parameter_comments=healthcareservice.search_parameter_comments)

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

    return render_template('provdir/results_search_parameters.html',
                           results=results,
                           search_parameter_comments=healthcareservice.search_parameter_comments)


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
        return render_template('provdir/results_search_parameters.html',
                               results=results,
                               search_parameter_comments=practitioner.search_parameter_comments)

    # Get the various fields from the first entry
    results = {
        'name': practitioner.get_name(first_entry),
        'family-name': practitioner.get_family_name(first_entry),
        'given-name': practitioner.get_given_name(first_entry),
        '_id': practitioner.get_id(first_entry),
        '_lastUpdated': practitioner.get_last_updated(first_entry)
    }

    return render_template('provdir/results_search_parameters.html',
                           results=results,
                           search_parameter_comments=practitioner.search_parameter_comments)


# Route - Test InsurancePlan Search Paramters
@provdir_bp.route('/insuranceplan_test', methods=['GET'])
def insuranceplan_test():
    """Test InsuranceType Search Parameters"""
    # Get the base URL from the query string
    base_url = request.args.get('base_url')

    # Get the first entry from the endpoint
    try:
        first_entry = insuranceplan.get_first_entry(base_url)
    except requests.exceptions.RequestException as e:
        results = {'error': str(e)}
        return render_template('provdir/results_search_parameters.html',
                               results=results)

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

    return render_template('provdir/results_search_parameters.html',
                           results=results,
                           search_parameter_comments=insuranceplan.search_parameter_comments)


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
        return render_template('provdir/results_search_parameters.html',
                               results=results)

    # Get the various fields from the first entry
    results = {
        'partOf': location.get_part_of(first_entry),
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

    return render_template('provdir/results_search_parameters.html',
                           results=results,
                           search_parameter_comments=location.search_parameter_comments)


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
        return render_template('provdir/results_search_parameters.html',
                               results=results,
                               search_parameter_comments=organization.search_parameter_comments)

    # Get the various fields from the first entry
    results = {
        'partOf': organization.get_part_of(first_entry),
        'endpoint': organization.get_endpoint(first_entry),
        'address': organization.get_address(first_entry),
        'name': organization.get_name(first_entry),
        'type': organization.get_type(first_entry),
        'coverage-area': organization.get_coverage_area(first_entry),
        '_id': organization.get_id(first_entry),
        '_lastUpdated': organization.get_last_updated(first_entry)
    }

    return render_template('provdir/results_search_parameters.html',
                           results=results,
                           search_parameter_comments=organization.search_parameter_comments)


# Route - Test OrganizationAffiliation Search Paramters
@provdir_bp.route('/organizationaffiliation_test', methods=['GET'])
def organizationaffiliation_test():
    """Test OrganizationAffiliation Search Parameters"""
    # Get the base URL from the query string
    base_url = request.args.get('base_url')

    # Get the first entry from the endpoint
    try:
        first_entry = organizationaffiliation.get_first_entry(base_url)
    except requests.exceptions.RequestException as e:
        results = {'error': str(e)}
        return render_template('provdir/results_search_parameters.html',
                               results=results,
                               search_parameter_comments=organizationaffiliation.search_parameter_comments)

    # Get the various fields from the first entry
    results = {
        'primary-organization': organizationaffiliation.get_primary_organization(first_entry),
        'participating-organization': organizationaffiliation.get_participating_organization(first_entry),
        'location': organizationaffiliation.get_location(first_entry),
        'service': organizationaffiliation.get_service(first_entry),
        'network': organizationaffiliation.get_network(first_entry),
        'endpoint': organizationaffiliation.get_endpoint(first_entry),
        'role': organizationaffiliation.get_role(first_entry),
        'specialty': organizationaffiliation.get_specialty(first_entry),
        '_id': organizationaffiliation.get_id(first_entry),
        '_lastUpdated': organizationaffiliation.get_last_updated(first_entry)
    }

    return render_template('provdir/results_search_parameters.html',
                           results=results,
                           search_parameter_comments=organizationaffiliation.search_parameter_comments)


# Route - Test PractitionerRole Search Paramters
@provdir_bp.route('/practitionerrole_test', methods=['GET'])
def practitionerrole_test():
    """Test PractitionerRole Search Parameters"""
    # Get the base URL from the query string
    base_url = request.args.get('base_url')

    # Get the first entry from the endpoint
    try:
        first_entry = practitionerrole.get_first_entry(base_url)
    except requests.exceptions.RequestException as e:
        results = {'error': str(e)}
        return render_template('provdir/results_search_parameters.html',
                               results=results,
                               search_parameter_comments=practitionerrole.search_parameter_comments)

    # Get the various fields from the first entry
    results = {
        'practitioner': practitionerrole.get_practitioner(first_entry),
        'organization': practitionerrole.get_organization(first_entry),
        'location': practitionerrole.get_location(first_entry),
        'service': practitionerrole.get_service(first_entry),
        'network': practitionerrole.get_network(first_entry),
        'endpoint': practitionerrole.get_endpoint(first_entry),
        'role': practitionerrole.get_role(first_entry),
        'specialty': practitionerrole.get_specialty(first_entry),
        '_id': practitionerrole.get_id(first_entry),
        '_lastUpdated': practitionerrole.get_last_updated(first_entry)
    }

    return render_template('provdir/results_search_parameters.html',
                           results=results,
                           search_parameter_comments=practitionerrole.search_parameter_comments)
