from rest_framework import permissions

class FrvUserRestrictedPermission(permissions.BasePermission):
    """
    Permission class that restricts 'frvuser' to only specific endpoints
    """
    
    def has_permission(self, request, view):
        # First, ensure the user is authenticated
        if not request.user or not request.user.is_authenticated:
            return False
            
        # Check if the current user is 'frvuser'
        if request.user.username == 'frvuser':
            # Allow access only to specific endpoints
            allowed_endpoints = [
                'change_detector_location',
                'change_cylinder_location',
            ]
            
            # Check if the current endpoint is in the allowed list
            if hasattr(request, 'resolver_match') and request.resolver_match:
                url_name = request.resolver_match.url_name
                if url_name in allowed_endpoints:
                    return True
                # If it's not an allowed endpoint, deny access for frvuser
                return False
        
        # For other authenticated users, allow normal access
        return True