from django.test import TestCase
from articles.models import Article
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
