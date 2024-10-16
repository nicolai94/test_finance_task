Запуск проекта:
- docker compose up --build
- http://localhost:8000/docs/ (документация swagger)


Запуск тестов:
 - зайти в контейнер docker compose exec task_backend
 - запустить тесты через poetry (poetry run pytest -vv)