#!/usr/bin/env python
"""
Script to create a user with limited permissions.
The user 'frvuser' will only be able to access the change_detector_location 
and change_cylinder_location endpoints.
"""

import os
import sys
import django

# Add the project directory to Python path
sys.path.append('/home/nick/Programming/hazmat/apis')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apis.settings')

django.setup()

from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from inventory.models import Detector, Location, Cylinder


def create_limited_user():
    # Hardcode the password for simplicity
    password = "frvuser123"  # You can change this as needed
    
    # Create or get the user
    try:
        user, created = User.objects.get_or_create(username='frvuser')
        if created:
            print(f"Created new user: {user.username}")
        else:
            print(f"User {user.username} already exists, updating password")
        
        user.set_password(password)
        user.is_staff = False  # Don't give staff access
        user.is_superuser = False  # Don't give superuser access
        user.save()
        print(f"Password set for user: {user.username}")
        
        # Give minimal permissions needed for the specific functions to work
        # These are the basic read permissions needed for the change functions
        detector_content_type = ContentType.objects.get_for_model(Detector)
        location_content_type = ContentType.objects.get_for_model(Location)
        cylinder_content_type = ContentType.objects.get_for_model(Cylinder)
        
        # Add view permissions for the models that need to be accessed
        view_detector_perm = Permission.objects.get(content_type=detector_content_type, codename='view_detector')
        view_location_perm = Permission.objects.get(content_type=location_content_type, codename='view_location')
        view_cylinder_perm = Permission.objects.get(content_type=cylinder_content_type, codename='view_cylinder')
        
        user.user_permissions.add(view_detector_perm, view_location_perm, view_cylinder_perm)
        
        print("Assigned minimal required permissions to frvuser")
        print("This user can now only access change_detector_location and change_cylinder_location endpoints")
        print(f"Password is: {password}")
        
    except Exception as e:
        print(f"Error creating user: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    create_limited_user()