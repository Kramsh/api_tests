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

    def _json_safe(self):
        if isinstance(getattr(self, "json", None), (dict, list)):
            return self.json
        try:
            return self.response.json()
        except Exception:
            return None

    @allure.step('Проверка: ответ не пустой')
    def check_response_not_empty(self):
        data = self._json_safe()
        assert data, "Ответ пустой"

    @allure.step('Проверка: объект содержит корректный id')
    def check_id_is_correct(self, expected_id):
        data = self._json_safe()
        assert isinstance(data, dict), f"Ожидался объект, получили: {type(data).__name__}"
        assert "id" in data, "В ответе отсутствует поле 'id'"
        assert data["id"] == expected_id, f"Ожидался id={expected_id}, получен id={data['id']}"

    @allure.step('Проверка: поля объекта совпадают с ожидаемыми')
    def check_fields_equal(self, expected: dict, fields: list | None = None):
        data = self._json_safe()
        assert isinstance(data, dict), f"Ожидался объект, получили: {type(data).__name__}"
        fields_to_check = fields or list(expected.keys())

        for key in fields_to_check:
            assert key in data, f"В ответе отсутствует поле '{key}'"
            assert data[key] == expected[key], f"Поле '{key}' некорректно. Ожидалось: {expected[key]!r}, получено: {data[key]!r}"

    @allure.step('Проверка: токен жив и соответствует пользователю')
    def check_token_is_alive(self, expected_username: str):

        assert self.response is not None, "Нет ответа для проверки токена"
        assert isinstance(self.response.text, str), "Ответ не текстовый"
        expected = f"Token is alive. Username is {expected_username}"
        assert expected in self.response.text, f"Ожидали сообщение: '{expected}', получили: '{self.response.text}'"
