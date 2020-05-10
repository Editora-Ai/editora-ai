from rest_framework import serializers, generics
from .models import BGR


class AdminBGRSerializer(serializers.ModelSerializer):
    class Meta:
        model = BGR
        fields = ('id', 'owner', 'original_image', 'modified_image',
                  'date_created')


class UserBGRSerializer(serializers.ModelSerializer):
    class Meta:
        model = BGR
        fields = ('id', 'owner', 'original_image', 'modified_image',
                  'date_created')
        read_only_fields = ('owner', 'id', 'date_created', 'modified_image')
