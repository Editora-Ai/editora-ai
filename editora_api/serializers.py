from rest_framework import serializers, generics
from rest_auth.registration.serializers import RegisterSerializer
from rest_auth.registration.views import RegisterView


from .models import BGR


class AdminBGRSerializer(serializers.ModelSerializer):

    class Meta:
        model = BGR
        fields = ('id', 'owner', 'original_image', 'modified_image',
                  'date_created')


class UserBGRSerializer(serializers.ModelSerializer):
    class Meta:
        model = BGR
        fields = ('id', 'original_image', 'modified_image',
                  'date_created')
        read_only_fields = ('id', 'date_created', 'modified_image')



class NameRegistrationSerializer(RegisterSerializer):

  first_name = serializers.CharField(required=False)
  last_name = serializers.CharField(required=False)

  def custom_signup(self, request, user):
    user.first_name = self.validated_data.get('first_name', '')
    user.last_name = self.validated_data.get('last_name', '')
    user.save(update_fields=['first_name', 'last_name'])


class NameRegistrationView(RegisterView):
  serializer_class = NameRegistrationSerializer