

# Продуктовый помощник

![Status](https://github.com/SowaSova/foodgram-project-react/actions/workflows/main.yml/badge.svg)

Этот онлайн-сервис поможет Вам:

- хранить свои рецепты
- искать чужие рецепты
- делиться и подписываться
- выводить ингредиенты в отдельный текстовый файл

## Как воспользоваться?

По этой -> [ссылке](...) (обновлена 29.03.2023)

Данные пользователя:

* Почта: 
```
num@lo.ck
```
* Пароль: 
```
useruser
```
Данные админа:

* Логин: 
```
admin
```
* Пароль: 
```
adminadmin
```
## Технологии

- Python 3.7
- Django 2.2.19
- Django REST framework 3.13
- PostgreSQL 13.0
- NGINX 1.19
- Gunicorn 20.1
- GitHub Actions


## Установки

Клонировать проект
```sh
git clone git@github.com:SowaSova/foodgram-project-react.git
```

Создать в папке infra .env файл
```sh
cd foodgram-project-react/infra
nano .env
```

Заполните его информацией
```sh
DB_ENGINE='django.db.backends.postgresql'
DB_NAME='postgres'
POSTGRES_USER='postgres'
POSTGRES_PASSWORD='postgres'
DB_HOST='127.0.0.1'
DB_PORT='5432'
```

Инициируйте создание образов и контейнеров
```sh
sudo docker-compose up -d --build
```

Финальные шаги
```sh
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser
docker-compose exec backend python manage.py collectstatic --no-input
docker-composer exec backend python manage.py load_ingredients
```

