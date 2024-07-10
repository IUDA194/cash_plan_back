from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q


class EmailOrUsernameModelBackend(ModelBackend):
    """
    This is a ModelBackend that allows authentication with either a username or an email address.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            # Try to fetch the user by searching username or email field
            user = UserModel.objects.filter(Q(username__iexact=username) | Q(email__iexact=username)).first()
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
        else:
            # If the user exists, check the password using the built-in method
            if not user:
                return None
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
