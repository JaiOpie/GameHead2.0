from allauth.account.signals import user_signed_up
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile
from django.db import IntegrityError
from django.contrib.auth.models import User
from .utils import credit_wallet



@receiver(user_signed_up)
def create_user_profile(request, user, **kwargs):
    try:
        Profile.objects.create(user=user)
    except IntegrityError:
        pass


@receiver(post_save, sender=User)
def create_wallet_for_user(sender, instance, created, **kwargs):
    if created:
        from .models import Wallet
        Wallet.objects.create(user=instance)

@receiver(post_save, sender=User)
def give_signup_bonus(sender, instance, created, **kwargs):
    if created:
        credit_wallet(instance, 100, description="Signup Bonus")
