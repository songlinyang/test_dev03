from django.shortcuts import render
import requests
import json
from django.http import JsonResponse
from app_manage.models import Project
from app_manage.models import Module
from app_case.models import TestCase
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.forms.models import model_to_dict

# Create your views here.

def case_list(request):

    if request.method == "GET":
        cases = TestCase.objects.all()
        p = Paginator(cases,2) #默认2条数据进行分页
        page = request.GET.get("page","")
        if page == "":
            page = 1

        try:
            page_cases = p.page(page)
        except EmptyPage:
            page_cases = p.page(p.num_pages)
        except PageNotAnInteger:
            page_cases = p.page(1)

        return render(request, "case/list.html",{
            "cases":page_cases
        })

def add_case(request):
    """
    创建用例
    """
    return render(request, "case/add.html")

def case_edit(request,cid):
    """
    编辑用例
    """
    if request.method == "GET":
        if cid:
            return render(request, "case/edit.html")

def send_req(request):
    """
    处理发送过来的用例请求
    """
    if request.method == "GET":
        req_url = request.GET.get("req_url","")
        req_method = request.GET.get("req_method","")
        req_headers= request.GET.get("req_headers","")
        req_type = request.GET.get("req_type","")
        req_body = request.GET.get("req_body","")

        print("req_url",req_url,type(req_url))
        print("req_method",req_method,type(req_method))
        print("req_headers",req_headers,type(req_headers))
        print("req_type",req_type,type(req_type))
        print("req_body",req_body,type(req_body))

        if req_url == "":
            return JsonResponse({"code":10101,"message":"URL不能为空"})

        # str转成dict对象
        try:
            header = json.loads(req_headers)
        except json.decoder.JSONDecodeError:
            return JsonResponse({"code": 10102, "message": "Header格式错误，必须是标准的JSON格式！"})
        try:
            pay_load = json.loads(req_body)
        except json.decoder.JSONDecodeError:
            return JsonResponse({"code": 10103, "message": "参数格式错误，必须是标准的JSON格式！"})

        rsp = {}
        try:
            if req_method == "get":
                rsp = requests.get(url=req_url,headers=header,params=pay_load)

            elif req_method == "post":
                if req_type == "form":
                    rsp = requests.post(url=req_url,headers=header,data=pay_load)

                elif req_type == "json":
                    rsp = requests.post(url=req_url,headers=header,json=pay_load)
        except Exception as e:
            return JsonResponse({"code":10101,"message":e})

        if rsp:
            return JsonResponse({"code": 10200, "message": "success", "data": rsp.text})
        else:
            return JsonResponse({"code": 10101, "message":"响应失败"})

def assert_result(request):
    """
    处理发送过来的断言请求
    """
    if request.method == "POST":
        result_text = request.POST.get("result_text","")
        assert_text = request.POST.get("assert_text","")
        assert_type = request.POST.get("assert_type","")

        print("result_text",result_text,type(result_text))
        print("assert_text",assert_text,type(assert_text))
        print("assert_type",assert_type,type(assert_type))

        # 此处有学习的总结点：前端做得校验属于弱验证，所以后端也需要做接口强验证
        if result_text == "" or assert_text == "":
            return JsonResponse({"code":10101,"message":"断言的参数不能为空"})

        if assert_type != "include" and assert_type !="equal":
            return JsonResponse({"code":10102,"message":"断言类型错误"})


        if assert_type == "include":
            if assert_text in result_text:
                return JsonResponse({"code":10200,"message":"断言包含成功"})
            else:
                return JsonResponse({"code":10200,"message":"断言包含失败"})

        if assert_type == "equal":
            if assert_text == result_text:
                return JsonResponse({"code": 10200, "message": "断言相等成功"})
            else:
                return JsonResponse({"code": 10200, "message": "断言相等失败"})
        return JsonResponse({"code":10201,"message":"系统开小差了，请联系开发小朋友."})


def get_select_data(request):
    """
    获取下拉选项的值
    """
    if request.method == "GET":
        projects = Project.objects.all()
        data_list = []
        for p in projects:
           module_list = []
           p_dict = {
               "id":int(p.id),
               "name":p.name
           }
           modules = Module.objects.filter(project=p)
           for m in modules:
               m_dict = {
                   "id": int(m.id),
                   "name": m.name
               }
               module_list.append(m_dict)
           p_dict["moduleList"] = module_list
           data_list.append(p_dict)
        return JsonResponse({"code":10200,"data":data_list})

def get_case_info(request):
    if request.method == "POST":
        cid = request.POST.get("cid","")
        if cid:
            case = TestCase.objects.get(id=cid)
            case_dict = model_to_dict(case)
            module = Module.objects.get(id=case.module_id)
            project = Project.objects.get(module=module)
            case_dict["project"]=project.id
            return JsonResponse({"code":10200,"message":"success","data":case_dict})
        else:
            return JsonResponse({"code":10101,"message":"请求参数错误"})


def save_case(request):
    """
    保存用例
    """
    if request.method == "POST":
        name = request.POST.get("name","")
        url = request.POST.get("url","")
        method = request.POST.get("method","")
        header = request.POST.get("header","")
        paramter_type = request.POST.get("paramter_type","")
        paramter_body = request.POST.get("paramter_body","")
        result = request.POST.get("result","")
        assert_type = request.POST.get("assert_type","")
        assert_text = request.POST.get("assert_text","")
        module_id = request.POST.get("module_id","")
        case_id = request.POST.get("case_id","")


        if method == "post":
            method_int = 2
        elif method == "get":
            method_int = 1
        else:
            return JsonResponse({"code": 10101, "message": "接口请求方法不正确"})

        if paramter_type == "form":
            paramter_type_int = 1
        elif paramter_type == "json":
            paramter_type_int = 2
        else:
            return JsonResponse({"code": 10101, "message": "接口参数类型不正确"})

        if assert_type == "include":
            assert_type_int = 1
        elif assert_type == "equal":
            assert_type_int = 2
        else:
            return JsonResponse({"code": 10101, "message": "接口断言方法不正确"})
        if case_id == "":
            print("创建")
            try:
                TestCase.objects.create(
                    name = name,
                    url = url,
                    method = method_int,
                    header = header,
                    paramter_type = paramter_type_int,
                    paramter_body = paramter_body,
                    result=result,
                    assert_type=assert_type_int,
                    assert_text=assert_text,
                    module_id=module_id
                )
                return JsonResponse({"code": 10200, "message": "创建成功"})
            except Exception as e:
                return JsonResponse({"code": 10500, "message": "服务器异常","error":e})
        else:
            print("更新")
            try:
                update_case = TestCase.objects.get(id=case_id)
                update_case.name = name
                update_case.url = url
                update_case.method = method_int
                update_case.header = header
                update_case.paramter_type = paramter_type_int
                update_case.paramter_body = paramter_body
                update_case.result = result
                update_case.assert_type = assert_type_int
                update_case.assert_text = assert_text
                update_case.module_id = module_id
                update_case.save()
                return JsonResponse({"code":10200,"message":"更新成功"})
            except Exception as e:
                return JsonResponse({"code":10500,"message":"服务器异常","error":e})
    else:
        return JsonResponse({"code":10101,"message":"请求方式有误，请重试"})