import allure
import jsonschema
import requests
from .schemas.pet_schema import PET_SCHEMA

base_url = 'http://5.181.109.28:9090/api/v3'

@allure.feature("Pet")
class TestPet:
    @allure.title("Попытка удалить несуществующего питомца")
    def test_delete_nonexistent_pet(self):
        with allure.step('Отправка запроса на удаление несуществующего питомца'):
            response = requests.delete(url=f'{base_url}/pet/9999')

        with allure.step('Проверка статуса ответа'):
            assert response.status_code == 200, "Код не совпал"


        with allure.step('Проверка текста'):
            assert response.text == "Pet deleted", "Текст не совпал"

    @allure.title("Попытка обновить несуществующего питомца ")
    def test_update_nonexistent_pet(self):
        with allure.step('Подготовка данных на изменение несуществующего питомца'):
            payload = {
                "id": 9999,
                "name": "Non-existent Pet",
                "status": "available"
            }
        with allure.step('Отправка запроса на изменение несуществующего питомца'):
            response = requests.put(url=f'{base_url}/pet', json=payload)

        with allure.step('Проверка статуса ответа'):
            assert response.status_code == 404, "Код не совпал"

        with allure.step('Проверка текста ответа'):
            assert response.text == "Pet not found", "Текст не совпал"

    @allure.title("Добавление нового питомца")
    def test_add_pet(self):
        with allure.step('Подготовка данных для создания питомца'):
            payload = {
                "id": 1,
                "name": "Buddy",
                "status": "available"
            }
        with allure.step('Отправка запроса для создания питомца'):
            response = requests.post(url=f'{base_url}/pet', json=payload)
            respone_json = response.json()

        with allure.step('Проверка статуса кода'):
            assert response.status_code == 200, "Код не совпал"

        with allure.step('Проверка ответа запроса'):
            jsonschema.validate(response.json(), PET_SCHEMA)

        with allure.step('Проверка параметров питомца в ответе'):
            assert respone_json['id'] == payload['id'], 'Айди не совпало'
            assert respone_json['name'] == payload['name'] , 'Имя не совпало'
            assert respone_json['status'] == payload['status'] , 'Статус не совпало'

    @allure.title("Попытка получить информацию о несуществующем питомце")
    def test_update_nonexistent_pet(self):
        with allure.step('Попытка получить информацию о несуществующем питомце'):
            response = requests.get(url=f'{base_url}/pet/9999')

        with allure.step('Проверка статус кода'):
            assert response.status_code == 404, "Статус кода не совпал"
        with allure.step('Проверка сообщения'):
            assert response.text == "Pet not found", "Текст не совпал"


