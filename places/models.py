from django.db import models
from django.utils.translation import ugettext_lazy as _

from places.settings import PLACE_TYPE_NONE, PLACE_TYPES
from articles.models import Article
from blog_api.abstract_models import AbstractNameSlug, AbstractCreatedUpdated


class PlaceManager(models.Manager):
    pass


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

    objects = PlaceManager()

    class Meta:
        verbose_name = _('Place')
        verbose_name_plural = _('Places')

    def get_articles(self):
        return Article.objects.filter(place=self)
