from django.db import models
from ../inventory/models import DetectorType, DetectorModel, Detector

# Create your models here.

class Gas(models.TextChoices):
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
 #ethylene oxide
 ETO = "ET", "ETO"    

class Units(models.TextChoices):
 PPM = "PM", "ppm"
 PPB = "PB", "ppb"
 VFV = "VV", "%v/v"
 VLE = "VL", "%lel"
 MGM = "MM", "mg/m3"
 MIGM = "MI", "microgram/m3"

class Incident(models.Model):
 label = models.CharField(max_length=16)
 start_date = models.DateField()
 street_address = models.CharField(max_length=256)
 suburb = models.CharField(max_length=36)
 latitude = models.FloatField(null=True)
 longitude = models.FloatField(null=True)

class DetectorSite(models.Model):
 incident = models.ForeignKey(Incident, on_delete=models.CASCADE)
 label = models.CharField(max_length=1)
 description = models.CharField(max_length=256, null=Ture, blank=True)
 latitude = models.FloatField(null=True)
 longitude = models.FloatField(null=True)
 
class ReadingType(models.Model):
 gas = models.CharField(max_length=2, choices=Gas.choices, default=Gas.CO)
 units = model.CharField(max_length=2, choices=Units.choices, default=Units.PPM)
 threshold1 = models.FloatField(null=True)
 threshold2 = models.FloatField(null=True)
 threshold3 = models.FloatField(null=True)
 #translate data header format from safety suite responder
 responder_header = models.CharField(max_length=16, null=True, blank=True)
    
class Reading(models.Model):
 detector = models.ForeignKey(Detector, on_delete=models.CASCADE)
 reading_type = models.ForeignKey(ReadingType, on_delete=models.CASCADE)
 value = models.FloatField()
 dt = models.DateTime()
 detector_stie = models.ForeignKey(DetectorSite, on_delete=models.CASCADE)
 
