# Проект yamdb_final

[![yamdb-workflows Actions Status](https://github.com/Syzhet/yamdb_final/workflows/yamdb-workflows/badge.svg)](https://github.com/Syzhet/yamdb_final/actions)

### Описание проекта

Проект YaMDb собирает отзывы пользователей на различные произведения. Более подробную информацию см. на странице с
описанием Redoc: http://127.0.0.1:8000/redoc/
(после запуска локального сервера).

Также проект YaMDb это совместный учебный проект, который позволяет на практике отработать более продвинутые методы
программирования api сервиса с использованием DRF, а также отработать опыт взаимодействия в команде и получить навыки
совместной работы в репозитории с использованием инструментария GIT.

### Об авторах проекта

Проект подготовлен студентами ШАД (Яндекс Практикума) Курса Python - разработчик:
Ионовым Алексеем, Смольяновым Серегеем, Герасимовым Александром.

### Применяемые технологии

Язык программирования Python; Фреймворк для разработки веб-приложений Django и встроенные модули для API DRF;
Инструментарий Git

### Как развернуть проект на локальной машине:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:AlexGer86/api_yamdb.git
```

```
cd api_yamdb
```

Создать и активировать виртуальное окружение:

```
python -m venv venv
```

```
source venv/Scripts/activate
```

```
python -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```

Перейти на страницу с описанием Redoc:

```
http://127.0.0.1:8000/redoc/
```

### Некоторые примеры запросов к API:

Регистрация нового пользователя: получить код подтверждения на переданный email. При отправке POST-запроса Поля email и
username должны быть уникальными.

```
http://127.0.0.1:8000/api/v1/auth/signup/
```

Получение JWT-токена в обмен на username и confirmation code (POST-запрос):

```
http://127.0.0.1:8000/api/v1/auth/token/
```

Получить список всех категорий (GET - запрос):

```
http://127.0.0.1:8000/api/v1/categories/
```

Создать категорию (POST-запрос):

```
http://127.0.0.1:8000/api/v1/categories/
```

Удаление категории (DELETE):

```
http://127.0.0.1:8000/api/v1/categories/{slug}/
```

Получить список всех жанров (GET - запрос):

```
http://127.0.0.1:8000/api/v1/genres/
```

Добавление жанра (POST-запрос):

```
http://127.0.0.1:8000/api/v1/genres/
```

Удаление жанра (DELETE):

```
http://127.0.0.1:8000/api/v1/genres/{slug}/
```

Получение списка всех произведений (GET - запрос):

```
http://127.0.0.1:8000/api/v1/titles/
```

Добавление произведения (POST - запрос):

```
http://127.0.0.1:8000/api/v1/titles/
```

Получение информации о произведении (GET - запрос):

```
http://127.0.0.1:8000/api/v1/titles/{titles_id}/
```

Частичное обновление информации о произведении (PATCH - запрос):

```
http://127.0.0.1:8000/api/v1/titles/{titles_id}/
```

Удаление произведения (DELETE):

```
http://127.0.0.1:8000/api/v1/titles/{titles_id}/
```

Получение списка всех отзывов (GET - запрос):

```
http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/
```

Добавление нового отзыва (POST - запрос):

```
http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/
```

Полуение отзыва по id (GET - запрос)

```
http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/
```

Частичное обновление отзыва по id (PATCH - запрос):

```
http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/
```
Удаление отзыва по id (DELETE):

```
http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/
```

### Шаблон наполнения env файла:

DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=login
POSTGRES_PASSWORD=password
DB_HOST=db
DB_PORT=5432
EMAIL_HOST_USER=your_adress@your_domen.com
MAIL_HOST_PASSWORD=email_password

### Описание команд для запуска приложения в контейнерах:

Запускаем контейнеры при помощи docker-compose:
'''
sudo docker-compose up -d --build
'''

Выполняем миграции в запущенном контейнере web:
'''
sudo docker-compose exec web python manage.py migrate
'''

Создаем суперпользователя для управления проектом через админку:
'''
sudo docker-compose exec web python manage.py createsuperuser
'''

Собираем статику в папку static/:
'''
sudo docker-compose exec web python manage.py collectstatic --no-input
'''