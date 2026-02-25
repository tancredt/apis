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

# Register your models here.

admin.site.register(Location)
admin.site.register(DetectorModel)
admin.site.register(DetectorModelConfiguration)
admin.site.register(Detector)
admin.site.register(LocationDetectorSlot)
admin.site.register(Maintenance)
admin.site.register(MaintenanceTask)
admin.site.register(DetectorFault)
admin.site.register(CylinderType)
admin.site.register(Cylinder)
admin.site.register(CylinderFault)
admin.site.register(SensorType)
admin.site.register(Sensor)
admin.site.register(SensorSlot)


