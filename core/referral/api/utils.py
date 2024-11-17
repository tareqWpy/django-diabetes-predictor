import secrets

from ..models import Referral


def generate_unique_refer_token():
    while True:
        token = secrets.token_urlsafe(32)
        if not Referral.objects.filter(refer_token=token).exists():
            return token
