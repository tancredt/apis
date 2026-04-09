#!/usr/bin/env python
"""
Management command to export the inventory database to a SQL/text file.

The output file contains SQL statements that can be used to reconstruct
the database data using: python manage.py dbshell < <output_file>

Or the file can be read by the populate_from_export command to repopulate
via Django ORM.

Usage:
    python manage.py export_db [--output FILENAME]
"""

import os
from django.core.management.base import BaseCommand
from django.db import connection
from django.utils import timezone


class Command(BaseCommand):
    help = 'Export the inventory database to a SQL/text file for backup and reconstruction.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--output',
            type=str,
            default=None,
            help='Output file path (default: db_export_YYYYMMDD_HHMMSS.sql in project root)',
        )

    def handle(self, *args, **options):
        output_path = options['output']
        if not output_path:
            timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
            base_dir = os.path.dirname(
                os.path.dirname(
                    os.path.dirname(
                        os.path.dirname(os.path.abspath(__file__))
                    )
                )
            )
            output_path = os.path.join(base_dir, f'db_export_{timestamp}.sql')

        self.stdout.write(f'Exporting database to: {output_path}')

        # Models to export in dependency order
        from inventory.models import (
            Location,
            DetectorModel,
            SensorType,
            DetectorModelConfiguration,
            Detector,
            Sensor,
            SensorSlot,
            Maintenance,
            MaintenanceTask,
            DetectorFault,
            CylinderType,
            Cylinder,
            CylinderFault,
            LocationDetectorSlot,
        )

        export_order = [
            Location,
            DetectorModel,
            SensorType,
            DetectorModelConfiguration,
            Detector,
            Sensor,
            SensorSlot,
            Maintenance,
            MaintenanceTask,
            DetectorFault,
            CylinderType,
            Cylinder,
            CylinderFault,
            LocationDetectorSlot,
        ]

        total_records = 0
        with open(output_path, 'w') as f:
            f.write('-- Database Export for Inventory System\n')
            f.write(f'-- Generated: {timezone.now().strftime("%Y-%m-%d %H:%M:%S")}\n')
            f.write('-- This file contains SQL statements to reconstruct the database.\n')
            f.write('-- Usage: python manage.py dbshell < <this_file>\n\n')

            # Disable foreign key checks during import (SQLite compatible)
            f.write('PRAGMA foreign_keys = OFF;\n\n')

            for model in export_order:
                table_name = model._meta.db_table
                queryset = model.objects.all()
                count = queryset.count()
                total_records += count

                self.stdout.write(f'  Exporting {model.__name__}: {count} records')

                if count == 0:
                    f.write(f'-- No records in {table_name}\n\n')
                    continue

                # Write DELETE statement to clear existing data
                f.write(f'-- Clear existing data in {table_name}\n')
                f.write(f'DELETE FROM {table_name};\n\n')

                # Get database column names (Django adds _id suffix for FK columns)
                columns = []
                for field in model._meta.fields:
                    if field.get_internal_type() == 'ForeignKey':
                        columns.append(f'{field.name}_id')
                    else:
                        columns.append(field.name)
                column_names = ', '.join(columns)

                # Write INSERT statements
                f.write(f'-- Insert records into {table_name}\n')
                for obj in queryset:
                    values = []
                    for field in model._meta.fields:
                        # For ForeignKey, use the _id attribute to get the raw integer ID
                        if field.get_internal_type() == 'ForeignKey':
                            fk_value = getattr(obj, f'{field.name}_id', None)
                            if fk_value is None:
                                values.append('NULL')
                            else:
                                values.append(str(fk_value))
                        else:
                            value = getattr(obj, field.name)

                            if value is None:
                                values.append('NULL')
                            elif field.get_internal_type() in ('CharField', 'TextField', 'DateField', 'DateTimeField'):
                                # Escape single quotes in string values
                                escaped = str(value).replace("'", "''")
                                values.append(f"'{escaped}'")
                            elif field.get_internal_type() in ('DecimalField', 'FloatField'):
                                values.append(str(value))
                            elif field.get_internal_type() == 'BooleanField':
                                values.append('1' if value else '0')
                            else:
                                escaped = str(value).replace("'", "''")
                                values.append(f"'{escaped}'")

                    values_str = ', '.join(values)
                    f.write(f'INSERT INTO {table_name} ({column_names}) VALUES ({values_str});\n')

                f.write('\n')

            # Re-enable foreign key checks
            f.write('PRAGMA foreign_keys = ON;\n')

        self.stdout.write(self.style.SUCCESS(
            f'\nExport complete! Total records: {total_records}'
        ))
        self.stdout.write(self.style.SUCCESS(f'Output file: {output_path}'))
