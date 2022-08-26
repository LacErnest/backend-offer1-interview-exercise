from rest_framework import serializers
from rest_framework_friendly_errors.mixins import FriendlyErrorMessagesMixin

from .models import Address, Item, ListingAgent, Company, Property, Home
from user.models import User
from datetime import date, datetime as dt
from offer1_backend.mixins.get_or_none import get_or_none


class AddressSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):

    class Meta:
      model = Address
      fields = [
          'id',
          'address_line1',
          'address_line2',
          'city',
          'state',
          'zip',
          'created_at',
          'updated_at',
      ]
      read_only_fields = ['id', 'created_at', 'updated_at', ]
      
      
class ItemSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):

    class Meta:
      model = Item
      fields = [
          'id',
          'name',
          'listing',
          'created_at',
          'updated_at',
      ]
      read_only_fields = ['id', 'created_at', 'updated_at', ]
      
      
class ListingAgentSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        many=False, allow_null=True, required=False, queryset=User.objects.all(),  label="User associated")
    
    class Meta:
      model = ListingAgent
      fields = [
          'id',
          'license_number',
          'license_state',
          'user',
          'status',
          'created_at',
          'updated_at',
      ]
      read_only_fields = ['id', 'created_at', 'updated_at', ]
      
      # def to_representation(self, instance):
      #     ret = super().to_representation(instance)

      #     if ret['owner']:
      #         owner = User.objects.get(id=ret['owner'])
      #         ret['owner'] = owner.username

      #     return ret
      
      
class CompanySerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    address = serializers.PrimaryKeyRelatedField(
        many=False, allow_null=True, required=False, queryset=Address.objects.all(),  label="Address associated")

    class Meta:
      model = Company
      fields = [
          'id',
          'name',
          'phone',
          'email',
          'officer_name',
          'address',
          'type',
          'created_at',
          'updated_at',
      ]
      read_only_fields = ['id', 'created_at', 'updated_at', ]

      # def to_representation(self, instance):
      #     ret = super().to_representation(instance)

      #     if ret['owner']:
      #         owner = User.objects.get(id=ret['owner'])
      #         ret['owner'] = owner.username

      #     return ret


class PropertySerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    address = serializers.PrimaryKeyRelatedField(
        many=False, allow_null=True, required=False, queryset=Address.objects.all(),  label="Address associated")
    
    primary_owner = serializers.PrimaryKeyRelatedField(
        many=False, allow_null=True, required=False, queryset=User.objects.all(),  label="Primary Owner associated")

    class Meta:
      model = Property
      fields = [
          'id',
          'address',
          'property_type',
          'square_feet',
          'number_bedroom',
          'number_bath',
          'description',
          'primary_owner',
          'owner_type',
          'primary_image_url',
          'created_at',
          'updated_at',
      ]
      read_only_fields = ['id', 'created_at', 'updated_at', ]

      # def to_representation(self, instance):
      #     ret = super().to_representation(instance)

      #     if ret['owner']:
      #         owner = User.objects.get(id=ret['owner'])
      #         ret['owner'] = owner.username

      #     return ret
      
      
class HomeSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    property = serializers.PrimaryKeyRelatedField(
        many=False, allow_null=True, required=False, queryset=Property.objects.all(),  label="Property associated")

    escrow_company = serializers.PrimaryKeyRelatedField(
        many=False, allow_null=True, required=False, queryset=Company.objects.all(),  label="Escrow Company associated")
    
    title_company = serializers.PrimaryKeyRelatedField(
        many=False, allow_null=True, required=False, queryset=Company.objects.all(),  label="Title Company associated")
    
    listing_agent = serializers.PrimaryKeyRelatedField(
        many=False, allow_null=True, required=False, queryset=ListingAgent.objects.all(),  label="Listing Agent associated")
    
    included_items = serializers.PrimaryKeyRelatedField(
        many=True, allow_null=True, required=False, queryset=Item.objects.all(),  label="Included Items")
    
    excluded_items = serializers.PrimaryKeyRelatedField(
        many=True, allow_null=True, required=False, queryset=Item.objects.all(),  label="Excluded Items")

    class Meta:
      model = Home
      fields = [
          'id',
          'property',
          'state',
          'price',
          'escrow_company',
          'title_company',
          'listing_agent',
          'included_items',
          'excluded_items',
          'created_at',
          'updated_at',
      ]
      read_only_fields = ['id', 'created_at', 'updated_at', ]

      # def to_representation(self, instance):
      #     ret = super().to_representation(instance)

      #     if ret['owner']:
      #         owner = User.objects.get(id=ret['owner'])
      #         ret['owner'] = owner.username

      #     return ret
