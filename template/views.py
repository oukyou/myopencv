from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.http import HttpResponse, HttpResponseRedirect

from template.models import Templates, Images
from template.forms import TemplateForm, ImageForm

from django.views.generic.list import ListView
from myopencv.settings import WEBROOT

from django.db import transaction


# Create your views here.
def template_list(request):
    """テンプレート一覧"""
    templates = Templates.objects.all().order_by('id')
    return render(request, 'template/list.html', {'templates': templates})

@transaction.atomic
def template_update(request, id=None):
    """テンプレート編集"""
    if id:
        template = get_object_or_404(Templates, pk=id)
        images = template.Images.all().order_by('rank')
    else:
        template = Templates();
        images = [];

    if request.method == 'POST':
        form = TemplateForm(request.POST, instance=template);
        if form.is_valid():
            ranks = request.POST.getlist('rank')
            ids = request.POST.getlist('id')
            for index, value in enumerate(ids):
                img = get_object_or_404(Images, pk=value)
                img.rank = ranks[index]
                img.save();

            template = form.save()
            template.save();

            return redirect('template:template_list')
    else:
        form = TemplateForm(instance=template)

    return render(request, 'template/update.html', dict(
            form=form, id=id, images=images, webroot = WEBROOT
        ))


def template_delete(request, id):
    """テンプレート削除"""
    template = get_object_or_404(Templates, pk=id)
    template.delete()
    return redirect('template:template_list')

def image_delete(request, id):
    """テンプレート削除"""
    image = get_object_or_404(Images, pk=id)
    template_id = image.template_id
    image.delete()
    return redirect('template:template_update', id=template_id)


def image_upload(request, id):
    template = get_object_or_404(Templates, pk=id)

    """イメージアップロード"""
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('template:template_update', id=id)
    else:
        # http://stackoverflow.com/questions/813418/django-set-field-value-after-a-form-is-initialized
        #form  = ImageForm(initial = {'template': get_object_or_404(Templates, pk=id)})

        form = ImageForm()
        form.fields["template"].initial = get_object_or_404(Templates, pk=id);

    return render(request, 'template/upload.html', {
        'form': form,
        'template': template
    })

