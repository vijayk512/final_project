# Final Project

Web Programming with Python and JavaScript

IT is a Survey APP and it's mobile responsive.

Application using.
HTML, CSS, Bootstrap4, jquery, for database I am using Heroku PostgreSQL, forms.py for creating a form and JSON

For admin theme I am using sb-admin-2 css and js

Form.py containing a reigster and login form.

view.py having all the business logic.

models.py created all models also added in admin as well.

all views are login secured.

please create a super user to acces the admin in django.

command to install pip3 install -r requirements.txt

Django==3.0.6

djangorestframework~=3.11.0


Please update settings.py for email settings and database connections.

Functionality:
When you access surveys-admin application, you see login page, login as super user will take you to home page.
Home page is dashboard having basic info about active survey and users and admin users count.
admin_users page able to edit, delete, create admin_users
survey page able to edit, delete, create survey pages and able to add question to relevant surveys.
user page is a page for people who give survey.

When access to survey, its take you to either home page or login page if not logged in.
you are able to register your self or logged in if already have an account.
once you logged in able to submit to take the any survey any number of time.
