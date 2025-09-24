# School Management System Build with Django 
## Alx capstone project using Django Rest as Backend


# Features 

    `1. User Registration`
    The user is registerd via a custom user model that extends the Abstract user. Additional logic includes
    - required field for the first_name, last_name,email and password
    - users are also required to belong to an organization/institutions
    - user role as we will implement role based access




# Testing
    Testing is done with coverage
    `coverage run manage.py test && coverage report && coverage html`