from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils.translation import gettext_lazy as _
from referral.models import ReferralCode, ReferralRelation


class UserType(models.IntegerChoices):
    admin = 1, _("admin")
    patient = 2, _("patient")
    doctor = 3, _("doctor")
    superuser = 4, _("superuser")


class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifier for authentication instead of username.
    """

    def create_user(self, email, referral_token, password=None, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_("Email must be set."))
        email = self.normalize_email(email)

        if referral_token:
            ref_code = ReferralCode.objects.filter(token=referral_token).first()
            if not ref_code:
                raise ValueError(_("Your token is not valid."))

            usages_token = ReferralRelation.objects.filter(refer_token=ref_code)
            if usages_token.exists():
                raise ValueError(_("This referral token has already been used."))

            # Create user
            user = self.model(email=email, **extra_fields)
            user.set_password(password)
            user.save()

            # Create relationship for inviter and invited person
            ReferralRelation.objects.create(
                refer_from=ref_code.creator,
                refer_to=user.user_profile,
                refer_token=ref_code,
            )
        else:
            # Create user without referral token
            user = self.model(email=email, **extra_fields)
            user.set_password(password)
            user.save()

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("type", UserType.superuser.value)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("SuperUser must have is_staff=True"))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("SuperUser must have is_superuser=True"))

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    This is a class to define custom user for accounts app.
    """

    email = models.EmailField(max_length=255, unique=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    type = models.IntegerField(choices=UserType.choices, default=UserType.patient.value)
    referral_token = models.CharField(max_length=32, null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["referral_token"]

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    objects = UserManager()

    def __str__(self):
        return self.email
