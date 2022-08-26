from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework import routers
from user import views
#from market import views

app_name = 'user'

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)

urlpatterns = [
    # Les URL des API sont déterminées automatiquement par le routeur.
    path('', include(router.urls)),
    # URL personnalisées.
    path('login', views.CustomLoginView.as_view(), name="my_custom_login"),
]
