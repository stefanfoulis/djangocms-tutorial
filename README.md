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

apphook_pool.register(PollsApp)
```


Phew, quite some work done. If you're still on fire, check out branch [`step-4`](https://github.com/Chive/djangocms-tutorial/tree/step-4)!
