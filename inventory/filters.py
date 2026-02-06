from django_filters import rest_framework as filters

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
    LocationDetectorSlots,
    SensorType,
    Sensor,
    SensorSlot
)

class LocationFilter(filters.FilterSet):
    label = filters.CharFilter(lookup_expr='icontains')
    address = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Location
        fields = []

class DetectorModelFilter(filters.FilterSet):
    detector_type = filters.CharFilter(lookup_expr='iexact')
    model_name = filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = DetectorModel
        fields=[]
        
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

    class Meta:
        model = Detector
        fields = []

class DetectorFaultFilter(filters.FilterSet):
    detector = filters.NumberFilter()
    detector__label = filters.CharFilter(lookup_expr='iexact')
    report_dt_gte = filters.DateFilter(field_name='report_dt', lookup_expr='gte')
    report_dt_lte = filters.DateFilter(field_name='report_dt', lookup_expr='lte')
    report_location__label = filters.CharFilter(lookup_expr='iexact')
    fault_type = filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = DetectorFault
        fields = []
        
   
class MaintenanceFilter(filters.FilterSet):
    maintenance_type = filters.CharFilter(lookup_expr='iexact')
    status = filters.CharFilter(lookup_expr='iexact')
    detector = filters.NumberFilter()
    detector__label = filters.CharFilter(lookup_expr='iexact')
    date_due_lte = filters.DateFilter(field_name='date_due', lookup_expr='lte')

    class Meta:
        model = Maintenance
        fields = []

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
        fields = []

class CylinderTypeFilter(filters.FilterSet):
    active = filters.BooleanFilter()

    class Meta:
        model = CylinderType
        fields = []
        
class CylinderFilter(filters.FilterSet):
    cylinder_number = filters.NumberFilter()
    serial = filters.CharFilter(lookup_expr='icontains')
    location__label = filters.CharFilter(lookup_expr='iexact')
    location = filters.NumberFilter()
    status = filters.CharFilter(lookup_expr='iexact')
    cylinder_type__part_number = filters.CharFilter(lookup_expr='icontains')
    expiry_date_lte = filters.DateFilter(field_name='expiry_date', lookup_expr='lte')
    expiry_date_gte = filters.DateFilter(field_name='expiry_date', lookup_expr='gte')

    class Meta:
        model = Cylinder
        fields = []
    
class SensorTypeFilter(filters.FilterSet):
    active = filters.BooleanFilter()
    part_number = filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = SensorType
        fields = []

class SensorFilter(filters.FilterSet):
    serial = filters.CharFilter(lookup_expr='icontains')
    status = filters.CharFilter(lookup_expr='iexact')
    sensor_type__part_number = filters.CharFilter(lookup_expr='icontains')
    detector = filters.NumberFilter()
    detector__label = filters.CharFilter(lookup_expr='iexact')
    detector__serial = filters.CharFilter(lookup_expr='icontains')
    warranty_date_lte = filters.CharFilter(field_name='warranty_date', lookup_expr='lte')
    warranty_date_gte = filters.CharFilter(field_name='warranty_date', lookup_expr='gte')
    end_date_lte = filters.CharFilter(field_name='end_date', lookup_expr='lte')
    end_date_gte = filters.CharFilter(field_name='end_date', lookup_expr='gte')
    class Meta:
        model = Sensor
        fields = ["sensor_type"]

class SensorSlotFilter(filters.FilterSet):
    sensor_type__part_number = filters.CharFilter(lookup_expr='icontains')
    detector = filters.NumberFilter()
    detector__label = filters.CharFilter(lookup_expr='iexact')
    detector__serial = filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = SensorSlot
        fields = []
    
class DetectorModelConfigurationFilter(filters.FilterSet):
    detector_model__model_name = filters.CharFilter(lookup_expr='iexact')
    detector_model__detector_type = filters.CharFilter(lookup_expr='iexact')
    detector_model = filters.NumberFilter()

    class Meta:
        model = DetectorModelConfiguration
        fields = []
class LocationDetectorSlotsFilter(filters.FilterSet):
    class Meta:
        model = LocationDetectorSlots
        fields = []

class CylinderFaultFilter(filters.FilterSet):
    cylinder__label = filters.CharFilter(lookup_expr='iexact')
    report_dt_gte = filters.DateFilter(field_name='report_dt', lookup_expr='gte')
    report_dt_lte = filters.DateFilter(field_name='report_dt', lookup_expr='lte')
    report_location__label = filters.CharFilter(lookup_expr='iexact')
    fault_type = filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = CylinderFault
        fields = []
