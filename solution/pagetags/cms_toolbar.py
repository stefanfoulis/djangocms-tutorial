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
