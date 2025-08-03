from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Profile, Wallet, Transaction, event, match, Game

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ["id", "user"]

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ["id", "balance"]

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ["id", "wallet", "amount", "type", "description", "timestamp"]

class EventSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    game_name = serializers.CharField(source='game.name', read_only=True)
    game_image = serializers.ImageField(source='game.image', read_only=True)

    class Meta:
        model = event
        fields = [
            "id", "game", "user", "user1ingame", "user2ingame", "match_type",
            "amount", "is_completed", "room_id", "is_match", "game_name", "game_image"
        ]

class MatchSerializer(serializers.ModelSerializer):
    game = EventSerializer(read_only=True)
    user1 = UserSerializer(read_only=True)
    user2 = UserSerializer(read_only=True)
    winner = UserSerializer(read_only=True)

    class Meta:
        model = match
        fields = ["id", "game", "user1", "user2", "winner"]

class CreditWalletSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    description = serializers.CharField(required=False, allow_blank=True)


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'