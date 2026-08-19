# Последовательнсоть действия после скачивания

1. собрать образ `docker compose up --build -d`
2. посмотреть что контейнеры поднялись `docker compose ps`
3. Создадим суперпользователя `docker compose exec web python manage.py createsuperuser`
4. Можно зайти в админ-панель http://localhost:8000/admin/
5. Запустим тесты `docker compose exec web python manage.py test`

# Работа со Swagger

1. Пойдем по адресу `http://localhost:8000/api/docs`
2. Регистрируемся `POST /api/user/register/` с телом скажем `{"username": "user", "password": "password"}` и получаем
   токен
3. Получаем токен так же через `POST /api/user/login`
4. С данным токеном авторизуемся и можем создавать статьи и комментарии

# Просмотр данных в БД

Строка подключения к БД `DATABASE_URL: postgres://bloguser:blogpass@db:5432/blogdb`
Можно подключиться с помощью Бобра или DataGrip.

