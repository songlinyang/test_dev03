from django.urls import path,include
from . import  views


urlpatterns = [
    path('',views.loginViews),
    path('login/',views.loginViews),
    path('manage/',views.manage),
    path('logout/',views.logout),

]