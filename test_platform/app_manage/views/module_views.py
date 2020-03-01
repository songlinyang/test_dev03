from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from app_manage.models import Project
from app_manage.models import Module
from app_manage.forms import ProjectForm
from app_manage.forms import ProjectEditForm
from app_manage.forms import ModuleForm



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
    if request.method == "POST":
        forms = ModuleForm(request.POST)
        if forms.is_valid():
            project = forms.cleaned_data['project']
            name = forms.cleaned_data['name']
            describe = forms.cleaned_data['describe']
            m = Module.objects.create(project=project, name=name, describe=describe)
            return HttpResponseRedirect('/manage/module/')
        else:
            pass #需处理
    else:
        forms = ModuleForm()
        return render(request,"module/add.html",{
            "forms":forms
        })


def edit_module(request,mid):
    """
    编辑模块
    """
    if request.method == "POST":
        forms = ModuleForm(request.POST)
        if forms.is_valid():
            project = forms.cleaned_data['project']
            name = forms.cleaned_data['name']
            describe = forms.cleaned_data['describe']
            m = Module.objects.get(id=mid)
            m.project = project
            m.name = name
            m.describe = describe
            m.save()
            return HttpResponseRedirect("/manage/module/")
        else:
            print('模块编辑表单数据，有误...')
            return HttpResponseRedirect("/manage/module/")
    else:
        if mid:
            m = Module.objects.get(id=mid)
            forms = ModuleForm(instance=m)
            return render(request,"module/edit.html",{
                "forms":forms,
                "mid":mid
            })
        else:
            pass #跳转处理

def del_module(request,mid):
    """
    删除模块
    """
    if request.method == "GET":
        if mid:
            Module.objects.get(id=mid).delete()
            return HttpResponseRedirect("/manage/module/")
        else:
            pass # 数据处理
    else:
        pass # 数据处理