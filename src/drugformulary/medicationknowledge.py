"""
Flame Check - Drug Formulary
MedicationKnowledge Endpoint
"""

# Imports
import requests


# MedicationKnowledge Comments
search_parameter_comments = {
    'status': 'formulary_drug.drug_status',
    'code': 'formulary_drug.rxcui',
    'drug-name': 'formulary_drug.drug_name',
    'doseform': 'This search parameter is not supported by HealthTrio '
                'nor does it appear in the IG examples for '
                'MedicationKnowledge as a data element',
    '_id': 'Combination of formulary_drug.formulary_id and '
           'formulary_drug.rxcui',
    '_lastUpdated': 'HealthTrio will populate this field with the '
                    'timestamp of when the record was last updated'
}


# MedicationKnowledge Elements
def get_first_entry(base_url):
    """Get the first entry from the MedicationKnowledge endpoint"""
    try:
        response = requests.get(
            base_url + "fhirformulary/MedicationKnowledge", timeout=15)
        response.raise_for_status()
        data = response.json()
        return data['entry'][0]
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Failed to get first entry: {e}") from e


def get_status(first_entry):
    """Get the status from the first entry"""
    try:
        return first_entry['resource']['status']
    except KeyError:
        return "Status not found"


def get_code(first_entry):
    """Get the code from the first entry"""
    try:
        return first_entry['resource']['code']['coding'][0]['code']
    except KeyError:
        return "Code not found"


def get_drug_name(first_entry):
    """Get the drug-name from the first entry"""
    try:
        return first_entry['resource']['code']['coding'][0]['display']
    except KeyError:
        return "Drug Name not found"


def get_doseform(first_entry):
    """Get the dose-form from the first entry"""
    try:
        return first_entry['resource']['doseForm']['coding'][0]['code']
    except KeyError:
        return "Dose Form not found"


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
