from rest_framework import serializers, generics
from rest_auth.registration.serializers import RegisterSerializer
from rest_auth.registration.views import RegisterView


from .models import BGR


class AdminBGRSerializer(serializers.ModelSerializer):

    class Meta:
        model = BGR
        fields = ('id', 'owner', 'original_image', 'modified_image',
                  'date_created')
        read_only_fields = ('id', 'owner', 'date_created', 'modified_image')


class UserBGRSerializer(serializers.ModelSerializer):
    class Meta:
        model = BGR
        fields = ('id', 'original_image', 'modified_image',
                  'date_created')
        read_only_fields = ('id', 'owner', 'date_created', 'modified_image')
