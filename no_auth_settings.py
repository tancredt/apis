"""
Settings module to run the Django API without authentication for development/testing purposes.
"""

from apis.settings import *

# Override the REST Framework settings to remove authentication
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [],
    'DEFAULT_PERMISSION_CLASSES': [],
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']
}