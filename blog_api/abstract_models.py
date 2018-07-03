from django.conf import settings
from django.db import models
from django.template import defaultfilters
from django.utils import formats
from django.utils.translation import ugettext_lazy as _
from unidecode import unidecode


class AbstractNameSlug(models.Model):
    name = models.CharField(
        verbose_name=_('Title'),
        max_length=100
    )

    slug = models.CharField(
        verbose_name=_('Slug'),
        max_length=32,
        db_index=True,
        help_text=_('This field will be filled automatically.'),
        default=''
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = defaultfilters.slugify(unidecode(self.name))[:32]
        super().save(*args, **kwargs)


class AbstractCreatedUpdated(models.Model):
    created_at = models.DateTimeField(
        verbose_name=_('Created at'),
        auto_now_add=True,
        blank=True
    )

    updated_at = models.DateTimeField(
        verbose_name=_('Updated at'),
        auto_now=True,
        blank=True
    )

    @property
    def created_at_formatted(self):
        return formats.date_format(self.created_at, settings.DATETIME_FORMAT)

    @property
    def updated_at_formatted(self):
        return formats.date_format(self.updated_at, settings.DATETIME_FORMAT)

    class Meta:
        abstract = True
        ordering = ['-updated_at', '-created_at']
