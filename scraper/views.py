from __future__ import print_function

from rest_framework import viewsets
from rest_framework.decorators import api_view

from scraper.models import Apartment
from .common import main
from .serializers import ApartmentSerializer


@api_view(['GET'])
def run_all(request):
    main()


class ProductRESTView(viewsets.ModelViewSet):
    queryset = Apartment.objects.all()
    serializer_class = ApartmentSerializer
