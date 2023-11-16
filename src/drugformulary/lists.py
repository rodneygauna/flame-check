"""
Flame Check - Drug Formulary
List Endpoint
"""

# Imports
import requests
import random


# List Comments
search_parameter_comments = {
    'identifier': 'formulary_plan.formulary_id',
    'status': 'formulary_plan.list_status',
    '_id': 'formulary_plan.formulary_id',
    '_lastUpdated': 'HealthTrio will populate this field with the '
                    'timestamp of when the record was last updated',
}


# List Elements
def get_first_entry(base_url):
    """Get the first entry from the List endpoint"""
    try:
        response = requests.get(
            base_url + "fhirformulary/List", timeout=15)
        response.raise_for_status()
        data = response.json()
        return data['entry'][0]
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Failed to get first entry: {e}") from e


def get_entries(base_url):
    """Get 10 random entries from the List endpoint"""
    try:
        response = requests.get(
            base_url + "fhirformulary/List", timeout=60)
        response.raise_for_status()
        data = response.json()
        total = data['total']
        if total == 0:
            return []
        elif total <= 10:
            return data['entry']
        else:
            return random.sample(data['entry'], 10)
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Failed to get entries: {e}") from e


def get_identifier(first_entry):
    """Get the identifier from the first entry"""
    try:
        return first_entry['resource']['identifier'][0]['value']
    except KeyError:
        return "Identifier not found"


def get_status(first_entry):
    """Get the status from the first entry"""
    try:
        return first_entry['resource']['status']
    except KeyError:
        return "Status not found"


def get_id(first_entry):
    """Get the ID from the first entry"""
    try:
        return first_entry['resource']['id']
    except KeyError:
        return "ID not found"


def get_last_updated(first_entry):
    """Get the last updated timestamp from the first entry"""
    try:
        return first_entry['resource']['meta']['lastUpdated']
    except KeyError:
        return "Last Updated not found"
