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
            assert respone_json['name'] == payload['name'], 'Имя не совпало'
            assert respone_json['status'] == payload['status'], 'Статус не совпало'

    @allure.title("Попытка получить информацию о несуществующем питомце")
    def test_get_nonexistent_pet(self):
        with allure.step('Попытка получить информацию о несуществующем питомце'):
            response = requests.get(url=f'{base_url}/pet/9999')
        with allure.step('Проверка статус кода'):
            assert response.status_code == 404, "Статус кода не совпал"
        with allure.step('Проверка сообщения'):
            assert response.text == "Pet not found", "Текст не совпал"

    @allure.title("Добавление нового питомца c полными данными")
    def test_add_pet_full_info(self):
        with allure.step('Подготовка данных'):
            payload = {"id": 10,
                       "name": "doggie",
                       "category": {"id": 1,
                                    "name": "Dogs"},
                       "photoUrls": ["string"],
                       "tags": [
                           {"id": 0,
                            "name": "string"}],
                       "status": "available"}
        with allure.step('Отправка запроса для добавления нового питомца c полными данными'):
            response = requests.post(url=f'{base_url}/pet', json=payload)
            response_json = response.json()
        with allure.step('Проверка ответа'):
            jsonschema.validate(response_json, PET_SCHEMA)
        with allure.step('Проверка статуса кода'):
            assert response.status_code == 200, "Статус кода не совпал"
        with allure.step('Проверка параметров питомца в ответе'):
            assert response_json['id'] == response_json['id'], 'Айди не совпало'
            assert response_json['name'] == response_json['name'], 'Нейм не совпало'
            assert response_json['status'] == response_json['status'], 'Статус не совпало'
            assert response_json['photoUrls'] == response_json['photoUrls'], 'Фотоурл не совпало'
            assert response_json['tags'] == response_json['tags'], 'Теги не совпало'
            assert response_json['category'] == response_json['category'], 'Категории не совпало'

    @allure.title("Получение информации о питомце по ID")
    def test_get_pet_by_id(self, create_pet):
        with allure.step('Получение ID созданного питомца'):
            pet_id = create_pet["id"]

        with allure.step('Отправка запроса'):
            response = requests.get(url=f'{base_url}/pet/{pet_id}')

        with allure.step('Проверка статуса'):
            assert response.status_code == 200, "Статус код не совпал"
            assert response.json()["id"] == pet_id, "Айди совпал"

    @allure.title("Обновление информации о питомце")
    def test_update_pet(self,create_pet):

        with allure.step('Получение ID созданного питомца'):
            pet_id = create_pet["id"]

        with allure.step('Подготовка данных'):
            payload = {"id": pet_id, "name": "Buddy", "status": "available"}

        with allure.step('Отправка запроса'):
            response = requests.put(url=f'{base_url}/pet', json=payload)
            response_json = response.json()

        with allure.step('Проверка статуса кода'):
            assert response.status_code == 200, "Код не совпал"

        with allure.step('Проверка ответа'):
            jsonschema.validate(response.json(), PET_SCHEMA)

        with allure.step('Проверка тела ответа'):
            assert response_json['id'] == payload['id'], 'Айди не совпало'
            assert response_json['name'] == payload['name'], 'Название не совпало'
            assert response_json['status'] == payload['status'], 'Cтатус не совпал'

    @allure.title("Удаление питомца по ID")
    def test_delete_pet(self,create_pet):
        with allure.step('Получение ID созданного питомца'):
            pet_id = create_pet["id"]

        with allure.step('Удаление питомца'):
            response_delete = requests.delete(url=f'{base_url}/pet/{pet_id}')

        with allure.step('Проверка статус кода и текста'):
            assert response_delete.status_code == 200, "Код не совпал"
            assert response_delete.text == "Pet deleted"

        with allure.step('Проверка что питомец удален'):
            response_get = requests.get(url=f'{base_url}/pet/{pet_id}')
            assert response_get.status_code == 404, "Код не совпал"


