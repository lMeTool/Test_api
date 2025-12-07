# Q&A API with Django REST Framework

Этот проект — Q&A API на Django REST Framework, контейнеризованный с Docker и Docker Compose.

## Модели
- **Question**: text, created_at
- **Answer**: text, created_at, user_id, question (ForeignKey)

## Запуск
1. Установите Docker и Docker Compose (если не установлены).
2. В корне проекта выполните:
docker-compose up --build

- Это соберёт образы, запустит PostgreSQL (БД: bd_posgre, пользователь: postgres, пароль: 12345) и Django-сервер.
- API будет доступно на http://localhost:8000.
3. Для остановки: `docker-compose down`.
4. Для пересборки после изменений: `docker-compose up --build`.

## Миграции и данные
- Миграции применяются автоматически при запуске.
- Если нужно загрузить данные из QandA.json (фикстура), добавьте в docker-compose.yml в command:
command: >
sh -c "python manage.py migrate && python manage.py loaddata QandA.json && python manage.py runserver 0.0.0.0:8000"

(Убедитесь, что файл QandA.json в корне и кодировка UTF-8.)

## API Эндпоинты
- GET/POST /questions/ — список вопросов.
- GET/POST /answers/ — список ответов.
- Подробности в QandA_api/urls.py (приложения core).

## Производство
- Для production добавьте Gunicorn: установите в requirements.txt, измените CMD в Dockerfile на `gunicorn QandA_api.wsgi:application --bind 0.0.0.0:8000`.
- Установите DEBUG=0 и настройте ALLOWED_HOSTS.

## Решение проблем
- Если ошибка с БД: проверьте логи `docker-compose logs db`.
- Для доступа к БД: используйте pgAdmin, подключившись к localhost:5432 с credentials (postgres/12345).