from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.http import HttpResponse, HttpResponseRedirect

from template.models import Templates, Images
from template.forms import TemplateForm, DocumentForm, ImageForm

from django.views.generic.list import ListView

# Create your views here.
def template_list(request):
    """テンプレート一覧"""
    templates = Templates.objects.all().order_by('id')
    return render(request, 'template/list.html', {'templates': templates})


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
            template = form.save(commit=False)
            template.save();
            return redirect('template:template_list')
    else:
        form = TemplateForm(instance=template)

    return render(request, 'template/update.html', dict(form=form, id=id, images=images))


def template_delete(request, id):
    """テンプレート削除"""
    template = get_object_or_404(Templates, pk=id)
    template.delete()
    return redirect('template:template_list')


def image_upload(request, id):
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

    return render(request, 'template/simple_upload.html', {
        'form': form
    })

#
#
# def file_upload(request):
#     if request.method == 'POST':
#         form = DocumentForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('template:template_list')
#     else:
#         form = DocumentForm()
#
#     return render(request, 'template/simple_upload.html', {
#         'form': form
#     })



# # Create your views here.
# def image_list(request, template_id):
#     """テンプレート一覧"""
#     template = get_object_or_404(Templates, pk=id)
#     images = template.Images.all().order_by('rank')
#     return render(request, 'template/list.html', {'images': images})
#
# def image_update(request, id=None):
#     """イメージ編集"""
#     if id:
#         image = get_object_or_404(Images, pk=id)
#     else:
#         image = Images();
#
#     if request.method == 'POST':
#         form = ImageForm(request.POST, instance=image);
#         if form.is_valid():
#             template = form.save(commit=False)
#             template.save();
#             return redirect('template:image_list')
#     else:
#         form = ImageForm(instance=image)
#
#     return render(request, 'template/image_create.html', dict(form=form, id=id))


# def image_delete(request, id):
#     """イメージ削除"""
#     image = get_object_or_404(Images, pk=id)
#     image.delete()
#     return redirect('template:template_list')
#


# class ImagesList(ListView):
#     context_object_name = 'Images'
#     template_name = 'template/image_list.html'
#
#     def get(self, request, *args, **kwargs):
#         template = get_object_or_404(Templates, pk=kwargs['id'])
#         images = template.impressions.all().order_by('rank')
#         self.object_list = images
#
#         context = self.get_context_data(object_list=self.object_list, template=template)
#         return self.render_to_response(context)


