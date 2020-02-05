from django.urls import path,include
from django.contrib import admin
from app_manage.views import project_views
from app_manage.views import module_views

urlpatterns = [
    #默认项目管理
    path('',project_views.manage),

    #项目管理

    path('project/',project_views.manage),
    path('project_add/',project_views.add_project),
    path('project_edit/<int:pid>/',project_views.edit_project),
    path('project_del/<int:pid>/',project_views.del_project),

    #模块管理
    path('module/',module_views.manage),
    path('module_add/',module_views.add_module),
    path('module_edit/<int:mid>',module_views.edit_module),
    path('module_del/<int:mid>',module_views.del_module),
]