# DRF with Template rendering

[Django Rest Framework](http://www.django-rest-framework.org/) is a powerfull and flexible toolkit for building Web API's.

This project contains two viewset, one for registration of users and other for login. Both these viewset can be used as web APIs and template based views(can be rendered on browser) using django rest html. All the API end-points uses JWT based authentications.

### Quick Setup
- Create a vitual environment.
  - `virtualenv -p python3.6 venv`
- Activate your virtual environment by
  - `source venv/bin/activate`
- Install required python libraries by using `pip`.
  - `pip install -r requirements.txt`
- Migrate database queries.
  - `python manage.py migrate`
- Finally, run your django runserver.
  - `python manage.py runserver`

##### Registeration
- end-point: `/accounts/register/`
- In API, paramters in json need to register:
    - `username`
    - `email`
    - `password`

##### Login
- end-point: `/accounts/login/`
- In API, paramters in json need to login:
    - `email`
    - `password`
