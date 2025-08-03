from rest_framework import viewsets, permissions, status, parsers
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.db.models import Q

from .models import Profile, Wallet, Transaction, event, match, Game
from .serializers import (
    UserSerializer, ProfileSerializer, WalletSerializer,
    TransactionSerializer, EventSerializer, MatchSerializer, CreditWalletSerializer, GameSerializer
)
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi



# User Registration
@api_view(['POST'])
def signup_api(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    password2 = request.data.get('confirm_password')

    if password != password2:
        return Response({'error': 'Passwords do not match'}, status=400)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=400)

    if User.objects.filter(email=email).exists():
        return Response({'error': 'Email already exists'}, status=400)

    user = User.objects.create_user(username=username, email=email, password=password)
    Profile.objects.create(user=user)
    # Wallet.objects.create(user=user)
    user = authenticate(username=username, password=password)
    if user:
        login(request, user)

    return Response({'message': 'User created and logged in successfully'})


# Login
@api_view(['POST'])
def login_api(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return Response({'message': 'Logged in successfully'})
    return Response({'error': 'Invalid credentials'}, status=401)


# Logout
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_api(request):
    logout(request)
    return Response({'message': 'Logged out'})


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
            user = self.request.user

            if self.action in ['destroy', 'retrieve', 'update', 'partial_update']:
                return event.objects.all()

            queryset = event.objects.filter(is_match=False).exclude(user=user)

            query = self.request.query_params.get("q")
            if query:
                queryset = queryset.filter(
                    Q(game__name__icontains=query) |
                    Q(user__username__icontains=query) |
                    Q(match_type__icontains=query)
                )
            return queryset


    def perform_create(self, serializer):
        match_type = self.request.data.get("match_type")
        gamename = self.request.data.get("game")
        characterid = self.request.data.get("user1ingame")

        event_obj = serializer.save(user=self.request.user)
        match.objects.create(game=event_obj, user1=self.request.user)



class MatchViewSet(viewsets.ModelViewSet):
    queryset = match.objects.all()
    serializer_class = MatchSerializer
    permission_classes = [permissions.IsAuthenticated]


# Event Matching
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def join_event(request, event_id):
    event_obj = get_object_or_404(event, id=event_id)
    if event_obj.user == request.user:
        return Response({'error': 'You cannot join your own event'}, status=403)

    ingame_name = request.data.get("ingame_name")
    if not ingame_name:
        return Response({'error': 'In-game name required'}, status=400)

    event_obj.user2ingame = ingame_name
    event_obj.is_match = True
    event_obj.save()

    match_obj = get_object_or_404(match, game=event_obj)
    match_obj.user2 = request.user
    match_obj.save()

    return Response({'message': 'Successfully joined the match'})


# Complete Event
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def complete_event_api(request, event_id):
    winner_id = request.data.get('winner_id')
    winner_user = get_object_or_404(User, id=winner_id)

    event_obj = get_object_or_404(event, id=event_id)
    if event_obj.user != request.user:
        return Response({'error': 'Only event creator can complete it'}, status=403)

    event_obj.is_completed = True
    event_obj.save()

    match_obj = get_object_or_404(match, game=event_obj)
    match_obj.winner = winner_user
    match_obj.save()

    return Response({'message': 'Event completed'})


# Room ID Update
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def update_room_id_api(request, event_id):
    event_obj = get_object_or_404(event, id=event_id)

    if event_obj.user != request.user:
        return Response({'error': 'Permission denied'}, status=403)

    room_id = request.data.get("room_id")
    event_obj.room_id = room_id
    event_obj.save()

    return Response({'message': 'Room ID updated'})


# Delete Event
@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def delete_event_api(request, event_id):
    event_obj = get_object_or_404(event, id=event_id)

    if event_obj.user != request.user:
        return Response({'error': 'Permission denied'}, status=403)

    event_obj.delete()
    return Response({'message': 'Event deleted successfully'})


# Wallet Balance
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def wallet_balance_api(request):
    return Response({"balance": request.user.wallet.balance})


# Credit Wallet
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def credit_wallet_api(request):
    amount = float(request.data.get("amount"))
    description = request.data.get("description", "Top-up")
    wallet = request.user.wallet
    wallet.balance += amount
    wallet.save()
    Transaction.objects.create(wallet=wallet, amount=amount, type='credit', description=description)
    return Response({"balance": wallet.balance})


# Debit Wallet
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def debit_wallet_api(request):
    amount = float(request.data.get("amount"))
    description = request.data.get("description", "Game Fee")
    wallet = request.user.wallet

    if wallet.balance < amount:
        return Response({"error": "Insufficient funds"}, status=400)

    wallet.balance -= amount
    wallet.save()
    Transaction.objects.create(wallet=wallet, amount=amount, type='debit', description=description)
    return Response({"balance": wallet.balance})


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_upcoming_events(request, user_id):
    if request.user.id != user_id:
        return Response({'error': 'Permission denied'}, status=403)

    events = event.objects.filter(
        Q(user__id=user_id) | Q(match__user2__id=user_id),
        is_completed=False
    ).distinct()
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_completed_events(request, user_id):
    if request.user.id != user_id:
        return Response({'error': 'Permission denied'}, status=403)

    events = event.objects.filter(
        Q(user__id=user_id) | Q(match__user2__id=user_id),
        is_completed=True
    ).distinct()
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)

from rest_framework.permissions import IsAdminUser

@api_view(['POST'])
@permission_classes([IsAdminUser])
def create_wallets_for_all_users(request):
    users_without_wallet = User.objects.filter(wallet__isnull=True)
    created_count = 0

    for user in users_without_wallet:
        Wallet.objects.create(user=user)
        created_count += 1

    return Response({
        "message": f"Wallets created for {created_count} users.",
        "total_users_without_wallet": users_without_wallet.count()
    }, status=status.HTTP_201_CREATED)




@swagger_auto_schema(method='post', request_body=CreditWalletSerializer)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def credit_user_wallet(request):
    serializer = CreditWalletSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    user_id = serializer.validated_data['user_id']
    amount = serializer.validated_data['amount']
    description = serializer.validated_data.get('description', 'Admin credit')

    user = User.objects.filter(id=user_id).first()
    if not user:
        return Response({"error": "User not found"}, status=404)

    wallet, _ = Wallet.objects.get_or_create(user=user)
    wallet.balance += amount
    wallet.save()

    Transaction.objects.create(wallet=wallet, amount=amount, type='credit', description=description)

    return Response({
        "message": f"₹{amount:.2f} credited to {user.username}'s wallet.",
        "new_balance": wallet.balance
    })


class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [permissions.IsAuthenticated]  # or AllowAny if you want it open
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]  # 👈 this is key
