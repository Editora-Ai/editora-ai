from rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model


User = get_user_model()

class CustomRegisterSerializer(RegisterSerializer):

    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(write_only=True)
    firstname = serializers.CharField(required=True)
    lastname = serializers.CharField(required=True)
    company = serializers.CharField(required=False)

    def get_cleaned_data(self):
        super(CustomRegisterSerializer, self).get_cleaned_data()

        return {
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'firstname': self.validated_data.get('firstname', ''),
            'lastname': self.validated_data.get('lastname', ''),
            'company': self.validated_data.get('company', ''),
        }
    def custom_signup(self, request, user):
        user.firstname = self.validated_data.get('firstname')
        user.lastname = self.validated_data.get('lastname')
        user.company = self.validated_data.get('company')
        user.save(update_fields=['firstname', 'lastname', 'company',])


class CustomUserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email','firstname','lastname', 'company')
        read_only_fields = ('email',)