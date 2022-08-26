from django.db import models
from djmoney.models.fields import MoneyField


TITLE = 'TITLE'
ESCROW = 'ESCROW'
TYPE_CHOICES = (
    (TITLE, 'Title'),
    (ESCROW, 'Escrow')
)


INDIVIDUAL = 'INDIVIDUAL'
FAMILY = 'FAMILY'
OWNER_TYPE_CHOICES = (
    (INDIVIDUAL, 'Individual'),
    (FAMILY, 'Family')
)

SINGLE = 'SINGLE'
GROUP = 'GROUP'
PROPERTY_TYPE_CHOICES = (
    (SINGLE, 'SingleFamilyHome'),
    (GROUP, 'GroupHome')
)


PRESALE = 'PRESALE'
ACTIVE = 'ACTIVE'
PENDING = 'PENDING'
STATE_CHOICES = (
    (PRESALE, 'PreSale'),
    (ACTIVE, 'Active'),
    (PENDING, 'Pending'),
)

class Address(models.Model):
  address_line1 = models.CharField(max_length=100, blank=True,
                            null=True)
  address_line2 = models.CharField(max_length=100, blank=True,
                                   null=True)
  city = models.CharField(max_length=100, blank=True,
                                   null=True)
  state = models.CharField(max_length=100, blank=True,
                                   null=True)
  zip = models.CharField(max_length=10, blank=True,
                                   null=True)
  
  updated_at = models.DateTimeField(auto_now=True, editable=False)
  created_at = models.DateTimeField(auto_now_add=True, editable=False)

  class Meta:
      verbose_name_plural = "Addresses"
      ordering = ['-created_at']

  def __str__(self):
      return self.address_line1
    
    
class Item(models.Model):
  name = models.CharField(max_length=100, blank=True,
                                   null=True)
  listing = models.CharField(max_length=100, blank=True,
                                   null=True)
  
  updated_at = models.DateTimeField(auto_now=True, editable=False)
  created_at = models.DateTimeField(auto_now_add=True, editable=False)

  class Meta:
      verbose_name_plural = "Items"
      ordering = ['-created_at']
  

  def __str__(self):
      return self.name


class ListingAgent(models.Model):
  license_number = models.CharField(max_length=100, blank=True,
                                   null=True)
  
  license_state = models.CharField(max_length=100, blank=True, null=True)
  
  user = models.ForeignKey(
      'user.User', on_delete=models.CASCADE, related_name="listing_agents")
  
  status = models.CharField(max_length=10, blank=True,
                            null=True, default="Active")
  
  updated_at = models.DateTimeField(auto_now=True, editable=False)
  created_at = models.DateTimeField(auto_now_add=True, editable=False)

  class Meta:
      verbose_name_plural = "ListingAgents"
      ordering = ['-created_at']
  

class Company(models.Model):
  name = models.CharField(max_length=255, blank=True, null=True)
  phone = models.CharField(max_length=255, blank=True, null=True)
  email = models.CharField(max_length=255, blank=True, null=True)
  officer_name = models.CharField(max_length=255, blank=True, null=True)
  address = models.ForeignKey(
      'housing.Address', on_delete=models.CASCADE, related_name="companies")
  type = models.CharField(choices=TYPE_CHOICES,
                          max_length=20, default=TITLE)
  
  updated_at = models.DateTimeField(auto_now=True, editable=False)
  created_at = models.DateTimeField(auto_now_add=True, editable=False)

  class Meta:
      verbose_name_plural = "Companies"
      ordering = ['-created_at']
      
      
class Property(models.Model):
  address = models.ForeignKey(
      'housing.Address', on_delete=models.CASCADE, related_name="properties")
  property_type = models.CharField(choices=PROPERTY_TYPE_CHOICES,
                          max_length=20, default=SINGLE)
  square_feet = models.FloatField(default=0)
  number_bedroom = models.IntegerField(default=0)
  number_bath = models.IntegerField(default=0)
  description = models.TextField(null=True, blank=True)
  primary_owner = models.ForeignKey(
      'user.User', on_delete=models.CASCADE, related_name="properties")
  owner_type = models.CharField(choices=OWNER_TYPE_CHOICES,
                                   max_length=20, default=INDIVIDUAL)
  
  primary_image_url = models.ImageField(null=True, upload_to="uploads/",
                                                verbose_name="Property Image")
  
  updated_at = models.DateTimeField(auto_now=True, editable=False)
  created_at = models.DateTimeField(auto_now_add=True, editable=False)

  class Meta:
      verbose_name_plural = "Properties"
      ordering = ['-created_at']
      
      
      
class Home(models.Model):
  property = models.ForeignKey(
      'housing.Property', on_delete=models.CASCADE, related_name="homes")
  
  state = models.CharField(choices=STATE_CHOICES,
                                   max_length=20, default=PENDING)
  price = MoneyField(max_digits=15, decimal_places=2,
                               default_currency='USD', null=True, default=0)
  
  escrow_company = models.ForeignKey(
      'housing.Company', on_delete=models.CASCADE, related_name="escrow_homes")
  
  title_company = models.ForeignKey(
      'housing.Company', on_delete=models.CASCADE, related_name="title_homes")
  
  listing_agent = models.ForeignKey(
      'housing.ListingAgent', on_delete=models.CASCADE, related_name="homes")
  
  included_items = models.ManyToManyField('housing.Item', related_name="included_items_homes", blank=True)
  
  excluded_items = models.ManyToManyField('housing.Item', related_name="excluded_items_homes", blank=True)
  
  updated_at = models.DateTimeField(auto_now=True, editable=False)
  created_at = models.DateTimeField(auto_now_add=True, editable=False)

  class Meta:
      verbose_name_plural = "Homes"
      ordering = ['-created_at']
