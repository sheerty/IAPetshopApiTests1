import allure
import jsonschema
import requests
import pytest
from .schemas.store_schema import STORE_SCHEMA
from .schemas.inventory_schema import INVENTORY_SCHEMA

base_url = 'http://5.181.109.28:9090/api/v3'


@allure.feature("Store")
class TestStore:
    @allure.title("Размещение заказа")
    def test_create_order(self):
        with allure.step('Подготовка данных для размещения заказа'):
            payload = {"id": 1, "petId": 1, "quantity": 1, "status": "placed", "complete": True}

        with allure.step('Отправка запроса на размещение заказа'):
            response = requests.post(f'{base_url}/store/order', json=payload)
            response_json = response.json()

        with allure.step('Проверка статус кода'):
            assert response.status_code == 200, 'Код не совпал'

        with allure.step('Проверка ответа запроса'):
            jsonschema.validate(response.json(), STORE_SCHEMA)

        with allure.step('Проверка параметров ответа'):
            assert response_json['id'] == payload['id'], 'Айди не совпало'
            assert response_json['petId'] == payload['petId'], 'Айди животного не совпало'
            assert response_json['quantity'] == payload['quantity'], 'Кол-во не совпало'
            assert response_json['status'] == payload['status'], 'Статус не совпало'
            assert response_json['complete'] == payload['complete'], 'Заверешние не совпало'

    @allure.title("Получение информации о заказе по ID")
    def test_get_order_by_id(self, create_order):
        with allure.step('Получение ID заказа'):
            order_id = create_order['id']
        with allure.step('Отправка запроса на получение заказа по ID'):
            response = requests.get(f'{base_url}/store/order/{order_id}')
            response_json = response.json()

        with allure.step('Проверка кода ответа'):
            assert response.status_code == 200, 'Код не совпал'

        with allure.step('Проверка содержимой инфы в ответе'):
            assert response_json['id'] == create_order['id'], 'Айди совпало'

        with allure.step('Проверка ответа'):
            jsonschema.validate(response.json(), STORE_SCHEMA)

    @allure.title("Удаление заказа по ID")
    def test_delete_order_by_id(self, create_order):
        with allure.step('Получение ID заказа'):
            order_id = create_order['id']

        with allure.step('Удаление заказа по ID'):
            response = requests.delete(f'{base_url}/store/order/{order_id}')

        with allure.step('Проверка код статуса'):
            assert response.status_code == 200, 'Код совпал'

        with allure.step('Проверка заказа на удаление и кода'):
            response = requests.get(f'{base_url}/store/order/{order_id}')
            assert response.status_code == 404, "Код не совпал"

    @allure.title("Попытка получить информацию о несуществующем заказе")
    def test_get_order_by_nonexistant_id(self):
        with allure.step('Отправка запроса на получение оредра по не сущетсвующиму айди'):
            response = requests.get(f'{base_url}/store/order/99999999')

        with allure.step('Проверка код статуса и текста'):
            assert response.status_code == 404, 'Код не воспал'
            assert response.text == 'Order not found', "Текст не совпал"

    @allure.title("Получение инвентаря магазина")
    def test_get_inventory(self):
        with allure.step('Отправка запроса на получение инвентаря'):
            response = requests.get(f'{base_url}/store/inventory')

        with allure.step('Проверка статуса ответа'):
            assert response.status_code == 200, 'Код не совпал'

        with allure.step('проверка ответа '):
            jsonschema.validate(response.json(), INVENTORY_SCHEMA)