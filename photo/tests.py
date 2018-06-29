import os

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from photo.models import Image


class PhotoTestCase(TestCase):

    def setUp(self):
        with open(os.path.join(settings.BASE_DIR, 'static', 'test.jpeg'), 'rb') as file:
            suf = SimpleUploadedFile('image.jpeg', file.read(), 'image/jpeg')
            Image.objects.create(original=suf)

    def test_thumbnails_created(self):
        image = Image.objects.first()
        self.assertNotEqual(image.thumbnail, '')
        self.assertNotEqual(image.thumbnail2x, '')
        image_path = os.path.join(settings.MEDIA_ROOT, image.original.url)
        thumbnail_path = os.path.join(settings.MEDIA_ROOT, image.thumbnail.url)
        thumbnail2x_path = os.path.join(settings.MEDIA_ROOT, image.thumbnail2x.url)
        self.assertTrue(os.path.exists(settings.BASE_DIR + image_path))
        self.assertTrue(os.path.exists(settings.BASE_DIR + thumbnail_path))
        self.assertTrue(os.path.exists(settings.BASE_DIR + thumbnail2x_path))
