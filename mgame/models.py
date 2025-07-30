from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth import get_user_model

# Create your models here.

User=get_user_model()

class Profile(models.Model):
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING,null=True,related_name="user")
    def __str__(self):
        return self.user.username




class event(models.Model):
    game=models.CharField(max_length=100)
    user=models.ForeignKey(User,null=True,on_delete=models.CASCADE,related_name="createuser")
    user1ingame=models.CharField(null=True,blank=True,max_length=10)
    user2ingame=models.CharField(null=True,blank=True,max_length=10)
    match_type=models.CharField(max_length=50)
    amount=models.IntegerField(default=0)
    is_completed=models.BooleanField(default=False)
    room_id=models.CharField(null=True,blank=True,max_length=20)
    is_match=models.BooleanField(default=False)



class match(models.Model):
    game = models.ForeignKey(event, on_delete=models.CASCADE, null=True)
    user1 = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name="user1")
    user2 = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name="user2")
    winner = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="match_winner")







