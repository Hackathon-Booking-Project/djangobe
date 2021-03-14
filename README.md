# Django Backend for Booking Project

This is the Backendapplication for a short booking project.
It's based on Python Django and Django Restframework.

## Requirements & Setup
- Python 3.6 or higher.
- Postgres

Create a `.env` File and use your variables
```
cp ./app/.env.example ./app/.env
```

Migrate Database
```
python manage.py migrate
```

Create Superuser
```
python manage.py createsuperuser
```

Runserver
```
python manage.py runserver
```

Your application should run at http://localhost:8000