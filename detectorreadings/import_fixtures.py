import csv
import os
from django.db import transaction
from .models import ReadingType, Gas, Units


# Hardcoded path to the fixtures directory and CSV file
FIXTURES_DIR = os.path.join(os.path.dirname(__file__), 'fixtures')
READING_TYPES_CSV = os.path.join(FIXTURES_DIR, 'ReadingTypes.csv')


def import_reading_types(clear=False):
    """
    Import ReadingType data from the hardcoded CSV file.
    
    Args:
        clear: If True, delete all existing ReadingType records before importing.
    
    Returns:
        dict: Summary with keys 'created', 'updated', 'skipped'
    """
    filepath = READING_TYPES_CSV
    
    if not os.path.exists(filepath):
        raise FileNotFoundError(f'CSV file not found: {filepath}')
    
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
            ReadingType.objects.all().delete()
        
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
                    skipped_count += 1
                    continue
                
                if not units_choice:
                    skipped_count += 1
                    continue
                
                # Parse threshold values
                threshold1 = _parse_float(row.get('threshold1', ''))
                threshold2 = _parse_float(row.get('threshold2', ''))
                threshold3 = _parse_float(row.get('threshold3', ''))
                
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
                else:
                    updated_count += 1
        
        return {
            'created': created_count,
            'updated': updated_count,
            'skipped': skipped_count,
        }


def _parse_float(value):
    """Parse a string value to float, return None if empty or invalid."""
    if not value or not value.strip():
        return None
    try:
        return float(value.strip())
    except ValueError:
        return None
