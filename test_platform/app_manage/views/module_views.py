from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from app_manage.models import Project
from app_manage.models import Module
from app_manage.forms import ProjectForm
from app_manage.forms import ProjectEditForm



@login_required #2
def manage(request):
    """
    模块列表管理视图
    """
    if request.method == "GET":
        module_list = Module.objects.all()
        return render(request, "module/list.html", {
            "modules": module_list,
        })


def add_module(request):
    """
    创建模块
    """
    pass

def edit_module(request,mid):
    """
    编辑模块
    """
    pass

def del_module(request,mid):
    """
    删除模块
    """
    pass