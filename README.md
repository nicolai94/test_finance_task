Запуск проекта:
- создать .env файл из .env.template (шаблона)
- создать и запустить контейнер docker compose up --build
- открыть документацию http://localhost:8000/docs/ (документация swagger)


Запуск тестов:
 - зайти в контейнер docker compose exec task_backend
 - запустить тесты через poetry (poetry run pytest -vv)