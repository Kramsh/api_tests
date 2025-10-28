import requests
import allure
from endpoints.endpoint import Endpoint


class ChangeMeme(Endpoint):

    @allure.step('Create new meme')
    def change_meme_data(self, meme_id, body, headers=None):
        headers = headers if headers else self.headers
        self.response = requests.put(
            f'{self.url}/meme/{meme_id}',
            json=body,
            headers=headers
        )
        try:
            self.json = self.response
        except ValueError:
            self.json = None

        return self.response
