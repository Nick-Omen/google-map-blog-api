import re

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.html import strip_tags
from django.db import models
from blog_api.abstract_models import AbstractCreatedUpdated, AbstractNameSlug
from django.utils.translation import ugettext_lazy as _
from articles.settings import ARTICLE_TYPES, PLACE_TYPE_PHOTO, PLACE_TYPE_ARTICLE


class Article(AbstractNameSlug, AbstractCreatedUpdated):
    date = models.DateTimeField(
        verbose_name=_('Date'),
        default=timezone.now,
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

    main_image = models.ForeignKey(
        'photo.Image',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        default=None,
        related_name='main_image'
    )

    images = models.ManyToManyField(
        'photo.Image',
        verbose_name=_('Images'),
        blank=True
    )

    class Meta:
        verbose_name = _('Article')
        verbose_name_plural = _('Articles')

    def save(self, *args, **kwargs):
        content_short = re.sub(r'[\n\r]+', ' ', strip_tags(self.content)[:140])
        self.content_short = re.sub(r' +', ' ', content_short)
        self.type = self.get_identified_type()
        super().save(*args, **kwargs)

    def get_identified_type(self):
        if self.content and len(self.content) > 0:
            return PLACE_TYPE_ARTICLE
        return PLACE_TYPE_PHOTO

    def get_main_image_url(self):
        return self.main_image.get_original_url()

    def get_thumbnail_url(self):
        return self.main_image.get_thumbnail_url()

    def get_thumbnail2x_url(self):
        return self.main_image.get_thumbnail2x_url()

    def set_main_image(self):
        first_image = self.images.order_by('-order').first()
        if first_image is not None:
            self.main_image = first_image
            self.save(update_fields=['main_image'])


@receiver(post_save, sender=Article)
def article_saved(sender, instance, **kwargs):
    instance.place.update_type()
