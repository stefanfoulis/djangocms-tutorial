djangoCMS Tutorial - Step 2
===========================
Still with us? Great! So far we set up our environment by installing django, djangoCMS and all necessary dependencies. We also configured djangoCMS and ran it for the first time.

Next up, we want to extend djangoCMS by installing an app. We're gonna be using the aldryn_blog module for this example. Let's get going!

At first, we need to install the extension from the python Package Index (remember, always in the virtual environment!):

```
$ source env/bin/activate
$ pip install aldryn-blog
```

Add the apps below to `INSTALLED_APPS` in `settings.py`:

```
INSTALLED_APPS = [
    …
    'aldryn_blog',
    'django_select2',
    'djangocms_text_ckeditor',
    'easy_thumbnails',
    'filer',
    'taggit',
    …
]
```
Since we added a new app, we need to update our database. Thankfully, django comes with set of awesome tools which do most of the job. We just need to run the following two commands:

```
$ python manage.py syncdb
$ python manage.py migrate
```

and it's done. We can now run our server again

```
$ python manage.py runserver
```
Now go to the admin panel at [localhost:8000/admin](http://localhost:8000/admin) and

* Go to _Cms_ > _Pages_ and add a new page
* Go to the advanced settings of the page we just created
* Under _Application_, select the 'Blog' application and give it a namespace (e.g. `myblog`)
* Save and publish the page
* Restart the server (`CTRL+C` and `python manage.py runserver` again)
* Now go to _Aldryn Blog_ and add a new post
* Voila :)

Quick, check out [`step-3`](https://github.com/Chive/djangocms-tutorial/tree/step-3)!
