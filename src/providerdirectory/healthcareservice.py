"""
Flame Check - Provider Directory
HealthcareService Endpoint
"""

# Imports
import requests


# HealthcareService Comments
search_parameter_comments = {
    'location': 'References PlannetLocation '
                '(medical_group_address.address_id)',
    'organization': 'References PlannetOrganization '
    '(medical_group.external_medical_group_id)',
    'endpoint': 'Currently not supported by HealthTrio',
    'coverage-area': 'Currently not supported by HealthTrio',
    'name': 'medical_group.medical_group_name',
    'service-category': 'Code value: '
                        'provider_payor_provservicetypes.provservicetype '
                        'Display value: '
                        'payor_provservicetypes.provservicetype_description',
    'service-type': 'HealthTrio populates "FILL" for this field',
    'specialty': 'provider_medical_group_contract.taxonomy_code',
    '_id': 'Combination of medical_group_address.provider_id, '
           'medical_group_address.medical_group_id, '
           'and medical_group_address.address_id',
    '_lastUpdated': 'provider_payor_provservicetype.change_date (max value)'
}


# HealthcareService Elements
def get_first_entry(base_url):
    """Get the first entry from the HealthcareService endpoint"""
    try:
        response = requests.get(
            base_url + "fhirprovdir/HealthcareService", timeout=15)
        response.raise_for_status()
        data = response.json()
        return data['entry'][0]
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Failed to get first entry: {e}") from e


def get_location(first_entry):
    """Get the location from the first entry"""
    try:
        return first_entry['resource']['location'][0]['reference']
    except KeyError:
        return "Location not found"


def get_organization(first_entry):
    """Get the organization from the first entry"""
    try:
        return first_entry['resource']['providedBy']['reference']
    except KeyError:
        return "Organization not found"


def get_endpoint(first_entry):
    """Get the endpoint from the first entry"""
    try:
        return first_entry['resource']['endpoint'][0]['reference']
    except KeyError:
        return "Endpoint not found"


def get_coverage_area(first_entry):
    """Get the coverage area from the first entry"""
    try:
        return first_entry['resource']['coverageArea'][0]['reference']
    except KeyError:
        return "Coverage Area not found"


def get_name(first_entry):
    """Get the name from the first entry"""
    try:
        return first_entry['resource']['name']
    except KeyError:
        return "Name not found"


def get_service_category(first_entry):
    """Get the service category from the first entry"""
    try:
        return first_entry['resource']['category'][0]['coding'][0]['code']
    except KeyError:
        return "Service Category not found"


def get_service_type(first_entry):
    """Get the service type from the first entry"""
    try:
        return first_entry['resource']['extension'][0]['extension'][0][
            'valueCodeableConcept']['coding'][0]['code']
    except KeyError:
        return "Service Type not found"


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
