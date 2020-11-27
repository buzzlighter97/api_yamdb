from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, access_token_obtain, user_create_with_email

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet, basename='user')

auth_patterns = [
    path(
        'email/',
        user_create_with_email,
        name='user-create-with-email',
    ),
    path(
        'token/',
        access_token_obtain,
        name='access-token-obtain',
    ),
]

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/', include(auth_patterns)),
]
