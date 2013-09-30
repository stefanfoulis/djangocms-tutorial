djangoCMS
=========
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


aldryn-blog
===========
```
# Credentials in passpack (pkg.divio.ch / Access)
$ pip install aldryn-blog --extra-index-url http://pkg.divio.ch
```

Add the apps below to `INSTALLED_APPS`
```
INSTALLED_APPS = [
    …

    'aldryn_blog',
    'django_select2',
    'djangocms_text_ckeditor',
    'easy_thumbnails',
    'filer',
    'hvad',
    'taggit',
    …
]
```

```
$ python manage.py syncdb
$ python manage.py migrate

$ python manage.py runserver
```
Now go to the admin panel at localhost:8000/admin and

* Create a new page
* Go to advanced settings
* Hook the 'Blog' Application and give it a namespace (e.g. 'myblog')
* restart server
* Now to Admin > Aldryn Blog > Add post
* Voila


django-poll-app to cmsApp
=========================
Follow this tutorial to create a new django App: <https://docs.djangoproject.com/en/dev/intro/tutorial01/>

or for the lazy ones: <https://github.com/Chive/django-poll-app> - I knew it would come to use at some point @pat ;)

```
cd src
svn export https://github.com/Chive/django-poll-app/trunk/polls
```

```

```

---------------------------------------





























# old #
Open the file `~/workspace/demo/demo/settings.py`

To make your life easier, add the following at the top of the file:
```
# -*- coding: utf-8 -*-
import os
gettext = lambda s: s
PROJECT_PATH = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0]
```
Add the following apps to your INSTALLED_APPS. This includes django CMS itself as well as its dependenices and other highly recommended applications/libraries:

* `'cms'`, django CMS itself
* `'cms.stacks'`, for reusable content
* `'mptt'`, utilities for implementing a modified pre-order traversal tree
* `'menus'`, helper for model independent hierarchical website navigation
* `'south'`, intelligent schema and data migrations
* `'sekizai'`, for javascript and css management
* `'djangocms_admin_style'`, for the admin skin. You **must** add `'djangocms_admin_style'` in the list before `'django.contrib.admin'`.
* `'django.contrib.messages'` to enable messages framework

You need to add the django CMS middlewares to your MIDDLEWARE_CLASSES at the right position:

```
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.middleware.common.CommonMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware',
)
```
You need at least the following TEMPLATE_CONTEXT_PROCESSORS:
```
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'cms.context_processors.media',
    'sekizai.context_processors.sekizai',
)
```

Point your STATIC_ROOT to where the static files should live (that is, your images, CSS files, Javascript files, etc.):
```
STATIC_ROOT = os.path.join(PROJECT_PATH, "static")
STATIC_URL = "/static/"
```

For uploaded files, you will need to set up the MEDIA_ROOT setting:
```
MEDIA_ROOT = os.path.join(PROJECT_PATH, "media")
MEDIA_URL = "/media/"
```

> Note: Please make sure both the static and media subfolders exist in your project and are writable.

