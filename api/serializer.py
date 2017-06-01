# coding: utf-8

from rest_framework import serializers
from template.models import Templates, Images
from .models import Transaction;

from template.services import handler
import os

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


# class TransactionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Transaction
#         #fields = ('id', 'name', 'path', 'rank')
#         fields = '__all__'

class TransactionSerializer(serializers.Serializer):
    # 公開される項目
    id = serializers.IntegerField(required=False)
    name = serializers.CharField(required=True, allow_blank=True, max_length=100)
    src_image = serializers.ImageField(required=True, )
    dest_image = serializers.ImageField(required=False, allow_null=True)
    template_id = serializers.CharField(required=False, )
    type = serializers.CharField(required=False, )

    def create(self, request):
        """
        """

        # テンプレート
        template = Templates.objects.filter(id=request['template_id'])

        # トランザクション
        transaction = Transaction.objects.create(**request);

        #
        #if handler(transaction):
        #    transaction.dest_image = os.path.join("transaction", "result", os.path.basename(transaction.src_image.path));
        #transaction.save();

        try:
            status = handler(transaction, None)
            transaction.dest_image = os.path.join("transaction", "result", os.path.basename(transaction.src_image.path))
            transaction.save()
        except BaseException:
            print(BaseException);

        return transaction


