from django.contrib import admin

# Register your models here.
from django.contrib import admin
from template.models import Templates

#admin.site.register(Templates)

class TemplatesAdmin(admin.ModelAdmin):
    list_display = ('name', 'memo')  # 一覧に出したい項目
    list_display_links = ('name',)  # 修正リンクでクリックできる項目
admin.site.register(Templates, TemplatesAdmin)

