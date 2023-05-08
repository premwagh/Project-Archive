"""
User model defined here.
"""
from django.apps import apps
from django.db import models
from django.contrib.auth.models import (
    AbstractUser, UserManager as DjUserManager, make_password)
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from phonenumber_field.modelfields import PhoneNumberField

# from core.db.models.fields import CaseInsensitiveEmailField
from core.db.models.mixins import (
    TimeStampModelMixin,
    TokenVerificationMixin,
)
from .settings import user_settings


class UserManager(DjUserManager):

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        email = self.normalize_email(email)
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        email = GlobalUserModel.normalize_username(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(email, password, **extra_fields)


class User(TokenVerificationMixin, TimeStampModelMixin, AbstractUser):
    """
    Class implementing a custom user model.
    """
    class RoleChoices(models.TextChoices):
        STUDENT = "student", _("Student")
        FACULTY = "faculty", _("Faculty")

    email = models.EmailField(_('Email'), unique=True, db_index=True,)
    phone_number = PhoneNumberField(
        _('Phone Number'), unique=True, max_length=16)
    first_name = models.CharField(
        _('First Name'), max_length=50, blank=True, null=True)
    last_name = models.CharField(
        _('Last Name'), max_length=50, blank=True, null=True)
    date_of_birth = models.DateField(
        null=True, blank=True, default=None, db_index=True)
    address = models.TextField(
        _('Address'), max_length=255, blank=True, null=True)
    city = models.CharField(_('City'), max_length=50, blank=True, null=True)
    state = models.CharField(_('State'), max_length=50, blank=True, null=True)
    country = models.CharField(
        _('Country'), max_length=50, blank=True, null=True)
    zip_code = models.CharField(
        _('Zip code'), max_length=20, blank=True, null=True)
    is_email_verified = models.BooleanField('Is Email Verified', default=False)
    role = models.CharField(
        _('User Type'), choices=RoleChoices.choices, default=RoleChoices.STUDENT)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']
    username = None

    def __str__(self):
        return self.email

    def get_password_reset_token(self, ttl):
        return self._get_token(
            context_fields=('email', 'password'),
            token_type='password_reset',
            ttl=ttl,
        )

    def get_email_verification_token(self, ttl):
        return self._get_token(
            context_fields=('id', 'email'),
            token_type='email_verification',
            ttl=ttl,
        )

    @classmethod
    def get_object_from_password_reset_token(cls, token):
        return cls._get_object_from_token(('email', 'password'), 'password_reset', token)

    @classmethod
    def get_object_from_email_verification_token(cls, token):
        return cls._get_object_from_token(('id', 'email'), 'email_verification', token)


class Student(User):

    class DepartmentChoices(models.TextChoices):
        INFORMATION_TECHNOLOGY = "information_technology", _(
            "Information Technology")
        COMPUTER_SCIENCE = "computer_science", _("Computer Science")
        ELECTRONICS = "electronics", _("Electronics and Telecommunication")
        ELECTRICAL = "electrical", _("Electrical")
        MECHANICAL = "mechanical", _("Mechanical")
        CIVIL = "civil", _("Civil")

    user_ptr = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='student_profile',
        parent_link=True,
        primary_key=True,
    )
    enrolment_number = models.CharField(_('Email'), unique=True, db_index=True)
    department = models.CharField(_('Email'), choices=DepartmentChoices.choices)
    project_group = models.ForeignKey(
        'project.ProjectGroup',
        verbose_name=_('Project Group'),
        on_delete=models.SET_NULL,
        related_name='students',
        limit_choices_to={"role": User.RoleChoices.FACULTY},
        null=True,
        blank=True,
    )

class Faculty(User):

    class DepartmentChoices(models.TextChoices):
        INFORMATION_TECHNOLOGY = "information_technology", _(
            "Information Technology")
        COMPUTER_SCIENCE = "computer_science", _("Computer Science")
        ELECTRONICS = "electronics", _("Electronics and Telecommunication")
        ELECTRICAL = "electrical", _("Electrical")
        MECHANICAL = "mechanical", _("Mechanical")
        CIVIL = "civil", _("Civil")

    user_ptr = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='faculty_profile',
        parent_link=True,
        primary_key=True,
    )
    department = models.CharField(_('Email'), choices=DepartmentChoices.choices)
