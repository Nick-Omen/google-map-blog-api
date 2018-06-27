from django.utils.translation import ugettext_lazy as _

PLACE_TYPE_NONE = '0'
PLACE_TYPE_PHOTO = '1'
PLACE_TYPE_ARTICLE = '2'
PLACE_TYPE_MIXED = '3'

PLACE_TYPES = (
    (PLACE_TYPE_NONE, _('None')),
    (PLACE_TYPE_PHOTO, _('Photo')),
    (PLACE_TYPE_ARTICLE, _('Article')),
    (PLACE_TYPE_MIXED, _('Mixed')),
)
