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
            self.assertIsNot(place.slug, '')
            self.assertEqual(place.slug, slugs.pop(0))

    def test_created_at_exists(self):
        for place in Place.objects.all():
            self.assertIsNot(place.created_at, '')

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
    created_ids = list()

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
        self.created_ids.append(response.data['id'])

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

    def test_delete_place_bulk(self):
        p = Place.objects.create(name='name',
                                 latitude=42,
                                 longitude=74)
        self.created_ids.append(p.pk)
        response = self.client.delete('/places/', {
            'ids': self.created_ids
        })
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        place_ids = Place.objects.all().values_list('pk', flat=True)
        for pk in self.created_ids:
            self.assertFalse(pk in place_ids)

    def test_get_place_details(self):
        p = Place.objects.create(name='name',
                                 latitude=42,
                                 longitude=74)
        response = self.client.get('/places/%d/' % p.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], p.pk)
        self.assertEqual(response.data['name'], p.name)
        self.assertEqual(response.data['latitude'], p.latitude)
        self.assertEqual(response.data['longitude'], p.longitude)

    def test_get_not_created_place_details(self):
        response = self.client.get('/places/999999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_place(self):
        p = Place.objects.create(name='name',
                                 latitude=42,
                                 longitude=74)
        new_data = {
            'name': 'new name',
            'latitude': 74.124123,
            'longitude': 42.412512,
        }
        response = self.client.put('/places/%d/' % p.pk, new_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], p.pk)
        self.assertNotEqual(response.data['name'], p.name)
        self.assertNotEqual(response.data['latitude'], p.latitude)
        self.assertNotEqual(response.data['longitude'], p.longitude)
        self.assertEqual(response.data['name'], new_data['name'])
        self.assertEqual(response.data['latitude'], new_data['latitude'])
        self.assertEqual(response.data['longitude'], new_data['longitude'])

    def test_update_place_with_patch_data(self):
        p = Place.objects.create(name='name',
                                 latitude=42,
                                 longitude=74)
        new_data = {
            'name': 'new name'
        }
        response = self.client.put('/places/%d/' % p.pk, new_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_place(self):
        p = Place.objects.create(name='name',
                                 latitude=42,
                                 longitude=74)
        new_data = {
            'name': 'new name'
        }
        response = self.client.patch('/places/%d/' % p.pk, new_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], p.pk)
        self.assertEqual(response.data['name'], new_data['name'])

    def test_delete_place(self):
        p = Place.objects.create(name='name',
                                 latitude=42,
                                 longitude=74)
        response = self.client.delete('/places/%d/' % p.pk)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        p = Place.objects.filter(pk=p.pk).first()
        self.assertIsNone(p)
