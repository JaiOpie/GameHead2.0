"""gamify URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from mgame import views

urlpatterns = [
    path("admin", admin.site.urls),
    path("",views.signin,name="index"),
    path("signup/",views.signup,name="signup"),
    path("dashboard",views.dashboard,name="dashboard"),
    path("signin",views.signin,name="signin"),
    path("profile/<int:pk>",views.profile,name="profile"),
    path("logout",views.logout,name="logout"),
    path("addevent/",views.addevent,name="addevent"),
    path('delete_event/<int:event_id>/', views.delete_event, name='delete_event'),
    path('event/<int:event_id>/',views.event_detail, name='event_detail'),
    path('event/<int:event_id>/update-room-id/', views.update_room_id, name='update_room_id'),
    path('complete_event/<int:event_id>/', views.complete_event, name='complete_event'),
    path('dashboard/guest/<str:token>/', views.guest_dashboard, name='guest_dashboard'),
    path('search-events/', views.search_events, name='search_events'),
    path('accounts/', include('allauth.urls')),  # ← This enables Google login



]
