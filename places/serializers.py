from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _
from places.models import Place


class PlaceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Place
        exclude = ['created_at', 'updated_at']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['type_title'] = instance.get_type_display()
        return ret

    def validate_latitude(self, value):
        if value > 90 or value < -90:
            raise serializers.ValidationError(_('Latitude could only be in range from -90 to 90 degrees.'))
        return value

    def validate_longitude(self, value):
        if value > 180 or value < -180:
            raise serializers.ValidationError(_('Longitude could only be in range from -180 to 180 degrees.'))
        return value
