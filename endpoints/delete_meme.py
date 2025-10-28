import requests
import allure
from endpoints.endpoint import Endpoint


class DeleteMeme(Endpoint):

    @allure.step('Get memes list')
    def delete_meme_by_id(self, meme_id, headers=None):
        headers = headers if headers else self.headers
        self.response = requests.delete(
            f'{self.url}/meme/{meme_id}',
            headers=headers
        )
        try:
            self.json = self.response.json()
        except ValueError:
            self.json = None

        return self.response
