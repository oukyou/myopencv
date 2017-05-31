from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.http import HttpResponse, HttpResponseRedirect

from template.models import Templates, Images
from template.forms import TemplateForm, ImageForm, TransactionForm

from api.models import Transaction

from django.views.generic.list import ListView
from myopencv.settings import WEBROOT
from template.services import handler
from template.services import handler_surf

from django.db import transaction
from django.contrib import messages
from api.models import TYPE_CHOICES

import cv2
import os

# Create your views here.

#===========================================
# Template
#===========================================
def template_list(request):
    """テンプレート一覧"""
    templates = Templates.objects.all().order_by('id')
    if len(templates) == 0:
        messages.info(request, 'テンプレートが登録されていません。')

    return render(request, 'template/list.html', {'templates': templates})

@transaction.atomic
def template_update(request, id=None):
    """テンプレート編集"""
    if id:
        template = get_object_or_404(Templates, pk=id)
        images = template.Images.all().order_by('rank')
        if len(images) == 0:
            messages.info(request, 'テンプレート画像が登録されていません。')
    else:
        template = Templates();
        images = [];

    if request.method == 'POST':
        form = TemplateForm(request.POST, instance=template);
        if form.is_valid():
            ranks = request.POST.getlist('rank')
            names = request.POST.getlist('image_name')
            ids = request.POST.getlist('id')
            for index, value in enumerate(ids):
                img = get_object_or_404(Images, pk=value)
                img.rank = ranks[index]
                img.name = names[index]
                img.save();

            template = form.save()
            template.save();
            if id:
                messages.info(request, 'テンプレートを更新しました。')
            else:
                messages.info(request, 'テンプレートを登録しました。')
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
    messages.info(request, 'テンプレートを削除しました。')
    return redirect('template:template_list')

def image_delete(request, id):
    """テンプレート削除"""
    image = get_object_or_404(Images, pk=id)
    template_id = image.template_id
    image.delete()
    messages.info(request, 'テンプレート画像を削除しました。')
    return redirect('template:template_update', id=template_id)


def image_upload(request, id):
    template = get_object_or_404(Templates, pk=id)

    """イメージアップロード"""
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.info(request, 'テンプレート画像を登録しました。')
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

#===========================================
# Transation
#===========================================
def transaction_list(request):
    """テンプレート履歴一覧"""
    transactions = Transaction.objects.all().order_by('id').reverse()
    if len(transactions) == 0:
        messages.info(request, 'テンプレートマッチング結果がありません。')
    return render(request, 'transaction/list.html', {'transactions': transactions, 'types': TYPE_CHOICES})


def transaction_create(request):
    """マーチング実施"""
    transaction = Transaction();

    if request.method == 'POST':
        form = TransactionForm(request.POST, request.FILES, instance=transaction);
        if form.is_valid():
            transaction = form.save()

            if transaction.type == '1' :
                # 特徴量マッチング処理
                try:
                    status = handler_surf(transaction,request)
                    transaction.dest_image = os.path.join("transaction", "result", os.path.basename(transaction.src_image.path))
                    transaction.save()
                    if status:
                        messages.info(request, '特徴量マッチング処理が正常に終了しました。')
                except:
                    messages.error(request, '特徴量マッチング処理が失敗しました。')
                    return render(request, 'transaction/create.html', dict(form=form))
            else:
                # テンプレートマッチング処理
                try:
                    status = handler(transaction,request)
                    transaction.dest_image = os.path.join("transaction", "result", os.path.basename(transaction.src_image.path))
                    transaction.save()
                    if status:
                        messages.info(request, 'テンプレートマッチング処理が正常に終了しました。')
                except:
                    messages.error(request, 'テンプレートマッチング処理が失敗しました。')
                    return render(request, 'transaction/create.html', dict(form=form))

            return redirect('template:transaction_list')
    else:
        form = TransactionForm(instance=transaction)

    return render(request, 'transaction/create.html', dict(form=form))


