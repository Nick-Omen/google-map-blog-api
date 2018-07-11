from rest_framework import serializers
from articles.models import Article
from places.models import Place
from photo.serializers import ImageSerializer
from places.serializers import PlaceSerializer


class ArticleListSerializer(serializers.ModelSerializer):
    place = PlaceSerializer(read_only=True)
    main_image = ImageSerializer(read_only=True)

    class Meta:
        model = Article
        exclude = ['content', 'images']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['type_title'] = instance.get_type_display()
        ret['place_id'] = instance.place_id
        return ret


class ArticleDetailsSerializer(serializers.ModelSerializer):
    place = PlaceSerializer(read_only=True)
    images = ImageSerializer(read_only=True, many=True)

    class Meta:
        model = Article
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['type_title'] = instance.get_type_display()
        ret['place_id'] = instance.place_id
        return ret


class CreateArticleSerializer(serializers.ModelSerializer):
    place = serializers.PrimaryKeyRelatedField(queryset=Place.objects.all(), required=True)

    class Meta:
        model = Article
        exclude = ['content_short', 'images']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['type_title'] = instance.get_type_display()
        return ret
