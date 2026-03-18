from django.urls import path
from .views import (
    GasView,
    UnitsView,
    IncidentListCreateView,
    IncidentDetailView,
    DetectorSiteListCreateView,
    DetectorSiteDetailView,
    ReadingTypeListCreateView,
    ReadingTypeDetailView,
    ReadingListCreateView,
    ReadingDetailView,
    ReadingStatsView,
    ValidationListCreateView,
    ValidationDetailView,
    ActiveValidationView,
)

urlpatterns = [
    # Choice endpoints
    path('gas/', GasView.as_view(), name='gas-list'),
    path('units/', UnitsView.as_view(), name='units-list'),
    
    # Incident endpoints
    path('incidents/', IncidentListCreateView.as_view(), name='incident-list-create'),
    path('incidents/<int:pk>/', IncidentDetailView.as_view(), name='incident-detail'),
    
    # Detector Site endpoints
    path('detector-sites/', DetectorSiteListCreateView.as_view(), name='detectorsite-list-create'),
    path('detector-sites/<int:pk>/', DetectorSiteDetailView.as_view(), name='detectorsite-detail'),
    
    # Reading Type endpoints
    path('reading-types/', ReadingTypeListCreateView.as_view(), name='readingtype-list-create'),
    path('reading-types/<int:pk>/', ReadingTypeDetailView.as_view(), name='readingtype-detail'),
    
    # Reading endpoints
    path('readings/', ReadingListCreateView.as_view(), name='reading-list-create'),
    path('readings/<int:pk>/', ReadingDetailView.as_view(), name='reading-detail'),
    path('readings/stats/', ReadingStatsView.as_view(), name='reading-stats'),
    
    # Validation endpoints
    path('validations/', ValidationListCreateView.as_view(), name='validation-list-create'),
    path('validations/<int:pk>/', ValidationDetailView.as_view(), name='validation-detail'),
    path('validations/active/', ActiveValidationView.as_view(), name='validation-active'),
]
