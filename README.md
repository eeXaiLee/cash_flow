# Cash Flow

Веб-сервис для управления движением денежных средств (ДДС). Позволяет создавать, редактировать, удалять и просматривать записи о денежных операциях, а также управлять справочниками статусов, типов операций, категорий и подкатегорий.

## Возможности

* создание, просмотр, изменение и удаление записей ДДС;
* управление справочниками:

  * статусы;
  * типы операций;
  * категории;
  * подкатегории;
* фильтрация операций:

  * по диапазону дат;
  * по статусу;
  * по типу операции;
  * по категории;
  * по подкатегории;
* проверка бизнес-правил:

  * категория должна относиться к выбранному типу операции;
  * подкатегория должна относиться к выбранной категории;
* автоматическое заполнение даты операции с возможностью её ручного изменения;
* API для получения категорий по типу операции и подкатегорий по категории.

## Технологии

* Python 3.12+
* Django 5
* Django REST Framework
* django-filter
* SQLite
* python-dotenv
* mypy
* flake8
* isort
* pytest
* Docker
* Docker Compose

## Структура проекта

```text
cash_flow/
├── config/
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   ├── constants.py
│   └── __init__.py
├── fixtures/
│   ├── 01_references.json
│   └── 02_transactions.json
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_api.py
│   └── test_models.py
├── references/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── admin.py
│   └── migrations/
├── transactions/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── filters.py
│   ├── admin.py
│   └── migrations/
├── .dockerignore
├── docker-compose.yml
├── Dockerfile
├── manage.py
├── requirements.txt
├── pyproject.toml
├── README.md
└── .env
```

## Установка и запуск

### 1. Клонировать репозиторий

```bash
git clone git@github.com:eeXaiLee/cash_flow.git
cd cash_flow
```

### 2. Создать и активировать виртуальное окружение

Для Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

Для Windows:

```bash
python -m venv venv
source venv/Scripts/activate
```

### 3. Установить зависимости

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Создать файл `.env`

Пример содержимого:

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

### 5. Применить миграции

```bash
python manage.py migrate
```

### 6. Создать суперпользователя

```bash
python manage.py createsuperuser
```

### 7. Запустить сервер разработки

```bash
python manage.py runserver
```

После запуска приложение будет доступно по адресу:

```text
http://127.0.0.1:8000/
```

Административная панель:

```text
http://127.0.0.1:8000/admin/
```

API:

```text
http://127.0.0.1:8000/api/
```

## Запуск через Docker (альтернативный способ)

Если у вас установлены Docker и Docker Compose, можно запустить приложение в контейнере без ручной настройки окружения.

```bash
docker compose build
docker compose up
```

### Основные команды внутри контейнера

| Действие | Команда |
|----------|---------|
| Применить миграции | `docker compose exec web python manage.py migrate` |
| Создать суперпользователя | `docker compose exec web python manage.py createsuperuser` |
| Загрузить справочники | `docker compose exec web python manage.py loaddata fixtures/01_references.json` |
| Загрузить операции | `docker compose exec web python manage.py loaddata fixtures/02_transactions.json` |
| Запустить тесты | `docker compose exec web pytest` |
| Остановить контейнеры | `docker compose down` |

## Загрузка тестовых данных (фикстуры)

В проекте предусмотрены фикстуры для быстрого заполнения базы данных.

Фикстуры содержат тестовые данные для:

- статусов операций;
- типов операций;
- категорий;
- подкатегорий;
- операций ДДС.

### Файлы фикстур

- `fixtures/01_references.json` — справочники
- `fixtures/02_transactions.json` — операции

### Загрузка фикстур

```bash
python manage.py loaddata fixtures/01_references.json
python manage.py loaddata fixtures/02_transactions.json
```

## Основные эндпоинты API

### Справочники

```text
GET, POST   /api/statuses/
GET, PATCH, PUT, DELETE /api/statuses/{id}/

GET, POST   /api/operation-types/
GET, PATCH, PUT, DELETE /api/operation-types/{id}/

GET, POST   /api/categories/
GET, PATCH, PUT, DELETE /api/categories/{id}/

GET, POST   /api/subcategories/
GET, PATCH, PUT, DELETE /api/subcategories/{id}/
```

### Операции ДДС

```text
GET, POST   /api/operations/
GET, PATCH, PUT, DELETE /api/operations/{id}/
```

### Фильтрация операций

Примеры запросов:

```text
/api/operations/?status=1
/api/operations/?operation_type=2
/api/operations/?category=1
/api/operations/?subcategory=3
/api/operations/?date_from=2026-01-01
/api/operations/?date_to=2026-12-31
/api/operations/?date_from=2026-01-01&date_to=2026-12-31
```

### Получение зависимых справочников

Категории по типу операции:

```text
/api/categories/?operation_type=2
```

Подкатегории по категории:

```text
/api/subcategories/?category=1
```

## API документация (Swagger)

Проект включает автоматически сгенерированную документацию API:

- Swagger UI: `/api/docs/`
- ReDoc: `/api/redoc/`
- OpenAPI schema: `/api/schema/`

Документация формируется автоматически на основе DRF ViewSet и сериализаторов.

## Бизнес-правила

* Нельзя выбрать категорию, которая не относится к указанному типу операции.
* Нельзя выбрать подкатегорию, которая не относится к указанной категории.
* Поля `amount`, `operation_type`, `category` и `subcategory` являются обязательными.
* Сумма операции должна быть больше нуля.
* Дата операции по умолчанию устанавливается автоматически и может быть изменена вручную.

## Проверка качества кода

Запуск flake8:

```bash
flake8 .
```

Проверка сортировки импортов:

```bash
isort .
```

Проверка типов:

```bash
mypy .
```

## Тестирование

Проект содержит базовые тесты на `pytest` и `pytest-django`, покрывающие наиболее важную функциональность:

- создание и валидацию моделей;
- получение данных через API;
- создание операций;
- проверку бизнес-правил;
- фильтрацию операций.

Запуск всех тестов:

```bash
pytest
```

Подробный вывод:

```bash
pytest -v
```

## Ссылки проекта

- Автор: **[Евгений Димитриев](https://github.com/eeXaiLee)**
- Репозиторий: **https://github.com/eeXaiLee/cash_flow**
- API: `/api/`
- Swagger: `/api/docs/`
- ReDoc: `/api/redoc/`
- Административная панель: `/admin/`
