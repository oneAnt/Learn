import datetime

from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from .models import Task


# Create your views here.
@transaction.atomic
def index(request):
    """
    默认页面
    :param request:
    :return: render
    """
    today = datetime.date.today()
    tasks = Task.objects.filter(created_at__year=today.year,
                                created_at__month=today.month,
                                created_at__day=today.day)
    print(tasks)
    return render(request, "index.html", {"tasks": tasks})

@transaction.atomic
def add_task(request):
    """
    添加任务
    :param request:
    :return: redirect
    """
    if request.method == "POST":
        task_title = request.POST.get("task").strip()
        if task_title:
            # 创建任务
            task = Task.objects.create(title=task_title)
            print(task)
        else:
            messages.warning(request, "请输入内容！")
    return redirect("index")

@transaction.atomic
def change_status(request, task_id):
    """
    修改任务状态
    :param request:
    :param task_id:
    :return: JsonResponse
    """
    task = get_object_or_404(Task, id=task_id)
    task.status = not task.status
    task.save()
    return JsonResponse({"status": task.status})

@transaction.atomic
def del_task(request, task_id):
    """
    删除任务
    :param request:
    :param task_id:
    :return: redirect
    """
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect("index")
