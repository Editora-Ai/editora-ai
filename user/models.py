from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager, PermissionsMixin
from django.utils import timezone
import datetime
from django.core.files.base import ContentFile
from PIL import Image
from io import BytesIO


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
        user.is_active = True
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
    user_logo = models.ImageField(upload_to='user_r/logos', null=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = 'email'

    def save(self):
        if self.user_logo:
            filename = "%s.jpg" % self.user_logo.name.split('.')[0]

            image = Image.open(self.user_logo)
            # for PNG images discarding the alpha channel and fill it with some color
            if image.mode in ('RGBA', 'LA'):
                background = Image.new(image.mode[:-1], image.size, '#fff')
                background.paste(image, image.split()[-1])
                image = background
            image_io = BytesIO()
            image.save(image_io, format='JPEG', quality=100)

            # change the image field value to be the newly modified image value
            self.user_logo.save(filename, ContentFile(image_io.getvalue()), save=False)
        super(User, self).save()

    def __str__(self):              
        return self.email
