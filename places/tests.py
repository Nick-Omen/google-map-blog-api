from django.test import TestCase
from rest_framework import status

from places.models import Place
from articles.models import Article
from rest_framework.test import APIRequestFactory, APITestCase


class PlaceTestCase(TestCase):

    def setUp(self):
        Place.objects.create(name='short name',
                             latitude=42.8768537,
                             longitude=74.5218215)
        Place.objects.create(name='коротное название латиницей',
                             latitude=42.8768537,
                             longitude=74.5218215)
        Place.objects.create(name='long name longer then slug length, and slug length is 32 symbols',
                             latitude=42.8768537,
                             longitude=74.5218215)

    def test_slug_created(self):
        slugs = [
            'short-name',
            'korotnoe-nazvanie-latinitsei',
            'long-name-longer-then-slug-lengt'
        ]
        for place in Place.objects.all():
            self.assertTrue(place.slug != '')
            self.assertEqual(place.slug, slugs.pop(0))

    def test_created_at_exists(self):
        for place in Place.objects.all():
            self.assertTrue(place.created_at != '')

    def test_updated_at_changed(self):
        place = Place.objects.first()
        updated_at_old = place.updated_at
        place.title = 'New title updated'
        place.save()
        self.assertNotEqual(updated_at_old, place.updated_at)

    def test_slug_changed(self):
        place = Place.objects.last()
        slug_old = place.slug
        place.name = 'New title should update slug'
        place.save()
        self.assertNotEqual(slug_old, place.slug)
        self.assertEqual(place.slug, 'new-title-should-update-slug')

    def test_get_articles_by_place(self):
        place = Place.objects.last()
        article = Article.objects.create(name='Trip to the Ocean',
                                         place=place)
        place_articles = place.get_articles()
        self.assertQuerysetEqual(place_articles, [repr(a) for a in Article.objects.filter(pk=article.pk)])


class PlaceAPITestCase(APITestCase):

    def test_get_places(self):
        response = self.client.get('/places/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response.data, list))

    def test_create_place(self):
        data = {
            'name': 'place name',
            'latitude': 42.831241,
            'longitude': 74.141214
        }
        response = self.client.post('/places/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['latitude'], data['latitude'])
        self.assertEqual(response.data['longitude'], data['longitude'])

    def test_create_place_empty_name(self):
        data = {
            'latitude': 42.831241,
            'longitude': 74.141214
        }
        response = self.client.post('/places/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(isinstance(response.data['name'], list))

    def test_create_place_empty_location(self):
        data = {
            'name': 'place name'
        }
        response = self.client.post('/places/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(isinstance(response.data['latitude'], list))
        self.assertTrue(isinstance(response.data['longitude'], list))

    def test_create_place_wrong_location(self):
        data = {
            'name': 'place name',
            'latitude': 90.3124123,
            'longitude': 180.4123123
        }
        response = self.client.post('/places/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(isinstance(response.data['latitude'], list))
        self.assertTrue(isinstance(response.data['longitude'], list))

    def test_create_place_wrong_location_negative(self):
        data = {
            'name': 'place name',
            'latitude': -90.3124123,
            'longitude': -180.4123123
        }
        response = self.client.post('/places/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(isinstance(response.data['latitude'], list))
        self.assertTrue(isinstance(response.data['longitude'], list))
