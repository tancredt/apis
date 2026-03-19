import csv
import os
from django.db import transaction
from django.db.models import Q
from .models import Reading, ReadingType, Detector


# Hardcoded path to the fixtures directory and CSV file
FIXTURES_DIR = os.path.join(os.path.dirname(__file__), 'fixtures')
DATALOG_CSV = os.path.join(FIXTURES_DIR, 'DataLog.csv')


def import_datalog(clear=False, batch_size=1000):
    """
    Import Reading data from the hardcoded DataLog CSV file.
    
    Args:
        clear: If True, delete all existing Reading records before importing.
        batch_size: Number of records to create in each batch.
    
    Returns:
        dict: Summary with keys 'created', 'skipped'
    """
    filepath = DATALOG_CSV
    
    if not os.path.exists(filepath):
        raise FileNotFoundError(f'CSV file not found: {filepath}')
    
    with transaction.atomic():
        if clear:
            count = Reading.objects.count()
            Reading.objects.all().delete()
            print(f'Deleted {count} existing Reading records')
        
        # Build a map of responder_header to ReadingType
        reading_type_map = {}
        for rt in ReadingType.objects.all():
            if rt.responder_header:
                reading_type_map[rt.responder_header] = rt
        
        # Map of CSV column headers to responder_header values
        # These should match the responder_header field in ReadingType
        column_to_responder_header = {
            'CO(ppm)': 'CO(ppm)',
            'Custom1(ppm)': 'Custom1(ppm)',
            'H2S(ppm)': 'H2S(ppm)',
            'LEL(%LEL)': 'LEL(%LEL)',
            'O2(%)': 'O2(%)',
        }
        
        # Get the gas columns from the CSV header
        gas_columns = [col for col in column_to_responder_header.keys()]
        
        created_count = 0
        skipped_count = 0
        detector_cache = {}
        readings_to_create = []
        
        with open(filepath, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                serial_number = row.get('SERIAL NUMBER', '').strip()
                log_time = row.get('LOG TIME', '').strip()
                
                if not serial_number or not log_time:
                    skipped_count += 1
                    continue
                
                # Get or cache the detector
                if serial_number not in detector_cache:
                    try:
                        detector = Detector.objects.get(serial=serial_number)
                        detector_cache[serial_number] = detector
                    except Detector.DoesNotExist:
                        detector_cache[serial_number] = None
                
                detector = detector_cache[serial_number]
                
                if detector is None:
                    skipped_count += 1
                    continue
                
                # Process each gas column
                for column in gas_columns:
                    value_str = row.get(column, '').strip()
                    
                    # Skip empty values
                    if not value_str:
                        continue
                    
                    try:
                        value = float(value_str)
                    except ValueError:
                        skipped_count += 1
                        continue
                    
                    # Get the responder_header for this column
                    responder_header = column_to_responder_header.get(column)
                    
                    if not responder_header:
                        skipped_count += 1
                        continue
                    
                    # Get the ReadingType for this responder_header
                    reading_type = reading_type_map.get(responder_header)
                    
                    if not reading_type:
                        skipped_count += 1
                        continue
                    
                    # Create the reading
                    readings_to_create.append(Reading(
                        detector=detector,
                        reading_type=reading_type,
                        value=value,
                        dt=log_time,
                        detector_site=None,
                        is_valid=True,
                    ))
                    
                    created_count += 1
                    
                    # Bulk create in batches
                    if len(readings_to_create) >= batch_size:
                        Reading.objects.bulk_create(readings_to_create)
                        readings_to_create = []
        
        # Create any remaining readings
        if readings_to_create:
            Reading.objects.bulk_create(readings_to_create)
    
    return {
        'created': created_count,
        'skipped': skipped_count,
    }
