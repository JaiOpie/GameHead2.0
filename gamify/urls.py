from django.urls import path, include
from rest_framework.routers import DefaultRouter
from mgame import views  # Template views
from mgame import api_views  # API views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

# REST Framework router for viewsets
router = DefaultRouter()
router.register(r'events', api_views.EventViewSet, basename='event')
router.register(r'matches', api_views.MatchViewSet, basename='match')
router.register(r'games', api_views.GameViewSet, basename='game')

urlpatterns = [
    # ---------- Template-based views ----------
    path("admin/", admin.site.urls),
    path("", views.signin, name="index"),
    path("signup/", views.signup, name="signup"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("signin", views.signin, name="signin"),
    path("profile/<int:pk>", views.profile, name="profile"),
    path("logout", views.logout, name="logout"),
    path("addevent/", views.addevent, name="addevent"),
    path("delete_event/<int:event_id>/", views.delete_event, name="delete_event"),
    path("event/<int:event_id>/", views.event_detail, name="event_detail"),
    path("event/<int:event_id>/update-room-id/", views.update_room_id, name="update_room_id"),
    path("complete_event/<int:event_id>/", views.complete_event, name="complete_event"),
    path("search-events/", views.search_events, name="search_events"),
    path("accounts/", include("allauth.urls")),
    path("demo-login/", views.demo_login, name="demo_login"),

    # ---------- API views ----------
    path("api/signup/", api_views.signup_api, name="api_signup"),
    path("api/login/", api_views.login_api, name="api_login"),
    path("api/logout/", api_views.logout_api, name="api_logout"),
    path("api/wallet/balance/", api_views.wallet_balance_api, name="wallet_balance"),
    path("api/wallet/credit/", api_views.credit_wallet_api, name="wallet_credit"),
    path("api/wallet/debit/", api_views.debit_wallet_api, name="wallet_debit"),
    path("api/event/<int:event_id>/join/", api_views.join_event, name="join_event"),
    path("api/event/<int:event_id>/complete/", api_views.complete_event_api, name="complete_event_api"),
    path("api/event/<int:event_id>/room-id/", api_views.update_room_id_api, name="update_room_id_api"),
    path("api/users/<int:user_id>/events/upcoming/", api_views.user_upcoming_events, name="user_upcoming_events"),
    path("api/users/<int:user_id>/events/completed/", api_views.user_completed_events, name="user_completed_events"),
    path('api/admin/create-wallets/', api_views.create_wallets_for_all_users, name='create_wallets_for_all_users'),
    path('api/admin/credit-wallet/', api_views.credit_user_wallet, name='credit_user_wallet'),



    # ---------- Router for ModelViewSets ----------
    path("api/", include(router.urls)),
]


from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="HeadToHead API",
      default_version='v1',
      description="API documentation for HeadToHead gaming platform",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

