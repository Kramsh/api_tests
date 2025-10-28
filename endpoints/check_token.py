import requests
import allure
from endpoints.endpoint import Endpoint


class AuthorizeStatus(Endpoint):

    @allure.step('Check tokens is valid')
    def check_token(self, token_id):
        self.response = requests.get(
            f'{self.url}/authorize/{token_id}'
        )
        self.json = self.response
        return self.response
