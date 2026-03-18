from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from django_filters import rest_framework as filters
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q, Avg, Max, Min, Count

from .models import Incident, DetectorSite, ReadingType, Reading, Validation, Gas, Units
from .serializers import (
    IncidentSerializer,
    DetectorSiteSerializer,
    ReadingTypeSerializer,
    ReadingSerializer,
    ReadingListSerializer,
    ValidationSerializer,
    GasChoiceSerializer,
    UnitsChoiceSerializer,
)


# ============== Choice Views ==============
class GasView(APIView):
    """Return list of available gas choices."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        choices = Gas.choices
        choice_list = [{'value': value, 'label': label} for value, label in choices]
        serializer = GasChoiceSerializer(choice_list, many=True)
        return Response(serializer.data)


class UnitsView(APIView):
    """Return list of available units choices."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        choices = Units.choices
        choice_list = [{'value': value, 'label': label} for value, label in choices]
        serializer = UnitsChoiceSerializer(choice_list, many=True)
        return Response(serializer.data)


# ============== Filter Classes ==============
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
            Q(detector__label__icontains=value) |
            Q(detector__serial__icontains=value)
        )

    class Meta:
        model = Reading
        fields = [
            'detector', 'detector__label', 'detector__serial',
            'reading_type', 'reading_type__gas', 'reading_type__units',
            'dt_gte', 'dt_lte', 'is_valid', 'detector_site', 'search'
        ]


class ValidationFilter(filters.FilterSet):
    start_dt_gte = filters.DateTimeFilter(field_name='start_dt', lookup_expr='gte')
    start_dt_lte = filters.DateTimeFilter(field_name='start_dt', lookup_expr='lte')
    end_dt_gte = filters.DateTimeFilter(field_name='end_dt', lookup_expr='gte')
    end_dt_lte = filters.DateTimeFilter(field_name='end_dt', lookup_expr='lte')

    class Meta:
        model = Validation
        fields = ['start_dt_gte', 'start_dt_lte', 'end_dt_gte', 'end_dt_lte']


# ============== Main API Views ==============
class IncidentListCreateView(APIView):
    """List all incidents or create a new incident."""
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

    def get(self, request):
        queryset = Incident.objects.all()
        
        # Apply filters
        filter_set = IncidentFilter(request.GET, queryset=queryset)
        incidents = filter_set.qs
        
        # Sorting
        sort_key = request.GET.get('sort_key', 'start_date')
        sort_direction = request.GET.get('sort_direction', 'desc')
        
        valid_sort_fields = ['label', 'start_date', 'suburb']
        if sort_key in valid_sort_fields:
            if sort_direction.lower() == 'desc':
                incidents = incidents.order_by(f'-{sort_key}')
            else:
                incidents = incidents.order_by(sort_key)
        
        serializer = IncidentSerializer(incidents, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = IncidentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IncidentDetailView(APIView):
    """Retrieve, update, or delete a single incident."""
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

    def get_object(self, pk):
        try:
            return Incident.objects.get(pk=pk)
        except Incident.DoesNotExist:
            return None

    def get(self, request, pk):
        incident = self.get_object(pk)
        if incident is None:
            return Response({'error': 'Incident not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = IncidentSerializer(incident)
        return Response(serializer.data)

    def put(self, request, pk):
        incident = self.get_object(pk)
        if incident is None:
            return Response({'error': 'Incident not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = IncidentSerializer(incident, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        incident = self.get_object(pk)
        if incident is None:
            return Response({'error': 'Incident not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = IncidentSerializer(incident, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        incident = self.get_object(pk)
        if incident is None:
            return Response({'error': 'Incident not found'}, status=status.HTTP_404_NOT_FOUND)
        incident.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DetectorSiteListCreateView(APIView):
    """List all detector sites or create a new detector site."""
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

    def get(self, request):
        queryset = DetectorSite.objects.select_related('incident').all()
        
        # Apply filters
        filter_set = DetectorSiteFilter(request.GET, queryset=queryset)
        sites = filter_set.qs
        
        # Sorting
        sort_key = request.GET.get('sort_key', 'label')
        sort_direction = request.GET.get('sort_direction', 'asc')
        
        valid_sort_fields = ['label', 'incident']
        if sort_key in valid_sort_fields:
            if sort_direction.lower() == 'desc':
                sites = sites.order_by(f'-{sort_key}')
            else:
                sites = sites.order_by(sort_key)
        
        serializer = DetectorSiteSerializer(sites, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DetectorSiteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DetectorSiteDetailView(APIView):
    """Retrieve, update, or delete a single detector site."""
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

    def get_object(self, pk):
        try:
            return DetectorSite.objects.get(pk=pk)
        except DetectorSite.DoesNotExist:
            return None

    def get(self, request, pk):
        site = self.get_object(pk)
        if site is None:
            return Response({'error': 'Detector site not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = DetectorSiteSerializer(site)
        return Response(serializer.data)

    def put(self, request, pk):
        site = self.get_object(pk)
        if site is None:
            return Response({'error': 'Detector site not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = DetectorSiteSerializer(site, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        site = self.get_object(pk)
        if site is None:
            return Response({'error': 'Detector site not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = DetectorSiteSerializer(site, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        site = self.get_object(pk)
        if site is None:
            return Response({'error': 'Detector site not found'}, status=status.HTTP_404_NOT_FOUND)
        site.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReadingTypeListCreateView(APIView):
    """List all reading types or create a new reading type."""
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

    def get(self, request):
        queryset = ReadingType.objects.all()
        
        # Apply filters
        filter_set = ReadingTypeFilter(request.GET, queryset=queryset)
        reading_types = filter_set.qs
        
        serializer = ReadingTypeSerializer(reading_types, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ReadingTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReadingTypeDetailView(APIView):
    """Retrieve, update, or delete a single reading type."""
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

    def get_object(self, pk):
        try:
            return ReadingType.objects.get(pk=pk)
        except ReadingType.DoesNotExist:
            return None

    def get(self, request, pk):
        reading_type = self.get_object(pk)
        if reading_type is None:
            return Response({'error': 'Reading type not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ReadingTypeSerializer(reading_type)
        return Response(serializer.data)

    def put(self, request, pk):
        reading_type = self.get_object(pk)
        if reading_type is None:
            return Response({'error': 'Reading type not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ReadingTypeSerializer(reading_type, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        reading_type = self.get_object(pk)
        if reading_type is None:
            return Response({'error': 'Reading type not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ReadingTypeSerializer(reading_type, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        reading_type = self.get_object(pk)
        if reading_type is None:
            return Response({'error': 'Reading type not found'}, status=status.HTTP_404_NOT_FOUND)
        reading_type.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReadingListCreateView(APIView):
    """List all readings or create a new reading."""
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

    def get(self, request):
        queryset = Reading.objects.select_related(
            'detector', 'reading_type', 'detector_site'
        ).all()
        
        # Apply filters
        filter_set = ReadingFilter(request.GET, queryset=queryset)
        readings = filter_set.qs
        
        # Sorting
        sort_key = request.GET.get('sort_key', 'dt')
        sort_direction = request.GET.get('sort_direction', 'desc')
        
        valid_sort_fields = ['dt', 'value', 'detector__label', 'reading_type__gas', 'is_valid']
        if sort_key in valid_sort_fields:
            if sort_direction.lower() == 'desc':
                readings = readings.order_by(f'-{sort_key}')
            else:
                readings = readings.order_by(sort_key)
        
        # Use list serializer for detailed output
        serializer = ReadingListSerializer(readings, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ReadingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReadingDetailView(APIView):
    """Retrieve, update, or delete a single reading."""
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

    def get_object(self, pk):
        try:
            return Reading.objects.select_related(
                'detector', 'reading_type', 'detector_site'
            ).get(pk=pk)
        except Reading.DoesNotExist:
            return None

    def get(self, request, pk):
        reading = self.get_object(pk)
        if reading is None:
            return Response({'error': 'Reading not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ReadingSerializer(reading)
        return Response(serializer.data)

    def put(self, request, pk):
        reading = self.get_object(pk)
        if reading is None:
            return Response({'error': 'Reading not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ReadingSerializer(reading, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        reading = self.get_object(pk)
        if reading is None:
            return Response({'error': 'Reading not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ReadingSerializer(reading, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        reading = self.get_object(pk)
        if reading is None:
            return Response({'error': 'Reading not found'}, status=status.HTTP_404_NOT_FOUND)
        reading.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReadingStatsView(APIView):
    """Get statistics for readings within a time range."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        detector = request.GET.get('detector')
        gas = request.GET.get('gas')
        start_dt = request.GET.get('start_dt')
        end_dt = request.GET.get('end_dt')
        
        queryset = Reading.objects.filter(is_valid=True)
        
        if detector:
            queryset = queryset.filter(detector_id=detector)
        if gas:
            queryset = queryset.filter(reading_type__gas=gas)
        if start_dt:
            queryset = queryset.filter(dt__gte=start_dt)
        if end_dt:
            queryset = queryset.filter(dt__lte=end_dt)
        
        if not queryset.exists():
            return Response({
                'count': 0,
                'average': None,
                'min': None,
                'max': None,
                'latest': None
            })
        
        stats = queryset.aggregate(
            count=Count('id'),
            average=Avg('value'),
            min=Min('value'),
            max=Max('value')
        )
        
        latest_reading = queryset.order_by('-dt').first()
        
        return Response({
            'count': stats['count'],
            'average': stats['average'],
            'min': stats['min'],
            'max': stats['max'],
            'latest': ReadingSerializer(latest_reading).data if latest_reading else None
        })


class ValidationListCreateView(APIView):
    """List all validations or create a new validation."""
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

    def get(self, request):
        queryset = Validation.objects.all()
        
        # Apply filters
        filter_set = ValidationFilter(request.GET, queryset=queryset)
        validations = filter_set.qs
        
        # Sorting
        sort_key = request.GET.get('sort_key', 'start_dt')
        sort_direction = request.GET.get('sort_direction', 'desc')
        
        valid_sort_fields = ['start_dt', 'end_dt', 'reason']
        if sort_key in valid_sort_fields:
            if sort_direction.lower() == 'desc':
                validations = validations.order_by(f'-{sort_key}')
            else:
                validations = validations.order_by(sort_key)
        
        serializer = ValidationSerializer(validations, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ValidationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ValidationDetailView(APIView):
    """Retrieve, update, or delete a single validation."""
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

    def get_object(self, pk):
        try:
            return Validation.objects.get(pk=pk)
        except Validation.DoesNotExist:
            return None

    def get(self, request, pk):
        validation = self.get_object(pk)
        if validation is None:
            return Response({'error': 'Validation not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ValidationSerializer(validation)
        return Response(serializer.data)

    def put(self, request, pk):
        validation = self.get_object(pk)
        if validation is None:
            return Response({'error': 'Validation not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ValidationSerializer(validation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        validation = self.get_object(pk)
        if validation is None:
            return Response({'error': 'Validation not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ValidationSerializer(validation, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        validation = self.get_object(pk)
        if validation is None:
            return Response({'error': 'Validation not found'}, status=status.HTTP_404_NOT_FOUND)
        validation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ActiveValidationView(APIView):
    """Get currently active validation (now is within start_dt and end_dt)."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        now = timezone.now()
        validation = Validation.objects.filter(
            start_dt__lte=now,
            end_dt__gte=now
        ).order_by('-start_dt').first()
        
        if validation is None:
            return Response({'active': False, 'validation': None})
        
        return Response({
            'active': True,
            'validation': ValidationSerializer(validation).data
        })
