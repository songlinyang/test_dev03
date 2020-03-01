from django.urls import path,include
from . import views

urlpatterns = [
    path("",views.task_list),
    path("task_add/",views.task_add),
    path("task_edit/<int:tid>",views.task_edit),
   # path("task_edit/",views.task_edit),


    path("case_node/",views.case_node),
    path("save_task/",views.save_task),
    path("task_run/<int:tid>/",views.task_run),
    path("task_log/<int:tid>/",views.task_log),
    path("get_log/",views.get_log),
]
