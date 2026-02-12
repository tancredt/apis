from rest_framework import serializers

from .models import (
    Location,
    DetectorModel,
    Detector,
    DetectorModelConfiguration,
    LocationDetectorSlots,
    Maintenance,
    MaintenanceTask,
    DetectorFault,
    CylinderType,
    Cylinder,
    CylinderFault,
    LocationType,
    Manufacturer,
    DetectorType,
    Supplier,
    DetectorStatus,
    MaintenanceType,
    MaintenanceTaskType,
    MaintenanceStatus,
    DetectorFaultType,
    CylinderGas,
    CylinderUnit,
    CylinderStatus,
    SensorType,
    Sensor,
    SensorStatus,
    SensorSlot
)

###################---Choice Serializers---###################
class LocationTypeChoiceSerializer(serializers.Serializer):
    value = serializers.CharField()
    label = serializers.CharField()
    
class ManufacturerChoiceSerializer(serializers.Serializer):
    value = serializers.CharField()
    label = serializers.CharField()

class DetectorTypeChoiceSerializer(serializers.Serializer):
    value = serializers.CharField()
    label = serializers.CharField()

class SupplierChoiceSerializer(serializers.Serializer):
    value = serializers.CharField()
    label = serializers.CharField()

class DetectorStatusChoiceSerializer(serializers.Serializer):
    value = serializers.CharField()
    label = serializers.CharField()

class MaintenanceTypeChoiceSerializer(serializers.Serializer):
    value = serializers.CharField()
    label = serializers.CharField()

class MaintenanceTaskTypeChoiceSerializer(serializers.Serializer):
    value = serializers.CharField()
    label = serializers.CharField()

class MaintenanceStatusChoiceSerializer(serializers.Serializer):
    value = serializers.CharField()
    label = serializers.CharField()

class DetectorFaultTypeChoiceSerializer(serializers.Serializer):
    value = serializers.CharField()
    label = serializers.CharField()

class CylinderGasChoiceSerializer(serializers.Serializer):
    value = serializers.CharField()
    label = serializers.CharField()

class CylinderVolumeChoiceSerializer(serializers.Serializer):
    value = serializers.CharField()
    label = serializers.CharField()

class CylinderUnitChoiceSerializer(serializers.Serializer):
    value = serializers.CharField()
    label = serializers.CharField()

class CylinderStatusChoiceSerializer(serializers.Serializer):
    value = serializers.CharField()
    label = serializers.CharField()

class SensorStatusChoiceSerializer(serializers.Serializer):
    value = serializers.CharField()
    label = serializers.CharField()

class SensorGasChoiceSerializer(serializers.Serializer):
    value = serializers.CharField()
    label = serializers.CharField()

    
#################---Main Serializers---#####################
class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"
        read_only_fields = []

class DetectorModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetectorModel
        fields = "__all__"
        read_only_fields = []

class DetectorSerializer(serializers.ModelSerializer):
    purchase_date = serializers.DateField(allow_null=True, required=False)

    class Meta:
        model = Detector
        fields = "__all__"
        read_only_fields = []

    def validate(self, attrs):
        # Get the instance if this is an update operation
        instance = getattr(self, 'instance', None)

        # Check for duplicate label (only if it's a new instance or label is being changed)
        label = attrs.get('label')
        if label:
            if instance and instance.label != label:
                # Update operation with label change - check for duplicates
                if Detector.objects.filter(label=label).exists():
                    raise serializers.ValidationError({'label': ['A detector with this label already exists.']})
            elif not instance:
                # Create operation - check for duplicates
                if Detector.objects.filter(label=label).exists():
                    raise serializers.ValidationError({'label': ['A detector with this label already exists.']})

        # Check for duplicate serial (only if it's a new instance or serial is being changed)
        serial = attrs.get('serial')
        if serial:
            if instance and instance.serial != serial:
                # Update operation with serial change - check for duplicates
                if Detector.objects.filter(serial=serial).exists():
                    raise serializers.ValidationError({'serial': ['A detector with this serial already exists.']})
            elif not instance:
                # Create operation - check for duplicates
                if Detector.objects.filter(serial=serial).exists():
                    raise serializers.ValidationError({'serial': ['A detector with this serial already exists.']})

        # Check for required fields that shouldn't be null
        required_fields = ['detector_model', 'status', 'location']
        for field in required_fields:
            if not attrs.get(field):
                raise serializers.ValidationError({field: [f'{field.replace("_", " ").title()} is required.']})

        # Validate purchase_cost if provided
        purchase_cost = attrs.get('purchase_cost')
        if purchase_cost is not None and purchase_cost < 0:
            raise serializers.ValidationError({'purchase_cost': ['Purchase cost cannot be negative.']})

        # Validate purchase_date if provided
        purchase_date = attrs.get('purchase_date')
        if purchase_date:
            from datetime import date
            if purchase_date > date.today():
                raise serializers.ValidationError({'purchase_date': ['Purchase date cannot be in the future.']})

        return attrs

class DetectorModelConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetectorModelConfiguration
        fields = "__all__"
              
class MaintenanceSerializer(serializers.ModelSerializer):
    date_due = serializers.DateField(allow_null=True, required=False)
    date_performed = serializers.DateField(allow_null=True, required=False)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Maintenance
        fields = ['id', "maintenance_type", "status", "detector", "date_due", "date_performed", "performed_by", "notes", "created_at", "updated_at"]

class MaintenanceTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceTask
        fields = "__all__"
        
class DetectorFaultSerializer(serializers.ModelSerializer):
    report_dt = serializers.DateField(allow_null=True, required=False)
    resolve_dt = serializers.DateField(allow_null=True, required=False)

    class Meta:
        model = DetectorFault
        fields = "__all__"

class CylinderTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CylinderType
        fields = "__all__"
        
class CylinderSerializer(serializers.ModelSerializer):
    order_date = serializers.DateField(allow_null=True, required=False)
    receive_date = serializers.DateField(allow_null=True, required=False)
    expiry_date = serializers.DateField(allow_null=True, required=False)
    operational_date = serializers.DateField(allow_null=True, required=False)
    empty_date = serializers.DateField(allow_null=True, required=False)

    class Meta:
        model = Cylinder
        exclude = ['cylinder_number']  # Exclude cylinder_number from input

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Add the computed label field
        data['label'] = f"CYL{instance.cylinder_number:05d}"
        return data

    def create(self, validated_data):
        from django.db import models
        from django.db import transaction
        # Find the next available cylinder number in a transaction-safe way
        with transaction.atomic():
            last_cylinder = Cylinder.objects.select_for_update().aggregate(models.Max('cylinder_number'))
            next_number = (last_cylinder['cylinder_number__max'] or 0) + 1
            validated_data['cylinder_number'] = next_number
            return super().create(validated_data)

class SensorTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorType
        fields = "__all__"
        
class SensorSerializer(serializers.ModelSerializer):
    order_date = serializers.DateField(allow_null=True, required=False)
    receive_date = serializers.DateField(allow_null=True, required=False)
    warranty_date = serializers.DateField(allow_null=True, required=False)
    expiry_date = serializers.DateField(allow_null=True, required=False)
    install_date = serializers.DateField(allow_null=True, required=False)
    remove_date = serializers.DateField(allow_null=True, required=False)

    class Meta:
        model = Sensor
        fields = "__all__"
        
class SensorSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorSlot
        fields = "__all__"
        
class LocationDetectorSlotsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationDetectorSlots
        fields = "__all__"


class ChangeDetectorLocationSerializer(serializers.Serializer):
    detector_id = serializers.IntegerField()
    location_id = serializers.IntegerField()


class ChangeCylinderLocationSerializer(serializers.Serializer):
    cylinder_id = serializers.IntegerField()
    location_id = serializers.IntegerField()


class ComplexChangeDetectorLocationSerializer(serializers.Serializer):
    outgoing_detector_id = serializers.IntegerField()
    outgoing_location_id = serializers.IntegerField()
    returning_detector_id = serializers.IntegerField()
    returning_location_id = serializers.IntegerField()


class ComplexChangeCylinderLocationSerializer(serializers.Serializer):
    outgoing_cylinder_id = serializers.IntegerField()
    outgoing_location_id = serializers.IntegerField()
    returning_cylinder_id = serializers.IntegerField()
    returning_location_id = serializers.IntegerField()

class CylinderFaultSerializer(serializers.ModelSerializer):
    report_dt = serializers.DateTimeField(read_only=True)
    resolve_dt = serializers.DateField(allow_null=True, required=False)

    class Meta:
        model = CylinderFault
        fields = "__all__"
