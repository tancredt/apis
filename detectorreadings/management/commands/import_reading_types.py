import csv
import os
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from detectorreadings.models import ReadingType, Gas, Units
from detectorreadings.import_fixtures import READING_TYPES_CSV


class Command(BaseCommand):
    help = 'Import ReadingType data from the hardcoded CSV file (detectorreadings/fixtures/ReadingTypes.csv)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear all existing ReadingType records before importing'
        )

    def handle(self, *args, **options):
        clear = options['clear']
        filepath = READING_TYPES_CSV

        # Check if file exists
        if not os.path.exists(filepath):
            raise CommandError(f'File "{filepath}" does not exist')

        # Map CSV units to model choices
        units_mapping = {
            'ppm': Units.PPM,
            'ppb': Units.PPB,
            '%v/v': Units.VFV,
            '%LEL': Units.VLE,
            'mg/m3': Units.MGM,
            'microgram/m3': Units.MIGM,
        }

        # Map CSV gas to model choices
        gas_mapping = {
            'CO': Gas.CO,
            'H2S': Gas.H2S,
            'VOC': Gas.VOC,
            'LEL': Gas.LEL,
            'O2': Gas.O2,
            'HCN': Gas.HCN,
            'CL2': Gas.CL2,
            'PH3': Gas.PH3,
            'SO2': Gas.SO2,
            'NO2': Gas.NO2,
            'CO2': Gas.CO2,
            'NH3': Gas.NH3,
            'ETO': Gas.ETO,
        }

        with transaction.atomic():
            if clear:
                count = ReadingType.objects.count()
                ReadingType.objects.all().delete()
                self.stdout.write(
                    self.style.WARNING(f'Deleted {count} existing ReadingType records')
                )

            created_count = 0
            updated_count = 0
            skipped_count = 0

            with open(filepath, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)

                for row in reader:
                    gas_value = row.get('gas', '').strip()
                    units_value = row.get('units', '').strip()

                    # Map gas and units to model choices
                    gas_choice = gas_mapping.get(gas_value)
                    units_choice = units_mapping.get(units_value)

                    if not gas_choice:
                        self.stdout.write(
                            self.style.WARNING(
                                f'Skipping row with unknown gas "{gas_value}"'
                            )
                        )
                        skipped_count += 1
                        continue

                    if not units_choice:
                        self.stdout.write(
                            self.style.WARNING(
                                f'Skipping row with unknown units "{units_value}"'
                            )
                        )
                        skipped_count += 1
                        continue

                    # Parse threshold values
                    threshold1 = self._parse_float(row.get('threshold1', ''))
                    threshold2 = self._parse_float(row.get('threshold2', ''))
                    threshold3 = self._parse_float(row.get('threshold3', ''))

                    responder_header = row.get('responder_header', '').strip()

                    # Get or create the ReadingType
                    reading_type, created = ReadingType.objects.update_or_create(
                        gas=gas_choice,
                        units=units_choice,
                        defaults={
                            'threshold1': threshold1,
                            'threshold2': threshold2,
                            'threshold3': threshold3,
                            'responder_header': responder_header,
                        }
                    )

                    if created:
                        created_count += 1
                        self.stdout.write(
                            self.style.SUCCESS(
                                f'Created ReadingType: {gas_choice} ({units_choice})'
                            )
                        )
                    else:
                        updated_count += 1
                        self.stdout.write(
                            self.style.SUCCESS(
                                f'Updated ReadingType: {gas_choice} ({units_choice})'
                            )
                        )

        # Summary
        self.stdout.write(self.style.SUCCESS('\n--- Import Summary ---'))
        self.stdout.write(f'Created: {created_count}')
        self.stdout.write(f'Updated: {updated_count}')
        self.stdout.write(f'Skipped: {skipped_count}')
        self.stdout.write(self.style.SUCCESS('Import completed successfully!'))

    def _parse_float(self, value):
        """Parse a string value to float, return None if empty or invalid."""
        if not value or not value.strip():
            return None
        try:
            return float(value.strip())
        except ValueError:
            return None
