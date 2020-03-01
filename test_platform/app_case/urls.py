from django.urls import path,include
from django.contrib import admin
from . import views

urlpatterns = [
    #用例管理
    path('case/',views.case_list),
    path('case/case_add/',views.add_case),
    path('case/send_req/',views.send_req),
    path('case/assert_result/',views.assert_result),
    path('case/get_select_data/',views.get_select_data),
    path('case/save_case/',views.save_case),
    path('case/get_case_info/',views.get_case_info),

    path('case_edit/<int:cid>/',views.case_edit),
]