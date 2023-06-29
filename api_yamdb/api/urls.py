from rest_framework import routers
from django.urls import include, path

from .views import TitleViewSet, CategoryViewSet, GenreViewSet

router = routers.DefaultRouter()
router.register(r'titles', TitleViewSet, basename='titles')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'genres', GenreViewSet, basename='genres')

urlpatterns = [
    path('', include(router.urls))
]
