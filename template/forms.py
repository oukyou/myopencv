from django import forms
from django.forms import ModelForm
from template.models import Templates,Images
from api.models import Transaction

class TemplateForm(ModelForm):
    """テンプレートフォーム"""
    class Meta:
        model = Templates
        fields = ('name', 'memo',)

class ImageForm(forms.ModelForm):
    class Meta:
        model = Images
        fields = ('name', 'path', 'rank', 'template', )

class TransactionForm(ModelForm):
    """テンプレートフォーム"""
    class Meta:
        model = Transaction
        fields = ('name', 'src_image', 'template', 'type')

