from django.contrib import admin

# Register your models here.
from django.contrib import admin
from template.models import Templates, Images

#admin.site.register(Templates)
#admin.site.register(Images)


class TemplatesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'memo')  # 一覧に出したい項目
    list_display_links = ('id',)  # 修正リンクでクリックできる項目


class ImagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'custom_path', 'rank', 'template', )  # 一覧に出したい項目
    list_display_links = ('id',)  # 修正リンクでクリックできる項目

    def custom_path(self, obj):
        return '<img src="{url}"/ width="50px" height="50px">'.format(url=obj.path);
    custom_path.short_description = u'画像'
    custom_path.allow_tags = True  # htmlタグ許可


admin.site.register(Templates, TemplatesAdmin)
admin.site.register(Images, ImagesAdmin)

# title/header変更
admin.site.site_header = 'OpenCVテンプレート管理'
admin.site.site_title = 'OpenCV'