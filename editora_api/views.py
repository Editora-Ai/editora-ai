from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect, Http404
from django.utils.crypto import get_random_string
from .serializers import AdminBGRSerializer, UserBGRSerializer, AdminFRSerializer, UserFRSerializer, AdminPRSerializer, UserPRSerializer
from rest_framework import generics, parsers
from editora_service.celery import app
import cv2
import numpy as np
import os
from .models import BGR, FR, PR
from user.models import User


@app.task
def bgr_process(image, name, idstr):
    from .bgr import Final
    obj = BGR.objects.get(img_id=idstr)
    obj.status = "processing"
    obj.save()
    img = cv2.imread(image)
    try:
        modified_img = Final(img)
        cv2.imwrite("media/bgr/modified/" + idstr + "_" + name, modified_img)
        obj.status = "success"
    except:
        obj.status = "failed"
    obj.save()


class ListBGR(generics.ListCreateAPIView):

    def post(self, request):
        info = {}
        for file in self.request.FILES.getlist('original_image'):
            new_task = BGR()
            file_name = str(file.name)
            img = cv2.imdecode(np.fromstring(file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
            AVG = np.mean(img)
            if AVG <185:
                ALPHA = 1+(185-AVG)/100
                BETA = 1000/AVG
                img = np.array(img , np.float32)
                img *=ALPHA
                img +=BETA
                img = np.clip(img, 0 , 255)
                img = np.array(img , np.uint8)
            if AVG >232:
                ALPHA = 1-(AVG-225)/100
                BETA = -1000/AVG
                img = np.array(img , np.float32)
                img *=ALPHA
                img +=BETA
                img = np.clip(img, 0 , 255)
                img = np.array(img , np.uint8)
            random_str = get_random_string(length=6)
            cv2.imwrite('media/bgr/original/' + random_str + "_" + file_name, img)
            new_task.owner = self.request.user
            new_task.original_image = 'bgr/original/' + random_str + "_" + file_name
            new_task.modified_image = "bgr/modified/" + random_str + "_" + file_name
            new_task.img_id= random_str
            new_task.save()
            bgr_process.apply_async(kwargs={'image': 'media/bgr/original/' + random_str + "_" + file_name,
                        'name': file_name, 'idstr': random_str})
            info[file_name] = { 'id': new_task.id, 'url': request.META['HTTP_HOST'] + new_task.modified_image.url }
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
        return UserBGRSerializer

    def perform_destroy(self, instance):
        """
        orig_path = os.path.abspath(instance.original_image.url)
        modif_path = os.path.abspath(instance.modified_image.url)
        try:
            os.remove(orig_path.strip("/"))
        except:
            pass
        try:
            os.remove(modif_path.strip("/"))
        except:
            pass
        """
        instance.delete()


@app.task
def fr_process(image, name, idstr):
    from .face_removal import face_removal
    obj = FR.objects.get(img_id=idstr)
    obj.status = "processing"
    obj.save()
    img = cv2.imread(image)
    try:
        modified_img = face_removal(img)
        cv2.imwrite("media/fr/modified/" + idstr + "_" + name, modified_img)
        obj.status = "success"
    except:
        obj.status = "failed"
    obj.save()


class ListFR(generics.ListCreateAPIView):

    def post(self, request):
        info = {}
        for file in self.request.FILES.getlist('original_image'):
            new_task = FR()
            file_name = str(file.name)
            img = cv2.imdecode(np.fromstring(file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
            random_str = get_random_string(length=6)
            cv2.imwrite('media/fr/original/' + random_str + "_" + file_name, img)
            new_task.owner = self.request.user
            new_task.original_image = 'fr/original/' + random_str + "_" + file_name
            new_task.modified_image = "fr/modified/" + random_str + "_" + file_name
            new_task.img_id= random_str
            new_task.save()
            fr_process.apply_async(kwargs={'image': 'media/fr/original/' + random_str + "_" + file_name,
                        'name': file_name, 'idstr': random_str})
            info[file_name] = { 'id': new_task.id, 'url': request.META['HTTP_HOST'] + new_task.modified_image.url }
        content = {'Message': 'Your task is successfully queued on editora.',
                   'outputs': info,
                   }
        return Response(content, status=status.HTTP_200_OK)

    def get_queryset(self):
        if self.request.user.is_staff:
            return FR.objects.all()
        else:
            return FR.objects.filter(owner=self.request.user)

    def get_serializer_class(self):
        if self.request.user.is_superuser:
            return AdminFRSerializer
        return UserFRSerializer


class DetailFR(generics.RetrieveUpdateDestroyAPIView):

    def get_queryset(self):
        if self.request.user.is_staff:
            return FR.objects.filter(id=self.kwargs.get('pk'))
        else:
            return FR.objects.filter(owner=self.request.user,
                                      id=self.kwargs.get('pk'))

    def get_serializer_class(self):
        if self.request.user.is_superuser:
            return AdminFRSerializer
        return UserFRSerializer

    def perform_destroy(self, instance):
        """
        orig_path = os.path.abspath(instance.original_image.url)
        modif_path = os.path.abspath(instance.modified_image.url)
        try:
            os.remove(orig_path.strip("/"))
        except:
            pass
        try:
            os.remove(modif_path.strip("/"))
        except:
            pass
        """
        instance.delete()


@app.task
def pr_process(image, name, idstr, user_id):
    from .plate_data.Plate_removal import replace_LOGO_on_white_plate
    obj = PR.objects.get(img_id=idstr)
    obj.status = "processing"
    obj.save()
    img = cv2.imread(image)
    if User.objects.get(id=user_id).user_logo:
        logo = cv2.imread('media/' + str(User.objects.get(id=user_id).user_logo))
    else:
        logo = cv2.imread("media/user_r/logos/default.jpg")
    try:
        modified_img = replace_LOGO_on_white_plate(img, logo)
        cv2.imwrite("media/pr/modified/" + idstr + "_" + name, modified_img)
        obj.status = "success"
    except:
        obj.status = "failed"
    obj.save()


class ListPR(generics.ListCreateAPIView):

    def post(self, request):
        info = {}
        for file in self.request.FILES.getlist('original_image'):
            new_task = PR()
            file_name = str(file.name)
            img = cv2.imdecode(np.fromstring(file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
            random_str = get_random_string(length=6)
            cv2.imwrite('media/pr/original/' + random_str + "_" + file_name, img)
            new_task.owner = self.request.user
            new_task.original_image = 'pr/original/' + random_str + "_" + file_name
            new_task.modified_image = "pr/modified/" + random_str + "_" + file_name
            new_task.img_id= random_str
            new_task.save()
            pr_process.apply_async(kwargs={'image': 'media/pr/original/' + random_str + "_" + file_name,
                        'name': file_name, 'idstr': random_str, 'user_id': self.request.user.id})
            info[file_name] = { 'id': new_task.id, 'url': request.META['HTTP_HOST'] + new_task.modified_image.url }
        content = {'Message': 'Your task is successfully queued on editora.',
                   'outputs': info,
                   }
        return Response(content, status=status.HTTP_200_OK)

    def get_queryset(self):
        if self.request.user.is_staff:
            return PR.objects.all()
        else:
            return PR.objects.filter(owner=self.request.user)

    def get_serializer_class(self):
        if self.request.user.is_superuser:
            return AdminPRSerializer
        return UserPRSerializer


class DetailPR(generics.RetrieveUpdateDestroyAPIView):

    def get_queryset(self):
        if self.request.user.is_staff:
            return PR.objects.filter(id=self.kwargs.get('pk'))
        else:
            return PR.objects.filter(owner=self.request.user,
                                      id=self.kwargs.get('pk'))

    def get_serializer_class(self):
        if self.request.user.is_superuser:
            return AdminPRSerializer
        return UserPRSerializer

    def perform_destroy(self, instance):
        """
        orig_path = os.path.abspath(instance.original_image.url)
        modif_path = os.path.abspath(instance.modified_image.url)
        try:
            os.remove(orig_path.strip("/"))
        except:
            pass
        try:
            os.remove(modif_path.strip("/"))
        except:
            pass
        """
        instance.delete()

# Getting filtered image
def get_filtered_image(request, name, is_sensitive):
    image_name = name
    if is_sensitive == "is_sensitive":
        image_url = FR.objects.get(img_id=name).modified_image
    elif is_sensitive == "is_not_sensitive":
        image_url = FR.objects.get(img_id=name).original_image
    return HttpResponseRedirect(image_url.url)