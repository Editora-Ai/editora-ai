from django.db import models
#from django.contrib.auth.models import User
from django.conf import settings
import ntpath
import datetime
import os



class BGR(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, unique=False, on_delete=models.CASCADE)
    original_image = models.ImageField(upload_to='bgr/original')
    modified_image = models.ImageField(upload_to='bgr/modified', null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    img_id = models.CharField(max_length=100)

    # Status field
    QUEUED = 'queued'
    SUCCESS = 'success'
    FAILED = 'failed'
    PROCESSING = 'processing'

    STATUS = [
        (QUEUED, 'Queued'),
        (SUCCESS, 'Success'),
        (FAILED, 'Failed'),
        (PROCESSING, 'Processing'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default=QUEUED,
    )

    def original_filename(self):
        return ntpath.basename(str(self.original_image))

    def modified_filename(self, path):
        return ntpath.basename(self.modified_image)

    def __str__(self):
        return (str(self.owner.firstname) + " " + str(self.owner.lastname) + " | " +  str(os.path.basename(str(self.original_image))))  + " | " + str(self.status)
