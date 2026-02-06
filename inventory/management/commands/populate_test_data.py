from django.core.management.base import BaseCommand
from inventory.models import (
    Location, LocationType, DetectorModel, DetectorType, Manufacturer, Supplier,
    SensorType, SensorGas, MaintenanceType, CylinderType, Cylinder, CylinderGas, CylinderVolume, CylinderUnit,
    DetectorModelConfiguration
)


class Command(BaseCommand):
    help = 'Populate database with test data for detectormodels, locations, sensortypes, cylindertypes and detectormodelconfigurations'

    def handle(self, *args, **options):
        self.stdout.write('Starting to populate test data...')
        
        # Create Locations
        self.stdout.write('Creating locations...')
        locations_data = [
            {'label': 'ST001', 'address': '123 Main St, Sydney NSW', 'location_type': LocationType.STATION},
            {'label': 'ST002', 'address': '456 Oak Ave, Melbourne VIC', 'location_type': LocationType.STATION},
            {'label': 'WH001', 'address': '789 Industrial Blvd, Brisbane QLD', 'location_type': LocationType.WAREHOUSE},
            {'label': 'DO001', 'address': '321 Admin Rd, Perth WA', 'location_type': LocationType.DISTRICT_OFFICE},
            {'label': 'AP001', 'address': '654 Fire Station, Adelaide SA', 'location_type': LocationType.APPLIANCE},
        ]
        
        for loc_data in locations_data:
            Location.objects.get_or_create(**loc_data)
        
        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(locations_data)} locations'))

        # Create Detector Models
        self.stdout.write('Creating detector models...')
        detector_models_data = [
            {
                'manufacturer': Manufacturer.HONEYWELL,
                'detector_type': DetectorType.PID,
                'supplier': Supplier.MSA,
                'model_name': 'MultiRAE Lite',
                'part_number': 'MR-LITE-001'
            },
            {
                'manufacturer': Manufacturer.HONEYWELL,
                'detector_type': DetectorType.PID,
                'supplier': Supplier.MSA,
                'model_name': 'MiniRAE 3000',
                'part_number': 'MINI-3000-002'
            },
            {
                'manufacturer': Manufacturer.HONEYWELL,
                'detector_type': DetectorType.PID,
                'supplier': Supplier.MSA,
                'model_name': 'MicroRAE',
                'part_number': 'MICRO-RAE-003'
            },
            {
                'manufacturer': Manufacturer.HONEYWELL,
                'detector_type': DetectorType.PUMPED_MULTI,
                'supplier': Supplier.MSA,
                'model_name': 'AutoRAE Plus',
                'part_number': 'AUTO-PLUS-004'
            },
        ]
        
        for model_data in detector_models_data:
            DetectorModel.objects.get_or_create(**model_data)
        
        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(detector_models_data)} detector models'))

        # Create Sensor Types first (before configurations that reference them)
        self.stdout.write('Creating sensor types...')
        sensor_types_data = [
            {
                'manufacturer': Manufacturer.HONEYWELL,
                'part_number': 'CO-SENSOR-001',
                'active': True,
                'sensorgas': SensorGas.CO,
                'compatible_detectormodels': '1,2,3',  # Comma-separated IDs of compatible detector models
                'warranty_months': 12,
                'expiry_months': 24
            },
            {
                'manufacturer': Manufacturer.MSA,
                'part_number': 'H2S-SENSOR-002',
                'active': True,
                'sensorgas': SensorGas.H2S,
                'compatible_detectormodels': '1,3',
                'warranty_months': 12,
                'expiry_months': 36
            },
            {
                'manufacturer': Manufacturer.DRAEGER,
                'part_number': 'O2-SENSOR-003',
                'active': True,
                'sensorgas': SensorGas.O2,
                'compatible_detectormodels': '2,4',
                'warranty_months': 12,
                'expiry_months': 24
            },
            {
                'manufacturer': Manufacturer.PROENGIN,
                'part_number': 'LEL-SENSOR-004',
                'active': True,
                'sensorgas': SensorGas.LEL,
                'compatible_detectormodels': '1,4',
                'warranty_months': 12,
                'expiry_months': 36
            },
            {
                'manufacturer': Manufacturer.THERMO,
                'part_number': 'VOC-SENSOR-005',
                'active': True,
                'sensorgas': SensorGas.VOC,
                'compatible_detectormodels': '1,2,3,4',
                'warranty_months': 12,
                'expiry_months': 24
            },
        ]
        
        for sensor_data in sensor_types_data:
            SensorType.objects.get_or_create(**sensor_data)
        
        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(sensor_types_data)} sensor types'))

        # Create Detector Model Configurations
        self.stdout.write('Creating detector model configurations...')
        detector_configs_data = [
            {
                'detector_model_id': 1,  # MultiRAE Lite
                'label': 'Blue',
                'sensor_partnumbers': 'CO-SENSOR-001,H2S-SENSOR-002,O2-SENSOR-003'
            },
            {
                'detector_model_id': 1,  # MultiRAE Lite
                'label': 'Red',
                'sensor_partnumbers': 'CO-SENSOR-001,LEL-SENSOR-004,VOC-SENSOR-005'
            },
            {
                'detector_model_id': 2,  # MiniRAE 3000
                'label': 'Standard',
                'sensor_partnumbers': 'H2S-SENSOR-002,O2-SENSOR-003'
            },
            {
                'detector_model_id': 3,  # MicroRAE
                'label': 'Industrial',
                'sensor_partnumbers': 'CO-SENSOR-001,H2S-SENSOR-002,O2-SENSOR-003,LEL-SENSOR-004'
            },
            {
                'detector_model_id': 4,  # AutoRAE Plus
                'label': 'Portable',
                'sensor_partnumbers': 'VOC-SENSOR-005,O2-SENSOR-003'
            },
        ]
        
        for config_data in detector_configs_data:
            # Get the detector model instance
            detector_model = DetectorModel.objects.get(id=config_data.pop('detector_model_id'))
            DetectorModelConfiguration.objects.get_or_create(
                detector_model=detector_model,
                label=config_data['label'],
                sensor_partnumbers=config_data['sensor_partnumbers']
            )
        
        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(detector_configs_data)} detector model configurations'))


        # Create Cylinder Types
        self.stdout.write('Creating cylinder types...')
        cylinder_types_data = [
            {
                'part_number': 'CYL-CO-001',
                'supplier': Supplier.AES,
                'volume': CylinderVolume.L34,
                'percent_error': 2.0,
                'expiry_months': 24,
                'balance_gas': CylinderGas.N2,
                'active': True,
                'cylinder_1_gas': CylinderGas.CO,
                'cylinder_1_conc': 50.0,
                'cylinder_1_units': CylinderUnit.PPM,
                'cylinder_2_gas': '',
                'cylinder_2_conc': None,
                'cylinder_2_units': ''
            },
            {
                'part_number': 'CYL-H2S-002',
                'supplier': Supplier.MSA,
                'volume': CylinderVolume.L65,
                'percent_error': 2.0,
                'expiry_months': 12,
                'balance_gas': CylinderGas.N2,
                'active': True,
                'cylinder_1_gas': CylinderGas.H2S,
                'cylinder_1_conc': 25.0,
                'cylinder_1_units': CylinderUnit.PPM,
                'cylinder_2_gas': '',
                'cylinder_2_conc': None,
                'cylinder_2_units': ''
            },
            {
                'part_number': 'CYL-O2-003',
                'supplier': Supplier.DRAEGER,
                'volume': CylinderVolume.L103,
                'percent_error': 1.5,
                'expiry_months': 18,
                'balance_gas': CylinderGas.N2,
                'active': True,
                'cylinder_1_gas': CylinderGas.O2,
                'cylinder_1_conc': 16.0,
                'cylinder_1_units': CylinderUnit.PERCENTVOLUMNE,
                'cylinder_2_gas': '',
                'cylinder_2_conc': None,
                'cylinder_2_units': ''
            },
            {
                'part_number': 'CYL-MIX-004',
                'supplier': Supplier.AES,
                'volume': CylinderVolume.L112,
                'percent_error': 2.5,
                'expiry_months': 24,
                'balance_gas': CylinderGas.N2,
                'active': True,
                'cylinder_1_gas': CylinderGas.CO,
                'cylinder_1_conc': 100.0,
                'cylinder_1_units': CylinderUnit.PPM,
                'cylinder_2_gas': CylinderGas.H2S,
                'cylinder_2_conc': 50.0,
                'cylinder_2_units': CylinderUnit.PPM
            },
        ]
        
        for cyl_data in cylinder_types_data:
            CylinderType.objects.get_or_create(**cyl_data)

        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(cylinder_types_data)} cylinder types'))

        # Create Cylinders
        self.stdout.write('Creating cylinders...')
        cylinders_data = [
            {
                'serial': 'CYL-SER-001',
                'cylinder_type_id': 1,  # CYL-CO-001
                'location_id': 1,  # ST001
                'status': 'OP',  # Operational
                'order_date': '2023-01-15',
                'receive_date': '2023-02-01',
                'expiry_date': '2025-02-01',
                'operational_date': '2023-02-02',
                'empty_date': None
            },
            {
                'serial': 'CYL-SER-002',
                'cylinder_type_id': 2,  # CYL-H2S-002
                'location_id': 2,  # ST002
                'status': 'IS',  # In Stock
                'order_date': '2023-03-10',
                'receive_date': '2023-04-05',
                'expiry_date': '2024-04-05',
                'operational_date': None,
                'empty_date': None
            },
            {
                'serial': 'CYL-SER-003',
                'cylinder_type_id': 3,  # CYL-O2-003
                'location_id': 3,  # WH001
                'status': 'OO',  # On Order
                'order_date': '2023-05-20',
                'receive_date': None,
                'expiry_date': '2026-05-20',
                'operational_date': None,
                'empty_date': None
            },
            {
                'serial': 'CYL-SER-004',
                'cylinder_type_id': 4,  # CYL-MIX-004
                'location_id': 4,  # DO001
                'status': 'MT',  # Empty
                'order_date': '2022-11-05',
                'receive_date': '2022-12-01',
                'expiry_date': '2024-12-01',
                'operational_date': '2022-12-02',
                'empty_date': '2024-01-15'
            },
            {
                'serial': 'CYL-SER-005',
                'cylinder_type_id': 1,  # CYL-CO-001
                'location_id': 5,  # AP001
                'status': 'OP',  # Operational
                'order_date': '2023-06-12',
                'receive_date': '2023-07-01',
                'expiry_date': '2025-07-01',
                'operational_date': '2023-07-02',
                'empty_date': None
            },
        ]

        for cyl_data in cylinders_data:
            # Get the foreign key objects
            cylinder_type = CylinderType.objects.get(id=cyl_data.pop('cylinder_type_id'))
            location = Location.objects.get(id=cyl_data.pop('location_id'))

            # Find the next available cylinder number
            from django.db import models
            from django.db import transaction
            with transaction.atomic():
                last_cylinder = Cylinder.objects.select_for_update().aggregate(models.Max('cylinder_number'))
                next_number = (last_cylinder['cylinder_number__max'] or 0) + 1

            # Create or get the cylinder with the next available number
            cylinder, created = Cylinder.objects.get_or_create(
                serial=cyl_data['serial'],  # Use serial as unique identifier for get_or_create
                defaults={
                    'cylinder_number': next_number,  # Assign the next available number
                    'cylinder_type': cylinder_type,
                    'location': location,
                    'status': cyl_data['status'],
                    'order_date': cyl_data['order_date'],
                    'receive_date': cyl_data['receive_date'],
                    'expiry_date': cyl_data['expiry_date'],
                    'operational_date': cyl_data['operational_date'],
                    'empty_date': cyl_data['empty_date']
                }
            )

        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(cylinders_data)} cylinders'))

        self.stdout.write(
            self.style.SUCCESS('Successfully populated all test data!')
        )