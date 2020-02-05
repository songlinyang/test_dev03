from django.contrib import admin

# Register your models here.
from django.contrib import admin
from app_manage.models import Project
from app_manage.models import Module


#自带管理平台 自定义
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name','status','describe',] #显示字段
    search_fields = ['name',] #搜索栏
    list_filter = ['status',] #筛选栏

class ModuleAdmin(admin.ModelAdmin):
    list_display = ['project','name','describe','create_time'] #显示字段
    search_fields =  ['name']
    list_filter = ['project']


#注册
admin.site.register(Project,ProjectAdmin)
admin.site.register(Module,ModuleAdmin)