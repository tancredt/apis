from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from django.db.models import Q

from .models import Incident, DetectorSite, ReadingType, Reading, DetectorValidation, DetectorSiteValidation, Gas, Units
from .serializers import (
    IncidentSerializer,
    DetectorSiteSerializer,
    ReadingTypeSerializer,
    ReadingSerializer,
    ReadingListSerializer,
    DetectorValidationSerializer,
    DetectorSiteValidationSerializer,
    GasChoiceSerializer,
    UnitsChoiceSerializer,
)
from .filters import (
    IncidentFilter,
    DetectorSiteFilter,
    ReadingTypeFilter,
    ReadingFilter,
    DetectorValidationFilter,
    DetectorSiteValidationFilter,
)


# ============== Choice Views ==============
class GasView(APIView):
    """Return list of available gas choices."""
    # No permission classes - matches inventory/views.py choice views

    def get(self, request):
        choices = Gas.choices
        choice_list = [{'value': value, 'label': label} for value, label in choices]
        serializer = GasChoiceSerializer(choice_list, many=True)
        return Response(serializer.data)


class UnitsView(APIView):
    """Return list of available units choices."""
    # No permission classes - matches inventory/views.py choice views

    def get(self, request):
        choices = Units.choices
        choice_list = [{'value': value, 'label': label} for value, label in choices]
        serializer = UnitsChoiceSerializer(choice_list, many=True)
        return Response(serializer.data)


# ============== Main ViewSets ==============
class IncidentViewSet(viewsets.ModelViewSet):
    """ViewSet for Incident CRUD operations."""
    serializer_class = IncidentSerializer
    queryset = Incident.objects.all()
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    filterset_fields = ['label', 'suburb', 'start_date']

    def get_queryset(self):
        queryset = Incident.objects.all()
        
        # Apply filtering
        label = self.request.query_params.get('label', None)
        suburb = self.request.query_params.get('suburb', None)
        start_date_gte = self.request.query_params.get('start_date_gte', None)
        start_date_lte = self.request.query_params.get('start_date_lte', None)
        
        if label:
            queryset = queryset.filter(label__icontains=label)
        if suburb:
            queryset = queryset.filter(suburb__icontains=suburb)
        if start_date_gte:
            queryset = queryset.filter(start_date__gte=start_date_gte)
        if start_date_lte:
            queryset = queryset.filter(start_date__lte=start_date_lte)
        
        # Sorting
        sort_key = self.request.query_params.get('sort_key', 'start_date')
        sort_direction = self.request.query_params.get('sort_direction', 'desc')
        
        valid_sort_fields = ['label', 'start_date', 'suburb']
        if sort_key in valid_sort_fields:
            if sort_direction.lower() == 'desc':
                queryset = queryset.order_by(f'-{sort_key}')
            else:
                queryset = queryset.order_by(sort_key)
        
        return queryset


class DetectorSiteViewSet(viewsets.ModelViewSet):
    """ViewSet for DetectorSite CRUD operations."""
    serializer_class = DetectorSiteSerializer
    queryset = DetectorSite.objects.all()
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    filterset_fields = ['incident', 'label']

    def get_queryset(self):
        queryset = DetectorSite.objects.select_related('incident').all()
        
        # Apply filtering
        incident = self.request.query_params.get('incident', None)
        label = self.request.query_params.get('label', None)
        
        if incident:
            queryset = queryset.filter(incident_id=incident)
        if label:
            queryset = queryset.filter(label__iexact=label)
        
        # Sorting
        sort_key = self.request.query_params.get('sort_key', 'label')
        sort_direction = self.request.query_params.get('sort_direction', 'asc')
        
        valid_sort_fields = ['label', 'incident']
        if sort_key in valid_sort_fields:
            if sort_direction.lower() == 'desc':
                queryset = queryset.order_by(f'-{sort_key}')
            else:
                queryset = queryset.order_by(sort_key)
        
        return queryset


class ReadingTypeViewSet(viewsets.ModelViewSet):
    """ViewSet for ReadingType CRUD operations."""
    serializer_class = ReadingTypeSerializer
    queryset = ReadingType.objects.all()
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    filterset_fields = ['gas', 'units']

    def get_queryset(self):
        queryset = ReadingType.objects.all()
        
        # Apply filtering
        gas = self.request.query_params.get('gas', None)
        units = self.request.query_params.get('units', None)
        
        if gas:
            queryset = queryset.filter(gas=gas)
        if units:
            queryset = queryset.filter(units=units)
        
        return queryset


class ReadingViewSet(viewsets.ModelViewSet):
    """ViewSet for Reading CRUD operations."""
    serializer_class = ReadingSerializer
    queryset = Reading.objects.all()
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    filterset_fields = ['detector', 'reading_type', 'is_valid']

    def get_queryset(self):
        queryset = Reading.objects.select_related(
            'detector', 'reading_type', 'detector_site'
        ).all()
        
        # Apply filtering
        detector = self.request.query_params.get('detector', None)
        detector_label = self.request.query_params.get('detector__label', None)
        detector_serial = self.request.query_params.get('detector__serial', None)
        reading_type = self.request.query_params.get('reading_type', None)
        reading_type_gas = self.request.query_params.get('reading_type__gas', None)
        reading_type_units = self.request.query_params.get('reading_type__units', None)
        dt_gte = self.request.query_params.get('dt_gte', None)
        dt_lte = self.request.query_params.get('dt_lte', None)
        is_valid = self.request.query_params.get('is_valid', None)
        detector_site = self.request.query_params.get('detector_site', None)
        search = self.request.query_params.get('search', None)
        
        if detector:
            queryset = queryset.filter(detector_id=detector)
        if detector_label:
            queryset = queryset.filter(detector__label__iexact=detector_label)
        if detector_serial:
            queryset = queryset.filter(detector__serial__icontains=detector_serial)
        if reading_type:
            queryset = queryset.filter(reading_type_id=reading_type)
        if reading_type_gas:
            queryset = queryset.filter(reading_type__gas=reading_type_gas)
        if reading_type_units:
            queryset = queryset.filter(reading_type__units=reading_type_units)
        if dt_gte:
            queryset = queryset.filter(dt__gte=dt_gte)
        if dt_lte:
            queryset = queryset.filter(dt__lte=dt_lte)
        if is_valid is not None:
            queryset = queryset.filter(is_valid=is_valid.lower() == 'true')
        if detector_site:
            queryset = queryset.filter(detector_site_id=detector_site)
        if search:
            queryset = queryset.filter(
                Q(detector__label__icontains=search) |
                Q(detector__serial__icontains=search)
            )
        
        # Sorting
        sort_key = self.request.query_params.get('sort_key', 'dt')
        sort_direction = self.request.query_params.get('sort_direction', 'desc')
        
        valid_sort_fields = ['dt', 'value', 'detector__label', 'reading_type__gas', 'is_valid']
        if sort_key in valid_sort_fields:
            if sort_direction.lower() == 'desc':
                queryset = queryset.order_by(f'-{sort_key}')
            else:
                queryset = queryset.order_by(sort_key)
        
        return queryset

    def list(self, request, *args, **kwargs):
        """Override list to use ReadingListSerializer for detailed output."""
        queryset = self.filter_queryset(self.get_queryset())
        serializer = ReadingListSerializer(queryset, many=True)
        return Response(serializer.data)


# ============== Detector Validation ViewSets ==============
class DetectorValidationViewSet(viewsets.ModelViewSet):
    """ViewSet for DetectorValidation CRUD operations."""
    serializer_class = DetectorValidationSerializer
    queryset = DetectorValidation.objects.all()
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    filterset_fields = ['detector', 'reason']

    def get_queryset(self):
        queryset = DetectorValidation.objects.select_related('detector').all()
        
        # Apply filtering
        detector = self.request.query_params.get('detector', None)
        detector_label = self.request.query_params.get('detector__label', None)
        start_dt_gte = self.request.query_params.get('start_dt_gte', None)
        start_dt_lte = self.request.query_params.get('start_dt_lte', None)
        end_dt_gte = self.request.query_params.get('end_dt_gte', None)
        end_dt_lte = self.request.query_params.get('end_dt_lte', None)
        reason = self.request.query_params.get('reason', None)
        
        if detector:
            queryset = queryset.filter(detector_id=detector)
        if detector_label:
            queryset = queryset.filter(detector__label__iexact=detector_label)
        if start_dt_gte:
            queryset = queryset.filter(start_dt__gte=start_dt_gte)
        if start_dt_lte:
            queryset = queryset.filter(start_dt__lte=start_dt_lte)
        if end_dt_gte:
            queryset = queryset.filter(end_dt__gte=end_dt_gte)
        if end_dt_lte:
            queryset = queryset.filter(end_dt__lte=end_dt_lte)
        if reason:
            queryset = queryset.filter(reason__icontains=reason)
        
        # Sorting
        sort_key = self.request.query_params.get('sort_key', 'start_dt')
        sort_direction = self.request.query_params.get('sort_direction', 'desc')
        
        valid_sort_fields = ['start_dt', 'end_dt', 'reason', 'detector__label']
        if sort_key in valid_sort_fields:
            if sort_direction.lower() == 'desc':
                queryset = queryset.order_by(f'-{sort_key}')
            else:
                queryset = queryset.order_by(sort_key)
        
        return queryset


# ============== Detector Site Validation ViewSets ==============
class DetectorSiteValidationViewSet(viewsets.ModelViewSet):
    """ViewSet for DetectorSiteValidation CRUD operations."""
    serializer_class = DetectorSiteValidationSerializer
    queryset = DetectorSiteValidation.objects.all()
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    filterset_fields = ['detector_site', 'reason']

    def get_queryset(self):
        queryset = DetectorSiteValidation.objects.select_related('detector_site').all()
        
        # Apply filtering
        detector_site = self.request.query_params.get('detector_site', None)
        detector_site_label = self.request.query_params.get('detector_site__label', None)
        start_dt_gte = self.request.query_params.get('start_dt_gte', None)
        start_dt_lte = self.request.query_params.get('start_dt_lte', None)
        end_dt_gte = self.request.query_params.get('end_dt_gte', None)
        end_dt_lte = self.request.query_params.get('end_dt_lte', None)
        reason = self.request.query_params.get('reason', None)
        
        if detector_site:
            queryset = queryset.filter(detector_site_id=detector_site)
        if detector_site_label:
            queryset = queryset.filter(detector_site__label__iexact=detector_site_label)
        if start_dt_gte:
            queryset = queryset.filter(start_dt__gte=start_dt_gte)
        if start_dt_lte:
            queryset = queryset.filter(start_dt__lte=start_dt_lte)
        if end_dt_gte:
            queryset = queryset.filter(end_dt__gte=end_dt_gte)
        if end_dt_lte:
            queryset = queryset.filter(end_dt__lte=end_dt_lte)
        if reason:
            queryset = queryset.filter(reason__icontains=reason)
        
        # Sorting
        sort_key = self.request.query_params.get('sort_key', 'start_dt')
        sort_direction = self.request.query_params.get('sort_direction', 'desc')
        
        valid_sort_fields = ['start_dt', 'end_dt', 'reason', 'detector_site__label']
        if sort_key in valid_sort_fields:
            if sort_direction.lower() == 'desc':
                queryset = queryset.order_by(f'-{sort_key}')
            else:
                queryset = queryset.order_by(sort_key)
        
        return queryset
