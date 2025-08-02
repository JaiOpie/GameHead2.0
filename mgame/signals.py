from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from .models import Profile
from django.db import IntegrityError


@receiver(user_signed_up)
def create_user_profile(request, user, **kwargs):
    try:
        Profile.objects.create(user=user)
    except IntegrityError:
        pass

