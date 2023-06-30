from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (TitleViewSet,
                    CategoryViewSet,
                    GenreViewSet,
                    UserViewSet,
                    SignUpViewSet,
                    TokenViewSet) 

app_name = 'api'

v1_router = DefaultRouter()

v1_router.register(r'titles', TitleViewSet, basename='titles')
v1_router.register(r'categories', CategoryViewSet, basename='categories')
v1_router.register(r'genres', GenreViewSet, basename='genres')
v1_router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(v1_router.urls)),
    #path('v1/auth/signup/', SignUpViewSet.as_view(), name='signup'),
    #path('v1/auth/token/', TokenViewSet.as_view(), name='get_token'), 
]
