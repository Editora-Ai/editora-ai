"""editora_service URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.views.generic import RedirectView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from allauth.account.views import confirm_email
from rest_auth.views import PasswordResetConfirmView
from temp_front.views import confirm_email



admin.autodiscover()

schema_view = get_schema_view(
   openapi.Info(
      title="Editora API",
      default_version='v1',
      description="This is the first version of our API for background removal.",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@editoria.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    #### API Related Paths ####
    path('admin/', admin.site.urls),
    path('api/v1/', include('editora_api.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/',
         include('rest_auth.registration.urls')),
    url(r'^account/', include('allauth.urls')),
    path('rest-auth/password/reset/confirm/<uidb64>/<token>/', confirm_email, name="password_reset_confirm"),


    # Editoria Service Documentation
   url(r'^api-docs(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   url(r'^api-docs/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

   #### API Related Paths ####


   #### Front-End Related Paths ####
   path('', include('temp_front.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

