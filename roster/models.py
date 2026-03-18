from django.db import models

# Create your models here.

class Scientist(models.Model):
    first_name = models.CharField(max_length=16)
    last_name = models.CharField(max_length=16)
    initials = models.CharField(max_length=4)
    active = models.BooleanField(default=True)

class RosterSlot(models.Model):
    scientist = models.ForeignKey(Scientist, null=True, on_delete=models.PRESERVE)
    start_date = models.DateField()
    end_date = models.DateField()

class PublicHolidays(models.Model):
    name = models.CharField(max_length=16)
    instance_date = models.DateField()
