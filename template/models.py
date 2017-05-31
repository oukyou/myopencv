from django.db import models

# Create your models here.
class Templates(models.Model):
    """テンプレート"""
    id = models.AutoField(primary_key=True)
    name = models.CharField('名前', max_length=255)
    memo = models.CharField('メモ', max_length=255, blank=True)

    def __str__(self):
        return self.name

# python manage.py makemigrations template
# python manage.py migrate
# http://qiita.com/kaki_k/items/ebc8d8b07434e1721756
class Images(models.Model):
    class Meta:
        ordering = ['rank']

    name = models.CharField('画像名', max_length=255, default=None)
    path = models.ImageField('画像ファイル', upload_to='template/')
    rank = models.IntegerField('順位', blank=False, default=1);
    template = models.ForeignKey(Templates, verbose_name='テンプレート名', related_name='Images')

    def __str__(self):
        return self.name;


