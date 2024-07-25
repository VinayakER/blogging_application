# Blog API


## Installation

1. Clone the repository:

```bash
git clone https://github.com/VinayakER/blogging_application.git
cd blogging_application
```
Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
Install the dependencies:
```bash
pip install -r requirements.txt
```
Apply migrations:

```bash
python manage.py migrate
```
Create a superuser:
```bash
python manage.py createsuperuser
```
Run the development server:
```bash
python manage.py runserver
```

Swagger Documentation
The API documentation is available at:

Redoc UI: http://127.0.0.1:8000/redoc/


Running Tests
To run the tests, use the following command:

```bash
python manage.py test
```





