from django.db import models

# Create your models here.
class Templates(models.Model):
    """テンプレート"""
    id = models.AutoField(primary_key=True)
    name = models.CharField('名前', max_length=255)
    memo = models.CharField('メモ', max_length=255, blank=True)

    #create_time = models.DateField('登録日付')
    #update_time = models.DateField('更新日付')

    def __str__(self):
        return self.name


# python manage.py makemigrations template
# python manage.py migrate
# http://qiita.com/kaki_k/items/ebc8d8b07434e1721756
class Images(models.Model):
    #id = models.AutoField(primary_key=True)
    #name = models.CharField('画像名', max_length=255)
    path = models.FileField(upload_to='data/')
    rank = models.IntegerField('順位', blank=False, default=0);
    #uploaded_at = models.DateTimeField(auto_now_add=True)

    template = models.ForeignKey(Templates, verbose_name='テンプレート名', related_name='Images')

    def __str__(self):
        return self.name;

class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)



