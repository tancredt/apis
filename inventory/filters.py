from django_filters import rest_framework as filters
from django.db import models

from .models import (
    Location,
    DetectorModel,
    Detector,
    DetectorModelConfiguration,
    DetectorFault,
    Maintenance,
    MaintenanceTask,
    CylinderType,
    Cylinder,
    CylinderFault,
    LocationDetectorSlot,
    SensorType,
    Sensor,
    SensorSlot
)

class LocationFilter(filters.FilterSet):
    label = filters.CharFilter(lookup_expr='icontains')
    address = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Location
        fields = ['label', 'address']

class DetectorModelFilter(filters.FilterSet):
    detector_type = filters.CharFilter(lookup_expr='iexact')
    label = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = DetectorModel
        fields = ['detector_type', 'label']

class DetectorFilter(filters.FilterSet):
    label = filters.CharFilter(lookup_expr='icontains')
    serial = filters.CharFilter(lookup_expr='icontains')
    status = filters.CharFilter(lookup_expr='iexact')
    configuration__label = filters.CharFilter(lookup_expr='iexact')
    location__label = filters.CharFilter(lookup_expr='iexact')
    location = filters.NumberFilter()
    detector_model__model_name = filters.CharFilter(lookup_expr='iexact')
    detector_model__detector_type = filters.CharFilter(lookup_expr='iexact')
    detector_model = filters.NumberFilter()
    exclude_status = filters.CharFilter(field_name='status', lookup_expr='iexact', exclude=True)
    search = filters.CharFilter(method='filter_search')

    def filter_search(self, queryset, name, value):
        # Search in label and serial
        return queryset.filter(
            models.Q(label__icontains=value) |
            models.Q(serial__icontains=value)
        )

    class Meta:
        model = Detector
        fields = ['search', 'status', 'location', 'detector_model', 'configuration__label', 'exclude_status']

class DetectorFaultFilter(filters.FilterSet):
    detector = filters.NumberFilter()
    detector__label = filters.CharFilter(lookup_expr='iexact')
    report_dt_gte = filters.DateFilter(field_name='report_dt', lookup_expr='gte')
    report_dt_lte = filters.DateFilter(field_name='report_dt', lookup_expr='lte')
    report_location__label = filters.CharFilter(lookup_expr='iexact')
    fault_type = filters.CharFilter(lookup_expr='iexact')
    exclude_status = filters.CharFilter(field_name='status', lookup_expr='iexact', exclude=True)

    class Meta:
        model = DetectorFault
        fields = ['detector', 'detector__label', 'report_dt_gte', 'report_dt_lte', 'report_location__label', 'fault_type', 'exclude_status']


class MaintenanceFilter(filters.FilterSet):
    maintenance_type = filters.CharFilter(lookup_expr='iexact')
    status = filters.CharFilter(lookup_expr='iexact')
    detector = filters.NumberFilter()
    detector__label = filters.CharFilter(lookup_expr='iexact')
    date_due_lte = filters.DateFilter(field_name='date_due', lookup_expr='lte')
    exclude_status = filters.CharFilter(field_name='status', lookup_expr='iexact', exclude=True)

    class Meta:
        model = Maintenance
        fields = ['maintenance_type', 'status', 'detector', 'detector__label', 'date_due_lte', 'exclude_status']

class MaintenanceTaskFilter(filters.FilterSet):
    maintenance = filters.NumberFilter()
    maintenance__maintenance_type = filters.CharFilter(lookup_expr='iexact')
    maintenance__detector = filters.NumberFilter()
    maintenance__detector__label = filters.CharFilter(lookup_expr='iexact')
    maintenance__detector__detector_model__detector_type = filters.CharFilter(lookup_expr='iexact')
    maintenance__date_performed_gte = filters.DateFilter(field_name='maintenance__date_performed', lookup_expr='gte')
    maintenance__date_performed_lte = filters.DateFilter(field_name='maintenance__date_performed', lookup_expr='lte')
    task_type = filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = MaintenanceTask
        fields = ['maintenance', 'task_type']

class CylinderTypeFilter(filters.FilterSet):
    active = filters.BooleanFilter()

    class Meta:
        model = CylinderType
        fields = ['active']

class CylinderFilter(filters.FilterSet):
    cylinder_number = filters.NumberFilter()
    serial = filters.CharFilter(lookup_expr='icontains')
    location__label = filters.CharFilter(lookup_expr='iexact')
    location = filters.NumberFilter()
    status = filters.CharFilter(lookup_expr='iexact')
    cylinder_type__part_number = filters.CharFilter(lookup_expr='icontains')
    expiry_date_lte = filters.DateFilter(field_name='expiry_date', lookup_expr='lte')
    expiry_date_gte = filters.DateFilter(field_name='expiry_date', lookup_expr='gte')
    exclude_status = filters.CharFilter(field_name='status', lookup_expr='iexact', exclude=True)
    search = filters.CharFilter(method='filter_search')

    def filter_search(self, queryset, name, value):
        # Search in serial
        return queryset.filter(
            models.Q(serial__icontains=value)
        )

    class Meta:
        model = Cylinder
        fields = ['search', 'serial', 'location', 'status', 'cylinder_type__part_number', 'expiry_date_lte', 'expiry_date_gte', 'exclude_status']

class SensorTypeFilter(filters.FilterSet):
    active = filters.BooleanFilter()
    part_number = filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = SensorType
        fields = ['active', 'part_number']

class SensorFilter(filters.FilterSet):
    serial = filters.CharFilter(lookup_expr='icontains')
    status = filters.CharFilter(lookup_expr='iexact')
    sensor_type = filters.NumberFilter()
    sensor_type__part_number = filters.CharFilter(lookup_expr='icontains')
    detector = filters.NumberFilter()
    detector__label = filters.CharFilter(lookup_expr='iexact')
    detector__serial = filters.CharFilter(lookup_expr='icontains')
    warranty_date_lte = filters.CharFilter(field_name='warranty_date', lookup_expr='lte')
    warranty_date_gte = filters.CharFilter(field_name='warranty_date', lookup_expr='gte')
    end_date_lte = filters.CharFilter(field_name='end_date', lookup_expr='lte')
    end_date_gte = filters.CharFilter(field_name='end_date', lookup_expr='gte')
    exclude_status = filters.CharFilter(field_name='status', lookup_expr='iexact', exclude=True)
    search = filters.CharFilter(method='filter_search')

    def filter_search(self, queryset, name, value):
        # Search in serial and sensor_type__part_number
        return queryset.filter(
            models.Q(serial__icontains=value) |
            models.Q(sensor_type__part_number__icontains=value)
        )

    class Meta:
        model = Sensor
        fields = ['search', 'serial', 'status', 'sensor_type', 'sensor_type__part_number', 'detector', 'detector__label', 'detector__serial', 'warranty_date_lte', 'warranty_date_gte', 'end_date_lte', 'end_date_gte', 'exclude_status']

class SensorSlotFilter(filters.FilterSet):
    sensor_type__part_number = filters.CharFilter(lookup_expr='icontains')
    detector = filters.NumberFilter()
    detector__label = filters.CharFilter(lookup_expr='iexact')
    detector__serial = filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = SensorSlot
        fields = ['sensor_type__part_number', 'detector', 'detector__label', 'detector__serial']

class DetectorModelConfigurationFilter(filters.FilterSet):
    detector_model__model_name = filters.CharFilter(lookup_expr='iexact')
    detector_model__detector_type = filters.CharFilter(lookup_expr='iexact')
    detector_model = filters.NumberFilter()

    class Meta:
        model = DetectorModelConfiguration
        fields = ['detector_model__model_name', 'detector_model__detector_type', 'detector_model']

class LocationDetectorSlotFilter(filters.FilterSet):
    class Meta:
        model = LocationDetectorSlot
        fields = []

class CylinderFaultFilter(filters.FilterSet):
    cylinder__label = filters.CharFilter(lookup_expr='iexact')
    report_dt_gte = filters.DateFilter(field_name='report_dt', lookup_expr='gte')
    report_dt_lte = filters.DateFilter(field_name='report_dt', lookup_expr='lte')
    report_location__label = filters.CharFilter(lookup_expr='iexact')
    fault_type = filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = CylinderFault
        fields = ['cylinder__label', 'report_dt_gte', 'report_dt_lte', 'report_location__label', 'fault_type']
