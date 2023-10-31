"""
Flame Check - Provider Directory
InsurancePlan Endpoint
"""

# Imports
import requests


# InsurancePlan Comments
search_parameter_comments = {
    'administered-by': 'References PlannetOrganization (medical_group.external_medical_group_id)',
    'owned-by': 'References PlannetOrganization (medical_group.external_medical_group_id)',
    'coverage-area': 'Currently not supported by HealthTrio',
    'name': 'benefit_plan_name.plan_name',
    'plan-type': 'Currently not supported by HealthTrio',
    'identifier': 'Currently not supported by HealthTrio',
    'type': 'business.business_name',
    '_id': 'benefit_plan_.external_benefit_plan_id',
    '_lastUpdated': 'benefit_plan.external_change_date (max value)',
}


# InsurancePlan Elements
def get_first_entry(base_url):
    """Get the first entry from the InsurancePlan endpoint"""
    try:
        response = requests.get(
            base_url + "fhirprovdir/InsurancePlan", timeout=15)
        response.raise_for_status()
        data = response.json()
        return data['entry'][0]
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Failed to get first entry: {e}") from e


def get_administer_by(first_entry):
    """Get the administer-by from the first entry"""
    try:
        return first_entry['resource']['administeredBy'][0]['reference']
    except KeyError:
        return "Administered By not found"


def get_owned_by(first_entry):
    """Get the owned-by from the first entry"""
    try:
        return first_entry['resource']['ownedBy']['reference']
    except KeyError:
        return "Owned By not found"


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


def get_plan_type(first_entry):
    """Get the plan type from the first entry"""
    try:
        return first_entry['resource']['plan'][0]['type']['coding'][0]['display']
    except KeyError:
        return "Plan Type not found"


def get_identifier(first_entry):
    """Get the identifier from the first entry"""
    try:
        return first_entry['resource']['identifier'][0]['value']
    except KeyError:
        return "Identifier not found"


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
