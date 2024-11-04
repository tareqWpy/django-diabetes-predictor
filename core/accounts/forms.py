from accounts.models import User
from django.contrib.auth.forms import UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    """
    A Custom form inheritanced from UserCreationForm to present only email and passwords (password and repeat password fields).
    """

    class Meta:
        model = User
        fields = ("email", "password1", "password2")
