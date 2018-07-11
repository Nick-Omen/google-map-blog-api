import os

from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.test import TestCase
from django.test.client import encode_multipart
from django.urls import reverse
from rest_framework import status

from articles.models import Article
from articles.settings import PLACE_TYPE_ARTICLE, PLACE_TYPE_PHOTO
from places.models import Place


class ArticleTestCase(TestCase):

    def setUp(self):
        place = Place.objects.create(name='Test place',
                                     latitude=40.666,
                                     longitude=20.666)
        Article.objects.create(name='Trip in the galaxy!',
                               content="<h2>Galaxy \r\r  trip!</h2>\n\n<p>Long  time  ago, in a galaxy far away...</p>",
                               place=place)

    def test_article_short_content_created(self):
        article = Article.objects.first()
        article_stripped_tags = 'Galaxy trip! Long time ago, in a galaxy far away...'
        self.assertTrue(article.content_short != '')
        self.assertEqual(article.content_short, article_stripped_tags)


class ArticleListAPITestCase(TestCase):

    def setUp(self):
        place = Place.objects.create(name='Test place',
                                     latitude=40.666,
                                     longitude=20.666)
        Article.objects.create(name='Trip in the galaxy!',
                               content="<h2>Galaxy \r\r  trip!</h2>\n\n<p>Long  time  ago, in a galaxy far away...</p>",
                               place=place)

    def test_get_articles(self):
        response = self.client.get(reverse('articles:list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response.data, list))

    def test_create_article_with_content(self):
        place = Place.objects.first()
        self.assertIsNotNone(place)

        data = {
            'name': 'article name',
            'content': '<h2>Galaxy \r\r  trip!</h2>\n\n<p>Long  time  ago, in a galaxy far away...</p>',
            'place': place.pk
        }
        response = self.client.post(reverse('articles:list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['content'], data['content'])
        self.assertIsNot(response.data['content_short'], '')
        self.assertEqual(response.data['type'], PLACE_TYPE_ARTICLE)

    def test_create_article_with_photo(self):
        place = Place.objects.first()
        self.assertIsNotNone(place)

        image_path = os.path.join(settings.BASE_DIR, 'static', 'test.jpeg')
        with open(image_path, 'rb') as file:
            # imuf = InMemoryUploadedFile(file, 'image', 'image.jpeg', 'image/jpeg', os.path.getsize(image_path), None)
            data = {
                'name': 'article name',
                'place': place.pk,
                'images': [
                    {
                        'image': file.read(),
                        'order': 1
                    }
                ]
            }
            response = self.client.post(reverse('articles:list'), data=data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(response.data['name'], data['name'])
            self.assertEqual(response.data['content_short'], '')
            self.assertEqual(response.data['type'], PLACE_TYPE_PHOTO)
            self.assertIsInstance(response.data['images'], list)
            self.assertEqual(len(response.data['images']), 1)
            article = Article.objects.get(pk=response.data['id'])
            self.assertIsNotNone(article.main_image)
            self.assertIn(article.main_image.get_, response.data['images'][0]['id'])

    def test_create_article_with_multiple_photos(self):
        place = Place.objects.first()
        self.assertIsNotNone(place)

        image_path = os.path.join(settings.BASE_DIR, 'static', 'test.jpeg')
        with open(image_path, 'rb') as file:
            imuf = InMemoryUploadedFile(file, 'image', 'image.jpeg', 'image/jpeg', os.path.getsize(image_path), None)
            data = {
                'name': 'article name',
                'place': place.pk,
                'images': [
                    {
                        'image': imuf,
                        'order': 3
                    },
                    {
                        'image': imuf,
                        'order': 2
                    },
                    {
                        'image': imuf,
                        'order': 1
                    },
                ]
            }
            response = self.client.post(reverse('articles:list'), data=data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
