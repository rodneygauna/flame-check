"""
Flame-Check - Provider Directory
Practitioner Endpoint
"""

# Imports
import requests


# Practitioner Comments
search_parameter_comments = {
    'name': 'Combination of provider.physician_first_name, provider.physician_middle_name, and provider.physician_last_name ',
    'family-name': 'provider.physician_last_name',
    'given-name': 'provider.physician_first_name and provider.physician_middle_name',
    '_id': 'provider.external_provider_id',
    '_lastUpdated': 'provider.external_change_date'
}


# Practitioner Endpoint
def get_first_entry(base_url):
    """Get the first entry from the Practitioner endpoint"""
    try:
        response = requests.get(
            base_url + "fhirprovdir/Practitioner", timeout=15)
        response.raise_for_status()
        data = response.json()
        return data['entry'][0]
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Failed to get first entry: {e}") from e


def get_name(first_entry):
    """Get the name from the first entry"""
    try:
        return first_entry['resource']['name'][0]['text']
    except KeyError:
        return "Name not found"


def get_family_name(first_entry):
    """Get the family name from the first entry"""
    try:
        return first_entry['resource']['name'][0]['family']
    except KeyError:
        return "Family name not found"


def get_given_name(first_entry):
    """Get the given name from the first entry"""
    try:
        return first_entry['resource']['name'][0]['given'][0]
    except KeyError:
        return "Given name not found"


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
