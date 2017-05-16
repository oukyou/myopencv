from django import forms
from django.forms import ModelForm
from template.models import Templates,Images, Document

# class TemplateForm(ModelForm):
#     """テンプレートフォーム"""
#     class Meta:
#         model = Templates
#         fields = ('name', 'memo',)

class TemplateForm(ModelForm):
    """テンプレートフォーム"""
    class Meta:
        model = Templates
        fields = ('name', 'memo',)

class ImageForm(forms.ModelForm):
    class Meta:
        model = Images
        fields = ('rank', 'path', 'template')

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('description', 'document', )

