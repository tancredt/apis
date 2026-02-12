
from django.db import models


class LocationType(models.TextChoices):
    STATION = "ST", "Station"
    APPLIANCE = "AP", "Appliance"
    DISTRICT_OFFICE = "DI", "District Office"
    WORK_GROUP = "WG", "Work Group"
    WAREHOUSE = "WA", "Warehouse"
    WORKSHOP = "WK", "Workshop"
    
    
class Manufacturer(models.TextChoices):
    HONEYWELL = "HW", "Honeywell/Rae"
    MSA = "MS", "MSA"
    DRAEGER = "DR", "Draeger"
    PROENGIN = "PR", "Proengin"
    THERMO = "TH", "Thermo Scientific"
    SMITHS = "SM", "Smiths"
    INFICON = "IN", "Inficon"
    MIRION = "MI", "Mirion"
    CANBERRA = "CB", "Canberra"
    PRINCETON = "PI", "Princeton Electronics"
    AUTOMESS = "AU", "Automess"
    TSI = "TS", "TSI"
    
class DetectorType(models.TextChoices):
    PID = "PI", "PID"
    FID = "FI", "FID"
    PUMPED_MULTI = "PM", "Pumped Multi Sensor"
    PERSONAL_MULTI = "NM", "Personal Multi Sensor"
    AREA_MONITOR = "AM", "Area Monitor"
    PARTICULATE_DETECTOR = "PD", "Particulate"
    DOSIMETER = "DI", "DOSIMETER"
    DOSERATE_METER = "DO", "Doserate Meter"
    SURVEY_METER = "SM", "Survey Meter"
    ION_MOBILITY_SPECTROMETER = "IM", "IMS"
    FPD = "FP", "FPD"
    CALIBRATION_DOCK = "CD", "Calibration Dock"
    CALIBRATION_CRADLE = "CC", "Calibration Cradle"
    
class Supplier(models.TextChoices):
    AIRMET = "AM", "AirMet"
    AES = "AE", "AES"
    MSA = "MS", "MSA"
    DRAEGER = "DR", "Draeger"
    WARSACH = "WS", "WARSACH"
    CAC = "CA", "CAC"
    

class DetectorStatus(models.TextChoices):
    ONORDER = "OO", "On Order"
    OFFLINE = "OF", "Offline Repair"
    INSTOCK = "IS", "In Stock"
    OPERATIONAL = "OP", "Operational"
    DECOMMISS = "DC", "Decommissioned"

class MaintenanceType(models.TextChoices):
    #major service is like the 6 monthly
    RSERVICE = "SV", "Scheduled Service"
    #minor service would be the result of a fault report
    USERVICE = "MS", "Unscheduled Service"
    BATTERY = "BT", "Battery Replacement"
    FILTER = "FC", "Filter Replacement"
    DESSICANT = "DR", "Dessicant Replacement"
class MaintenanceTaskType(models.TextChoices):
    CALIBRATION = "CB", "Calibration"
    BUMP = "BM", "Bump"
    SENSOR = "SN", "Sensor Replacement"
    DISPLAY = "DS", "Display Replacement"
    LABEL = "LB", "Label Replacement"
    BATTERY = "BT", "Battery Replacement"
    FILTER = "FC", "Filter Replacement"
    BOARD = "BD", "Board Replacement"
    REPAIR = "RP", "Repair"
    #carabiners, etc.
    ATTACHMENT = "AT", "Attachment Replacement"
    
class MaintenanceStatus(models.TextChoices):
    SCHEDULED = "SC", "Scheduled"
    OPEN = "OP", "Open"
    CLOSED = "CL", "Closed"

class DetectorFaultStatus(models.TextChoices):
    OPEN = "OP", "Open"
    CLOSED = "CL", "Closed"

class CylinderFaultStatus(models.TextChoices):
    OPEN = "OP", "Open"
    COMPLETE = "CP", "Complete"

class DetectorFaultType(models.TextChoices):
    BUMPFAIL = "BF", "Failed Bump"
    SENSORFAIL = "SF", "Sensor Fail"
    DISPLAYSERROR = "DE", "Displays Error"
    WONTSTART = "WS", "Will not turn on"
    DAMAGEDDISPLAY ="DD", "Damaged Display"
    MISSINGATTACHMENT = "MA", "Missing Attachment"
    
class CylinderGas(models.TextChoices):
    CO = "CO", "CO"
    H2S = "HS", "H2S"
    CH4 = "CH", "CH4"
    O2 = "O2", "O2"
    ISOBUTYLENE = "IB", "Isobutylene"
    HCN = "HC", "HCN"
    N2 = "N2", "N2"
    CL2 = "CL", "Cl2"
    PH3 = "PH", "PH3"
    SO2 = "SO", "SO2"
    NO2 = "NO", "NO2"
    CO2 = "C2", "CO2"
    NH3 = "NH", "NH3"
    
class SensorGas(models.TextChoices):
    CO = "CO", "CO"
    H2S = "HS", "H2S"
    LEL = "LE", "LEL"
    O2 = "O2", "O2"
    VOC = "VO", "VOC"
    HCN = "HC", "HCN"
    CL2 = "CL", "Cl2"
    PH3 = "PH", "PH3"
    SO2 = "SO", "SO2"
    NO2 = "NO", "NO2"
    CO2 = "C2", "CO2"
    NH3 = "NH", "NH3"
    
class CylinderVolume(models.TextChoices):
    L34 = "L034", "34 L"
    L65 = "L065", "65 L"
    L103 = "L103", "103 L"
    L112 = "L112", "112 L"
    L552 = "L552", "552 L"
    
class CylinderUnit(models.TextChoices):
    PPM = "PM", "ppm"
    PERCENTVOLUMNE = "PV", "%v/v"
    PERCENTLEL = "PL", "%LEL"
    MGPERLITRE = "ML", "mg/L"

class CylinderStatus(models.TextChoices):
    ONORDER = "OO", "On Order"
    INSTOCK = "IS", "In Stock"
    OPERATIONAL = "OP", "Operational"
    EMPTY = "MT", "Empty"

class SensorStatus(models.TextChoices):
    ONORDER = "OO", "On Order"
    INSTOCK = "IS", "In Stock"
    OPERATIONAL = "OP", "Operational"
    DECOMMISSIONED = "DC", "Decommissioned"
    
###############-----Main Models----------#######################        
class Location(models.Model):
    label = models.CharField(max_length=16, unique=True)
    address = models.CharField(max_length=256, blank=True)
    location_type = models.CharField(max_length=2, choices=LocationType.choices, default=LocationType.STATION)
    station = models.CharField(max_length=32, default="N/A")
    priority = models.PositiveSmallIntegerField(default=1)
    
    class Meta:
        ordering = ["-priority", "location_type", "label"]
        constraints = [
            models.UniqueConstraint(fields=["label"], name="uniq_location_label"),
        ]
        indexes = [
            models.Index(fields=["location_type", "priority"]),
        ]

    def __str__(self):
        return f"{self.get_location_type_display()} {self.label}"

class DetectorModel(models.Model):
    manufacturer = models.CharField(max_length=2, choices=Manufacturer.choices, default=Manufacturer.HONEYWELL)
    detector_type = models.CharField(max_length=2, choices=DetectorType.choices, default=DetectorType.PID)
    supplier = models.CharField(max_length=2, choices=Supplier.choices, default=Supplier.MSA)
    model_name = models.CharField(max_length=32, unique=True)
    part_number = models.CharField(max_length=32, blank=True)
    
    class Meta:
        ordering = ["detector_type"]

    def __str__(self):
        return f"{self.get_manufacturer_display()} {self.model_name} ({self.get_detector_type_display()})"

#This is used to label the configuration of detector, eg "Blue MultiRAE"
#The sensors_partnumbers is a comma delimited string with partnumbers
#This is use to create the sensor slots for the detector when the detector is created
class DetectorModelConfiguration(models.Model):
    detector_model = models.ForeignKey(DetectorModel, on_delete=models.PROTECT, related_name="detectormodelconfigurations")
    label = models.CharField(max_length=64)
    sensor_partnumbers = models.CharField(max_length=256)

    def __str__(self):
        return f"{self.label} ({self.detector_model.model_name})"

class Detector(models.Model):
    label = models.CharField(max_length=16, unique=True)
    serial = models.CharField(max_length=32, unique=True)
    status = models.CharField(max_length=2, choices=DetectorStatus.choices, default=DetectorStatus.ONORDER)
    configuration = models.ForeignKey(DetectorModelConfiguration, on_delete=models.PROTECT, null=True)
    purchase_date = models.DateField(null=True, blank=True)
    purchase_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.PROTECT, related_name="detectors")
    detector_model = models.ForeignKey(DetectorModel, on_delete=models.PROTECT, related_name="detectors")
    firmware = models.CharField(max_length=8, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    location_updated = models.DateTimeField(auto_now_add=True)  # Track when location was last updated

    class Meta:
        ordering = ["label"]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["detector_model"]),
            models.Index(fields=["location"]),
        ]

    def save(self, *args, **kwargs):
        # Check if this is an update and location has changed
        if self.pk:
            original = Detector.objects.get(pk=self.pk)
            if original.location != self.location:
                # Location has changed, update location_updated field
                from django.utils import timezone
                self.location_updated = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.label} {self.serial or ''}".strip()

class LocationDetectorSlots(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="detector_model_slots")
    detector_model = models.ForeignKey(DetectorModel, on_delete=models.CASCADE, related_name="location_slots")
    detector = models.ForeignKey(Detector, on_delete=models.PROTECT, null=True, related_name="detector_slots")

    def __str__(self):
        return f"{self.location.label} - {self.detector_model.model_name} - {self.detector.label if self.detector else 'Unassigned'}"

class DetectorFault(models.Model):
    detector = models.ForeignKey(Detector, on_delete=models.CASCADE, related_name="faults")
    report_dt = models.DateField()
    reported_by = models.CharField(max_length=32, blank=True)
    report_location = models.ForeignKey(Location, on_delete=models.CASCADE)
    status = models.CharField(max_length=2, choices=DetectorFaultStatus.choices, default="OP")
    fault_type = models.CharField(max_length=2, choices=DetectorFaultType.choices, default=DetectorFaultType.BUMPFAIL)
    submit_notes = models.TextField(blank=True)
    resolved_by = models.CharField(max_length=16, blank=True)
    resolve_dt = models.DateField(blank=True, null=True)
    resolve_notes = models.TextField(blank=True)
    class Meta:
        ordering = ["-report_dt", "detector"]

    def __str__(self):
        return f"{self.detector.label} - {self.get_fault_type_display()} ({self.report_dt.strftime('%Y-%m-%d %H:%M')})"
    
class Maintenance(models.Model):
    maintenance_type = models.CharField(max_length=2, choices=MaintenanceType.choices, default=MaintenanceType.RSERVICE)
    status = models.CharField(max_length=2, choices=MaintenanceStatus.choices, default=MaintenanceStatus.OPEN)
    detector = models.ForeignKey(Detector, on_delete=models.PROTECT, related_name="maintenance")
    date_due = models.DateField()
    date_performed = models.DateField(null=True, blank=True)
    performed_by = models.CharField(max_length=32, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["-date_due", "detector"]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["date_due"]),
            models.Index(fields=["date_performed"]),
        ]

    def __str__(self):
        base = f"{self.get_maintenance_type_display()} – {self.detector}"
        return f"{base} due {self.date_due} ({self.get_status_display()})"

class MaintenanceTask(models.Model):
    maintenance = models.ForeignKey(Maintenance, on_delete = models.CASCADE, related_name="tasks")
    task_type = models.CharField(max_length=2, choices=MaintenanceTaskType.choices, default=MaintenanceTaskType.CALIBRATION)

    class Meta:
        indexes = [
            models.Index(fields=["task_type"]),
            models.Index(fields=["maintenance"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["maintenance", "task_type"],
                name="uniq_maintenance_task"
            ),
        ]

    def __str__(self):
        return f"{self.maintenance} - {self.get_task_type_display()}"

###############---cylinders----------------##################

class CylinderType(models.Model):
    part_number = models.CharField(max_length=16, unique=True)
    supplier = models.CharField(max_length=2, choices=Supplier.choices, default=Supplier.AES)
    volume = models.CharField(max_length=4, choices=CylinderVolume.choices, default=CylinderVolume.L34)
    percent_error = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    expiry_months = models.PositiveIntegerField(null=True)
    balance_gas =  models.CharField(max_length=2, choices=CylinderGas.choices, default=CylinderGas.CO)
    #just filter out inactive cylinder types
    active = models.BooleanField(default=True)
    cylinder_1_gas = models.CharField(max_length=2, choices=CylinderGas.choices, default=CylinderGas.CO)
    cylinder_1_conc = models.DecimalField(max_digits=8, decimal_places=2)
    cylinder_1_units = models.CharField(max_length=2, choices=CylinderUnit.choices, default=CylinderUnit.PPM)

    cylinder_2_gas = models.CharField(max_length=2, choices=CylinderGas.choices, blank=True)
    cylinder_2_conc = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    cylinder_2_units = models.CharField(max_length=2, choices=CylinderUnit.choices, blank=True)

    cylinder_3_gas = models.CharField(max_length=2, choices=CylinderGas.choices, blank=True)
    cylinder_3_conc = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    cylinder_3_units = models.CharField(max_length=2, choices=CylinderUnit.choices, blank=True)

    cylinder_4_gas = models.CharField(max_length=2, choices=CylinderGas.choices, blank=True)
    cylinder_4_conc = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    cylinder_4_units = models.CharField(max_length=2, choices=CylinderUnit.choices, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["part_number"]),
            models.Index(fields=["cylinder_1_gas"]),
        ]

    def __str__(self):
        retstring = f"{self.part_number} - {self.get_cylinder_1_gas_display()}({self.cylinder_1_conc} {self.get_cylinder_1_units_display()})"
        if self.cylinder_2_gas != "":
            retstring += f"/{self.get_cylinder_2_gas_display()}({self.cylinder_2_conc} {self.get_cylinder_2_units_display()})"
            if self.cylinder_3_gas != "":
                retstring += f"/{self.get_cylinder_3_gas_display()}({self.cylinder_3_conc} {self.get_cylinder_3_units_display()})"
                if self.cylinder_4_gas != "":
                    retstring += f"/{self.get_cylinder_4_gas_display()}({self.cylinder_4_conc} {self.get_cylinder_4_units_display()})"
        return retstring
        
class Cylinder(models.Model):
    cylinder_number = models.IntegerField(unique=True)
    serial = models.CharField(max_length=16, null=True, blank=True)
    cylinder_type = models.ForeignKey(CylinderType, on_delete=models.PROTECT)
    location = models.ForeignKey(Location, on_delete=models.PROTECT)
    detector = models.ForeignKey(Detector, on_delete=models.PROTECT, null=True)
    status = models.CharField(max_length=2, choices=CylinderStatus.choices, default=CylinderStatus.ONORDER)
    order_date = models.DateField(null=True)
    receive_date = models.DateField(null=True)
    expiry_date = models.DateField(null=True)
    operational_date = models.DateField(null=True)
    empty_date = models.DateField(null=True)
                              
    class Meta:
        ordering = ['cylinder_type', 'receive_date',]

class CylinderFault(models.Model):
    cylinder = models.ForeignKey(Cylinder, on_delete=models.CASCADE)
    report_dt = models.DateTimeField(auto_now_add=True)
    reported_by = models.CharField(max_length=32)
    report_location = models.ForeignKey(Location, on_delete=models.CASCADE)
    status = models.CharField(max_length=2, choices=CylinderFaultStatus.choices, default="OP")
    fault_type = models.CharField(max_length=2, choices=DetectorFaultType.choices, default=DetectorFaultType.BUMPFAIL)
    submit_notes = models.TextField(blank=True)
    resolved_by = models.CharField(max_length=16, blank=True)
    resolve_dt = models.DateTimeField(null=True)
    resolve_notes = models.TextField(blank=True)
    class Meta:
        ordering = ["report_dt", "cylinder"]

    def __str__(self):
        return f"{self.cylinder.label} - ({self.report_dt.strftime('%Y-%m-%d %H:%M')})"
###########---Sensors---########################################

class SensorType(models.Model):
    manufacturer = models.CharField(max_length=2, choices=Manufacturer.choices, default=Manufacturer.HONEYWELL)
    part_number = models.CharField(max_length=32, unique=True)
    active = models.BooleanField(default=True)
    sensorgas = models.CharField(max_length=2, choices=SensorGas.choices, blank=True)
    #This just lists the detector models that the sensor is compatible with
    #Some sensors are compatible with multiple detector models
    #Making it a comma delimeted string rather than joining a new many-to-many table
    compatible_detectormodels = models.CharField(max_length=256)
    warranty_months = models.PositiveIntegerField(null=True)
    expiry_months = models.PositiveIntegerField(null=True)

    def __str__(self):
        return f"{self.part_number} - {self.get_sensorgas_display()}"
            
class Sensor(models.Model):
    serial = models.CharField(max_length=32, null=True, blank=True, unique=True)
    sensor_type = models.ForeignKey(SensorType, on_delete=models.CASCADE)
    detector = models.ForeignKey(Detector, on_delete=models.PROTECT, null=True)
    status = models.CharField(max_length=2, choices=SensorStatus.choices, default=SensorStatus.ONORDER)
    order_date = models.DateField(null=True)
    receive_date = models.DateField(null=True)
    warranty_date = models.DateField(null=True)
    expiry_date = models.DateField(null=True)
    install_date = models.DateField(null=True)
    remove_date = models.DateField(null=True)
    def __str__(self):
        return f"{self.serial} - {self.sensor_type.get_sensorgas_display()}"

#these should be created automatically for each detector when the detector is created. The sensors are slotted in an out as required.
class SensorSlot(models.Model):
    detector = models.ForeignKey(Detector, on_delete=models.PROTECT)
    sensor_type = models.ForeignKey(SensorType, on_delete=models.PROTECT)
    sensor = models.ForeignKey(Sensor, on_delete=models.PROTECT, null=True)
    
        
