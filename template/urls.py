from django.conf.urls import url
from template import views


urlpatterns = [
    # テンプレート
    url(r'^$', views.template_list, name='template_list'),  # 一覧
    url(r'^create/$', views.template_update, name='template_create'),  # 登録
    url(r'^update/(?P<id>\d+)/$', views.template_update, name='template_update'),  # 修正
    url(r'^delete/(?P<id>\d+)/$', views.template_delete, name='template_delete'),  # 削除

    # 画像
    url(r'^update/(?P<id>\d+)/upload$', views.image_upload, name='image_upload'),  # 修正
    url(r'^image/delete/(?P<id>\d+)/$', views.image_delete, name='image_delete'),  # 削除

    #
    url(r'^transaction$', views.transaction_list, name='transaction_list'),  # 一覧
    url(r'^transaction/create/$', views.transaction_create, name='transaction_create'),  # 登録

]
