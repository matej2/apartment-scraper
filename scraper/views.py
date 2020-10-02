from __future__ import print_function

from rest_framework import viewsets

from scraper.models import Apartment
from .serializers import ApartmentSerializer


class ProductRESTView(viewsets.ModelViewSet):
    queryset = Apartment.objects.all()
    serializer_class = ApartmentSerializer
