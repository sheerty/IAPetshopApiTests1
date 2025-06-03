import pytest
import requests

base_url = 'http://5.181.109.28:9090/api/v3'

@pytest.fixture(scope='function')
def create_pet():
    payload = {
        "id": 1,
        "name": "Buddy",
        "status": "available"
    }

    response = requests.post(f'{base_url}/pet', json=payload)
    assert response.status_code == 200
    return response.json()

@pytest.fixture(scope='function')
def create_order():
    payload = {"id": 1, "petId": 1, "quantity": 1, "status": "placed", "complete": True}

    response = requests.post(f'{base_url}/store/order', json=payload)
    response_json = response.json()

    assert response.status_code == 200
    return response_json