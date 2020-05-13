from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect, Http404
from django.utils.crypto import get_random_string
from .models import BGR
from .bgr import Final
from .serializers import AdminBGRSerializer, UserBGRSerializer
from rest_framework import generics
import cv2
from PIL import Image

def bgr_process(self, image, name):
    img = Image.open(image)
    modified_img = Final(img)
    cv2.imwrite("media/bgr/modified/" + name, modified_img)


class ListBGR(generics.ListCreateAPIView):

    def perform_create(self, serializer):
        file_name = str(self.request.FILES['original_image'].name)
        bgr_process(self, image= self.request.data.get('original_image'),
                    name= file_name)
        serializer.save(owner=self.request.user,
                        original_image= self.request.data.get('original_image')
                       ,modified_image= "bgr/modified/" + file_name
        )
    def get_queryset(self):
        if self.request.user.is_staff:
            return BGR.objects.all()
        else:
            return BGR.objects.filter(owner=self.request.user)

    def get_serializer_class(self):
        if self.request.user.is_superuser:
            return AdminBGRSerializer
        return UserBGRSerializer

class DetailBGR(generics.RetrieveUpdateDestroyAPIView):

    def get_queryset(self):
        if self.request.user.is_staff:
            return BGR.objects.filter(id=self.kwargs.get('pk'))
        else:
            return BGR.objects.filter(owner=self.request.user,
                                      id=self.kwargs.get('pk'))

    def get_serializer_class(self):
        if self.request.user.is_superuser:
            return AdminBGRSerializer
        return UserBGRSerializer