import string
import os
import random
import hashlib
import mimetypes
import logging

from django.db import models
from django.utils.translation import ugettext_lazy as _
from blog_api.abstract_models import AbstractCreatedUpdated
from django.utils.deconstruct import deconstructible
from django.utils.datetime_safe import datetime

THUMBNAIL_SIZE = (640, 360)
THUMBNAIL_SIZE_2X = (1280, 720)


@deconstructible
class PathAndRename(object):
    def __init__(self, sub_path, prefix=''):
        self.filepath = sub_path
        self.prefix = prefix

    def __call__(self, instance, filename):
        date = datetime.now()
        m = hashlib.md5()
        update_hash = str(''.join([random.choice(string.ascii_letters + string.digits)
                                   for n in range(0, 64)]))
        m.update(update_hash.encode('utf-8'))
        new_filename = '{prefix}{hex}-{timestamp}.{ext}'.format(prefix=self.prefix + '_',
                                                                timestamp=str(date.timestamp()),
                                                                hex=m.hexdigest(),
                                                                ext=filename.split('.')[-1])
        return '%(filepath)s/%(year)s/%(month)s/%(day)s/%(filename)s' % {
            'filepath': self.filepath,
            'year': date.year,
            'month': date.month,
            'day': date.day,
            'filename': new_filename
        }


image_path = PathAndRename('images', 'o')
thumbnail_path = PathAndRename('images', 't')
thumbnail2x_path = PathAndRename('images', 't@2x')


class ImageManager(models.Manager):
    pass


class Image(AbstractCreatedUpdated):
    original = models.ImageField(
        verbose_name=_('Image'),
        upload_to=image_path
    )

    thumbnail = models.ImageField(
        verbose_name=_('Thumbnail'),
        upload_to=thumbnail_path,
        blank=True,
        default=''
    )

    thumbnail2x = models.ImageField(
        verbose_name=_('Thumbnail @2x'),
        upload_to=thumbnail2x_path,
        blank=True,
        default=''
    )

    order = models.PositiveSmallIntegerField(
        verbose_name=_('Order number'),
        default=0,
        blank=True
    )

    objects = ImageManager()

    def __str__(self):
        return '#{} {}'.format(self.id, str(self.original))

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = _('Image')
        verbose_name_plural = _('Images')

    def save(self, *args, **kwargs):
        self.create_thumbnails()

        force_update = False

        if self.id:
            force_update = True

        super().save(force_update=force_update)

    def create_thumbnails(self):
        if not self.original :
            return

        try:

            from PIL import Image
            from io import BytesIO
            from django.core.files.uploadedfile import SimpleUploadedFile

            if not hasattr(self.original.file, 'content_type'):
                django_type = mimetypes.guess_type(self.original.path)
            else:
                django_type = self.original.file.content_type

            if django_type == 'image/jpeg':
                file_type = 'jpeg'
                file_ext = 'jpg'
            elif django_type == 'image/png':
                file_type = 'png'
                file_ext = 'png'
            else:
                file_ext = self.original.file.name.split('.').pop()
                file_type = file_ext

            bytes_file = BytesIO(self.original.read())
            image = Image.open(bytes_file)
            image2x = Image.open(bytes_file)

            image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)

            temp_handle = BytesIO()
            image.save(temp_handle, file_type)
            temp_handle.seek(0)

            image2x.thumbnail(THUMBNAIL_SIZE_2X, Image.ANTIALIAS)

            temp_handle2x = BytesIO()
            image2x.save(temp_handle2x, file_type)
            temp_handle2x.seek(0)

            suf = SimpleUploadedFile(os.path.split(self.original.name)[-1],
                                     temp_handle.read(), content_type=django_type)

            suf2x = SimpleUploadedFile(os.path.split(self.original.name)[-1],
                                       temp_handle2x.read(), content_type=django_type)

            self.thumbnail.save(
                '%s_thumbnail.%s' % (os.path.splitext(suf.name)[0], file_ext),
                suf, save=False
            )
            self.thumbnail2x.save(
                '%s_thumbnail2x.%s' % (os.path.splitext(suf.name)[0], file_ext),
                suf2x, save=False)
        except AttributeError as e:
            logger = logging.getLogger('photo.models.image')
            logger.error(e)

    def delete(self, **kwargs):
        if self.original and hasattr(self.original, 'path') and os.path.exists(self.original.path):
            os.remove(self.original.path)

        if self.thumbnail and hasattr(self.thumbnail, 'path') and os.path.exists(self.thumbnail.path):
            os.remove(self.thumbnail.path)

        if self.thumbnail2x and hasattr(self.thumbnail2x, 'path') and os.path.exists(self.thumbnail2x.path):
            os.remove(self.thumbnail2x.path)
        super().delete(**kwargs)

    def get_thumbnail_url(self):
        if self.thumbnail:
            return self.thumbnail.url
        elif self.original:
            return self.original.url
        return ''

    def get_thumbnail2x_url(self):
        if self.thumbnail2x:
            return self.thumbnail2x.url
        elif self.original:
            return self.original.url
        return ''

    def get_original_url(self):
        if self.original:
            return self.original.url
        return ''
