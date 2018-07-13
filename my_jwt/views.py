from django.conf import settings
from rest_framework import serializers
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer, RefreshJSONWebTokenSerializer
from rest_framework_jwt.views import JSONWebTokenAPIView


def get_token_from_request(request):
    token = request.META.get('HTTP_AUTHORIZATION', None)
    if token is None:
        raise serializers.ValidationError('Authorization header is not set.')

    prefix_len = len(settings.JWT_AUTH['JWT_AUTH_HEADER_PREFIX']) + 1
    return token[prefix_len:]


class CustomVerifyJSONWebTokenSerializer(VerifyJSONWebTokenSerializer):
    token = serializers.CharField(required=False)

    def validate(self, attrs):
        attrs['token'] = get_token_from_request(self.context['request'])
        return super().validate(attrs)


class CustomRefreshJSONWebTokenSerializer(RefreshJSONWebTokenSerializer):
    token = serializers.CharField(required=False)

    def validate(self, attrs):
        attrs['token'] = get_token_from_request(self.context['request'])
        return super().validate(attrs)


class CustomVerifyJSONWebToken(JSONWebTokenAPIView):
    serializer_class = CustomVerifyJSONWebTokenSerializer


class CustomRefreshJSONWebToken(JSONWebTokenAPIView):
    serializer_class = CustomRefreshJSONWebTokenSerializer


verify_jwt_token = CustomVerifyJSONWebToken.as_view()
refresh_jwt_token = CustomRefreshJSONWebToken.as_view()
