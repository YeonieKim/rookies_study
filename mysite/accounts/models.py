# accounts/models.py
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, id, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not id:
            raise ValueError('The given id must be set')
        # id = self.normalize_id(id)
        user = self.model(id=id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, id, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(id, password, **extra_fields)
    
class CustomUser(AbstractUser): 
    name = models.CharField(max_length=100) 
    id = models.CharField(max_length=100, unique=True, primary_key=True)  # id 필드를 고유하게 설정

    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = ['name']
    # 커스텀 매니저 설정
    objects = CustomUserManager()

    class Meta:
        db_table = 'users'
