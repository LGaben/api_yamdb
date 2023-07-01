from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (TitleViewSet,
                    CategoryViewSet,
                    GenreViewSet,
                    UserViewSet,
                    SignUpViewSet,
                    TokenViewSet)

router_v1 = DefaultRouter()

router_v1.register(r'titles', TitleViewSet, basename='titles')
router_v1.register(r'categories', CategoryViewSet, basename='categories')
router_v1.register(r'genres', GenreViewSet, basename='genres')
router_v1.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(router_v1.urls)),
    #path('v1/auth/signup/', SignUpViewSet.as_view(), name='signup'),
    #path('v1/auth/token/', TokenViewSet.as_view(), name='get_token'), 
]
