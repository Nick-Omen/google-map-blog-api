from datetime import datetime
from django.utils.html import strip_tags
from django.db import models
from blog_api.abstract_models import AbstractCreatedUpdated, AbstractNameSlug
from django.utils.translation import ugettext_lazy as _
from places.models import PLACE_TYPE_PHOTO, PLACE_TYPE_ARTICLE

ARTICLE_TYPES = (
    (PLACE_TYPE_ARTICLE, _('Article')),
    (PLACE_TYPE_PHOTO, _('Photo')),
)


class Article(AbstractNameSlug, AbstractCreatedUpdated):
    date = models.DateTimeField(
        verbose_name=_('Date'),
        default=datetime.now,
        blank=True
    )

    content = models.TextField(
        verbose_name=_('Content'),
        blank=True,
        default=''
    )

    content_short = models.CharField(
        verbose_name=_('Content short'),
        max_length=155,
        blank=True,
        default=''
    )

    place = models.ForeignKey(
        'places.Place',
        verbose_name=_('Place'),
        on_delete=models.SET_NULL,
        null=True
    )

    type = models.CharField(
        verbose_name=_('Type'),
        max_length=1,
        choices=ARTICLE_TYPES,
        default=PLACE_TYPE_ARTICLE
    )

    class Meta:
        verbose_name = _('Article')
        verbose_name_plural = _('Articles')

    def save(self, *args, **kwargs):
        self.content_short = strip_tags(self.content)[:140]
        self.type = self.get_identified_type()
        super().save(*args, **kwargs)

    def get_identified_type(self):
        if self.content and len(self.content) > 0:
            return PLACE_TYPE_ARTICLE
        return PLACE_TYPE_PHOTO
