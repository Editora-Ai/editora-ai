from rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from rest_auth.serializers import PasswordResetSerializer

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
        user.email = self.validated_data.get('email')
        user.firstname = self.validated_data.get('firstname')
        user.lastname = self.validated_data.get('lastname')
        user.company = self.validated_data.get('company')
        user.save(update_fields=['firstname', 'lastname', 'company', 'email'])


class CustomUserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email','firstname','lastname', 'company')


# For overriding rest_auth default email
class CustomPasswordResetSerializer(PasswordResetSerializer):
    def get_email_options(self):
        return {
            'subject_template_name': 'registration/password_reset_subject.txt',
            'email_template_name': 'registration/password_reset_message.txt',
            'html_email_template_name': 'registration/'
                                    'password_reset_message.html',
        }

    def validate_email(self, value):
        # Create PasswordResetForm with the serializer
        self.reset_form = self.password_reset_form_class(data=self.initial_data)
        if not self.reset_form.is_valid():
            raise serializers.ValidationError(self.reset_form.errors)

        if not get_user_model().objects.filter(email=value).exists():
            raise serializers.ValidationError(_('Invalid e-mail address'))
        
        return value