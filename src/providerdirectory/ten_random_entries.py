""""Store 10 random entries from the API endpoint in a list"""

# Imports
import requests
import random


# Get 10 random entries from the API endpoint
def get_entries(base_url, endpoint):
    """Get 10 random entries from the API endpoint"""
    try:
        response = requests.get(
            base_url + "fhirformulary/" + endpoint, timeout=60)
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
