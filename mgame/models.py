from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth import get_user_model
from django.utils.text import slugify
import os

# Create your models here.

User=get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

    def __str__(self):
        return self.user.username

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet')
    balance = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.user.username}'s Wallet - ₹{self.balance}"

class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=10, choices=[('credit', 'Credit'), ('debit', 'Debit')])
    description = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type.upper()} ₹{self.amount} - {self.description}"

def upload_game_image(instance, filename):
    base, ext = os.path.splitext(filename)
    return f"game_images/{slugify(instance.name)}{ext.lower()}"


class Game(models.Model):
    name = models.CharField(max_length=100, unique=True)
    genre = models.CharField(max_length=50, default="Battle Royale")
    image = models.ImageField(upload_to=upload_game_image, blank=True, null=True)  # Image field
    def __str__(self):
        return self.name


class event(models.Model):
    old_game=models.CharField(max_length=100,default="Game")
    user=models.ForeignKey(User,null=True,on_delete=models.CASCADE,related_name="createuser")
    user1ingame=models.CharField(null=True,blank=True,max_length=200)
    user2ingame=models.CharField(null=True,blank=True,max_length=200)
    match_type=models.CharField(max_length=50)
    amount=models.IntegerField(default=0)
    is_completed=models.BooleanField(default=False)
    room_id=models.CharField(null=True,blank=True,max_length=20)
    is_match=models.BooleanField(default=False)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=True, blank=True)  # New FK field



class match(models.Model):
    game = models.ForeignKey(event, on_delete=models.CASCADE, null=True)
    user1 = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name="user1")
    user2 = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name="user2")
    winner = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="match_winner")







