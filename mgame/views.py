from django.shortcuts import render,redirect, get_object_or_404
from mgame.models import *
from django.contrib import messages
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.contrib.auth.models import AnonymousUser
from django.db.models import Q
from django.http import JsonResponse
from django.template.loader import render_to_string


# Create your views here.

def index(request):
    return render(request,"index.html")



def guest_dashboard(request, token):
    # Replace with your actual secret token
    SECRET_TOKEN = "df15d893-35e5-43bd-98e2-efd3e64300a7"

    if token != SECRET_TOKEN:
        raise Http404("Invalid access token.")

    # Use public or sample data (or all events, as you prefer)
    game = event.objects.filter(is_match=False)

    context = {
        'user_object': None,
        'gamedata': game,
    }
    return render(request, "dashboard.html", context)


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['pass1']
        password2 = request.POST['pass2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model)
                new_profile.save()
                return redirect('dashboard')
    else:
        return render(request,'signup.html')



@login_required(login_url='signin')
def search_events(request):
    query = request.GET.get('q', '')
    user = request.user

    if query:
        events = event.objects.filter(
            Q(id__icontains=query) |
            Q(game__icontains=query) |
            Q(match_type__icontains=query) |
            Q(user__username__icontains=query) |
            Q(amount__icontains=query),
            is_match=False
        ).exclude(user=user)
    else:
        events = event.objects.filter(is_match=False).exclude(user=user)

    html = render_to_string('partial_event_list.html', {'gamedata': events}, request=request)
    return JsonResponse({'html': html})



@login_required(login_url='signin')
def dashboard(request):
    user_object = request.user
    query = request.GET.get('q')

    if query:
        game = event.objects.filter(
            Q(id__icontains=query) |
            Q(game__icontains=query) |
            Q(match_type__icontains=query) |
            Q(user__username__icontains=query) |
            Q(amount__icontains=query),
            is_match=False
        ).exclude(user=request.user)
    else:
        game = event.objects.filter(is_match=False).exclude(user=request.user)

    context = {
        'user_object': user_object,
        'gamedata': game,
    }
    return render(request, "dashboard.html", context)


@login_required(login_url='signin')
def profile(request, pk):
    user_object = User.objects.get(id=pk)
    user_profile = Profile.objects.get(user=user_object)
    ematch=match.objects.all()
    upcoming_matches=[]
    completed_matches=[]
    for i in ematch:
        if i.user1==user_object or i.user2==user_object:
            if not i.game.is_completed:
                upcoming_matches.append(i.game)
            else:
                completed_matches.append(i.game)

    context = {
        'upcoming_matches': upcoming_matches,
        'completed_matches': completed_matches,
        'user_object': user_object,
        'user_profile': user_profile,
    }
    return render(request, 'profile.html', context)

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('dashboard')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('signin')

    else:
        return render(request, 'signin.html')


@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')

@login_required(login_url='signin')
def addevent(request):
    if request.method =="POST":
        gamename=request.POST['gamename']
        characterid=request.POST['ingamename']
        matchtype=request.POST['matchtype']
        amount=request.POST['amount']
        user_object = User.objects.get(username=request.user.username)
        event1=event.objects.create(
            game=gamename,
            user1ingame=characterid,
            match_type=matchtype,
            amount=amount,
            user_id=user_object.id
        )
        match.objects.create(
            game_id=event1.id,
            user1_id=user_object.id
        )
        messages.success(request, "Event created successfully!")
        return redirect("dashboard")
    return render(request,"add event.html")


@login_required(login_url='signin')
def delete_event(request, event_id):
    try:
        event_obj = event.objects.get(id=event_id)
        if event_obj.user != request.user:
            raise Http404("You are not allowed to delete this event.")
        event_obj.delete()
        messages.success(request, "Event deleted successfully.")
        return redirect('profile', pk=request.user.id)
    except event.DoesNotExist:
        messages.error(request, "Event not found.")
        return redirect('dashboard')


def event_detail(request, event_id):
    # Retrieve the event object and match
    event_obj = event.objects.get(id=event_id)
    user_object = User.objects.get(username=request.user.username)
    match_object = match.objects.get(game_id=event_id)

    if request.method == 'POST':
        new_room_id = request.POST.get('new_room_id')
        if new_room_id:
            event_obj.room_id = new_room_id
            event_obj.save()

        ingame_name = request.POST.get('ingame_name')
        if ingame_name:
            event_obj.user2ingame = ingame_name
            event_obj.is_match = True
            event_obj.save()

            match_object.user2 = user_object
            match_object.save()

    user1 = match_object.user1
    user2 = match_object.user2

    context = {
        'event': event_obj,
        'user_object': user_object,
        'user1': user1,
        'user2': user2,
        'match': match_object,
    }

    return render(request, 'event_detail.html', context)


def update_room_id(request, event_id):
    event_obj = event.objects.get(id=event_id)

    if request.method == 'POST':
        new_room_id = request.POST.get('new_room_id')
        event_obj.room_id = new_room_id
        event_obj.save()
        return redirect('event_detail', event_id=event_id)

    return redirect('event_detail', event_id=event_id)

def complete_event(request, event_id):
    if request.method == 'POST':
        winner_id = request.POST.get('winner_id')
        winner_user = get_object_or_404(User, id=winner_id)

        event_obj = get_object_or_404(event, id=event_id)
        event_obj.is_completed = True
        event_obj.save()

        try:
            match_obj = match.objects.get(game=event_obj)
            match_obj.winner = winner_user
            match_obj.save()
        except match.DoesNotExist:
            pass

    return redirect('/dashboard')





