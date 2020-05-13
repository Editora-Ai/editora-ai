from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager, PermissionsMixin
from django.utils import timezone
import datetime


class UserManager(BaseUserManager):

    use_in_migrations = True

    def create_user(self, email, password, firstname="Not defined",
                    lastname="Not defined", company="Not defined"):
        user = self.model(
            email=self.normalize_email(email),
            firstname=firstname,
            lastname=lastname,
            company=company,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password, firstname="Not defined",
                         lastname="Not defined", company="Not defined"):
        user = self.create_user(
            email,
            password=password,
            firstname=firstname,
            lastname=lastname,
            company=company,
        )
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, firstname="Not defined",
                         lastname="Not defined", company="Not defined"):
        user = self.create_user(
            email,
            password=password,
            firstname=firstname,
            lastname=lastname,
            company=company,
        )
        user.is_staff = True
        user.is_superuser = True
        user.has_perm = True
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):

    username = None
    email = models.EmailField(('email address'), unique=True)
    firstname = models.CharField(max_length=100, default="havent set")
    lastname = models.CharField(max_length=100,  default="havent set")
    company = models.CharField(max_length=100,  default="havent set", null=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = 'email'

    def __str__(self):              # __unicode__ on Python 2
        return self.email
