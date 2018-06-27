from places.settings import PLACE_TYPE_PHOTO, PLACE_TYPE_ARTICLE
from django.utils.translation import ugettext_lazy as _

ARTICLE_TYPES = (
    (PLACE_TYPE_ARTICLE, _('Article')),
    (PLACE_TYPE_PHOTO, _('Photo')),
)
