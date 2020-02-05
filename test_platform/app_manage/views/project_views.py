from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from app_manage.models import Project
from app_manage.forms import ProjectForm
from app_manage.forms import ProjectEditForm
# Create your views here.


@login_required #2
def manage(request):
    """
    这是一个接口管理的视图函数
    :param request:
    :return:
    """
    if request.method == "GET":
        project_list = Project.objects.all()
        user = request.COOKIES.get("user","")
        return render(request, "project/list.html", {
            "projects": project_list,
            "user": user
        })

def add_project(request):
    """
    添加项目
    :param request:
    :return:
    """
    if request.method == "POST":
        try:
            forms = ProjectForm(request.POST)
            if forms.is_valid():
                name = forms.cleaned_data["name"]
                describe = forms.cleaned_data["describe"]
                status = forms.cleaned_data["status"]
                Project.objects.create(name=name,describe=describe,status=status)
            else:
                pass #待日志处理
        except Exception:
            pass #待日志处理
        return HttpResponseRedirect('/manage/')


    else:
        forms = ProjectForm()
        return render(request,"project/add.html",{
            "forms":forms
        })


def edit_project(request,pid):
    if request.method == "POST":
        try:
            forms = ProjectEditForm(request.POST)
            if forms.is_valid():
                name = forms.cleaned_data['name']
                describe = forms.cleaned_data['describe']
                status = forms.cleaned_data['status']
                p = Project.objects.get(id=pid)
                p.name = name
                p.describe = describe
                p.status = status
                p.save()
            else:
                pass #待日志处理
        except Exception:
            pass #带日志处理
        return  HttpResponseRedirect("/manage/")
    else:
        if pid:

            p = Project.objects.get(id=pid)
            forms = ProjectEditForm(instance=p)
        else:
            forms = ProjectEditForm()
        return render(request,"project/edit.html",{
            "forms":forms,
            "pid":pid
        })


def del_project(request,pid):
    """
    删除项目
    :param request:
    :param pid:
    :return:
    """
    if request.method == "GET":
        try:
            if pid:
                p = Project.objects.get(id=pid)
                p.delete()
            else:
                pass
        except Exception:
            pass #添加日志
        return HttpResponseRedirect('/manage/')
    else:
       return HttpResponseRedirect('/manage/')