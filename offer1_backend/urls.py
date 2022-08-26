"""zebest_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import include, path, re_path
from django.contrib import admin
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.static import serve
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import permissions
from user.views import *
from django.conf.urls.static import static
from allauth.account.views import confirm_email as allauthemailconfirmation
from dj_rest_auth.views import LoginView
from dj_rest_auth.registration.views import VerifyEmailView, RegisterView
from rest_framework.documentation import include_docs_urls
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

import os


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def api_root(request, format=None):
    """
    APIs Links
    """
    return Response({
        'USER APIs': "https://backend-offer1-interview.herokuapp.com/user-api/",
        'HOUSING APIs': "https://backend-offer1-interview.herokuapp.com/housing-api/",
    })


schema_view = get_schema_view(
    openapi.Info(
        title="Offer1 Interview exercise API",
        default_version='v0',
        description="API description",
        # terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="victorilome@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path('admin-offer1/', admin.site.urls),
    path('housing-api/', include('housing.urls')),
    path('user-api/', include('user.urls')),
    path('api/auth/', include('rest_framework.urls')),
    path('api-token-auth/', CustomAuthToken.as_view()),
    re_path(r'^', include('django.contrib.auth.urls')),
    path('auth/', include('dj_rest_auth.urls')),
    re_path(r'^rest-auth/registration/account-confirm-email/(?P<key>.+)/$',
            allauthemailconfirmation, name="account_confirm_email"),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
    path('registration/', RegisterView.as_view(), name='account_signup'),
    path('login/', LoginView.as_view(), name='account_login'),
    path('accounts/', include('allauth.urls')),
    path('docs/', include_docs_urls(title='Offer1 interview API Documentation', public=False)),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger',
                                               cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc',
                                             cache_timeout=0), name='schema-redoc'),
    path('', api_root)
]

# This is only needed when using runserver.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
