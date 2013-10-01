djangoCMS Tutorial - Step 1
===========================
Hey, you made it! Awesome. Now let's get started by setting up our environment.

Preparing the environment
-------------------------

```
# Install dependencies
$ pip install --upgrade virtualenv
$ pip install --upgrade django
$ pip install -e git+https://github.com/nephila/aldryn-installer#egg=aldryn-installer
```
Installing the CMS
------------------
```
$ cd ~/workspace
$ mkdir demo
$ cd demo
$ virtualenv env --no-site-packages
$ source env/bin/activate
$ aldryn -p . my_demo
$ python manage.py runserver
```

### Where to go from here

Congratulations, you now have a fully functional CMS! Awesome job! Let's continue by checking out branch [`step-2`](https://github.com/Chive/djangocms-tutorial/tree/step-2) (You should know how that works by now :)
