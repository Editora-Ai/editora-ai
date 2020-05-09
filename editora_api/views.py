from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect, Http404
from .models import BGR
from .serializers import BGRSerializer
from rest_framework import generics


class ListBGR(generics.ListCreateAPIView):
    serializer_class = BGRSerializer

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