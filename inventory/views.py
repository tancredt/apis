from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, generics
from django_filters import rest_framework as filters

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
    LocationDetectorSlots,
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
    LocationDetectorSlotsSerializer,
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
    SensorGasChoiceSerializer
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
    LocationDetectorSlotsFilter,
    SensorTypeFilter,
    SensorFilter,
    SensorSlotFilter,
)

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
class LocationViewSet(viewsets.ModelViewSet):
    serializer_class = LocationSerializer
    queryset = Location.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = LocationFilter

class DetectorModelViewSet(viewsets.ModelViewSet):
    serializer_class = DetectorModelSerializer
    queryset = DetectorModel.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = DetectorModelFilter
        
class DetectorViewSet(viewsets.ModelViewSet):
    serializer_class = DetectorSerializer
    queryset = Detector.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = DetectorFilter
    
class MaintenanceViewSet(viewsets.ModelViewSet):
    serializer_class = MaintenanceSerializer
    queryset = Maintenance.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = MaintenanceFilter

class MaintenanceTaskViewSet(viewsets.ModelViewSet):
    serializer_class = MaintenanceTaskSerializer
    queryset = MaintenanceTask.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = MaintenanceTaskFilter
    
class DetectorFaultViewSet(viewsets.ModelViewSet):
    serializer_class = DetectorFaultSerializer
    queryset = DetectorFault.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = DetectorFaultFilter
    
class CylinderTypeViewSet(viewsets.ModelViewSet):
    serializer_class = CylinderTypeSerializer
    queryset = CylinderType.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = CylinderTypeFilter
    
class CylinderViewSet(viewsets.ModelViewSet):
    serializer_class = CylinderSerializer
    queryset = Cylinder.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = CylinderFilter
    
class SensorTypeViewSet(viewsets.ModelViewSet):
    serializer_class = SensorTypeSerializer
    queryset = SensorType.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = SensorTypeFilter

class SensorViewSet(viewsets.ModelViewSet):
    serializer_class = SensorSerializer
    queryset = Sensor.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = SensorFilter

class SensorSlotViewSet(viewsets.ModelViewSet):
    serializer_class = SensorSlotSerializer
    queryset = SensorSlot.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = SensorSlotFilter


from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Detector, Cylinder, Location


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_detector_location(request):
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
@permission_classes([IsAuthenticated])
def change_cylinder_location(request):
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
    
class LocationDetectorSlotsViewSet(viewsets.ModelViewSet):
    serializer_class = LocationDetectorSlotsSerializer
    queryset = LocationDetectorSlots.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = LocationDetectorSlotsFilter

class CylinderFaultViewSet(viewsets.ModelViewSet):
    serializer_class = CylinderFaultSerializer
    queryset = CylinderFault.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = CylinderFaultFilter
