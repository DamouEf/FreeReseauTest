import json
from unittest import result
from django.http import HttpResponse
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializer import MyTokenObtainPairSerializer
# Create your views here.

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
