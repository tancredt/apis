from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import status
import json


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    """
    API endpoint for logging in users.
    """
    permission_classes = [AllowAny]  # Allow access without authentication

    def post(self, request):
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            if username and password:
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return JsonResponse({
                        'success': True,
                        'message': 'Login successful',
                        'user': {
                            'id': user.id,
                            'username': user.username,
                            'email': user.email,
                            'first_name': user.first_name,
                            'last_name': user.last_name
                        }
                    })
                else:
                    return JsonResponse({
                        'success': False,
                        'message': 'Invalid credentials'
                    }, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Username and password are required'
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(csrf_exempt, name='dispatch')
class LogoutView(APIView):
    """
    API endpoint for logging out users.
    """
    def post(self, request):
        try:
            logout(request)
            return JsonResponse({
                'success': True,
                'message': 'Logout successful'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CurrentUserView(APIView):
    """
    API endpoint to get current user info.
    """
    def get(self, request):
        if request.user.is_authenticated:
            return JsonResponse({
                'authenticated': True,
                'user': {
                    'id': request.user.id,
                    'username': request.user.username,
                    'email': request.user.email,
                    'first_name': request.user.first_name,
                    'last_name': request.user.last_name
                }
            })
        else:
            return JsonResponse({
                'authenticated': False,
                'user': None
            })

class CsrfTokenView(APIView):
    """
    API endpoint to get CSRF token for frontend.
    """
    permission_classes = [AllowAny]  # Allow access without authentication

    def get(self, request):
        csrf_token = get_token(request)
        return JsonResponse({
            'csrfToken': csrf_token
        })