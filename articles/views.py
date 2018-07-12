import logging

from django.http import Http404
from rest_framework import status, serializers
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from articles.models import Article
from articles.serializers import ArticleListSerializer, CreateArticleSerializer, ArticleDetailsSerializer
from photo.serializers import ImageSerializer, ImageOrderSerializer


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

    def put(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        serializer = ArticleDetailsSerializer(article, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        serializer = ArticleDetailsSerializer(article, data=request.data,
                                              context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        article.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class ArticleImageList(APIView):
    def get(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        serializer = ImageSerializer(article.images.all(), many=True,
                                     context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        data = list()
        image_orders = list(article.images.all().values_list('order', flat=True))
        order = max(*list(article.images.all().values_list('order', flat=True))) + 1 if len(image_orders) > 0 else 0
        images = request.data.getlist('images')
        if isinstance(images, list) and len(images) > 0 and isinstance(images[0], dict):
            for item in images:
                try:
                    if int(item['order']):
                        order = int(item['order'])
                except ValueError as e:
                    order += 1
                    logger = logging.getLogger('articles.views.imagelist')
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
        serializer = ImageSerializer(data=data, many=True,
                                     context={'request': request})
        if serializer.is_valid():
            images = serializer.save()
            article.images.add(*images)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        serializer = ImageOrderSerializer(article.images.all().order_by('id'), data=request.data,
                                          many=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            serializer = ImageSerializer(article.images.all(), many=True,
                                         context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        if 'ids' not in request.data:
            raise serializers.ValidationError('`ids` parameter is required.')
        images = article.images.filter(pk__in=request.data['ids'])
        if images is not None:
            images.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class ArticleImageDetails(APIView):
    def put(self, request, pk, image_pk):
        article = get_object_or_404(Article, pk=pk)
        image = article.images.filter(pk=image_pk).first()
        if image is None:
            raise Http404
        serializer = ImageSerializer(image, data={
            'original': request.data['photo'] if 'photo' in request.data else None
        }, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, image_pk):
        article = get_object_or_404(Article, pk=pk)
        image = article.images.filter(pk=image_pk).first()
        if image is None:
            raise Http404
        image.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
