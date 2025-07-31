from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from .models import Profile

@receiver(user_signed_up)
def create_user_profile(request, user, **kwargs):
    print("🔥 SIGNAL TRIGGERED FOR USER:", user.username)  # Add this
    Profile.objects.create(user=user)
