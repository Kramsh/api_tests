import pytest
from endpoints.auth import Authorization
from endpoints.check_token import AuthorizeStatus
from endpoints.get_memes import GetAllMemes
from endpoints.create_meme import CreateMeme
from endpoints.get_meme_by_id import GetMeme
from endpoints.change_meme import ChangeMeme
from endpoints.delete_meme import DeleteMeme


@pytest.fixture
def base_url():
    return 'http://memesapi.course.qa-practice.com'


@pytest.fixture
def create_new_token(base_url):
    return Authorization(base_url)


@pytest.fixture
def token_status(base_url):
    return AuthorizeStatus(base_url)


@pytest.fixture
def get_all_memes(base_url):
    return GetAllMemes(base_url)


@pytest.fixture
def get_meme(base_url):
    return GetMeme(base_url)


@pytest.fixture
def create_new_meme(base_url):
    return CreateMeme(base_url)


@pytest.fixture
def change_meme(base_url):
    return ChangeMeme(base_url)


@pytest.fixture
def delete_meme(base_url):
    return DeleteMeme(base_url)


@pytest.fixture
def token_data(token_status, create_new_token):
    body = {
        "name": "Test user"
        }
    response = create_new_token.auth(body=body, headers=None)

    response_json = response.json()
    token_id = response_json["token"]

    return token_id, body


@pytest.fixture
def get_auth_header(create_new_token, token_data):
    token_id, _ = token_data
    auth_header = {
        "Content-Type": "application/json",
        "Authorization": f"{token_id}"
    }

    return auth_header


@pytest.fixture
def get_invalid_auth_header():
    token_id = 'Notvalidtoken'
    invalid_auth_header = {
        "Content-Type": "application/json",
        "Authorization": f"{token_id}"
    }

    return invalid_auth_header


@pytest.fixture
def meme_id(create_new_meme, delete_meme, get_auth_header):
    response = create_new_meme.create_meme(
        body={
            "text": "Test Stonks",
            "url": "https://i.ytimg.com/vi/BWKOVX-74Z0/maxresdefault.jpg",
            "tags": [
                "Funny", "Economy"
            ],
            "info": {
                "Author": "Test_User"
            }
        },
        headers=get_auth_header
    )
    response_json = response.json()
    meme_id = response_json["id"]

    yield meme_id

    cleanup_response = delete_meme.delete_meme_by_id(
        meme_id, headers=get_auth_header
    )
    if cleanup_response.status_code == 404:
        return
