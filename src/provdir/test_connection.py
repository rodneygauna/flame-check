"""
Flame-Check - Provider Directory
Test connection to a FHIR server
"""

# Imports
import requests


# Test Connection
def test_connection(api_endpoint):
    """Test the connection to the API endpoint"""
    try:
        response = requests.get(api_endpoint, timeout=10)
        response.raise_for_status()
        return {'success': True, 'message': 'Connection successful'}
    except requests.exceptions.RequestException as e:
        return {'success': False, 'message': f'Connection failed: {e}'}
