# coding: utf-8

from rest_framework import serializers

from template.models import Templates, Images
from .models import Transaction;

class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Templates
        #fields = ('id', 'name', 'memo')
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        #fields = ('id', 'name', 'path', 'rank')
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        #fields = ('id', 'name', 'path', 'rank')
        fields = '__all__'
