djangoCMS Tutorial - Step 1
===========================
Hey, you made it! Awesome. Now let's get started by setting up django.

django
------
```
# Install dependencies
$ sudo pip install --upgrade virtualenv
$ sudo pip install --upgrade django

# Start django project
$ cd ~/workspace
$ django-admin.py startproject demo

# make virtualenv for project + install project dependencies
$ cd demo
$ virtualenv --no-site-packages env
$ source env/bin/activate
$ sudo pip install --upgrade django

# try & check if it worked at localhost:8000
$ python manage.py runserver
```

djangoCMS
---------
```
# install latest egg from github
$ pip install git+git://github.com/divio/django-cms.git#egg=django-cms
```
### Edit settings
follow <http://docs.django-cms.org/en/develop/getting_started/tutorial.html>

Awesome job! Let's continue by checking out branch 'step-2' (You should know how that works by now :)
