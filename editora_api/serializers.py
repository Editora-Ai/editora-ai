from rest_framework import serializers, generics
from rest_auth.registration.serializers import RegisterSerializer
from rest_auth.registration.views import RegisterView
from .models import BGR, FR, PR


class AdminBGRSerializer(serializers.ModelSerializer):

    class Meta:
        model = BGR
        fields = ('id', 'img_id', 'status', 'owner', 'original_image', 'modified_image',
                  'date_created')
        read_only_fields = ('id', 'owner', 'img_id', 'date_created', 'modified_image')


class UserBGRSerializer(serializers.ModelSerializer):

    class Meta:
        model = BGR
        fields = ('id', 'status', 'original_image', 'modified_image',
                  'date_created')
        read_only_fields = ('id', 'status', 'owner', 'img_id' , 'date_created', 'modified_image')


class AdminFRSerializer(serializers.ModelSerializer):

    class Meta:
        model = FR
        fields = ('id', 'img_id', 'status', 'owner', 'original_image', 'modified_image',
                  'date_created')
        read_only_fields = ('id', 'owner', 'img_id', 'date_created', 'modified_image')


class UserFRSerializer(serializers.ModelSerializer):

    class Meta:
        model = FR
        fields = ('id', 'status', 'original_image', 'modified_image',
                  'date_created')
        read_only_fields = ('id', 'status', 'owner', 'img_id' , 'date_created', 'modified_image')


class AdminPRSerializer(serializers.ModelSerializer):

    class Meta:
        model = PR
        fields = ('id', 'img_id', 'status', 'owner', 'original_image', 'modified_image',
                  'date_created')
        read_only_fields = ('id', 'owner', 'img_id', 'date_created', 'modified_image')


class UserPRSerializer(serializers.ModelSerializer):

    class Meta:
        model = PR
        fields = ('id', 'status', 'original_image', 'modified_image',
                  'date_created')
        read_only_fields = ('id', 'status', 'owner', 'img_id' , 'date_created', 'modified_image')
