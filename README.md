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

### Create a template
The aldryn installer did most of the work for us, however we need to add our custom template to the CMS.

First, delete the two files in `demo/my_demo/templates/`. Afterwards, create these two files in that folder:

**`base.html`**:

```html
{% load cms_tags sekizai_tags menu_tags %}
<html>
    <head>
        {% render_block "css" %}
    </head>
    <body>
        {% cms_toolbar %}
        <ul>
            {% show_menu 0 100 100 100 %}
        </ul>
        {% block content %}{% endblock %}
        {% render_block "js" %}
    </body>
</html>
```

**`page.html`**:

```html
{% extends "base.html" %}
{% load cms_tags sekizai_tags menu_tags placeholder_tags %}

{% block content %}
    {% placeholder content %}
{% endblock %}
```

Next, open up `my_demo/settings.py`, look for `CMS_TEMPLATES` and change it to this:

```python
CMS_TEMPLATES = (
    ('page.html', 'Page'),
)
```

### let's run it
```bash
$ python manage.py runserver
```

### Where to go from here

Congratulations, you now have a fully functional CMS! Awesome job! Let's continue by checking out branch [`step-2`](https://github.com/Chive/djangocms-tutorial/tree/step-2) (You should know how that works by now :)
