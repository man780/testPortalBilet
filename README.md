# testPortalBilet

### Заходим в постгрес
```psql -U postgres -h localhost```
### Создаем базу в постгрес
```CREATE DATABASE aiohttp_demo;```
### Добавляем user в постгрес
```CREATE USER aiohttpdemo_user WITH PASSWORD 'aiohttpdemo_pass';```
### Дать юзеру привилегии
```GRANT ALL PRIVILEGES ON DATABASE aiohttp_demo TO aiohttpdemo_user;```

### Установляем requirements
Установляем и virtualenv, активируем и там же запускаем код:

```pip install -r requirements.txt```

## И наконец запускаем приложение
```python main.py```

## Проверяем
### В браузере 
http://0.0.0.0/

http://0.0.0.0/pages/

http://0.0.0.0/page/first-test-page/

### Или в консоли
http GET http://0.0.0.0/pages/

http GET http://0.0.0.0/page/first-test-page/