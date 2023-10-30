"""
Flame Check - Provider Directory
Organization Endpoint
"""

# Imports
import requests


# Organization
def get_first_entry(base_url):
    """Get the first entry from the Organization endpoint"""
    try:
        response = requests.get(
            base_url + "fhirprovdir/Organization", timeout=15)
        response.raise_for_status()
        data = response.json()
        return data['entry'][0]
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Failed to get first entry: {e}") from e


def get_part_of(first_entry):
    """Get the part-of from the first entry"""
    try:
        return first_entry['resource']['partOf']['reference']
    except KeyError:
        return "Part Of not found"


def get_endpoint(first_entry):
    """Get the endpoint from the first entry"""
    try:
        return first_entry['resource']['endpoint'][0]['reference']
    except KeyError:
        return "Endpoint not found"


def get_address(first_entry):
    """Get the address city from the first entry"""
    try:
        return first_entry['resource']['address'][0]['text']
    except KeyError:
        return "Address not found"


def get_name(first_entry):
    """Get the name from the first entry"""
    try:
        return first_entry['resource']['name']
    except KeyError:
        return "Name not found"


def get_type(first_entry):
    """Get the type from the first entry"""
    try:
        return first_entry['resource']['type'][0]['coding'][0]['code']
    except KeyError:
        return "Type not found"


def get_coverage_area(first_entry):
    """Get the coverage area from the first entry"""
    try:
        return first_entry['resource']['coverageArea'][0]['reference']
    except KeyError:
        return "Coverage Area not found"


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
