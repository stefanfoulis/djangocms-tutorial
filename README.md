djangoCMS Tutorial - Step 1
===========================
Hey, you made it! Awesome. Now let's get started by setting up our environment.

Preparing your workstation
--------------------------

```bash
$ pip install --upgrade virtualenv
```
Installing the CMS
------------------

### Make a project folder

```bash
$ cd ~/workspace	
$ mkdir demo && cd demo
```

### Setup virtual environment

```bash
$ virtualenv env --no-site-packages
$ source env/bin/activate
$ pip install -e git+https://github.com/nephila/aldryn-installer#egg=aldryn-installer
```

### install djangoCMS
follow the interactive setup, don't worry if takes a while :)

```bash
$ aldryn -p . my_demo
```

If you want to be safe, use the settings below:

```bash
§ Database configuration (in URL format) [default sqlite://locahost/project.db]: [ENTER]
§ django CMS version (choices: 2.4, stable, beta, develop) [default stable]: develop
§ Django version (choices: 1.4, 1.5, stable) [default stable]: 1.5
§ Activate Django I18N / L10N setting (choices: yes, no) [default yes]: [ENTER]
§ Install and configure reversion support (choices: yes, no) [default yes]: [ENTER]
§ Languages to enable. Option can be provided multiple times, or as a comma separated list: en,de
§ Optional default timezone [default America/Chicago]: Europe/Zurich
§ Activate Django timezone support (choices: yes, no) [default yes]: [ENTER]
§ Activate CMS permission management (choices: yes, no) [default yes]: [ENTER]

§ Username: admin
§ Email address: admin@example.com 
§ Password: admin
```

### let's run it
```bash
$ python manage.py runserver
```

### Where to go from here

Congratulations, you now have a fully functional CMS! Awesome job! Let's continue by checking out branch [`step-2`](https://github.com/Chive/djangocms-tutorial/tree/step-2) (You should know how that works by now :)
