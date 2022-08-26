from rest_framework.response import Response
from rest_framework import permissions, renderers, viewsets, status
from django.http import JsonResponse
from rest_framework.exceptions import APIException
from django.core.mail import send_mail
from django.db.models import Q, Sum, Count
from .models import *
from .serializers import *
from user.serializers import UserSerializer
from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.utils import timezone
import datetime
from django.conf import settings
from django.http import JsonResponse
import traceback
import logging
import math
import decimal

logger = logging.getLogger(__name__)


class AddressViewSet(viewsets.ModelViewSet):
    """
    CRUD Address
    """
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = AddressSerializer
    queryset = Address.objects.all()

    def perform_create(self, serializer):
        try:
          serializer.save()
        except Exception as e:
            traceback.print_exc()
            return Response(data={"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
          
    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = AddressSerializer(
                instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(**serializer.validated_data)
            print(serializer.data)
            return Response(serializer.data)
        except Exception as e:
            print(str(e))
            traceback.print_exc()
            return Response(data={'error_message': str(e)})


class ItemViewSet(viewsets.ModelViewSet):
    """
    CRUD Item
    """
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = ItemSerializer
    queryset = Item.objects.all()

    def perform_create(self, serializer):
        try:
          serializer.save()
        except Exception as e:
            traceback.print_exc()
            return Response(data={"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = ItemSerializer(
                instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(**serializer.validated_data)
            print(serializer.data)
            return Response(serializer.data)
        except Exception as e:
            print(str(e))
            traceback.print_exc()
            return Response(data={'error_message': str(e)})


class ListingAgentViewSet(viewsets.ModelViewSet):
    """
    CRUD ListingAgent
    """
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = ListingAgentSerializer
    queryset = ListingAgent.objects.all()

    def perform_create(self, serializer):
        try:
          serializer.save()
        except Exception as e:
            traceback.print_exc()
            return Response(data={"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = ListingAgentSerializer(
                instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(**serializer.validated_data)
            print(serializer.data)
            return Response(serializer.data)
        except Exception as e:
            print(str(e))
            traceback.print_exc()
            return Response(data={'error_message': str(e)})


class CompanyViewSet(viewsets.ModelViewSet):
    """
    CRUD Company
    """
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = CompanySerializer
    queryset = Company.objects.all()

    def perform_create(self, serializer):
        try:
          serializer.save()
        except Exception as e:
            traceback.print_exc()
            return Response(data={"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = CompanySerializer(
                instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(**serializer.validated_data)
            print(serializer.data)
            return Response(serializer.data)
        except Exception as e:
            print(str(e))
            traceback.print_exc()
            return Response(data={'error_message': str(e)})


class PropertyViewSet(viewsets.ModelViewSet):
    """
    CRUD Property
    """
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = PropertySerializer
    queryset = Property.objects.all()

    def perform_create(self, serializer):
        try:
          serializer.save()
        except Exception as e:
            traceback.print_exc()
            return Response(data={"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = PropertySerializer(
                instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(**serializer.validated_data)
            print(serializer.data)
            return Response(serializer.data)
        except Exception as e:
            print(str(e))
            traceback.print_exc()
            return Response(data={'error_message': str(e)})


class HomeViewSet(viewsets.ModelViewSet):
    """
    CRUD Home
    """
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = HomeSerializer
    queryset = Home.objects.all()

    def perform_create(self, serializer):
        try:
          serializer.save()
        except Exception as e:
            traceback.print_exc()
            return Response(data={"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = HomeSerializer(
                instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(**serializer.validated_data)
            print(serializer.data)
            return Response(serializer.data)
        except Exception as e:
            print(str(e))
            traceback.print_exc()
            return Response(data={'error_message': str(e)})


class SearchHome(APIView):
  """Search house by _city_&min=_price_&max=_price_&bmin=_number_of_bedroom_&bmax=_number_of_bedroom_"""
  
  permission_classes = [permissions.AllowAny,]
  
  def get(self, request, format=None):
    
    homes=city=min=max=bmin=bmax=None
    
    if 'city' in request.query_params:
      city = request.query_params.get('city')
    if 'min' in request.query_params:
      min = request.query_params.get('min')
    if 'max' in request.query_params:
      max = request.query_params.get('max')
    if 'bmin' in request.query_params:
      bmin = request.query_params.get('bmin')
    if 'bmax' in request.query_params:
      bmax = request.query_params.get('bmax')
      
    
    if city is not None:
      if min is not None:
        if max is not None:
          if bmin is not None:
            if bmax is not None:
              homes = Home.objects.filter(property__address__city=city, price__gte=min, price__lte=max, property__number_bedroom__gte=bmin,
                                          property__number_bedroom__lte=bmax)
            else:
              homes = Home.objects.filter(property__address__city=city, price__gte=min, price__lte=max, property__number_bedroom__gte=bmin)
          else:  #bmin None
            if bmax is not None:
              homes = Home.objects.filter(property__address__city=city, price__gte=min, price__lte=max, property__number_bedroom__lte=bmax)
            else:
              homes = Home.objects.filter(property__address__city=city, price__gte=min, price__lte=max)
        else: #max None
          if bmin is not None:
            if bmax is not None:
              homes = Home.objects.filter(property__address__city=city, price__gte=min, property__number_bedroom__gte=bmin,
                                          property__number_bedroom__lte=bmax)
            else:
              homes = Home.objects.filter(property__address__city=city, price__gte=min, property__number_bedroom__gte=bmin)
          else: #bmin and max None
            if bmax is not None:
              homes = Home.objects.filter(property__address__city=city, price__gte=min,property__number_bedroom__lte=bmax)
            else: #max and bmin and bmax None
              homes = Home.objects.filter(property__address__city=city, price__gte=min)
      else: #min None
        if max is not None:
          if bmin is not None:
            if bmax is not None:
              homes = Home.objects.filter(property__address__city=city, price__lte=max, property__number_bedroom__gte=bmin,
                                          property__number_bedroom__lte=bmax)
            else: #min and bmax None
              homes = Home.objects.filter(property__address__city=city, price__lte=max, property__number_bedroom__gte=bmin)
          else: #min and bmin None
            if bmax is not None:
              homes = Home.objects.filter(property__address__city=city, price__lte=max, property__number_bedroom__lte=bmax)
            else: #min and bmin and bmax None
              homes = Home.objects.filter(property__address__city=city, price__lte=max)
        else: #max and min None
          if bmin is not None:
            if bmax is not None:
              homes = Home.objects.filter(property__address__city=city, property__number_bedroom__gte=bmin,
                                          property__number_bedroom__lte=bmax)
            else: #max and min and bmax None
              homes = Home.objects.filter(property__address__city=city, price__gte=min, price__lte=max, property__number_bedroom__gte=bmin,
                                          property__number_bedroom__lte=bmax)
          else: #max and min and bmin None
            if bmax is not None:
              homes = Home.objects.filter(property__address__city=city, property__number_bedroom__lte=bmax)
            else: # max and min and bmin and bmax None
              homes = Home.objects.filter(property__address__city=city)
    else: #city None
      if min is not None:
        if max is not None:
          if bmin is not None:
            if bmax is not None:
              homes = Home.objects.filter(price__gte=min, price__lte=max, property__number_bedroom__gte=bmin,
                                          property__number_bedroom__lte=bmax)
            else:
              homes = Home.objects.filter(price__gte=min, price__lte=max, property__number_bedroom__gte=bmin)
          else:  # bmin None
            if bmax is not None:
              homes = Home.objects.filter(price__gte=min, price__lte=max, property__number_bedroom__lte=bmax)
            else:
              homes = Home.objects.filter(price__gte=min, price__lte=max)
        else:  # max None
          if bmin is not None:
            if bmax is not None:
              homes = Home.objects.filter(price__gte=min, property__number_bedroom__gte=bmin,
                                          property__number_bedroom__lte=bmax)
            else:
              homes = Home.objects.filter(price__gte=min, property__number_bedroom__gte=bmin)
          else:  # bmin and max None
            if bmax is not None:
              homes = Home.objects.filter(price__gte=min, property__number_bedroom__lte=bmax)
            else:  # max and bmin and bmax None
              homes = Home.objects.filter(price__gte=min)
      else:  # min None
        if max is not None:
          if bmin is not None:
            if bmax is not None:
              homes = Home.objects.filter(price__lte=max, property__number_bedroom__gte=bmin,
                                          property__number_bedroom__lte=bmax)
            else:  # min and bmax None
              homes = Home.objects.filter(price__lte=max, property__number_bedroom__gte=bmin)
          else:  # min and bmin None
            if bmax is not None:
              homes = Home.objects.filter(price__lte=max, property__number_bedroom__lte=bmax)
            else:  # min and bmin and bmax None
              homes = Home.objects.filter(price__lte=max)
        else:  # max and min None
          if bmin is not None:
            if bmax is not None:
              homes = Home.objects.filter(property__number_bedroom__gte=bmin,
                                          property__number_bedroom__lte=bmax)
            else:  # max and min and bmax None
              homes = Home.objects.filter(price__gte=min, price__lte=max, property__number_bedroom__gte=bmin,
                                          property__number_bedroom__lte=bmax)
          else:  # max and min and bmin None
            if bmax is not None:
              homes = Home.objects.filter(property__number_bedroom__lte=bmax)
            else:  # max and min and bmin and bmax None
              homes = Home.objects.all()
              
    serializer = HomeSerializer(homes, many=True)
    return Response(serializer.data)
  
  

class GetHomePerState(APIView):
  """Get home per State params: ?_state_ [PreSale, Active, Pending]"""
  
  permission_classes = [permissions.AllowAny,]
  
  def get(self, request, format=None):
    homes = state = None

    if 'state' in request.query_params:
      state = request.query_params.get('state')
    

    if state is not None:
      homes = Home.objects.filter(state=state)
    else:
      homes = Home.objects.all()
      
    serializer = HomeSerializer(homes, many=True)
    return Response(serializer.data)
