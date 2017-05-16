from django.conf.urls import url
from template import views


urlpatterns = [
    # 書籍
    url(r'^template/$', views.template_list, name='template_list'),   # 一覧
    url(r'^template/create/$', views.template_update, name='template_create'),  # 登録
    url(r'^template/update/(?P<id>\d+)/$', views.template_update, name='template_update'),  # 修正
    url(r'^template/delete/(?P<id>\d+)/$', views.template_delete, name='template_delete'),   # 削除

    #url(r'^template/upload/$', views.image_upload, name='image_upload'),  # アップロード

    url(r'^template/update/(?P<id>\d+)/upload$', views.image_upload, name='image_upload'),  # 修正
    url(r'^image/delete/(?P<id>\d+)/$', views.image_delete, name='image_delete'),  # 削除

]
