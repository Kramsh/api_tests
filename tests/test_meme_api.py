import allure
import pytest


TEST_USERS = [
    {"name": "Test user 1"},
    {"name": "Test user 2"},
    {"name": "Test user 3"}
]


@allure.feature("Авторизация")
@allure.story("Успешная авторизация")
@pytest.mark.parametrize('data', TEST_USERS)
def test_successful_auth(data, create_new_token):
    create_new_token.auth(
        body=data, headers=None
    )
    create_new_token.check_status_code_is_200()


@allure.feature("Авторизация")
@allure.story("Авторизация без тела запроса")
@pytest.mark.parametrize('data', [TEST_USERS[0]])
def test_auth_w_o_body(data, create_new_token):
    create_new_token.auth(
        body=None, headers=None
    )
    create_new_token.check_status_code_is_400()


@allure.feature("Статус токена")
@allure.story("Получение статуса живого токена")
def test_token_status_by_valid_id(token_status, token_data):
    token_id, body = token_data
    response = token_status.check_token(token_id)
    token_status.check_status_code_is_200()
    assert f'Token is alive. Username is {body["name"]}' in response.text


NOT_VALID_TOKEN = 'Notvalidtoken'


@allure.feature("Статус токена")
@allure.story("Получение статуса невалидного токена")
def test_token_status_by_not_valid_id(token_status):
    token_id = NOT_VALID_TOKEN
    token_status.check_token(token_id)
    token_status.check_status_code_is_404()


@allure.feature("Получение списка всех мемов")
@allure.story("Получение списка всех мемов с валидным токеном авторизации")
def test_get_all_memes(get_all_memes, get_auth_header):
    get_all_memes.get_memes_list(headers=get_auth_header)
    get_all_memes.check_status_code_is_200()


@allure.feature("Получение списка всех мемов")
@allure.story("Получение списка всех мемов с невалидным токеном авторизации")
def test_get_all_memes_wo_auth(get_all_memes, get_invalid_auth_header):
    get_all_memes.get_memes_list(headers=get_invalid_auth_header)
    get_all_memes.check_status_code_is_401()


TEST_BODY = {
    "text": "Test Stonks",
    "url": "https://i.ytimg.com/vi/BWKOVX-74Z0/maxresdefault.jpg",
    "tags": [
        "Funny", "Economy"
    ],
    "info": {
        "Author": "Test_User"
    }
}


@allure.feature("Создание мема")
@allure.story("Успешное создание мема с валидным токеном авторизации")
def test_successful_create_meme(create_new_meme, get_auth_header):
    create_new_meme.create_meme(
        body=TEST_BODY, headers=get_auth_header
    )
    create_new_meme.check_status_code_is_200()


@allure.feature("Создание мема")
@allure.story("Попытка создания мема с невалидным токеном авторизации")
def test_create_meme_wo_auth(create_new_meme, get_invalid_auth_header):
    create_new_meme.create_meme(
        body=TEST_BODY, headers=get_invalid_auth_header
    )
    create_new_meme.check_status_code_is_401()


@allure.feature("Создание мема")
@allure.story("Проверка обязательности поля text")
def test_create_meme_wo_text(create_new_meme, get_auth_header):
    body_wo_id = {
        "url": "https://i.ytimg.com/vi/BWKOVX-74Z0/maxresdefault.jpg",
        "tags": [
            "Funny", "Economy"
        ],
        "info": {
            "Author": "Test_User"
        }
    }
    create_new_meme.create_meme(
        body=body_wo_id, headers=get_auth_header
    )
    create_new_meme.check_status_code_is_400()


@allure.feature("Создание мема")
@allure.story("Проверка обязательности поля url")
def test_create_meme_wo_url(create_new_meme, get_auth_header):
    body_wo_url = {
        "text": "Test Stonks",
        "tags": [
            "Funny", "Economy"
        ],
        "info": {
            "Author": "Test_User"
        }
    }
    create_new_meme.create_meme(
        body=body_wo_url, headers=get_auth_header
    )
    create_new_meme.check_status_code_is_400()


@allure.feature("Создание мема")
@allure.story("Проверка обязательности поля tags")
def test_create_meme_wo_tags(create_new_meme, get_auth_header):
    body_wo_tags = {
        "text": "Test Stonks",
        "url": "https://i.ytimg.com/vi/BWKOVX-74Z0/maxresdefault.jpg",
        "info": {
            "Author": "Test_User"
        }
    }
    create_new_meme.create_meme(
        body=body_wo_tags, headers=get_auth_header
    )
    create_new_meme.check_status_code_is_400()


@allure.feature("Создание мема")
@allure.story("Проверка обязательности поля info")
def test_create_meme_wo_info(create_new_meme, get_auth_header):
    body_wo_info = {
        "text": "Test Stonks",
        "url": "https://i.ytimg.com/vi/BWKOVX-74Z0/maxresdefault.jpg",
        "tags": [
            "Funny", "Economy"
        ]
    }
    create_new_meme.create_meme(
        body=body_wo_info, headers=get_auth_header
    )
    create_new_meme.check_status_code_is_400()


@allure.feature("Получение мема")
@allure.story("""Получение мема с 
"валидным токеном авторизации и валидным id""")
def test_get_meme_by_id_valid_data(
    get_meme, meme_id, get_auth_header
):
    get_meme.get_meme_by_id(meme_id=meme_id, headers=get_auth_header)
    get_meme.check_status_code_is_200()


@allure.feature("Получение мема")
@allure.story("Попытка получения мема без авторизации")
def test_get_meme_by_id_wo_auth(
    get_meme, meme_id, get_invalid_auth_header
):
    get_meme.get_meme_by_id(meme_id=meme_id, headers=get_invalid_auth_header)
    get_meme.check_status_code_is_401()


@allure.feature("Получение мема")
@allure.story("Попытка получения мема по невалидному id")
def test_get_meme_by_invalid_id(
    get_meme, get_auth_header
):
    get_meme.get_meme_by_id(meme_id='invalid_id', headers=get_auth_header)
    get_meme.check_status_code_is_404()


@allure.feature("Редактирование мема")
@allure.story("Успешное редактирование мема с валидным токеном авторизации")
def test_successful_change_meme(change_meme, meme_id, get_auth_header):
    TEST_BODY_FOR_CHANGE = {
        "id": meme_id,
        "text": "Test Stonks Changed",
        "url": "https://i.ytimg.com/vi/BWKOVX-74Z0/maxresdefault.jpg",
        "tags": [
            "Funny", "Economy"
        ],
        "info": {
            "Author": "Test_User"
        }
    }
    change_meme.change_meme_data(
        meme_id=meme_id, body=TEST_BODY_FOR_CHANGE, headers=get_auth_header
    )
    change_meme.check_status_code_is_200()


@allure.feature("Редактирование мема")
@allure.story("Редактирование мема с невалидным токеном авторизации")
def test_change_meme_wo_auth(change_meme, meme_id, get_invalid_auth_header):
    TEST_BODY_FOR_CHANGE = {
        "id": meme_id,
        "text": "Test Stonks Changed",
        "url": "https://i.ytimg.com/vi/BWKOVX-74Z0/maxresdefault.jpg",
        "tags": [
            "Funny", "Economy"
        ],
        "info": {
            "Author": "Test_User"
        }
    }
    change_meme.change_meme_data(
        meme_id=meme_id,
        body=TEST_BODY_FOR_CHANGE,
        headers=get_invalid_auth_header
    )
    change_meme.check_status_code_is_401()


@allure.feature("Редактирование мема")
@allure.story("Редактирование мема с невалидным id")
def test_change_meme_by_invalid_id(change_meme, get_auth_header):
    TEST_BODY_FOR_CHANGE = {
        "id": "invalid_id",
        "text": "Test Stonks Changed",
        "url": "https://i.ytimg.com/vi/BWKOVX-74Z0/maxresdefault.jpg",
        "tags": [
            "Funny", "Economy"
        ],
        "info": {
            "Author": "Test_User"
        }
    }
    change_meme.change_meme_data(
        meme_id='invalid_id',
        body=TEST_BODY_FOR_CHANGE,
        headers=get_auth_header
    )
    change_meme.check_status_code_is_404()


@allure.feature("Редактирование мема")
@allure.story("Проверка обязательности поля id")
def test_change_meme_wo_id(change_meme, get_auth_header):
    TEST_BODY_FOR_CHANGE = {
        "text": "Test Stonks Changed",
        "url": "https://i.ytimg.com/vi/BWKOVX-74Z0/maxresdefault.jpg",
        "tags": [
            "Funny", "Economy"
        ],
        "info": {
            "Author": "Test_User"
        }
    }
    change_meme.change_meme_data(
        meme_id=None, body=TEST_BODY_FOR_CHANGE, headers=get_auth_header
    )
    change_meme.check_status_code_is_404()


@allure.feature("Редактирование мема")
@allure.story("Проверка обязательности поля text")
def test_change_meme_wo_text(change_meme, meme_id, get_auth_header):
    TEST_BODY_FOR_CHANGE = {
        "id": meme_id,
        "url": "https://i.ytimg.com/vi/BWKOVX-74Z0/maxresdefault.jpg",
        "tags": [
            "Funny", "Economy"
        ],
        "info": {
            "Author": "Test_User"
        }
    }
    change_meme.change_meme_data(
        meme_id=meme_id, body=TEST_BODY_FOR_CHANGE, headers=get_auth_header
    )
    change_meme.check_status_code_is_400()


@allure.feature("Редактирование мема")
@allure.story("Проверка обязательности поля url")
def test_change_meme_wo_url(change_meme, meme_id, get_auth_header):
    TEST_BODY_FOR_CHANGE = {
        "id": meme_id,
        "text": "Test Stonks Changed",
        "tags": [
            "Funny", "Economy"
        ],
        "info": {
            "Author": "Test_User"
        }
    }
    change_meme.change_meme_data(
        meme_id=meme_id, body=TEST_BODY_FOR_CHANGE, headers=get_auth_header
    )
    change_meme.check_status_code_is_400()


@allure.feature("Редактирование мема")
@allure.story("Проверка обязательности поля tags")
def test_change_meme_wo_tags(change_meme, meme_id, get_auth_header):
    TEST_BODY_FOR_CHANGE = {
        "id": meme_id,
        "text": "Test Stonks Changed",
        "url": "https://i.ytimg.com/vi/BWKOVX-74Z0/maxresdefault.jpg",
        "info": {
            "Author": "Test_User"
        }
    }
    change_meme.change_meme_data(
        meme_id=meme_id, body=TEST_BODY_FOR_CHANGE, headers=get_auth_header
    )
    change_meme.check_status_code_is_400()


@allure.feature("Редактирование мема")
@allure.story("Проверка обязательности поля info")
def test_change_meme_wo_info(change_meme, meme_id, get_auth_header):
    TEST_BODY_FOR_CHANGE = {
        "id": meme_id,
        "text": "Test Stonks Changed",
        "url": "https://i.ytimg.com/vi/BWKOVX-74Z0/maxresdefault.jpg",
        "tags": [
            "Funny", "Economy"
        ]
    }
    change_meme.change_meme_data(
        meme_id=meme_id, body=TEST_BODY_FOR_CHANGE, headers=get_auth_header
    )
    change_meme.check_status_code_is_400()


@allure.feature("Удаление мема")
@allure.story("Успешное удаление мема с валидным id")
def test_delete_meme_valid_data(
    delete_meme, meme_id, get_auth_header
):
    delete_meme.delete_meme_by_id(meme_id=meme_id, headers=get_auth_header)
    delete_meme.check_status_code_is_200()


@allure.feature("Удаление мема")
@allure.story("Попытка удаления мема с невалидным токеном авторизации")
def test_delete_meme_wo_auth(
    delete_meme, meme_id, get_invalid_auth_header
):
    delete_meme.delete_meme_by_id(
        meme_id=meme_id, headers=get_invalid_auth_header
        )
    delete_meme.check_status_code_is_401()


@allure.feature("Удаление мема")
@allure.story("Попытка удаления мема с невалидным id")
def test_delete_meme_by_invalid_id(
    delete_meme, meme_id, get_auth_header
):
    delete_meme.delete_meme_by_id(
        meme_id='invalid_id', headers=get_auth_header
        )
    delete_meme.check_status_code_is_404()
