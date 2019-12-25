from django.shortcuts import render
from django.http.response import HttpResponse,HttpResponseRedirect
from django.contrib import auth

# Create your views here.

def loginViews(request):
    if request.method == "GET":
        return render(request,"login.html")

    elif request.method == "POST":
        username = request.POST.get("username","")
        password = request.POST.get("password", "")
        if username == "" or password == "":
            print("用户后密码不能为空")





def manageViews(request):
    pass

def logout(request):
    pass
