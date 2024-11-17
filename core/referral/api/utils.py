import secrets

from ..models import ReferralCode


def generate_unique_refer_token():
    while True:
        token = secrets.token_urlsafe(32)
        token = token[:32]
        if not ReferralCode.objects.filter(token=token).exists():
            return token
