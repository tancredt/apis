from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, generics, status
from django_filters import rest_framework as filters
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils import timezone
from datetime import timedelta
from weasyprint import HTML

from .models import (
    Location,
    DetectorModel,
    Detector,
    SensorType,
    Sensor,
    SensorSlot,
    Maintenance,
    MaintenanceTask,
    DetectorFault,
    Cylinder,
    CylinderType,
    CylinderFault,
    LocationDetectorSlot,
    LocationType,
    Manufacturer,
    DetectorType,
    DetectorModelConfiguration,
    Supplier,
    DetectorStatus,
    MaintenanceType,
    MaintenanceTaskType,
    MaintenanceStatus,
    DetectorFaultType,
    CylinderUnit,
    CylinderVolume,
    CylinderStatus,
    SensorStatus,
    SensorGas
)

from .serializers import (
    LocationSerializer,
    DetectorModelSerializer,
    DetectorSerializer,
    DetectorModelConfigurationSerializer,
    MaintenanceSerializer,
    MaintenanceTaskSerializer,
    DetectorFaultSerializer,
    CylinderSerializer,
    CylinderTypeSerializer,
    CylinderFaultSerializer,
    LocationDetectorSlotSerializer,
    SensorTypeSerializer,
    SensorSerializer,
    SensorSlotSerializer,
    LocationTypeChoiceSerializer,
    ManufacturerChoiceSerializer,
    DetectorTypeChoiceSerializer,
    SupplierChoiceSerializer,
    DetectorStatusChoiceSerializer,
    MaintenanceTypeChoiceSerializer,
    MaintenanceTaskTypeChoiceSerializer,
    MaintenanceStatusChoiceSerializer,
    DetectorFaultTypeChoiceSerializer,
    CylinderGasChoiceSerializer,
    CylinderUnitChoiceSerializer,
    CylinderVolumeChoiceSerializer,
    CylinderStatusChoiceSerializer,
    SensorStatusChoiceSerializer,
    SensorGasChoiceSerializer,
    ChangeDetectorLocationSerializer,
    ChangeCylinderLocationSerializer

)

from .filters import (
    LocationFilter,
    DetectorModelFilter,
    DetectorFilter,
    DetectorFaultFilter,
    DetectorModelConfigurationFilter,
    MaintenanceFilter,
    MaintenanceTaskFilter,
    CylinderFilter,
    CylinderTypeFilter,
    CylinderFaultFilter,
    LocationDetectorSlotFilter,
    SensorTypeFilter,
    SensorFilter,
    SensorSlotFilter,
)

from .permissions import FrvUserRestrictedPermission

# Create your views here.
################---Choice Views---#################
class LocationTypeView(APIView):
    def get(self, request):
        choices = LocationType.choices
        choice_list = [{'value': value, 'label': label} for value, label in choices]
        serializer = LocationTypeChoiceSerializer(choice_list, many=True)
        return Response(serializer.data)

class ManufacturerView(APIView):
    def get(self, request):
        choices = Manufacturer.choices
        choice_list = [{'value': value, 'label': label} for value, label in choices]
        serializer = ManufacturerChoiceSerializer(choice_list, many=True)
        return Response(serializer.data)

class DetectorTypeView(APIView):
    def get(self, request):
        choices = DetectorType.choices
        choice_list = [{'value': value, 'label': label} for value, label in choices]
        serializer = DetectorTypeChoiceSerializer(choice_list, many=True)
        return Response(serializer.data)

class SupplierView(APIView):
    def get(self, request):
        choices = Supplier.choices
        choice_list = [{'value': value, 'label': label} for value, label in choices]
        serializer = SupplierChoiceSerializer(choice_list, many=True)
        return Response(serializer.data)

class DetectorStatusView(APIView):
    def get(self, request):
        choices = DetectorStatus.choices
        choice_list = [{'value': value, 'label': label} for value, label in choices]
        serializer = DetectorStatusChoiceSerializer(choice_list, many=True)
        return Response(serializer.data)

class CylinderStatusView(APIView):
    def get(self, request):
        choices = CylinderStatus.choices
        choice_list = [{'value': value, 'label': label} for value, label in choices]
        serializer = CylinderStatusChoiceSerializer(choice_list, many=True)
        return Response(serializer.data)

class SensorStatusView(APIView):
    def get(self, request):
        choices = SensorStatus.choices
        choice_list = [{'value': value, 'label': label} for value, label in choices]
        serializer = SensorStatusChoiceSerializer(choice_list, many=True)
        return Response(serializer.data)
    
class MaintenanceTypeView(APIView):
    def get(self, request):
        choices = MaintenanceType.choices
        choice_list = [{'value': value, 'label': label} for value, label in choices]
        serializer = MaintenanceTypeChoiceSerializer(choice_list, many=True)
        return Response(serializer.data)

class MaintenanceTaskTypeView(APIView):
    def get(self, request):
        choices = MaintenanceTaskType.choices
        choice_list = [{'value': value, 'label': label} for value, label in choices]
        serializer = MaintenanceTaskTypeChoiceSerializer(choice_list, many=True)
        return Response(serializer.data)

class MaintenanceStatusView(APIView):
    def get(self, request):
        choices = MaintenanceStatus.choices
        choice_list = [{'value': value, 'label': label} for value, label in choices]
        serializer = MaintenanceStatusChoiceSerializer(choice_list, many=True)
        return Response(serializer.data)

class DetectorFaultTypeView(APIView):
    def get(self, request):
        choices = DetectorFaultType.choices
        choice_list = [{'value': value, 'label': label} for value, label in choices]
        serializer = DetectorFaultTypeChoiceSerializer(choice_list, many=True)
        return Response(serializer.data)

class CylinderUnitView(APIView):
    def get(self, request):
        choices = CylinderUnit.choices
        choice_list = [{'value': value, 'label': label} for value, label in choices]
        serializer = CylinderUnitChoiceSerializer(choice_list, many=True)
        return Response(serializer.data)

class CylinderGasView(APIView):
    def get(self, request):
        choices = CylinderGas.choices
        choice_list = [{'value': value, 'label': label} for value, label in choices]
        serializer = CylinderGasChoiceSerializer(choice_list, many=True)
        return Response(serializer.data)

class CylinderVolumeView(APIView):
    def get(self, request):
        choices = CylinderVolume.choices
        choice_list = [{'value': value, 'label': label} for value, label in choices]
        serializer = CylinderVolumeChoiceSerializer(choice_list, many=True)
        return Response(serializer.data)

class SensorGasView(APIView):
    def get(self, request):
        choices = SensorGas.choices
        choice_list = [{'value': value, 'label': label} for value, label in choices]
        serializer = SensorGasChoiceSerializer(choice_list, many=True)
        return Response(serializer.data)

    
##################---Main Views---##########################
from rest_framework.permissions import IsAuthenticated

class LocationViewSet(viewsets.ModelViewSet):
    serializer_class = LocationSerializer
    queryset = Location.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = LocationFilter
    permission_classes = [IsAuthenticated, FrvUserRestrictedPermission]  # Require auth and restrict access for frvuser

class DetectorModelViewSet(viewsets.ModelViewSet):
    serializer_class = DetectorModelSerializer
    queryset = DetectorModel.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = DetectorModelFilter
    permission_classes = [IsAuthenticated, FrvUserRestrictedPermission]  # Require auth and restrict access for frvuser

class DetectorViewSet(viewsets.ModelViewSet):
    serializer_class = DetectorSerializer
    queryset = Detector.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = DetectorFilter
    permission_classes = [IsAuthenticated, FrvUserRestrictedPermission]  # Require auth and restrict access for frvuser

class MaintenanceViewSet(viewsets.ModelViewSet):
    serializer_class = MaintenanceSerializer
    queryset = Maintenance.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = MaintenanceFilter
    permission_classes = [IsAuthenticated, FrvUserRestrictedPermission]  # Require auth and restrict access for frvuser

class MaintenanceTaskViewSet(viewsets.ModelViewSet):
    serializer_class = MaintenanceTaskSerializer
    queryset = MaintenanceTask.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = MaintenanceTaskFilter
    permission_classes = [IsAuthenticated, FrvUserRestrictedPermission]  # Require auth and restrict access for frvuser

class DetectorFaultViewSet(viewsets.ModelViewSet):
    serializer_class = DetectorFaultSerializer
    queryset = DetectorFault.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = DetectorFaultFilter
    permission_classes = [IsAuthenticated, FrvUserRestrictedPermission]  # Require auth and restrict access for frvuser

class CylinderTypeViewSet(viewsets.ModelViewSet):
    serializer_class = CylinderTypeSerializer
    queryset = CylinderType.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = CylinderTypeFilter
    permission_classes = [IsAuthenticated, FrvUserRestrictedPermission]  # Require auth and restrict access for frvuser

class CylinderViewSet(viewsets.ModelViewSet):
    serializer_class = CylinderSerializer
    queryset = Cylinder.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = CylinderFilter
    permission_classes = [IsAuthenticated, FrvUserRestrictedPermission]  # Require auth and restrict access for frvuser

class SensorTypeViewSet(viewsets.ModelViewSet):
    serializer_class = SensorTypeSerializer
    queryset = SensorType.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = SensorTypeFilter
    permission_classes = [IsAuthenticated, FrvUserRestrictedPermission]  # Require auth and restrict access for frvuser

class SensorViewSet(viewsets.ModelViewSet):
    serializer_class = SensorSerializer
    queryset = Sensor.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = SensorFilter
    permission_classes = [IsAuthenticated, FrvUserRestrictedPermission]  # Require auth and restrict access for frvuser

class SensorSlotViewSet(viewsets.ModelViewSet):
    serializer_class = SensorSlotSerializer
    queryset = SensorSlot.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = SensorSlotFilter
    permission_classes = [IsAuthenticated, FrvUserRestrictedPermission]  # Require auth and restrict access for frvuser


from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Detector, Cylinder, Location


@api_view(['POST'])
@permission_classes([IsAuthenticated, FrvUserRestrictedPermission])
def change_detector_location(request):
    # Check if the user is 'frvuser' and only allow specific functionality
    if request.user.username == 'frvuser':
        # Validate that only allowed fields are being accessed
        serializer = ChangeDetectorLocationSerializer(data=request.data)
        if serializer.is_valid():
            detector_id = serializer.validated_data['detector_id']
            location_id = serializer.validated_data['location_id']

            detector = get_object_or_404(Detector, id=detector_id)
            location = get_object_or_404(Location, id=location_id)

            # Update the detector's location
            detector.location = location
            detector.save()

            return Response({
                'success': True,
                'message': 'Detector location updated successfully',
                'detector': {
                    'id': detector.id,
                    'label': detector.label,
                    'location': {
                        'id': location.id,
                        'label': location.label
                    }
                }
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'success': False,
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
    else:
        # For other authenticated users, allow broader functionality
        # Check if they have the necessary permissions
        if not request.user.has_perm('inventory.change_detector'):
            return Response({
                'error': 'Permission denied'
            }, status=status.HTTP_403_FORBIDDEN)
            
        serializer = ChangeDetectorLocationSerializer(data=request.data)
        if serializer.is_valid():
            detector_id = serializer.validated_data['detector_id']
            location_id = serializer.validated_data['location_id']

            detector = get_object_or_404(Detector, id=detector_id)
            location = get_object_or_404(Location, id=location_id)

            # Update the detector's location
            detector.location = location
            detector.save()

            return Response({
                'success': True,
                'message': 'Detector location updated successfully',
                'detector': {
                    'id': detector.id,
                    'label': detector.label,
                    'location': {
                        'id': location.id,
                        'label': location.label
                    }
                }
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'success': False,
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated, FrvUserRestrictedPermission])
def change_cylinder_location(request):
    # Check if the user is 'frvuser' and only allow specific functionality
    if request.user.username == 'frvuser':
        serializer = ChangeCylinderLocationSerializer(data=request.data)
        if serializer.is_valid():
            cylinder_id = serializer.validated_data['cylinder_id']
            location_id = serializer.validated_data['location_id']

            cylinder = get_object_or_404(Cylinder, id=cylinder_id)
            location = get_object_or_404(Location, id=location_id)

            # Update the cylinder's location
            cylinder.location = location
            cylinder.save()

            return Response({
                'success': True,
                'message': 'Cylinder location updated successfully',
                'cylinder': {
                    'id': cylinder.id,
                    'cylinder_number': cylinder.cylinder_number,
                    'location': {
                        'id': location.id,
                        'label': location.label
                    }
                }
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'success': False,
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
    else:
        # For other authenticated users, allow the full functionality
        # Check if they have the necessary permissions
        if not request.user.has_perm('inventory.change_cylinder'):
            return Response({
                'error': 'Permission denied'
            }, status=status.HTTP_403_FORBIDDEN)
            
        serializer = ChangeCylinderLocationSerializer(data=request.data)
        if serializer.is_valid():
            cylinder_id = serializer.validated_data['cylinder_id']
            location_id = serializer.validated_data['location_id']

            cylinder = get_object_or_404(Cylinder, id=cylinder_id)
            location = get_object_or_404(Location, id=location_id)

            # Update the cylinder's location
            cylinder.location = location
            cylinder.save()

            return Response({
                'success': True,
                'message': 'Cylinder location updated successfully',
                'cylinder': {
                    'id': cylinder.id,
                    'cylinder_number': cylinder.cylinder_number,
                    'location': {
                        'id': location.id,
                        'label': location.label
                    }
                }
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'success': False,
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
    
class DetectorModelConfigurationViewSet(viewsets.ModelViewSet):
    serializer_class = DetectorModelConfigurationSerializer
    queryset = DetectorModelConfiguration.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = DetectorModelConfigurationFilter
    permission_classes = [IsAuthenticated, FrvUserRestrictedPermission]  # Require auth and restrict access for frvuser

class LocationDetectorSlotViewSet(viewsets.ModelViewSet):
    serializer_class = LocationDetectorSlotSerializer
    queryset = LocationDetectorSlot.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = LocationDetectorSlotFilter
    permission_classes = [IsAuthenticated, FrvUserRestrictedPermission]  # Require auth and restrict access for frvuser

class CylinderFaultViewSet(viewsets.ModelViewSet):
    serializer_class = CylinderFaultSerializer
    queryset = CylinderFault.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = CylinderFaultFilter
    permission_classes = [IsAuthenticated, FrvUserRestrictedPermission]  # Require auth and restrict access for frvuser


# ============== PDF Report Views ==============

def get_date_context():
    """Get common date context for PDF templates."""
    today = timezone.now().date()
    eight_weeks = today + timedelta(weeks=8)
    return {'today': today, 'eight_weeks': eight_weeks}


def detectors_pdf(request):
    """Generate PDF report of all detectors."""
    detectors = Detector.objects.select_related(
        'detector_model', 'location', 'configuration'
    ).order_by('label')
    
    context = {
        'detectors': detectors,
        **get_date_context()
    }
    
    html_string = render_to_string('inventory/pdf/detectors.html', context)
    pdf = HTML(string=html_string, base_url=request.build_absolute_uri('/')).write_pdf()
    
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="detectors.pdf"'
    return response


def sensors_pdf(request):
    """Generate PDF report of all sensors."""
    sensors = Sensor.objects.select_related(
        'sensor_type', 'detector'
    ).order_by('sensor_type__part_number', 'serial')
    
    context = {
        'sensors': sensors,
        **get_date_context()
    }
    
    html_string = render_to_string('inventory/pdf/sensors.html', context)
    pdf = HTML(string=html_string, base_url=request.build_absolute_uri('/')).write_pdf()
    
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="sensors.pdf"'
    return response


def cylinders_pdf(request):
    """Generate PDF report of all calibration cylinders."""
    cylinders = Cylinder.objects.select_related(
        'cylinder_type', 'location', 'detector'
    ).order_by('cylinder_number')
    
    context = {
        'cylinders': cylinders,
        **get_date_context()
    }
    
    html_string = render_to_string('inventory/pdf/cylinders.html', context)
    pdf = HTML(string=html_string, base_url=request.build_absolute_uri('/')).write_pdf()
    
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="cylinders.pdf"'
    return response


def maintenance_pdf(request):
    """Generate PDF report of all maintenance records."""
    maintenances = Maintenance.objects.select_related(
        'detector'
    ).prefetch_related('tasks').order_by('-date_due')
    
    context = {
        'maintenances': maintenances,
        **get_date_context()
    }
    
    html_string = render_to_string('inventory/pdf/maintenance.html', context)
    pdf = HTML(string=html_string, base_url=request.build_absolute_uri('/')).write_pdf()
    
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="maintenance.pdf"'
    return response


def faults_pdf(request):
    """Generate PDF report of all fault reports."""
    faults = DetectorFault.objects.select_related(
        'detector', 'report_location'
    ).order_by('-report_dt')
    
    context = {
        'faults': faults,
        **get_date_context()
    }
    
    html_string = render_to_string('inventory/pdf/faults.html', context)
    pdf = HTML(string=html_string, base_url=request.build_absolute_uri('/')).write_pdf()
    
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="faults.pdf"'
    return response


def detector_detail_pdf(request, detector_id):
    """Generate PDF report for a single detector with all details."""
    from django.shortcuts import get_object_or_404
    
    detector = get_object_or_404(
        Detector.objects.select_related(
            'detector_model', 'location', 'configuration'
        ),
        id=detector_id
    )
    
    sensor_slots = SensorSlot.objects.select_related(
        'sensor__sensor_type'
    ).filter(detector=detector).order_by('sensorgas')
    
    maintenances = Maintenance.objects.filter(detector=detector).order_by('-date_due')
    faults = DetectorFault.objects.filter(detector=detector).order_by('-report_dt')
    
    context = {
        'detector': detector,
        'sensor_slots': sensor_slots,
        'maintenances': maintenances,
        'faults': faults,
        **get_date_context()
    }
    
    html_string = render_to_string('inventory/pdf/detector_detail.html', context)
    pdf = HTML(string=html_string, base_url=request.build_absolute_uri('/')).write_pdf()
    
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="detector_{detector.label}.pdf"'
    return response
