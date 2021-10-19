import os
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models, transaction


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email, and password.
        """
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
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


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, db_index=True, blank=True, null=True)
    GENDER_CHOICES = [("M", "Male"), ("F", "Female"), ("D", "Do not specify")]
    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES, null=True, blank=True
    )
    full_name = models.CharField(max_length=100, null=True, blank=True)

    phone_number = models.CharField(unique=True, max_length=20, db_index=True)
    date_of_birth = models.DateField(null=True, blank=True)

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "User"

    @transaction.atomic
    def save(self, *args, **kwargs):
        if not self.full_name:
            self.first_name = self.first_name.capitalize()
            self.last_name = self.last_name.capitalize()
            self.full_name = f"{self.first_name} {self.last_name}"
        else:
            self.full_name = self.full_name.capitalize()

        super(User, self).save(*args, **kwargs)


class Driver(models.Model):
    user: User = models.OneToOneField(
        User, related_name="driver_profile", on_delete=models.CASCADE
    )
    is_verified = models.BooleanField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.full_name


class Customer(models.Model):
    user: User = models.OneToOneField(
        User, related_name="customer_profile", on_delete=models.CASCADE
    )
    is_verified = models.BooleanField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.full_name


def get_user_document_path(_, filename):
    return os.path.join("images/documents/", filename)


class DriverDocument(models.Model):
    driver: Driver = models.ForeignKey(
        Driver, on_delete=models.CASCADE, related_name="documents"
    )
    image = models.ImageField(upload_to=get_user_document_path)

    def __str__(self):
        return self.driver


class CustomerDocument(models.Model):
    customer: Customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="documents"
    )
    image = models.ImageField(upload_to=get_user_document_path)

    def __str__(self):
        return self.customer
