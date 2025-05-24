import allure
import requests

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
        with allure.step('Отправка запроса на изменение несуществующего питомца'):
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

