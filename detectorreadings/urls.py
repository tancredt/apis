from rest_framework import routers
from django.urls import path, include

from .views import (
    GasView,
    UnitsView,
    IncidentViewSet,
    DetectorSiteViewSet,
    ReadingTypeViewSet,
    ReadingViewSet,
    DetectorValidationViewSet,
    DetectorSiteValidationViewSet,
)

router = routers.SimpleRouter()
router.register(r'incidents', IncidentViewSet, basename='incident')
router.register(r'detector-sites', DetectorSiteViewSet, basename='detectorsite')
router.register(r'reading-types', ReadingTypeViewSet, basename='readingtype')
router.register(r'readings', ReadingViewSet, basename='reading')
router.register(r'detector-validations', DetectorValidationViewSet, basename='detectorvalidation')
router.register(r'detector-site-validations', DetectorSiteValidationViewSet, basename='detectorsitevalidation')

urlpatterns = [
    # Choice endpoints
    path('gas/', GasView.as_view(), name='gas-list'),
    path('units/', UnitsView.as_view(), name='units-list'),
    
    # Router URLs for ViewSets
    path('', include(router.urls)),
]
