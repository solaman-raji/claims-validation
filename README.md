# Claims Validation

**Claims Validation** Web APIs made with Django REST Framework

API documentation for the project is available at [docs](http://bit.ly/claims-validation).

### Requirements
- Python (3.6)
- Django (2.1)
- Django REST Framework (3.8)

### Installation - Virtual Environment

```
git clone git@github.com:solaman-raji/claims-validation.git
cd claims-validation

virtualenv -p python3 virtual-env/claims-validation-env
source virtual-env/claims-validation-env/bin/activate
```

Install dependencies
```
pip install -r requirements.txt
```

Run migrations

```
python manage.py migrate
```

Run the server

```
python manage.py runserver 0.0.0.0:8000
```

### Installation - Docker

```
git clone git@github.com:solaman-raji/claims-validation.git
cd claims-validation

docker-compose up
```

### Importing Sample Bills

```
python manage.py import_sample_bills
```

Using docker

```
docker-compose run web python manage.py import_sample_bills
```

### Settings

File location for exclusion rules

```
EXCLUSION_RULES_FILENAME = 'exclusion_rules.txt'
EXCLUSION_RULES_FILE_PATH = f'{BASE_DIR}/{EXCLUSION_RULES_FILENAME}'
```

File location for sample bill

```
SAMPLE_BILLS_FILENAME = 'sample_bills.txt'
SAMPLE_BILLS_FILE_PATH = f'{BASE_DIR}/{SAMPLE_BILLS_FILENAME}'
```

## Built With

* [Python 3.6](https://docs.python.org/3.6/) - Python version 3.6
* [Django](https://www.djangoproject.com/) - The web framework used
* [Django REST Framework](http://www.django-rest-framework.org/) - Used to generate RESTful API
