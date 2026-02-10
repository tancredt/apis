from rest_framework import routers
from django.urls import path, include

from .views import (
    LocationViewSet,
    DetectorModelViewSet,
    DetectorViewSet,
    MaintenanceViewSet,
    MaintenanceTaskViewSet,
    DetectorFaultViewSet,
    CylinderTypeViewSet,
    CylinderViewSet,
    CylinderFaultViewSet,
    LocationDetectorSlotsViewSet,
    DetectorModelConfigurationViewSet,
    SensorTypeViewSet,
    SensorViewSet,
    SensorSlotViewSet,
    LocationTypeView,
    ManufacturerView,
    DetectorTypeView,
    SupplierView,
    DetectorStatusView,
    MaintenanceTypeView,
    MaintenanceTaskTypeView,
    MaintenanceStatusView,
    DetectorFaultTypeView,
    CylinderGasView,
    CylinderUnitView,
    CylinderVolumeView,
    CylinderStatusView,
    SensorStatusView,
    SensorGasView
)
from .views_auth import LoginView, LogoutView, CurrentUserView, CsrfTokenView
from .views import change_detector_location, change_cylinder_location

router = routers.SimpleRouter()
router.register(r'locations', LocationViewSet)
router.register(r'detectormodels', DetectorModelViewSet)
router.register(r'detectors', DetectorViewSet)
router.register(r'maintenances', MaintenanceViewSet),
router.register(r'maintenancetasks', MaintenanceTaskViewSet)
router.register(r'detectorfaults', DetectorFaultViewSet)
router.register(r'cylindertypes', CylinderTypeViewSet)
router.register(r'cylinders', CylinderViewSet)
router.register(r'cylinderfaults', CylinderFaultViewSet)
router.register(r'locationdetectorslots', LocationDetectorSlotsViewSet)
router.register(r'detectormodelconfigurations', DetectorModelConfigurationViewSet)
router.register(r'sensortypes', SensorTypeViewSet)
router.register(r'sensors', SensorViewSet)
router.register(r'sensorslots', SensorSlotViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('location-types/', LocationTypeView.as_view(), name='location-type-list'),
    path('manufacturers/', ManufacturerView.as_view(), name='manufacturer-list'),
    path('detector-types/', DetectorTypeView.as_view(), name='detector-type-list'),
    path('suppliers/', SupplierView.as_view(), name='supplier-list'),
    path('detector-statuses/', DetectorStatusView.as_view(), name='detector-status-list'),
    path('maintenance-types/', MaintenanceTypeView.as_view(), name='maintenance-type-list'),
    path('maintenance-task-types/', MaintenanceTaskTypeView.as_view(), name='maintenance-task-type-list'),
    path('maintenance-statuses/', MaintenanceStatusView.as_view(), name='maintenance-status-list'),
    path('detector-fault-types/', DetectorFaultTypeView.as_view(), name='detector-fault-type-list'),
    path('cylinder-gas/', CylinderGasView.as_view(), name='cylinder-gas-list'),
    path('cylinder-unit/', CylinderUnitView.as_view(), name='cylinder-unit-list'),
    path('cylinder-volume/', CylinderVolumeView.as_view(), name='cylinder-volumne-list'),
    path('cylinder-statuses/', CylinderStatusView.as_view(), name='cylinder-status-list'),
    path('sensor-statuses/', SensorStatusView.as_view(), name='sensor-status-list'),
    path('sensor-gases/', SensorGasView.as_view(), name='sensor-gas-list'),
    path('auth/login/', LoginView.as_view(), name='api-login'),
    path('auth/logout/', LogoutView.as_view(), name='api-logout'),
    path('auth/current-user/', CurrentUserView.as_view(), name='current-user'),
    path('csrf-token/', CsrfTokenView.as_view(), name='csrf-token'),
    path('change-detector-location/', change_detector_location, name='change-detector-location'),
    path('change-cylinder-location/', change_cylinder_location, name='change-cylinder-location'),
]
