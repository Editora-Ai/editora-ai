from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect, Http404
from django.utils.crypto import get_random_string
from .models import BGR
from .bgr import Final
from .serializers import BGRSerializer
from rest_framework import generics
import cv2
from PIL import Image

def bgr_process(self, image):
    img = Image.open(image)
    modified_img = Final(img)
    name = get_random_string(length=6)
    cv2.imwrite("media/bgr/modified/" + name + ".jpeg", modified_img)
    return name + ".jpeg"


class ListBGR(generics.ListCreateAPIView):
    serializer_class = BGRSerializer
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user,
                        original_image= self.request.data.get('original_image'),
                        modified_image= "bgr/modified/"
                        + bgr_process(self,
                        image= self.request.data.get('original_image')))

    def get_queryset(self):
        if self.request.user.is_staff:
            return BGR.objects.all()
        else:
            return BGR.objects.filter(owner=self.request.user)


class DetailBGR(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BGRSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return BGR.objects.filter(id=self.kwargs['pk'])
        else:
            return BGR.objects.filter(owner=self.request.user,
                                      id=self.kwargs['pk'])