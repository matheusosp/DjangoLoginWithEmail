from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email required')
        email = self.normalize_email(email)
        user = self.model(email = email, username=email, **extra_fields)
        # criptografa a senha
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
  #      extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('superuser required True')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('staff required True')

        return self._create_user(email,password,**extra_fields)


class CustomUser(AbstractUser):
    email = models.EmailField('Email', unique=True)
    phone = models.CharField('Phone', max_length=15)
    is_staff = models.BooleanField('Member team', default=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone']

    def __str__(self):
        return self.email

    objects = UserManager()