"""
Custom authentication backend to support phone number login
"""
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()


class PhoneNumberBackend(ModelBackend):
    """
    Authenticate using phone number from UserProfile instead of username
    """
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Authenticate user by phone number or username
        """
        try:
            # First try to authenticate with username (for backward compatibility)
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # If username not found, try to find user by phone number
            try:
                from .models import UserProfile
                user_profile = UserProfile.objects.get(phone=username)
                user = user_profile.user
            except UserProfile.DoesNotExist:
                return None
        
        # Check password
        if user and user.check_password(password) and self.user_can_authenticate(user):
            return user
        
        return None
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
