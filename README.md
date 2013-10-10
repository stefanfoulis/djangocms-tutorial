django CMS Tutorial - Step 6
============================
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
    list_display = ['extended_object']

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
                url = reverse('admin:pagetags_pagetag_change',
                              args=(page_tag.pk,))
            else:
                url = reverse(
                    'admin:pagetags_pagetag_add')\
                      +'?extended_object=%s' % self.page.pk
        except NoReverseMatch:
            # not in urls
            pass
        else:
            not_edit_mode = not self.toolbar.edit_mode
            current_page_menu = self.toolbar.get_or_create_menu('page')
            current_page_menu.add_modal_item(_('Tags'), url=url,
                                             disabled=not_edit_mode)
```

Congrats, we're finished with the app - let's add it to our project. Open up `my_demo/settings.py` and add `pagetags` to your `INSTALLED_APPS`. Afterwards, update your database using `python manage.py syncdb` and start the server again.

You can now change a page's tags through the toolbar directly in the front end! (`Page` > `Tags ...`)

So, we're almost at the end! You can check out [`step-7`](https://github.com/Chive/djangocms-tutorial/tree/step-7) to see solution for this step.
