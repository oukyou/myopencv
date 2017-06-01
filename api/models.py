from django.db import models

from template.models import Templates
from datetime import datetime

TYPE_CHOICES = (
    ('', '---------'),
    ('0','テンプレートマッチング'),
    ('1', '特徴量マッチング')
)

# Create your models here.
class Transaction(models.Model):

    name = models.CharField('名前', max_length=255, default=None)
    src_image = models.ImageField('画像ファイル', upload_to='transaction/')
    template = models.ForeignKey(Templates, verbose_name='テンプレート名', related_name='Template')

    dest_image = models.ImageField('結果画像', upload_to='result/', max_length=255, null=True, default=None)
    create_time = models.DateTimeField(auto_now_add=True, blank=True)
    update_time = models.DateTimeField(auto_now_add=True, blank=True)

    type = models.CharField("マーチングタイプ", max_length=1, choices=TYPE_CHOICES, default='0', null=False)

    def __str__(self):
        return self;


class TypeField(models.Field):
    def db_type(self):
        return 'mytype'
