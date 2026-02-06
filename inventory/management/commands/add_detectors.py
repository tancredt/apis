from django.core.management.base import BaseCommand
from inventory.models import Detector, Location, DetectorModel, DetectorModelConfiguration, DetectorStatus
from django.utils.text import slugify
import random
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'Add 500 new detectors of various models'

    def handle(self, *args, **options):
        self.stdout.write('Starting to add 500 new detectors...')

        # Get all existing locations and detector models
        locations = list(Location.objects.all())
        detector_models = list(DetectorModel.objects.all())
        configurations = list(DetectorModelConfiguration.objects.all())

        if not locations:
            self.stdout.write(
                self.style.ERROR('No locations found. Please run populate_test_data first.')
            )
            return

        if not detector_models:
            self.stdout.write(
                self.style.ERROR('No detector models found. Please run populate_test_data first.')
            )
            return

        # Define possible statuses
        statuses = [status[0] for status in DetectorStatus.choices]

        # Generate 500 detectors
        detectors_to_create = []
        for i in range(500):
            # Create unique label and serial
            label = f"D{i+1:03d}"  # D001, D002, ..., D500
            serial = f"SER{i+1001:04d}"  # SER1001, SER1002, ..., SER1500

            # Randomly select related objects
            location = random.choice(locations)
            detector_model = random.choice(detector_models)
            
            # Select a configuration that matches the detector model, if available
            compatible_configs = [c for c in configurations if c.detector_model == detector_model]
            configuration = random.choice(compatible_configs) if compatible_configs else None

            # Random status
            status = random.choice(statuses)

            # Random purchase date within the last 3 years
            days_ago = random.randint(0, 1095)  # 3 years in days
            purchase_date = datetime.now().date() - timedelta(days=days_ago)

            # Random purchase cost between $500 and $5000
            purchase_cost = round(random.uniform(500.0, 5000.0), 2)

            detector = Detector(
                label=label,
                serial=serial,
                status=status,
                configuration=configuration,
                purchase_date=purchase_date,
                purchase_cost=purchase_cost,
                location=location,
                detector_model=detector_model
            )
            detectors_to_create.append(detector)

        # Bulk create the detectors
        Detector.objects.bulk_create(detectors_to_create, ignore_conflicts=True)

        self.stdout.write(
            self.style.SUCCESS(f'Successfully added {len(detectors_to_create)} new detectors!')
        )