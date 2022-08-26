from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework import routers
from housing import views

app_name = 'housing'

router = routers.DefaultRouter()
router.register(r'addresses', views.AddressViewSet)
router.register(r'items', views.ItemViewSet)
router.register(r'listing-agents', views.ListingAgentViewSet)
router.register(r'companies', views.CompanyViewSet)
router.register(r'properties', views.PropertyViewSet)
router.register(r'homes', views.HomeViewSet)

urlpatterns = [
    # Les URL des API sont déterminées automatiquement par le routeur.
    path('', include(router.urls)),

    # URL personnalisées
    path('search-home/', views.SearchHome.as_view(), name="search-home-by"),
    path('get-per-state/', views.GetHomePerState.as_view(), name="get-home-per-state"),
]
