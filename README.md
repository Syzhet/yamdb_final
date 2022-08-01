## Проект yamdb_final

![yamdb-workflows Actions Status](https://github.com/Syzhet/yamdb_final/blob/master/.github/workflows/yamdb_workflow.yml)

## Стек технологий 

<div>
  <a href="https://www.python.org/">
    <img src="https://github.com/devicons/devicon/blob/master/icons/python/python-original-wordmark.svg" title="Python" alt="Python" width="40" height="40"/>&nbsp;
  </a>
  <a href="https://www.djangoproject.com/">
    <img src="https://github.com/devicons/devicon/blob/master/icons/django/django-plain.svg" title="Django" alt="Django" width="40" height="40"/>&nbsp;
  </a>
  <a href="https://github.com/">
    <img src="https://github.com/devicons/devicon/blob/master/icons/github/github-original.svg" title="GitHub" alt="GitHub" width="40" height="40"/>&nbsp;
  </a>
</div>

## Описание проекта

Проект YaMDb собирает отзывы пользователей на различные произведения. Более подробную информацию см. на странице с
описанием Redoc: http://127.0.0.1:8000/redoc/
(после запуска локального сервера).

YaMDb это совместный проект трех авторов с использованием инструментария GIT.

## Об авторах проекта

Проект подготовлен следующими разработчиками:
- [Ионов А.В.](https://github.com/Syzhet)
- Смольяновым Серегеем
- Герасимовым Александром.

## Как развернуть проект на локальной машине:

Клонировать репозиторий и перейти в него в командной строке:
```sh
git clone git@github.com:Syzhet/yamdb_final.git
```

Перейти в директорию
```sh
cd api_yamdb
```

Создать и активировать виртуальное окружение:
```sh
python -m venv venv
```
```sh
source venv/Scripts/activate
```

Выполнить обновление pip:
```sh
python -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:
```sh
pip install -r requirements.txt
```

Выполнить миграции:
```sh
python manage.py migrate
```

Создать суперпользователя:
```sh
python manage.py createsuperuser
```

Запустить проект:
```sh
python manage.py runserver
```

Перейти на страницу с описанием Redoc:
```sh
http://127.0.0.1:8000/redoc/
```

## Некоторые примеры запросов к API:

Регистрация нового пользователя: получить код подтверждения на переданный email. При отправке POST-запроса Поля email и
username должны быть уникальными.
```sh
http://127.0.0.1:8000/api/v1/auth/signup/
```

Получение JWT-токена в обмен на username и confirmation code (POST-запрос):
```sh
http://127.0.0.1:8000/api/v1/auth/token/
```

Получить список всех категорий (GET - запрос):
```sh
http://127.0.0.1:8000/api/v1/categories/
```

Создать категорию (POST-запрос):
```sh
http://127.0.0.1:8000/api/v1/categories/
```

Удаление категории (DELETE):
```sh
http://127.0.0.1:8000/api/v1/categories/{slug}/
```

Получить список всех жанров (GET - запрос):
```sh
http://127.0.0.1:8000/api/v1/genres/
```

Добавление жанра (POST-запрос):
```sh
http://127.0.0.1:8000/api/v1/genres/
```

Удаление жанра (DELETE):
```sh
http://127.0.0.1:8000/api/v1/genres/{slug}/
```

Получение списка всех произведений (GET - запрос):
```sh
http://127.0.0.1:8000/api/v1/titles/
```

Добавление произведения (POST - запрос):
```sh
http://127.0.0.1:8000/api/v1/titles/
```

Получение информации о произведении (GET - запрос):
```sh
http://127.0.0.1:8000/api/v1/titles/{titles_id}/
```

Частичное обновление информации о произведении (PATCH - запрос):
```sh
http://127.0.0.1:8000/api/v1/titles/{titles_id}/
```

Удаление произведения (DELETE):
```sh
http://127.0.0.1:8000/api/v1/titles/{titles_id}/
```

Получение списка всех отзывов (GET - запрос):
```sh
http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/
```

Добавление нового отзыва (POST - запрос):
```sh
http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/
```

Полуение отзыва по id (GET - запрос)
```sh
http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/
```

Частичное обновление отзыва по id (PATCH - запрос):
```sh
http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/
```
Удаление отзыва по id (DELETE):
```sh
http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/
```

## Шаблон наполнения env файла:

DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=login
POSTGRES_PASSWORD=password
DB_HOST=db
DB_PORT=5432
EMAIL_HOST_USER=your_adress@your_domen.com
MAIL_HOST_PASSWORD=email_password

## Описание команд для запуска приложения в контейнерах:

Запускаем контейнеры при помощи docker-compose:
'''sh
sudo docker-compose up -d --build
'''

Выполняем миграции в запущенном контейнере web:
'''sh
sudo docker-compose exec web python manage.py migrate
'''

Создаем суперпользователя для управления проектом через админку:
'''sh
sudo docker-compose exec web python manage.py createsuperuser
'''

Собираем статику в папку static/:
'''sh
sudo docker-compose exec web python manage.py collectstatic --no-input
'''