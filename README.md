djangoCMS Tutorial - Step 1
===========================
Hey, you made it! Awesome. Now let's get started by setting up our environment.

Preparing your workstation
--------------------------

```
$ pip install --upgrade virtualenv
```
Installing the CMS
------------------
```
# Make a project folder
$ cd ~/workspace	
$ mkdir demo && cd demo

# Setup virtual environment
$ virtualenv env --no-site-packages
$ source env/bin/activate
$ pip install -e git+https://github.com/nephila/aldryn-installer#egg=aldryn-installer

# install djangoCMS (follow the recommandations in the brackets by just hitting enter on most prompts, don't worry if the setup takes a while :)
$ aldryn -p . my_demo

# let's run it
$ python manage.py runserver
```

### Where to go from here

Congratulations, you now have a fully functional CMS! Awesome job! Let's continue by checking out branch [`step-2`](https://github.com/Chive/djangocms-tutorial/tree/step-2) (You should know how that works by now :)
