from django.db import models
from django.contrib.auth.models import User
import datetime


class BGR(models.Model):
    owner = models.ForeignKey(User, unique=False, on_delete=models.CASCADE)
    original_image = models.ImageField(upload_to='bgr/original')
    modified_image = models.ImageField(upload_to='bgr/modified', null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.owner)
