import requests
import allure
from endpoints.endpoint import Endpoint


class CreateMeme(Endpoint):

    @allure.step('Create new meme')
    def create_meme(self, body, headers=None):
        headers = headers if headers else self.headers
        self.response = requests.post(
            f'{self.url}/meme',
            json=body,
            headers=headers
        )
        try:
            self.json = self.response
        except ValueError:
            self.json = None

        return self.response
