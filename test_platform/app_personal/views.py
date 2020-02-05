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
               "error":"用户名或密码为空!"
           })

        user = auth.authenticate(username=username,password=password)
        print("用户信息>>>:",user)

        if user is not None:
            auth.login(request,user) #记录用户的登陆状态 1

            response = HttpResponseRedirect("/manage/project/")
            response.set_cookie('user',username,3600) #设置Cookies过时时间，同时Cookies中记录username
            return response
        else:
            return render(request,"login.html",{
                "error":"用户名或密码错误!"
            })


@login_required
def logout(request):
    # 退出，清空掉session
    auth.logout(request)
    return HttpResponseRedirect("/login/")
