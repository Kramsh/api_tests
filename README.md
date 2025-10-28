Api тесты сервиса http://memesapi.course.qa-practice.com/
Для запуска тестов необходимо в директории final_project прописать pytest -vs
Для генерации репорта необходимо в директории final_project прописать:
pytest --alluredir=allure-results
allure serve allure-results