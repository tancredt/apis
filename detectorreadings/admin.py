from django.contrib import admin

from .models import (
    Incident,
    DetectorSite,
    ReadingType,
    Reading,
    DetectorValidation,
    DetectorSiteValidation,
)


@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    list_display = ("label", "start_date", "street_address", "suburb")
    list_filter = ("start_date",)
    search_fields = ("label", "street_address", "suburb")
    date_hierarchy = "start_date"


@admin.register(DetectorSite)
class DetectorSiteAdmin(admin.ModelAdmin):
    list_display = ("label", "incident", "description")
    list_filter = ("incident",)
    search_fields = ("description",)


@admin.register(ReadingType)
class ReadingTypeAdmin(admin.ModelAdmin):
    list_display = ("gas", "units", "threshold1", "threshold2", "threshold3", "responder_header")
    list_filter = ("gas", "units")


@admin.register(Reading)
class ReadingAdmin(admin.ModelAdmin):
    list_display = ("detector", "reading_type", "value", "dt", "detector_site", "is_valid")
    list_filter = ("is_valid", "reading_type__gas", "reading_type__units", "detector", "detector_site__incident")
    search_fields = ("detector__label",)
    date_hierarchy = "dt"


@admin.register(DetectorValidation)
class DetectorValidationAdmin(admin.ModelAdmin):
    list_display = ("detector", "reason", "start_dt", "end_dt")
    list_filter = ("detector",)
    search_fields = ("reason",)
    date_hierarchy = "start_dt"


@admin.register(DetectorSiteValidation)
class DetectorSiteValidationAdmin(admin.ModelAdmin):
    list_display = ("detector_site", "reason", "start_dt", "end_dt")
    list_filter = ("detector_site__incident",)
    search_fields = ("reason",)
    date_hierarchy = "start_dt"
