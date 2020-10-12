from __future__ import print_function

from django.contrib.auth import get_user_model
from rest_framework import viewsets

from scraper.models import Apartment
from .serializers import ApartmentSerializer

User = get_user_model()

class ProductRESTView(viewsets.ModelViewSet):
    queryset = Apartment.objects.all()
    serializer_class = ApartmentSerializer

