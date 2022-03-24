from django_filters import rest_framework as filters, DateFromToRangeFilter, CharFilter, ModelChoiceFilter
from django.contrib.auth.models import User

from advertisements.models import Advertisement


class AdvertisementFilter(filters.FilterSet):
    """Фильтры для объявлений."""
    created_at = DateFromToRangeFilter()
    updated_at = DateFromToRangeFilter()
    status = CharFilter(lookup_expr='iexact')
    creator = ModelChoiceFilter(queryset=User.objects.all())

    class Meta:
        model = Advertisement
        fields = ['created_at', 'updated_at', 'status', 'creator']
