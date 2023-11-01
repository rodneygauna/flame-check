"""
Flame Check - Provider Directory
Location Endpoint
"""

# Imports
import requests


# Location Comments
search_parameter_comments = {
    'partof': 'Currently not supported by HealthTrio',
    'organization': 'References PlannetOrganization (medical_group.external_medical_group_id)',
    'endpoint': 'Currently not supported by HealthTrio',
    'address-city': 'medical_group_address.city',
    'address-state': 'medical_group_address.state',
    'address-postalcode': 'medical_group_address.zip',
    'address': 'Generated from medical_group_address.address1, medical_group_address.address2, medical_group_address.city, medical_group_address.state, medical_group_address.zip, and medical_group_address.country',
    'type': 'Currently not supported by HealthTrio',
    '_id': 'medical_group_address.address_id',
    '_lastUpdated': 'medical_group_address.external_change_date'
}


# Location Elements
def get_first_entry(base_url):
    """Get the first entry from the Location endpoint"""
    try:
        response = requests.get(
            base_url + "fhirprovdir/Location", timeout=15)
        response.raise_for_status()
        data = response.json()
        return data['entry'][0]
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Failed to get first entry: {e}") from e


def get_part_of(first_entry):
    """Get the partof from the first entry"""
    try:
        return first_entry['resource']['partOf']['reference']
    except KeyError:
        return "PartOf not found"


def get_organization(first_entry):
    """Get the organization from the first entry"""
    try:
        return first_entry['resource']['managingOrganization']['reference']
    except KeyError:
        return "Organization not found"


def get_endpoint(first_entry):
    """Get the endpoint from the first entry"""
    try:
        return first_entry['resource']['endpoint'][0]['reference']
    except KeyError:
        return "Endpoint not found"


def get_address_city(first_entry):
    """Get the address city from the first entry"""
    try:
        return first_entry['resource']['address']['city']
    except KeyError:
        return "Address City not found"


def get_address_state(first_entry):
    """Get the address state from the first entry"""
    try:
        return first_entry['resource']['address']['state']
    except KeyError:
        return "Address State not found"


def get_address_postalcode(first_entry):
    """Get the address country from the first entry"""
    try:
        return first_entry['resource']['address']['postalCode']
    except KeyError:
        return "Address Country not found"


def get_address(first_entry):
    """Get the address from the first entry"""
    try:
        return first_entry['resource']['address']['text']
    except KeyError:
        return "Address not found"


def get_type(first_entry):
    """Get the type from the first entry"""
    try:
        return first_entry['resource']['type'][0]['coding'][0]['code']
    except KeyError:
        return "Type not found"


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
