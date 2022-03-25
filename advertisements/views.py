from django.contrib.auth.models import AnonymousUser
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from advertisements.filters import AdvertisementFilter
from advertisements.models import Advertisement
from advertisements.permissions import IsOwner
from advertisements.serializers import AdvertisementSerializer


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = AdvertisementFilter

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsOwner()]
        return []

    def get_queryset(self):
        current_user = self.request.user
        objects = Advertisement.objects.all()
        if current_user.is_anonymous:
            queryset = objects.filter(draft=False)
            return queryset
        else:
            queryset = objects.exclude(~Q(creator=current_user) & Q(draft=True))
            return queryset

