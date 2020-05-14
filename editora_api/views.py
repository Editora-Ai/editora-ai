from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect, Http404
from django.utils.crypto import get_random_string
from .models import BGR
from .bgr import Final
from .serializers import AdminBGRSerializer, UserBGRSerializer
from rest_framework import generics
import cv2
import os
from PIL import Image


def bgr_process(image, name, idstr):
    img = Image.open(image)
    modified_img = Final(img)
    cv2.imwrite("media/bgr/modified/" + idstr + "_" + name, modified_img)
    # Remove tempfile
    try:
        os.remove("service_tmp/bgr/bgr_temp.jpg")
    except: pass


class ListBGR(generics.ListCreateAPIView):

    def perform_create(self, serializer):
        file_name = str(self.request.FILES['original_image'].name)
        img = Image.open(self.request.data.get('original_image'))
        img.save('media/bgr/original/' + file_name)
        random_str = get_random_string(length=6)
        bgr_process(image='media/bgr/original/' + file_name,
                    name=file_name, idstr=random_str)
        serializer.save(owner=self.request.user,
                        original_image= 'bgr/original/' + file_name
                       ,modified_image= "bgr/modified/" + random_str + "_" +
                       file_name)

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