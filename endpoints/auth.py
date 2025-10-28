import requests
import allure
from endpoints.endpoint import Endpoint


class Authorization(Endpoint):

    @allure.step('Create new token')
    def auth(self, body, headers):
        headers = headers if headers else self.headers
        self.response = requests.post(
            f'{self.url}/authorize',
            json=body,
            headers=headers
        )

        try:
            self.json = self.response.json()
        except ValueError:
            self.json = None
            allure.attach(
                self.response.text,
                "Raw HTML response",
                allure.attachment_type.TEXT
            )

        return self.response
