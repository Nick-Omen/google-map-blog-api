import pytz
from rest_framework_jwt.utils import jwt_decode_handler
from datetime import datetime

from django.conf import settings


def response_payload_handler(token, *args):
    payload = jwt_decode_handler(token)
    exp_datetime = datetime.fromtimestamp(payload['exp'], tz=pytz.timezone(settings.TIME_ZONE))
    return {
        'token': token,
        'token_type': settings.JWT_AUTH['JWT_AUTH_HEADER_PREFIX'],
        'expired_at': exp_datetime.isoformat()
    }
