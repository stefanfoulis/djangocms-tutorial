from cms.extensions import PageExtensionAdmin
from django.contrib import admin
from .models import PageTag


class PageTagAdmin(PageExtensionAdmin):
    list_display = ('extended_object')

    def is_draft_page(self, obj):
        return obj.extended_object.publisher_is_draft

admin.site.register(PageTag, PageTagAdmin)