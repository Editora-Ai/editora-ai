from rest_framework import serializers, generics
from rest_auth.registration.serializers import RegisterSerializer
from rest_auth.registration.views import RegisterView


from .models import BGR


class AdminBGRSerializer(serializers.ModelSerializer):
    """
    original_image = serializers.ListField(
                                child=serializers.ImageField(max_length=100000,
                                                  allow_null=False,)
    )
    """
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
        read_only_fields = ('id', 'status' 'owner', 'img_id' , 'date_created', 'modified_image')
