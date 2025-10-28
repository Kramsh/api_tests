import requests
import allure
from endpoints.endpoint import Endpoint


class GetAllMemes(Endpoint):

    @allure.step('Get memes list')
    def get_memes_list(self, headers=None):
        headers = headers if headers else self.headers
        self.response = requests.get(
            f'{self.url}/meme',
            headers=headers
        )
        try:
            self.json = self.response.json()
        except ValueError:
            self.json = None

        return self.response
