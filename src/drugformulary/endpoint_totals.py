"""
Flame-Check - Provider Directory
Endpoint Totals
"""

# Imports
import requests


# Endpoint Totals
def get_endpoint_total(base_url, endpoint):
    """Get the total number of entries for an endpoint"""
    try:
        response = requests.get(
            base_url + f"fhirformulary/{endpoint}", timeout=15)
        response.raise_for_status()
        data = response.json()
        return data['total']
    except requests.exceptions.RequestException as e:
        return f"Failed: {e}"
