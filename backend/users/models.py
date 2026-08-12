from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, email, name, phone, role, password=None):
        if not email:
            raise ValueError("Please enter your Email!")
        user = self.model(
            email=self.normalize_email(email),
            name=name,
            phone=phone,
            role=role,
        )
        user.set_password(password)  # Django hashes with PBKDF2 (equivalent role to bcrypt)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, phone, role, password=None):
        user = self.create_user(email, name, phone, role, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ("Job Seeker", "Job Seeker"),
        ("Employer", "Employer"),
    )

    name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "phone", "role"]

    objects = UserManager()

    def __str__(self):
        return self.email
