from rest_framework import serializers
from .models import BGR


class BGRSerializer(serializers.ModelSerializer):
    class Meta:
        model = BGR
        fields = ('id', 'owner', 'original_image', 'modified_image',
                  'date_created')