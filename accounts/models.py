from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, phone, username=None, password=None):
        if not phone:
            raise ValueError("phone number is necessary")
        
        user = self.model(phone=phone, username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone=None, username=None, password=None):
        if not username:
            username = 'admin'  # یا هر مقدار پیش‌فرض دیگری که بخواهید
        if not password:
            raise ValueError("رمز عبور الزامی است")

        user = self.create_user(phone=phone, username=username, password=password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=15, unique=True)  # ligin with phone number
    profile_picture = models.ImageField(upload_to="profiles/", blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "phone"  # login with phone number
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone
