from django.db import models
from django.utils.translation import ugettext_lazy as _

from blog_api.abstract_models import AbstractNameSlug, AbstractCreatedUpdated

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


class Place(AbstractNameSlug, AbstractCreatedUpdated):
    name = models.CharField(
        verbose_name=_('Name'),
        max_length=100
    )

    slug = models.CharField(
        verbose_name=_('Slug'),
        max_length=32,
        default='',
        blank=True
    )

    latitude = models.FloatField(
        verbose_name=_('Latitude')
    )

    longitude = models.FloatField(
        verbose_name=_('Latitude')
    )

    type = models.CharField(
        verbose_name=_('Place type'),
        max_length=1,
        choices=PLACE_TYPES,
        default=PLACE_TYPE_NONE
    )

    class Meta:
        verbose_name = _('Place')
        verbose_name_plural = _('Places')
