"""myopencv URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from django.conf.urls.static import static

from api.urls import router as api_router

from .settings import MEDIA_ROOT, MEDIA_URL
from django.views.static import serve

urlpatterns = [
    # admin を有効にする
    url(r'^admin/', admin.site.urls),

    # template
    url(r'^template/', include('template.urls', namespace='template')),

    # API
    url(r'^api/', include(api_router.urls)),

    # link: http://stackoverflow.com/questions/34727928/django-1-10-urls-deprecation
    url(r'^data/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT})
]

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

#urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)

