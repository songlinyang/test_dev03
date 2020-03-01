import os
import json
from pathlib import Path
from xml.dom.minidom import parse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from app_manage.models import Project
from app_manage.models import Module
from app_case.models import TestCase
from app_task.models import TestResult
from app_task.models import Task
from test_platform.common import Response
from test_platform.logout import info

from .settings import TASK_DATA,TASK_RUN,TASK_RESULT
from app_task.extend.task_threader import TaskThreader
TASK_RESULT = TASK_RESULT.replace("\\","/")
# Create your views here.


def task_list(request):
    if request.method == "GET":
        task_list = Task.objects.all();
        return render(request,"task/list.html",{
            "tasks":task_list
        })


def task_add(request):
    return render(request,"task/add.html")


def task_edit(request,tid):
    return render(request,"task/edit.html")

def case_node(request):
    # 组装用例的树型节点
    if request.method == "GET":
        data = []
        projects = Project.objects.all()
        for p in projects:
            p_dict = {
                "name":p.name,
                "isParent":True
            }
            modules = Module.objects.filter(project_id=p.id)
            modules_list = []
            for m in modules:
                m_dict = {
                    "id":m.id,
                    "name":m.name,
                    "isParent":True
                }
                cases = TestCase.objects.filter(module_id=m.id)
                cases_list = []
                for c in cases:
                    c_dict = {
                        "id":c.id,
                        "name":c.name,
                        "isParent":False
                    }
                    cases_list.append(c_dict)
                m_dict["children"] = cases_list
                modules_list.append(m_dict)
            p_dict["children"] = modules_list
            data.append(p_dict)
        return Response(data=data)

    elif request.method == "POST":
        return Response(code=10405,message="请求方法错误")

def save_task(request):
    if request.method == "POST":
        tid = request.POST.get("tid","")
        name = request.POST.get("name","")
        desc = request.POST.get("desc","")
        cases = request.POST.get("cases","")

        print(type(tid))
        print(name)
        print(desc)
        print(cases)
        if name == "":
            return Response(code=10101,message="任务名称不能为空")

        if cases == "":
            return Response(code=10102, message="所需用例获取失败")

        if tid == "0":

            try:
                Task.objects.create(name=name, desc=desc, status=0, tests=cases)
                info(f"添加用例成功，用例为:{cases}，且status=0状态为未执行")
            except Exception as e:
                print(e)
        else:
            pass
        return Response()




    else:
        return Response(code=10405,message="请求方法错误")


def task_run(request,tid):
    if request.method == "GET":
        task = TaskThreader(tid)
        task.run()
        return HttpResponseRedirect("/task/")


    else:
        return Response(code=10405, message="请求方法错误")


def task_log(request,tid):
    if request.method == "GET":
        results_list = TestResult.objects.filter(task_id=tid)
        return render(request,"task/log_list.html",{
            "results":results_list
        })

def get_log(request):
    if request.method == "POST":
        rid = request.POST.get("rid","")
        if rid == "":
            return Response(10101,"日志ID不能为空")

        result = TestResult.objects.get(id=rid)

        return Response(10200,data=result.result)
