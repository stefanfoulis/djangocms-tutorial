djangoCMS Tutorial
==================

Prerequisites / Requirements
----------------------------
* python
* git
* pip
* ..more?

Start
-----
In order to start, you first need to clone this repository. Open a shell,
cd into your workspace and git clone the tutorial

```bash
cd ~/workspace
git clone git@github.com:Chive/djangocms-tutorial.git
cd djangocms-tutorial
```

Now checkout branch [`step-1`](https://github.com/Chive/djangocms-tutorial/tree/step-1) to get going!

```bash
git checkout step-1
```

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

djangoCMS Tutorial - Step 2
===========================
Still with us? Great! So far we set up our environment by installing django, djangoCMS and all necessary dependencies. We also configured djangoCMS and ran it for the first time.

Next up, we want to extend djangoCMS by installing an app. We're gonna be using the aldryn_blog module for this example. Let's get going!

At first, we need to install the extension from the python Package Index (remember, always in the virtual environment!):

```bash
$ source env/bin/activate
$ pip install aldryn-blog
```

Add the apps below to `INSTALLED_APPS` in `settings.py`:

```python
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

```bash
$ python manage.py syncdb
$ python manage.py migrate
```

and it's done.

Finally, we need to copy a html template for our blog to our project:

```bash
cp ../djangocms-tutorial/sources/base.html my_demo/templates/
```

We can now run our server again

```bash
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

djangoCMS Tutorial - Step 3
===========================
In this part of the tutorial we're going to take a django app and modify it like that so we can use it in the CMS. We're gonna use the django-poll app.

You can either complete the tutorial here <https://docs.djangoproject.com/en/dev/intro/tutorial01/> or copy the folder `polls` from `djangocms-tutorial/sources/` to your project root.

```bash
~/workspace/demo $ cp -r ../djangocms-tutorial/sources/polls .
```

You should end up with this folder structure:

```
workspace
	djangocms-tutorial/
	my_demo/
		env/
		manage.py
		my_demo/
			__init__.py
			settings.py
			templates/
				base.html
				index.html
				page.html
			urls.py
			wsgi.py
		polls/
			README.md
			__init__.py
			admin.py
			models.py
			templates/
				polls/
					detail.html
					index.html
					results.html
			tests.py
			urls.py
			views.py
		project.db
		requirements.txt
```

Our first plugin
----------------

### The Model
For our polling app we would like to have a small poll plugin which shows a poll and lets the user vote.

In your poll application’s `models.py` add the following:

```python
from cms.models import CMSPlugin

class PollPlugin(CMSPlugin):
    poll = models.ForeignKey('polls.Poll', related_name='plugins')

    def __unicode__(self):
      return self.poll.question
```

**Note:** django CMS plugins must inherit from `cms.models.CMSPlugin` (or a subclass thereof) and not `models.Model`.

### The Plugin Class
Now create a file `cms_plugins.py` in the same folder your models.py is in. The plugin class is responsible for providing the django CMS with the necessary information to render your Plugin.

For our poll plugin, write the following plugin class:

```python
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from polls.models import PollPlugin as PollPluginModel
from django.utils.translation import ugettext as _

class PollPlugin(CMSPluginBase):
    model = PollPluginModel # Model where data about this plugin is saved
    name = _("Poll Plugin") # Name of the plugin
    render_template = "polls/plugin.html" # template to render the plugin with

    def render(self, context, instance, placeholder):
        context.update({'instance':instance})
        return context

plugin_pool.register_plugin(PollPlugin) # register the plugin
```

**Note**: All plugin classes must inherit from `cms.plugin_base.CMSPluginBase` and must register themselves with the `cms.plugin_pool.plugin_pool`.

### The Template
You probably noticed the render_template attribute in the above plugin class. In order for our plugin to work, that template must exist and is responsible for rendering the plugin.

The template is located at `polls/templates/polls/plugin.html` and should look something like this:

```html
<h1>{{ instance.poll.question }}</h1>

<form action="{% url polls.views.vote instance.poll.id %}" method="post">
	{% csrf_token %}
	{% for choice in instance.poll.choice_set.all %}
    	<input type="radio" name="choice" id="choice{{ forloop.counter }}" value="{{ choice.id }}" />
		<label for="choice{{ forloop.counter }}">{{ choice.choice }}</label><br />
	{% endfor %}
	<input type="submit" value="Vote" />
</form>
```

**Note**: We don’t show the errors here, because when submitting the form you’re taken off this page to the actual voting page.

Quite some work done by now, let's add it to our project. Add your polls plugin to the `INSTALLED_APPS` in your projects `settings.py`:

```python
INSTALLED_APPS = (

	...
	
    'polls',
    
    ...
)
```

Secondly, add it to the project's `urls.py` so it looks something like this:

```python
urlpatterns = i18n_patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^polls/', include('polls.urls')),
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': {'cmspages': CMSSitemap}}),
    url(r'^', include('cms.urls')),
)
```

Now to create the database tables for this model (using South):

```bash
$ python manage.py schemamigration polls --initial
$ python manage.py migrate polls
```

Finally, run the server and go visit <http://localhost:8000/polls/>. Yay!


### My First App (apphook)
Right now, external apps are statically hooked into the main `urls.py`. This is not the preferred approach in the django CMS. Ideally you attach your apps to CMS pages.

For that purpose you write a CMSApp. That is just a small class telling the CMS how to include that app.

CMS Apps live in a file called `cms_app.py`, so go ahead and create it to make your polls app look like this:

```
polls/
    __init__.py
    cms_app.py
    cms_plugins.py
    models.py
    tests.py
    views.py
```

In this file, write:

```python
from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _

class PollsApp(CMSApp):
    name = _("Poll App") # give your app a name, this is required
    urls = ["polls.urls"] # link your app to url configuration(s)

apphook_pool.register(PollsApp) # register your app
```

Now remove the inclusion of the polls urls in your project's `urls.py` so it looks like this:

```python
urlpatterns = i18n_patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': {'cmspages': CMSSitemap}}),
    url(r'^', include('cms.urls')),
)
```

Now open your admin in your browser and edit a CMS Page. Open the ‘Advanced Settings’ tab and choose ‘Polls App’ for your ‘Application’. Just like we did with the blog some minutes ago.

Again, for these changes to take effect, you will have to restart your server. So do that and afterwards if you navigate to that CMS Page, you will see your polls application.

### My First Menu
Now you might have noticed that the menu tree stops at the CMS Page you created in the last step. So let’s create a menu that shows a node for each poll you have active.

For this we need a file called `menu.py`. Create it and ensure your polls app looks like this:

````
polls/
    __init__.py
    cms_app.py
    cms_plugins.py
    menu.py
    models.py
    tests.py
    views.py
```

In your `menu.py` write:

```python
from cms.menu_bases import CMSAttachMenu
from menus.base import Menu, NavigationNode
from menus.menu_pool import menu_pool
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from polls.models import Poll

class PollsMenu(CMSAttachMenu):
    name = _("Polls Menu") # give the menu a name, this is required.

    def get_nodes(self, request):
        """
        This method is used to build the menu tree.
        """
        nodes = []
        for poll in Poll.objects.all():
            # the menu tree consists of NavigationNode instances
            # Each NavigationNode takes a label as its first argument, a URL as
            # its second argument and a (for this tree) unique id as its third
            # argument.
            node = NavigationNode(
                poll.question,
                reverse('polls.views.detail', args=(poll.pk,)),
                poll.pk
            )
            nodes.append(node)
        return nodes
menu_pool.register_menu(PollsMenu) # register the menu.
```

At this point this menu alone doesn’t do a whole lot. We have to attach it to the Apphook first.

So open your `cms_apps.py` and write:

```python
from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from polls.menu import PollsMenu
from django.utils.translation import ugettext_lazy as _

class PollsApp(CMSApp):
    name = _("Poll App")
    urls = ["polls.urls"]
    menus = [PollsMenu] # attach a CMSAttachMenu to this apphook.
    app_name = 'polls'

apphook_pool.register(PollsApp)
```


Phew, quite some work done. If you're still on fire, check out branch [`step-4`](https://github.com/Chive/djangocms-tutorial/tree/step-4)!

djangoCMS Tutorial - Step 4
===========================
Extending the Toolbar
---------------------
In the new version 3.0 you can add and remove items to the toolbar. This allows you to integrate your application in the frontend editing mode of django CMS and provide your users with a streamlined editing experience.

### Registering
There are two ways to control what gets shown in the toolbar.

One is the `CMS_TOOLBARS`. This gives you full control over which classes are loaded, but requires that you specify them all manually.

The other is to provide `cms_toolbar.py` files in your apps, which will be automatically loaded as long `CMS_TOOLBARS` is not set (or set to `None`).

If you use the automated way, your `cms_toolbar.py` file should contain classes that extend from `cms.toolbar_base.CMSToolbar` and are registered using `cms.toolbar_pool.toolbar_pool.register()`. The register function can be used as a decorator.

These have four attributes:

* `toolbar` (the toolbar object)
* `request` (the current request)
* `is_current_app` (a flag indicating whether the current request is handled by the same app as the function is in)
* `app_path` (the name of the app used for the current request)

This classes must implement a populate function. The populate function will only be called if the current user is a staff user.

A simple example, registering a class that does nothing:

```python
from cms.toolbar_pool import toolbar_pool
from cms.toolbar_base import CMSToolbar

@toolbar_pool.register
class MoopModifier(CMSToolbar):

    def populate(self):
        pass
```

### Adding items
Items can be added through the various APIs exposed by the toolbar and its items.

To add a `cms.toolbar.items.Menu` to the toolbar, use `cms.toolbar.toolbar.CMSToolbar.get_or_create_menu()` which will either add a menu if it doesn’t exist, or create it.

Then, to add a link to your changelist that will open in the sideframe, use the `cms.toolbar.items.ToolbarMixin.add_sideframe_item()` method on the menu object returned.

When adding items, all arguments other than the name or identifier should be given as keyword arguments. This will help ensure that your custom toolbar items survive upgrades.

Following our Extending the CMS: Examples, let’s add the poll app to the toolbar:

```python
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from cms.toolbar_pool import toolbar_pool
from cms.toolbar_base import CMSToolbar

@toolbar_pool.register
class PollToolbar(CMSToolbar):

    def populate(self):
        if self.is_current_app:
            menu = self.toolbar.get_or_create_menu('poll-app', _('Polls'))
            url = reverse('admin:polls_poll_changelist')
            menu.add_sideframe_item(_('Poll overview'), url=url)
```

However, there’s already a menu added by the CMS which provides access to various admin views, so you might want to add your menu as a sub menu there. To do this, you can use positional insertion coupled with the fact that `cms.toolbar.toolbar.CMSToolbar.get_or_create_menu()` will return already existing menus:

```python
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from cms.toolbar_pool import toolbar_pool
from cms.toolbar.items import Break
from cms.cms_toolbar import ADMIN_MENU_IDENTIFIER, ADMINISTRATION_BREAK
from cms.toolbar_base import CMSToolbar

@toolbar_pool.register
class PollToolbar(CMSToolbar):

    def populate(self):
        admin_menu = self.toolbar.get_or_create_menu(ADMIN_MENU_IDENTIFIER, _('Site'))
        position = admin_menu.find_first(Break, identifier=ADMINISTRATION_BREAK)
        menu = admin_menu.get_or_create_menu('poll-menu', _('Polls'), position=position)
        url = reverse('admin:polls_poll_changelist')
        menu.add_sideframe_item(_('Poll overview'), url=url)
        admin_menu.add_break('poll-break', position=menu)
```

### Adding items through views
Another way to add items to the toolbar is through our own views (`polls/views.py`). This method can be useful if you need to access certain variables, in our case e.g. the selected poll and its sub-methods:

```python
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render
from django.utils.translation import ugettext_lazy as _

from polls.models import Poll


def detail(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)

    request.toolbar.populate()
    menu = request.toolbar.get_or_create_menu('polls-app', _('Polls'))
    menu.add_modal_item(_('Change this Poll'), url=reverse('admin:polls_poll_change', args=[poll_id]))
    menu.add_sideframe_item(_('Show History of this Poll'), url=reverse('admin:polls_poll_history', args=[poll_id]))
    menu.add_sideframe_item(_('Delete this Poll'), url=reverse('admin:polls_poll_delete', args=[poll_id]))

    return render(request, 'polls/detail.html', {'poll': poll})
```

step-5: extending the page model

djangoCMS Tutorial - Step 5
===========================
Extending the page model
------------------------
Create a new python module in your project root - let's call it `pagetags`. Add all the files below:

```
pagetags/
	__init.py__
	admin.py
	cms_toolbar.py
	models.py
```


### The Model
At first, we're gonna set up the model. To do so, open up `models.py`, create a class extending `cms.extensions.PageExtension` and make a `tags` field of the type `taggit.managers.TaggableManager`. Afterwards, register the class in the `cms.extensions.extension_pool`. It should look something like this:

```python
from cms.extensions import PageExtension, extension_pool
from taggit.managers import TaggableManager


class PageTag(PageExtension):
    tags = TaggableManager()

extension_pool.register(PageTag)
```

### The Admin
Let's make a very simple admin class in the `admin.py`.

```python
from cms.extensions import PageExtensionAdmin
from django.contrib import admin
from .models import PageTag


class PageTagAdmin(PageExtensionAdmin):
    list_display = ('extended_object')

admin.site.register(PageTag, PageTagAdmin)
```

Oh wait, let's add a method to the `PageTagAdmin` class, so we can see whether the tags where added to a draft page or not:

```python
    def is_draft_page(self, obj):
        return obj.extended_object.publisher_is_draft
```

### The Toolbar
Let's get to the fun part: Putting it all together and adding it to the toolbar!

```python
from django.core.urlresolvers import reverse, NoReverseMatch
from django.utils.translation import ugettext_lazy as _

from cms.api import get_page_draft
from cms.toolbar_pool import toolbar_pool
from cms.toolbar_base import CMSToolbar
from .models import PageTag


@toolbar_pool.register
class PageTagsToolbar(CMSToolbar):
    def populate(self):
        # always use draft if we have a page
        self.page = get_page_draft(self.request.current_page)

        if not self.page:
            # Nothing to do
            return

        try:
            page_tag = PageTag.objects.get(extended_object_id=self.page.id)
        except PageTag.DoesNotExist:
            page_tag = None
        try:
            if page_tag:
                url = reverse('admin:pagetags_pagetag_change', args=(page_tag
                                                                 .pk,))
            else:
                url = reverse('admin:pagetags_pagetag_add')+'?extended_object' \
                                                            '=%s' % self.page.pk
        except NoReverseMatch:
            # not in urls
            pass
        else:
            not_edit_mode = not self.toolbar.edit_mode
            current_page_menu = self.toolbar.get_or_create_menu('page')
            current_page_menu.add_modal_item(_('Tags'), url=url,
                                             disabled=not_edit_mode)
```

What we did here is # TODO: this.

djangoCMS Tutorial - Step 6
===========================
Stacks: displaying the same content on multiple locations
---------------------------------------------------------
If you need to display the same content on multiple locations you can use stacks.

Stacks have a name and a placeholder attached to them. There are 3 ways to use stacks.

### 1. Stack Template Tags	
You can use a template tag to display a placeholder in a template without the need for an actual placeholder on you models. This can be useful for:
	* Footer
	* Logo
	* Header
	* Text or content inside you app
	* Text or content inside of 3th party apps.
	
**Example:**
	
```python
{% load stack_tags %} {% stack “footer” %}
```
	
***Note:*** It is recommended to use stacks in your apphook apps instead of show_placeholder templatetags

### 2. Stack Plugins

You can create a stack out of plugins. You can create stacks out of plugin trees. After you created a stack this way you can insert a stack plugin and select a stack to be displayed instead of the stack plugin.

### 3. Stacks as templates

If you create stacks out of plugin tree you can paste the plugins contained in a stack as template. For example you can create a teaser plugin tree out of a multicolumn, text and picture plugin. You can then paste this template at the appropriate place and just edit the plugins instead of creating the same structure over and over.


`# TODO: improve
