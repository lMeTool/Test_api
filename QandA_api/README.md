# Q&A API

Это простой API для системы вопросов и ответов (Q&A), разработанный с использованием Django REST Framework. Проект позволяет создавать вопросы, добавлять ответы, просматривать и удалять их. API обернут в Docker для удобного развертывания.

## Функциональность
- **Вопросы (Questions)**: Текстовое поле, дата создания.
- **Ответы (Answers)**: Текстовое поле, дата создания, ID пользователя (UUID), связь с вопросом.
- **Эндпоинты**:
  - `GET /api/questions/` — Получить список вопросов с ответами.
  - `POST /api/questions/` — Создать новый вопрос (требуется поле `text`).
  - `GET /api/questions/<id>/` — Получить конкретный вопрос.
  - `DELETE /api/questions/<id>/` — Удалить вопрос (автоматически удаляются связанные ответы).
  - `POST /api/questions/<question_id>/answers/` — Добавить ответ к вопросу (требуется поле `text`, `user_id` опционально, по умолчанию генерируется UUID).
  - `GET /api/answers/<id>/` — Получить конкретный ответ.
  - `DELETE /api/answers/<id>/` — Удалить ответ.
- **База данных**: PostgreSQL (миграция с SQLite).
- **Контейнеризация**: Docker и Docker Compose для лёгкого запуска.

## Требования
- Docker и Docker Compose (установи их, если не установлены).
- Python 3.11 (для локального запуска без Docker).

## Установка и запуск
1. Клонируй репозиторий или скачай файлы проекта.
2. Убедись, что у тебя есть `docker-compose.yml`, `Dockerfile` и `requirements.txt`.
3. Запусти проект:
docker-compose up --build

- Это соберёт образы, запустит PostgreSQL и Django-сервер.
- Сервер будет доступен по адресу: `http://localhost:8000`.
4. Примени миграции (если не применились автоматически):
docker-compose exec web python manage.py migrate


## Тестирование API
Используй Postman, curl или любой REST-клиент для тестирования эндпоинтов. Примеры:

- **Создать вопрос**:
POST http://localhost:8000/api/questions/
Content-Type: application/json
{
"text": "Как установить Docker?"
}


- **Получить все вопросы**:
GET http://localhost:8000/api/questions/


- **Добавить ответ**:
POST http://localhost:8000/api/questions/1/answers/
Content-Type: application/json
{
"text": "Установи Docker Desktop с официального сайта.",
"user_id": "123e4567-e89b-12d3-a456-426614174000" // Опционально
}


- **Удалить вопрос**:
DELETE http://localhost:8000/api/questions/1/


Если возникают ошибки (например, с кодировкой или БД), проверь логи: `docker-compose logs`.

## Структура проекта
- `QandA/` — Основные настройки Django (settings.py, urls.py).
- `core/` — Приложение с моделями, сериализаторами, views и urls.
- `requirements.txt` — Зависимости (Django 6.0, DRF, psycopg2-binary).
- `Dockerfile` — Сборка образа для Django.
- `docker-compose.yml` — Конфигурация сервисов (web и db).

## Дальнейшие улучшения
- Добавь аутентификацию (например, JWT с DRF Simple JWT).
- Создай фронтенд (React/Vue) для взаимодействия с API.
- Добавь пагинацию, фильтры или поиск по вопросам.
- Настрой тесты (pytest или Django TestCase).

## Лицензия
Этот проект — открытый. Используй на своё усмотрение.

Если возникнут вопросы или нужны доработки, пиши!