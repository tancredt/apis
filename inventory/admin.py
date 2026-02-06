from django.contrib import admin

from .models import (
    Location,
    DetectorModel,
    Detector,
    LocationDetectorSlots,
    Maintenance,
    MaintenanceTask,
    DetectorFault,
    DetectorModelConfiguration,
    CylinderFault
)

# Register your models here.

admin.site.register(Location)
admin.site.register(DetectorModel)
admin.site.register(Detector)
admin.site.register(LocationDetectorSlots)
admin.site.register(Maintenance)
admin.site.register(MaintenanceTask)
admin.site.register(DetectorFault)
admin.site.register(CylinderFault)


