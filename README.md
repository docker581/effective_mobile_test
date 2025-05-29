# effective_mobile_test

## Описание
Платформа для обмена вещами (бартерная система)

## Стек технологий
- Python 3.11.5
- Django 5.2.1
- Django Rest Framework (DRF) 3.16.0
- SQLite 3.42.0


## Установка docker
https://docs.docker.com/engine/install/

## Команды
### Клонирование репозитория
```bash
git clone https://github.com/docker581/effective_mobile_test
```

### Запуск приложения
```bash
python manage.py runserver
```

### Применение миграций
```bash
python manage.py makemigrations
python manage.py migrate
```

### Загрузка тестовых данных
```bash
python manage.py load_test_data
```

### Выполнение тестов
```bash
python manage.py test ads.web.tests
```

## Документация по API
```bash
http://127.0.0.1/swagger - Swagger
```
```bash
http://127.0.0.1/redoc - Redoc
```

## Автор
Докторов Денис
