"""
Flame Check - Provider Directory
OrganizationAffiliation Endpoint
"""

# Imports
import requests


# OrganizationAffiliation
def get_first_entry(base_url):
    """Get the first entry from the OrganizationAffiliation endpoint"""
    try:
        response = requests.get(
            base_url + "fhirprovdir/OrganizationAffiliation", timeout=15)
        response.raise_for_status()
        data = response.json()
        return data['entry'][0]
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Failed to get first entry: {e}") from e


def get_primary_organization(first_entry):
    """Get the primary organization from the first entry"""
    try:
        return first_entry['resource']['organization']['reference']
    except KeyError:
        return "Primary Organization not found"


def get_participating_organization(first_entry):
    """Get the participating organization from the first entry"""
    try:
        return first_entry['resource']['participatingOrganization']['reference']
    except KeyError:
        return "Participating Organization not found"


def get_location(first_entry):
    """Get the location from the first entry"""
    try:
        return first_entry['resource']['location'][0]['reference']
    except KeyError:
        return "Location not found"


def get_service(first_entry):
    """Get the service from the first entry"""
    try:
        return first_entry['resource']['healthcareService'][0]['reference']
    except KeyError:
        return "Service not found"


def get_network(first_entry):
    """Get the network from the first entry"""
    try:
        return first_entry['resource']['network'][0]['reference']
    except KeyError:
        return "Network not found"


def get_endpoint(first_entry):
    """Get the endpoint from the first entry"""
    try:
        return first_entry['resource']['endpoint'][0]['reference']
    except KeyError:
        return "Endpoint not found"


def get_role(first_entry):
    """Get the role from the first entry"""
    try:
        return first_entry['resource']['code'][0]['coding'][0]['code']
    except KeyError:
        return "Role not found"


def get_specialty(first_entry):
    """Get the specialty from the first entry"""
    try:
        return first_entry['resource']['specialty'][0]['coding'][0]['code']
    except KeyError:
        return "Specialty not found"


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
