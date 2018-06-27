from django.test import TestCase
from places.models import Place


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
