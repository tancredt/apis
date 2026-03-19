from django_filters import rest_framework as filters
from django.db import models

from .models import Incident, DetectorSite, ReadingType, Reading, DetectorValidation, DetectorSiteValidation


class IncidentFilter(filters.FilterSet):
    label = filters.CharFilter(lookup_expr='icontains')
    suburb = filters.CharFilter(lookup_expr='icontains')
    start_date_gte = filters.DateFilter(field_name='start_date', lookup_expr='gte')
    start_date_lte = filters.DateFilter(field_name='start_date', lookup_expr='lte')

    class Meta:
        model = Incident
        fields = ['label', 'suburb', 'start_date_gte', 'start_date_lte']


class DetectorSiteFilter(filters.FilterSet):
    incident = filters.NumberFilter()
    label = filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = DetectorSite
        fields = ['incident', 'label']


class ReadingTypeFilter(filters.FilterSet):
    gas = filters.CharFilter(lookup_expr='iexact')
    units = filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = ReadingType
        fields = ['gas', 'units']


class ReadingFilter(filters.FilterSet):
    detector = filters.NumberFilter()
    detector__label = filters.CharFilter(lookup_expr='iexact')
    detector__serial = filters.CharFilter(lookup_expr='icontains')
    reading_type = filters.NumberFilter()
    reading_type__gas = filters.CharFilter(lookup_expr='iexact')
    reading_type__units = filters.CharFilter(lookup_expr='iexact')
    dt_gte = filters.DateTimeFilter(field_name='dt', lookup_expr='gte')
    dt_lte = filters.DateTimeFilter(field_name='dt', lookup_expr='lte')
    is_valid = filters.BooleanFilter()
    detector_site = filters.NumberFilter()
    search = filters.CharFilter(method='filter_search')

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            models.Q(detector__label__icontains=value) |
            models.Q(detector__serial__icontains=value)
        )

    class Meta:
        model = Reading
        fields = [
            'detector', 'detector__label', 'detector__serial',
            'reading_type', 'reading_type__gas', 'reading_type__units',
            'dt_gte', 'dt_lte', 'is_valid', 'detector_site', 'search'
        ]


class DetectorValidationFilter(filters.FilterSet):
    detector = filters.NumberFilter()
    detector__label = filters.CharFilter(lookup_expr='iexact')
    start_dt_gte = filters.DateTimeFilter(field_name='start_dt', lookup_expr='gte')
    start_dt_lte = filters.DateTimeFilter(field_name='start_dt', lookup_expr='lte')
    end_dt_gte = filters.DateTimeFilter(field_name='end_dt', lookup_expr='gte')
    end_dt_lte = filters.DateTimeFilter(field_name='end_dt', lookup_expr='lte')
    reason = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = DetectorValidation
        fields = ['detector', 'detector__label', 'start_dt_gte', 'start_dt_lte', 'end_dt_gte', 'end_dt_lte', 'reason']


class DetectorSiteValidationFilter(filters.FilterSet):
    detector_site = filters.NumberFilter()
    detector_site__label = filters.CharFilter(lookup_expr='iexact')
    start_dt_gte = filters.DateTimeFilter(field_name='start_dt', lookup_expr='gte')
    start_dt_lte = filters.DateTimeFilter(field_name='start_dt', lookup_expr='lte')
    end_dt_gte = filters.DateTimeFilter(field_name='end_dt', lookup_expr='gte')
    end_dt_lte = filters.DateTimeFilter(field_name='end_dt', lookup_expr='lte')
    reason = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = DetectorSiteValidation
        fields = ['detector_site', 'detector_site__label', 'start_dt_gte', 'start_dt_lte', 'end_dt_gte', 'end_dt_lte', 'reason']
