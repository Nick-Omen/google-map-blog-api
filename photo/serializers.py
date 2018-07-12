from rest_framework import serializers

from photo.models import Image


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ['id', 'original', 'order']

    def to_representation(self, instance):
        request = self.context.get('request')
        if request is None:
            raise ValueError('`ImageSerializer` require request inside context.')
        ret = super().to_representation(instance)
        ret['original'] = request.build_absolute_uri(instance.get_original_url())
        ret['thumbnail'] = request.build_absolute_uri(instance.get_thumbnail_url())
        ret['thumbnail_2x'] = request.build_absolute_uri(instance.get_thumbnail2x_url())
        return ret


class ImageOrderListSerializer(serializers.ListSerializer):

    def update(self, instances, validated_data):
        if instances.count() != len(validated_data):
            raise serializers.ValidationError('Wrong count of objects passed.')
        ret = []
        i = 0
        for image in instances:
            image.order = validated_data[i]['order']
            image.save(update_fields=['order'])
            ret.append(image)
            i += 1
        return ret


class ImageOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'order']
        list_serializer_class = ImageOrderListSerializer
