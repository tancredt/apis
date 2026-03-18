from rest_framework import serializers
from .models import Gas, Units, Incident, DetectorSite, ReadingType, Reading, Validation


###################---Choice Serializers---###################
class GasChoiceSerializer(serializers.Serializer):
    value = serializers.CharField()
    label = serializers.CharField()


class UnitsChoiceSerializer(serializers.Serializer):
    value = serializers.CharField()
    label = serializers.CharField()


#################---Main Serializers---#####################
class IncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incident
        fields = "__all__"
        read_only_fields = []

    def validate(self, attrs):
        # Validate that latitude is within valid range if provided
        latitude = attrs.get('latitude')
        if latitude is not None and (latitude < -90 or latitude > 90):
            raise serializers.ValidationError({'latitude': ['Latitude must be between -90 and 90.']})

        # Validate that longitude is within valid range if provided
        longitude = attrs.get('longitude')
        if longitude is not None and (longitude < -180 or longitude > 180):
            raise serializers.ValidationError({'longitude': ['Longitude must be between -180 and 180.']})

        return attrs


class DetectorSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetectorSite
        fields = "__all__"
        read_only_fields = []

    def validate(self, attrs):
        # Validate that latitude is within valid range if provided
        latitude = attrs.get('latitude')
        if latitude is not None and (latitude < -90 or latitude > 90):
            raise serializers.ValidationError({'latitude': ['Latitude must be between -90 and 90.']})

        # Validate that longitude is within valid range if provided
        longitude = attrs.get('longitude')
        if longitude is not None and (longitude < -180 or longitude > 180):
            raise serializers.ValidationError({'longitude': ['Longitude must be between -180 and 180.']})

        return attrs


class ReadingTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadingType
        fields = "__all__"
        read_only_fields = []


class ReadingSerializer(serializers.ModelSerializer):
    dt = serializers.DateTimeField()

    class Meta:
        model = Reading
        fields = "__all__"
        read_only_fields = []

    def validate(self, attrs):
        value = attrs.get('value')
        if value is not None and value < 0:
            raise serializers.ValidationError({'value': ['Value cannot be negative.']})

        # Validate that dt is not in the future
        dt = attrs.get('dt')
        if dt:
            from django.utils import timezone
            if dt > timezone.now():
                raise serializers.ValidationError({'dt': ['Date/time cannot be in the future.']})

        return attrs


class ReadingListSerializer(serializers.ModelSerializer):
    """Reading serializer with nested related object details for list views."""
    detector_label = serializers.CharField(source='detector.label', read_only=True)
    detector_serial = serializers.CharField(source='detector.serial', read_only=True)
    gas = serializers.CharField(source='reading_type.gas', read_only=True)
    units = serializers.CharField(source='reading_type.units', read_only=True)
    site_label = serializers.CharField(source='detector_site.label', read_only=True)

    class Meta:
        model = Reading
        fields = [
            'id', 'detector', 'detector_label', 'detector_serial',
            'reading_type', 'gas', 'units', 'value', 'dt',
            'detector_site', 'site_label', 'is_valid'
        ]


class ValidationSerializer(serializers.ModelSerializer):
    start_dt = serializers.DateTimeField()
    end_dt = serializers.DateTimeField()

    class Meta:
        model = Validation
        fields = "__all__"
        read_only_fields = []

    def validate(self, attrs):
        start_dt = attrs.get('start_dt')
        end_dt = attrs.get('end_dt')

        if start_dt and end_dt:
            if end_dt <= start_dt:
                raise serializers.ValidationError({
                    'end_dt': ['End date/time must be after start date/time.']
                })

        return attrs
