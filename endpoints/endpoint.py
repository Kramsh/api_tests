import allure


class Endpoint:
    def __init__(self, base_url):
        self.url = base_url
    response = None
    headers = {'Content-type': 'application/json'}

    @allure.step('Проверка кода ответа')
    def check_status_code_is_200(self):
        assert self.status_code == 200

    @allure.step('Проверка негативного кода ответа')
    def check_status_code_is_400(self):
        assert self.response.status_code == 400

    @allure.step('Проверка на отсутствие аутентификации')
    def check_status_code_is_401(self):
        assert self.response.status_code == 401

    @allure.step('Проверка на отсутствие прав')
    def check_status_code_is_403(self):
        assert self.response.status_code == 403

    @allure.step('Проверка на отсутствие аутентификации')
    def check_status_code_is_404(self):
        assert self.response.status_code == 404

    @property
    def status_code(self):
        if self.response:
            return self.response.status_code
        return None
