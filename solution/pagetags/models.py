from cms.extensions import PageExtension, extension_pool
from taggit.managers import TaggableManager


class PageTag(PageExtension):
    tags = TaggableManager()

extension_pool.register(PageTag)
