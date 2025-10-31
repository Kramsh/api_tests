import allure
import pytest


TEST_USERS = [
    {"name": "Test User"},
    {"name": "user_with_numbers_123"},
    {"name": "ИмяНаРусском"}
]


@allure.feature("Авторизация")
@allure.story("Успешная авторизация")
@pytest.mark.parametrize('data', TEST_USERS)
def test_successful_auth(data, create_new_token, token_status):
    response = create_new_token.auth(
        body=data, headers=None
    )
    create_new_token.check_status_code_is_200()
    response_json = response.json()
    token_id = response_json["token"]

    token_status.check_token(token_id)
    token_status.check_status_code_is_200()


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
    token_status.check_token(token_id)
    token_status.check_status_code_is_200()
    token_status.check_token_is_alive(body["name"])


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

    get_all_memes.check_response_not_empty()


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
def test_successful_create_meme(create_new_meme, get_auth_header, get_meme):
    response = create_new_meme.create_meme(
        body=TEST_BODY, headers=get_auth_header
    )
    create_new_meme.check_status_code_is_200()

    response_json = response.json()
    meme_id = response_json["id"]

    get_meme.get_meme_by_id(meme_id=meme_id, headers=get_auth_header)
    get_meme.check_status_code_is_200()

    get_meme.check_fields_equal(TEST_BODY, fields=["text", "url", "tags", "info"])


@allure.feature("Создание мема")
@allure.story("Попытка создания мема с невалидным токеном авторизации")
def test_create_meme_wo_auth(create_new_meme, get_invalid_auth_header):
    create_new_meme.create_meme(
        body=TEST_BODY, headers=get_invalid_auth_header
    )
    create_new_meme.check_status_code_is_401()


MISSING_REQUIRED_FIELDS = [
    (
        {
            "url": "https://i.ytimg.com/vi/BWKOVX-74Z0/maxresdefault.jpg",
            "tags": ["Funny", "Economy"],
            "info": {"Author": "Test_User"}
        },
        "text"
    ),
    (
        {
            "text": "Test Stonks",
            "tags": ["Funny", "Economy"],
            "info": {"Author": "Test_User"}
        },
        "url"
    ),
    (
        {
            "text": "Test Stonks",
            "url": "https://i.ytimg.com/vi/BWKOVX-74Z0/maxresdefault.jpg",
            "info": {"Author": "Test_User"}
        },
        "tags"
    ),
    (
        {
            "text": "Test Stonks",
            "url": "https://i.ytimg.com/vi/BWKOVX-74Z0/maxresdefault.jpg",
            "tags": ["Funny", "Economy"]
        },
        "info"
    )
]


@allure.feature("Создание мема")
@allure.story("Проверка обязательности обязательных поля")
@pytest.mark.parametrize("body, missing_field", MISSING_REQUIRED_FIELDS)
def test_create_meme_missing_required_fields(create_new_meme, get_auth_header, body, missing_field):
    create_new_meme.create_meme(
        body=body, headers=get_auth_header
    )
    create_new_meme.check_status_code_is_400()


@allure.feature("Получение мема")
@allure.story("""Получение мема с 
"валидным токеном авторизации и валидным id""")
def test_get_meme_by_id_valid_data(
    get_meme, meme_id, get_auth_header
):
    response = get_meme.get_meme_by_id(meme_id=meme_id, headers=get_auth_header)
    get_meme.check_status_code_is_200()

    get_meme.check_id_is_correct(meme_id)


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
def test_successful_change_meme(change_meme, meme_id, get_auth_header, get_meme):
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

    get_meme.get_meme_by_id(meme_id=meme_id, headers=get_auth_header)
    get_meme.check_status_code_is_200()

    get_meme.check_fields_equal(TEST_BODY_FOR_CHANGE, fields=["text", "url", "tags", "info"])


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


INVALID_ID_CASES = [
    ("invalid_id", {
        "id": "invalid_id",
        "text": "Test Stonks Changed",
        "url": "https://i.ytimg.com/vi/BWKOVX-74Z0/maxresdefault.jpg",
        "tags": ["Funny", "Economy"],
        "info": {"Author": "Test_User"}
    }),
    (None, {
        "text": "Test Stonks Changed",
        "url": "https://i.ytimg.com/vi/BWKOVX-74Z0/maxresdefault.jpg",
        "tags": ["Funny", "Economy"],
        "info": {"Author": "Test_User"}
    })
]


@allure.feature("Редактирование мема")
@allure.story("Редактирование мема с невалидным id и без id")
@pytest.mark.parametrize("meme_id, body", INVALID_ID_CASES)
def test_change_meme_invalid_id(change_meme, get_auth_header, meme_id, body):
    change_meme.change_meme_data(
        meme_id=meme_id,
        body=body,
        headers=get_auth_header
    )
    change_meme.check_status_code_is_404()


MISSING_FIELDS_FOR_UPDATE = [
    (
        "text",
        lambda meme_id: {
            "id": meme_id,
            "url": "https://i.ytimg.com/vi/BWKOVX-74Z0/maxresdefault.jpg",
            "tags": ["Funny", "Economy"],
            "info": {"Author": "Test_User"}
        }
    ),
    (
        "url",
        lambda meme_id: {
            "id": meme_id,
            "text": "Test Stonks Changed",
            "tags": ["Funny", "Economy"],
            "info": {"Author": "Test_User"}
        }
    ),
    (
        "tags",
        lambda meme_id: {
            "id": meme_id,
            "text": "Test Stonks Changed",
            "url": "https://i.ytimg.com/vi/BWKOVX-74Z0/maxresdefault.jpg",
            "info": {"Author": "Test_User"}
        }
    ),
    (
        "info",
        lambda meme_id: {
            "id": meme_id,
            "text": "Test Stonks Changed",
            "url": "https://i.ytimg.com/vi/BWKOVX-74Z0/maxresdefault.jpg",
            "tags": ["Funny", "Economy"]
        }
    )
]


@allure.feature("Редактирование мема")
@allure.story("Проверка обязательности обязательных полей при редактировании")
@pytest.mark.parametrize("missing_field, body_builder", MISSING_FIELDS_FOR_UPDATE)
def test_change_meme_missing_required_fields(change_meme, meme_id, get_auth_header, missing_field, body_builder):
    body = body_builder(meme_id)

    change_meme.change_meme_data(
        meme_id=meme_id,
        body=body,
        headers=get_auth_header
    )
    change_meme.check_status_code_is_400()


@allure.feature("Удаление мема")
@allure.story("Успешное удаление мема с валидным id")
def test_delete_meme_valid_data(
    delete_meme, meme_id, get_auth_header, get_meme
):
    delete_meme.delete_meme_by_id(meme_id=meme_id, headers=get_auth_header)
    delete_meme.check_status_code_is_200()

    get_meme.get_meme_by_id(meme_id=meme_id, headers=get_auth_header)
    get_meme.check_status_code_is_404()


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
