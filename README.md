# FastAPI Cargo Insurance

## Описание
* За основу взято [тестовое задание](https://docs.google.com/document/d/1ET0V9ZsLNsdwkaZQ-M3nC6Kkvx2KS75UUROg3kc68UA/edit).
* Используется FastAPI, Tortoise ORM, Docker, PostgreSQL, SQLite.


## Запуск приложения
### С помощью Docker:
1. Клонировать репозиторий
2. `make build`
3. `make up`
4. Запуск тестов осуществляется командой `make test_backend`
5. Проверить доступ на http://localhost:8000/

### С помощью виртуального окружения:
1. `python3.10 -m venv .venv`
2. `source .venv/bin/activate`
3. `pip install -r requirements.txt`
4. В `config/database` вместо `POSTGRESQL_URL` подставить `SQLITE_URL`
5. `make run`
6. Запуск тестов - `make test`
7. Проверить доступ на http://localhost:8000/

## API

* __GET__ `/docs`: документация 1
* __GET__ `/redoc`: документация 2
---
* __GET__ `/api/rates/`: Получить все Тарифы
* __POST__ `/api/rates/`: Импорт Тарифов
---
* __GET__ `/api/cargos/<cargo_id>/`: Получить Груз по ID
* __PATCH__ `/api/cargos/<cargo_id>/`: Изменить Объявленную стоимость у Груза
* __GET__ `/api/cargos/`: Получить все Грузы
* __POST__ `/api/cargo_insurance/`: Посчитать стоимость страхования для выбранного типа груза и даты
