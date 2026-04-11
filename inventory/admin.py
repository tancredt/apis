from django.contrib import admin

from .models import (
    Location,
    DetectorModel,
    DetectorModelConfiguration,
    Detector,
    LocationDetectorSlot,
    Maintenance,
    MaintenanceTask,
    DetectorFault,
    CylinderType,
    Cylinder,
    CylinderFault,
    SensorType,
    Sensor,
    SensorSlot,
)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("label", "location_type", "station", "priority", "address")
    list_filter = ("location_type", "station", "priority")
    search_fields = ("label", "address", "station")


@admin.register(DetectorModel)
class DetectorModelAdmin(admin.ModelAdmin):
    list_display = ("label", "manufacturer", "detector_type", "supplier", "part_number")
    list_filter = ("manufacturer", "detector_type", "supplier")
    search_fields = ("label", "part_number")


@admin.register(DetectorModelConfiguration)
class DetectorModelConfigurationAdmin(admin.ModelAdmin):
    list_display = ("label", "detector_model", "sensor_gases")
    list_filter = ("detector_model",)
    search_fields = ("label", "detector_model__label")


@admin.register(Detector)
class DetectorAdmin(admin.ModelAdmin):
    list_display = ("label", "serial", "status", "detector_model", "location", "purchase_date")
    list_filter = ("status", "detector_model", "location", "location__location_type", "firmware")
    search_fields = ("label", "serial", "notes")
    date_hierarchy = "purchase_date"


@admin.register(LocationDetectorSlot)
class LocationDetectorSlotAdmin(admin.ModelAdmin):
    list_display = ("location", "detector_model", "detector")
    list_filter = ("location", "detector_model")
    search_fields = ("location__label", "detector_model__label")


@admin.register(Maintenance)
class MaintenanceAdmin(admin.ModelAdmin):
    list_display = ("detector", "maintenance_type", "status", "date_due", "date_performed", "performed_by")
    list_filter = ("maintenance_type", "status", "detector__detector_model", "detector__location")
    search_fields = ("notes", "performed_by")
    date_hierarchy = "date_due"


@admin.register(MaintenanceTask)
class MaintenanceTaskAdmin(admin.ModelAdmin):
    list_display = ("task_type", "maintenance")
    list_filter = ("task_type",)


@admin.register(DetectorFault)
class DetectorFaultAdmin(admin.ModelAdmin):
    list_display = ("detector", "fault_type", "status", "report_dt", "report_location")
    list_filter = ("fault_type", "status", "report_location", "report_location__location_type")
    search_fields = ("reported_by", "submit_notes", "resolve_notes")
    date_hierarchy = "report_dt"


@admin.register(CylinderType)
class CylinderTypeAdmin(admin.ModelAdmin):
    list_display = ("part_number", "supplier", "volume", "balance_gas", "active")
    list_filter = ("supplier", "volume", "balance_gas", "active")
    search_fields = ("part_number",)


@admin.register(Cylinder)
class CylinderAdmin(admin.ModelAdmin):
    list_display = ("cylinder_number", "serial", "cylinder_type", "location", "status", "receive_date", "expiry_date")
    list_filter = ("status", "cylinder_type", "location", "location__location_type")
    search_fields = ("serial", "cylinder_type__part_number")
    date_hierarchy = "receive_date"


@admin.register(CylinderFault)
class CylinderFaultAdmin(admin.ModelAdmin):
    list_display = ("cylinder", "fault_type", "status", "report_dt", "report_location")
    list_filter = ("fault_type", "status", "report_location")
    search_fields = ("cylinder__serial", "reported_by", "submit_notes", "resolve_notes")
    date_hierarchy = "report_dt"


@admin.register(SensorType)
class SensorTypeAdmin(admin.ModelAdmin):
    list_display = ("part_number", "manufacturer", "sensorgas", "active", "warranty_months", "expiry_months")
    list_filter = ("manufacturer", "sensorgas", "active")
    search_fields = ("part_number", "compatible_detectormodels")


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = ("serial", "sensor_type", "status", "detector", "order_date", "install_date")
    list_filter = ("status", "sensor_type__sensorgas", "sensor_type__manufacturer", "detector__detector_model", "detector__location")
    search_fields = ("serial", "sensor_type__part_number")
    date_hierarchy = "order_date"


@admin.register(SensorSlot)
class SensorSlotAdmin(admin.ModelAdmin):
    list_display = ("detector", "sensorgas", "sensor")
    list_filter = ("sensorgas", "detector__detector_model", "detector__location")
    search_fields = ("detector__label", "sensor__serial")
