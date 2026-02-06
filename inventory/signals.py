from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date
from .models import Detector, DetectorModelConfiguration, SensorSlot, SensorType, Sensor

@receiver(post_save, sender=Detector)
def create_sensor_slots(sender, instance, created, **kwargs):
    if created:
        res = SensorSlot.objects.filter(detector=instance)
        if res:
            res.delete()
        if instance.configuration:
            if instance.configuration.sensor_partnumbers:
                for pn in instance.configuration.sensor_partnumbers.split(','):
                    st = SensorType.objects.get(part_number=pn)
                    if st:
                        sensorslot = SensorSlot(detector=instance, sensor_type=st)
                        sensorslot.save()

#updates the sensorslot when the sensors detector is updated
@receiver(post_save, sender=Sensor)
def update_sensor_slot(sender, instance, created, **kwargs):
    # Only run if the sensor is being assigned to a detector
    if instance.detector:
        try:
            sensor_slot = SensorSlot.objects.get(
                sensor_type=instance.sensor_type,
                detector=instance.detector
            )
            # Mark the old sensor as decommissioned only if a different sensor is in the slot
            if sensor_slot.sensor and sensor_slot.sensor.pk != instance.pk:
                old_sensor = sensor_slot.sensor
                old_sensor.status = "DC"
                old_sensor.remove_date = instance.install_date or date.today()
                old_sensor.save()
            sensor_slot.sensor = instance
            sensor_slot.save()
        except SensorSlot.DoesNotExist:
            # If no sensor slot exists for this detector and sensor type combination,
            # do nothing - don't create a new slot
            pass

