How to install the project

```bash
python3.12 -m venv env
source env/bin/activate
pip install poetry
poetry install
```

Then run the project
```bash
python manage.py runserver
```

inside .conf folder, create a .env file and set those environments

```env
SECRET_KEY=
DATABASE_HOST=
DATABASE_PASSWORD=
DATABASE_USER=
DATABASE_PORT=
DATABASE_NAME=
DATABASE_NAME_MULTI= #This is optional, you can use this if you want to set multiples databases
```

To configure multiples databases, you need to go into settings.py, uncomment this line of code, and set the DATABASE_NAME_MULTI for you new database name, you can create as much you want, just following the database configuration pattern

```python
f"{DATABASE_NAME_MULTI}": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": DATABASE_NAME_MULTI,
        "HOST": DATABASE_HOST,
        "PASSWORD": DATABASE_PASSWORD,
        "USER": DATABASE_USER,
        "PORT": DATABASE_PORT,
        #SCHEMA IS SET AS PUBLIC, YOU CAN CHANGE IT TO YOUR SCHEMA
        "OPTIONS": {"options": "-c search_path=public"},
    },
```