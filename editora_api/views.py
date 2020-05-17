from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect, Http404
from django.utils.crypto import get_random_string
from .models import BGR
from .bgr import Final
from .serializers import AdminBGRSerializer, UserBGRSerializer
from rest_framework import generics, parsers
import cv2
import os
from PIL import Image
from editora_service.celery import app


@app.task
def bgr_process(image, name, idstr):
    obj = BGR.objects.get(img_id=idstr)
    obj.status = "processing"
    obj.save()
    img = Image.open(image)
    modified_img = Final(img)
    cv2.imwrite("media/bgr/modified/" + idstr + "_" + name, modified_img)
    obj.status = "success"
    obj.save()
    # Remove tempfile
    try:
        os.remove("service_tmp/bgr/bgr_temp.jpg")
    except: pass


class ListBGR(generics.ListCreateAPIView):

    def post(self, request):
        outputs = []
        ids = []
        info = {}
        for file in self.request.FILES.getlist('original_image'):
            new_task = BGR()
            file_name = str(file.name)
            img = Image.open(file)
            img.save('media/bgr/original/' + file_name)
            random_str = get_random_string(length=6)
            new_task.owner = self.request.user
            new_task.original_image = 'bgr/original/' + file_name
            new_task.modified_image = "bgr/modified/" + random_str + "_" + file_name
            new_task.img_id= random_str
            new_task.save()
            outputs.append(request.META['HTTP_HOST'] + new_task.modified_image.url)
            ids.append(new_task.id)
            bgr_process.apply_async(kwargs={'image': 'media/bgr/original/' + file_name,
                        'name': file_name, 'idstr': random_str})
        for i in ids:
            for x in outputs:
                info[i] = x
        content = {'Message': 'Your task is successfully queued on editora.',
                   'outputs': info,
                   }
        return Response(content, status=status.HTTP_200_OK)

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
        return UserBGRSerialize

    def perform_destroy(self, instance):
        instance.delete()
        orig_path = os.path.abspath(instance.modified_image.url)
        modif_path = os.path.abspath(instance.original_image.url)
        os.remove(orig_path.strip("/"))
        os.remove(modif_path.strip("/"))

