from django.shortcuts import render
from django.http.response import HttpResponse,HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required

# Create your views here.

def loginViews(request):
    if request.method == "GET":
        return render(request,"login.html")

    elif request.method == "POST":
        username = request.POST.get("username","")
        password = request.POST.get("password", "")
        if username == "" or password == "":
           return render(request,"login.html",{
               " ":"用户名或密码为空!"
           })

        user = auth.authenticate(username=username,password=password)
        print("用户信息>>>:",user)

        if user is not None:
            auth.login(request,user) #记录用户的登陆状态 1
            return HttpResponseRedirect("/manage/")
        else:
            return render(request,"login.html",{
                "error":"用户名或密码错误!"
            })

@login_required #2
def manage(request):
    """
    这是一个接口管理的视图函数
    :param request: 
    :return: 
    """
    return render(request, "manage.html")



def logout(request):
    pass
