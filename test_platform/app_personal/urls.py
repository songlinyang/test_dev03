from django.urls import path,include
from . import  views

appname="manage"

urlpatterns = [
    path('',views.manageViews),
    path('logout/',views.logout),
]