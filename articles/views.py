import logging

from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from articles.models import Article
from articles.serializers import ArticleListSerializer, CreateArticleSerializer, ArticleDetailsSerializer
from photo.serializers import ImageSerializer


class ArticleList(APIView):
    parser_classes = (MultiPartParser, FormParser,)

    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleListSerializer(articles, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        data = list()
        order = 0
        images = request.data.getlist('images')
        if isinstance(images, list) and len(images) > 0 and isinstance(images[0], dict):
            for item in images:
                try:
                    if int(item['order']):
                        order = int(item['order'])
                except ValueError as e:
                    order += 1
                    logger = logging.getLogger('articles.views.list')
                    logger.error(e)
                data.append({
                    'original': item['image'],
                    'order': order
                })
        else:
            for item in images:
                data.append({
                    'original': item,
                    'order': order
                })
                order += 1

        images_serializer = ImageSerializer(data=data,
                                            many=True, context={'request': request})
        images_valid = False
        if images_serializer.is_valid():
            images_valid = True

        serializer = CreateArticleSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            article = serializer.save()
            if images_valid:
                images = images_serializer.save()
                article.images.set(images)
                article.set_main_image()
            serializer = ArticleDetailsSerializer(article, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleDetails(APIView):

    def get(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        serializer = ArticleDetailsSerializer(article, context={'request': request})
        return Response(serializer.data)
