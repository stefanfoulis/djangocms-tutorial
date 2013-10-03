Solution Step 1
===========================
This is the solution to step 1. If you messed up or want to continue with a clean solution, copy the contents of this folder to your project folder

```
$ cd ~/workspace/djangocms-tutorial
$ git checkout step-2
$ cp -r solution/* ../demo
$ cd ../demo
```


and setup your environment:

```
$ virtualenv env --no-site-packages
$ source env/bin/activate
$ pip install -r requirements.txt
$ python manage.py syncdb --all
$ python manage.py migrate --fake
```



*is that all?*
