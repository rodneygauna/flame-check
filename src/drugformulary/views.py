"""
Flame Check
Views for the Drug Formulary API testing
"""

# Imports
import requests
from flask import (
    render_template, Blueprint, request, redirect, url_for
)

from .test_connection import test_connection
from .endpoint_totals import get_endpoint_total
from . import (
    medicationknowledge,
    lists,
)


# Blueprint
drugformulary_bp = Blueprint('drugformulary', __name__)


# Route - Landing Page
@drugformulary_bp.route('/drugformulary', methods=['GET', 'POST'])
def index():
    """Landing Page"""

    if request.method == 'POST':
        base_url = request.form.get('base_url')

        # Ensure the URL starts with https:// and ends with a slash
        if not base_url.startswith('https://'):
            base_url = f'https://{base_url}'
        if not base_url.endswith('/'):
            base_url = f'{base_url}/'

        api_endpoint = f"{base_url}fhirformulary/MedicationKnowledge"

        connection_result = test_connection(api_endpoint)

        if connection_result['success']:
            return redirect(url_for('drugformulary.test_endpoints',
                                    base_url=base_url))
        else:
            return render_template('drugformulary/index.html',
                                   title='Flame Check - Drug Formulary',
                                   connection_result=(
                                       connection_result['message']))

    return render_template('drugformulary/index.html',
                           title='Flame Check - Drug Formulary')


# Route - Test Endpoints
@drugformulary_bp.route('/drugformulary/test_endpoints',
                        methods=['GET'])
def test_endpoints():
    """Test Drug Formulary Endpoints"""
    # Get the base URL from the query string
    base_url = request.args.get('base_url')

    # Endpoints to test
    endpoints = [
        'List',
        'MedicationKnowledge',
    ]

    # Store results in a dictionary
    results = {endpoint: get_endpoint_total(
        base_url, endpoint) for endpoint in endpoints}

    return render_template('global/results_endpoints.html',
                           title='Flame Check - Test Endpoints',
                           base_url=base_url,
                           results=results)


# Route - Test MedicationKnowledge Search Parameters
@drugformulary_bp.route('/drugformulary/medicationknowledge_test',
                        methods=['GET'])
def medicationknowledge_test():
    """Test MedicationKnowledge Search Parameters"""
    base_url = request.args.get('base_url')
    try:
        first_entry = medicationknowledge.get_first_entry(base_url)
    except requests.exceptions.RequestException as e:
        results = {'error': str(e)}
        return render_template('global/results_search_parameters.html',
                               title='Flame Check - Test MedicationKnowledge',
                               results=results,
                               search_parameter_comments=(
                                   medicationknowledge
                                   .search_parameter_comments
                               ))

    # Get the various fields from the first entry
    results = {
        'status': medicationknowledge.get_status(first_entry),
        'code': medicationknowledge.get_code(first_entry),
        'drug-name': medicationknowledge.get_drug_name(first_entry),
        'doseform': medicationknowledge.get_doseform(first_entry),
        '_id': medicationknowledge.get_id(first_entry),
        '_lastUpdated': medicationknowledge.get_last_updated(first_entry)
    }

    return render_template('global/results_search_parameters.html',
                           title='Flame Check - Test medicationknowledge',
                           results=results,
                           search_parameter_comments=(
                               medicationknowledge.search_parameter_comments))


# Route - Test MedicationKnowledge Required Data Elements with 10 Random Entries
@drugformulary_bp.route('/drugformulary/medicationknowledge_required',
                        methods=['GET'])
def medicationknowledge_required():
    """Test MedicationKnowledge Required Data Elements with 10 Random Entries"""
    base_url = request.args.get('base_url')
    try:
        entries = medicationknowledge.get_entries(base_url)
    except requests.exceptions.RequestException as e:
        results = {'error': str(e)}
        return render_template('global/results_required.html',
                               title='Flame Check - Required Data Elements',
                               results=results,)

    # Loop through the entries and get the various fields
    results = []
    for entry in entries:
        results.append({
            '_id': medicationknowledge.get_id(entry),
            '_lastUpdated': medicationknowledge.get_last_updated(entry),
            'code': medicationknowledge.get_code(entry),
            'drug-name': medicationknowledge.get_drug_name(entry),
            'status': medicationknowledge.get_status(entry),
            'doseform': medicationknowledge.get_doseform(entry),
        })

    return render_template('global/results_required.html',
                           title='Flame Check - Required Data Elements',
                           results=results,)


# Route - Test List Search Parameters
@drugformulary_bp.route('/drugformulary/list_test',
                        methods=['GET'])
def list_test():
    """Test List Search Parameters"""
    base_url = request.args.get('base_url')
    try:
        first_entry = lists.get_first_entry(base_url)
    except requests.exceptions.RequestException as e:
        results = {'error': str(e)}
        return render_template('global/results_search_parameters.html',
                               title='Flame Check - Test List',
                               results=results,
                               search_parameter_comments=(
                                   lists.search_parameter_comments
                               ))

    # Get the various fields from the first entry
    results = {
        'identifier': lists.get_identifier(first_entry),
        'status': lists.get_status(first_entry),
        '_id': lists.get_id(first_entry),
        '_lastUpdated': lists.get_last_updated(first_entry)
    }

    return render_template('global/results_search_parameters.html',
                           title='Flame Check - Test List',
                           results=results,
                           search_parameter_comments=(
                               lists.search_parameter_comments))


# Route - Test List Required Data Elements with 10 Random Entries
@drugformulary_bp.route('/drugformulary/list_required',
                        methods=['GET'])
def list_required():
    """Test List Required Data Elements with 10 Random Entries"""
    base_url = request.args.get('base_url')
    try:
        entries = lists.get_entries(base_url)
    except requests.exceptions.RequestException as e:
        results = {'error': str(e)}
        return render_template('global/results_required.html',
                               title='Flame Check - Required Data Elements',
                               results=results,)

    # Loop through the entries and get the various fields
    results = []
    for entry in entries:
        results.append({
            '_id': lists.get_id(entry),
            '_lastUpdated': lists.get_last_updated(entry),
            'identifier': lists.get_identifier(entry),
            'status': lists.get_status(entry),
        })

    return render_template('global/results_required.html',
                           title='Flame Check - Required Data Elements',
                           results=results,)
