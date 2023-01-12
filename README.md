# Магазин игрушек

## Backend:
Python 3.10, Django, POSTGRES

Подробный перечень используемых библиотек находятся в файле requirements.txt

## Функционал
 Функционал

  - авторизация
  - список товаров
  - один товар
  - корзина
  - поиск и фильтр
  - оплата
      - заглушка
  - отзывы
  - оценка товара
  - чат поддержки
  - рассылка смс с акциями
  - управление товарами с интерфейса администратора

## Клонирование проекта

## Установка зависимостей
pip install -r requirements.txt

## Создайте файл .env в корневой директории и укажите ваши настройки.
    DEBUG=1
    DJANGO_SECRET_KEY=
    DJANGO_ALLOWED_HOSTS=*
    CORS_ALLOWED_HOSTS=http://127.0.0.1:8000 http://localhost:3000
    DB_ENGINE=django.db.backends.postgresql
    POSTGRES_DB=
    POSTGRES_USER=
    POSTGRES_PASSWORD=
    DB_HOST=


## Создайте контейнер
    docker-compose build

## Запустите контейнер.
    docker-compose up

## Создайте суперпользователя.
    docker-compose run webapp python manage.py createsuperuser
