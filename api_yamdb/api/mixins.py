from rest_framework.mixins import CreateModelMixin, ListModelMixin, DestroyModelMixin
from rest_framework import viewsets


class ListCreateDeleteViewSet(
    DestroyModelMixin,
    ListModelMixin,
    CreateModelMixin,
    viewsets.GenericViewSet
):
    pass
