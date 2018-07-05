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
        main_image_serializer = ImageSerializer(data={
            'original': request.data.get('main_image')
        }, context={'request': request})
        images_serializer = ImageSerializer(data=[{'original': i} for i in request.data.getlist('images')],
                                            many=True, context={'request': request})
        main_image = None
        images = None
        if main_image_serializer.is_valid():
            main_image = main_image_serializer.save()
        if images_serializer.is_valid():
            images = images_serializer.save()

        request.data['main_image'] = main_image.pk if main_image is not None else None

        serializer = CreateArticleSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            article = serializer.save()
            if images is not None:
                article.images.set(images)
            serializer = ArticleDetailsSerializer(article, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if main_image is not None:
            main_image.delete()
        if images is not None:
            for image in images:
                image.delete()
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleDetails(APIView):

    def get(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        serializer = ArticleDetailsSerializer(article, context={'request': request})
        return Response(serializer.data)
