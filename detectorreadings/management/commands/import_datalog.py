from django.core.management.base import BaseCommand, CommandError
from detectorreadings.import_datalog import import_datalog, DATALOG_CSV
import os


class Command(BaseCommand):
    help = 'Import Reading data from the hardcoded DataLog CSV file (detectorreadings/fixtures/DataLog.csv)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear all existing Reading records before importing'
        )

    def handle(self, *args, **options):
        clear = options['clear']
        filepath = DATALOG_CSV

        # Check if file exists
        if not os.path.exists(filepath):
            raise CommandError(f'File "{filepath}" does not exist')

        self.stdout.write(f'Importing DataLog from: {filepath}')
        
        if clear:
            self.stdout.write(
                self.style.WARNING('WARNING: This will delete all existing Reading records!')
            )

        result = import_datalog(clear=clear)

        # Summary
        self.stdout.write(self.style.SUCCESS('\n--- Import Summary ---'))
        self.stdout.write(f'Created: {result["created"]}')
        self.stdout.write(f'Skipped: {result["skipped"]}')
        self.stdout.write(self.style.SUCCESS('Import completed successfully!'))
