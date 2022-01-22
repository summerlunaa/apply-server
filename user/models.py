from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, major, phone_number, student_id, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            major=major,
            phone_number=phone_number,
            student_id=student_id,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, major, phone_number, student_id, password=None):
        user = self.create_user(
            email,
            password=password,
            name=name,
            major=major,
            phone_number=phone_number,
            student_id=student_id,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    email = models.EmailField(max_length=100, unique=True)
    name = models.CharField(max_length=20)
    major = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    student_id = models.CharField(max_length=12)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELD = ['name', 'major', 'phone_number', 'student_id']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True