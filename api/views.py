from django.shortcuts import render

# Create your views here.
import django_filters
from rest_framework import viewsets, filters

from template.models import Templates, Images
from .serializer import ImageSerializer, TemplateSerializer, TransactionSerializer
from .models import Transaction;


class TemplateViewSet(viewsets.ModelViewSet):
    queryset = Templates.objects.all();
    serializer_class = TemplateSerializer;

class ImageViewSet(viewsets.ModelViewSet):
    queryset = Images.objects.all();
    serializer_class = ImageSerializer;

class TransactionViewSet(viewsets.ModelViewSet):
    authentication_classes = []

    queryset = Transaction.objects.all();
    serializer_class = TransactionSerializer;



