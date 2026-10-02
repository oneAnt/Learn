from .views import *
from django.urls import path

urlpatterns = [
    path("", index, name="index"),
    path("add", add_task, name="add"),
    path("change/<int:task_id>", change_status, name="change"),
    path("del/<int:task_id>", del_task, name="del")
]
