# django-crud
### Windows installation
To install the dependencies use the following commands in the cmd or PowerShell
```
# create a virtual environment, activate it, install all the packages
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

Then, create a database, a superuser and run the server
```
python django\mysite\manage.py migrate
python django\mysite\manage.py createsuperuser
python django\mysite\manage.py runserver
```
