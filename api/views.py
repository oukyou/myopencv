from django.shortcuts import render

# Create your views here.
import django_filters
from rest_framework import viewsets, filters

from template.models import Templates, Images
from .serializer import ImageSerializer, TemplateSerializer, TransactionSerializer
from .models import Transaction;

from rest_framework import filters, generics

class TemplateViewSet(viewsets.ModelViewSet):
    authentication_classes = []

    queryset = Templates.objects.all();
    serializer_class = TemplateSerializer;


class ImageViewSet(viewsets.ModelViewSet):
    authentication_classes = []

    queryset = Images.objects.all();
    serializer_class = ImageSerializer;

    def get_queryset(self):
        queryset = Images.objects.all().order_by('rank')
        template = self.request.query_params.get('template', None)
        if template is not None:
            queryset = queryset.filter(template=template)

        return queryset


class TransactionViewSet(viewsets.ModelViewSet):
    authentication_classes = []

    queryset = Transaction.objects.all().order_by('id').reverse();
    serializer_class = TransactionSerializer;
